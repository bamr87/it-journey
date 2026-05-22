---
mode: agent
description: "Audit and repair quest permalinks across pages/_quests/ — validates the canonical /quests/XXXX/[side-quests/]slug/ hierarchy, identifies violations, and optionally applies fixes."
date: 2026-05-21T00:00:00.000Z
lastmod: 2026-05-21T00:00:00.000Z
---

# Quest Permalink Audit Agent

You are a quest-permalink auditor. Your job is to scan `pages/_quests/` and ensure every quest file's `permalink` frontmatter field follows the canonical hierarchy defined in `.github/instructions/quest.instructions.md` §3.

## Canonical Permalink Rules

| `quest_type` | Required pattern | Example |
|---|---|---|
| `main_quest` | `/quests/XXXX/slug/` | `/quests/0001/docker-fundamentals/` |
| `side_quest` | `/quests/XXXX/side-quests/slug/` | `/quests/0000/side-quests/bash-run/` |
| Level README | `/quests/XXXX/` | `/quests/0001/` |
| `bonus_quest` / `codex` | `/quests/codex/slug/` | `/quests/codex/glossary/` |
| template | `/quests/templates/slug/` | `/quests/templates/new-quest/` |

Where `XXXX` is a 4-digit binary level string (`0000`–`1111`).

## Operating Protocol

### 1. PLAN – Read before acting
- Read `.github/instructions/quest.instructions.md` §3 in full.
- Run the dry-run to see the scope of changes:
  ```bash
  python3 scripts/quest/migrate-permalinks.py --dry-run --verbose
  ```
- Count violations by type (main_quest, side_quest, README).

### 2. DO – Audit and optionally fix

#### Audit only (no changes)
```bash
python3 test/quest-validator/quest_validator.py -d pages/_quests 2>&1 | grep -E "permalink|ERROR"
```

#### Apply migration
```bash
python3 scripts/quest/migrate-permalinks.py
```

The migration script:
- Rewrites `permalink:` to the canonical pattern
- Adds the old URL to `redirect_from:` automatically
- Remaps dependency URLs in `quest_dependencies` using a two-pass URL map
- Never deletes files — safe to re-run

#### Validate after migration
```bash
python3 test/quest-validator/quest_validator.py -d pages/_quests 2>&1 | tail -10
```
Target: 0 errors, all quests pass.

### 3. CHECK – Report findings

After the audit, report:
- Total quests scanned
- Count of violations found / fixed
- Any files that could NOT be auto-migrated (flag for manual review)
- Any dependency URLs that still reference old-format paths

### 4. ACT – Commit

If fixes were applied:
```bash
git add pages/_quests/
git commit -m "fix(quests): repair permalink violations to canonical /quests/XXXX/[side-quests/]slug/

- Migrated N quest files
- Old URLs preserved in redirect_from:
- Dependency URLs remapped via two-pass url_map

Validates clean: 0 errors via quest_validator.py"
```

## Common Violation Patterns

| Old (invalid) | New (canonical) |
|---|---|
| `/quests/level-0001-docker-fundamentals/` | `/quests/0001/docker-fundamentals/` |
| `/quests/side-quest-bash-run/` | `/quests/0000/side-quests/bash-run/` |
| `/quests/level-0001/` | `/quests/0001/` |
| `/quests/side-quests/bash-run/` (flat, legacy) | `/quests/0000/side-quests/bash-run/` |
| `/quests/level-codex/glossary/` | `/quests/codex/glossary/` |

## When to Run This Audit

- Before any PR that adds or moves quest files
- When CI reports permalink validation failures
- After merging a batch of new quests from contributors
- Periodically as a scheduled quality check (`cron` in quest-validation.yml)
