---
title: 'Walkthrough — System Engineer · Level 0101 (CI/CD & DevOps)'
date: '2026-07-28T00:00:00.000Z'
character: system-engineer
level: '0101'
theme: CI/CD & DevOps
tier: Adventurer
quest_count: 5
mode: execute
overall_verdict: warn
session:
  window: '1 of 3 (offset 5, size 5)'
  level_total_quests: 13
  engine_average: 76.8
  engine_counts: '2 pass · 3 warn · 0 fail'
  engine_cost_usd: 3.5415
  evidence_source: sealed walk-evidence.json (workflow-precomputed execute engine)
---

## 🎯 Session Summary

I walked a **5-quest window** (window 1 of 3; the full 0101 level holds 13 quests) of the **System Engineer / Level 0101 — CI/CD & DevOps (Adventurer ⚔️)** slice as a learner, consuming the workflow-sealed execute-engine evidence and reading every quest source in plan order. The headline verdict is **warn**: the engine returned **2 pass · 3 warn · 0 fail**, average **76.8%**, every quest actually executed in the sandbox. Nothing in the slice is unsafe or broken beyond repair, but three of the five quests carry **concrete, hands-on-order bugs** — commands that fail exactly when a learner is told they should work (a missing `test/unit` folder, a Node flag-ordering error, a `docker build` with no Dockerfile) plus a real methodological flaw in the Cartographer's isolation script. The four "Gates of the Pipeline" quests form a genuinely coherent, dependency-sorted CI/CD arc; the one outlier is **The Cartographer**, a chapter grafted in from a *different* campaign whose prerequisites and Ruby/Jekyll toolchain don't match the rest of the slice — a maintainer should note it reads as an interloper when walked first.

## 🗺️ The Journey

Plan order (dependency-sorted by the planner):

1. ⚠️ **The Cartographer: File Platform Bugs Upstream** — **68** · Narrative and issue-filing guidance are accurate, but the Chapter 1 triage script doesn't actually isolate anything (both builds are near-identical full-site rebuilds) and the `gem contents` SHA-pinning route is verifiably wrong.
2. ⚠️ **Testing Integration: Tiered CI/CD Test Gates** — **68** · Solid testing-pyramid theory, but two order-breaking bugs: `npm run test:unit` fails because no `test/unit` folder is ever created, and the flaky-test reporter command breaks on Node CLI flag ordering.
3. ⚠️ **Deployment Pipelines: Production Release Automation** — **72** · Conceptually strong and structurally excellent, but a 'Hard' hands-on quest whose `docker build` fails with no Dockerfile and whose mastery challenges reference scripts (`deploy.sh`, `rollback.yml`, …) that are never scaffolded.
4. ✅ **Environment Management: Dev, Staging, and Prod Parity** — **91** · The standout. Every runnable snippet (three OS env-var demos, the JS config loader, both YAML files) ran exactly as documented; only gap is the promised "tiny app" never wires the JS + YAML examples together.
5. ✅ **Secrets Management: Secure CI Credentials** — **85** · Technically accurate and safe; all JSON/YAML valid, all CLI commands well-formed (gh/aws failures were expected auth/credential gaps, not bugs). Gaps: two secondary objectives undemonstrated and a Jekyll `{% raw %}` artifact that breaks if copied from raw Markdown.

## 🔬 Evidence

All evidence below is from the **sealed `walk-evidence.json`** — the workflow ran `agentic_validate.py --mode execute` deterministically in the disposable runner sandbox (real Jekyll 4.4.1 / Ruby 3.2.3, Node v20.20.2, AWS CLI v2.36.2, gh 2.96.0, Docker). I did **not** re-run the engine; I consumed the file as-is and reasoned over the quest sources myself.

### 1. The Cartographer — 68 (warn) · ran 11/12 recorded snippets (7✓ 4✗ 1 reasoned)
- ✅ `triage.sh` ran end-to-end **only after** adding jekyll-seo-tag, jekyll-include-cache, jekyll-sitemap, jekyll-paginate, jekyll-feed — plugins the real theme needs but the quest never lists (bare Gemfile first failed with `Unknown tag seo` / `Unknown tag include_cached`).
- ✅ Dotdir claim verified empirically: `.triage/min.md` produced **no** `_site/` output; visible `triage/min.md` built to `_site/triage/min/index.html` — matching the quest's inline warning.
- ❌ `diff build-product.log build-minimal.log` → **249 lines each, virtually identical** (only randomized temp-dir names differ). The "minimal page against the bare theme" build is *not* isolated — it's the full product site plus one extra page. The central "removing your repo's customizations as variables" objective is not delivered by the script.
- ❌ `bundle exec gem contents jekyll-remote-theme` runs but lists only the plugin's own `lib/` source — never the fetched theme. Inspecting jekyll-remote-theme 0.5.1 source confirmed the theme is fetched to a `Dir.mktmpdir` deleted after each build ("Cleaning up …" in `--verbose`); there is **no persistent cache** to inspect.
- ✅ All three YAML snippets (personal draft, GitHub issue-form, Actions workflow) parsed cleanly; the tracking-note `git commit` ran verbatim and preserved the multi-line message.

### 2. Testing Integration — 68 (warn) · ran 7/13 recorded (5✓ 2✗ 3 reasoned, 3 skipped OS blocks)
- ✅ Chapter 1 `total.js`/`total.test.js` → `npm test` = 2/2 passed. `npm pkg set scripts.test:unit=…` wrote nested keys correctly despite the colon.
- ❌ `npm run test:unit` **immediately after** defining the scripts → `Could not find '.../test/unit'` (exit 1). The quest never tells the learner to create `test/unit/` or move the test file into it, yet asserts the scripts "run locally exactly as the CI jobs invoke them."
- ❌ `npm run test:unit -- --test-reporter=tap` (Chapter 3) → `Could not find '.../--test-reporter=tap'`. With `test:unit = node --test test/unit`, `npm run … -- <flag>` appends the flag *after* the path, and Node's test runner treats it as another path glob. `node --test --test-reporter=tap test/unit` (flag first) works — but that's not what the quest's invocation composes.
- ✅ `npx c8 --check-coverage --lines 80 --functions 80 node --test` → correct 100% coverage table, exit 0.
- 🔵 Reasoned: 3-job tiered pipeline YAML parses valid (PyYAML) but Postgres `services:` omits `--health-cmd pg_isready …` health checks — a plausible flakiness source, ironic in a flakiness chapter.

### 3. Deployment Pipelines — 72 (warn) · ran 5/15 recorded (4✓ 1✗ 4 reasoned, 6 skipped)
- ✅ `gh api repos/:owner/:repo/environments` — the `:owner`/`:repo` colon placeholders actually expand and hit the live API (401 Bad credentials, not a literal 404), so the non-canonical syntax is functionally correct. macOS block's `|| echo "create environments in repo settings"` fallback worked unauthenticated.
- ❌ `docker build -t myapp:$(git rev-parse --short HEAD) .` → `failed to read dockerfile: open Dockerfile: no such file or directory`. The quest never provides or references a Dockerfile before this snippet.
- ✅ After a minimal Dockerfile was added manually, `docker build` + `docker tag … registry.example.com/myapp:staging` succeeded.
- 🔵 Reasoned/skipped: `./scripts/deploy.sh`, `smoke-test.sh`, `health-check.sh`, `rollback.sh`, `rollback.yml` are all referenced but never defined anywhere; `gh workflow run rollback.yml …` syntax is correct but references an undefined workflow. The deploy workflow YAML parsed valid.

### 4. Environment Management — 91 (pass) · ran 6/9 recorded (6✓ 0✗ 2 reasoned, 1 skipped)
- ✅ All three OS env-var snippets (bash/zsh, PowerShell via pwsh 7.6.3, POSIX) produced the exact documented output: `Running in: development against postgres://localhost:5432/app_dev`.
- ✅ `config.js` as ESM: with `DATABASE_URL` set → correct config object; unset → correctly throws `Missing required config: DATABASE_URL` (the "fail loudly" claim holds).
- ✅ `base.yml` + `production.yml` parse cleanly; a shallow-merge simulation produced the expected layered result.
- 🔵 Terraform `main.tf`/`apply` reasoned only (terraform not installable offline; HCL valid but `app_service` is a fictional resource type with no provider — illustrative pseudocode). `docker run myapp:1.4.2` skipped (placeholder image, expected pull-access-denied).

### 5. Secrets Management — 85 (pass) · ran 8/10 recorded (5✓ 3✗ 0 reasoned, 2 skipped)
- ✅ Both IAM policy JSON fragments valid (`jq .`); both workflow YAMLs (secret injection + OIDC with `id-token: write` + `aws-actions/configure-aws-credentials@v4`) valid and idiomatic current syntax.
- ✅ Linux `apt` path confirmed accurate — gh 2.45.0 is in Ubuntu 24.04 `noble` universe. `gh secret set` unauthenticated returned the expected `set the GH_TOKEN environment variable` (exit 4).
- ❌ `aws sts get-caller-identity` → `NoCredentials`; `aws secretsmanager get-secret-value …` → `NoRegion`; `gh secret set STRIPE_API_KEY` → GH_TOKEN error. **All three are expected outcomes of an unconfigured sandbox, not quest bugs** — but the quest never tells a first-timer to run `aws configure`/set a region before these steps.
- 📌 Verified in source (line 234): `STRIPE_API_KEY: ${% raw %}{{ secrets.STRIPE_API_KEY }}{% endraw %}` — renders correctly on the site, but the **raw Markdown** shows literal Liquid tags; copy-pasted from GitHub's raw view it yields an invalid, silently-non-functional Actions expression.

## 🐞 Issues Found

Every item below cites a command actually run in the sealed sandbox (`tested`) or an exact quoted line from the quest source (`reasoned`). These are for a content pass to act on — I make **no** edits.

- **HIGH · The Cartographer · Chapter 1, `triage.sh` step 2 (lines 120–136)** · *tested* — The "minimal page against the bare theme" build is not isolated: `diff build-product.log build-minimal.log` = 249/249 near-identical lines because step 2 adds one page to the SAME full site (same `_config.yml`, layouts, includes, CSS) and rebuilds. The central objective "Reproduce the platform bug in isolation, removing your repo's customizations as variables" is not delivered. **Fix:** build the minimal page from a *separate* temp directory with only a minimal `_config.yml` + `remote_theme:` and no product customizations.
- **HIGH · The Cartographer · Chapter 1, SHA-pinning guidance (lines 142–148)** · *tested* — "Run `bundle exec gem contents jekyll-remote-theme` … then check the theme's working copy under your cache" is wrong: `gem contents` lists only the plugin's own source, and the theme is fetched to a `Dir.mktmpdir` deleted after each build — no cache exists. **Fix:** drop routes 1–2; keep only the upstream-commit-history route, or add `jekyll build --verbose` + grep for `Downloading … zip/<ref>`.
- **HIGH · Testing Integration · Chapter 2, "Define the Three Test Scripts"** · *tested* — After `npm pkg set`, `npm run test:unit` fails with `Could not find '.../test/unit'`; the quest never creates `test/unit/` or moves `total.test.js` into it, yet claims the scripts "run locally exactly as the CI jobs invoke them." **Fix:** instruct learners to create `test/unit|integration|e2e` and move/copy `total.test.js` into `test/unit/` (updating its import path) before that claim.
- **HIGH · Deployment Pipelines · Cloud Realms Path, docker build snippet** · *tested* — `docker build -t myapp:$(git rev-parse --short HEAD) .` fails (`no such file or directory: Dockerfile`) as literally written in an empty repo. **Fix:** provide a minimal inline Dockerfile before the command, or a callout that one must already exist.
- **MEDIUM · Testing Integration · Chapter 3, flaky-test reporter** · *tested* — `npm run test:unit -- --test-reporter=tap` errors (`Could not find '.../--test-reporter=tap'`) because the flag lands after the path arg. **Fix:** bake `--test-reporter=tap` into the script definition (`node --test --test-reporter=tap test/unit`) or show the flag correctly placed.
- **MEDIUM · Deployment Pipelines · Mastery Challenges (Intermediate/Advanced)** · *reasoned* — Challenges ask learners to "build" a gated pipeline and "add" automated rollback, but `deploy.sh`, `smoke-test.sh`, `health-check.sh`, `rollback.sh`, `rollback.yml` are referenced and never scaffolded. **Fix:** embed minimal example/stub contents so the challenge is concretely completable.
- **MEDIUM · Secrets Management · Chapter 1 YAML (line 234)** · *tested/source* — `${% raw %}{{ secrets.STRIPE_API_KEY }}{% endraw %}` shows literal Liquid tags in raw Markdown; copy-pasted from GitHub raw view it's invalid Actions syntax. **Fix:** wrap the whole fenced block in `{% raw %}…{% endraw %}` (as the Cartographer's Chapter 2 correctly does) so the escape never appears inside the copied expression.
- **MEDIUM · Secrets Management · Secondary objectives** · *reasoned* — "Environment Scoping" and "Leak Detection" are listed objectives but never demonstrated (no `environment: production` block; trufflehog/git-secrets appear only as Resources links, though the Novice challenge asks learners to scan for hardcoded credentials). **Fix:** add one worked example each.
- **MEDIUM · Testing Integration · Chapter 2, Postgres service YAML** · *reasoned* — `services: postgres:` omits health-check options, risking the integration job racing an unready DB — ironic in a flakiness chapter. **Fix:** add `--health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5`.
- **LOW · Environment Management · Chapter 2** · *tested* — The intro promises a "tiny app," but `config.js` and `base.yml`/`production.yml` are never wired together into one runnable demo. **Fix:** show `config.js` loading + deep-merging the YAML files by `APP_ENV`.
- **LOW · Deployment Pipelines · promotion story** · *reasoned* — The Cloud Realms comment says "Push once; deploy the identical digest to staging, then production," but the snippet has no `docker push` and only a `:staging` tag. **Fix:** add `docker push` and a `:production` re-tag/push.
- **LOW · Secrets Management · Cloud Realms prerequisites** · *tested* — `aws sts get-caller-identity` hits `NoCredentials` with no prior guidance; **Fix:** note `aws configure`/SSO is required first.
- **LOW · The Cartographer / Testing Integration · setup completeness** · *tested* — Cartographer omits the theme's required plugins from the Gemfile (a from-scratch learner hits unrelated `Unknown tag` errors); Testing Integration's `package.json` lacks `"type": "module"` (recurring `MODULE_TYPELESS_PACKAGE_JSON` warning). Both are prerequisite/hygiene notes, not blockers.

**No fail-verdict, no unsafe command, and no fully-broken quest** was found in this window — the issues above are fixable content bugs, not blockers.

## 🔗 Chain Continuity

**The coherent core (quests 2→5) holds together well.** Testing Integration → Deployment Pipelines → Environment Management → Secrets Management are all from the *DevOps Pipeline Mastery* series / *Gates of the Pipeline* arc, and their declared `quest_dependencies` form a clean DAG the plan order respects: `testing-integration` unlocks `deployment-pipelines`, which unlocks both `environment-management` and `secrets-management`; `environment-management` in turn recommends into `secrets-management`. A learner finishing testing genuinely arrives at deployment with the CI-gating mental model it assumes, and deployment's "Next Steps" point explicitly at the last two. The shared Node.js + GitHub Actions + gh/aws toolchain is consistent across all four.

**Two continuity gaps a real learner would hit:**

1. **The shared hard prerequisite is outside the window.** All four DevOps quests list `/quests/0101/cicd-fundamentals/` as a *required* quest, and it is **not** in this window (this is window 1 of 3, offset 5, so the planner already swept the earlier quests including, presumably, cicd-fundamentals and github-actions-basics). That's expected for a windowed sweep — but worth stating: a learner dropped into this window cold would be missing the assumed CI baseline. The ledger's earlier windows should cover it.
2. **The Cartographer is an interloper in this slice.** It belongs to a *different* campaign — *The Autonomous Realm* / *The Self-Operating Website* (`quest_arc: The Cartographer`), not *Gates of the Pipeline*. Its `required_quests` is empty; it *recommends* Chapter VII at **level 1101** and *unlocks* Chapter IX at **level 1110** — i.e., its real chain lives at other levels, and it only shares level 0101 by tag. Its prerequisites (a "working autonomous repo with named agents," a Ruby/Jekyll toolchain, `bundle exec jekyll build`) are a completely different stack from the Node.js CI/CD quests around it. Walked *first* in plan order, it gives a jarring cold open: a learner is thrown into Jekyll platform-triage before the CI/CD arc even begins, and its own prerequisite chapter isn't anywhere in the slice. This is a planner/taxonomy observation, not a bug in the quest itself — but a maintainer sequencing the 0101 learner path should either group the Self-Operating-Website chapters into their own arc or accept that this level mixes two unrelated journeys.

**Ordering within the core is correct** and no quest silently assumes setup a *prior in-slice* quest failed to provide — the only "missing setup" failures (test/unit folder, Dockerfile, AWS creds) are gaps *within* a single quest, not broken hand-offs between quests.

## 🧠 Reasoning & Method

- **Mode:** `execute`, real sandbox. I did **not** run the engine — per the workflow contract the evidence was pre-computed and sealed into `walk-evidence.json` / `walk-evidence.md` (the engine's child `claude` processes can't authenticate from my Bash tool). I consumed those files verbatim and never edited, regenerated, or hand-wrote them.
- **What I ran myself:** only read-only inspection of the five quest sources and two confirmations — `wc`/line counts, and a `grep` that verified the `{% raw %}` artifact at `secrets-management.md:234`. Every `passed`/`failed` in the Evidence section traces to a command the sealed engine actually ran; every static judgement is labelled `reasoned`.
- **Coverage & limits:** This is **window 1 of 3** of a 13-quest level — I walked exactly the 5 planned quests and did **not** expand beyond them; `cicd-fundamentals` and other earlier quests are covered by other windows/ledger runs. Snippet coverage varied by quest (Cartographer 11/12, Testing 7/13, Deployment 5/15, Environment 6/9, Secrets 8/10); the low-ratio quests are dominated by **OS-specific blocks skipped** on a Linux sandbox (macOS/Homebrew, Windows/winget/PowerShell) and **reasoned-only** artifacts (Terraform with no offline install, GitHub Actions YAML that can't run outside real Actions, ASCII diagrams). Those skips are honest environment limits, not evasions.
- **Confidence:** High on the four hands-on HIGH/MEDIUM bugs (each reproduced by a real command with quoted output). High on the chain-continuity findings (derived directly from declared `quest_dependencies` frontmatter I read). Medium on the reasoned-only items (Postgres health check, rollback scripts, Terraform) — flagged as `reasoned`, not `tested`, exactly because no renderer/executor confirmed them.
- **Deliverable:** this one report. I made zero content edits and performed no git actions — the workflow handles that.
