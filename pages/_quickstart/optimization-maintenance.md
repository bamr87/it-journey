---
title: "Optimization & Maintenance"
author: bamr87
description: "Optimize your Jekyll site for SEO, performance, and accessibility — then maintain it with dependency updates, content reviews, and scaling patterns."
permalink: /quickstart/optimization-maintenance/
categories:
  - quickstart
slug: optimization-maintenance
lastmod: 2026-04-01T00:00:00.000Z
draft: false
date: 2026-04-01T00:00:00.000Z
difficulty: 🟡 Medium
estimatedTime: 20-30 minutes
prerequisites:
  - Site deployed (see [Deployment](/quickstart/deployment/))
  - CI/CD configured (see [CI/CD & Automation](/quickstart/cicd-automation/))
tags:
  - seo
  - performance
  - accessibility
  - maintenance
keywords:
  primary:
    - jekyll seo
    - site performance
    - accessibility
  secondary:
    - dependency updates
    - content maintenance
    - scaling
sidebar:
  nav: quickstart
---

This guide covers **Phases 14 and 15** of the [Quick Start](/quickstart/) — optimizing your site for SEO, performance, and accessibility, then keeping it healthy with ongoing maintenance and scaling.

---

## SEO Configuration

The `jekyll-seo-tag` plugin automatically generates meta tags from your `_config.yml` and page frontmatter.

### Site-Level SEO

```yaml
# _config.yml
title: "IT-Journey"
description: "Democratizing IT education"
url: "https://it-journey.dev"
og_image: "/assets/images/wizard-on-journey.png"
```

### Per-Page SEO

```yaml
---
title: "Page Title"
description: "Page-specific description for search engines."
image: /assets/images/page-cover.jpg
---
```

### Auto-Generated Assets

| Plugin | Generates | URL |
|--------|-----------|-----|
| `jekyll-sitemap` | XML sitemap | `/sitemap.xml` |
| `jekyll-feed` | RSS feed | `/feed.xml` |
| `jekyll-seo-tag` | Meta tags | In `<head>` of every page |

---

## Performance Checklist

- [ ] **Optimize images** before committing (max width 1200px, compress with tools like ImageOptim)
- [ ] **Lazy load** images below the fold: `loading="lazy"` attribute
- [ ] **Minimize custom JavaScript** — only load what's needed
- [ ] **Enable minification** in production: `JEKYLL_ENV=production`
- [ ] **Use CDN** for static assets when self-hosting
- [ ] **Audit with Lighthouse** — run Chrome DevTools → Lighthouse tab

### Image Optimization Tips

```bash
# Install ImageOptim CLI (macOS)
brew install imageoptim-cli

# Optimize all images in assets
imageoptim assets/images/

# Or use sips to resize (macOS built-in)
sips --resampleWidth 1200 assets/images/large-photo.jpg
```

---

## Accessibility Checklist

- [ ] All images have descriptive `alt` text
- [ ] Color contrast meets WCAG AA (4.5:1 ratio for text)
- [ ] All interactive elements are keyboard-navigable
- [ ] Heading hierarchy is logical (h1 → h2 → h3, no skips)
- [ ] Links have descriptive text (not "click here")
- [ ] Language attribute set: `<html lang="en">`
- [ ] Forms have associated labels
- [ ] Focus indicators are visible

### Testing Accessibility

| Tool | Type | URL |
|------|------|-----|
| **Lighthouse** | Browser built-in | Chrome DevTools |
| **axe DevTools** | Browser extension | [deque.com/axe](https://www.deque.com/axe/) |
| **WAVE** | Online checker | [wave.webaim.org](https://wave.webaim.org/) |
| **Pa11y** | CLI tool | `npm install -g pa11y` |

---

## Keeping Dependencies Updated

```bash
# Update Ruby gems
bundle update

# Check for outdated gems
bundle outdated

# Update Docker images
docker-compose pull
docker-compose up --build -d
```

The **Dependency Checker** workflow also alerts you automatically on a schedule.

---

## Content Maintenance

| Task | Frequency | Tool/Command |
|------|-----------|-------------|
| Fix broken links | Weekly (automated) | Link Health Guardian workflow |
| Validate quest frontmatter | On PR (automated) | Frontmatter Validation workflow |
| Organize posts by category | Weekly (automated) | Organize Posts workflow |
| Update content statistics | As needed | `make stats-update` |
| Review draft content | Monthly | Front Matter CMS dashboard |

---

## Scaling Your Content

As your site grows, these patterns help manage complexity:

### Add New Content Types

Define new collections in `_config.yml`:

```yaml
collections:
  tutorials:
    output: true
    permalink: /tutorials/:name/
```

Create the directory:

```bash
mkdir -p pages/_tutorials
```

Add defaults:

```yaml
defaults:
  - scope:
      path: pages/_tutorials
      type: tutorials
    values:
      layout: default
      sidebar:
        nav: tutorials
```

### Keep Navigation Updated

Add entries to `_data/navigation/` when creating new sections. Each collection should have its own navigation YAML file.

### Use Data Files

Move structured data out of content files and into `_data/` YAML files. Multiple pages can reference the same data.

### Extract Includes

When HTML patterns repeat across layouts, extract them into `_includes/` partials.

### Extend with Plugins

Custom Ruby plugins in `_plugins/` can generate pages, transform content, or add Liquid filters. Note: custom plugins don't work on default GitHub Pages — use GitHub Actions for the build step instead.

---

## Version Management

Use the version manager script for semantic versioning across the project:

```bash
./scripts/core/version-manager.sh patch   # Bug fixes: 1.0.0 → 1.0.1
./scripts/core/version-manager.sh minor   # New features: 1.0.0 → 1.1.0
./scripts/core/version-manager.sh major   # Breaking changes: 1.0.0 → 2.0.0
```

---

## Monthly Maintenance Routine

1. **Update dependencies**: `bundle update` and `docker-compose pull`
2. **Run link checker**: `python3 scripts/link-checker.py --scope website`
3. **Review draft content**: Check Front Matter CMS dashboard
4. **Check Lighthouse scores**: Run audits on key pages
5. **Update statistics**: `make stats-update`
6. **Review GitHub Dependabot alerts**: Fix security issues

---

## What's Next

You've completed the full Quick Start guide. From here:

| Goal | Resource |
|------|----------|
| Deepen your skills | Explore [IT-Journey Quests](/quests/home/) |
| Contribute to the project | Read the [Contributing Guide](/CONTRIBUTING/) |
| Ask questions | Join [IT-Journey Discussions](https://github.com/bamr87/it-journey/discussions) |
| Learn more about Jekyll | [Jekyll Documentation](https://jekyllrb.com/docs/) |

> **IT-Journey Quests:** [SEO Optimization](/quests/advanced/seo-optimization/) · [Analytics Integration](/quests/advanced/analytics-integration/)
>
> **IT-Journey Docs:** [Scripts Guide](/docs/scripts/SCRIPTS_GUIDE/) · [GitHub Actions](/docs/workflows/GITHUB_ACTIONS/)
>
> **External Docs:** [Jekyll SEO Tag](https://github.com/jekyll/jekyll-seo-tag) · [WCAG Guidelines](https://www.w3.org/WAI/standards-guidelines/wcag/) · [Google Lighthouse](https://developer.chrome.com/docs/lighthouse/)
