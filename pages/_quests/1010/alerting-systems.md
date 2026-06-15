---
title: 'Alerting Systems: Alertmanager, Routing, On-Call & Runbooks'
author: IT-Journey Team
description: Build production alerting with Prometheus alert rules and Alertmanager. Learn routing, grouping, silencing, inhibition, escalation, on-call schedules, and runbook-driven response.
excerpt: Turn signals into actionable pages with alert rules, Alertmanager routing, on-call, and runbooks
preview: images/previews/alerting-systems-pagerduty-quest-title-incident-ma.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1010'
difficulty: 🔴 Hard
estimated_time: 75-90 minutes
primary_technology: alertmanager
quest_type: main_quest
quest_series: Observability Mastery
quest_line: The Warrior's Watchtower
quest_arc: From Signal to Response
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/1010/monitoring-fundamentals/
  unlocks_quests:
  - /quests/1011/security-fundamentals/
skill_focus: devops
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Comfort on the command line and reading YAML
  - SLIs, SLOs, and error budgets from Monitoring Fundamentals
  - Basic PromQL or willingness to read the examples carefully
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Docker and Docker Compose for the Prometheus + Alertmanager lab
  - A terminal and a text editor or IDE (VS Code recommended)
  skill_level_indicators:
  - Can run a small monitoring stack and read a dashboard
  - Ready to design alerts humans will actually trust at 3 a.m.
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A firing alert routed and silenced through Alertmanager
  skill_demonstrations:
  - Can write a Prometheus alert rule with for, labels, and annotations
  - Can configure Alertmanager routing, grouping, and a silence
  knowledge_checks:
  - Understands grouping, inhibition, and silencing
  - Can explain what makes an alert actionable and runbook-ready
permalink: /quests/1010/alerting-systems/
categories:
- Quests
- DevOps
- Hard
tags:
- '1010'
- alertmanager
- prometheus
- on-call
- main_quest
- devops
- hands-on
keywords:
  primary:
  - '1010'
  - alertmanager
  - prometheus
  secondary:
  - alert-routing
  - on-call
  - runbooks
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1010 (10) Quest: Main Quest - Alerting Systems'
rewards:
  badges:
  - 🏆 Warden of the Pager - Built alerts humans actually trust
  - 🔔 Master of the Routing - Tamed grouping, silencing, and escalation
  skills_unlocked:
  - 🛠️ Alert Rule & Alertmanager Configuration
  - 🧠 On-Call and Runbook-Driven Incident Response
  progression_points: 75
  unlocks_features:
  - Completes the Level 1010 Monitoring & Observability quest line
layout: quest
---
*Greetings, brave adventurer! From the **Watchtower** you have learned to see fires - in metrics, in logs, in traces. But sight alone does not save a kingdom; someone must be **woken** when the fire is real, and *not* woken for every harmless spark. This final quest of the Watchtower, **Alerting Systems**, teaches you to forge the signal-horn: alert rules that fire only on what matters, routing that wakes the right defender, and runbooks that tell them exactly what to do when the horn sounds.*

*Whether you have been paged at 3 a.m. for a problem that fixed itself, or you have watched a real outage go unnoticed because the alert was buried in noise, this adventure forges the discipline every on-call Warrior needs: actionable alert rules, Alertmanager routing, grouping and silencing, escalation, and the humble, life-saving runbook.*

## 📖 The Legend Behind This Quest

*In the early ages, an operator watched a dashboard with their own eyes and shouted when something broke. That does not scale past one tired human. The kingdoms that survived learned a hard truth: an alert that does not demand action is **noise**, and noise trains defenders to ignore the very horn that should save them. This is alert fatigue, and it has caused more outages than any single bug.*

*Good alerting is therefore as much about **what you do not alert on** as what you do. This quest teaches you to wire Prometheus alert rules into Alertmanager, route each alert to the right receiver, silence the expected, suppress the redundant, and attach a runbook so the person you wake knows precisely what to do.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Alert Rules** - Write a Prometheus alerting rule with `expr`, `for`, `labels`, and `annotations`
- [ ] **Alertmanager Routing** - Route alerts to receivers by label, with grouping to batch related alerts
- [ ] **Silencing & Inhibition** - Mute expected alerts and suppress redundant ones during an outage
- [ ] **On-Call & Runbooks** - Connect alerts to escalation and to a runbook the responder can follow

### Secondary Objectives (Bonus Achievements)
- [ ] **Symptom-Based Alerting** - Alert on user-visible symptoms, not raw resource causes
- [ ] **Burn-Rate Alerts** - Tie pages to error-budget burn so they fire only when it matters
- [ ] **Escalation Policies** - Page a secondary responder when the primary does not acknowledge

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Write an alert rule that fires only after a condition holds for several minutes
- [ ] Route a `severity: page` alert to on-call and a `severity: ticket` alert elsewhere
- [ ] Create a silence so a planned maintenance window stays quiet
- [ ] Explain why every page must link to a runbook

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] SLIs, SLOs, and error budgets (complete [Monitoring Fundamentals](/quests/1010/monitoring-fundamentals/) first)
- [ ] Comfort reading and writing YAML
- [ ] Basic PromQL, or willingness to read the worked examples carefully

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Docker and Docker Compose installed
- [ ] A terminal and a text editor or IDE (VS Code recommended)

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can run a small monitoring stack and read a dashboard
- [ ] You are ready to design alerts a human will trust at 3 a.m.
- [ ] Ready for 75-90 minutes of focused, hands-on building

## 🌍 Choose Your Adventure Platform

*Prometheus and Alertmanager run in containers everywhere; only Docker installation differs. Then everyone meets at the same `docker compose up`.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
brew install --cask docker
docker --version && docker compose version
# Bring up the lab (compose file below), then open the UIs:
open http://localhost:9090   # Prometheus
open http://localhost:9093   # Alertmanager
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
winget install Docker.DockerDesktop
docker --version; docker compose version
start http://localhost:9090   # Prometheus
start http://localhost:9093   # Alertmanager
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
sudo systemctl enable --now docker
xdg-open http://localhost:9090   # Prometheus
xdg-open http://localhost:9093   # Alertmanager
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# In a Codespace or container host, run the same compose file and forward
# ports 9090 (Prometheus) and 9093 (Alertmanager) to your browser.
docker compose up -d
```

</details>

## 🧙‍♂️ Chapter 1: Anatomy of a Good Alert Rule

*An alert begins as a question asked of your metrics, every few seconds: "is this still true?" Learn to phrase that question so it fires on real problems and stays quiet otherwise.*

### ⚔️ Skills You'll Forge in This Chapter
- The four parts of a Prometheus alerting rule
- Why `for:` prevents flapping
- Symptom-based versus cause-based alerting

### 🏗️ The Four Parts of a Rule

```yaml
# rules.yml — a symptom-based alert wired into Prometheus
groups:
  - name: checkout-slos
    rules:
      - alert: CheckoutHighErrorRate
        expr: |
          sum(rate(http_requests_total{service="checkout",status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total{service="checkout"}[5m]))
          > 0.05
        for: 5m                       # condition must hold 5m before firing (anti-flap)
        labels:
          severity: page              # routing key Alertmanager uses
          team: payments
        annotations:
          summary: "Checkout 5xx error rate above 5%"
          description: "{% raw %}{{ $value | humanizePercentage }}{% endraw %} of checkout requests are failing."
          runbook_url: "https://runbooks.example.com/checkout-5xx"
```

- **`expr`** - the PromQL condition; when it returns results, the alert is *pending*.
- **`for`** - how long the condition must persist before *firing*. This single line kills most flapping.
- **`labels`** - metadata Alertmanager routes on (`severity`, `team`).
- **`annotations`** - human-facing text, including the all-important `runbook_url`.

> **Alert on symptoms, not causes.** Page on "checkout error rate above 5%" (a user feels this), not "CPU at 80%" (a clue, not a problem). Users never notice your CPU; they notice failed checkouts.

### 🔍 Knowledge Check: Alert Rules
- [ ] What does the `for:` clause prevent?
- [ ] Why route on `labels` rather than the alert name?
- [ ] Why is "5xx rate above 5%" a better page than "CPU above 80%"?

### ⚡ Quick Wins and Checkpoints
- [ ] **Wrote a rule**: You can name `expr`, `for`, `labels`, `annotations`
- [ ] **Chose a symptom**: You picked a user-visible condition to alert on

## 🧙‍♂️ Chapter 2: Routing, Grouping, and Receivers with Alertmanager

*Prometheus decides *when* an alert fires; **Alertmanager** decides *who hears it and how*. Its routing tree sends each alert to the right receiver, grouped so one incident is one notification, not fifty.*

### ⚔️ Skills You'll Forge in This Chapter
- The Alertmanager routing tree
- Grouping related alerts into a single notification
- Configuring receivers (email, Slack, PagerDuty)

### 🏗️ A Routing Configuration

```yaml
# alertmanager.yml — route by label, group related alerts, wire receivers
route:
  receiver: default-email           # catch-all
  group_by: ['alertname', 'service'] # one notification per service incident
  group_wait: 30s                    # wait to batch alerts that fire together
  group_interval: 5m
  repeat_interval: 4h                # re-notify if still firing after 4h
  routes:
    - matchers: [ 'severity = page' ] # pages go to on-call (e.g. PagerDuty)
      receiver: oncall-pagerduty
    - matchers: [ 'severity = ticket' ]
      receiver: ticket-slack

receivers:
  - name: default-email
    email_configs:
      - to: 'ops@example.com'
  - name: oncall-pagerduty
    pagerduty_configs:
      - service_key: '<integration-key>'
  - name: ticket-slack
    slack_configs:
      - channel: '#alerts-tickets'
        api_url: '<webhook-url>'
```

**Grouping** is the unsung hero: if a database fails and twenty services error at once, `group_by` collapses them into *one* notification instead of twenty pages. `group_wait` gives related alerts a moment to arrive together.

### 🔍 Knowledge Check: Routing and Grouping
- [ ] How does Alertmanager decide which receiver an alert goes to?
- [ ] What problem does `group_by` solve during a large outage?
- [ ] What does `repeat_interval` control?

## 🧙‍♂️ Chapter 3: Silencing and Inhibition

*Not every firing alert deserves a page. **Silencing** mutes alerts you already know about; **inhibition** suppresses lesser alerts when a bigger one is already firing.*

### ⚔️ Skills You'll Forge in This Chapter
- Creating time-boxed silences
- Writing inhibition rules
- Keeping the on-call experience signal-rich

### 🏗️ Silencing for Planned Work

A **silence** is a label-matched mute with an expiry - perfect for maintenance windows. Create one from the CLI:

```bash
# Silence all checkout alerts for a 2-hour maintenance window
amtool silence add \
  service=checkout \
  --duration=2h \
  --comment="Planned checkout DB migration — see CHG-4821" \
  --author="oncall@example.com"

# List and later expire active silences
amtool silence query
amtool silence expire <silence-id>
```

### 🏗️ Inhibition: Suppress the Redundant

When an entire datacenter is down, you do not also want a page for every service inside it. **Inhibition** says "if the big alert is firing, mute the small ones it implies":

```yaml
# alertmanager.yml — suppress per-service alerts when the cluster is down
inhibit_rules:
  - source_matchers: [ 'alertname = ClusterDown' ]   # if this fires...
    target_matchers: [ 'severity = page' ]            # ...mute these
    equal: ['cluster']                                # ...for the same cluster
```

Together, silencing (you act ahead of time) and inhibition (Alertmanager acts automatically) keep the pager meaningful.

### 🔍 Knowledge Check: Silencing and Inhibition
- [ ] When would you create a silence rather than edit a rule?
- [ ] What does inhibition prevent during a large, cascading failure?
- [ ] Why should every silence have an expiry and a comment?

## 🧙‍♂️ Chapter 4: On-Call, Escalation, and Runbooks

*An alert is only as useful as the human response behind it. On-call schedules decide who is woken; escalation ensures someone *is* woken; runbooks ensure they know what to do.*

### ⚔️ Skills You'll Forge in This Chapter
- On-call rotations and escalation policies
- Writing a runbook a half-asleep responder can follow
- Closing the loop with postmortems

### 🏗️ Escalation Policies

An **escalation policy** defines what happens if the first responder does not acknowledge:

```text
Escalation policy: payments-oncall
  Level 1: page primary on-call         -> wait 5 min for ack
  Level 2: page secondary on-call       -> wait 5 min for ack
  Level 3: page engineering manager + open an incident bridge
```

This guarantees that a missed page does not become a missed outage. Alertmanager's `severity = page` route feeds an incident tool (PagerDuty, Opsgenie) that runs this policy.

### 🏗️ The Runbook

Every paging alert must link a **runbook** via `runbook_url`. A good runbook is short, specific, and written for 3 a.m.:

```markdown
# Runbook: CheckoutHighErrorRate

## What this means
Checkout is returning 5xx to real users. Revenue is impacted right now.

## First checks (in order)
1. Open the checkout dashboard: <link>. Is the spike still climbing?
2. Check the payment-gateway status page: <link>. Provider outage?
3. Check recent deploys: `kubectl rollout history deploy/checkout`.

## Likely fixes
- Bad deploy in the last 30 min  -> `kubectl rollout undo deploy/checkout`
- Provider outage                -> flip to backup processor (feature flag PAY_FALLBACK)

## If unresolved in 15 min
Escalate to Level 2 and open an incident. Page #incident-bridge.
```

A runbook turns a panicked guess into a checklist. After the incident, a blameless postmortem feeds improvements back into both the rule and the runbook - closing the loop.

### 🔍 Knowledge Check: On-Call and Runbooks
- [ ] What does an escalation policy guarantee that a single page cannot?
- [ ] What three things make a runbook usable at 3 a.m.?
- [ ] How does a postmortem improve future alerting?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Fire Your First Alert
**Objective**: Write a Prometheus alert rule that fires when a target is down, and watch it reach Alertmanager.

**Requirements**:
- [ ] A rule using `up == 0` with a `for:` clause and a `severity` label
- [ ] The alert moves from pending to firing in the Prometheus UI
- [ ] The firing alert appears in the Alertmanager UI

**Validation**: Stop a scrape target and see the alert fire end to end.

### 🟡 Intermediate Challenge: Route and Silence
**Objective**: Route `severity: page` and `severity: ticket` to different receivers, then silence one during "maintenance."

**Requirements**:
- [ ] Two routes sending to two receivers based on `severity`
- [ ] Grouping configured so related alerts batch into one notification
- [ ] A time-boxed silence that mutes the page during a window

**Validation**: The page is suppressed while the silence is active and resumes after it expires.

### 🔴 Advanced Challenge: Symptom-Based, Runbook-Ready Page
**Objective**: Build a burn-rate or error-rate alert that fires on a user-visible symptom and links a runbook.

**Requirements**:
- [ ] The `expr` is a symptom (error rate / budget burn), not a resource threshold
- [ ] The alert carries `severity`, `team`, and a `runbook_url`
- [ ] An inhibition rule prevents a flood when a parent alert is already firing

**Validation**: A reviewer agrees the page is actionable, deduplicated, and would not fire on harmless blips.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Warden of the Pager** - You built alerts humans actually trust
- 🔔 **Master of the Routing** - You tamed grouping, silencing, and escalation

**🛠️ Skills Unlocked**:
- **Alert Rule & Alertmanager Configuration** - Fire, route, group, and mute with intent
- **On-Call and Runbook-Driven Incident Response** - Wake the right person with the right plan

**🔓 Unlocked Quests**:
- Security Fundamentals - Begin the Warrior tier's next bastion, Security & Compliance

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Security Fundamentals](/quests/1011/security-fundamentals/) - Cross into the Security & Compliance tier

**Explore Side Adventures**:
- ⚔️ [Distributed Tracing](/quests/1010/distributed-tracing/) - Use traces to enrich incident response
- ⚔️ [ELK Stack](/quests/1010/elk-stack/) - Correlate alerts with the logs behind them

### Character Class Recommendations

**💻 Software Developer**: Continue to [Security Fundamentals](/quests/1011/security-fundamentals/)  
**🏗️ System Engineer**: Revisit [Monitoring Fundamentals](/quests/1010/monitoring-fundamentals/) to tighten SLOs  
**🛡️ Security Specialist**: Advance to [Security Fundamentals](/quests/1011/security-fundamentals/)

## 📚 Resources

### Official Documentation
- [Prometheus Alerting Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/) - `expr`, `for`, labels, annotations
- [Alertmanager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/) - Routing, grouping, silencing, inhibition
- [amtool](https://github.com/prometheus/alertmanager#amtool) - The Alertmanager CLI used for silences
- [PagerDuty Integration Guide](https://www.pagerduty.com/docs/guides/prometheus-integration-guide/) - Wiring Alertmanager to on-call

### Community Resources
- [Google SRE Book - Being On-Call](https://sre.google/sre-book/being-on-call/) - The on-call chapter
- [My Philosophy on Alerting (Rob Ewaschuk)](https://docs.google.com/document/d/199PqyG3UsyXlwieHaqbGiWVa8eMWi8zzAn0YfcApr8Q/edit) - The classic essay on actionable alerts
- [Awesome SRE](https://github.com/dastergon/awesome-sre) - Curated reliability resources

### Learning Materials
- [Multi-Window, Multi-Burn-Rate Alerts (SRE Workbook)](https://sre.google/workbook/alerting-on-slos/) - Budget-aware alerting in depth
- [Writing Runbooks](https://www.atlassian.com/incident-management/devops/runbooks) - How to write an actionable runbook

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Wrote and fired a Prometheus alert rule
- [ ] ✅ Configured Alertmanager routing and grouping
- [ ] ✅ Created a silence and an inhibition rule
- [ ] ✅ Linked a paging alert to a runbook
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1010 - Monitoring & Observability]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Requires:** [[Monitoring Fundamentals: Metrics, Logs, and Traces for Observability]]
**Unlocks:** [[Security Fundamentals: CIA Triad and Defense in Depth Strategies]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
