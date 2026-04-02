---
title: Styling & Navigation
author: bamr87
description: Customize your site's look with theme skins, colors, and CSS — then configure navigation menus, sidebars, search, and comments.
permalink: /quickstart/styling-navigation/
categories:
  - quickstart
slug: styling-navigation
lastmod: 2026-04-02T03:14:50.937Z
draft: false
date: 2026-04-01T00:00:00.000Z
difficulty: 🟡 Medium
estimatedTime: 25-35 minutes
prerequisites:
  - Site configured (see [Site Configuration](/quickstart/site-configuration/))
  - Understand layouts and includes (see [Theme Architecture](/quickstart/theme-architecture/))
tags:
  - styling
  - navigation
  - css
  - themes
  - sidebar
keywords:
  primary:
    - jekyll styling
    - site navigation
    - theme skins
  secondary:
    - css customization
    - sidebar config
    - giscus comments
sidebar:
  nav: quickstart
---

This guide covers **Phases 9 and 10** of the [Quick Start](/quickstart/) — styling your site with skins, colors, and CSS, then setting up navigation, sidebars, search, and comments.

---

## Theme Skins

Change the entire look with one line in `_config.yml`:

```yaml
theme_skin: "dark"
```

### Available Skins

| Skin | Description |
|------|-------------|
| `air` | Light, clean, minimal |
| `aqua` | Blue-tinted light theme |
| `contrast` | High-contrast for accessibility |
| `dark` | Dark background, light text |
| `dirt` | Earthy tones |
| `neon` | Vibrant colors on dark |
| `mint` | Green-tinted light theme |
| `plum` | Purple-tinted dark theme |
| `sunrise` | Warm orange/gold tones |

Switch skins and rebuild to preview — no other changes needed.

---

## Color Overrides

Override any theme color in `_config.yml`:

```yaml
theme_color:
  main: "#007bff"       # Primary brand color
  secondary: "#6c757d"  # Secondary elements
  bg: "#111111"         # Background
  text: "#f9f9f9"       # Text color
  link: "#007bff"       # Link color
  link_hover: "#0056b3" # Link hover state
  red: "#a11111"
  yellow: "#ffe900"
  green: "#24b47e"
  blue: "#007bff"
  white: "#f9f9f9"
  gray: "#5a5a5a"
  black: "#111111"
```

These override the skin defaults, so you can use a base skin and tweak specific colors.

---

## Custom CSS

Add your own styles in `assets/css/`. Any SCSS or CSS file in that directory is compiled and loaded by the theme.

### Assets Structure

```
assets/
├── css/            # Your custom stylesheets (SCSS or CSS)
├── js/             # Custom JavaScript
│   ├── particles.js    # Background particle effects
│   └── color-modes.js  # Theme switching logic
├── images/         # Site images, favicons, og:image
├── gif/            # Animated images
└── svg/            # Vector graphics
```

### Example: Custom Stylesheet

Create `assets/css/custom.scss`:

```scss
---
---

// Override heading colors
h1, h2, h3 {
  color: var(--theme-main);
}

// Custom card styling
.quest-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
```

The empty frontmatter (`---` lines) at the top tells Jekyll to process the file through its SCSS pipeline.

---

## Navigation Configuration

Navigation menus are defined as YAML files in `_data/navigation/`.

### Main Navigation

`_data/navigation/main.yml`:

```yaml
- title: "Quick-Start"
  children:
    - title: "Machine Setup"
      url: /quickstart/machine-setup/
    - title: "GitHub Setup"
      url: /quickstart/github/
    - title: "Jekyll Setup"
      url: /quickstart/jekyll/

- title: "Journey"
  children:
    - title: "Posts"
      url: /posts/
    - title: "Quests"
      url: /quests/home/
```

### Sidebar Navigation

Each collection can have its own sidebar. Set it in frontmatter:

```yaml
sidebar:
  nav: quests    # References _data/navigation/quests.yml
```

Or set it globally via defaults in `_config.yml`:

```yaml
defaults:
  - scope:
      path: pages/_quests
      type: quests
    values:
      sidebar:
        nav: quests
```

### Navigation File Patterns

| File | Controls | Used By |
|------|----------|---------|
| `_data/navigation/main.yml` | Top navbar | All pages |
| `_data/navigation/quests.yml` | Quest sidebar | Quest pages |
| `_data/navigation/posts.yml` | Posts sidebar | Blog posts |
| `_data/navigation/quickstart.yml` | Quickstart sidebar | Setup guides |
| `_data/navigation/docs.yml` | Docs sidebar | Documentation |

### Adding a New Nav Item

Edit the appropriate YAML file and add an entry:

```yaml
- title: "New Section"
  children:
    - title: "First Page"
      url: /new-section/first-page/
    - title: "Second Page"
      url: /new-section/second-page/
```

Rebuild the site to see changes.

---

## Search

Jekyll can integrate with client-side or hosted search:

| Solution | Type | Setup |
|----------|------|-------|
| **Lunr.js** | Client-side | No server needed, works with static sites |
| **Algolia** | Hosted API | Fast, powerful, requires account |
| **Custom search page** | JSON index | Jekyll generates a JSON index, JS searches it |

The zer0-mistakes theme includes a search page that uses a JSON index generated at build time.

---

## Comments (Giscus)

[Giscus](https://giscus.app/) uses GitHub Discussions as a comments backend — no separate database needed.

### Enable Comments

Per-page in frontmatter:

```yaml
comments: true
```

### Global Configuration

In `_config.yml`:

```yaml
giscus:
  enabled: true
  data-repo: "bamr87/it-journey"
  data-repo-id: "your-repo-id"
  data-category-id: "your-category-id"
  data-mapping: "pathname"
  data-theme: "preferred_color_scheme"
```

To get your repo and category IDs, visit [giscus.app](https://giscus.app/) and follow the setup wizard.

---

## What's Next

| Next Step | Guide |
|-----------|-------|
| Run your site locally with Docker | [Local Development](/quickstart/local-development/) |
| Deploy to GitHub Pages or Azure | [Deployment](/quickstart/deployment/) |
| Set up CI/CD automation | [CI/CD & Automation](/quickstart/cicd-automation/) |

> **IT-Journey Quests:** [CSS Styling Basics](/quests/intermediate/css-styling-basics/) · [Bootstrap Framework](/quests/intermediate/bootstrap-framework/) · [GitHub Pages Hidden Gem](/quests/advanced/github-pages-hidden-gem/)
>
> **External Docs:** [Jekyll Assets](https://jekyllrb.com/docs/assets/) · [Bootstrap Docs](https://getbootstrap.com/docs/) · [Jekyll Navigation](https://jekyllrb.com/tutorials/navigation/) · [Giscus](https://giscus.app/)
