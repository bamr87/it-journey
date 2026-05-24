---
mode: agent
description: "Validate article and quest content against IT-Journey standards and frontmatter rules"
date: 2025-11-22T16:10:21.000Z
lastmod: 2026-05-23T00:00:00.000Z
---

# Validate Content Quality

Validate article and quest content against IT-Journey standards. For quests, [`.github/instructions/quest.instructions.md`](../instructions/quest.instructions.md) is the canonical reference.

## Run Validators

| Content | Command |
|---|---|
| Quest (single file) | `python3 test/quest-validator/quest_validator.py <path>` |
| Quest (directory) | `make quest-audit` |
| Quest (strict score) | `python3 test/quest-validator/quest_validator.py -d pages/_quests/ --fail-threshold 70 --summary` |
| Post / doc frontmatter | `python3 scripts/validation/frontmatter-validator.py <paths>` |
| Links | `python3 scripts/link-checker.py --scope website --timeout 30` |

## Quest Validation Criteria

### Errors (must fix)

- Missing required frontmatter fields (§1 in `quest.instructions.md`)
- `fmContentType` ≠ `quest` for playable content
- `permalink` does not match `quest_type` pattern
- Missing `## 🎯 Quest Objectives` section
- Code blocks without language tags
- Broken dependency URLs in `quest_dependencies` (network validator)
- Score below **70%**

### Warnings (should fix)

- Missing recommended fields (`quest_dependencies`, `rewards`, `validation_criteria`)
- No Mermaid quest-network diagram
- No multi-platform sections for OS-dependent topics
- Weak fantasy theme integration
- Placeholder brackets in prerequisites or dependencies
- Unquoted numeric tags in YAML

### Permalink checks

| `quest_type` | Expected pattern |
|---|---|
| `main_quest` | `/quests/XXXX/slug/` |
| `side_quest` | `/quests/XXXX/side-quests/slug/` |
| `bonus_quest` / `epic_quest` | `/quests/codex/slug/` |

Dependency URLs must be full canonical paths with trailing slashes.

## Article Validation

- Frontmatter completeness (30–60 title, 120–160 description)
- Learning objectives clarity
- Technical accuracy
- Code examples with language tags
- Accessibility (headings, alt text)

## Scoring

Quest scores come from `quest_validator.py`:

| Score | Status |
|---|---|
| 90–100% | Excellent — ready to publish |
| 80–89% | Good — optional polish |
| 70–79% | Acceptable — meets merge threshold |
| < 70% | **Failing — must fix before merge** |

Articles: 80+ excellent, 60–79 minor improvements, below 60 needs significant work.

## Output Format

Return a structured report:

1. **Summary** — pass/fail, score, file path
2. **Errors** — numbered, with fix instructions
3. **Warnings** — numbered, prioritized
4. **Commands run** — what was validated
5. **Next steps** — specific edits or `make quest-audit` if not yet run
