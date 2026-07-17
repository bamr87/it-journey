---
title: 'Quest Walkthrough — Data Scientist · Level 0011 (AI-Assisted Development)'
date: '2026-07-17T00:00:00.000Z'
character: data-scientist
level: '0011'
theme: AI-Assisted Development
tier: Apprentice
quest_count: 4
mode: execute
overall_verdict: warn
session:
  planner: walk-plan.json (window 0 of 1, size 5, 4 quests — full level, not truncated)
  engine: test/quest-validator/agentic_validate.py --mode execute (sealed by workflow)
  evidence: walk-evidence.json / walk-evidence.md (consumed as-is, not re-run)
  average_score: 65.8
  verdicts: 1 pass · 2 warn · 1 fail
  cost_usd: 6.4993
---

## 🎯 Session Summary

I walked the full **Data Scientist · Level 0011 (AI-Assisted Development, 🌱 Apprentice)**
slice — all **4** main quests the planner selected, in plan order — as a learner
would, using the workflow-sealed execute-mode evidence plus a close read of each
quest source. Headline: **warn — the slice is mostly usable, but it is not a clean
linear path and it contains one hard, blocking failure.**

Three quests hold up when their commands are actually run (Summon the Golem passes
cleanly at 88; Hidden Gem and Prompt Crystal warn at 68/64 with fixable defects).
The one that breaks a learner is **The PRD Codex (43, fail)**: its entire hands-on
core hangs on `docker compose build prd-machine`, which the engine verified fails
with *"no configuration file provided"* in any repo that doesn't already ship the
PRD Machine tooling — and the quest never shows how to obtain that tooling. A
maintainer's most valuable next action is to make PRD Codex self-contained (or
gate it behind the repo it assumes); everything else in the slice is polish.

Note on cohesion: these four quests share the `0011` level but belong to **four
different quest series/lines** (The Ouroboros Loop, Documentation Mastery,
Web Publishing, AI Development Mastery). This is a themed *bundle*, not a single
authored chain — an important framing for the continuity findings below.

## 🗺️ The Journey

Plan order (dependency-sorted by the planner):

1. ✅ **Summon the Golem: An AI Agent Joins the Loop** — **88/100** (pass) ·
   Drive headless Claude Code from GitHub Actions under a bounded role. Technically
   tight: every CLI flag, env var, and Action version checked out; the gating/no-op
   bash ran exactly as claimed. Only gaps are a missing env-wiring reference and no
   answer key for the knowledge checks.
2. ❌ **The PRD Codex: Master Product Reality Distillation** — **43/100** (fail) ·
   The pivotal `docker compose build prd-machine` was verified to fail with *"no
   configuration file provided"* — the quest never provides or points to the PRD
   Machine tooling, so Chapters 2–3 and all four Challenges are unrunnable from the
   document alone. **Blocking.**
3. ⚠️ **Hidden Gem: Publish AI Chats on GitHub Pages** — **68/100** (warn) ·
   Jekyll config, Gemfile, AI-chat post, and `bundle exec jekyll serve` genuinely
   work; a Linux `bundle install` permission gotcha (no vendor-path/.gitignore
   guidance) plus a wrong theme URL and a suspect extension ID drag accuracy down.
4. ⚠️ **Forging the Prompt Crystal: VS Code Copilot Mastery** — **64/100** (warn) ·
   Cross-platform scaffolding and both Mermaid diagrams run; but `{% raw %}` Jekyll
   build artifacts leak into the `.prompt.md` templates, several prompt blocks are
   mislabeled `javascript` and error as JS, and the Windows/Cloud setup silently
   overwrites an existing `copilot-instructions.md`.

## 🔬 Evidence

All results are from **execute mode** (`walk-evidence.json`, sealed by the
workflow — I consumed it as-is and did not re-run the engine). Snippet counts are
`ran / passed / failed / skipped / reasoned`. Dimension scores are on the 1–5
rubric (commands_work, content_accuracy, completeness, clarity, structure, safety).

### 1. Summon the Golem — 88 ✅ (5/5 passed, 1 skipped, 2 reasoned)
Dimensions: commands_work 4 · content_accuracy 5 · completeness 4 · clarity 4 · structure 5 · safety 5

- **passed** — Composite `action.yml` and the workflow step YAML fragments parse
  cleanly with pyyaml (no syntax errors).
- **passed** — The no-auth guard `if [ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then …
  exit 0; fi` was extracted and run with the var unset: it printed the `::warning::`
  line and exited 0, exactly as the quest claims ("No auth = exit 0 with a warning").
- **passed** — The gate logic (`go=false; if [ "$ENABLED" = "true" ] && [ -n
  "$OAUTH" ]; then go=true; fi`) tested across all 4 ENABLED/OAUTH combinations —
  arms only when both true, matching stated intent.
- **passed** — Mermaid quest-network diagram compiled to valid SVG.
- **reasoned** — `claude -p … --append-system-prompt … --allowedTools … --permission-mode
  acceptEdits`, `npm install -g @anthropic-ai/claude-code`, `claude setup-token` are
  all valid/current commands (verified against docs, not executed end-to-end — a full
  CI run needs a real repo + secret).
- **skipped** — `.claude/agents/potion-scribe.md` role file (markdown, nothing to run).

### 2. The PRD Codex — 43 ❌ (13 ran: 5 passed, 8 failed, 2 skipped, 4 reasoned)
Dimensions: commands_work 1 · content_accuracy 2 · completeness 2 · clarity 3 · structure 4 · safety 4

- **failed** — Cloud Realms path `cd /workspaces/it-journey; docker compose build
  prd-machine; …` — build fails: *"no configuration file provided: not found"*. The
  same `docker compose build prd-machine` recurs at source lines 182, 208, 234, 249
  across the macOS / Linux / Cloud paths; none can succeed without pre-existing
  tooling the quest never supplies.
- **failed** — All downstream `docker compose run --rm prd-machine …/prd-machine sync`
  (incl. `--days 7`, `--output /tmp/custom-prd.md`), `status`, `conflicts`, and the
  "Quick Win Checkpoint" sequence — every one fails because the container never built.
- **failed** — macOS and Linux path bash blocks (`docker --version; … cd
  /path/to/your/repository; cd ~/github/it-journey; …`) error as written (contradictory
  back-to-back `cd`s, unbuildable target).
- **failed** — "Best Practices for Commit Signals" block (~line 384) is fenced
  ```bash``` but is commit-message prose; run as bash it throws *"syntax error near
  unexpected token 'auth'"*.
- **passed** — Static content is sound: Signal-Rich Frontmatter YAML, `features/features.yml`,
  and all three Mermaid diagrams (Signal Source Architecture, Quest Network Position,
  Implementation Flow sequence) parse/render correctly.
- **reasoned** — The "Expected Output" transcripts (two mislabeled ```sql```, actually
  log text) are repo-specific sample output, not literal expected results.

### 3. Hidden Gem: GitHub Pages — 68 ⚠️ (4 ran: 3 passed, 1 failed, 3 skipped, 1 reasoned)
Dimensions: commands_work 3 · content_accuracy 3 · completeness 3 · clarity 4 · structure 4 · safety 5

- **passed** — `_config.yml` (minima), the captured AI-chat post
  `_posts/2025-11-14-ai-quest-chat.md`, and `bundle exec jekyll serve` build/serve —
  the hands-on core genuinely works.
- **passed** — `_config.yml` with `plugins: [jekyll-feed, jekyll-sitemap]` is valid.
- **failed** — Gemfile + plain `bundle install`: fails with a PermissionError on
  distro/system Ruby; the quest offers no `bundle config set --local path
  vendor/bundle` fallback and no `.gitignore` for `vendor/bundle`, `_site/`, `.bundle/`.
- **skipped** — OS-specific install blocks (brew / winget / apt + `code
  --install-extension …`) — environment-dependent, not run.
- **reasoned** — AI Conversation Capture markdown template is well-formed.

### 4. Forging the Prompt Crystal — 64 ⚠️ (10 ran: 5 passed, 5 failed, 4 skipped, 21 reasoned)
Dimensions: commands_work 3 · content_accuracy 3 · completeness 4 · clarity 3 · structure 4 · safety 3

- **passed** — Setup scaffolding runs: `mkdir -p .github/prompts && touch
  .github/copilot-instructions.md` (Linux), the Cloud `echo '# …' > …` variant, and
  the Windows PowerShell `code --install-extension …` / `Select-String` block. Both
  Mermaid diagrams (Quest Network, Implementation Flow) render.
- **failed** — Five ```javascript-fenced blocks (source lines ~194, 205, 581, 948,
  953) are plain-English prompt text and throw SyntaxErrors when linted/run as JS.
- **reasoned** — The RCTF/CoT/few-shot templates and the `.prompt.md` template bodies
  (lines ~683–839) are prose/markdown: static-checked. These carry the two high-severity
  defects below (leaked `{% raw %}` tags; non-native prompt-file syntax).
- **skipped** — macOS/Linux `code --install-extension` and `code --list-extensions |
  grep` blocks (no `code` CLI in sandbox / environment-dependent).
- **safety = 3** — flagged because the Windows/Cloud setup silently truncates an
  existing `copilot-instructions.md` via `-Force` / `>` with no warning.

## 🐞 Issues Found

Severity · quest · where · observed · suggested fix. (Every item below is grounded in
a command the engine actually ran or an exact line in the quest source.)

- **HIGH · PRD Codex · Chapters 2–3, `docker compose build prd-machine` (lines 182,
  208, 234, 249)** — Verified failure *"no configuration file provided: not found"*
  in a fresh repo; the PRD Machine tooling is never provided. → Add an explicit
  bootstrap step (git clone URL, or a minimal `docker-compose.yml` + `Dockerfile` +
  `scripts/prd-machine` snippet) *before* the build, so a learner starting fresh can
  actually reach `sync`/`status`/`conflicts`. This alone is the difference between a
  fail and a pass for the quest.
- **HIGH · PRD Codex · "Best Practices for Commit Signals" (~line 384)** — ```bash```
  fence around commit-message prose; running it throws *"syntax error near unexpected
  token 'auth'"*. → Re-fence as ```text``` or ```git-commit```.
- **HIGH · Prompt Crystal · Chapter 4 `.github/prompts/` templates** — Leaked
  `{% raw %}…{% endraw %}` Jekyll escape tags (12 occurrences) in the code-review,
  debug-assistant, and test-generator bodies; copied verbatim they pollute a learner's
  real `.prompt.md`. → Strip the `raw` tags from the rendered template content.
- **HIGH · Prompt Crystal · Chapter 4 prompt-file syntax** — The shown
  `name`/`version`/`inputs`/`{{ inputs.x }}` convention is not VS Code Copilot's native
  prompt-file spec (`mode`/`tools`/`description` frontmatter, `${input:var}`). → Align
  with the native spec, or explicitly label it an IT-Journey doc convention Copilot
  won't resolve.
- **MEDIUM · Hidden Gem · Chapter 3 `bundle install`** — Verified PermissionError on
  system Ruby; no vendor-path fallback, no `.gitignore` before the Step 6 commit
  (risks committing tens of thousands of dependency files). → Add `bundle config set
  --local path vendor/bundle` guidance + a `.gitignore` (`vendor/bundle`, `_site/`,
  `.bundle/`) and recommend rbenv/rvm.
- **MEDIUM · Hidden Gem · line 148 theme link** — `themes.jekyllrc.org` contradicts the
  quest's own Resource Codex (which correctly links jekyllthemes.io). → Fix to the real
  site / jekyllrb.com/docs/themes.
- **MEDIUM · Hidden Gem · VS Code extension IDs (lines 47, 62)** — "GitHub Pull Requests
  and Issues" ID looks wrong (`ms-vscode.…`); it lives under the GitHub publisher
  namespace. → Verify and correct.
- **MEDIUM · Prompt Crystal · Windows/Cloud setup file-overwrite** — `New-Item …
  -Force -Path '.github\copilot-instructions.md'` and `echo … > …/copilot-instructions.md`
  silently truncate an existing populated file (verified). → Add a warning / guard for
  "your current project."
- **MEDIUM · PRD Codex · Challenge 4** — requires reviewing `.github/workflows/prd-sync.yml`
  that is never shown/linked. → Include the workflow (or a representative excerpt).
- **LOW · Golem · env wiring** — The composite action reads `CLAUDE_CODE_OAUTH_TOKEN`
  from job env but this chapter never shows the `env:`/`secrets` wiring. → Add a one-line
  reference to where the token is injected.
- **LOW · Golem · knowledge checks** — Open-ended questions have no answer key for
  self-paced learners. → Add collapsible answers.
- **LOW · Prompt Crystal · 5 ```javascript blocks (lines 194, 205, 581, 948, 953)** —
  plain prompt text; SyntaxError if run as JS. → Re-tag ```text```/```markdown```.
- **LOW · Prompt Crystal · RCTF vs. examples** — 4-letter "RCTF" but nearly every
  worked example adds a 5th [CONSTRAINTS] section. → Rename (e.g. RCTFC) or note
  Constraints as an optional 5th block.
- **LOW · PRD Codex · code-fence languages** — two ```sql``` blocks (lines 248, 300)
  are plain log lines; a macOS block has contradictory back-to-back `cd`s. → Re-tag
  ```text``` and drop the duplicate `cd`.

## 🔗 Chain Continuity

**This slice is a level bundle, not a single authored chain.** The four quests carry
four different `quest_series`: *The Ouroboros Loop* (Golem), *Documentation Mastery*
(PRD Codex), *Web Publishing* (Hidden Gem), *AI Development Mastery* (Prompt Crystal).
A Data Scientist arriving at 0011 is not walking one story — they're picking among
parallel AI-assisted-development tracks. Judged that way, the *theme* coheres
(everything is about wielding AI tooling), but the *narrative* does not.

Prerequisite reality for a learner walking in plan order:

- **Golem** assumes "your potion-book repository with the Warden's Gate in place"
  (Chapters I–II of the Ouroboros Loop, which live at level **0101** — outside this
  slice) *and* a `claude setup-token` OAuth token. Its `quest_dependencies.required_quests`
  is empty, so nothing in-slice or in-frontmatter surfaces that gate. A learner who
  starts here cold has no gated loop to attach the golem to — the quest teaches the
  agent well in isolation, but its assumed repo state is unmet by the slice.
- **PRD Codex** `unlocks_quests` explicitly lists **prompt-crystal** and **github-pages** —
  the only real intra-slice dependency edge, and the planner honored it by ordering
  PRD before those two. But PRD is exactly the quest that *fails*: its Docker core is
  unrunnable, so the "unlock" is hollow — a learner following the intended order hits a
  wall on quest 2 and cannot legitimately complete it before moving on. The good news:
  Hidden Gem and Prompt Crystal don't actually consume any artifact PRD produces, so the
  wall is a motivation/credential break, not a hard technical block on quests 3–4.
- **Hidden Gem** requires `/quests/0000/hello-noob/` (an earlier level — reasonable and
  met by normal progression) and is the gentlest, most self-contained entry (🟢 Easy) —
  arguably the best *first* quest for a newcomer to this level, ahead of the Medium ones.
- **Prompt Crystal** requires `/quests/0010/prompt-engineering-mastery/` (prior level).
  It stands alone fine; its defects are content-quality, not continuity.

**Ordering observation for a maintainer:** as a *learning* path for a Data Scientist,
Hidden Gem (Easy, self-contained) → Prompt Crystal (prompt skills) → Golem (agent in CI,
but flag the 0101 Warden's-Gate prerequisite) is a smoother ramp than the current
dependency-sort, and PRD Codex should be treated as *not yet walkable* until its tooling
bootstrap is added. No quest in the slice silently depends on an artifact produced by
another that I could not otherwise obtain — the friction is (a) the unmet Warden's-Gate
repo state Golem assumes, and (b) PRD's missing tooling.

## 🧠 Reasoning & Method

- **Mode:** execute. I did **not** run the engine myself — per the skill and the CI
  contract, the workflow pre-computed and sealed `walk-evidence.json` / `walk-evidence.md`
  (the engine's child `claude` processes can't authenticate from an agent's Bash tool).
  I consumed the sealed evidence verbatim and did not edit, regenerate, or hand-write any
  number. `walk-plan.json` and `walk-evidence.*` were left untouched.
- **What was actually run (in the sandbox, by the sealed engine):** 32 recorded
  commands across the four quests, of which the engine ran ~32 and reasoned statically
  about the rest — Golem 5/5 passed; PRD Codex 5 passed / 8 failed; Hidden Gem 3 passed /
  1 failed; Prompt Crystal 5 passed / 5 failed. Every `passed`/`failed` above traces to
  one of those runs; every `reasoned` item is labeled as static-only.
- **What I reasoned about (me, statically):** the linked-journey continuity — series
  cohesion, prerequisite satisfaction, and ordering — by reading each quest's frontmatter
  and body in plan order. Those are the §🔗 findings and are explicitly reasoning, not
  fresh command evidence.
- **Coverage / limits:** Nothing was capped by me (the planner's window covers the full
  4-quest level; `truncated: false`). OS-specific installs and `code`-CLI steps were
  `skipped` by the engine as environment-dependent, so cross-platform install accuracy is
  only partially witnessed. PRD Codex's Docker path is genuinely broken in a clean repo, so
  its downstream chapters are unverifiable *by design of the defect* — that is itself the
  finding, not a coverage gap on my side. No network-dependent or destructive steps were run.
- **Confidence:** High on the per-quest verdicts (they come from real sandbox runs with
  quoted failure output). High on the PRD blocking-fail and the two high-severity Prompt
  Crystal defects. Medium on the extension-ID / theme-URL slips (asserted by the engine's
  content check, not independently re-verified here). The overall slice verdict is **warn**:
  three of four quests are usable today, but the slice contains one hard fail that a
  content pass should fix before this level is called "perfect."

---

*Machine evidence header (verbatim from `walk-evidence.md`): "**4** quests evaluated ·
✅ 1 pass · ⚠️ 2 warn · ❌ 1 fail · avg **65.8%** · ~$6.4993". One slice, one report —
findings only; a content pass (content-curator / human) acts on the issues above.*
