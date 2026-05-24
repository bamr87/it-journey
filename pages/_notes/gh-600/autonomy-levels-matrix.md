---
title: Autonomy Levels Matrix
description: Quick reference for the five-level autonomy spectrum (L0–L4) — task classification criteria, appropriate use cases, and guardrail requirements for each level.
date: '2026-05-17T00:00:00.000Z'
layout: default
permalink: /notes/gh-600/autonomy-levels-matrix/
author: IT-Journey Team
tags:
- gh-600
- autonomy
- responsible-ai
- quick-reference
categories:
- Notes
lastmod: '2026-05-17T00:00:00.000Z'
draft: false
---
# Autonomy Levels Matrix

## The Five Levels

| Level | Name | Agent Acts? | Human Reviews? | Human Approves? |
|---|---|---|---|---|
| **L0** | Manual | ❌ | N/A | N/A |
| **L1** | Assisted | Suggests only | ✅ Every action | ✅ Every action |
| **L2** | Supervised | ✅ Yes | ✅ Every output | ✅ Before publish |
| **L3** | Monitored | ✅ Yes | Exceptions only | ❌ Not required |
| **L4** | Autonomous | ✅ Yes | Periodic audits | ❌ Not required |

## Task Classification Criteria

When classifying a task, answer three questions:

| Question | Low Score → Higher Level OK | High Score → Lower Level Required |
|---|---|---|
| **Reversibility** | Easily undoable (delete a comment) | Hard to undo (deploy to prod) |
| **Blast Radius** | Affects 1 file in 1 PR | Affects security config or user data |
| **Predictability** | Same task done correctly 50+ times | Novel task or unstable codebase |

## Level Guidance by Task Type

| Task Type | Suggested Level |
|---|---|
| Fix typo in docs | L3 |
| Add unit tests for existing function | L2–L3 |
| Implement new API endpoint | L2 |
| Refactor authentication module | L1–L2 |
| Modify CODEOWNERS / security config | L1 |
| Create/delete repository | L1 |
| Infrastructure changes | L1 |

## Guardrail Requirements by Level

| Level | Required Guardrails |
|---|---|
| L1 | N/A (human approves every action) |
| L2 | CODEOWNERS on sensitive paths, PR review required |
| L3 | Environment approval gate for deployments, audit logging |
| L4 | All of L3 + automated anomaly detection + kill switch |

## Related Quest

[Q18: Autonomy Levels Matrix](/quests/gh-600/agentic-autonomy-levels-matrix/) — Full implementation with `_data/autonomy-matrix.yml` schema.

---

*Part of: [[GH-600 Agentic AI Quick-Reference Notes]] · Related quest: [[The Autonomy Scales: Mapping Agent Autonomy Levels]] · Hub: [[The Agentic Codex: GH-600 Study Hub]]*
