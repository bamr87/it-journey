---
title: Data Scientist · L1100 · 2026-07-20
description: Quest-perfection walkthrough of the Data Engineering slice data-scientist/1100 on 2026-07-20,
  engine verdict fail (avg 64.0%). An evidence-based…
date: '2026-07-20T00:00:00.000Z'
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
  from 2026-07-20.'
slice: data-scientist/1100
character: data-scientist
level: '1100'
theme: Data Engineering
tier: Master
verdict: fail
quest_count: 5
engine_average: 64.0
walk_date: '2026-07-20'
run_url: https://github.com/bamr87/it-journey/actions/runs/29740320814
source_report: test/quest-validator/walkthroughs/2026-07-20-data-scientist-1100.md
---

> **Slice** `data-scientist/1100` · **Level** 1100 (Data Engineering) · **Master tier** · **Engine verdict** ❌ fail (avg 64.0%) · **Walked** 2026-07-20
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29740320814) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-20-data-scientist-1100.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-20-data-scientist-1100.md)

---

## 🎯 Session Summary

I walked a **5-quest window (window 2 of 3)** of the **Data Scientist → Level 1100** slice as a learner would, consuming the sealed execute-engine evidence and reading every quest source in plan order. The window is **not one learning path** — it splices two unrelated tracks that happen to share the `1100` level code: the **GH-600 "Agentic Codex" arc** (Warden's Pact → Grand Capstone) and the **Data Engineering Mastery arc** (Apache Spark → Stream Processing → Data Quality). A data-scientist reading top-to-bottom would whiplash between GitHub governance and PySpark.

**Headline verdict: FAIL for the slice.** Three of five quests fail with **high-severity, copy-paste-breaking bugs** verified by real command execution: the Warden's Pact ships three GitHub Actions workflows with literal `{​% raw %​}`/`{​% endraw %​}` tags *inside* `${​{ }​}` expressions (every `run:` step throws `bad substitution`), Stream Processing pins a Kafka image (`bitnami/kafka:3.7`) that no longer exists on Docker Hub so no learner can start Chapter 2, and Data Quality never provides the `orders.csv` that all four of its snippets read (plus a Great Expectations example broken against the 1.x API `pip` now installs). The two passing quests are genuinely strong: **Apache Spark (95%)** ran all 7 executed snippets cleanly, and the **Grand Capstone (85%)** validator behaved exactly as documented in both failing and passing states. The most actionable maintainer takeaway: **the correct fix for the Warden's Pact templating bug already exists one quest away** — the Capstone escapes the identical Liquid mechanism correctly.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ❌ fail | The Warden's Pact: Guardrails & Human-in-the-Loop | 34 | All 3 workflow snippets die on `bad substitution`; CODEOWNERS ordering defeats its own guardrail; validator script doesn't exist. |
| 2 | ✅ pass | Trial of the Agentic Codex: The Grand Capstone | 85 | Sole runnable snippet (`validate-capstone.sh`) ran true in both fail & pass states; ~2/3 of sub-challenges are "refer to Q_" stubs. |
| 3 | ✅ pass | Apache Spark Mastery: Big Data with PySpark | 95 | Every executed snippet worked and matched the prose; only the stale "JDK 11/17" prereq is inaccurate for pip's pyspark 4.x. |
| 4 | ❌ fail | Stream Processing: Real-Time with Kafka & Flink | 56 | Strong concepts and working Python, but the first infra step (`docker compose up`) fails — image tag is gone from Docker Hub. |
| 5 | ❌ fail | Data Quality Engineering: Validation & Monitoring | 50 | Dependency-free validator & anomaly check work; but no `orders.csv` is ever provided and the GX/pandera examples fail as written. |

## 🔬 Evidence

All outcomes below are from the sealed execute-engine pass (`walk-evidence.json`, `mock:false`, `mode:execute`) — commands actually run in a disposable sandbox. I did not re-run the engine (its child processes cannot authenticate from an agent Bash tool); I reasoned over the chain against the quest sources.

### 1. The Warden's Pact — 34% ❌  ·  ran 4 extracted commands, **0 passed / 4 failed**, 3 reasoned (1 of 7 snippets literally runnable)
- The only literally-runnable command, `python3 scripts/validate_quest.py --quest q19`, **failed**: `can't open file '.../scripts/validate_quest.py': [Errno 2] No such file or directory` — the script is never provided or linked.
- The engine extracted each `run:` step from the three workflow YAML blocks and executed them under `bash -eo pipefail` (Actions' real default). Every step containing `${​% raw %​}{​{ ... }​}{​% endraw %​}` **failed** with `bad substitution`, exit 1 — reproduced individually for Ch.2 (`gh pr view "${​% raw %​}{​{ github.event.pull_request.number }​}{​% endraw %​}"`), Ch.3 (`echo "Deploying plan: ${​% raw %​}{​{ needs.prepare.outputs.deploy_plan }​}{​% endraw %​}"`), and Ch.4 (the audit-log heredoc). Confirmed against source lines 155, 238, and 275–280.
- CODEOWNERS ordering bug confirmed by reading source (lines 121–133): the catch-all `* @team-dev` sits at the **bottom**, and GitHub CODEOWNERS is *last-match-wins*, so it silently overrides the `@team-security` rules on `/src/auth/` and `/src/crypto/` — the inverse of the guardrail's stated purpose.

### 2. The Grand Capstone — 85% ✅  ·  ran 5, **5 passed / 0 failed**, 4 reasoned (1 of 9 snippets runnable)
- `validate-capstone.sh` was created from its heredoc, `chmod +x`'d, and run **verbatim**: against an empty repo it printed **14 ❌ lines and exited 1**, exactly as the prose predicts ("one that fails a few times first was written honestly"). Re-run after synthesizing all 14 artifacts, it **passed** — the machine-verifiable contract works in both directions.
- `jq`, `git`, `gh` all present; the Seal-4 `jq -e '.criteria | length >= 3'` filter worked against a real JSON file. Both YAML blocks parsed cleanly (yamllint: cosmetic line-length only). The two JSON snippets only fail strict `json.loads()` because of a leading `// path` JSONC comment — cosmetic for illustrative config.

### 3. Apache Spark Mastery — 95% ✅  ·  ran 7, **7 passed / 0 failed**, 1 skipped, 4 reasoned (10 of 12 runnable)
- Linux setup ran end-to-end; `pip install pyspark` pulled **pyspark 4.2.0** and printed the version.
- Ch.1 `spark_intro.py`: `printSchema()` + `df.show()` produced the exact 3-row table shown. Ch.2 lazy snippet: `result.show()` → `checkout | 105.0` and `explain(mode="formatted")` contained **two `Exchange` nodes**, exactly the shuffle marker the quest tells learners to hunt for. Ch.3 `groupByKey`/`reduceByKey` both returned identical `[('b', 6), ('a', 4)]`; `coalesce(1)` produced one output file and `repartition(4,…)` produced several. Ch.4 SQL `explain("cost")` and the cache/unpersist cycle both ran clean.
- Only gap: prereq says "JDK 11/17" (line 127), but pip's pyspark 4.x requires **Java 17+** — stale, not blocking.

### 4. Stream Processing — 56% ❌  ·  ran 6, **3 passed / 3 failed**, 2 skipped, 3 reasoned (7 of 11 runnable)
- The gating infra command **failed live**: `docker compose up -d` against the Ch.2 compose file (`image: bitnami/kafka:3.7`, source line 258) → `manifest for bitnami/kafka:3.7 not found: manifest unknown`. Verified `docker pull bitnami/kafka:3.7` also fails. This blocks **every platform path** at the first hands-on step.
- After swapping to `bitnamilegacy/kafka:3.7`, the broker started in KRaft mode and **everything downstream worked with zero further edits** — so the compose config itself is correct, only the image reference is stale. `producer.py` printed `produced 5 events`; the consumer printed `partition=X offset=Y value=…` per message and correctly showed offset tracking on re-run; the Ch.4 exactly-once producer (idempotence + transactions) ran and the message was committed/consumable.

### 5. Data Quality Engineering — 50% ❌  ·  ran 8, **5 passed / 3 failed**, 1 skipped, 0 reasoned (9 of 9 runnable)
- **No `orders.csv` is ever provided** — all four snippets (`profile.py`, `validate_ge.py`, `validate_simple.py`, `contract.py`) call `pd.read_csv("orders.csv")` and **fail with `FileNotFoundError`** for a literal learner; the engine had to synthesize a CSV to proceed.
- Ch.3 Great Expectations snippet **failed**: `context.sources.add_pandas(...)` → `AttributeError: 'EphemeralDataContext' object has no attribute 'sources'` on the `great_expectations 1.19.0` that `pip install` resolves to (the `.sources` fluent API was removed in the GX 1.0 rewrite).
- Ch.4 pandera `contract.py` **failed**: without `parse_dates=["created_at"]`, `Column(pa.DateTime)` raises `SchemaErrors … expected datetime64[ns], got str`. Adding it (not in the quest) fixes it.
- What **passed**: `validate_simple.py` correctly passed a clean CSV and flagged duplicate/out-of-range/malformed-email on a corrupted copy; `anomaly.py` raised `SystemExit` with a −220.8σ deviation; once patched, pandera `strict=True`/`lazy=True` rejected an extra column and reported all violations at once.

## 🐞 Issues Found

**high** · Stream Processing · Ch.2 `docker-compose.yml` (line 258) · `docker compose up -d` fails for all platforms with `manifest unknown` — `bitnami/kafka:3.7` is gone from Docker Hub, blocking the entire hands-on quest at step 1 · **Fix:** repin to a pullable image (`apache/kafka:3.9.0`, `confluentinc/cp-kafka`, or `bitnamilegacy/kafka:3.7`) and re-verify.

**high** · The Warden's Pact · Ch.2/3/4 workflow YAML (lines 155, 216, 232, 238, 263, 275–291) · Literal `{​% raw %​}`/`{​% endraw %​}` tags left *inside* `${​{ }​}`; every `run:` step throws `bad substitution` (exit 1) when executed · **Fix:** wrap each YAML **fence** in one `{​% raw %​}…{​% endraw %​}` pair (as the Capstone's Challenge 1.2 already does, lines 175/217) so the `${​{ }​}` expressions render intact.

**high** · The Warden's Pact · Ch.2 CODEOWNERS (lines 121–133) · Catch-all `* @team-dev` at the bottom wins under last-match-wins, silently defeating the `@team-security` scope rule — the opposite of the guardrail's purpose · **Fix:** move the catch-all to the **top** of the file.

**high** · Data Quality · Chapters 2–4 (line 239 et al.) · No `orders.csv` is ever provided; every snippet fails `FileNotFoundError` on first run · **Fix:** ship an inline CSV block or a small generator snippet (clean + corrupted) before Chapter 2.

**high** · Data Quality · Ch.3 `validate_ge.py` (lines 270–289) · `context.sources.add_pandas(...)` throws `AttributeError` on the GX 1.19 `pip` installs today · **Fix:** update to the GX 1.x `context.data_sources.add_pandas(...)` API, or pin `great-expectations<1.0`.

**medium** · Data Quality · Ch.4 `contract.py` (line 353) · `Column(pa.DateTime)` fails `WRONG_DATATYPE` because `created_at` reads as string · **Fix:** add `parse_dates=["created_at"]` to `pd.read_csv`.

**medium** · The Warden's Pact · Quest Validation (line 341) · `python3 scripts/validate_quest.py --quest q19` fails — script never provided · **Fix:** ship the script or replace with a manual self-check checklist.

**medium** · The Warden's Pact · Objectives vs. content (lines 89–93) · Objective 5 ("intentionally trigger each guardrail and verify it fires") and objective 3 (forbidden-action *detection*) have no delivered exercise — only an AGENTS.md policy list · **Fix:** add a trigger-and-verify exercise, or reword objective 3 to match the policy-only delivery.

**medium** · Stream Processing · Ch.3 / Intermediate Challenge (lines 418–426) · The tumbling-window-over-event-time exercise has **no reference code anywhere** in the quest · **Fix:** add a minimal windowing example (kafka-python/Faust/PyFlink).

**medium** · Stream Processing · Title/framing · "& Flink" in the title but Flink is never used (all snippets are kafka-python) · **Fix:** add minimal Flink content or drop it from the title.

**low** · Apache Spark · Prereq (line 127) · "JDK 11/17" is stale — pip's pyspark 4.x needs Java 17+ · **Fix:** state "JDK 17+" and consider pinning `pyspark==4.2.0`.

**low** · Grand Capstone · Completeness (Challenges 1.3, 2.3, 3.2–3.3, 4.2–4.3, 5.1–5.4, 6.1–6.2) · ~2/3 of sub-challenges are "Refer to Q_" stubs with no inline artifact/filename hint; the Domain Coverage Rubric (`/18`, `/19`…) is never tied to the validator's pass/fail · **Fix:** add a one-line expected-artifact note per stub and state the rubric↔validator mapping.

## 🔗 Chain Continuity

- **The window is two arcs, not one path.** Quests 1–2 belong to `quest_series: agentic-ai-mastery` (GH-600 Agentic Codex); quests 3–5 belong to `quest_series: Data Engineering Mastery`. They share only the `1100` level code. For a **data-scientist** character, the Data Engineering sub-chain is the on-theme track; the two agentic-governance quests read as a different curriculum bolted onto the same level. This is a slicing/windowing artifact worth flagging to a maintainer — the level bundles disjoint learning tracks, so no single reader is the intended audience for all five.
- **Data Engineering sub-chain (3→4→5) is well-ordered.** Spark's frontmatter `unlocks` Stream + Data Quality, and Stream `unlocks` Data Quality; the plan presents them in that dependency order, and each opens by referencing ETL Pipeline Design as the shared prerequisite. Conceptually the chain is coherent and Spark leaves a learner genuinely ready for the next two. The break is **environmental, not pedagogical**: Spark (self-contained local PySpark) passes, but Stream (needs a live Kafka broker) and Data Quality (needs a dataset + version-sensitive libs) both fail the moment a learner leaves pure-Python territory. A beginner who finishes Spark cleanly would hit a wall at Stream's very first `docker compose up`.
- **Agentic sub-chain (1→2): the prerequisite carries a broken artifact forward.** The Warden's Pact `unlocks` the Capstone, and the Capstone's **Seal 6 / Challenge 6.2 explicitly refers back to Q19** for its three guardrails. A learner who copy-pasted Q19's workflows would carry three `bad substitution`-failing files into the capstone — yet the capstone's validator only checks `test -s .github/CODEOWNERS` and `grep -qi forbidden AGENTS.md`, so **the capstone would still "pass" despite the upstream workflows being non-functional.** The chain hides the Q19 defect rather than catching it.
- **The fix already exists inside the slice.** The Capstone's Challenge 1.2 (source lines 175/217) wraps its YAML fence in a single `{​% raw %​}…{​% endraw %​}` pair *and* tells the learner "drop them when you copy the YAML" — the correct handling of this site's Liquid escape. The Warden's Pact does the same escape *wrong* (tags interleaved inside `${​{ }​}`). A maintainer fixing Q19 can copy the sibling quest's proven pattern verbatim.

## 🧠 Reasoning & Method

- **Mode:** `execute`. The machine evidence in `walk-evidence.json` / `walk-evidence.md` was **pre-computed and sealed by the workflow** in a disposable sandbox (`mock:false`). Per the skill, I consumed it as-is and did **not** re-run, edit, or regenerate it — the engine's child `claude` processes can't authenticate from an agent Bash tool. Every `passed`/`failed` above is a command the engine actually ran; items I judged from reading the source (CODEOWNERS ordering, the two-arcs observation, the capstone-hides-Q19 continuity finding) are labelled as source-line reasoning, not execution.
- **What I ran vs. reasoned:** I ran no quest commands myself; I read all five quest sources in plan order and cross-checked each engine finding against the exact source lines it cites. The linked-journey analysis (§ Chain Continuity) is my own reasoning over those sources plus the sealed per-quest verdicts.
- **Coverage & limits:** This is **window 2 of 3** — quests 11–15 of the 15-quest level 1100. Quests 1–10 (windows 1 & 3, including the Autonomy Levels Matrix that Q19 depends on and ETL Pipeline Design that the Data Engineering arc assumes) were **not** in this session; the ledger accumulates them across runs. Snippet coverage was partial by design: the Warden's Pact exposed only 1 of 7 snippets as literally runnable (the rest are illustrative YAML/CODEOWNERS/markdown, reasoned statically), and the Capstone 1 of 9. Full execution coverage was strongest on Spark (10 runnable) and Data Quality (9/9 runnable). No network access beyond what quests required; the Kafka/Docker and pip installs happened inside the sealed engine sandbox, not here.
- **Confidence:** High on the three high-severity blockers (each backed by a reproduced error string) and on the two passes (Spark and the Capstone validator both executed end-to-end with matching output). Medium on the "two-arcs" slicing observation, which is a curriculum-design judgment rather than an executable fact.

---

<details><summary>Appended machine evidence (verbatim from walk-evidence.md)</summary>

**5** quests evaluated · ✅ 2 pass · ⚠️ 0 warn · ❌ 3 fail · avg **64.0%** · ~$3.4092

| | Score | Quest | Snippets run |
|---|--:|---|:-:|
| ❌ | 34 | The Warden's Pact: Guardrails and Human-in-the-Loop Patterns | 4/1 (4✗) |
| ✅ | 85 | Trial of the Agentic Codex: The Grand Capstone | 5/1 |
| ✅ | 95 | Apache Spark Mastery: Big Data with PySpark | 7/10 |
| ❌ | 56 | Stream Processing: Real-Time Data with Apache Kafka & Flink | 6/7 (3✗) |
| ❌ | 50 | Data Quality Engineering: Validation & Monitoring | 8/9 (3✗) |

</details>
