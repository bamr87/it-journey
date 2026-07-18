---
title: 'Walkthrough — System Engineer · Level 1001 (Kubernetes Orchestration / Warrior)'
date: '2026-07-17T00:00:00.000Z'
character: system-engineer
level: '1001'
theme: Kubernetes Orchestration
tier: Warrior
quest_count: 5
mode: execute
overall_verdict: warn
session:
  window: '1 of 2 (quests 1–5 of 9)'
  average_score: 75.4
  verdicts: '2 pass · 2 warn · 1 fail'
  evidence: walk-evidence.json (sealed by workflow, execute mode)
  cost_usd: 3.7734
---

## 🎯 Session Summary

I walked a **5-quest window** (window 1 of 2; the level holds 9 quests total) of the **System Engineer** path at **Level 1001 — "Kubernetes Orchestration" (Warrior 🔥)**, as a learner following each quest end-to-end. Evidence comes from the sealed execute-mode engine run (`walk-evidence.json`), which sandboxed each quest and ran its safe snippets for real; my value-add is reasoning about the five as one linked journey.

**Headline verdict: ⚠️ warn.** Average score **75.4%** — two strong passes (Kubernetes Fundamentals 92, Codex Memory & State 97), two warns (Safe Execution 67, Memory Strategies 65) and one **fail** (Dev Environment Integration 56). The two bookend quests are genuinely excellent hands-on labs. The problem is concentrated in the middle three GH-600 agentic quests (Q6→Q7→Q8), which share three *repeating, verified* defects: a `scripts/validate_quest.py` "Quest Validation" command that does not exist (fails identically in Q6, Q7 **and** Q8), undefined cross-quest file dependencies (`copilot-instructions.md`, `run_agent_task.py`), and hollow/broken "do this" artifacts. A maintainer can fix most of the slice by addressing those three patterns once, across the chain.

A second, structural observation: this level's theme is **"Kubernetes Orchestration,"** yet **4 of the 5 quests are GH-600 agentic-AI content with no Kubernetes in them.** Only `kubernetes-fundamentals` matches the level name.

## 🗺️ The Journey

Walked in planner order (dependency-sorted):

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ✅ pass | Vaults of Recollection: Memory & State (Codex Ch. III) | 97 | Excellent local lab — every bash snippet reproduced its documented output byte-for-byte; only gap is the promised real-Actions exercise is never actually run. |
| 2 | ❌ fail | Bind the Agent to the Realm: Dev Environment Integration (Q6) | 56 | Its own parity script `check_agent_env.sh` can **never** pass because it checks for a `copilot-instructions.md` no exercise creates. |
| 3 | ⚠️ warn | The Shield of Retries: Safe Execution & Error Handling (Q7) | 67 | Retry/escalation logic is sound and verified, but the Ex 7.3 test is a hollow stub and the validation command fails outright. |
| 4 | ⚠️ warn | Vaults of Recollection: Agent Memory Strategies (Q8) | 65 | Sound model, but a `$(date)` in a quoted heredoc never expands and the validation command is again missing. |
| 5 | ✅ pass | Kubernetes Fundamentals: Container Orchestration Essentials | 92 | Unusually strong — a live `kind` cluster, self-healing demo, and `ImagePullBackOff` fix all reproduced exactly. |

## 🔬 Evidence

All outcomes below are from the sealed execute-mode engine run (`walk-evidence.json`); `reasoned` marks snippets judged statically (not runnable in the sandbox, e.g. GitHub Actions-only YAML). Outputs are quoted trimmed from the evidence.

### 1 · Codex Ch. III — Memory & State — 97 ✅ (ran 8, 7 passed / 1 failed; 6 reasoned)

- **Lab Step 1–5 (bash)** — all **passed**. The full drift-guard transcript reproduced
the quest's "Expected" block *byte-for-byte*: `Snapshot taken.` / `No drift — safe to act.` / `exit=0` / `README.md: FAILED` / `sha256sum: WARNING: 1 computed checksum did NOT match` / `::warning::Context drift detected…` / `exit=78`. Tier-2 plan/act emitted exactly `read`/`edit`/`verify`; Tier-3 JSONL register read back `local-1 → completed`; context-handoff produced `handoff fresh (0s old) — proceeding`.
- **Chapter-3 `drift-guard.sh` (WATCH includes `_config.yml`)** — **failed** in a scratch
dir (`sha256sum: _config.yml: No such file or directory`, exit 1). This is the *exact* failure the quest flags inline ("EDIT for YOUR repo — a missing file kills snapshot() under set -e"), so it is documented/intentional template behavior, not a defect.
- 4 workflow YAML blocks + the context-handoff JSON — **reasoned** (parse-valid;
  Actions-only pieces can't run in-sandbox, but their local analogues matched).

### 2 · Q6 — Dev Environment Integration — 56 ❌ (ran 4, 2 passed / 2 failed, 2 skipped; 1 reasoned)

- **`AGENTS.md` (Ex 6.1)** and **`devcontainer.json` (Ex 6.2)** — **passed** as written;
`npx @devcontainers/cli read-configuration` parsed the devcontainer, and `docker manifest inspect` confirmed both `mcr.microsoft.com/devcontainers/javascript-node:1-18-bullseye` and `ghcr.io/devcontainers/features/github-cli:1` resolve to real registry artifacts.
- **`check_agent_env.sh` (Ex 6.3)** — **failed**. Ran cleanly as a script but reported
  `Passed: 7 | Failed: 1`, exit 1, `❌ Environment not ready for agent use.` — because
its `check "copilot-instructions.md present" "test -f .github/copilot-instructions.md"` looks for a file **no exercise ever creates**.
- **Cold-start clone & Quest Validation** — **skipped**: `YOUR_ORG/YOUR_REPO` is a
  placeholder (intentional templating), and `scripts/validate_quest.py` is not present.
- Caveat surfaced by testing: `jq` / `python json.load` both reject the devcontainer file
  because of its leading `// .devcontainer/devcontainer.json` comment (JSONC, not strict JSON).

### 3 · Q7 — Safe Execution & Error Handling — 67 ⚠️ (ran 5, 4 passed / 1 failed; 2 reasoned)

- **`agent-with-retries.yml` retry loop** — **passed**. Simulated end-to-end against a
mock `run_agent_task.py`: transient error retried with 1s/2s backoff then succeeded on attempt 3 (exit 0); `auth_error` escalated immediately with no retry (exit 1); persistent errors exhausted 3 attempts and emitted `error_code=max_retries_exceeded`. All three documented behaviors verified. YAML passes `yamllint`; the error-report JSON schema is valid.
- **`test_failure_scenarios.sh` (Ex 7.3)** — recorded **passed** only in the sense that
the shell exited 0; the engine flags it as a **hollow stub** — every "scenario" is just an `echo` and a `# Mock a 503 response and verify…` comment; it never invokes the workflow, mocks a response, or asserts anything.
- **`python3 scripts/validate_quest.py --quest q7`** — **failed**: `python3: can't open
  file '.../scripts/validate_quest.py': [Errno 2] No such file or directory`.

### 4 · Q8 — Agent Memory Strategies — 65 ⚠️ (ran 2, 1 passed / 1 failed, 4 skipped; 1 reasoned)

- **`mkdir -p docs/agent-memory && touch …` (Ex 8.2)** — **passed**; all three files created.
- **`agent-with-session-memory.yml` (Ex 8.1)** — **reasoned**, with a *verified* bug:
after correctly accounting for YAML block-scalar dedent, the heredoc runs, but because the delimiter is quoted (`<< 'EOF'`), `"started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"` is **never expanded** — `session.json` literally stores the command string, not a timestamp.
- **`python3 scripts/validate_quest.py --quest q8`** — **failed** (same missing script as Q7).
- 4 markdown/config blocks (`copilot-instructions.md` snippets, learned-patterns example) — skipped (illustrative, not runnable).

### 5 · Kubernetes Fundamentals — 92 ✅ (ran 10, 10 passed, 2 skipped; 1 reasoned)

- **`kind create cluster --name citadel` → `kubectl cluster-info` / `get nodes`** —
  **passed**; node `Ready` after ~30s.
- **`hello-pod.yaml` apply / describe / logs / exec**, imperative `kubectl run
hello --image=nginx:1.27`, namespace workflow (`create namespace dojo` → apply → set context) — all **passed**.
- **Self-healing demo** — **passed**: after `kubectl delete pod hello-pod`, the bare Pod
  did **not** return, confirming the quest's central claim.
- **Advanced Challenge** — **passed**: `image: nginx:does-not-exist` reproduced
`ErrImagePull` → `ImagePullBackOff`, diagnosed via the Events pipeline, fixed to `nginx:1.27`, re-applied → `Running`.
- macOS `brew` / Windows `winget` install blocks — **skipped** (OS-gated on a Linux sandbox).

## 🐞 Issues Found

Concrete, evidence-backed problems. Severity per the rubric's learner-impact lens. Verified = a command actually ran in the sandbox; reasoned = judged from reading the sources + evidence across the chain.

- **HIGH · Q6 · Chapter 4 / `check_agent_env.sh` · verified** — Script always reports
  failure (`Passed: 7 | Failed: 1`, exit 1) because it checks for
`.github/copilot-instructions.md`, which **no exercise in the quest ever creates**. A learner who follows the quest exactly can never get a green environment check, gutting the whole validation chapter. *Fix:* add an exercise that creates `.github/copilot-instructions.md` (with sample content), or remove that check.
- **HIGH · Q7 · Quest Validation · verified** — `python3 scripts/validate_quest.py
--quest q7` fails with `No such file or directory`. *Fix:* ship the script, or replace with a runnable check (e.g. `actionlint .github/workflows/agent-with-retries.yml`), or clearly label the block as illustrative expected-output.
- **HIGH · Q7 · Chapter 4 / Exercise 7.3 · verified** — `test_failure_scenarios.sh` is an
echo-only stub; it fulfils the "Test failure recovery" objective on paper but tests nothing. *Fix:* replace with a real script that mocks each failure mode and asserts the retry-count / escalation output (the engine's sandbox did exactly this with a stub `run_agent_task.py`).
- **HIGH · Q8 · Chapter 3 / `session.json` `started_at` · verified** — `$(date …)` inside
the quoted `<< 'EOF'` heredoc never expands; the timestamp field is stored as the literal command string. *Fix:* unquote the delimiter for expanded fields, or compute `NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)` on a separate `run` line and interpolate `$NOW`.
- **HIGH · Q8 · Quest Validation · verified** — same missing `scripts/validate_quest.py`
  as Q7 (`No such file or directory`). *Fix:* provide the script or mark the block illustrative.
- **MEDIUM · Q7 · Chapter 2 workflow dependency · reasoned** — the workflow calls
`python3 work/gh-600/scripts/run_agent_task.py`, never defined in this quest and not produced by Q6 (which only creates `check_agent_env.sh`). Prerequisites don't call it out, so the workflow is unrunnable from the chain alone. *Fix:* state where it comes from, or include a minimal stub.
- **MEDIUM · Q6 · Chapter 5 / cold-start · verified+reasoned** — `AGENTS.md` calls
`GITHUB_TOKEN` a "fine-grained PAT" but the example uses `ghp_yourToken` (classic-PAT prefix; fine-grained is `github_pat_…`). Placeholder token also makes the check appear runnable when it isn't. *Fix:* reconcile the prefix and note the token must be real.
- **MEDIUM · Q8 · Chapter 2 objective · reasoned** — "Implement ephemeral memory" is only
prose about `copilot-instructions.md`; no concrete exercise/artifact, unlike the other two tiers. *Fix:* add a short worked example.
- **MEDIUM · Kubernetes Fundamentals · Chapter 2 · reasoned** — the object-model YAML is
never explicitly named; the filename `hello-pod.yaml` is only inferable from the later `kubectl apply -f hello-pod.yaml`. *Fix:* tell the learner to save it as `hello-pod.yaml`.
- **MEDIUM · Kubernetes Fundamentals · Windows path · reasoned** — `winget install -e
--id Kubernetes.kind` uses a package id the engine could not verify as real (kind's docs recommend Chocolatey / `go install` / binary download on Windows). *Fix:* verify or replace to avoid dead-ending Windows learners.
- **LOW · Q6 · devcontainer.json JSONC · verified** — leading `//` comment makes `jq`/
strict JSON linters reject the file even though `@devcontainers/cli` accepts it. *Fix:* drop the comment or add a one-line JSONC note.
- **LOW · Codex Ch. III · Prerequisites vs Lab · verified** — Prerequisites promise "you
will run real workflows that upload artifacts and commit files," but the lab is entirely local git/jq/sha256sum; real Actions is never exercised. *Fix:* add a minimal `workflow_dispatch` exercise or soften the prerequisite wording.
- **LOW · Q7 · jq fallback · verified** — `jq -r '.error_code // "unknown"'` yields an
  empty string (not `"unknown"`) when `agent-result.json` is absent entirely. *Fix:*
  guard with `[ -f agent-result.json ]` or `|| echo unknown`.
- **LOW · Q6/Q7/Q8 · Level metadata · reasoned** — filed under "Kubernetes Orchestration"
but contain zero Kubernetes; they are GH-600 / GitHub Actions content. *Fix:* reclassify under the GH-600 / agentic-CI track (see Chain Continuity).

No fabricated results: every "passed/failed" above is an engine-run command; everything labeled `reasoned` was judged from the source + evidence, not executed.

## 🔗 Chain Continuity

Reading the five in order as one learner, the slice is really **three overlapping tracks**, not one path — and the cross-quest seams are where the real problems live:

1. **The clean linear chain Q6 → Q7 → Q8** (dev-env → safe-execution → memory-strategies)
is well-wired by frontmatter (`required_quests`/`unlocks_quests`) and by `sub_title` ("Quest 1/3, 2/3, 3/3"). Ordering is correct and each quest's mermaid "Quest Network Position" agrees with its neighbors (Q5→Q6→Q7→Q8→Q9). **But three prerequisite/handoff gaps break the journey:**
   - **`copilot-instructions.md` is orphaned across the chain.** Q6's parity check
     *requires* `.github/copilot-instructions.md` (verified failure), and Q8 twice tells
     the learner to "update in `copilot-instructions.md`" — yet **no quest in the slice
     ever has the learner create that file**. Even a learner who completes the entire
     Q6→Q7→Q8 chain still cannot make Q6's own validation pass. This is the single
     highest-value fix: introduce the file once (logically in Q6) and the whole chain
     coheres.
   - **`run_agent_task.py` is assumed but never delivered.** Q7's headline workflow calls
     it; Q6 — the stated prerequisite — creates only `check_agent_env.sh`. The chain never
     provides the script the next link depends on.
   - **The `scripts/validate_quest.py` "Quest Validation" gate is broken in Q6, Q7 *and*
     Q8** (verified `FileNotFoundError` in Q7 and Q8; skipped-as-absent in Q6). Three
     consecutive quests end on a completion command that can't run — a repeated dead-end
     that a learner hits at the finish line of each.

2. **Codex Ch. III (quest 1) is a parallel "campaign" map**, not a step in the Q6→Q7→Q8
line. Its own network diagram is Codex Ch. II → III → IV (levels 1000→1001→1010), and it explicitly points at `agentic-memory-strategies` (Q8) as one of "the chambers" of Domain 3. So it *does* connect to Q8 — but it also **overlaps** it: both teach the three-tier memory model, and they disagree in a way a learner would notice. Codex Ch. III defines **Tier 2 / session = "one run, across jobs," artifacts**; Q8's table defines **Session = "Hours to days," artifacts + issue comments, persist across runs.** A learner reading both gets two different lifespans for "session memory." Worth reconciling so the map and the chamber agree. (Notably, Codex Ch. III is the far stronger, fully-runnable treatment; Q8 is the weaker duplicate.)

3. **Kubernetes Fundamentals (quest 5) is disconnected from the other four** — it is the
only quest that matches the level's "Kubernetes Orchestration" theme, and it stands alone as an excellent self-contained lab. The mismatch cuts both ways: the four agentic quests are mis-themed as Kubernetes, and the one true Kubernetes quest shares no chain with them. For a System Engineer learner arriving at "Level 1001 — Kubernetes," landing on four GitHub-Actions/agentic quests first would be disorienting.

**Net:** the slice does *not* yet hold together as one Kubernetes learning path. The Q6→Q7→Q8 sub-chain is close but blocked by the three shared gaps above; Codex Ch. III is a strong standalone that lightly conflicts with Q8; Kubernetes Fundamentals is a strong standalone under the wrong roommates.

## 🧠 Reasoning & Method

- **Mode: execute (sealed).** I did **not** run the engine — the workflow pre-computed and
sealed `walk-evidence.json` / `walk-evidence.md` (execute mode, real commands in a disposable sandbox: a live `kind` cluster, `docker manifest inspect`, `jq`/`sha256sum`, bash simulation of the retry loops and heredocs). I consumed that evidence as-is and never edited or regenerated it.
- **What is tested vs. reasoned.** Every `passed`/`failed` in §Evidence and the "verified"
issues came from a command the engine actually ran. GitHub-Actions-only YAML, cross-quest dependency gaps, the metadata/theme mismatch, and the Codex↔Q8 conceptual conflict are **reasoned** — inferred from reading all five sources in plan order plus the sealed evidence. They are labeled as such and not reported as executed results.
- **My contribution** is §Chain Continuity: the engine scores each quest in isolation, so
the orphaned `copilot-instructions.md`, the undelivered `run_agent_task.py`, the thrice-broken validation gate, and the two-tracks-under-one-theme structure are only visible when the five are read as one journey.
- **Coverage limits (honest):** (a) This is **window 1 of 2** — quests 6–9 of Level 1001
were **not** walked this run; the ledger accumulates them separately. (b) OS-gated install blocks (macOS `brew`, Windows `winget`) and real GitHub-Actions execution (artifact upload/download, live workflow triggers, real `git push`) could not run in the Linux sandbox and were reasoned/skipped, not executed. (c) The `winget Kubernetes.kind` package id and the GH-600 "19% of the exam" citation are external facts the sandbox could not verify. (d) I made **zero** content edits — fixable bugs live only in §Issues Found for a later content pass.
- **Confidence:** High on the per-quest verdicts (grounded in reproduced command output,
e.g. the byte-for-byte drift-guard transcript and the live `ImagePullBackOff` fix). High on the chain-continuity findings, which are directly traceable to quoted lines in the sources (`test -f .github/copilot-instructions.md`, `run_agent_task.py`, `scripts/validate_quest.py`, the two divergent session-memory tables).
