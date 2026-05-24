---
title: Quest Scripts
description: Automation tools for quest generation, validation, and maintenance.
permalink: /scripts/quest/readme/
lastmod: 2026-01-16T00:00:00.000Z
date: 2026-01-14T22:23:32.000Z

---

# Quest Scripts

Tools for quest generation, validation, and network maintenance.

## Recommended runbook

Run before opening a quest-related PR (CI enforces these checks):

```bash
make quest-audit          # build-network → validator → network-validator --strict
```

When you need to refresh derived files individually:

```bash
make quest-build-network  # rebuild assets/data/quest-network.json + _data/quests/network.yml
make quest-nav            # regenerate _data/navigation/quests.yml from the quest collection
make quest-levels-data    # regenerate _data/quests/levels.yml from quest_registry.py
```

When migrating permalinks:

```bash
python3 scripts/quest/migrate-permalinks.py --dry-run  # preview
python3 scripts/quest/migrate-permalinks.py            # apply (adds redirect_from automatically)
make quest-build-network                                # re-emit network artifacts
```

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

### add-obsidian-wiki-references.py

**Purpose**: Add or refresh the `## 🕸️ Knowledge Graph` section with Obsidian-style `[[wiki links]]` on every playable quest (level hubs, dependencies, GH-600 study track, overworld).

**Usage**:
```bash
python3 scripts/quest/add-obsidian-wiki-references.py --dry-run
python3 scripts/quest/add-obsidian-wiki-references.py
```

### generate-network-report.sh

**Purpose**: Generate a quest network validation report.

**Usage**:
```bash
./scripts/quest/generate-network-report.sh
```

### generate-quest-navigation.py

**Purpose**: Regenerate `_data/navigation/quests.yml` from the quest collection.
Sidebar nav is fully derived from quest frontmatter — do not edit the YAML by hand.

**Usage**:
```bash
python3 scripts/quest/generate-quest-navigation.py --dry-run
python3 scripts/quest/generate-quest-navigation.py
# or
make quest-nav
```

### generate-quest-levels-data.py

**Purpose**: Emit `_data/quests/levels.yml` from `scripts/quest/quest_registry.py` so quest layouts/includes can render tier names and XP ranges without hardcoded strings.

**Usage**:
```bash
python3 scripts/quest/generate-quest-levels-data.py --dry-run
python3 scripts/quest/generate-quest-levels-data.py
# or
make quest-levels-data
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
