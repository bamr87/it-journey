# Quest Quality Checklist - Quick Reference

*Use this checklist when creating or updating quests to ensure high quality*

## ✅ Required Frontmatter (17 points)

### Basic Information
- [ ] `title` - Clear, action-oriented (< 60 chars for SEO)
- [ ] `description` - Complete description (150-300 chars)
- [ ] `date` - ISO 8601 format (YYYY-MM-DDTHH:MM:SS.000Z)
- [ ] `preview` - Image path
- [ ] `author` - Quest creator name
- [ ] `layout` - Should be "journals"
- [ ] `permalink` - Start with `/quests/level-XXXX-name/`
- [ ] `fmContentType` - Should be "quest"

### Quest Classification
- [ ] `level` - 4-digit binary (0000-1111)
- [ ] `difficulty` - One of: 🟢 Easy, 🟡 Medium, 🔴 Hard, ⚔️ Epic
- [ ] `estimated_time` - Format: "XX-XX minutes" or "X-X hours"
- [ ] `primary_technology` - Main tech focus
- [ ] `quest_type` - E.g., tool-mastery, language-learning
- [ ] `skill_focus` - E.g., frontend, backend, testing
- [ ] `learning_style` - E.g., hands-on, conceptual
- [ ] `quest_series` - Series name or "Standalone Quest"

### Metadata
- [ ] `tags` - Include level tag (lvl-XXXX) + relevant tags
- [ ] `categories` - [Quests, Tech-Category, Skill-Level]
- [ ] `keywords` - primary and secondary keywords

## 🌟 Enhanced Fields (8 points)

- [ ] `quest_line` - Campaign/storyline name
- [ ] `quest_arc` - Story arc or thematic grouping
- [ ] `prerequisites` - Knowledge, system, skill requirements
- [ ] `quest_dependencies` - Recommended/unlocked quests
- [ ] `quest_relationships` - Parent/child/parallel/sequel quests
- [ ] `learning_paths` - Primary paths and character classes
- [ ] `rewards` - Badges, skills, progression points
- [ ] `validation_criteria` - Completion requirements

## 📝 Content Structure (9 points)

- [ ] **Opening** - Fantasy-themed introduction
- [ ] **Legend** - Explain why this quest matters
- [ ] **🎯 Quest Objectives** - Clear learning outcomes
- [ ] **🗺️ Prerequisites** - Required knowledge and systems
- [ ] **🌍 Platform Instructions** - macOS, Windows, Linux paths
- [ ] **Chapters** - Progressive learning sections
- [ ] **🎮 Challenges** - Implementation exercises
- [ ] **✅ Completion Verification** - Achievement checklist
- [ ] **🏆 Rewards** - Next steps and resources

## 💻 Code Quality (5 points)

- [ ] All code blocks have language specification
  ```python
  # Good - has "python" specification
  ```
  
  ```
  # Bad - no language specification
  ```

## ✨ Interactivity (5 points)

- [ ] Interactive checkboxes throughout
- [ ] Knowledge checks after chapters
- [ ] Progress tracking elements
- [ ] Engagement prompts

Examples:
- [ ] Can you explain this concept?
- [ ] What would happen if...?
- [ ] Try implementing...

## 🧙‍♂️ Fantasy Theme (10 points)

Use gamification language throughout:
- ⚔️ Skills, spells, quests, adventures
- 🏰 Towers, realms, kingdoms, territories
- 🧙‍♂️ Wizards, masters, heroes, champions
- 🏆 Badges, achievements, rewards
- ✨ Magic, enchantments, powers
- 🗺️ Paths, journeys, expeditions

Fantasy element checklist:
- [ ] Opening uses adventure language
- [ ] Objectives framed as quest goals
- [ ] Chapter titles use fantasy themes
- [ ] Rewards described as achievements
- [ ] Consistent emoji usage
- [ ] Engaging narrative voice

## 📱 Accessibility (3 points)

- [ ] All images have descriptive alt text
- [ ] Clear heading hierarchy
- [ ] Descriptive link text (not "click here")
- [ ] Inclusive language throughout
- [ ] Multi-platform support

## 📚 Citations (5 points)

- [ ] References section included
- [ ] Official documentation linked
- [ ] Academic sources cited
- [ ] Tutorial resources provided

Example structure:
```markdown
### 📚 Further Study and Resources

**Official Documentation**:
- [Tool Documentation](https://example.com/docs)

**Academic Resources**:
- [University Course](https://example.edu/course)

**Tutorials**:
- [Community Guide](https://example.com/guide)
```

## 🎯 Target Scores

- **Minimum Passing**: 70% (52.5 / 75 points)
- **Good Quality**: 80% (60 / 75 points)
- **Excellent Quality**: 90% (67.5 / 75 points)
- **Perfect Quest**: 100% (75 / 75 points)

## 🚀 Quick Validation Commands

```bash
# Validate your quest (from project root)
docker-compose run --rm quest-validator \
    /opt/venv/bin/python /app/test/quest-validator/quest_validator.py \
    /app/pages/_quests/your-quest.md

# Verbose output for details
docker-compose run --rm quest-validator \
    /opt/venv/bin/python /app/test/quest-validator/quest_validator.py \
    /app/pages/_quests/your-quest.md -v

# Generate report
docker-compose run --rm quest-validator \
    /opt/venv/bin/python /app/test/quest-validator/quest_validator.py \
    /app/pages/_quests/your-quest.md \
    --report /app/test/quest-validator/report.json

# Run full test suite
./test/quest-validator/test-validator.sh
```

## 🔧 Common Issues & Fixes

### Issue: Low Code Quality Score
**Fix**: Add language specifications to all code blocks
```markdown
```python  ← Add this
def example():
    pass
\```
```

### Issue: Missing Enhanced Fields
**Fix**: Add quest hierarchy to frontmatter
```yaml
quest_line: "Your Campaign Name"
quest_arc: "Story Arc"
quest_dependencies:
    recommended_quests:
        - "Prerequisite Quest"
```

### Issue: Low Fantasy Theme Score
**Fix**: Use more gamification language
- Change "Learn" → "Master" or "Forge"
- Change "Tutorial" → "Quest" or "Adventure"
- Change "Complete" → "Conquer" or "Achieve"
- Add emoji indicators (🎯⚔️🏆✨)

### Issue: No Interactive Elements
**Fix**: Add checkboxes throughout
```markdown
- [ ] Can you explain the concept?
- [ ] Have you tested your code?
- [ ] Did you document your work?
```

## 📋 Pre-Submission Checklist

Before submitting your quest:

1. [ ] Run validator and check score (aim for 90%+)
2. [ ] Fix all errors (critical issues)
3. [ ] Address warnings when possible
4. [ ] Test all code examples
5. [ ] Verify multi-platform instructions
6. [ ] Check spelling and grammar
7. [ ] Ensure fantasy theme consistency
8. [ ] Add citations and references
9. [ ] Include completion criteria
10. [ ] Request peer review

## 🎓 Quality Philosophy

**Remember**: High-quality quests create better learning experiences!

- ✨ **Engage** - Use fantasy themes and interactivity
- 📚 **Educate** - Provide clear, progressive learning
- 🌍 **Include** - Support all platforms and skill levels
- 🎯 **Validate** - Ensure measurable outcomes
- 🔗 **Connect** - Link to broader learning paths

---

*For detailed documentation, see: [Quest Validator README](README.md)*

**Happy Quest Crafting!** 🧙‍♂️✨
