---
title: 'Walkthrough — Digital Artist · Level 0001 (Web Fundamentals)'
date: '2026-07-16T00:00:00.000Z'
character: digital-artist
level: '0001'
theme: Web Fundamentals
tier: Apprentice
quest_count: 5
mode: execute
overall_verdict: warn
session:
  window: 1 of 6 (offset 5, size 5)
  level_total_quests: 26
  scored: 3
  engine_errored: 2
  average_score: 83.3
  cost_usd: 2.7973
  evidence: walk-evidence.json (sealed by workflow, consumed as-is)
---

## 🎯 Session Summary

Walked a **5-quest window** (window 1 of 6; the full Level 0001 slice is 26 quests) of the **Digital Artist (UI/UX)** path at level **0001 — Web Fundamentals** as a learner, using the sealed execute-mode evidence the workflow pre-computed. The three quests the engine scored are **technically solid**: every locally-runnable command in GitHub Pages Basics (82), Jekyll Fundamentals (88), and Git Workflow Mastery (80) was actually executed in a disposable Jekyll sandbox and behaved as documented — no broken commands, no unsafe steps. Average score across the scored quests is **83.3%**.

The headline verdict is **WARN, not PASS**, for one honest reason: **2 of the 5 planned quests have no execute evidence at all** — `yaml-configuration` and `liquid-templating` both hit the engine's `max_turns` limit (40) and returned no verdict (`overall: 0.0`, `verdict: "fail"`). That is a **harness/engine exhaustion**, **not** an observed content defect — I did not witness those quests fail, so I refuse to report them as passing *or* as genuinely failing. They are reasoned about statically below and flagged as **uncovered**. A maintainer should treat this slice as 60% machine-verified.

## 🗺️ The Journey

Plan order (as `walk-plan.json` selected — note this window is **not** dependency-sorted; see Chain Continuity):

1. ✅ **GitHub Pages Basics: Host Your Jekyll Site for Free** — **82** · every baseurl /
`relative_url` / `JEKYLL_ENV=production` / `gh api :owner` path ran clean; docked for a stated-but-undelivered "GitHub Actions Build" objective and no plugin-safelist warning.
2. ✅ **Jekyll Fundamentals: Build Static Sites with Ruby** — **88** · strongest quest;
install → `jekyll new` → serve → collections → build all verified live; the one real failure is `remote_theme` silently no-op'ing without the unmentioned `jekyll-remote-theme` plugin.
3. ❌ **YAML Configuration: Site Settings Mastery** — **no verdict** · engine hit
   `max_turns` (40); **no commands recorded**. Reasoned-only below — treat as **uncovered**.
4. ✅ **Git Workflow Mastery: Branches, Merging & Team Collaboration** — **80** · branch/commit/push,
true merge-commit vs rebase, and a hand-built conflict all reproduced exactly; docked for no `gh auth login` step and `git revert` named-but-never-shown.
5. ❌ **Liquid Templating: Dynamic Content for Jekyll Sites** — **no verdict** · engine hit
`max_turns` (40) after a sandbox permission denial on a background `jekyll serve --livereload`; **no commands recorded**. Reasoned-only below — treat as **uncovered**.

## 🔬 Evidence

All command outcomes below come verbatim from the sealed `walk-evidence.json` (execute mode, real sandbox). I ran no engine myself; I read the quest sources and the sealed evidence.

### 1. GitHub Pages Basics — 82 / pass · ran 9/7 runnable snippets (9 passed, 0 failed, 1 skipped, 3 reasoned)
- `git init && git add . && git commit -m "Initial site"` on a real `jekyll new` scaffold → **passed** (7 files committed, exit 0).
- `_config.yml` `url`/`baseurl` + `bundle exec jekyll build --baseurl "/my-castle"` → **passed**: every href in `_site/index.html` correctly prefixed `/my-castle/…`, confirming `relative_url`/baseurl mechanics.
- `JEKYLL_ENV=production bundle exec jekyll build` with `{% if jekyll.environment == "production" %}{% include analytics.html %}{% endif %}` → **passed**: include absent from dev build, present in production build (verified end-to-end with a real `_includes/analytics.html`).
- `gh api -X POST repos/:owner/my-castle/pages …` → **passed**: `:owner` placeholder verified to resolve to the repo owner (401 on fake token, i.e. syntactically/semantically correct).
- `gh repo create --public --source=. --push` flags all validated against `--help`.
- **skipped**: Windows PowerShell block (no PowerShell on Linux sandbox). **reasoned**: macOS `brew install gh`, the DNS A/CNAME tables. `gh auth login` / actual publish → untested (needs real GitHub credentials — inherent, not a defect).

### 2. Jekyll Fundamentals — 88 / pass · ran 11/10 runnable snippets (10 passed, **1 failed**, 4 skipped, 3 reasoned)
- Linux `gem install jekyll bundler` (GEM_HOME, no sudo) → **passed** ("Successfully installed jekyll-4.4.1", "bundler-4.0.16").
- `jekyll new my-castle` + `bundle exec jekyll serve` → **passed**: HTTP 200 via Ruby Net::HTTP with the expected Jekyll SEO title tag.
- `collections: recipes:` + `mkdir _recipes` + `_recipes/bread.md` + `bundle exec jekyll build --verbose` → **passed**: wrote `_site/recipes/bread/index.html`.
- `bundle exec jekyll serve --livereload --drafts` → **passed**: GET `/recipes/bread/` → 200, `<title>Hearth Bread | …</title>`.
- `bundle exec jekyll serve --config _config.yml,_config_dev.yml` → **passed**: dev override title won, confirming merge order.
- `remote_theme: "bamr87/zer0-mistakes"` → **FAILED**: built without error but **silently ignored** the theme — vanilla `jekyll` gem lacks `jekyll-remote-theme`; no warning, a silent no-op the quest never caveats.
- **skipped**: macOS/Windows install paths, `docker run … jekyll/jekyll:4`, and `docker-compose up -d` (the latter references a compose file **never defined anywhere in the quest**).

### 3. YAML Configuration — **NO EVIDENCE** (engine `max_turns`, 40)
- `verdict_obj: null`, `overall: 0.0`, **zero commands recorded**. The engine child process reached its turn limit before emitting a verdict. **Nothing was witnessed** — no pass, no fail. See Issues for the reasoned-only static read.

### 4. Git Workflow Mastery — 80 / pass · ran 7/10 runnable snippets (7 passed, 0 failed, 3 skipped, 2 reasoned)
- `git switch -c feature/… / git add / git commit / git push -u origin …` against a local origin → **passed** (tracking set up as documented).
- `git status` / `git log --oneline --graph --all` / `git diff` → **passed** (output matched the quest's descriptions).
- Merge vs rebase demo → **passed**: on a genuinely diverged history, `git merge` made a true merge commit and `git rebase main` replayed the commit with a new hash — reproduced the quest's ASCII diagrams exactly. (Engine notes a non-diverged history fast-forwards silently, which the diagram doesn't caveat.)
- Hand-built conflict → **passed**: markers matched the quest's `<<<<<<< / ======= / >>>>>>>` format exactly; `git merge --abort` / `git rebase --continue` / `--abort` all restored state cleanly.
- **skipped**: `gh pr create` / `gh pr merge --squash --delete-branch` — `gh auth status` showed "not logged into any GitHub hosts"; flags are valid, behavior judged by docs, not executed. macOS/Windows installs skipped (wrong OS); Linux `apt install gh` **reasoned** (confirmed available via `apt-cache policy gh`).

### 5. Liquid Templating — **NO EVIDENCE** (engine `max_turns`, 40)
- `verdict_obj: null`, `overall: 0.0`, **zero commands recorded**. Recorded `permission_denials`: a backgrounded `bundle exec jekyll serve --livereload … && curl …` was denied by the sandbox before the run exhausted its turns. **Nothing was witnessed.** Reasoned-only static read is in Issues.

## 🐞 Issues Found

Every item below is either engine-observed (cites a recorded command result) or, where marked **reasoned**, a static read of the quest source with the quoted line — never invented.

**High**
- **[GitHub Pages Basics] · Chapter 1 / secondary objective** — *observed (content_accuracy/completeness)*: the objective "**GitHub Actions Build** — Understand how Pages can build Jekyll automatically" (line 114) is listed but **no chapter ever explains the Settings → Pages → Source: GitHub Actions path**; only "Deploy from a branch" is covered. Fix: add a short GitHub Actions section or drop the objective/mastery indicator.
- **[Git Workflow Mastery] · Chapter 2 / System Requirements** — *observed*: `gh auth status` returned "not logged into any GitHub hosts", so `gh pr create` / `gh pr merge` cannot run as written; the quest never instructs `gh auth login`. Fix: add an explicit `gh auth login` step before the PR snippet.
- **[Jekyll Fundamentals] · Chapter 4 — `docker-compose up -d`** — *observed (skipped as unrunnable)*: line ~452 `docker-compose up -d` / port 4002 references a `docker-compose.yml` that is **never defined anywhere in the quest**. Fix: provide the compose file or replace with the already-shown `docker run … jekyll/jekyll:4` pattern.

**Medium**
- **[Jekyll Fundamentals] · Chapter 4 — `remote_theme`** — *observed (the one FAILED command)*: `remote_theme: "bamr87/zer0-mistakes"` builds but silently applies nothing without the `jekyll-remote-theme` plugin (absent from the vanilla `jekyll` gem used all quest). Fix: note the plugin dependency, or the learner sees a no-op with no error.
- **[GitHub Pages Basics] · Content accuracy** — *observed*: no mention of the `github-pages` gem pin / plugin safelist for the "Deploy from a branch" build — the single most common "builds locally, breaks on Pages" cause. Fix: add a short note.
- **[GitHub Pages Basics] · Linux path — `sudo apt install -y gh`** — *reasoned* (line 188): on many stock Debian/Ubuntu images `gh` isn't in default apt repos without first adding GitHub CLI's apt repository; verbatim followers may hit "package not found". Fix: add the repo-add caveat.
- **[Git Workflow Mastery] · Chapter 1 setup** — *observed*: no step wires a real GitHub remote (`git remote add origin …` / `gh repo create`) before `git push -u origin feature/…`; Chapter 1 assumes `origin` + tracking already exist. Plausibly deferred to the `/quests/0000/git-basics/` prerequisite, but not called out.
- **[Git Workflow Mastery] · Secondary objective "Undo Safely"** — *observed*: `git revert` is named in the objectives but **no snippet ever demonstrates it** (only `git restore`/`git reflog` get a one-line mention). Fix: add a runnable `git revert <commit>` example.

**Low**
- **[GitHub Pages Basics] · Windows path** — *reasoned* (lines 174-176): PowerShell `;` does not short-circuit on failure like bash `&&`, so a failed `git init` won't stop the chain. Minor note worth adding.
- **[Jekyll Fundamentals] · Chapter 2 diagram** — *observed (reasoned in engine)*: the tree shows `index.md` (line 307) but `jekyll new` scaffolds `index.markdown`/`about.markdown`. Cosmetic; note both extensions.
- **[Jekyll Fundamentals] · Chapter 4 webrick entry** — *reasoned*: Jekyll 4.4+ already declares `webrick` as a runtime dep, so the LoadError is now rare on a fresh `jekyll new`; keep the fix for older setups but note this.
- **[Git Workflow Mastery] · Chapter 2 merge diagram** — *observed*: caveat that `git merge` only produces the "M" commit on a diverged history; a fast-forward-able branch merges with no merge commit, diverging from the diagram.

**Reasoned-only (no execute evidence — quests the engine could not score)**
- **[YAML Configuration] · uncovered** — no engine evidence (max_turns). Static read: the quest is well-structured (syntax → front matter/`_config.yml` → data files/pitfalls → production config) and its Chapter 4 plugin list **does** include `jekyll-remote-theme` (line 415) — which is exactly the plugin whose absence made Jekyll Fundamentals' `remote_theme` no-op. Its commands (`yamllint`, `--config` layering, `strict_front_matter: true`) look runnable but were **not verified this session**. Needs a re-run with a higher turn budget.
- **[Liquid Templating] · uncovered** — no engine evidence (max_turns + a serve-binding permission denial). Static read: Chapter 2's "New" badge snippet uses `{% elsif post.date > site.time | date: "%s" | minus: 604800 %}` — a date-vs-string comparison whose correctness I **could not** verify without running it; a real learner could plausibly hit a type mismatch here. Flag for a targeted re-run.

## 🔗 Chain Continuity

Reasoning about the window as one journey a Digital-Artist learner would actually take:

- **Window order ≠ learning order.** The plan walks **GitHub Pages Basics first**, but
its own frontmatter lists `required_quests: /quests/0001/jekyll-fundamentals/` and its prose opens *"You forged a Jekyll site in the workshop…"* — you cannot host a site you haven't built. The dependency spine is **jekyll-fundamentals → {yaml-configuration, liquid-templating, github-pages-basics} → git-workflow-mastery**. This is expected for a date-rotated **window** (offset 5 of a 26-quest level, not a topological cut), but a learner following this window's *listed* order verbatim would start in the wrong place. Not a content bug — an ordering caveat for anyone reading the window as a syllabus.
- **Shared "my-castle" scaffold holds the chain together.** Every quest assumes the same
`my-castle` Jekyll site from Jekyll Fundamentals (verified: the engine reused one scaffold across quests). Naming and setup are consistent — good continuity once the learner has done Jekyll Fundamentals first.
- **Cross-quest `remote_theme` inconsistency.** Jekyll Fundamentals Ch4 introduces
`remote_theme: "bamr87/zer0-mistakes"` **without** mentioning the `jekyll-remote-theme` plugin (verified: silent no-op). The very plugin that fixes it only appears later, in **YAML Configuration** Ch4's plugin list. A learner hitting the silent failure in quest 2 gets no pointer forward; the two quests should cross-reference. Evidence: the one FAILED command in the whole session.
- **Unstated GitHub-account/auth prerequisite spans two quests.** Both GitHub Pages Basics
and Git Workflow Mastery assume an authenticated GitHub session and an existing `origin` remote, yet neither walks `gh auth login` or remote creation (both defer implicitly to `/quests/0000/git-basics/`, which is *recommended* but **outside this window**). Evidence: `gh auth status` → "not logged in"; `gh pr` and publish steps were the exact commands the engine could not complete. A learner who jumped straight into level 0001 gets stuck at the "last mile" of both quests.
- **Concepts reinforce well where they overlap.** `baseurl`/`relative_url`,
`JEKYLL_ENV=production`, and `_config.yml,_config_dev.yml` layering recur across Jekyll Fundamentals, YAML Configuration, and GitHub Pages Basics with consistent syntax — good spaced repetition for the tier.
- **Chain coverage is only 60% machine-verified.** Two of the five links (YAML, Liquid) have
no execute evidence, so I cannot certify that quest 2→3 or 4→5 hand-offs actually work end to end this session. The dependency *declarations* are coherent; the *executed* proof is partial.

## 🧠 Reasoning & Method

- **What I ran vs. reasoned:** I ran **no** engine myself. The evidence is the sealed
`walk-evidence.json` / `walk-evidence.md` the workflow pre-computed in a deterministic execute-mode step (the engine's child `claude` processes can't authenticate from an agent's Bash tool). I consumed those files **as-is**, then read all five quest sources in plan order and reasoned about the linked journey. Every "passed"/"failed" above is quoted from the sealed evidence; everything I judged from source alone is marked **reasoned**.
- **Mode:** `execute` (disposable sandbox), as recorded in the evidence. Not review-only,
  not `--mock`.
- **Coverage limits (stated plainly):**
  - **2 of 5 quests have no evidence** — `yaml-configuration` and `liquid-templating` both
    exhausted the engine's `max_turns` (40) and returned `verdict_obj: null` / `overall: 0.0`.
    Their `verdict: "fail"` is an **engine-exhaustion artifact, not a witnessed content
    failure.** I did not fabricate scores for them; they are reasoned-only and flagged
    **uncovered**. They should be re-run with a higher turn budget (or fewer snippets per
    turn) before this slice is called complete.
  - The `average` (83.3) and `pass 3 / fail 2` counts in the evidence are computed only over
    the scored quests; do not read the "2 fail" as two bad quests.
  - Publish/auth "last-mile" steps (`gh auth login`, `gh repo create --push`, live Pages
    publish, custom-domain DNS) are inherently unrunnable in a credential-less sandbox and
    were correctly skipped — not counted against the quests.
  - Windows/macOS platform blocks were skipped on the Linux sandbox (reasoned, not tested).
- **Confidence:** **High** for the three scored quests — their commands were genuinely
executed and the recommendations align with the quest rubric's dimensions. **Low** for YAML Configuration and Liquid Templating — no evidence gathered; treat my notes there as hypotheses to verify, not findings.
- **Scope discipline:** one slice, one report. No quest content was edited; no other
  character/level was touched. The caller handles git.
