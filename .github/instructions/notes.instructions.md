---
applyTo: "pages/_notes/**/*.md"
description: "Author IT-Journey notes: dated dev notes, cheatsheets, code snippets, and working scratch pads at /notes/"
date: 2026-05-24T00:00:00.000Z
lastmod: 2026-05-24T00:00:00.000Z
---

# Notes Collection — `pages/_notes/**`

Working notes, cheatsheets, dated dev journal entries, and code snippets. Lower formality bar than posts or docs — the point is to capture useful fragments without ceremony.

## 1. Required Frontmatter

| Field | Constraint |
|---|---|
| `title` | Plain string; descriptive |
| `description` | 80–160 chars; one sentence |
| `date` | ISO 8601 with milliseconds (creation date — leave alone after) |
| `lastmod` | ISO 8601 with milliseconds; bump on every meaningful edit |
| `categories` | YAML list, never a string |
| `tags` | YAML list, never a string |
| `author` | String; default `bamr87` |
| `draft` | Boolean (`false` for publish) |

**Recommended:** `keywords` (3–10 phrases), `excerpt`, `permalink` when the auto-permalink is unwieldy.

### Frontmatter skeleton

```yaml
---
title: iTerm Tips and Tricks
description: "Working notes on iTerm2 split-pane shortcuts, profile switching, and shell integration tweaks collected on macOS."
date: 2025-01-16T00:00:00.000Z
lastmod: 2026-05-24T00:00:00.000Z
author: bamr87
categories: [notes, terminal]
tags: [iterm, macos, terminal, productivity]
keywords: [iterm2, terminal shortcuts, macos productivity, shell integration]
draft: false
---
```

## 2. Subfolder Conventions

| Subfolder | Purpose |
|---|---|
| `cheetsheets/` | Long-running command references (bash, git, vim, etc.) — body can be many hundreds of lines |
| `code-snippets/` | One-off reusable snippets; minimal frontmatter is fine |
| `gh-600/` | GH-600 study notes hub and per-domain notes |
| `zero/` | Onboarding scratch notes |
| Top-level dated notes | `YYYY-MM-DD-slug.md` for dev journal entries |

Cheatsheet bodies are kept long and dense on purpose; do **not** "polish" them into prose. Reference voice wins.

## 3. Body Structure

No fixed template. Common shapes:

### Cheatsheet

```markdown
## <Category 1>
| Command | Meaning |
|---|---|
| `cmd1` | does X |
| `cmd2` | does Y |

## <Category 2>
...
```

### Dated dev note

```markdown
## Context
What problem prompted the note.

## What I Tried
Steps and outcomes.

## Resolution
What worked, and one-line lesson.
```

### Snippet

```markdown
Short context paragraph.

```python
# the snippet
```

Optional usage note.
```

## 4. Style

- **Working notes tone:** dry, minimal scaffolding, no narrative warm-up.
- **Imperative for commands**, past tense for journal entries.
- **One H1** auto-generated from `title`; body starts at `##`.
- **Code blocks** always have a language tag.
- **Cross-references** as markdown links.

## 5. Hard Validation Rules

1. `categories` and `tags` are YAML lists.
2. `description` 80–160 chars (notes can be a hair shorter than posts).
3. `lastmod` bumped on edits.
4. Code blocks have language tags.
5. No literal secret prefixes (`ghp_`, `sk-`, `AKIA`) — use placeholders.

## 6. Pre-publish Checklist

- [ ] Frontmatter fields present and validly shaped
- [ ] `description` in length range
- [ ] `categories` / `tags` as lists
- [ ] Code blocks language-tagged
- [ ] `lastmod` updated
- [ ] `draft: false`

---

**Related:** [`docs.instructions.md`](docs.instructions.md) · [`posts.instructions.md`](posts.instructions.md) · canonical frontmatter rules in [`../FRONTMATTER.md`](../FRONTMATTER.md).
