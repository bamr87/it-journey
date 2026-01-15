# Quest Templates and Tools

This directory contains templates and tools for creating and managing quests in the IT-Journey quest system.

## Templates

### Main Quest Template
**File**: `main-quest-template.md`

Comprehensive template for main storyline quests. Includes:
- Complete frontmatter with all required and optional fields
- Quest network positioning diagrams
- Multi-platform implementation paths (macOS, Windows, Linux, Cloud)
- Progressive learning chapters (3+ chapters)
- Hands-on mastery challenges (Novice, Intermediate, Advanced)
- Rewards and achievement systems
- Resource library and next steps

**Use for**: Core learning path quests that advance the main storyline.

### Level README Template
**File**: `level-readme-template.md`

Standard template for level directory README files. Includes:
- Level overview and positioning
- Complete quest listings (main, side, bonus)
- Quest network map with Mermaid diagrams
- Character class progression paths
- Prerequisites and unlocks
- Resources and tools for the level

**Use for**: Creating or updating level directory README files.

### Side Quest Template (Coming Soon)
**File**: `side-quest-template.md` (Planned)

Template for optional learning adventures that enhance skills without being required for progression.

### Bonus Quest Template (Coming Soon)
**File**: `bonus-quest-template.md` (Planned)

Template for advanced challenges and mastery demonstrations.

## Tools

### Quest Generation Script
**File**: `../scripts/quest/generate-placeholder-quest.sh`

Automated script to create placeholder quest files from templates.

**Usage**:
```bash
./scripts/quest/generate-placeholder-quest.sh <level> <quest-slug> "<quest-title>" [options]
```

**Examples**:
```bash
# Create a basic quest
./scripts/quest/generate-placeholder-quest.sh 0110 database-design-fundamentals "Database Design Fundamentals"

# Create with additional options
./scripts/quest/generate-placeholder-quest.sh 0110 sql-sorcery "SQL Sorcery" \
  --difficulty medium \
  --time "45-60 minutes" \
  --tech sql \
  --skill data-engineering

# Dry run to preview
./scripts/quest/generate-placeholder-quest.sh 1101 ml-fundamentals "ML Fundamentals" --dry-run
```

**Options**:
- `--difficulty`: easy, medium, hard, epic (default: easy)
- `--type`: main_quest, side_quest, bonus_quest (default: main_quest)
- `--time`: Estimated time (e.g., "30-45 minutes")
- `--tech`: Primary technology (e.g., docker, react, python)
- `--skill`: Skill focus (e.g., frontend, backend, devops)
- `--dry-run`: Preview without creating files

### Quest Network Validator
**File**: `../scripts/quest/validate-quest-network.py`

Python script to validate quest network integrity.

**Usage**:
```bash
python3 scripts/quest/validate-quest-network.py
```

**Checks**:
- ✅ Required frontmatter fields present
- ✅ Quest dependencies exist
- ✅ No circular dependencies
- ✅ Identifies orphaned quests
- ✅ Validates quest relationships
- ✅ Generates comprehensive report

**Output**:
- Quest statistics (total, complete, placeholder, draft)
- List of errors (broken dependencies, missing fields)
- List of warnings (orphaned quests, invalid formats)
- Overall validation status (pass/fail)

## Quick Start Guide

### Creating a New Quest

1. **Plan your quest**:
   - Determine level (binary format: 0000-1111)
   - Choose quest type (main, side, or bonus)
   - Define difficulty and estimated time
   - Identify technologies and skills covered

2. **Generate placeholder**:
   ```bash
   ./scripts/quest/generate-placeholder-quest.sh 0110 my-quest-slug "My Quest Title" \
     --difficulty medium --tech python --skill backend
   ```

3. **Edit the generated file**:
   - Fill in the description and learning objectives
   - Add multi-platform implementation details
   - Create hands-on challenges
   - Define prerequisites and unlocks
   - Add resources and documentation links

4. **Update level README**:
   - Add quest to appropriate section
   - Update quest network diagram
   - Include in character class paths

5. **Validate the quest network**:
   ```bash
   python3 scripts/quest/validate-quest-network.py
   ```

6. **When complete**:
   - Set `draft: false` in frontmatter
   - Update home.md and main README.md
   - Create git commit with conventional format

### Creating a New Level

1. **Create level directory**:
   ```bash
   mkdir -p pages/_quests/XXXX  # Replace XXXX with binary level
   ```

2. **Generate level README**:
   ```bash
   cp pages/_quests/templates/level-readme-template.md pages/_quests/XXXX/README.md
   ```

3. **Customize level README**:
   - Fill in level details
   - Define core objectives
   - List planned quests
   - Create quest network diagram

4. **Generate quests for the level**:
   ```bash
   ./scripts/quest/generate-placeholder-quest.sh XXXX quest-1-slug "Quest 1 Title"
   ./scripts/quest/generate-placeholder-quest.sh XXXX quest-2-slug "Quest 2 Title"
   # ... etc
   ```

## Template Customization

### Frontmatter Fields

**Required Fields** (all quests must have):
- `title`: Quest title
- `description`: SEO-friendly description (150-300 chars)
- `level`: Binary level (e.g., "0110")
- `difficulty`: 🟢 Easy | 🟡 Medium | 🔴 Hard | ⚔️ Epic
- `estimated_time`: Time estimate (e.g., "30-45 minutes")
- `quest_type`: main_quest | side_quest | bonus_quest
- `permalink`: URL path for the quest

**Recommended Fields**:
- `quest_dependencies`: Prerequisites and unlocks
- `quest_relationships`: Parent, child, parallel, sequel quests
- `learning_paths`: Character class alignment
- `rewards`: Badges, skills, XP
- `validation_criteria`: Completion requirements

**Optional Fields**:
- `quest_line`: Campaign/storyline name
- `quest_arc`: Story arc grouping
- `quest_mapping`: Position on quest map
- `primary_technology`: Main tech focus
- `skill_focus`: Skill category

### Content Structure

Each quest should include:

1. **Epic Introduction** - Fantasy-themed opening
2. **Quest Network Position** - Mermaid diagram
3. **Quest Objectives** - Primary, Secondary, Mastery
4. **Prerequisites** - Knowledge, System, Skill Level
5. **Multi-Platform Paths** - macOS, Windows, Linux, Cloud
6. **Learning Chapters** (3-5):
   - Skills to forge
   - Step-by-step implementation
   - Knowledge checks
   - Quick wins and checkpoints
7. **Mastery Challenges** (3):
   - Novice (🟢)
   - Intermediate (🟡)
   - Advanced (🔴)
8. **Rewards & Achievements**
9. **Next Steps & Quest Network**
10. **Resource Library**

## Best Practices

### Quest Design

1. **Clear Learning Objectives**: Be specific and measurable
2. **Progressive Difficulty**: Build from simple to complex
3. **Hands-On Practice**: Include practical implementations
4. **Multi-Platform**: Cover macOS, Windows, Linux, Cloud where applicable
5. **Fantasy Theme**: Maintain RPG language and metaphors
6. **Validation Criteria**: Define clear success metrics

### Frontmatter Standards

1. **Complete Metadata**: Fill all required fields
2. **Accurate Dependencies**: Link to actual quest permalinks
3. **Proper Formatting**: Follow YAML syntax strictly
4. **Consistent Naming**: Use kebab-case for slugs
5. **Draft Status**: Set `draft: true` until complete

### Quest Network

1. **No Orphans**: Every quest should be referenced
2. **Clear Progression**: Define prerequisites and unlocks
3. **No Circular Deps**: Avoid circular dependencies
4. **Character Alignment**: Map to character classes
5. **Level Coherence**: Quests should fit level theme

## Validation Checklist

Before marking a quest complete:

- [ ] All required frontmatter fields present
- [ ] Quest network position diagram included
- [ ] All prerequisites listed and linked
- [ ] All unlocked quests listed and linked
- [ ] Multi-platform instructions present
- [ ] At least 2 hands-on challenges defined
- [ ] Learning objectives clearly stated
- [ ] Validation criteria specified
- [ ] Fantasy theme integrated throughout
- [ ] Resources section populated
- [ ] Level README updated
- [ ] home.md updated
- [ ] Main README.md updated
- [ ] All internal links validated
- [ ] Validation script passes

## Contributing

When creating new templates or improving existing ones:

1. Follow existing template structure
2. Include comprehensive comments
3. Test with generation script
4. Update this README
5. Submit PR with examples

## Support

- **Documentation**: See `.github/instructions/quest.instructions.md`
- **Build Plan**: See `QUEST_BUILD_PLAN.md`
- **Issues**: Report template issues in GitHub Issues
- **Discussions**: Use GitHub Discussions for questions

---

**Last Updated**: 2025-11-29  
**Maintainers**: IT-Journey Team
