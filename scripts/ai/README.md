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
the frontend canary). Brand is anchored by `_data/brand/*` and enforced cheaply by
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
   # issue autopilot
   gh variable set ISSUE_AUTOPILOT_ENABLED   --body true --repo bamr87/it-journey
   gh variable set ISSUE_RESOLVE_ENABLED     --body true --repo bamr87/it-journey
   gh variable set ISSUE_AUTOCLOSE_ENABLED   --body true --repo bamr87/it-journey
   gh variable set ISSUE_AUTOMERGE_ENABLED   --body true --repo bamr87/it-journey
   # frontend canary
   gh variable set THEME_SCOUT_ENABLED       --body true --repo bamr87/it-journey
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
