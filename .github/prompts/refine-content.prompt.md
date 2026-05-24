---
mode: agent
description: "Refine quest content with implementation challenges, Mermaid diagrams, and validation criteria"
date: 2025-11-22T16:10:21.000Z
lastmod: 2026-05-23T00:00:00.000Z
---

# Refine Quest Content

Enhance an existing quest with implementation details, diagrams, and validation — without breaking [`.github/instructions/quest.instructions.md`](../instructions/quest.instructions.md) compliance.

**Quest file**: {{ inputs.quest_outline }}
**Related article**: {{ inputs.article_content }}

## Hard Rules

- Preserve `permalink`, `quest_type`, and `level` unless explicitly asked to migrate
- Keep `## 🎯 Quest Objectives` with `- [ ]` checkboxes
- All code blocks must have language tags
- Cross-links use canonical permalinks (`/quests/XXXX/slug/`)
- Do not introduce `[placeholder]` brackets in dependencies

## Requirements

1. **Implementation challenges** — tiered, with acceptance criteria and validation commands
2. **Mermaid diagrams** — quest network (prerequisites → current → unlocks) + optional flow diagram
3. **Validation criteria** — align with frontmatter `validation_criteria` when present
4. **Rewards section** — match frontmatter `rewards` including `progression_points`
5. **Multi-platform paths** — add or expand macOS / Windows / Linux sections if topic is OS-dependent

## Quality Gate

After refining, verify:

```bash
python3 test/quest-validator/quest_validator.py <quest-file>
```

Target: ≥70% score, zero errors.

## Output Format

Return the enhanced quest markdown (full file or diff-friendly sections). Note any frontmatter fields that should be updated to match new content.
