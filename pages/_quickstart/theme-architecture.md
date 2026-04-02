---
title: "Theme Architecture"
author: bamr87
description: "Understand how the zer0-mistakes theme builds pages — layouts, includes, Liquid templating, data files, and the Jekyll build pipeline."
permalink: /quickstart/theme-architecture/
categories:
  - quickstart
slug: theme-architecture
lastmod: 2026-04-01T00:00:00.000Z
draft: false
date: 2026-04-01T00:00:00.000Z
difficulty: 🟡 Medium
estimatedTime: 30-40 minutes
prerequisites:
  - Jekyll installed (see [Jekyll Setup](/quickstart/jekyll/))
  - Site configuration complete (see [Site Configuration](/quickstart/site-configuration/))
tags:
  - jekyll
  - liquid
  - layouts
  - includes
  - theme
keywords:
  primary:
    - jekyll theme architecture
    - liquid templating
    - jekyll layouts
  secondary:
    - includes
    - data files
    - zer0-mistakes theme
sidebar:
  nav: quickstart
---

This guide covers **Phase 7** of the [Quick Start](/quickstart/) — how the zer0-mistakes theme assembles pages from layouts, includes, Liquid templates, and data files.

---

## How Jekyll Builds a Page

Every page follows this pipeline:

```
Markdown file (content + frontmatter)
        ↓
Layout template (_layouts/articles.html)
        ↓
Includes (_includes/header.html, sidebar.html, etc.)
        ↓
Theme base layout (root.html → default.html)
        ↓
Static HTML file (in _site/)
```

When you run `jekyll build`, it reads each content file, merges it with its assigned layout, resolves all `{% raw %}{% include %}{% endraw %}` calls, evaluates Liquid expressions, and writes the final HTML to `_site/`.

---

## Layouts

Layouts are HTML templates that wrap your content. Set the layout in front matter:

```yaml
---
layout: articles
title: "My Blog Post"
---
```

### Available Layouts

| Layout | Purpose | Used By |
|--------|---------|---------|
| `root` | Base HTML shell — `<head>`, `<body>`, scripts, stylesheets | Everything (parent of other layouts) |
| `default` | Standard page with header, footer, and sidebar | General pages, docs, notes |
| `articles` | Blog post layout with date, author, tags, reading time | Posts |
| `quest` | Quest layout with level badge, XP, achievements, prerequisites | Quests |
| `quest-collection` | Groups quests by tier in a filterable grid | Quest index pages |
| `journals` | Journal/notebook layout for dated entries | Notebooks |
| `javascript` | Layout for JS-heavy interactive pages | Special pages |

### Layout Inheritance

Layouts chain together. For example:

```
articles.html  →  default.html  →  root.html
(post content)    (header/footer)   (HTML skeleton)
```

The `content` variable in each layout is replaced by the child layout or the page content.

---

## Includes (Partials)

Includes are reusable HTML snippets injected into layouts with:

```liquid
{% raw %}{% include component.html %}{% endraw %}
```

### Key Includes in IT-Journey

```
_includes/
├── components/
│   └── powered-by.html          # Footer attribution
├── contributor/
│   ├── profile_card.html        # Contributor profile card
│   ├── character_sheet.html     # RPG-style character stats
│   ├── achievement_wall.html    # Achievement badge display
│   └── stats_panel.html         # Activity statistics panel
├── content_statistics/          # Site-wide content stats
├── quest-card.html              # Individual quest display card
├── quest-filters.html           # Quest filtering controls
├── quest-stats.html             # Quest completion statistics
└── quest_grid.html              # Quest grid layout
```

### Passing Variables to Includes

```liquid
{% raw %}{% include quest-card.html quest=quest show_xp=true %}{% endraw %}
```

Inside the include, access variables via `include.quest` and `include.show_xp`.

---

## Liquid Templating

Jekyll uses the [Liquid](https://shopify.github.io/liquid/) templating language for dynamic content. There are three main constructs:

### Output Tags

Display variables with double curly braces:

```liquid
{% raw %}{{ page.title }}
{{ site.title }}
{{ page.date | date: "%B %d, %Y" }}
{{ page.content | number_of_words }} words{% endraw %}
```

### Logic Tags

Control flow with `{% raw %}{% %}{% endraw %}` tags:

```liquid
{% raw %}{% if page.comments %}
  {% include comments.html %}
{% endif %}

{% unless page.draft %}
  <p>Published: {{ page.date | date: "%Y-%m-%d" }}</p>
{% endunless %}

{% case page.layout %}
  {% when "quest" %}
    <span class="badge">Quest</span>
  {% when "articles" %}
    <span class="badge">Article</span>
{% endcase %}{% endraw %}
```

### Loops

Iterate over collections and arrays:

```liquid
{% raw %}{% for post in site.posts limit:5 %}
  <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
  <p>{{ post.description }}</p>
{% endfor %}

{% for quest in site.quests %}
  {% if quest.difficulty == "beginner" %}
    {% include quest-card.html quest=quest %}
  {% endif %}
{% endfor %}{% endraw %}
```

### Useful Filters

| Filter | Example | Result |
|--------|---------|--------|
| `date` | `{% raw %}{{ page.date \| date: "%B %d, %Y" }}{% endraw %}` | "March 31, 2026" |
| `upcase` | `{% raw %}{{ "hello" \| upcase }}{% endraw %}` | "HELLO" |
| `slugify` | `{% raw %}{{ "My Title" \| slugify }}{% endraw %}` | "my-title" |
| `where` | `{% raw %}{{ site.quests \| where: "difficulty", "beginner" }}{% endraw %}` | Filtered array |
| `sort` | `{% raw %}{{ site.posts \| sort: "date" \| reverse }}{% endraw %}` | Sorted array |
| `markdownify` | `{% raw %}{{ page.description \| markdownify }}{% endraw %}` | HTML from markdown |
| `number_of_words` | `{% raw %}{{ page.content \| number_of_words }}{% endraw %}` | Word count |
| `strip_html` | `{% raw %}{{ page.content \| strip_html }}{% endraw %}` | Plain text |

---

## Data Files

YAML files in `_data/` are accessible as `site.data.*` in templates. This keeps structured data out of your templates and content files.

### IT-Journey Data Files

| File | Contains | Access As |
|------|----------|-----------|
| `_data/navigation/main.yml` | Primary site menu | `site.data.navigation.main` |
| `_data/navigation/quests.yml` | Quest sidebar menu | `site.data.navigation.quests` |
| `_data/navigation/posts.yml` | Posts sidebar menu | `site.data.navigation.posts` |
| `_data/navigation/quickstart.yml` | Quickstart sidebar | `site.data.navigation.quickstart` |
| `_data/ui-text.yml` | UI strings (i18n-ready) | `site.data.ui-text` |
| `_data/prerequisites.yml` | Learning prerequisites | `site.data.prerequisites` |
| `_data/content_statistics.yml` | Content stats | `site.data.content_statistics` |

### Using Data in Templates

```liquid
{% raw %}{% for item in site.data.navigation.main %}
  <a href="{{ item.url }}">{{ item.title }}</a>
  {% if item.children %}
    <ul>
      {% for child in item.children %}
        <li><a href="{{ child.url }}">{{ child.title }}</a></li>
      {% endfor %}
    </ul>
  {% endif %}
{% endfor %}{% endraw %}
```

---

## The `_site/` Output Directory

Everything Jekyll generates ends up in `_site/`. This directory:

- Is **regenerated** each build — never edit files here directly
- Contains only static files (HTML, CSS, JS, images)
- Is the directory you deploy to your hosting provider
- Is listed in `.gitignore` so it's not committed

---

## Customizing the Theme

### Override a Theme Layout

To override a theme layout, create the same file in your project:

```
_layouts/default.html    ← Your override takes priority
```

Jekyll checks your project first, then the theme gem.

### Override an Include

Same pattern:

```
_includes/header.html    ← Your override takes priority
```

### Add New Layouts or Includes

Add them to `_layouts/` or `_includes/` in your project. They're automatically available.

---

## What's Next

| Next Step | Guide |
|-----------|-------|
| Create posts, quests, and docs | [Content Creation](/quickstart/content-creation/) |
| Style your site with skins and CSS | [Styling & Navigation](/quickstart/styling-navigation/) |
| Run the site locally | [Local Development](/quickstart/local-development/) |

> **IT-Journey Quests:** [Liquid Templating](/quests/frontend/liquid-templating/) · [Jekyll Fundamentals](/quests/frontend/jekyll-fundamentals/)
>
> **External Docs:** [Jekyll Layouts](https://jekyllrb.com/docs/layouts/) · [Jekyll Includes](https://jekyllrb.com/docs/includes/) · [Liquid Reference](https://shopify.github.io/liquid/) · [Jekyll Data Files](https://jekyllrb.com/docs/datafiles/)
