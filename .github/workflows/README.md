# GitHub Actions Workflows

This directory holds every CI/CD and automation workflow for IT-Journey. This
README is the **inventory + map**; each workflow file has a header comment with
its own rationale.

> Keep this file in sync when you add, remove, or repurpose a workflow.

## Conventions (all workflows)

- **Least privilege.** Default `permissions: contents: read`; write is granted
  only on the job that needs it.
- **Pinned actions.** Third-party actions are pinned to a full commit SHA;
  [Dependabot](../dependabot.yml) keeps them current.
- **Concurrency.** Each workflow declares a `concurrency:` group. Fast PR checks
  cancel in-progress runs; mutating/long jobs (auto-merge, CMS loop, contributor
  refresh) use `cancel-in-progress: false`.
- **Untrusted input.** `github.event.*` values are passed through `env:`, never
  interpolated directly into `run:`.
- **AI is opt-in.** Every Claude-powered workflow gates on a `*_ENABLED` repo
  variable **and** the `CLAUDE_CODE_OAUTH_TOKEN`/`ANTHROPIC_API_KEY` secret, so
  nothing AI runs until both are present (see `scripts/ai/README.md`).

## Inventory

### Build & validation (PR gates)

| Workflow | Triggers | What it does |
|---|---|---|
| `build-validation.yml` | PR + push on build inputs; dispatch | Jekyll build (CI-parity) on every relevant change. The **Docker build** and the **3-OS cross-platform matrix** only run when `Gemfile`/`Dockerfile`/`docker-compose.yml` change or on manual dispatch — a `detect-changes` job gates them so content-only pushes don't spin up Windows/macOS runners. |
| `frontmatter-validation.yml` | PR on `pages/**/*.md`; dispatch | Validation-only gate. Runs the canonical `scripts/validation/frontmatter-validator.py` (same code as `make content-validate`) on changed **non-quest** pages, plus the Mermaid-flag check, and comments results on the PR. Mechanical auto-fixing lives in `cms-daily-loop.yml`, not here. |
| `quest-validation.yml` | PR/push on `pages/_quests/**`; weekly; dispatch | Quest content scoring (≥70%), network integrity, and stale generated-data check (the weekly/push full audit runs the unified Docker audit = `make docker-validate`). |
| `validate-solutions.yml` | PR/push on `test/quest-solutions/**` (main/master); dispatch | Structural validation of quest solution fixtures. |
| `codeql-analysis.yml` | push/PR to main (code paths only); weekly | CodeQL security analysis (JavaScript, Python, Ruby). Push/PR runs skip content-only diffs (`pages/**`, `**/*.md`, `_data/**`, `assets/images/**`); the weekly cron always runs a full scan. |

### Content quality & AI fleet (opt-in)

These implement the AI-augmented CMS described in the root `CLAUDE.md` and
`scripts/ai/README.md`.

| Workflow | Triggers | What it does |
|---|---|---|
| `agent-plan-then-act.yml` | dispatch (gated) | **The GH-600 reference pipeline.** A deterministic plan job → `agent-approval` Environment (required-reviewer human gate) → execute job with an artifact-carried plan, a `scripts/ai/drift-guard.sh` verify, a threaded correlation ID, and an audit artifact (instruction → action → outcome). Teaching-grade demo of the control plane the whole fleet shares; no model call, no auth needed. OFF behind `AGENT_DEMO_ENABLED`. Mapped in `/notes/gh-600/implemented-in-it-journey/`. |
| `content-quality.yml` | PR on content | Deterministic brand lint (`scripts/ci/brand_lint.py`). **Spelling drift fails** the check; hype terms warn. No AI, no cost. |
| `content-review.yml` | PR on content (gated) | `content-reviewer` agent editorial pass; applies small on-brand fixes, posts bigger ideas as comments. Never merges. |
| `content-factory.yml` | daily 08:00 UTC (gated) | `content-curator` improves one page per collection from the `.cms` worklist → one `auto:content` PR each. |
| `content-auto-merge.yml` | labeled PR events (gated) | **The single label-routed auto-merge lane** (absorbed `issue-pr-auto-merge.yml` and `quest-report-auto-merge.yml`). Routes by label — `auto:content` (content-only diff, `CONTENT_AUTOMERGE_ENABLED`), `auto:issue` (same-repo + resolver scope, `ISSUE_AUTOMERGE_ENABLED`; merging closes the linked issues), `automated`+`quest-walkthrough` (report/ledger paths, `QUEST_REPORT_AUTOMERGE_ENABLED`) — then smuggle-guard (`scripts/ci/classify_changes.py`) + all checks green → squash-merge. |
| `cms-daily-loop.yml` | daily 09:00 UTC; dispatch | **Lane A** deterministic normalization (`make content-normalize-apply`, free) → PR; **Lane B** (gated) agentic `cms-curator` pass → PR for review. |
| `agentic-quest-review.yml` | dispatch; PR on quests; `agentic-review` label | Agentic quest review/execute (`test/quest-validator/agentic_validate.py`); spend-capped per run **and converged per PR**: a sticky-comment ledger skips quests whose last score ≥ `AGENTIC_REVIEW_SCORE_EXEMPT` (default 85) and stops after `AGENTIC_REVIEW_MAX_RUNS` automatic passes (default 3); the label/dispatch bypasses both. |
| `quest-walkthrough.yml` | daily 10:00 UTC; dispatch (gated) | **End-to-end quest validation.** The `quest-walker` agent picks one linked (character, level) quest slice via `scripts/quest/walkthrough_plan.py`, plays it end-to-end in the runner sandbox as a learner (execute engine: `agentic_validate.py`), and opens one report PR (evidence/issues/reasoning) under `test/quest-validator/walkthroughs/`. Also uploads **session screenshots** (each walked quest's rendered page mobile+desktop + a terminal render of the recorded transcript, via `scripts/quest/walkthrough_screenshots.mjs`) as run artifacts. Read-only over content; never merges. OFF behind `QUEST_WALKTHROUGH_ENABLED`. |
| `agent-audit.yml` | weekly; dispatch (gated) | `agent-auditor` checks the AI fleet (`.claude/agents`, skills, workflows) for drift; opens at most one tightening PR. |
| `theme-scout.yml` | weekly Tue 06:00; dispatch (gated) | **Frontend canary.** A Playwright crawler (`scripts/frontend/crawl.mjs`) tests **it-journey.dev** (mobile + desktop); `triage_findings.py` classifies findings theme-vs-content + dedups; the `theme-scout` agent files **theme** bugs (site-wide / theme-injected, e.g. `/tags/` 404s) upstream to `bamr87/zer0-mistakes`. OFF behind `THEME_SCOUT_ENABLED` + `THEME_REPO_TOKEN` (cross-repo PAT). |
| `quest-forge.yml` | issue labeled `epic-quest`; `/forge-quest` comment; dispatch (gated) | `quest-forge` agent reads an epic-quest **proposal issue**, collects it deterministically (`scripts/quest/forge_issue.py`), authors an `epic_quest` hub + `bonus_quest` chapters in `pages/_quests/codex/`, runs `make quest-audit`, and opens one `auto:content`+`auto:quest` PR. Never merges. |
| `quest-perfection.yml` | daily; dispatch (gated) | **The autonomous quest-perfection orchestrator.** For every character path, selects the highest-priority not-yet-perfect (character, level) slice from the committed ledger (`scripts/quest/ledger.py select`), drives the walk arm (`quest-walkthrough.yml`) + fix arm (`quest-fix.yml`), and updates `.quests/ledger.json` + the generated `.quests/DASHBOARD.md` — repeating "until perfect" (a circuit breaker marks a slice `needs_human` after `max_fix_rounds`). OFF behind `QUEST_PERFECTION_ENABLED`. |
| `quest-fix.yml` | reusable / dispatch (gated) | **The fix lane** (inverse of the walkthrough). The `quest-fix` agent repairs only a walkthrough's *verified* issues under a deterministic keep/revert gate (tier-1 score + `brand_lint` + sandbox commands — never the model's own grade), runs `make quest-data` (fails on uncommitted `_data/quests` drift), refuses vendored (`source_repo`/`source_url`) quests, and hard-fails without a PAT (`AUTO_PR_GITHUB_TOKEN`/`PAT_TOKEN`) so required checks fire. Opens one **content-only** fix PR (`auto:content` + `auto:quest-fix` + `automated`); the ledger never rides this PR. OFF behind `QUEST_FIX_ENABLED`. |

### Scheduled maintenance & generation

| Workflow | Triggers | What it does |
|---|---|---|
| `dependency-checker.yml` | push on `Gemfile*`; weekly; dispatch | **Security-only**: `bundler-audit`, outdated-gem report, workflow-YAML lint, and a single deduped tracking issue. Build/Docker compatibility is owned by `build-validation.yml`. |
| `link-checker.yml` | PR on `*.md`/`*.html`; twice weekly; dispatch | Incremental link check on PRs; full Link Health Guardian sweep on schedule. |
| `sync-github.yml` | daily; dispatch; on script change | Regenerates GitHub-derived site data (`scripts/generation/sync_github.py`). |
| `update-contributor-profiles.yml` | **weekly** (Mon 05:00 UTC); dispatch | Refreshes `_data/contributors/*.yml`. (Previously ran on every push to main — now weekly, since the stats barely move per-commit.) |

### Issue / PR automation

| Workflow | Triggers | What it does |
|---|---|---|
| `issue-autopilot.yml` | daily 07:00 UTC; dispatch; `autopilot:go` label (gated) | **The issue autopilot loop.** Deterministic engine (`scripts/issues/triage.py`) classifies every open issue + groups into batches; `issue-triager` comments a plan, labels, and closes **bot-noise only** (never a human's issue, double-gated on `ISSUE_AUTOCLOSE_ENABLED`); `issue-resolver` turns one batch into one `auto:issue` PR (`Closes #N`), backpressured via `scripts/issues/dispatch.py` + `.issues/budget.yml`. OFF behind `ISSUE_AUTOPILOT_ENABLED` (+ `ISSUE_RESOLVE_ENABLED` for the PR lane). Green `auto:issue` PRs merge via the `auto:issue` policy in `content-auto-merge.yml`. |
| `quest-forge.yml` | issue labeled `epic-quest`; `/forge-quest` comment; dispatch (gated) | Forges an epic-quest **proposal issue** into a quest-campaign PR (see the AI fleet table above). |
| `dependabot-auto-merge.yml` | Dependabot PRs | Enables auto-merge for passing Dependabot PRs. |

## Required vs advisory checks

Mark these as **required status checks** in branch protection for `main`
(Settings → Branches / Rulesets). They block merge:

| Required check | Workflow (job) |
|---|---|
| Jekyll build (CI-parity) | `build-validation.yml` (`🏗️ Jekyll Build Test`) |
| Quest content + network + stale-data | `quest-validation.yml` |
| Frontmatter validation | `frontmatter-validation.yml` (`validate-frontmatter`) |
| Content brand lint | `content-quality.yml` |
| CodeQL | `codeql-analysis.yml` — **caveat:** now path-filtered to code diffs, so only mark it required if content-only PRs are exempted (a required check that never starts blocks the merge) |

**Advisory** (run but non-blocking): `link-checker.yml` (PR incremental),
`content-review.yml`, `agentic-quest-review.yml`, and the scheduled
`dependency-checker.yml` security scan.

Also enable **"Require review from Code Owners"** (see [CODEOWNERS](../CODEOWNERS)).

## Deployment

The production site (`it-journey.dev`) is served by **GitHub Pages** in legacy
**"Deploy from a branch"** mode: Pages builds Jekyll from the **`gh-pages`**
branch (source, not `_site`) and publishes it. That Pages build (shown as
**"pages build and deployment"**) is the only thing that should ever run when
`gh-pages` changes.

`sync-gh-pages.yml` keeps `gh-pages` in sync automatically, replacing the old
manual "Merge main into gh-pages" PRs:

| Workflow | Triggers | What it does |
|---|---|---|
| `sync-gh-pages.yml` | 2×/day (02:20, 14:20 UTC); dispatch | **Routine deploy sync.** If `main` is ahead of `gh-pages` **and** main's latest commit is fully green (all check-runs + commit statuses passed), it opens a PR from `main` into `gh-pages` and merges it (merge commit). Pages then builds `gh-pages`. Reads main's already-finished CI — **no reruns, no waiting**. Does nothing if gh-pages is up to date or main is pending/red. |

`gh-pages` is a pure mirror of `main` (kept in lockstep by this workflow), so
the PR is always a clean, conflict-free merge. If the branches ever diverge,
re-run the one-time reconciliation: merge `main` into `gh-pages` with `-X theirs`
(main authoritative) so their trees match again.

Guarantees behind "only the Pages build runs on a `gh-pages` update":

1. Every push-triggered workflow is scoped to `main`/`master` (this is why
   `validate-solutions.yml` — previously branchless — is now branch-guarded).
2. The merge is performed with `GITHUB_TOKEN`, whose pushes do not start new
   Actions runs; the legacy Pages build is a Pages-service job, not an Actions
   workflow, so it still fires on the branch update.

Operational notes:

- Scheduled/dispatch runs resolve this file **from `main`**, so it only takes
  effect once merged to `main`.
- Trigger it on demand from the Actions tab (`workflow_dispatch`) to publish
  immediately instead of waiting for the next scheduled tick (02:20/14:20 UTC).
- **Prefer the default `GITHUB_TOKEN`** (used automatically): its pushes create
  no Actions runs at all, so the `gh-pages` update stays Pages-build-only. An
  optional `GH_PAGES_DEPLOY_TOKEN` secret (a PAT with `contents:write`) is used
  if present — only set it if the legacy Pages build ever fails to fire from a
  `GITHUB_TOKEN` push. A PAT push, unlike `GITHUB_TOKEN`, makes GitHub
  re-evaluate the workflow files now mirrored on `gh-pages`, which can log a
  harmless startup-failure for reusable-workflow files (e.g. `quest-perfection`);
  branch-scoping still keeps the real CI workflows from running.
- If you migrate to "Deploy from GitHub Actions", replace this workflow with an
  `actions/deploy-pages` workflow and update this section.

## Contributing

1. Test workflow changes in a fork or via `workflow_dispatch` first.
2. Keep the least-privilege / SHA-pin / concurrency conventions above.
3. Update this README's inventory in the same PR.
