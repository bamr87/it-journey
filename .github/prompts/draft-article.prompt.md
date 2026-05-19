---
mode: agent
description: "Generate IT-education article outline with learning objectives, target audience, and Kaizen structure"
date: 2025-11-22T16:10:21.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# Draft Article

Generate a complete IT-Journey article outline (post or doc) ready for human prose. Front matter compliant with [`posts.instructions.md`](../instructions/posts.instructions.md), structure follows Kaizen pedagogy.

## Intake (PLAN)

Ask only what's missing:

- **Topic** (1-line)
- **Target audience** — `beginner | intermediate | advanced`
- **Learning objectives** — 3-5 verbs ("install…", "configure…", "deploy…")
- **Platform scope** — `macos | linux | windows | docker | cloud | all`
- **Article category** — `feature-implementation | debugging | process-improvement | infrastructure | learning-journey`
- **Estimated time** to complete (reader)

Default to `intermediate` and `all platforms` if user says "default".

## Operating Protocol (DO)

### 1. Generate Front Matter

```yaml
---
title: "<60-char compelling title>"
description: "<120-160 char SEO summary>"
date: <today ISO>
lastmod: <today ISO>
permalink: /posts/<kebab-slug>/
categories: [<primary>, <secondary>]
tags: [<3-7 tags>]
author: bamr87
excerpt: "<1-2 sentence preview>"
learning_objectives:
  - "<verb> <thing>"
  - "<verb> <thing>"
target_audience:
  skill_level: <beginner|intermediate|advanced>
  prerequisites:
    - "<prereq>"
estimated_time: "<X> minutes"
draft: true
---
```

### 2. Generate Outline

```markdown
# <Title>

## TL;DR
<3-sentence summary: problem, approach, outcome>

## Why This Matters
<1-2 paragraphs: real-world context, who benefits>

## Prerequisites
- <skill/tool>
- <skill/tool>

## What You'll Build
<concrete deliverable + screenshot/diagram placeholder>

## Step 1: <Action Verb> <Thing>
<intent in 1 sentence>

```<lang>
# command or code
```

**Verify:**
```bash
# expected output check
```

## Step 2: <Action Verb> <Thing>
…

## Step 3: <Action Verb> <Thing>
…

## Platform Notes
- **macOS:** <delta>
- **Linux:** <delta>
- **Windows / WSL:** <delta>
- **Docker:** <delta>

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| … | … | … |

## Validation Checklist
- [ ] <observable outcome 1>
- [ ] <observable outcome 2>

## What You Learned
<3-5 bullets mapping back to learning_objectives>

## Next Steps
- Related quest: [<title>](path)
- Related post: [<title>](path)
- Deeper dive: <external link>

## References
- <official docs>
- <related IT-Journey content>
```

### 3. Section Count Guidance

| Article category | Step sections | Total length |
|---|---|---|
| feature-implementation | 4-7 | 1500-3000 words |
| debugging | 3-5 (problem → diagnosis → fix → prevent) | 1000-2000 |
| process-improvement | 3-4 (before → change → after → metrics) | 1200-2000 |
| infrastructure | 5-8 | 2000-4000 |
| learning-journey | 4-6 (chronological) | 1500-2500 |

## Quality Checklist (CHECK)

Before returning to user:

- [ ] Front matter passes validation rules (title 30-60, description 120-160, lists not strings)
- [ ] `learning_objectives` are action verbs, measurable
- [ ] Every step has a verify/expected-output block
- [ ] Code blocks specify language
- [ ] Nested fenced blocks use longer outer fences
- [ ] No literal secrets in examples (use `${env:TOKEN}` placeholders)
- [ ] Platform notes present if scope > 1 platform
- [ ] Cross-links to ≥ 1 related quest/post
- [ ] Permalink follows `/posts/<slug>/` (required if non-post content will link here)

## Kaizen Hook (ACT)

After draft delivered, suggest:

```
Next:
1. Human writes prose into the outline.
2. Run /commit-publish when done.
3. After publication, run /retrospective if any reusable lessons emerged.
```

## Output Format

Return exactly:

```markdown
## Draft Created

**File:** `pages/_posts/<YYYY-MM-DD-slug>.md` (not yet written — preview below)

**Front matter validation:** ✅
**Outline sections:** N
**Estimated reader time:** N min
**Target audience:** <level>

---

<full file content here>

---

**Next:** User authors prose into outline → `/commit-publish`
```

Do **not** write the file to disk unless user confirms.

## Hard Rules

- Never invent learning objectives — derive from user input.
- Never set `draft: false` on first generation.
- Never skip the validation checklist.
- Never use generic stock examples — tailor to user's topic.

---

**Related:** [`.github/instructions/posts.instructions.md`](../instructions/posts.instructions.md) · [`.github/prompts/kaizen.prompt.md`](kaizen.prompt.md)
