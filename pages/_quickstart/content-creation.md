---
title: Content Creation
author: bamr87
description: Create blog posts, quests, documentation, and other content types with proper frontmatter, naming conventions, and file organization.
permalink: /quickstart/content-creation/
categories:
  - quickstart
slug: content-creation
lastmod: 2026-04-02T03:14:50.929Z
draft: false
date: 2026-04-01T00:00:00.000Z
difficulty: 🟢 Easy
estimatedTime: 20-30 minutes
prerequisites:
  - Jekyll and theme installed (see [Jekyll Setup](/quickstart/jekyll/))
  - Understand layouts and frontmatter (see [Theme Architecture](/quickstart/theme-architecture/))
tags:
  - content
  - frontmatter
  - posts
  - quests
  - markdown
keywords:
  primary:
    - jekyll content creation
    - frontmatter standards
    - blog posts
  secondary:
    - quests
    - documentation
    - content types
sidebar:
  nav: quickstart
---

This guide covers **Phase 8** of the [Quick Start](/quickstart/) — creating content across all IT-Journey collection types with proper frontmatter, naming, and organization.

---

## Frontmatter — The Metadata That Powers Everything

Every content file starts with YAML frontmatter between `---` fences. These fields control how the page is rendered, categorized, and discovered.

### Minimum Required Frontmatter (All Content Types)

```yaml
---
title: "Your Page Title"
---
```

That's it — Jekyll will render the page. But for a production site, you'll want much more.

---

## Blog Posts

Posts live in `pages/_posts/` and follow a strict naming convention.

### Naming Convention

```
YYYY-MM-DD-slug-title-with-hyphens.md
```

Example: `2026-03-31-deploying-jekyll-to-azure.md`

The date in the filename is used as the post's publication date. The slug becomes part of the URL.

### Post Frontmatter

```yaml
---
title: "Deploying Jekyll to Azure Cloud"
layout: articles
description: "Step-by-step guide to deploying a Jekyll site on Azure Static Web Apps."
date: 2026-03-31
lastmod: 2026-03-31
author: bamr87
categories:
  - devops
tags:
  - jekyll
  - azure
  - deployment
draft: false
image: /assets/images/azure-deploy-cover.png
mermaid: true
toc: true
---
```

### Creating a Post

**Option A — Manually:**

```bash
touch pages/_posts/2026-03-31-my-first-post.md
```

**Option B — Front Matter CMS:**

1. Open the Front Matter dashboard
2. Click **Create content**
3. Select the "posts" folder
4. Fill in the fields visually
5. The CMS generates a properly formatted file

### Post Organization

Posts are auto-organized by category into subfolders:

```
pages/_posts/
├── ai & machine learning/
├── devops/
├── infrastructure/
├── tutorials/
└── web development/
```

---

## Quests

Quests are gamified learning content with RPG-style progression. They live in `pages/_quests/` organized by binary level directories.

### Quest Directory Structure

```
pages/_quests/
├── 0000/    # Level 0000 — Foundation
├── 0001/    # Level 0001 — Beginner (Frontend)
├── 0010/    # Level 0010 — Intermediate
├── 0011/    # Level 0011 — Advanced
├── 0100/    # Level 0100 — Containers
├── 0101/    # Level 0101 — CI/CD
├── 0110/    # Level 0110 — Databases
├── 1000/    # Level 1000 — Cloud
├── 1001/    # Level 1001 — Kubernetes
├── 1010/    # Level 1010 — Monitoring
├── 1100/    # Level 1100 — Data Engineering
├── 1101/    # Level 1101 — ML/AI
├── 1110/    # Level 1110 — System Design
└── 1111/    # Level 1111 — Leadership
```

### Quest Frontmatter

```yaml
---
title: "Docker Container Fundamentals"
layout: quest
description: "Master Docker container images, volumes, and networking."
level: "0100"              # Binary level code
difficulty: "intermediate"  # beginner, intermediate, advanced, expert
quest_type: "containers"
estimated_time: "60-75 min"
xp: 500
achievements:
  - "Container Commander"
platforms:
  - macOS
  - Windows
  - Linux
prerequisites:
  - "Terminal Fundamentals"
  - "Git Basics"
---
```

### Binary Level System

| Level | Tier | Focus Area |
|-------|------|-----------|
| `0000` | Foundation | OS setup, terminal, Git, Markdown, VS Code |
| `0001` | Beginner | GitHub Pages, Jekyll, YAML, Liquid |
| `0010` | Intermediate | JavaScript, CSS, Bootstrap, Bash |
| `0011` | Advanced | Git workflows, plugins, SEO, analytics |
| `0100` | Containers | Docker, Docker Compose |
| `0101` | CI/CD | GitHub Actions, pipelines |
| `0110` | Databases | SQL, data modeling |
| `1000` | Cloud | AWS, Azure, IaC |
| `1001` | Kubernetes | Pods, workloads, config |
| `1010` | Monitoring | Prometheus, Grafana, ELK |
| `1100` | Data Eng. | Stream processing, warehousing |
| `1101` | ML/AI | Python data science, deep learning |
| `1110` | Architecture | Microservices, design patterns |
| `1111` | Leadership | Technical leadership, mentorship |

---

## Documentation

Docs live in `pages/_docs/` and use the `default` layout.

### Doc Frontmatter

```yaml
---
title: "API Reference"
layout: default
description: "Complete API reference for the IT-Journey platform."
categories:
  - reference
---
```

---

## Other Content Types

### Quickstart Guides

```
pages/_quickstart/
```

Quickstart guides like this one use the `default` layout with a `quickstart` sidebar nav.

### Notebooks

```
pages/_notebooks/
```

Jupyter notebooks converted to Markdown, using the `journals` layout.

### Notes

```
pages/_notes/
```

Draft notes and code snippets using the `default` layout.

### About Pages

```
pages/_about/
```

About pages, profiles, and feature descriptions.

---

## Content Types Summary

| Collection | Folder | Layout | Naming Convention | Permalink Pattern |
|-----------|--------|--------|-------------------|-------------------|
| Posts | `pages/_posts/` | `articles` | `YYYY-MM-DD-slug.md` | `/posts/YYYY/MM/DD/slug/` |
| Quests | `pages/_quests/` | `quest` | `quest-name.md` in level folder | `/quests/category/name/` |
| Docs | `pages/_docs/` | `default` | `descriptive-name.md` | `/docs/category/name/` |
| Quickstart | `pages/_quickstart/` | `default` | `descriptive-name.md` | `/quickstart/name/` |
| Notebooks | `pages/_notebooks/` | `journals` | `name.md` or converted `.ipynb` | `/notebooks/path/name/` |
| Notes | `pages/_notes/` | `default` | `descriptive-name.md` | `/notes/path/name/` |
| About | `pages/_about/` | `default` | `descriptive-name.md` | `/about/category/name/` |

---

## Best Practices

1. **Always include `title` and `description`** — they drive SEO and site navigation
2. **Set `draft: true`** for work in progress — draft pages are hidden in production
3. **Use categories and tags consistently** — they power filtering and navigation
4. **Add `lastmod` dates** — helps search engines and readers track freshness
5. **Use Front Matter CMS** for visual editing — reduces frontmatter errors
6. **Follow naming conventions** — especially the `YYYY-MM-DD` date prefix for posts

---

## What's Next

| Next Step | Guide |
|-----------|-------|
| Style your site with skins and custom CSS | [Styling & Navigation](/quickstart/styling-navigation/) |
| Run the site locally with Docker | [Local Development](/quickstart/local-development/) |
| Deploy to GitHub Pages | [Deployment](/quickstart/deployment/) |

> **IT-Journey Docs:** [Frontmatter Standards](/docs/standards/FRONTMATTER_STANDARDS/) · [Content Guidelines](/docs/standards/CONTENT_GUIDELINES/)
>
> **IT-Journey Quests:** [Markdown Mastery](/quests/init_world/markdown-mastery/) · [Forge Your Character](/quests/frontend/forge-your-character/)
