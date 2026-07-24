---
title: 'Walkthrough — Data Scientist · Level 0011 (AI-Assisted Development)'
date: '2026-07-24T13:05:28.000Z'
character: data-scientist
level: '0011'
theme: AI-Assisted Development
tier: Apprentice
quest_count: 4
mode: execute
overall_verdict: warn
session:
  planner: walk-plan.json (windowed, window 0 of 1, size 5)
  engine_evidence: walk-evidence.json (sealed by workflow; consumed as-is)
  scored: 3
  errored: 1
  average_score: 77.3
  cost_usd: 3.3098
  note: >-
    One quest (PRD Codex) produced no content verdict — the execute engine hit
    its 40-turn ceiling before scoring. That is a harness/timeout outcome, not a
    quality judgement, and is reported as such.
---

## 🎯 Session Summary

Walked the four **Level 0011 (AI-Assisted Development)** main quests assigned to the **Data Scientist 📊** path, in planner order, from the sealed execute-mode evidence the workflow gathered (`walk-evidence.json`). Three quests received real per-dimension verdicts (avg **77.3%**): **Summon the Golem** passed cleanly (88), while **Hidden Gem** (67) and **Prompt Crystal** (77) both warn on fixable authoring defects. The fourth, **The PRD Codex**, **was not scored at all** — the engine reached its 40-turn limit mid-run and exited 1, so there is no content verdict to report for it (honest gap, not a fail-on-merit).

Headline verdict: **warn.** No safety problems and every runnable snippet that executed *passed* — the friction is entirely in polish (leftover authoring placeholders, a wrong VS Code extension ID, an invented prompt-file variable syntax) plus one harness timeout. Just as important for this character slice: these four quests share only their *level*, not a storyline — they are four independent series stitched together by the level cohort, and several assume prerequisites that live **outside** the slice.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ✅ pass | Summon the Golem: An AI Agent Joins the Loop | 88 | Technically excellent CI-agent quest; extracted logic ran exactly as documented, CLI flags real. |
| 2 | ⛔ no verdict | The PRD Codex: Master Product Reality Distillation | — | Engine hit max-turns (40) and exited before scoring — **un-evaluated**, not judged. |
| 3 | ⚠️ warn | Hidden Gem Quest: Publish AI Chats on GitHub Pages | 67 | Jekyll mechanics build end-to-end, but ships visible authoring placeholders + a wrong extension ID. |
| 4 | ⚠️ warn | Forging the Prompt Crystal: VS Code Copilot Mastery | 77 | Solid prompt-engineering quest; the reusable `.prompt.md` templates use an invented variable syntax. |

## 🔬 Evidence

All evidence below is from the sealed execute-mode run (`walk-evidence.json` / `walk-evidence.md`); commands were run by the engine in its disposable sandbox. I did not re-run the engine. My own contribution is the static read of each quest source (labeled `reasoned`).

### 1. Summon the Golem — ✅ 88 (execute)
Dimensions: commands_work 4 · content_accuracy 5 · completeness 4 · clarity 4 · structure 5 · safety 5.
Snippets: 5 total, 0 classified runnable, **3 ran / 3 passed**, 1 skipped, 1 reasoned.

- **`passed`** — composite-action shell block extracted and run with `CLAUDE_CODE_OAUTH_TOKEN` unset: printed `::warning::no Claude auth — AI step is a clean no-op.` and exited 0, *exactly* matching the quest's "No auth = exit 0 with a warning" claim.
- **`passed`** — gate-arming snippet run across all four `ENABLED`/`OAUTH` combinations; `(true, unset) → go=false` matches the Mastery Challenge "disarm only the golem" scenario.
- **`passed`** — the two workflow YAML fragments parse via `yaml.safe_load`; `actions/upload-artifact@v4` confirmed as current major.
- Cross-checked against an actually-installed Claude Code CLI (v2.1.197): `--append-system-prompt`, `--allowedTools`, `--permission-mode`, `claude setup-token`, and `npm view @anthropic-ai/claude-code` all resolve as documented.
- **`skipped`** — Mermaid diagram couldn't render (headless Chromium "No usable sandbox!" — environment limit, not a quest defect); syntax reviewed and well-formed.

### 2. The PRD Codex — ⛔ no verdict (execute, harness timeout)
Engine error, verbatim from evidence: `claude exited 1: … "terminal_reason":"max_turns" … "errors":["Reached maximum number of turns (40)"]`. No dimensions, no commands, no score were produced. **Nothing about this quest's quality is asserted here** — it was not walked to completion. From a static read (my own, `reasoned`) the quest is Docker-heavy and tightly coupled to the IT-Journey repo (`docker compose build prd-machine`, `./scripts/prd-machine/prd-machine sync|status|conflicts`), which plausibly explains why the agent burned its turn budget building/running containers without reaching a verdict.

### 3. Hidden Gem (GitHub Pages) — ⚠️ 67 (execute)
Dimensions: commands_work 3 · content_accuracy 3 · completeness 4 · clarity 3 · structure 3 · safety 5.
Snippets: 8 total, 3 runnable, **5 ran / 5 passed**, 3 skipped, 1 reasoned.

- **`passed`** — `_config.yml` (Step 2) parses via Ruby `YAML.load_file`; the Step-4 post `_posts/2025-11-14-ai-quest-chat.md` built via `bundle exec jekyll build` and rendered at `_site/2025/11/14/ai-quest-chat.html` — the date-prefixed-filename convention works as taught.
- **`passed` but with friction** — the Step-3 `Gemfile` resolved and installed **97 gems**, *but only after* adding `bundle config set --local path vendor/bundle`; running `bundle install` verbatim as instructed failed with `Bundler::PermissionError: … write to /var/lib/gems/3.2.0/cache/minima-2.5.1.gem` on a stock system-Ruby setup. The quest never warns about this.
- **`skipped`** — macOS/Windows/Linux setup blocks (no brew/winget/`code`/sudo in sandbox), reasonably platform-specific.
- The `code --install-extension ms-vscode.vscode-github-pull-requests-and-issues` line (in both macOS and Linux blocks) uses a **wrong extension ID**; the real one is `GitHub.vscode-pull-request-github`.

### 4. Prompt Crystal (VS Code Copilot) — ⚠️ 77 (execute)
Dimensions: commands_work 4 · content_accuracy 3 · completeness 4 · clarity 4 · structure 4 · safety 5.
Snippets: 32 total, 9 runnable, **11 ran / 11 passed**, 5 skipped, 21 reasoned.

- **`passed`** — every genuinely runnable snippet ran clean: directory/file setup on macOS/Linux (`mkdir -p .github/prompts && touch …`), the Windows `New-Item` equivalent, the Cloud `echo > .github/copilot-instructions.md`, both Mermaid diagrams (graph TB + flowchart TD), and all three `.prompt.md` YAML frontmatter blocks (`code-review`, `debug-assistant`, `test-generator`) parse.
- **`skipped`** — `code --install-extension` / `--list-extensions` blocks (no `code` CLI in sandbox), platform-specific.
- **`reasoned` (defect)** — the reusable `.github/prompts/*.prompt.md` templates use an **invented** `inputs:` frontmatter + `{{ inputs.x }}` Liquid-style substitution (confirmed in source at lines 785–794). VS Code Copilot's real prompt-file syntax is `${input:variableName}` with `mode`/`model`/`tools`/`description` frontmatter — templates pasted as-is won't interpolate.

## 🐞 Issues Found

Every item below is backed by a command result or a quoted source line. Fixes are for a later content pass — this session edits nothing.

- **HIGH · Hidden Gem · opening (source line 105)** — a raw authoring placeholder ships to learners: `*[Opening paragraph that sets the fantasy context using RPG metaphors…]*`, sitting directly above the real opening paragraph. **Fix:** delete the placeholder line.
- **HIGH · Hidden Gem · Chapter 2 macOS & Linux setup (lines 139, 154)** — `code --install-extension ms-vscode.vscode-github-pull-requests-and-issues` is a non-existent extension ID; a learner running it verbatim gets "extension not found." **Fix:** use `GitHub.vscode-pull-request-github`.
- **HIGH · Prompt Crystal · Chapter 4 templates (lines 785–794)** — the `.prompt.md` `inputs:`/`{{ inputs.x }}` mechanic is not VS Code Copilot's real syntax; templates are non-functional if used as taught. **Fix:** switch to `${input:variableName}` and real frontmatter fields (`mode`, `model`, `tools`, `description`).
- **MEDIUM · Hidden Gem · Chapter 3 Step 3 (`bundle install`)** — verified in sandbox: `bundle install` verbatim fails with `Bundler::PermissionError` on stock Linux/system-Ruby; only succeeds after `bundle config set --local path vendor/bundle`. **Fix:** document the failure mode + the local-path/rbenv workaround.
- **MEDIUM · Hidden Gem · objectives (lines 100–103 vs 113–129)** — a generic auto-seeded objectives checklist *plus* an explicit self-flagging note (`objectives auto-seeded during framework alignment — authors should refine…`) sits above the detailed Primary/Secondary/Mastery block. Redundant and signals an unfinished edit. **Fix:** keep only the detailed block.
- **MEDIUM · Prompt Crystal · prerequisites** — the quest assumes GitHub Copilot access without stating an active Copilot subscription/trial is required. **Fix:** state it near platform setup.
- **LOW · Hidden Gem · Resource Codex** — dead GitHub Community Forum link (`github.community`, retired 2023). **Fix:** point to `github.com/orgs/community/discussions`.
- **LOW · Summon the Golem · Chapter 2 workflow step** — the "Summon the scribe" step inherits the composite action's default `tools: Bash,Read,Write,Grep,Glob`, granting Bash to a golem whose "never run git" oath is enforced only behaviorally. **Fix:** override `tools: "Read,Write,Grep,Glob"` for real defense-in-depth, or note why Bash is retained.
- **LOW · Summon the Golem · completeness** — `steps.check.outputs.status` and `steps.pick.outputs.potion` are used but defined only in prior campaign chapters (not in this file). A one-line footnote would make the chapter self-contained.
- **LOW · Prompt Crystal · structure** — two near-duplicate "Quest Validation" sections and an RCTF acronym (4 letters) that doesn't match the 5-section (Role-Context-Task-Constraints-Format) examples. **Fix:** merge/reconcile.

**Harness note (not a content bug):** PRD Codex hit the 40-turn engine ceiling and yielded no verdict. If it keeps timing out, consider raising `--max-turns` for Docker-heavy quests or pre-flighting whether `prd-machine` is even buildable in the sandbox — otherwise this quest can never be certified by the loop.

## 🔗 Chain Continuity

Reasoned from reading all four sources in plan order, as a Data Scientist arriving at Level 0011:

- **This is a level cohort, not a linked campaign.** The four quests belong to four *different* series — "The Ouroboros Loop" (Autonomous Realm), "Documentation Mastery Path", "Web Publishing Mastery", and the Prompt-Crystal line. They share the `0011` level and the "AI-Assisted Development" theme, nothing more. Finishing quest N does **not** set up quest N+1; there is no carried state between them.
- **Planner ordering surfaces the hardest quest first.** "Summon the Golem" is explicitly **Chapter III** of a multi-part campaign whose prerequisites ("Chapters I–II… the gate is load-bearing today", `claude setup-token` already run) live **outside this slice** (the Warden's Gate at `/quests/0101/`). A learner who lands here first, cold, hits `steps.check.outputs.status`/`steps.pick.outputs.potion` with no idea where they came from. It reads best as the *last*, most advanced quest of the four, not the first.
- **Cross-slice prerequisites are the norm here.** Hidden Gem requires `/quests/0000/hello-noob/`; PRD Codex assumes a working IT-Journey checkout with Docker and the repo's `prd-machine` tool; Prompt Crystal assumes a Copilot subscription. None of these are provided by a sibling quest in the slice — each is a self-contained on-ramp that leans on setup elsewhere.
- **PRD Codex is the intended connective tissue but couldn't be walked.** Its frontmatter `unlocks_quests` lists both `prompt-crystal-vscode-copilot` and `github-pages-hidden-gem`, so on paper it's the hub feeding two of the other three. That makes its un-evaluated status the biggest coverage gap in this slice — the one quest that ties the cohort together is the one with no verdict.
- **Character fit:** none of the four is data-science-specific — they're general AI-assisted-development quests shared across character paths at this level. That's fine for a foundation tier, but a Data Scientist won't find pandas/notebooks/modeling here; the "data" framing is entirely in the level's AI theme, not the quest content.

## 🧠 Reasoning & Method

- **Mode:** `execute`, sealed by the workflow. I consumed `walk-plan.json` + `walk-evidence.json`/`.md` **as-is** and did **not** re-run the engine (its child `claude` processes can't authenticate from my Bash tool) and did not edit either file.
- **What I ran vs. reasoned:** I ran **nothing** myself against the quests — all `passed`/`failed`/`skipped` verdicts come from the engine's sandboxed commands. My added value is the static linked-journey read of all four quest sources (labeled `reasoned` throughout), plus verifying the two high-severity source-line citations (Hidden Gem placeholder line 105 / extension IDs lines 139 & 154; Prompt Crystal `inputs:` template lines 785–794) directly in the files.
- **Coverage & limits (honest):**
  - **3 of 4 quests scored.** PRD Codex has **no content verdict** — engine max-turns timeout. I have not asserted any quality for it; treat it as **un-walked**, needing a re-run (possibly with a higher turn budget or a sandbox pre-check for `prd-machine`).
  - Several snippets were legitimately **skipped** as platform-specific (brew/winget/`code`/sudo unavailable in the Linux sandbox) or environment-limited (Mermaid render blocked by headless-Chromium sandbox). These are engine/environment limits, not quest defects, and are not counted as failures.
  - Every runnable snippet that *did* execute **passed** (Golem 3/3, Hidden Gem 5/5, Prompt Crystal 11/11) — the warns are about polish and real-tool-accuracy, not broken mechanics.
- **Confidence:** High for the three scored quests (per-dimension evidence + verified source citations). Zero for PRD Codex — flagged explicitly as a coverage gap rather than a pass or fail.
- **Overall verdict — warn:** one clean pass, two fixable warns, one un-evaluated quest, no safety issues. The slice is usable but rough at the edges, and does not yet hold together as a *linked* journey for the Data Scientist path.

---

*Machine evidence excerpted verbatim above is drawn from `./walk-evidence.md` and `./walk-evidence.json` (sealed execute-mode run, avg 77.3%, ~$3.31). This report is the only artifact this session writes; git is handled by the caller.*
