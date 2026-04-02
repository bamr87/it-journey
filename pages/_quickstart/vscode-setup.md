---
title: VS Code & CMS Setup
author: bamr87
description: Set up Visual Studio Code with recommended extensions, Front Matter CMS, pre-configured tasks, and debug configurations for Jekyll development.
permalink: /quickstart/vscode-setup/
categories:
  - quickstart
slug: vscode-setup
lastmod: 2026-04-02T03:14:50.912Z
draft: false
date: 2026-04-01T00:00:00.000Z
difficulty: 🟢 Easy
estimatedTime: 15-20 minutes
prerequisites:
  - VS Code installed (see [Machine Setup](/quickstart/machine-setup/))
  - IT-Journey repository cloned (see [GitHub Setup](/quickstart/github/))
tags:
  - vscode
  - front-matter-cms
  - extensions
  - ide
keywords:
  primary:
    - vscode setup
    - front matter cms
    - jekyll editor
  secondary:
    - extensions
    - tasks
    - debug configuration
sidebar:
  nav: quickstart
---

This guide covers **Phase 6** of the [Quick Start](/quickstart/) — turning VS Code into a full Jekyll development and content management environment with Front Matter CMS.

---

## Recommended Extensions

Install these extensions for the best Jekyll development experience. They're also listed in the repo's `.vscode/extensions.json`:

| Extension | What It Does | Extension ID |
|-----------|-------------|-------------|
| **GitHub Copilot** | AI code completion | `github.copilot` |
| **GitHub Copilot Chat** | AI chat in editor | `github.copilot-chat` |
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

### Install All at Once

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

---

## Front Matter CMS Configuration

[Front Matter CMS](https://frontmatter.codes/) turns VS Code into a headless CMS with a visual dashboard for managing content.

### What It Provides

- **Dashboard** — visual overview of all content (posts, quests, docs)
- **Content types** — field schemas with validation
- **Snippets** — reusable content templates
- **Preview** — live preview URLs for content
- **Media management** — manage images and assets

### Configuration File

The `frontmatter.json` file at the repo root configures everything. It defines:

- **Page folders** — where each content collection lives
- **Content types** — field schemas for posts, quests, and other types
- **Snippets** — reusable content templates
- **Preview paths** — live preview URLs for content

### Key Content Types

| Content Type | Fields | Used By |
|-------------|--------|---------|
| **default** | title, description, date, draft, tags, categories, layout, author, permalink, image | Posts, pages, docs, notes |
| **quest** | All default fields + level (binary), difficulty, estimated_time, xp, achievements, prerequisites, platforms, quest_type, skill_focus, learning_style | Quests |

### Using the Dashboard

The dashboard auto-opens when you open the project (`frontMatter.dashboard.openOnStart: true`), giving you a visual interface for creating, editing, and managing all your content without touching frontmatter YAML by hand.

To open manually: **Ctrl+Shift+P** → **Front Matter: Open Dashboard**

### Creating Content via CMS

1. Open the Front Matter dashboard
2. Click **Create content**
3. Select the target folder (posts, quests, docs, etc.)
4. Fill in the fields visually
5. The CMS generates a properly formatted Markdown file with correct frontmatter

---

## Pre-Configured VS Code Tasks

The project includes `.vscode/tasks.json` with built-in tasks accessible via **Ctrl+Shift+B** (or **Cmd+Shift+B** on macOS):

| Task | Command | Purpose |
|------|---------|---------|
| **Docker: Compose Up** | `docker-compose up -d` | Start dev environment |
| **Docker: Compose Down** | `docker-compose down` | Stop and clean up |
| **Docker: Rebuild (Force)** | `docker-compose up --build --force-recreate -d` | Full rebuild |
| **Docker: Logs (Follow)** | `docker-compose logs -f jekyll` | Watch build output |
| **Jekyll: Build Site** | `bundle exec jekyll build` (in Docker) | Production build |
| **Lint: Markdown Files** | `markdownlint **/*.md` | Check markdown quality |
| **Docker: Clean Up** | `docker system prune -f` | Clean up Docker system |
| **Dependencies: Update Jekyll** | `bundle update` (in Docker) | Update Jekyll dependencies |

### Running Tasks

1. Press **Ctrl+Shift+B** (or **Cmd+Shift+B**)
2. Select the task from the list
3. Output appears in the integrated terminal

Or use the Command Palette: **Ctrl+Shift+P** → **Tasks: Run Task**

---

## Debug Configurations

Launch configurations in `.vscode/launch.json` include:

| Configuration | What It Does |
|--------------|-------------|
| **Debug IT-Journey (Docker)** | Launches browser with remote debugging |
| **Attach to Running Jekyll** | Connects to already-running container |
| **Docker Rebuild & Debug** | Force rebuilds then debugs |
| **Mobile Debug** | Simulates iPhone screen for responsive testing |

Start debugging: **F5** or **Run → Start Debugging**, then select the configuration.

---

## Workspace Settings

Useful workspace settings for Jekyll development in `.vscode/settings.json`:

```json
{
  "files.associations": {
    "*.html": "liquid",
    "*.md": "markdown"
  },
  "editor.wordWrap": "on",
  "editor.minimap.enabled": false,
  "markdown.validate.enabled": true
}
```

---

## What's Next

| Next Step | Guide |
|-----------|-------|
| Understand layouts, includes, and Liquid templating | [Theme Architecture](/quickstart/theme-architecture/) |
| Create posts, quests, and docs | [Content Creation](/quickstart/content-creation/) |
| Run the site locally with Docker | [Local Development](/quickstart/local-development/) |

> **IT-Journey Quests:** [VS Code Mastery](/quests/init_world/vscode-mastery/) · [Prompt Crystal: VS Code Copilot Mastery](/quests/advanced/prompt-crystal-mastery-vscode-copilot/)
>
> **External Docs:** [VS Code Docs](https://code.visualstudio.com/docs) · [Front Matter CMS Docs](https://frontmatter.codes/docs) · [Liquid Language Reference](https://shopify.github.io/liquid/)
