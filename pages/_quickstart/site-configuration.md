---
title: Site Configuration
author: bamr87
description: Complete walkthrough of _config.yml — site identity, theme skins, collections, default frontmatter, plugins, comments, and analytics for the zer0-mistakes theme.
permalink: /quickstart/site-configuration/
categories:
  - quickstart
slug: site-configuration
lastmod: 2026-04-02T03:14:50.902Z
draft: false
date: 2026-04-01T00:00:00.000Z
difficulty: 🟡 Medium
estimatedTime: 30-45 minutes
prerequisites:
  - Jekyll and zer0-mistakes theme installed (see [Jekyll Setup](/quickstart/jekyll/))
  - Basic understanding of YAML syntax
tags:
  - configuration
  - yaml
  - jekyll
  - theme
keywords:
  primary:
    - jekyll configuration
    - config.yml
    - zer0-mistakes theme
  secondary:
    - collections
    - plugins
    - frontmatter defaults
sidebar:
  nav: quickstart
---

This guide covers **Phase 5** of the [Quick Start](/quickstart/) — configuring the `_config.yml` file that controls every aspect of your Jekyll site. This is the brain of your site.

---

## Site Identity

These settings define how your site appears in browsers, search engines, and social media:

```yaml
title: "IT-Journey"
subtitle: "zer0 to her0"
title_url: "/"
title_icon: "globe"
url: "https://it-journey.dev"
baseurl: ""
description: "Democratizing IT education through open-source learning."
founder: "Amr Abdel-Motaleb"
port: 4002
```

| Setting | Purpose | Example |
|---------|---------|---------|
| `title` | Site name in header and browser tab | `"IT-Journey"` |
| `subtitle` | Tagline below the title | `"zer0 to her0"` |
| `url` | Production URL (used for SEO, sitemaps, RSS) | `"https://it-journey.dev"` |
| `baseurl` | Path prefix if hosted in a subfolder | `""` or `"/blog"` |
| `description` | Default meta description for SEO | Short, descriptive text |
| `port` | Local development server port | `4002` |

---

## Theme Skin & Colors

The zer0-mistakes theme ships with **9 built-in skins**. Change the entire look with one line:

```yaml
theme_skin: "dark"
```

**Available skins:**

| Skin | Style |
|------|-------|
| `air` | Light, clean |
| `aqua` | Blue tones |
| `contrast` | High contrast |
| `dark` | Dark background |
| `dirt` | Earthy tones |
| `neon` | Bright accents |
| `mint` | Green tones |
| `plum` | Purple tones |
| `sunrise` | Warm tones |

### Color Overrides

Override any theme color directly in `_config.yml`:

```yaml
theme_color:
  main: "#007bff"       # Primary brand color
  secondary: "#6c757d"  # Secondary elements
  red: "#a11111"
  yellow: "#ffe900"
  green: "#24b47e"
  blue: "#007bff"
  white: "#f9f9f9"
  gray: "#5a5a5a"
  black: "#111111"
```

Additional overrides for page elements:

```yaml
theme_color:
  bg: "#111111"         # Background
  text: "#f9f9f9"       # Text color
  link: "#007bff"       # Link color
  link_hover: "#0056b3" # Link hover state
```

---

## Collections

Collections define your content types. Each collection maps to a folder under `pages/`:

```yaml
collections_dir: pages

collections:
  posts:
    output: true
    permalink: /:collection/:year/:month/:day/:slug/
  quests:
    output: true
    permalink: /:collection/:categories/:name/
  docs:
    output: true
    permalink: /:collection/:categories/:name/
  quickstart:
    output: true
    permalink: /:collection/:name/
  notebooks:
    output: true
    permalink: /:collection/:path/:name/
  notes:
    output: true
    permalink: /:collection/:path/:name/
  about:
    output: true
    permalink: /:collection/:categories/:name/
  hobbies:
    output: true
    permalink: /:collection/:categories/:name/
```

| Setting | Purpose |
|---------|---------|
| `collections_dir` | Root directory containing all collection folders |
| `output: true` | Generate HTML pages for this collection |
| `permalink` | URL pattern for collection pages |

---

## Default Frontmatter

Set automatic frontmatter values by collection so you don't repeat yourself in every file:

```yaml
defaults:
  # All documents
  - scope:
      path: ""
    values:
      layout: root
      author_profile: false
      read_time: true
      comments: false
      share: true
      sidebar:
        nav: main

  # Blog posts
  - scope:
      path: pages/_posts
      type: posts
    values:
      layout: article
      sidebar:
        nav: posts

  # Quests
  - scope:
      path: pages/_quests
      type: quests
    values:
      layout: quest
      sidebar:
        nav: quests

  # Quickstart guides
  - scope:
      path: pages/_quickstart
    values:
      layout: default
      collection: quickstart
      share: true
      related: true
      sidebar:
        nav: quickstart
```

The `scope` determines which files the defaults apply to. The `values` are applied as if they were written in the file's frontmatter (but can be overridden per file).

---

## Markdown Processing

```yaml
markdown: kramdown
kramdown:
  input: GFM           # GitHub Flavored Markdown
  header_offset: 0
  toc_levels: 1..6
  syntax_highlighter: rouge
```

| Setting | Purpose |
|---------|---------|
| `GFM` | Enables GitHub Flavored Markdown (tables, fenced code blocks, task lists) |
| `header_offset` | Shift heading levels (0 = no shift) |
| `toc_levels` | Which heading levels appear in table of contents |
| `rouge` | Syntax highlighter for code blocks |

---

## Plugins

```yaml
plugins:
  - github-pages
  - jekyll-remote-theme
  - jekyll-feed          # RSS feed at /feed.xml
  - jekyll-sitemap       # Automatic sitemap.xml
  - jekyll-seo-tag       # SEO meta tags
  - jekyll-paginate      # Blog pagination
  - jekyll-relative-links

paginate: 10
paginate_path: "/pages/:num/"
```

| Plugin | What It Generates |
|--------|------------------|
| `jekyll-feed` | RSS feed at `/feed.xml` |
| `jekyll-sitemap` | Sitemap at `/sitemap.xml` |
| `jekyll-seo-tag` | `<meta>` tags for SEO and social sharing |
| `jekyll-paginate` | Paginated blog listing |
| `jekyll-remote-theme` | Load themes from GitHub repositories |

---

## Comments (Giscus)

[Giscus](https://giscus.app/) uses GitHub Discussions as a comments backend. Enable it globally:

```yaml
gisgus:
  enabled: true
  data-repo: "bamr87/it-journey"
  data-repo-id: "your-repo-id"
  data-category-id: "your-category-id"
  data-mapping: "pathname"
  data-theme: "preferred_color_scheme"
```

Enable per-page in frontmatter:

```yaml
comments: true
```

To get your repo ID and category ID, visit [giscus.app](https://giscus.app/) and follow the configuration wizard.

---

## Analytics

```yaml
analytics:
  provider: "google-gtag"
  google:
    tracking_id: "G-XXXXXXXXXX"
```

Replace the tracking ID with your Google Analytics measurement ID.

---

## Exclude Files from Build

Prevent certain files and directories from being processed by Jekyll:

```yaml
exclude:
  - scripts/
  - test/
  - docs/
  - work/
  - "*.sh"
  - Dockerfile
  - docker-compose.yml
  - Makefile
  - AGENTS.md
```

This keeps build times fast and avoids publishing internal tooling files.

---

## Development Overrides (_config_dev.yml)

Create a `_config_dev.yml` for local development settings that override production values:

```yaml
# _config_dev.yml
theme: "jekyll-theme-zer0"
url: "http://localhost:4002"
```

Use both configs together:

```bash
bundle exec jekyll serve --config _config.yml,_config_dev.yml
```

Values in `_config_dev.yml` override `_config.yml` where they overlap.

---

## What's Next

| Next Step | Guide |
|-----------|-------|
| Set up VS Code with extensions and Front Matter CMS | [VS Code Setup](/quickstart/vscode-setup/) |
| Understand layouts, includes, and Liquid templating | [Theme Architecture](/quickstart/theme-architecture/) |
| Create posts, quests, and docs | [Content Creation](/quickstart/content-creation/) |

> **IT-Journey Quests:** [YAML Configuration](/quests/frontend/yaml-configuration/) · [Jekyll Plugins](/quests/advanced/jekyll-plugins/) · [SEO Optimization](/quests/advanced/seo-optimization/) · [Analytics Integration](/quests/advanced/analytics-integration/)
>
> **IT-Journey Docs:** [Frontmatter Standards](/docs/standards/FRONTMATTER_STANDARDS/) · [Content Guidelines](/docs/standards/CONTENT_GUIDELINES/)
>
> **External Docs:** [Jekyll Configuration Options](https://jekyllrb.com/docs/configuration/options/) · [Jekyll Collections](https://jekyllrb.com/docs/collections/) · [Jekyll Frontmatter Defaults](https://jekyllrb.com/docs/configuration/front-matter-defaults/) · [kramdown Options](https://kramdown.gettalong.org/options.html) · [Giscus Setup](https://giscus.app/)
