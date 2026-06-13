---
title: versioning
author: bamr87
excerpt: How IT-Journey versions its releases — semantic versioning conventions, changelog format, and the relationship between the site content and the zer0-mistakes theme.
description: Release strategy and versioning conventions for IT-Journey — semantic versioning, changelog format, and the relationship to the zer0-mistakes theme.
snippet: null
categories:
- posts
tags:
- article
- versioning
- semver
meta: null
draft: false
lastmod: '2026-06-13T00:00:00.000Z'
date: '2022-01-10T17:00:49.000Z'
---

## Why Version a Content Site

A blog does not ship binaries, but it does accumulate breaking changes: layout overhauls, frontmatter schema migrations, permalink restructures, dependency upgrades. Without version markers it is impossible to answer "what changed between two deploys?" or "which content was affected by that theme update?"

IT-Journey treats the site as a product and versions it accordingly.

## Convention: Semantic Versioning

Releases follow [semver](https://semver.org/) — `MAJOR.MINOR.PATCH`:

| Segment | Increment when... |
|---|---|
| `MAJOR` | A breaking change hits the live site — permalink restructure, schema migration, removed content type |
| `MINOR` | New feature shipped — new layout, new content category, new tooling integration |
| `PATCH` | Bug fix, copy edit, typo, frontmatter correction |

Pre-release builds get a suffix: `1.3.0-beta.1` for a layout overhaul in staging, `2.0.0-rc.1` for a permalink migration under review.

## Theme vs. Content

The site has two versioned components that move independently:

- **zer0-mistakes theme** — the Jekyll theme that controls layout, CSS, and includes. Versioned in its own repository.
- **IT-Journey content** — the `_posts`, `_pages`, `_docs`, and `_notes` that make up the actual site. Versioned here.

A theme update that does not break content is a `MINOR` bump on the theme and a `PATCH` on the content. A theme update that forces frontmatter changes is a `MAJOR` bump on both.

## Changelog Format

Changelog entries follow [Keep a Changelog](https://keepachangelog.com/) conventions under four sections:

```markdown
## [1.2.0] - 2024-07-01

### Added
- New `data-analytics` post category with index page

### Changed
- Frontmatter `categories` normalized from string to list across all posts

### Deprecated
- `snippet` frontmatter field (use `excerpt` instead)

### Fixed
- Broken permalink on `/posts/build-destroy-repeat-mastery/`
```

The changelog lives at `/CHANGELOG.md` in the repository root. CI fails if a PR bumps the version tag without a matching changelog entry.

## Tagging a Release

```bash
# patch release
git tag -a v1.2.1 -m "fix: correct broken permalink on retropie post"
git push origin v1.2.1

# minor release
git tag -a v1.3.0 -m "feat: add data-analytics category and index"
git push origin v1.3.0
```

GitHub Actions picks up the tag, builds the site, and deploys to GitHub Pages. The tag also creates a GitHub Release entry automatically via the `release.yml` workflow.

## Related

- [semver.org](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [About: Contributing](/about/contribute/)
