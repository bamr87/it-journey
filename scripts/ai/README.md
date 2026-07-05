# IT-Journey AI runner & content fleet

This directory holds the **one place AI is wired** for the repo. Everything that
calls a model — every workflow agent step and every skill — goes through
`run.sh`, which reads `_data/ai.yml` for the model and runs **Claude Code first**
(the full agent, authed by `CLAUDE_CODE_OAUTH_TOKEN`), falling back to the Claude
API (`api_call.py` → `scripts/lib/ai_client.py`) only if the CLI is missing/fails
and an `ANTHROPIC_API_KEY` is present. Ported from lifehacker.dev so the sibling
sites share one agentic convention.

```
scripts/ai/run.sh          # universal runner (Claude Code → API fallback)
scripts/ai/api_call.py     # single-shot API fallback
_data/ai.yml               # model + budget (claude-opus-4-8)
.github/actions/claude-run # the composite CI step every AI workflow uses
```

## The content fleet (continuous, on-brand improvement)

| Workflow | Trigger | Agent | What it does | Gate variable |
|---|---|---|---|---|
| `content-factory.yml` | daily 08:00 UTC | `content-curator` | improves one page per collection from the `.cms` worklist, opens one `auto:content` PR each | `CONTENT_FACTORY_ENABLED` |
| `content-review.yml` | content PR opened | `content-reviewer` | editorial pass: small on-brand fixes + comments | `CONTENT_REVIEW_ENABLED` |
| `content-quality.yml` | content PR | _(none — deterministic)_ | `brand_lint` gate; **spelling drift fails the check** | _(always on)_ |
| `content-auto-merge.yml` | `auto:content` PR | _(none)_ | smuggle-guard (content-only) + checks green → squash-merge | `CONTENT_AUTOMERGE_ENABLED` |
| `quest-forge.yml` | issue labeled `epic-quest`, `/forge-quest` comment, dispatch | `quest-forge` | reads an epic-quest **proposal issue**, collects it deterministically (`scripts/quest/forge_issue.py`), authors a full `epic_quest` hub + `bonus_quest` chapters in `pages/_quests/codex/`, validates (`make quest-audit`), opens one `auto:content`+`auto:quest` PR | `QUEST_FORGE_ENABLED` |
| `quest-idea-intake.yml` | issue labeled `quest-idea` (the portal's issue form), `/refine` comment, dispatch | `idea-refiner` | reviews a **Quest Idea Forge** submission (portal: `/quests/ideas/`): deterministic floor first (`scripts/quest/idea_intake.py` — rubric score, spam flags, duplicate radar), then one review comment + one `idea:ready`/`idea:needs-detail`/`idea:declined` label; never closes, never escalates — a human promotes a ready idea with the `epic-quest` label | `QUEST_IDEA_ENABLED` |
| `agent-audit.yml` | weekly Mon 06:00 | `agent-auditor` | tightens the fleet for drift / least-privilege | `AGENT_AUDIT_ENABLED` |

The **issue→quest** lane closes the loop with lifehacker.dev: its quest-forge hook
*files* a proposal issue here (e.g. [#365](https://github.com/bamr87/it-journey/issues/365)),
and `quest-forge.yml` *consumes* it into a published quest campaign. The output PR
reuses the existing content gates (quest-validation, content-quality,
content-review, agentic-quest-review, build) and the same content-only smuggle
guard, so a forged campaign is reviewed and merged exactly like any content PR —
human still holding the merge button.

## The issue autopilot (analyze open issues → grouped resolution PRs)

The issue-side analogue of the content fleet. A deterministic engine
(`scripts/issues/triage.py`) classifies every open issue into a **disposition**
and groups them into PR-sized **batches**; `scripts/issues/dispatch.py` applies
backpressure (`.issues/budget.yml`) so the loop never buries the reviewer. See
[`.issues/README.md`](../../.issues/README.md) for the full data-layer contract.

| Workflow | Trigger | Agent | What it does | Gate variable |
|---|---|---|---|---|
| `issue-autopilot.yml` (triage) | daily 07:00 UTC + `autopilot:go` label | `issue-triager` | comment a triage plan, label, close **bot-noise only** | `ISSUE_AUTOPILOT_ENABLED` |
| `issue-autopilot.yml` (resolve) | (same run) | `issue-resolver` | turn one batch into one `auto:issue` PR (`Closes #N`) | `ISSUE_RESOLVE_ENABLED` (+ master) |
| `issue-pr-auto-merge.yml` | `auto:issue` PR | _(none)_ | smuggle-guard (content-only) + checks green → squash-merge | `ISSUE_AUTOMERGE_ENABLED` |

Closing bot-noise is double-gated on `ISSUE_AUTOCLOSE_ENABLED`; a **human-authored
issue is never auto-closed** (the engine downgrades it to `needs-human`).

## The quest walkthrough (end-to-end validation → report)

The validation arm of the fleet: instead of improving content, it *plays* the
curriculum to find out whether it actually works. A deterministic planner
(`scripts/quest/walkthrough_plan.py`) picks ONE coherent slice — a character class
at a binary level, date-rotated so a daily run sweeps everything over time — and
resolves its **linked, dependency-ordered set of quests** from the same data the
site renders from (`_data/quests/network.yml` + `paths.yml`). The `quest-walker`
agent then walks that set **end-to-end in the disposable runner sandbox as if it
were a learner**, running quest commands for real via the existing execute engine
(`test/quest-validator/agentic_validate.py`), and writes ONE evidence-based session
report (evidence, issues, reasoning) to `test/quest-validator/walkthroughs/`.

| Workflow | Trigger | Agent | What it does | Gate variable |
|---|---|---|---|---|
| `quest-walkthrough.yml` | dispatch only (the daily sweep is `quest-perfection.yml`) | `quest-walker` | plays one linked (character, level) quest slice end-to-end in a sandbox, opens one report PR (`quest-walkthrough` label) for human review | `QUEST_WALKTHROUGH_ENABLED` |

The evidence is **workflow-minted**: a deterministic workflow step runs the agentic
engine (its child `claude` processes authenticate from the job env — Claude Code
scrubs auth env vars from Bash-tool subprocesses, so an engine launched inside an
agent auth-aborts), seals `walk-plan.json`/`walk-evidence.*`, and restores them
after the agent step, so the walker can only *consume* evidence, never write it.
The procedure is the **`quest-walkthrough`** skill (plan → execute → walk the chain →
one report); locally the same loop runs via `make quest-walkthrough`
(`make quest-walkthrough-plan` previews the slice with no AI/cost). The agent is
read-only over content — it **never edits a quest and never merges**; fixable bugs
land in the report's issues section for a content pass or a human. Each run also
uploads **session screenshots** — every walked quest's rendered page (mobile +
desktop) plus a terminal render of its recorded command transcript
(`scripts/quest/walkthrough_screenshots.mjs`) — as run artifacts for review. See
[`test/quest-validator/walkthroughs/README.md`](../../test/quest-validator/walkthroughs/README.md)
for the report contract.

## The quest-perfection loop (walk → fix → ledger, until perfect)

The walkthrough arm only *witnesses* where the curriculum breaks; the perfection
loop closes that gap by *repairing* it, autonomously, until every (character,
level) slice is perfect. A daily orchestrator (`quest-perfection.yml`) fans out
over all six character paths and, per path, picks the highest-priority
not-yet-perfect slice from the committed ledger.

**Rotating window (why a run stays bounded).** A level can hold 20–30 quests;
walking them all in one run runs the engine for hours and exhausts the OAuth
token's rate limit (the 2026-07-05 run auth-failed 5/6 slices doing exactly
this). So the loop walks a **rotating window** of `caps.max_quests_per_slice`
quests (`.quests/budget.yml`, default 5) per slice per run — `walkthrough_plan.py
--window N`, rotated by date so following days sweep the rest. The ledger
**accumulates per-quest coverage across runs** (`slice.coverage`, keyed by quest
path) and certifies a slice `perfect` only once the *whole* level is covered,
every quest execute-mode + passing, within a freshness window
(`perfect.coverage_days`). A re-walk overwrites a quest's prior verdict, so a
fix that flips fail→pass sticks; the circuit breaker only counts a fully-covered
slice that stays imperfect (a mid-sweep run is progress, not a failed round).

- **Walk arm** — the orchestrator's `slice` job plays each selected slice: a
  deterministic engine step mints sealed evidence, the `quest-walker` agent writes
  the session report, and a consolidated `report` job replays every slice into the
  ledger (`scripts/quest/ledger.py update` recomputes "perfect" — which requires an
  honest `execute`-mode, non-truncated, fully-scored run) and opens **ONE**
  walkthrough+ledger PR per run (per-slice PRs would carry sibling ledger deltas
  that conflict with each other).
- **Fix arm** — `quest-fix.yml` runs the `quest-fix` agent over that slice's
  *verified* issues, keeping an edit **only** when a deterministic signal improves
  (tier-1 structural score holds/rises **and** `brand_lint` stays clean **and** no
  sandbox command regresses) — never because the model graded its own work up. It
  opens a **separate** content-only fix PR (`auto:content` + `auto:quest-fix` +
  `automated`), runs `make quest-data` (failing on uncommitted `_data/quests`
  drift), refuses to touch vendored (`source_repo`/`source_url`) quests, and
  hard-fails without a PAT so the PR's required checks actually fire.
- **Ledger** — `scripts/quest/ledger.py` is the one deterministic source of truth
  (`.quests/ledger.json`, committed; `.quests/DASHBOARD.md` generated). It tracks
  per-slice state, `fix-update` bumps a fix round without ever certifying perfect,
  and a circuit breaker marks a slice `needs_human` after `max_fix_rounds` (default
  3) fixes that never reached perfect. Ledger commits ride the **walkthrough report
  PR**, never the fix PR (which is content-only).

Staged kill switches (all OFF): `QUEST_PERFECTION_ENABLED` (the orchestrator),
`QUEST_FIX_ENABLED` (the write/fix lane), with the existing
`QUEST_WALKTHROUGH_ENABLED` (walk arm) and `CONTENT_AUTOMERGE_ENABLED` (gates the
fix PR through `content-auto-merge.yml`). Locally: `make quest-perfection-plan`,
`make quest-fix CHARACTER=… LEVEL=…`, `make quest-ledger-dashboard`.

**Safety note:** `result.verdict_obj.executed` is model-supplied, so fully
hands-off auto-merge of *fix* PRs stays gated (behind `CONTENT_AUTOMERGE_ENABLED`)
until a harness-stamped execution proof exists — even though the loop already
requires execute mode + a non-truncated run to certify perfect.

## The frontend canary (theme bugs → upstream)

| Workflow | Trigger | Agent | What it does | Gate variable |
|---|---|---|---|---|
| `theme-scout.yml` | weekly Tue 06:00 | `theme-scout` | a Playwright crawler tests the **it-journey.dev** frontend; the agent files **theme** bugs (site-wide / theme-injected) upstream to `bamr87/zer0-mistakes`, deduped | `THEME_SCOUT_ENABLED` (+ `THEME_REPO_TOKEN`) |

it-journey.dev consumes the theme via `remote_theme`, so it's a live canary: the
deterministic `scripts/frontend/crawl.mjs` + `triage_findings.py` find site-wide
defects (e.g. 404s on theme-injected `/tags/`, `/search.json`), and the
`theme-scout` agent reports them to the theme repo. See [`.frontend/README.md`](../../.frontend/README.md).

Roles live in `.claude/agents/*.md`; procedures in `.claude/skills/` (the
`content-curator` skill composes `cms-curator` + `brand-voice`; the `issue-triage`
skill drives the issue-triager + issue-resolver; the `theme-scout` skill drives
the frontend canary; the `quest-walkthrough` skill drives the quest-walker). Brand is anchored by `_data/brand/*` and enforced cheaply by
`scripts/ci/brand_lint.py`; the auto-merge guard is `scripts/ci/classify_changes.py`.

## Setup (required to turn it on)

The whole fleet is **OFF by default** and idles silently until you do both:

1. **Add the auth secret** — on a machine logged into Claude:
   ```bash
   claude setup-token         # prints a Claude Code OAuth token
   gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo bamr87/it-journey
   ```
   (Optional: `gh secret set ANTHROPIC_API_KEY …` to enable the API fallback.)

2. **Flip the kill-switches** you want on (repo variables):
   ```bash
   # content fleet
   gh variable set CONTENT_FACTORY_ENABLED   --body true --repo bamr87/it-journey
   gh variable set CONTENT_REVIEW_ENABLED    --body true --repo bamr87/it-journey
   gh variable set CONTENT_AUTOMERGE_ENABLED --body true --repo bamr87/it-journey
   gh variable set AGENT_AUDIT_ENABLED       --body true --repo bamr87/it-journey
   # quest forge
   gh variable set QUEST_FORGE_ENABLED       --body true --repo bamr87/it-journey
   # quest idea intake (the /quests/ideas/ portal's reviewer)
   gh variable set QUEST_IDEA_ENABLED        --body true --repo bamr87/it-journey
   # one-time: issue forms only apply labels that already exist, so create the
   # trigger label BEFORE flipping the variable or early submissions go unreviewed
   gh label create quest-idea --color F9D0C4 \
     --description "Community quest idea from the Quest Idea Forge portal" \
     --repo bamr87/it-journey
   # issue autopilot
   gh variable set ISSUE_AUTOPILOT_ENABLED   --body true --repo bamr87/it-journey
   gh variable set ISSUE_RESOLVE_ENABLED     --body true --repo bamr87/it-journey
   gh variable set ISSUE_AUTOCLOSE_ENABLED   --body true --repo bamr87/it-journey
   gh variable set ISSUE_AUTOMERGE_ENABLED   --body true --repo bamr87/it-journey
   # frontend canary
   gh variable set THEME_SCOUT_ENABLED       --body true --repo bamr87/it-journey
   # quest walkthrough (end-to-end validation)
   gh variable set QUEST_WALKTHROUGH_ENABLED --body true --repo bamr87/it-journey
   ```

   The theme scout also needs a cross-repo PAT to file upstream:
   ```bash
   gh secret set THEME_REPO_TOKEN --repo bamr87/it-journey   # issues:write on zer0-mistakes
   ```

   With `QUEST_FORGE_ENABLED` on, label any epic-quest proposal issue `epic-quest`
   (or comment `/forge-quest`) to forge it into a quest-campaign PR. Locally, the
   same procedure runs via the `/forge-quest <issue#>` prompt-agent.

Recommended ramp: turn on `CONTENT_FACTORY_ENABLED` + `CONTENT_REVIEW_ENABLED`
first, watch a few PRs, then enable `CONTENT_AUTOMERGE_ENABLED` once you trust the
output. For the issue autopilot, ramp the same way: `ISSUE_AUTOPILOT_ENABLED`
(triage + comments only) first; then `ISSUE_AUTOCLOSE_ENABLED` (lets it close
bot-authored review noise); then `ISSUE_RESOLVE_ENABLED` (lets it open resolution
PRs); finally `ISSUE_AUTOMERGE_ENABLED` (hands-off merge of content-only ones).
Add the `needs-human` label to any PR or issue to force manual handling.

## Guardrails (how drift is minimized)

- **Deterministic gate** — `brand_lint` blocks spelling drift before merge.
- **Smuggle guard** — an `auto:content` / `auto:issue` PR that touches
  infra/config/deps is routed to a human, never auto-merged.
- **Never close a human's issue** — the issue autopilot can only auto-close
  bot/automation-authored noise (and only when `ISSUE_AUTOCLOSE_ENABLED`); the
  deterministic engine downgrades any human-authored "close" match to `needs-human`.
- **Agent hard rules** — every agent is content-only and never merges; the
  honesty rule forbids invented commands/output/links.
- **Meta audit** — `agent-audit` keeps the agents/skills accurate to the repo.
- **Kill switches** — every AI workflow gates on its `*_ENABLED` variable + auth,
  so the fleet is off until you opt in and stops the instant you unset a variable.
- **Policy as data** — the fleet roster (`_data/agents/registry.yml`: lane, kill
  switch, status, review date per agent) and the autonomy matrix
  (`_data/agents/autonomy-matrix.yml`: recurring action → L0–L4 level + the
  guardrails that justify it) are the machine-readable contract the weekly
  audit checks reality against; the forbidden-actions Warden Pact lives in
  `AGENTS.md`.
- **Drift guard** — `scripts/ai/drift-guard.sh` snapshots watched files at plan
  time and aborts (exit 78) before an agent acts on a world that changed while
  it waited; `scripts/ai/mcp/` holds committed MCP server configs (tokens come
  from the environment, allow-lists at the `run.sh --tools` call site). Both are
  demonstrated end-to-end by `.github/workflows/agent-plan-then-act.yml` — the
  GH-600 reference pipeline, mapped in `/notes/gh-600/implemented-in-it-journey/`.
