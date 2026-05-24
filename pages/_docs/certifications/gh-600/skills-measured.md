---
title: GH-600 Skills Measured — Full Breakdown
description: Complete breakdown of all 6 domains and 19 sub-skills for GH-600, each linked to its corresponding quest.
permalink: /docs/certifications/gh-600/skills-measured/
layout: default
categories:
- Docs
- Certifications
- Agentic-AI
tags:
- gh-600
- agentic-ai
- skills-measured
- certifications
lastmod: '2026-05-17T00:00:00.000Z'
date: '2026-05-17T00:00:00.000Z'
author: IT-Journey Team
toc: true
toc_sticky: true
draft: false
keywords:
- gh-600
- agentic-ai
- skills-measured
- certifications
- docs
- skills
- measured
- full
---
# GH-600 Skills Measured — Full Breakdown

*Official source: [learn.microsoft.com/credentials/certifications/resources/study-guides/gh-600](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600)*

Each sub-skill maps to exactly one quest. Click the quest link to start practising that skill immediately.

> **How to use this page:** Work through each domain in order. After reading each sub-skill, rate your confidence (1–5). Return to this page before your exam and ensure every sub-skill is ≥ 4. The [Skills Checklist](/notes/gh-600/skills-checklist/) provides a printable version.

---

## Exam Question Archetypes

Understanding the question *type* is as important as knowing the content. GH-600 uses three primary patterns:

| Archetype | Description | Example stem |
|---|---|---|
| **Scenario → Diagnosis** | A failing or misbehaving agent is described — identify root cause | "An agent repeatedly requests the same API endpoint. What is the most likely cause?" |
| **Config Selection** | Choose the YAML/config that satisfies a stated constraint | "Which `permissions:` block grants the minimum privilege for an agent to open a PR?" |
| **Best Practice** | Select the *most* appropriate design decision from four plausible options | "Which guardrail approach best preserves velocity while preventing irreversible file deletions?" |

Keep these archetypes in mind as you read each sub-skill below.

---

## Domain 1 — Prepare Agent Architecture & SDLC Processes (15–20%)

### Sub-Skill 1.1 — Integrate agents into the SDLC
- Identify steps for agents to perform  
- Identify and mitigate common anti-patterns in agents  
- Define inputs, outputs, and success criteria for agents  
**→ Quest:** [Q1: Initiation Rites — Embedding Agents in the SDLC](/quests/gh-600/agentic-sdlc-integration/)

### Sub-Skill 1.2 — Define boundaries between planning, reasoning, and action
- Configure agent planning to be distinct from agent execution  
- Configure an agent to output a structured plan  
- Validate agent plans  
- Prevent agent action until the agent checked and approved  
**→ Quest:** [Q2: The Three Sigils — Plan, Reason, Act](/quests/gh-600/agentic-plan-vs-action-boundaries/)

### Sub-Skill 1.3 — Configure observability and control for autonomous agents
- Plan and implement the degree of agent autonomy, including guardrails  
- Configure agent to produce inspectable artifacts within standard development tooling  
- Configure human intervention for autonomous agents without slowing delivery  
**→ Quest:** [Q3: The All-Seeing Eye — Observability & Control](/quests/gh-600/agentic-observability-and-control/)

---

## Domain 2 — Implement Tool Use & Environment Interaction (20–25%)

### Sub-Skill 2.1 — Select and configure agent tools
- Identify required tools  
- Configure agent tools  
- Configure agent tool permissions  
**→ Quest:** [Q4: Forging the Agent's Arsenal](/quests/gh-600/agentic-tool-selection-and-permissions/)

### Sub-Skill 2.2 — Configure MCP servers
- Add an MCP server as a tool to an agent  
- Configure a GitHub remote MCP server  
- Configure the MCP registries  
- Configure MCP allow lists  
**→ Quest:** [Q5: The MCP Conclave](/quests/gh-600/agentic-mcp-server-mastery/)

### Sub-Skill 2.3 — Integrate agents within development environments
- Evaluate the execution context for an agent  
- Configure an agent's scope to a specific repository  
- Configure an agent to be invoked in a CI workflow  
- Configure an agent to use branch-based scope  
- Enable an agent to perform autonomous actions (branches, PRs)  
- Configure an agent to handle environment-specific constraints  
**→ Quest:** [Q6: Bind the Agent to the Realm](/quests/gh-600/agentic-dev-environment-integration/)

### Sub-Skill 2.4 — Operate agents with safe execution paths and robust error handling
- Implement error handling  
- Implement retries  
- Implement rollbacks  
- Implement escalation paths  
- Implement traceability and accountability for agent actions  
**→ Quest:** [Q7: The Shield of Retries](/quests/gh-600/agentic-safe-execution-and-error-handling/)

---

## Domain 3 — Manage Memory, State & Execution (10–15%)

### Sub-Skill 3.1 — Implement agent memory strategies
- Choose between short-term, long-term, and external memory  
- Scope agent memory to task-relevant information  
- Define memory expiration, pruning, and reset rules  
**→ Quest:** [Q8: Vaults of Recollection — Memory Strategies](/quests/gh-600/agentic-memory-strategies/)

### Sub-Skill 3.2 — Persist agent state and manage context drift
- Capture task progress and decisions as durable artifacts  
- Resume agent work without repeating steps or diverging from prior decisions  
- Detect and correct drift during extended agent execution  
**→ Quest:** [Q9: Anchoring the Drifting Agent](/quests/gh-600/agentic-state-persistence-and-drift/)

### Sub-Skill 3.3 — Ensure continuity of agent memory and state across tools and environments
- Share agent state  
- Prevent conflicting context  
- Prevent stale context  
**→ Quest:** [Q10: Crossing the Tool Planes](/quests/gh-600/agentic-state-continuity-cross-tools/)

---

## Domain 4 — Perform Evaluation, Error Analysis & Tuning (15–20%)

### Sub-Skill 4.1 — Define success criteria and evaluation signals for agent tasks
- Specify expected outcomes and operational constraints  
- Identify qualitative and quantitative evaluation signals  
- Align evaluation criteria with development intent  
- Generate evaluation signals by using automated scanning tools  
**→ Quest:** [Q11: The Oracle's Rubric](/quests/gh-600/agentic-success-criteria-and-signals/)

### Sub-Skill 4.2 — Analyze agent failures and identify root causes
- Identify failures using logs, plans, traces, outputs, and workflow artifacts  
- Classify root causes: reasoning errors, tool misuse, context/environment issues  
**→ Quest:** [Q12: The Necromancer's Inquest](/quests/gh-600/agentic-failure-root-cause-analysis/)

### Sub-Skill 4.3 — Tune agent behavior based on evaluation results
- Revise instructions, workflows, or constraints  
- Refine memory usage  
- Refine tool usage and tool access  
**→ Quest:** [Q13: Reforging the Agent's Mind](/quests/gh-600/agentic-behavior-tuning/)

---

## Domain 5 — Orchestrate Multi-Agent Coordination (15–20%)

### Sub-Skill 5.1 — Operate and manage multi-agent workflows
- Apply an orchestration pattern to coordinate multiple agents  
- Configure agent isolation for parallel execution  
- Detect and resolve agent conflicts (overlapping code changes, duplicated effort, contradictory outputs)  
**→ Quest:** [Q14: The Council of Many — Orchestration Patterns](/quests/gh-600/agentic-multi-agent-orchestration-patterns/)

### Sub-Skill 5.2 — Configure observability for multi-agent behavior
- Configure multi-agent workflows to produce artifacts suitable for review and audit  
- Document key decisions, handoffs, and outcomes across agents  
- Perform post-hoc analysis of multi-agent behavior  
**→ Quest:** [Q15: The Scribe's Codex — Multi-Agent Observability](/quests/gh-600/agentic-multi-agent-observability/)

### Sub-Skill 5.3 — Detect and respond to multi-agent failures and degraded behavior
- Identify failed, partial, or stalled agent executions  
- Respond to degraded behavior or coordination across agents  
- Implement multi-agent recovery patterns (rollback, human-in-the-loop)  
**→ Quest:** [Q16: When Familiars Fall — Failure & Recovery](/quests/gh-600/agentic-multi-agent-failure-recovery/)

### Sub-Skill 5.4 — Manage the lifecycle of agents within multi-agent workflows
- Add agents to existing multi-agent workflows  
- Update, reconfigure, or replace agents without disrupting active workflows  
- Retire agents while preserving auditability and workflow continuity  
**→ Quest:** [Q17: The Agent Pantheon — Lifecycle Management](/quests/gh-600/agentic-multi-agent-lifecycle-management/)

---

## Domain 6 — Implement Guardrails & Accountability (10–15%)

### Sub-Skill 6.1 — Define autonomy levels
- Classify agent actions by operational, security, and compliance risk  
- Assign autonomy levels to maximize delivery speed while remaining compliant  
**→ Quest:** [Q18: The Autonomy Scales](/quests/gh-600/agentic-autonomy-levels-matrix/)

### Sub-Skill 6.2 — Implement guardrails and human-in-the-loop workflows
- Identify the subset of actions that require human judgment  
- Block actions that violate defined security, compliance, or Responsible AI policies  
- Scope permissions and execution contexts to enforce least-privilege access  
- Require explicit authorization for irreversible or compliance-sensitive changes  
- Preserve execution velocity by minimizing approvals that do not materially reduce risk  
**→ Quest:** [Q19: The Warden's Pact — Guardrails & HITL](/quests/gh-600/agentic-guardrails-and-human-in-the-loop/)

---

## Coverage Matrix

| GH-600 Sub-Skill | Quest | Level |
|---|---|---|
| 1.1 Integrate agents into SDLC | Q1 | 0111 |
| 1.2 Plan vs. action boundaries | Q2 | 0111 |
| 1.3 Observability & control | Q3 | 1000 |
| 2.1 Select & configure tools | Q4 | 1000 |
| 2.2 Configure MCP servers | Q5 | 1000 |
| 2.3 Dev environment integration | Q6 | 1001 |
| 2.4 Safe execution & error handling | Q7 | 1001 |
| 3.1 Memory strategies | Q8 | 1001 |
| 3.2 State persistence & drift | Q9 | 1010 |
| 3.3 State continuity cross-tools | Q10 | 1010 |
| 4.1 Success criteria & signals | Q11 | 1010 |
| 4.2 Failure root cause analysis | Q12 | 1010 |
| 4.3 Behavior tuning | Q13 | 1011 |
| 5.1 Multi-agent workflows | Q14 | 1011 |
| 5.2 Multi-agent observability | Q15 | 1011 |
| 5.3 Multi-agent failure & recovery | Q16 | 1011 |
| 5.4 Agent lifecycle management | Q17 | 1100 |
| 6.1 Autonomy levels | Q18 | 1100 |
| 6.2 Guardrails & HITL | Q19 | 1100 |
| **Capstone** | All 6 domains | 1100 |

**Coverage: 19/19 (100%)** — no gaps, no duplicates.

---

## Domain-by-Domain Exam Tips

### Domain 1 — What to watch for
Questions tend to be **best-practice selection**: given a scenario where an agent is "doing too much" or "acting before planning," choose the architecture fix. Know the difference between planning output (structured plan artifact) and action execution — and know what a valid "approval gate" looks like.

### Domain 2 — What to watch for
The highest-weight domain. Expect **config selection** questions (MCP server YAML, `permissions:` blocks, scope constraints) alongside **scenario → diagnosis** questions where a CI-triggered agent fails silently. Know the exact structure of an MCP tool definition and the allow-list syntax.

### Domain 3 — What to watch for
Questions often appear embedded in Domain 4 or 5 scenarios. The key pattern: an agent "forgets" a prior decision — which memory strategy would have prevented it? Understand the difference between short-term context, long-term store, and external memory, and when each is appropriate.

### Domain 4 — What to watch for
Expect **scenario → diagnosis**: a trace or log excerpt is shown, and you must classify the root cause (reasoning error vs tool misuse vs environment issue). Also expect **best-practice** questions on how to revise instructions vs tool access vs memory when a particular pattern of failure is shown.

### Domain 5 — What to watch for
Orchestration questions test whether you can distinguish *sequential*, *parallel*, and *hierarchical* patterns — and when to use each. Failure-recovery questions ask what signal indicates a stalled sub-agent vs a conflicting sub-agent, and how to respond differently.

### Domain 6 — What to watch for
The Autonomy Levels Matrix is heavily tested. Be able to **classify** an action by risk level and **select** the correct human-in-the-loop gate. Know what "least-privilege" means in the context of agent permissions and how it differs from traditional RBAC.
