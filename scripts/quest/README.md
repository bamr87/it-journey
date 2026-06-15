---
title: Quest Framework & Tooling
description: The single source of truth, schema, data pipeline, and tooling for IT-Journey quests.
permalink: /scripts/quest/readme/
lastmod: 2026-06-14T00:00:00.000Z
date: 2026-01-14T22:23:32.000Z
---

# Quest Framework & Tooling

Everything about the quest taxonomy and schema is defined exactly once, in
[`quest_registry.py`](quest_registry.py). Every data file, validator, template,
and generator derives from it, so the framework cannot drift.

## Single source of truth

`quest_registry.py` owns:

- **Taxonomy** — 4 tiers (Apprentice 🌱 / Adventurer ⚔️ / Warrior 🔥 / Master ⚡;
  there is **no** "Legend" tier — level 1111 is Master), the 16 binary levels
  (`0000`–`1111`), their themes, XP ranges, and Bootstrap icons.
- **Controlled vocabularies** — `QUEST_TYPES` (`main_quest`, `side_quest`,
  `epic_quest`, `bonus_quest`), `FM_CONTENT_TYPES` (`quest`, `documentation`,
  `template`, `codex`), `DIFFICULTIES` (🟢 Easy / 🟡 Medium / 🔴 Hard / ⚔️ Epic),
  `SKILL_FOCUS`, `LEARNING_STYLE`.
- **Frontmatter schema** — `REQUIRED_FIELDS`, `OPTIONAL_FIELDS`, and the nested
  contracts for `prerequisites`, `rewards`, `quest_dependencies`.
- **Collection rules** — `SKIP_SUBDIRS`, `SKIP_STEMS`, `is_quest()`, `is_draft()`.
- **Routing** — canonical permalink helpers + slug rules + regexes.

`👑` is the `epic_quest` icon, never a tier emoji.

## Quest type vs content type

- `quest_type` (a playable quest's kind) is one of `QUEST_TYPES`.
- `fmContentType` decides whether a page **is** a quest. Only `fmContentType: quest`
  enters quest collections, scoring, and the dependency graph. Support pages use
  `documentation` / `template` / `codex` and are excluded.

## Canonical permalinks

| kind | pattern |
|---|---|
| main / side / epic quest | `/quests/{level}/{slug}/` |
| bonus quest / codex | `/quests/codex/{slug}/` |
| documentation | `/quests/docs/{slug}/` |
| template | `/quests/templates/{slug}/` |

The filename slug must equal the permalink slug. Side quests are **flattened**
(no `/side-quests/` segment).

## Quest lifecycle

`placeholder → draft → published`

A quest containing placeholder scaffolding (`[technology]` tokens or the
"🔮 Placeholder" footer) **fails validation** unless it declares `draft: true`.
Drafts are allowed through CI; remove `draft` only when the quest is real and
passes the validator at ≥ 70%.

## Generated data (never hand-edit)

All four are regenerated from the registry + quest files by `make quest-data`:

| file | accessor | generator |
|---|---|---|
| `_data/quests/levels.yml` | `site.data.quests.levels[code]` | `generate-quest-levels-data.py` |
| `_data/quests/tiers.yml` | `site.data.quests.tiers[name]` | `generate-quest-levels-data.py` |
| `_data/quests/order.yml` | `site.data.quests.order` | `generate-quest-levels-data.py` |
| `_data/navigation/quests.yml` | sidebar nav | `generate-quest-navigation.py` |
| `_data/quests/network.yml` + `assets/data/quest-network.json` | dependency graph | `build-quest-network.py` |

> Jekyll keys data files by path, so the three files above split what used to be
> one nested file — that's why the accessors are shallow (`site.data.quests.tiers`,
> not `site.data.quests.levels.tiers`). The network output is deterministic so CI
> can detect stale data.

## The toolset

| script | purpose |
|---|---|
| `quest_registry.py` | the single source of truth (imported by everything) |
| `generate-quest-levels-data.py` | emit `levels.yml` / `tiers.yml` / `order.yml` |
| `generate-quest-navigation.py` | emit `_data/navigation/quests.yml` |
| `build-quest-network.py` | emit the dependency graph (JSON + YAML) |
| `validate-quest-network.py` | graph integrity: required-cycle, broken-dep, orphan checks |
| `normalize-quest-frontmatter.py` | the ONE idempotent frontmatter normalizer |
| `generate-placeholder-quest.sh` | scaffold a new placeholder quest |

Quest **content quality** is validated by
[`test/quest-validator/quest_validator.py`](../../test/quest-validator/quest_validator.py),
which imports its schema from the registry.

## Runbook

```bash
make quest-data        # regenerate all derived data from the registry + files
make quest-normalize   # idempotently normalize quest frontmatter
make quest-validate    # content-quality validation (quest_validator.py)
make quest-network     # dependency-graph validation
make quest-audit       # build network → validate content → validate network
```

Scaffold a new quest, then fill and validate it:

```bash
./scripts/quest/generate-placeholder-quest.sh 0110 sql-sorcery "SQL Sorcery"
# write real content, then:
python3 test/quest-validator/quest_validator.py pages/_quests/0110/sql-sorcery.md --fail-threshold 70
```

## CI gate

`.github/workflows/quest-validation.yml` enforces, on every quest PR:

- **content quality** — `quest_validator.py` on changed files (`--fail-threshold 70`);
  placeholders fail unless `draft: true`.
- **graph integrity** — `validate-quest-network.py` (errors fail the job).
- **non-stale data** — regenerates all derived data and fails if the committed
  copies differ (so a registry change must ship with regenerated data).

These should be marked **required** in branch protection (see
[`.github/workflows/README.md`](../../.github/workflows/README.md)).
