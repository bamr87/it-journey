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

import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import List, Optional

from . import prompts, schema

_FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)

AUTH_HINT = (
    "Claude could not authenticate. The agentic validator delegates auth to the "
    "`claude` CLI, so set up ONE of:\n"
    "  • Local: run `claude login` (or `claude setup-token`) so credentials live in ~/.claude.\n"
    "  • CI / headless: export CLAUDE_CODE_OAUTH_TOKEN=$(claude setup-token) as a secret.\n"
    "Note: inside a managed/sandboxed agent session, host-managed auth is NOT passed to child\n"
    "`claude` processes — run this validator from a normal shell or a CI runner with the token set."
)


class RunnerError(RuntimeError):
    pass


class AuthError(RunnerError):
    pass


def _looks_like_auth_failure(text: str) -> bool:
    t = (text or "").lower()
    return ("401" in t and "auth" in t) or "failed to authenticate" in t \
        or "invalid authentication" in t or "invalid api key" in t


class AgenticRunner:
    def __init__(self, mode: str = "review", model: Optional[str] = None,
                 timeout: int = 600, claude_bin: str = "claude",
                 mock: bool = False, dry_run: bool = False, verbose: bool = False):
        if mode not in ("review", "execute"):
            raise ValueError(f"mode must be 'review' or 'execute', got {mode!r}")
        self.mode = mode
        self.model = model
        self.timeout = timeout
        self.claude_bin = claude_bin
        self.mock = mock
        self.dry_run = dry_run
        self.verbose = verbose

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
            user_prompt = prompts.build_user_prompt(quest)
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
        if self.model:
            cmd += ["--model", self.model]
        return cmd

    # ---- invocation + parsing ------------------------------------------

    def _invoke(self, quest, cmd: List[str], sandbox: Path) -> dict:
        if not self.available():
            raise RunnerError(
                f"`{self.claude_bin}` not found on PATH. Install Claude Code, or run with --mock."
            )
        env = dict(os.environ)
        env.setdefault("CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC", "1")
        t0 = time.time()
        try:
            proc = subprocess.run(
                cmd, cwd=str(sandbox), env=env, capture_output=True, text=True,
                timeout=self.timeout,
            )
        except subprocess.TimeoutExpired:
            raise RunnerError(f"claude timed out after {self.timeout}s")
        dur = round(time.time() - t0, 1)

        combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
        if _looks_like_auth_failure(combined):
            raise AuthError(AUTH_HINT)
        if proc.returncode != 0:
            tail = (proc.stderr or proc.stdout or "").strip()[-800:]
            raise RunnerError(f"claude exited {proc.returncode}: {tail}")

        envelope = self._parse_envelope(proc.stdout)
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
        return result

    # ---- mock ----------------------------------------------------------

    @staticmethod
    def _mock_verdict(quest) -> dict:
        """Deterministic synthetic verdict derived from the quest text so the
        full pipeline (parse → score → report) can be tested offline."""
        body = quest.body or ""
        # Cheap, deterministic signals — NOT a real assessment.
        h = abs(hash((quest.slug, len(body)))) % 3
        base = 4 if len(body) > 4000 else 3
        dims = {}
        for i, key in enumerate(schema.DIM_KEYS):
            s = max(0, min(schema.MAX_DIM, base + ((i + h) % 2)))
            dims[key] = {"score": s, "findings": [f"[mock] {key}: synthetic score {s} (offline pipeline test)."]}
        return {
            "executed": False,
            "dimensions": dims,
            "commands": [{"command": "(mock) no commands run", "status": "reasoned",
                          "detail": "Mock mode — pipeline test only."}],
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
