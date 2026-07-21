---
title: "Walkthrough — Game Developer · Level 0001 (Web Fundamentals)"
date: 2026-07-21T00:00:00.000Z
character: game-developer
level: "0001"
theme: Web Fundamentals
tier: Apprentice
quest_count: 5
mode: execute
overall_verdict: warn
session:
  window: "1 of 6 (offset 0, size 5)"
  total_level_quests: 26
  engine_average: 65.2
  engine_counts: { pass: 3, warn: 0, fail: 2 }
  engine_cost_usd: 5.1377
  evidence_source: ./walk-evidence.json (sealed by workflow, consumed as-is)
---

## 🎯 Session Summary

I walked the first window (5 of 26 quests) of the **Game Developer → Level 0001 "Web
Fundamentals" (🌱 Apprentice)** slice as a learner would, in the dependency-sorted
order the planner chose. Evidence was sealed by the workflow's deterministic execute
engine (`--mode execute`); I consumed `walk-evidence.json`/`.md` as-is and did not
re-run the engine.

**Headline: warn — a strong, empirically-verified teaching spine bookended by two
broken quests.** Three quests (Advanced Markdown, CSS Styling Basics, Bootstrap
Framework) score **94%** each and every syntax/layout claim in them was actually
rendered and verified (kramdown/GFM/Liquid engines, headless Chromium). But two
quests fail hard: the **Barodybroject stack-analysis** side quest (**33%**) is a stale,
mislabeled analysis report whose live-repo facts have drifted and whose code snippets
don't run, and **Building & Testing the Git Init Shell Script** (**11%**) is *not
runnable as written* — it references a `scripts/git_init.sh` that the quest never
provides, and one code block is corrupted with pasted boilerplate. A real learner
sweeping this level top-to-bottom hits a wall at the git-init quest.

## 🗺️ The Journey

Ordered as planned (window 1/6). `emoji · title · score · one-line takeaway`:

1. ✅ · **Advanced Markdown: Tables, Footnotes & Kramdown** (`main_quest`) · **94** ·
   Technically excellent; every markdown feature rendered exactly as described. Only
   pedagogical gaps (implicit GFM-Kramdown dependency; unsupported build step).
2. ❌ · **Technology Stack Analysis: Barodybroject** (`side_quest`) · **33** ·
   Stale point-in-time report; 7/12 runnable snippets fail; live-repo facts drifted;
   objectives are an auto-seeded placeholder.
3. ✅ · **CSS Styling Basics: Selectors, the Box Model & Layout** (`main_quest`) ·
   **94** · Every HTML/CSS example assembled and rendered in headless Chromium;
   box-model, flexbox, grid, breakpoints, theming all empirically verified.
4. ✅ · **Bootstrap Framework: Build Responsive Sites Fast** (`main_quest`) · **94** ·
   Accurate Bootstrap 5.3; only friction is a non-portable Windows PowerShell block
   and network-gated CDN/npm steps (a sandbox limit, not a defect).
5. ❌ · **Building & Testing the Git Init Shell Script** (`main_quest`) · **11** ·
   Not runnable: referenced `scripts/git_init.sh` never provided; all 5 snippets fail;
   a bash fence is corrupted with injected "Quest Objectives" boilerplate.

## 🔬 Evidence

All figures below are from the sealed execute-engine run (commands actually run in a
disposable sandbox). Snippet coverage is `ran/available_runnable`.

### 1. Advanced Markdown — 94% ✅ (ran 10/4 runnable; 10 passed, 0 failed, 1 skipped, 2 reasoned)
- Table / footnote / definition-list / callout / IAL blocks rendered via
  `Kramdown::Document.new(...).to_html` → alignment cells, superscript footnotes,
  `<dl>` pairs, `<blockquote>` all produced **exactly as described** (`passed`).
- Task lists + triple-backtick fences: bare kramdown rendered them as literal text,
  but installing `kramdown-parser-gfm` + `input: 'GFM'` (Jekyll's real default)
  produced real `<input type=checkbox>` and Rouge-highlighted code (`passed`).
- YAML frontmatter parsed with PyYAML; `{{ page.title }}` + `{% raw %}` for-loop
  verified with the Liquid gem (`passed`).
- macOS / Windows setup snippets `reasoned` (no macOS; pwsh confirmed `New-Item`
  works); `code guide.md` GUI launch and the Cloud comment block `skipped`.

### 2. Barodybroject Stack Analysis — 33% ❌ (ran 12/12 runnable; 5 passed, 7 failed, 9 skipped, 2 reasoned)
- **6 of 9 python-fenced snippets fail on execution** because they are *not Python*:
  directory trees → `SyntaxError: invalid character '├' (U+251C)`; `requirements.txt`
  content `Django==4.2.20` → `SyntaxError` (two dots); `pyproject.toml` TOML →
  `NameError: name 'project' is not defined`; Redis/settings excerpts →
  `NameError: name 'env' is not defined`; an `if` branch with only a comment →
  `IndentationError` (all `failed`).
- **The one real hands-on flow breaks:** `git clone --depth 1` of the live repo +
  venv + `pip install` succeeded, but `manage.py migrate` fails — the live repo now
  hard-fails `ImproperlyConfigured` on SQLite, contradicting the quest's own
  documented SQLite fallback (`failed`).
- **Factual drift confirmed against live source:** `pip-audit` (which the quest claims
  is unnecessary — "no known vulnerabilities") surfaced **numerous real CVEs** for
  Django 5.1.4 and django-allauth 65.3.0 (`passed` run, contradicting the claim). The
  clone showed Django is 5.1.4 not the quest's 4.2.20, and a `views/` package already
  exists (quest recommends splitting a monolithic `views.py`).
- Quest Objectives (source line 70–78) are the **auto-seeded placeholder**:
  "> *Note: objectives auto-seeded during framework alignment — authors should
  refine these…*" — verified directly in the source.

### 3. CSS Styling Basics — 94% ✅ (ran 12/4 runnable; 12 passed, 0 failed, 1 skipped, 2 reasoned)
- Full project assembled and **rendered in headless Chromium**; `getComputedStyle`
  confirmed border-box width stays 300px and `margin:auto` centers (232px each side in
  a 1000px viewport) (`passed`).
- `grid-template-columns: repeat(auto-fit, minmax(200px,1fr))` verified to reflow
  4 cols @1000px → 1 col @375px **with no media query**; mobile-first breakpoints then
  verified 375→1, 700→2, 1000→3 cols by screenshot (`passed`).
- CSS-variable theming toggled via `data-theme="dark"` and confirmed by screenshot
  (`passed`). `open`/macOS `skipped`; `prefers-color-scheme` `reasoned` (needs DevTools
  emulation beyond the screenshot run).

### 4. Bootstrap Framework — 94% ✅ (ran 8/4 runnable; 7 passed, 1 failed, 1 skipped, 1 reasoned)
- Starter page, navbar, card, utility-class blocks assembled and validated with
  Python's `html.parser` — all tags balanced, every cited grid/navbar/card/utility
  class matches the **real Bootstrap 5.3 API** (`passed`).
- `:root` `--bs-*` CSS-variable overrides match Bootstrap 5.2+ per-component pattern
  (`passed`); the SCSS `$primary`/`@import "bootstrap/scss/bootstrap"` block is
  `reasoned` (no network to `npm install` sass — a sandbox limit).
- **1 fail:** the Windows block `mkdir $HOME\bootstrap-quest; …` run under pwsh on
  Linux treated the literal backslash as part of the folder name (`failed`) — a real
  cross-platform portability defect (see Issues).

### 5. Building & Testing the Git Init Shell Script — 11% ❌ (ran 5/5 runnable; 0 passed, 5 failed)
- `bash -n scripts/git_init.sh` → **`No such file or directory` (exit 127)**; the
  script the whole quest revolves around is never provided, linked, or created.
- `bash scripts/git_init.sh --headless …` → same, command not found (`failed`).
- `shellcheck scripts/git_init.sh` → shellcheck v0.9.0 installed fine but
  `openBinaryFile: does not exist` — nothing to lint (`failed`).
- Bats example test → `not ok 1` because the referenced path
  `/path/to/scripts/git_init.sh` (source line 95) is a literal placeholder (`failed`).
- The 4th bash fence is **corrupted**: the `## 🎯 Quest Objectives` boilerplate
  (source lines 126–137, incl. the "auto-seeded during framework alignment" note) was
  pasted *inside* the ```bash fence that begins with `# install bats-core`, so
  copy-pasting the block runs narrative markdown as shell (`failed`). Verified in
  source.

## 🐞 Issues Found

Every item below is backed by a command actually run in the sandbox or a line quoted
from the quest source.

- **HIGH · Git Init Testing · missing prerequisite / whole quest** — The quest
  references `scripts/git_init.sh` throughout (lines 59, 103, 107, 114, 120, 145) but
  never provides it, links it, or tells the learner to clone/`cd` into a repo that
  contains it. *Observed:* every runnable command failed with exit 127 /
  file-not-found. *Fix:* embed the full `git_init.sh` source, or add an explicit
  prerequisite step (`git clone <repo> && cd`) so the file exists before any command.
- **HIGH · Git Init Testing · corrupted bash fence (source lines 125–137)** — The
  "## 🎯 Quest Objectives" placeholder block was injected inside the ```bash fence
  that starts at `# install bats-core`. *Observed:* the block executes as 7+ failing
  shell statements if copy-pasted. *Fix:* remove the injected markdown (and the
  auto-seed authoring note) from inside the fence; close the fence after
  `bats tests/bats`.
- **HIGH · Git Init Testing · placeholder path in Bats example (source line 95)** —
  `run bash /path/to/scripts/git_init.sh …`. *Observed:* Bats reports `not ok 1`.
  *Fix:* use a real relative path (e.g. `"$BATS_TEST_DIRNAME/../../scripts/git_init.sh"`)
  or explicitly tell the learner to substitute their own.
- **HIGH · Barodybroject · python-fenced non-Python content** — Directory trees,
  `requirements.txt`, and TOML are fenced as ```python. *Observed:* 6 snippets raise
  `SyntaxError`/`IndentationError`/`NameError` when run. *Fix:* fence them as ```text
  (or the correct language) so learners don't run prose as Python.
- **HIGH · Barodybroject · factual drift vs. live repo** — Claims (Django 4.2.20,
  monolithic `views.py`, "no known vulnerabilities", SQLite dev fallback) are stale.
  *Observed:* clone shows Django 5.1.4 and an existing `views/` package; `pip-audit`
  surfaced multiple real CVEs; `manage.py migrate` hard-fails on SQLite
  (`ImproperlyConfigured`). *Fix:* re-verify every version/structure/security claim
  against the live source, or clearly label the doc as a dated point-in-time snapshot.
- **MEDIUM · Barodybroject · placeholder objectives (source lines 70–78)** — Objectives
  are the auto-seeded framework boilerplate with the "authors should refine these"
  note still present. *Fix:* replace with concrete, verifiable objectives and add a
  real hands-on exercise with a success check.
- **MEDIUM · Bootstrap Framework · non-portable Windows setup block** — The
  PowerShell `mkdir $HOME\bootstrap-quest; …` block. *Observed:* run under pwsh the
  literal backslash became part of the folder name (`failed`). *Fix:* use
  `New-Item -ItemType Directory` / `Join-Path`, or note the block is `cmd`-only, not
  WSL/pwsh-compatible.
- **LOW · Advanced Markdown · unspoken GFM-Kramdown dependency** — Task lists and
  triple-backtick fences only render under the GFM-flavored Kramdown parser.
  *Observed:* bare kramdown rendered task lists as literal text; GFM fixed it. *Fix:*
  state that Jekyll ships this parser by default, and add instructions for the
  Advanced Challenge's Jekyll-build validation step (currently unsupported in the text).
- **LOW · CSS Styling Basics · silent rule override** — Chapter 3's media queries
  silently override Chapter 2's `auto-fit` grid without explanation, and "Specificity"
  is a named objective that is quizzed but never taught. *Fix:* add a sentence bridging
  the two grid approaches and a short specificity explainer.

## 🔗 Chain Continuity

Reasoning about the five quests as one learning path a Game-Developer apprentice would
walk in order:

- **The main-quest spine holds together well.** Advanced Markdown → CSS Styling Basics
  → Bootstrap Framework is a coherent Web-Fundamentals progression. Frontmatter
  confirms it: CSS `unlocks_quests` includes `bootstrap-framework`, and Bootstrap lists
  CSS as a `recommended_quests`. All three assume only "modern OS + editor/browser" and
  each delivers what the next assumes — a learner finishing CSS is genuinely ready for
  Bootstrap. No prerequisite gap between these three.
- **The side quest is an interruption, not a step.** Barodybroject (a Django/Python
  stack-analysis report) sits between two frontend HTML/CSS quests. It shares no
  prerequisite or skill thread with its neighbors (`skill_focus: backend` vs the
  surrounding `frontend`), assumes Python/venv/Django comfort the level never taught,
  and — being a stale point-in-time report whose live facts have drifted — actively
  misinforms. For a Level-0001 apprentice this is both a difficulty spike and a
  continuity break; it reads as an auto-seeded import (placeholder objectives confirm
  it) rather than an authored link in the chain.
- **The git-init quest is the hard stop.** It carries empty `knowledge_requirements`
  and a `Git Mastery Series` line, yet drops the learner into shell scripting, Bats,
  and ShellCheck with **no working script to test**. A beginner following it from a
  clean environment cannot complete a single command. It does not build on the
  markdown/CSS/Bootstrap spine and leaves the learner with nothing runnable — the
  clearest example of a step that "silently assumes setup the path never provided."
- **Ordering observation:** the two failing quests are the two that are *not* part of
  the `The Web Fundamentals Codex` / `Forging Your First Website` arc (they carry
  `Level 0001 Quest Line` / `Git Mastery Series` instead). The authored arc is healthy;
  the drift is entirely in the imported/auto-seeded quests. A maintainer could restore
  slice continuity by fixing or relocating those two out of the beginner web spine.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sealed by the workflow). I did **not** run the engine — its
  child `claude` processes can't authenticate from the agent's Bash tool. I consumed
  `./walk-evidence.json` and `./walk-evidence.md` as-is and did not modify `walk-plan.json`
  or `walk-evidence.*`.
- **What was tested (sandbox, real commands):** all per-quest snippet runs, scores, and
  the 5/2 pass/fail split in §🔬 come directly from the sealed engine — commands
  actually run in a disposable temp dir (kramdown/Liquid/PyYAML render, headless
  Chromium screenshots, live `git clone`/`pip install`/`pip-audit`/`migrate`,
  `bash -n`/`shellcheck`/`bats`).
- **What I verified statically (`reasoned`) from source myself:** the corrupted bash
  fence and `/path/to/…` placeholder in git-init (source lines 95, 125–137), the
  auto-seeded placeholder objectives in both git-init (128–136) and Barodybroject
  (70–78), the dependency frontmatter used for the continuity analysis, and the
  skill-focus/arc mismatches. These are quoted, not inferred.
- **Engine-labeled limits carried forward honestly:** several snippets are `reasoned`
  or `skipped` due to the sandbox, not defects — macOS `open`/`code` GUI launches
  (no GUI), `prefers-color-scheme` (needs DevTools emulation), and Bootstrap's
  CDN/`npm install` sass step (no outbound network). I did not count these against the
  quests and neither did the engine.
- **Coverage:** this is window **1 of 6** — 5 of the level's 26 quests. I did not walk
  the other 21; the ledger accumulates coverage across runs. Nothing here should be
  read as a verdict on the full level, only on this window.
- **Confidence:** high on the two failures (each backed by multiple real command
  failures *and* quoted source) and on the three passes (each empirically rendered).
  Overall slice verdict **warn**: the authored web-fundamentals spine passes cleanly,
  but two quests must be repaired before the window reads as a clean pass — consistent
  with the engine's 65.2% average.

<details><summary>Machine evidence (verbatim from ./walk-evidence.md)</summary>

> **5** quests evaluated · ✅ 3 pass · ⚠️ 0 warn · ❌ 2 fail · avg **65.2%** · ~$5.1377
>
> | Score | Quest | Snippets run |
> |--:|---|:-:|
> | 94 | Advanced Markdown: Tables, Footnotes & Kramdown | 10/4 |
> | 33 | Technology Stack Analysis: Barodybroject | 12/12 (7✗) |
> | 94 | CSS Styling Basics: Selectors, the Box Model & Layout | 12/4 |
> | 94 | Bootstrap Framework: Build Responsive Sites Fast | 8/4 (1✗) |
> | 11 | Building & Testing the Git Init Shell Script | 5/5 (5✗) |

</details>
