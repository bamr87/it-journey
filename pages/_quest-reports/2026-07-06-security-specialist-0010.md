---
title: Security Specialist · L0010 · 2026-07-06
description: Quest-perfection walkthrough of the Terminal Mastery slice security-specialist/0010 on 2026-07-06,
  engine verdict warn. An evidence-based, learner's-eye…
date: '2026-07-06T13:01:45.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Security Specialist
tags:
- security-specialist
- level-0010
- walkthrough
- quest-perfection
- warn
- terminal-mastery
render_with_liquid: false
excerpt: 'Security Specialist · Level 0010 — Terminal Mastery: an evidence-based quest-perfection walkthrough
  from 2026-07-06.'
slice: security-specialist/0010
character: security-specialist
level: '0010'
theme: Terminal Mastery
tier: Apprentice
verdict: warn
quest_count: 1
walk_date: '2026-07-06'
run_url: https://github.com/bamr87/it-journey/actions/runs/28791022929
source_report: test/quest-validator/walkthroughs/2026-07-06-security-specialist-0010.md
---

> **Slice** `security-specialist/0010` · **Level** 0010 (Terminal Mastery) · **Apprentice tier** · **Engine verdict** ⚠️ warn · **Walked** 2026-07-06
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/28791022929) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-06-security-specialist-0010.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-06-security-specialist-0010.md)

---

# 📆 Quest Walkthrough — Security Specialist · Level 0010

## 🎯 Session Summary

I walked **1 quest** — the only quest in this window (window **3 of 4**, offset 15)
of the 16-quest **Level 0010 "Terminal Mastery"** slice for the **Security
Specialist** path. The single quest, *Contribution Calendar: Mapping Your Journey
Through Time*, earned a **warn** verdict at **62%**. The underlying design is sound —
the execute engine verified the Liquid intensity-bucket logic and the CSS with real
tooling — but **the quest's own fenced code blocks are broken as literally written**:
every individual Liquid tag in Step 1 and Step 3 is wrapped in its own
`{% raw %}...{% endraw %}` pair, so a learner who copy-pastes the raw `.md` source
gets inert, un-executed tag text instead of a working include. A maintainer should
treat the raw-tag escaping (high) and a non-matching CSS sibling combinator (medium)
as the two concrete, verified defects to fix.

**Headline verdict: ⚠️ WARN** — the feature *can* work, but the copy-paste path the
quest hands the learner does not.

## 🗺️ The Journey

Only one quest fell inside this planned window, so this is a single-station walk, not
a multi-quest chain. `stats.total_quests = 16` for the full level; the ledger sweeps
the rest across other windows.

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ⚠️ | Contribution Calendar: Mapping Your Journey Through Time (`side_quest`, 🟡 Medium) | 62% | Logic + CSS are sound, but the verbatim Step 1/Step 3 snippets render as escaped text, not working Liquid. |

## 🔬 Evidence

All evidence below is from the sealed execute-mode run
(`walk-evidence.json` / `walk-evidence.md`, session `ddea0dae…`, 23 turns, 291 s).
Snippet coverage for the quest: **ran 4/5 recorded snippets — 2 passed, 2 failed, 1
skipped** (`available_runnable: 1`).

**Quest 1 — `pages/_quests/0010/side-quest-contribution-calendar.md`**

- ✅ **`passed` — Background YAML (`contribution_calendar` example data):** parsed
  cleanly with PyYAML; valid list-of-weeks shape.
- ❌ **`failed` — Step 1 include (`_includes/contributor/contribution_calendar.html`):**
  the block was copy-pasted verbatim and rendered with the `liquid` gem (v5.13.0).
  Output was the **literal, un-executed tag text** (e.g. `{% assign calendar =
  include.calendar %}`), producing "zero interactivity, no cells, nothing but escaped
  tag text." When the engine *stripped* the per-tag `{% raw %}/{% endraw %}` wrappers,
  the same logic rendered correctly — sample commits `3/0/7/20/1` produced
  `calendar-medium/zero/high/max/low`, confirming the bucket thresholds
  (`0 / <3 / <7 / <15 / else`) are correct.
- ✅ **`passed` — Step 2 CSS (`assets/css/contributor-profile.css`):** copied into a
  real `.css` file; braces balanced (17/17), standard Grid / `aspect-ratio` / custom
  properties / media query all parse. *However*, jsdom testing of the wizard-theme
  rule surfaced a content-accuracy defect (see Issues).
- ❌ **`failed` — Step 3 integration (`{% include contributor/contribution_calendar.html … %}`):**
  same raw/endraw corruption as Step 1 — rendering the line exactly as it appears in
  the source printed the include tag as text instead of executing it. The
  include-parameter syntax itself (`calendar=contributor.stats.contribution_calendar`
  → `include.calendar`) is otherwise correct Jekyll idiom once uncorrupted.
- ⏭️ **`skipped` — Step 4 (`bundle exec jekyll serve`):** no Gemfile/bundler in the
  isolated sandbox (`bundle: command not found`). This is an **inherent limitation of
  testing a side-quest in isolation**, not a quest defect — the quest assumes a
  pre-existing Jekyll project from the prerequisite quest.

Per-dimension scores (engine): `commands_work 2 · content_accuracy 3 · completeness 4
· clarity 3 · structure 4 · safety 5` → overall **62%**, weight covered 1.0.

## 🐞 Issues Found

- **HIGH · Contribution Calendar · Step 1 & Step 3 code fences · `raw`-tag corruption.**
  *Observed:* every Liquid tag is individually wrapped in `{% raw %}…{% endraw %}`
  (source lines 108–140 for Step 1, line 208 for Step 3). Rendering the verbatim
  blocks with the `liquid` gem produced escaped tag text, not a heatmap — a learner
  copying the raw `.md` (from GitHub, an editor, or this artifact) gets a completely
  non-functional feature. *Suggested fix:* stop wrapping each tag; wrap the whole
  block once (single `{% raw %}` … `{% endraw %}`), or verify the docs pipeline even
  needs escaping inside fenced code blocks — many Jekyll configs don't process Liquid
  inside fences at all.
- **MEDIUM · Contribution Calendar · Step 2 CSS · wizard-theme sibling combinator is dead code.**
  *Observed:* the rule `.contributor-card--wizard ~ .contributor-calendar .calendar-*`
  (source lines 174–177) uses the general-sibling combinator `~`. jsdom confirmed it
  did **not** match when the calendar is nested *inside* the card container — which is
  exactly the structure Step 3 instructs ("add after the stats panel or achievement
  wall" inside `character_sheet.html`). It only matched when the calendar was a true
  following sibling. *Suggested fix:* use a descendant selector
  (`.contributor-card--wizard .contributor-calendar .calendar-*`, drop the `~`).
- **MEDIUM · Contribution Calendar · Accessibility (Steps 1 & 4 checklist).**
  *Observed:* the grid is built from bare `<div class="calendar-cell">` elements whose
  only label is a hover `title` attribute — inaccessible to keyboard/screen-reader
  users, and the quest's "verify" checklist never mentions accessibility. *Suggested
  fix:* add `role="img"` + an `aria-label` (or visually-hidden summary) to the grid.
- **LOW · Contribution Calendar · Step 4 prerequisite is only implied.**
  *Observed:* `bundle exec jekyll serve` (line 215) assumes a working Jekyll
  project/Gemfile, but that hard dependency appears only as a wiki-link at the very
  bottom of the page (line 244) — easy to miss before starting. *Suggested fix:* state
  near Step 4 that the *Forge Your Character* project/Gemfile must already be set up.

No high-severity safety issues — `safety` scored **5/5**; the quest contains only file
creation/editing and a local dev server, nothing destructive.

## 🔗 Chain Continuity

This window contained **only one quest**, so there is no in-slice quest-to-quest
handoff to evaluate on this run. Two continuity observations still stand:

1. **Cross-path assignment.** This is a *Contributor Path* side-quest
   (`quest_series: 'Contributor Path: Identity & Recognition'`, `skill_focus:
   frontend`) surfaced under the **Security Specialist** character at level 0010. The
   quest itself is character-agnostic front-end work; a security-specialist learner
   should reach it comfortably as a shared Terminal-Mastery station, but nothing in
   the body ties it to a security narrative. Worth a maintainer noting whether that's
   the intended mapping for this path's 0010 tier.
2. **Unmet upstream prerequisite = a real friction point.** The quest declares
   `required_quests: /quests/0001/forge-your-character/` and needs its scaffolded
   Jekyll project/Gemfile for Step 4. The sandbox had no Gemfile, so Step 4 could only
   be `skipped` — mirroring exactly where a learner who arrives *without* having
   completed *Forge Your Character* would stall (`bundle: command not found`). The
   dependency is correctly declared in frontmatter; the body just under-signposts it
   (see the LOW issue). For a learner walking the level in order, this handoff holds
   **iff** they did the 0001 prerequisite first.

The rest of the 16-quest level (windows 1, 2, 4) was **not** walked in this session
and is out of scope for this report — the ledger accumulates that coverage separately.

## 🧠 Reasoning & Method

- **Mode:** `execute` (real commands in a disposable sandbox). Evidence was
  **pre-computed and sealed by the workflow** (`walk-evidence.json` / `walk-evidence.md`)
  because the engine's child `claude` processes cannot authenticate from an agent's
  Bash tool. I consumed it **as-is** — I did not re-run the engine, and I did not edit
  `walk-plan.json` or the evidence files.
- **What was actually run (from the sealed engine):** PyYAML parse of the Background
  data; verbatim + stripped Liquid renders of Step 1 and Step 3 via the `liquid` gem
  v5.13.0; a real `.css` brace/syntax check plus a jsdom test of the wizard sibling
  selector for Step 2; an attempted `bundle exec jekyll serve` for Step 4 (skipped, no
  bundler). Coverage: **4/5 snippets ran**, 1 skipped for an inherent isolation limit.
- **What I reasoned about statically:** the chain-continuity findings above (single-quest
  window, cross-path assignment, prerequisite signposting) — these are `reasoned` from
  reading the quest source and frontmatter in plan order, not separately executed.
- **Limits of this pass:** (a) single-quest window, so no multi-quest continuity was
  exercised; (b) Step 4's `jekyll serve` was un-testable in isolation, so the rendered
  end-to-end page was never seen — the "does the heatmap actually appear on the profile"
  completion criterion is verified only indirectly (logic + CSS render correctly in
  isolation), not on a live built site; (c) all numeric scores come from the sealed
  engine, not from me.
- **Confidence:** **High** on the two `failed` code-fence defects and the CSS
  combinator finding (each backed by a real render/DOM test). **Medium** on the
  end-to-end profile integration, which could not be booted in the sandbox.

_Machine summary (verbatim from `walk-evidence.md`):_ "The underlying Liquid logic and
CSS design are sound … but the quest's own fenced code blocks are broken as literally
written: every Liquid tag is individually wrapped in {% raw %}/{% endraw %}, so
copy-pasting Step 1 or Step 3 verbatim produces inert, unexecuted tag text rather than
a working include. A secondary, verified bug is that the wizard-theme CSS uses a
sibling combinator that doesn't match the nested DOM structure the quest itself
instructs learners to build."
