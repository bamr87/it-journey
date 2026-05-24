---
applyTo: "pages/_quickstart/**/*.md"
description: "Author IT-Journey quickstart guides: phased onboarding from machine setup through deployment, beginner-friendly and encouraging"
date: 2026-05-24T00:00:00.000Z
lastmod: 2026-05-24T00:00:00.000Z
---

# Quickstart Collection — `pages/_quickstart/**`

The onboarding ramp: phased guides from a fresh machine through a deployed Jekyll site. Aim is to get someone unblocked fast without sacrificing accuracy. Encouraging second-person voice; imperative for every actionable step.

## 1. Required Frontmatter

| Field | Constraint |
|---|---|
| `title` | Plain string; phase + topic ("Phase 4: Jekyll Setup") |
| `description` | 120–160 chars |
| `date` | ISO 8601 with milliseconds |
| `lastmod` | ISO 8601 with milliseconds; bump on every edit |
| `author` | String; default `bamr87` |
| `categories` | YAML list, never a string |
| `tags` | YAML list, never a string |
| `draft` | Boolean (`false` for publish) |
| `permalink` | `/quickstart/<slug>/` |

**Recommended:** `keywords`, `excerpt`, `difficulty` (`beginner` / `intermediate` / `advanced`), `estimatedTime` (`30 minutes`, `1 hour`), `prerequisites` (YAML list of slugs or human descriptions).

### Frontmatter skeleton

```yaml
---
title: "Phase 4: Jekyll Setup"
description: "Install Ruby, Bundler, and Jekyll on macOS, Windows, or Linux, then bootstrap your first site with the zer0-mistakes theme."
date: 2024-09-01T00:00:00.000Z
lastmod: 2026-05-24T00:00:00.000Z
author: bamr87
categories: [quickstart, jekyll]
tags: [jekyll, ruby, setup, onboarding]
keywords: [jekyll setup, ruby install, bundler, zer0-mistakes, static site]
permalink: /quickstart/jekyll-setup/
difficulty: beginner
estimatedTime: "45 minutes"
prerequisites:
  - /quickstart/machine-setup/
  - /quickstart/github-setup/
draft: false
---
```

## 2. Body Structure

```markdown
## What You'll Accomplish
One paragraph: end state after this phase.

## Prerequisites
What needs to be true before starting (linked).

## Steps

### Step 1 — <name>
What to do; why; expected output.

### Step 2 — <name>
...

## Verify
Concrete checks that confirm success (a command, a URL, a file appears).

## Troubleshooting
Common failure modes with fixes.

## Next Phase
Link to the following quickstart entry.
```

## 3. Multi-Platform Pattern

When platform matters, use the same headings as quests for consistency:

```markdown
### macOS
```bash
brew install ruby
```

### Windows
```powershell
choco install ruby
```

### Linux
```bash
sudo apt install ruby-full
```
```

## 4. Style

- **Second person, imperative:** "Run `bundle exec jekyll serve`", "Open `http://localhost:4002`".
- **Encouraging, not condescending:** "You're almost there", not "Don't worry, this is easy".
- **No marketing fluff:** cut "comprehensive", "amazing", "seamless".
- **One H1** auto-generated; body starts at `##`.
- **Every code block has a language tag.**
- **Verifiable success criteria** — each phase ends with something the reader can confirm.

## 5. Hard Validation Rules

1. `categories` and `tags` are YAML lists.
2. `description` 120–160 chars.
3. `permalink` follows `/quickstart/<slug>/`.
4. `lastmod` bumped on edits.
5. Code blocks language-tagged.
6. `prerequisites` (when present) is a YAML list, not a string.

## 6. Pre-publish Checklist

- [ ] Frontmatter fields present and validly shaped
- [ ] `description` 120–160 chars
- [ ] `categories` / `tags` as lists
- [ ] `permalink` matches `/quickstart/<slug>/`
- [ ] Code blocks language-tagged
- [ ] Verify section is concrete and testable
- [ ] Next-phase link present
- [ ] `lastmod` updated
- [ ] `draft: false`

---

**Related:** [`posts.instructions.md`](posts.instructions.md) · [`quest.instructions.md`](quest.instructions.md) · canonical frontmatter rules in [`../FRONTMATTER.md`](../FRONTMATTER.md).
