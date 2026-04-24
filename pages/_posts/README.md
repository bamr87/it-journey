---
title: "Blog Posts (`pages/_posts/`)"
description: "Conventions, validation tooling, and authoring standards for IT-Journey blog posts."
lastmod: 2025-11-16
---

# Blog Posts — `pages/_posts/`

This directory holds the IT-Journey blog. Each post is a standalone Jekyll
collection item that follows shared conventions for frontmatter, layout,
formatting, and link hygiene.

> Working on a draft? Put it in [`pages/_drafts/`](../_drafts/) instead.
> Drafts are not built into production but render locally with
> `jekyll serve --drafts`.

---

## 1. Directory layout

Posts are grouped by **topical category** in kebab-case folders:

```
pages/_posts/
├── ai-machine-learning/
├── business/
├── creative-experimental/
├── culture-society/
├── data-analytics/
├── devops/
├── learning/
├── programming/
├── system-administration/
├── tools-environment/
├── trends-ideas/
├── web-development/
└── .markdownlint.json   ← posts-scoped lint config (extends repo root)
```

The folder name is **not** the Jekyll category. The `categories:` frontmatter
field is the source of truth (see §3) and is what Jekyll uses to build the
`/categories/<slug>/` pages.

---

## 2. File naming

```
YYYY-MM-DD-kebab-case-slug.md
```

- **Date**: must match the `date:` frontmatter field
- **Slug**: kebab-case, lowercase, ≤ ~80 chars, no stop-words at start
- **Extension**: `.md` only

✅ `2025-11-17-deploying-jekyll-sites-to-azure-cloud.md`
❌ `2025-11-17_DeployingJekyllSitesToAzureCloud.md`

---

## 3. Required frontmatter

```yaml
---
title: "Human-readable title"
description: "≤ 160 char SEO description; first sentence is fine"
date: YYYY-MM-DDTHH:MM:SS-05:00     # ISO 8601, matches filename
categories: ["DevOps", "Tutorials"]  # Title Case; folder-derived default ok
tags: [docker, jekyll, ci-cd]        # lowercase, kebab-case
author: "Bamr"                       # default value if unsure
preview: "images/previews/<slug>.png" # AI-generated preview image
draft: false                          # set true to relocate to _drafts/
---
```

Recommended additions:

```yaml
excerpt: "Short summary used in card layouts"
lastmod: YYYY-MM-DDTHH:MM:SS-05:00
layout: "post"   # only override the default if you have a reason
```

### Auto-fill helper

If you skip optional metadata, run:

```bash
python3 scripts/validation/fix-frontmatter.py pages/_posts --verbose
```

It populates missing `date`, `categories`, and `description` (from the first
prose paragraph). Idempotent.

---

## 4. Validation tooling

| What | Command | When |
|------|---------|------|
| Frontmatter | `python3 scripts/validation/frontmatter-validator.py pages/_posts/ --type posts` | Pre-commit + CI (`frontmatter-validation.yml`) |
| Markdown lint | `markdownlint-cli2 "pages/_posts/**/*.md"` | Pre-commit + CI (`posts-markdown-lint.yml`) |
| Internal links | `lychee --offline --base "$PWD/_site" pages/_posts/**/*.md` | After `bundle exec jekyll build` |
| External links | `lychee --base "$PWD/_site" --max-concurrency 10 --timeout 15 pages/_posts/**/*.md` | Periodically; results in `link-check-results/posts-external-baseline.md` |
| Build | `bundle exec jekyll build --config _config.yml,_config_dev.yml` | Before every PR |

### Markdownlint config

Posts have a relaxed config at `pages/_posts/.markdownlint.json` that
**extends the repo-root config** and disables four rules that produce noise
on legitimate blog content:

| Rule | Why disabled |
|------|--------------|
| MD025 (single-h1) | Frontmatter title is the implicit H1 |
| MD036 (emphasis-as-heading) | Many posts use `**Bold:**` as a stylistic intro |
| MD040 (fenced-code-language) | Short snippets / pseudo-code don't need a language |
| MD060 (table-column-style) | Cosmetic; doesn't affect rendering |

It also widens `MD033` (no-inline-html) `allowed_elements` to include the
SVG/multimedia/table elements posts legitimately use.

---

## 5. Link hygiene

- **Prefer Jekyll absolute paths** for internal links: `/quests/level-0000-git-basics/`,
  `/categories/architecture/`. Lychee resolves them against `_site/` after build.
- **Use HTTPS** for all external links.
- **Don't hard-code GitHub line numbers** unless the file is stable; prefer
  permalinks (commit SHA in URL) for code references.
- **External link rot** is tracked at
  [`link-check-results/posts-external-baseline.md`](../../link-check-results/posts-external-baseline.md).
  Add new known-broken external links there with status, context, and
  remediation strategy.

---

## 6. Preview images

- Frontmatter `preview:` should reference a PNG under `assets/images/previews/`.
- Generate with:

  ```bash
  ./scripts/generation/generate-preview-images.sh -f pages/_posts/<file>.md
  ```

- Requires `OPENAI_API_KEY` in `.env`.
- Default size: `1792x1024` (DALL-E 3 landscape).

---

## 7. Drafts and lifecycle

| Stage | Location | Frontmatter | Built? |
|-------|----------|-------------|--------|
| Draft | `pages/_drafts/` | `draft: true` (optional in `_drafts/`) | Only with `--drafts` |
| Published | `pages/_posts/<category>/` | `draft: false` (or omitted) | Yes |
| Archived | `pages/_posts/<category>/` | `archived: true` | Yes, with notice banner |

To move a draft into a category folder when ready:

```bash
git mv pages/_drafts/<file>.md pages/_posts/<category>/<YYYY-MM-DD>-<slug>.md
# Then ensure date: field in frontmatter matches the new filename
```

---

## 8. Cleanup history

The `chore/posts-mass-cleanup` branch (Nov 2025) brought the collection from:

| Metric | Before | After |
|--------|--------|-------|
| Files | 124 | 86 (+ 34 moved to `_drafts/`) |
| Frontmatter valid | 73/124 | 86/86 |
| Frontmatter errors | 102 | 0 |
| SEO score | 54.5 | 65.5 |
| Markdownlint issues | 1,790 | 25 |
| Internal links broken | unknown | 0/282 |

See `TODO/posts-cleanup.md` for the full phase-by-phase plan and
[`work/posts-cleanup/reports/`](../../work/posts-cleanup/reports/) (gitignored)
for the raw validator outputs at each phase.

---

## 9. Related docs

- [`.github/instructions/posts.instructions.md`](../../.github/instructions/posts.instructions.md) — authoring guidelines for AI agents
- [`scripts/validation/`](../../scripts/validation/) — all validation scripts
- [`scripts/generation/generate-preview-images.sh`](../../scripts/generation/generate-preview-images.sh) — preview image generator
- [`link-check-results/posts-external-baseline.md`](../../link-check-results/posts-external-baseline.md) — known external link rot

---

**Last updated**: 2025-11-16 (Phase 7 of `chore/posts-mass-cleanup`)
