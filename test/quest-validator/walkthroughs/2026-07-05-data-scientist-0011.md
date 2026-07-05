---
title: "Walkthrough — Data Scientist · Level 0011 (AI-Assisted Development)"
date: '2026-07-05T00:00:00.000Z'
character: data-scientist
level: '0011'
theme: AI-Assisted Development
tier: Apprentice
quest_count: 3
mode: execute
overall_verdict: warn
session:
  planned: 3
  scored: 2
  errored: 1
  average_score: 71.0
  engine_cost_usd: 1.698
  notes: >-
    Evidence sealed by the workflow's deterministic execute-engine step
    (agentic_validate.py --mode execute). Consumed as-is; not re-run. Quest 1
    (prd-codex-mastery) produced no per-quest verdict — the engine hit max_turns
    (40) after the sandbox denied its network calls, so it is unscored, not a
    demonstrated content failure. The two quests that scored are both warn.
---

## 🎯 Session Summary

I walked the **Data Scientist** path at **Level 0011 — AI-Assisted Development**
(🌱 Apprentice tier), a 3-quest slice chosen by `walk-plan.json`, in plan order:
`prd-codex-mastery` → `github-pages-hidden-gem` → `prompt-crystal-mastery-vscode-copilot`.
All three are `main_quest`s. Evidence was pre-computed and sealed by the workflow's
execute-engine step; I consumed `walk-evidence.json` / `walk-evidence.md` as-is and
read every quest source to reason about the linked journey.

**Headline verdict: ⚠️ warn.** Two quests scored `warn` (75 and 67) and one
(`prd-codex-mastery`) could not be scored at all because the execute engine ran out
of turns after the sandbox blocked its network probes — so that quest is **unscored
for lack of evidence, not judged failing on content**. Both scored quests have their
core technical workflow *actually executed and working* in the sandbox (Jekyll
build/serve; directory scaffolding; mermaid rendering), but each carries concrete,
copy-paste-breaking defects a real learner would hit: a wrong VS Code extension id, a
dead theme URL, and — most seriously — a whole Chapter 4 of prompt-file templates in
`prompt-crystal` that use invented syntax and leak literal Jekyll `{% raw %}` tags.
The slice is also only *loosely* a "data scientist" journey: these are general
AI-assisted-dev / documentation quests, dependency-independent of each other.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:---:|---|--:|---|
| 1 | ❌ unscored | The PRD Codex: Master Product Reality Distillation | — | Engine hit max_turns after network denial; needs Docker + the *it-journey* repo's own `prd-machine` tool, so it isn't runnable by a learner in their own repo. |
| 2 | ⚠️ warn | Hidden Gem Quest: Publish AI Chats on GitHub Pages | 75 | Full Jekyll build/serve workflow executed flawlessly; loses points on a wrong extension id, a dead theme URL, and un-refined placeholder objectives. |
| 3 | ⚠️ warn | Forging the Prompt Crystal: VS Code Copilot Mastery | 67 | Sound prompting theory and working scaffolding, but Chapter 4 templates use invented `inputs:`/`{{ inputs.x }}` syntax and leak literal `{% raw %}` tags. |

Average of the two scored quests: **71.0%**. Engine cost: ~$1.698.

## 🔬 Evidence

All statuses below come from commands the sealed execute engine actually ran in the
disposable sandbox, except items explicitly marked `reasoned` (judged statically from
the quest source, by the engine or by me on this read).

### Quest 1 — `prd-codex-mastery.md` — ❌ unscored (no verdict)

- **Snippet coverage: 0 recorded / none run.** The engine returned an error, not a
  verdict: `claude exited 1 … terminal_reason: max_turns … errors: ["Reached maximum
  number of turns (40)"]`.
- The one recorded machine event is a **sandbox permission denial**: the engine tried
  `curl … https://github.com` and `https://api.github.com/search/repositories?q=it-journey+prd-machine`
  and was blocked by sandbox network policy (`permission_denials` in the evidence).
- **Reasoned (from source):** every runnable command in this quest is
  `docker compose build prd-machine` / `docker compose run --rm prd-machine
  ./scripts/prd-machine/prd-machine {sync,status,conflicts}` executed from
  `cd ~/github/it-journey` (lines 170–251, 336–431). These depend on Docker **and** on
  a `prd-machine` tool that lives only inside the it-journey repo — none of it is
  exercisable in the headless sandbox, which is why the engine burned its turns and
  produced no score. This is an **evidence-gathering limitation**, so I make no
  pass/fail claim about the quest's content; I only flag the learner-facing coupling
  in Issues below.

### Quest 2 — `github-pages-hidden-gem.md` — ⚠️ warn · 75

- **Snippet coverage: ran 4 / 3 runnable (8 recorded total); 4 passed, 0 failed, 3
  skipped, 1 reasoned.** Per-dimension: commands_work 4, content_accuracy 3,
  completeness 3, clarity 4, structure 5, safety 5.
- ✅ **passed** — `_config.yml` (title/description/`theme: minima` with inline `#`
  comment): created verbatim and parsed with Ruby `YAML.load_file` → valid.
- ✅ **passed** — `Gemfile` + `bundle install`: resolved and installed **97 gems**
  including `github-pages 232`, `jekyll 3.10.0`, `minima 2.5.1`, no errors.
- ✅ **passed** — `_posts/2025-11-14-ai-quest-chat.md` + `bundle exec jekyll build`
  then `serve`: generated `_site/2025/11/14/ai-quest-chat.html` with correctly
  rendered bold speaker labels, and the server **bound to 127.0.0.1:4000** (proven by
  a second invocation failing with "Address already in use"). Direct `curl` was
  network-blocked, but bind + HTML generation confirm the described behavior.
- ✅ **passed** — plugin `_config.yml` variant (`jekyll-feed`, `jekyll-sitemap`):
  rebuilt cleanly, producing `feed.xml`, `sitemap.xml`, `robots.txt`.
- ⏭️ **skipped** (OS mismatch — Linux sandbox) — the macOS `brew`, Windows `winget`,
  and Linux `apt` setup blocks. Two of them carry a **reasoned** concern: the extension
  id `ms-vscode.vscode-github-pull-requests-and-issues` does not match the real
  extension id `GitHub.vscode-pull-request-github`.
- 🧠 **reasoned** — the "AI Conversation Capture Format" markdown template is
  structurally identical to the post already built above; not re-run.

### Quest 3 — `prompt-crystal-mastery-vscode-copilot.md` — ⚠️ warn · 67

- **Snippet coverage: ran 10 / 9 runnable (28 recorded, 32 total); 6 passed, 4
  failed, 4 skipped, 14 reasoned.** Per-dimension: commands_work 3,
  content_accuracy 2, completeness 4, clarity 4, structure 5, safety 5.
- ✅ **passed** — both mermaid diagrams (Quest Network `graph TB` lines 48–84;
  Implementation `flowchart TD` lines 1012–1049) rendered with `mmdc` (mermaid-cli
  11.16.0) to SVG, exit 0.
- ✅ **passed** — the directory-scaffolding commands across all platform blocks:
  `mkdir -p .github/prompts && touch .github/copilot-instructions.md` (macOS/Linux),
  the PowerShell `New-Item -ItemType Directory -Force -Path ".github\prompts"`
  equivalent (via `pwsh 7`), and the Cloud-Realms `echo … > …copilot-instructions.md`
  variant — all created the exact layout described.
- ❌ **failed (4)** — the five ```` ```javascript ```` blocks at **lines 194, 205,
  581, 948, 953** are plain-English prompt strings, not code. Running them through
  `node` threw `SyntaxError` every time (e.g. line 581 `#selection …` →
  `SyntaxError: Private field '#selection' must be declared in an enclosing class`).
  They should be fenced ```` ```text ````.
- ⏭️ **skipped (4)** — all `code --install-extension` / `code --list-extensions`
  blocks: no VS Code CLI in the headless sandbox (`command not found`, exit 127).
  Syntax is valid; the quest never notes the macOS "add `code` to PATH" gotcha.
- 🧠 **reasoned (14)** — the RCTF/zero-shot/few-shot/CoT/PDCA template text (prose to
  paste into a chat, not executable). Two accuracy defects surfaced here and I
  **confirmed both directly in the source**:
  - **Invented prompt-file syntax.** Lines 785–830 (`code-review.prompt.md`) use
    frontmatter `name/description/version/inputs: [...]` and `{{ inputs.focus_area }}`
    substitution. VS Code Copilot's real prompt-file feature uses `mode`/`tools`/
    `description` frontmatter and `${input:variableName}` placeholders — Copilot would
    paste `{{ inputs.x }}` literally, never substitute it.
  - **Leaked Liquid tags.** The same lines show `# Code Review: {% raw %}{{ inputs.focus_area }}{% endraw %}`
    — the `{% raw %}`/`{% endraw %}` wrappers (17 pairs across the doc) are *visible
    inside the copyable code block*, so a learner copying from the rendered page gets
    literal Jekyll tags in their template.

> Machine summary (verbatim, quest 3): "…it has a real technical-accuracy defect:
> the `.github/prompts/*.prompt.md` template examples use an invented
> `inputs:`/`{{ inputs.x }}` frontmatter and substitution syntax that doesn't match
> how VS Code Copilot's actual prompt-file feature works, and those same examples
> leak literal Jekyll `{% raw %}`/`{% endraw %}` tags into the copyable code…"

## 🐞 Issues Found

**Quest 3 — Prompt Crystal (VS Code Copilot)**

- **high** · `prompt-crystal` · Chapter 4 `.github/prompts/*.prompt.md` templates
  (lines ~785–839; witnessed 785–830) · **Observed:** frontmatter `inputs: [...]` +
  `{{ inputs.focus_area }}` substitution does not match VS Code Copilot's actual
  prompt-file spec; a learner's "production-ready" template would never have its
  variables substituted. · **Fix:** rewrite to real spec — `mode`/`tools`/`description`
  frontmatter and `${input:variableName}` placeholders.
- **high** · `prompt-crystal` · Chapter 4 code blocks (17 `{% raw %}…{% endraw %}`
  pairs; witnessed at line 794 etc.) · **Observed:** literal Liquid tags appear inside
  the copyable template text. · **Fix:** move the raw/endraw wrapping outside the
  fenced block, or pre-render it out, so copied templates are clean.
- **medium** · `prompt-crystal` · mislabeled fences at lines 194, 205, 581, 948, 953 ·
  **Observed:** ```` ```javascript ```` blocks are prompt strings that throw
  `SyntaxError` under `node` (4 failed runs). · **Fix:** change the fence to
  ```` ```text ````.
- **low** · `prompt-crystal` · platform install blocks · **Observed:**
  `code --install-extension` assumes `code` is on PATH; on macOS it isn't until you
  run "Shell Command: Install code command in PATH". · **Fix:** add a one-line note.
- **low** · `prompt-crystal` · RCTF naming · **Observed:** the 4-letter acronym
  (Role-Context-Task-Format) is taught, but nearly every worked example silently adds
  a 5th `[CONSTRAINTS]` section. · **Fix:** reconcile the acronym with the templates.

**Quest 2 — Hidden Gem (GitHub Pages)**

- **high** · `github-pages-hidden-gem` · Chapter 2 macOS/Linux setup blocks (lines 139,
  154) · **Observed:** extension id `ms-vscode.vscode-github-pull-requests-and-issues`
  is not the real id; `code --install-extension` would fail to resolve it. · **Fix:**
  use `GitHub.vscode-pull-request-github`.
- **medium** · `github-pages-hidden-gem` · Chapter 3 Step 2 `_config.yml` comment
  (line 240) · **Observed:** points learners to `themes.jekyllrc.org`, which is
  wrong/dead; the quest's own Resource Codex (line 469) already links the correct
  `jekyllthemes.io`. · **Fix:** correct or drop the comment.
- **medium** · `github-pages-hidden-gem` · un-refined objectives (lines 99–105) ·
  **Observed (reasoned, from source):** the top objectives are still the auto-seeded
  generic placeholders ("Understand the core concepts introduced in this quest") with
  the meta-note "objectives auto-seeded during framework alignment — authors should
  refine these", and line 105 still contains a literal template placeholder
  `*[Opening paragraph that sets the fantasy context…]*`. A learner sees scaffolding
  the author never filled in. · **Fix:** replace with quest-specific objectives and
  remove the bracketed placeholder.
- **medium** · `github-pages-hidden-gem` · Chapter 3 Step 3 (`bundle install`, line
  248) · **Observed:** verification installed 97 vendor gems locally; the quest gives
  no `.gitignore` guidance, so a learner following it literally risks committing
  `vendor/bundle`, `_site`, `.jekyll-cache` into their `username.github.io` repo. ·
  **Fix:** add a `.gitignore` step before `bundle install`.
- **low** · `github-pages-hidden-gem` · line 248 · **Observed:** `rubyinstaller.org`
  is offered generically but is Windows-only. · **Fix:** scope it to the Windows path.

**Quest 1 — PRD Codex** *(no content pass/fail — evidence not gathered)*

- **medium (learner-friction, reasoned)** · `prd-codex-mastery` · platform blocks +
  challenges · **Observed:** the entire quest drives `scripts/prd-machine/prd-machine`
  from `cd ~/github/it-journey`; that tool exists only in the it-journey repo, so a
  data-scientist learner in their *own* repo has nothing to run `sync`/`status`/
  `conflicts` against. · **Fix:** state explicitly that this quest is run *inside a
  clone of the it-journey repo* (or provide the tool as a standalone), and set
  learner expectations that Docker + repo checkout are hard prerequisites.
- *Note:* the engine's `fail` here is a **max_turns / network-denied engine error**,
  not a witnessed content defect. No fabricated score is reported for this quest.

## 🔗 Chain Continuity

Reading the three in plan order as one learner's path:

- **Not a tightly-linked chain — three parallel main_quests.** By frontmatter,
  `prd-codex-mastery` lists `unlocks_quests` that *include* both `prompt-crystal` and
  `github-pages-hidden-gem`, positioning it as a level hub. But the **content** of the
  three does not build on each other: `github-pages` requires `/quests/0000/hello-noob/`,
  `prompt-crystal` requires `/quests/0010/prompt-engineering-mastery/`, and
  `prd-codex` requires nothing. A learner can take them in any order; nothing produced
  in quest N is consumed by quest N+1.
- **Prerequisite gaps for this slice.** Two of the three lean on quests *outside* the
  slice (level 0000 and 0010). That's normal cross-level layering, but it means this
  0011 slice is not self-contained: a learner dropped straight into level 0011 hasn't
  necessarily met `prompt-engineering-mastery` (0010), which `prompt-crystal` assumes.
- **Theme/character fit is loose.** The level theme is "AI-Assisted Development", and
  all three quests fit *that* — but none is data-science-specific (no data, notebooks,
  models, or analysis). For a learner who chose the **Data Scientist** path expecting
  data work, this level reads as general AI-assisted developer tooling. Worth a
  maintainer decision: is 0011 intentionally shared across paths, or should the Data
  Scientist path surface a data-flavored variant?
- **Environment continuity is the real snag.** `prd-codex` (first in the order) is the
  hardest to actually *do*: it needs Docker and the it-journey repo's internal tool.
  A beginner hitting it first could stall before reaching the two genuinely
  self-serviceable quests (`github-pages`, `prompt-crystal`). Ordering the hub-style,
  repo-coupled quest first is a friction point.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sealed). The workflow ran `agentic_validate.py --mode execute`
  in a disposable sandbox and sealed `walk-evidence.json` / `walk-evidence.md` before I
  started. I did **not** re-run the engine (its child `claude` processes can't
  authenticate from my Bash tool) and did **not** modify the plan or evidence. Per-quest
  `passed`/`failed`/`skipped` above are the engine's real sandbox runs; `reasoned`
  items are static judgments.
- **What I ran vs. reasoned:** I ran no commands myself — evidence is entirely the
  sealed engine's. My value-add is the linked-journey reasoning plus **direct source
  reads** to corroborate the engine's flagged defects: I confirmed the
  `{% raw %}{{ inputs.focus_area }}{% endraw %}` / `inputs:` syntax at lines 785–830 of
  `prompt-crystal`, and I independently spotted the **un-refined placeholder objectives
  and `[Opening paragraph …]` template stub** at lines 99–105 of `github-pages`, which
  the engine did not call out.
- **Coverage & limits (stated honestly):**
  - **Quest 1 is unscored.** The engine errored (max_turns after a network denial), so
    there is *no* per-dimension evidence for `prd-codex`. I did not invent one; its
    "fail" in the counts is an engine error, and I've framed its issue as reasoned
    learner-friction only.
  - **OS-specific and `code`-CLI commands were skipped** — the sandbox is headless
    Linux, so macOS/Windows blocks and all VS Code CLI installs are unverified (valid
    syntax, unconfirmed behavior).
  - **Network was restricted** — `curl` to github.com was blocked; the `jekyll serve`
    check relied on the bind-success signal rather than an HTTP fetch.
  - Snippet coverage was partial by design (runnable-only): quest 2 ran 4/3-runnable,
    quest 3 ran 10/9-runnable; quest 1 ran none.
- **Confidence:** High that the two scored quests' core workflows work (executed) and
  that the flagged defects are real (executed failures + my own source confirmation).
  Low/none on quest 1's content quality — I simply lack the evidence and say so.
- **Scope:** One slice, one report. No content edited, no git actions taken — the
  workflow handles those.
