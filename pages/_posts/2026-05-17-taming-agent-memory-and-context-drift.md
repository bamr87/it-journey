---
title: Taming Agent Memory and Context Drift
description: The three tiers of agent memory, how to persist state in GitHub Actions, and how to detect and recover from context drift. GH-600 Domain 3.
permalink: /posts/taming-agent-memory-and-context-drift/
draft: false
date: '2026-05-17T00:00:00.000Z'
preview: /images/previews/taming-agent-memory-and-context-drift.png
sub-title: Domain 3 deep-dive for GH-600 candidates
excerpt: An agent with no memory reinvents the wheel every time. An agent with bad memory builds on broken foundations. Domain 3 tests your understanding of how to manage both risks.
snippet: Three memory tiers. One persistence strategy. Zero drift.
author: IT-Journey Team
layout: article
breaking: true
featured: true
keywords:
- agent memory github
- context drift
- gh-600 domain 3
- state persistence
- ephemeral session persistent memory
lastmod: '2026-05-17T00:00:00.000Z'
tags:
- gh-600
- agentic-ai
- memory
- context-management
- domain-3
categories:
- AI & Machine Learning
- Architecture
---
Domain 3 of GH-600 (19% of the exam — the largest domain alongside D4) covers memory, context, and state management. This is where many agentic AI designs fail.

The core problem: agents don't automatically remember things across tasks. Every time a GitHub Actions workflow runs, it starts in a clean environment. Every time a Copilot session begins, the model has no memory of previous conversations. This is by design — but it means you must design memory explicitly.

## The Three Memory Tiers

The Agentic Codex uses a three-tier model:

### Tier 1: Ephemeral Memory

Exists only within a single workflow job. It's the `env:` block, the `$GITHUB_ENV` file, and step outputs. When the job ends, it's gone.

**Use for:** Intermediate calculations, step-to-step data passing, temporary counters.

### Tier 2: Session Memory

Persists for the duration of a workflow run (across jobs). In GitHub Actions, this is implemented using **artifacts** — one job uploads a file, another downloads it.

**Use for:** Plans generated in the planning phase and consumed in the execution phase, task checklists that span multiple steps.

### Tier 3: Persistent Memory

Persists across workflow runs. In GitHub Actions, this means **repository files** (committed and pushed by the agent) or **GitHub Actions cache**.

**Use for:** Agent instruction changelogs, running task registers, approved action history, evaluation metrics.

## Context Drift: The Quiet Failure

Context drift happens when the state the agent *believes* the world is in diverges from the state the world is *actually* in. A few common causes:

- The agent read a file at the start of the run; someone else changed the file mid-run
- The agent based its plan on a previous task's output, but that output is stale
- The agent has a persistent memory file that wasn't updated after the last run ended abnormally

Drift detection (Domain 3 sub-skill 3.2) involves comparing a **state snapshot** taken at the start of a task against the current state. The comparison is straightforward in principle: hash the key files, compare the hashes, abort or re-plan if they differ.

## Cross-Surface Context Continuity (Sub-skill 3.3)

This is the most nuanced sub-skill in Domain 3. It covers how an agent maintains continuity as work moves from issue → branch → PR → Actions run → merge.

The key tool is a **context handoff document** — a JSON file that captures the relevant state at each transition. When the PR is created, the agent writes a `context-handoff.json` that summarises the issue intent, the decisions made during planning, and any unresolved questions. When the Actions workflow runs on the PR, it reads this file to understand what it's supposed to be doing.

## Domain 3 Quests

| Quest | Skill | Link |
|---|---|---|
| Q8 | Memory Strategies | [Memory Strategies](/quests/gh-600/agentic-memory-strategies/) |
| Q9 | State Persistence & Drift | [State Persistence & Drift](/quests/gh-600/agentic-state-persistence-and-drift/) |
| Q10 | Cross-Tool Continuity | [State Continuity Cross-Tools](/quests/gh-600/agentic-state-continuity-cross-tools/) |

These quests include complete workflow implementations, Python scripts for drift detection, and the context handoff schema.
