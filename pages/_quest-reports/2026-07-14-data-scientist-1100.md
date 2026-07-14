---
title: Data Scientist · L1100 · 2026-07-14
description: Quest-perfection walkthrough of the Data Engineering slice data-scientist/1100 on 2026-07-14,
  engine verdict fail. An evidence-based, learner's-eye…
date: '2026-07-14T12:53:49.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Data Scientist
tags:
- data-scientist
- level-1100
- walkthrough
- quest-perfection
- fail
- data-engineering
render_with_liquid: false
excerpt: 'Data Scientist · Level 1100 — Data Engineering: an evidence-based quest-perfection walkthrough
  from 2026-07-14.'
slice: data-scientist/1100
character: data-scientist
level: '1100'
theme: Data Engineering
tier: Master
verdict: fail
quest_count: 5
walk_date: '2026-07-14'
run_url: https://github.com/bamr87/it-journey/actions/runs/29329246935
source_report: test/quest-validator/walkthroughs/2026-07-14-data-scientist-1100.md
---

> **Slice** `data-scientist/1100` · **Level** 1100 (Data Engineering) · **Master tier** · **Engine verdict** ❌ fail · **Walked** 2026-07-14
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29329246935) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-14-data-scientist-1100.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-14-data-scientist-1100.md)

---

## 🎯 Session Summary

I walked a **5-quest window** (window 2 of 3) of the **Data Scientist · Level 1100
(Data Engineering, Master)** slice, in the exact order the planner selected, as a
learner would. The machine evidence was sealed by the workflow in `--mode execute`
(disposable sandbox, commands run for real); I consumed `walk-evidence.json` /
`walk-evidence.md` as-is and reasoned about the linked journey against the five quest
sources.

**Headline verdict: FAIL.** Three of five quests (**Stream Processing 44%**,
**Data Quality 51%**, **The Warden's Pact 51%**) have concrete, reproduced blockers
that would stop a real learner cold before they finish the hands-on work — a dead
Docker image + missing single-broker replication overrides, a never-supplied
`orders.csv` plus an outdated Great Expectations API, and a self-defeating CODEOWNERS
ordering bug plus a validation script the quest never ships. **Apache Spark (83%,
PASS)** is the standout: every Python snippet ran and behaved exactly as taught. The
**Capstone (68%, WARN)** mostly holds, but its own `acceptance-criteria.json` breaks
the `jq -e` check its own validator runs. A maintainer should treat Stream Processing
and Data Quality as the two highest-value fixes: both teach accurate concepts but are
**not completable as written today**.

One structural note for the caller: this window mixes **two different quest lines**
that happen to share the `1100` level code — the *Agentic Codex (GH-600)* arc
(quests 1–2) and *Data Engineering Mastery* (quests 3–5). For a **data-scientist**
learner, only the latter trio is on-path; see §🔗 Chain Continuity.

## 🗺️ The Journey

Ordered as walked (plan order = `walk-plan.json`):

1. ❌ **The Warden's Pact: Guardrails and Human-in-the-Loop Patterns** — 51% ·
   Sound guardrail concepts, but the only runnable command fails and the CODEOWNERS
   example silently defeats its own file-scope guardrail.
2. ⚠️ **Trial of the Agentic Codex: The Grand Capstone** — 68% · The `validate-capstone.sh`
   contract genuinely works, but the quest's own `acceptance-criteria.json` fails the
   exact `jq -e` check that validator runs.
3. ✅ **Apache Spark Mastery: Big Data with PySpark** — 83% · Technically solid; all six
   PySpark snippets ran and behaved as described. Only the platform-setup notes have bugs.
4. ❌ **Stream Processing: Real-Time Data with Apache Kafka & Flink** — 44% · Excellent
   theory, but the hands-on setup is broken end-to-end: dead broker image + missing
   replication overrides mean no consumer group ever receives messages.
5. ❌ **Data Quality Engineering: Validation & Monitoring** — 51% · Accurate concepts and
   working pure-Python validators, but every example depends on an `orders.csv` that is
   never provided, and the flagship GE example is broken against the current library.

## 🔬 Evidence

All statuses below come from commands the sealed execute engine actually ran in the
sandbox (`passed`/`failed`/`skipped`), or from static reasoning over the quest source
(`reasoned`). Nothing here is asserted without a witnessed command or a quoted line.

### 1. The Warden's Pact — 51% ❌ (13 turns · commands_work 2/5, content_accuracy 2/5, safety 5/5)
Coverage: **0 passed · 1 failed · 6 reasoned** (of 7). The only literally-runnable
snippet failed; the four YAML/markdown config blocks are non-executable and were
reasoned about.

- `python3 scripts/validate_quest.py --quest q19` → **FAILED**. Real sandbox output:
  `python3: can't open file '.../scripts/validate_quest.py': [Errno 2] No such file or
  directory`, exit code 2. The quest (lines 340–347) presents this as the completion
  check but never ships or links the script.
- `.github/CODEOWNERS` block (lines 117–134) → **reasoned**: the catch-all `* @team-dev`
  is the **last** rule, and GitHub CODEOWNERS is "last matching pattern wins", so the
  wildcard overrides every specific `/src/auth/`, `/src/crypto/` rule above it — the
  file-scope guardrail this chapter exists to teach would not apply.
- `guardrail-file-scope.yml` (lines 151–178) → **reasoned**: `gh pr view` step has no
  `GH_TOKEN`/`GITHUB_TOKEN` env, so `gh` fails in Actions with the standard "set the
  GH_TOKEN environment variable" error.
- `agent-audit-trail.yml` (lines 249–293) → **reasoned**: `workflow_run.workflows:
  ["*Agent*", "*Copilot*"]` uses wildcards this filter doesn't support (needs exact
  names); the final `git push` has no `permissions: contents: write` and will likely 403.
- Verified via PyYAML that all three YAML blocks parse, but every `${​{ ... }​}`
  expression is wrapped in literal `{​% raw %​}...{​% endraw %​}` — copied from raw markdown
  they are not valid Actions expressions.
- Audit heredoc reproduced locally → produces a pretty-printed multi-line JSON block,
  not JSON-Lines, contradicting the `.jsonl` filename the workflow uses.

### 2. The Grand Capstone — 68% ⚠️ (22 turns · commands_work 3/5, content_accuracy 3/5, safety 5/5)
Coverage: **6 passed · 1 failed · 3 reasoned** (of 10).

- `validate-capstone.sh` (lines 448–486) → **PASSED**. Verified it correctly fails on a
  partial build and cleanly passes once all 14 seal artifacts exist. This is the quest's
  strongest artifact.
- `acceptance-criteria.json` (lines 311–336) → **FAILED**. As given (with the leading
  `// work/gh-600/capstone/acceptance-criteria.json` comment) it is invalid JSON:
  `jq -e '.criteria | length >= 3' ...` → `jq: parse error: Invalid numeric literal at
  line 1, column 3`. This is the exact command `validate-capstone.sh` runs for seal S4, so
  a verbatim copy fails the quest's own validator. Removing the comment line makes jq
  return true.
- `plan-then-execute.yml` and the `permissions:` block (Challenges 1.2 / 2.1) → **PASSED**
  as valid YAML; the `sdlc-diagram.md` and `grand-reflection.md` templates → **PASSED**.
- `.vscode/mcp.json` (lines 250–263) → **reasoned**: missing the `inputs` array VS Code
  needs to resolve `${input:github-token}`, so it isn't a working config as shown.

### 3. Apache Spark Mastery — 83% ✅ (17 turns · commands_work 4/5, structure 5/5, safety 5/5)
Coverage: **7 passed · 0 failed · 2 reasoned · 3 skipped** (of 12). Skips are the
macOS/Windows/Docker setup paths not applicable to the Linux sandbox.

- Linux setup path (lines 173–178, `apt install openjdk-17-jdk … pip install pyspark`) →
  **PASSED**.
- `spark_intro.py` (SparkSession + createDataFrame + printSchema + show) → **PASSED**.
- Lazy pipeline `filter/groupBy/agg/orderBy` then `.show()` / `.explain(mode="formatted")`
  → **PASSED**; the `Exchange` (shuffle) step was visible in the plan as taught.
- `groupByKey().mapValues(sum)` vs `reduceByKey(...)` → **PASSED** (same result verified).
- `coalesce(1).write` vs `repartition(200,"service")` → **PASSED** (file counts as claimed).
- `spark.sql(...).explain("cost")` and the `.cache()`/`count()`/`unpersist()` flow →
  **PASSED**.
- The one substantive accuracy gap is **reasoned/tested in setup**: the prereq says
  "JDK 11/17" (line 127), but the engine directly disproved JDK 11 — current PySpark
  (4.1.2) against JDK 11 raises `UnsupportedClassVersionError`. Windows PowerShell
  activation `.\.venv\Scripts\activate` is also broken (should be `Activate.ps1`).

### 4. Stream Processing — 44% ❌ (35 turns · commands_work 1/5, content_accuracy 2/5, safety 5/5)
Coverage: **4 passed · 7 failed · 6 reasoned** (of 17). This quest ate the most turns
and produced the most failures — the setup is broken end-to-end.

- `pip install kafka-python` + `from kafka import KafkaProducer, KafkaConsumer` → **PASSED**.
- `docker compose up -d` with the quest's `docker-compose.yml` (`image: bitnami/kafka:3.7`,
  lines 254–269) → **FAILED**: `manifest for bitnami/kafka:3.7 not found: manifest unknown`.
  Also failed for `:latest, :3.9, :4.0, :3.8, :3.6` — the whole bitnami/kafka tag family is
  gone from the registry.
- After substituting `apache/kafka:3.7.0`, `docker compose up -d` → **PASSED**, but then:
- `consumer.py` (lines 289–303) → **FAILED**: with the quest's exact broker env (no
  offsets-topic replication override) the consumer received **0 messages after 25s** —
  the broker loops auto-creating `__consumer_offsets` (needs RF 3, only 1 broker). Passed
  only after manually adding `KAFKA_CFG_OFFSETS_TOPIC_REPLICATION_FACTOR=1`.
- `eos_producer.py` (Chapter 4 exactly-once, lines 379–397) → **FAILED**: hung
  indefinitely (30s timeout, zero output) on the quest's config; broker logs showed
  infinite `__transaction_state` retries. Passed only after adding
  `KAFKA_CFG_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1` and `..._MIN_ISR=1`, neither of
  which the quest provides.
- Linux setup (line 176, `apt install … docker-compose-plugin`) → **FAILED**:
  `apt-cache policy` on the Ubuntu 24.04 sandbox shows `docker-compose-plugin` Candidate
  `(none)` — not installable without adding Docker's official apt repo first.
- Net effect verified by reproduction: **none of the three Mastery Challenges are
  completable** by following the quest as written today.

### 5. Data Quality Engineering — 51% ❌ (24 turns · commands_work 2/5, content_accuracy 2/5, safety 5/5)
Coverage: **5 passed · 2 failed · 1 reasoned · 1 skipped** (of 9).

- Linux + Cloud `pip install pandas great-expectations pandera` → **PASSED**.
- `profile.py`, `validate_simple.py`, `anomaly.py` → **PASSED** (the dependency-free and
  pure-logic snippets run correctly).
- `validate_ge.py` (Chapter 3, lines 270–289) → **FAILED**:
  `context.sources.add_pandas('orders_src')` raises
  `AttributeError: 'EphemeralDataContext' object has no attribute 'sources'` on
  great_expectations **1.19.0** (what `pip install great-expectations` resolves to today).
  The fluent `.sources` API was removed in GE 1.0+.
- `contract.py` (Chapter 4, lines 339–353) → **FAILED**: correctly raised `SchemaErrors`
  on the corrupted CSV, but **also fails on a fully clean CSV** —
  `WRONG_DATATYPE: expected series 'created_at' to have type datetime64[ns]` because
  `pd.read_csv` has no `parse_dates=['created_at']`. This contradicts the Novice
  Challenge's "on a clean copy it passes" criterion.
- Underlying all of it: every hands-on snippet reads `orders.csv` (first used line 239),
  which the quest **never provides or generates** — so nothing is runnable out of the box.

## 🐞 Issues Found

Each issue below is backed by a witnessed sandbox command (§Evidence) or an exact quoted
line. Severities mirror the rubric dimensions (commands_work / content_accuracy first).

**High**
- **Stream Processing · Ch.2 `docker-compose.yml` (line 258) · dead image.** Observed
  `manifest for bitnami/kafka:3.7 not found` (and every other bitnami tag). *Fix:* pin a
  currently-published image (e.g. `apache/kafka:3.7.0`), and periodically re-verify the tag.
- **Stream Processing · Ch.2 broker env (lines 261–268) · missing single-broker
  replication.** Observed: consumer gets 0 messages, EOS producer hangs forever. *Fix:* add
  `KAFKA_CFG_OFFSETS_TOPIC_REPLICATION_FACTOR=1`, `KAFKA_CFG_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1`,
  `KAFKA_CFG_TRANSACTION_STATE_LOG_MIN_ISR=1`.
- **Data Quality · Chapters 2–4 · missing `orders.csv`.** Every hands-on snippet reads it;
  it is never supplied. *Fix:* add a downloadable `orders.csv` or a short "generate sample
  data" script before Chapter 2.
- **Data Quality · Ch.3 `validate_ge.py` (line 277) · outdated GE API.** Observed
  `AttributeError: … has no attribute 'sources'` on GE 1.19.0. *Fix:* update to the current
  Data Source/Batch Definition API (`context.data_sources.add_pandas(...)`) or pin a
  pre-1.0 `great-expectations` version.
- **Data Quality · Ch.4 `contract.py` (line 353) · fails on clean data.** Observed
  `WRONG_DATATYPE` on `created_at` even for clean input. *Fix:* add `parse_dates=['created_at']`
  to `pd.read_csv`.
- **The Warden's Pact · Validation (line 341) · missing script.** Observed
  `No such file or directory` for `scripts/validate_quest.py`. *Fix:* ship/link the script
  or explain it is repo tooling not runnable from QUEST.md alone.
- **The Warden's Pact · Ch.2 CODEOWNERS (lines 121–133) · self-defeating order.** Wildcard
  `* @team-dev` is last and (last-match-wins) overrides all specific rules. *Fix:* move the
  wildcard first, specific overrides after.

**Medium**
- **Capstone · Challenge 4.1 `acceptance-criteria.json` (line 312) · invalid JSON.** The
  leading `// …` comment breaks the `jq -e` check `validate-capstone.sh` itself runs (S4).
  Observed `jq: parse error: Invalid numeric literal`. *Fix:* move the comment to prose above
  the fenced block.
- **The Warden's Pact · Ch.2 `guardrail-file-scope.yml` (line 155) · missing `GH_TOKEN`.**
  `gh pr view` will fail in Actions. *Fix:* add `env: { GH_TOKEN: ${​{ secrets.GITHUB_TOKEN }​} }`.
- **The Warden's Pact · Ch.4 `agent-audit-trail.yml` (lines 254, 292) · wildcard
  `workflow_run.workflows` + missing push permissions.** *Fix:* use exact workflow names and
  add `permissions: contents: write`.
- **Stream Processing · Ch.3 windowing has no runnable code.** The Intermediate Challenge
  ("late event lands in its true window") is only described. *Fix:* add a minimal runnable
  tumbling-window-over-event-time example.
- **Stream Processing · Ch.4 elided EOS offset commit (line 394).** The `# … also commit the
  consumed offsets …` comment hides the exact mechanism the Advanced Challenge tests. *Fix:*
  spell out `producer.send_offsets_to_transaction(...)`.
- **Capstone · Challenge 2.2 `mcp.json` (line 252) · not a working config.** Missing the
  `inputs` array to resolve `${input:github-token}`. *Fix:* add it or note it must be added.
- **Data Quality · Advanced Challenge · no quarantine/lineage examples.** Required
  deliverables with zero worked example in the body. *Fix:* add a small quarantine-DataFrame
  snippet and a lineage-map template.

**Low**
- **Apache Spark · prereq "JDK 11/17" (line 127) is wrong for current PySpark.** Testing
  PySpark 4.1.2 on JDK 11 gave `UnsupportedClassVersionError`. *Fix:* state JDK 17 (drop 11).
- **Apache Spark / Stream Processing · Windows PowerShell activation.** `.\.venv\Scripts\activate`
  → should be `.\.venv\Scripts\Activate.ps1`.
- **Data Quality · setup blocks · unpinned installs.** Pin `great-expectations==1.x` (and
  peers) so a future breaking API change doesn't silently reappear.

**No issues** were found in Apache Spark's core teaching content — all six PySpark snippets
ran and matched the quest's claims about lazy evaluation, shuffles, and caching.

## 🔗 Chain Continuity

**Two distinct quest lines share this level code.** This window is `2 of 3` (offset 10) of
a 15-quest level, and it straddles a seam:

- **Quests 1–2 (Agentic Codex / GH-600):** `quest_series: agentic-ai-mastery`,
  `quest_line: gh-600`. Their internal chain is coherent — *Warden's Pact* declares
  `unlocks_quests: agentic-codex-capstone-exam-trial`, and the Capstone lists Q19 among its
  19 `required_quests`, so the local N→N+1 link (guardrails → capstone) **is satisfied within
  this window**. But the Capstone assumes **all 19** prior GH-600 quests are done; only Q19 is
  in-window, so a learner arriving here cold is missing 18 prerequisites the capstone leans on
  (its per-seal "Refer to Qn…" pointers mitigate this by design).
- **Quests 3–5 (Data Engineering Mastery):** `quest_line: The Data Engineer's Ascent`.
  This trio is internally well-ordered: *Apache Spark* declares `unlocks_quests:
  [stream-processing, data-quality]`, *Stream Processing* unlocks *Data Quality*, and each
  "Next Steps" section points forward correctly. All three list **ETL Pipeline Design** as a
  required/recommended prerequisite — that quest is **not in this window** (earlier in the
  level), so a learner starting at this window lacks the assumed idempotency/ETL grounding the
  three quests repeatedly reference ("just like the idempotent load from the ETL quest").

**For a data-scientist learner specifically:** the on-path chain is the Data Engineering
trio (the character-class recommendation lines in each quest literally route the "📊 Data
Scientist" to Data Quality). The two agentic-AI quests are a *different* track that happens to
carry the `1100` code — worth a maintainer's awareness that the date-rotated planner will keep
sampling both lines under this character/level pairing.

**Readiness hand-off, quest by quest, as a learner:**
- *Spark → Stream/Data Quality*: Spark **leaves the learner genuinely ready** — its content
  works and it correctly frames distributed thinking that Stream Processing extends. This is the
  one clean hand-off in the slice.
- *Stream Processing → Data Quality*: conceptually fine, but a learner who tried the hands-on
  work would arrive **frustrated and blocked** (they never got a working broker), carrying no
  runnable streaming artifact forward.
- *Data Quality (terminus)*: as the end of the data-eng line it should feel like a capstone;
  instead the missing `orders.csv` means a learner cannot run a single example end to end, so
  the line finishes on a broken note.
- *Warden's Pact → Capstone*: the concepts chain, but both quests carry defects that surface
  at exactly the validation step each one builds toward (missing `validate_quest.py`; the
  capstone's own `acceptance-criteria.json` failing its own validator).

## 🧠 Reasoning & Method

- **What I ran vs. reasoned:** I did **not** run the engine — per the skill and the task,
  `walk-evidence.json` was pre-sealed by the workflow (the engine's child `claude` processes
  can't authenticate from an agent Bash tool). I consumed it and `walk-evidence.md` **verbatim**
  and did not regenerate or edit them, `walk-plan.json`, or any quest. Every `passed`/`failed`
  in §Evidence is a command the sealed **execute-mode** engine actually ran in its disposable
  per-quest sandbox; every `reasoned` item is my static read of the quoted quest source.
- **My value-add** is §🔗 Chain Continuity and the linked-journey framing: reading all five
  sources in plan order and judging whether each quest leaves a learner ready for the next,
  which prerequisites the window assumes but doesn't contain, and that the level code mixes two
  quest lines.
- **Mode / sandbox:** execute, sealed by `quest-perfection`/`quest-walkthrough` workflow;
  Ubuntu 24.04 runner sandbox. Safety scored 5/5 on all five quests — no destructive or
  unsafe commands were needed or run.
- **Coverage & limits, stated honestly:**
  - This is a **windowed** slice: **5 of the level's 15 quests** were walked (window 2/3). I did
    **not** expand to the other 10; `stats.total_quests=15` is context only.
  - Setup paths for **non-Linux OSes** (macOS/Windows/Docker-desktop) were `skipped` by the
    engine (3 in Spark, 1 in Data Quality) — those platform commands are **reasoned-only**, not
    tested, so Windows/macOS-specific bugs (e.g. the PowerShell `Activate.ps1` issue) are
    flagged from source inspection, not execution.
  - A few quest artifacts are non-executable config (CODEOWNERS, workflow YAML, mermaid) and are
    necessarily `reasoned`, not run.
  - Stream Processing consumed the most engine turns (35) and still could not complete its
    challenges even after the engine substituted a working image — I report it as **verified
    broken**, not merely suspected.
- **Confidence:** High on the three FAIL verdicts — each rests on a reproduced command with
  quoted real output (dead manifest, 0 messages, `AttributeError`, `WRONG_DATATYPE`,
  `No such file`). High on Spark's PASS. Medium-high on the Capstone WARN (structure works;
  the one hard failure is its own JSON-vs-validator contradiction).

*One slice, one report. No quest content changed; git is the caller's job.*
