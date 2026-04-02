---
title: "Local Development with Docker and Ruby"
author: bamr87
description: Run your Jekyll site locally with Docker, native Ruby, or VS Code tasks — with live reload, development config overrides, and debugging.
excerpt: "Run your Jekyll site locally using Docker, native Ruby, or VS Code tasks — with live reload, config overrides, and debugging support."
permalink: /quickstart/local-development/
categories:
  - quickstart
slug: local-development
lastmod: 2026-04-02T03:14:50.948Z
draft: false
date: 2026-04-01T00:00:00.000Z
difficulty: 🟢 Easy
estimatedTime: 15-20 minutes
prerequisites:
  - Jekyll installed (see [Jekyll Setup](/quickstart/jekyll/))
  - Docker installed (see [Machine Setup](/quickstart/machine-setup/))
tags:
  - docker
  - development
  - local
  - livereload
keywords:
  primary:
    - local development
    - docker compose
    - jekyll serve
  secondary:
    - livereload
    - development config
    - debugging
sidebar:
  nav: quickstart
---

This guide covers **Phase 11** of the [Quick Start](/quickstart/) — running your Jekyll site locally with Docker, native Ruby, or VS Code tasks.

---

## Option A: Docker (Recommended)

Docker gives you a consistent, isolated environment that matches production. No need to install Ruby or manage gem versions directly on your machine.

```bash
# Start the development server
docker-compose up -d

# View at http://localhost:4002

# Watch logs in real-time
docker-compose logs -f jekyll

# Stop the server
docker-compose stop

# Full cleanup (removes containers and networks)
docker-compose down
```

The `docker-compose.yml` mounts your project directory into the container, so edits to Markdown, data files, and templates are reflected immediately with live reload.

### What `docker-compose.yml` Does

The project's Docker Compose configuration:

- Builds a Ruby container with Jekyll and all gem dependencies
- Mounts the project directory so source changes reflect instantly
- Exposes the site on port `4002`
- Uses `_config.yml` and `_config_dev.yml` together for development overrides
- Enables livereload for automatic browser refresh

---

## Option B: Native Ruby

If you prefer running Jekyll directly on your machine:

```bash
# Install dependencies (first time, or after Gemfile changes)
bundle install

# Serve with both production and development configs
bundle exec jekyll serve --config _config.yml,_config_dev.yml

# View at http://localhost:4002

# Build without serving (for production testing)
bundle exec jekyll build
```

### Useful Flags

| Flag | Purpose |
|------|---------|
| `--livereload` | Auto-refresh browser on changes |
| `--drafts` | Include draft posts |
| `--incremental` | Faster rebuilds (only changed files) |
| `--verbose` | Detailed build output for debugging |
| `--trace` | Full stack traces on errors |

Example with all flags:

```bash
bundle exec jekyll serve --config _config.yml,_config_dev.yml --livereload --drafts --incremental
```

---

## Option C: VS Code Tasks

Use the pre-configured tasks (press **Cmd+Shift+B** on macOS or **Ctrl+Shift+B**):

1. Run **Docker: Compose Up (Detached)** to start the server
2. Run **Docker: Logs (Follow)** to watch build output
3. Open `http://localhost:4002` in your browser
4. Run **Docker: Compose Down** when done

All tasks are defined in `.vscode/tasks.json`.

---

## Live Reload

Livereload watches for file changes and triggers automatic rebuilds:

| What Changed | Rebuild Needed? | Browser Refresh? |
|-------------|-----------------|------------------|
| Markdown content | Automatic | Automatic |
| Data files (`_data/`) | Automatic | Automatic |
| Includes (`_includes/`) | Automatic | Automatic |
| Layouts (`_layouts/`) | Automatic | Automatic |
| CSS/SCSS | Automatic | Automatic |
| `_config.yml` | **Manual restart required** | Manual |
| `Gemfile` | **`bundle install` + restart** | Manual |

---

## Development vs Production Config

| Setting | Development (`_config_dev.yml`) | Production (`_config.yml`) |
|---------|--------------------------------|---------------------------|
| Theme | `theme: "jekyll-theme-zer0"` (local gem) | `remote_theme: "bamr87/zer0-mistakes"` |
| URL | `http://localhost:4002` | `https://it-journey.dev` |
| Drafts | Shown | Hidden |
| Minification | Off | On |

When using Docker Compose, both configs are loaded automatically. When using native Ruby, pass both with `--config`:

```bash
bundle exec jekyll serve --config _config.yml,_config_dev.yml
```

The second config file overrides values from the first.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 4002 already in use | `docker-compose down` then retry, or use `--port 4003` |
| Gem dependency errors | `bundle install` or rebuild Docker: `docker-compose up --build` |
| Changes not showing | For `_config.yml` changes, restart the server |
| Build fails on `remote_theme` | Use `_config_dev.yml` override with `theme:` for local dev |
| Slow incremental builds | Try `bundle exec jekyll clean` to clear cache, then rebuild |

---

## What's Next

| Next Step | Guide |
|-----------|-------|
| Deploy to GitHub Pages or Azure | [Deployment](/quickstart/deployment/) |
| Set up CI/CD automation | [CI/CD & Automation](/quickstart/cicd-automation/) |
| Optimize for SEO and performance | [Optimization & Maintenance](/quickstart/optimization-maintenance/) |

> **IT-Journey Quests:** [Container Fundamentals](/quests/containers/container-fundamentals/) · [Docker Compose Orchestration](/quests/containers/docker-compose-orchestration/)
>
> **IT-Journey Docs:** [Development Environment](/docs/setup/DEVELOPMENT_ENVIRONMENT/)
>
> **External Docs:** [Docker Compose](https://docs.docker.com/compose/) · [Jekyll Serve Command](https://jekyllrb.com/docs/usage/)
