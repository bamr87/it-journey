---
title: GH-600 Week-by-Week Learning Path
description: A structured 6-week study schedule for GH-600 with daily objectives, time estimates, and prerequisites.
permalink: /docs/certifications/gh-600/learning-path/
layout: default
categories:
- Docs
- Certifications
- Agentic-AI
tags:
- gh-600
- agentic-ai
- learning-path
- study-plan
author: IT-Journey Team
draft: false
lastmod: '2026-05-17T00:00:00.000Z'
date: '2026-05-17T00:00:00.000Z'
toc: true
toc_sticky: true
keywords:
- gh-600
- agentic-ai
- learning-path
- study-plan
- docs
- certifications
- week-by-week
- learning
---
# GH-600 Week-by-Week Learning Path

*The Scrollmaster's Prescribed Curriculum — for those who prefer a map over wandering.*

**Total estimated time:** ~40 hours over 6 weeks (~7 hours/week)  
**Assumed background:** Comfortable with GitHub Actions, basic Python or JS, VS Code, and basic AI-tool usage.

> **Choose your pace:** [6-week standard track](#week-1) (default) · [2-week sprint](#two-week-sprint) (experience required) · [micro-learning track](#micro-learning-15-minday) (busy schedules)

---

## Before You Begin

1. Read the [Skills Measured breakdown](../skills-measured/) and mark which sub-skills you already know.
2. Skim the [Recommended Resources](../recommended-resources/) list.
3. Set up your sandbox: clone this repo and run `./work/gh-600/setup.sh` to get the starter kit.
4. Ensure you have a GitHub account with Copilot access (free trial is fine for most quests).

---

## Week 1 — Domain 1: Agent Architecture & SDLC (≈7 hrs)

**Goal:** Understand what an agent is in the SDLC, how planning differs from action, and how to make agent behavior observable.

| Day | Activity | Time |
|---|---|---|
| Mon | Read [Skills Measured — Domain 1](../skills-measured/#domain-1) · Skim [Copilot coding agent docs](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-for-pull-requests/about-copilot-coding-agent) | 1 hr |
| Tue | Complete **Q1: Initiation Rites** — SDLC Integration | 90 min |
| Wed | Complete **Q2: The Three Sigils** — Plan vs. Action Boundaries | 90 min |
| Thu | Complete **Q3: The All-Seeing Eye** — Observability & Control | 90 min |
| Fri | Write a 1-page reflection: anti-patterns you've seen in your own AI usage; review [Domain 1 chronicle post](/posts/embedding-agents-in-the-sdlc/) | 30 min |

---

## Week 2 — Domain 2: Tool Use & Environment Interaction (≈8 hrs)

**Goal:** Configure and operate agents with real tools — including spinning up an MCP server and integrating into a CI workflow.

| Day | Activity | Time |
|---|---|---|
| Mon | Read [MCP Quick Reference](/notes/gh-600/mcp-quickref/) · Skim [MCP specification](https://modelcontextprotocol.io/) | 1 hr |
| Tue | Complete **Q4: Forging the Arsenal** — Tool Selection & Permissions | 90 min |
| Wed | Complete **Q5: The MCP Conclave** — MCP Server Mastery | 2 hrs |
| Thu | Complete **Q6: Bind the Realm** — Dev Environment Integration | 2 hrs |
| Fri | Complete **Q7: The Shield of Retries** — Safe Execution & Error Handling | 2 hrs |

---

## Week 3 — Domain 3: Memory, State & Execution (≈5 hrs)

**Goal:** Design durable agent memory strategies and detect/correct context drift.

| Day | Activity | Time |
|---|---|---|
| Mon | Read [Skills Measured — Domain 3](../skills-measured/#domain-3) | 30 min |
| Tue | Complete **Q8: Vaults of Recollection** — Memory Strategies | 90 min |
| Wed | Complete **Q9: Anchoring the Drifting Agent** — State Persistence & Drift | 90 min |
| Thu | Complete **Q10: Crossing the Tool Planes** — State Continuity Cross-Tools | 90 min |
| Fri | Review [Taming Agent Memory post](/posts/taming-agent-memory-and-context-drift/) | 30 min |

---

## Week 4 — Domain 4: Evaluation, Error Analysis & Tuning (≈6 hrs)

**Goal:** Define testable success criteria, read agent failure traces, and tune instructions/tools based on evidence.

| Day | Activity | Time |
|---|---|---|
| Mon | Read [Evaluation Signals Table](/notes/gh-600/evaluation-signals-table/) | 30 min |
| Tue | Complete **Q11: The Oracle's Rubric** — Success Criteria & Signals | 90 min |
| Wed | Complete **Q12: The Necromancer's Inquest** — Failure Root Cause Analysis | 90 min |
| Thu | Complete **Q13: Reforging the Agent's Mind** — Behavior Tuning | 2 hrs |
| Fri | Review [Evaluation post](/posts/evaluating-and-tuning-agents-with-github-signals/) | 30 min |

---

## Week 5 — Domain 5: Multi-Agent Coordination (≈7 hrs)

**Goal:** Orchestrate parallel agents, capture audit trails, recover from failures, and manage agent lifecycles.

| Day | Activity | Time |
|---|---|---|
| Mon | Read [Skills Measured — Domain 5](../skills-measured/#domain-5) | 30 min |
| Tue | Complete **Q14: The Council of Many** — Orchestration Patterns | 2 hrs |
| Wed | Complete **Q15: The Scribe's Codex** — Multi-Agent Observability | 90 min |
| Thu | Complete **Q16: When Familiars Fall** — Failure & Recovery | 90 min |
| Fri | Complete **Q17: The Agent Pantheon** — Lifecycle Management | 2 hrs |

---

## Week 6 — Domain 6 & Capstone (≈7 hrs)

**Goal:** Apply Responsible AI policy, classify risk, implement HITL gates, then prove mastery in the capstone.

| Day | Activity | Time |
|---|---|---|
| Mon | Read [Autonomy Levels Matrix](/notes/gh-600/autonomy-levels-matrix/) | 30 min |
| Tue | Complete **Q18: The Autonomy Scales** — Autonomy Levels Matrix | 90 min |
| Wed | Complete **Q19: The Warden's Pact** — Guardrails & HITL | 2 hrs |
| Thu | Review [Skills Checklist](/notes/gh-600/skills-checklist/) — mark every box | 30 min |
| Fri–Sat | Complete **🏆 Capstone: Trial of the Agentic Codex** (includes 50-question self-assessment) | 4 hrs |

---

## Exam Day Checklist

- [ ] All 19 quests completed and validated
- [ ] Skills Checklist: every box ticked
- [ ] Capstone self-assessment score ≥ 80%
- [ ] Reviewed [Glossary](/notes/gh-600/glossary/) the night before
- [ ] Rested, fed, and ready
- [ ] [Schedule your exam at Pearson VUE](https://learn.microsoft.com/en-us/credentials/certifications/exam-gh-600)

---

## 2-Week Sprint

*For experienced GitHub Copilot users who already understand agent concepts and need structured exam preparation rather than a full learning journey.*

**Prerequisites:** Active GitHub Copilot usage, familiarity with GitHub Actions, and basic awareness of LLM concepts. Complete the [Skills Checklist](/notes/gh-600/skills-checklist/) self-assessment first — aim to already pass ≥60% before starting the sprint.

**Total time:** ~20 hours over 14 days

| Day | Focus | Activities | Time |
|---|---|---|---|
| 1 | Domains 1–2 overview | Skim [Skills Measured](../skills-measured/) + Q1 + Q2 | 3 hrs |
| 2 | Domain 2 tools | Q4 + Q5 (MCP) | 3 hrs |
| 3 | Domain 2 deep dive | Q6 + Q7 | 3 hrs |
| 4 | Domain 3 memory | Q8 + Q9 + Q10 | 3 hrs |
| 5 | Domain 4 eval | Q11 + Q12 | 2 hrs |
| 6 | Domain 4 tuning | Q13 + review D4 chronicle post | 2 hrs |
| 7 | **Rest day** — light review of [Glossary](/notes/gh-600/glossary/) | 30 min |
| 8 | Domain 5 part 1 | Q14 + Q15 | 3 hrs |
| 9 | Domain 5 part 2 | Q16 + Q17 | 3 hrs |
| 10 | Domain 6 | Q18 + Q19 | 3 hrs |
| 11 | Weaknesses | Re-do quests where you scored below 80% | 2 hrs |
| 12 | Reference pass | Read all 7 [Quick-Reference Notes](/notes/gh-600/) | 1 hr |
| 13 | Capstone attempt | Full capstone — identify gaps | 4 hrs |
| 14 | Final review | Gaps from capstone + [Skills Checklist](/notes/gh-600/skills-checklist/) | 2 hrs |

---

## Micro-Learning (15 min/day)

*For those with demanding schedules who can only commit to short, daily sessions. Completion time: ~3 months at 5 days/week.*

**How it works:** Each 15-minute session is a single, self-contained activity. Sessions build sequentially — do not skip. Mark each checkbox as you go.

### Phase 1 — Orientation (Days 1–10)

| Day | Session |
|---|---|
| 1 | Read [Exam at a Glance](/docs/certifications/gh-600/) (the hub table) |
| 2 | Read [Domain 1 Skills Measured](../skills-measured/#domain-1) |
| 3 | Skim [Copilot coding agent docs](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-for-pull-requests/about-copilot-coding-agent) |
| 4 | Start **Q1** (first half — read through "Quest Setup") |
| 5 | Finish **Q1** (complete all exercises) |
| 6 | Start **Q2** (first half) |
| 7 | Finish **Q2** |
| 8 | Start **Q3** |
| 9 | Finish **Q3** |
| 10 | Read [Domain 1 chronicle post](/posts/embedding-agents-in-the-sdlc/) |

### Phase 2 — Tools & Environment (Days 11–30)

Work through Q4–Q7 across these 20 sessions, reading reference material between quests. See the [Week 2 schedule](#week-2) for the activity sequence — split each day's entry into 2–3 sessions of 15 minutes each.

### Phase 3 — Memory, Evaluation & Coordination (Days 31–70)

Work through Q8–Q17 using the [Weeks 3–5 schedules](#week-3--domain-3-memory-state--execution-5-hrs) as a guide, splitting each day into micro-sessions.

### Phase 4 — Guardrails & Capstone (Days 71–90)

Complete Q18–Q19, review all notes, and finish the capstone across the final 20 sessions.

---
