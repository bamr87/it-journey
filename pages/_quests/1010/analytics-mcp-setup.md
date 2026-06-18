---
title: 'Connect Google Analytics to Your AI Agent via MCP'
description: Set up the Google Analytics MCP server in Claude Code with a secure service-account key, then pull your first live traffic report from the command line.
date: '2026-06-14T18:00:00.000Z'
preview: /images/previews/quest-analytics-mcp-setup.png
level: '1010'
difficulty: 🟡 Medium
estimated_time: 45-60 minutes
primary_technology: mcp
quest_type: main_quest
fmContentType: quest
skill_focus: devops
learning_style: hands-on
quest_series: Measure & Master Your Site
quest_line: The Observability Path
quest_arc: Analytics, SEO & Site Health
sub_title: 'Level 1010 (10) Quest: Main Quest - Model Context Protocol'
excerpt: Wire Google Analytics into your AI agent over MCP and run your first live report — securely.
snippet: Give your agent eyes on the traffic.
author: Quest Master IT-Journey
tags:
- '1010'
- mcp
- google-analytics
- claude-code
- main_quest
- hands-on
- gamified-learning
- observability
categories:
- Quests
- Monitoring & Observability
- Medium
keywords:
  primary:
  - '1010'
  - mcp
  - google-analytics
  - service-account
  secondary:
  - claude-code
  - hands-on
  - observability
  - analytics-data-api
lastmod: '2026-06-14T18:00:00.000Z'
permalink: /quests/1010/analytics-mcp-setup/
attachments: ''
comments: true
prerequisites:
  knowledge_requirements:
  - Basic command-line proficiency
  - A Google Analytics 4 property already collecting data
  - Familiarity with JSON and environment variables
  system_requirements:
  - Node.js 18+ and npx
  - Claude Code CLI installed
  - A Google Cloud account with permission to create service accounts
  skill_level_indicators:
  - Comfortable editing shell environment variables
  - Can navigate the Google Cloud Console
  - Understands the difference between a public and private repository
quest_dependencies:
  required_quests: []
  recommended_quests: []
  unlocks_quests:
  - /quests/1010/query-traffic-with-mcp/
quest_relationships:
  parent_quest: null
  child_quests: []
  parallel_quests: []
  sequel_quests:
  - /quests/1010/query-traffic-with-mcp/
learning_paths:
  primary_paths:
  - DevOps Automation
  - Web Analytics
  character_classes:
  - 💻 Software Developer
  - 📊 Data Analyst
  - 🛠️ DevOps Engineer
  skill_trees:
  - MCP & AI Tooling
  - Web Analytics
rewards:
  badges:
  - 🏆 MCP Connector
  - 🔐 Key Keeper
  skills_unlocked:
  - 🛠️ MCP server configuration
  - 🔐 Service-account credential handling
  - 📊 Google Analytics Data API queries
  progression_points: 150
  unlocks_features:
  - Live analytics access for your AI agent
validation_criteria:
  completion_requirements:
  - The google-analytics MCP server is registered and connects
  - A live runReport query returns data for your property
  - No credentials are committed to the repository
  skill_demonstrations:
  - Explain why GA_PROPERTY_ID differs from the G- measurement ID
  - Distinguish a service-account key from an OAuth client file
  knowledge_checks:
  - Which Google API must be enabled for the Data API to work?
  - Where should the service-account key file live?
quest_mapping:
  coordinates: '[10, 0]'
  region: Warrior
  realm: Observability
  biome: Terminal
draft: false
layout: quest
---

## 📖 The Legend Behind This Quest

Your site has been quietly collecting analytics for months, but nobody reads them. In this quest you'll give your AI agent **eyes on the traffic** by connecting Google Analytics through a **Model Context Protocol (MCP)** server — the standard way agents gain new tools. By the end, you can ask your agent "how's traffic this week?" and it will actually know.

The catch, as every seasoned adventurer learns: connecting a data source is the easy part. Doing it *securely* — without leaking a private key into a public repo — is the real test.

## 🎯 Quest Objectives

### Primary Objectives (Required for Quest Completion)
- [ ] Create a Google Cloud **service account** and enable the **Analytics Data API**
- [ ] Grant the service account **Viewer** access on your GA4 property
- [ ] Register the `google-analytics` MCP server in your agent
- [ ] Run a live report and see real numbers

### Secondary Objectives (Bonus Achievements)
- [ ] Move the key out of your repo and `chmod 600` it
- [ ] Add gitignore patterns so credentials can never be committed

### Mastery Indicators
- You can explain the JWT service-account flow vs. the OAuth redirect flow
- You can find the numeric property ID without confusing it with the `G-` tag

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- Basic command-line navigation and environment variables
- A GA4 property that is already collecting data

### 🛠️ System Requirements
- Node.js 18+ with `npx`, and the Claude Code CLI
- A Google Cloud account that can create service accounts

## 🧙‍♂️ Chapter 1: Forge the Credential

The MCP server uses **server-to-server (JWT) auth**, which means a **service account** — not an OAuth client. Watch this trap: a file named `client_secret_….apps.googleusercontent.com.json` is an OAuth *web client* and will **not** work.

1. **Enable the API** — in the Google Cloud Console, enable **Analytics Data API** (`analyticsdata.googleapis.com`) for your project.
2. **Create the service account** — IAM & Admin → Service Accounts → Create. Name it something like `ga-reader`.
3. **Download a JSON key** — open the account → **Keys → Add key → Create new key → JSON**. This file has `type: service_account`, `client_email`, and `private_key`.
4. **Grant access in GA** — Analytics → Admin → **Property Access Management** → add the service account's email with **Viewer**. Uncheck "Notify by email" (service accounts can't receive mail).

Verify you grabbed a real service-account key (no secrets printed):

```bash
node -e "const k=require('./key.json'); \
  console.log('type:', k.type, '| has private_key:', !!k.private_key)"
# Expect: type: service_account | has private_key: true
```

## 🔐 Chapter 2: Keep the Secret Out of Your Repo

A private key in a public repo is a breach waiting to happen. **Move it out of the repo entirely** and lock down permissions:

```bash
mkdir -p ~/.config/gcloud
mv ./key.json ~/.config/gcloud/ga-reader.json
chmod 600 ~/.config/gcloud/ga-reader.json
```

Add a safety net so a stray `git add .` can never catch a key:

```bash
printf '%s\n' 'client_secret_*.json' '*.apps.googleusercontent.com.json' \
  '*service-account*.json' >> .gitignore
```

> 🧠 **Rule of thumb:** gitignore is a safety net, not a storage location. Credentials live *outside* the repo.

## ⚙️ Chapter 3: Register the MCP Server

Find your **numeric** property ID in GA → Admin → **Property Settings** (a number like `314278834`) — this is *not* the `G-XXXX` measurement ID. Then register the server, reading the key from the file so the secret never appears in your shell history:

```bash
KEY="$HOME/.config/gcloud/ga-reader.json"
claude mcp add google-analytics --scope user \
  -e GOOGLE_CLIENT_EMAIL="$(node -p "require('$KEY').client_email")" \
  -e GOOGLE_PRIVATE_KEY="$(node -p "require('$KEY').private_key")" \
  -e GA_PROPERTY_ID="123456789" \
  -- npx -y mcp-server-google-analytics
```

Restart your agent so the new tools (`runReport`, `getPageViews`, `getActiveUsers`, `getEvents`, `getUserBehavior`) load.

## ✅ Validation

Ask your agent to run a 28-day report, or test the chain directly:

```bash
# A PERMISSION_DENIED about the Data API means step 1 (enable API) was skipped.
# A property error means the Viewer grant (step 4) is missing.
```

A successful run returns active users, sessions, and page views for your property. 🎉

## 🏆 Rewards

- 🏆 **MCP Connector** — your agent can now query live analytics
- 🔐 **Key Keeper** — credentials secured outside the repo

## ➡️ Next Quest

Your agent can see the traffic — now learn to ask it the right questions. Continue to **[Query Your Traffic with the GA MCP Tools](/quests/1010/query-traffic-with-mcp/)**.
