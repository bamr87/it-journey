---
title: Repository & GitHub Setup
author: bamr87
description: Create your Git repository, configure GitHub CLI, and set up the IT-Journey project structure for Jekyll development.
permalink: /quickstart/github/
categories:
  - quickstart
slug: github
lastmod: 2026-04-02T03:14:50.885Z
draft: false
date: 2022-01-10T18:47:51.000Z
difficulty: 🟢 Easy
estimatedTime: 15-20 minutes
prerequisites:
  - Git installed (see [Machine Setup](/quickstart/machine-setup/))
  - GitHub account ([github.com](https://github.com))
tags:
  - git
  - github
  - repository
  - setup
keywords:
  primary:
    - github setup
    - git repository
    - github cli
  secondary:
    - fork
    - clone
    - submodules
sidebar:
  nav: quickstart
---

This guide covers **Phase 3** of the [Quick Start](/quickstart/) — creating your Git repository and configuring GitHub for the IT-Journey project. Every Jekyll site lives in a Git repository, and this phase sets yours up.

---

## Prerequisites

- [GitHub CLI](https://cli.github.com/) (optional but recommended)
- Git installed and configured
- A GitHub account

Confirm your tools:

**macOS:**

```bash
brew -v
```

**Windows:**

```powershell
winget -v
```

---

## Install GitHub CLI

### macOS

```bash
brew install gh
```

### Windows

```powershell
winget install git.git
winget install GitHub.cli
```

### Linux (Ubuntu/Debian)

```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh
```

### Verify

```bash
gh --version
```

---

## Configure Git Identity

```bash
# Set your name and email (used in commits)
git config --global user.name "Your Full Name"
git config --global user.email "your-email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# For GitHub noreply email (replace <username>):
git config --global user.email "<username>@users.noreply.github.com"

# Verify
git config --list
```

---

## Authenticate with GitHub

```bash
# Login to GitHub CLI (follow the interactive prompts)
gh auth login

# Verify authentication
gh auth status
```

---

## Create Your Repository

Choose one of these three approaches:

### Option A: Fork IT-Journey (Recommended for Learning)

Fork the full IT-Journey repository to get all content, themes, workflows, and configuration:

```bash
cd ~
mkdir -p github && cd github
gh repo fork bamr87/it-journey
cd it-journey
```

This creates a fork under your GitHub account and clones it locally.

### Option B: Start Fresh with zer0-mistakes

Create a new repository and add the zer0-mistakes theme from scratch:

```bash
mkdir my-site && cd my-site
git init
git remote add origin https://github.com/YOUR-USERNAME/my-site.git
```

Then add the theme configuration manually (see [Jekyll Setup](/quickstart/jekyll/)).

### Option C: Use the zer0-mistakes Installer

One-command setup that creates the Gemfile, docker-compose.yml, starter `_config.yml`, and a GitHub Actions workflow:

```bash
curl -fsSL https://raw.githubusercontent.com/bamr87/zer0-mistakes/main/install.sh | bash
```

---

## Repository Structure

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
├── assets/                   # Static files (CSS, JS, images)
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

---

## Add Submodules (Optional)

If your project uses [Git submodules](http://git-scm.com/book/en/v2/Git-Tools-Submodules):

```bash
git submodule add https://github.com/bamr87/winget-packages.git winget

# If the submodule directory is empty, initialize it:
git submodule update --init
```

---

## What's Next

| Next Step | Guide |
|-----------|-------|
| Install Jekyll and the zer0-mistakes theme | [Jekyll Setup](/quickstart/jekyll/) |
| Configure `_config.yml` for your site | [Site Configuration](/quickstart/site-configuration/) |
| Set up your development environment | [Machine Setup](/quickstart/machine-setup/) |

> **IT-Journey Quests:** [Git Basics](/quests/init_world/git-basics/) · [GitHub Pages Basics](/quests/frontend/github-pages-basics/)
>
> **IT-Journey Docs:** [Repository Structure](/docs/architecture/REPOSITORY_STRUCTURE/)
>
> **External Docs:** [GitHub: Creating a Repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) · [Git Documentation](https://git-scm.com/doc)
