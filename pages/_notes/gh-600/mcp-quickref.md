---
title: MCP Quick Reference
description: Quick reference for setting up, configuring, and using Model Context Protocol (MCP) servers with GitHub Copilot — setup commands, configuration schema, and common server list.
date: '2026-05-17T00:00:00.000Z'
layout: default
permalink: /notes/gh-600/mcp-quickref/
author: IT-Journey Team
tags:
- gh-600
- mcp
- model-context-protocol
- quick-reference
categories:
- Notes
lastmod: '2026-05-17T00:00:00.000Z'
draft: false
---
# MCP Quick Reference

## What Is MCP?

The **Model Context Protocol** is an open standard that lets AI models connect to external tools. MCP servers expose structured tools (functions) that an AI can call.

## Setup: GitHub MCP Server

### Install
```bash
npx @modelcontextprotocol/server-github
```

### VS Code Configuration (`.vscode/mcp.json`)
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

### User Settings (`settings.json` or Copilot MCP settings)

> **Never** commit a literal PAT (`ghp_...`) into `settings.json`. Use a VS Code input prompt (‘`${input:github-token}`‘), an environment variable (‘`${env:GITHUB_TOKEN}`‘), or a secret manager. The example below shows the safe environment-variable pattern.

```json
{
  "github.copilot.chat.mcp.servers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_TOKEN}"
      }
    }
  }
}
```

## Common MCP Servers

| Server | Package | Purpose |
|---|---|---|
| GitHub | `@modelcontextprotocol/server-github` | Issues, PRs, repo contents |
| Filesystem | `@modelcontextprotocol/server-filesystem` | Local file read/write |
| Fetch | `@modelcontextprotocol/server-fetch` | Web page retrieval |
| Memory | `@modelcontextprotocol/server-memory` | Persistent key-value store |

## Token Scopes for GitHub MCP

| Capability | Required Scope |
|---|---|
| Read repos | `repo:read` |
| Create issues | `issues:write` |
| Create PRs | `pull-requests:write` |
| Read Actions | `actions:read` |
| Read users | `user:read` |

**Principle:** Grant only the scopes needed for the task. Prefer fine-grained PATs over classic PATs.

## Testing an MCP Server

Open VS Code Command Palette → `MCP: List Servers` → confirm server shows as connected.

In Copilot Chat, test with: `@github list my open issues in {owner}/{repo}`

---

*Part of: [[GH-600 Agentic AI Quick-Reference Notes]] · Related quest: [[The MCP Conclave: Mastering Model Context Protocol Servers]] · Hub: [[The Agentic Codex: GH-600 Study Hub]]*
