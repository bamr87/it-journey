# Quest Validator - IT-Journey Quest Testing Framework

**Version**: 1.0.0  
**Author**: IT-Journey Team  
**Created**: 2025-10-08

## Overview

The Quest Validator is a comprehensive testing framework designed to validate IT-Journey quest files against established standards. It ensures quest quality, consistency, and adherence to the gamified learning experience guidelines.

## Features

### ✅ Comprehensive Validation

- **Frontmatter Validation**: Checks all required and enhanced fields
- **Structure Analysis**: Validates quest content organization
- **Code Quality**: Ensures code blocks have language specifications
- **Accessibility**: Verifies alt text and inclusive design
- **Gamification**: Validates fantasy theme integration
- **Educational Standards**: Checks learning objectives and progression
- **Citations**: Ensures proper referencing of external resources

### 📊 Quality Scoring

Each quest receives a quality score based on:
- Required field completeness (40%)
- Enhanced hierarchy fields (20%)
- Content structure (15%)
- Code quality (10%)
- Fantasy theme integration (10%)
- Accessibility (5%)

### 🎯 Validation Categories

1. **Critical Errors**: Must be fixed for quest to pass
2. **Warnings**: Should be addressed for optimal quality
3. **Info**: Additional insights about quest quality

## Installation

### Prerequisites

- Docker and Docker Compose
- Access to the IT-Journey repository

### Setup

The quest validator is now containerized and runs within Docker. No local Python installation is required.

```bash
# Navigate to the project root
cd /path/to/it-journey

# Build the Docker image with quest validation support
docker-compose build quest-validator

# Verify the setup
docker-compose run --rm quest-validator python3 --version
```

## Usage

### Validate a Single Quest

```bash
docker-compose run --rm quest-validator \
    /opt/venv/bin/python /app/test/quest-validator/quest_validator.py \
    /app/pages/_quests/your-quest.md
```

### Validate All Quests in a Directory

```bash
docker-compose run --rm quest-validator \
    /opt/venv/bin/python /app/test/quest-validator/quest_validator.py \
    -d /app/pages/_quests/
```

### Verbose Output (Detailed Information)

```bash
docker-compose run --rm quest-validator \
    /opt/venv/bin/python /app/test/quest-validator/quest_validator.py \
    -d /app/pages/_quests/ -v
```

### Generate JSON Report

```bash
docker-compose run --rm quest-validator \
    /opt/venv/bin/python /app/test/quest-validator/quest_validator.py \
    -d /app/pages/_quests/ \
    --report /app/test/quest-validator/quest_report.json
```

### Custom File Pattern

```bash
docker-compose run --rm quest-validator \
    /opt/venv/bin/python /app/test/quest-validator/quest_validator.py \
    -d /app/pages/_quests/ \
    --pattern "*recursive*.md"
```

### Run the Full Test Suite

```bash
# Navigate to the project root
cd /path/to/it-journey

# Run the comprehensive test suite
./test/quest-validator/test-validator.sh
```

## Example Output

```
============================================================
Validating: recursive-realms-testing.md
============================================================
ℹ️  Validating required frontmatter fields...
ℹ️  Validating quest hierarchy fields...
ℹ️  Level 0010 (decimal: 2) valid
ℹ️  Difficulty 🟡 Medium valid
✅ Found: Quest Objectives section
✅ All 5 code blocks have language specification
✅ Found 15 interactive checkboxes for learner engagement
✅ Strong fantasy theme integration (score: 5/6)

============================================================
Quest: recursive-realms-testing.md
============================================================
✅ PASSED - Excellent quest quality!

📊 Quality Score: 95/100 (95.0%)

⚠️  Warnings (2):
   • Missing enhanced field: quest_dependencies
   • No citations/references section found

============================================================
VALIDATION SUMMARY
============================================================
Total Quests:     1
Passed:           1 ✅
Failed:           0 ❌
Total Errors:     0
Total Warnings:   2
Average Score:    95.0%
============================================================
```

## Validation Rules

### Required Frontmatter Fields

These fields MUST be present:
- `title` - Quest title (preferably under 60 chars for SEO)
- `description` - Complete description (150-300 chars)
- `date` - Publication date (ISO 8601 format)
- `level` - Binary level indicator (4 digits, e.g., "0010")
- `difficulty` - One of: 🟢 Easy, 🟡 Medium, 🔴 Hard, ⚔️ Epic
- `estimated_time` - Format: "XX-XX minutes" or "X-X hours"
- `primary_technology` - Main technology focus
- `quest_type` - Type: tool-mastery, language-learning, etc.
- `skill_focus` - Primary skill category
- `learning_style` - Teaching approach: hands-on, conceptual, etc.
- `quest_series` - Series or standalone
- `author` - Quest creator
- `layout` - Jekyll layout (usually "journals")
- `keywords` - Primary and secondary keywords
- `permalink` - URL path (must start with /quests/)
- `fmContentType` - Should be "quest"

### Enhanced Quest Hierarchy Fields

Recommended for better organization:
- `quest_line` - Campaign/storyline name
- `quest_arc` - Story arc or thematic grouping
- `prerequisites` - Knowledge, system, and skill requirements
- `quest_dependencies` - Required, recommended, and unlocked quests
- `quest_relationships` - Parent, child, parallel, and sequel quests
- `learning_paths` - Primary paths and character classes
- `rewards` - Badges, skills, progression points
- `validation_criteria` - Completion requirements

### Content Structure Requirements

Recommended sections:
- **🌟 The Legend Behind This Quest** - Opening context
- **🎯 Quest Objectives** - Clear learning outcomes
- **🗺️ Quest Prerequisites** - Required knowledge/setup
- **🌍 Choose Your Adventure Platform** - Multi-platform support
- **Chapters** - Progressive learning content
- **🎮 Quest Implementation Challenges** - Hands-on practice
- **Citations/References** - External resources

### Level Format

- Must be 4-digit binary: 0000-1111
- Represents difficulty progression
- Examples:
  - `0000` (0) - Tutorial/Introduction
  - `0001` (1) - Beginner
  - `0010` (2) - Novice/Apprentice
  - `0101` (5) - Intermediate
  - `1000` (8) - Advanced
  - `1111` (15) - Master/Expert

### Permalink Structure

- Must start with `/quests/`
- Should include level indicator: `/quests/level-0010-descriptive-name/`
- Use kebab-case for readability

## Integration with CI/CD

### GitHub Actions Workflow

Create `.github/workflows/validate-quests.yml`:

```yaml
name: Validate Quests

on:
  push:
    paths:
      - 'pages/_quests/**/*.md'
  pull_request:
    paths:
      - 'pages/_quests/**/*.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          cd test/quest-validator
          pip install -r requirements.txt
      
      - name: Validate quests
        run: |
          python test/quest-validator/quest_validator.py \
            -d pages/_quests/ \
            --report quest-validation-report.json
      
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: quest-validation-report
          path: quest-validation-report.json
```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Validate quests before committing

echo "🔍 Validating quest files..."

# Find changed quest files
QUEST_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep 'pages/_quests/.*\.md$')

if [ -n "$QUEST_FILES" ]; then
    for file in $QUEST_FILES; do
        python test/quest-validator/quest_validator.py "$file"
        if [ $? -ne 0 ]; then
            echo "❌ Quest validation failed for: $file"
            echo "   Fix errors before committing"
            exit 1
        fi
    done
    echo "✅ All quests validated successfully"
fi

exit 0
```

## Development

### Adding New Validation Rules

1. Add validation method to `QuestValidator` class:

```python
def validate_custom_rule(self, fm: Dict, body: str, result: ValidationResult):
    """Validate custom requirement"""
    self.log_info("Validating custom rule...")
    
    # Your validation logic
    if some_condition:
        result.score += points
        result.info.append("Custom validation passed")
    else:
        result.warnings.append("Custom validation warning")
    
    result.max_score += points
```

2. Call it in `validate_quest_file` method:

```python
self.validate_custom_rule(frontmatter, body, result)
```

### Testing the Validator

```bash
# Test with the sample quest
python quest_validator.py pages/_quests/testing-quests-with-recurrisive-questing.md -v

# Test with all quests
python quest_validator.py -d pages/_quests/ -v

# Generate test report
python quest_validator.py -d pages/_quests/ --report test-report.json
```

## Troubleshooting

### YAML Parsing Errors

**Issue**: "YAML parsing error: ..."

**Solution**: Check frontmatter syntax:
- Ensure all strings with colons are quoted
- Verify proper indentation (use spaces, not tabs)
- Check for unmatched brackets or quotes

### Missing Dependencies

**Issue**: "Import 'yaml' could not be resolved"

**Solution**: Install requirements:
```bash
pip install -r requirements.txt
```

### File Not Found

**Issue**: "❌ File not found: ..."

**Solution**: Use correct path:
```bash
# Absolute path
python quest_validator.py /full/path/to/quest.md

# Relative path from project root
python quest_validator.py pages/_quests/quest-name.md
```

## Best Practices

### For Quest Authors

1. **Run Validator Before Committing**: Always validate your quest
2. **Aim for 90%+ Score**: Strive for excellence in quest quality
3. **Address All Errors**: Fix critical errors immediately
4. **Review Warnings**: Address warnings when possible
5. **Use Verbose Mode**: Learn from detailed feedback

### For Reviewers

1. **Check Validation Report**: Review automated validation results
2. **Test Interactive Elements**: Verify checkboxes and challenges work
3. **Verify Learning Outcomes**: Ensure objectives are measurable
4. **Check Platform Coverage**: Confirm multi-platform support
5. **Assess Fantasy Theme**: Evaluate gamification effectiveness

## Future Enhancements

- [ ] Spell check integration
- [ ] Link validation (check broken links)
- [ ] Code execution testing
- [ ] Difficulty calibration analysis
- [ ] Learning path consistency checking
- [ ] Automated prerequisite verification
- [ ] Interactive web dashboard
- [ ] Integration with quest analytics

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the IT-Journey open-source initiative. See the main repository LICENSE file for details.

## Support

For questions or issues:
- Open an issue on GitHub
- Contact the IT-Journey Team
- Check the main documentation

---

*"Testing quests recursively to ensure quality through self-validating patterns."* 🧙‍♂️✨
