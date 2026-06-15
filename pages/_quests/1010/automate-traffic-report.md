---
title: 'Automate a Weekly Traffic Report'
description: Build a standalone analytics digest script and schedule it with launchd or cron to post a weekly traffic report as a dated file and a GitHub issue.
date: '2026-06-14T18:00:00.000Z'
preview: /images/previews/quest-automate-traffic-report.png
level: '1010'
difficulty: 🔴 Hard
estimated_time: 60-90 minutes
primary_technology: automation
quest_type: main_quest
fmContentType: quest
skill_focus: devops
learning_style: hands-on
quest_series: Measure & Master Your Site
quest_line: The Observability Path
quest_arc: Analytics, SEO & Site Health
sub_title: 'Level 1010 (10) Quest: Main Quest - Scheduled Automation'
excerpt: Turn an on-demand query into a hands-off weekly digest that shows up where you work.
snippet: A report you have to remember to run is a report you never run.
author: Quest Master IT-Journey
tags:
- '1010'
- automation
- launchd
- cron
- main_quest
- hands-on
- gamified-learning
- observability
categories:
- Quests
- Monitoring & Observability
- Hard
keywords:
  primary:
  - '1010'
  - automation
  - launchd
  - scheduled-reports
  secondary:
  - cron
  - github-cli
  - hands-on
  - analytics-data-api
lastmod: '2026-06-14T18:00:00.000Z'
permalink: /quests/1010/automate-traffic-report/
attachments: ''
comments: true
prerequisites:
  knowledge_requirements:
  - Node.js scripting basics
  - Familiarity with the GA Data API client
  - Comfort with the terminal and a scheduler (launchd or cron)
  system_requirements:
  - Node.js 18+ and the @google-analytics/data package
  - The GitHub CLI (gh) authenticated, for issue creation
  - macOS (launchd) or Linux (cron)
  skill_level_indicators:
  - Can write and run a standalone Node script
  - Understands file paths and environment in scheduled jobs
quest_dependencies:
  required_quests:
  - /quests/1010/analytics-mcp-setup/
  recommended_quests:
  - /quests/1010/query-traffic-with-mcp/
  unlocks_quests: []
quest_relationships:
  parent_quest: null
  child_quests: []
  parallel_quests: []
  sequel_quests: []
learning_paths:
  primary_paths:
  - DevOps Automation
  - Web Analytics
  character_classes:
  - 🛠️ DevOps Engineer
  - 💻 Software Developer
  - 📊 Data Analyst
  skill_trees:
  - Automation & Scheduling
  - Web Analytics
rewards:
  badges:
  - 🏆 Automation Architect
  - ⏰ Scheduler Sage
  skills_unlocked:
  - 🛠️ Standalone GA Data API scripting
  - ⏰ Scheduling with launchd / cron
  - 🐙 Posting reports via the GitHub CLI
  progression_points: 200
  unlocks_features:
  - Hands-off weekly reporting
validation_criteria:
  completion_requirements:
  - A script that writes a dated markdown digest
  - A scheduled job that runs it weekly
  - Output delivered as a file and/or a GitHub issue
  skill_demonstrations:
  - Explain why a cloud scheduler cannot reach the local key
  - Show the scheduled job is registered
  knowledge_checks:
  - Why use absolute paths in a launchd/cron job?
  - Where does the service-account key live, and why not in the repo?
quest_mapping:
  coordinates: '[10, 3]'
  region: Warrior
  realm: Observability
  biome: Terminal
draft: false
layout: quest
---

## 📖 The Legend Behind This Quest

A report you have to remember to run is a report you never run. In this final quest of the path you'll turn the on-demand queries from the last quest into a **hands-off weekly digest** — a small script the scheduler runs for you, dropping a Markdown summary on disk and opening a GitHub issue so the numbers show up where you already work.

## 🎯 Quest Objectives

### Primary Objectives (Required for Quest Completion)
- [ ] Write a standalone Node script that queries GA and writes a Markdown digest
- [ ] Deliver it as a dated file **and** a GitHub issue
- [ ] Schedule it weekly with **launchd** (macOS) or **cron** (Linux)

### Secondary Objectives (Bonus Achievements)
- [ ] Filter the report to production traffic only
- [ ] Add a week-over-week comparison

### Mastery Indicators
- You know why a *cloud* scheduler can't reach a *local* key
- Your job uses absolute paths and a defined environment

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- Completed [Connect Google Analytics to Your AI Agent](/quests/1010/analytics-mcp-setup/)
- Node scripting and basic scheduling

### 🛠️ System Requirements
- Node.js 18+, the `gh` CLI authenticated, and a scheduler

## 🏗️ Chapter 1: A Self-Contained Digest Script

The script reads the **same service-account key** from `~/.config/gcloud/` (never the repo), queries GA, and writes Markdown. Keep it standalone so it doesn't depend on your agent being online.

```js
const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");
const { BetaAnalyticsDataClient } = require("@google-analytics/data");

const key = require(path.join(os.homedir(), ".config/gcloud/ga-reader.json"));
const client = new BetaAnalyticsDataClient({
  credentials: { client_email: key.client_email, private_key: key.private_key },
});
const property = "properties/" + process.env.GA_PROPERTY_ID;
const HOST = { filter: { fieldName: "hostName",
  stringFilter: { matchType: "EXACT", value: "your-site.dev" } } };

async function main() {
  const [r] = await client.runReport({
    property,
    dimensionFilter: HOST,
    dateRanges: [{ startDate: "7daysAgo", endDate: "today" }],
    metrics: [{ name: "activeUsers" }, { name: "sessions" }, { name: "screenPageViews" }],
  });
  const m = (r.rows?.[0]?.metricValues || []).map(v => v.value);
  const today = new Date().toISOString().slice(0, 10);
  const md = `# Weekly traffic — week ending ${today}\n\n` +
    `- Active users: ${m[0] ?? 0}\n- Sessions: ${m[1] ?? 0}\n- Page views: ${m[2] ?? 0}\n`;

  const dir = path.join(os.homedir(), "ga-reports");
  fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, `report-${today}.md`);
  fs.writeFileSync(file, md);

  // Deliver as a GitHub issue (gh must be authenticated)
  execFileSync("/opt/homebrew/bin/gh", ["issue", "create", "--repo", "you/your-repo",
    "--title", `Weekly traffic — ${today}`, "--body-file", file], { stdio: "inherit" });
}
main().catch(e => { console.error(e.message); process.exit(1); });
```

Install the one dependency locally (outside the repo) and test it once:

```bash
npm install --prefix ~/.local/share/ga-report @google-analytics/data
GA_PROPERTY_ID=123456789 node ~/.local/share/ga-report/ga-weekly-report.js
```

## ⏰ Chapter 2: Schedule It (macOS — launchd)

A LaunchAgent runs the script on a calendar interval. Use **absolute paths** — scheduled jobs don't inherit your interactive shell's PATH.

```xml
<!-- ~/Library/LaunchAgents/com.you.ga-weekly-report.plist -->
<dict>
  <key>Label</key><string>com.you.ga-weekly-report</string>
  <key>ProgramArguments</key>
  <array>
    <string>/opt/homebrew/bin/node</string>
    <string>/Users/you/.local/share/ga-report/ga-weekly-report.js</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key><string>/opt/homebrew/bin:/usr/bin:/bin</string>
    <key>GA_PROPERTY_ID</key><string>123456789</string>
  </dict>
  <key>StartCalendarInterval</key>
  <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>9</integer></dict>
</dict>
```

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.you.ga-weekly-report.plist
launchctl print gui/$(id -u)/com.you.ga-weekly-report | grep -i "state\|calendar"
```

### Linux — cron

```cron
# Mondays at 09:00 — note the absolute paths and env var
0 9 * * 1 GA_PROPERTY_ID=123456789 /usr/bin/node /home/you/.local/share/ga-report/ga-weekly-report.js
```

## ☁️ Chapter 3: Why Not a Cloud Scheduler?

It's tempting to run this as a hosted cron, but the script needs the **local service-account key file**. A cloud runner won't have `~/.config/gcloud/ga-reader.json`, so the job belongs on a machine that holds the key — a local launchd/cron job, or a CI runner with the key injected as a **secret** (never committed). Pick whichever matches where your key safely lives.

## ✅ Validation

- [ ] Running the script by hand writes a dated digest and opens an issue
- [ ] `launchctl print` (or `crontab -l`) shows the job registered
- [ ] The report contains production-only numbers

## 🏆 Rewards

- 🏆 **Automation Architect** — reporting now runs itself
- ⏰ **Scheduler Sage** — launchd/cron hold no mysteries

## 🎓 Path Complete

You've connected Google Analytics to your agent, learned to query it, and automated the reporting. Loop back to **[the series hub](/quests/1010/)** for more Monitoring & Observability quests — or read the full story in the post [Auditing Site Analytics & SEO with an AI Agent and MCP](/posts/ai-assisted-analytics-seo-audit/).
