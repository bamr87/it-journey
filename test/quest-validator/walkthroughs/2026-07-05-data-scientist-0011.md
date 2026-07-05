---
title: 'Quest Walkthrough — Data Scientist · Level 0011 (AI-Assisted Development)'
date: '2026-07-05T00:00:00.000Z'
character: data-scientist
level: '0011'
theme: AI-Assisted Development
tier: Apprentice
quest_count: 3
mode: execute
overall_verdict: warn
session:
  planner: walk-plan.json (windowed, index 0/1, size 5, offset 0)
  quests_scored_by_engine: 1
  quests_engine_errored: 2
  engine_average: 61.0
  engine_cost_usd: 1.0898
  note: >-
    Machine evidence was pre-computed and sealed by the workflow's execute-engine
    step; the quest-walker consumed walk-evidence.json/.md as-is and did not re-run
    the engine. 2 of 3 quests carry NO machine verdict — the engine aborted on them
    (max_turns / 600s timeout), which is an engine-run failure, not proof the quests
    are broken. Those two were assessed by static reading only (reasoned, not tested).
---

## 🎯 Session Summary

**Character:** 📊 Data Scientist · **Level:** 0011 (🌱 Apprentice, theme *AI-Assisted
Development*) · **Quests walked:** 3 of 3 in the planned window (the whole level;
`total_quests: 3`, not truncated).

**Headline verdict: ⚠️ warn — and honestly, this session is only *one quest deep* on
machine evidence.** Of the three planned quests, the sealed execute engine returned a
real scored verdict for exactly **one** — *Hidden Gem Quest: Publish AI Chats on
GitHub Pages* (61%, warn). The other two (*PRD Codex Mastery* and *Prompt Crystal*)
show as "fail" in the raw summary only because the engine **aborted** on them (PRD
Codex hit `max_turns` after 40 turns; Prompt Crystal timed out at 600s). That is an
engine-execution failure, **not** evidence the quests are defective, so I refuse to
report them as content failures. For those two I did what the skill asks when a step
wasn't run: I read the source as a learner and reasoned statically (labeled
`reasoned`), and both look structurally complete but carry cross-slice prerequisites
and paywalls that a cold-starting data scientist would hit.

The actionable core: the one quest with hard evidence has real, fixable issues
(leftover authoring placeholders in learner-facing text, a missing Ruby-3.x
`webrick` fix that breaks `jekyll serve` today, and a command-before-install ordering
bug). The slice as a "linked journey" is loose — the three quests are thematic
siblings, not a state-carrying chain.

## 🗺️ The Journey

Plan order (dependency-sorted by the planner; note it is not the natural
easy→hard order):

1. ❓ **The PRD Codex: Master Product Reality Distillation** — 🟡 Medium — score **n/a
   (engine aborted, `max_turns`)** — *Reasoned only: structurally solid Docker/CLI
   quest, but it silently assumes the learner is working **inside the it-journey
   monorepo** (`docker compose run prd-machine ./scripts/prd-machine/...`), which no
   external data-scientist learner has.*
2. ⚠️ **Hidden Gem Quest: Publish AI Chats on GitHub Pages** — 🟢 Easy — score **61%
   (warn)** — *Tested: static file steps (`_config.yml`, `Gemfile`, `_posts/*.md`) all
   parse and work; the build/preview path couldn't be verified (sandbox network) and
   the quest omits the `webrick` gem fix; leftover template placeholders drag clarity.*
3. ❓ **Forging the Prompt Crystal: VS Code Copilot Mastery Quest** — 🟡 Medium —
   score **n/a (engine aborted, 600s timeout)** — *Reasoned only: rich, well-structured
   prompt-engineering content, but gated behind a **paid GitHub Copilot subscription**
   and a prerequisite quest (0010) outside this slice.*

## 🔬 Evidence

### Quest 1 — PRD Codex Mastery — ❓ no machine evidence

The execute engine **did not produce a verdict**: it ran to `max_turns` (40) and
exited 1 (`"terminal_reason":"max_turns"`, `"errors":["Reached maximum number of
turns (40)"]`). No per-dimension scores and **no recorded commands** exist in
`walk-evidence.json` for this quest. Therefore **every observation below is
`reasoned` from the quest source, not tested.**

- `reasoned` — All learner commands are Docker invocations of the form
  `docker compose run --rm prd-machine ./scripts/prd-machine/prd-machine sync|status|conflicts`
  (lines 185–188, 336–344, 396, 428–430). These resolve a `prd-machine` compose
  service and a `./scripts/prd-machine/` script that **only exist in the it-journey
  repo**; the macOS/Linux paths even hardcode `cd ~/github/it-journey` (lines 179,
  231). A data scientist following this in their own project has nothing to run.
- `reasoned` — Prereqs (frontmatter lines 53–56, body 148–153) require Docker running
  and "a git repository with at least 7 days of commit history"; reasonable, and the
  troubleshooting table (lines 695–700) is honest about the common failure modes.
- `reasoned` — Expected-output blocks (lines 348–362, 373–381, 400–410) are concrete
  and plausible but unverifiable without the repo + Docker image; a learner can't
  self-check whether "Ingested 60 commits" is normal for their own history.

### Quest 2 — Hidden Gem: Publish AI Chats on GitHub Pages — ⚠️ tested (61%, warn)

This is the **only quest with machine evidence.** Snippet coverage from
`walk-evidence.json`: `available_total: 8`, `available_runnable: 3`, `recorded: 10`,
**ran 6 · passed 5 · failed 1 · skipped 4** (`executed: true`). Per-dimension:
commands_work 3, content_accuracy 3, completeness 3, clarity 2, structure 3,
safety 5.

Commands actually run in the sandbox:

- ✅ `passed` — `_config.yml` (Ch.3 Step 2) created verbatim, parsed with Ruby
  `YAML.load_file`.
- ✅ `passed` — `Gemfile` (Ch.3 Step 3: `source ...` + `gem "github-pages"`) — valid
  Bundler syntax.
- ✅ `passed` — `_posts/2025-11-14-ai-quest-chat.md` (Ch.3 Step 4) — correct
  `YYYY-MM-DD-title.md` convention, frontmatter parsed cleanly.
- ✅ `passed` — the second `_config.yml` (with `plugins:`) from the "Knowledge
  Foundation" box parsed; and the AI-capture markdown template parsed.
- ❌ `failed` — `bundle install` (Ch.3 Step 3): after `gem install bundler` succeeded,
  `bundle install` errored — *"An error occurred while installing minima (2.5.1), and
  Bundler cannot continue."* Engine attributes this to the **sandbox's blocked
  outbound HTTP to rubygems.org**, so it's an environment limit, **not a confirmed
  quest defect** — but it means the Gemfile→bundle→serve path was **not verified
  end-to-end.**
- ⏭️ `skipped` (×4) — `bundle exec jekyll serve` (never installable here); the macOS
  `brew`/`code`, Windows `winget`, and Linux `sudo apt`/`code` blocks (OS mismatch +
  sudo denied + no `code` CLI on the Linux sandbox).

Quoted engine summary (verbatim from `walk-evidence.md`): *"The quest's static,
hand-created-file steps (\_config.yml, Gemfile, \_posts/\*.md) all work exactly as
written and are technically sound, but the actual build/preview workflow (bundle
install, jekyll serve) could not be verified end-to-end due to sandbox network
limits, and — independent of that — the quest omits the very common Ruby 3.x webrick
gem fix needed for `jekyll serve` to work today."*

### Quest 3 — Prompt Crystal (VS Code Copilot) — ❓ no machine evidence

The execute engine **timed out after 600s** (`"error": "claude timed out after
600s"`) with no verdict and **no recorded commands**. All observations below are
`reasoned` from source.

- `reasoned` — Platform blocks (lines 195–252) run `code --install-extension
  GitHub.copilot` / `GitHub.copilot-chat` then `mkdir -p .github/prompts` /
  `touch .github/copilot-instructions.md`. These are safe and correct *if* VS Code +
  the `code` CLI are already on PATH — the same class of "assumes `code` exists"
  dependency the engine actually hit on Quest 2's Linux block.
- `reasoned` — Frontmatter requires "Active GitHub Copilot subscription (individual or
  enterprise)" (line 31). This is a **paid gate** at the Apprentice tier — a real
  stopping point for a beginner data scientist.
- `reasoned` — The bulk of the quest (RCTF, few-shot, CoT, PDCA, template library) is
  conceptual/writing practice with no runnable commands, so an execute-mode engine has
  little to *run* here regardless — consistent with a long, output-heavy session that
  ran past the timeout.

## 🐞 Issues Found

Only Quest 2 carries evidence-backed issues. Quests 1 and 3 issues are explicitly
`reasoned` (static reading), never tested — flagged as such.

| # | Severity | Quest | Where | Observed (evidence type) | Suggested fix |
|---|----------|-------|-------|--------------------------|---------------|
| 1 | **high** | Hidden Gem (GH Pages) | Ch.3 Step 3/5 (Gemfile & `jekyll serve`) | Ruby 3.2.3 is present; quest never adds `gem "webrick"`, which Ruby 3.0+ dropped from stdlib → `jekyll serve` fails with `cannot load such file -- webrick (LoadError)` for most modern learners. *(reasoned + partially tested — bundle path blocked by sandbox network)* | Add `gem "webrick"` to the Gemfile (or note `bundle add webrick`). |
| 2 | **high** | Hidden Gem (GH Pages) | Opening (line 105) & objectives (line 103) | Two authoring artifacts leaked into learner-facing text: the bracketed `*[Opening paragraph that sets the fantasy context…]*` placeholder and `> *Note: objectives auto-seeded during framework alignment…*`. *(tested — engine read them verbatim; I confirmed both in source)* | Delete both; write the real opening paragraph and refine the objectives list. |
| 3 | **medium** | Hidden Gem (GH Pages) | "Choose Your Adventure Platform" (lines 135–156) vs Ch.2 (line 195) | `code --install-extension …` is presented **before** Chapter 2 tells the learner to install VS Code — the `code` binary doesn't exist yet at that point. *(tested — sandbox `which code` → exit 1)* | Move the `code --install-extension` commands after VS Code install, or state VS Code + the `code` CLI (macOS: "Shell Command: Install code command in PATH") are prerequisites. |
| 4 | **medium** | Hidden Gem (GH Pages) | Ch.3 Step 3 (line 248) | "download from rubyinstaller.org if needed" is Windows-only advice given with no OS branching. *(reasoned)* | Note rubyinstaller.org is Windows-only; point macOS/Linux to rbenv/rvm/apt/brew. |
| 5 | **low** | Hidden Gem (GH Pages) | Resource Codex (line 464) | `github.community/c/pages/24` is the retired Discourse forum (migrated to GitHub Discussions ~2023). *(reasoned)* | Replace with `github.com/orgs/community/discussions`. |
| 6 | **low** | Hidden Gem (GH Pages) | Ch.3 Step 2 (lines 237–241) vs box (lines 281–289) | Two slightly different `_config.yml` snippets (minimal vs with `plugins:`) with no note on which supersedes. *(tested — both parse; ambiguity is editorial)* | Reconcile, or state the second extends the first. |
| 7 | **medium** | PRD Codex | macOS/Linux blocks (lines 179, 231) + all CLI cmds | Quest hardcodes `cd ~/github/it-journey` and runs the repo-local `prd-machine` compose service/script — an external learner has nothing to run. *(reasoned — engine produced no verdict)* | State up front this quest runs inside a clone of the it-journey repo (or ship a standalone `prd-machine` image/instructions). |
| 8 | **low** | Prompt Crystal | Prereqs (line 31) | Requires a **paid** GitHub Copilot subscription at Apprentice tier with no free-tier/trial note. *(reasoned)* | Note the Copilot free-tier / student options, or flag the paid requirement prominently before Chapter 1. |

No **blocking** content defect was *proven by a run* — the single failed command
(Quest 2 `bundle install`) is a sandbox network limit, and Issues 1/7/8 are the
highest-value fixes but rest on reasoning, not execution.

## 🔗 Chain Continuity

**This slice is a set of thematic siblings, not a state-carrying chain.** Reading the
three in plan order as a learner:

- **No shared state flows between quests.** PRD Codex leaves you with a generated
  `PRD.md` inside the it-journey repo; the GitHub Pages quest never uses it; Prompt
  Crystal never uses either. Finishing quest N does not set up quest N+1 — they're
  parallel tools a data scientist might pick up independently.
- **Declared prerequisites point *outside* the slice.** PRD Codex `required_quests: []`;
  Hidden Gem requires `/quests/0000/hello-noob/`; Prompt Crystal requires
  `/quests/0010/prompt-engineering-mastery/`. PRD Codex's frontmatter *unlocks* the
  other two, which is why the planner sorted it first — but the other two never
  declare PRD Codex as a prereq, so the "link" is one-directional metadata, not a
  learning dependency. A learner cold-starting at 0011 could hit gaps that only two
  earlier levels (0000, 0010) fill.
- **Ordering friction for a beginner.** The plan opens with a 🟡 Medium, Docker- and
  monorepo-bound quest (PRD Codex), then a 🟢 Easy one (GitHub Pages), then another 🟡
  Medium. A real Apprentice would more naturally start with the Easy GitHub Pages
  quest. The Medium-first ordering is an artifact of the unlocks edge, not pedagogy.
- **One genuinely coherent thread:** VS Code + the `code` CLI is a shared dependency
  of quests 2 and 3. If a learner does them **in order 2→3**, quest 2's Chapter 2
  installs VS Code, leaving them ready for quest 3's extension commands. That's the
  only place the slice actually "hands off." Note both quests share the *same*
  "assumes `code` is already on PATH" weakness (Issue 3), so the hand-off only works
  if the learner set up the CLI correctly.
- **Character fit:** For a Data Scientist, the AI thread (capture AI chats → engineer
  Copilot prompts) is on-theme; PRD Codex (documentation automation) is the outlier
  and the most environment-bound. None of the three touch data/notebooks/ML, so the
  "Data Scientist" framing at this level is generic-developer content reused across
  paths rather than data-specific.

## 🧠 Reasoning & Method

- **Mode:** `execute` — but consumed as **sealed, pre-computed evidence**. The
  workflow ran `agentic_validate.py --mode execute` in a prior deterministic step and
  wrote `walk-evidence.json` / `walk-evidence.md`; I did **not** re-run the engine (its
  child `claude` processes can't authenticate from my Bash tool) and did not edit the
  plan or evidence. I read all three quest sources in plan order for the linked-journey
  pass.
- **What was actually tested vs reasoned:** Real sandbox commands exist for **only
  Quest 2** (6 ran: 5 passed, 1 failed on a network-blocked `bundle install`; 4
  skipped). **Quests 1 and 3 have zero recorded commands** because the engine aborted
  (`max_turns` for PRD Codex; 600s timeout for Prompt Crystal). Every issue I raise
  for those two is marked `reasoned` and comes from a quoted source line — I did not
  invent scores or output for them, and I did **not** treat their raw "fail" tag as a
  content verdict.
- **Coverage limits (stated plainly):**
  - Two-thirds of the slice has **no machine verdict** — this is a partial evidence
    session, not a clean three-quest pass. Treat the "0 pass / 1 warn / 2 fail"
    summary line as "1 scored, 2 engine-errored."
  - Quest 2's **build/preview path (`bundle install` → `jekyll serve`) was never
    verified** — the sandbox blocks outbound HTTP to rubygems.org. The webrick issue
    (Issue 1) is therefore reasoned-from-environment (Ruby 3.2.3 present), not observed
    as a live `jekyll serve` failure.
  - All OS-specific and paid-subscription steps were skipped (Linux sandbox, no `code`
    CLI, no Docker image pulls, no Copilot subscription).
- **Confidence:** *High* on Quest 2's file-creation findings and the two leaked
  template artifacts (directly observed). *Medium* on the webrick and ordering issues
  (reasoned from the environment + source). *Low-to-medium* on Quests 1 and 3 —
  structural reading only, no execution; the engine aborts prevent any commands-work
  judgment, and a future re-run with a higher turn/time budget is needed before either
  can be scored.
- **Recommended follow-up:** Re-run the execute engine for PRD Codex and Prompt
  Crystal with a larger `--max-turns` / longer timeout (and, for PRD Codex, inside an
  it-journey checkout with Docker) so the two currently-unscored quests get real
  verdicts. Nothing here should be read as certifying level 0011 for the Data
  Scientist path — one of three quests carries evidence.

---

*Machine evidence source: `walk-evidence.json` / `walk-evidence.md` (sealed by the
workflow; `schema_version 1.0.0`, engine avg 61.0%, cost ~$1.09). Read-only session —
no quest content was modified; git is handled by the caller.*
