---
mode: agent
description: "Audit posts for brand/voice drift: run the CMS brand check and report banned terms, spellings, emoji, structure, and formality issues by section"
date: 2026-06-21T00:00:00.000Z
lastmod: 2026-06-21T00:00:00.000Z
---

# Brand Audit

Read-only reporter for **brand/voice drift** across posts. It runs the CMS engine's
brand check and surfaces what drifted, grouped by section. It does **not** rewrite
content — fixing is a separate, reviewed step (the `brand-voice` skill or
`cms-curator`).

Brand rules live in `_data/brand/` (facts) and `.cms/config.yml › brand`
(thresholds). Drift is **advisory**: it never affects the health score and never
blocks CI.

## Operating Protocol

1. **Refresh the index + report:**

```bash
make cms-all     # or: python3 scripts/cms/cms.py all
```

2. **Read the drift.** Two sources, same data:
   - `.cms/reports/<date>.md` → the **Brand drift by section (advisory)** table and
     the `brand_drift` row in **Top issue types**.
   - `.cms/index/content-index.json` → per-file `issues` where
     `kind` starts with `brand_drift:` (also `section_guide` / `voice_profile`
     fields show how each post resolved).

3. **Optionally scope** to a single file or section the user names; otherwise audit
   all posts.

## What the `brand_drift:*` kinds mean

| kind | meaning | fix |
|---|---|---|
| `brand_drift:banned_term` | empty-hype word (powerful, seamless, …) | rephrase / drop |
| `brand_drift:preferred_term` | non-canonical spelling (Github → GitHub) | use canonical form |
| `brand_drift:emoji_intensity` | emoji count outside the section band | trim / add structure |
| `brand_drift:missing_structural` | required element absent (e.g. Verify for devops) | add the element |
| `brand_drift:length` | outside the format's word band (muses) | tighten / expand |
| `brand_drift:formality` | tone far from the section target (heuristic) | adjust voice (advisory) |
| `brand_drift:guide_unresolved` | `section_guide`/`voice_profile` names an unknown slug/profile | fix the frontmatter |

## Output Format

```markdown
## Brand Audit — <date>

**Posts audited:** N   **Posts with drift:** M   **Total drift issues:** K

### By section
| Section | Profile | Drift issues | Top kinds |
|---|---|---|---|
| devops | practitioner-chronicle | 24 | banned_term, missing_structural |
| … |

### Notable items (top 10 by issue count)
- `pages/_posts/<...>.md` (section, profile) — <kind: message>; <kind: message>

### Recommendation
<1–3 lines: which sections need attention; whether to dispatch `brand-voice` or
queue items for `cms-curator`. Note this is advisory — nothing is blocking.>
```

## Hard Rules

- **Read-only.** Never edit content or frontmatter from this prompt.
- Report exactly what the engine found; do not infer drift the engine didn't flag.
- If `brand.enabled` is `false` in `.cms/config.yml`, say so and stop — there is
  nothing to audit.

---

**Related:** [`.claude/skills/brand-voice/SKILL.md`](../../.claude/skills/brand-voice/SKILL.md) · [`validate-content.prompt.md`](validate-content.prompt.md) · brand store at `_data/brand/`.
