#!/usr/bin/env python3
"""
Offline contract test for the agentic validator's CLI-envelope handling.

The agentic runner depends on the *shape* of what `claude -p --output-format
json` prints and on `--json-schema` structured output. Those are undocumented
and unpinned, so a CLI release could silently change them and break scoring
without any test noticing — the failure mode the synthesis called out.

This test pins the contract with NO network and NO `claude` process: it feeds
the runner's pure parsing/scoring/mock functions every envelope shape we know
the CLI can emit and asserts they're handled. Run it in CI before the agentic
job so a CLI drift is caught as a red test, not a wrong score.

    python3 test/quest-validator/agentic/test_envelope.py     # exit 0 = contract holds
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Import the agentic package whether run as a file or a module.
_PKG_DIR = Path(__file__).resolve().parent
_QV_DIR = _PKG_DIR.parent
if str(_QV_DIR) not in sys.path:
    sys.path.insert(0, str(_QV_DIR))

from agentic import runner, schema  # noqa: E402
from agentic.runner import AgenticRunner, RunnerError  # noqa: E402

_failures = []


def check(name, cond):
    print(("  ✅ " if cond else "  ❌ ") + name)
    if not cond:
        _failures.append(name)


def expect_raises(name, fn):
    try:
        fn()
        check(name, False)
    except RunnerError:
        check(name, True)
    except Exception as e:  # wrong exception type
        print(f"  ❌ {name} (raised {type(e).__name__}, expected RunnerError)")
        _failures.append(name)


class _StubQuest:
    """Minimal Quest stand-in for the mock-determinism check."""
    def __init__(self, slug, body):
        self.slug = slug
        self.body = body
        self.title = slug
        self.level = "0000"

    def to_meta(self):
        return {"path": f"{self.slug}.md", "title": self.title, "level": self.level,
                "theme": "", "difficulty": "", "quest_type": "main_quest", "slug": self.slug}


def test_parse_envelope():
    print("\n_parse_envelope — stdout shapes the CLI can emit:")
    # 1) Single JSON object (the common --output-format json case).
    obj = AgenticRunner._parse_envelope(json.dumps({"result": "ok", "num_turns": 3}))
    check("single JSON object", obj.get("num_turns") == 3)
    # 2) Streamed JSON lines — last object line wins.
    streamed = '{"type":"system"}\n{"type":"assistant"}\n{"result":"done","total_cost_usd":0.01}'
    obj = AgenticRunner._parse_envelope(streamed)
    check("streamed JSON lines → last object", obj.get("result") == "done")
    # 3) Empty stdout → RunnerError.
    expect_raises("empty stdout raises", lambda: AgenticRunner._parse_envelope("   "))
    # 4) Pure non-JSON → RunnerError.
    expect_raises("non-JSON stdout raises", lambda: AgenticRunner._parse_envelope("not json at all"))


def test_extract_verdict():
    print("\n_extract_verdict — every structured-output shape:")
    verdict = {"executed": False, "dimensions": {}, "commands": [],
               "recommendations": [], "summary": "x"}
    # 1) Native structured_output key.
    v, _ = AgenticRunner._extract_verdict({"structured_output": verdict})
    check("structured_output key", v == verdict)
    # 2) camelCase variant.
    v, _ = AgenticRunner._extract_verdict({"structuredOutput": verdict})
    check("structuredOutput key", v == verdict)
    # 3) result is already a dict.
    v, _ = AgenticRunner._extract_verdict({"result": verdict})
    check("result is dict", v == verdict)
    # 4) result is a JSON string.
    v, _ = AgenticRunner._extract_verdict({"result": json.dumps(verdict)})
    check("result is JSON string", v == verdict)
    # 5) result wraps the verdict in a fenced ```json block.
    fenced = f"Here is my verdict:\n```json\n{json.dumps(verdict)}\n```\n"
    v, _ = AgenticRunner._extract_verdict({"result": fenced})
    check("result has fenced json block", v == verdict)
    # 6) Nothing parseable → (None, text).
    v, raw = AgenticRunner._extract_verdict({"result": "no verdict here"})
    check("unparseable → None", v is None and "no verdict" in raw)


def test_error_envelopes():
    print("\nerror-envelope detection (is_error / max-turns cap):")
    # A success envelope is NOT an error.
    check("success envelope → no error",
          AgenticRunner._error_from_envelope({"result": "{}", "is_error": False}) is None)
    # The --max-turns cap shape the CLI emits with returncode 0.
    cap = {"subtype": "error_max_turns", "is_error": True,
           "result": "Reached maximum number of turns"}
    err = AgenticRunner._error_from_envelope(cap)
    check("error_max_turns → classified as error",
          err is not None and "error_max_turns" in err)
    # Generic error envelope.
    err = AgenticRunner._error_from_envelope({"is_error": True, "result": "boom"})
    check("generic is_error → error string", err is not None and "boom" in err)
    # A plain envelope with no is_error key is fine.
    check("no is_error key → None",
          AgenticRunner._error_from_envelope({"result": "ok"}) is None)


def test_schema_and_scoring():
    print("\nschema + deterministic scoring:")
    js = schema.build_json_schema()
    check("schema has required keys", set(js.get("required", [])) >=
          {"executed", "dimensions", "commands", "recommendations", "summary"})
    check("schema dimensions match DIM_KEYS",
          set(js["properties"]["dimensions"]["required"]) == set(schema.DIM_KEYS))
    # All-5 verdict → 100%; all-0 → 0%.
    full = {"dimensions": {k: {"score": 5, "findings": []} for k in schema.DIM_KEYS}}
    zero = {"dimensions": {k: {"score": 0, "findings": []} for k in schema.DIM_KEYS}}
    check("all-5 scores → 100.0", schema.score_verdict(full)["overall"] == 100.0)
    check("all-0 scores → 0.0", schema.score_verdict(zero)["overall"] == 0.0)
    check("weights sum to 1.0", abs(sum(schema.WEIGHTS.values()) - 1.0) < 1e-9)
    check("schema_version present", bool(getattr(schema, "SCHEMA_VERSION", "")))


def test_snippet_extraction():
    print("\ncode-snippet extraction (drives execute mode):")
    import importlib, sys as _sys
    qd = str(Path(__file__).resolve().parents[3] / "scripts" / "quest")
    if qd not in _sys.path:
        _sys.path.insert(0, qd)
    ql = importlib.import_module("quest_lib")
    body = (
        "Intro\n\n```bash\necho hi\nls -la\n```\n\n"
        "Config:\n```yaml\nkey: value\n```\n\n"
        "```python\nprint('x')\n```\n"
    )
    blocks = ql.extract_code_blocks(body)
    check("extracts all fenced blocks", len(blocks) == 3)
    check("classifies bash/python runnable, yaml not",
          [b.runnable for b in blocks] == [True, False, True])
    s = ql.snippet_summary(body)
    check("summary counts runnable", s["total"] == 3 and s["runnable"] == 2)
    check("longer display fence not mis-closed",
          len(ql.extract_code_blocks("````md\n```bash\nx\n```\n````\n")) == 1)


def test_mock_determinism():
    print("\nmock determinism (sha256, not salted hash()):")
    q = _StubQuest("terminal-mastery", "x" * 5000)
    r1 = AgenticRunner(mode="review", mock=True)
    r2 = AgenticRunner(mode="review", mock=True)
    v1 = r1._mock_verdict(q)
    v2 = r2._mock_verdict(q)
    check("same quest → identical mock verdict across runner instances", v1 == v2)
    # A different quest should (almost always) differ in at least one dimension.
    other = AgenticRunner(mode="review", mock=True)._mock_verdict(_StubQuest("yaml-config", "y" * 100))
    check("different quest → different verdict", other != v1)


class _FakeProc:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _valid_envelope():
    """A clean CLI envelope carrying a parseable verdict, so a successful
    _invoke reaches _finalize without raising."""
    verdict = {"executed": True, "dimensions": {}, "commands": [],
               "recommendations": [], "summary": "ok"}
    return json.dumps({"result": verdict, "num_turns": 1, "total_cost_usd": 0.0})


def test_retry_policy():
    print("\nretry policy — transient blips self-heal, sustained ones stop the batch:")
    from agentic.runner import AuthError
    import tempfile as _tf

    orig_run = runner.subprocess.run
    orig_sleep = runner.time.sleep
    runner.time.sleep = lambda *_a, **_k: None  # no real waits in the test

    def _make_runner():
        # 3 attempts, ~0 backoff; pretend the claude CLI is on PATH.
        r = AgenticRunner(mode="execute", max_attempts=3,
                          retry_base_s=0.001, retry_max_s=0.001)
        r.available = lambda: True
        return r

    def _drive(procs):
        """Feed a queue of fake process results to a single _invoke call and
        return (result_or_exception, call_count)."""
        seq = list(procs)
        calls = {"n": 0}

        def fake_run(*_a, **_k):
            calls["n"] += 1
            return seq[min(calls["n"] - 1, len(seq) - 1)]

        runner.subprocess.run = fake_run
        r = _make_runner()
        q = _StubQuest("retry-probe", "x" * 200)
        sandbox = Path(_tf.mkdtemp(prefix="retry-test-"))
        try:
            return r._invoke(q, ["claude", "-p", "x"], sandbox), calls["n"]
        finally:
            import shutil as _sh
            _sh.rmtree(sandbox, ignore_errors=True)

    try:
        # 1) One transient (overload) blip, then a clean run → recovers, 2 calls.
        res, n = _drive([
            _FakeProc(returncode=1, stderr="API Error: 529 overloaded_error"),
            _FakeProc(returncode=0, stdout=_valid_envelope()),
        ])
        check("transient blip then success → recovers", isinstance(res, dict))
        check("recovered after exactly one retry (2 calls)", n == 2)

        # 2) Sustained rate-limit across all attempts → AuthError (stops the batch).
        raised = None
        try:
            _drive([_FakeProc(returncode=1, stderr="429 Too Many Requests")] * 5)
        except AuthError as e:
            raised = e
        check("sustained throttle → AuthError (batch-stop signal)", raised is not None)

        # 3) A CLEAN run whose transcript merely MENTIONS a 503 is a real result,
        #    never retried (guards the agent-transcript false-positive).
        env = json.loads(_valid_envelope())
        env["result"]["summary"] = "the tutorial covers 503 Service Unavailable and rate limit handling"
        res, n = _drive([_FakeProc(returncode=0, stdout=json.dumps(env))])
        check("clean run mentioning '503' is NOT retried", isinstance(res, dict) and n == 1)

        # 4) A non-transient hard error (exit 2, no transient/auth text) fails fast.
        raised = None
        try:
            _drive([_FakeProc(returncode=2, stderr="unexpected boom")] * 5)
        except RunnerError as e:
            raised = e
        check("non-transient error fails fast (RunnerError, no retry)",
              isinstance(raised, RunnerError) and not isinstance(raised, AuthError))
    finally:
        runner.subprocess.run = orig_run
        runner.time.sleep = orig_sleep


def main():
    print("=" * 64)
    print("AGENTIC ENVELOPE CONTRACT TEST (offline, no claude, no cost)")
    print("=" * 64)
    test_parse_envelope()
    test_extract_verdict()
    test_error_envelopes()
    test_snippet_extraction()
    test_schema_and_scoring()
    test_mock_determinism()
    test_retry_policy()
    print("\n" + "=" * 64)
    if _failures:
        print(f"❌ {len(_failures)} contract check(s) FAILED: {_failures}")
        return 1
    print("✅ All envelope/scoring contract checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
