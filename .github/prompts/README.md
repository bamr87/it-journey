---
title: ".github/prompts Directory"
description: "AI agent prompt collection powering IT-Journey automation flows"
permalink: /github/prompts/readme/
lastmod: 2025-11-14T00:00:00.000Z
layout: default
---

# .github/prompts

This directory houses the reusable prompt blueprints that power IT-Journey's internal AI agents. Each prompt documents an end-to-end operating protocol (mission, intake checklist, output format, quality gates) so that automated `/slash` commands inside GitHub issues, pull requests, or VS Code Copilot Sessions always produce predictable results.

## Directory Structure

```
.github/prompts/
├── kaizen.prompt.md        # Continuous improvement / PDCA facilitator
├── stackattack.prompt.md   # Repository stack analysis playbook
├── write-quest.prompt.md   # Epic quest authoring protocol
└── README.md               # This guide
```

## Prompt Catalog

{: .table .table-bordered .table-striped .table-hover .table-responsive}
| Prompt | Trigger | Primary Mission | Key Deliverables |
|--------|---------|-----------------|------------------|
| `kaizen.prompt.md` | `/kaizen` | Lead incremental PDCA improvement sessions for code, process, or tooling | PLAN/DO/CHECK/ACT report with metrics, risks, next iteration |
| `stackattack.prompt.md` | `/stackattack` | Analyze any repository's full technology stack with diagrams and recommendations | Stack overview, five-layer analysis, Mermaid diagrams, modernization roadmap saved under quests/stacks |
| `write-quest.prompt.md` | `/write-quest` | Transform learning context into IT-Journey compliant epic quests | Complete quest front matter, chaptered narrative, multi-platform paths, diagrams, validation + Kaizen hooks |

Note: `write-quest` references the canonical front matter template stored at `/.frontmatter/templates/quests.md`. Do not duplicate YAML fields in the prompt; the agent must read and use the template to produce consistent front matter for every quest.

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
