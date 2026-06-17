---
title: 'Query Your Traffic with the GA MCP Tools'
description: Put your MCP connection to work — run reports, choose dimensions and metrics, filter by date and page, and turn plain-English questions into GA queries.
date: '2026-06-14T18:00:00.000Z'
preview: /images/previews/quest-query-traffic-with-mcp.png
level: '1010'
difficulty: 🟡 Medium
estimated_time: 30-45 minutes
primary_technology: google-analytics
quest_type: main_quest
fmContentType: quest
skill_focus: data
learning_style: hands-on
quest_series: Measure & Master Your Site
quest_line: The Observability Path
quest_arc: Analytics, SEO & Site Health
sub_title: 'Level 1010 (10) Quest: Main Quest - Analytics Data API'
excerpt: Learn the five MCP tools and the dimensions and metrics that turn raw analytics into answers.
snippet: Stop staring at dashboards. Ask questions.
author: Quest Master IT-Journey
tags:
- '1010'
- google-analytics
- mcp
- analytics-data-api
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
  - google-analytics
  - mcp
  - runreport
  secondary:
  - dimensions-and-metrics
  - hands-on
  - observability
  - traffic-analysis
lastmod: '2026-06-14T18:00:00.000Z'
permalink: /quests/1010/query-traffic-with-mcp/
attachments: ''
comments: true
prerequisites:
  knowledge_requirements:
  - A connected google-analytics MCP server
  - Basic understanding of GA4 dimensions and metrics
  system_requirements:
  - The google-analytics MCP server registered and connecting
  - An AI agent that can call MCP tools
  skill_level_indicators:
  - Can read a table of metrics by dimension
  - Comfortable iterating on a query to refine results
quest_dependencies:
  required_quests:
  - /quests/1010/analytics-mcp-setup/
  recommended_quests: []
  unlocks_quests:
  - /quests/1010/automate-traffic-report/
quest_relationships:
  parent_quest: null
  child_quests: []
  parallel_quests: []
  sequel_quests:
  - /quests/1010/automate-traffic-report/
learning_paths:
  primary_paths:
  - Web Analytics
  - DevOps Automation
  character_classes:
  - 📊 Data Analyst
  - 💻 Software Developer
  - 🛠️ DevOps Engineer
  skill_trees:
  - Web Analytics
  - MCP & AI Tooling
rewards:
  badges:
  - 🏆 Report Runner
  - 📊 Dimension Wrangler
  skills_unlocked:
  - 📊 runReport with dimensions and metrics
  - 🔎 Date ranges and dimension filters
  - 🤖 Natural-language analytics queries
  progression_points: 150
  unlocks_features:
  - On-demand traffic answers from your agent
validation_criteria:
  completion_requirements:
  - Ran a top-pages report for a date range
  - Segmented traffic by channel
  - Filtered a report by a dimension value
  skill_demonstrations:
  - Name the five GA MCP tools and when to use each
  - Explain the difference between a dimension and a metric
  knowledge_checks:
  - What does sessionDefaultChannelGroup tell you?
  - How do you compare two date ranges in one report?
quest_mapping:
  coordinates: '[10, 1]'
  region: Warrior
  realm: Observability
  biome: Terminal
draft: false
layout: quest
---

## 📖 The Legend Behind This Quest

Your agent can reach Google Analytics now — but a connection without good questions is just a faster way to be confused. In this quest you'll learn the **five tools** the MCP server exposes, the GA4 vocabulary of **dimensions and metrics**, and how to turn "how's traffic?" into a precise, repeatable report.

## 🎯 Quest Objectives

### Primary Objectives (Required for Quest Completion)
- [ ] Run a **top-pages** report for a date range
- [ ] Segment sessions by **channel**
- [ ] Apply a **dimension filter** to narrow a report

### Secondary Objectives (Bonus Achievements)
- [ ] Compare two date ranges in one report (week-over-week)
- [ ] Ask your agent a plain-English question and read its query back

### Mastery Indicators
- You can name the five tools and pick the right one quickly
- You can build a `runReport` call from a question in your head

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- Completed [Connect Google Analytics to Your AI Agent](/quests/1010/analytics-mcp-setup/)
- Basic GA4 concepts

### 🛠️ System Requirements
- The `google-analytics` MCP server connected to your agent

## 🧰 Chapter 1: Know Your Five Tools

The MCP server exposes five tools. Four are convenience wrappers; one is the workhorse.

| Tool | Use it for |
|---|---|
| `getActiveUsers` | quick active-user count |
| `getPageViews` | page views, optionally by a dimension |
| `getEvents` | event counts |
| `getUserBehavior` | session duration, bounce/engagement |
| `runReport` | **anything** — custom dimensions + metrics + filters |

When in doubt, reach for `runReport`. The others are shortcuts for common questions.

## 📐 Chapter 2: Dimensions vs. Metrics

Every report is **metrics** (numbers) grouped by **dimensions** (attributes).

- **Metrics:** `activeUsers`, `sessions`, `screenPageViews`, `engagementRate`, `averageSessionDuration`
- **Dimensions:** `pagePath`, `pageTitle`, `sessionDefaultChannelGroup`, `country`, `deviceCategory`, `hostName`, `date`

A report = "give me these *metrics*, broken down by these *dimensions*, for this *date range*."

## 🔎 Chapter 3: Build Real Reports

Just ask your agent: *"Top 10 pages by views over the last 28 days."* Behind the scenes it calls `runReport`:

```js
runReport({
  dateRanges: [{ startDate: "28daysAgo", endDate: "today" }],
  dimensions: [{ name: "pagePath" }],
  metrics: [{ name: "screenPageViews" }, { name: "activeUsers" }],
  orderBys: [{ metric: { metricName: "screenPageViews" }, desc: true }],
  limit: 10,
})
```

**Traffic by channel** — where visitors come from:

```js
runReport({
  dateRanges: [{ startDate: "28daysAgo", endDate: "today" }],
  dimensions: [{ name: "sessionDefaultChannelGroup" }],
  metrics: [{ name: "sessions" }, { name: "engagementRate" }],
})
```

**Week-over-week** — two date ranges in one report:

```js
dateRanges: [
  { startDate: "7daysAgo",  endDate: "today",     name: "cur" },
  { startDate: "14daysAgo", endDate: "8daysAgo",  name: "prev" },
]
```

**Filter to one slice** — e.g. only one section of the site:

```js
dimensionFilter: { filter: { fieldName: "pagePath",
  stringFilter: { matchType: "BEGINS_WITH", value: "/quests/" } } }
```

## 🧪 Chapter 4: Sanity-Check Before You Trust

One habit pays for itself forever: before believing a headline number, group by **`hostName`** once. It instantly reveals whether `localhost`, Docker, or another site is mixed into your data — so you analyze *production* traffic, not your own dev machine. Add this filter to keep reports honest:

```js
dimensionFilter: { filter: { fieldName: "hostName",
  stringFilter: { matchType: "EXACT", value: "your-site.dev" } } }
```

## ✅ Validation

- [ ] You produced a top-pages report and a channel report
- [ ] You filtered a report by a dimension value
- [ ] You can explain when to use `runReport` vs. the wrappers

## 🏆 Rewards

- 🏆 **Report Runner** — you build reports on demand
- 📊 **Dimension Wrangler** — dimensions and metrics are second nature

## ➡️ Next Quest

Running reports by hand gets old. Put it on autopilot in **[Automate a Weekly Traffic Report](/quests/1010/automate-traffic-report/)**.
