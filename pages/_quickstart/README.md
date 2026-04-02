---
title: "Quickstart Collection Index"
description: "Index of all quickstart guides for building and deploying a Jekyll site with the zer0-mistakes theme — from machine setup to CI/CD automation."
date: 2026-04-02T00:00:00.000Z
lastmod: 2026-04-02T00:00:00.000Z
author: bamr87
categories:
  - quickstart
tags:
  - quickstart
  - index
  - readme
  - jekyll
  - zer0-mistakes
excerpt: "Overview of every quickstart guide in this collection, covering machine setup, GitHub, Jekyll, content creation, deployment, and CI/CD."
draft: false
keywords:
  primary:
    - quickstart
    - jekyll setup
  secondary:
    - zer0-mistakes
    - github pages
    - documentation index
---

# Quickstart Collection

The `_quickstart/` collection contains the complete setup and configuration guides for building a Jekyll site with the zer0-mistakes theme, VS Code, Front Matter CMS, and GitHub Pages.

## Structure

| File | Phase | Topic |
|------|-------|-------|
| [index.md](index.md) | All | Navigation hub — links to every phase |
| [machine-setup.md](machine-setup.md) | 1 | Prerequisites & machine setup (macOS, Windows, Linux) |
| [github-setup.md](github-setup.md) | 3 | Repository creation & GitHub configuration |
| [jekyll-setup.md](jekyll-setup.md) | 4 | Jekyll & zer0-mistakes theme installation |
| [site-configuration.md](site-configuration.md) | 5 | `_config.yml` deep-dive |
| [vscode-setup.md](vscode-setup.md) | 6 | VS Code extensions, tasks, Front Matter CMS |
| [theme-architecture.md](theme-architecture.md) | 7 | Layouts, includes, Liquid, data files |
| [content-creation.md](content-creation.md) | 8 | Posts, quests, docs, frontmatter standards |
| [styling-navigation.md](styling-navigation.md) | 9–10 | Skins, CSS, navigation, sidebars, comments |
| [local-development.md](local-development.md) | 11 | Docker, native Ruby, VS Code tasks |
| [deployment.md](deployment.md) | 12 | GitHub Pages, Azure, manual deployment |
| [cicd-automation.md](cicd-automation.md) | 13 | GitHub Actions workflows, testing, scripts |
| [optimization-maintenance.md](optimization-maintenance.md) | 14–15 | SEO, performance, accessibility, maintenance |
| [charm-setup.md](charm-setup.md) | — | Charm terminal tools (supplementary) |

## Supplementary Guides

- `2025-07-22-vscode-for-neuroscience.md` — VS Code for neuroscience workflows
- `2025-03-08-setting-up-django-and-git.md` — Django project with Git

## Navigation

The sidebar navigation for this collection is defined in `_data/navigation/quickstart.yml`.

## Adding a New Guide

1. Create a new `.md` file in this directory
2. Add frontmatter with `title`, `description`, `permalink: /quickstart/<name>/`, and `sidebar: nav: quickstart`
3. Add the file to `_data/navigation/quickstart.yml` under the appropriate group
4. Link to it from `index.md`

---

**Last Updated:** 2026-04-02
