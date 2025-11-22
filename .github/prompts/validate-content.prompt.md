---
name: "Validate Content"
description: "Validate article and quest content against IT-Journey standards"
version: "1.0.0"
category: "quality-assurance"
inputs:
  - article_content
  - article_frontmatter
  - quest_content
  - quest_frontmatter
outputs:
  - validation_report
  - article_score
  - quest_score
---

# Validate Content Quality

Validate both article and quest content against IT-Journey educational standards.

## Validation Criteria

### Article Validation
- Frontmatter completeness and correctness
- Learning objectives clarity and measurability
- Technical accuracy
- Code examples tested and working
- Multi-platform coverage
- Accessibility (headings, alt text, clear language)

### Quest Validation
- All article criteria PLUS:
- Fantasy theme integration
- Binary level format correct
- Quest objectives clear and achievable
- Challenges appropriately difficult
- Mermaid diagrams present and valid
- Validation criteria defined

## Scoring

Return scores out of 100 for both article and quest.
- 80-100: Excellent, ready to publish
- 60-79: Good, minor improvements needed
- Below 60: Needs significant work

## Output Format

Return detailed validation report with specific issues and recommendations.
