---
mode: agent
description: "Prepare final files for publication: file naming, READMEs, navigation, and cross-references"
date: 2025-11-22T16:10:21.000Z
lastmod: 2026-05-23T00:00:00.000Z
---

# Publish Preparation

Prepare final files with proper naming and integration into IT-Journey structure. Quest rules: [`.github/instructions/quest.instructions.md`](../instructions/quest.instructions.md).

## Tasks

### 1. Generate filenames

| Content | Path pattern |
|---|---|
| Article | `pages/_posts/<category>/YYYY-MM-DD-title-with-hyphens.md` |
| Main quest | `pages/_quests/XXXX/<slug>.md` |
| Side quest | `pages/_quests/XXXX/<slug>.md` (permalink includes `/side-quests/`) |
| Bonus / epic quest | `pages/_quests/codex/<slug>.md` |
| Level README | `pages/_quests/XXXX/README.md` |

Quest files are **flat in the level directory** — never `pages/_quests/XXXX/slug/slug.md`.

### 2. Frontmatter + content

- Merge frontmatter and body; validate YAML (quote colons in titles, quote numeric tags)
- Playable quests: `fmContentType: quest`, `layout: quest`, `draft: false`
- Level READMEs: `layout: quest-collection`, quoted `level: "XXXX"`
- Set `permalink` to match `quest_type`
- Bump `lastmod`

### 3. Validate

```bash
make quest-audit          # quests
python3 scripts/validation/frontmatter-validator.py <paths>  # posts/docs
```

Commit regenerated `_data/quests/network.yml` and `assets/data/quest-network.json` when dependencies changed.

### 4. README and navigation

- README-last: bump `lastmod` on touched READMEs
- Level hubs auto-list quests via `quest-collection` layout — update narrative only when needed
- Run `make quest-nav` if sidebar navigation needs refresh

### 5. Cross-references

- Use canonical permalinks in links (`/quests/XXXX/slug/`), not relative file paths
- Update `quest_dependencies` with full canonical URLs

## Output Format

Return file paths and content for each file to create or update, plus the validation commands to run.
