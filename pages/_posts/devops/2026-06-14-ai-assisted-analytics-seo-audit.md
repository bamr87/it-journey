---
title: 'Auditing Site Analytics & SEO with an AI Agent and MCP'
description: How an MCP-connected AI agent set up Google Analytics, found 85% of traffic was dev noise, fixed it at the source, and audited the site's crawlability.
date: '2026-06-14T18:00:00.000Z'
preview: /images/previews/ai-assisted-analytics-seo-audit.png
tags:
- google-analytics
- mcp
- claude-code
- seo
- jekyll
- devops
- ai-development
- observability
categories:
- Posts
- DevOps
- Tools & Environment
sub-title: A real session connecting Google Analytics over MCP, then cleaning the data and the crawl
excerpt: A connect-measure-fix story — wiring Google Analytics into an AI agent via MCP, discovering the numbers were mostly local-dev noise, and fixing both the data and the site's SEO.
snippet: The traffic spike was real. It was just us.
author: IT-Journey Team
section: DevOps
keywords:
- google-analytics-mcp
- service-account-security
- jekyll-analytics
- crawlability-audit
- bot-traffic-filtering
- automated-reporting
lastmod: '2026-06-14T18:00:00.000Z'
permalink: /posts/ai-assisted-analytics-seo-audit/
attachments: ''
comments: true
difficulty: 🟡 Intermediate
estimated_reading_time: 12-16 minutes
prerequisites:
- A site with Google Analytics 4 installed
- Basic Git, GitHub, and command-line familiarity
- Comfort reading Jekyll / Liquid templates
learning_outcomes:
- 🎯 Connect Google Analytics to an AI agent through an MCP server
- 🔐 Tell a service-account key from an OAuth client and keep secrets out of a public repo
- 📊 Diagnose polluted analytics with a hostname breakdown
- 🛠️ Gate analytics to production so dev traffic stops skewing the data
- 🔎 Audit crawlability: robots.txt, sitemaps, permalinks, and broken internal links
content_series: AI-Assisted DevOps
related_posts:
- /posts/prd-machine-self-writing-documentation/
validation_methods:
- Run a hostName breakdown in GA and confirm production vs dev split
- Verify the analytics tag does not fire on localhost
- Confirm clean URLs resolve and old duplicated URLs redirect
draft: false
---

> **TL;DR** — We connected Google Analytics to an AI coding agent over MCP, asked it to "analyze the traffic," and learned that ~85% of our sessions were *us* — `localhost`, Docker, and CI hitting the site during development. Fixing that exposed the real numbers, which pointed straight at an SEO problem: duplicated URLs and hundreds of broken internal links. Here's the whole journey, including the parts that went sideways.

## The goal: stop guessing about traffic

IT-Journey has had Google Analytics 4 wired up for a while (`G-ZBDKNMC168`), but nobody was actually *looking* at it. The idea was simple: connect GA to [Claude Code](https://claude.com/claude-code) through an **MCP server** so the agent could pull traffic data on demand and help prioritize content.

[Model Context Protocol (MCP)](https://modelcontextprotocol.io) servers are how an AI agent gets new tools. The [`mcp-server-google-analytics`](https://github.com/ruchernchong/mcp-server-google-analytics) package wraps the **Google Analytics Data API** and exposes tools like `runReport`, `getPageViews`, and `getActiveUsers`. To run it you need three things:

- `GA_PROPERTY_ID` — the **numeric** property ID (e.g. `314278834`), *not* the `G-…` measurement ID
- `GOOGLE_CLIENT_EMAIL` + `GOOGLE_PRIVATE_KEY` — from a Google Cloud **service account** with the Analytics Data API enabled and **Viewer** access on the GA4 property

## Gotcha #1: a service account is not an OAuth client

The first credential handed over was a `client_secret_….apps.googleusercontent.com.json` file — an **OAuth 2.0 web client**, not a service account. They look similar but they're different beasts:

| | OAuth client | Service account |
|---|---|---|
| Top-level key | `web` / `installed` | `type: service_account` |
| Auth style | interactive browser redirect | server-to-server JWT |
| Has `private_key`? | no | yes |

The MCP server needs the **service account** (JWT) flow. In Google Cloud that means **IAM & Admin → Service Accounts → Create**, then **Keys → Add key → JSON**, then granting that service account's email **Viewer** in GA's **Property Access Management**.

## Gotcha #2: secrets in a public repo

Both credential files were saved straight into the repository root — a **public** repo. They were never committed (verified with `git log --all`), so nothing leaked, but they were one `git add .` away from disaster. The fixes:

```bash
# Belt: a local, never-committed ignore for the main checkout
printf '%s\n' 'client_secret_*.json' '*.apps.googleusercontent.com.json' \
  '*service-account*.json' >> .git/info/exclude

# Suspenders: patterns in .gitignore so the protection is permanent
```

Then the service-account key was moved out of the repo entirely to `~/.config/gcloud/` with `chmod 600`. Lesson: **credentials never belong inside a repo directory** — gitignore is a safety net, not a storage location.

With the key relocated, the server registered cleanly:

```bash
claude mcp add google-analytics --scope user \
  -e GOOGLE_CLIENT_EMAIL="$(node -p "require('$KEY').client_email")" \
  -e GOOGLE_PRIVATE_KEY="$(node -p "require('$KEY').private_key")" \
  -e GA_PROPERTY_ID="314278834" \
  -- npx -y mcp-server-google-analytics
```

A live test query returned **18,943 active users in the last 28 days, up 304%**. 🎉

Except… that number was a lie.

## The plot twist: 85% of "traffic" was us

A 304% spike with a *collapsing* engagement rate (3%, down from 7%) and 10-second sessions is a classic tell. The smoking gun was the **`hostName` dimension**:

| Hostname | Sessions | What it is |
|---|---:|---|
| `127.0.0.1` | 15,415 | local `jekyll serve` |
| `it-journey.dev` | 1,765 | ✅ real production |
| `localhost` | 471 | local dev |
| `host.docker.internal` | 308 | local Docker |
| `zer0-mistakes.com` | 251 | another site reusing the same tag |

Roughly **85% of sessions were development traffic**, plus the GA tag was shared across several sibling sites. Corroborating signals all lined up: 99% Direct, 99% Chrome/desktop, datacenter "cities." **Real** production traffic was ~1,765 sessions in 28 days — about 63/day, not thousands.

> The lesson that kept repeating: *a connected data source is not a trustworthy one.* The first real win from analytics was discovering the analytics were wrong.

## Fixing it at the source

The root cause lived in the Jekyll theme: the analytics include fired on **every** build, with no environment guard. The fix is the canonical Jekyll pattern plus a belt-and-suspenders hostname check:

```liquid
{% raw %}{% if jekyll.environment == "production" %}
  {% include analytics/google-analytics.html %}
{% endif %}{% endraw %}
```

```js
// Inside the include: skip dev hostnames even in a prod-env Docker/CI preview
var h = location.hostname;
if (h === 'localhost' || h === '127.0.0.1' || h === 'host.docker.internal' ||
    h.endsWith('.local') || h.endsWith('.test')) return;
```

`jekyll serve` runs in `development`, so the tag never loads locally; GitHub Pages builds with `JEKYLL_ENV=production`, so real visits still count.

## Automating the part nobody does

Dashboards you have to remember to open don't get opened. So the report became a tiny standalone script (reading the same service-account key) wired to a weekly **launchd** job that writes a dated Markdown digest *and* opens a GitHub issue. No dependency on the agent being online — just `node ga-weekly-report.js` on a schedule, filtered to `hostName == it-journey.dev` so it only ever reports real traffic.

## Then the real numbers pointed at SEO

With clean data, the story changed. Organic search was tiny (~316 sessions/90d) but **engaged at 41%** — and the top organic landing pages were quests and wargame walkthroughs. So the agent ran a crawlability audit, and it found real problems:

- **Duplicated URLs.** A collection permalink of `/:collection/:path/:name/` repeated the filename, producing `/notes/slug/slug/`. (`:path` already ends in the filename, so `:name` is redundant.)
- **436 broken `.md` links** across 51 files. The `jekyll-relative-links` plugin was enabled but defaults to `collections: false`, so it silently skipped `_quests`/`_notes`/`_docs`/`_posts` — leaving `[text](file.md)` links as dead URLs.
- **Indexable junk**: internal planning docs (`PRD.md`, `QUEST_BUILD_PLAN.md`) being crawled and ranked.

The fixes were small and surgical: change the permalink to `/:collection/:path/`, set `relative_links.collections: true`, and `published: false` the planning docs. A generic redirect in `404.html` (`/x/y/y/` → `/x/y/`) preserved any already-indexed duplicate URLs without cluttering 34 files with `redirect_from` frontmatter.

## Workflow lessons (the unglamorous ones)

- **Verify before you "fix."** The live `robots.txt` didn't match the repo's — but checking revealed the branch had *already* fixed it; main just hadn't deployed. Nearly fixed a non-bug.
- **Mind your worktree.** Edits made with absolute paths landed in the main checkout's branch instead of the intended worktree. Always confirm `git branch --show-current` for the path you're editing.
- **Let CI be the build oracle.** The local environment couldn't build (wrong Ruby), so the authoritative check was the **Jekyll Build Test** on a clean PR — which is exactly what a PR is for.

## Takeaways

1. **Connected ≠ trustworthy.** Segment by hostname before believing a single GA number.
2. **Gate analytics to production.** One `{% raw %}{% if jekyll.environment %}{% endraw %}` saves you from measuring yourself.
3. **Keep secrets out of repos** — and know your credential types.
4. **Crawlability is plumbing.** Duplicated URLs and broken internal links quietly cap your organic reach.

Want the hands-on version? This whole journey is broken into a quest series under **[Level 1010 · Monitoring & Observability](/quests/1010/)** — start with [Connect Analytics to Your AI Agent](/quests/1010/analytics-mcp-setup/).
