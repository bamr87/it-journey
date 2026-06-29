# IT-Journey Issue Autopilot — the `.issues/` data layer

This directory is the **content layer for the open-issue queue**, the issue-side
analogue of `.cms/`. A deterministic engine reads every open GitHub issue,
classifies each into a **disposition**, groups related issues into **PR-sized
batches**, and emits a dated, bounded worklist. AI agents then act on that plan —
they never re-decide the policy encoded here.

```
.issues/config.yml          # disposition rules + label namespace + safety globs (hand-edited)
.issues/budget.yml          # backpressure caps (max open PRs, batch caps) (hand-edited)
.issues/worklists/<date>.md  # generated — committed on local runs, uploaded as a CI artifact
.issues/reports/<date>.md    # generated — committed on local runs, uploaded as a CI artifact
.issues/index.json           # generated, NOT committed — raw open-issue snapshot
.issues/plan.json            # generated, NOT committed — the machine contract
.issues/dispatch.json        # generated, NOT committed — what this run will resolve
```

## The loop (mirrors `cms-daily-loop`)

1. **Engine** — `scripts/issues/triage.py plan` fetches open issues via `gh`,
   classifies each per `config.yml` (first matching rule wins), groups them into
   batches, and writes `plan.json` + the dated worklist/report. **Read/plan only —
   it never comments, labels, closes, or opens PRs.**
2. **Controller** — `scripts/issues/dispatch.py` observes how many `auto:issue`
   PRs are already open and decides, against `budget.yml`, which resolve batches
   become PRs *this* run (backpressure clamps throughput to human review speed).
3. **Agents** — the `issue-triager` acts on the triage batches (comment, label,
   close bot-noise) and the `issue-resolver` turns one resolve batch into one
   `auto:issue` PR. Both run the `issue-triage` skill.
4. **Workflow** — `issue-autopilot.yml` schedules the loop; `issue-pr-auto-merge.yml`
   merges green content-only `auto:issue` PRs (which closes the linked issues).

## Dispositions (what can happen to an issue)

| Disposition | Trigger (see `config.yml`) | Action |
|---|---|---|
| `close-stale` | bot-authored superseded review noise | comment + `autopilot:stale`; close **iff** bot-authored & `ISSUE_AUTOCLOSE_ENABLED` |
| `close-report` | recurring report issues | comment (recommend roll-up) + `autopilot:stale`; close iff bot-authored & enabled |
| `epic` | large enhancement / tracking issue | comment a decomposition plan + `autopilot:epic`; **keep open** |
| `content` | actionable content work | `autopilot:triaged`; resolver opens an `auto:issue` PR |
| `bug` | actionable code/bug | `autopilot:triaged`; resolver attempts, else escalates to a human |
| `needs-human` | everything else (the default) | `needs-human` + a short read; left for a person |

**Hard guardrail (in code, not config):** a **human-authored** issue can never get
a close disposition — the engine downgrades it to `needs-human`. Only
bot/automation issues are ever auto-closeable, and only when
`ISSUE_AUTOCLOSE_ENABLED` is set.

## Run it locally

```bash
make issue-triage    # build today's worklist/report from the live queue
make issue-status    # quick dashboard (counts by disposition, batches)
make issue-plan      # show what the resolve lane would dispatch this run
```

All three need only Python 3.12 + PyYAML and an authenticated `gh`.

## Turn it on (everything is OFF by default)

See `scripts/ai/README.md` for the full fleet setup. In short: add the
`CLAUDE_CODE_OAUTH_TOKEN` secret, then opt in with repo variables —
`ISSUE_AUTOPILOT_ENABLED` (triage), then `ISSUE_RESOLVE_ENABLED` (open PRs),
then `ISSUE_AUTOCLOSE_ENABLED` (close bot-noise) and `ISSUE_AUTOMERGE_ENABLED`
(hands-off merge) once you trust the output. Add `needs-human` to any PR or issue
to force manual handling.

**One-time: create the label namespace** (the agents `--add-label` these, which
errors if they don't exist):

```bash
R=bamr87/it-journey
gh label create auto:issue        -R $R -c 0e8a16 -d "Autonomous issue-resolution PR (issue autopilot)" || true
gh label create autopilot:triaged -R $R -c ededed -d "Analyzed by the issue autopilot" || true
gh label create autopilot:stale   -R $R -c cccccc -d "Recommended for closing (bot-noise / report)" || true
gh label create autopilot:epic    -R $R -c a2eeef -d "Large issue — decomposed, kept open" || true
gh label create autopilot:go      -R $R -c 5319e7 -d "Human opt-in: resolve this issue now" || true
# `needs-human` and `collection/<name>` already exist from the content fleet.
```
