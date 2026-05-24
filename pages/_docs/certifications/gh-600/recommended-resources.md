---
title: GH-600 Recommended Resources
description: 'Curated resources for GH-600 exam preparation: Microsoft Learn paths, GitHub documentation, MCP specification, and the GitHub Models API.'
permalink: /docs/certifications/gh-600/recommended-resources/
layout: default
categories:
- Docs
- Certifications
- Agentic-AI
tags:
- gh-600
- agentic-ai
- resources
- microsoft-learn
- mcp
author: IT-Journey Team
draft: false
lastmod: '2026-05-17T00:00:00.000Z'
date: '2026-05-17T00:00:00.000Z'
toc: true
keywords:
- gh-600
- agentic-ai
- resources
- microsoft-learn
- mcp
- docs
- certifications
- recommended
---
# GH-600 Recommended Resources

*The Arcane Library — texts and scrolls gathered from across the digital realm.*

---

## Microsoft Learn (Official)

| Resource | Type | Relevant Domains |
|---|---|---|
| [GH-600 Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600) | Study Guide | All |
| [GH-600 Exam page](https://learn.microsoft.com/en-us/credentials/certifications/exams/gh-600/) | Exam Overview | All |
| [Microsoft Learn — GitHub Copilot collection](https://learn.microsoft.com/en-us/training/browse/?products=github-copilot) | Catalog | D1–D6 |
| [Microsoft Learn — Agentic AI search](https://learn.microsoft.com/en-us/training/browse/?terms=agentic) | Catalog | D1, D3, D5 |

> **Note:** Microsoft Learn does not yet ship a dedicated "GH-600 learning path." The two catalog links above are the closest official curation. We mirror the same material in the GH-600 quest line and chronicle posts below — use those as the structured path and refer to Microsoft Learn when you want the official source on a single concept.

## GitHub Documentation

| Resource | Relevant Domains |
|---|---|
| [GitHub Copilot documentation](https://docs.github.com/en/copilot) | D1, D2, D6 |
| [GitHub Copilot coding agent](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-for-pull-requests/about-copilot-coding-agent) | D1, D2, D3 |
| [Model Context Protocol (MCP) with Copilot](https://docs.github.com/en/copilot/extensibility/using-model-context-protocol/using-model-context-protocol-with-github-copilot) | D2 |
| [GitHub Actions documentation](https://docs.github.com/en/actions) | D2, D4, D5 |
| [GitHub Models API](https://docs.github.com/en/github-models) | D2, D4 |
| [GitHub Advanced Security / CodeQL](https://docs.github.com/en/code-security) | D4, D6 |
| [Repository rules & rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets) | D6 |

## MCP Specification

| Resource | Type |
|---|---|
| [modelcontextprotocol.io](https://modelcontextprotocol.io/) | Official Spec |
| [MCP GitHub Repository](https://github.com/modelcontextprotocol/specification) | Source |
| [MCP Servers Registry](https://github.com/modelcontextprotocol/servers) | Reference Implementations |

## Community & Support

| Resource | Type |
|---|---|
| [GitHub Community Discussions](https://github.com/orgs/community/discussions) | Forum |
| [GitHub Blog — Copilot](https://github.blog/tag/github-copilot/) | News & Tutorials |
| [GitHub on YouTube](https://www.youtube.com/@GitHub) | Videos |

## Hands-On Sandboxes

| Resource | Notes |
|---|---|
| `work/gh-600/` in this repo | Starter MCP server, Actions workflow, eval harness |
| [GitHub Skills](https://skills.github.com/) | Free interactive GitHub courses |
| [GitHub Codespaces](https://github.com/features/codespaces) | Cloud dev environment for all quests |

---

## Video & Talk Resources

| Resource | Type | Relevant Domains |
|---|---|---|
| [GitHub Universe keynotes (youtube.com/@GitHub)](https://www.youtube.com/@GitHub) | Conference talks | D1–D6 |
| [GitHub Copilot — What's new (GitHub Blog)](https://github.blog/tag/github-copilot/) | Changelog deep-dives | D1, D2 |
| [Model Context Protocol Explained (modelcontextprotocol.io)](https://modelcontextprotocol.io/) | Spec walkthrough | D2 |
| [GitHub Actions: CI/CD for beginners (GitHub Skills)](https://skills.github.com/) | Interactive course | D2, D5 |

---

## GitHub Blog Deep-Dives

These posts cover real-world agentic AI patterns directly relevant to GH-600 exam domains:

| Post | Domain(s) |
|---|---|
| [How GitHub Copilot coding agent works](https://github.blog/engineering/infrastructure/how-github-copilot-coding-agent-works/) | D1, D2 |
| [Inside GitHub: Working with the LLMs](https://github.blog/ai-and-ml/generative-ai/inside-github-working-with-the-llms-behind-github-copilot/) | D3, D4 |
| [The architecture of today's LLM applications](https://github.blog/ai-and-ml/generative-ai/the-architecture-of-todays-llm-applications/) | D1, D3, D5 |
| [How to build a CI/CD pipeline with GitHub Actions in four steps](https://github.blog/enterprise-software/ci-cd/build-ci-cd-pipeline-github-actions-four-steps/) | D2, D5 |

---

## Exam Strategy

### Scoring & Format

- **700 / 1000** passing threshold
- Expect a mix of **scenario-based questions** ("an agent produces X output — which root cause is most likely?"), **configuration questions** ("which YAML block correctly scopes the agent to a single repo?"), and **best-practice selection** ("which approach preserves least-privilege while enabling autonomous PRs?")
- **Domain 2 (20–25%)** and **Domain 1 (15–20%)** are the highest-weight areas — prioritize if short on time

### Weak-Area Triage

Use the [Skills Checklist](/notes/gh-600/skills-checklist/) to identify gaps, then:

1. Re-do the corresponding quest for any sub-skill below confidence
2. Re-read the chronicle post that covers the domain
3. Use the [Evaluation Signals Table](/notes/gh-600/evaluation-signals-table/) or [Autonomy Levels Matrix](/notes/gh-600/autonomy-levels-matrix/) reference notes to solidify decision-making frameworks

### Common Mistakes to Avoid

| Mistake | Better Approach |
|---|---|
| Skipping Domain 3 (only 10–15%) | Memory & drift are tested implicitly in D4 and D5 scenarios too |
| Memorising commands without context | Focus on *why* a config choice matters, not just *what* the syntax is |
| Treating the capstone as a final exam | Use it as a diagnostic two days before — there's still time to fix gaps |
| Studying only from this repo | Cross-check with the [official Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600) for language alignment |

---
