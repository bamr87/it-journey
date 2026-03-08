---
title: Streamlining Content Creation - Using Crush in VSCode for Instant GitHub Pages Publishing
description: Discover how to leverage Crush AI in VSCode to write, edit, and publish articles to GitHub Pages with near-instant deployment through efficient CI/CD pipelines.
date: 2025-11-20
lastmod: 2025-11-20
version: 1.0.0
categories: [ai & machine learning, devops, web development]
tags: [crush, vscode, github-pages, ci-cd, jekyll, ai-assisted-writing]
permalink: /posts/2025-11-20-using-crush-vscode-github-pages/
author: IT-Journey AI Assistant
---

# Streamlining Content Creation: Using Crush in VSCode for Instant GitHub Pages Publishing

In the fast-paced world of technical content creation, efficiency is key. As part of the IT-Journey platform, we've optimized our workflow to allow creators to write articles using AI assistance and see them live on GitHub Pages almost instantly. This post explores how we use Crush—an AI-powered CLI assistant—integrated with VSCode, combined with robust CI/CD pipelines, to achieve this seamless publishing experience.

## What is Crush?

Crush is a powerful AI assistant that operates through CLI commands and function calls, enabling tasks like file editing, bash execution, web fetching, and more. In the context of IT-Journey, it's used for autonomous code and content generation without constant user intervention. When integrated into VSCode's terminal, it becomes a potent tool for content creators.

Key features observed in Crush:
- Autonomous decision-making: Breaks down tasks, searches codebase, edits files.
- Tool usage: Bash, edit, write, view, grep, glob for file operations.
- Safety-focused: Adheres to strict rules, never invents information.

## Setting Up Crush in VSCode

To get started:

1. **Install Crush CLI**: Follow the setup from Charm (crush@charm.land) tools. Ensure it's available in your PATH.

2. **VSCode Configuration**:
   - Open VSCode in the IT-Journey repo.
   - Use the integrated terminal for Crush commands.
   - Optional: Set up keybindings or tasks for common Crush operations.

3. **Repo-Specific Setup**:
   - Clone `bamr87/it-journey`.
   - Run `bundle install` for Jekyll dependencies.
   - Use `make` commands from Makefile for stats and builds.

From the repo's AGENTS.md, essential commands include Jekyll build/serve and script executions.

## The Writing Process with Crush

Crush excels at generating and editing Markdown content. Here's a typical workflow:

1. **Generate Article Structure**:
   - Prompt Crush: "Create a new post in pages/_posts/ with front matter for topic X."
   - Crush uses `write` tool to create the file with proper YAML front matter (observed standards: title, description, date, categories, tags).

2. **Content Creation**:
   - Use Crush to research: Fetch web content via `fetch` or `agentic_fetch`.
   - Generate sections: "Write section on Y using info from Z."
   - Edit existing: Use `edit` with exact matches for precise changes.

3. **Validation**:
   - Run repo's validators: `python3 test/quest-validator/quest_validator.py` (adapt for posts).
   - Check links: `python3 scripts/validation/link-checker.py`.

Example: To create this article, a prompt like "write an article for this repo, about using Crush in vscode to write articles and publishing them to github-pages almost instantly because of CI/CD designs" was used—Crush handled the rest autonomously.

## Instant Publishing via CI/CD

The magic lies in the repo's GitHub Actions setup (from .github/workflows/):

- **Triggers**: On push to main or PRs.
- **Jobs**:
  - Build Jekyll site.
  - Deploy to GitHub Pages or Azure.
  - Validate front matter, links, dependencies.

From azure-jekyll-deploy.yml:
- Uses Ruby setup, bundle install, jekyll build.
- Deploys via Azure static-web-apps-deploy.
- Post-deployment link checking.

Pushing changes triggers near-instant builds (typically <1 minute), making content live quickly.

Gotchas:
- Always read before editing (from critical rules).
- Use exact matches for edits.
- Test after changes.

## Benefits and Patterns

- **Speed**: From idea to published in minutes.
- **Consistency**: Enforces front matter standards.
- **Automation**: CI/CD handles building/deploying.
- **Observed Patterns**: Fantasy-themed content, multi-platform support, conventional commits.

This workflow transforms content creation into an efficient, AI-assisted process while maintaining educational quality in IT-Journey.

---

*Generated with Crush AI assistance. Last updated: 2025-11-20*
