---
applyTo: "TODO/**/*"
description: "Manage TODO/ items as actionable PDCA tasks; integrates with the /wtd agent and TODO hygiene"
date: 2025-12-20T10:05:28.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# TODO Directory Instructions

Rules for managing `TODO/` items in IT-Journey. The `/wtd` agent operates against these structures.

## AI Agent Role

- ✅ Create, prioritize, and update TODO files using the schemas below.
- ✅ Cross-reference TODOs with related quests, posts, scripts.
- ✅ Surface stale or blocked items.
- ❌ Never silently delete tasks; archive with reason instead.
- ❌ Never escalate priority without user confirmation.

## Directory Layout

```
TODO/
├── README.md                # Index; auto-maintained
├── _archive/                # Completed/abandoned items (preserved)
├── projects/                # Multi-task initiatives
│   └── <project-slug>/      # README.md + tasks/*.md
├── critical/                # Single-file urgent items
├── high/                    # Single-file high-priority items
├── medium/                  # Backlog
└── dashboard.md             # Generated status summary
```

## File Naming

| Type | Pattern | Example |
|---|---|---|
| Project | `projects/<slug>/README.md` | `projects/seo-overhaul/README.md` |
| Task | `<priority>/<YYYY-MM-DD>-<slug>.md` | `critical/2026-01-15-fix-broken-links.md` |
| Archive | `_archive/<YYYY-MM>/<original-name>` | `_archive/2026-01/2025-12-…md` |

Slugs: kebab-case, ≤ 40 chars.

## Required Front Matter

```yaml
---
title: "Imperative phrase (≤ 60 chars)"
status: not-started | in-progress | blocked | completed | abandoned
priority: critical | high | medium | low
created: 2026-01-15T09:00:00.000Z
updated: 2026-01-15T09:00:00.000Z
owner: bamr87
project: <slug or empty>
estimate: <S | M | L | XL>           # S<2h, M<1d, L<1w, XL>1w
tags: [tag1, tag2]
blockers: []                          # list of paths or issue URLs
related: []                           # paths to quests/posts/scripts
---
```

## Task Body Structure

```markdown
# <Title>

## Why
<1-3 sentences. Connects to project goal.>

## Definition of Done
- [ ] Specific, observable outcome 1
- [ ] Specific, observable outcome 2

## Plan (PDCA)
- **Plan:** approach in 2-4 bullets
- **Do:** action steps with file paths
- **Check:** how to verify
- **Act:** what to update after (docs, related TODOs)

## Notes
<scratch space — moved to log on completion>
```

## Priority Definitions

| Priority | Criteria |
|---|---|
| **critical** | Site-breaking, security, or hard deadline this week |
| **high** | Blocks ≥1 other task, or commitment this sprint |
| **medium** | Backlog with intent to do within month |
| **low** | Nice-to-have, no deadline |

## Status Definitions

| Status | Meaning |
|---|---|
| `not-started` | Created, not yet picked up |
| `in-progress` | Active work in last 7 days |
| `blocked` | Cannot proceed; `blockers:` must list cause |
| `completed` | Definition of Done satisfied; ready for `_archive/` |
| `abandoned` | Will not pursue; archive with rationale |

## AI Workflows

### Create new TODO

1. Confirm: title, priority, project (or standalone), estimate.
2. Place file under correct directory using naming rules.
3. Populate full front matter + body template.
4. Update `TODO/README.md` index and `dashboard.md`.

### Prioritize backlog

1. Read all front matter under `TODO/`.
2. Surface: critical/high items > 7 days idle, blocked items, missing estimates.
3. Propose re-ordering with rationale; await confirmation.

### Track and report

Update `dashboard.md` with:

```markdown
## Critical Items
| Title | Owner | Updated | Blockers |
|---|---|---|---|

## In Progress
| Title | Priority | Owner | Updated |
|---|---|---|---|

## Recently Completed (last 7 days)
| Title | Closed |
|---|---|

## Blocked
| Title | Blocker | Days blocked |
|---|---|---|
```

## Archival

On `status: completed | abandoned`:

1. Append `## Outcome` section: what was done, links to commits/PRs/docs.
2. Move file to `_archive/<YYYY-MM>/`.
3. Update `TODO/README.md` index.
4. Remove from `dashboard.md` (it auto-regenerates).

Never delete an archived file — they are the project's PDCA history.

## Validation Checks (run before any write)

- [ ] Front matter complete and valid YAML
- [ ] Filename matches priority directory
- [ ] `updated` ≥ `created`
- [ ] If `status: blocked`, `blockers:` non-empty
- [ ] If `status: completed`, body includes `## Outcome`
- [ ] Related paths exist in repo

## Integration with `/wtd` Agent

`.github/prompts/wtd.prompt.md` consumes this structure. Keep schemas in sync — if you add a front-matter field here, update `wtd.prompt.md` to read it.

## Cross-References

- Link to quests: `related: [pages/_quests/1010/<file>.md]`
- Link to commits: `related: [https://github.com/bamr87/it-journey/commit/<sha>]`
- Bidirectional: when a TODO references a quest, the quest's footer may reference the TODO.

## Maintenance Schedule

| Cadence | Action |
|---|---|
| Daily (AI) | Refresh `dashboard.md`, flag stale `in-progress` |
| Weekly | Triage `medium` → promote or close, archive completed |
| Monthly | Audit `_archive/` for lessons → `/retrospective` |

## Hard Rules

- Never bypass priority directories — file location must match `priority:` field.
- Never close a TODO without `## Outcome`.
- Never delete from `_archive/`.
- Never set `status: in-progress` on > 5 tasks at once.

---

**Related:** [`.github/prompts/wtd.prompt.md`](../prompts/wtd.prompt.md) · [`.github/prompts/kaizen.prompt.md`](../prompts/kaizen.prompt.md) · [`.github/prompts/retrospective.prompt.md`](../prompts/retrospective.prompt.md)
