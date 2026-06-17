---
title: 'Prometheus & Grafana: Metrics Collection and Visualization'
author: IT-Journey Team
description: 'Master the Prometheus data model, write PromQL queries, run exporters and scrape targets, and build Grafana dashboards from raw time series.'
excerpt: Collect metrics with Prometheus and visualize them in Grafana dashboards
preview: images/previews/prometheus-grafana-metrics-collection-quest-title.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1010'
difficulty: 🟡 Medium
estimated_time: 2-3 hours
primary_technology: prometheus
quest_type: main_quest
quest_series: Observability Mastery
quest_line: The Warrior's Watchtower
quest_arc: Eyes on the Realm
quest_dependencies:
  required_quests:
  - /quests/1010/monitoring-fundamentals/
  recommended_quests: []
  unlocks_quests:
  - /quests/1010/alerting-systems/
skill_focus: devops
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Completion of Monitoring Fundamentals (recommended)
  - Comfort with the command line and YAML
  - Familiarity with Docker basics
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Docker and Docker Compose installed
  - A terminal and a text editor or IDE (VS Code recommended)
  skill_level_indicators:
  - Comfortable running containers and editing config files
  - Ready to query time-series data
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A working Prometheus + Grafana stack scraping at least one exporter
  skill_demonstrations:
  - Can write PromQL using rate(), histogram_quantile(), and aggregation
  - Can build a Grafana dashboard panel from a PromQL query
  knowledge_checks:
  - Understands the pull-based scrape model
  - Can explain counters, gauges, and histograms
permalink: /quests/1010/prometheus-grafana/
categories:
- Quests
- DevOps
- Medium
tags:
- '1010'
- prometheus
- grafana
- promql
- main_quest
- devops
- hands-on
- gamified-learning
keywords:
  primary:
  - '1010'
  - prometheus
  - grafana
  secondary:
  - promql
  - exporters
  - dashboards
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1010 (10) Quest: Main Quest - Prometheus & Grafana'
rewards:
  badges:
  - 🏆 Metric Smith - Stood up a Prometheus scrape pipeline
  - 🛡️ Dashboard Artisan - Built a Grafana dashboard from PromQL
  skills_unlocked:
  - 🛠️ PromQL Query Writing
  - 🧠 Pull-Based Metrics Architecture
  progression_points: 80
  unlocks_features:
  - The ability to instrument and visualize any service in the realm
layout: quest
---
*Greetings, brave adventurer! You return to the **Watchtower** with the spyglass of theory in hand - now it is time to forge the instrument itself. In this quest you will raise **Prometheus**, the tireless scout who rides out every few seconds to gather numbers from across your realm, and **Grafana**, the cartographer who paints those numbers into living maps. Together they are the beating heart of the metrics pillar.*

*Whether you have only ever watched a dashboard built by someone else or you are ready to instrument your own services from scratch, this adventure will leave you fluent in PromQL and confident at the dashboard editor.*

## 📖 The Legend Behind This Quest

*Prometheus was born at SoundCloud and forged in the fires of the Cloud Native Computing Foundation, where it became the second project ever to graduate after Kubernetes itself. Its insight was simple and radical: instead of agents pushing data to a central server, a central server pulls metrics from targets on a schedule. This pull model, paired with a dimensional data model and a query language called PromQL, became the de facto standard for cloud-native metrics.*

*Grafana grew alongside it as the open-source window into those metrics. Master the two together and you hold the most widely deployed observability duo in the modern realm.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **The Prometheus Data Model** - Explain metric names, labels, samples, and the four metric types
- [ ] **PromQL** - Query time series with selectors, `rate()`, aggregation, and `histogram_quantile()`
- [ ] **Exporters and Scraping** - Configure a scrape job and read metrics from an exporter
- [ ] **Grafana Dashboards** - Build a panel from a PromQL query with thresholds and units

### Secondary Objectives (Bonus Achievements)
- [ ] **Recording Rules** - Pre-compute an expensive query for faster dashboards
- [ ] **Labels and Cardinality** - Choose labels that stay queryable without exploding storage
- [ ] **Service Discovery** - Understand how Prometheus finds targets dynamically

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain why Prometheus pulls instead of receiving pushes
- [ ] Write a PromQL query that returns the 95th percentile request latency
- [ ] Stand up the full stack with Docker Compose and reach a green target
- [ ] Build a Grafana panel that turns a counter into a per-second rate

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] The three pillars of observability (from Monitoring Fundamentals)
- [ ] Comfort editing YAML configuration files
- [ ] Basic Docker and container concepts

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Docker and Docker Compose installed
- [ ] A terminal and a text editor or IDE (VS Code recommended)

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You can run a container and edit a config file without hand-holding
- [ ] You are ready to think in time series and labels
- [ ] Ready for 2-3 hours of focused, hands-on learning

## 🌍 Choose Your Adventure Platform

*The fastest path is Docker Compose, which runs identically everywhere. Native installs are shown for those who want them.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install Docker Desktop, then use the Compose file below
brew install --cask docker

# Native binaries are also available via Homebrew if you prefer
brew install prometheus grafana
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install Docker Desktop
winget install Docker.DockerDesktop

# Then bring up the stack with the Compose file shown below
docker compose up -d
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Install Docker and Compose plugin
sudo apt update && sudo apt install -y docker.io docker-compose-v2
sudo systemctl enable --now docker

# Bring up the stack
sudo docker compose up -d
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# In any container runtime (Codespaces, a VM, a managed cluster) the same
# Compose file works. Forward ports 9090 (Prometheus) and 3000 (Grafana).
docker compose up -d
```

</details>

## 🧙‍♂️ Chapter 1: The Prometheus Data Model and a Running Stack

*Before you can query, you must understand the shape of the data and get the scout riding.*

### ⚔️ Skills You'll Forge in This Chapter
- Metric names, labels, and samples
- The four metric types
- Standing up Prometheus, Grafana, and an exporter

### 🏗️ The Data Model

Every Prometheus sample is a number attached to a metric name and a set of key-value labels, observed at a timestamp:

```text
http_requests_total{method="GET", handler="/checkout", status="200"} = 80421
metric name ─────────┘ └──────────────── labels ────────────────┘     value
```

The four metric types you must know:

- **Counter** - a number that only goes up (or resets to zero on restart), e.g. `http_requests_total`. Always query it with `rate()`, never raw.
- **Gauge** - a number that goes up and down, e.g. `node_memory_MemAvailable_bytes`.
- **Histogram** - bucketed observations plus `_sum` and `_count`, used to compute quantiles server-side.
- **Summary** - like a histogram but with client-side quantiles.

### Step 1: Bring Up the Stack

```yaml
# docker-compose.yml
services:
  prometheus:
    image: prom/prometheus:latest
    ports: ["9090:9090"]
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  node-exporter:
    image: prom/node-exporter:latest
    ports: ["9100:9100"]
  grafana:
    image: grafana/grafana:latest
    ports: ["3000:3000"]
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

```yaml
# prometheus.yml — tell the scout where to ride and how often
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["localhost:9090"]
  - job_name: node
    static_configs:
      - targets: ["node-exporter:9100"]
```

```bash
# Launch everything and confirm the targets are healthy
docker compose up -d
# Open http://localhost:9090/targets — both jobs should be "UP"
```

### 🔍 Knowledge Check: Data Model
- [ ] Why do you always wrap a counter in `rate()`?
- [ ] What is the difference between a histogram and a summary?
- [ ] What makes a target show as "DOWN" on the targets page?

### ⚡ Quick Wins and Checkpoints
- [ ] **Stack is up**: Prometheus, Grafana, and node-exporter are running
- [ ] **Targets green**: Both scrape jobs report "UP"

## 🧙‍♂️ Chapter 2: PromQL - The Language of Time Series

*PromQL is the incantation that turns a wall of raw samples into the answer to a single question.*

### ⚔️ Skills You'll Forge in This Chapter
- Selectors and label matchers
- `rate()`, aggregation, and `by`/`without`
- Computing latency percentiles from histograms

### 🏗️ PromQL in Practice

Select a metric and filter by label:

```promql
# All 5xx checkout requests
http_requests_total{service="checkout", status=~"5.."}
```

Turn a counter into a per-second rate over a 5-minute window:

```promql
# Requests per second over the last 5 minutes
rate(http_requests_total{service="checkout"}[5m])
```

Aggregate across instances, keeping the dimension you care about:

```promql
# Total request rate grouped by HTTP status code
sum by (status) (rate(http_requests_total{service="checkout"}[5m]))
```

Compute an error ratio (a perfect SLI):

```promql
sum(rate(http_requests_total{service="checkout", status=~"5.."}[5m]))
/
sum(rate(http_requests_total{service="checkout"}[5m]))
```

Compute the 95th percentile latency from a histogram:

```promql
histogram_quantile(
  0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket{service="checkout"}[5m]))
)
```

### 🔍 Knowledge Check: PromQL
- [ ] What does `[5m]` mean, and why is it required for `rate()`?
- [ ] Why use `sum by (le)` before `histogram_quantile()`?
- [ ] How would you find the top 5 noisiest endpoints by error rate?

## 🧙‍♂️ Chapter 3: Grafana Dashboards and Recording Rules

*Numbers become understanding only when a human can see them at a glance. Grafana is where the war-map comes alive.*

### ⚔️ Skills You'll Forge in This Chapter
- Connecting Grafana to Prometheus
- Building a panel from a PromQL query
- Pre-computing heavy queries with recording rules

### 🏗️ Build Your First Dashboard

1. Open Grafana at `http://localhost:3000` (login `admin` / `admin`).
2. Add a data source: **Connections → Data sources → Prometheus**, URL `http://prometheus:9090`.
3. Create a new dashboard, add a **Time series** panel, and paste a PromQL query:

```promql
# Panel query: request rate by status code
sum by (status) (rate(http_requests_total{service="checkout"}[5m]))
```

4. Set the unit to `requests/sec`, add a threshold so error series turn red, and save.

Heavy queries that many dashboards reuse should be pre-computed as **recording rules** so Grafana reads a cheap, ready-made series:

```yaml
# rules.yml — load via rule_files in prometheus.yml
groups:
  - name: checkout-slo
    interval: 30s
    rules:
      - record: job:checkout_request_errors:ratio_rate5m
        expr: |
          sum(rate(http_requests_total{service="checkout",status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total{service="checkout"}[5m]))
```

### 🔍 Knowledge Check: Grafana
- [ ] Why is `http://prometheus:9090` the right URL inside Docker Compose?
- [ ] When is a recording rule worth the extra config?
- [ ] How does a threshold help a human read a panel faster?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Reach a Green Target
**Objective**: Bring up the Compose stack and confirm both scrape jobs are healthy.

**Requirements**:
- [ ] Prometheus running at port 9090
- [ ] node-exporter scraped as a job named `node`
- [ ] Both targets show "UP" on the targets page

**Validation**: `curl -s http://localhost:9090/api/v1/targets` shows `"health":"up"` for both jobs.

### 🟡 Intermediate Challenge: Write Three PromQL Queries
**Objective**: Produce three working queries against your running stack.

**Requirements**:
- [ ] One `rate()` query over a counter
- [ ] One aggregation using `sum by (...)`
- [ ] One `histogram_quantile()` latency query

**Validation**: Each query returns data in the Prometheus expression browser.

### 🔴 Advanced Challenge: Build a Grafana SLO Panel
**Objective**: Build a dashboard panel showing the checkout error ratio against a 99.9% SLO line.

**Requirements**:
- [ ] A panel driven by an error-ratio PromQL query
- [ ] A threshold marking the SLO boundary
- [ ] A recording rule backing the query for performance

**Validation**: The panel renders, turns red when the ratio crosses the SLO, and reads from the recording rule.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Metric Smith** - You stood up a Prometheus scrape pipeline
- 🛡️ **Dashboard Artisan** - You built a Grafana dashboard from PromQL

**🛠️ Skills Unlocked**:
- **PromQL Query Writing** - Turn raw samples into answers
- **Pull-Based Metrics Architecture** - Design scrape pipelines

**🔓 Unlocked Quests**:
- Alerting Systems - Turn your PromQL into pages that matter

**📊 Progression Points**: +80 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Alerting Systems](/quests/1010/alerting-systems/) - Fire alerts from these very queries

**Explore Side Adventures**:
- ⚔️ [Distributed Tracing](/quests/1010/distributed-tracing/) - Add the traces pillar
- ⚔️ [ELK Stack](/quests/1010/elk-stack/) - Add the logs pillar

### Character Class Recommendations

**💻 Software Developer**: Continue to [Distributed Tracing](/quests/1010/distributed-tracing/)  
**🏗️ System Engineer**: Advance to [Alerting Systems](/quests/1010/alerting-systems/)  
**🛡️ Security Specialist**: Explore [ELK Stack](/quests/1010/elk-stack/)

## 📚 Resources

### Official Documentation
- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/) - The canonical reference
- [Querying with PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/) - Selectors, functions, operators
- [Grafana Documentation](https://grafana.com/docs/grafana/latest/) - Dashboards and data sources

### Community Resources
- [PromQL Cheat Sheet (PromLabs)](https://promlabs.com/promql-cheat-sheet/) - Quick reference
- [Prometheus Exporters and Integrations](https://prometheus.io/docs/instrumenting/exporters/) - The exporter catalog
- [Grafana Dashboards Library](https://grafana.com/grafana/dashboards/) - Importable community dashboards

### Learning Materials
- [Node Exporter on GitHub](https://github.com/prometheus/node_exporter) - The exporter used in this quest
- [Histograms and Summaries](https://prometheus.io/docs/practices/histograms/) - Quantile computation explained

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Stood up the Prometheus + Grafana stack
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1010 - Monitoring & Observability]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Monitoring Fundamentals: Metrics, Logs, and Traces for Observability]]
**Unlocks:** [[Alerting Systems: Alertmanager, Routing, and On-Call]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
