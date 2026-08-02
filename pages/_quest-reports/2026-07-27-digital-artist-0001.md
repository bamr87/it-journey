---
title: Digital Artist · L0001 · 2026-07-27
description: Quest-perfection walkthrough of the Web Fundamentals slice digital-artist/0001 on 2026-07-27,
  engine verdict fail (avg 63.5%). An evidence-based…
date: '2026-07-27T00:00:00.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Digital Artist
tags:
- digital-artist
- level-0001
- walkthrough
- quest-perfection
- fail
- web-fundamentals
render_with_liquid: false
excerpt: 'Digital Artist · Level 0001 — Web Fundamentals: an evidence-based quest-perfection walkthrough
  from 2026-07-27.'
slice: digital-artist/0001
character: digital-artist
level: '0001'
theme: Web Fundamentals
tier: Apprentice
verdict: fail
quest_count: 5
engine_average: 63.5
walk_date: '2026-07-27'
run_url: https://github.com/bamr87/it-journey/actions/runs/30264458312
source_report: test/quest-validator/walkthroughs/2026-07-27-digital-artist-0001.md
---

> **Slice** `digital-artist/0001` · **Level** 0001 (Web Fundamentals) · **Apprentice tier** · **Engine verdict** ❌ fail (avg 63.5%) · **Walked** 2026-07-27
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/30264458312) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-27-digital-artist-0001.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-27-digital-artist-0001.md)

---

## 🎯 Session Summary

I walked the first window (5 of 26 quests) of the **Digital Artist (UI/UX)** path at **Level 0001 · Web Fundamentals (🌱 Apprentice)** as a learner would, consuming the sealed execute-engine evidence and reading each quest source in plan order. The window mixes strong foundational front-end content with two hard blockers and one un-scored quest, so the slice **fails** as a continuous learning path today.

The two pure teaching quests — **Advanced Markdown (92)** and **CSS Styling Basics (82)** — are technically excellent and their snippets were verified against real engines. But the window also drops a learner into **two quests that cannot be completed as written**: *Building & Testing the Git Init Shell Script (23)* targets a `scripts/git_init.sh` that **does not exist in the repo** (I independently confirmed this on the host tree), and *Technology Stack Analysis: Barodybroject (57)* ships a **broken Quick Setup** whose `DB_CHOICE=sqlite` workaround is rejected by the live app. The **Bootstrap Framework** quest returned **no verdict** — the engine hit its 40-turn ceiling retrying CDN reachability checks in the network-restricted sandbox. A maintainer should treat the git-init and barodybroject issues as the actionable fixes for this window.

## 🗺️ The Journey

Plan order (deterministic, from `walk-plan.json`; verdicts from `walk-evidence.json`):

1. ✅ **Advanced Markdown: Tables, Footnotes & Kramdown** — 92 · `main_quest` — Every markdown/kramdown/Liquid example rendered exactly as claimed; only gap is the unqualified "task lists render as real checkboxes" claim (GFM-only).
2. ❌ **Technology Stack Analysis: Barodybroject** — 57 · `side_quest` — Self-aware, well-researched, but the hands-on Quick Setup is broken and several claims drift past what its disclaimer covers.
3. ✅ **CSS Styling Basics: Selectors, the Box Model & Layout** — 82 · `main_quest` — All CSS snippets verified via headless Chromium; two real cascade bugs surface when you build the stylesheet in the order taught.
4. ❌ **Bootstrap Framework: Build Responsive Sites Fast** — no score · `main_quest` — Engine errored (`max_turns`) while probing the Bootstrap CDN; **not evaluated**, not a confirmed content defect.
5. ❌ **Building & Testing the Git Init Shell Script** — 23 · `main_quest` — Unrunnable: the single artifact every command targets (`scripts/git_init.sh`) is absent from the repository.

Engine headline: **avg 63.5% · 2 pass · 0 warn · 3 fail** (`scored 4`, `errored 1`).

## 🔬 Evidence

All command outcomes below come from the sealed `walk-evidence.json` execute pass (real commands run in the disposable sandbox). Static judgements are labelled `reasoned`.

### 1. Advanced Markdown — ✅ 92 · ran 12/13 recorded (12 passed, 1 skipped) · 4 runnable snippets
- `passed` · 3-column aligned table → correct left/center/right in **both** python-markdown and the real `kramdown` gem (`<th style="text-align: …">`).
- `passed` · Footnote `[^speed]` → superscript link + bottom `<div class="footnotes">` with back-link, matching the prose.
- `passed` · Full frontmatter file + Liquid `{​% for post in site.posts %​}` verified against the real liquid gem.
- `passed` · macOS / Windows / Linux setup blocks (`mkdir`/`touch`) all ran cleanly.
- Dimensions: commands_work 5, content_accuracy 4, completeness 5, clarity 4, structure 5, safety 5.

### 2. Technology Stack Analysis: Barodybroject — ❌ 57 · ran 6/23 recorded (5 passed, 1 failed, 6 reasoned, 11 skipped) · 8 runnable
- `failed` · **Quick Setup bash block**: `git clone`, `venv`, `pip install -r src/requirements.txt`, and `migrate` succeeded, **but** `export DB_CHOICE=sqlite && python manage.py …` is rejected by the live `settings.py`, which hard-raises for non-Postgres. This is the documented "quick local run" path (body l.671-673) and it does not work.
- `reasoned` · `requirements.txt` excerpt (l.380-418) drifts: live Django is pinned **5.1.4**, quest shows 4.2.20; the django-filer/django-cms family is absent from the live file.
- `reasoned` · settings.py excerpts (l.205-236, l.650-658) reference undefined `env`/`IS_PRODUCTION` → `NameError` if a learner runs them standalone.
- Body l.538 / l.591 claim "**None identified** in current dependency scan" — the engine notes the quest's own recommended `pip-audit` surfaces real CVEs against the pinned versions, contradicting the text.
- Dimensions: commands_work 2, content_accuracy 3, completeness 3, clarity 3, structure 2, safety 5.

### 3. CSS Styling Basics — ✅ 82 · ran 12/15 recorded (12 passed, 2 reasoned, 1 skipped) · 4 runnable
- `passed` · Selector, box-model, flexbox, grid, custom-property, and theming snippets each verified via **headless Chromium computed-style checks**.
- `reasoned` · macOS `open` / Windows PowerShell `New-Item` setup blocks judged equivalent to the Linux block that actually ran (not executed on those OSes).
- Two confirmed **cascade bugs** flagged (see Issues): Ch.3 mobile-first `.card-grid` media queries silently override the Ch.2 auto-fit grid demo; the Theming `:root { --brand }` silently overrides Ch.3's `--brand`.
- Dimensions: commands_work 4, content_accuracy 4, completeness 4, clarity 4, structure 4, safety 5.

### 4. Bootstrap Framework — ❌ no verdict (engine `max_turns`)
- No `verdict_obj`, no dimensions, no snippet record. The sealed error shows the engine looping on `curl -sI https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/…` and a general `curl -sI https://www.google.com` connectivity probe until it hit the 40-turn cap.
- **Reasoned (static read of source):** the quest loads Bootstrap purely via jsDelivr CDN (`<link …bootstrap@5.3.3…min.css>` l.237, `<script …bootstrap.bundle.min.js>` l.252) and mentions `npm install bootstrap sass` (l.381). The content is plausibly sound; it simply could not be exercised because the sandbox is network-restricted. **Not a confirmed content defect — coverage gap only.**

### 5. Building & Testing the Git Init Shell Script — ❌ 23 · ran 6/7 recorded (0 passed, 6 failed, 1 reasoned) · 5 runnable
- `failed` · `bash -n scripts/git_init.sh` → `No such file or directory (exit 127)`.
- `failed` · `bash scripts/git_init.sh --headless …` → same missing-file error; headless mode never exercised.
- `failed` · Bats test (l.28-45) → `not ok 1` (built bats-core from source since `sudo apt` is sandbox-blocked).
- `failed` · `shellcheck scripts/git_init.sh` → shellcheck 0.9.0 was preinstalled but the target file is absent.
- **Independent host-tree confirmation:** I ran `ls scripts/git_init.sh` on the checked-out repo → `No such file or directory`, and no `git*`-named script exists under `scripts/`. This corroborates the engine's clone/`git log --all`/submodule search.
- Body l.113-121 asserts "*It ships in the IT-Journey repository — clone it … chmod +x scripts/git_init.sh*", which sets the learner up to fail at the very first command.
- Dimensions: commands_work ~0 (overall 23).

## 🐞 Issues Found

- **HIGH · Building & Testing the Git Init Shell Script · core dependency / body l.59, l.113-121, l.127-155** — The entire quest targets `scripts/git_init.sh`, which **does not exist** anywhere in the repo (confirmed by the engine's clone + full `git log --all` + submodule search, and independently by me via `ls scripts/git_init.sh` on the host tree). All 5 runnable snippets fail with exit 127. *Fix:* inline the full script in the quest, commit it to `scripts/git_init.sh`, or link a specific commit/gist that contains it; then add a "confirm the script exists and is executable" precondition step.
- **HIGH · Building & Testing the Git Init Shell Script · "Get the script first" callout (l.113-114)** — The claim "*It ships in the IT-Journey repository*" is false and is the first thing a learner acts on. *Fix:* remove or correct the claim once the script actually ships.
- **HIGH · Technology Stack Analysis: Barodybroject · Quick Setup bash block (l.671-673)** — The documented `export DB_CHOICE=sqlite` no-external-DB path fails; the live `settings.py` hard-rejects SQLite. *Fix:* document a real no-external-DB path (e.g. a docker-compose local-Postgres profile) or drop the SQLite claim and require Postgres.
- **MEDIUM · Technology Stack Analysis: Barodybroject · Security & Quality section (l.538, l.591)** — "None identified in current dependency scan" is contradicted by the quest's own `pip-audit` recommendation, which surfaces real CVEs against the pinned versions. *Fix:* date-stamp the claim to the analysis date or remove it.
- **MEDIUM · Technology Stack Analysis: Barodybroject · factual drift (requirements.txt l.380-418, settings/views layout)** — Live Django is 5.1.4 (quest shows 4.2.20); django-filer/django-cms family absent from the live repo; workflow/utils/views layout drifted beyond what the top-of-doc disclaimer names. *Fix:* turn the disclaimer into a guided diff exercise, or refresh the pinned facts.
- **LOW · Technology Stack Analysis: Barodybroject · settings.py excerpts (l.205-236, l.650-658)** — Reference undefined `env`/`IS_PRODUCTION` → `NameError` if run standalone. *Fix:* label them "# excerpt — add inside settings.py where `env` is defined".
- **HIGH · CSS Styling Basics · Ch.3 vs Ch.2 `.card-grid` (cascade)** — Building the stylesheet top-to-bottom as taught, Ch.3's mobile-first `.card-grid { grid-template-columns: 1fr }` + media query **silently overrides** Ch.2's `repeat(auto-fit, minmax(200px,1fr))` demo, with no warning. *Fix:* tell the learner to replace the earlier rule, or rename the demo class.
- **HIGH · CSS Styling Basics · Theming `:root` vs Ch.3 `:root` (cascade)** — A second `:root { --brand }` in the Theming section silently overrides Ch.3's `--brand`. *Fix:* merge into one `:root` block or rename the variable.
- **MEDIUM · CSS Styling Basics · Secondary objective "Specificity"** — Named as a secondary objective/knowledge check but never taught. *Fix:* add a short paragraph on the specificity hierarchy.
- **MEDIUM · Advanced Markdown · Chapter 1 Task Lists (l.241)** — "*Task lists render as real checkboxes*" is stated unconditionally, but this is only true under GFM-mode parsing (GitHub, VS Code preview, or kramdown `input: GFM`); vanilla Jekyll/kramdown renders `- [ ]` literally. *Fix:* add a one-line caveat.
- **LOW · Advanced Markdown · setup snippets** — Trailing `code guide.md` silently fails if the VS Code `code` CLI isn't on PATH. *Fix:* note the "Install 'code' command in PATH" step.
- **INFO (not a content bug) · Bootstrap Framework · engine coverage gap** — The quest was not scored because the execute engine exhausted its 40-turn budget retrying CDN/connectivity `curl` probes in the network-restricted sandbox. No content defect is claimed; re-run in a network-enabled sandbox (or add a `--allow-domains cdn.jsdelivr.net` allowance) to get a real verdict.

## 🔗 Chain Continuity

Reading the five quests in plan order as a single Digital Artist journey:

- **Ordering is jarring for this character path.** The Digital Artist is a UI/UX learner. Quests 1 (Markdown), 3 (CSS), 4 (Bootstrap) form a coherent front-end arc — but quest 2 (**Barodybroject Django stack analysis**, a `side_quest`) and quest 5 (**git_init shell-script testing**) drop a beginning designer into a ~1,100-line backend analyst report and a Bash/Bats/shellcheck CI exercise. Neither builds on the CSS/markdown skills the arc otherwise develops. This is an artifact of the date-rotated **window** (5 of 26, level-wide not path-curated), so it reflects level ordering rather than a hand-built sequence — worth noting for maintainers weighing per-character sequencing.
- **Prerequisites are honest and self-contained.** Quests 1, 3, 4 each declare `required_quests: []` and only assume basic file editing / CLI navigation; Bootstrap correctly lists CSS Styling Basics as a *recommended* (not required) prior quest, and CSS `unlocks` Bootstrap — that pairing is internally consistent and a learner finishing CSS is genuinely ready for Bootstrap.
- **Two quests break the "leave the learner ready for the next step" contract on their own terms** — not because of a missing prior quest, but because the artifacts they depend on are absent/broken: git_init.sh does not exist, and Barodybroject's setup path is rejected by the live app. A learner following either literally hits a wall on the first hands-on command, regardless of what preceded it.
- **The strong quests are self-sufficient.** Markdown and CSS need nothing from earlier quests and deliver their stated objectives, so the arc's *teaching spine* is sound; the failures are isolated artifact/drift problems, not a cascading prerequisite gap.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sealed). I consumed `walk-plan.json` + `walk-evidence.json` / `walk-evidence.md` exactly as the workflow sealed them — I did **not** re-run the agentic engine (its child `claude` processes cannot authenticate from my Bash tool), did not edit the plan or evidence, and did not touch any quest content.
- **What I ran myself:** only read-only corroboration — `ls scripts/git_init.sh` and a scan of `scripts/` on the host tree (confirmed absent), plus reading each of the five quest sources in plan order and grep-checking the specific lines the evidence cites (git-init l.113-121, barodybroject l.671-673 / l.538 / l.591, advanced-markdown l.241, bootstrap CDN l.237-252). No quest commands were executed by me and no files were modified beyond writing this report.
- **What is `reasoned` vs `tested`:** every `passed`/`failed` above is a command the sealed engine actually ran in the sandbox. Cross-OS setup blocks (macOS/Windows) and the mermaid/settings.py excerpts are `reasoned`. The git_init.sh absence is `tested` by the engine **and** independently re-confirmed by me on the host tree.
- **Coverage & limits:**
  - **1 of 5 quests (Bootstrap) has no machine verdict** — engine `max_turns` on network probes. I only reasoned statically about it and explicitly did **not** assert a content pass/fail.
  - The sandbox is **network-restricted** (blocked the Bootstrap CDN and Barodybroject external-DB paths) and **`sudo`/apt-blocked** (bats-core was built from source). These are environment limits, not quest defects, except where a quest's *only* documented path depends on them (Barodybroject SQLite).
  - This is a **window of 5 of 26** quests for the level (`window 1 of 6`); the remaining 21 quests are out of scope for this session and are swept by later runs per the ledger.
- **Confidence:** High on the two blockers (git_init.sh absence independently reproduced; Barodybroject setup failure is a run-real failure). Medium on the CSS cascade bugs (engine-observed, plausible on read, not re-run by me). Bootstrap: no confidence in either direction — genuinely un-evaluated.
- **Overall verdict — fail:** 3 of 5 quests do not deliver a completable hands-on path in this window (2 confirmed blockers + 1 un-scored), which outweighs the two excellent teaching quests for a learner trying to walk the slice front-to-back.
