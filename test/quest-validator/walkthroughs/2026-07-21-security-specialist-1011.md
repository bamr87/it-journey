---
title: 'Walkthrough — Security Specialist · Level 1011 (Security & Compliance / Warrior)'
date: '2026-07-21T00:00:00.000Z'
character: security-specialist
level: '1011'
theme: Security & Compliance
tier: Warrior
quest_count: 5
mode: execute
overall_verdict: fail
session: >-
  Windowed slice (window 1 of 3, 5 of 12 quests) walked end-to-end from
  pre-sealed agentic execute-engine evidence plus a learner read of every quest
  source in plan order. Two Hard quests carry blocking, learner-stopping bugs
  (copy-paste-broken workflow YAML; a baseline script that reports success while
  writing nothing). Evidence was minted deterministically by the workflow and
  consumed as-is — not re-run, not edited.
---

## 🎯 Session Summary

- **Character / path:** 🛡️ Security Specialist
- **Level:** 1011 — *Security & Compliance*, Warrior tier (🔥)
- **Quests walked:** 5 of 12 (windowed slice, window index 0 of 3; `stats.windowed = true`)
- **Mode:** `execute` — engine evidence pre-computed and **sealed** by the workflow, then read alongside every quest source as a learner would.
- **Headline verdict:** ❌ **FAIL** — avg score **68.8%**, split **2 pass · 1 warn · 2 fail**.

Quest 1 (`security-fundamentals`) is a genuinely good conceptual security quest and passes cleanly. The other four are all **GH-600 "Agentic Codex" quests** — DevOps/AI-ML material that happens to share the `1011` level code but belongs to a different quest line and skill focus than a Security Specialist expects here. Two of them are **blocking-broken as written**: `agentic-multi-agent-orchestration-patterns` ships workflow YAML corrupted by leaked Jekyll `{% raw %}` tags inside every `${{ }}` expression (confirmed by execution) plus three referenced Python scripts that don't exist, and `agentic-behavior-tuning` has a baseline script that prints `✅ Baseline recorded` while silently failing to write its output file, leaving its own validation unsatisfiable in a fresh environment. A maintainer should treat those two as the priority fixes; the middle survey quest (`agentic-codex-05`) is the strongest of the chain and actually works.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:---:|---|--:|---|
| 1 | ✅ pass | Security Fundamentals: CIA Triad and Defense in Depth | 81 | Solid, accurate conceptual quest; runnable lab + checksum both worked. Gaps are pedagogical (Risk Mgmt promised-not-taught, buried safety warning). |
| 2 | ❌ fail | Reforging the Agent's Mind: Tuning Behavior by Instruction | 55 | Baseline script reports success while writing nothing; validation can't pass without un-bootstrapped live-repo infra. |
| 3 | ✅ pass | The Council of Many: Multi-Agent Coordination | 87 | Strongest quest — trace lab + all YAML ran and matched expected output exactly. One reasoned semantics doubt on the escalate pattern. |
| 4 | ❌ fail | The Council of Many: Multi-Agent Orchestration Patterns | 45 | Copy-paste-broken: leaked `${% raw %}{{…}}{% endraw %}` in every expression + 3 missing scripts. Self-check goes green on a non-functional deliverable. |
| 5 | ⚠️ warn | The Scribe's Codex: Observability in Multi-Agent Systems | 76 | Scripts + jq all run and produce correct output, but the workflow calls an undefined script and the pipeline is never wired end-to-end. |

## 🔬 Evidence

All command outcomes below come from the sealed `walk-evidence.json` execute run (sandboxed, real commands). Items I only judged from reading the source are labelled **reasoned**.

### 1. `security-fundamentals.md` — 81, ✅ pass · ran 3/6 runnable snippets

- `docker run --rm -d -p 3000:3000 bkimminich/juice-shop` — **passed**. Image pulled, container started; `docker logs` showed `info: Server listening on port 3000`.
- `sha256sum app-release.tar.gz` — **passed**. Produced a valid 64-char digest.
- `echo "EXPECTED_HASH  app-release.tar.gz" | sha256sum --check` — **passed**. Matching hash → `OK`; deliberately wrong hash → `FAILED` + WARNING + non-zero exit, exactly as the quest describes.
- macOS `brew install --cask docker`, Windows `winget install Docker.DockerDesktop`, Linux `sudo apt install docker.io` — **skipped** (Linux sandbox, no sudo/brew/winget). Package IDs verified correct by static review.
- OWASP mapping block, 7-layer defense diagram, `GRANT` least-privilege example — **reasoned**. OWASP Top 10:2021 mappings and MySQL GRANT syntax verified correct; no DB provisioned to run the SQL live.

### 2. `agentic-behavior-tuning.md` — 55, ❌ fail · ran 2/2 runnable (both failed)

- `work/gh-600/scripts/measure_agent_baseline.sh` (Exercise 13.1) — **failed**. Run verbatim in a fresh repo with `gh` installed but unauthenticated (the realistic first-time-learner state): exited `0`, printed `✅ Baseline recorded in work/gh-600/baseline-results.jsonl`, **but the file was never created** (`test -f …` fails). Root cause: the `continue` in the no-`RUN_ID` branch skips the heredoc write for all 3 tasks, yet the final success `echo` is unconditional.
- Quest Validation self-check — **failed**. Run verbatim: after the tester manually authored the Ch.3/4 files, 2 of 3 checks printed ✅ (iteration log, changelog); the baseline check stayed silent/❌ because `baseline-results.jsonl` never existed.
- Mermaid diagram, Ex 13.2 iteration template, Ch.4 CHANGELOG template — **reasoned**. Valid markdown, but the quest gives no explicit shell command to create the files; the engine had to infer and hand-create them.

### 3. `agentic-codex-05-multi-agent-coordination.md` — 87, ✅ pass · ran 7 (all passed)

- Hands-On Lab Steps 1–3 (`mkdir`, `trace()`, 8 trace calls, `jq -s 'sort_by(.seq)'`) — **passed**. Output matched the quest's documented "Expected" block **line-for-line**, including the seeded empty handoff at seq 5.
- Ch.2 correlation-ID excerpt (JSONL + `$GITHUB_STEP_SUMMARY`) — **passed**. Correct JSONL and `### backend agent — run <cid>` summary.
- Ch.2 collect step (`cat … | jq -s 'sort_by(.ts)'`) — **passed**, with a caveat surfaced: `sort_by(.ts)` is a *string* sort; only safe here because `date -u +%s.%N` yields fixed-width epoch seconds.
- `_data/agents.yml`, `council-fanout.yml`, correlation-ID YAML — **passed/reasoned** (parse cleanly via `yaml.safe_load`).
- Ch.3 `continue-on-error: true` + `recover` `if: failure()` escalate — **reasoned**. Not runnable offline; per documented GitHub Actions semantics a job-level `continue-on-error: true` job reports **success** to `needs`-dependents, so `if: failure()` likely never fires. This is *also literally the Mastery Challenge requirement*.

### 4. `agentic-multi-agent-orchestration-patterns.md` — 45, ❌ fail · ran 6 (3 passed, 3 failed)

- Write `orchestrator-fan-out.yml` / `orchestrator-chain.yml` — **failed**. Files parse as YAML but every `${{ }}` expression is corrupted into a literal string by interleaved Jekyll tags, e.g. `outputs.subtasks == '${% raw %}{{ steps.plan.outputs.subtasks }}{% endraw %}'`. I confirmed this directly in the source (line 124 and throughout Ch.2/Ch.3): GitHub Actions only evaluates `${{ … }}`, so these expressions never fire. Copy-pasting the quest breaks outputs, `matrix.subtask`, and every `needs.*.outputs.*`.
- `python3 work/gh-600/scripts/partition_task.py …` — **failed**: `No such file or directory`. `partition_task.py`, `run_subtask.py`, `aggregate_results.py` are referenced by the workflows but **never provided** anywhere in the quest.
- `mkdir -p …`, write `sub-agent-contract.json`, Quest Validation self-check — **passed**. The JSON schema is valid draft-07. **But** the self-check prints all three ✅ purely on file-presence, so a learner sees full green on a non-functional pipeline.

### 5. `agentic-multi-agent-observability.md` — 76, ⚠️ warn · ran 5 (all passed), 1 skipped

- `CORRELATION_ID=task-42-999 python3 …/trace_writer.py` — **passed**. Correct `[TRACE]` lines + valid JSONL.
- `aggregate_traces.py --traces-dir traces …` — **passed**. Filtered by correlation_id, sorted by timestamp, computed `agents_involved`, printed the failure-detection block for the induced failure.
- Three Ch.4 `jq` queries (agent filter, `status=="failed"`, human-readable split) — **passed**, correct output.
- `.github/workflows/orchestrator-with-tracing.yml` — **reasoned**. Valid YAML, but it invokes `work/gh-600/scripts/traced_subtask.py`, which is **never defined** in the quest — the workflow can't succeed end-to-end.
- `python3 scripts/validate_quest.py --quest q15` (Quest Validation) — **skipped**. Script does not exist in sandbox or quest content; it's platform tooling the learner can't run from the quest alone.

## 🐞 Issues Found

**High**

- **high · `agentic-multi-agent-orchestration-patterns` · Ch.2 & Ch.3 YAML blocks (from ~line 124) · tested** — Leaked `{% raw %}/{% endraw %}` tags are interleaved *inside* each expression, producing `${% raw %}{{ … }}{% endraw %}`, which GitHub Actions will never evaluate. Confirmed via `yaml.safe_load` (deserializes to the broken literal string) and by direct source read. **Fix:** wrap the whole fenced block in `{% raw %}…{% endraw %}` at the Liquid level (as `agentic-codex-05` correctly does at its lines 137/174), leaving the `${{ … }}` expressions intact.
- **high · `agentic-multi-agent-orchestration-patterns` · fan-out workflow deps · tested** — `partition_task.py`, `run_subtask.py`, `aggregate_results.py` are invoked but never supplied (`No such file or directory`). **Fix:** ship minimal working stubs, or explicitly mark them as learner-authored placeholders.
- **high · `agentic-behavior-tuning` · Exercise 13.1 `measure_agent_baseline.sh` · tested** — Prints `✅ Baseline recorded` while the `continue` branch skips the only write, so the output file is never created; the success `echo` is unconditional. **Fix:** count successfully-recorded tasks and only print success when `count > 0`, else print a clear skip/failure summary and exit non-zero.
- **high · `agentic-behavior-tuning` · Exercise 13.1 prerequisites + Quest Validation · tested** — The baseline (and thus the first validation check) is unattainable without a live authenticated repo containing `agent-task.yml` and prior agent runs — infra the quest never bootstraps. **Fix:** provide a minimal bootstrap or label the exercise "requires an existing production-like repo, not completable in a fresh sandbox."
- **high · `agentic-multi-agent-observability` · Ch.1 workflow `traced_subtask.py` · tested** — The orchestrator workflow calls a script that is never defined in the quest. **Fix:** include its source, or reuse the already-defined `trace_writer.py` so the example is self-contained.

**Medium**

- **medium · `agentic-codex-05` · Ch.3 escalate pattern + Mastery Challenge · reasoned** — `continue-on-error: true` at job level reports success to `needs`-dependents, so the `recover` job's `if: failure()` likely never triggers. **Fix:** use `if: needs.agent_security.result == 'failure'` (verify on a live run), since this pattern is also literally required by the Mastery Challenge.
- **medium · `security-fundamentals` · objectives vs body (Risk Management) · reasoned** — "Risk Management (likelihood × impact)" is a named secondary objective and mastery indicator ("Justify a fix-it-first decision using a simple risk rating"), but no chapter teaches or demonstrates a rating framework. **Fix:** add a short worked example (e.g., a 3×3 likelihood/impact matrix).
- **medium · `security-fundamentals` · safety warning placement (line 207) · reasoned** — The "⚠️ Only ever run intentionally vulnerable apps on isolated/local/throwaway environments" warning lives *only inside the collapsible Cloud Realms `<details>`*; the macOS/Windows/Linux readers (the common cases) never see it. **Fix:** hoist the warning above all four platform tabs.
- **medium · `agentic-multi-agent-orchestration-patterns` · objectives vs content · tested/reasoned** — "Event-driven" and "Test aggregation" are stated objectives but never given an exercise. **Fix:** add worked exercises or trim the objectives.
- **medium · `agentic-multi-agent-observability` · pipeline never wired end-to-end · tested** — The three pieces (emit / aggregate / query) are never connected into one runnable workflow; no job downloads sub-agent artifacts and calls `aggregate_traces.py`. **Fix:** add the aggregation job (`actions/download-artifact@v4` + invoke the aggregator).

**Low**

- **low · `security-fundamentals` · knowledge checks · reasoned** — No answer key anywhere for self-directed learners. Add a collapsed `<details>` answer block.
- **low · `security-fundamentals` · Advanced Challenge "Break the Juice Shop" · reasoned** — No scaffolding/pointer to where the flaws live. Link the official Juice Shop challenge list.
- **low · `agentic-codex-05` · `_data/agents.yml` `review_date: 2026-07-15` · reasoned** — Already in the past relative to today (2026-07-21); either intentional (add a "deliberately overdue" comment) or refresh.
- **low · `agentic-codex-05` · `jq sort_by(.ts)` string-sort fragility · tested** — Safe only because epoch seconds are fixed-width. Add a `| tonumber` cast or a footnote.
- **low · `agentic-multi-agent-observability` · Python 3.10+ requirement · reasoned** — `dict[str, Any] | None` needs 3.10+ but no minimum version is stated. Note it.
- **low · slice-wide · level hub name mismatch · reasoned** — `security-fundamentals` links `[[Level 1011 - Security & Compliance]]` while all four agentic quests link `[[Level 1011 - Feature Development]]` — two names for the same level code (see continuity note below).

## 🔗 Chain Continuity

**This "slice" is two unrelated tracks glued by a shared level code, not one learning path.** Quest 1 (`security-fundamentals`) is authentic Security & Compliance / Warrior content (`quest_series: Security Mastery`, `skill_focus: security`, unlocking secure-coding / threat-modeling / pen-testing / compliance). Quests 2–5 are all **GH-600 "Agentic Codex"** quests (`quest_line: gh-600`, `skill_focus: devops`/`ai-ml`) about tuning and orchestrating GitHub Copilot agents. For a Security Specialist walking level 1011, quest 1 is on-theme and quests 2–5 read as a different curriculum. The planner grouped strictly by `level: '1011'`; a maintainer may want the level's theme label and its member quests reconciled. The **level-hub naming split** ("Security & Compliance" vs "Feature Development" for the same 1011) is the concrete symptom.

**Within the agentic sub-chain, the dependency ordering is coherent but the slice is missing its root.** The declared chain is Q12 (`1010/agentic-failure-root-cause-analysis`) → Q13 `agentic-behavior-tuning` → Q14 `agentic-multi-agent-orchestration-patterns` → Q15 `agentic-multi-agent-observability` → Q16. The plan order (behavior-tuning → coordination survey → orchestration-patterns → observability) is a sensible dependency sort. **But Q13 hard-requires Q12, which sits at level 1010 outside this window** — a learner entering this window fresh has no RCA output, which the engine confirmed leaves Ch.2's "select top-2 failure patterns" disconnected from real data. Every agentic quest also assumes an authenticated GitHub repo with Actions + Copilot coding-agent access — heavy prerequisites a learner arriving from the conceptual security quest would not have provisioned.

**`agentic-codex-05` (score 87) overlaps and out-performs its own sub-quests.** It is explicitly a Domain 5 *survey hub* that funnels to four sub-quests including `orchestration-patterns` (Q14) and `observability` (Q15). Yet its hands-on lab teaches the same fan-out + correlation-ID + trace-stitch material **and actually runs correctly**, while Q14 ships copy-paste-broken YAML and Q15 leaves the pipeline unwired. A learner who does the survey gets a *working* version of what the two dedicated deep-dive quests botch — a strong signal that the fixes to Q14/Q15 can borrow directly from the coordination quest's verified snippets.

**Net continuity verdict:** the security-fundamentals entry stands alone and holds; the agentic chain is internally well-ordered but (a) missing its Q12 root in this window, (b) blocked by two learner-stopping bugs mid-chain (Q13 baseline, Q14 workflow), and (c) thematically mismatched to the Security Specialist path. A beginner would clear quest 1, then hit a hard wall at quest 2 (cheerful-but-empty baseline) and quest 4 (green self-check on a broken workflow).

## 🧠 Reasoning & Method

- **What I ran vs. reasoned about:** I did **not** execute the agentic engine — per the workflow contract the evidence was pre-computed deterministically and **sealed** into `walk-evidence.json` / `walk-evidence.md` (the engine's child `claude` processes can't authenticate from an agent's Bash tool). I consumed that evidence **as-is** — no edits, no regeneration — and independently **read all five quest sources in plan order** as a learner to produce the Chain Continuity findings and to cross-check the machine evidence against the actual text. Several issues are corroborated by both the sealed execution *and* my direct source read (the `${% raw %}` corruption at line 124; the buried safety warning at line 207; the Risk Management objective absent from every chapter).
- **Mode & sandbox:** `execute` mode, sandboxed by the engine in a disposable dir (Linux, `gh 2.96.0`, Python 3.12). Every `passed`/`failed` above traces to a real command in that sandbox; everything I judged from text alone is tagged **reasoned**.
- **Coverage & limits:** This is a **windowed** walk — 5 of the level's 12 quests (window 0 of 3); the remaining 8 belong to later windows in the perfection sweep. Snippet coverage was partial by nature: OS-specific installs (`brew`/`winget`/`sudo apt`) were **skipped** on a Linux sandbox; GitHub Actions workflow semantics (the `continue-on-error` escalate pattern) could not be executed offline and are **reasoned**, not tested; `scripts/validate_quest.py` (Q15) was **skipped** as absent platform tooling. Total engine cost ≈ $2.70 across the five quests.
- **Confidence:** High on the two FAIL quests — their blocking bugs were reproduced by execution and I re-confirmed them in the source. High on quest 1 and quest 3 passing. Medium on the `agentic-codex-05` escalate-pattern doubt (reasoned from documented GH Actions semantics; needs a live-workflow check). I made **zero** content edits and touched only this one report file.
