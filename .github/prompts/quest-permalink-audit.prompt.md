---
mode: agent
description: "Audit and repair quest permalinks across pages/_quests/ — validates the canonical /quests/XXXX/slug/ hierarchy (side quests flattened), identifies violations, and optionally applies fixes."
date: 2026-05-21T00:00:00.000Z
lastmod: 2026-05-23T00:00:00.000Z
---

# Quest Permalink Audit

You are a quest-permalink auditor. Scan `pages/_quests/` and ensure every file's `permalink` follows [`.github/instructions/quest.instructions.md`](../instructions/quest.instructions.md) §3 and matches its `quest_type`.

## Canonical Permalink Rules

| `quest_type` | Required pattern | Example |
|---|---|---|
| `main_quest` | `/quests/XXXX/slug/` | `/quests/0001/docker-fundamentals/` |
| `side_quest` | `/quests/XXXX/slug/` | `/quests/0000/bash-run/` |
| `bonus_quest` | `/quests/codex/slug/` | `/quests/codex/cheat-sheet-git/` |
| `epic_quest` | `/quests/codex/slug/` | `/quests/codex/full-stack-epic/` |
| Level README | `/quests/XXXX/` | `/quests/0001/` |
| template | `/quests/templates/slug/` | `/quests/templates/new-quest/` |

`XXXX` = 4-digit binary level (`0000`–`1111`). **Permalink must match `quest_type`** — side quests are flattened, so a `/side-quests/` segment is invalid.

## `redirect_from` Policy

- **New quests:** no `redirect_from`
- **Migrations only:** add `redirect_from` when changing slug or level to preserve external links
- Prefer [`scripts/quest/migrate-permalinks.py`](../../scripts/quest/migrate-permalinks.py) — it emits redirects and rewrites internal references
- After migration, update all in-repo links to the canonical URL; `redirect_from` is a safety net, not a substitute

## Procedure

### 1. PLAN — Read before acting

- Read `quest.instructions.md` §3
- Dry-run migration scope:
  ```bash
  python3 scripts/quest/migrate-permalinks.py --dry-run --verbose
  ```
- Count violations by type (`main_quest`, `side_quest`, `bonus_quest`, `epic_quest`, README)

### 2. DO — Audit and optionally fix

**Audit only:**

```bash
python3 test/quest-validator/quest_validator.py -d pages/_quests/ 2>&1 | grep -E "permalink|ERROR"
python3 scripts/quest/validate-quest-network.py --strict
```

**Apply migration:**

```bash
python3 scripts/quest/migrate-permalinks.py
make quest-build-network
make quest-audit
```

The migration script:

- Rewrites `permalink:` to the canonical pattern
- Remaps dependency URLs in `quest_dependencies`
- Adds `redirect_from` for old URLs when migrating
- Rewrites internal references to canonical URLs
- Never deletes files — safe to re-run

### 3. CHECK — Report findings

Report:

- Total quests scanned
- Violations found / fixed (by type)
- Files requiring manual review
- Dependency URLs still using legacy patterns (`gh-600`, bare slugs, flat side-quest paths)
- Whether `make quest-audit` passes

### 4. ACT — Commit

If fixes were applied, commit quest files **and** regenerated network artifacts:

```bash
git add pages/_quests/ _data/quests/network.yml assets/data/quest-network.json
git commit -m "fix(quests): repair permalink violations to canonical patterns

- Migrated N quest files
- redirect_from added for migrated URLs only
- Network artifacts rebuilt

Validates: make quest-audit passes"
```

## Common Violation Patterns

| Old (invalid) | New (canonical) |
|---|---|
| `/quests/gh-600/agentic-mcp-server-mastery/` | `/quests/1000/agentic-mcp-server-mastery/` |
| `/quests/level-0001-docker-fundamentals/` | `/quests/0001/docker-fundamentals/` |
| `/quests/side-quests/bash-run/` (no level) | `/quests/0000/bash-run/` |
| `/quests/epic-digital-portfolio-fortress/` | `/quests/codex/epic-digital-portfolio-fortress/` |
| `side_quest` at `/quests/0001/side-quests/avatar-forge/` | `/quests/0001/avatar-forge/` |

## When to Run

- Before any PR that adds or moves quest files
- When CI reports permalink or network validation failures
- After merging a batch of new quests from contributors
