---
title: "Quest Walkthrough — Data Scientist · Level 0011 (AI-Assisted Development)"
date: 2026-07-04T12:05:00.000Z
character: data-scientist
level: "0011"
theme: "AI-Assisted Development"
tier: "Apprentice 🌱"
quest_count: 3
mode: execute
overall_verdict: warn
session: |
  planner: scripts/quest/walkthrough_plan.py (./walk-plan.json, date-rotated, slug data-scientist/0011)
  agentic_engine: UNAUTHENTICATED — test/quest-validator/agentic_validate.py --mode execute (and --mode review)
    both aborted with "Claude could not authenticate": the validator delegates auth to a child `claude`
    process and no CLAUDE_CODE_OAUTH_TOKEN is present in this managed session (host auth is not inherited
    by child claude processes). walk-evidence.json / walk-evidence.md were therefore NOT produced by the engine.
  fallback: the walker played the three quests directly as a learner, running every safe, runnable command
    for real in a disposable sandbox. All passed/failed below come from commands I actually ran.
  sandbox: disposable /tmp/walk-sandbox.* ; bash, python 3.12.13, git 2.54, node 20.20.2, docker 28.0.4 present;
    VS Code `code` CLI ABSENT; jekyll/bundler ABSENT. Scores below are my REASONED assessment, not machine-computed.
---

## 🎯 Session Summary

I walked the **Data Scientist · Level 0011 (AI-Assisted Development, Apprentice 🌱)**
slice the planner selected in `./walk-plan.json` — three linked main quests, in plan
order: **The PRD Codex → Hidden Gem: Publish AI Chats on GitHub Pages → Forging the
Prompt Crystal (VS Code Copilot)**. I played them end-to-end as an apprentice would,
executing every safe command in a disposable sandbox.

**Headline verdict: ⚠️ warn** (1 pass, 2 warn; reasoned avg ≈ 76%). The executable
core of the slice is genuinely sound: the **PRD Machine CLI runs cleanly** — I ran
`sync`, `status`, and `conflicts` for real and got a complete 10-section `PRD.md`,
a HEALTHY status, and an 18-conflict report. The warn is driven by three concrete,
fixable problems a learner *will* hit: (1) the PRD quest's taught `--days N` flag is
**silently ignored** by the tool (always "last 30 days"), which breaks its own
"compare `--days 7` vs 30-day" challenge; (2) that same quest sends learners to review
`.github/workflows/prd-sync.yml`, **which does not exist**; and (3) the *GitHub Pages
Hidden Gem* quest ships an **unfinished top section** — a literal `*[Opening
paragraph…]*` template placeholder plus auto-seeded objectives with an author note
still visible to readers, under `draft: false`. The *Prompt Crystal* quest is the
strongest of the three and passes.

> **Coverage honesty:** the prescribed `agentic_validate.py --mode execute` engine
> could **not run** here (child-`claude` auth failure — see frontmatter). I did not
> fabricate its JSON verdicts. Every "passed"/"failed" is from a command I ran myself;
> everything else is labelled `reasoned` or `skipped`. Docker-image builds and all
> VS Code / GitHub Copilot GUI steps were not runnable in this sandbox.

## 🗺️ The Journey

| # | Quest | Type · Difficulty | Verdict | Reasoned Score | One-line takeaway |
|---|-------|-------------------|---------|----------------|-------------------|
| 1 | The PRD Codex: Master Product Reality Distillation | main · 🟡 Medium | ⚠️ warn | ~76% | CLI works & generates all 10 PRD sections, but `--days` is ignored and the CI workflow it references is missing. |
| 2 | Hidden Gem: Publish AI Chats on GitHub Pages | main · 🟢 Easy | ⚠️ warn | ~64% | Correct Jekyll/GitHub flow, but unfinished top: placeholder paragraph + auto-seeded/duplicate objectives shipped live. |
| 3 | Forging the Prompt Crystal: VS Code Copilot Mastery | main · 🟡 Medium | ✅ pass | ~89% | Excellent, well-structured prompt-engineering quest; scaffold commands run clean; prereq resolves. |

## 🔬 Evidence

### Quest 1 — The PRD Codex (`pages/_quests/0011/prd-codex-mastery.md`)
Ran the underlying `scripts/prd-machine/prd-machine` CLI directly (the Docker-wrapped
tool the quest teaches); Docker-image build was not attempted (no image pull). Snippet
coverage: **ran 5/5 runnable CLI commands**; Docker `compose build/run` invocations
`reasoned` (equivalent CLI tested).

- `python3 scripts/prd-machine/prd-machine.py --help` → **passed**. Shows `sync|status|conflicts` subcommands exactly as the quest describes.
- `prd-machine sync --days 7 --output <sandbox>/PRD.md` → **passed** (exit 0). Output: `Ingested 138 commits … Ingested 32 markdown files … Ingested 1 features … Detected 18 potential conflicts … PRD generated successfully … Total signals processed: 191`.
- PRD section check → **passed**. Generated `PRD.md` contains all 10 sections: `## 0. WHY` through `## 9. DONE (Definition of Done)` (`grep -cE '^## [0-9]'` = 10). Matches the quest's "10 sacred sections" table.
- `prd-machine status` → **passed**. `Health: HEALTHY`, `Age: 0.0 hours` — matches the quest's expected HEALTHY output and 6-hour freshness model.
- `prd-machine conflicts` → **passed**. Emitted `Found 18 conflicts` with `[fix] Bug fix suggests incomplete requirement…` entries and `Resolution:` lines, exactly the shape the quest documents (real counts differ from the quest's illustrative "4", which is fine for a living repo).
- `prd-machine sync --days 1` and `--days 30` (default) → both **passed but identical**: each ingested **138 commits** and logged `Ingesting git commits from last 30 days`, whereas `git log --since` reports **4** (1d) / **38** (7d) / **136** (30d) commits. → evidence the `--days` flag is not honored (see Issues).

### Quest 2 — Hidden Gem: GitHub Pages (`pages/_quests/0011/github-pages-hidden-gem.md`)
Almost all steps target the learner's *own external* GitHub repo + VS Code GUI, so
most are `reasoned`/`skipped`, not runnable in-sandbox. Snippet coverage: **ran 2
runnable scaffolds; skipped the VS Code/`code` and GitHub-web steps**.

- `_config.yml` + `_posts/2025-11-14-ai-quest-chat.md` scaffold (Ch.3) → **passed**. Files created; `_config.yml` parses as valid YAML. The `layout: post` + dated-filename convention is correct standard Jekyll.
- `code --install-extension …` (macOS/Win/Linux paths) → **skipped**: `code` (VS Code) CLI absent in sandbox; these are learner-machine GUI steps.
- `sudo apt update && sudo apt install git`, GitHub repo creation, Pages settings, `bundle exec jekyll serve` → **reasoned** (correct, standard instructions; not executed — privileged/external/no bundler).
- Static read of the quest body surfaced two content defects (see Issues) — quoted directly from lines 95–109.

### Quest 3 — Forging the Prompt Crystal (`pages/_quests/0011/prompt-crystal-mastery-vscode-copilot.md`)
Snippet coverage: **ran the 1 runnable shell scaffold; Copilot/VS Code steps skipped**.

- `mkdir -p .github/prompts && touch .github/copilot-instructions.md && echo … > …` (all platform paths) → **passed** (exit 0). Directory + file created as described; this is the quest's only sandbox-runnable command block and it is correct.
- `code --install-extension GitHub.copilot[-chat]` + `code --list-extensions | grep copilot` → **skipped**: requires VS Code + a Copilot subscription; not present.
- Prerequisite resolution → **passed** (reasoned/verified): `quest_dependencies.required_quests: /quests/0010/prompt-engineering-mastery/` resolves — `pages/_quests/0010/prompt-engineering.md` carries `permalink: /quests/0010/prompt-engineering-mastery/`. The RCTF/few-shot/CoT/PDCA content is accurate and internally consistent.

## 🐞 Issues Found

- **medium · Quest 1 (PRD Codex) · `sync --days N` flag / Ch.2 + Challenge 1 Bonus + Knowledge Check** — What I observed: `sync --days 1`, `--days 7`, and default all ingested **138 commits** and printed `Ingesting git commits from last 30 days`, while `git log --since` gives 4/38/136 for 1/7/30 days. The flag has no measurable effect and the log line is hardcoded to "30 days". The quest teaches `sync --days 7`, asks "What does `--days 7` do?" (answer claims "commits from last 7 days"), and Challenge 1 Bonus tells learners to "Compare with `--days 7` vs default 30 days / Document signal count differences" — a learner will find **no difference**, contradicting the quest. *Suggested fix:* either fix the tool to honor `--days` (and make the log line reflect the value), or, since the quest is read-only over the tool, soften the Knowledge-Check answer + Challenge and note the current 30-day default behavior.
- **medium · Quest 1 (PRD Codex) · Challenge 4 "CI/CD Integration"** — What I observed: Challenge 4 says "Review `.github/workflows/prd-sync.yml`" and "Understand the 6-hour cron schedule", but no such file exists (`ls .github/workflows | grep -i prd` → none). The "Configure CI/CD Integration" secondary objective is therefore uncompletable. *Suggested fix:* point to the actual workflow if one exists under a different name, add the `prd-sync.yml` workflow, or reframe Challenge 4 as "author your own workflow" rather than "review the existing one".
- **high · Quest 2 (Hidden Gem) · body lines 95–105 (top of quest)** — What I observed: shipped `draft: false` but the opening is unfinished. Line 105 is a literal template placeholder: `*[Opening paragraph that sets the fantasy context using RPG metaphors…]*`. Lines 99–103 are generic auto-seeded objectives ("Understand the core concepts introduced in this quest") followed by a reader-visible author note: `> *Note: objectives auto-seeded during framework alignment — authors should refine these…*`. This violates quest.instructions §4 (no `[placeholder]` brackets) and reads as broken to a learner. *Suggested fix:* delete the placeholder paragraph and the auto-seed note; keep the real narrative at line 107 and the real objectives at line 109.
- **medium · Quest 2 (Hidden Gem) · duplicate objectives sections (lines 95 & 109)** — What I observed: two objectives headers — `## 🎯 Quest Objectives` (placeholder text, the one the validator keys on) at line 95 and `## 🌟 Quest Objectives and Learning Outcomes` (the real, detailed objectives) at line 109. Redundant and contradictory. *Suggested fix:* merge into a single `## 🎯 Quest Objectives` populated with the real objectives.
- **low · Quest 2 (Hidden Gem) · Knowledge Graph footer + no Mermaid** — What I observed: unlike quests 1 & 3, the `## 🕸️ Knowledge Graph` footer has only level-hub + overworld links (no related-quest wiki-links), and the quest has no Mermaid network diagram. Weakens discoverability/continuity. *Suggested fix:* add related-quest wiki-links and a small prerequisite/unlock Mermaid graph.
- **low · Quest 3 (Prompt Crystal) · Ch.3 copilot-instructions example (~line 719)** — What I observed: the illustrative `copilot-instructions.md` says `Quests: pages/_quests/lvl_XXX/quest-name/index.md`, an outdated path convention; current repo layout is flat `pages/_quests/XXXX/<slug>.md` (per quest.instructions §3). *Suggested fix:* update the example path to the current flat convention.
- **low · Quest 3 (Prompt Crystal) · "Next Epic Adventures" all planned** — What I observed: every follow-up is "Planned quest (see Quest Build Plan)" and `unlocks_quests: []`, so the chain dead-ends here. Honest, but no live next step. *Suggested fix:* link at least one existing 0100-level quest when available.

No destructive or unsafe commands were found in any of the three quests (safety is good across the slice; the only privileged command, `sudo usermod -aG docker $USER` in Quest 1, is standard and contextualized).

## 🔗 Chain Continuity

- **Ordering is coherent, but the quests are parallel, not sequential.** Plan order is PRD Codex → Hidden Gem → Prompt Crystal. PRD Codex declares no required quests (a clean entry point) and its `unlocks_quests` lists *both* the other two slice members — so "PRD Codex first" is the right call. However, none of the three consume another's artifacts; they're thematically linked (AI-assisted development) rather than dependency-linked. A learner can complete them in any order after external prerequisites.
- **No prerequisite gaps within the slice.** External prereqs all resolve: Hidden Gem → `/quests/0000/hello-noob/` (exists); Prompt Crystal → `/quests/0010/prompt-engineering-mastery/` (exists, permalink verified). Nothing in the slice silently assumes setup an earlier slice member was supposed to provide.
- **Tooling continuity is uneven.** Quest 1 needs Docker (or Python) locally; Quest 2 needs a GitHub account + Ruby/Bundler + VS Code; Quest 3 needs VS Code + a paid Copilot subscription. An apprentice moving through the slice must stand up three fairly different toolchains — worth a shared "what you'll need" note at the level hub.
- **Character-fit is loose.** The slice is filed under the **Data Scientist** path, but all three quests are character-agnostic AI/dev-tooling topics (PRD automation, GitHub Pages publishing, Copilot prompting) — nothing data-science-specific (no data wrangling, notebooks, or modeling). They fit the *level theme* "AI-Assisted Development" well; the *character* mapping is thematic, not topical. Not a blocker, but a data-scientist learner won't find domain content here.

## 🧠 Reasoning & Method

- **What I ran vs. reasoned:** I executed the full PRD Machine CLI (`--help`, `sync` with `--days 1/7/30`, `status`, `conflicts`) and inspected the generated `PRD.md`; I ran the Quest 2 `_config.yml`/`_posts` scaffold (validated YAML) and the Quest 3 `.github/prompts` scaffold. All of those are real `passed` results. Docker-image builds, VS Code/`code` extension installs, GitHub-web/Pages steps, `bundle exec jekyll serve`, and Copilot interactions were **skipped** (tooling/subscription/GUI absent) or **reasoned** (external, correct-looking instructions). Cross-quest prerequisite/permalink resolution was verified against the repo.
- **Mode & sandbox:** Intended `--mode execute`. The prescribed `agentic_validate.py` engine **could not run** — both `execute` and `review` abort with "Claude could not authenticate" because the validator spawns a child `claude` process and no `CLAUDE_CODE_OAUTH_TOKEN` is present in this managed session. Consequently **`walk-evidence.json` / `walk-evidence.md` were not produced**, and the per-dimension **scores in this report are my own reasoned assessment**, computed by hand against the schema weights (commands 0.30 / accuracy 0.25 / completeness 0.15 / clarity 0.15 / structure 0.05 / safety 0.10) from what I directly observed — they are **not** machine-generated verdicts and should be read as such. Where the standard pipeline runs with auth, its numbers supersede mine.
- **Limits of this pass:** No Docker image was built (I tested the equivalent Python CLI the container wraps); no VS Code, Copilot, Ruby/Bundler, or Jekyll available; no external GitHub repo created. I did not mutate the host working tree — the PRD `sync` runs wrote only to `--output` paths under the disposable sandbox (`status` read a committed `PRD.md` already in the checkout).
- **Confidence:** High on Quest 1's CLI behavior and the `--days`/missing-workflow findings (directly reproduced); high on Quest 2's placeholder/duplicate-objectives defects (quoted from source); medium-high on the reasoned scores and on steps I could only read (VS Code/Copilot/Jekyll paths).
