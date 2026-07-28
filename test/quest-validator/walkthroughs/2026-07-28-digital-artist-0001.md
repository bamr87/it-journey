---
title: 'Quest Walkthrough — Digital Artist · Level 0001 (Web Fundamentals)'
date: '2026-07-28T00:00:00.000Z'
character: digital-artist
level: '0001'
theme: Web Fundamentals
tier: Apprentice
quest_count: 5
mode: execute
overall_verdict: warn
session: >-
  Windowed slice (window 2 of 6, offset 5) of the 26-quest level, walked as a
  Digital Artist learner. Machine evidence was pre-sealed by the workflow's
  deterministic execute-engine step (walk-evidence.json / walk-evidence.md) and
  consumed as-is; the engine was NOT re-run. 4 of 5 quests produced sandbox
  verdicts (avg 84.8%); the 5th (Liquid Templating) yielded no machine verdict
  because the engine hit its 40-turn budget — that quest is assessed
  reasoned-only from source, never scored.
---

## 🎯 Session Summary

**Character:** 🎨 Digital Artist (UI/UX) · **Level:** `0001` — Web Fundamentals (🌱 Apprentice) · **Quests walked:** 5 (a rotating window — window 2 of 6 — of the level's 26 quests) · **Mode:** execute (sealed engine evidence) · **Headline verdict:** ⚠️ warn.

This is a strong, coherent Jekyll-building thread. Every quest that the engine actually scored (4 of 5) verified its core technical claims by *running real commands* in a disposable sandbox — Jekyll 4.4.1 scaffolds, builds, serves, baseurl/`relative_url` resolution, `JEKYLL_ENV=production` gating, YAML type-coercion gotchas, and a full Git branch/merge/rebase/conflict cycle all behaved exactly as written. The slice earns **warn** rather than **pass** for two reasons: (1) **GitHub Pages Basics** (79%, warn) carries a real, reproducible `master`-vs-`main` branch-naming bug plus a declared-but-untaught "GitHub Actions Build" objective, and (2) **Liquid Templating** produced **no machine verdict at all** — the execute engine exhausted its 40-turn budget and exited before scoring, so it must be treated as unverified, not as a content failure. The chain itself holds together unusually well: all five quests operate on the same `my-castle` site, so a learner carries one project the whole way through.

## 🗺️ The Journey

Walked in `walk-plan.json` order:

1. ⚠️ **GitHub Pages Basics: Host Your Jekyll Site for Free** — score **79** · Core url/baseurl/CNAME/production-build content verified by real builds; docked for a `git init` → `master` vs. hardcoded `main` mismatch and an untaught secondary objective.
2. ✅ **Jekyll Fundamentals: Build Static Sites with Ruby** — score **83** · Scaffold → serve → build → collections → drafts/livereload → multi-config all ran and worked; the "build with no warnings" validation criterion is factually wrong (default scaffold emits Sass deprecations).
3. ✅ **YAML Configuration: Site Settings Mastery** — score **97** · Best of the slice; every YAML/Jekyll claim (type coercion, parse errors, block scalars, config layering, `strict_front_matter`) held up against real yamllint/PyYAML/Ruby Psych/Jekyll 4.4.1.
4. ✅ **Git Workflow Mastery: Branches, Merging & Team Collaboration** — score **80** · Branch/commit/merge/rebase/conflict/abort/reflog all executed in a real repo; docked for an untaught `git revert` secondary objective and a merge diagram that won't match the fast-forward a learner actually sees.
5. ❌ **Liquid Templating: Dynamic Content for Jekyll Sites** — **no score** · Engine reached max turns (40) and exited 1 before emitting a verdict. Not a demonstrated content defect — **unverified**. Assessed `reasoned`-only from source below.

## 🔬 Evidence

All `passed`/`failed` items below come from commands the sealed execute engine actually ran in the sandbox (quoted/trimmed from `walk-evidence.json` / `walk-evidence.md`). Items I could only judge from the source text are marked `reasoned`.

### 1. GitHub Pages Basics — ran 10/7 runnable snippets (10 passed, 0 failed, 6 reasoned) · overall 79 (warn)
Dimensions: commands_work 4 · content_accuracy 4 · completeness 3 · clarity 4 · structure 4 · safety 5.

- `passed` — Installed Jekyll 4.4.1 + bundler, ran `jekyll new` / `bundle install` / `bundle exec jekyll build` on a fresh site → succeeded (only harmless minima/Sass deprecation warnings).
- `passed` — `bundle exec jekyll build --baseurl "/my-castle"` → generated `_site/index.html` contains `href="/my-castle/assets/main.css"` and `href="/my-castle/about/"`; `relative_url` guidance in Chapter 2 verified correct.
- `passed` — `JEKYLL_ENV=production bundle exec jekyll build` vs. a plain build with `{% if jekyll.environment == "production" %}…{% endif %}` → include emitted only in the production build, exactly as Chapter 4 describes.
- `passed` — `git init && git add . && git commit` and `echo "www.mysite.dev" > CNAME` → both work as written.
- `passed` (the key finding) — On a stock system with no `init.defaultBranch`, `git init` creates **`master`, not `main`** (verified live). The macOS/Windows/Linux paths never rename the branch (`git branch -M main` appears only in the Cloud Realms path), yet the "Enable Pages" step and `gh api … source[branch]=main` hardcode `main`.
- `reasoned` — `gh repo create --push`, `gh api … pages`, DNS A/CNAME records, and the per-OS install/auth commands were validated for syntax (via `--help`, apt-cache policy, a fake-token call returning "no git remotes found" rather than a syntax error) but not executed, since they need real GitHub auth / a registrar.

### 2. Jekyll Fundamentals — ran 9/10 runnable snippets (9 passed, 0 failed, 4 skipped, 3 reasoned) · overall 83 (pass)
Dimensions: commands_work 4 · content_accuracy 4 · completeness 4 · clarity 4 · structure 5 · safety 5.

- `passed` — `gem install jekyll bundler` (via `GEM_HOME=$HOME/.gems`, no sudo) → jekyll 4.4.1 / bundler installed; `jekyll new my-castle` auto-ran `bundle install` and produced a working scaffold.
- `passed` — `bundle exec jekyll serve` printed the exact expected `Server address: http://127.0.0.1:4567/` and `Server running…` lines; `bundle exec jekyll build` produced `_site/index.html`, `_site/404.html`, `_site/about/`, `_site/feed.xml`.
- `passed` — Chapter 3 collection workflow end-to-end: `collections: recipes:{output:true,…}` + `_recipes/bread.md` + `jekyll build --verbose` → `_site/recipes/bread/index.html` with correct title/content.
- `passed` — `jekyll serve --livereload --drafts`, `--config _config.yml,_config_dev.yml`, and `JEKYLL_ENV=production … build` all ran clean.
- **Contradiction found** — The Advanced Challenge asserts "`bundle exec jekyll build` succeeds **with no warnings**"; every default-scaffold build emits ~15 Sass `DEPRECATION WARNING` lines plus a Bundler platform warning. A learner literally cannot satisfy this criterion as written.

### 3. YAML Configuration — ran 17/7 runnable snippets (17 passed, 0 failed, 2 skipped, 0 reasoned) · overall 97 (pass)
Dimensions: commands_work 5 · content_accuracy 5 · completeness 5 · clarity 4 · structure 5 · safety 5.

- `passed` — `yamllint _config.yml` (macOS/Windows/Linux/Docker checks), and every teaching block: core shapes, front matter, full `_config.yml`, `_data/team.yml`, the Liquid loop over `site.data.team`, the Chapter 3 pitfalls block (yes/on booleans, `1.20` float truncation, unquoted colon, leading-zero octal), the plugins block, `_config_dev.yml` override, and `strict_front_matter` — all parsed/behaved as described against real yamllint, PyYAML, Ruby Psych, and a live Jekyll 4.4.1 build.
- `passed` — `bundle exec jekyll serve --config _config.yml,_config_dev.yml` and `JEKYLL_ENV=production bundle exec jekyll build` both ran without error.
- Only nits: the near-universal `missing document-start [document-start]` yamllint warning on the quest's own examples is never mentioned (warning, exit 0), and the Chapter 3 pitfalls block should say it's illustrative bad/good pairs, not one pasteable file.

### 4. Git Workflow Mastery — ran 8/10 runnable snippets (8 passed, 0 failed, 3 skipped, 3 reasoned) · overall 80 (pass)
Dimensions: commands_work 4 · content_accuracy 4 · completeness 3 · clarity 4 · structure 5 · safety 5.

- `passed` — In a real sandbox repo: `git switch -c feature/add-about-page`, add/commit, `git status`, `git log --oneline --graph --all`, `git diff`, `git switch main && git merge`, `git rebase main`, `git fetch && git rebase origin/main`, finish-merge/`rebase --continue`/`merge --abort`/`rebase --abort`, `git restore <file>`, `git reflog` — all executed and behaved as documented; conflict-marker format and rebase history-rewriting independently verified.
- `skipped` — `gh pr create … / gh pr merge --squash --delete-branch` could not run (need a live authenticated GitHub remote).
- `reasoned` — Linux `apt install git gh` + `git config --global …` block and the commit-message good/bad text block judged correct from source, not executed.
- Gap observed: `git revert` is named as a required secondary-objective skill but never appears in the quest body; the Chapter 2 merge diagram shows a merge commit that a learner following the recommended rebase-then-merge flow won't see (Git fast-forwards).

### 5. Liquid Templating — NO MACHINE VERDICT (engine hit 40-turn max) · unverified
`walk-evidence.json` records `verdict_obj: null`, `overall: 0.0`, and `error: "claude exited 1 … terminal_reason: max_turns … Reached maximum number of turns (40)"`, with one `permission_denials` entry (a `curl -sI https://rubygems.org` the sandbox blocked). **No dimension scores, no commands, no snippet counts exist for this quest.** The `❌ / 0` is an engine-budget artifact, not evidence the quest is broken. I read the full source and assess it `reasoned`-only (see Chain Continuity). I did **not** run any Liquid commands myself — I have no auth to run the engine and must not fabricate results.

## 🐞 Issues Found

Every item below is backed by a sandbox command result or an exact quoted line. Grouped by severity. None are blocking for a learner who improvises around them, but the top two are worth a content pass.

- **medium** · GitHub Pages Basics · Chapter 1 platform push instructions · The engine verified `git init` creates `master` on an unconfigured system, while the macOS/Windows/Linux paths and the `gh api … source[branch]=main` call assume `main`. On such a machine the Pages-enable step fails or shows no `main` branch. **Fix:** add `git branch -M main` to all three platform paths (matching the Cloud Realms path).
- **medium** · Jekyll Fundamentals · Advanced Challenge validation criterion · "succeeds with **no warnings**" is false — every default-scaffold build emits Sass deprecation warnings (observed live). **Fix:** reword to "succeeds (Sass deprecation warnings from the default theme are expected)" or add the steps needed to silence them.
- **medium** · Git Workflow Mastery · Secondary Objectives / "Undo Safely" · `git revert` is declared a required skill but never taught anywhere in the body. **Fix:** add a short `git revert <commit>` demonstration, or relabel the objective.
- **low** · GitHub Pages Basics · Chapter 1 vs Chapter 2 ordering · Learners push and enable Pages before Chapter 2 teaches `baseurl`, so the first published site ships with broken CSS. **Fix:** set `baseurl` before the initial push, or note the fix comes next.
- **low** · GitHub Pages Basics · Quest Objectives · The "GitHub Actions Build" secondary objective has no instructional content — only an external link. **Fix:** add a minimal `.github/workflows/jekyll.yml` section or relabel as optional reading.
- **low** · Git Workflow Mastery · Chapter 2 merge diagram · Diagram shows a merge commit, but plain `git merge` fast-forwards after the recommended rebase, so the diagram won't match reality. **Fix:** use `git merge --no-ff` or add a fast-forward note.
- **low** · Jekyll Fundamentals · Chapter 4 · `docker-compose up -d` / `http://localhost:4002` referenced with no `docker-compose.yml` provided; and `remote_theme`/`theme: jekyll-theme-zer0` snippets are never wired into the Gemfile, so a verbatim copy hits a `LoadError`. **Fix:** provide the compose file or drop the reference; show the theme gem/plugin install.
- **low** · YAML Configuration · platform yamllint commands & Chapter 3 pitfalls block · The `missing document-start` warning on the quest's own examples is unmentioned; the pitfalls block reads like one pasteable file but is intentionally-broken illustrative pairs. **Fix:** one-line notes on each.
- **process/low** · Liquid Templating · execute engine · The engine could not score this quest within 40 turns (partly a blocked `curl` to rubygems.org). This is a **coverage gap**, not a quest bug — flagged so a future run re-walks it. **Fix:** re-run with a higher turn budget / pre-warmed gems, or split it.

## 🔗 Chain Continuity

Read in plan order, carrying prior state forward as a learner would:

- **One project carries the whole slice.** `jekyll-fundamentals` creates `my-castle` via `jekyll new my-castle`; `github-pages-basics`, `yaml-configuration`, and `liquid-templating` all `cd my-castle` and build on it, and `git-workflow-mastery` exercises the same repo. This is excellent continuity — a learner never loses their working artifact between quests.
- **Plan order ≠ pedagogical order (windowing artifact).** The dependency frontmatter makes `jekyll-fundamentals` the root (`required_quests: []`, and it unlocks the other three technical quests). Yet this rotating window walks `github-pages-basics` **first**, even though its own frontmatter lists `required_quests: [jekyll-fundamentals]`, which appears **second**. Because this is window 2 of 6 of a 26-quest sweep, a learner doing the full level in intended order would already have `jekyll-fundamentals` behind them, so the real journey is sound — but the *window's* internal ordering is not learner-intuitive on its own. Not a content defect; noted so a maintainer doesn't mistake it for one.
- **A latent cross-quest bug.** `github-pages-basics`' `master`-vs-`main` gap interacts with the chain: a learner who later runs `git-workflow-mastery` on a `master`-named repo (that quest's Linux/Codespaces setup sets `init.defaultBranch main` but the Pages quest never did) can end up with mismatched branch expectations between the two quests. Standardizing on `git branch -M main` in the Pages quest closes the gap for the whole path.
- **`baseurl` is the connective tissue.** `yaml-configuration` (baseurl/config layering), `github-pages-basics` (project-site baseurl), and `liquid-templating` (`relative_url`) all lean on the same baseurl mental model. The engine independently verified `relative_url` resolves against baseurl in the Pages quest, so the three reinforce each other correctly — provided the ordering issue above (baseurl set before publish) is fixed.
- **`liquid-templating` fits the chain by design** (recommended prereq `yaml-configuration` for its `site.data` loops; required `jekyll-fundamentals` for a running site). From source it is well-structured — four chapters (objects/tags/filters → loops/conditionals → includes/layouts → comments/raw/whitespace), each with knowledge checks and tiered challenges, and it correctly `{% raw %}`-wraps its own Liquid examples. I found no defect on read, but **I could not verify any of it in the sandbox**, so I make no `pass`/`fail` claim about it — only that it reads coherently and depends on state the earlier quests establish.

## 🧠 Reasoning & Method

- **What I ran vs. reasoned:** I ran **no** quest commands myself. The machine evidence was pre-computed and sealed by the workflow's deterministic execute-engine step (Claude Code scrubs auth from Bash-tool subprocesses, so I cannot re-run the engine). I consumed `walk-plan.json`, `walk-evidence.json`, and `walk-evidence.md` **as-is** and read all five quest sources to reason about the linked journey. Every `passed`/`failed`/`skipped`/`reasoned` above is quoted or summarized from the sealed evidence; every `reasoned` chain observation is tied to an exact quoted frontmatter/body line.
- **Mode & sandbox:** execute mode, disposable runner sandbox, Ubuntu 24.04 / Ruby 3.2.3 / Jekyll 4.4.1 (per engine findings). Sandbox denied outbound network/localhost (e.g. curl to rubygems.org, localhost serve checks), so network-dependent steps (`gh` auth, PR commands, DNS, live-site verification) are `reasoned`, not `tested` — correctly labeled as such.
- **Coverage & limits (stated honestly):** 4 of 5 quests were machine-scored (avg **84.8%**; snippet coverage 10/7, 9/10, 17/7, 8/10). The **5th quest, Liquid Templating, has zero machine coverage** — the engine hit its 40-turn ceiling and produced no verdict, so it is reported as unverified and assessed reasoned-only. This is the single biggest gap in this session and a future run should re-walk it. This slice is also a **window (2 of 6)** of the 26-quest level, so it is *not* a full-level certification.
- **Confidence:** High for the four scored quests (real commands, consistent findings). Medium for the Liquid Templating static read (well-structured on paper, but unexecuted). The overall **warn** reflects the one real warn-level quest plus the one unverified quest — not a demonstrated content failure.
