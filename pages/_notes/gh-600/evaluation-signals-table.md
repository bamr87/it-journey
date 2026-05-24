---
title: Evaluation Signals Table
description: Quick reference mapping GitHub-native signals to acceptance criteria types — for defining machine-verifiable success criteria in agent evaluation (GH-600 Domain 4).
date: '2026-05-17T00:00:00.000Z'
layout: default
permalink: /notes/gh-600/evaluation-signals-table/
author: IT-Journey Team
tags:
- gh-600
- evaluation
- signals
- quick-reference
categories:
- Notes
lastmod: '2026-05-17T00:00:00.000Z'
draft: false
---
# Evaluation Signals Table

## GitHub Signal → Acceptance Criteria Mapping

| Signal | Type | Check Command |
|---|---|---|
| CI workflow passes | Quality | `gh run list --workflow=ci.yml --branch={branch} --status=success` |
| All tests pass | Quality | `gh run view {run_id} --json conclusion -q '.conclusion=="success"'` |
| No new critical security alerts | Security | `gh api /repos/{owner}/{repo}/code-scanning/alerts?state=open&severity=critical \| jq 'length==0'` |
| PR has ≥1 approving review | Human approval | `gh pr view {number} --json reviewDecision -q '.reviewDecision=="APPROVED"'` |
| PR has no requested changes | Review quality | `gh pr view {number} --json reviewDecision -q '.reviewDecision!="CHANGES_REQUESTED"'` |
| No merge conflicts | Branch quality | `gh pr view {number} --json mergeable -q '.mergeable=="MERGEABLE"'` |
| Coverage threshold met | Coverage | Depends on coverage tool; check uploaded artifact |
| No new lint errors | Code quality | Parse lint output from workflow run |
| Docs updated | Documentation | `git diff --name-only HEAD~1 \| grep -q README` |

## Signal Categories

| Category | What It Tests |
|---|---|
| **ci-pass** | Build and test pipeline execution |
| **security-scan-pass** | No new vulnerabilities introduced |
| **review-approved** | Human reviewer endorsement |
| **coverage-pass** | Test coverage meets threshold |
| **lint-pass** | Code quality conventions |
| **docs-updated** | Documentation kept current |

## Acceptance Criteria Quality Levels

| Level | Description | Example |
|---|---|---|
| ❌ Vague | Cannot be checked automatically | "Implement the feature correctly" |
| ⚠️ Subjective | Requires human interpretation | "Code should be clean" |
| ✅ Verifiable | Binary pass/fail, checkable via API | "CI passes on the feature branch" |
| ✅✅ Machine-verifiable | Automated check in workflow | `gh run view` returns `success` |

**For GH-600:** All acceptance criteria should be machine-verifiable (✅✅ level).

## Related Quest

[Q11: Success Criteria & Signals](/quests/gh-600/agentic-success-criteria-and-signals/) — Full `acceptance-criteria.json` schema and `check-task-completion.yml` workflow.

---

*Part of: [[GH-600 Agentic AI Quick-Reference Notes]] · Related quest: [[The Oracle's Rubric: Defining Agent Success Criteria and Signals]] · Hub: [[The Agentic Codex: GH-600 Study Hub]]*
