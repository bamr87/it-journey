---
applyTo: "pages/_posts/**/2000-01-01-index.md"
description: "Author IT-Journey post category landing pages: layout: section hubs that aggregate posts under /news/<category>/"
date: 2026-05-24T00:00:00.000Z
lastmod: 2026-05-24T00:00:00.000Z
---

# Post Category Landings — `pages/_posts/<category>/2000-01-01-index.md`

These files are **section landing pages**, not posts. They live inside `pages/_posts/<category>/` so Jekyll picks them up alongside the posts they represent, but they render with `layout: section` at `/news/<category>/` and are excluded from chronological feeds via `index: true`.

Do **not** apply the post schema to these files — the rules below supersede `posts.instructions.md` for the 13 category index files.

## 1. Filename and Date

- Filename is always `2000-01-01-index.md` (sentinel date keeps it ordered first).
- Frontmatter `date` is the date the landing was meaningfully updated, not 2000.

## 2. Required Frontmatter

| Field | Constraint |
|---|---|
| `title` | Display name of the section ("AI & Machine Learning", "DevOps") — not an article title, so length is flexible |
| `description` | 80–160 chars; describes what readers find in this section |
| `layout` | `section` |
| `category` | Display name matching `title` (used by the news layout to filter) |
| `icon` | Bootstrap Icon name without prefix (`robot`, `gear`, `terminal`) |
| `index` | `true` — flags this as a non-chronological landing |
| `section_style` | `grid`, `list`, or `magazine` (defaults to `grid` for category hubs) |
| `permalink` | `/news/<category-slug>/` |
| `date` | ISO 8601 with milliseconds |
| `lastmod` | ISO 8601 with milliseconds |
| `categories` | YAML list — typically `[<display name>]` |

**Optional:** `excerpt` (used in the news index summary), `keywords`, `preview` (banner image), `tags`.

### Frontmatter skeleton

```yaml
---
title: AI & Machine Learning
description: "Chronicles and tutorials covering agentic AI, GitHub Copilot workflows, model context protocol, prompt engineering, and ML pipelines."
layout: section
category: AI & Machine Learning
icon: robot
index: true
section_style: grid
permalink: /news/ai-machine-learning/
date: 2026-05-24T00:00:00.000Z
lastmod: 2026-05-24T00:00:00.000Z
categories: [AI & Machine Learning]
excerpt: "Agentic patterns, Copilot workflows, MCP servers, and ML pipelines."
keywords: [ai, machine learning, copilot, mcp, agents]
draft: false
---
```

## 3. Body Structure

Keep bodies short — the layout does the heavy lifting. Useful additions:

```markdown
## In This Section
Two or three sentences describing what's collected here and who it's for.

## Featured
- [Post title](/posts/...) — one-line hook
- [Post title](/posts/...) — one-line hook

## Related Sections
- [Other section](/news/other/)
```

If the landing has no narrative content beyond the post list, leave the body empty — `layout: section` will render the post grid by itself.

## 4. Canonical Category Map

These are the 13 sections; keep slugs and titles in sync with `_data/navigation/posts.yml`:

| Folder | Title | Permalink | Icon |
|---|---|---|---|
| `ai-machine-learning` | AI & Machine Learning | `/news/ai-machine-learning/` | `robot` |
| `business` | Business | `/news/business/` | `briefcase` |
| `creative-experimental` | Creative & Experimental | `/news/creative-experimental/` | `palette` |
| `culture-society` | Culture & Society | `/news/culture-society/` | `people` |
| `data-analytics` | Data & Analytics | `/news/data-analytics/` | `bar-chart` |
| `devops` | DevOps | `/news/devops/` | `gear` |
| `learning` | Learning | `/news/learning/` | `book` |
| `programming` | Programming | `/news/programming/` | `code-slash` |
| `system-administration` | System Administration | `/news/system-administration/` | `server` |
| `technology` | Technology | `/news/technology/` | `cpu` |
| `tools-environment` | Tools & Environment | `/news/tools-environment/` | `tools` |
| `trends-ideas` | Trends & Ideas | `/news/trends-ideas/` | `lightbulb` |
| `web-development` | Web Development | `/news/web-development/` | `globe` |

## 5. Hard Validation Rules

1. `layout: section` — required (not `article`).
2. `index: true` — required so post chronological listings skip this file.
3. `permalink` matches `/news/<slug>/` exactly.
4. `category` value matches `title`.
5. `categories` is a YAML list containing at least the section title.
6. `lastmod` bumped on edits.

## 6. Pre-publish Checklist

- [ ] Filename is `2000-01-01-index.md`
- [ ] `layout: section`, `index: true`
- [ ] `permalink` matches `/news/<slug>/`
- [ ] `icon` matches Bootstrap Icons name (no `bi-` prefix)
- [ ] `category` matches `title`
- [ ] `lastmod` updated
- [ ] Body is short or empty — let the layout render the post grid

---

**Related:** [`posts.instructions.md`](posts.instructions.md) · canonical frontmatter rules in [`../FRONTMATTER.md`](../FRONTMATTER.md). The `news` layout lives at [`_layouts/news.html`](../../_layouts/news.html) and the section navigation source is `_data/navigation/posts.yml`.
