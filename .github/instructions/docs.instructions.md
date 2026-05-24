---
applyTo: "pages/_docs/**/*.md"
description: "Author IT-Journey docs collection entries: technical reference, cheatsheets, wargame writeups, and certification study material"
date: 2026-05-24T00:00:00.000Z
lastmod: 2026-05-24T00:00:00.000Z
---

# Docs Collection — `pages/_docs/**`

Published reference library at `/docs/...`. Distinct from the repo-root `docs/` directory, which is developer-only and excluded from the Jekyll build. Permalink default in `_config.yml` is `/docs/:categories/:name/`.

## 1. Required Frontmatter

| Field | Constraint |
|---|---|
| `title` | Plain string; reference style ("Bandit Level 5", "Liquid Filter Cheatsheet") — no marketing fluff |
| `description` | 120–160 characters; one sentence describing what the doc covers |
| `date` | ISO 8601 with milliseconds (`2026-05-24T00:00:00.000Z`) |
| `lastmod` | ISO 8601 with milliseconds; bump on every meaningful edit |
| `categories` | YAML list, never a string |
| `tags` | YAML list, never a string |
| `author` | String; default `bamr87` |
| `draft` | Boolean (`false` for publish) |
| `permalink` | Match the section pattern (see §4) when overriding the default |

**Recommended:** `keywords` (list of 5–10 phrases), `excerpt` (short summary for indexes), `source_repo` and `source_url` for imported content (wargames, vendor docs), `preview` (social card image).

### Frontmatter skeleton

```yaml
---
title: Bandit Level 5
description: "Walk through OverTheWire Bandit level 5 — finding a 1033-byte readable, non-executable file hidden inside inhere/."
date: 2025-06-12T00:00:00.000Z
lastmod: 2026-05-24T00:00:00.000Z
author: bamr87
categories: [wargames, security]
tags: [security, wargames, linux, ctf, bandit]
keywords: [bandit, overthewire, find command, file permissions, ctf walkthrough]
permalink: /docs/wargames/bandit/bandit5/
source_repo: https://github.com/OverTheWireOrg/OverTheWire-website
source_url: https://overthewire.org/wargames/bandit/bandit5.html
draft: false
---
```

## 2. Subsection Conventions

| Subfolder | Purpose | Notes |
|---|---|---|
| `wargames/overthewire/<game>/` | CTF level walkthroughs | Imported; preserve `source_repo` / `source_url`. Body verbatim from author; do **not** rewrite solution steps |
| `jekyll/` | IT-Journey Jekyll implementation notes | Full reference voice; cross-link with `/quests/` and `/posts/` |
| `terminal/` | Bash/zsh/iTerm reference and cheatsheets | Compact tables, command + meaning |
| `certifications/<exam>/` | Study hubs (currently `gh-600/`) | Long-form; well-developed bodies |
| `obsidian/` | Knowledge-graph and PKM docs | Same as `jekyll/` |

Wargame writeups are the largest cohort (~200 files). Their `description` field is the most common frontmatter gap — derive from the level goal or first prose paragraph.

## 3. Body Structure

Pick the shape that fits the subsection:

### Reference / cheatsheet

```markdown
## Overview
One paragraph: what this covers, when to reach for it.

## <Topic 1>
Definition, syntax, minimal example.

## <Topic 2>
...

## See Also
- Cross-links to other docs, posts, quests
```

### Wargame walkthrough

```markdown
## Level Goal
Verbatim from the game.

## Approach
Hypothesis: what command/tool to reach for and why.

## Solution
```bash
# commands with output
```

## Lessons
What the level taught (file permissions, find flags, etc.).
```

### Certification study hub

```markdown
## Exam Overview
Format, domains, weights, time limit.

## Domain N — <name>
Concept → example → practice link.

## Resources
Official docs, practice exams, IT-Journey quests.
```

## 4. Permalink Patterns

Default is `/docs/:categories/:name/`. Override `permalink` explicitly when the categories list would produce an awkward URL.

| Subsection | Pattern | Example |
|---|---|---|
| Wargames | `/docs/wargames/<game>/<level>/` | `/docs/wargames/bandit/bandit5/` |
| Jekyll | `/docs/jekyll/<name>/` | `/docs/jekyll/liquid-filters/` |
| Terminal | `/docs/terminal/<name>/` | `/docs/terminal/bash-cheatsheet/` |
| Certifications | `/docs/certifications/<exam>/<name>/` | `/docs/certifications/gh-600/study-plan/` |

## 5. Style

- **Imperative voice** for instructions ("Run `find . -size 1033c -readable -! -executable`").
- **Past tense** for solution narratives ("The flag lived inside `inhere/maybehere07/.file2`").
- **One H1** auto-generated from `title`; body starts at `##`.
- **No marketing fluff:** cut "comprehensive", "powerful", "seamless".
- **Code blocks** always have a language tag (` ```bash `, ` ```yaml `, ` ```html `).
- **Cross-links** as markdown links — never inline code.

## 6. Hard Validation Rules

These break CI or the docs index:

1. `categories` and `tags` are YAML lists.
2. `description` length 50–160 chars; aim 120–155.
3. Update `lastmod` on every edit.
4. Code blocks have language tags; nested fences use 4 backticks if the inner block uses 3.
5. Never commit secret prefixes (`ghp_`, `sk-`, `AKIA`) — use `${env:NAME}` placeholders.
6. For imported content (wargames), preserve `source_repo` and `source_url`.
7. Don't link to `../../docs/...` (the developer-only directory excluded from Jekyll). Use a GitHub URL instead.

## 7. Pre-publish Checklist

- [ ] All required frontmatter fields present
- [ ] `description` 120–160 chars
- [ ] `categories` and `tags` are lists
- [ ] `permalink` matches subsection pattern
- [ ] `lastmod` bumped to today
- [ ] Body code blocks have language tags
- [ ] Cross-links to related quests/posts/notes
- [ ] `draft: false`
- [ ] Local Jekyll build succeeds (`bundle exec jekyll build`)

---

**Related:** [`posts.instructions.md`](posts.instructions.md) · [`quest.instructions.md`](quest.instructions.md) · canonical frontmatter rules in [`../FRONTMATTER.md`](../FRONTMATTER.md).
