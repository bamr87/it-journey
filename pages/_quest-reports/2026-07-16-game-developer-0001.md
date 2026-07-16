---
title: Game Developer · L0001 · 2026-07-16
description: Quest-perfection walkthrough of the Web Fundamentals slice game-developer/0001 on 2026-07-16,
  engine verdict warn. An evidence-based, learner's-eye…
date: '2026-07-16T13:51:30.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Game Developer
tags:
- game-developer
- level-0001
- walkthrough
- quest-perfection
- warn
- web-fundamentals
render_with_liquid: false
excerpt: 'Game Developer · Level 0001 — Web Fundamentals: an evidence-based quest-perfection walkthrough
  from 2026-07-16.'
slice: game-developer/0001
character: game-developer
level: '0001'
theme: Web Fundamentals
tier: Apprentice
verdict: warn
quest_count: 5
walk_date: '2026-07-16'
run_url: https://github.com/bamr87/it-journey/actions/runs/29494904212
source_report: test/quest-validator/walkthroughs/2026-07-16-game-developer-0001.md
---

> **Slice** `game-developer/0001` · **Level** 0001 (Web Fundamentals) · **Apprentice tier** · **Engine verdict** ⚠️ warn · **Walked** 2026-07-16
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29494904212) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-16-game-developer-0001.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-16-game-developer-0001.md)

---

## 🎯 Session Summary

I walked a **5-quest window** of the **Game Developer → Level 0001 (Web
Fundamentals, 🌱 Apprentice)** path as a learner would: publish a site (GitHub
Pages), build the site engine (Jekyll), configure it (YAML), version it (Git),
and template it (Liquid). This is window **1 of 6** over the level's full 26
quests, so the ledger will sweep the rest across later runs.

**Headline verdict: ⚠️ warn.** The slice is fundamentally sound — the *core*
technical spine of every quest was executed for real in a sandboxed Jekyll 4.4.1
site and behaved as documented, and the middle of the chain (**YAML Configuration
scored a perfect 100**) is exemplary. But three of five quests carry a **single
concrete copy-paste bug each** that a beginner following the text literally will
hit: an unsupported `:owner` placeholder in a `gh api` call (GitHub Pages), a
broken dev/prod theme-config example that throws a fatal `MissingDependencyException`
(Jekyll), and an invalid-Liquid `elsif` with a filter in the condition that warns
on every build (Liquid). None are structural or unsafe; each is a small, precise
fix that a content pass can land. Average **79.2%**, `2 pass / 3 warn / 0 fail`.

## 🗺️ The Journey

Walked in plan order (`walk-plan.json`, dependency-sorted window):

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ⚠️ | GitHub Pages Basics: Host Your Jekyll Site for Free | 74 | Baseurl/production mechanics verified live; `gh api :owner` placeholder and a never-renamed `master`→`main` branch will trip a literal follower. |
| 2 | ⚠️ | Jekyll Fundamentals: Build Static Sites with Ruby | 68 | Install→scaffold→serve→collections→build all run clean; the Chapter 4 dev/prod theme example is broken as written (uninstalled gem). |
| 3 | ✅ | YAML Configuration: Site Settings Mastery | 100 | Flawless — every runnable snippet, including all 5 pitfalls and a real build, executed exactly as described. |
| 4 | ✅ | Git Workflow Mastery: Branches, Merging & Team Collaboration | 83 | Branch/commit/rebase/conflict all reproduced faithfully; `git revert` is a named objective but never taught. |
| 5 | ⚠️ | Liquid Templating: Dynamic Content for Jekyll Sites | 71 | 14/15 snippets accurate; the flagship Chapter 2 badge `elsif` is invalid Liquid (filter inside condition) and warns on every build. |

## 🔬 Evidence

All outcomes below come from the sealed execute-engine evidence
(`walk-evidence.json` / `walk-evidence.md`) — commands the engine actually ran in
a disposable sandbox against a real Jekyll 4.4.1 site. I did not re-run the engine
(its child processes cannot authenticate from the agent Bash tool); I read each
quest source and cross-checked the findings against the text.

### 1 · GitHub Pages Basics — ⚠️ 74 · ran 7/7 runnable (1 ✗), 3 reasoned, 4 skipped
- **passed** — `bundle exec jekyll build --baseurl "/my-castle"` produced
  `href="/my-castle/assets/main.css"` and `/my-castle/`-prefixed canonical URLs,
  confirming the Chapter 2 baseurl/`relative_url` claims.
- **passed** — `bundle exec jekyll serve --baseurl "/my-castle"` printed
  `Server address: http://127.0.0.1:4000/my-castle/` (matches the quest text).
- **passed** — `JEKYLL_ENV=production bundle exec jekyll build` ran clean, produced `_site/`.
- **passed** — `git init && git add . && git commit -m "Initial site"` ran standalone.
- **failed** — `gh api -X POST repos/:owner/my-castle/pages ...` (lines 146-147):
  `gh api --help` supports only `{owner}`/`{repo}`/`{branch}` placeholders; the
  Rails-style `:owner` is sent literally and the call fails.
- **skipped/reasoned** — `gh repo create ... --push` and the `gh api` Pages-enable
  call require real GitHub auth + external repo mutation; correctly out of sandbox
  scope (so the quest's most consequential steps are unverifiable by any QA pass).

### 2 · Jekyll Fundamentals — ⚠️ 68 · ran 13/10 runnable (1 ✗), 3 reasoned, 5 skipped
- **passed** — full Linux path end-to-end: `gem install jekyll bundler`
  (jekyll 4.4.1, bundler 4.0.16) → `jekyll new my-castle` → `bundle exec jekyll serve`.
- **passed** — Chapter 3 collections walkthrough verbatim: `collections: recipes`
  in `_config.yml` + `_recipes/bread.md` rendered at the documented permalink.
- **passed** — `bundle exec jekyll serve --livereload --drafts` and
  `JEKYLL_ENV=production bundle exec jekyll build` both ran clean.
- **failed** — Chapter 4 dev/prod config: `theme: "jekyll-theme-zer0"` in
  `_config_dev.yml` merged via `--config _config.yml,_config_dev.yml` throws
  `MissingDependencyException` — the theme gem is never installed.
- **reasoned** — `echo "_site/" >> .gitignore` runs but is redundant; `jekyll new`
  already seeds `.gitignore`. `docker-compose up -d` has no accompanying compose file.

### 3 · YAML Configuration — ✅ 100 · ran 14/7 runnable, 0 failed, 2 skipped
- **passed** — core shapes, `about.md` front matter, and the practical
  `_config.yml` all parsed exactly as claimed; `_config.yml` fed to a real
  `jekyll build` (4.4.1) built with no errors.
- **passed** — `_data/team.yml` + Liquid loop rendered `<p>Ada Lovelace - Architect</p>`
  and `<p>Grace Hopper - Compiler Smith</p>` exactly.
- **passed** — all 5 pitfalls reproduced bit-for-bit: `yes`→True, `on`→True,
  `1.20`→1.2, `01234`→668 (octal), and the colon-in-value quoting case.
- **passed** — `_config_dev.yml` layering order, `strict_front_matter: true`
  fail-fast, `yamllint`, and the `cytopia/yamllint` Docker lint all verified.
- **skipped** — `brew install yamllint` / `apt install yamllint` (no Homebrew,
  no sudo/apt in sandbox); standard, well-known commands — reasoned, not run.

### 4 · Git Workflow Mastery — ✅ 83 · ran 7/10 runnable, 3 reasoned, 4 skipped
- **passed** — `git switch -c`, `add`, `commit`, `push -u`, `status`,
  `log --oneline --graph --all`, `diff`, `merge`, `fetch`, `rebase`,
  `rebase --continue`, `merge --abort`, `restore`, `reflog` all ran as documented
  against a bare `origin`.
- **passed** — rebase rewrote the feature commit hash (c348d05 → b9865cd),
  confirming the "rewrites history" claim; conflict scenario produced the exact
  `<<<<<<< / ======= / >>>>>>>` markers the quest shows.
- **reasoned** — the Chapter 2 `git merge` example captioned "adds a merge commit"
  actually fast-forwarded in the sandbox (no divergent main commits) — diagram
  omits the fast-forward case.
- **skipped** — `gh pr create` / `gh pr merge --squash --delete-branch` need an
  authenticated remote (`gh auth status` → not logged in); inherent QA limit.

### 5 · Liquid Templating — ⚠️ 71 · ran 13/4 runnable (1 ✗), 1 reasoned, 1 skipped
- **passed** — Chapters 1/3/4 snippets reproduced under Jekyll 4.4.1:
  `{​{ greeting | upcase }​}`→`HI`, the capitalize/replace chain, `forloop.index`,
  `sort`+`reversed`, `_data/navigation.yml` loop, parameterized
  `{​% include card.html title=... %​}`, layout wrapping, `comment`, `raw`.
- **passed** — all 6 external doc links returned HTTP 200.
- **failed** — Chapter 2 flagship badge logic
  `{​% elsif post.date > site.time | date: "%s" | minus: 604800 %​}` throws
  `Liquid syntax error: Expected end_of_string but found pipe` on every build;
  filters are not allowed inside `if`/`elsif` conditions, so the "New" badge date
  comparison never runs.
- **reasoned** — the `forloop.first`/`unless` comma-suppression example is
  functionally correct but the inline comment implies a single clean line that a
  learner won't see without whitespace-control dashes.

> Verbatim engine roll-up: **5 quests · ✅ 2 pass · ⚠️ 3 warn · ❌ 0 fail · avg 79.2% · ~$4.8117** (from `walk-evidence.md`).

## 🐞 Issues Found

Concrete, evidenced problems only. Every item cites a command result from the
sealed sandbox run or an exact line in the quest source. These are for a content
pass / human — this session makes **no** content edits.

**HIGH**
- **high** · Jekyll Fundamentals · Chapter 4 "One Repo, Two Configs" · *observed:*
  merging `_config_dev.yml` (which sets `theme: "jekyll-theme-zer0"`) via
  `--config _config.yml,_config_dev.yml` throws a fatal `MissingDependencyException`
  because the theme gem is never installed. · *fix:* add the install/Gemfile step
  (`gem install jekyll-theme-zer0` + `jekyll-remote-theme`) before the example, or
  swap to an already-installed theme (e.g. `minima`) so the merged config runs.
- **high** · Liquid Templating · Chapter 2 "Looping and Branching" ·
  `{​% elsif post.date > site.time | date: "%s" | minus: 604800 %​}` · *observed:*
  invalid Liquid (filter inside condition) → syntax-error warning on every build,
  badge logic never evaluates. · *fix:* precompute with `{​% assign week_ago = ... %​}`
  before the loop and coerce both sides to the same numeric type, then compare
  `{​% elsif post_ts > week_ago %​}` (engine confirmed the corrected pattern builds clean).
- **high** · GitHub Pages Basics · Chapter 1 `gh api` Pages-enable (lines 146-147) ·
  `repos/:owner/my-castle/pages` · *observed:* `gh api` supports only `{owner}`
  placeholders; `:owner` is sent literally and the call fails. · *fix:* use
  `repos/{owner}/my-castle/pages` or tell readers to substitute their real username.

**MEDIUM**
- **medium** · GitHub Pages Basics · macOS/Windows/Linux quick-start paths (lines
  ~150-105) · *observed:* only the Cloud Realms path runs `git branch -M main`; a
  fresh `git init` in the sandbox (git 2.54, no `init.defaultBranch`) creates
  `master`, which collides with the hardcoded `main` in the `gh api` call and the
  Settings → Pages instructions. · *fix:* add `git branch -M main` to every OS path.
- **medium** · GitHub Pages Basics · Secondary objective "GitHub Actions Build"
  (line 24/114) · *observed:* listed as an objective but never taught in the body —
  no workflow YAML, only an external link. · *fix:* add a minimal Actions-Pages
  workflow example or downgrade the objective.
- **medium** · Git Workflow Mastery · Secondary objective "Undo Safely" · *observed:*
  `git revert` is a named learning objective but is never explained, demonstrated,
  or mentioned again anywhere in the body (unlike `restore`/`reflog`, which at least
  get a warning-callout mention). · *fix:* add a short worked `git revert` example.
- **medium** · Jekyll Fundamentals · Chapter 4 · *observed:* a `docker-compose up -d`
  line with no accompanying `docker-compose.yml` — nothing for the learner to run.
  · *fix:* include a minimal compose file or remove the line.
- **medium** · Liquid Templating · Chapter 4 `forloop.first`/`unless` comma example ·
  *observed:* claimed "Output: liquid, jekyll, templating" single line is not what
  renders without whitespace-control dashes. · *fix:* add the `-` dashes or correct
  the inline comment.

**LOW**
- **low** · Jekyll Fundamentals · Chapter 2 anatomy diagram · lists `index.md` but
  `jekyll new` scaffolds `index.markdown`; also implies `_layouts/`/`_includes/`/`_data/`
  exist in a fresh scaffold when they are theme-supplied. · *fix:* correct the names
  and clarify they come from the theme gem.
- **low** · Jekyll Fundamentals · webrick troubleshooting entry is stale — Jekyll
  4.3+ lists webrick as a gemspec dependency, so the error is now rare. · *fix:*
  reframe as an older-Jekyll caveat.
- **low** · Git Workflow Mastery · merge diagram implies `git merge` always creates a
  merge commit, omitting the common fast-forward case (which is what actually
  happened in the sandbox). · *fix:* note the fast-forward case.
- **low** · GitHub Pages Basics · Pre-Launch Checklist "robots.txt and sitemap.xml
  generated" (line 309) — a bare `jekyll new` site generates neither without
  `jekyll-sitemap`. · *fix:* note the plugin requirement. Also mention optional
  IPv6 AAAA records alongside the four A records.
- **low** · Liquid Templating · Intermediate Challenge requires an
  `{​% if item.url == page.url %​}active{​% endif %​}` current-page comparison never
  demonstrated in the lesson; `case`/`when` and `and`/`or`/`contains` are named in
  prose but never shown as code. · *fix:* add short worked examples.

## 🔗 Chain Continuity

Reasoning about these five quests as one linked journey for a Game Developer
apprentice (reasoned from the quest sources + dependency frontmatter; not a
separate execution):

- **Intra-window ordering inverts a hard prerequisite.** The plan presents
  **GitHub Pages Basics first**, but its frontmatter `required_quests` lists
  `/quests/0001/jekyll-fundamentals/` and its body (line 133) assumes "A working
  Jekyll site from the previous quest." Jekyll Fundamentals is quest **#2** in this
  window. A learner walking these five strictly top-to-bottom would try to deploy a
  site they haven't built yet. This is a **window-slice artifact** (the window is
  offset 5 of a 26-quest dependency graph, so intra-window order need not equal
  learner order), but it is worth flagging: as delivered, the first quest's stated
  prerequisite is satisfied only by the second. Confidence: high (frontmatter +
  body text).
- **The Jekyll → YAML → Liquid spine is coherent and well-sequenced.** Jekyll
  Fundamentals establishes install/scaffold/serve/collections; YAML Configuration
  (which `requires` Jekyll) deepens `_config.yml`/`_data` mastery flawlessly; Liquid
  Templating (which `requires` Jekyll, `recommends` YAML) then consumes exactly the
  `_data/*.yml` + front-matter concepts those two taught — the `_data/navigation.yml`
  loop in Liquid lands cleanly because YAML already drilled data files. This is the
  strongest stretch of the chain and reads as a genuine progression.
- **Prerequisite reaching outside the window is satisfied elsewhere.** Git Workflow
  Mastery `requires` `/quests/0000/git-basics/` (an earlier level, not in this
  window) and GitHub Pages `recommends` it too — appropriate for level 0001 and
  presumably covered by an earlier window; nothing in this slice re-teaches basic
  Git, which is correct.
- **A curious `unlocks` edge:** Git Workflow Mastery lists
  `unlocks_quests: /quests/0001/jekyll-fundamentals/`, yet Jekyll Fundamentals has
  no `required_quests` and clearly precedes Git in difficulty (🟢 vs 🟡). Not a
  blocker, but the unlock direction reads backwards; a maintainer may want to sanity
  check the registry edges for this level.
- **No prerequisite *knowledge* gap inside the taught content.** Where a quest
  assumes a skill, an earlier quest in the spine actually teaches it (baseurl builds
  rely on Jekyll build, verified; Liquid data loops rely on YAML data files,
  verified). The friction points are the three copy-paste bugs above, not missing
  conceptual scaffolding.

## 🧠 Reasoning & Method

- **Mode:** `execute` (real commands in a disposable sandbox), consumed from the
  workflow-sealed `walk-evidence.json` / `walk-evidence.md`. I did **not** run the
  engine myself — its child `claude` processes cannot authenticate from the agent's
  Bash tool — and I did not edit the plan or evidence in any way.
- **What was tested vs. reasoned:** All `passed`/`failed` verdicts above come from
  commands the engine actually ran (Jekyll 4.4.1 builds/serves, git operations,
  yamllint, Liquid renders). Items labeled **reasoned/skipped** were *not* executed:
  anything needing real GitHub auth or external mutation (`gh repo create`,
  `gh api` Pages-enable, `gh pr create/merge`) and package installs needing
  Homebrew/sudo (`brew`/`apt install yamllint`). The chain-continuity ordering
  finding is **reasoned** from frontmatter + body text, not a separate run.
- **Coverage honesty:** This is **window 1 of 6** — 5 of the level's 26 quests. The
  remaining 21 are out of scope for this session and will be swept by later ledger
  runs; I did not expand beyond the planned window. Snippet coverage per quest is
  reported inline in §Evidence (e.g. Liquid ran 13, with 4 counted "runnable" and 1
  failing). The single most consequential class of steps in GitHub Pages Basics
  (the actual deploy) is inherently unverifiable in a sandbox and should be read as
  untested, not passing.
- **Confidence:** High on the three HIGH bugs (each reproduced or statically
  unambiguous and cross-checked against the source lines). High on the coherence of
  the Jekyll→YAML→Liquid spine. Medium on the ordering call-out (likely a
  window-slice artifact rather than a curriculum defect). Overall session verdict
  **⚠️ warn**: no failures, no safety issues (`safety = 5` across all five), but
  three warn-level quests each gated by one literal copy-paste bug a beginner will
  hit.
