---
mode: agent
description: "Expand an article outline with multi-platform code examples, explanations, and hands-on exercises"
date: 2025-11-22T16:10:21.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# Expand Content

Expand the outline into full content with technical depth and practical examples.

**Outline**: {{ inputs.outline }}
**Target Audience**: {{ inputs.target_audience }}
**Section guide**: {{ inputs.section_guide }} (optional — defaults to the post's folder)

## Brand context

Load the `brand-voice` skill for the resolved section (the `section_guide` input,
or the post's `pages/_posts/<category>/` folder). Expand in that voice profile:
honor the formality/emoji band, avoid the discouraged terms, use canonical
spellings, and keep the section's required structure (e.g. a **Verify** step for
devops/system-administration).

## Requirements

1. **Detailed Explanations**: Write complete paragraphs explaining each concept
2. **Multi-Platform Code**: Provide examples for macOS, Linux, Windows, Cloud
3. **Hands-On Exercises**: Include step-by-step exercises readers can follow
4. **Troubleshooting**: Add common issues and solutions
5. **Best Practices**: Include security, performance, and production considerations
6. **On-brand voice**: Match the resolved section profile (see `_data/brand/voice.md`)

## Output Format

Return complete expanded content ready for publication.
