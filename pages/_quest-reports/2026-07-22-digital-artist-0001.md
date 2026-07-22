---
title: Digital Artist · L0001 · 2026-07-22
description: Quest-perfection walkthrough of the Web Fundamentals slice digital-artist/0001 on 2026-07-22,
  engine verdict warn. An evidence-based, learner's-eye…
date: '2026-07-22T13:37:17.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Digital Artist
tags:
- digital-artist
- level-0001
- walkthrough
- quest-perfection
- warn
- web-fundamentals
render_with_liquid: false
excerpt: 'Digital Artist · Level 0001 — Web Fundamentals: an evidence-based quest-perfection walkthrough
  from 2026-07-22.'
slice: digital-artist/0001
character: digital-artist
level: '0001'
theme: Web Fundamentals
tier: Apprentice
verdict: warn
quest_count: 5
walk_date: '2026-07-22'
run_url: https://github.com/bamr87/it-journey/actions/runs/29916378064
source_report: test/quest-validator/walkthroughs/2026-07-22-digital-artist-0001.md
---

> **Slice** `digital-artist/0001` · **Level** 0001 (Web Fundamentals) · **Apprentice tier** · **Engine verdict** ⚠️ warn · **Walked** 2026-07-22
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29916378064) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-22-digital-artist-0001.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-22-digital-artist-0001.md)

---

## 🎯 Session Summary

I walked the **Digital Artist (🎨 UI/UX)** path through **Level 0001 — Web Fundamentals (Apprentice 🌱)**, the first data-rotated window (1 of 6) of a 26-quest level: five `main_quest`s in the planner's order — **GitHub Pages Basics → Jekyll Fundamentals → YAML Configuration → Git Workflow Mastery → Liquid Templating**. The sealed execute engine produced real, in-sandbox verdicts for only **two** of the five: **Git Workflow Mastery passed at 89** (15/10 runnable snippets executed, every one green) and **GitHub Pages Basics warned at 74** (9 snippets executed, all green, but a reproducible `master`-vs-`main` branch-naming gap). The other **three — Jekyll Fundamentals, YAML Configuration, Liquid Templating — did not complete in the engine**: each child validator exhausted its 40-turn budget (`terminal_reason: max_turns`) mid-walkthrough, so they carry **no machine verdict** and I could only reason about them statically from their source.

Headline verdict: **warn**. Not because the content is weak — the two quests that were actually executed are strong, and the three unscored quests read as well-structured and pedagogically sound — but because **60% of the slice has no sandbox evidence**, and the one high-severity content bug the engine *did* catch (the branch-naming gap in GitHub Pages Basics) would genuinely block a beginner at the "enable Pages" step. A maintainer should treat this run as *two verified quests + three DNFs to re-walk*, not as a clean sweep.

## 🗺️ The Journey

Walked in planner order (note: this window is **not** in pedagogical dependency order — see Chain Continuity):

1. ⚠️ **GitHub Pages Basics: Host Your Jekyll Site for Free** — **74** · Every runnable snippet (url/baseurl, `relative_url`, `JEKYLL_ENV`, CNAME, `gh api` Pages-enable) verified green, but the default branch stays `master` on the macOS/Windows/Linux paths while the Pages-enable step hardcodes `main`.
2. ❌ **Jekyll Fundamentals: Build Static Sites with Ruby** — **DNF (no score)** · Engine hit `max_turns` (40) mid-walkthrough (repeated `jekyll new` / `bundle` / `serve` cycles); reasoned-only below.
3. ❌ **YAML Configuration: Site Settings Mastery** — **DNF (no score)** · Engine hit `max_turns` (40); reasoned-only below.
4. ✅ **Git Workflow Mastery: Branches, Merging & Team Collaboration** — **89** · Branch/commit/push, merge, rebase, conflict create+resolve, abort/continue, restore/revert/reflog all ran exactly as written against a local bare remote. Only `gh pr` flow untestable (no GitHub auth in sandbox).
5. ❌ **Liquid Templating: Dynamic Content for Jekyll Sites** — **DNF (no score)** · Engine hit `max_turns` (40), with a `curl` permission-denial on a localhost fetch; reasoned-only below.

## 🔬 Evidence

Two quests carry real execute-mode evidence; three are DNF and carry none. All numbers below are quoted from `./walk-evidence.json` (sealed by the workflow), never re-derived.

### ⚠️ GitHub Pages Basics — 74 (warn), execute mode · ran **9/7 runnable snippets** (9 passed, 0 failed, 3 skipped, 4 reasoned)
Per-dimension: commands_work 3 · content_accuracy 4 · completeness 3 · clarity 4 · structure 5 · safety 5. weight_covered 1.0.

Commands actually run and their real outcomes:
- **`git init && git add . && git commit` (Ch.1)** — `passed`: "Ran the equivalent sequence in a fresh `jekyll new my-castle` site … succeeded, creating commit 85bf6ca with 7 files." Engine notes the default branch came up **`master`** with git 2.54 (no `init.defaultBranch` set).
- **`git branch -M main` (Cloud Realms path)** — `passed`: "run directly on the sandbox repo (previously on `master`) and correctly renamed it to `main`, confirmed via `git branch`."
- **`gh api -X POST repos/:owner/my-castle/pages -f "source[branch]=main" …`** — `passed`: with `GH_DEBUG=api` + fake token, "`:owner` correctly resolved … JSON body `{"source":{"branch":"main","path":"/"}​}` … failed only with 401 Bad credentials (expected)," confirming correct syntax.
- **`_config.yml` url/baseurl + `bundle exec jekyll build --baseurl "/my-castle"` (Ch.2)** — `passed`: generated `_site/` with correctly prefixed `/my-castle/assets/main.css` and `/my-castle/about/`.
- **`{​{ '/assets/css/style.css' | relative_url }​}` (Ch.2)** — `passed`: rendered `/my-castle/assets/css/style.css` under `--baseurl /my-castle`.
- **`jekyll serve --baseurl "/my-castle"`** — `passed`: log showed `Server address: http://127.0.0.1:4001/my-castle/` (HTTP curl blocked by sandbox, startup+paths confirmed via build instead).
- **CNAME file `www.mysite.dev` (Ch.3)** — `passed`.
- **`JEKYLL_ENV=production bundle exec jekyll build` + `jekyll.environment == "production"` gate (Ch.4)** — `passed`: only the production build rendered the guarded block.
- **`sudo apt install -y gh` (Linux path)** — `reasoned`: gh preinstalled; `apt-cache policy` confirmed available in Ubuntu 24.04 universe; Debian/older Ubuntu may need GitHub's apt repo.
- Skipped (correctly, unsafe/impossible in sandbox): `brew install gh` / `winget install`, `gh auth login`, `gh repo create --push`, Windows PowerShell block.

Engine summary (verbatim): *"its runnable snippets … all verified correctly when actually executed in a real Jekyll site. The main defect is a reproducible one: only the Cloud Realms path renames the default branch to `main`, while the macOS/Windows/Linux paths leave it as `master` (confirmed with git 2.54), which would break the hardcoded `main`-branch Pages-enable step for most readers."*

### ✅ Git Workflow Mastery — 89 (pass), execute mode · ran **15/10 runnable snippets** (15 passed, 0 failed, 4 skipped, 2 reasoned)
Per-dimension: commands_work 5 · content_accuracy 4 · completeness 4 · clarity 4 · structure 5 · safety 5. weight_covered 1.0.

Commands actually run and their real outcomes:
- **Branch Loop** (`git switch main; git pull; git switch -c feature/add-about-page; git add; git commit; git push -u origin …`) — `passed` end-to-end against a local bare `origin`.
- **`git config --global user.name/user.email/init.defaultBranch main`** — `passed` (all three).
- **`git status` / `git log --oneline --graph --all` / `git diff`** — `passed`.
- **MERGE example** — `passed`, tested twice: main unchanged → **fast-forward, no merge commit**; main diverged → real merge commit ("Merge made by the ort strategy").
- **REBASE example** + **`git fetch; git rebase origin/main`** — `passed`, produced linear history as diagrammed.
- **Conflict walkthrough** — `passed`: real conflict generated, markers identical to the quest's (`<<<<<<< HEAD / ======= / >>>>>>>`), hand-resolved, `git add`, `git commit`, clean tree.
- **`git merge --abort`** and **`git rebase --continue`** — `passed`.
- **`git restore` / `git revert --no-edit` / `git reflog`** — `passed`, all three exercised directly.
- Skipped: macOS/Windows install blocks; **`gh pr create`** and **`gh pr merge --squash --delete-branch`** — "`gh auth status` confirmed 'not logged into any GitHub hosts'"; both flags validated via `gh pr merge --help`.

Engine summary (verbatim): *"every single one ran exactly as described. The only untestable piece is the `gh pr create/merge` flow … the one real content nit is that the merge example's ASCII diagram implies a merge commit that a literal walkthrough would actually fast-forward past."*

### ❌ Jekyll Fundamentals / ❌ YAML Configuration / ❌ Liquid Templating — DNF, no machine verdict
All three record `verdict_obj: null`, `overall: 0.0` and an `error` string ending in `"terminal_reason":"max_turns" … "errors":["Reached maximum number of turns (40)"]`. The truncated JSON tails show the validator was still mid-work when cut off — e.g. Jekyll Fundamentals was running `curl … http://127.0.0.1:4000/` and `rm -rf …/my-castle` cleanup; Liquid Templating hit a `permission_denial` on `curl -s http://127.0.0.1:4444/`. **These are engine/harness DNFs (turn-budget exhaustion on long `bundle`/`serve` builds), not evidence that the quests are broken.** No `passed`/`failed`/score exists for any snippet in these three — everything I say about them below is `reasoned` from reading the source, not tested.

## 🐞 Issues Found

Only the first two issues are backed by executed sandbox evidence; the rest are `reasoned` from source or are process/coverage observations and are labelled as such.

- **HIGH · GitHub Pages Basics · Ch.1, macOS/Windows/Linux platform blocks (lines ~150–195) · evidence: executed.** A plain `git init && git add . && git commit` produced a **`master`** branch (verified, git 2.54), but only the Cloud Realms block runs `git branch -M main`, while Ch.1's `gh api … source[branch]=main` snippet and the web-UI instructions both require `main`. A learner on the default macOS/Windows/Linux path pushes `master`, then the Pages-enable step silently fails to find `main`. **Fix:** add `git branch -M main` (or `git init -b main`) to the macOS, Windows, and Linux blocks, or add one sentence telling learners to rename/verify the default branch before enabling Pages.
- **MEDIUM · GitHub Pages Basics · "Secondary Objective: GitHub Actions Build" (line 114) · evidence: reasoned (completeness score 3).** The objective is listed as a badge-relevant skill but the body never teaches it — it appears only as one Resources link ("Understanding GitHub Actions"). A learner cannot check this box from the quest alone. **Fix:** add a short section (minimal Pages-build workflow YAML, or when Pages auto-builds Jekyll vs. needs a workflow), or downgrade/remove the objective.
- **MEDIUM · Git Workflow Mastery · Ch.2 merge diagram (lines ~283–295) · evidence: executed.** The ASCII diagram implies a merge commit `M`, but a learner who did all work only on the feature branch and follows the quest linearly will get **"Fast-forward"** (verified both behaviors). The quest never distinguishes fast-forward from a true merge, which looks like something went wrong. **Fix:** note that `git merge` fast-forwards unless `main` has diverged, and show `--no-ff` (or a diverged-main scenario) if a merge commit is the intent.
- **LOW · Git Workflow Mastery · Secondary "Undo Safely" (line 112) · evidence: executed (tools work) + reasoned (coverage gap).** `git restore` / `git revert` / `git reflog` all ran correctly, but they appear only as a one-line mention in the conflict warning callout — no worked snippet, unlike every other objective. **Fix:** add a short runnable snippet for each.
- **LOW · GitHub Pages Basics · "Verify the Live Site" primary objective (line 109) · evidence: reasoned.** Only implicitly covered via the Novice Challenge validation line. **Fix:** add an explicit step on finding the published URL / checking the Actions build status.
- **LOW · GitHub Pages Basics & YAML Configuration & Git Workflow Mastery · Linux `apt install` blocks · evidence: reasoned.** `sudo apt install -y gh` (and `yamllint`) works on Ubuntu 24.04 (confirmed for `gh`) but is not guaranteed on Debian/older Ubuntu without extra repos. **Fix:** link GitHub's official apt-repo setup for `gh`.
- **LOW · Liquid Templating · Ch.2, line ~266 · evidence: reasoned (NOT executed — quest DNF'd).** The "New" badge uses `{​% raw %​}{​% elsif post.date > site.time | date: "%s" | minus: 604800 %​}{​% endraw %​}`, comparing a date object to a string of epoch seconds. This is fragile Liquid (type-mismatched comparison) and may not behave as implied. **I did not run this** — flag for a content pass to verify against a real build.
- **LOW · Jekyll Fundamentals · Ch.4, lines ~429–453 · evidence: reasoned (NOT executed — quest DNF'd).** Ch.4 introduces `remote_theme: "bamr87/zer0-mistakes"`, a `_config_dev.yml` with `theme: "jekyll-theme-zer0"`, and `docker-compose up -d` — but `jekyll new` scaffolds the Minima theme and no compose file, so a beginner following literally has none of these artifacts. They read as repo-specific illustrations rather than steps the learner can run. **Fix:** label them as "this repo's setup" examples or provide the missing scaffolding.
- **PROCESS/HIGH (coverage, not content) · Jekyll Fundamentals, YAML Configuration, Liquid Templating · evidence: the sealed engine output.** 3 of 5 planned quests DNF'd on the engine's 40-turn ceiling and have **no** machine verdict. **Fix (for the harness, not the content):** raise `--max-turns` for build-heavy Jekyll quests or split their walkthrough so the `bundle install` + `serve` + `curl` loop fits the budget; re-walk this window before the ledger certifies the level.

## 🔗 Chain Continuity

Reading the five as one learner's journey surfaced a real ordering problem and some genuinely good linkage:

- **The walked order is not the dependency order — and it exposes the branch bug.** The planner's window runs **GitHub Pages Basics first, Jekyll Fundamentals second**, yet GitHub Pages Basics lists `required_quests: [/quests/0001/jekyll-fundamentals/]` and its prerequisites literally say *"A working Jekyll site from the previous quest."* A learner walking this window top-to-bottom is asked to publish a Jekyll site before the slice has taught them to build one. This is a **windowing artifact** (the ledger sweeps 26 quests across 6 windows, not a single dependency-sorted path), but worth calling out: the honest pedagogical root is **Jekyll Fundamentals** (`required_quests: []`), which unlocks the other three main quests.
- **The `master`/`main` gap is a cross-quest continuity failure, not just a local bug.** The fix for GitHub Pages Basics' HIGH issue — `git config --global init.defaultBranch main` — **is taught, but in Git Workflow Mastery** (verified running green in the sandbox). In the intended chain GitHub Pages Basics *unlocks* Git Workflow Mastery, so the learner meets the `master` default (and the broken Pages-enable) **before** the quest that teaches the one-time config that would have prevented it. Either quest could close the loop with a single line.
- **Where the chain holds together well (reasoned):** Jekyll Fundamentals establishes the `my-castle` site, the `recipes` collection, `_config.yml`, and `_config_dev.yml`; **YAML Configuration** reuses exactly those (`_config.yml`, the `recipes` collection, `_data/team.yml`, `_config_dev.yml`) and deepens them; **Liquid Templating** then consumes the `_data` files YAML Configuration teaches (`site.data.navigation`, looping over `_data/team.yml`). That is a clean, deliberate hand-off: build the site → configure/structure its data → template over that data. Git Workflow Mastery is the odd one out thematically (its own prereq is `git-basics` at level 0000, and it even lists Jekyll Fundamentals as something it *unlocks*), so it reads as a parallel track a learner can take any time rather than a strict link in this line.
- **Prerequisite honesty is generally good.** Every quest's `prerequisites` block names the right prior knowledge; the only under-specified one is Git Workflow Mastery's "A GitHub account," which should say "push access to a real GitHub repo" since `gh pr create/merge` (the untestable core of Ch.2) needs it — flagged by the engine and consistent with what I read.

## 🧠 Reasoning & Method

- **What I ran vs. reasoned about.** I ran **nothing** myself against quest content — this is a CI-sealed run. I consumed `./walk-plan.json` and `./walk-evidence.json`/`.md` **as-is** (per the skill: step 2 was pre-computed and sealed by the workflow because the engine's child `claude` processes can't authenticate from an agent's Bash tool). I then **Read all five quest sources** in plan order to do the linked-journey pass. Every `passed`/`failed`/score above is quoted from the sealed evidence; every judgment I made from source alone is labelled **reasoned**.
- **Mode & sandbox.** `execute` mode, disposable runner sandbox. Real machine evidence covers **2 of 5** quests (GitHub Pages Basics, Git Workflow Mastery). The engine reported `mock: false` for both, total cost ~$1.81 across the run.
- **Coverage I did NOT get (stated plainly).** **Three of five quests (Jekyll Fundamentals, YAML Configuration, Liquid Templating) DNF'd** on the validator's 40-turn ceiling and have **no** score, no per-dimension marks, and no snippet pass/fail. I did not (and could not, without auth) re-run the engine, and I did not substitute numbers for them — the tally's `overall: 0.0` / `verdict: fail` for those three is a **DNF, not a quality judgment**, and I've treated it that way throughout. Additionally, within the two scored quests, network-dependent and auth-dependent steps were correctly skipped: `gh auth login`, `gh repo create --push`, `gh pr create/merge`, DNS changes, `brew`/`winget` installs, and a couple of localhost `curl`s blocked by sandbox permissions.
- **Confidence.** **High** for the two executed quests — the evidence is detailed, the commands map to real snippets, and the branch-naming bug is reproducible and independently plausible from my own read of Ch.1. **Low** for the three DNF quests — my notes on them are source-only inferences and must not be read as verified; they need a re-walk with a larger turn budget before the level can be certified.
- **Bottom line for a maintainer:** ship the GitHub Pages Basics `master`/`main` fix (HIGH), consider the merge/fast-forward clarification in Git Workflow Mastery (MEDIUM), and **re-walk the three DNF quests** with a raised `--max-turns` before this window counts toward a `perfect` level in the ledger. One slice, one report — no content was modified; git is the caller's job.
