---
title: GitHub Copilot Coding Agent Cheatsheet
description: Quick reference for activating, configuring, and constraining the GitHub Copilot coding agent — including AGENTS.md structure, copilot-instructions.md, and permission scopes.
date: '2026-05-17T00:00:00.000Z'
layout: default
permalink: /notes/gh-600/copilot-coding-agent-cheatsheet/
author: IT-Journey Team
tags:
- gh-600
- copilot
- coding-agent
- quick-reference
categories:
- Notes
lastmod: '2026-05-17T00:00:00.000Z'
draft: false
---
# GitHub Copilot Coding Agent Cheatsheet

## Activating the Coding Agent

1. Assign an issue to `@copilot` (or add the `copilot` label — check your organisation settings)
2. Copilot creates a branch, opens a PR, and begins work
3. Monitor in the "Copilot" tab of the issue/PR

## AGENTS.md Structure

The `AGENTS.md` file in the repository root tells agents how to work in this repo.

```markdown
# AGENTS.md

## Repository Context
[Brief description of the project purpose]

## Development Environment
[How to build and test locally]

## Conventions
[Code style, naming, commit format]

## Forbidden Actions
- Do not modify files in `infrastructure/`
- Do not push directly to `main`
- Do not delete any files without explicit instruction
- Do not store credentials in code

## Preferred Patterns
[Architecture patterns the agent should follow]
```

## .github/copilot-instructions.md

Project-level instructions that Copilot reads for all interactions in this repository.

```markdown
# Copilot Instructions

## Project Summary
[One paragraph describing the project]

## Coding Standards
- Language: [primary language]
- Style guide: [link]
- Testing: [framework and requirements]

## AI Collaboration Guidelines
- Prefer small, focused PRs
- Always include tests for new code
- Update documentation when changing interfaces
```

## Workflow Permissions (Minimum for Coding Agent)

```yaml
permissions:
  contents: write       # Create branches, commit files
  pull-requests: write  # Create and update PRs
  issues: write         # Comment on issues
```

## Key GitHub Actions Contexts

| Context | Value |
|---|---|
| `github.actor` | Who triggered the run |
| `github.event_name` | Event type (`push`, `issues`, etc.) |
| `github.sha` | Current commit SHA |
| `github.ref` | Current branch/tag ref |
| `github.run_id` | Unique ID for this workflow run |

## Environment Variables for Agent Context

```bash
GITHUB_REPOSITORY   # owner/repo
GITHUB_WORKFLOW     # workflow name
GITHUB_RUN_ID       # unique run ID (use as correlation ID)
GITHUB_ACTOR        # who triggered this run
GITHUB_EVENT_NAME   # trigger event type
```

---

*Part of: [[GH-600 Agentic AI Quick-Reference Notes]] · Hub: [[The Agentic Codex: GH-600 Study Hub]]*
