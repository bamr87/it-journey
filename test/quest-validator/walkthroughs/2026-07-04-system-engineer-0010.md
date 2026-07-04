---
title: "Quest Walkthrough — System Engineer · Level 0010 (Terminal Mastery)"
date: 2026-07-04T00:00:00.000Z
character: system-engineer
level: "0010"
theme: Terminal Mastery
tier: Apprentice
quest_count: 16
mode: manual-sandbox-execution
engine: agentic execute engine UNAVAILABLE (child claude process had no OAuth token) — walked manually + tier-1 deterministic
overall_verdict: warn
session: >
  Walked the full 16-quest system-engineer/0010 slice as a learner in a disposable
  GitHub Actions runner sandbox. The agentic execute engine could not authenticate,
  so evidence comes from (a) commands the walker ran directly and (b) the deterministic
  tier-1 validator. The 0010/ "Terminal Mastery" quests are strong and runnable; the
  tools/ "Tools Collection" quests are imported blog chapters that bypass the quest
  rubric — one (planting-seeds) is completely empty.
---

## 🎯 Session Summary

**Character:** 🏗️ System Engineer · **Level:** `0010` — Terminal Mastery (🌱 Apprentice).
**Quests walked:** 16 (12 main, 4 side), in the planner's order. **Verdict: ⚠️ WARN.**

This slice is really **two curricula wearing one level number**. The seven `pages/_quests/tools/`
quests (`quest_series: Tools Collection`) are imported, prose-only blog chapters: none has a
`## 🎯 Quest Objectives` section, none has multi-platform paths or a Rewards/Next-Adventures
structure, and one — **`planting-seeds.md` — has no body content at all** (127 words, almost
entirely frontmatter + the auto-generated Knowledge Graph footer). Critically, the tier-1
validator **silently skips everything under `tools/` as a "non-quest directory"**, so these
seven published `layout: quest` pages ship with **zero quality gating** even though they render
as playable 0010 quests on the level hub.

By contrast, the nine `pages/_quests/0010/` quests are genuine, well-structured, and largely
runnable. I executed real commands for `bash-scripting`, `django-and-git`, and
`nerd-font-enchantment` — they work as written (django-and-git installed Django 6.0.6 and made a
commit end-to-end). The one command failure I *witnessed* is a paste-corruption bug in
`django-and-git`'s bundled automation script (`<end_o` on line 168, exit 1 at runtime).

## 🗺️ The Journey

| # | Verdict | Quest (type) | Tier-1 | One-line takeaway |
|---|---|---|---|---|
| 1 | ⚠️ | Understanding Action Triggers (main) | 0/0 *skipped* | Prose GitHub-Actions chapter; no objectives, illustrative YAML only |
| 2 | ⚠️ | Mastering Branches & Pull Requests (main) | 0/0 *skipped* | Concept-only; zero runnable commands, no objectives |
| 3 | ⚠️ | Changelogs & the Chronicles of Code (main) | 0/0 *skipped* | Concept-only; empty `categories`/`tags`, no objectives |
| 4 | ⚠️ | Commit Hygiene: Clean Atomic Commits (main) | 0/0 *skipped* | Concept-only; commit-message examples mis-tagged as `yaml`/`bash` |
| 5 | ⚠️ | Conjure a Django Project into GitHub (main) | 0/0 *skipped* | Steps 1–6 run clean; **bundled script line 168 crashes** (`<end_o`) |
| 6 | ✅ | Nerd Font Enchantment (side) | 87.8% | Solid; test script + unicode snippets ran; install needs a real GUI |
| 7 | ✅ | Oh-My-Zsh Mastery (main) | 91.9% | Well-built; install not runnable here (zsh absent) — reasoned |
| 8 | ❌ | Planting Seeds: Set Up Your Dev Toolkit (main) | 0/0 *skipped* | **Empty quest** — frontmatter + footer only, no content |
| 9 | ⚠️ | Revolutionizing Work with AI Automation (main) | 0/0 *skipped* | Prose chapter; OpenAI snippet mis-tagged `bash`, no objectives |
| 10 | ✅ | Terminal Artificer: Glass Interface (side) | 96.1% | Excellent structure; `gum` absent so commands syntax-checked only |
| 11 | ✅ | Bash Incantations: Scripting Quest (main) | 95.9% | Strong; `data_wizard.sh` + `system_monitor.sh` ran successfully |
| 12 | ⚠️ | Jekyll-Mermaid Integration (main) | 81.1% | Good body, but **Quest Objectives are auto-seeded placeholders** |
| 13 | ✅ | Prompt Engineering Mastery (main) | 91.9% | Structurally sound (objectives present); not command-walked |
| 14 | ✅ | Recursive Realms: Testing Quests (main) | 100.0% | Top tier-1 score; not command-walked |
| 15 | ✅ | Stats Dashboard (side) | 78.4% | Good Liquid quest; **belongs to Contributor Path, not Terminal Mastery** |
| 16 | ✅ | Contribution Calendar (side) | 78.4% | Good CSS-grid quest; also Contributor Path, prereq outside slice |

## 🔬 Evidence

Sandbox: disposable runner temp dir (`/tmp/questwalk.*`). Toolchain present: git 2.54.0,
python3 3.12.13, node 20.20.2, bash 5.2.21. **Absent:** `zsh`, `gum`, `mmdc` (mermaid),
`fc-list`/Nerd Fonts. Network + `pip` were available.

**Quest 11 — bash-scripting** · ran 2/? runnable non-interactive scripts, syntax-checked 1 interactive.
- `data_wizard.sh` → **passed** (exit 0). Output matched the quest's claims exactly:
  `Lowercase: mighty_fireball_enchantment`, `First word: MIGHTY`, `Length: 27 characters`,
  arithmetic `Remaining mana: 75 / Maximum spells possible: 4 / Current level: 15`,
  parameter expansion `Extension: spell`, `Default value demo: default_value`.
- `system_monitor.sh` (the `--test` / `analyze_system_health` path) → **passed** (exit 0),
  logged `[INFO] CPU: 0%, Memory: 7%, Disk: 40%` → `System health normal`. Memory/disk correct;
  **CPU parse fell back to `0%`** (the `top -bn1 | grep "Cpu(s)"` awk/sed chain didn't match on
  this runner). Non-fatal, but a learner's monitor would never fire a CPU alert.
- `hello_wizard.sh` → **passed** `bash -n` (syntax OK); not run live (interactive `read`).

**Quest 5 — django-and-git** · ran the local half of the 7-step ritual.
- `mkdir django-magic && python3 -m venv venv && source .../activate && pip install django &&
  django-admin startproject myproject . && git init && git add . && git commit` → **passed**.
  Installed **django 6.0.6**, generated `manage.py` + `myproject/`, produced commit
  `bfadc1f "Initial commit - A wizard is never late!"`. Steps 4/5/7 (create GitHub repo,
  `git remote add`, `git push`) **skipped** — need real GitHub auth.
- Bundled full-automation script, line 168 `echo "🚀 Navigating to ~/github directory..."<end_o`
  → **failed** at runtime: `end_o: No such file or directory`, exit 1. The stray `<end_o`
  redirects stdin from a nonexistent file. A learner who copies the whole script hits this.

**Quest 6 — nerd-font-enchantment** · ran the safe display snippets.
- `test-nerd-fonts.sh` heredoc + `chmod +x` + run → **passed** (exit 0); emoji/unicode printed.
- `echo` unicode line, `time echo …`, and the `for i in {1..N}` loop → **passed**.
- `brew`/`apt`/`choco` font installs and `fc-list | grep meslo` verification → **skipped**
  (no Nerd Font / fontconfig on the runner; installs need a real desktop). Reasoned.

**Quest 10 — terminal-artificer** · `class_selector.sh` → **passed** `bash -n`; `gum` **absent**,
so `gum choose/input/confirm` were **skipped** (install needs network + sudo/apt keyring).

**Quests 7, 12, 15, 16 — skipped/reasoned:** Oh-My-Zsh needs `zsh` (absent) + a network install;
Jekyll-Mermaid and the two side-quests are Jekyll Liquid/CSS that require a full site build
(Docker/Ruby ≥3.2 per repo docs) — not runnable in a bare sandbox. Judged statically.

**Quests 1–4, 9 (tools prose):** no learner-runnable commands exist to execute — the only fenced
blocks are illustrative CI YAML, a PR/changelog template, and commit-message examples.

**Deterministic tier-1 (`quest_validator.py`) — this DID run:** the nine `0010/` quests score
78.4–100.0%; all seven `tools/` quests return `0/0 (0.0%)` with the info line
`Skipped: non-quest directory (tools/)`.

## 🐞 Issues Found

- **HIGH · planting-seeds.md · whole file** — Observed: the quest body is **empty** (127 words
  total; only frontmatter + the Knowledge Graph footer). A learner landing on
  `/quests/0010/planting-seeds/` ("Set Up Your Dev Toolkit", a *main_quest*) gets nothing.
  *Fix:* author the toolkit-setup content, or set `draft: true` / remove it from the level hub
  until written.

- **HIGH · all 7 `tools/` quests · validator coverage** — Observed: `quest_validator.py` prints
  `Skipped: non-quest directory (tools/)` and scores them `0/0`, yet they are published with
  `fmContentType: quest`, `layout: quest`, `quest_type: main_quest`, and `/quests/0010/…`
  permalinks, so they render as playable quests with **no quality gate**. *Fix:* either migrate
  these files into a real level directory (`pages/_quests/0010/`) so the rubric applies, or stop
  presenting `tools/` files as playable quests. This is a fleet-wide coverage gap, not just this
  slice.

- **HIGH · django-and-git.md · bundled automation script, line 168** — Observed: `bash` run of
  `echo "…"<end_o` fails with `end_o: No such file or directory` (exit 1) — a paste corruption.
  *Fix:* delete the stray `<end_o` so the line is a plain `echo`.

- **MEDIUM · action-triggers / branches-and-pull-requests / change-logs / commitments-to-clean-commits
  / django-and-git / revolutionizing-work-with-ai-automation · structure** — Observed: none of
  these has a `## 🎯 Quest Objectives` section (rubric §4 requires it with `- [ ]` checkboxes);
  none has multi-platform sections or a Rewards/Next-Adventures structure. They read as sequential
  blog chapters ("Chapter 2…5"). *Fix:* add Quest Objectives + the required body skeleton, or
  reclassify as `docs`/notes rather than quests.

- **MEDIUM · jekyll-mermaid-integration.md · Quest Objectives** — Observed (quoted): objectives are
  boilerplate — "Understand the core concepts introduced in this quest / Complete the hands-on
  exercises…" — followed by the visible author note *"objectives auto-seeded during framework
  alignment — authors should refine these…"*. *Fix:* replace with Mermaid-specific outcomes
  (CDN conditional loading, diagram types, dark-mode, etc.).

- **LOW · commitments-to-clean-commits.md & revolutionizing-work-with-ai-automation.md · code fences**
  — Observed: commit-message examples are fenced ` ```yaml `/` ```bash ` though they are neither
  YAML nor bash; the OpenAI workflow example is fenced ` ```bash ` though it's YAML. *Fix:* use
  `text`/`yaml` tags to match content.

- **LOW · action-triggers.md & revolutionizing-work-with-ai-automation.md · `{% raw %}` inside code**
  — Observed (quoted): `Bearer ${% raw %}{{ secrets.OPENAI_API_KEY }}{% endraw %}` and
  `${% raw %}{{ secrets.GITHUB_TOKEN }}{% endraw %}` appear *inside* fenced code, so learners see
  the literal `{% raw %}` wrappers. *Fix:* move the raw guards outside the token or restructure the
  snippet. (Not build-verified this session — Jekyll build wasn't run — so flagged as observed-in-source.)

- **LOW · bash-scripting.md · system_monitor CPU check** — Observed: on a standard Linux runner the
  CPU-usage parse returns `0%` (parse miss), so the CPU threshold never triggers. *Fix:* use a more
  portable CPU read (e.g. `/proc/stat` delta) or note the fragility.

- **LOW · django-and-git.md · `python` vs `python3`** — Observed: Step 1 uses `python -m venv` /
  `pip install django`; many Linux systems only ship `python3`. I substituted `python3` to run it.
  *Fix:* prefer `python3`, or add a note.

- **LOW · jekyll-mermaid-integration.md · relative prerequisite links** — Observed (quoted):
  prerequisites link `../0000/hello-noob.md` and `../0010/bash-scripting.md` (relative `.md` paths).
  Rubric §11 asks for canonical permalinks in published content. *Fix:* use `/quests/0000/hello-noob/` etc.

**No blocking issues** were found in the nine `0010/` quests' *runnable* content — every command I
executed there worked (the one failure was django-and-git, which lives in `tools/`).

## 🔗 Chain Continuity

- **The slice is not one learning path — it's two, merged by level number.** Quests 1–5 + 9 are the
  "Tools Collection" (a Git → commits → changelogs → Actions → AI five-chapter arc, plus a Django
  setup). Quests 6, 7, 10, 11 are the actual "Terminal Mastery Path" (fonts → zsh → gum → bash).
  Quests 12–14 are Jekyll/AI craft quests. Quests 15–16 are the **Contributor Path** ("Identity &
  Recognition"), whose required prerequisite `/quests/0001/forge-your-character/` is **outside this
  slice**. A learner told "play system-engineer level 0010" would bounce between four unrelated
  storylines.

- **Ordering within the Tools arc is broken by presentation.** The chapters clearly assume the order
  Branches → Commits → Changelogs → Actions → AI (each opens "You've mastered X, now Y"), but the
  planner orders them alphabetically (action-triggers *first*, though it's "Chapter 4"). There are no
  `quest_dependencies` linking them, so nothing enforces the intended sequence.

- **Good local continuity in the Terminal Mastery sub-chain.** `oh-my-zsh` correctly lists
  `nerd-font-enchantment` as recommended and `bash-scripting` as an unlock; `nerd-font` → `oh-my-zsh`
  → `bash-scripting` is a coherent, well-linked progression, and `terminal-artificer` sensibly
  requires terminal + scripting basics. This is what the whole level *should* feel like.

- **Prerequisite gaps a beginner would hit:** `oh-my-zsh` and `terminal-artificer` assume a Unix shell
  with `zsh`/`gum` installable; `jekyll-mermaid` + both side-quests assume a **running local Jekyll
  site** and a character sheet from a level-0001 quest never introduced in this slice. None of these
  setups is bootstrapped inside the slice — and the one quest that *should* bootstrap the toolkit,
  `planting-seeds` ("Set Up Your Dev Toolkit"), is empty.

## 🧠 Reasoning & Method

- **What I ran vs. reasoned:** I executed real commands in a disposable sandbox for
  `bash-scripting` (data_wizard, system_monitor, hello_wizard syntax), `django-and-git`
  (venv→pip→startproject→git, plus the corrupted line), and `nerd-font-enchantment` (test
  script + display snippets). I ran the deterministic **tier-1 validator** on all 16 files. I
  **reasoned statically** (read the source) about `oh-my-zsh`, `jekyll-mermaid`, both side-quests,
  and the tools prose chapters, and only partially read `prompt-engineering` / `testing-quests`
  (relied on their tier-1 scores of 91.9% / 100% + objective presence). Those are labeled
  accordingly above.

- **Mode / engine limitation (important):** the intended **agentic execute engine**
  (`agentic_validate.py --mode execute`) **could not run** — in this managed agent session the
  child `claude` process it spawns has no OAuth credentials (host-managed auth isn't passed to
  children; `CLAUDE_CODE_OAUTH_TOKEN` is unset), and it failed at quest 1/16 with an auth error.
  Both `execute` and `review` modes use that same child process, so `review` fallback was also
  unavailable. Rather than report nothing, I performed the walkthrough **manually as the learner**
  — which still yields real, sandbox-gathered evidence — and wrote honest `walk-evidence.json` /
  `walk-evidence.md` clearly labeled as manual (not engine output). In a normal CI run with the
  token set, the agentic per-dimension scores should supersede this.

- **Coverage capped/skipped:** No `zsh`, `gum`, `mmdc`, or Nerd Fonts on the runner, and no Jekyll
  build available → the Oh-My-Zsh install, gum interactions, mermaid rendering, and all Liquid/CSS
  side-quest code were not executed. GitHub push/remote steps were skipped (no auth). I did not run
  destructive commands or reach beyond `pip install django` for network.

- **Confidence:** High on the concrete findings (empty planting-seeds, tools/ validator skip,
  django `<end_o` runtime crash, jekyll-mermaid placeholder objectives, the passing bash/django/font
  runs — all directly witnessed). Medium on the quests judged statically. The headline **WARN**
  reflects a level that is half excellent (the `0010/` quests) and half ungated imported prose (the
  `tools/` quests, one of them empty).
