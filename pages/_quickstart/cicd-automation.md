---
title: CI/CD & Automation
author: bamr87
description: Set up GitHub Actions workflows for automated building, testing, link checking, frontmatter validation, and deployment of your Jekyll site.
permalink: /quickstart/cicd-automation/
categories:
  - quickstart
slug: cicd-automation
lastmod: 2026-04-02T03:14:50.968Z
draft: false
date: 2026-04-01T00:00:00.000Z
difficulty: 🟡 Medium
estimatedTime: 30-40 minutes
prerequisites:
  - GitHub repository set up (see [GitHub Setup](/quickstart/github/))
  - Site deploys successfully (see [Deployment](/quickstart/deployment/))
tags:
  - cicd
  - github-actions
  - automation
  - testing
keywords:
  primary:
    - github actions
    - ci/cd
    - jekyll automation
  secondary:
    - build validation
    - link checking
    - frontmatter validation
sidebar:
  nav: quickstart
---

This guide covers **Phase 13** of the [Quick Start](/quickstart/) — setting up GitHub Actions for automated building, testing, and deployment.

---

## Active Workflows in IT-Journey

IT-Journey runs 7 GitHub Actions workflows:

| Workflow | Trigger | What It Does |
|----------|---------|-------------|
| **Build Validation** | Push, PR | Builds the Jekyll site and catches errors |
| **Link Health Guardian** | Schedule (Mon/Fri), Manual | Scans for broken links with optional AI analysis |
| **Frontmatter Validation** | PR, Manual | Validates YAML metadata with auto-fix |
| **AI Content Review** | PR, Push | GPT-4 quality analysis of content |
| **Organize Posts** | Weekly schedule | Auto-categorizes posts into folders |
| **CodeQL Analysis** | Schedule, Push | Security vulnerability scanning |
| **Dependency Checker** | Schedule | Alerts on outdated dependencies |

Workflow files live in `.github/workflows/`.

---

## Basic Build & Deploy Workflow

A minimal workflow that builds your Jekyll site and deploys to GitHub Pages:

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

This workflow:
1. Checks out the code
2. Sets up Ruby 3.2 with bundler caching
3. Builds the Jekyll site
4. Uploads `_site/` as an artifact
5. Deploys to GitHub Pages

---

## Testing Tools

| Tool | Command | What It Checks |
|------|---------|---------------|
| **Link Checker** | `python3 scripts/link-checker.py --scope website` | Broken internal/external links |
| **Quest Validator** | `python3 test/quest-validator/quest_validator.py -d pages/_quests/` | Quest frontmatter and content structure |
| **Markdown Lint** | `markdownlint **/*.md` | Markdown style and formatting |

### Running Tests Locally

```bash
# Check links
python3 scripts/link-checker.py --scope website --timeout 30

# Validate quests
python3 test/quest-validator/quest_validator.py -d pages/_quests/

# Lint markdown
markdownlint "**/*.md"
```

---

## Automation Scripts

IT-Journey includes scripts for common tasks:

### Environment & Build

```bash
# Set up development environment
./scripts/core/environment-setup.sh

# Build for production
./scripts/development/build/build-site.sh --production
```

### Version Management

```bash
# Semantic version bumping
./scripts/core/version-manager.sh patch   # 1.0.0 → 1.0.1
./scripts/core/version-manager.sh minor   # 1.0.0 → 1.1.0
./scripts/core/version-manager.sh major   # 1.0.0 → 2.0.0
```

### Content Management

```bash
# Convert Jupyter notebooks to Markdown
./scripts/development/content/jupyter-to-markdown.sh pages/_notebooks/

# Organize posts by category
python3 scripts/development/content/organize-posts.py --dry-run

# Generate content statistics
make stats-update
```

---

## Writing Custom Workflows

### Workflow Triggers

| Trigger | When It Runs |
|---------|-------------|
| `push` | On every push to specified branches |
| `pull_request` | On PR open, sync, or reopen |
| `schedule` | On a cron schedule |
| `workflow_dispatch` | Manual trigger from GitHub UI |

### Example: PR Validation

```yaml
name: PR Quality Check
on:
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build site
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
      - run: bundle exec jekyll build
      
      - name: Check links
        run: python3 scripts/link-checker.py --scope website --timeout 30
      
      - name: Lint markdown
        run: |
          npm install -g markdownlint-cli
          markdownlint "**/*.md" || true
```

---

## Secrets and Environment Variables

Store sensitive values as GitHub Secrets (**Settings → Secrets and variables → Actions**):

| Secret | Used By |
|--------|---------|
| `AZURE_STATIC_WEB_APPS_API_TOKEN` | Azure deployment |
| `OPENAI_API_KEY` | AI Content Review workflow |

Access in workflows with `${{ secrets.SECRET_NAME }}`.

---

## What's Next

| Next Step | Guide |
|-----------|-------|
| Optimize for SEO, performance, and accessibility | [Optimization & Maintenance](/quickstart/optimization-maintenance/) |

> **IT-Journey Quests:** [CI/CD Fundamentals](/quests/cicd/cicd-fundamentals/) · [GitHub Actions Basics](/quests/cicd/github-actions-basics/) · [Bash Scripting](/quests/intermediate/bash-scripting/)
>
> **IT-Journey Docs:** [GitHub Actions Workflows](/docs/workflows/GITHUB_ACTIONS/) · [Testing Frameworks](/docs/testing/TESTING_FRAMEWORKS/) · [Scripts Guide](/docs/scripts/SCRIPTS_GUIDE/)
>
> **External Docs:** [GitHub Actions](https://docs.github.com/en/actions) · [markdownlint Rules](https://github.com/DavidAnson/markdownlint)
