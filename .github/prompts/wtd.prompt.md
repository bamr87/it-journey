---
mode: agent
description: "What-To-Do agent: work through TODO/ items using PDCA methodology and maintain TODO hygiene"
date: 2025-12-20T10:05:28.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# WTD — What To Do Agent

Pick the next TODO, execute it with PDCA, update state. One task per invocation.

Reads `TODO/` per [`.github/instructions/todo.instructions.md`](../instructions/todo.instructions.md). If that schema changes, this prompt must change with it.

## Intake

1. **Scan** `TODO/` — read all front matter, build current state map.
2. **Ask** (only if unclear):
   - "Continue an `in-progress` task or start a new one?"
   - "Any specific area to focus on (project / priority / tag)?"
3. **Load** context: project README, related quests/posts/scripts named in `related:`.

## PDCA Cycle (one per invocation)

### PLAN — select & prep

Pick exactly one task using this order:

1. Any `status: blocked` whose blockers are now resolved → unblock first.
2. Any `status: in-progress` updated > 7 days ago → resume or close.
3. Highest priority `not-started` matching user's focus.

Confirm selection with user. Then load the task file and produce:

```markdown
## Task: <title>
- Priority: <p>   Estimate: <S/M/L/XL>
- Definition of Done:
  - [ ] <copy from task file>
- Approach (3-5 bullets):
  - <bullet>
- Files I will touch:
  - <path>
```

### DO — execute

- Update task front matter: `status: in-progress`, `updated: <now>`.
- Work through Approach. Log each substep:

```markdown
## Work Log — <YYYY-MM-DD>
- <HH:MM> <action> → <result/file:line>
- <HH:MM> <action> → <result>
```

- Run validation/tests as you go (do not batch to the end).

### CHECK — validate

Walk the Definition of Done checklist. For each item:

| Outcome | Action |
|---|---|
| ✅ verified | Tick the box |
| ❌ failed | Note in `## Issues`, decide: fix now / split into new TODO / mark blocked |
| ⚠️ partial | Document gap, downgrade to `in-progress` (do not mark complete) |

Run:

```bash
# Markdown / link / frontmatter checks if content changed
python3 scripts/validation/frontmatter-validator.py <files>
python3 scripts/link-checker.py --scope changed --paths <files>
```

### ACT — update & iterate

If complete:

1. Append `## Outcome` to task file (what was done, commits, PRs, lessons).
2. Set `status: completed`, `updated: <now>`.
3. Move file to `TODO/_archive/<YYYY-MM>/`.
4. Update `TODO/dashboard.md` (or regenerate).
5. Suggest commit via `/commit-publish`.

If not complete:

1. Update task body with current state.
2. If blocked: `status: blocked`, populate `blockers:`.
3. If scope grew: split — new TODO for the extra work, keep original focused.

Then propose: "Run again for another task?" (do not auto-loop).

## Edge Cases

### No clear priority

Surface 3-5 candidates with reasoning, ask user to pick.

### Task is blocked

```yaml
status: blocked
blockers:
  - "Waiting on PR #234"
  - "Needs design decision on X"
```

Add `## Blockers` section to body explaining what would unblock. Do not start work.

### Scope creep mid-task

Stop. Create a new TODO for the extra work. Resume original task with original scope only.

## Task-Type Cheats

| Task type | Specific steps |
|---|---|
| **SEO** | Audit current state (Lighthouse) → fix → re-audit → record metrics in Outcome |
| **Content (quest/post)** | Use `/draft-article` or `quest.instructions.md` template → write → validate → commit |
| **Technical** | Branch → implement → test → docs → PR (use `/commit-publish`) |
| **Refactor** | Identify scope → tests as safety net → small steps → verify no behavior change |

## Session Summary (return to user)

```markdown
## WTD Session — <YYYY-MM-DD>

### Task
<title> (<priority>, <estimate>)

### Outcome
<status>: <one-line>

### Files Touched
- <path>

### Tests
- ✅ <name>
- ❌ <name>

### Next Steps
- <suggested follow-up TODO or commit>
```

## Hard Rules

- Never work on more than 1 task per invocation.
- Never mark `completed` with unfinished Definition of Done items.
- Never delete a TODO — archive it.
- Never bypass `/commit-publish` for changes that touch the live site.
- Never auto-promote priority without user confirmation.

---

**Related:** [`.github/instructions/todo.instructions.md`](../instructions/todo.instructions.md) · [`.github/prompts/kaizen.prompt.md`](kaizen.prompt.md) · [`.github/prompts/commit-publish.prompt.md`](commit-publish.prompt.md)
