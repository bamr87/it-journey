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

    def objectives(self):
        return []


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

        # 2) Sustained rate-limit across all attempts → ThrottleError. Still an
        #    AuthError subclass (batch-stop), but the orchestrator must be able to
        #    tell "wait for the window to refill" from "a human must rotate the
        #    token" — conflating them is what mislabeled 8 days of dead-token runs
        #    as an expected rate-limit.
        raised = None
        try:
            _drive([_FakeProc(returncode=1, stderr="429 Too Many Requests")] * 5)
        except AuthError as e:
            raised = e
        check("sustained throttle → AuthError (batch-stop signal)", raised is not None)
        check("sustained throttle is the ThrottleError flavor",
              isinstance(raised, runner.ThrottleError))

        # 2b) Sustained CREDENTIAL failure → plain AuthError, never ThrottleError.
        raised = None
        try:
            _drive([_FakeProc(returncode=1,
                              stderr="OAuth token has expired · Please run /login")] * 5)
        except AuthError as e:
            raised = e
        check("dead token → AuthError, NOT ThrottleError",
              raised is not None and not isinstance(raised, runner.ThrottleError))

        # 2c) Subscription-window exhaustion phrasing is throttle, not auth.
        raised = None
        try:
            _drive([_FakeProc(returncode=1,
                              stderr="Claude AI usage limit reached · resets 3am")] * 5)
        except AuthError as e:
            raised = e
        check("usage-limit-reached → ThrottleError (refills on its own)",
              isinstance(raised, runner.ThrottleError))

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


def test_preflight():
    print("\npreflight — auth-state probe the workflow gates route on:")
    orig_run = runner.subprocess.run
    orig_sleep = runner.time.sleep
    runner.time.sleep = lambda *_a, **_k: None

    def _probe(procs):
        seq = list(procs)
        calls = {"n": 0}

        def fake_run(*_a, **_k):
            calls["n"] += 1
            return seq[min(calls["n"] - 1, len(seq) - 1)]

        runner.subprocess.run = fake_run
        r = AgenticRunner(mode="review", max_attempts=2,
                          retry_base_s=0.001, retry_max_s=0.001)
        r.available = lambda: True
        return r.preflight()

    try:
        check("mock mode → ok without any probe",
              AgenticRunner(mode="review", mock=True).preflight()[0] == "ok")
        missing = AgenticRunner(mode="review", claude_bin="claude-definitely-not-here")
        check("missing CLI → unknown (fail-open, never a false auth verdict)",
              missing.preflight()[0] == "unknown")
        check("clean exit → ok",
              _probe([_FakeProc(returncode=0, stdout='{"result":"ok"}')])[0] == "ok")
        check("sustained 429 → throttled",
              _probe([_FakeProc(returncode=1, stderr="429 Too Many Requests")] * 3)[0]
              == "throttled")
        check("invalid key → auth",
              _probe([_FakeProc(returncode=1,
                                stderr="Invalid API key · Please run /login")] * 3)[0]
              == "auth")
        check("novel error → unknown (fail-open)",
              _probe([_FakeProc(returncode=1, stderr="segfault in flux capacitor")])[0]
              == "unknown")
        check("blip then clean → ok (retry inside the probe)",
              _probe([_FakeProc(returncode=1, stderr="529 overloaded"),
                      _FakeProc(returncode=0, stdout='{"result":"ok"}')])[0] == "ok")
    finally:
        runner.subprocess.run = orig_run
        runner.time.sleep = orig_sleep


class _Env:
    """Temporarily set (or, with None, unset) environment variables."""
    def __init__(self, **kv):
        self.kv, self.saved = kv, {}

    def __enter__(self):
        import os
        for k, v in self.kv.items():
            self.saved[k] = os.environ.get(k)
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def __exit__(self, *_exc):
        import os
        for k, v in self.saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def test_auth_order_and_fallback():
    print("\nauth — OAuth preferred, one credential per call, a refused one hands over:")
    from agentic.runner import AuthError, ThrottleError
    import shutil as _sh
    import tempfile as _tf

    O, K = "CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_API_KEY"
    both = {O: "oauth-test-value", K: "apikey-test-value"}

    check("both present → oauth, then api_key",
          runner.auth_order(both) == ["oauth", "api_key"])
    check("blank secrets (unset GitHub secrets) count as absent",
          runner.auth_order({O: "", K: "  "}) == [])
    check("only the key → api_key", runner.auth_order({K: "k"}) == ["api_key"])
    check("AI_AUTH_ORDER can flip the order",
          runner.auth_order({**both, "AI_AUTH_ORDER": "api_key,oauth"}) == ["api_key", "oauth"])
    check("QUEST_QA_AUTH_ORDER wins over AI_AUTH_ORDER",
          runner.auth_order({**both, "AI_AUTH_ORDER": "api_key",
                             "QUEST_QA_AUTH_ORDER": "oauth"}) == ["oauth"])
    e_o = runner.child_env("oauth", both)
    e_k = runner.child_env("api_key", both)
    e_a = runner.child_env("ambient", both)
    check("an oauth call never sees the API key", O in e_o and K not in e_o)
    check("an api_key call never sees the OAuth token", K in e_k and O not in e_k)
    check("an ambient call sees neither", O not in e_a and K not in e_a)
    check("a blank OAuth secret is stripped",
          O not in runner.child_env("api_key", {O: "", K: "k"}))

    orig_run, orig_sleep = runner.subprocess.run, runner.time.sleep
    runner.time.sleep = lambda *_a, **_k: None
    seen = []

    def _script(by_method):
        """Answer each call by the credential its env carries, and record it."""
        def fake_run(*_a, env=None, **_k):
            m = "oauth" if O in env else ("api_key" if K in env else "ambient")
            seen.append(m)
            return by_method[m]
        seen.clear()
        runner.subprocess.run = fake_run

    def _runner():
        r = AgenticRunner(mode="review", max_attempts=2,
                          retry_base_s=0.001, retry_max_s=0.001)
        r.available = lambda: True
        return r

    def _invoke(r):
        sandbox = Path(_tf.mkdtemp(prefix="auth-test-"))
        try:
            return r._invoke(_StubQuest("auth-probe", "x" * 200), ["claude", "-p", "x"], sandbox)
        finally:
            _sh.rmtree(sandbox, ignore_errors=True)

    def _raises(r):
        try:
            _invoke(r)
        except AuthError as e:
            return e
        return None

    ok = _FakeProc(returncode=0, stdout=_valid_envelope())
    probe_ok = _FakeProc(returncode=0, stdout='{"result":"ok"}')
    secret = "sk-" + "ant-" + "api03-" + "Z" * 16   # built at runtime: no literal key in the repo
    dead_key = _FakeProc(returncode=1, stdout=json.dumps({
        "is_error": True, "subtype": "error",
        "result": f"Credit balance is too low ({secret})"}))
    dead_oauth = _FakeProc(returncode=1, stderr="OAuth token has expired · Please run /login")
    clear_order = {"AI_AUTH_ORDER": None, "QUEST_QA_AUTH_ORDER": None}

    try:
        with _Env(**both, **clear_order):
            _script({"oauth": ok, "api_key": dead_key})
            res = _invoke(_runner())
            check("healthy OAuth + dead key → OAuth alone serves it (the PR #933 failure)",
                  isinstance(res, dict) and seen == ["oauth"] and res["meta"]["auth"] == "oauth")

            _script({"oauth": dead_oauth, "api_key": ok})
            r = _runner()
            res = _invoke(r)
            check("refused OAuth falls back to the key",
                  isinstance(res, dict) and res["meta"]["auth"] == "api_key")
            check("…only after OAuth's own retries (oauth ×2, then the key)",
                  seen == ["oauth", "oauth", "api_key"])
            seen.clear()
            _invoke(r)
            check("…and the refused OAuth is skipped for the rest of the batch",
                  seen == ["api_key"])

            _script({"oauth": dead_oauth, "api_key": dead_key})
            e = _raises(_runner())
            check("both refused → AuthError, not ThrottleError",
                  e is not None and not isinstance(e, ThrottleError))
            check("…naming both credentials",
                  e is not None and [m for m, _, _ in e.failures] == ["oauth", "api_key"])
            check("…with the CLI's own words in the reason",
                  e is not None and "Credit balance is too low" in e.reason
                  and "expired" in e.reason)
            check("…and never the secret itself",
                  e is not None and secret not in str(e) and secret not in e.reason)

            _script({"oauth": _FakeProc(returncode=1,
                                        stderr="Claude AI usage limit reached · resets 3am"),
                     "api_key": dead_key})
            e = _raises(_runner())
            check("OAuth window spent + dead key → ThrottleError (the window refills)",
                  isinstance(e, ThrottleError) and seen[-1] == "api_key")

            _script({"oauth": _FakeProc(returncode=1, stderr="API Error: 529 overloaded_error"),
                     "api_key": ok})
            e = _raises(_runner())
            check("a backend overload does NOT switch credential",
                  isinstance(e, ThrottleError) and "api_key" not in seen)

            _script({"oauth": dead_oauth, "api_key": probe_ok})
            status, detail = _runner().preflight()
            check("preflight: refused OAuth + working key → ok via api_key, refusal named",
                  status == "ok" and "via api_key" in detail and "oauth" in detail)

            _script({"oauth": probe_ok, "api_key": dead_key})
            status, detail = _runner().preflight()
            check("preflight: healthy OAuth → ok via oauth, the key is never touched",
                  status == "ok" and "via oauth" in detail and seen == ["oauth"])

            _script({"oauth": dead_oauth, "api_key": dead_key})
            status, detail = _runner().preflight()
            check("preflight: both refused → auth, with both reasons",
                  status == "auth" and "oauth:" in detail and "api_key:" in detail
                  and secret not in detail)

        with _Env(**{O: None, K: None}, **clear_order):
            _script({"ambient": ok})
            res = _invoke(_runner())
            check("no credential in the env → one ambient call (the local login)",
                  isinstance(res, dict) and seen == ["ambient"])
    finally:
        runner.subprocess.run, runner.time.sleep = orig_run, orig_sleep


def test_truncation_banner():
    print("\nreport — an incomplete run says so instead of rendering an empty table:")
    from agentic import report as _report

    agg = _report.aggregate([])
    agg.update(truncated=True, evaluated=0, requested=7, truncation_reason="auth",
               truncation_detail="oauth: token expired; api_key: error: Credit balance is too low",
               auth_method=None)
    md = _report.render_markdown(agg)
    check("banner says the review is incomplete (0/7)", "Incomplete review — evaluated 0/7" in md)
    check("banner blames the credential, not the quests", "credential problem" in md)
    check("banner carries the CLI's reason", "Credit balance is too low" in md)
    check("no empty results table", "| Score |" not in md)

    full = _report.aggregate([])
    full["auth_method"] = "oauth"
    md2 = _report.render_markdown(full)
    check("a complete run has no banner", "Incomplete review" not in md2)
    check("the headline names the credential that served it", "auth: `oauth`" in md2)


def test_turn_budget_and_exhaustion():
    print("\nturn budgets — adaptive sizing + budget-exhausted becomes a SCORED fail:")
    import types
    from agentic import prompts

    # --- adaptive sizing (deterministic from the runnable-snippet count) -----
    fake_lib = types.SimpleNamespace(
        snippet_summary=lambda body: {"total": 99, "runnable": int((body or "0").split(":")[-1])})
    orig_lib = runner.quest_lib
    runner.quest_lib = fake_lib
    try:
        r = AgenticRunner(mode="execute", max_turns=40, adaptive_turns=True)
        check("adaptive: tiny quest floors at 16",
              r._turn_budget(_StubQuest("t", "runnable:0")) == 16)
        check("adaptive: mid quest = 14 + 3×runnable",
              r._turn_budget(_StubQuest("t", "runnable:5")) == 29)
        check("adaptive: heavy quest caps at max_turns",
              r._turn_budget(_StubQuest("t", "runnable:50")) == 40)
        fixed = AgenticRunner(mode="execute", max_turns=40)
        check("fixed mode ignores snippet count",
              fixed._turn_budget(_StubQuest("t", "runnable:1")) == 40)
        uncapped = AgenticRunner(mode="execute", max_turns=0, adaptive_turns=True)
        check("no cap → no flag (0)", uncapped._turn_budget(_StubQuest("t", "runnable:5")) == 0)
    finally:
        runner.quest_lib = orig_lib

    # --- the budget number reaches the agent's prompt (execute mode only) ----
    q = _StubQuest("paced", "```bash\necho hi\n```")
    up = prompts.build_user_prompt(q, mode="execute", turn_budget=29)
    check("execute prompt states the turn budget", "at most 29 tool turns" in up)
    check("review prompt carries no budget block",
          "tool turns" not in prompts.build_user_prompt(q, mode="review", turn_budget=29))

    # --- error_max_turns → scored fail, not an errored void ------------------
    orig_run = runner.subprocess.run
    runner.subprocess.run = lambda *_a, **_k: _FakeProc(
        returncode=0,
        stdout=json.dumps({"is_error": True, "subtype": "error_max_turns",
                           "result": "Reached maximum number of turns",
                           "num_turns": 40, "total_cost_usd": 0.1}))
    try:
        r = AgenticRunner(mode="execute", max_turns=40)
        r.available = lambda: True
        import tempfile as _tf, shutil as _sh
        sandbox = Path(_tf.mkdtemp(prefix="budget-test-"))
        try:
            res = r._invoke(_StubQuest("heavy", "x" * 100), ["claude", "-p", "x"], sandbox)
        finally:
            _sh.rmtree(sandbox, ignore_errors=True)
        check("budget-exhausted result carries no error key", "error" not in res)
        check("…is flagged budget_exhausted", res.get("budget_exhausted") is True)
        check("…scores 0.0 with verdict fail",
              res.get("overall") == 0.0 and res.get("verdict") == schema.VERDICT_FAIL)
        check("…is clearly harness-labeled",
              "[harness]" in (res.get("verdict_obj") or {}).get("summary", ""))
        recs = (res.get("verdict_obj") or {}).get("recommendations") or []
        check("…carries the split-the-quest recommendation",
              len(recs) == 1 and recs[0].get("priority") == "high")
        from agentic import report as _report
        agg = _report.aggregate([res])
        check("…counts as SCORED in the aggregate (ledger coverage completes)",
              agg["scored"] == 1 and agg["errored"] == 0)
    finally:
        runner.subprocess.run = orig_run


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
    test_preflight()
    test_auth_order_and_fallback()
    test_truncation_banner()
    test_turn_budget_and_exhaustion()
    print("\n" + "=" * 64)
    if _failures:
        print(f"❌ {len(_failures)} contract check(s) FAILED: {_failures}")
        return 1
    print("✅ All envelope/scoring contract checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
