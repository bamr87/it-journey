---
applyTo: "pages/_about/**/*.md"
description: "Author IT-Journey site about pages: project overview, contributor profiles, versioning, features, and meta content at /about/"
date: 2026-05-24T00:00:00.000Z
lastmod: 2026-05-24T00:00:00.000Z
---

# About Collection — `pages/_about/**`

Site meta: project overview, mission, contributor profiles, features, versioning, settings exports. Warm and professional voice — these are the pages new visitors land on to figure out what IT-Journey is.

## 1. Required Frontmatter

| Field | Constraint |
|---|---|
| `title` | Plain string |
| `description` | 120–160 chars |
| `date` | ISO 8601 with milliseconds |
| `lastmod` | ISO 8601 with milliseconds; bump on every edit |
| `categories` | YAML list, never a string |
| `tags` | YAML list, never a string |
| `author` | String; default `bamr87` |
| `draft` | **Boolean** (`true` or `false`) — never a string like `"published"` |
| `permalink` | Default `/about/:categories/:name/`; override when the categories list would be awkward |

**Recommended:** `keywords`, `excerpt`, `preview` (banner image).

### Frontmatter skeleton

```yaml
---
title: About IT-Journey
description: "Open-source educational platform documenting the journey from zer0 to her0 — quests, chronicles, and reference docs for IT learners."
date: 2024-04-01T00:00:00.000Z
lastmod: 2026-05-24T00:00:00.000Z
author: bamr87
categories: [about]
tags: [about, mission, open-source]
keywords: [it-journey, open source education, learning platform, jekyll]
draft: false
---
```

## 2. Subsection Patterns

| Subfolder / file | Purpose |
|---|---|
| `about.md` | Mission, audience, what the site offers |
| `purpose.md` | Why this exists; long-form rationale |
| `versioning.md` | Release strategy and changelog convention |
| `features.md` | Feature catalog (links into quests/docs) |
| `automation.md` | Site automation overview |
| `contributors/<handle>.md` | Contributor profile (one per maintainer) |
| `settings/*.md` | Exported site configuration documentation |

## 3. Contributor Profile Template

```yaml
---
title: "<Display Name>"
description: "<120–160 char one-liner describing role and contributions to IT-Journey>"
date: <ISO timestamp of profile creation>
lastmod: <ISO timestamp of last edit>
author: <handle>
categories: [about, contributors]
tags: [contributor, <areas>]
github_username: <handle>
draft: false
permalink: /about/contributors/<handle>/
---

## Role
One paragraph: what you contribute and why.

## Focus Areas
- <bullet>
- <bullet>

## Links
- GitHub: [@handle](https://github.com/handle)
- Site: <optional>
```

## 4. Style

- **Warm, professional** — first or third person, consistent within a page.
- **No marketing fluff:** cut "comprehensive", "innovative", "cutting-edge", "revolutionary".
- **One H1** auto-generated from `title`; body starts at `##`.
- **Cross-references** as markdown links to `/quests/...`, `/docs/...`, `/posts/...`.

## 5. Hard Validation Rules

1. `draft` is a boolean — `true` or `false`, never `"published"` or `"draft"`.
2. `categories` and `tags` are YAML lists.
3. `description` 120–160 chars.
4. `lastmod` bumped on edits.
5. Code blocks (rare in this collection) have language tags.

## 6. Pre-publish Checklist

- [ ] All required frontmatter fields present
- [ ] `draft` is a boolean
- [ ] `description` 120–160 chars
- [ ] `categories` / `tags` as lists
- [ ] `lastmod` updated
- [ ] Local Jekyll build succeeds

---

**Related:** [`posts.instructions.md`](posts.instructions.md) · [`quickstart.instructions.md`](quickstart.instructions.md) · canonical frontmatter rules in [`../FRONTMATTER.md`](../FRONTMATTER.md).
