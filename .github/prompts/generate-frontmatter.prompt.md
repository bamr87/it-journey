---
mode: agent
description: "Generate Jekyll frontmatter for posts, quests, docs, and READMEs that passes IT-Journey CI validation"
date: 2026-05-18T17:21:39.000Z
lastmod: 2026-05-23T00:00:00.000Z
---

# Generate Jekyll Frontmatter (validator-aligned)

Return YAML frontmatter that passes CI on the first attempt. Constraints differ by content type — **do not apply post rules to quests**.

## Hard Constraints — Posts, Docs, READMEs

Enforced by `.github/workflows/frontmatter-validation.yml`:

| Field | Rule |
|---|---|
| `title` | **30–60** chars |
| `description` | **120–160** chars |
| `date` | ISO 8601 `YYYY-MM-DDTHH:MM:SS.sssZ` |
| `categories` | YAML **list** |
| `tags` | YAML **list**, ≥ 3 entries |
| `author` | non-empty string |
| `draft` | `false` unless caller specifies otherwise |

Count `title` and `description` characters; state counts in a YAML comment. Fix and recount if out of bounds.

## Hard Constraints — Quests (`pages/_quests/**/*.md`)

Enforced by `test/quest-validator/quest_validator.py`. Read [`.github/instructions/quest.instructions.md`](../instructions/quest.instructions.md) and `.frontmatter/templates/quests.md` — **do not invent fields**.

| Field | Rule |
|---|---|
| `title` | **10–100** chars (quest rule — not the 30–60 post rule) |
| `description` | **150–300** chars (quest rule — not the 120–160 post rule) |
| `level` | quoted 4-digit binary: `"1100"` |
| `difficulty` | exact emoji+label: `"🟢 Easy"`, `"🟡 Medium"`, `"🔴 Hard"`, `"⚔️ Epic"` |
| `estimated_time` | `"X-X hours"` or `"X-X minutes"` |
| `primary_technology` | lowercase string |
| `quest_type` | `main_quest` \| `side_quest` \| `bonus_quest` \| `epic_quest` |
| `skill_focus` | `frontend` \| `backend` \| `devops` \| `security` \| `data-engineering` \| `fullstack` |
| `learning_style` | `hands-on` \| `conceptual` \| `project-based` |
| `quest_series` | non-empty string |
| `fmContentType` | `quest` (playable quests) |
| `layout` | `quest` (playable quests) |
| `permalink` | must match `quest_type` — see § Permalink below |
| `keywords` | object with `primary` and `secondary` lists |

**Recommended:** `quest_line`, `quest_arc`, `prerequisites`, `quest_dependencies`, `rewards`, `validation_criteria`, `lastmod`.

**Level READMEs** (`pages/_quests/XXXX/README.md`): use `layout: quest-collection`, `permalink: /quests/XXXX/`, quoted `level`. Do **not** set `fmContentType: quest`.

### Quest permalink by type

| `quest_type` | `permalink` |
|---|---|
| `main_quest` | `/quests/XXXX/<slug>/` |
| `side_quest` | `/quests/XXXX/side-quests/<slug>/` |
| `bonus_quest` / `epic_quest` | `/quests/codex/<slug>/` |

### Quest dependency URLs

Use full canonical paths in `quest_dependencies` — never bare slugs:

```yaml
quest_dependencies:
  required_quests:
    - /quests/0000/terminal-fundamentals/
  unlocks_quests:
    - /quests/0010/next-quest/ # planned quest
```

### YAML quoting

Quote 4-digit levels and numeric tags to avoid Jekyll `gsub` errors:

```yaml
level: "1100"
tags: ["1100", docker, main_quest]
```

## Per-Type Summary

| Type | Path | Extra rules |
|---|---|---|
| `post` | `pages/_posts/**` | Post title/description lengths; `learning_objectives` recommended |
| `quest` | `pages/_quests/**` (not templates) | Quest title/description lengths; full quest field set above |
| `doc` | `pages/_docs/**` | Post hard constraints; omit quest-only fields |
| `readme` | `pages/**/README.md` | Post hard constraints for Jekyll-processed READMEs |
| `note` | `pages/_notes/**` | Post hard constraints only |

## Output Format

Return valid YAML between `---` fences with a comment showing character counts:

```yaml
---
# title=48 chars, description=172 chars — quest bounds OK
title: "Docker Mastery: Container Orchestration Fundamentals"
description: "Learn container orchestration with Docker Compose: multi-service networking, volume persistence, environment configuration, and production-ready local dev stacks for teams."
date: 2026-05-18T17:21:39.000Z
lastmod: 2026-05-18T17:21:39.000Z
level: "1100"
difficulty: "🔴 Hard"
estimated_time: "6-8 hours"
primary_technology: docker
quest_type: main_quest
skill_focus: devops
learning_style: hands-on
quest_series: "Container Mastery"
author: IT-Journey Team
fmContentType: quest
layout: quest
draft: false
permalink: /quests/1100/docker-mastery/
# ... remaining recommended fields
---
```

## Self-Check

- [ ] Used the correct title/description length band for the content type
- [ ] Quest: `permalink` matches `quest_type`
- [ ] Quest: `fmContentType: quest`, `layout: quest`, `draft: false`
- [ ] Numeric tags and levels quoted in YAML lists
- [ ] `categories` and `tags` are lists, not strings
- [ ] No invented fields outside the template / instructions
