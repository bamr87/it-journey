---
title: Data Scientist · L0011 · 2026-07-06
description: Quest-perfection walkthrough of the AI-Assisted Development slice data-scientist/0011 on
  2026-07-06, engine verdict fail. An evidence-based, learner's-eye…
date: '2026-07-06T13:18:22.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Data Scientist
tags:
- data-scientist
- level-0011
- walkthrough
- quest-perfection
- fail
- ai-assisted-development
render_with_liquid: false
excerpt: 'Data Scientist · Level 0011 — AI-Assisted Development: an evidence-based quest-perfection walkthrough
  from 2026-07-06.'
slice: data-scientist/0011
character: data-scientist
level: '0011'
theme: AI-Assisted Development
tier: Apprentice
verdict: fail
quest_count: 3
walk_date: '2026-07-06'
run_url: https://github.com/bamr87/it-journey/actions/runs/28791022929
source_report: test/quest-validator/walkthroughs/2026-07-06-data-scientist-0011.md
---

> **Slice** `data-scientist/0011` · **Level** 0011 (AI-Assisted Development) · **Apprentice tier** · **Engine verdict** ❌ fail · **Walked** 2026-07-06
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/28791022929) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-06-data-scientist-0011.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-06-data-scientist-0011.md)

---

## 🎯 Session Summary

I walked the **Data Scientist → Level 0011 (Apprentice · "AI-Assisted Development")**
slice as a learner would: three `main_quest` pages in planner order — the PRD Codex,
the GitHub Pages Hidden Gem, and the Prompt Crystal (VS Code Copilot). The machine
evidence was sealed by the workflow's execute-mode engine (I consumed
`walk-evidence.json` verbatim — I did not re-run the engine); I then read each quest
source and reasoned about them as one linked path.

**Headline verdict: FAIL for the slice as a walkable learning path**, even though the
average is a middling 59.7% (0 pass · 2 warn · 1 fail). The reason is ordering + a
hard blocker: the **first** quest a learner meets, *The PRD Codex* (score **39, fail**),
is **not runnable as written** — every one of its core `docker compose build/run
prd-machine …` commands failed in the clean sandbox with `no configuration file
provided: not found`, because the quest never tells the learner where the
`docker-compose.yml` / `scripts/prd-machine` it depends on comes from. A beginner
starting this level in order hits a wall on quest 1. The other two quests are usable
(warn): the GitHub Pages quest's Jekyll build-and-serve path **actually worked
end-to-end in the sandbox**, and the Prompt Crystal's shell scaffolding **all ran
clean** — both just ship fixable content defects (wrong extension IDs, leftover
authoring placeholders, and Liquid `{​% raw %​}` artifacts). All three are read-only
findings for a later content pass; I changed nothing.

## 🗺️ The Journey

Planner order (from `walk-plan.json`), with per-quest engine score and my one-line
learner takeaway:

1. ❌ **The PRD Codex: Master Product Reality Distillation** — **39 / fail** ·
   Conceptually sound and well-structured, but a learner can't run a single core
   command: no clone/setup step exists, so `docker compose … prd-machine` fails
   immediately. *This is the entry quest and it blocks.*
2. ⚠️ **Hidden Gem Quest: Publish AI Chats on GitHub Pages** — **65 / warn** ·
   The central Jekyll workflow genuinely builds and serves in the sandbox; spoiled by
   a wrong VS Code extension ID and visible template scaffolding never deleted from
   the opening.
3. ⚠️ **Forging the Prompt Crystal: VS Code Copilot Mastery Quest** — **75 / warn** ·
   Strongest of the three; all scaffolding commands run, but it overstates Copilot's
   `{​{ inputs.x }​}` templating and leaves `{​% raw %​}` website-rendering artifacts in
   copy-paste fragments.

Difficulty as declared: 🟡 Medium, 🟢 Easy, 🟡 Medium. Note the ordering hazard —
the hardest-to-run and only *failing* quest is presented **first**.

## 🔬 Evidence

All command outcomes below come from the sealed execute-engine run
(`walk-evidence.json`, `mode: execute`, `mock: false`); prose/line observations I
verified by reading the quest source are labelled **reasoned**.

### 1. PRD Codex — score 39, weight covered 1.0
Snippet coverage: **ran 13 of 12 runnable** (5 passed · 8 failed) · 2 skipped ·
4 reasoned · 19 recorded.
Dimensions: commands_work **1**, content_accuracy 2, completeness 1, clarity 2,
structure 4, safety 5.

- **failed** — *macOS / Linux / Cloud platform paths* and the `sync`, `status`,
  `conflicts`, and "Quick Win" command blocks: engine detail —
  > "`docker compose build prd-machine` fails with 'no configuration file provided:
  > not found' since no docker-compose.yml or scripts/prd-machine exist in this
  > sandbox (or is created by the quest)."
  `docker --version` / `docker compose version` **succeed** (Docker 28.0.4, Compose
  v2.38.2), so Docker itself is fine — the quest simply never provisions the project.
- **reasoned** — *sync Expected Output*: engine flagged an internal arithmetic error —
  > "60 commits + 81 markdown files + 1 feature = 142, but the block claims 'Total
  > signals processed: 146'."
- **passed** — the Mermaid diagrams (Signal Source Architecture, Quest Network
  Position, Implementation Flow) and the illustrative YAML blocks (frontmatter,
  `features.yml`) parse cleanly.
- **failed** — the "Best Practices for Commit Signals" block is fenced ` ```bash `
  but contains commit-message prose, not runnable shell.

### 2. GitHub Pages Hidden Gem — score 65, weight covered 1.0
Snippet coverage: **ran 7 of 3 runnable** (5 passed · 2 failed) · 3 skipped ·
2 reasoned · 12 recorded.
Dimensions: commands_work 3, content_accuracy 3, completeness 3, clarity 3,
structure 4, safety 5.

- **passed** — the **core hands-on path ran end-to-end in the sandbox**: `_config.yml`,
  `Gemfile` (`gem "github-pages"`), the `_posts/2025-11-14-ai-quest-chat.md` post,
  `bundle install`, and `bundle exec jekyll serve` all succeeded. This is the quest's
  spine and it is sound.
- **failed** — `code --install-extension ms-vscode.vscode-github-pull-requests-and-issues`
  (both macOS and Linux blocks): the extension ID is wrong. **reasoned** confirmation
  from source lines 139 & 154; correct ID is `GitHub.vscode-pull-request-github`.
- **reasoned** — leftover authoring placeholders in the published body: source line
  103 `> *Note: objectives auto-seeded during framework alignment — authors should
  refine these…*` and line 105 `*[Opening paragraph that sets the fantasy context…]*`.
  I verified both are present in the file.

### 3. Prompt Crystal (VS Code Copilot) — score 75, weight covered 1.0
Snippet coverage: **ran 9 of 9 runnable** (9 passed · 0 failed) · 3 skipped ·
23 reasoned · 35 recorded.
Dimensions: commands_work 4, content_accuracy 3, completeness 4, clarity 3,
structure 5, safety 5.

- **passed** — every runnable scaffolding command worked across all four platform
  paths: `mkdir -p .github/prompts && touch .github/copilot-instructions.md`
  (macOS/Linux), the PowerShell `New-Item …` equivalents, and the Cloud
  `echo … > .github/copilot-instructions.md`. Zero command failures.
- **skipped** — the `code --install-extension GitHub.copilot …` lines (Copilot CLI
  install can't run in the sandbox) — a coverage gap, not a defect.
- **reasoned** — the 23 prompt/template text blocks are illustrative, not executable.
  Two content problems verified in source: the `.prompt.md` templates literally carry
  `{​% raw %​}{​{ inputs.x }​}{​% endraw %​}` Liquid escaping (lines 794–829, 861–919), and
  the frontmatter `inputs:` + `{​{ inputs.x }​}` convention (lines 789–791, 856–858,
  898–900) implies native Copilot variable substitution that does not exist.

## 🐞 Issues Found

Grouped by severity. Each cites what was observed (engine command result, or a quoted
source line I read). These are for a later content pass — **no edits were made here.**

- **HIGH · PRD Codex · Platform paths / Prerequisites (lines 168–253)** — *Observed:*
  every `docker compose build/run prd-machine …` command **failed** in the sandbox
  with `no configuration file provided: not found`; the quest jumps straight to
  `docker compose build prd-machine` with only placeholder `cd ~/github/it-journey`
  paths. A learner outside an existing IT-Journey checkout cannot execute a single
  core command. *Suggested fix:* add an explicit setup step (`git clone …` of the repo
  that actually contains `docker-compose.yml` + `scripts/prd-machine/`) before any
  Docker command.
- **HIGH · PRD Codex · sync Expected Output (lines 347–362)** — *Observed (reasoned):*
  sample output claims `Total signals processed: 146`, but 60 + 81 + 1 = **142**.
  *Fix:* correct the total or explain the extra 4.
- **HIGH · GitHub Pages · Chapter 2 install blocks (lines 139, 154)** — *Observed:*
  `code --install-extension ms-vscode.vscode-github-pull-requests-and-issues`
  **failed**; ID is wrong. *Fix:* use `GitHub.vscode-pull-request-github` in both the
  macOS and Linux blocks.
- **HIGH · GitHub Pages · Opening / Objectives (lines 103, 105)** — *Observed
  (reasoned):* un-deleted authoring scaffolding is published to the learner:
  `> *Note: objectives auto-seeded during framework alignment…*` and
  `*[Opening paragraph that sets the fantasy context…]*`. *Fix:* delete both.
- **HIGH · Prompt Crystal · Chapter 4 `{​{ inputs.x }​}` templating (lines 785–829,
  852–920)** — *Observed (reasoned):* the quest presents `inputs:` frontmatter +
  `{​{ inputs.x }​}` as if VS Code Copilot renders variables; it does not. *Fix:* state
  it's a manual find-and-replace placeholder convention, or drop the templating claim.
- **HIGH · Prompt Crystal · `.prompt.md` code fences (lines 794–829, 861–919)** —
  *Observed (reasoned):* fragments literally contain `{​% raw %​}…{​% endraw %​}` Liquid
  escaping that would break if copy-pasted into a real prompt file. *Fix:* strip the
  tags, or add a visible note they are website-render artifacts.
- **MEDIUM · PRD Codex · conflicts Expected Output (lines 400–410)** — *Observed
  (reasoned):* claims "4 conflicts" but shows only 2, both `fix` type; the Conflict
  Types table's `revert`/`contradiction` rows are never illustrated. *Fix:* show all 4
  or add a truncation marker plus one non-`fix` example.
- **MEDIUM · PRD Codex · code fence languages (Best Practices block ~484; Expected
  Output ~348, ~400)** — *Observed:* commit-message prose fenced as ` ```bash `
  (fails if pasted); log lines fenced as ` ```sql `. *Fix:* re-tag to ` ```text ` /
  ` ```log ` / ` ```git-commit `.
- **MEDIUM · GitHub Pages · `_config.yml` theme comment (line 240)** — *Observed
  (reasoned):* `theme: minima  # … explore others at themes.jekyllrc.org` — that host
  is not a known Jekyll theme site; the quest itself correctly links `jekyllthemes.io`
  later. *Fix:* correct the URL.
- **MEDIUM · GitHub Pages · Step 5 local preview (line 270)** — *Observed (reasoned):*
  recommends the Live Server extension to preview a Jekyll site, but Live Server can't
  render Liquid. *Fix:* recommend `bundle exec jekyll serve --livereload`, or scope
  Live Server to static `_site` output only.
- **MEDIUM · Prompt Crystal · Platform install blocks (lines 193–269)** — *Observed
  (reasoned):* `code --install-extension …` assumes the `code` CLI is on PATH and an
  active Copilot subscription. *Fix:* add a one-line prerequisite note (enable "Shell
  Command: Install 'code'…"; Copilot requires a subscription/trial).
- **LOW · PRD Codex** — Challenge 4 references `.github/workflows/prd-sync.yml` but
  doesn't include/link it (lines 593–604); consider adding it.
- **LOW · GitHub Pages** — Chapter 2 lists 5 "essential" extensions but only installs
  2 via command (lines 197–201); either provide all install commands or trim the list.
  Also add the "Install 'code' in PATH" note before the CLI commands.
- **LOW · Prompt Crystal** — several ` ```javascript ` fences (≈lines 296, 307, 683,
  1050, 1055) actually hold prose/ASCII/diagrams; re-tag as ` ```text `/` ```markdown `.
  Add an explicit Prerequisites section (min VS Code version, experimental prompt-files
  setting).

**No fabricated issues:** every item above is either a command result from the sealed
engine run or a line I read in the quest source.

## 🔗 Chain Continuity

- **These three quests are loosely-coupled siblings, not a dependency chain.** Read as
  one journey, no quest builds on artifacts or state produced by an earlier one in the
  slice. The PRD Codex frontmatter *unlocks* the other two (`unlocks_quests` lists
  `/quests/0011/prompt-crystal-vscode-copilot/` and `…/github-pages-hidden-gem/`), but
  neither actually consumes anything the PRD quest teaches. A learner can do them in
  any order — which is fortunate, because quest 1 is the broken one.
- **The declared hard prerequisites point *outside* the slice, to earlier levels, and
  are consistent.** GitHub Pages requires `/quests/0000/hello-noob/`; Prompt Crystal
  requires `/quests/0010/prompt-engineering-mastery/`. Both are earlier-level quests,
  so they're reasonable assumed-knowledge gates, not gaps within this window. PRD Codex
  declares no required quests.
- **Ordering hazard.** The planner presents the quests hardest-first: the only failing,
  non-runnable quest (PRD Codex) leads, and the easy, fully-working GitHub Pages quest
  is second. A real beginner walking in order would hit the `no configuration file
  provided` wall on their very first command and likely abandon the level before
  reaching the two quests that actually work. Fixing PRD Codex's setup step, or
  surfacing an Easy quest first, would materially improve the learner path.
- **Character fit is generic, by design.** This is the shared Level 0011 content
  ("AI-Assisted Development"); nothing here is data-science-specific (it's PRD
  automation, GitHub Pages publishing, and Copilot prompt engineering). The theme is
  relevant to a data scientist's AI-tooling literacy, but a learner expecting
  data-centric material would find general dev tooling. This is an observation about
  the level design, not a defect in these quests.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sandboxed). I did **not** run the engine — per the skill and my
  constraints, the workflow pre-computed and sealed `walk-evidence.json` /
  `walk-evidence.md`, and I consumed them verbatim. I did not edit, regenerate, or
  hand-write any evidence, plan, or quest file.
- **What I ran vs. reasoned:** all `passed`/`failed`/`skipped` verdicts are the
  engine's real sandbox command results (Docker 28.0.4 present; PRD's compose commands
  failed; the Jekyll build/serve and all Copilot scaffolding commands ran). Everything
  I label **reasoned** — arithmetic errors, placeholder scaffolding, wrong URLs,
  `{​% raw %​}` artifacts, `{​{ inputs.x }​}` overstatement, fence-language mismatches — I
  confirmed by reading the quest source and citing exact lines; I did not execute those
  parts.
- **Coverage / limits:** Snippet coverage was strong for PRD Codex (13 runnable ran)
  and Prompt Crystal (9/9 runnable ran), thinner for GitHub Pages (3 runnable, though
  the full build-and-serve chain executed). The 23 "reasoned" blocks in Prompt Crystal
  are prompt-text illustrations that are not meant to execute — not a testing gap.
  Extension-install and OS-specific (Windows/macOS `brew`, Codespaces) commands were
  correctly **skipped** as unrunnable in a Linux sandbox; their syntax was inspected,
  not executed. No network access beyond what the Jekyll build needed.
- **Slice verdict rationale:** I set `overall_verdict: fail` despite a 59.7% average
  because the honest learner outcome is that the *entry* quest cannot be completed as
  written — a blocking, not cosmetic, failure. The two `warn` quests are genuinely
  usable once their listed defects are fixed.
- **Confidence:** High on command outcomes (real sandbox execution) and on the source
  citations (verified line-by-line). Lower only on the exact user-facing impact of the
  Copilot `{​{ inputs.x }​}` behavior, which depends on VS Code version — flagged as
  reasoned. One slice, one report; no content was changed and nothing was merged.

---

_Machine evidence summary (verbatim from `walk-evidence.md`): 3 quests · ✅ 0 pass ·
⚠️ 2 warn · ❌ 1 fail · avg 59.7% · ~$2.4322._
