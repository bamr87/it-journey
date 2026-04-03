---
title: "Jekyll & zer0-mistakes Theme Installation"
author: bamr87
description: Install Jekyll with the zer0-mistakes theme — via Gemfile or Docker — then verify your site builds and serves correctly.
excerpt: "Install Jekyll with the zer0-mistakes theme via Gemfile or Docker, configure Bundler, and verify your local site builds and serves correctly."
permalink: /quickstart/jekyll/
categories:
  - quickstart
slug: jekyll
lastmod: 2026-04-02T03:14:50.876Z
draft: false
date: 2021-11-09T17:30:29.000Z
difficulty: 🟢 Easy
estimatedTime: 15-30 minutes
prerequisites:
  - Ruby 3.2+ and Bundler installed (see [Machine Setup](/quickstart/machine-setup/))
  - Git repository created (see [GitHub Setup](/quickstart/github/))
tags:
  - jekyll
  - ruby
  - theme
  - installation
keywords:
  primary:
    - jekyll installation
    - zer0-mistakes theme
    - jekyll setup
  secondary:
    - bundler
    - gemfile
    - ruby gems
sidebar:
  nav: quickstart
---

This guide covers **Phase 4** of the [Quick Start](/quickstart/) — installing Jekyll and the zer0-mistakes theme that powers [it-journey.dev](https://it-journey.dev). By the end, you'll have a working Jekyll site running locally.

---

## Prerequisites

Before starting, confirm these tools are installed:

```bash
ruby --version       # 3.2+
bundler --version    # 2.x+
git --version        # 2.x+
```

If anything is missing, complete the [Machine Setup](/quickstart/machine-setup/) first.

Jekyll also requires:

- **RubyGems** (ships with Ruby)
- **GCC and Make** (included with Xcode CLI on macOS, `build-essential` on Linux)

If you want to use GitHub Pages, here are the [supported dependency versions](https://pages.github.com/versions.json).

---

## Install Dependencies via Gemfile

The IT-Journey repository already includes a `Gemfile`. If you're starting fresh or want to understand the setup:

```bash
cd ~/github/it-journey   # or your project directory
```

### Using the Existing Gemfile

```bash
# Install all dependencies specified in Gemfile
bundle install
```

### Creating a Gemfile from Scratch

If you don't have a Gemfile yet (e.g., starting a new zer0-mistakes site):

```bash
cat > Gemfile << 'EOF'
source "https://rubygems.org"

gem 'github-pages'
gem 'jekyll-theme-zer0'
gem 'webrick'
EOF

bundle install
```

**Key gems:**

| Gem | Purpose |
|-----|---------|
| `github-pages` | GitHub Pages-compatible Jekyll build with all supported plugins |
| `jekyll-theme-zer0` | The zer0-mistakes theme gem for local development |
| `webrick` | Required web server for Ruby 3.0+ |

---

## Theme Configuration

The zer0-mistakes theme can be loaded in two ways. Which one you use depends on whether you're developing locally or deploying to GitHub Pages.

### Option 1: Remote Theme (GitHub Pages Deployment)

In your `_config.yml`:

```yaml
remote_theme: "bamr87/zer0-mistakes"
```

This is what GitHub Pages uses when building your site. No gem installation needed on the server.

### Option 2: Local Gem (Local/Docker Development)

In your `_config.yml` (or `_config_dev.yml`):

```yaml
theme: "jekyll-theme-zer0"
```

This uses the locally installed gem, which is faster for development and works offline.

### Using Both Configs Together

The recommended workflow uses the remote theme for production and the local gem for development:

```bash
# Development: loads _config_dev.yml overrides (including local theme)
bundle exec jekyll serve --config _config.yml,_config_dev.yml

# Production: uses remote_theme from _config.yml only
JEKYLL_ENV=production bundle exec jekyll build
```

---

## Verify Your Installation

### Native Ruby

```bash
bundle exec jekyll serve
# Open http://localhost:4000 (or 4002 if configured) in your browser
```

You should see the zer0-mistakes theme with the site title and navigation.

### Docker (Alternative)

If you prefer Docker (no Ruby installation needed on your host machine):

```bash
docker-compose up -d
# Open http://localhost:4002 in your browser
```

See the [Local Development](/quickstart/local-development/) guide for the full Docker workflow.

---

## Common Issues

### `webrick` LoadError (Ruby 3.0+)

If you see `cannot load such file -- webrick`:

```bash
bundle add webrick
```

### Bundler Version Mismatch

If `bundle install` fails with a version error:

```bash
gem install bundler
bundle install
```

### Theme Not Loading

If pages render without styling:

1. Confirm `remote_theme` or `theme` is set in `_config.yml`
2. For local development, ensure `jekyll-theme-zer0` is in your `Gemfile`
3. Run `bundle install` again after Gemfile changes
4. Restart the Jekyll server (`Ctrl+C`, then `bundle exec jekyll serve`)

### Live Reload

Pass `--livereload` to automatically refresh the browser when files change:

```bash
bundle exec jekyll serve --livereload
```

---

## What's Next

| Next Step | Guide |
|-----------|-------|
| Configure `_config.yml` — site identity, skins, collections | [Site Configuration](/quickstart/site-configuration/) |
| Set up VS Code with extensions and Front Matter CMS | [VS Code Setup](/quickstart/vscode-setup/) |
| Run the site with Docker or native Ruby | [Local Development](/quickstart/local-development/) |

> **IT-Journey Quests:** [Jekyll Fundamentals](/quests/frontend/jekyll-fundamentals/) · [YAML Configuration](/quests/frontend/yaml-configuration/)
>
> **IT-Journey Docs:** [Installation Update](/docs/setup/INSTALLATION_UPDATE/)
>
> **External Docs:** [Jekyll Installation](https://jekyllrb.com/docs/installation/) · [Jekyll Themes](https://jekyllrb.com/docs/themes/) · [zer0-mistakes Theme](https://github.com/bamr87/zer0-mistakes)
