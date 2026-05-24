---
title: ".github/prompts Directory"
description: "AI agent prompt collection powering IT-Journey automation flows"
permalink: /github/prompts/readme/
lastmod: 2026-05-18T17:21:39.000Z
layout: default
date: 2025-11-15T16:34:42.000Z

---

# .github/prompts

This directory houses the reusable prompt blueprints that power IT-Journey's internal AI agents. Each prompt documents an end-to-end operating protocol (mission, intake checklist, output format, quality gates) so that automated `/slash` commands inside GitHub issues, pull requests, or VS Code Copilot Sessions always produce predictable results.

## Directory Structure

```
.github/prompts/
├── bash-it.prompt.md            # Comprehensive bash script generation agent
├── commit-publish.prompt.md     # Commit, document, and publish to gh-pages
├── draft-article.prompt.md      # Long-form article drafting agent
├── expand-content.prompt.md     # Content expansion helper
├── generate-frontmatter.prompt.md  # Validator-aligned frontmatter generator
├── kaizen.prompt.md             # Continuous improvement / PDCA facilitator
├── publish-prep.prompt.md       # Pre-publish content readiness checks
├── refine-content.prompt.md     # Targeted content refinement
├── retrospective.prompt.md      # Review AI conversations → update instructions/prompts incrementally
├── stackattack.prompt.md        # Repository stack analysis playbook
├── validate-content.prompt.md   # Content validation against repo standards
├── workflow-summary.prompt.md   # Summarize a recent workflow/run
├── quest-permalink-audit.prompt.md  # Audit/repair quest permalink hierarchy
├── write-quest.prompt.md        # Epic quest authoring protocol
├── wtd.prompt.md                # What To Do - TODO task execution agent
└── README.md                    # This guide
```

## Prompt Catalog

{: .table .table-bordered .table-striped .table-hover .table-responsive}
| Prompt | Trigger | Primary Mission | Key Deliverables |
|--------|---------|-----------------|------------------|
| `bash-it.prompt.md` | `/bash-it` | Transform articles, quests, and documentation into production-ready bash scripts with comprehensive best practices | Complete bash script with error handling, logging, testing checklist, installation guide, and integration examples |
| `generate-frontmatter.prompt.md` | `/generate-frontmatter` | Produce Jekyll frontmatter that passes `frontmatter-validation.yml` and `content-reviewer.py` on the first try | YAML block with self-counted title (30–60) and description (120–160) char lengths and all required fields |
| `kaizen.prompt.md` | `/kaizen` | Lead incremental PDCA improvement sessions for code, process, or tooling | PLAN/DO/CHECK/ACT report with metrics, risks, next iteration |
| `retrospective.prompt.md` | `/retrospective` | Review an AI agent conversation/PR thread and fold lessons back into `.github/copilot-instructions.md`, `.github/instructions/*`, and `.github/prompts/*` with citations | Lesson ledger, triage table, surgical diffs, `store_memory` calls, validation report |
| `stackattack.prompt.md` | `/stackattack` | Analyze any repository's full technology stack with diagrams and recommendations | Stack overview, five-layer analysis, Mermaid diagrams, modernization roadmap saved under quests/stacks |
| `write-quest.prompt.md` | `/write-quest` | Transform learning context into IT-Journey compliant quests | Complete quest at `pages/_quests/XXXX/slug.md`, canonical frontmatter, `make quest-audit` gate |
| `quest-permalink-audit.prompt.md` | `/quest-permalink-audit` | Audit and repair permalink violations across `pages/_quests/` | Violation report, migration via `migrate-permalinks.py`, network rebuild |
| `wtd.prompt.md` | `/wtd` | Work through TODO directory items using PDCA methodology | Task selection, execution, status updates, progress tracking, suggested commits |

Note: `write-quest` references the canonical front matter template stored at `/.frontmatter/templates/quests.md`. Do not duplicate YAML fields in the prompt; the agent must read and use the template to produce consistent front matter for every quest.

> **Closing the loop:** `/retrospective` is the meta-prompt that keeps every other prompt and instruction file honest. Run it after any session that produced a correction loop — the proposed edits land in this same `.github/` tree, so the prompt library is self-improving.

## Usage Workflow

1. **README-First** – Before invoking a prompt, review the relevant quest, stack, or feature README to capture constraints and context.
2. **Trigger** – Call the appropriate `/command` inside VS Code Copilot Chat, GitHub Issues, or Discussions and supply the required intake payload listed inside each prompt file.
3. **Review Output** – Validate that the response satisfies the embedded quality checklist (metrics, diagrams, links, tests).
4. **README-Last** – After accepting the AI-generated artifact, update the affected README/index files and log the change history.

## Authoring New Prompts

When adding a new agent protocol:
- Follow the structure demonstrated in the existing prompt files (front matter, mission briefing, operating framework, quality checklist)
- Include explicit intake requirements so agents know what context to request
- Document storage/automation expectations (e.g., where outputs must be saved)
- Reuse canonical templates from `/.frontmatter/templates/` instead of embedding YAML field lists inside prompts.
- Update the table above with the new prompt and adjust `lastmod`

## Related References

- [`quest.instructions.md`](../instructions/quest.instructions.md) – Canonical quest creation standards
- [`prompts.instructions.md`](../instructions/prompts.instructions.md) – Prompt engineering guidance with Kaizen integration
- [`README.instructions.md`](../instructions/README.instructions.md) – Required workflow for maintaining this file

---
**Maintained by:** IT-Journey Automation Guild  
**Questions?** [Open an issue](https://github.com/bamr87/it-journey/issues)
