---
name: "Expand Content"
description: "Expand content with detailed explanations, multi-platform code examples, and hands-on exercises"
version: "1.0.0"
category: "content-creation"
inputs:
  - outline
  - target_audience
outputs:
  - expanded_content
  - code_examples
---

# Expand Content

Expand the outline into full content with technical depth and practical examples.

**Outline**: {{ inputs.outline }}
**Target Audience**: {{ inputs.target_audience }}

## Requirements

1. **Detailed Explanations**: Write complete paragraphs explaining each concept
2. **Multi-Platform Code**: Provide examples for macOS, Linux, Windows, Cloud
3. **Hands-On Exercises**: Include step-by-step exercises readers can follow
4. **Troubleshooting**: Add common issues and solutions
5. **Best Practices**: Include security, performance, and production considerations

## Output Format

Return complete expanded content ready for publication.
