---
name: "Draft Article Outline"
description: "Generate a comprehensive article outline with learning objectives"
version: "1.0.0"
category: "content-creation"
inputs:
  - topic
  - level
  - difficulty
outputs:
  - article_outline
  - learning_objectives
  - target_audience
---

# Draft Article Outline

Create a comprehensive outline for an IT education article on the topic: {{ inputs.topic }}

**Target Level**: {{ inputs.level }}
**Difficulty**: {{ inputs.difficulty }}

## Requirements

1. **Article Outline**: Create a detailed outline with:
   - Introduction (hook, context, what readers will learn)
   - Main sections (3-5 sections covering key concepts)
   - Code examples placeholders
   - Hands-on exercises
   - Conclusion with next steps

2. **Learning Objectives**: Define 3-5 specific, measurable learning objectives
   - Use action verbs (understand, implement, configure, deploy)
   - Focus on practical skills
   - Align with the target level

3. **Target Audience**: Define the ideal reader
   - Prerequisites knowledge
   - Skill level
   - Use cases and motivation

## Output Format

Return structured content with clear sections for each output.
