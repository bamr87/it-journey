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


class RunnerError(RuntimeError):
    pass


class AuthError(RunnerError):
    """The backend refused to serve us and won't recover mid-batch — a bad/expired
    token OR a *sustained* rate-limit/overload that outlived every retry. The batch
    stops on this (auth won't fix itself between quests), writes the quests that DID
    score as partial evidence, and — if zero scored — exits non-zero so the caller
    can soft-skip the slice. Transient blips are retried in `_invoke` first; this is
    only raised once retries are exhausted."""
    pass


def _looks_like_auth_failure(text: str) -> bool:
    t = (text or "").lower()
    return ("401" in t and "auth" in t) or "failed to authenticate" in t \
        or "invalid authentication" in t or "invalid api key" in t \
        or "invalid x-api-key" in t or "no credentials" in t \
        or ("oauth" in t and "token" in t and ("expired" in t or "invalid" in t)) \
        or "please run" in t and "login" in t


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
    )
    return any(n in t for n in needles)


class AgenticRunner:
    def __init__(self, mode: str = "review", model: Optional[str] = None,
                 timeout: int = 600, claude_bin: str = "claude",
                 mock: bool = False, dry_run: bool = False, verbose: bool = False,
                 max_turns: int = 0, max_attempts: int = 0,
                 retry_base_s: float = 0.0, retry_max_s: float = 0.0):
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
        # Transient-failure retry policy (see _invoke). A single overload/rate-limit
        # blip on the first quest otherwise aborts the whole batch and wastes the
        # slice, so retry the recoverable classes with exponential backoff + jitter
        # before giving up. 0 = fall back to env/default; tests pass explicit small
        # values to keep them fast. Total added worst-case wait per quest is bounded
        # by (max_attempts-1) × retry_max_s.
        self.max_attempts = max_attempts or int(os.environ.get("QUEST_QA_MAX_ATTEMPTS", "4") or 4)
        self.retry_base_s = retry_base_s or float(os.environ.get("QUEST_QA_RETRY_BASE_S", "3") or 3)
        self.retry_max_s = retry_max_s or float(os.environ.get("QUEST_QA_RETRY_MAX_S", "45") or 45)

    # ---- public ---------------------------------------------------------

    def available(self) -> bool:
        """Is the claude CLI resolvable? (Not needed for mock/dry-run.)"""
        return shutil.which(self.claude_bin) is not None

    def run(self, quest) -> dict:
        """Validate one quest; return a result dict (see _finalize)."""
        sandbox = Path(tempfile.mkdtemp(prefix="quest-qa-"))
        try:
            (sandbox / "QUEST.md").write_text(quest.body, encoding="utf-8")
            system_prompt = prompts.build_system_prompt(self.mode)
            user_prompt = prompts.build_user_prompt(quest, mode=self.mode)
            cmd = self._build_cmd(system_prompt, user_prompt)

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

    def _build_cmd(self, system_prompt: str, user_prompt: str) -> List[str]:
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
        if self.max_turns and self.max_turns > 0:
            cmd += ["--max-turns", str(self.max_turns)]
        if self.model:
            cmd += ["--model", self.model]
        return cmd

    # ---- invocation + parsing ------------------------------------------

    def _backoff(self, attempt: int, reason: str) -> None:
        """Sleep exponentially (base × 2^(attempt-1), capped) with jitter before the
        next retry, narrating to stderr so CI logs show why the pause happened."""
        delay = min(self.retry_base_s * (2 ** (attempt - 1)), self.retry_max_s)
        delay += random.uniform(0, self.retry_base_s)  # jitter, avoid thundering herd
        print(f"⏳ transient failure ({reason}) — retry {attempt}/{self.max_attempts - 1} "
              f"in {delay:.1f}s …", file=sys.stderr, flush=True)
        time.sleep(delay)

    def _invoke(self, quest, cmd: List[str], sandbox: Path) -> dict:
        if not self.available():
            raise RunnerError(
                f"`{self.claude_bin}` not found on PATH. Install Claude Code, or run with --mock."
            )
        env = dict(os.environ)
        env.setdefault("CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC", "1")

        # Retry the recoverable failure classes before surfacing a hard error: a
        # single overload/rate-limit/5xx/network blip (or an ambiguous auth-endpoint
        # hiccup) on ANY quest — especially the first — otherwise aborts the whole
        # batch and throws away the slice. Only a NON-clean exit (returncode != 0)
        # is eligible: a clean run is a real result even if its transcript happens
        # to mention "503"/"rate limit" as quest content. A genuine timeout or a
        # non-transient error still fails fast (retrying won't help). Once retries
        # are exhausted, auth/throttle raise AuthError (stop the batch, write partial
        # evidence); any other non-zero exit is a per-quest RunnerError (batch
        # continues to the next quest).
        attempts = max(1, self.max_attempts)
        for attempt in range(1, attempts + 1):
            t0 = time.time()
            try:
                proc = subprocess.run(
                    cmd, cwd=str(sandbox), env=env, capture_output=True, text=True,
                    timeout=self.timeout,
                )
            except subprocess.TimeoutExpired:
                # A timeout is expensive (up to self.timeout burned) and often a
                # runaway quest rather than a transport blip, so don't multiply it —
                # record it as this quest's error and let the batch move on.
                raise RunnerError(f"claude timed out after {self.timeout}s")
            dur = round(time.time() - t0, 1)

            combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
            clean = proc.returncode == 0
            auth = (not clean) and _looks_like_auth_failure(combined)
            transient = (not clean) and _looks_like_transient(combined)

            if (auth or transient) and attempt < attempts:
                self._backoff(attempt, "auth-endpoint" if auth and not transient
                              else "rate-limit/overload")
                continue
            if auth:
                raise AuthError(AUTH_HINT)
            if transient:
                tail = (proc.stderr or proc.stdout or "").strip()[-400:]
                raise AuthError(f"{THROTTLE_HINT}\nLast output: {tail}")
            if not clean:
                tail = (proc.stderr or proc.stdout or "").strip()[-800:]
                raise RunnerError(f"claude exited {proc.returncode}: {tail}")
            break  # clean run — fall through to envelope parsing below

        envelope = self._parse_envelope(proc.stdout)
        # The CLI signals failures (incl. the --max-turns cap) with is_error=true
        # and a subtype, often WITH returncode 0. Surface it as a real error
        # rather than letting it fall through to "couldn't parse a verdict" —
        # otherwise the --max-turns governor's own trip is invisible.
        err = self._error_from_envelope(envelope)
        if err:
            meta = {"mock": False, "cost_usd": envelope.get("total_cost_usd"),
                    "turns": envelope.get("num_turns"),
                    "session_id": envelope.get("session_id"), "duration_s": dur}
            return self._finalize(quest, None, meta=meta, error=err,
                                  raw=json.dumps(envelope)[:2000])
        verdict, raw = self._extract_verdict(envelope)
        meta = {
            "mock": False,
            "cost_usd": envelope.get("total_cost_usd"),
            "turns": envelope.get("num_turns"),
            "session_id": envelope.get("session_id"),
            "duration_s": dur,
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
