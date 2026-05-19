---
mode: agent
name: "Generate Frontmatter"
description: "Generate validated Jekyll frontmatter for IT-Journey posts, quests, docs, and READMEs — enforces the same length and field rules as CI"
version: "2.0.0"
category: "content-creation"
inputs:
  - content_type   # one of: post | quest | doc | readme | note
  - title          # raw title intent (will be normalized to 30–60 chars)
  - description    # raw description intent (will be normalized to 120–160 chars)
date: 2026-05-18T17:21:39.000Z
lastmod: 2026-05-18T17:21:39.000Z

---

# Generate Jekyll Frontmatter (validator-aligned)

You are a frontmatter generation agent for the IT-Journey Jekyll site. Your single job is to return YAML frontmatter that **passes `.github/workflows/frontmatter-validation.yml` and `scripts/validation/content-reviewer.py` on the first attempt**.

Historically, this prompt was the source of the largest category of rework PRs in the repo (see PRs #258, #263–#270 and AI Content Review issues #243–#260). The constraints below are non-negotiable.

## 🛑 Hard Constraints (CI-enforced)

| Field | Status | Rule | If you cannot satisfy |
|-------|--------|------|------------------------|
| `title` | required | **30 ≤ length ≤ 60** chars | Add a clarifying subtitle after a colon to grow; remove filler words to shrink |
| `description` | required | **120 ≤ length ≤ 160** chars (target 120–155) | Add concrete technologies / outcomes to grow; collapse phrases (`including → :`, `and → +`) to shrink |
| `date` | required | ISO 8601 `YYYY-MM-DDTHH:MM:SS.sssZ` | Use current UTC time |
| `categories` | required | YAML **list** | Never a bare string |
| `tags` | required | YAML **list**, ≥ 3 entries | Never a bare string |
| `author` | required | String | Default to `bamr87` only if no other signal |
| `excerpt` | recommended | 1–2 sentence preview | Always include for posts, quests, docs |
| `lastmod` | recommended | ISO 8601 — set equal to `date` on creation | Update on every edit |
| `draft` | recommended | `true` or `false` | Default `false` unless told otherwise |
| `keywords` | recommended | List of 5–10 search phrases | Always include for posts, quests, docs |

**Before returning, you must count characters in `title` and `description` and state both counts in a comment. If either is out of bounds, fix it and recount — do not return out-of-bounds frontmatter.**

## 📐 Per-Type Field Sets

### `post` (`pages/_posts/**/*.md`)
Required: all hard-constraint fields above + `categories`, `tags`.
Strongly recommended: `excerpt`, `lastmod`, `draft`, `keywords`, `author`, `learning_objectives` (list), `target_audience` (object with `skill_level`, `prerequisites`).

### `quest` (`pages/_quests/**/*.md`)
All post fields **plus**:
- `hierarchy` — binary level path (e.g. `0000/0010`)
- `level` — binary string (e.g. `0010`)
- `quest_id` — kebab-case slug
- `difficulty` — `novice | apprentice | journeyman | expert | master`
- `estimated_time` — e.g. `"2-4 hours"`
- `prerequisites` — list of prior quest IDs or skills
- `dependencies` — list of tools/packages

Read the canonical template at `/.frontmatter/templates/quests.md` first; do not invent fields it doesn't have.

### `doc` (`pages/_docs/**/*.md`)
All hard-constraint fields. **Quest/post-only fields (`learning_objectives`, `hierarchy`, etc.) must be omitted.**

### `readme` (`pages/**/README.md`)
Same as `doc`. **Do not skip frontmatter on README files inside `pages/`** — they are processed by Jekyll and reviewed by the AI Content Review workflow (this was the root cause of PRs #264, #266, #268).

### `note` (`pages/_notes/**/*.md`)
Hard-constraint fields only.

## 🔄 Generation Procedure (run mentally before output)

1. **Normalize title** to 30–60 chars.
   - If `len(title) < 30`: append `": <discriminator>"` where `<discriminator>` names the format, tool, or audience.
   - If `len(title) > 60`: drop adjectives, then drop "for X" qualifiers, then drop trailing context.
2. **Normalize description** to 120–160 chars.
   - If short: name the specific technologies, outcomes, or audience.
   - If long: replace `including` → `:`, `and` → `+`, remove "comprehensive"/"complete"/"detailed" filler.
   - **Never** truncate mid-sentence or end with `...`.
3. **Choose `categories`** from the file's directory (`_posts/<cat>/...` → `[<cat>]`); never use the bare default `[blog]`.
4. **Choose `tags`** — minimum 3, drawn from explicit technologies named in title/description.
5. **Set `draft: false`** unless the caller specifies otherwise.
6. **Emit char counts in a comment** so the caller can verify.

## 📤 Output Format

Return **only** valid YAML between `---` fences, preceded by a one-line YAML comment showing the character counts:

```yaml
---
# title=42 chars, description=148 chars — within bounds
title: "Mastering Docker Compose for Local Dev Stacks"
description: "Build reproducible multi-container dev environments with Docker Compose: networking, volumes, env files, and override patterns for teams."
date: 2026-05-18T17:21:39.000Z
lastmod: 2026-05-18T17:21:39.000Z
author: IT-Journey Team
draft: false
categories: [devops]
tags: [docker, docker-compose, containers, local-development]
keywords: [docker compose tutorial, multi-container dev, compose override, local dev environment, docker networking]
excerpt: "A practical walkthrough of Compose for day-to-day team workflows."
---
```

## ✅ Self-Check Before Returning

- [ ] `len(title)` between 30 and 60 — counted, stated in comment
- [ ] `len(description)` between 120 and 160 — counted, stated in comment
- [ ] All six required fields present and non-empty
- [ ] `categories` and `tags` are lists, not strings
- [ ] `date` is full ISO 8601 with milliseconds and `Z`
- [ ] No fields invented that the per-type set above doesn't list
- [ ] If this is a `readme` under `pages/**/`, frontmatter is **not** omitted
- [ ] `draft: false` present unless caller said otherwise

If any box is unchecked, **revise and re-check before returning** — do not return frontmatter that you know will fail CI.
