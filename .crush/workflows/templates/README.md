# Workflow Templates

This directory contains reusable workflow definitions for content creation, refinement, and publishing in the IT-Journey repository.

## Available Templates

### 1. article-quest-creation.yml ✅
**Status**: Fully Defined  
**Purpose**: Complete content creation pipeline  
**Steps**: Draft article → Create quest → Expand → Refine → Improve (3x) → Validate → Publish  
**Duration**: ~60 minutes  
**Use When**: Creating new educational content with complementary quest

**Inputs Required**:
- `topic`: Main learning topic (e.g., "Docker Containerization")
- `level`: Binary level code (e.g., "0011")
- `difficulty`: beginner | intermediate | advanced | expert
- `estimated_time`: Expected completion time (e.g., "2-3 hours")

**Outputs**:
- Complete article with frontmatter in `pages/_posts/`
- Complete quest with enhanced frontmatter in `pages/_quests/`
- Validation reports and improvement logs
- README update instructions

### 2. quest-only.yml ⏳
**Status**: Planned (Template Pending)  
**Purpose**: Standalone quest creation  
**Steps**: Draft quest → Frontmatter → Challenges → Diagrams → Validate → Publish  
**Duration**: ~30 minutes  
**Use When**: Creating a quest without an accompanying article

### 3. article-only.yml ⏳
**Status**: Planned (Template Pending)  
**Purpose**: Standalone article creation  
**Steps**: Draft → Expand → Code examples → Validate → Publish  
**Duration**: ~30 minutes  
**Use When**: Writing articles that don't need a related quest

### 4. iterative-refinement.yml ⏳
**Status**: Planned (Template Pending)  
**Purpose**: Improve existing content  
**Steps**: Load → Analyze (Kaizen) → Improve → Expand → Refine → Repeat  
**Duration**: ~20 minutes  
**Use When**: Enhancing or updating existing articles/quests

## Creating New Templates

To create a custom workflow template:

1. **Copy Example Template**:
   ```bash
   cp article-quest-creation.yml my-custom-workflow.yml
   ```

2. **Edit Workflow Definition**:
   - Update `workflow.name`, `version`, `description`
   - Define required/optional inputs
   - Specify step sequence with prompts
   - Set state management and error handling
   - Configure notifications

3. **Validate Syntax**:
   ```bash
   ../.crush/workflows/engine.sh validate my-custom-workflow.yml
   ```

4. **Test with Dry Run**:
   ```bash
   ../.crush/workflows/engine.sh dry-run my-custom-workflow.yml
   ```

5. **Document in This README**:
   - Add to "Available Templates" section
   - Describe purpose, steps, duration
   - List required inputs and outputs

## Template Schema

All workflows must include:

```yaml
workflow:
  name: "Descriptive Name"
  version: "1.0.0"
  description: "What this workflow accomplishes"
  
inputs:
  required: [...]
  optional: [...]

steps:
  - id: "step_1"
    name: "Step Name"
    prompt: ".github/prompts/prompt-file.md"
    inputs: {...}
    outputs: [...]
    on_success: "next_step"
    on_failure: "abort"
    
state:
  persistence: "file"
  checkpoints: [...]
  
error_handling:
  retry_on_failure: true
  max_retries: 2
```

See `article-quest-creation.yml` for a complete annotated example.

## Integration with Journey.sh

Workflows are accessible through the Journey.sh TUI menu:

```
🎯 Run Content Workflow
├── 📝 Article + Quest Creation (Full Pipeline)
├── ⚔️ Quest Only
├── 📰 Article Only
├── 🔄 Resume Previous Workflow
└── 📊 View Recent Executions
```

## Related Documentation

- [Workflow System README](../README.md) - Complete system documentation
- [Quest Instructions](../../.github/instructions/quest.instructions.md) - Quest creation standards
- [Post Instructions](../../.github/instructions/posts.instructions.md) - Article creation standards
- [Prompts Catalog](../../.github/prompts/README.md) - Available AI prompts

---

**Last Updated**: 2025-11-20  
**Maintained by**: IT-Journey Automation Guild
