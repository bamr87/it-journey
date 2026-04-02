---
title: "Quick Start: Build a Jekyll Site from Scratch"
author: bamr87
description: End-to-end guide to establishing a development environment, implementing the zer0-mistakes Jekyll theme, and building a CMS-powered site like it-journey.dev — from first install to full deployment.
permalink: /quickstart/
sidebar:
  nav: quickstart
lastmod: 2026-04-02T03:24:28.768Z
date: 2021-12-05T18:52:20.000Z
---

This guide walks you through everything you need to build, configure, and maintain a Jekyll site like [it-journey.dev](https://it-journey.dev) — from installing your first tool to deploying a fully themed, CMS-powered site with CI/CD automation. We're using the [zer0-mistakes](https://github.com/bamr87/zer0-mistakes) theme, [VS Code](https://code.visualstudio.com/) as the editor, [Front Matter CMS](https://frontmatter.codes/) for content management, and [GitHub Pages](https://pages.github.com/) for free hosting.

Every section builds on the one before it. If you already have some tools installed, skip ahead. Each phase links to a dedicated deep-dive guide with full details, examples, and troubleshooting.

---

## Inside This Guide

| Phase | What You'll Do | Guide |
|-------|---------------|-------|
| **1** | Install prerequisites (Ruby, Git, Docker, VS Code) | [Machine Setup](/quickstart/machine-setup/) |
| **2** | Understand how HTML, Markdown, and static sites work | [Web Fundamentals](#phase-2-web-fundamentals) |
| **3** | Create a GitHub repo and clone it locally | [GitHub Setup](/quickstart/github/) |
| **4** | Install Jekyll and the zer0-mistakes theme | [Jekyll Setup](/quickstart/jekyll/) |
| **5** | Configure `_config.yml` — site identity, theme skin, collections | [Site Configuration](/quickstart/site-configuration/) |
| **6** | Set up VS Code with extensions, tasks, and Front Matter CMS | [VS Code & CMS Setup](/quickstart/vscode-setup/) |
| **7** | Understand layouts, includes, Liquid, and YAML data | [Theme Architecture](/quickstart/theme-architecture/) |
| **8** | Create posts, quests, docs, and other content types | [Content Creation](/quickstart/content-creation/) |
| **9–10** | Style your site and add navigation, sidebars, search, comments | [Styling & Navigation](/quickstart/styling-navigation/) |
| **11** | Run your site locally with Docker or native Ruby | [Local Development](/quickstart/local-development/) |
| **12** | Deploy to GitHub Pages, Azure, or other hosts | [Deployment](/quickstart/deployment/) |
| **13** | Set up GitHub Actions for CI/CD, testing, and validation | [CI/CD & Automation](/quickstart/cicd-automation/) |
| **14–15** | Optimize for SEO, performance, accessibility — then maintain and scale | [Optimization & Maintenance](/quickstart/optimization-maintenance/) |

---

## Phase 1: Prerequisites & Machine Setup

Before you write a single line of code, your machine needs the right tools.

| Tool | What It Does |
|------|-------------|
| **Git** | Version control |
| **Ruby 3.2+** | Language Jekyll runs on |
| **Bundler** | Ruby dependency manager |
| **Node.js** | JavaScript runtime |
| **Docker Desktop** | Isolated container environment |
| **VS Code** | Code editor and CMS interface |

### Quick Setup (macOS)

```bash
brew install git ruby node
gem install bundler
brew install --cask docker visual-studio-code
```

### Verify Installation

```bash
git --version        # 2.x+
ruby --version       # 3.2+
bundler --version    # 2.x+
node --version       # 18+
docker --version     # 24+
code --version       # Latest
```

**Full guide:** [Machine Setup](/quickstart/machine-setup/) — cross-platform instructions for macOS, Windows, Linux, and automated setup scripts.

---

## Phase 2: Web Fundamentals

Before you dive into Jekyll, it helps to understand what's actually happening when a browser loads a web page. Jekyll generates static HTML files, so everything you build ultimately becomes HTML, CSS, and (optionally) JavaScript.

### HTML — The Structure

HTML (Hypertext Markup Language) defines the **content and structure** of a web page using tags. A minimal HTML page looks like this:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My Site</title>
    <meta name="description" content="A site about things.">
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <header>
      <h1>Welcome</h1>
    </header>
    <main>
      <p>This is a paragraph of text.</p>
      <a href="https://example.com">This is a link</a>
      <img src="photo.jpg" alt="Description of the photo">
    </main>
    <footer>&copy; 2026</footer>
  </body>
</html>
```

**Key tags to know:**

| Tag | Purpose | Example |
|-----|---------|---------|
| `<h1>` to `<h6>` | Headings (h1 is the biggest) | `<h2>Section Title</h2>` |
| `<p>` | Paragraph of text | `<p>Some text here.</p>` |
| `<a>` | Hyperlink | `<a href="/about">About</a>` |
| `<img>` | Image | `<img src="pic.jpg" alt="A photo">` |
| `<ul>`, `<ol>`, `<li>` | Lists (unordered/ordered) | `<ul><li>Item</li></ul>` |
| `<div>`, `<section>` | Content grouping | `<section id="blog">...</section>` |
| `<header>`, `<footer>` | Page structure | `<header><h1>Title</h1></header>` |
| `<blockquote>` | Quoted text | `<blockquote>A wise saying.</blockquote>` |

### CSS — The Style

CSS (Cascading Style Sheets) controls how HTML **looks** — colors, fonts, layout, spacing. You link a CSS file to your HTML, and the browser applies the styles.

```css
body { font-family: sans-serif; margin: 0; }
h1 { color: #007bff; }
.intro { font-size: 1.2rem; padding: 1rem; }
```

### Markdown — The Shortcut

Jekyll uses **Markdown** instead of raw HTML for content. Markdown is much simpler to write:

```markdown
# This becomes an <h1>
## This becomes an <h2>

This is a paragraph.

**Bold text** and *italic text*.

- Bullet item
- Another item

[Link text](https://example.com)

![Alt text](image.jpg)
```

Jekyll converts Markdown to HTML automatically using [kramdown](https://kramdown.gettalong.org/).

> **External References:** [MDN HTML Basics](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/HTML_basics) · [W3Schools HTML](https://www.w3schools.com/html/) · [Markdown Guide](https://www.markdownguide.org/)
>
> **IT-Journey Quests:** [Markdown Mastery](/quests/init_world/markdown-mastery/) · [HTML/CSS Basics](/quickstart/html-css-basics)

---

## Phase 3: Repository Setup

Every Jekyll site lives in a Git repository. You have three options: fork IT-Journey, start fresh with zer0-mistakes, or use the installer script.

**Full guide:** [GitHub Setup](/quickstart/github/) — all three options with step-by-step instructions and repo structure diagram.

---

## Phase 4: Jekyll & Theme Installation

Install Jekyll, the zer0-mistakes theme, and verify everything works.

```bash
bundle install
bundle exec jekyll serve
# Open http://localhost:4000
```

**Full guide:** [Jekyll Setup](/quickstart/jekyll/) — Gemfile configuration, theme options (remote vs local gem), Docker-based setup, and troubleshooting.

---

## Phase 5: Site Configuration

The `_config.yml` file is the brain of your Jekyll site — site identity, theme skin, collections, plugins, comments, analytics, and more.

**Full guide:** [Site Configuration](/quickstart/site-configuration/) — every major configuration section with examples.

---

## Phase 6: VS Code & CMS Setup

VS Code is both your code editor and your CMS dashboard when paired with the Front Matter extension.

**Full guide:** [VS Code & CMS Setup](/quickstart/vscode-setup/) — extensions, Front Matter CMS, pre-configured tasks, and debug configurations.

---

## Phase 7: Theme Architecture

Understanding how layouts, includes, and Liquid templating work lets you customize anything.

**Full guide:** [Theme Architecture](/quickstart/theme-architecture/) — build pipeline, layouts, includes, Liquid patterns, and data files.

---

## Phase 8: Content Creation

Create blog posts, quests, documentation, and other content types with proper frontmatter and naming.

**Full guide:** [Content Creation](/quickstart/content-creation/) — frontmatter standards, naming conventions, and content types summary.

---

## Phases 9–10: Styling & Navigation

Style your site with skins and CSS, then configure navigation menus, sidebars, search, and comments.

**Full guide:** [Styling & Navigation](/quickstart/styling-navigation/) — skins, color overrides, custom CSS, nav config, Giscus comments.

---

## Phase 11: Local Development

Run your site locally with Docker, native Ruby, or VS Code tasks — with live reload and development config overrides.

**Full guide:** [Local Development](/quickstart/local-development/) — all three options with troubleshooting.

---

## Phase 12: Deployment

Deploy to GitHub Pages, Azure Static Web Apps, or any static host with custom domain configuration.

**Full guide:** [Deployment](/quickstart/deployment/) — GitHub Pages, Azure, manual build, custom domains.

---

## Phase 13: CI/CD & Automation

Set up GitHub Actions for automated building, testing, link checking, and deployment.

**Full guide:** [CI/CD & Automation](/quickstart/cicd-automation/) — all 7 active workflows, testing tools, automation scripts.

---

## Phases 14–15: Optimization & Maintenance

Optimize for SEO, performance, and accessibility — then keep your site healthy with dependency updates, content reviews, and scaling patterns.

**Full guide:** [Optimization & Maintenance](/quickstart/optimization-maintenance/) — checklists, maintenance routines, scaling patterns.

---

## Quick Reference

### Essential Commands

```bash
# Start development server (Docker)
docker-compose up -d

# Start development server (native)
bundle exec jekyll serve --config _config.yml,_config_dev.yml

# Build for production
JEKYLL_ENV=production bundle exec jekyll build

# Run link checker
python3 scripts/link-checker.py --scope website

# Validate quests
python3 test/quest-validator/quest_validator.py -d pages/_quests/

# Update dependencies
bundle update

# Clean build artifacts
bundle exec jekyll clean
```

### Key URLs

| Resource | URL |
|----------|-----|
| IT-Journey (Live) | [it-journey.dev](https://it-journey.dev) |
| GitHub Repository | [github.com/bamr87/it-journey](https://github.com/bamr87/it-journey) |
| zer0-mistakes Theme | [github.com/bamr87/zer0-mistakes](https://github.com/bamr87/zer0-mistakes) |
| Jekyll Documentation | [jekyllrb.com/docs](https://jekyllrb.com/docs/) |
| Liquid Reference | [shopify.github.io/liquid](https://shopify.github.io/liquid/) |
| kramdown Reference | [kramdown.gettalong.org](https://kramdown.gettalong.org/) |
| Front Matter CMS | [frontmatter.codes](https://frontmatter.codes/) |
| GitHub Pages Docs | [docs.github.com/en/pages](https://docs.github.com/en/pages) |
| GitHub Actions Docs | [docs.github.com/en/actions](https://docs.github.com/en/actions) |
| Docker Docs | [docs.docker.com](https://docs.docker.com/) |

### Quest Roadmap

The IT-Journey quest system uses binary level codes. Here's the full progression:

| Level | Tier | Focus Area | Example Quests |
|-------|------|-----------|----------------|
| `0000` | Foundation | OS setup, terminal, Git, Markdown, VS Code | [Begin Your IT Journey](/quests/init_world/begin-your-it-journey/), [Terminal Fundamentals](/quests/init_world/terminal-fundamentals/) |
| `0001` | Beginner | GitHub Pages, Jekyll, YAML, Liquid | [Jekyll Fundamentals](/quests/frontend/jekyll-fundamentals/), [YAML Configuration](/quests/frontend/yaml-configuration/) |
| `0010` | Intermediate | JavaScript, CSS, Bootstrap, Bash scripting | [JavaScript Fundamentals](/quests/intermediate/javascript-fundamentals/), [Bash Scripting](/quests/intermediate/bash-scripting/) |
| `0011` | Advanced | Git workflows, Jekyll plugins, SEO, analytics | [Advanced Git Workflows](/quests/advanced/advanced-git-workflows/), [SEO Optimization](/quests/advanced/seo-optimization/) |
| `0100` | Containers | Docker, Docker Compose, frontend containers | [Container Fundamentals](/quests/containers/container-fundamentals/), [Docker Compose](/quests/containers/docker-compose-orchestration/) |
| `0101` | CI/CD | GitHub Actions, deployment pipelines, secrets | [CI/CD Fundamentals](/quests/cicd/cicd-fundamentals/), [GitHub Actions Basics](/quests/cicd/github-actions-basics/) |
| `0110` | Databases | SQL, data modeling, migrations, security | [Database Fundamentals](/quests/databases/database-fundamentals/) |
| `1000` | Cloud | AWS, Azure, infrastructure as code | [Cloud Computing Fundamentals](/quests/cloud/cloud-computing-fundamentals/) |
| `1001` | Kubernetes | Pods, workloads, config, secrets | [Kubernetes Fundamentals](/quests/kubernetes/kubernetes-fundamentals/) |
| `1010` | Monitoring | Prometheus, Grafana, ELK, tracing | [Monitoring Fundamentals](/quests/monitoring/monitoring-fundamentals/) |
| `1100` | Data Eng. | Stream processing, data warehousing | [Stream Processing](/quests/data_engineering/stream-processing/) |
| `1101` | ML/AI | Python data science, deep learning, NLP | [Python Data Science](/quests/ai_ml/python-data-science/) |
| `1110` | Architecture | Microservices, design patterns, scaling | [Microservices Architecture](/quests/architecture/microservices-architecture/) |
| `1111` | Leadership | Technical leadership, mentorship, community | [Technical Leadership](/quests/mastery/technical-leadership/) |

---

## What's Next

You now have the complete blueprint for building and running a Jekyll site with the zer0-mistakes theme. The best way forward is to pick one phase, work through it, and keep going.

### Continue Your Journey

Now that you can build and deploy a Jekyll site, explore the rest of IT-Journey:

| Collection | What It Is | Start Here |
|------------|-----------|------------|
| [🏰 Quest Map](/quests/home/) | Gamified learning adventures across 16 binary levels (0000–1111) — from terminal basics to system architecture. Track XP, unlock tiers, and follow character-class paths. | [Hello n00b](/quests/init_world/hello-noob/) | 
| [📚 Docs Library](/docs/) | Reference documentation for the tools powering IT-Journey — terminal shortcuts, Bash reference, Jekyll configuration, Liquid templating, Mermaid diagrams, and MathJax. | [Terminal Shortcuts](/docs/terminal-shortcuts-cheat-sheet/) |
| [📝 Notes](/notes/) | Working notes, code snippets, and quick references collected during development — PowerShell, Linux, macOS tips, and more. | [Notes Index](/notes/) |
| [📰 Blog Posts](/posts/) | Tutorials, AI-assisted development chronicles, and technical write-ups organized across 10 categories — from web development to DevOps to data analytics. | [Posts Index](/posts/) |
| [🏠 Site Home](/home/) | The main IT-Journey hub with links to every section of the platform. | [Home](/home/) |

### Get Involved

- **Questions or ideas?** Start a thread in [IT-Journey Discussions](https://github.com/bamr87/it-journey/discussions)
- **Want to contribute?** Read the [Contributing Guide](/CONTRIBUTING/)
- **Found a bug?** Open an [issue on GitHub](https://github.com/bamr87/it-journey/issues/new)
