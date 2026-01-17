---
title: Quest Scripts
description: Automation tools for quest generation, validation, and maintenance.
permalink: /scripts/quest/readme/
lastmod: 2026-01-16T00:00:00.000Z
---

# Quest Scripts

Tools for quest generation, validation, and network maintenance.

## Scripts

### update-quest-links.py

**Purpose**: Update quest links across documentation files (level READMEs and main quest README).

**Usage**:
```bash
python3 scripts/quest/update-quest-links.py --dry-run
python3 scripts/quest/update-quest-links.py
```

### update-quest-home.py

**Purpose**: Generate and inject an auto-updated quest index into pages/_quests/home.md.

**Usage**:
```bash
python3 scripts/quest/update-quest-home.py --dry-run
python3 scripts/quest/update-quest-home.py
```

### remove-placeholder-deps.py

**Purpose**: Remove placeholder dependency references from quest frontmatter.

**Usage**:
```bash
python3 scripts/quest/remove-placeholder-deps.py --dry-run
python3 scripts/quest/remove-placeholder-deps.py
```

### fix-quest-types.py

**Purpose**: Standardize quest_type values in quest frontmatter.

**Usage**:
```bash
python3 scripts/quest/fix-quest-types.py --dry-run
python3 scripts/quest/fix-quest-types.py
```

### validate-quest-network.py

**Purpose**: Validate quest dependencies, detect cycles, and report orphaned quests.

**Usage**:
```bash
python3 scripts/quest/validate-quest-network.py
```

### fix-quest-frontmatter.py

**Purpose**: Normalize quest frontmatter fields and validate required keys.

**Usage**:
```bash
python3 scripts/quest/fix-quest-frontmatter.py
```

### generate-network-report.sh

**Purpose**: Generate a quest network validation report.

**Usage**:
```bash
./scripts/quest/generate-network-report.sh
```

### cleanup-placeholder-deps.sh

**Purpose**: Bash alternative to remove placeholder dependencies.

**Usage**:
```bash
./scripts/quest/cleanup-placeholder-deps.sh --dry-run
./scripts/quest/cleanup-placeholder-deps.sh
```

### generate-placeholder-quest.sh

**Purpose**: Generate a placeholder quest file from templates.

**Usage**:
```bash
./scripts/quest/generate-placeholder-quest.sh 0110 sql-sorcery "SQL Sorcery"
```

### quest-tools.sh

**Purpose**: Convenience wrapper for quest-related tooling.

**Usage**:
```bash
./scripts/quest/quest-tools.sh --help
```

## Compatibility

Wrapper scripts remain at the original paths (e.g., `scripts/update-quest-links.py`) and will continue to work, but new development should use the `scripts/quest/` paths.
