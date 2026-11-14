"""
Claude Code invocation for the agentic validator.

Per quest the runner:
  1. Creates a disposable sandbox dir and drops the quest body in as QUEST.md
     (so the agent sees ONLY the quest, never the repo).
  2. Builds and runs ``claude -p ... --output-format json`` with the right tool
     allow/deny list for the mode (review = no Bash; execute = sandboxed Bash).
  3. Parses the result envelope, extracts the JSON verdict (schema-constrained
     output, with a fenced-block fallback), normalizes it, and scores it.

Auth is delegated to the ``claude`` CLI itself: locally it uses your logged-in
OAuth session; in CI set ``CLAUDE_CODE_OAUTH_TOKEN`` (from ``claude setup-token``).
When the job env carries BOTH ``CLAUDE_CODE_OAUTH_TOKEN`` and ``ANTHROPIC_API_KEY``,
the CLI on its own would pick the API key (it outranks the OAuth token), so the
runner hands each credential to the CLI alone, OAuth first: a refused OAuth token
falls back to the API key, never the other way round unless
``QUEST_QA_AUTH_ORDER`` / ``AI_AUTH_ORDER`` says so (the fleet ``claude-run``
contract — see ``auth_order``).

``mock=True`` returns a deterministic synthetic verdict (no CLI, no cost) so the
whole pipeline can be exercised offline. ``dry_run=True`` returns the exact
command + prompts without invoking anything.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import List, Optional

from . import prompts, schema

# Shared deterministic snippet extractor (single source of truth for "runnable
# snippet"), used to report how much of the quest's code the agent actually ran.
_QUEST_DIR = Path(__file__).resolve().parents[3] / "scripts" / "quest"
if str(_QUEST_DIR) not in sys.path:
    sys.path.insert(0, str(_QUEST_DIR))
try:
    import quest_lib  # noqa: E402
except Exception:  # pragma: no cover
    quest_lib = None

_FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)

AUTH_HINT = (
    "Claude could not authenticate. The agentic validator delegates auth to the "
    "`claude` CLI, so set up ONE of:\n"
    "  • Local: run `claude login` (or `claude setup-token`) so credentials live in ~/.claude.\n"
    "  • CI / headless: export CLAUDE_CODE_OAUTH_TOKEN=$(claude setup-token) as a secret.\n"
    "Note: inside a managed/sandboxed agent session, host-managed auth is NOT passed to child\n"
    "`claude` processes — run this validator from a normal shell or a CI runner with the token set."
)

THROTTLE_HINT = (
    "Claude's backend stayed unavailable (rate-limit / overload / transient 5xx) across every "
    "retry. This is almost always temporary — the OAuth token is shared across the slice sweep "
    "and its rate limit refills over time, so the loop retries this slice on its next run."
)


# Credential methods, the env var each one lives in, and what a human does when
# that credential is refused. Same names as the fleet's claude-run runner.
_CRED_VARS = {"oauth": "CLAUDE_CODE_OAUTH_TOKEN", "api_key": "ANTHROPIC_API_KEY"}
_DEFAULT_AUTH_ORDER = "oauth,api_key"
_FIX_HINT = {
    ("oauth", "auth"): "mint a fresh token with `claude setup-token` and update the "
                       "CLAUDE_CODE_OAUTH_TOKEN repo secret",
    ("oauth", "quota"): "the subscription's usage window is spent — it refills on its own",
    ("api_key", "auth"): "the ANTHROPIC_API_KEY was rejected (revoked key or empty credit "
                         "balance) — fix it in the Anthropic console or delete the secret",
    ("api_key", "quota"): "the API key hit its rate or spend limit — raise it in the "
                          "Anthropic console",
}
_SECRET_RE = re.compile(r"sk-ant-[A-Za-z0-9_-]{8,}")


def auth_order(environ=None) -> List[str]:
    """The credential methods to try, in order, keeping only those whose secret is
    actually present. ``QUEST_QA_AUTH_ORDER`` (or the fleet-wide ``AI_AUTH_ORDER``)
    overrides the default ``oauth,api_key``. An unset GitHub secret renders as an
    empty string, so blank values count as absent. ``[]`` means no credential is
    in the environment: the CLI's own stored login is used (a human running
    locally)."""
    env = os.environ if environ is None else environ
    raw = (env.get("QUEST_QA_AUTH_ORDER") or env.get("AI_AUTH_ORDER")
           or _DEFAULT_AUTH_ORDER)
    out: List[str] = []
    for method in re.split(r"[,\s]+", raw.strip()):
        var = _CRED_VARS.get(method)
        if var and (env.get(var) or "").strip() and method not in out:
            out.append(method)
    return out


def child_env(method: str, environ=None) -> dict:
    """The environment for ONE ``claude`` call that may use only ``method``'s
    credential. The other credential is removed, not just de-prioritised: with
    both present the CLI prefers ANTHROPIC_API_KEY, which is how a dead API key
    silently shadowed a healthy OAuth token here for weeks. ``ambient`` strips
    both, leaving the CLI's stored login."""
    env = dict(os.environ if environ is None else environ)
    env.setdefault("CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC", "1")
    for m, var in _CRED_VARS.items():
        if m != method or not (env.get(var) or "").strip():
            env.pop(var, None)
    return env


def _one_line(text: str, limit: int = 400, tail: bool = False) -> str:
    """Secret-scrubbed, whitespace-collapsed, length-bounded — safe for a log
    line, an annotation, or a public PR comment."""
    t = re.sub(r"\s+", " ", _SECRET_RE.sub("sk-ant-***", text or "")).strip()
    if len(t) > limit:
        t = ("…" + t[-limit:]) if tail else (t[:limit] + "…")
    return t


def failure_reason(proc) -> str:
    """Why a ``claude -p --output-format json`` call failed, as one line. The CLI
    writes its refusal to STDOUT as a result payload (``subtype`` + ``result``),
    so read that first and fall back to the stderr/stdout tail."""
    out = (proc.stdout or "").strip()
    if out:
        try:
            env = json.loads(out.splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            env = None
        if isinstance(env, dict):
            parts = [str(p) for p in (env.get("subtype"),
                                      env.get("result") or env.get("error")) if p]
            if parts:
                return _one_line(": ".join(parts))
    return _one_line(proc.stderr or out, tail=True)


def _annotate(level: str, title: str, message: str) -> None:
    """Emit a GitHub Actions annotation (no-op elsewhere), so a credential problem
    is visible on the run even when the calling step is continue-on-error."""
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return
    msg = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    print(f"::{level} title={title}::{msg}", file=sys.stderr, flush=True)


class RunnerError(RuntimeError):
    pass


class AuthError(RunnerError):
    """The backend refused to serve us and won't recover mid-batch. The batch stops
    on this (it won't fix itself between quests), writes the quests that DID score
    as partial evidence, and — if zero scored — exits non-zero so the caller can
    route the slice. Transient blips are retried in `_invoke` first; this is only
    raised once retries are exhausted. Two flavors, because they need OPPOSITE
    responses from the orchestrator:

      AuthError      — CREDENTIALS are broken (invalid/expired/revoked token, or a
                       billing hold): retrying tomorrow with the same secret fails
                       identically, so a HUMAN must rotate it. Permanent until acted on.
      ThrottleError  — a *sustained* rate-limit/overload that outlived every retry:
                       the shared token's window refills, so the loop should soft-skip
                       and simply retry on its next run. Transient by nature.

    ``failures`` lists ``(method, outcome, reason)`` for every credential that was
    tried; ``reason`` is the one-line, secret-scrubbed summary of them, safe to
    put in a PR comment."""

    def __init__(self, message: str = "", failures=None):
        super().__init__(message)
        self.failures = list(failures or [])
        self.reason = "; ".join(f"{m}: {r or o}" for m, o, r in self.failures)


class ThrottleError(AuthError):
    """Sustained rate-limit/overload (see AuthError). Subclasses AuthError so
    existing `except AuthError` batch-stop handling keeps working unchanged."""
    pass


def _looks_like_auth_failure(text: str) -> bool:
    """CREDENTIAL problems a retry can never fix — a human must rotate the token
    (or settle billing). Deliberately distinct from `_looks_like_transient`."""
    t = (text or "").lower()
    return ("401" in t and "auth" in t) or "failed to authenticate" in t \
        or "invalid authentication" in t or "invalid api key" in t \
        or "invalid x-api-key" in t or "no credentials" in t \
        or "authentication_error" in t or "invalid bearer token" in t \
        or ("token" in t and ("expired" in t or "revoked" in t or "invalid" in t)) \
        or ("credit balance" in t and "low" in t) \
        or ("please run" in t and "login" in t)


def _looks_like_transient(text: str) -> bool:
    """Recoverable backend/transport conditions — overload, rate-limit, a 5xx, or a
    network blip — that a short backoff usually clears. Kept deliberately DISTINCT
    from auth (a bad token never recovers, so retrying it just burns time) and
    matched only on distinctive error phrasings, not bare status numbers, so an
    agent transcript that merely *mentions* '503' can't masquerade as a transport
    failure. Callers additionally gate this on a non-zero exit — a clean run is a
    real result no matter what its transcript says."""
    t = (text or "").lower()
    needles = (
        "overloaded", "rate limit", "rate_limit", "rate-limit", "429", "529",
        "too many requests", "internal server error", "service unavailable",
        "bad gateway", "gateway timeout", "temporarily unavailable",
        "please try again", "try again later", "connection reset",
        "connection refused", "econnreset", "etimedout", "eai_again",
        "network error", "request timed out",
        # Subscription-plan window exhaustion ("Claude AI usage limit reached …
        # resets at <time>") — refills on its own, so it's throttle, not auth.
        "usage limit",
    )
    return any(n in t for n in needles)


def _looks_like_quota(text: str) -> bool:
    """The CREDENTIAL-specific slice of `_looks_like_transient`: a rate or usage
    limit belongs to one credential, so the next credential may still be served.
    An overload/5xx/network blip is the backend's, and switching credential won't
    help it."""
    t = (text or "").lower()
    return any(n in t for n in ("usage limit", "rate limit", "rate_limit", "rate-limit",
                                "429", "too many requests"))


class AgenticRunner:
    def __init__(self, mode: str = "review", model: Optional[str] = None,
                 timeout: int = 600, claude_bin: str = "claude",
                 mock: bool = False, dry_run: bool = False, verbose: bool = False,
                 max_turns: int = 0, max_attempts: int = 0,
                 retry_base_s: float = 0.0, retry_max_s: float = 0.0,
                 adaptive_turns: bool = False):
        if mode not in ("review", "execute"):
            raise ValueError(f"mode must be 'review' or 'execute', got {mode!r}")
        self.mode = mode
        self.model = model
        self.timeout = timeout
        self.claude_bin = claude_bin
        self.mock = mock
        self.dry_run = dry_run
        self.verbose = verbose
        # Per-quest turn ceiling (0 = CLI default). Bounds runaway agent loops
        # and is the cheapest cost governor: fewer turns ≈ less spend.
        self.max_turns = max_turns
        # Adaptive per-quest budget: size the turn allowance to the quest's own
        # DETERMINISTIC runnable-snippet count instead of spending the full cap
        # on every quest (a 2-snippet intro doesn't need a capstone's budget).
        # max_turns stays the hard cap; see _turn_budget for the formula. Only
        # meaningful with max_turns > 0 — with no cap there is nothing to adapt.
        self.adaptive_turns = adaptive_turns
        # Transient-failure retry policy (see _invoke). A single overload/rate-limit
        # blip on the first quest otherwise aborts the whole batch and wastes the
        # slice, so retry the recoverable classes with exponential backoff + jitter
        # before giving up. 0 = fall back to env/default; tests pass explicit small
        # values to keep them fast. Total added worst-case wait per quest is bounded
        # by (max_attempts-1) × retry_max_s.
        self.max_attempts = max_attempts or int(os.environ.get("QUEST_QA_MAX_ATTEMPTS", "4") or 4)
        self.retry_base_s = retry_base_s or float(os.environ.get("QUEST_QA_RETRY_BASE_S", "3") or 3)
        self.retry_max_s = retry_max_s or float(os.environ.get("QUEST_QA_RETRY_MAX_S", "45") or 45)
        # Credentials refused earlier in this process (see _auth_plan): skipped on
        # later quests so a dead OAuth token costs its retries once per batch, not
        # once per quest. `auth_method` is the method that last authenticated.
        self._refused: set = set()
        self.auth_method: Optional[str] = None

    # ---- auth -----------------------------------------------------------

    def _auth_plan(self) -> List[str]:
        """Credential methods to try for the next call, in order (``ambient`` = no
        credential in the env; use the CLI's stored login)."""
        order = auth_order()
        if not order:
            return ["ambient"]
        return [m for m in order if m not in self._refused] or order

    def _attempt(self, cmd: List[str], cwd: Path, method: str):
        """Run ``cmd`` with ONE credential, retrying the recoverable classes with
        backoff. Returns ``(outcome, proc, duration_s)``; outcome is ``ok``,
        ``auth`` / ``quota`` (this credential was refused), ``transient`` (the
        backend stayed overloaded) or ``error`` (anything else). Only a NON-clean
        exit is classified: a clean run is a real result even if its transcript
        happens to mention "503"/"rate limit" as quest content. Lets
        ``subprocess.TimeoutExpired`` propagate (each caller handles it its way)."""
        env = child_env(method)
        attempts = max(1, self.max_attempts)
        for attempt in range(1, attempts + 1):
            t0 = time.time()
            proc = subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True,
                                  text=True, timeout=self.timeout)
            dur = round(time.time() - t0, 1)
            if proc.returncode == 0:
                return "ok", proc, dur
            combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
            auth = _looks_like_auth_failure(combined)
            transient = _looks_like_transient(combined)
            if (auth or transient) and attempt < attempts:
                self._backoff(attempt, "auth-endpoint" if auth and not transient
                              else "rate-limit/overload", method)
                continue
            if auth:
                return "auth", proc, dur
            if transient:
                return ("quota" if _looks_like_quota(combined) else "transient"), proc, dur
            return "error", proc, dur
        return "error", proc, dur  # unreachable: the last attempt always returns

    def _refuse(self, method: str, outcome: str, reason: str, nxt: Optional[str]) -> None:
        """Record that ``method`` was refused and, if another credential is left,
        say loudly that we are falling back to it."""
        self._refused.add(method)
        if not nxt:
            return
        msg = f"{method} was refused ({outcome}) — falling back to {nxt}"
        print(f"⚠️  {msg}: {reason or 'no error text'}", file=sys.stderr, flush=True)
        _annotate("warning", "Claude auth fallback", f"{msg}. {reason}")

    @staticmethod
    def _auth_error(failures) -> AuthError:
        """The batch-stopping error once every credential was refused. A quota
        refusal anywhere means something refills on its own (ThrottleError, retry
        next run); otherwise a human has to fix a secret (AuthError)."""
        lines = []
        for method, outcome, reason in failures:
            var = _CRED_VARS.get(method, "the CLI's stored login")
            lines.append(f"  • {method} ({var}) → {outcome}: {reason or 'no error text'}")
            hint = _FIX_HINT.get((method, outcome))
            if hint:
                lines.append(f"    fix: {hint}")
        detail = "\n".join(lines)
        if any(o == "quota" for _, o, _ in failures):
            return ThrottleError(f"{THROTTLE_HINT}\n{detail}", failures)
        return AuthError(f"{AUTH_HINT}\nWhat each credential said:\n{detail}", failures)

    # ---- public ---------------------------------------------------------

    def available(self) -> bool:
        """Is the claude CLI resolvable? (Not needed for mock/dry-run.)"""
        return shutil.which(self.claude_bin) is not None

    def preflight(self):
        """One tiny end-to-end call to classify the CURRENT auth state before any
        expensive work is scheduled. Returns ``(status, detail)`` with status one of:

          ok        — the CLI authenticated and answered (auth + backend healthy)
          throttled — sustained rate-limit/overload: refills on its own, retry later
          auth      — credentials are broken: a human must rotate the token
          unknown   — could not classify (CLI missing, timeout, novel error). Callers
                      should FAIL OPEN on this: the preflight is an optimization and
                      a diagnoser, never a new single point of failure.

        Runs from an empty temp dir so the CLI never scans a repo, and retries the
        recoverable classes with the runner's (short) backoff policy so a single
        blip doesn't misreport a healthy token."""
        if self.mock:
            return "ok", "mock mode — no probe sent"
        if not self.available():
            return "unknown", f"`{self.claude_bin}` not found on PATH"
        cmd = [
            self.claude_bin, "-p", "Reply with exactly: ok",
            "--output-format", "json", "--max-turns", "1",
            "--permission-mode", "default",
            "--disallowedTools", "Bash", "Read", "Write", "Edit", "WebFetch", "WebSearch",
        ]
        if self.model:
            cmd += ["--model", self.model]
        if self.dry_run:
            return "ok", "dry-run — would send: " + " ".join(cmd[:6]) + " …"
        sandbox = Path(tempfile.mkdtemp(prefix="quest-preflight-"))
        try:
            plan = self._auth_plan()
            failures = []
            for i, method in enumerate(plan):
                try:
                    outcome, proc, _ = self._attempt(cmd, sandbox, method)
                except subprocess.TimeoutExpired:
                    return "unknown", f"probe timed out after {self.timeout}s"
                if outcome == "ok":
                    self.auth_method = method
                    detail = "authenticated end-to-end"
                    if method != "ambient":
                        detail += f" via {method}"
                    if failures:
                        detail += " (refused first: " + "; ".join(
                            f"{m}: {r or o}" for m, o, r in failures) + ")"
                    return "ok", detail
                reason = failure_reason(proc)
                if outcome in ("auth", "quota"):
                    failures.append((method, outcome, reason))
                    nxt = plan[i + 1] if i + 1 < len(plan) else None
                    self._refuse(method, outcome, reason, nxt)
                    if nxt:
                        continue
                    err = self._auth_error(failures)
                    return ("throttled" if isinstance(err, ThrottleError) else "auth"), err.reason
                if outcome == "transient":
                    return "throttled", f"{method}: {reason}"
                return "unknown", f"{method}: {reason}"
            return "unknown", "no credential method was tried"
        finally:
            shutil.rmtree(sandbox, ignore_errors=True)

    def _turn_budget(self, quest) -> int:
        """The per-quest turn allowance actually sent to the CLI.

        Fixed mode (default): the flat ``max_turns`` cap for every quest.
        Adaptive mode: ``14 + 3 × runnable_snippets`` clamped to [16, max_turns] —
        derived from the SAME deterministic snippet inventory the prompt hands the
        agent as its checklist, so the budget scales with the work the quest
        actually contains. Small quests stop paying the capstone rate; heavy
        quests still hit the cap (and are handled by the budget-exhausted
        fallback in _invoke). Returns 0 (no flag) when max_turns is 0.
        """
        if not self.max_turns or self.max_turns <= 0:
            return 0
        if not self.adaptive_turns or quest_lib is None:
            return self.max_turns
        try:
            runnable = int(quest_lib.snippet_summary(quest.body or "")["runnable"])
        except Exception:
            return self.max_turns
        return max(16, min(self.max_turns, 14 + 3 * runnable))

    def run(self, quest) -> dict:
        """Validate one quest; return a result dict (see _finalize)."""
        sandbox = Path(tempfile.mkdtemp(prefix="quest-qa-"))
        try:
            (sandbox / "QUEST.md").write_text(quest.body, encoding="utf-8")
            turns = self._turn_budget(quest)
            system_prompt = prompts.build_system_prompt(self.mode)
            user_prompt = prompts.build_user_prompt(quest, mode=self.mode,
                                                    turn_budget=turns)
            cmd = self._build_cmd(system_prompt, user_prompt, max_turns=turns)

            if self.dry_run:
                return {"quest": quest.to_meta(), "dry_run": True,
                        "command": _redact(cmd), "system_prompt": system_prompt,
                        "user_prompt": user_prompt}
            if self.mock:
                return self._finalize(quest, self._mock_verdict(quest),
                                      meta={"mock": True, "cost_usd": 0.0, "turns": 0,
                                            "duration_s": 0.0})

            return self._invoke(quest, cmd, sandbox)
        finally:
            shutil.rmtree(sandbox, ignore_errors=True)

    # ---- command construction ------------------------------------------

    def _build_cmd(self, system_prompt: str, user_prompt: str,
                   max_turns: Optional[int] = None) -> List[str]:
        cmd = [
            self.claude_bin, "-p", user_prompt,
            "--output-format", "json",
            "--append-system-prompt", system_prompt,
            "--json-schema", json.dumps(schema.build_json_schema()),
        ]
        if self.mode == "execute":
            # Sandboxed execution: bypass prompts (disposable cwd), allow local
            # build tools, hard-deny network + the obvious foot-guns.
            cmd += [
                "--permission-mode", "bypassPermissions",
                "--allowedTools", "Bash", "Read", "Write", "Edit",
                "--disallowedTools",
                "WebFetch", "WebSearch",
                "Bash(sudo:*)", "Bash(rm -rf /*)", "Bash(curl:*)", "Bash(wget:*)",
            ]
        else:
            # Review: read-only. No Bash at all.
            cmd += [
                "--permission-mode", "default",
                "--allowedTools", "Read",
                "--disallowedTools", "Bash", "Write", "Edit", "WebFetch", "WebSearch",
            ]
        turns = self.max_turns if max_turns is None else max_turns
        if turns and turns > 0:
            cmd += ["--max-turns", str(turns)]
        if self.model:
            cmd += ["--model", self.model]
        return cmd

    # ---- invocation + parsing ------------------------------------------

    def _backoff(self, attempt: int, reason: str, method: str = "") -> None:
        """Sleep exponentially (base × 2^(attempt-1), capped) with jitter before the
        next retry, narrating to stderr so CI logs show why the pause happened."""
        delay = min(self.retry_base_s * (2 ** (attempt - 1)), self.retry_max_s)
        delay += random.uniform(0, self.retry_base_s)  # jitter, avoid thundering herd
        via = f" [{method}]" if method and method != "ambient" else ""
        print(f"⏳ transient failure ({reason}){via} — retry {attempt}/{self.max_attempts - 1} "
              f"in {delay:.1f}s …", file=sys.stderr, flush=True)
        time.sleep(delay)

    def _invoke(self, quest, cmd: List[str], sandbox: Path) -> dict:
        if not self.available():
            raise RunnerError(
                f"`{self.claude_bin}` not found on PATH. Install Claude Code, or run with --mock."
            )
        # Each credential is tried on its own, OAuth first (see _auth_plan), and
        # _attempt retries the recoverable failure classes before giving up on it:
        # a single overload/rate-limit/5xx/network blip (or an ambiguous
        # auth-endpoint hiccup) on ANY quest — especially the first — otherwise
        # aborts the whole batch and throws away the slice. A credential that is
        # still REFUSED after its retries (auth / quota) hands over to the next
        # one; once none is left, AuthError/ThrottleError stops the batch (partial
        # evidence is written). A sustained overload stops it too — switching
        # credential won't help the backend. A genuine timeout or any other
        # non-zero exit is a per-quest RunnerError (the batch moves on).
        plan = self._auth_plan()
        failures = []
        for i, method in enumerate(plan):
            try:
                outcome, proc, dur = self._attempt(cmd, sandbox, method)
            except subprocess.TimeoutExpired:
                # A timeout is expensive (up to self.timeout burned) and often a
                # runaway quest rather than a transport blip, so don't multiply it —
                # record it as this quest's error and let the batch move on.
                raise RunnerError(f"claude timed out after {self.timeout}s")
            if outcome == "ok":
                self.auth_method = method
                break  # clean run — fall through to envelope parsing below
            reason = failure_reason(proc)
            if outcome in ("auth", "quota"):
                failures.append((method, outcome, reason))
                nxt = plan[i + 1] if i + 1 < len(plan) else None
                self._refuse(method, outcome, reason, nxt)
                if nxt:
                    continue
                raise self._auth_error(failures)
            if outcome == "transient":
                raise ThrottleError(f"{THROTTLE_HINT}\nLast output [{method}]: {reason}",
                                    failures + [(method, outcome, reason)])
            tail = _one_line(proc.stderr or proc.stdout, limit=800, tail=True)
            raise RunnerError(f"claude exited {proc.returncode}: {tail}")

        envelope = self._parse_envelope(proc.stdout)
        # The CLI signals failures (incl. the --max-turns cap) with is_error=true
        # and a subtype, often WITH returncode 0. Surface it as a real error
        # rather than letting it fall through to "couldn't parse a verdict" —
        # otherwise the --max-turns governor's own trip is invisible.
        err = self._error_from_envelope(envelope)
        if err:
            meta = {"mock": False, "cost_usd": envelope.get("total_cost_usd"),
                    "turns": envelope.get("num_turns"),
                    "session_id": envelope.get("session_id"), "duration_s": dur,
                    "auth": self.auth_method}
            # error_max_turns is a VERDICT about the quest, not an engine fault:
            # the walk happened and ran out of budget — in learner terms the
            # session ended unfinished, which is a FAIL, not a void. Recording it
            # as an errored (unscored) result had a nasty consequence: errored
            # quests contribute NO ledger coverage, so a quest that always
            # overruns blocks its slice's full-coverage forever — the circuit
            # breaker (M6) never trips and the loop grinds that slice for good
            # (observed: issue #642, "Stack Attack" at 40 turns). Convert it to a
            # SCORED fail with a clearly harness-labeled verdict instead:
            # coverage completes, the breaker can act, and the fix lane gets the
            # one recommendation that is actually true — the quest is too heavy
            # for a single walk session.
            if envelope.get("subtype") == "error_max_turns":
                return self._budget_exhausted_result(quest, meta)
            return self._finalize(quest, None, meta=meta, error=err,
                                  raw=json.dumps(envelope)[:2000])
        verdict, raw = self._extract_verdict(envelope)
        meta = {
            "mock": False,
            "cost_usd": envelope.get("total_cost_usd"),
            "turns": envelope.get("num_turns"),
            "session_id": envelope.get("session_id"),
            "duration_s": dur,
            "auth": self.auth_method,
        }
        if verdict is None:
            return self._finalize(quest, None, meta=meta,
                                  error=f"could not parse a JSON verdict from the agent.",
                                  raw=raw)
        return self._finalize(quest, verdict, meta=meta)

    @staticmethod
    def _parse_envelope(stdout: str) -> dict:
        stdout = (stdout or "").strip()
        if not stdout:
            raise RunnerError("claude returned empty stdout")
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            # Some configs stream multiple JSON lines; take the last object line.
            for line in reversed(stdout.splitlines()):
                line = line.strip()
                if line.startswith("{") and line.endswith("}"):
                    try:
                        return json.loads(line)
                    except json.JSONDecodeError:
                        continue
            raise RunnerError("claude stdout was not valid JSON")

    @staticmethod
    def _error_from_envelope(envelope: dict) -> Optional[str]:
        """Return an error string if the CLI envelope signals a failure
        (``is_error: true``, e.g. ``subtype: error_max_turns``), else None.
        Pulled out as a pure function so the contract test can pin it."""
        if not isinstance(envelope, dict) or not envelope.get("is_error"):
            return None
        subtype = envelope.get("subtype") or "error"
        detail = str(envelope.get("result") or envelope.get("error") or "")[:200]
        return f"agent run failed ({subtype}): {detail}"

    @classmethod
    def _extract_verdict(cls, envelope: dict):
        """Return (verdict_dict_or_None, raw_text). Handles every shape the CLI
        might use for structured output."""
        # 1) Native structured output keys, if the CLI surfaces them.
        for key in ("structured_output", "structuredOutput", "structured_result"):
            val = envelope.get(key)
            if isinstance(val, dict):
                return val, json.dumps(val)
        result = envelope.get("result")
        if isinstance(result, dict):
            return result, json.dumps(result)
        text = result if isinstance(result, str) else json.dumps(envelope)
        # 2) Whole result is JSON.
        try:
            return json.loads(text), text
        except (json.JSONDecodeError, TypeError):
            pass
        # 3) Last fenced ```json block.
        matches = _FENCE_RE.findall(text or "")
        if matches:
            try:
                return json.loads(matches[-1]), text
            except json.JSONDecodeError:
                pass
        return None, text

    # ---- normalization + scoring ---------------------------------------

    def _budget_exhausted_result(self, quest, meta: dict) -> dict:
        """A SCORED fail for a walk that hit the turn cap before emitting a verdict.

        Every value is deliberately harness-labeled ("[harness] …") — this is not
        a model assessment and never pretends to be one. Dimensions score 0 (the
        session ended with nothing verified), the single recommendation carries
        the one finding the overrun actually proves (the quest exceeds a walk
        session), and ``budget_exhausted: true`` marks the result for downstream
        readers. Because the result carries no ``error`` key it counts as scored:
        the ledger records coverage (verdict=fail), the slice can still reach
        full coverage, and the M6 circuit breaker stays reachable.
        """
        turns = meta.get("turns") or self.max_turns or 0
        turns_txt = str(turns) if turns else "its configured"
        note = ("[harness] Not scored by the model: the walk exhausted its turn "
                "budget before a verdict could be emitted.")
        verdict = {
            "executed": False,  # turns were spent, but nothing was verified into a verdict
            "dimensions": {k: {"score": 0, "findings": [note]} for k in schema.DIM_KEYS},
            "commands": [],
            "recommendations": [{
                "priority": "high",
                "area": "structure",
                "suggestion": (
                    f"[harness] The sandboxed walk hit its {turns_txt}-turn budget before "
                    "finishing this quest. Split it into smaller linked quests/chapters, or "
                    "reduce the number of required commands, so a learner-paced session can "
                    "complete it end to end."
                ),
            }],
            "summary": (
                f"[harness] Budget exhausted: the agent ran out of turns ({turns_txt}) "
                "mid-walk and produced no verdict. Recorded as a FAIL so slice coverage "
                "completes; the zeroed dimension scores are harness-assigned, not "
                "model-assessed."
            ),
        }
        result = self._finalize(quest, verdict, meta=meta)
        result["budget_exhausted"] = True
        return result

    def _finalize(self, quest, verdict, meta: dict,
                  error: Optional[str] = None, raw: Optional[str] = None) -> dict:
        result = {"quest": quest.to_meta(), "mode": self.mode, "meta": meta}
        if error or verdict is None:
            result["error"] = error or "no verdict produced"
            if raw and self.verbose:
                result["raw"] = raw[:2000]
            result["overall"] = 0.0
            result["verdict"] = schema.VERDICT_FAIL
            result["verdict_obj"] = None
            return result
        verdict = _normalize_verdict(verdict)
        scored = schema.score_verdict(verdict)
        result["verdict_obj"] = verdict
        result["overall"] = scored["overall"]
        result["per_dimension"] = scored["per_dimension"]
        result["weight_covered"] = scored["weight_covered"]
        result["verdict"] = schema.verdict_label(scored["overall"])
        result["snippets"] = self._snippet_coverage(quest, verdict)
        return result

    @staticmethod
    def _snippet_coverage(quest, verdict: dict) -> dict:
        """Cross the deterministic snippet inventory with what the agent reported
        running, so a report can show 'ran N/M runnable snippets'."""
        total = runnable = None
        if quest_lib is not None:
            try:
                s = quest_lib.snippet_summary(getattr(quest, "body", "") or "")
                total, runnable = s["total"], s["runnable"]
            except Exception:
                pass
        cmds = verdict.get("commands") or []
        status = {"passed": 0, "failed": 0, "skipped": 0, "reasoned": 0}
        for c in cmds:
            st = (c.get("status") if isinstance(c, dict) else None)
            if st in status:
                status[st] += 1
        return {
            "available_total": total, "available_runnable": runnable,
            "recorded": len(cmds), "ran": status["passed"] + status["failed"],
            **status,
            "executed": bool(verdict.get("executed")),
        }

    # ---- mock ----------------------------------------------------------

    @staticmethod
    def _mock_verdict(quest) -> dict:
        """Deterministic synthetic verdict derived from the quest text so the
        full pipeline (parse → score → report) can be tested offline."""
        body = quest.body or ""
        # Cheap, DETERMINISTIC signals — NOT a real assessment. Uses sha256 (not
        # Python's salted hash()) so the same quest always yields the same mock
        # verdict across processes — required for a reproducible offline pipeline
        # test and the envelope contract test.
        digest = hashlib.sha256(f"{quest.slug}:{len(body)}".encode("utf-8")).digest()
        h = digest[0] % 3
        base = 4 if len(body) > 4000 else 3
        dims = {}
        for i, key in enumerate(schema.DIM_KEYS):
            s = max(0, min(schema.MAX_DIM, base + ((i + h) % 2)))
            dims[key] = {"score": s, "findings": [f"[mock] {key}: synthetic score {s} (offline pipeline test)."]}
        # Snippet-aware synthetic commands so the coverage report is exercisable
        # offline. Mock doesn't run anything, so each is `reasoned`.
        commands = [{"command": "(mock) no commands run", "status": "reasoned",
                     "detail": "Mock mode — pipeline test only."}]
        if quest_lib is not None:
            try:
                snips = quest_lib.runnable_snippets(body)
                if snips:
                    commands = [
                        {"command": (b.code.splitlines()[0][:80] if b.code.splitlines() else b.lang),
                         "status": "reasoned",
                         "detail": f"[mock] {b.lang} snippet at line {b.line} (not run in mock)."}
                        for b in snips[:25]
                    ]
            except Exception:
                pass
        return {
            "executed": False,
            "dimensions": dims,
            "commands": commands,
            "recommendations": ([] if base + h >= 5 else
                                [{"priority": "low", "area": "mock",
                                  "suggestion": "Run without --mock for a real assessment."}]),
            "summary": f"[mock] Synthetic verdict for '{quest.title}'. Use a live run for a real score.",
        }


def _normalize_verdict(v: dict) -> dict:
    """Defensive cleanup so a slightly-off verdict still scores + renders."""
    v = dict(v) if isinstance(v, dict) else {}
    v["executed"] = bool(v.get("executed", False))
    dims = v.get("dimensions") if isinstance(v.get("dimensions"), dict) else {}
    fixed = {}
    for key in schema.DIM_KEYS:
        d = dims.get(key) if isinstance(dims.get(key), dict) else {}
        findings = d.get("findings")
        fixed[key] = {
            "score": d.get("score"),
            "findings": [str(x) for x in findings] if isinstance(findings, list) else [],
        }
    v["dimensions"] = fixed
    v["commands"] = v.get("commands") if isinstance(v.get("commands"), list) else []
    v["recommendations"] = v.get("recommendations") if isinstance(v.get("recommendations"), list) else []
    v["summary"] = str(v.get("summary") or "")
    return v


def _redact(cmd: List[str]) -> List[str]:
    """Shorten the giant system-prompt arg for dry-run display."""
    out = []
    skip_next = False
    for i, a in enumerate(cmd):
        if skip_next:
            out.append(f"<{len(a)}-char prompt>")
            skip_next = False
            continue
        out.append(a)
        if a in ("--append-system-prompt", "--json-schema", "-p"):
            skip_next = True
    return out
