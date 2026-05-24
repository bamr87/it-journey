---
title: GH-600 Glossary
description: 'Definitions of key terms from all six domains of GH-600: Developing in Agentic AI Systems.'
date: '2026-05-17T00:00:00.000Z'
layout: default
permalink: /notes/gh-600/glossary/
author: IT-Journey Team
tags:
- gh-600
- glossary
- definitions
- quick-reference
categories:
- Notes
lastmod: '2026-05-17T00:00:00.000Z'
draft: false
---
# GH-600 Glossary

## A

**AGENTS.md**  
A file placed in the root of a repository that provides instructions, conventions, and constraints for AI agents working in that repository. Similar in purpose to `CONTRIBUTING.md` but addressed to AI systems.

**Acceptance Criteria**  
Specific, machine-verifiable conditions that must be true for an agent task to be considered complete. Should be binary (pass/fail) and checkable via GitHub API or workflow output.

**Agentic AI**  
An AI system that takes autonomous actions across a sequence of steps, maintaining state and adapting its behaviour based on feedback, rather than responding to single prompts.

**Autonomy Level**  
A classification of how independently an AI agent operates on a given task, from L0 (no agent involvement) to L4 (fully autonomous with periodic human audit).

## B

**Blast Radius**  
The maximum potential impact if an agent makes a mistake on a given task. High blast radius tasks require lower autonomy levels and stronger guardrails.

**Bounded Agency**  
The principle that agents should operate within defined scope, permissions, and reversibility constraints, rather than with unlimited access.

## C

**Coding Agent (GitHub Copilot)**  
The autonomous mode of GitHub Copilot that can be assigned issues, create branches, write code, run tests, and open PRs without continuous human guidance.

**Context Drift**  
Gradual degradation of an agent's contextual understanding over a long-running task, caused by the finite size of the model's context window filling with less-relevant earlier content.

**Context Window**  
The maximum number of tokens an AI model can process in a single request, including both input (system prompt, history, documents) and output (response).

**Correlation ID**  
A unique identifier attached to all log entries, workflow runs, and actions related to a single agent task execution, enabling end-to-end tracing.

## D

**Drift (Context Drift)**  
See *Context Drift*.

## E

**Ephemeral Memory**  
Memory that exists only within a single agent session or conversation. Lost when the session ends.

## F

**Fan-out Pattern**  
A multi-agent orchestration pattern in which an orchestrator agent dispatches subtasks to multiple specialist agents in parallel, then aggregates their results.

## G

**Guardrail**  
A constraint that limits what an agent can do, regardless of its instructions. Implemented via CODEOWNERS, environment approval gates, workflow conditions, or AGENTS.md forbidden actions lists.

## H

**HITL (Human-in-the-Loop)**  
A design pattern requiring human review or approval at one or more checkpoints in an agent workflow, preventing fully autonomous execution for tasks above a defined risk threshold.

## K

**Kill Switch**  
A mechanism to immediately stop all agent activity, typically implemented as a flag file, workflow concurrency group, or emergency environment variable.

## L

**LLM (Large Language Model)**  
The AI model underlying an agent, responsible for reasoning, planning, and generating text or code.

## M

**MCP (Model Context Protocol)**  
An open standard protocol for connecting AI models to external tools. MCP servers expose structured tools (functions with schemas) that an AI agent can call.

**Memory Tier**  
The classification of agent memory by persistence: ephemeral (session-only), session (multi-turn within a task), or persistent (survives across agent sessions).

**Multi-Agent System**  
A system in which multiple AI agents collaborate, each handling a specialised part of a larger task, coordinated by an orchestrator or peer-to-peer communication.

## O

**Observability**  
The degree to which the internal state and actions of an agent can be inferred from its external outputs. Implemented via structured logging, correlation IDs, and workflow run summaries.

**Orchestrator (Agent)**  
An agent responsible for decomposing a complex goal into subtasks and dispatching those subtasks to specialist agents.

## P

**Persistent Memory**  
Memory that is stored durably and survives across multiple agent sessions. Implemented via committed files, database records, or external stores.

**Plan Phase**  
The stage of agentic execution in which the agent determines what it will do before taking any actions. Kept separate from the Action Phase to enable human review of the plan.

## R

**Reversibility**  
A property of an agent action describing how easily it can be undone. File edits in a branch are reversible; production deployments are not.

## S

**Session Memory**  
Memory that persists within a single multi-turn task or agent session, but is not retained across separate sessions.

**Specialist Agent**  
An agent designed to perform a specific, narrow function within a larger multi-agent system.

## T

**Tool (Agent Tool)**  
A capability exposed to an agent, typically as a function with a defined schema. Examples: `create_file`, `run_command`, `search_issues`.

**Tool Poisoning**  
A security attack in which malicious content in a tool's output contains hidden instructions that redirect the agent's behaviour.

## W

**Workflow Trigger**  
The GitHub Actions event that initiates an agent workflow (e.g., `issues`, `push`, `workflow_dispatch`).

---

*Part of: [[GH-600 Agentic AI Quick-Reference Notes]] · Hub: [[The Agentic Codex: GH-600 Study Hub]]*
