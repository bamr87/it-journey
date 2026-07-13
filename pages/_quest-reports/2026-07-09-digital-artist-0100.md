---
title: Digital Artist · L0100 · 2026-07-09
description: Quest-perfection walkthrough of the Frontend & Containers slice digital-artist/0100 on 2026-07-09,
  engine verdict fail. An evidence-based, learner's-eye…
date: '2026-07-09T00:00:00.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Digital Artist
tags:
- digital-artist
- level-0100
- walkthrough
- quest-perfection
- fail
- frontend-containers
render_with_liquid: false
excerpt: 'Digital Artist · Level 0100 — Frontend & Containers: an evidence-based quest-perfection walkthrough
  from 2026-07-09.'
slice: digital-artist/0100
character: digital-artist
level: '0100'
theme: Frontend & Containers
tier: Adventurer
verdict: fail
quest_count: 5
walk_date: '2026-07-09'
run_url: https://github.com/bamr87/it-journey/actions/runs/29190829265
source_report: test/quest-validator/walkthroughs/2026-07-09-digital-artist-0100.md
---

> **Slice** `digital-artist/0100` · **Level** 0100 (Frontend & Containers) · **Adventurer tier** · **Engine verdict** ❌ fail · **Walked** 2026-07-09
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29190829265) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-09-digital-artist-0100.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-09-digital-artist-0100.md)

---

## 🎯 Session Summary

I walked the first window (5 of 8 quests) of the **Digital Artist → Level 0100
"Frontend & Containers"** (Adventurer ⚔️) slice as a learner, consuming the
workflow-sealed execute-engine evidence (`walk-evidence.json`) and reading each
quest source in plan order. The slice splits into two sub-journeys: a **Docker
core** (`container-fundamentals` → `docker-compose-orchestration`) and a **Jekyll +
Bootstrap** trio (`frontend-docker`, `frontend`, `jekyll-component-refactoring`).

**Headline verdict: FAIL for the slice as a linked path** — 1 pass, 1 warn, 3 fail,
average 62.2%. The Docker half is strong (Compose scored 83; Container Fundamentals
could not be scored because the engine exhausted its turn budget waiting on a live
container the sandbox can't run). The Jekyll half is where a real beginner breaks:
**both** `frontend-docker` (33) and `frontend` (55) fail on the *same* defect — they
tell the learner to edit `_includes/head.html` and `_layouts/default.html`, files
that don't exist in a freshly scaffolded gem-theme Jekyll site — so the central
"add Bootstrap" promise never actually lands. `jekyll-component-refactoring` (78,
warn) is the healthiest of the Jekyll three but ships CSS that never gets imported.
A maintainer should prioritise the two shared Jekyll-scaffold bugs, since fixing that
one pattern lifts the whole back half of the level.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ❌ | Docker Container Fundamentals: Images to Registries | — (errored) | Engine hit max-turns curling a container the sandbox can't run — **unscored**, not a proven quest defect. |
| 2 | ✅ | Docker Compose Orchestration: Multi-Container Apps | 83 | Technically excellent; every compose/lifecycle claim verified — one real bug: `--scale web=3` collides with a fixed host port. |
| 3 | ❌ | Dockering Jekyll with Bootstrap 5 | 33 | Breaks at nearly every checkpoint: `jekyll new .` conflict, phantom `cd`, `{​% raw %​}`-wrapped include, gem-persistence crash, Bootstrap 4 markup. |
| 4 | ❌ | Frontend Forests: Building a Jekyll Site with Bootstrap | 55 | Scaffolding works, but the core Bootstrap step edits files that don't exist in the default theme; no concrete CDN snippet; placeholder objectives. |
| 5 | ⚠️ | The Artisan's Forge: Refactoring Jekyll Theme Components | 78 | Solid, verified refactoring pattern — but the new SCSS partial is never imported, so a green build ships zero nanobar styling. |

## 🔬 Evidence

All outcomes below are from commands the sealed execute engine **actually ran** in a
disposable sandbox (per `walk-evidence.json`); items I only reasoned about statically
are labelled `reasoned`.

### 1 · Container Fundamentals — ❌ errored / unscored
- **No score produced.** The engine terminated with `terminal_reason: max_turns`
  ("Reached maximum number of turns (40)"). The transcript tail shows it looping on
  `curl http://localhost:8080` / `curl http://127.0.0.1:8080/` — i.e. trying to reach
  a running `nginx`/Node container. Docker isn't runnable in this sandbox, so the
  agent burned its turn budget retrying network calls and never returned a verdict.
- **Interpretation:** this is a **coverage/harness gap, not evidence of a broken
  quest.** Reading the source, the quest is well-structured (clear image-vs-container
  model, per-platform install blocks, staged chapters, knowledge checks). I did not
  witness any content defect — treat quest 1 as **`reasoned`-clean, unverified**.

### 2 · Docker Compose Orchestration — ✅ 83
- Snippets: **ran 13, passed 12, failed 1, skipped 4** (available_runnable 8).
- `passed` — `app.py` (Flask+Redis), `Dockerfile` (python:3.12-slim), `compose.yaml`
  web+redis stack, full `up -d / ps / logs -f / down` lifecycle.
- `passed` — custom `frontend`/`backend` networks compose file (network isolation
  claim verified); postgres named-volume + bind-mount; volume persistence across
  `down`/`up` and removal on `down -v`.
- `passed` — `.env` + full stack with `env_file`, `healthcheck`,
  `depends_on: condition` (health-gated startup order verified).
- `failed` — Chapter 3 final block `docker compose up -d --scale web=3`:
  > "`config` and `up -d` passed cleanly (db went healthy, web started).
  > `docker compose up -d --scale web=3` **FAILED**: 'Error response from daemon: …
  > Bind for 0.0.0.0:8080 failed: port is already allocated' — because web publishes
  > a fixed host port. `down -v` afterward worked fine."
- `skipped` — the macOS/Windows/other-platform install blocks (sandbox is Linux).
- Dimensions: commands_work 4, content_accuracy 4, completeness 4, clarity 4,
  structure 5, safety 5.

### 3 · Dockering Jekyll with Bootstrap 5 — ❌ 33
- Snippets: **ran 8, passed 4, failed 4, skipped 1, reasoned 1** (runnable 4).
- `passed` — create `Dockerfile` (FROM jekyll/jekyll:latest); create
  `docker-compose.yml`; `git init && add && commit`.
- `failed` — `docker-compose run jekyll jekyll new .` → conflicts with the
  Dockerfile/compose files created two steps earlier. Engine confirmed the workaround
  `jekyll new . --force` `passed`.
- `failed` — `cd my-jekyll-site` → **directory never exists** (`jekyll new .`
  installs into the current dir, so there is no subfolder).
- `failed` — `index.html` containing `{​% raw %​}{​% include head.html %​}{​% endraw %​}`
  → the `{​% raw %​}` wrapper is in the *copy-pasteable* sample, so the include (and
  thus Bootstrap) never loads when built.
- `failed` — final `docker-compose up` → crashes `Bundler::GemNotFound` because
  installed gems don't persist between container runs (no bundle volume).
- `reasoned` — the `head.html` Bootstrap tags carry `integrity="sha384-xxx"`
  placeholder hashes.
- Dimensions: commands_work 1, content_accuracy 1, completeness 2, clarity 2,
  structure 2, safety 4.

### 4 · Frontend Forests: Building a Jekyll Site with Bootstrap — ❌ 55
- Snippets: **ran 8, passed 6, failed 2, skipped 1, reasoned 9** (runnable 0 fenced-
  runnable; much of the quest is prose/Liquid explanation, verified by reasoning +
  a real build).
- `passed` — `gem install jekyll bundler`, `jekyll new your-site-name`,
  `cd your-site-name`, `bundle exec jekyll build`, `bundle exec jekyll serve`
  (scaffolding chain works exactly as written); Chapter 9 filter table
  (`date`/`slugify`/`where`/`markdownify`) verified against a real build.
- `failed` — Step 3 "Open `_includes/head.html` and add the Bootstrap CSS link" and
  Step 3/4 "Edit `_layouts/default.html`" → **these files don't exist** in a
  freshly scaffolded site using the default gem theme; no guidance to create/override
  them. This is the quest's central task and it can't be completed as written.
- `reasoned` — Chapter 9 Liquid/layout-chain/`include` explanations (accurate).
- Dimensions: commands_work 2, content_accuracy 3, completeness 2, clarity 3,
  structure 3, safety 5.

### 5 · The Artisan's Forge: Refactoring Jekyll Theme Components — ⚠️ 78
- Snippets: **ran 11, passed 11, failed 0, skipped 1, reasoned 2** (runnable 3).
- `passed` — full refactor verified end-to-end in a real **Jekyll 4.4.1** build:
  `touch _includes/components/nanobar.html`, the `{​% include %​}` tag, the
  `{​% if site.nanobar.enabled %​}` config guard, the `nanobar:` YAML config,
  `mkdir -p _sass/components && touch _nanobar.scss`, the SCSS partial, the
  custom-property `style` attribute, the scroll-progress `<script>`, the
  BEFORE/AFTER footer restructuring, `bundle exec jekyll build`, and the
  `nanobar.enabled: false` toggle.
- **Not surfaced as a failure by the engine but flagged in its summary:** the quest
  never shows how to `@import "components/nanobar"` into a compiled stylesheet, so a
  learner gets a green `jekyll build` with **no nanobar CSS actually shipped**.
- `skipped` — `docker-compose exec -T jekyll …` (Compose V1 binary absent in sandbox).
- Dimensions: commands_work 4, content_accuracy 4, completeness 3, clarity 4,
  structure 3, safety 5.

## 🐞 Issues Found

Every item below cites a command the engine ran or an exact line from the quest
source. Severity uses the engine's own recommendation grading where present.

### Dockering Jekyll with Bootstrap 5 (`frontend-docker.md`) — the most broken quest
- **HIGH · Step 2.3 (`jekyll new .` conflict)** — observed the command `failed`
  against the Dockerfile/compose files created two steps earlier. *Fix:* run
  `jekyll new .` in an empty dir first, or document `--force` and why.
- **HIGH · Step 3.1 (`cd my-jekyll-site`)** — observed the directory does not exist.
  *Fix:* remove the step; `jekyll new .` stays in the current directory.
- **HIGH · Step 4 (`{​% raw %​}{​% include head.html %​}{​% endraw %​}`)** — observed the
  built site never includes Bootstrap because the `raw` wrapper is in the pasteable
  sample. *Fix:* use plain `{​% include head.html %​}`.
- **HIGH · Final `docker-compose up` (gem persistence)** — observed
  `Bundler::GemNotFound` crash. *Fix:* add a named `bundle_cache:/usr/local/bundle`
  volume, or run `bundle install && jekyll serve` in the serving container.
- **MEDIUM · Bootstrap 5 markup accuracy** — sample uses `data-toggle`, `sr-only`,
  `.jumbotron`, jQuery+Popper (all Bootstrap 4). *Fix:* `data-bs-toggle`,
  `visually-hidden`, drop `.jumbotron`/jQuery; `bootstrap.bundle.min.js` includes
  Popper.
- **MEDIUM · `docker-compose` vs `docker compose`** — the standalone binary is
  deprecated / absent on the sandbox. *Fix:* use Compose V2 `docker compose`.
- **MEDIUM · SRI `sha384-xxx` placeholders** — `reasoned` from source. *Fix:* ship
  the real hash or link the exact CDN snippet page.
- **LOW** · obsolete `version: '3'` key; **LOW** · auto-seeded placeholder objectives.

### Frontend Forests (`frontend.md`)
- **HIGH · Steps 3-4 (Bootstrap integration)** — observed edits to
  `_includes/head.html` / `_layouts/default.html` fail because those files don't
  exist in a default gem-theme scaffold. *Fix:* state they don't exist and show how
  to override them (`bundle show minima` → copy, or create override files) **at
  Step 3**, not buried in Chapter 9.
- **HIGH · missing concrete CDN snippet** — the quest describes Bootstrap in prose
  only. *Fix:* provide fenced `<link …bootstrap.min.css>` / `<script
  …bootstrap.bundle.min.js>` blocks to paste.
- **MEDIUM** · placeholder Quest Objectives; **MEDIUM** · move Chapter 9's
  theme-override explanation before Step 3; **LOW** · add explicit Prerequisites
  (Ruby version, prior Jekyll knowledge) + Rewards/XP block.

### The Artisan's Forge (`jekyll-component-refactoring.md`)
- **HIGH · Phase 3 (SCSS never imported)** — verified a green build ships zero
  nanobar CSS because no step wires `_nanobar.scss` into a compiled stylesheet.
  *Fix:* add `@import "components/nanobar";` in `assets/css/main.scss` (with front
  matter).
- **HIGH · duplicated "📚 Resources" section** — appears twice verbatim. *Fix:*
  delete the copy after the closing banner.
- **MEDIUM** · under-specified bonus objectives ("step animation", "CI validation
  test") with no body instructions; **MEDIUM** · `docker-compose exec` → `docker
  compose exec` (V1 absent, confirmed skipped); **LOW** footer-example / step-order
  clarifications.

### Docker Compose Orchestration (`docker-compose-orchestration.md`)
- **MEDIUM · Chapter 3 final command** — verified `docker compose up -d --scale
  web=3` fails ("port is already allocated") because `web` publishes a fixed host
  port. *Fix:* remove the fixed `ports:` mapping for the scaled service (use a range
  or a reverse proxy), or explicitly caveat that `--scale` needs the host port
  dropped.

### Container Fundamentals (`container-fundamentals.md`)
- **No content issue witnessed.** The engine unscored it (max-turns while curling a
  container the sandbox can't run). Flagged only as a **coverage gap** (see §7).

**Not "no blocking issues":** this slice has 4 HIGH content bugs across the two
Jekyll main quests plus the SCSS-import bug — all blocking for a beginner.

## 🔗 Chain Continuity

Reading the five sources as one journey a Digital Artist would actually take:

- **Docker sub-chain (1 → 2) is well-linked.** `container-fundamentals` declares
  `unlocks_quests: [docker-compose-orchestration]`, and `docker-compose-orchestration`
  declares `required_quests: [container-fundamentals]` and names it in its knowledge
  prerequisites. A learner finishing quest 1 is genuinely ready for quest 2 — the
  Compose quest builds on images/Dockerfiles exactly as quest 1 taught them. Clean
  dependency hygiene, and the Compose quest scored 83 on its own merits. The only
  crack is that quest 1 couldn't be executed here, so I can't *prove* it hands off a
  working Docker install; its structure strongly implies it does.

- **Jekyll sub-chain (3, 4, 5) is loosely coupled and under-signposted.** Both
  `frontend-docker` and `frontend` declare **no `quest_dependencies` and empty/None
  prerequisites**, yet both demand Ruby/Jekyll fluency (theme internals, `_includes`,
  `_layouts`) that nothing earlier in this level establishes. A learner arriving from
  the Docker half knows containers but has never scaffolded a Jekyll site — there is
  **no bridge quest** teaching Jekyll basics before the Bootstrap-integration steps
  that both quests hinge on.

- **The two Bootstrap main quests share one systemic defect.** `frontend-docker`
  (33) and `frontend` (55) independently break at the *same* place: "edit
  `_includes/head.html` / `_layouts/default.html`" against a default gem theme where
  those files don't exist. This isn't two bugs; it's one authoring anti-pattern
  duplicated across the level. Fixing the "override a gem-theme file" explanation
  once, and reusing it, repairs both.

- **Ordering nit.** The plan walks `frontend-docker` *before* `frontend`, but
  `frontend` (scaffold a plain Jekyll+Bootstrap site) is conceptually the more
  foundational of the two — dockering the site logically comes after you can build
  it. Neither declares an order, so the sequencing is incidental rather than designed.

- **The side quest is the well-behaved anchor.** `jekyll-component-refactoring`
  (78, warn) correctly `recommends` `frontend-docker` and assumes an existing themed
  Jekyll site — a reasonable prerequisite it actually states. It's the strongest
  Jekyll quest and the right capstone, once its SCSS-import gap is closed.

**Net:** the slice is really two mini-arcs. The Docker arc holds together as a
learning path; the Jekyll arc does not yet — a beginner following it literally cannot
complete the Bootstrap task in either main quest, and the path never bridges them
from "I know Docker" to "I know Jekyll."

## 🧠 Reasoning & Method

- **Mode:** `execute` (real sandboxed command runs), evidence **pre-sealed by the
  workflow** in `walk-evidence.json` / `walk-evidence.md`. I consumed it verbatim —
  I did **not** re-run the engine (its child `claude` processes can't authenticate
  from the agent's Bash tool) and did not edit the plan or evidence.
- **What I ran vs. reasoned:** every `passed`/`failed`/`skipped` above is a command
  the engine actually executed in a disposable temp dir (12 passed / 1 failed for
  Compose; 4/4 for `frontend-docker`; 6 passed / 2 failed for `frontend`; 11/0 for
  the refactor quest). My own contribution — the chain-continuity analysis and the
  ordering/prerequisite findings — is `reasoned` from reading each quest source in
  plan order, and is labelled as such.
- **Coverage caps / honesty:**
  - **Quest 1 (`container-fundamentals`) is unscored** — the engine hit its 40-turn
    limit retrying `curl localhost:8080` against a container the sandbox can't run.
    I report it as an executed-but-**errored** coverage gap, not as pass or fail, and
    I did not invent a score for it. Its clean structure is a `reasoned` observation
    only.
  - `frontend`'s content is heavily prose/Liquid (0 fenced *runnable* snippets); 9 of
    its items are `reasoned`, so its evidence is weaker than the container quests'.
  - Platform-specific (macOS/Windows) install blocks and Docker Compose **V1**
    (`docker-compose`) commands were `skipped` — the Linux sandbox has neither, which
    is itself a signal the quests should move to Compose V2.
  - **Window:** this was window **1 of 2** — quests 6-8 of the 8-quest level were
    not walked this run and are out of scope for this report.
- **Confidence:** High on the four scored quests (direct sandbox execution).
  Medium-low on quest 1 (unverified). High on the chain-continuity findings, since
  they rest on declared frontmatter dependencies + observed shared defects, not on
  guesswork.
