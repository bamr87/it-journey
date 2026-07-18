---
title: Data Scientist · L1100 · 2026-07-18
description: Quest-perfection walkthrough of the Data Engineering slice data-scientist/1100 on 2026-07-18,
  engine verdict warn. An evidence-based, learner's-eye…
date: '2026-07-18T00:00:00.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Data Scientist
tags:
- data-scientist
- level-1100
- walkthrough
- quest-perfection
- warn
- data-engineering
render_with_liquid: false
excerpt: 'Data Scientist · Level 1100 — Data Engineering: an evidence-based quest-perfection walkthrough
  from 2026-07-18.'
slice: data-scientist/1100
character: data-scientist
level: '1100'
theme: Data Engineering
tier: Master ⚡
verdict: warn
quest_count: 5
walk_date: '2026-07-18'
run_url: https://github.com/bamr87/it-journey/actions/runs/29642483805
source_report: test/quest-validator/walkthroughs/2026-07-18-data-scientist-1100.md
---

> **Slice** `data-scientist/1100` · **Level** 1100 (Data Engineering) · **Master ⚡ tier** · **Engine verdict** ⚠️ warn · **Walked** 2026-07-18
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29642483805) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-18-data-scientist-1100.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-18-data-scientist-1100.md)

---

## 🎯 Session Summary

I walked the first window (5 of 15 quests) of the **Data Scientist → Level 1100 "Data Engineering" (Master ⚡)** slice as a learner, driving the agentic execute engine over each quest in a disposable sandbox and then reasoning about the linked journey by reading each quest's source. **Headline verdict: `warn`** — average **68.8%**, with **1 pass, 3 warn, 1 fail**. Every quest's *conceptual* content is sound and everything ran **safely** (safety scored 5/5 across all five), but **four of the five quests contain at least one concrete, reproducible defect that stops a learner cold if they copy-paste literally** — a Jinja `{​% raw %​}` escaping leak, a broken watermark SQL column, BSD-only `sed`/default-branch assumptions, a mismatched "Expected" output line, and missing setup steps.

The most actionable takeaways for a maintainer: fix **The Temple of Templates** (the `fail`, 56%) where literal `{​% raw %​}/{​% endraw %​}` artifacts break *every* Jinja snippet, and fix the two `high`-severity accuracy bugs in **ETL Pipeline Design** (broken `updated_at` watermark) and **Mastering Version Control** (BSD `sed -i ''` + `git init` defaulting to `master`). Note also that this "slice" is a **level band, not a dependency chain** — the five quests come from five different quest series, so continuity is thematic, not prerequisite-linked (see §6).

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ⚠️ warn | The Warden Pact: Guardrails & Accountability | 78 | Lab mostly runs; one "Expected" line wrong (check-ordering bug) + audit heredoc isn't real JSONL. |
| 2 | ⚠️ warn | Mastering Version Control Workflows: The Grand Merge Ritual | 62 | Strong concepts, but BSD `sed`, `master`/`main` default, and a fake `bash` block break the hands-on steps. |
| 3 | ✅ pass | Conquer King EDGAR: Siege of the SEC Data Castle | 80 | All 5 Python snippets hit the live SEC API and returned real data; objectives under-exemplified. |
| 4 | ❌ fail | The Temple of Templates: Reusable Abstractions | 56 | Literal `{​% raw %​}` artifacts silently break every Jinja snippet; C++ concepts needs unstated `-std=c++20`. |
| 5 | ⚠️ warn | ETL Pipeline Design: Scalable Python Data Pipelines | 68 | ETL core is genuinely idempotent; watermark SQL references a non-existent `updated_at` column. |

## 🔬 Evidence

All evidence below is from commands **actually run** by the execute engine in a disposable sandbox (per `walk-evidence.json`), except where labeled `reasoned` (judged statically) or `skipped` (not run — no macOS/Windows/auth/heavy-install available).

### 1. The Warden Pact — 78% (warn) · ran 14 snippets, 11 passed / 3 failed / 3 reasoned
- **`./warden.sh format-and-lint src/app.js`** → `passed`: `✅ ALLOWED: format-and-lint is L4 — autonomous, audit-logged` (exit 0), matches docs.
- **`./warden.sh implement-feature src/routes/signup.ts`** → `passed`: `⏸️ WAITING… (exit 78)`; **`APPROVED=yes …`** → `✅ ALLOWED (gated)…` (exit 0). Both match docs.
- **`./warden.sh edit-database-migration database/migrations/001.sql`** → **`failed`**: actual output `🚫 REFUSED: database/migrations/001.sql is inside forbidden path database/migrations/` (exit 1), **not** the quest's documented `🚫 REFUSED: edit-database-migration is L0 — never the agent's call`. Exit code matches; the message a learner diffs does not.
- **`agent-audit-trail.yml` heredoc extracted and run** → **`failed`**: audit entry is written across **7 physical lines**, not the single-line-per-entry **JSONL** the prose explicitly claims and justifies ("one JSON object per line you can grep").
- Attack calls (`format-and-lint .github/workflows/deploy.yml`, `casually-drop-the-database prod.sql`) → both `passed`, refused as documented. All 4 YAML config blocks parse after stripping Liquid `{​% raw %​}` tags.

### 2. Mastering Version Control — 62% (warn) · ran 5 / passed 1 / failed 4 / skipped 3 / reasoned 16
- **Chapter 1 "```bash" block containing `fix(validator): skip required field checks…`** → **`failed`**: `syntax error near unexpected token 'validator'` — a commit *message* mislabeled as runnable shell.
- **Challenge 2 setup** `sed -i '' 's/world/esteemed colleague/' greetings.txt` → **`failed`** on GNU/Linux sed: `sed: can't read s/world/…: No such file or directory` (BSD/macOS-only syntax). Also `git switch main` fails because a bare `git init` (no `init.defaultBranch=main`) creates `master` — verified on the sandbox's git 2.54. After fixing both, the conflict simulation reproduced exactly as described.
- **Chapter 4** `npx standard-version --dry-run` / `npx standard-version` → **`failed`**: `Invalid version. Must be a string. Got type "undefined"` because the section never does `git init` / adds a `version` to `package.json` (unlike Challenges 2–3 which do).
- **Chapter 5 conflict-resolution block** (conflict markers mixed with real commands in one `bash` fence) → **`failed`**: `syntax error near unexpected token '<<<'` before reaching the real `git add`/`git rebase --continue`.
- `gh api … branch protection` and `gh release create` → **`skipped`** (no auth/remote); flags verified valid. **Challenge 3 five-branch setup** → `passed` once `main` was pre-configured.

### 3. Conquer King EDGAR — 80% (pass) · ran 6 / passed 6 / reasoned 3
- **Linux venv + `pip install requests pandas`** → `passed` (requests 2.34.2, pandas 3.0.3, Python 3.12.13).
- **Level 001 `get_submissions('320193')`** → `passed`, live `data.sec.gov`: `Apple Inc. 1000`. **Level 002** → `Accounts Payable, Current 2026-03-28 57349000000`. **Level 003** → saved `apple_net_income.csv` (334 rows). **Level 004** → `Points Foreseen: 3390`. All real API data.
- **Reasoned finding:** the quest claims "Malformed CIKs → 400 errors" but live test returned **404** for both unpadded and non-numeric CIKs. Also `HEADERS` is reused in Levels 002/003/004 without redefinition → `NameError` if a learner pastes blocks into separate files.
- macOS/Windows setup blocks → `reasoned` (no such env in sandbox).

### 4. The Temple of Templates — 56% (fail) · ran 10 / passed 5 / failed 5 / skipped 2 / reasoned 3
- **`templates/base.html`, `page.html`, `partials/button.html`, extended `page.html`** as literally shown → **`failed`**: every block is wrapped in literal `{​% raw %​}…{​% endraw %​}` text (Jekyll/Liquid escaping that leaked into the published Markdown). Copy-pasted verbatim into `render.py`, they output literal `{​% block title %​}` text instead of the documented `<h1>Hello Acolyte!</h1>`. **No exception is thrown → silent, confusing failure.**
- After manually stripping the raw tags, **`render.py`** and the `{​% include … with context %​}` composition → `passed` (`<button class="btn secondary">Click me</button>`).
- **C++20 concepts snippet** `g++ maxof.cpp -o maxof` → **`failed`**: `'requires' does not name a type … only available with '-std=c++20'`. Default GCC 13 mode is C++17; the quest never states the flag. Compiles/runs (`7 2.5`) only with `-std=c++20`.
- **Card.jsx / Layout.jsx** verified in a real Vite + Vitest project → `passed` (2/2 tests). The "Snapshot Test" block is commented-out pseudocode requiring unstated vitest/jsdom config.

### 5. ETL Pipeline Design — 68% (warn) · ran 6 / passed 5 / failed 1 / skipped 3 / reasoned 1
- **`extract()`** → `passed`, live `jsonplaceholder.typicode.com/users`: `Extracted 10 records`. **`transform()`** → `passed`, correct shape (`ingested_at`). **`load()` + double-run idempotency** → `passed`: `SELECT COUNT(*)` stayed at 10 across two full `python etl.py` invocations, no UNIQUE errors — **idempotency genuinely demonstrated**.
- **`SELECT COALESCE(MAX(updated_at), '1970-01-01') … FROM users;`** → **`failed`**: `no such column: updated_at` — the `users` table the quest itself builds only has `ingested_at`.
- **Airflow DAG `dags/users_etl.py`** → `reasoned`: `py_compile` clean; not run (heavy Airflow install). Noted the `docker run apache/airflow:2.9.3 standalone` command has **no `-v …/dags` volume mount**, so the DAG never appears in the UI the Advanced Challenge tells learners to check.
- `pandas` is installed in every setup path but **never imported/used** anywhere in the code.

## 🐞 Issues Found

Every issue below cites a command result or quoted line witnessed in this session. Grouped by severity.

**HIGH**
1. **high · Temple of Templates · every Jinja code block (Ch.1–2)** — Blocks contain literal `{​% raw %​}…{​% endraw %​}` escaping artifacts; copy-pasted verbatim they render literal template syntax instead of the documented output, *with no error thrown*. **Fix:** strip the `{​% raw %​}` wrappers from the published Markdown (this is a rendering-pipeline leak). *(observed: `render.py` printed `{​% extends 'base.html' %​}` as text; passed only after stripping.)*
2. **high · ETL Pipeline Design · Ch.3 watermark SQL** — `SELECT … MAX(updated_at) … FROM users` throws `no such column: updated_at` against the quest's own `warehouse.db`. **Fix:** use `ingested_at`, or add/populate an `updated_at` column in the `CREATE TABLE`.
3. **high · Mastering Version Control · Challenges 2 & 3** — `sed -i '' …` is BSD/macOS-only (fails on GNU/Linux); `git init` + `git switch main` fails where `init.defaultBranch` isn't `main` (default `master`, verified git 2.54). **Fix:** use `perl -pi -e` or portable sed, and `git init -b main` (or set `init.defaultBranch` up front).
4. **high · Mastering Version Control · Ch.4 standard-version block** — `npx standard-version --dry-run` fails `Invalid version. Must be a string.` — no `git init`/`version` field setup. **Fix:** add the `git init` + versioned `package.json` preamble.
5. **high · Warden Pact · Hands-On Lab Step 3** — Documented "Expected" line for `edit-database-migration` does not match actual output (script checks forbidden-paths before autonomy level). **Fix:** reorder `warden.sh` or update the Expected block to the real forbidden-path message.
6. **high · Warden Pact · Ch.3 audit-trail heredoc** — Emits multi-line JSON, not the single-line JSONL the prose claims/justifies. **Fix:** build the JSON on one line (`jq -c` or a shell var).

**MEDIUM**
7. **medium · Mastering Version Control · Ch.1** — commit message fenced as ```` ```bash ```` → `syntax error near unexpected token 'validator'`. **Fix:** refence as `text` or prefix `git commit -m`.
8. **medium · Mastering Version Control · Ch.5** — conflict markers + real commands in one `bash` fence → `syntax error near unexpected token '<<<'`. **Fix:** split "what you'll see" (`text`) from "what you type" (`bash`).
9. **medium · Mastering Version Control · Ch.6** — `gh api … --field required_status_checks='{JSON}'` sends a literal string, not a nested object (reasoned, per `gh api --help`). **Fix:** use `--input` or `key[subkey]=value` syntax.
10. **medium · Temple of Templates · Ch.3 C++** — concepts example needs unstated `-std=c++20` (fails on default C++17). **Fix:** state the flag + compiler-version requirement.
11. **medium · Temple of Templates · React setup** — only installs the CLI globally; never shows `npm create vite@latest … --template react`, and the snapshot test is commented-out pseudocode with no vitest/jsdom config. **Fix:** add the scaffold + minimal test config.
12. **medium · ETL · docker/Airflow** — `docker run … standalone` lacks a `dags/` volume mount, so the DAG never appears in the UI the Advanced Challenge validates against. **Fix:** add `-v $(pwd)/dags:/opt/airflow/dags`.
13. **medium · EDGAR · content accuracy** — "Malformed CIKs → 400 errors" is wrong; live test returned **404**. **Fix:** correct to 404.
14. **medium · EDGAR · completeness** — objectives "fetch ≥2 CIKs", "compare ≥2 entities", CSV export, and backoff-on-all-endpoints have no example code. **Fix:** add worked examples (name a peer CIK, e.g. Microsoft 789019).

**LOW**
15. **low · ETL** — `pandas` installed in every setup path but never used. **Fix:** use it or drop it.
16. **low · EDGAR** — `HEADERS` reused across Levels 002–004 without redefinition → `NameError` if pasted into separate files. **Fix:** note the blocks are one continuous session.
17. **low · Temple of Templates** — "Follow-Up Quests" lists a *Level 1100* quest as a follow-up to this Level 1100 quest. **Fix:** point to a higher level.
18. **low · Warden Pact** — knowledge checks have no answer key. **Fix:** add collapsed self-check answers.
19. **low · Mastering Version Control** — `standard-version` (primary hands-on tool) last published 2023; unmaintained. **Fix:** flag it and prefer `release-please`/`changesets`.

## 🔗 Chain Continuity

**This slice is a level band, not a dependency chain.** Reading the five quests in plan order, they belong to five *different* quest series with no cross-quest prerequisites among them:

| Quest | Series / line | primary_technology | `required_quests` |
|---|---|---|---|
| Warden Pact | The Agentic Codex (GH-600) | github-copilot | none (recommends Domain 5) |
| Mastering Version Control | Tools Collection | git/devops | Level 0010 branches/commits |
| EDGAR | Data Realm Conquests | python | (flat prereqs) |
| Temple of Templates | Binary Function Crafting | liquid | Levels 0011/0100 |
| ETL Pipeline Design | Data Engineering Mastery | python | none (recommends **EDGAR**) |

- **The only real link in the window is ETL → EDGAR:** `etl-pipeline-design.md` lists `conquer-king-edgar` as a recommended quest, and it's a sensible ordering — EDGAR teaches "pull JSON from a live HTTP API into pandas/CSV," which is exactly the `extract()` skill ETL assumes. A learner who did EDGAR first arrives at ETL's `extract()` genuinely prepared. Good continuity there.
- **For a Data Scientist specifically, the coherence is loose.** EDGAR and ETL are on-theme (Data Engineering). The Warden Pact (agentic-AI/Copilot guardrails), Mastering Version Control (git/devops), and Temple of Templates (C++/Jinja/React abstractions) are cross-cutting engineering skills grouped by the 1100 level band, not a data-engineering throughline. That's fine as a *level* — a Master data engineer does need git, templating, and agent governance — but a learner shouldn't expect a narrative progression; each is a standalone module.
- **Prerequisite realism:** none of the five silently assumes state produced by an *earlier quest in this window* (they each set up their own sandbox), so there's no broken hand-off between quests. The friction is *within* each quest (undefined `HEADERS`, missing `git init`, unstated `-std=c++20`), not *between* them. The `updated_at` bug in ETL and the raw-tag leak in Temple are the two places a diligent learner is most likely to abandon the quest.
- **Ordering observation:** difficulty ordering in the window is uneven (Hard, Hard, Medium, Medium, Hard). The two Medium quests (EDGAR at 80, Temple at 56) sit in the middle; a learner hitting Temple's silent Jinja failure right after the confidence-building EDGAR success would be especially confused.

## 🧠 Reasoning & Method

- **Mode: `execute`** — the workflow pre-computed and **sealed** `walk-evidence.json` / `walk-evidence.md` by running `test/quest-validator/agentic_validate.py --mode execute` in a disposable sandbox before I ran. I consumed that evidence **as-is** and did **not** re-run the engine (its child `claude` processes can't authenticate from my Bash tool) and did **not** edit the plan or evidence. Every `passed`/`failed` above is an engine-run command; everything I marked `reasoned` was judged statically by the engine (no macOS/Windows env, no `gh` auth, no heavy Airflow install).
- **What I ran vs. reasoned:** I did not execute quest commands myself — the sealed engine did. My contribution is the **linked-journey pass** (§6): I read all five quest sources in plan order and their frontmatter prerequisites/series to judge continuity, and I cross-referenced every issue in §5 against a witnessed command result or a quoted quest line.
- **Coverage & limits (honest):** This is **window 1 of 3** — 5 of the 15 quests in the full Level-1100 slice (`stats.total_quests: 15`). The remaining 10 quests are **not** covered here and should be swept in later runs before the level is certified. Skipped/reasoned areas: macOS/Windows setup paths (no such env), `gh api`/`gh release` branch-protection (no auth/remote), and the Airflow standalone container (heavy install / long-running server). Engine cost ~$4.52, avg 68.8%.
- **Confidence:** High on the executed findings (real commands, real output quoted). Medium on the reasoned items explicitly labeled as such (e.g. `gh api --field` nesting, `workflow_run.workflows` glob support, GitHub `workflow_run` wildcard behavior) — the engine flagged these as offline-unverifiable, and I've preserved that caveat rather than asserting them as certain.

*No content was modified. This is a read-only witness report; a content-curator or human should act on §5.*
