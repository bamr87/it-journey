---
title: Data Scientist · L1100 · 2026-07-16
description: Quest-perfection walkthrough of the Data Engineering slice data-scientist/1100 on 2026-07-16,
  engine verdict fail. An evidence-based, learner's-eye…
date: '2026-07-16T12:56:23.000Z'
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
  from 2026-07-16.'
slice: data-scientist/1100
character: data-scientist
level: '1100'
theme: Data Engineering
tier: Master
verdict: fail
quest_count: 5
walk_date: '2026-07-16'
run_url: https://github.com/bamr87/it-journey/actions/runs/29494904212
source_report: test/quest-validator/walkthroughs/2026-07-16-data-scientist-1100.md
---

> **Slice** `data-scientist/1100` · **Level** 1100 (Data Engineering) · **Master tier** · **Engine verdict** ❌ fail · **Walked** 2026-07-16
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29494904212) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-16-data-scientist-1100.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-16-data-scientist-1100.md)

---

## 🎯 Session Summary

I walked window **1 of 3** of the Data Scientist's Level **1100 (Data Engineering, Master tier)** — five `main_quest` files, dependency-sorted, played end-to-end by the sealed agentic **execute** engine and then re-read by me as a linked learner journey. The headline is **fail**: only the one genuinely on-theme data quest holds up.

**Data Warehousing** (the single SQL / dimensional-modeling quest in this window) is excellent — **92%, every runnable snippet ran and matched the documented output**. The other four quests are not really data-science content at all; they are GitHub-Actions / agentic-CI automation chapters from two unrelated quest lines that happen to carry the `1100` level tag. Each of those four ships copy-pasteable code with a **verified runtime bug**: two share the identical leaked-Jekyll-`{​% raw %​}` artifact that breaks `${​{ ... }​}` expressions, and two share GitHub-Actions permission / git-identity defects. A data-scientist learner who reached this level for warehousing would sail through the first quest and then hit four broken automation workflows that a maintainer should fix before learners rely on the code.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|--:|:--:|---|--:|---|
| 1 | ✅ pass | Data Warehousing: Build a Dimensional Star Schema in SQL | 92 | Every SQL/DuckDB snippet executed as documented; only a minor SQLite-FK-enforcement caveat. |
| 2 | ⚠️ warn | The Editor's Eye: A Reviewer, and the Dragon It Becomes | 64 | Sound design, but a real YAML syntax error in the BROKEN example + an actionlint-confirmed script-injection anti-pattern in the "safe CI" reference code. |
| 3 | ❌ fail | The Bard Forge: The Quest That Writes Quests | 57 | Logic works, but the `contents: read`-only permissions block 403s the script's own `gh pr view`, and the proposal-PR `git commit` fails (exit 128) with no git identity. |
| 4 | ❌ fail | The Agent Pantheon: Multi-Agent Lifecycle Management | 54 | Leaked `{​% raw %​}` breaks the artifact-name expression, two referenced scripts never provided, and a status-enum / workflow-filename mismatch. |
| 5 | ❌ fail | The Autonomy Scales: Mapping Agent Autonomy Levels | 59 | Same leaked-`{​% raw %​}` artifact (×4) causes a verified `bad substitution`; `\n` in a double-quoted PR body never becomes a newline; unscoped PR lookup. |

## 🔬 Evidence

All outcomes below come from commands the execute engine actually ran in its disposable per-quest sandbox (quoted/trimmed from `walk-evidence.json`). Snippet coverage is reported as ran/passed/failed/reasoned against the recorded snippets.

### 1. Data Warehousing — ✅ 92 (ran 7/9 runnable, 7 passed, 0 failed, 2 reasoned)
- **Linux setup** `python3 -m venv .venv && … pip install … duckdb` → *"ran cleanly,
  installing duckdb 1.5.4 into the venv with no errors."* **passed**
- **Star-schema DDL** (`dim_date, dim_product, dim_customer, fact_sales`) → *"executed in
  SQLite 3.45.1 with zero errors; `.tables` confirmed all four tables created."* **passed**
- **Revenue-by-city-by-quarter GROUP BY** → *"returned correct sensible aggregates (Denver
  199.99, Austin 49.95 + 29.97 split by quarter) exactly as the quest promises."* **passed**
- **Type-2 SCD walkthrough** → *"produced exactly the documented result: one closed
  historical row … and one current row."* **passed**
- **`columnar_demo.py` in DuckDB** → *"ran … in 0.36s, generating 5M rows and returning
  COUNT/SUM/AVG as documented — no modification needed."* **passed**
- macOS/Windows setup blocks → **reasoned** (Linux sandbox; syntax standard, consistent
  with the verified Linux path).
- Accuracy caveat (**reasoned**): the `REFERENCES` clauses imply enforced FK integrity, but
*"SQLite does not enforce foreign keys unless `PRAGMA foreign_keys = ON` is set — the quest never mentions this."*

### 2. The Editor's Eye — ⚠️ 64 (ran 6/6 recorded, 5 passed, 1 failed)
- **Smuggle-guard logic** — content-only diff → *"'Smuggle guard passed: content-only.'"*;
  a diff adding `.github/workflows/evil.yml` → *"correctly failed with exit 1."* **passed**
- **Loop-breaker** (`git log -1 --format='%an'` vs `content-review[bot]`) → *"correctly
produced skip=true for a bot-authored commit and skip=false for a human-authored commit."* **passed**
- **BROKEN example YAML** `with: { ref: ${​{ github.head_ref }​} }` → **failed**: *"both
PyYAML … and Ruby's Psych … reject it, because the flow-mapping `{ }` collides with the unquoted `${​{ }​}` expression syntax. A learner pasting this exact block gets a hard YAML syntax error."*
- **actionlint (v1.7.12)** on Chapter 1 + boss-fight "SLAIN" workflow → *"both flag
`git push origin HEAD:${​{ github.head_ref }​}` … as … 'potentially untrusted. avoid using it directly in inline scripts.' — a genuine script-injection anti-pattern."* **passed (finding confirmed by the run)**
- **fetch-depth clash** — combining the boss-fight `fetch-depth: 2` checkout with the
Chapter 2 smuggle-guard `git diff "origin/${BASE}...HEAD"` → *"fails with 'fatal: ambiguous argument origin/main...HEAD'."* **reasoned via reproduction**

### 3. The Bard Forge — ❌ 57 (recorded 7, ran 5, 4 passed, 1 failed, 1 skipped, 1 reasoned)
- **`scripts/mine_merge.sh` end-to-end** (mocked `gh`, real squash-merge repo) → *"The
  script's core logic … worked exactly as described and produced correct output."* **passed**
- **Permissions bug** — Chapter 1 sets `permissions: contents: read` only → *"specifying
any permission explicitly sets all unlisted scopes to `none` — including `pull-requests`. `gh pr view` … would fail with a 403."* **failed (verified against GitHub's model)**
- **Git-identity bug** — Chapter 2 "Open proposal PR" runs `git commit` on a fresh clone →
*"I reproduced this exact scenario … and got `fatal: empty ident name … not allowed` (exit 128)."* **failed (reproduced live)**
- **Quest Network mermaid** → *"Rendered … with `mmdc` (v10) successfully."* **passed**

### 4. The Agent Pantheon — ❌ 54 (ran 5/6, 3 passed, 2 failed, 1 reasoned)
- **`_data/agents.yml`** → *"parses cleanly via PyYAML — 3 valid agent entries."* **passed**
- **Leaked Jekyll tag** — `name: health-report-${​% raw %​}{​{ github.run_id }​}{​% endraw %​}`
→ *"the resulting string is `health-report-${​% raw %​}{​{ github.run_id }​}{​% endraw %​}` — NOT `${​{ github.run_id }​}` … the artifact name would literally contain the Jekyll tag text."* **failed**
- **Missing scripts** — `load_registry.py`, `agent_health_check.py` → *"neither script
exists anywhere in the quest content; a learner … gets an immediate 'No such file or directory' failure on the very first job step."* **failed**
- **`python3 scripts/validate_quest.py --quest q17`** → *"failed with … No such file or
  directory — the validator is never provided or linked."* **failed**
- Internal contradictions (**reasoned/accuracy**): `status: beta` used in Chapter 3 but
absent from the Chapter 1 enum; `agent-health-check.yml` vs the created `agent-health-monitor.yml`.

### 5. The Autonomy Scales — ❌ 59 (ran 2/5, 1 passed, 1 failed, 2 skipped, 1 reasoned)
- **`_data/autonomy-matrix.yml`** → *"parses cleanly with PyYAML (5 task_classifications …);
  yamllint only flags cosmetic issues."* **passed**
- **Leaked Jekyll tag ×4** — `${​% raw %​}{​{ github.event.issue.number }​}{​% endraw %​}` in
`feature-agent-l2.yml` → *"I extracted the exact `run:` string and executed it in bash: `line 1: ${​% raw %​}…{​% endraw %​}: bad substitution`, exit 1."* **failed**
- **`\n` in PR body** — `--body "…\n\n…"` in a plain double-quoted bash string → *"bash does
NOT convert `\n` to a real newline in this context — literal `\n\n` would land in the PR body."* **reasoned via reproduction**
- **`review_autonomy_compliance.sh`** — passes `bash -n` but *"unscoped … `gh pr list
--search 'head:copilot/'` … so every loop iteration would report the same (first) matching PR."* **skipped/reasoned** (sandbox `gh` unauthenticated).

## 🐞 Issues Found

Grouped by quest; every item is evidenced by a command run (or an exact quoted line) above. No issue is raised for the passing Data Warehousing quest beyond its one minor accuracy caveat.

- **[high] The Editor's Eye · boss-fight BROKEN example (lines ~195–211)** — *Observed:*
`with: { ref: ${​{ github.head_ref }​} }` is a hard YAML syntax error (PyYAML + Ruby Psych both reject the flow-mapping/`${​{ }​}` collision). *Fix:* quote the expression inside the flow mapping or use block style, so the block fails for the intended pedagogical reason, not on paste.
- **[high] The Editor's Eye · Chapter 1 + boss-fight git push** — *Observed:* actionlint
flags `git push origin HEAD:${​{ github.head_ref }​}` in `run:` as an untrusted-expression script-injection risk — in a quest whose whole premise is "event-safe" CI. *Fix:* pass `github.head_ref` through `env:` and reference `"$HEAD_REF"`; add an explicit callout.
- **[medium] The Editor's Eye · fetch-depth mismatch** — *Observed:* naively combining the
boss-fight `fetch-depth: 2` checkout with the Chapter 2 smuggle guard's `origin/main...HEAD` diff → "ambiguous argument … unknown revision". *Fix:* show one consolidated workflow with a single consistent `fetch-depth: 0`.
- **[high] The Bard Forge · Chapter 1 permissions** — *Observed:* `permissions: contents:
read` alone zeroes `pull-requests`, so `mine_merge.sh`'s `gh pr view` 403s. *Fix:* add `pull-requests: read`.
- **[high] The Bard Forge · Chapter 2 "Open proposal PR"** — *Observed:* `git commit` on a
fresh clone with no identity → exit 128 (reproduced). *Fix:* add `git config user.name / user.email` before the commit.
- **[high] The Agent Pantheon · Chapter 2 artifact name** — *Observed:* leaked
`${​% raw %​}{​{ github.run_id }​}{​% endraw %​}` yields a literal Jekyll string, not the run ID. *Fix:* wrap the whole fenced block in `{​% raw %​}`/`{​% endraw %​}` at the Markdown level so the visible YAML is plain `${​{ github.run_id }​}`.
- **[high] The Agent Pantheon · missing scripts** — *Observed:* `load_registry.py`,
`agent_health_check.py`, and `scripts/validate_quest.py` are referenced but never provided → "No such file or directory". *Fix:* provide/link them or mark clearly as platform-supplied and out of scope.
- **[medium] The Agent Pantheon · internal inconsistencies** — *Observed:* `status: beta`
absent from the documented enum; `agent-health-check.yml` vs the created `agent-health-monitor.yml`. *Fix:* reconcile the enum and the filename everywhere.
- **[high] The Autonomy Scales · Chapter 3 `feature-agent-l2.yml`** — *Observed:* leaked
`${​% raw %​}{​{ github.event.issue.number }​}{​% endraw %​}` (×4) → verified `bad substitution` at runtime. *Fix:* strip the leaked raw tags so the block renders valid `${​{ github.event.issue.number }​}`.
- **[medium] The Autonomy Scales · PR-body `\n`** — *Observed:* `\n\n` in a plain
  double-quoted bash arg stays literal. *Fix:* use `$'...\n\n...'` or a heredoc.
- **[medium] The Autonomy Scales · `review_autonomy_compliance.sh`** — *Observed:* unscoped
`gh pr list --search "head:copilot/"` returns the first match every iteration. *Fix:* scope the lookup to the specific run/branch.
- **[low] Data Warehousing · SQLite FK enforcement** — *Observed:* `REFERENCES` clauses
imply enforced integrity but SQLite needs `PRAGMA foreign_keys = ON`. *Fix:* add a one-line note (or the PRAGMA) so learners don't over-trust FK validation.

## 🔗 Chain Continuity

The most important finding of this walk is structural: **Level 1100 here is a difficulty/theme band, not a single learning path**, and this window interleaves **three unrelated quest lines**:

1. **`data-warehousing`** — quest_line *"The Data Engineer's Ascent"* (SQL). Its declared
`required_quests` is `/quests/1100/etl-pipeline-design/` and it unlocks apache-spark / data-quality — a coherent Data-Engineering spine, and the only quest that matches the Data Scientist's stated Level-1100 theme.
2. **`self-operating-website-06` and `-10`** — quest_line *"The Self-Operating Website"*
(GitHub Actions / Claude Code). Their prerequisites are Chapter V (`/quests/1010/…`) and Chapter IX (`/quests/1110/…`) respectively — **neither is in this window**, and they are two non-adjacent chapters (06 and 10) of a serialized campaign, so a learner meeting them here lands mid-story with the intervening chapters missing.
3. **`agentic-multi-agent-lifecycle-management` (Q17)** and **`agentic-autonomy-levels-matrix`
(Q18)** — quest_line *"gh-600 / The Agentic Codex"*. These are the **only genuine dependency edge inside the window**: Q17's `unlocks_quests` lists Q18, Q18's `required_quests` lists Q17, and the planner ordered them correctly (Q17 → Q18). Q17 still assumes Q16 (`/quests/1011/agentic-multi-agent-failure-recovery/`), outside the window.

**Prerequisite reality:** 4 of the 5 quests declare required/recommended prerequisites that live *outside* this window (earlier levels or other chapters). That is expected for a windowed sweep (window 1 of 3; the ledger accumulates the rest), but it means **this window does not stand alone as a journey** — a Data Scientist arriving for "Data Engineering mastery" gets one on-theme quest and four DevOps/agentic-automation quests from stories they haven't started.

**Cross-quest defect patterns** (the real value of reading the chain as one journey):
- The **leaked Jekyll `{​% raw %​}` artifact** appears identically in *both* gh-600 quests
(#4 and #5) — this is a **systemic rendering bug in the gh-600 source**, not two isolated typos, and any fix pass should sweep the whole `quest_line: gh-600` for the same pattern.
- The **GitHub-Actions safety defects** (permission scoping in #3, script-injection in #2,
git-identity in #3) cluster in the two *Self-Operating Website* quests — ironic given both quests explicitly teach "safe/event-safe automation." A learner following that line literally copies an anti-pattern the quest is trying to warn against.

Net: within the window the only edge that actually holds together for a learner is **Q17 → Q18**, and even that edge carries the same broken workflow code in both quests.

## 🧠 Reasoning & Method

- **Mode:** `execute` — the workflow pre-computed and **sealed** `walk-evidence.json` /
`walk-evidence.md` by running `test/quest-validator/agentic_validate.py --mode execute` in a disposable per-quest sandbox before I started. I consumed that evidence **as-is** and did **not** re-run the engine (its child `claude` processes can't authenticate from my Bash tool). Every `passed`/`failed` above is an engine-run command; anything I marked `reasoned` is a static/simulated judgment the engine labeled as such.
- **What I ran vs. reasoned:** I ran no quest commands myself — my Bash use was limited to
reading `walk-plan.json`, the two evidence files, and the five quest sources. My value-add is the **linked-journey analysis** in §🔗 (dependency graph, window composition, and the two cross-quest defect clusters), derived from reading each quest's frontmatter/dependencies in plan order against the sealed per-quest verdicts.
- **Coverage & limits:** This is **window 1 of 3** (offset 5) of a **15-quest** level — I
walked exactly the 5 planned quests and did **not** expand to the rest of the level; the ledger sweeps the other windows over subsequent runs. macOS/Windows setup blocks and any auth-gated `gh`/`claude` invocations were `reasoned`/`skipped` (Linux, unauthenticated sandbox), as the engine notes. Snippet coverage per quest is stated numerically in §🔬.
- **Confidence:** High on the four verified runtime bugs (each reproduced or confirmed
against a documented model in the sandbox) and on Data Warehousing's clean pass. High on the continuity findings (they derive directly from the quests' own `quest_dependencies` and `quest_line` frontmatter). The three `fail` verdicts reflect real, copy-paste-breaking defects, not stylistic nits — they should be fixed before learners rely on this window's automation code.

---

### Appendix — machine evidence (verbatim excerpt)

> **5** quests evaluated · ✅ 1 pass · ⚠️ 1 warn · ❌ 3 fail · avg **65.2%** · ~$3.8435
>
> | | Score | Quest | Snippets run |
> |---|--:|---|:-:|
> | ✅ | 92 | Data Warehousing: Build a Dimensional Star Schema in SQL | 7/9 |
> | ⚠️ | 64 | The Editor's Eye: A Reviewer, and the Dragon It Becomes | 6 (1✗) |
> | ❌ | 57 | The Bard Forge: The Quest That Writes Quests | 5 (1✗) |
> | ❌ | 54 | The Agent Pantheon: Multi-Agent Lifecycle Management | 5 (2✗) |
> | ❌ | 59 | The Autonomy Scales: Mapping Agent Autonomy Levels | 2 (1✗) |
</content>
</invoke>
