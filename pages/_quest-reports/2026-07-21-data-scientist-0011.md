---
title: Data Scientist · L0011 · 2026-07-21
description: Quest-perfection walkthrough of the AI-Assisted Development slice data-scientist/0011 on
  2026-07-21, engine verdict warn (avg 66.8%). An evidence-based…
date: '2026-07-21T13:03:14.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Data Scientist
tags:
- data-scientist
- level-0011
- walkthrough
- quest-perfection
- warn
- ai-assisted-development
render_with_liquid: false
excerpt: 'Data Scientist · Level 0011 — AI-Assisted Development: an evidence-based quest-perfection walkthrough
  from 2026-07-21.'
slice: data-scientist/0011
character: data-scientist
level: '0011'
theme: AI-Assisted Development
tier: Apprentice
verdict: warn
quest_count: 4
engine_average: 66.8
walk_date: '2026-07-21'
run_url: https://github.com/bamr87/it-journey/actions/runs/29826801543
source_report: test/quest-validator/walkthroughs/2026-07-21-data-scientist-0011.md
---

> **Slice** `data-scientist/0011` · **Level** 0011 (AI-Assisted Development) · **Apprentice tier** · **Engine verdict** ⚠️ warn (avg 66.8%) · **Walked** 2026-07-21
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29826801543) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-21-data-scientist-0011.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-21-data-scientist-0011.md)

---

## 🎯 Session Summary

I walked the **Data Scientist → Level `0011` (AI-Assisted Development, 🌱 Apprentice)**
slice — 4 main quests, the full level in one window — as a learner would, driving the
sealed execute-engine evidence and reading every quest source in plan order. The
headline is **warn**: two quests are technically sound and learner-ready with cosmetic
cleanup needed, one (`Summon the Golem`) is a strong design/config quest that verified
cleanly, and **one (`The PRD Codex`) fails outright** — every hands-on `docker compose …
prd-machine` command in it errors in a fresh sandbox because the quest never provides a
repo URL, `docker-compose.yml`, `Dockerfile`, or the tool itself.

The more important finding for a maintainer is a **structural one about the slice**: these
four quests share only the level code `0011` — they belong to four different quest series
with prerequisites that point *outside* the slice, not to each other. So this is a level
*cohort*, not a linked journey, and a Data Scientist arriving at `0011` gets an uneven
Apprentice tier: one publish-a-site "Easy", two prompt/PRD "Medium"s, and one
fleet-engineering campaign chapter that is really advanced meta-content sitting at the
same tier badge. Engine average **66.8%** (1 pass · 2 warn · 1 fail).

## 🗺️ The Journey

Plan order (from `walk-plan.json`), with per-quest engine verdict · score · takeaway:

1. ✅ **Summon the Golem: An AI Agent Joins the Loop** — **83** · Design/config quest
   (GitHub Actions YAML + agent role file); everything checkable (YAML validity, gate
   logic, live `claude` CLI flags, npm package) verified in-sandbox. Safety-exemplary.
2. ❌ **The PRD Codex: Master Product Reality Distillation** — **45** · Conceptually
   well-built, but the hands-on core is non-functional — no repo/compose file is ever
   provided, so 9 of 15 run commands fail identically.
3. ⚠️ **Hidden Gem Quest: Publish AI Chats on GitHub Pages** — **70** · Jekyll/Pages
   mechanics all worked end-to-end (`bundle install` → `jekyll build/serve`), but ships
   visible unedited template artifacts (bracketed authoring placeholder, duplicate
   objectives block).
4. ⚠️ **Forging the Prompt Crystal: VS Code Copilot Mastery** — **69** · File-creation
   commands + both Mermaid diagrams work; 5 prose snippets mislabeled as `javascript`
   error if run, and the Chapter 4 prompt-file frontmatter schema diverges from VS
   Code's real format.

## 🔬 Evidence

All results below are from the sealed `walk-evidence.json` (mode: **execute**, real
commands run in the disposable runner sandbox). I did not re-run the engine; I read each
quest source to reason about the chain (§🔗). Snippet coverage is quoted from the
evidence's `snippets` block.

### 1. Summon the Golem — ✅ pass (83) · ran 3/5 recorded, 0 runnable snippets, 2 reasoned
- `.github/actions/claude-run/action.yml` composite action — **passed**: parses via
  `yaml.safe_load`; embedded bash extracted and run — with `CLAUDE_CODE_OAUTH_TOKEN`
  unset it printed `::warning::no Claude auth — AI step is a clean no-op.` and exited 0,
  with it set it proceeded past the guard.
- Gate-update snippet (`ENABLED`/`OAUTH` → `go`) — **passed**: run in sandbox,
  `ENABLED=true`+`OAUTH=""` → `go=false`; both set → `go=true`, matching the quest's
  "switch AND secret" claim.
- CLI/flag reality check — **passed**: `-p`, `--append-system-prompt`, `--allowedTools`,
  `--permission-mode acceptEdits`, `setup-token` all confirmed present in the installed
  `claude --help`; `npm view @anthropic-ai/claude-code version` resolved (2.1.216).
- `potion-scribe.md` role file & Mermaid diagram — **reasoned** (not executable; no
  `mmdc` mismatch — the role file is prose, diagram judged statically).

### 2. The PRD Codex — ❌ fail (45) · ran 15/12 runnable (9 failed), 1 skipped, 4 reasoned
- `docker --version` / `docker info` / `docker compose version` — **passed** (Docker
  28.0.4, Compose v2.38.2 present).
- `cd ~/github/it-journey && docker compose build/run prd-machine …` across the macOS,
  Windows, Linux, Cloud paths + Quick-Win Checkpoint — **failed** identically:
  `no configuration file provided: not found` (no compose file) and `cd … No such file
  or directory` (no repo cloned/linked anywhere in 762 lines — confirmed via grep in the
  engine run).
- Commit-message examples fenced ` ```bash ` — **failed**: running verbatim throws
  `bash: syntax error near unexpected token` (they're commit text, not shell).
- 3 Mermaid diagrams + 2 YAML examples — **passed** (render/parse cleanly).
- Two "Expected Output" blocks fenced ` ```sql ` — **reasoned**: plain log lines, not
  SQL; numeric claims (60 commits, 81 md files) unverifiable without the tool.

### 3. Hidden Gem (GitHub Pages) — ⚠️ warn (70) · ran 5/3 runnable (0 failed), 3 skipped
- `Gemfile` → `bundle install` — **passed**: 97 gems installed incl. `github-pages 232`,
  `minima 2.5.1`, zero errors.
- Both `_config.yml` variants — **passed**: valid YAML, used in a real `jekyll build`.
- `_posts/…-ai-quest-chat.md` + `bundle exec jekyll serve --port 4001` — **passed**:
  generated `_site/2025/11/14/ai-quest-chat.html` with correct title/content/SEO.
- macOS `brew` / Windows `winget` / Linux `sudo apt` setup blocks — **skipped**
  (platform-specific / `sudo` disallowed by policy; git 2.54.0 already present).

### 4. Prompt Crystal (VS Code Copilot) — ⚠️ warn (69) · ran 14/9 runnable (5 failed), 4 skipped, 14 reasoned
- `mkdir -p .github/prompts && touch .github/copilot-instructions.md` (+ PowerShell
  `New-Item` + Cloud `echo >`) — **passed**: files/dirs created as described.
- `.github/copilot-instructions.md` content + two `*.prompt.md` templates — **passed**:
  written to disk, frontmatter parses as valid YAML.
- Both Mermaid diagrams — **passed** via `mmdc`.
- 5 snippets fenced ` ```javascript ` that are plain English prompt text (lines 194,
  205, 581, 948, 952) — **failed**: `node` throws `SyntaxError` each time.
- `code --install-extension …` / `--list-extensions` — **skipped**: no `code` CLI in the
  headless sandbox (expected on a real workstation).

## 🐞 Issues Found

Grouped by quest; every item is evidenced by a command result (§🔬) or a quoted source
line I read. Severity is from the learner-blocking angle.

**The PRD Codex (`prd-codex-mastery.md`)**
- **high** · hands-on core · macOS/Windows/Linux/Cloud paths + Quick-Win Checkpoint ·
  *Observed:* every `docker compose build/run prd-machine` fails with `no configuration
  file provided: not found`, and `cd ~/github/it-journey` fails with `No such file or
  directory`; no `git clone`/repo URL exists anywhere in the quest. · *Fix:* add an
  explicit `git clone <url>` step (or clearly state the quest only runs inside the
  existing IT-Journey monorepo and drop the generic-repo framing).
- **high** · PRD Machine setup · *Observed:* the quest tells learners to `cd
  /path/to/your/repository` implying any repo works, but never shows the
  `docker-compose.yml` service, `Dockerfile`, or `prd-machine` script. · *Fix:* show the
  minimal standalone tool definition, or explicitly scope to the monorepo.
- **medium** · code-fence labeling · L384-399 fenced ` ```bash ` is commit-message text
  (errors in a shell); L248-262 & L300-310 fenced ` ```sql ` are plain log lines. ·
  *Fix:* retag as ` ```text ` / ` ```git-commit ` / ` ```log `.
- **medium** · Challenge 2 (Health Monitoring) · "wait 10 minutes and check status"
  shows no change since HEALTHY spans <6h. · *Fix:* backdate the PRD mtime or reframe as
  explaining the math.
- **low** · Challenge 4 references `.github/workflows/prd-sync.yml` whose contents are
  never shown/linked. · *Fix:* inline or link it.

**Hidden Gem (`github-pages-hidden-gem.md`)**
- **high** · L13 opening paragraph · *Observed (source read):* a literal bracketed
  authoring placeholder — `*[Opening paragraph that sets the fantasy context using RPG
  metaphors…]*` — ships to the reader immediately before the real paragraph. · *Fix:*
  delete the scaffolding.
- **high** · top "Quest Objectives" (lines 3-11) · placeholder checklist + editorial
  note `*objectives auto-seeded during framework alignment — authors should refine
  these*`, duplicated by the real objectives at lines 17-38. · *Fix:* remove the
  placeholder block.
- **medium** · Challenge 2 theme switch · not caveated that GitHub Pages' built-in build
  only supports a fixed theme list (or needs `jekyll-remote-theme`) — an arbitrary theme
  builds locally but can fail on deploy. · *Fix:* add the supported-themes/remote-theme
  note.
- **medium** · Ch.3 Step 3 · "download from rubyinstaller.org" is presented universally
  but is Windows-only. · *Fix:* mention rbenv/rvm/apt/Homebrew for macOS/Linux.
- **low** · the "AI Conversation Capture Format" template omits `layout: post` (unlike
  the working Step-4 example) — builds but renders unstyled. · *Fix:* add `layout: post`.

**Prompt Crystal (`prompt-crystal-mastery-vscode-copilot.md`)**
- **high** · Chapter 4 prompt-file schema · *Observed:* templates use
  `name`/`description`/`version`/`inputs: […]` frontmatter with `{​{ inputs.x }​}`
  substitution; documented VS Code "prompt files" use `mode`/`description`/`tools`/`model`
  and `${input:variableName}` — so a learner's files likely won't have variables
  substituted. · *Fix:* verify against current docs and correct the schema.
- **medium** · code-fence labeling · 5 ` ```javascript ` blocks (L194, 205, 581, 948,
  952) are plain English prompt text and throw `SyntaxError` under `node`. · *Fix:*
  retag as ` ```text `/` ```markdown `.
- **low** · `{​% raw %​}…{​% endraw %​}` Liquid wrapper leaks into raw-source view as clutter
  around every `{​{ inputs.x }​}`. · *Fix:* cleaner escaping or a note.

**Summon the Golem (`ouroboros-loop-03-summon-the-golem.md`)** — no blocking issues.
- **low** · level-numbering · metadata says "Level 0011" but sibling links use
  `/quests/0101/` and `/quests/1011/`; unexplained. · *Fix:* reconcile / explain the
  binary level-per-quest scheme (see §🔗).
- **low** · Chapter 1 `action.yml` inputs omit `description:` fields (GitHub recommends
  them). · **low** · git-exclusion is enforced only at the prompt/role level — worth
  noting Bash-tool access is otherwise unrestricted.

## 🔗 Chain Continuity

Reading the four sources in plan order, **this slice is a level cohort, not a linked
chain** — and that is the single most useful continuity finding:

- **The quests don't reference each other; their prerequisites point outside the slice.**
  - `Summon the Golem` → `quest_dependencies.required_quests: []` but its *real*
    prerequisites (frontmatter + prose) are "Chapters I–II of this campaign" at
    `/quests/0101/…the-wardens-gate/` and it unlocks `/quests/1011/…the-sealed-evidence/`
    — a different campaign (The Ouroboros Loop) that isn't in this slice.
  - `The PRD Codex` → `required_quests: []`, but its `unlocks_quests` *does* list
    `prompt-crystal` and `github-pages` — the only intra-slice edge, and it points the
    "right" direction (PRD before the other two).
  - `Hidden Gem` → requires `/quests/0000/hello-noob/`.
  - `Prompt Crystal` → requires `/quests/0010/prompt-engineering-mastery/`.
  So a learner walking them *in the planned order* carries **no state** from quest N into
  N+1; each is standalone with its own external prereqs. Nothing breaks from ordering, but
  nothing reinforces either — the "journey" is four parallel doors, not a staircase.

- **Tier uniformity is misleading.** All four wear the `0011` Apprentice badge, but
  `Summon the Golem` is genuinely advanced fleet-engineering meta-content (composite
  actions, agent role files, CI gating) — it verified cleanly and is well-built, but it
  assumes the learner has already built a gated CI loop (Chapters I–II). A Data Scientist
  who reaches `0011` via the other three quests would hit a difficulty cliff here with no
  bridge quest in the slice.

- **Level-code vs. URL mismatch is a real learner snag across the campaign.** The engine
  flagged, and I confirmed by reading the source, that `Summon the Golem` says "Level
  0011" while linking siblings at `/quests/0101/` and `/quests/1011/`. This is the binary
  level-per-quest scheme (each campaign chapter sits at its own level), but it is never
  explained, so a learner trying to map level codes to quest IDs will be confused — this
  affects any learner who tries to *follow the chain* the diagram draws.

- **Thematic fit is uneven with the "AI-Assisted Development" theme.** `Prompt Crystal`
  and `Summon the Golem` fit squarely. `Hidden Gem` is manual copy/paste of chat
  transcripts into Jekyll + standard GitHub Pages publishing — the engine noted (and the
  title/objectives confirm) it doesn't actually teach an AI-assisted coding workflow. It
  fits the *level name* loosely at best.

Net: the slice holds together as a "here are the `0011` quests" set, but not as a guided
path. A maintainer could add explicit intra-level ordering/bridges, and should fix the
one hard-failing quest (`PRD Codex`) before it's presented as hands-on.

## 🧠 Reasoning & Method

- **Mode:** `execute` — the machine evidence was pre-computed and **sealed** by the
  workflow (`walk-evidence.json` / `walk-evidence.md`); I consumed it as-is and did **not**
  re-run the engine (its child `claude` processes can't authenticate from the agent's
  Bash tool). I did not edit `walk-plan.json` or the evidence.
- **What I ran vs. reasoned:** I ran no quest commands myself — every `passed`/`failed`
  in §🔬 comes from the sealed sandbox run. My own contribution is the **linked-journey
  reasoning** (§🔗), which I based on reading all four quest sources in plan order (their
  frontmatter `quest_dependencies`/`prerequisites`, series/line/arc, and prose).
- **Coverage & limits of the sealed run:** Windows/macOS setup blocks and `sudo`/`code`
  CLI steps were **skipped** in the sandbox (Linux, headless, policy) — those are
  `reasoned`, not verified live; a real workstation may differ. Live Copilot Chat, the
  actual `prd-machine` tool, and the private IT-Journey checkout were not available, so
  those behaviors are reasoned/unverifiable, not tested. The planner reports the window
  as **1 of 1** — the full 4-quest level was walked, nothing capped.
- **Confidence:** High on the per-quest verdicts (backed by real command output,
  especially the unambiguous `PRD Codex` failures and the `Hidden Gem` full build/serve
  success). High on the chain-continuity finding, since it rests on directly-read
  frontmatter dependency fields rather than inference.
- **Scope discipline:** One slice, one report. No quest content edited, no branch/commit/
  push, no merge — the workflow handles git. Fixable bugs are captured in §🐞 for a
  content pass to act on.
