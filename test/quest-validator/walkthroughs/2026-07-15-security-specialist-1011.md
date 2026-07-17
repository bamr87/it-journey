---
title: "Quest Walkthrough — Security Specialist · Level 1011 (Security & Compliance)"
date: 2026-07-15T13:20:00.000Z
character: security-specialist
level: "1011"
theme: Security & Compliance
tier: Warrior
quest_count: 5
mode: execute
overall_verdict: fail
session:
  planner: walk-plan.json (windowed, index 0 of 3, size 5, offset 0, total_quests 12)
  evidence: walk-evidence.json (sealed by workflow; agentic execute engine)
  engine_cost_usd: 9.8309
  average_score: 61.2
  counts:
    pass: 1
    warn: 2
    fail: 2
  note: >-
    Evidence was pre-computed and sealed by the workflow's deterministic
    execute-mode engine step and consumed as-is — I did NOT re-run the engine.
    I then read all five quest sources in plan order and reasoned about them as
    one linked learner journey. No quest content was modified.
---

## 🎯 Session Summary

I walked the **Security Specialist → Level 1011 (Warrior 🔥 · "Security & Compliance")** slice as a learner would. This is a **windowed** slice: the planner selected the first 5 of 12 level-1011 quests (window 0 of 3), all `main_quest`. The machine evidence was sealed by the workflow's execute-mode engine (I consumed `walk-evidence.json`/`.md` verbatim — I did not run the engine); I then read each quest source and reasoned about them as a linked path.

**Headline verdict: FAIL for the slice as a walkable learning path** (avg **61.2%**; 1 pass · 2 warn · 2 fail). Two independent reasons:

1. **The slice is thematically split.** Only the first quest — *Security Fundamentals*
(score **81, pass**) — is genuinely on-theme for a Security Specialist, and it is solid: its Docker/Juice-Shop and SQL `GRANT` snippets all executed cleanly in the sandbox. The other four are **GH-600 "agentic" certification quests** (GitHub Copilot agent tuning + multi-agent orchestration/observability) that happen to carry the `1011` level tag. A learner arriving here for security content meets four quests about CI agent orchestration instead.
2. **The agentic chain shares a systemic, execution-confirmed blocker.** Every agentic
quest points the learner at a `scripts/validate_quest.py` that **does not exist in the repo** (the engine ran it and got *No such file or directory*), and each references Python/Bash helper scripts (`partition_task.py`, `run_subtask.py`, `aggregate_results.py`, `traced_subtask.py`) that are **never provided**. The chain therefore cannot be completed end-to-end from its own content.

## 🗺️ The Journey

Plan order (dependency-sorted window), with the sealed engine verdict per quest:

1. ✅ **Security Fundamentals: CIA Triad and Defense in Depth** — **81** · CIA/OWASP/defense-in-depth taught accurately; Docker + SQL snippets verified live; only defect is a `sha256sum --check` placeholder example that errors as written.
2. ❌ **Reforging the Agent's Mind: Tuning Behavior by Instruction** — **49** · Both runnable snippets fail: the baseline script aborts with no `gh` auth/repo context, and the stated validation command targets a nonexistent `validate_quest.py`.
3. ⚠️ **The Council of Many: Multi-Agent Coordination** — **72** · Excellent Hands-On Lab (8 snippets ran, 7 passed, output matched exactly); undercut by a Chapter 2 `jq sort_by(.event)` mis-order bug + unverifiable "GH-600 / Domain 5 / 17%" cert citations.
4. ❌ **The Council of Many: Multi-Agent Orchestration Patterns** — **42** · 0/4 runnable snippets passed: missing `validate_quest.py` and every referenced sub-agent script, an illegal `//` comment inside a JSON block, and the promised event-driven pattern never demonstrated.
5. ⚠️ **The Scribe's Codex: Observability in Multi-Agent Systems** — **62** · The two Python scripts + all three `jq` queries ran and verified end-to-end; but a confirmed `.json` vs `*.jsonl` extension mismatch silently produces an empty audit log, and `traced_subtask.py` is never defined.

## 🔬 Evidence

All outcomes below come from commands the sealed execute engine actually ran in the disposable sandbox (`mode: execute`, `executed: true` on every quest). Coverage is quoted as `ran/available_runnable`.

### 1. Security Fundamentals — 81 (pass) · ran 4/6 runnable (3 passed · 1 failed · 1 skipped · 4 reasoned)
- **PASSED** — `docker run --rm -d -p 3000:3000 bkimminich/juice-shop` pulled the real
image (`bkimminich/juice-shop:latest`, digest `sha256:e68144…`), started, and `docker ps` confirmed the container Up with port 3000 mapped exactly as described.
- **PASSED** — `sha256sum app-release.tar.gz` produced a valid hash for a test file.
- **PASSED** — all three Chapter 3 SQL statements ran against a fresh **MySQL 8.0.46**
server; `SHOW GRANTS` confirmed the `ALL PRIVILEGES` vs. scoped `SELECT/INSERT/UPDATE/DELETE` privilege sets match the quest's least-privilege claim.
- **FAILED** — `echo "EXPECTED_HASH  app-release.tar.gz" | sha256sum --check` run
verbatim → `sha256sum: 'standard input': no properly formatted checksum lines found` (exit 1), because `EXPECTED_HASH` is a literal placeholder. Substituting a real hash confirmed the pattern works (OK/FAILED). Learner-facing copy-paste defect.
- **REASONED/skipped** — macOS `brew`/Windows `winget` blocks (wrong OS), and the
`sudo apt install`/`systemctl` Linux path (sandbox denies `sudo`); the core `docker run` was independently verified via the Cloud Realms block. `curl` to `localhost:3000` was blocked by sandbox network policy (limitation, not a defect).

### 2. Reforging the Agent's Mind — 49 (fail) · ran 3/2 runnable (1 passed · 2 failed · 2 reasoned)
- **FAILED** — `work/gh-600/scripts/measure_agent_baseline.sh` (Ex 13.1) run as given
aborts at the first `gh run list --workflow=agent-task.yml` with `gh: … set the GH_TOKEN environment variable` (exit 4). No auth/repo precheck; `set -euo pipefail` means it dies before writing any partial result.
- **FAILED** — `python3 scripts/validate_quest.py --quest q13` →
  `can't open file '…/scripts/validate_quest.py': [Errno 2] No such file or directory`.
- **PASSED (reasoned)** — `bash -n` on the baseline script passes; its `gh` flags
(`--search`, `-q`, `--json`) are real/current. Logic is sound; only missing execution context (auth + a pre-existing `agent-task.yml` + prior PRs) makes it fail out of the box.

### 3. Multi-Agent Coordination — 72 (warn) · ran 8/4 runnable (7 passed · 1 failed · 2 reasoned)
- **PASSED** — Hands-On Lab Steps 1–3 (`mkdir`/`export CID`, the `trace()` function, 8
`trace()` calls, and the `jq` collect/stitch) ran verbatim and reproduced the quest's "Expected" block **line for line**.
- **PASSED** — all 4 YAML snippets parse as valid YAML (PyYAML + yamllint, cosmetic
  warnings only).
- **FAILED** — the Chapter 2 collect snippet
  `cat trace-*-"$cid"/*.jsonl | jq -s 'sort_by(.event) …'` produced silent empty output:
the `trace-*-$cid/` layout only exists after an unshown `actions/download-artifact@v4` step, and `sort_by(.event)` sorts **alphabetically** (done/error/handoff/start), not chronologically — tested output came back `done, done, start, start`, contradicting the prose that this "sort[s] by event order." (The Lab correctly uses an explicit `seq` field.)

### 4. Multi-Agent Orchestration Patterns — 42 (fail) · ran 4/1 runnable (0 passed · 4 failed · 1 reasoned)
- **FAILED** — `python3 scripts/validate_quest.py --quest q14` → *No such file or directory*.
- **FAILED** — the fan-out/chain YAML `run:` steps call `partition_task.py`,
`run_subtask.py`, `aggregate_results.py` — **none exist or are provided**; even on a real runner these fail identically.
- **FAILED** — the Chapter 4 JSON block fed to `json.load()` raises
`Expecting value: line 1 column 1` because of a leading `// work/gh-600/schemas/…` comment (JSON has no `//`). Stripped of it, the Draft-07 schema is valid and a sample instance validated with `jsonschema.validate`.
- **FAILED (reasoned)** — every `${{ }}` expression in both workflows appears in raw source
as `${% raw %}{{ … }}{% endraw %}`; the engine (reviewing raw markdown) judged this as broken GitHub Actions syntax. **See the render-pipeline nuance in §7 — I believe these strip to correct `${{ }}` on the rendered page.**

### 5. Observability in Multi-Agent Systems — 62 (warn) · ran 6/4 runnable (5 passed · 1 failed · 1 skipped · 2 reasoned)
- **PASSED** — `trace_writer.py` produces correct JSONL with all fields; `aggregate_traces.py`
correctly filters by correlation_id, sorts by timestamp, aggregates 4 events across 3 agents, and flags the 1 `failed` event. All three Chapter 4 `jq` queries produced exactly the documented output.
- **FAILED** — **confirmed cross-chapter bug:** the Chapter 1 workflow writes
`trace-analysis-$CORRELATION_ID.json`, but `aggregate_traces.py` only discovers files via `rglob("*.jsonl")`. In the sandbox a valid trace under a `.json` name caused the aggregator to report **"Found 0 trace files"** — silent data loss, no error.
- **REASONED/skipped** — `traced_subtask.py` (invoked by the Ch1 workflow) is never provided,
so the workflow can't run even in real CI; `validate_quest.py` reasonably skipped as a platform-level script not present in-sandbox.

> Machine totals (from `walk-evidence.md`): **5 quests · 1 pass · 2 warn · 2 fail · avg 61.2% · ~$9.83**.

## 🐞 Issues Found

**Systemic (repeat across the agentic chain):**

- **HIGH · behavior-tuning, orchestration-patterns, observability, (failure-recovery) · Quest
Validation section** — the stated completion command `python3 scripts/validate_quest.py …` targets a script that **does not exist in the repository** (confirmed: `ls scripts/validate_quest.py` → not found; referenced by 4 level-1011 agentic quests). *Fix:* ship the validator (or point to its real location), or replace it with a manual self-check checklist that doesn't imply an external tool the learner lacks.
- **HIGH · orchestration-patterns, observability, behavior-tuning · referenced helper scripts
never provided** — `partition_task.py`, `run_subtask.py`, `aggregate_results.py`, `traced_subtask.py`, and the auth/context around `measure_agent_baseline.sh` are called but never written/scaffolded. Workflows fail with *No such file or directory* even on real CI. *Fix:* include the implementations (or clearly labeled stubs + a spec/starter template) and add prerequisites (`gh auth login`, an existing `agent-task.yml`, at least one prior run/PR).

**Per-quest:**

- **LOW→MEDIUM · security-fundamentals · Chapter 3, `sha256sum --check`** — `echo "EXPECTED_HASH
  … " | sha256sum --check` errors on the literal placeholder instead of demonstrating a
mismatch (verified: exit 1). *Fix:* use a real/sample hash or a code comment flagging `EXPECTED_HASH` as a replace-me placeholder.
- **LOW · security-fundamentals · Cloud-Realms safety warning placement** — the "only run
vulnerable apps on isolated/throwaway environments" warning sits only inside the collapsed Cloud section, not in the macOS/Windows/Linux sections that launch the same Juice Shop. *Fix:* repeat the warning in each platform block.
- **LOW · security-fundamentals · content freshness** — quest asserts "the current edition is
the OWASP Top 10:2021"; as of 2026-07-15 this should be re-verified against owasp.org (engine could not confirm — no network). `reasoned`, not tested.
- **HIGH · behavior-tuning · Ex 13.1 baseline script** — aborts immediately without `GH_TOKEN`/
repo context and no guard rails. *Fix:* add prerequisite checks + degrade gracefully instead of `set -e` aborting on a fresh repo.
- **MEDIUM · behavior-tuning · Ex 13.2 + objectives 2 & 4** — the iteration-log exercise has no
target file path (unlike 13.1/13.3), and "select top-2 failure patterns" + "re-measure and compare" are narrated but never become concrete exercises. *Fix:* add the path comment and turn both objectives into real steps.
- **HIGH · coordination · Chapter 2 collect snippet** — `sort_by(.event)` scrambles chronological
order and the glob assumes an unshown `download-artifact` step (both demonstrated). *Fix:* add a `seq`/timestamp field and sort on it; add the missing download step.
- **MEDIUM · coordination, orchestration-patterns · unverifiable cert citations** — "GH-600",
"Domain 5", "17% of the exam", sub-skills 5.1–5.4 could not be corroborated (known GitHub certs use GH-100/200/300/500). *Fix:* verify against the live Microsoft Learn study guide before publish.
- **MEDIUM · orchestration-patterns · Chapter 4 JSON block** — leading `//` comment breaks
  `json.load()` (confirmed). *Fix:* move the path hint into prose or use a JSONC-aware fence.
- **MEDIUM · orchestration-patterns · missing event-driven example** — Objective 1 + the Chapter 1
  table promise `workflow_run`/`repository_dispatch`, but only fan-out and chain are ever worked.
- **HIGH · observability · Ch1↔Ch3 extension mismatch** — `.json` output vs `*.jsonl` glob →
  silent empty audit log (confirmed). *Fix:* align on `.jsonl` or glob both.
- **MEDIUM (needs render verification) · orchestration-patterns (15 lines), observability (5) ·
`{% raw %}` leakage** — engine flagged `${% raw %}{{ … }}{% endraw %}` as broken copy-paste in raw source. See §7: this likely renders to correct `${{ … }}` — verify against built HTML before treating as a real learner defect. Coordination uses the correct block form and was not flagged.

**Celebrated result:** *Security Fundamentals* has **no blocking issues** — its hands-on core (Docker Juice Shop + MySQL `GRANT` least-privilege demo) executed cleanly and matched the quest's claims exactly.

## 🔗 Chain Continuity

Reading the five sources in plan order, as a learner carrying prior state forward:

- **The slice is two unrelated tracks.** *Security Fundamentals* is standalone
(`required_quests: []`) and unlocks security sequels (secure-coding, threat-modeling, pen-testing, compliance). The other four are the **GH-600 "Agentic" certification** line (Domain 4 "Evaluating Agent Performance" + Domain 5 "Multi-Agent Systems"). They form their own dependency chain and have nothing to do with the CIA triad. A Security Specialist landing on level 1011 for "Security & Compliance" gets one security quest, then four CI-agent quests — a **coherence gap for the character path** (reasoned; flagged for a curriculum decision, not a code fix).
- **Prerequisite leaks outside the window.** The first agentic quest, *behavior-tuning*
(`Quest 1/4`), lists `required_quests: /quests/1010/agentic-failure-root-cause-analysis/` — a **level-1010** quest not in this slice — and its baseline script assumes `gh` auth plus an `agent-task.yml` workflow and prior agent PRs that only exist if the learner did earlier quests. A learner walking only this window hits a wall on the very first agentic step (confirmed: the script aborts).
- **Plan order ≠ narrative chain.** By frontmatter deps the linear agentic path is
`behavior-tuning → orchestration-patterns → observability` (each `required_quests` the prior, `unlocks` the next). The planner placed *coordination* (the "Agentic Codex 05" retelling) at position 3, between them — it's a **parallel** treatment of the same Domain 5 material, not a link in that chain. Both cover Domain 5, so the sequencing isn't harmful, but a learner following the in-quest "Prerequisites/Next" links would take a different route than the plan order.
- **The chain compounds one blocker.** Because `validate_quest.py` and the sub-agent scripts are
missing in *every* agentic quest, the "measure → tune → orchestrate → observe" arc never reaches a green validation. Quest N never leaves the learner with a working, verifiable artifact for N+1 to build on — the observability aggregator can't ingest the orchestration output, and the orchestration validation can't run at all.
- **Real cross-chapter data-flow bugs** (both execution-confirmed) reinforce that these quests were
authored chapter-by-chapter without an end-to-end run: coordination's `sort_by(.event)` + missing download step, and observability's `.json`/`*.jsonl` mismatch. Each silently "succeeds" (exit 0, empty output), which is the worst failure mode for a beginner — no error to debug.

## 🧠 Reasoning & Method

- **What ran vs. what I reasoned about.** All per-command `passed`/`failed` outcomes come from the
**sealed execute-mode evidence** (`walk-evidence.json`, `executed: true` on all 5 quests, ~$9.83, MySQL 8.0.46 + real Docker pulls in a disposable sandbox). I consumed that evidence **as-is** — I did not re-run the engine (its child `claude` processes can't authenticate from my Bash tool). My own tool use was **read-only corroboration** of source-level facts the report leans on: confirming `scripts/validate_quest.py` is absent, counting `{% raw %}` lines (0/6/15/5 across the agentic quests), locating the undefined helper scripts, and reading each quest's frontmatter/dependency chain. Those are labeled where they inform an issue.
- **The `{% raw %}` nuance (important, honest caveat).** The engine reviewed **raw markdown** and
flagged `${% raw %}{{ … }}{% endraw %}` as broken Actions syntax. My reasoned read: `{% raw %}` is Jekyll's standard escape and is stripped at render, so `${% raw %}{{ x }}{% endraw %}` → `${{ x }}` on the published page — i.e. a **source-review artifact, not necessarily a learner-facing break** for someone copying from the rendered site. Coordination's use of the correct block form (and its clean YAML verdict) supports this. I did **not** render the pages (`make build-ci`) in this session, so I cannot certify it — I've marked the issue "needs render verification" rather than assert it either way. A content pass should confirm against built HTML.
- **Coverage/limits.** This is **window 0 of 3** — 5 of the level's 12 quests; the remaining 7
await later runs (the perfection ledger accumulates coverage). `sudo` and outbound network were denied by sandbox policy, so the Linux `apt`/`systemctl` path and the Juice-Shop HTTP check were reasoned, not run (noted inline; not counted against the quests). OS-specific macOS/Windows blocks were statically reviewed only.
- **Confidence.** High on the executed findings (missing scripts, `sha256sum` placeholder, the
`.json`/`.jsonl` and `sort_by(.event)` bugs — all reproduced live). Medium on the cert-citation and OWASP-edition freshness items (network-blocked, `reasoned`). Medium on the `{% raw %}` severity pending a render check. The thematic-split observation is a curriculum judgment, offered for a maintainer decision, not a defect claim.

*One slice, one report. No quest content was modified; git is left to the workflow.*
