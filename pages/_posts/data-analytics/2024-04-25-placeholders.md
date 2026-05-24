---
title: "Content Placeholders: Templates That Survive Contact With Authors"
description: "How Front Matter CMS placeholders cut frontmatter drift on a 600-file Jekyll site, and the four template patterns I keep reaching for."
date: '2024-04-25T10:40:43.000Z'
lastmod: '2026-05-24T00:00:00.000Z'
author: bamr87
permalink: /posts/content-placeholders-front-matter/
categories: [Data & Analytics, Tools & Environment]
tags:
  - frontmatter
  - jekyll
  - templates
  - content-strategy
  - data-quality
keywords:
  - front matter cms
  - content placeholders
  - jekyll templates
  - frontmatter consistency
  - content authoring
excerpt: "Templates do not enforce consistency. Placeholders do — they catch the fields you forgot before the validator ever sees them."
source: https://frontmatter.codes/docs/content-creation/placeholders
draft: false
---

## The Drift Problem

A Jekyll site with 600 markdown files has a frontmatter consistency problem whether you notice it or not. Some posts use `description`, some use `excerpt`, some define both with subtly different content. Categories appear as strings in 2022 and as YAML lists in 2024. The `lastmod` field exists on roughly 40% of the corpus, picked at random.

Most of this drift comes from a single, common situation: someone opened a new post in a different editor, copy-pasted the frontmatter from the file next to it, and renamed two fields. The template told them what to write; nothing told them what to *include*.

## What Placeholders Solve

[Front Matter CMS](https://frontmatter.codes) has a feature called **placeholders** that sits one layer underneath your content templates. A placeholder is a small declarative rule: "for this template, when the author opens a new file, pre-fill this field with this value."

The combination — template plus placeholders — covers the two halves of the consistency problem:

| Template | Placeholders |
|---|---|
| Says *which fields exist* | Says *what each field should contain by default* |
| Defines structure | Defines values |
| Stops authors from forgetting a key | Stops authors from leaving the key blank |

A placeholder for `date` becomes `{{now}}`. A placeholder for `slug` becomes `{{slugify ${title}}}`. A placeholder for `author` becomes the current user. By the time the file opens, the boring fields are filled in correctly and the author can focus on the body.

## The Four Patterns I Reach For

After running this on IT-Journey, four placeholder patterns covered roughly 90% of what we needed.

### 1. Time-stamped fields

```json
{
  "title": "Date now",
  "id": "DATE_NOW",
  "value": "{{now|YYYY-MM-DDTHH:mm:ss.SSSZ}}"
}
```

Applied to `date`, `lastmod`, and `publishDate`. Stops the "did I copy this from a 2022 post?" problem before it starts.

### 2. Slug derivation

```json
{
  "title": "Slug",
  "id": "SLUG",
  "value": "{{slugify ${title}}}"
}
```

Applied to `slug` and to `permalink` (with a path prefix). The slug always matches the title, even if the author renames the file later.

### 3. Author identity

```json
{
  "title": "Author",
  "id": "AUTHOR",
  "value": "{{user}}"
}
```

Removes the "imported as `2024-04-25 16:19:09.808000+00:00`" failure mode that broke our own `author` field on a few posts before this was set up.

### 4. Defaults for required-but-boring fields

```json
{
  "title": "Draft flag",
  "id": "DRAFT_FALSE",
  "value": "false"
}
```

Applied to `draft`. The default is "publishable"; authors must explicitly flip to `true` if they want to keep it private. This matches how the team actually works — most posts are intended to ship.

## Wiring It Up

In `frontmatter.json`:

```json
{
  "frontMatter.taxonomy.contentTypes": [
    {
      "name": "post",
      "pageBundle": false,
      "previewPath": null,
      "fields": [
        { "title": "Title", "name": "title", "type": "string" },
        { "title": "Description", "name": "description", "type": "string" },
        { "title": "Date", "name": "date", "type": "datetime", "default": "{{now}}" },
        { "title": "Author", "name": "author", "type": "string", "default": "{{user}}" },
        { "title": "Draft", "name": "draft", "type": "boolean", "default": false }
      ]
    }
  ]
}
```

The `default` keys on each field are the placeholders. Open a new post via the Front Matter sidebar and those four fields are already populated correctly.

## What It Did Not Solve

Placeholders fix the new-content path. They do nothing for the 600 files that already exist. For those, a normalizer script (we use `scripts/content/normalize-frontmatter.py`) walks the tree, coerces string-form categories into lists, normalizes dates to ISO 8601 with milliseconds, and bumps `lastmod` only on files that actually changed.

Two tools, two jobs. Placeholders make the new files correct. The normalizer makes the old files correct. Both run on every CI build now, and the drift has stopped accumulating.

## Related

- [Front Matter CMS — Placeholders documentation](https://frontmatter.codes/docs/content-creation/placeholders)
- [Post: VS Code Front Matter Fork Development Setup](/posts/vscode-front-matter-fork-development-setup/)
- [Doc: Frontmatter Preview Solution](/docs/frontmatter-preview-solution/)
