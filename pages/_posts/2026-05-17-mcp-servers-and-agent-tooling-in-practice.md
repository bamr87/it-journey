---
title: MCP Servers and Agent Tooling in Practice
description: A practical guide to the Model Context Protocol and GitHub-native agent tooling — what MCP servers do and how GH-600 tests them.
permalink: /posts/mcp-servers-and-agent-tooling-in-practice/
draft: false
date: '2026-05-17T00:00:00.000Z'
preview: /images/previews/mcp-servers-and-agent-tooling-in-practice.png
sub-title: Domain 2 deep-dive for GH-600 candidates
excerpt: MCP is the USB-C of AI tooling — a standard connector that lets agents speak to any external system. Here's how to use it on GitHub.
snippet: One protocol, many tools, infinite agent capability.
author: IT-Journey Team
layout: article
featured: true
keywords:
- MCP server github
- model context protocol
- gh-600 domain 2
- agentic tooling
- github copilot tools
lastmod: '2026-05-17T00:00:00.000Z'
tags:
- gh-600
- agentic-ai
- mcp
- tooling
- domain-2
categories:
- AI & Machine Learning
- Developer Tools
---
Domain 2 of GH-600 (18% of the exam) covers the tools, environments, and capabilities that GitHub Copilot agents can use. The centrepiece is the **Model Context Protocol (MCP)**.

## What Is MCP?

MCP is an open standard that allows AI models to connect to external tools in a structured, predictable way. Think of it as a universal adapter. Without MCP, every tool integration requires custom code. With MCP, a tool exposes a standard interface, and any MCP-compatible model can use it.

The GitHub MCP server is one of the most important implementations. It gives agents the ability to:

- Read and create issues
- Read and update pull requests
- Query repository contents
- Check workflow run statuses
- Manage labels and milestones

All without writing custom API code in every agent.

## Configuring MCP in VS Code

MCP servers are configured in `.vscode/mcp.json` (workspace level) or VS Code user settings:

```json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github-token}"
      }
    }
  }
}
```

The `${input:github-token}` pattern prompts for the token securely, rather than hardcoding it.

## Scoped vs. Unscoped Tools

Domain 2 sub-skill 2.1 covers **tool selection and permissions**. The principle: agents should only have access to tools they need for the current task. This is analogous to least-privilege in security.

For a code review agent:

- ✅ Read repository contents
- ✅ Create PR review comments
- ❌ Create issues (not needed)
- ❌ Manage repo settings (not needed)

Tool scoping reduces the blast radius of an agent that misbehaves or is given ambiguous instructions.

## Development Environment Integration (Sub-skill 2.3)

Sub-skill 2.3 covers how agents interact with the development environment. This includes:

- `AGENTS.md` — a file the agent reads to understand the repository conventions, forbidden actions, and preferred patterns
- `.github/copilot-instructions.md` — instructions that Copilot reads to understand the project context
- Git configuration — ensuring the agent uses a clearly identified committer identity

## Domain 2 Quests

| Quest | Skill | Link |
|---|---|---|
| Q4 | Tool Selection & Permissions | [Tool Selection & Permissions](/quests/gh-600/agentic-tool-selection-and-permissions/) |
| Q5 | MCP Server Mastery | [MCP Server Mastery](/quests/gh-600/agentic-mcp-server-mastery/) |
| Q6 | Dev Environment Integration | [Dev Environment Integration](/quests/gh-600/agentic-dev-environment-integration/) |
| Q7 | Safe Execution & Error Handling | [Safe Execution & Error Handling](/quests/gh-600/agentic-safe-execution-and-error-handling/) |

These quests cover MCP configuration, token scoping, `AGENTS.md` authoring, and error escalation workflows.
