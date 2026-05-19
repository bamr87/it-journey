---
applyTo: "**/README.md"
description: "Maintain and evolve README.md files: structure, frontmatter, lastmod hygiene, and cross-references"
date: 2025-10-17T17:25:30.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# README.md Maintenance Guidelines

Every directory of substance in IT-Journey gets a `README.md`. It is the gateway, the map, and the source of truth for that directory.

## 1. When to Create / Update

| Trigger | Action |
|---|---|
| New directory added | Create `README.md` |
| Files added / removed | Update file listing + bump `lastmod` |
| Purpose or scope changed | Rewrite overview + bump `lastmod` |
| Cross-referenced README changed | Update the link + bump `lastmod` |
| Broken link found | Fix + bump `lastmod` |

**Rule:** Any edit to a README must update its `lastmod` field.

## 2. Required Frontmatter

```yaml
---
title: "<Directory or Module Name>"
description: "<1-line purpose statement, 80–160 chars>"
permalink: /path/to/directory/
lastmod: 2026-05-18T12:00:00.000Z
---
```

Optional: `categories`, `tags`, `author`, `draft: false`. Posts/quests/notes have stricter frontmatter — see [`posts.instructions.md`](posts.instructions.md), [`quest.instructions.md`](quest.instructions.md).

## 3. Canonical Structure

```markdown
# <Directory Name>

<One-paragraph purpose statement.>

## Purpose

<Why this directory exists and what problem it solves.>

## Contents

| File / Subdir | Purpose |
|---|---|
| `file1.ext` | What it does |
| `subdir/` | What it contains |
| `README.md` | This file |

## Usage

<How to use, run, or consume the contents. Include 1–2 commands or examples.>

## Related

- [Parent context](../README.md)
- [Sibling resource](../sibling/README.md)
- [External reference](https://…)

---

**Last updated:** YYYY-MM-DD
```

Skip sections that don't apply. Don't pad with empty placeholders.

## 4. Specialized README Templates

### Feature / module README
Add these sections after `Usage`:
- `## Configuration` — env vars, config files, defaults
- `## Examples` — 1–2 worked examples with expected output
- `## Troubleshooting` — common errors and fixes
- `## Changelog` — link to project `CHANGELOG.md` or inline recent changes

### Collection README (e.g. `pages/_quests/1100/`)
- `## Overview` — collection theme / level
- `## Quest Map` — Mermaid diagram of progression
- `## Available Items` — table with title, difficulty, time, status
- `## Prerequisites` — what must be completed first
- `## Related Collections` — sibling level / series links

### Script directory README
- `## Scripts` — table: filename, purpose, primary args
- `## Dependencies` — runtime requirements
- `## Examples` — typical invocations

## 5. Cross-Reference Hygiene

- Every README should link **up** (parent), **across** (siblings), and **down** (children).
- Use relative paths for in-repo links: `[Title](../sibling/README.md)`.
- Use full URLs for external resources.
- After moving or renaming a file, grep for incoming links and fix them.

## 6. Style Rules

- **Headings:** Start at `#` (H1). Only one H1 per README. `##` for major sections, `###` sparingly. Avoid `####` unless absolutely needed.
- **Tables** beat bulleted lists when comparing properties.
- **Code blocks** always specify a language: ` ```bash `, ` ```yaml `, ` ```python `.
- **Links** use descriptive text, not "click here". File references are markdown links, never inline code.
- **Emojis** allowed sparingly in section headers for scannability.
- **No marketing fluff.** Cut "comprehensive", "powerful", "seamless", etc.

## 7. Update Checklist

Before committing a README change:

- [ ] `lastmod` bumped to today (ISO 8601 with milliseconds)
- [ ] File listing matches actual directory contents (`ls`)
- [ ] All internal links resolve
- [ ] All external links return 200 (spot check)
- [ ] No broken Markdown (preview locally)
- [ ] Linked from parent README if newly created
- [ ] No leftover template placeholders (`[Description]`, `YYYY-MM-DD`, etc.)

## 8. Validation

Quick local checks:

```bash
# Find READMEs with stale lastmod (>90 days)
find . -name README.md -mtime +90 -print

# Find broken internal links
markdown-link-check **/README.md

# Find READMEs missing required frontmatter keys
for f in $(find . -name README.md); do
  for k in title description lastmod; do
    grep -q "^$k:" "$f" || echo "MISSING $k → $f"
  done
done
```

## 9. README-First / README-Last Workflow

This is a core IT-Journey rule (see `.github/copilot-instructions.md`):

1. **Before** any change to a directory, read its `README.md` to load context.
2. **After** the change, update that README + any affected parent/sibling READMEs.
3. The README must always describe the current state — never let it drift behind reality.

---

**Related:** [`contributing.instructions.md`](contributing.instructions.md) · [`scripts.instructions.md`](scripts.instructions.md) · canonical frontmatter in [`../FRONTMATTER.md`](../FRONTMATTER.md).
