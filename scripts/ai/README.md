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

Roles live in `.claude/agents/*.md`; procedures in `.claude/skills/` (the new
`content-curator` skill composes the existing `cms-curator` + `brand-voice`
skills). Brand is anchored by `_data/brand/*` and enforced cheaply by
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
   gh variable set CONTENT_FACTORY_ENABLED   --body true --repo bamr87/it-journey
   gh variable set CONTENT_REVIEW_ENABLED    --body true --repo bamr87/it-journey
   gh variable set CONTENT_AUTOMERGE_ENABLED --body true --repo bamr87/it-journey
   gh variable set AGENT_AUDIT_ENABLED       --body true --repo bamr87/it-journey
   gh variable set QUEST_FORGE_ENABLED       --body true --repo bamr87/it-journey
   ```

   With `QUEST_FORGE_ENABLED` on, label any epic-quest proposal issue `epic-quest`
   (or comment `/forge-quest`) to forge it into a quest-campaign PR. Locally, the
   same procedure runs via the `/forge-quest <issue#>` prompt-agent.

Recommended ramp: turn on `CONTENT_FACTORY_ENABLED` + `CONTENT_REVIEW_ENABLED`
first, watch a few PRs, then enable `CONTENT_AUTOMERGE_ENABLED` once you trust the
output. Add the `needs-human` label to any PR to force manual review.

## Guardrails (how drift is minimized)

- **Deterministic gate** — `brand_lint` blocks spelling drift before merge.
- **Smuggle guard** — an `auto:content` PR that touches infra/config/deps is
  routed to a human, never auto-merged.
- **Agent hard rules** — every agent is content-only and never merges; the
  honesty rule forbids invented commands/output/links.
- **Meta audit** — `agent-audit` keeps the agents/skills accurate to the repo.
- **Kill switches** — every AI workflow gates on its `*_ENABLED` variable + auth,
  so the fleet is off until you opt in and stops the instant you unset a variable.
