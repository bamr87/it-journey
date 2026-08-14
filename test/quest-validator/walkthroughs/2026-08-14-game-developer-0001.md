---
title: 'Walkthrough — Game Developer · Level 0001 (Web Fundamentals)'
date: '2026-08-14T00:00:00.000Z'
character: game-developer
level: '0001'
theme: Web Fundamentals
tier: Apprentice
quest_count: 5
mode: execute
overall_verdict: fail
session:
  window: '1 of 6 (quests 1–5 of 26)'
  engine_average: 62.0
  engine_counts: '2 pass · 1 warn · 2 fail'
  engine_cost_usd: 5.3181
  evidence: walk-evidence.json (sealed by the workflow; consumed as-is)
---

## 🎯 Session Summary

I walked the first window (5 of 26 quests) of the **Game Developer → Level 0001 "Web Fundamentals" (🌱 Apprentice)** slice as a beginner learner would, in plan order, using the sealed execute-engine evidence (`walk-evidence.json`) plus a close read of every quest source. The window is a mixed bag that trends downward: two genuinely strong quests (**Bootstrap 94%**, **CSS Styling Basics 82%**), one flawed-but-usable quest (**Advanced Markdown 63%**), and **two failing quests** (**Barodybroject Stack Analysis 46%**, **Building & Testing the Git Init Shell Script 25%**). Engine average **62.0%**.

**Headline verdict: `fail`** — not because the whole slice is bad, but because two of the five quests contain *blocking, execution-verified* defects a learner cannot work around: the git-init quest is built entirely on a `scripts/git_init.sh` file that **does not exist in the repo** (I confirmed this first-hand), so every command in it errors out; and the Barodybroject quest's one runnable setup sequence fails on a wrong `DB_NAME`. The two CSS/Bootstrap main quests are the backbone of this level and hold up under real rendering. A maintainer can act on the issues below in priority order (git-init first — it is unwinnable as written).

## 🗺️ The Journey

Plan order (as `walk-plan.json` selected):

1. ⚠️ · **Advanced Markdown: Tables, Footnotes & Kramdown** · **63** · Tables/footnotes/attrs/def-lists render exactly as claimed, but two *Primary Objectives* (fenced code, task lists) silently fail on vanilla kramdown, and the Advanced Challenge contradicts its own validation.
2. ❌ · **Technology Stack Analysis: Barodybroject** (side quest) · **46** · A polished static analysis *report*, not an interactive quest — its only runnable command (`migrate`) fails on a wrong `DB_NAME`, and drift vs. the live repo is severe, not "minor."
3. ✅ · **CSS Styling Basics: Selectors, the Box Model & Layout** · **82** · Every CSS/HTML snippet parsed + rendered in headless Chrome with computed styles matching claims; one un-flagged Ch.2→Ch.3 `.card-grid` override is the only real defect.
4. ✅ · **Bootstrap Framework: Build Responsive Sites Fast** · **94** · Every class/variable cross-checked against a fresh Bootstrap 5.3.8 install and the Sass override actually compiled; only gap is two named-but-undemonstrated components (alerts, modal).
5. ❌ · **Building & Testing the Git Init Shell Script** · **25** · The `scripts/git_init.sh` the entire quest tests **does not exist in the repo** — every `bash -n` / run / bats / shellcheck command fails `No such file or directory`.

## 🔬 Evidence

All per-quest numbers, commands, and outcomes below come from the sealed execute pass (`walk-evidence.json`, `--mode execute`, real commands in a disposable sandbox). I additionally ran two read-only checks of my own on the host repo (noted as `reasoned`/verified) and read all five sources.

### 1. Advanced Markdown — 63% (warn) · ran 12/13 snippets, 10 passed / 2 failed / 1 reasoned
- **Passed (rendered exactly as documented via kramdown 2.5.2):** tables with `:---`/`:--:`/`---:` alignment → `text-align: left/center/right`; footnote `[^speed]` → superscript link + `<div class="footnotes">`; callout blockquotes; attribute list `{: .lead #intro }` → `<p class="lead" id="intro">`; definition list → `<dl><dt><dd>`; frontmatter parses as valid YAML; `{% raw %}…{% endraw %}` renders literally.
- **Failed — Primary Objective:** task lists `- [x]` / `- [ ]` rendered as literal `<li>[x] Learn tables</li>` with "No link definition for link ID" warnings — **not** checkboxes — until `kramdown-parser-gfm` + `input: GFM` was installed (undocumented).
- **Failed — Primary Objective:** fenced ```` ```python ```` blocks rendered as inline `<code>` inside a `<p>`, not a highlighted `<pre><code class="language-python">`, under default kramdown (native fence is `~~~`); only worked after switching to `input: GFM`.
- **Reasoned:** on GitHub Pages the `github-pages` gem forces GFM, so both "just work" there — but the quest's own System Requirements imply a vanilla install, where they don't.
- Resource links all returned HTTP 200.

### 2. Barodybroject Stack Analysis — 46% (fail) · ran 9/23 snippets, 6 passed / 3 failed / 12 skipped / 2 reasoned
- **Failed (verified bug):** the flagship Quick Setup block (source L677) does `export … DB_NAME=barodybroject …` then `python manage.py migrate`, which throws `django.db.utils.OperationalError: FATAL: database "barodybroject" does not exist`. The engine started the project's own `.devcontainer/docker-compose_dev.yml` Postgres, which creates **`barodydb`**; re-running with `DB_NAME=barodydb` succeeded (`OK`). I confirmed the offending line first-hand: source line 677 reads `export DB_HOST=localhost DB_NAME=barodybroject …`.
- **Passed:** `pip install -r src/requirements.txt` in a clean venv; `pip-audit` ("No known vulnerabilities found"); `pip list --outdated`.
- **Failed (illustrative excerpts run standalone):** the settings.py DB-config excerpt and the Redis `CACHES` excerpt both `NameError: name 'env' is not defined` — expected for excerpts, but nothing labels them non-runnable.
- **Content drift (verified against the live clone):** Django is **5.1.15** live, not the **4.2.20** the doc restates throughout; README is **71 lines**, not the "1,000+" claimed three times; `settings.py`/`views.py` are now split into packages; `django-filer` is absent. The single top-of-doc disclaimer under-states this.

### 3. CSS Styling Basics — 82% (pass) · ran 13/16 snippets, 12 passed / 1 failed / 2 skipped / 1 reasoned
- **Passed (headless Chrome, computed styles matched claims exactly):** `.lead` `box-sizing:border-box` keeps total width 300px; `#hero` 40px (2.5rem×16); `.site-header` `display:flex`/`space-between`; descendant combinator zeroed the `<h1>` margin; custom properties resolved (`--brand`=#2563eb, `--space`=16px, `--radius`=8px); media queries flipped 1→2→3 columns at 600/960px.
- **Failed (real behavioral gap):** when Ch.2's `.card-grid { repeat(auto-fit, minmax(200px,1fr)) }` and Ch.3's `.card-grid { 1fr }` + media queries are concatenated into one stylesheet **as instructed**, Ch.3 silently wins — at 1300px, Ch.2 alone gives 4 auto-fit columns but the combined sheet locks to 3. The quest never flags that Ch.3 supersedes Ch.2's "cards wrap automatically" demo.
- **Skipped/reasoned:** the Windows PowerShell path couldn't be verified on Linux (standard native syntax; failure was a cross-OS testing artifact, not a defect).

### 4. Bootstrap Framework — 94% (pass) · ran 8/10 snippets, 8 passed / 0 failed / 2 reasoned
- **Passed (cross-checked against a freshly-installed Bootstrap 5.3.8):** starter HTML parses valid; grid (`container`/`row`/`col-md-8`/`col-md-4`), navbar collapse API (`navbar-toggler`, `data-bs-toggle`, `data-bs-target`), card classes, and utilities all exist as documented — e.g. `.mt-4 { margin-top: 1.5rem !important }` matched exactly.
- **Passed (SCSS build actually run):** `npm install bootstrap sass` → compiled `custom.scss` with `npx sass … --load-path=node_modules` → output contained `--bs-primary: #6d28d9`, proving the override works.
- **Reasoned:** `open`/`xdg-open`/`Start-Process` couldn't open a browser in the headless sandbox (environment limit, not a defect). Minor: CDN pins 5.3.3 while npm resolves 5.3.8 — no breaking changes.

### 5. Building & Testing the Git Init Shell Script — 25% (fail) · ran 6/6 runnable snippets, **0 passed / 6 failed**
- **Failed (core deliverable missing):** cloning the repo per "Get the script first" succeeds, but the checkout contains **no `scripts/git_init.sh`**. I verified this myself on the host repo: `ls scripts/git_init.sh` → `No such file or directory`, and a glob for `*git*init*` under `scripts/` returned nothing.
- **Failed:** `bash -n scripts/git_init.sh` → exit 127 `No such file or directory`; the `--headless … --scaffold python` run → exit 127; the quest's own example bats test → `not ok 1` (inner command exits 127); `shellcheck scripts/git_init.sh` → exit 2 `does not exist`.
- The engine searched all branches/tags after `git fetch --unshallow` and found the file has **never existed** in this repo's history. Every one of the six Acceptance Criteria is therefore unverifiable.

## 🐞 Issues Found

- **HIGH · Git Init Shell Script · core prerequisite (`scripts/git_init.sh`) / entire quest** — The script the whole quest builds on does not exist anywhere in `bamr87/it-journey` (confirmed by me: `ls scripts/git_init.sh` → not found; and by the engine's full-history branch/tag search). All 6 runnable commands fail `No such file or directory`; the quest is uncompletable as written. **Fix:** add the actual `scripts/git_init.sh` (with the documented `--headless/--no-push/--gitignore/--scaffold/--dry-run` interface) to the repo, or repoint the quest at the correct repo/path — then re-verify every acceptance criterion against real output. Until then this quest should arguably be marked `draft`.
- **HIGH · Barodybroject · Quick Setup bash block (source L677)** — `DB_NAME=barodybroject` is wrong; the project's dev Postgres creates `barodydb`, so `python manage.py migrate` throws `OperationalError: database "barodybroject" does not exist`. Engine verified `DB_NAME=barodydb` makes it succeed. **Fix:** change the value to `barodydb` (or whatever the current `docker-compose_dev.yml` `POSTGRES_DB` default is).
- **HIGH · Advanced Markdown · Advanced Challenge (Chapter 3 / Mastery Challenges)** — Instruction "Use `{% raw %}{{ page.title }}{% endraw %}` in the body" contradicts its own validation "the title appears from frontmatter"; verified with the Liquid gem that raw-wrapping renders `{{ page.title }}` literally, so the validation can never pass as written. **Fix:** tell learners to use a plain (non-raw) `{{ page.title }}` in the body, and clarify separately that only the *Liquid-teaching example* should be raw-wrapped.
- **MEDIUM · Advanced Markdown · System Requirements / Ch.1 task lists / Ch.2 fenced code** — Two Primary Objectives (GFM task-list checkboxes, backtick fenced code) don't render on a vanilla kramdown install; they need `kramdown-parser-gfm` + `input: GFM`, which the quest never mentions. **Fix:** add a caveat (or the `_config.yml` `kramdown: { input: GFM }` snippet) noting these are GFM features enabled by default on GitHub Pages.
- **MEDIUM · Barodybroject · overall structure** — Objectives are stated but never operationalized: no numbered tasks, no validation checkpoints, no XP/rewards (`rewards.progression_points: 0`, empty `validation_criteria`). It reads as a static report, not an interactive quest. **Fix:** add hands-on steps tied to each objective plus explicit "you're done when…" criteria.
- **MEDIUM · Barodybroject · content accuracy / drift** — Django 4.2.20 (live 5.1.15), "1,000+ line README" (live 71), split settings/views, and dropped `django-filer` make several sections misleading despite the single disclaimer. **Fix:** regenerate against the live repo or add per-section "as of <date>" callouts near volatile facts.
- **MEDIUM · Barodybroject · illustrative excerpts (settings.py DB config, CACHES)** — Run standalone they `NameError: name 'env' is not defined`; nothing marks them non-runnable. **Fix:** label as "excerpt — assumes env/BASE_DIR already configured."
- **LOW · CSS Styling Basics · Ch.2 → Ch.3 `.card-grid` override** — Concatenating the chapters as instructed makes Ch.3's fixed-column media queries silently override Ch.2's `auto-fit` demo; the Ch.2 checkpoint ("cards reflow…") behaves differently after Ch.3. **Fix:** add a one-line note that Ch.3 intentionally replaces Ch.2's auto-fit rule (or scope them to different classes). Also: Ch.3 lacks the "⚡ Quick Wins and Checkpoints" block Ch.1/2 have.
- **LOW · Bootstrap · completeness** — "alerts" (Primary Objective) and "a modal" (Secondary Objective) are named but never demonstrated with code. **Fix:** add a short alert snippet and a minimal modal example, or drop them from the objective list.
- **LOW · Advanced Markdown & others · VS Code `code` CLI assumption** — Setup blocks call `code guide.md`; a learner without the VS Code shim on PATH sees it "fail." **Fix:** add "or open the file in any text editor."

## 🔗 Chain Continuity

Read as one Game-Developer Apprentice journey, this window has a **coherent web-fundamentals spine but a weak, mis-ordered tail**:

- **The strong spine is CSS → Bootstrap.** CSS Styling Basics (#3) teaches the box model, flexbox/grid, and responsive media queries; Bootstrap (#4) then hands the learner a component library that assumes exactly that CSS grounding — and its frontmatter even lists `css-styling-basics` as a recommended prerequisite. That is the one place the chain's dependency metadata and the actual learning path agree, and both quests execute cleanly. A learner finishing #3 is genuinely ready for #4.
- **Advanced Markdown (#1) is a fine standalone opener** (it has no required prerequisites and unlocks SEO/Jekyll-plugins), but its two silently-failing Primary Objectives mean a beginner's very first hands-on quest in the path can leave them thinking they did something wrong — a poor confidence-setter at the front of the slice.
- **The two failing quests are only loosely part of this journey.** Barodybroject (#2) is a Django/Azure *backend stack analysis* — its skill focus is backend, it's a side quest, and it assumes Python/Docker/Postgres a Web-Fundamentals apprentice hasn't been given yet. It sits in the slice as a level-0001 side quest but doesn't build on #1 or feed #3/#4; a game-developer beginner would be parachuted into an unrelated (and currently broken) enterprise codebase. Git-Init (#5) is a shell-scripting/testing quest whose prerequisite is a repo file that doesn't exist, so it dead-ends immediately.
- **Prerequisite gaps:** none of these five declares the others as required (`required_quests: []` throughout), so ordering is driven by the planner, not by authored dependencies. That's fine for the CSS→Bootstrap pair but means the two failing quests can be hit with no scaffolding. Neither #2 nor #5 provides fallback/troubleshooting for the exact first error a learner will hit (wrong DB name; missing script), which is where a real beginner gets stuck and quits.

Net: the slice does **not** currently hold together as an end-to-end path for this character — a learner walking 1→5 in order hits a demotivating silent failure at #1, an unrelated broken backend quest at #2, recovers on the solid #3/#4, then dead-ends at #5. The CSS/Bootstrap middle is ready to ship; the bookends need work.

## 🧠 Reasoning & Method

- **Mode:** `execute` — the workflow pre-computed and **sealed** `walk-evidence.json` / `walk-evidence.md` with the agentic execute engine (`agentic_validate.py`, real commands in a disposable sandbox). I consumed those verbatim and did **not** re-run, edit, or regenerate them (the engine's child processes can't authenticate from my Bash tool). Every `passed`/`failed` above is the engine's sandboxed result.
- **What I ran myself (read-only, host repo):** two verification checks — `ls scripts/git_init.sh` (→ not found) and a glob for `*git*init*` under `scripts/` (→ empty), independently confirming the git-init quest's blocking defect; and a source-line check confirming Barodybroject L677's `DB_NAME=barodybroject`. Everything else labeled a finding is the engine's evidence or a direct quote from the quest source, which I read in full for all five quests.
- **What I reasoned about (not executed by me):** the linked-journey/chain-continuity analysis above is static reasoning over the five sources + frontmatter dependency metadata, not a command result. Cross-OS paths (Windows PowerShell in CSS/Bootstrap) and GUI-open steps were `reasoned`/environment-limited in the sandbox, not genuine defects.
- **Coverage & limits:** this is **window 1 of 6** — 5 of the level's 26 quests. I make **no claim** about the other 21; the ledger accumulates the rest across future runs. Nothing was destructively run. `available_runnable` vs `ran` gaps (e.g. Barodybroject ran 9 of 23 recorded snippets, 12 skipped) reflect the engine's safety/relevance filtering, reported honestly rather than inflated.
- **Confidence:** high on the two blocking failures (execution-verified and independently reconfirmed by me), high on the two passes (rendered/compiled with concrete computed-style and CSS-variable evidence), and high on the Advanced Markdown warn (both defects reproduced through kramdown/Liquid). Confidence on the chain-continuity judgments is moderate — they are sound inferences from the sources, not runtime observations.

_No content was modified. This is a report artifact under `test/` (Jekyll-excluded); the caller handles git._
