---
name: "Refine Content"
description: "Refine quest content with implementation challenges, Mermaid diagrams, and validation criteria"
version: "1.0.0"
category: "content-creation"
inputs:
  - quest_outline
  - article_content
outputs:
  - refined_quest
  - mermaid_diagrams
---

# Refine Quest Content

Enhance the quest with rich implementation details, visual diagrams, and validation.

**Quest Outline**: {{ inputs.quest_outline }}
**Related Article**: {{ inputs.article_content }}

## Requirements

1. **Implementation Challenges**: Add specific coding challenges with acceptance criteria
2. **Mermaid Diagrams**: Create flowcharts, sequence diagrams, or quest maps
3. **Validation Criteria**: Define how learners validate their progress
4. **Boss Battle**: Add a comprehensive final challenge
5. **Rewards**: Define skills and knowledge gained

## Output Format

Return enhanced quest content with embedded Mermaid diagrams.
