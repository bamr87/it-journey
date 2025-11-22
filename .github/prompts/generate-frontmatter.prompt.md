---
name: "Generate Frontmatter"
description: "Generate Jekyll frontmatter for posts or quests following IT-Journey standards"
version: "1.0.0"
category: "content-creation"
inputs:
  - content_type
  - title
  - description
outputs:
  - frontmatter
---

# Generate Jekyll Frontmatter

Create complete frontmatter for {{ inputs.content_type }} following IT-Journey standards.

**Title**: {{ inputs.title }}
**Description**: {{ inputs.description }}

## Frontmatter Requirements

### For Posts
- title, description, date, lastmod
- keywords (array of 5-10)
- categories (array)
- tags (array)
- author, version
- learning_objectives (array)
- target_audience (object with skill_level, prerequisites)

### For Quests
- All post fields PLUS:
- hierarchy (binary level path)
- level (binary format)
- quest_id
- difficulty (enum)
- estimated_time
- prerequisites (array)
- dependencies (array)

## Output Format

Return valid YAML frontmatter enclosed in triple dashes.
