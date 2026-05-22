---
applyTo: "pages/_posts/**/*.md"
description: "Create and validate IT-Journey blog posts: frontmatter, structure, AI-session chronicles, and permalink rules"
date: 2026-05-18T00:00:00.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# Blog Posts — `pages/_posts/**`

Rules for writing IT-Journey posts and AI-session chronicles. Validated by CI (`frontmatter-validation.yml`, `content-reviewer.py`).

## 1. Filename

```
YYYY-MM-DD-kebab-case-slug.md
```

- Date matches `date:` in frontmatter.
- Slug is the URL-safe form of the title — short, descriptive, no stop words where avoidable.

## 2. Required Frontmatter

| Field | Constraint |
|---|---|
| `title` | 30–60 chars |
| `description` | 120–160 chars (optimal 120–155) |
| `date` | ISO 8601 with milliseconds: `2026-05-18T10:00:00.000Z` |
| `author` | String; default `bamr87` |
| `categories` | YAML list, never a string |
| `tags` | YAML list, never a string |
| `excerpt` | Short preview/RSS summary |
| `lastmod` | ISO 8601; update on every edit |
| `draft` | Boolean (`false` for publish) |

**Recommended:** `keywords` (5–10 phrases as a list), `preview` (social-share image path), `permalink` (when linked from non-post content — see §5).

```yaml
---
title: "<30–60 char title>"
description: "<120–160 char SEO description>"
date: 2026-05-18T10:00:00.000Z
lastmod: 2026-05-18T10:00:00.000Z
author: bamr87
categories: [ai-development, tutorials]
tags: [github-copilot, jekyll, automation]
keywords: [github copilot, jekyll automation, ai coding]
excerpt: "<one-sentence hook>"
draft: false
---
```

## 3. Body Structure

```markdown
## Introduction
What this post is about, who it's for, why it matters.

## Context
The problem, prior state, prerequisites.

## Approach
The plan or hypothesis.

## Implementation
Steps with code blocks. Every block has a language tag (```bash, ```python, ```yaml).

## Results
What worked, what didn't, before/after metrics.

## Lessons Learned
Specific takeaways. Not generic.

## Next Steps
Optional. What to try next.
```

Skip sections that don't apply. Don't pad.

## 4. AI-Session Chronicles

Posts documenting an AI-assisted development session must additionally include:

- **Session metadata:** model used, date/time, total prompts, approximate duration.
- **Prompt highlights:** 2–4 key prompts that drove the outcome (verbatim).
- **What the AI got right / wrong:** honest assessment.
- **Final artifact link:** PR, commit, or file path.

Use category `ai-development` or `chronicle`.

## 5. Permalink Rules

The site default in `_config.yml` is `/:collection/:year/:month/:day/:slug/`. If any **non-post** content (quest, doc, note) links to a post via `/posts/<slug>/`, the post **must** declare:

```yaml
permalink: /posts/<slug>/
```

Otherwise the cross-reference 404s. (See PR #272 for the breakage this caused.)

## 6. Hard Validation Rules

These break CI — never violate:

1. `categories` and `tags` are YAML lists: `categories: [foo, bar]` — never `categories: foo`.
2. `description` length 120–160 chars; trim by removing words, not by `…`.
3. Update `lastmod` on every meaningful edit.
4. Don't gitignore `Gemfile.lock`.
5. Every code block has a language tag.
6. Never commit literal secret prefixes (`ghp_`, `sk-`, `AKIA`, etc.) — use `${env:NAME}` or `${input:name}` placeholders.
7. Nested fenced blocks need a longer outer fence (4 backticks if inner uses 3).
8. Don't link from `pages/_docs/` to `../../docs/...` — that dir is excluded from Jekyll. Use a GitHub URL.

## 7. Style

- **Imperative voice** in instructions ("Run `bundle exec jekyll serve`").
- **Past tense** in chronicles ("The model suggested…").
- **One H1** (auto-generated from `title`); start body at `##`.
- **Cross-references** as markdown links, never inline code.
- **No marketing fluff:** cut "comprehensive", "powerful", "seamless".
- **Diagrams:** Mermaid for flows; PNG/SVG under `assets/images/posts/<slug>/`.

## 8. Cross-References

Link related quests, docs, and prior posts:

```markdown
**Related:**
- [Docker Fundamentals quest](/quests/level-00100-docker-fundamentals/)
- [Previous session](/posts/2026-05-17-some-prior-post/)
```

## 9. Pre-publish Checklist

- [ ] Filename matches `YYYY-MM-DD-slug.md` and `date:`
- [ ] All required frontmatter fields present and within length limits
- [ ] `categories` and `tags` are lists
- [ ] All code blocks have language tags
- [ ] No secrets / no broken links
- [ ] `permalink:` declared if linked from non-post content
- [ ] `lastmod` matches today
- [ ] Local Jekyll build succeeds (`bundle exec jekyll build`)
- [ ] `draft: false`

---

**Related:** [`quest.instructions.md`](quest.instructions.md) · [`README.instructions.md`](README.instructions.md) · canonical frontmatter rules in [`../FRONTMATTER.md`](../FRONTMATTER.md).
