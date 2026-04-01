---
title: "Quick Start: Build a Jekyll Site from Scratch"
author: bamr87
description: End-to-end guide to establishing a development environment, implementing the zer0-mistakes Jekyll theme, and building a CMS-powered site like it-journey.dev — from first install to full deployment.
permalink: /quickstart/
sidebar:
   nav: quickstart
lastmod: 2026-04-01T04:21:56.599Z
date: 2021-12-05T18:52:20.000Z
---

This guide walks you through everything you need to build, configure, and maintain a Jekyll site like [it-journey.dev](https://it-journey.dev) — from installing your first tool to deploying a fully themed, CMS-powered site with CI/CD automation. We're using the [zer0-mistakes](https://github.com/bamr87/zer0-mistakes) theme, [VS Code](https://code.visualstudio.com/) as the editor, [Front Matter CMS](https://frontmatter.codes/) for content management, and [GitHub Pages](https://pages.github.com/) for free hosting.

Every section builds on the one before it. If you already have some tools installed, skip ahead. If something breaks, check the troubleshooting notes at the end of each section — and remember, debugging is half the job.

---

## Inside This Guide

| Phase | What You'll Do | Jump To |
|-------|---------------|---------|
| **1** | Install prerequisites (Ruby, Git, Docker, VS Code) | [Prerequisites & Machine Setup](#phase-1-prerequisites--machine-setup) |
| **2** | Understand how HTML, Markdown, and static sites work | [Web Fundamentals](#phase-2-web-fundamentals) |
| **3** | Create a GitHub repo and clone it locally | [Repository Setup](#phase-3-repository-setup) |
| **4** | Install Jekyll and the zer0-mistakes theme | [Jekyll & Theme Installation](#phase-4-jekyll--theme-installation) |
| **5** | Configure `_config.yml` — site identity, theme skin, collections | [Site Configuration](#phase-5-site-configuration) |
| **6** | Set up VS Code with extensions, tasks, and Front Matter CMS | [VS Code & CMS Setup](#phase-6-vs-code--cms-setup) |
| **7** | Understand layouts, includes, Liquid, and YAML data | [Theme Architecture](#phase-7-theme-architecture) |
| **8** | Create posts, quests, docs, and other content types | [Content Creation](#phase-8-content-creation) |
| **9** | Style your site — skins, colors, CSS, and responsive design | [Styling & Customization](#phase-9-styling--customization) |
| **10** | Add navigation, sidebars, search, and comments | [Navigation & Site Features](#phase-10-navigation--site-features) |
| **11** | Run your site locally with Docker or native Ruby | [Local Development](#phase-11-local-development) |
| **12** | Deploy to GitHub Pages, Azure, or other hosts | [Deployment](#phase-12-deployment) |
| **13** | Set up GitHub Actions for CI/CD, testing, and validation | [CI/CD & Automation](#phase-13-cicd--automation) |
| **14** | Optimize for SEO, performance, and accessibility | [SEO, Performance & Accessibility](#phase-14-seo-performance--accessibility) |
| **15** | Maintain, update, and scale your site over time | [Maintenance & Scaling](#phase-15-maintenance--scaling) |

---

## Phase 1: Prerequisites & Machine Setup

Before you write a single line of code, your machine needs the right tools. This phase gets your operating system ready for Jekyll development across **macOS, Windows, and Linux**.

### What You'll Install

| Tool | What It Does | Official Docs |
|------|-------------|---------------|
| **Git** | Version control — tracks every change to your code | [git-scm.com](https://git-scm.com/doc) |
| **Ruby 3.2+** | The programming language Jekyll runs on | [ruby-lang.org](https://www.ruby-lang.org/en/documentation/) |
| **Bundler** | Ruby's dependency manager (like npm for Ruby) | [bundler.io](https://bundler.io/) |
| **Node.js** | JavaScript runtime (used by some build tools) | [nodejs.org](https://nodejs.org/en/docs/) |
| **Docker Desktop** | Runs your site in an isolated container | [docs.docker.com](https://docs.docker.com/get-docker/) |
| **VS Code** | Your code editor and CMS interface | [code.visualstudio.com](https://code.visualstudio.com/docs) |

### Quick Setup by Platform

**macOS** (Homebrew):

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install everything
brew install git ruby node
gem install bundler
brew install --cask docker visual-studio-code
```

**Windows** (WSL2 recommended):

```bash
# Install WSL2 first (PowerShell as Admin)
wsl --install

# Inside WSL2 (Ubuntu)
sudo apt update && sudo apt install -y git ruby-full build-essential zlib1g-dev nodejs npm
gem install bundler
```

**Linux** (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install -y git ruby-full build-essential zlib1g-dev nodejs npm
gem install bundler
```

### Automated Setup (IT-Journey Script)

If you've already cloned this repository, there's a script that handles everything:

```bash
./scripts/core/environment-setup.sh
```

### Verify Your Installation

```bash
git --version        # 2.x+
ruby --version       # 3.2+
bundler --version    # 2.x+
node --version       # 18+
docker --version     # 24+
code --version       # Latest
```

> **IT-Journey Quests:** [Begin Your IT Journey](/quests/init_world/begin-your-it-journey/) · [Terminal Fundamentals](/quests/init_world/terminal-fundamentals/) · [VS Code Mastery](/quests/init_world/vscode-mastery/)
>
> **IT-Journey Docs:** [Development Environment](/docs/setup/DEVELOPMENT_ENVIRONMENT/) · [Machine Setup Guide](/quickstart/machine-setup)

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

Every Jekyll site lives in a Git repository. This phase creates yours.

### Option A: Fork IT-Journey (Recommended for Learning)

```bash
# Fork on GitHub first, then:
git clone https://github.com/YOUR-USERNAME/it-journey.git
cd it-journey
```

### Option B: Start Fresh with zer0-mistakes

```bash
# Create a new repo on GitHub, then:
mkdir my-site && cd my-site
git init
git remote add origin https://github.com/YOUR-USERNAME/my-site.git
```

### Option C: Use the zer0-mistakes Installer

```bash
curl -fsSL https://raw.githubusercontent.com/bamr87/zer0-mistakes/main/install.sh | bash
```

This installs the Gemfile, docker-compose.yml, starter `_config.yml`, and a GitHub Actions workflow in one command.

### Repository Structure

A fully configured Jekyll site using the zer0-mistakes theme looks like this:

```
my-site/
├── _config.yml              # Main Jekyll configuration
├── _config_dev.yml           # Development overrides
├── Gemfile                   # Ruby dependencies
├── docker-compose.yml        # Docker development environment
├── Dockerfile                # Container build definition
├── index.md                  # Homepage
├── 404.html                  # Custom error page
├── _data/                    # Site data files
│   ├── navigation/           # Menu configurations (YAML)
│   └── ui-text.yml           # UI string translations
├── _includes/                # Reusable HTML partials
├── _layouts/                 # Page templates
├── _plugins/                 # Custom Jekyll plugins
├── assets/                   # Static files
│   ├── css/                  # Stylesheets
│   ├── js/                   # JavaScript
│   └── images/               # Images and media
├── pages/                    # Content collections
│   ├── _posts/               # Blog posts (YYYY-MM-DD-slug.md)
│   ├── _quests/              # Gamified learning content
│   ├── _docs/                # Reference documentation
│   ├── _quickstart/          # Quick start guides
│   ├── _notebooks/           # Jupyter notebooks
│   ├── _notes/               # Draft notes
│   └── _about/               # About pages
├── scripts/                  # Automation scripts
├── test/                     # Testing tools
├── docs/                     # Developer documentation
└── .github/                  # GitHub config & CI/CD workflows
```

> **IT-Journey Quests:** [Git Basics](/quests/init_world/git-basics/) · [GitHub Pages Basics](/quests/frontend/github-pages-basics/)
>
> **IT-Journey Docs:** [Repository Structure](/docs/architecture/REPOSITORY_STRUCTURE/) · [GitHub Setup Guide](/quickstart/github)
>
> **External Docs:** [GitHub: Creating a Repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) · [Git Documentation](https://git-scm.com/doc)

---

## Phase 4: Jekyll & Theme Installation

### Install Dependencies

```bash
cd my-site

# Create Gemfile if you don't have one
cat > Gemfile << 'EOF'
source "https://rubygems.org"

gem 'github-pages'
gem 'jekyll-theme-zer0'
gem 'webrick'
EOF

# Install everything
bundle install
```

### Verify Jekyll Works

```bash
bundle exec jekyll serve
# Open http://localhost:4000 in your browser
```

### Theme Configuration

In your `_config.yml`, you reference the zer0-mistakes theme in one of two ways:

```yaml
# Option 1: Remote theme (for GitHub Pages deployment)
remote_theme: "bamr87/zer0-mistakes"

# Option 2: Local gem (for local/Docker development)
# theme: "jekyll-theme-zer0"
```

The development config (`_config_dev.yml`) can override this for local work:

```yaml
theme: "jekyll-theme-zer0"
```

Run with both configs:

```bash
bundle exec jekyll serve --config _config.yml,_config_dev.yml
```

> **External Docs:** [Jekyll Installation](https://jekyllrb.com/docs/installation/) · [Jekyll Themes](https://jekyllrb.com/docs/themes/) · [zer0-mistakes Theme](https://github.com/bamr87/zer0-mistakes)
>
> **IT-Journey Quests:** [Jekyll Fundamentals](/quests/frontend/jekyll-fundamentals/) · [YAML Configuration](/quests/frontend/yaml-configuration/)
>
> **IT-Journey Docs:** [Installation Update](/docs/setup/INSTALLATION_UPDATE/)

---

## Phase 5: Site Configuration

The `_config.yml` file is the brain of your Jekyll site. Here's every major section you can configure in the zer0-mistakes theme.

### Site Identity

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

### Theme Skin & Colors

The zer0-mistakes theme ships with 9 built-in skins:

```yaml
theme_skin: "dark"   # Options: air, aqua, contrast, dark, dirt, neon, mint, plum, sunrise
```

Override any color:

```yaml
theme_color:
  main: "#007bff"
  secondary: "#6c757d"
  red: "#a11111"
  yellow: "#ffe900"
  green: "#24b47e"
  blue: "#007bff"
  white: "#f9f9f9"
  gray: "#5a5a5a"
  black: "#111111"
```

### Collections

Collections define your content types. Each collection maps to a folder under `pages/`:

```yaml
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

### Collection Paths

Tell Jekyll where to find each collection:

```yaml
collections_dir: pages
```

### Default Frontmatter

Set automatic frontmatter values by collection so you don't repeat yourself:

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
      layout: articles
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
```

### Markdown Processing

```yaml
markdown: kramdown
kramdown:
  input: GFM           # GitHub Flavored Markdown
  header_offset: 0
  toc_levels: 1..6
  syntax_highlighter: rouge
```

### Plugins

```yaml
plugins:
  - github-pages
  - jekyll-remote-theme
  - jekyll-feed          # RSS feed generation
  - jekyll-sitemap       # Automatic sitemap.xml
  - jekyll-seo-tag       # SEO meta tags
  - jekyll-paginate      # Blog pagination
  - jekyll-relative-links

paginate: 10
paginate_path: "/pages/:num/"
```

### Comments (Giscus)

```yaml
giscus:
  enabled: true
  data-repo: "bamr87/it-journey"
  data-repo-id: "your-repo-id"
  data-category-id: "your-category-id"
  data-mapping: "pathname"
  data-theme: "preferred_color_scheme"
```

### Analytics

```yaml
analytics:
  provider: "google-gtag"
  google:
    tracking_id: "G-XXXXXXXXXX"
```

> **External Docs:** [Jekyll Configuration Options](https://jekyllrb.com/docs/configuration/options/) · [Jekyll Collections](https://jekyllrb.com/docs/collections/) · [Jekyll Frontmatter Defaults](https://jekyllrb.com/docs/configuration/front-matter-defaults/) · [kramdown Options](https://kramdown.gettalong.org/options.html) · [Giscus Setup](https://giscus.app/)
>
> **IT-Journey Quests:** [YAML Configuration](/quests/frontend/yaml-configuration/) · [Jekyll Plugins](/quests/advanced/jekyll-plugins/) · [SEO Optimization](/quests/advanced/seo-optimization/) · [Analytics Integration](/quests/advanced/analytics-integration/)
>
> **IT-Journey Docs:** [Frontmatter Standards](/docs/standards/FRONTMATTER_STANDARDS/) · [Content Guidelines](/docs/standards/CONTENT_GUIDELINES/)

---

## Phase 6: VS Code & CMS Setup

VS Code is both your code editor and your CMS dashboard when paired with the Front Matter extension.

### Recommended Extensions

Install these extensions (also listed in `.vscode/extensions.json`):

| Extension | What It Does | Extension ID |
|-----------|-------------|-------------|
| **GitHub Copilot** | AI code completion | `github.copilot` |
| **GitHub Copilot Chat** | AI chat in the editor | `github.copilot-chat` |
| **Front Matter CMS** | Headless CMS dashboard | `eliostruyf.vscode-front-matter` |
| **Docker** | Container management | `ms-azuretools.vscode-docker` |
| **Ruby LSP** | Ruby language support | `shopify.ruby-lsp` |
| **Liquid** | Liquid template support | `shopify.liquid` |
| **YAML** | YAML validation | `redhat.vscode-yaml` |
| **Markdown All in One** | Markdown tools | `yzhang.markdown-all-in-one` |
| **markdownlint** | Markdown linting | `davidanson.vscode-markdownlint` |
| **GitLens** | Git history and blame | `eamodio.gitlens` |
| **Spell Checker** | Catch typos | `streetsidesoftware.code-spell-checker` |
| **Jupyter** | Notebook support | `ms-toolsai.jupyter` |

Install all at once:

```bash
code --install-extension github.copilot \
     --install-extension github.copilot-chat \
     --install-extension eliostruyf.vscode-front-matter \
     --install-extension ms-azuretools.vscode-docker \
     --install-extension shopify.ruby-lsp \
     --install-extension shopify.liquid \
     --install-extension redhat.vscode-yaml \
     --install-extension yzhang.markdown-all-in-one \
     --install-extension davidanson.vscode-markdownlint \
     --install-extension eamodio.gitlens \
     --install-extension streetsidesoftware.code-spell-checker
```

### Front Matter CMS Configuration

The `frontmatter.json` file at the repo root configures Front Matter CMS. It defines:

- **Page folders** — where each content collection lives
- **Content types** — field schemas for posts, quests, and other types
- **Snippets** — reusable content templates
- **Preview paths** — live preview URLs for content

**Key content types configured:**

| Content Type | Fields | Used By |
|-------------|--------|---------|
| **default** | title, description, date, draft, tags, categories, layout, author, permalink, image | Posts, pages, docs, notes |
| **quest** | All default fields + level (binary), difficulty, estimated_time, xp, achievements, prerequisites, platforms, quest_type, skill_focus, learning_style | Quests |

The dashboard auto-opens when you open the project (`frontMatter.dashboard.openOnStart: true`), giving you a visual interface for creating, editing, and managing all your content without touching frontmatter YAML by hand.

### VS Code Tasks (Pre-Configured)

The project includes `.vscode/tasks.json` with built-in tasks accessible via `Ctrl+Shift+B` (or `Cmd+Shift+B` on macOS):

| Task | Command | Purpose |
|------|---------|---------|
| Docker: Compose Up | `docker-compose up -d` | Start dev environment |
| Docker: Compose Down | `docker-compose down` | Stop and clean up |
| Docker: Rebuild (Force) | `docker-compose up --build --force-recreate -d` | Full rebuild |
| Docker: Logs (Follow) | `docker-compose logs -f jekyll` | Watch build output |
| Jekyll: Build Site | `bundle exec jekyll build` (in Docker) | Production build |
| Lint: Markdown Files | `markdownlint **/*.md` | Check markdown quality |

### Debug Configurations

Launch configurations in `.vscode/launch.json` include:

- **Debug IT-Journey (Docker)** — launches browser with remote debugging
- **Attach to Running Jekyll** — connects to already-running container
- **Docker Rebuild & Debug** — force rebuilds then debugs
- **Mobile Debug** — simulates iPhone screen for responsive testing

> **External Docs:** [VS Code Docs](https://code.visualstudio.com/docs) · [Front Matter CMS Docs](https://frontmatter.codes/docs) · [Liquid Language Reference](https://shopify.github.io/liquid/)
>
> **IT-Journey Quests:** [VS Code Mastery](/quests/init_world/vscode-mastery/) · [Prompt Crystal: VS Code Copilot Mastery](/quests/advanced/prompt-crystal-mastery-vscode-copilot/)

---

## Phase 7: Theme Architecture

Understanding how the zer0-mistakes theme assembles pages helps you customize anything.

### How Jekyll Builds a Page

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

### Layouts

Layouts are HTML templates that wrap your content. The zer0-mistakes theme provides:

| Layout | Purpose | Used By |
|--------|---------|---------|
| `root` | Base HTML shell (head, body, scripts) | Everything |
| `default` | Standard page with header/footer/sidebar | General pages |
| `articles` | Blog post layout with date, author, tags | Posts |
| `quest` | Quest layout with level, XP, achievements | Quests |
| `quest-collection` | Groups quests by tier in a grid | Quest index pages |
| `journals` | Journal/notebook layout | Notebooks |
| `javascript` | Layout for JS-heavy interactive pages | Special pages |

Set the layout in your file's frontmatter:

```yaml
---
layout: articles
title: "My Blog Post"
---
```

### Includes (Partials)

Includes are reusable HTML snippets injected into layouts with `{% raw %}{% include component.html %}{% endraw %}`. Key includes in IT-Journey:

```
_includes/
├── components/
│   └── powered-by.html          # Footer attribution
├── contributor/
│   ├── profile_card.html        # Contributor profile
│   ├── character_sheet.html     # RPG-style stats
│   ├── achievement_wall.html    # Badge display
│   └── stats_panel.html         # Activity statistics
├── quest-card.html              # Quest display card
├── quest-filters.html           # Quest filtering controls
└── quest-stats.html             # Quest completion statistics
```

### Liquid Templating

Jekyll uses the [Liquid](https://shopify.github.io/liquid/) templating language. Common patterns:

```liquid
{% raw %}
<!-- Variable output -->
{{ page.title }}
{{ site.title }}

<!-- Conditionals -->
{% if page.comments %}
  {% include comments.html %}
{% endif %}

<!-- Loops -->
{% for post in site.posts limit:5 %}
  <h2>{{ post.title }}</h2>
{% endfor %}

<!-- Filters -->
{{ page.date | date: "%B %d, %Y" }}
{{ page.content | number_of_words }} words
{% endraw %}
```

### Data Files

YAML files in `_data/` are accessible as `site.data.*` in templates:

| File | Contains | Access As |
|------|----------|-----------|
| `_data/navigation/main.yml` | Primary site menu | `site.data.navigation.main` |
| `_data/navigation/quests.yml` | Quest sidebar menu | `site.data.navigation.quests` |
| `_data/navigation/posts.yml` | Posts sidebar menu | `site.data.navigation.posts` |
| `_data/navigation/quickstart.yml` | Quickstart sidebar | `site.data.navigation.quickstart` |
| `_data/ui-text.yml` | UI strings (i18n-ready) | `site.data.ui-text` |
| `_data/prerequisites.yml` | Learning prerequisites | `site.data.prerequisites` |

> **External Docs:** [Jekyll Layouts](https://jekyllrb.com/docs/layouts/) · [Jekyll Includes](https://jekyllrb.com/docs/includes/) · [Liquid Reference](https://shopify.github.io/liquid/) · [Jekyll Data Files](https://jekyllrb.com/docs/datafiles/)
>
> **IT-Journey Quests:** [Liquid Templating](/quests/frontend/liquid-templating/) · [Jekyll Fundamentals](/quests/frontend/jekyll-fundamentals/)

---

## Phase 8: Content Creation

### Frontmatter — The Metadata That Powers Everything

Every content file starts with YAML frontmatter between `---` fences. The fields control how the page is rendered, categorized, and discovered.

**Minimum required frontmatter (all content types):**

```yaml
---
title: "Your Page Title"
---
```

**Blog post frontmatter:**

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

**Quest frontmatter:**

```yaml
---
title: "Docker Container Fundamentals"
layout: quest
description: "Master Docker container images, volumes, and networking."
level: "0100"              # Binary format: 0000-1111
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

### Creating a Blog Post

Posts live in `pages/_posts/` and follow the naming convention: `YYYY-MM-DD-slug-title.md`

```bash
# Create a new post
touch pages/_posts/2026-03-31-my-first-post.md
```

Or use Front Matter CMS: click **Create content** in the dashboard, select the "posts" folder, and fill in the fields visually.

### Creating a Quest

Quests live in `pages/_quests/` organized by level directory:

```
pages/_quests/
├── 0000/    # Level 0000 — Foundation
├── 0001/    # Level 0001 — Beginner
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

### Creating Documentation

Docs live in `pages/_docs/` and use the `default` layout:

```yaml
---
title: "API Reference"
layout: default
categories:
  - reference
---
```

### Content Types Summary

| Collection | Folder | Layout | Naming Convention | Permalink Pattern |
|-----------|--------|--------|-------------------|-------------------|
| Posts | `pages/_posts/` | `articles` | `YYYY-MM-DD-slug.md` | `/posts/YYYY/MM/DD/slug/` |
| Quests | `pages/_quests/` | `quest` | `quest-name.md` in level folder | `/quests/category/name/` |
| Docs | `pages/_docs/` | `default` | `descriptive-name.md` | `/docs/category/name/` |
| Quickstart | `pages/_quickstart/` | `default` | `descriptive-name.md` | `/quickstart/name/` |
| Notebooks | `pages/_notebooks/` | `journals` | `name.md` or converted `.ipynb` | `/notebooks/path/name/` |
| Notes | `pages/_notes/` | `default` | `descriptive-name.md` | `/notes/path/name/` |
| About | `pages/_about/` | `default` | `descriptive-name.md` | `/about/category/name/` |

> **IT-Journey Docs:** [Frontmatter Standards](/docs/standards/FRONTMATTER_STANDARDS/) · [Content Guidelines](/docs/standards/CONTENT_GUIDELINES/)
>
> **IT-Journey Quests:** [Markdown Mastery](/quests/init_world/markdown-mastery/) · [Forge Your Character](/quests/frontend/forge-your-character/)

---

## Phase 9: Styling & Customization

### Theme Skins

Change the entire look with one line in `_config.yml`:

```yaml
theme_skin: "dark"
```

Available skins: `air`, `aqua`, `contrast`, `dark`, `dirt`, `neon`, `mint`, `plum`, `sunrise`

### Custom CSS

Add your own styles in `assets/css/`. Any SCSS/CSS file in that directory is compiled and loaded by the theme.

### Color Overrides

Override any theme color in `_config.yml`:

```yaml
theme_color:
  main: "#007bff"       # Primary brand color
  secondary: "#6c757d"  # Secondary elements
  bg: "#111111"         # Background
  text: "#f9f9f9"       # Text color
  link: "#007bff"       # Link color
  link_hover: "#0056b3" # Link hover state
```

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

> **External Docs:** [Jekyll Assets](https://jekyllrb.com/docs/assets/) · [Bootstrap Docs](https://getbootstrap.com/docs/)
>
> **IT-Journey Quests:** [CSS Styling Basics](/quests/intermediate/css-styling-basics/) · [Bootstrap Framework](/quests/intermediate/bootstrap-framework/)

---

## Phase 10: Navigation & Site Features

### Navigation Configuration

Navigation menus are defined in `_data/navigation/` as YAML files:

**Main navigation** (`_data/navigation/main.yml`):

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

**Quest sidebar** (`_data/navigation/quests.yml`) is organized by tier — Foundation, Beginner, Intermediate, etc.

### Sidebar Configuration

Set the sidebar per page or per collection in frontmatter:

```yaml
sidebar:
  nav: quests    # References _data/navigation/quests.yml
```

Or globally in defaults:

```yaml
defaults:
  - scope:
      path: pages/_quests
      type: quests
    values:
      sidebar:
        nav: quests
```

### Search

Jekyll can integrate with search solutions. Common options:

- **Lunr.js** — client-side search (no server needed)
- **Algolia** — hosted search API
- **Custom search page** — using a JSON index generated by Jekyll

### Comments (Giscus)

Giscus uses GitHub Discussions as a comments backend. Enable per-page:

```yaml
comments: true
```

Configure globally in `_config.yml` (see [Phase 5](#phase-5-site-configuration)).

> **External Docs:** [Jekyll Navigation](https://jekyllrb.com/tutorials/navigation/) · [Giscus](https://giscus.app/)
>
> **IT-Journey Quests:** [GitHub Pages Hidden Gem](/quests/advanced/github-pages-hidden-gem/) · [Custom Domains](/quests/advanced/custom-domains/)

---

## Phase 11: Local Development

### Option A: Docker (Recommended)

Docker gives you a consistent, isolated environment that matches production:

```bash
# Start the development server
docker-compose up -d

# View at http://localhost:4002

# Watch logs in real-time
docker-compose logs -f jekyll

# Stop the server
docker-compose stop

# Full cleanup
docker-compose down
```

The `docker-compose.yml` mounts your project directory into the container, so edits are reflected immediately with live reload.

### Option B: Native Ruby

```bash
# Install dependencies
bundle install

# Serve with development config
bundle exec jekyll serve --config _config.yml,_config_dev.yml

# View at http://localhost:4002

# Build without serving (for production)
bundle exec jekyll build
```

### Option C: VS Code Tasks

Use the pre-configured tasks (`Cmd+Shift+B`):
1. Run **Docker: Compose Up (Detached)** to start
2. Run **Docker: Logs (Follow)** to watch output
3. Open `http://localhost:4002` in your browser

### Live Reload

Changes to Markdown content and data files trigger an automatic rebuild. Changes to `_config.yml` require a server restart.

### Development vs Production Config

| Setting | Development (`_config_dev.yml`) | Production (`_config.yml`) |
|---------|--------------------------------|---------------------------|
| Theme | `theme: "jekyll-theme-zer0"` (local gem) | `remote_theme: "bamr87/zer0-mistakes"` |
| URL | `http://localhost:4002` | `https://it-journey.dev` |
| Drafts | Shown | Hidden |
| Minification | Off | On |

> **IT-Journey Docs:** [Development Environment](/docs/setup/DEVELOPMENT_ENVIRONMENT/)
>
> **IT-Journey Quests:** [Container Fundamentals](/quests/containers/container-fundamentals/) · [Docker Compose Orchestration](/quests/containers/docker-compose-orchestration/)
>
> **External Docs:** [Docker Compose](https://docs.docker.com/compose/) · [Jekyll Serve Command](https://jekyllrb.com/docs/usage/)

---

## Phase 12: Deployment

### GitHub Pages (Free — Recommended for Starters)

1. Push your repo to GitHub
2. Go to **Settings → Pages**
3. Set source to **GitHub Actions** (or the `gh-pages` branch)
4. Your site will be live at `https://username.github.io/repo-name/`

For a custom domain:

```yaml
# In _config.yml
url: "https://yourdomain.com"
```

Create a `CNAME` file at the repo root:

```
yourdomain.com
```

Configure DNS records with your domain registrar (A records or CNAME).

### Azure Static Web Apps

Use the IT-Journey deployment script:

```bash
./scripts/azure-jekyll-deploy.sh deploy \
  --app-name my-jekyll-site \
  --github-repo https://github.com/username/repo
```

Configuration for Azure:
- **App location:** `/`
- **API location:** `api/`
- **Output location:** `_site/`

### Manual Build + Any Host

```bash
# Build the production site
JEKYLL_ENV=production bundle exec jekyll build

# The _site/ folder contains all static files
# Upload _site/ contents to any static hosting provider
```

Works with: Netlify, Vercel, Cloudflare Pages, AWS S3 + CloudFront, or any web server.

> **External Docs:** [GitHub Pages Docs](https://docs.github.com/en/pages) · [Azure Static Web Apps](https://learn.microsoft.com/en-us/azure/static-web-apps/) · [Jekyll Deployment](https://jekyllrb.com/docs/deployment/)
>
> **IT-Journey Quests:** [GitHub Pages Basics](/quests/frontend/github-pages-basics/) · [Azure Ascension](/quests/azure-ascension-jekyll-deployment-quest/) · [CI/CD Fundamentals](/quests/cicd/cicd-fundamentals/)

---

## Phase 13: CI/CD & Automation

IT-Journey uses GitHub Actions for automated building, testing, and deployment.

### Active Workflows

| Workflow | Trigger | What It Does |
|----------|---------|-------------|
| **Build Validation** | Push, PR | Builds the Jekyll site and catches errors |
| **Link Health Guardian** | Schedule (Mon/Fri), Manual | Scans for broken links with optional AI analysis |
| **Frontmatter Validation** | PR, Manual | Validates YAML metadata with auto-fix |
| **AI Content Review** | PR, Push | GPT-4 quality analysis |
| **Organize Posts** | Weekly schedule | Auto-categorizes posts into folders |
| **CodeQL Analysis** | Schedule, Push | Security vulnerability scanning |
| **Dependency Checker** | Schedule | Alerts on outdated dependencies |

### Setting Up GitHub Actions

Workflow files live in `.github/workflows/`. A basic Jekyll build workflow:

```yaml
name: Build and Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
      - run: bundle exec jekyll build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: _site/

  deploy:
    needs: build
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4
```

### Testing Tools

| Tool | Command | What It Checks |
|------|---------|---------------|
| **Link Checker** | `python3 scripts/link-checker.py --scope website` | Broken internal/external links |
| **Quest Validator** | `python3 test/quest-validator/quest_validator.py -d pages/_quests/` | Quest frontmatter and content structure |
| **Markdown Lint** | `markdownlint **/*.md` | Markdown style and formatting |

### Automation Scripts

```bash
# Environment setup
./scripts/core/environment-setup.sh

# Version management
./scripts/core/version-manager.sh patch   # 1.0.0 → 1.0.1
./scripts/core/version-manager.sh minor   # 1.0.0 → 1.1.0
./scripts/core/version-manager.sh major   # 1.0.0 → 2.0.0

# Build for production
./scripts/development/build/build-site.sh --production

# Convert Jupyter notebooks to Markdown
./scripts/development/content/jupyter-to-markdown.sh pages/_notebooks/

# Organize posts by category
python3 scripts/development/content/organize-posts.py --dry-run
```

> **IT-Journey Docs:** [GitHub Actions Workflows](/docs/workflows/GITHUB_ACTIONS/) · [Testing Frameworks](/docs/testing/TESTING_FRAMEWORKS/) · [Scripts Guide](/docs/scripts/SCRIPTS_GUIDE/)
>
> **IT-Journey Quests:** [CI/CD Fundamentals](/quests/cicd/cicd-fundamentals/) · [GitHub Actions Basics](/quests/cicd/github-actions-basics/) · [Bash Scripting](/quests/intermediate/bash-scripting/)
>
> **External Docs:** [GitHub Actions](https://docs.github.com/en/actions) · [markdownlint Rules](https://github.com/DavidAnson/markdownlint)

---

## Phase 14: SEO, Performance & Accessibility

### SEO Configuration

The `jekyll-seo-tag` plugin automatically generates meta tags from your `_config.yml` and page frontmatter:

```yaml
# _config.yml
title: "IT-Journey"
description: "Democratizing IT education"
url: "https://it-journey.dev"
og_image: "/assets/images/wizard-on-journey.png"

# Per-page frontmatter
---
title: "Page Title"
description: "Page-specific description for search engines."
image: /assets/images/page-cover.jpg
---
```

The `jekyll-sitemap` plugin generates `sitemap.xml` automatically. The `jekyll-feed` plugin generates an RSS feed at `/feed.xml`.

### Performance Checklist

- [ ] Optimize images before committing (max width 1200px)
- [ ] Use the `loading="lazy"` attribute on images below the fold
- [ ] Minimize custom JavaScript
- [ ] Enable CSS/JS minification in production (`JEKYLL_ENV=production`)
- [ ] Use CDN for static assets when self-hosting
- [ ] Check with [Lighthouse](https://developer.chrome.com/docs/lighthouse/)

### Accessibility Checklist

- [ ] All images have descriptive `alt` text
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] All interactive elements are keyboard-navigable
- [ ] Heading hierarchy is logical (h1 → h2 → h3, no skips)
- [ ] Links have descriptive text (not "click here")
- [ ] Language attribute set: `<html lang="en">`

> **IT-Journey Quests:** [SEO Optimization](/quests/advanced/seo-optimization/) · [Analytics Integration](/quests/advanced/analytics-integration/)
>
> **External Docs:** [Jekyll SEO Tag](https://github.com/jekyll/jekyll-seo-tag) · [WCAG Guidelines](https://www.w3.org/WAI/standards-guidelines/wcag/) · [Google Lighthouse](https://developer.chrome.com/docs/lighthouse/)

---

## Phase 15: Maintenance & Scaling

### Keeping Dependencies Updated

```bash
# Update Ruby gems
bundle update

# Check for outdated gems
bundle outdated

# Update Docker images
docker-compose pull
docker-compose up --build -d
```

The Dependency Checker workflow also alerts you automatically.

### Content Maintenance

| Task | Frequency | Tool/Command |
|------|-----------|-------------|
| Fix broken links | Weekly (automated) | Link Health Guardian workflow |
| Validate quest frontmatter | On PR (automated) | Frontmatter Validation workflow |
| Organize posts by category | Weekly (automated) | Organize Posts workflow |
| Update content statistics | As needed | `make stats-update` |
| Review draft content | Monthly | Front Matter CMS dashboard |

### Scaling Your Content

As your site grows, these patterns help:

- **Collections** — Add new content types by defining them in `_config.yml`
- **Navigation files** — Update `_data/navigation/` when adding new sections
- **Data files** — Use `_data/` for structured content that multiple pages reference
- **Includes** — Extract repeated HTML into `_includes/` partials
- **Plugins** — Extend Jekyll with custom Ruby plugins in `_plugins/`

### Version Management

Use the version manager script to bump semantic versions across the project:

```bash
./scripts/core/version-manager.sh patch   # Bug fixes
./scripts/core/version-manager.sh minor   # New features
./scripts/core/version-manager.sh major   # Breaking changes
```

> **IT-Journey Docs:** [Scripts Guide](/docs/scripts/SCRIPTS_GUIDE/) · [GitHub Actions](/docs/workflows/GITHUB_ACTIONS/)

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

You now have the complete blueprint for building and running a Jekyll site with the zer0-mistakes theme. The best way forward is to pick one phase, work through it, and keep going. If you get stuck, check the linked quests and docs — they go deeper into every topic covered here.

For questions or contributions, visit the [IT-Journey Discussions](https://github.com/bamr87/it-journey/discussions) or check the [Contributing Guide](/CONTRIBUTING/).
