---
title: Game Developer · L0001 · 2026-08-27
description: Quest-perfection walkthrough of the Web Fundamentals slice game-developer/0001 on 2026-08-27,
  engine verdict warn (avg 81.8%). An evidence-based…
date: '2026-08-27T00:00:00.000Z'
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
  from 2026-08-27.'
slice: game-developer/0001
character: game-developer
level: '0001'
theme: Web Fundamentals
tier: Apprentice
verdict: warn
quest_count: 5
engine_average: 81.8
walk_date: '2026-08-27'
run_url: https://github.com/bamr87/it-journey/actions/runs/33083807177
source_report: test/quest-validator/walkthroughs/2026-08-27-game-developer-0001.md
---

> **Slice** `game-developer/0001` · **Level** 0001 (Web Fundamentals) · **Apprentice tier** · **Engine verdict** ⚠️ warn (avg 81.8%) · **Walked** 2026-08-27
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/33083807177) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-08-27-game-developer-0001.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-08-27-game-developer-0001.md)

---

## 🎯 Session Summary

I walked **window 2 of 6** of the **Game Developer → Level 0001 "Web Fundamentals" (Apprentice 🌱)** path — 5 of the level's 26 quests, in the planner's dependency-sorted order — backed by the workflow's sealed execute-mode engine evidence (real commands run in a disposable sandbox, not model assertions): *GitHub Pages Basics*, *Jekyll Fundamentals*, *YAML Configuration*, *Git Workflow Mastery*, and *Liquid Templating*.

**Headline verdict: WARN**, avg **81.8%** (4 pass / 1 warn / 0 fail). Every quest's core hands-on material was actually run against real tooling (Jekyll 4.4.1, Liquid, yamllint, a live `gh`/`git` repo simulation) and worked largely as documented — *Git Workflow Mastery* (92) is the standout, with the full branch/merge/rebase/conflict lifecycle verified live. But I downgrade the session to WARN for two reasons a maintainer should act on: (1) *Liquid Templating* scored 71 with **two confirmed, verbatim-reproducible broken code snippets** (a genuine Liquid syntax error and a mis-claimed output), and (2) my own read of the five quests' `quest_dependencies` frontmatter against `_data/quests/network.yml` found that **this exact five-quest window is one single dependency cycle** — the planner could not topologically sort it and fell back to difficulty+alphabetical tie-breaking, which is *why* the walk order opens with *GitHub Pages Basics* even though that quest's own frontmatter declares `jekyll-fundamentals` as a hard `required_quests` prerequisite. That's a structural defect in the quest graph, not a quirk of this run.

## 🗺️ The Journey

Walked in planner order (window index 1 of 6; `stats.total_quests` = 26):

| # | Verdict | Quest | Type | Score | One-line takeaway |
|---|:--:|---|---|--:|---|
| 1 | ✅ | GitHub Pages Basics: Host Your Jekyll Site for Free | main | 83 | url/baseurl and `relative_url` verified live; the macOS/Windows/Linux paths never rename the default branch to `main` before the Pages-enable step assumes it. |
| 2 | ✅ | Jekyll Fundamentals: Build Static Sites with Ruby | main | 83 | Scaffold→serve→collections→build loop worked end-to-end; Chapter 4's `docker-compose up -d` fails because no compose file is ever shown. |
| 3 | ✅ | YAML Configuration: Site Settings Mastery | main | 80 | Every YAML/yamllint claim verified; the Chapter 3 Liquid sample is wrapped in `{​% raw %​}` and is a no-op if copied as shown. |
| 4 | ✅ | Git Workflow Mastery: Branches, Merging & Team Collaboration | main | 92 | Full branch/PR/merge/rebase/conflict cycle verified live; Chapter 2's merge diagram doesn't match the quest's own fast-forwarding walkthrough sequence. |
| 5 | ⚠️ | Liquid Templating: Dynamic Content for Jekyll Sites | main | 71 | Most Liquid constructs verified correct, but the Ch.2 "New badge" `elsif` and the Ch.4 forloop/whitespace example are both confirmed broken as written. |

Avg **81.8%** · 4 pass / 1 warn · engine cost ≈ $4.32 · engine wall time ≈ 1,062s across 108 turns.

## 🔬 Evidence

All outcomes below are commands the execute engine actually ran in its disposable sandbox, quoted/trimmed from the sealed `walk-evidence.json`.

### 1. GitHub Pages Basics — ✅ 83 (13 available, 7 runnable ran / 7 passed / 4 skipped / 4 reasoned)
- Dimensions: commands_work 4, content_accuracy 4, completeness 4, clarity 4, structure 5, safety 5.
- `git init && git add . && git commit -m "Initial site"` ran cleanly against a real `jekyll new my-castle` scaffold; `_config.yml` `url`/`baseurl` and the `relative_url` Liquid filter were built with real Jekyll 4.4.1 and produced exactly `/my-castle/assets/css/style.css` (vs. a hard-coded path that would 404).
- `bundle exec jekyll serve --baseurl "/my-castle"` and `JEKYLL_ENV=production bundle exec jekyll build` (paired with `{​% if jekyll.environment == "production" %​}`) both behaved exactly as documented.
- **Real gap (`tested`):** `git init` on this system defaults to branch `master` (git prints an explicit hint); only the Cloud Realms path runs `git branch -M main` before pushing. The macOS/Windows/Linux paths go straight from `git init` to `gh repo create ... --push` and then to a "Enable Pages" step and a `gh api ... -f "source[branch]=main"` example that both hardcode `main` — a learner on those paths can be left with a `master` default branch and a Pages-enable step that doesn't match reality.
- `gh api -X POST repos/:owner/my-castle/pages -f "source[branch]=main" ...` parsed correctly and reached GitHub's real auth layer (failed only for lack of a token) — confirms the command's syntax, not its full flow.
- Missing: no mention that GitHub Pages' classic "Deploy from a branch" build runs an older, pinned `github-pages` gem version with a fixed plugin whitelist — a real "works locally, fails on Pages" gotcha the quest's own "diagnose a broken build" framing implies it should cover.

### 2. Jekyll Fundamentals — ✅ 83 (16 available, 9 runnable ran / 8 passed / 1 failed / 2 skipped / 5 reasoned)
- Dimensions: commands_work 4, content_accuracy 4, completeness 4, clarity 4, structure 5, safety 5.
- `jekyll new my-castle && bundle exec jekyll serve` produced the exact quoted output ("Server address: http://127.0.0.1:4000/"); adding `collections: recipes:` to `_config.yml` plus `_recipes/bread.md` produced `_site/recipes/bread/index.html` exactly as promised.
- `bundle exec jekyll build --verbose`, `--drafts`, `--livereload`, and the multi-config merge `--config _config.yml,_config_dev.yml` (later file wins) all ran cleanly and matched the documented behavior.
- **Real bug (`tested`, `failed`):** `docker-compose up -d` (line 462, Chapter 4 "One Repo, Two Configs") fails outright — `docker-compose` reported `no configuration file provided: not found`. No `docker-compose.yml`/`Dockerfile` is ever created or shown anywhere in the quest, so this exact command cannot work for anyone following it linearly.
- Minor: `.gitignore` step (`echo "_site/" >> .gitignore ...`) duplicates entries `jekyll new` already adds by default — harmless but a no-op as presented.

### 3. YAML Configuration — ✅ 80 (16 available, 11 runnable ran / 10 passed / 1 failed / 4 skipped / 1 reasoned)
- Dimensions: commands_work 3, content_accuracy 4, completeness 5, clarity 4, structure 5, safety 5.
- All 8 YAML snippets parsed exactly as described with PyYAML; `yamllint _config.yml _data/team.yml` exited 0. Every "pitfall" claim was independently reproduced: `yes`/`on` → boolean `True`, `1.20` → float `1.2` (trailing zero lost), an unquoted colon in a string → real parse error, `01234` unquoted → octal `668`, `|` vs `>` → literal-newline vs folded-string.
- **Real bug (`tested`, `failed`):** the Chapter 3 Liquid sample (lines 360–364) wraps every tag in `{​% raw %​}...{​% endraw %​}` — e.g. `{​% raw %​}{​% for member in site.data.team %​}{​% endraw %​}`. Rendered with the Ruby `liquid` gem exactly as printed, it outputs the tags as **inert literal text**, not an iterating loop; only the unwrapped version actually prints "Ada Lovelace - Architect." A learner copying the shown block into a real template gets a silent no-op.
- `bundle exec jekyll serve --config ...` / `JEKYLL_ENV=production build` were correctly `skipped` (no Jekyll site present in this quest's own sandbox, matching its stated "pre-existing Jekyll site" prerequisite) — an environment limitation, not a quest defect.

### 4. Git Workflow Mastery — ✅ 92 (12 available, 8 runnable ran / 8 passed / 5 skipped / 2 reasoned)
- Dimensions: commands_work 5, content_accuracy 4, completeness 4, clarity 5, structure 5, safety 5.
- Ran the full lifecycle verbatim against a local bare-repo "origin": `git switch main`/`pull`/`switch -c`/`add`/`commit`/`push -u`, `git status`/`log --oneline --graph --all`/`diff`, a real merge conflict reproducing the exact `<<<<<<< HEAD` / `=======` / `>>>>>>>` markers, `git rebase --continue` across two sequential conflicts, and `git merge --abort`/`git rebase --abort` restoring a clean tree. `gh pr create`/`gh pr merge --squash --delete-branch` flags were verified against the installed `gh` 2.98.0's `--help` (not executed live — no auth/network).
- **Real gap (`tested`):** Chapter 2's merge-commit diagram (`main: A---B---------M`) only materializes when `main` has diverged since branching. Following the quest's own worked sequence (branch off current `main`, one commit, merge straight back with no intervening `main` commits) actually **fast-forwards** — no merge commit — a real mismatch between the diagram and what the quest's own walkthrough produces (confirmed by running both the fast-forward case and a genuinely-diverged case).
- `git restore`/`git revert` are a stated secondary objective but only appear in a prose warning (line ~268), with no worked code example, unlike every other objective.

### 5. Liquid Templating — ⚠️ 71 (15 available, 15 ran / 13 passed / 2 failed / 1 skipped / 1 reasoned)
- Dimensions: commands_work 3, content_accuracy 3, completeness 4, clarity 4, structure 4, safety 5.
- Verified against a real Jekyll 4.4.1 / Liquid 4.0.4 site: objects/filters (`{​{ page.title }​}`, `upcase`, `capitalize`+`replace`, `date`, `strip_html`+`truncatewords`), `for ... limit:`/`forloop.index`, `sort`+`reversed`, parameterized `include`, layouts with `{​{ content }​}`, `comment`/`raw` blocks, and whitespace-dash control (`{​%- -%​}`) all rendered exactly as documented.
- **Confirmed bug #1 (`tested`, `failed`):** Chapter 2's "New" badge condition, `{​% elsif post.date > site.time | date: "%s" | minus: 604800 %​}` (line 276), throws a real error under `jekyll build`/`jekyll serve`: `Liquid syntax error (line 5): Expected end_of_string but found pipe` — filters cannot be chained after a comparison operator inside an `elsif`. The badge silently never renders.
- **Confirmed bug #2 (`tested`, `failed`):** Chapter 4's forloop/whitespace example (line 408, `{​% unless forloop.first %​}{​% endunless %​}{​{ tag }​}`) does **not** produce the claimed single-line "liquid, jekyll, templating (no leading comma)." As printed, none of the `for`/`unless`/`endfor` tags use whitespace-control dashes, and the real rendered output (verified with `cat -A`) has stray newlines and leading spaces between tags — ironic since this is the exact chapter teaching whitespace control.
- `case`/`when` and `contains` are mentioned only in prose with no runnable example, unlike every other construct in the quest.

## 🐞 Issues Found

Every item cites what was actually run/observed (`tested`) or read directly from source/frontmatter/network data (`reasoned`); severities as the engine scored them (structural/network finding severity is my own judgment).

- **HIGH · Liquid Templating · Chapter 2, line 276 ("New" badge `elsif`) · `tested`** — `{​% elsif post.date > site.time | date: "%s" | minus: 604800 %​}` is a genuine Liquid syntax error in real Jekyll (`Expected end_of_string but found pipe`), reproduced via `jekyll build`. **Fix:** precompute the cutoff with `assign` first, e.g. `{​% assign week_ago = site.time | date: "%s" | minus: 604800 %​}{​% assign post_ts = post.date | date: "%s" %​}{​% if post_ts > week_ago %​}...{​% endif %​}` (both sides still need coercing to the same numeric type).
- **HIGH · Liquid Templating · Chapter 4, line 408 (forloop/whitespace example) · `tested`** — Claimed output "liquid, jekyll, templating (no leading comma)" is not what the snippet as written produces (verified with `cat -A`: stray newlines/leading spaces). **Fix:** add whitespace-control dashes (`{​%- for -%​}`, `{​%- unless forloop.first -%​}`, `{​%- endunless -%​}`, `{​%- endfor -%​}`), or correct the claimed output to match reality.
- **HIGH · Quest-graph structure (GitHub Pages Basics / Jekyll Fundamentals / Git Workflow Mastery) · `reasoned` (my own cross-read of `quest_dependencies` frontmatter + `_data/quests/network.yml`)** — This entire five-quest window is a single dependency cycle: `Jekyll Fundamentals --unlocks--> GitHub Pages Basics --unlocks--> Git Workflow Mastery --unlocks--> Jekyll Fundamentals` (confirmed directly in `_data/quests/network.yml`'s `edges` list). Because a true topological order doesn't exist, `walkthrough_plan.py`'s Kahn/SCC condensation collapses these three (plus `YAML Configuration` and `Liquid Templating`, which both also unlock back into the same loop via `Jekyll Fundamentals`) into one strongly-connected component and falls back to difficulty-then-alphabetical tie-breaking — which is *exactly* why this session was told to play **GitHub Pages Basics first**, even though its own `quest_dependencies.required_quests` (and its `prerequisites.knowledge_requirements: "Completion of Jekyll Fundamentals"`) name Jekyll Fundamentals as a hard prerequisite. The root cause looks like a single bad edge: `Git Workflow Mastery`'s frontmatter lists `unlocks_quests: - /quests/0001/jekyll-fundamentals/`, but `Jekyll Fundamentals` itself declares `required_quests: []` (it's the level's entry point) and does **not** list Git Workflow Mastery anywhere — the two files disagree about who unlocks whom. **Fix:** remove the spurious `jekyll-fundamentals` entry from `Git Workflow Mastery`'s `unlocks_quests` (or, if intentional, add the missing reciprocal `required_quests`/`recommended_quests` entry on `Jekyll Fundamentals` so the DAG closes correctly) and re-run `make quest-build-network`. Note: `scripts/quest/validate-quest-network.py`'s cycle check only inspects the *required* edge subgraph (which has no cycle here), so `make quest-audit` would not currently catch this — the cycle only shows up in the combined required+recommended+unlocks graph the walkthrough planner uses.
- **MEDIUM · GitHub Pages Basics · macOS/Windows/Linux platform blocks · `tested`** — `git init` defaults to branch `master` on this system; only the Cloud Realms path runs `git branch -M main`. The following "Enable Pages" instructions and the `gh api ... -f "source[branch]=main"` example hardcode `main`. **Fix:** add `git branch -M main` (or an explicit default-branch check) to the macOS/Windows/Linux blocks too.
- **MEDIUM · Jekyll Fundamentals · Chapter 4, line 462 (`docker-compose up -d`) · `tested`, `failed`** — Fails with "no configuration file provided: not found"; no `docker-compose.yml`/`Dockerfile` is ever shown in the quest. **Fix:** either supply the actual compose file (matching the stated `localhost:4002` port) or replace the snippet with the already-working `docker run ... jekyll/jekyll:4` command shown in the Cloud Realms section.
- **MEDIUM · YAML Configuration · Chapter 3, lines 360–364 (Liquid data-loop sample) · `tested`, `failed`** — Wrapped in `{​% raw %​}` tags that make it a literal no-op if copied as shown; only the unwrapped version actually loops and prints the data. **Fix:** remove the `{​% raw %​}` wrapping from the code block a learner is meant to copy (keep it only if it's illustrating the raw tag itself, and label it as such).
- **MEDIUM · Git Workflow Mastery · Chapter 2, merge-commit diagram · `tested`** — The diagram (`main: A---B---------M`) doesn't match what the quest's own worked sequence produces (a fast-forward, no merge commit) unless `main` has diverged first. **Fix:** either add an intervening `main` commit to the worked example before merging, or note that the diagram assumes divergence.
- **LOW · Git Workflow Mastery · secondary objective (`git restore`/`git revert`) · `reasoned`** — Named as a secondary objective and mentioned in a warning callout, but has no worked code example unlike every other objective. **Fix:** add a short `git restore <file>` / `git revert <commit>` snippet.
- **LOW · GitHub Pages Basics · "GitHub Actions Build" secondary objective · `reasoned`** — Mentioned only via a table link/knowledge-check bullet, no sample workflow YAML shown despite being a named secondary objective. **Fix:** link or embed a minimal `jekyll.yml` GitHub Actions starter workflow.
- **LOW · Liquid Templating · Chapter 2 (`case`/`when`, `contains`) · `reasoned`** — Mentioned only in prose, unlike every other construct in the quest, which gets a runnable example. **Fix:** add a short code sample.

No safety issues anywhere in the slice — every quest scored safety 5/5; the only privilege-adjacent commands (`sudo apt install gh`, `gh repo create --push`) are standard, expected, and clearly the quest's stated purpose (not unwarned side effects).

## 🔗 Chain Continuity

Read in plan order (GitHub Pages Basics → Jekyll Fundamentals → YAML Configuration → Git Workflow Mastery → Liquid Templating), carrying forward what a learner would actually have after each quest:

- **Topically, this is a coherent, well-designed arc.** All five quests share `quest_series: "Static Site Mastery"` / `quest_line: "The Web Fundamentals Codex"` / `quest_arc: "Forging Your First Website"`, and the skills genuinely build on each other: Jekyll's directory/build model → YAML config/data → Liquid templating → Git branching discipline → publishing to GitHub Pages is a sensible real-world sequence for a beginner building and shipping their first site.
- **But the *walk order this session was given* is not that sequence, and it should have been.** As detailed in Issues, the five quests' `quest_dependencies` frontmatter forms a genuine cycle when read together (`Jekyll Fundamentals ⇄ GitHub Pages Basics ⇄ Git Workflow Mastery`, with `YAML Configuration` and `Liquid Templating` also looping back through `Jekyll Fundamentals`'s `unlocks_quests`). Every one of `GitHub Pages Basics`, `YAML Configuration`, and `Liquid Templating` correctly declares `jekyll-fundamentals` as a **required** prerequisite in its own frontmatter — the intended chain is unambiguous and consistent on that point. The only quest that breaks it is `Git Workflow Mastery`, whose `unlocks_quests` claims it unlocks `Jekyll Fundamentals` — a quest that is supposed to be the level's zero-prerequisite entry point (`required_quests: []`). That single inverted edge is what defeats the planner's topological sort and produced this run's actual order (GitHub Pages Basics first), which — if a real learner followed it literally, in order, with no other context — would have them attempt a quest whose own stated prerequisite ("Completion of Jekyll Fundamentals") hasn't been met yet.
- **In practice the damage is contained, not catastrophic.** GitHub Pages Basics' body doesn't actually *require* Jekyll Fundamentals' specific artifacts beyond "a working Jekyll site already exists" (its own Chapter 1 starts from `cd my-castle`, assuming that site is already scaffolded) — so a learner who happened to have already built a Jekyll site some other way wouldn't be blocked outright. But that's exactly the ambiguity a correct dependency graph is supposed to eliminate, and it's the reason this walkthrough — simulating a first-time learner with *only* this window's stated order to go on — surfaced the problem at all.
- **Git Workflow Mastery's own prerequisite chain is also worth a second look.** It correctly requires `/quests/0000/git-basics/` (a different, foundational level) and recommends `GitHub Pages Basics`, which is reasonable — its own content (branches, PRs, conflict resolution) doesn't depend on Jekyll knowledge at all, so its actual body content sits *outside* this quest's Jekyll-focused arc even though it shares `level: "0001"` and the `quest_series`/`quest_line` tags with the other four. It's the odd one out topically as well as graph-wise.
- **Terminology and environment carry over cleanly.** None of the later quests silently assume something the earlier ones in this window didn't teach (aside from the cycle above) — `_config.yml`, `_data/`, Liquid delimiters, and Git branch/PR vocabulary are each introduced before they're relied upon in the *intended* (non-cyclic) reading order.

**Net:** the five quests are a genuinely well-conceived learning arc undermined by one bad frontmatter edge (`Git Workflow Mastery`'s spurious `unlocks_quests: jekyll-fundamentals`) that turns the whole window into an unsortable cycle for any tool — like this walkthrough's planner — that tries to derive a strict play order from the declared dependency graph.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sealed). The `quest-walkthrough.yml` workflow pre-computed and sealed `walk-evidence.json` / `walk-evidence.md` via the deterministic agentic execute engine before this session started; I consumed them **as-is** and made **zero** edits to `walk-plan.json`, `walk-evidence.*`, or any quest content (the engine's child `claude` processes can't authenticate from my Bash tool, so I could not and did not re-run it). This was not a `--mock` run — `walk-evidence.json`'s `meta` blocks show real `cost_usd`/`turns`/`duration_s`/`session_id` per quest.
- **What I ran vs. reasoned:** All `passed`/`failed`/`skipped` outcomes cited above are from commands the execute engine actually ran in its disposable sandbox (real Jekyll 4.4.1/Bundler builds, the Ruby `liquid` gem, `yamllint`, a local bare-repo git simulation, `gh --help` flag checks). I performed **one additional read-only verification of my own**: cross-reading all five quests' `quest_dependencies` frontmatter against `_data/quests/network.yml`'s `edges` list and re-deriving the planner's `succ`/SCC logic from `scripts/quest/walkthrough_plan.py` by hand — this is `reasoned`, not executed, and is the basis for the graph-cycle finding in Issues/Chain Continuity. Everything else in Chain Continuity is static reasoning over the five quest source files I read in full, in plan order.
- **Coverage / limits:** This is **window 2 of 6** — only 5 of the level's 26 quests were walked in this run; I make no claim about the other 21 (the perfection ledger accumulates coverage of the remaining windows across separate runs). Per-quest snippet coverage is reported in §Evidence (e.g. Liquid Templating ran 15/15 recorded snippets; GitHub Pages Basics ran 7/7 runnable but skipped 4 unsafe/interactive ones like `brew install`/`gh auth login`). Environment limits noted throughout: macOS (`brew`), Windows (PowerShell/`winget`), and real network-mutating steps (`gh repo create --push`, DNS record creation, `docker-compose` image pulls) could not be exercised in this headless Linux sandbox — these were correctly labeled `reasoned`/`skipped` by the engine, not scored as quest defects.
- **Confidence:** High on all five per-quest scores (each backed by real command execution, not inference) and on the two Liquid bugs (both independently reproduced with real error output/`cat -A` byte inspection). High on the dependency-cycle finding too — it's a direct, mechanical read of `_data/quests/network.yml`'s committed edges plus the planner's own documented algorithm, not a subjective judgment call.

---

*Machine evidence excerpt (verbatim from `walk-evidence.md`):*
> **5** quests evaluated · ✅ 4 pass · ⚠️ 1 warn · ❌ 0 fail · avg **81.8%** · ~$4.3236
>
> | | Score | Quest | Level | Snippets run | Summary |
> |---|--:|---|---|:-:|---|
> | ✅ | 83 | GitHub Pages Basics: Host Your Jekyll Site for Free | 0001 | 7/7 | The quest's core technical claims all held up under actual execution... |
> | ✅ | 83 | Jekyll Fundamentals: Build Static Sites with Ruby | 0001 | 9/10 (1✗) | The quest's core Jekyll workflow... was executed end-to-end in the sandbox and worked exactly as described... |
> | ✅ | 80 | YAML Configuration: Site Settings Mastery | 0001 | 11/7 (1✗) | The quest's YAML/Jekyll content is technically solid... |
> | ✅ | 92 | Git Workflow Mastery: Branches, Merging & Team Collaboration | 0001 | 8/10 | Git Workflow Mastery is a well-structured, technically sound quest... |
> | ⚠️ | 71 | Liquid Templating: Dynamic Content for Jekyll Sites | 0001 | 15/4 (2✗) | Most of the quest's Liquid content is accurate and was verified to work exactly as documented... |
