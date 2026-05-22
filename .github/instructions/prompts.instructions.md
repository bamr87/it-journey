---
applyTo: "**/prompts/**/*.md"
description: "Author and refine prompt files (.prompt.md) following the IT-Journey prompt-engineering and Kaizen schema"
date: 2025-11-02T22:15:37.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# Prompt Engineering — `.prompt.md`

Rules for writing and refining reusable AI prompts. Frontmatter schema lives in [`../FRONTMATTER.md`](../FRONTMATTER.md).

## 1. Required Frontmatter

```yaml
---
mode: agent
description: "One-line purpose, ≤160 chars"
tools: [optional, list, of, tool, names]   # omit if none required
date: YYYY-MM-DDTHH:MM:SS.sssZ
lastmod: YYYY-MM-DDTHH:MM:SS.sssZ
---
```

`mode` is almost always `agent`. Use `ask` only for read-only Q&A prompts.

## 2. Anatomy of a Good Prompt

```markdown
# <Title>

<Identity sentence: "You are <role>. When invoked with /<slug>, you …">

## 1. Intake (PLAN)
- Required inputs (ask once if missing)
- Optional inputs with defaults

## 2. Procedure (DO)
- Numbered, deterministic steps
- One canonical template/skeleton

## 3. Quality Gate (CHECK)
- Concrete checks (commands, checklists)
- Failure modes and recovery

## 4. Deliverable (ACT)
- What to return to the user
- Format requirements

## 5. Hard Rules
- Non-negotiables ("Never X", "Always Y")
```

## 3. Writing Rules

- **Imperative voice:** "Generate", "Validate", "Return" — not "you should consider".
- **One responsibility per prompt.** Split when a prompt tries to do more than one thing.
- **Single canonical example** per concept. No "Example 1, 2, 3" of the same idea.
- **No motivational filler.** Cut "comprehensive", "powerful", "leverage", "robust", "best-in-class".
- **No meta-prompts** ("As an AI…", "Think step by step about…"). Just give the steps.
- **Concrete over abstract:** show commands, file paths, exact field names.
- **Reference, don't duplicate:** link to instruction files for repo conventions instead of restating them.

## 4. Structure Patterns (use one)

| Pattern | When |
|---|---|
| **PDCA** (Plan/Do/Check/Act) | Multi-step workflows with quality gate |
| **Intake → Template → Output** | Code/content generators |
| **Audit → Report → Fix** | Validators, maintainers |
| **Q&A** | Read-only research / explanation |

Don't combine patterns. Pick one and stick to it.

## 5. Quality Checklist

Before merging a new or refined prompt:

- [ ] Frontmatter has all required keys (mode, description, date, lastmod)
- [ ] Description ≤160 chars and accurately states the trigger and outcome
- [ ] One clear identity sentence at the top
- [ ] Numbered procedure (not a wall of prose)
- [ ] At least one concrete example or template block
- [ ] Hard rules section with explicit don'ts
- [ ] No duplicate examples
- [ ] No generic AI-padding
- [ ] References sibling instruction files instead of restating them
- [ ] Tested end-to-end on a real input

## 6. Iteration (Kaizen)

When refining an existing prompt:

1. Identify the failure mode (vague output, hallucination, scope creep, slow).
2. Add the minimum constraint that fixes it (one rule, one example, one schema).
3. Remove anything the failure proved unnecessary.
4. Bump `lastmod`. Note the change in `CHANGELOG.md` if user-visible.

A prompt that works in one shot is better than a prompt with extensive scaffolding that *might* work.

## 7. Seven Wastes to Cut

| Waste | Symptom | Fix |
|---|---|---|
| Overproduction | Output longer than needed | Add length cap in deliverable section |
| Waiting | Multiple clarification rounds | Tighten intake checklist |
| Transportation | User must copy-paste between prompts | Combine or chain explicitly |
| Over-processing | Complex prompt for simple task | Use simpler pattern |
| Inventory | Unused prompt variants | Delete |
| Motion | Constant tweaking | Lock in canonical form |
| Defects | Bad output requiring rework | Add quality gate |

## 8. Tools Field

List only tools the prompt genuinely needs. Common values:

```
tools: [codebase, search, terminal, edit_file]
tools: [read_file, grep_search, file_search]
tools: [github, run_in_terminal]
```

Empty tools list → omit the key entirely.

## 9. Naming & Location

- `.github/prompts/<slug>.prompt.md` — kebab-case slug.
- Slug matches the invocation: `/<slug>`.
- One file per prompt; no `_v2`, `_new`, `_old`.

## 10. Hard Rules

- Never write a prompt longer than ~250 lines without strong justification.
- Never include three examples when one will do.
- Never preserve a section just because the previous version had it.
- Never produce a prompt that doesn't fit the four-section pattern in §2.

---

**Related:** [`../FRONTMATTER.md`](../FRONTMATTER.md) for schema · [`contributing.instructions.md`](contributing.instructions.md) for review flow.
