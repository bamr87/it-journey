---
title: Evaluating and Tuning Agents with GitHub Signals
description: Define machine-verifiable success criteria, debug agent failures, and tune behaviour using GitHub-native signals — GH-600 Domain 4.
permalink: /posts/evaluating-and-tuning-agents-with-github-signals/
draft: false
date: '2026-05-17T00:00:00.000Z'
preview: /images/previews/evaluating-and-tuning-agents-with-github-signals.png
sub-title: Domain 4 deep-dive for GH-600 candidates
excerpt: You can't improve what you can't measure. Domain 4 tests whether you can define what 'done' means, detect when it isn't, and systematically get better.
snippet: Define done. Measure it. Fix it. Repeat.
author: IT-Journey Team
layout: article
keywords:
- agent evaluation github
- agent success criteria
- gh-600 domain 4
- agent behavior tuning
- root cause analysis
lastmod: '2026-05-17T00:00:00.000Z'
tags:
- gh-600
- agentic-ai
- evaluation
- behavior-tuning
- domain-4
categories:
- AI & Machine Learning
- Engineering
---
Domain 4 of GH-600 (19% of the exam — tied with Domain 3 as the largest) covers evaluation and improvement. This is a domain that separates engineers who deploy agents from engineers who *operate* agents.

Deploying an agent is a one-time act. Operating an agent is continuous work: measuring its success rate, analysing its failures, and iterating on its instructions until it reliably does what you need.

## Machine-Verifiable Success Criteria (Sub-skill 4.1)

The most powerful concept in Domain 4 is the distinction between:

- **Vague criteria:** "The agent should implement the feature correctly."
- **Machine-verifiable criteria:** "All CI checks pass, no new security alerts are opened, and the PR receives at least one approving review."

Machine-verifiable criteria can be checked automatically by a workflow. This means you can know, without human review, whether the agent's output meets the bar — and you can do this check in a reproducible, consistent way across every agent run.

The implementation pattern is a `check-task-completion.yml` workflow that runs after the agent creates a PR and evaluates each criterion against GitHub's API signals.

## Root Cause Analysis (Sub-skill 4.2)

When an agent fails, the instinct is to re-run it. But re-running without understanding the failure is how you create a pattern of intermittent failures that are never really fixed.

Domain 4 sub-skill 4.2 covers a structured RCA approach for agent failures. The key artefacts are:

1. **Failure taxonomy** — a classification of failure types (tool failure, context failure, instruction failure, environment failure, etc.)
2. **5-Why analysis** — a root cause drill-down that asks "why" five times to find the systemic cause
3. **RCA document** — a written record of the findings, the root cause, and the fix applied

In GitHub Actions, forensics are collected using `gh run download` to get the full log and artifact set from a failed run.

## Behaviour Tuning (Sub-skill 4.3)

After identifying root causes, you change the agent's instructions to prevent recurrence. This is sub-skill 4.3: iterative instruction improvement.

The key discipline is **treating instructions like code**: version them, test changes, and keep a changelog. The Agentic Codex uses a `docs/agent-instructions/CHANGELOG.md` pattern where every instruction change is recorded with a before/after comparison and the metric it was targeting.

## Domain 4 Quests

| Quest | Skill | Link |
|---|---|---|
| Q11 | Success Criteria & Signals | [Success Criteria & Signals](/quests/gh-600/agentic-success-criteria-and-signals/) |
| Q12 | Failure Root Cause Analysis | [Failure Root Cause Analysis](/quests/gh-600/agentic-failure-root-cause-analysis/) |
| Q13 | Behaviour Tuning | [Behavior Tuning](/quests/gh-600/agentic-behavior-tuning/) |

These quests include the full success criteria schema, RCA template, instruction changelog pattern, and the `measure_agent_baseline.sh` script for establishing baselines before making changes.
