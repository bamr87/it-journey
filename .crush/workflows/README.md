---
title: "Crush Workflow System"
description: "AI-powered sequential prompt execution for multi-step content creation and refinement"
permalink: /crush/workflows/readme/
lastmod: 2025-11-20T00:00:00.000Z
---

# 🔮 Crush Workflow System

Crush-powered orchestration engine for executing sequential AI prompts with state management, iterative refinement, and cross-content integration. Transform complex multi-step content creation into reproducible, automated workflows.

## 🎯 Purpose

The Crush Workflow System enables:
- **Sequential Prompt Execution**: Chain prompts in defined order with data flow
- **State Management**: Pass context and outputs between workflow steps
- **Iterative Refinement**: Loop through improvement cycles (draft → refine → expand → publish)
- **Cross-Content Integration**: Create related content (article + quest) with shared metadata
- **Reproducible Flows**: Define workflows once, execute many times
- **Progress Tracking**: Visual feedback and checkpoint management

## 📁 Directory Structure

```
.crush/workflows/
├── README.md                           # This guide
├── engine.sh                          # Workflow execution engine
├── state-manager.sh                   # State and context management
├── prompt-runner.sh                   # Individual prompt executor
├── templates/                         # Workflow definition templates
│   ├── article-quest-creation.yml    # Article + quest full workflow
│   ├── quest-only.yml                # Standalone quest creation
│   ├── article-only.yml              # Standalone article creation
│   ├── iterative-refinement.yml      # Generic improvement loop
│   └── README.md                     # Template documentation
├── schemas/                           # Workflow validation schemas
│   ├── workflow.schema.json          # Main workflow schema
│   └── step.schema.json              # Individual step schema
└── examples/                          # Real workflow executions
    ├── docker-article-quest/         # Example: Docker article + quest
    └── README.md                     # Examples documentation
```

## 🚀 Quick Start

### 1. Execute a Workflow

```bash
# Interactive workflow selection with Crush
./journey.sh --workflow

# Direct workflow execution
.crush/workflows/engine.sh run templates/article-quest-creation.yml

# With custom input
.crush/workflows/engine.sh run templates/article-quest-creation.yml \
  --input '{"topic": "Kubernetes Basics", "level": "0011", "difficulty": "intermediate"}'
```

### 2. Create Custom Workflow

```bash
# Copy template
cp .crush/workflows/templates/article-quest-creation.yml \
   .crush/workflows/my-custom-workflow.yml

# Edit workflow definition (see schema below)
crush .crush/workflows/my-custom-workflow.yml

# Validate workflow
.crush/workflows/engine.sh validate my-custom-workflow.yml

# Execute
.crush/workflows/engine.sh run my-custom-workflow.yml
```

## 📋 Workflow Definition Format

Workflows are defined in YAML with this structure:

```yaml
---
# Workflow Metadata
workflow:
  name: "Article and Quest Creation"
  version: "1.0.0"
  description: "Draft article, create related quest, iterate to refine and publish"
  author: "IT-Journey Team"
  created: "2025-11-20"
  tags: ["content-creation", "article", "quest", "iterative"]

# Input Requirements
inputs:
  required:
    - name: "topic"
      type: "string"
      description: "Main topic or learning objective"
      example: "Docker Containerization"
    - name: "level"
      type: "string"
      description: "Binary level code (0000-11111+)"
      example: "0011"
  optional:
    - name: "difficulty"
      type: "string"
      description: "Difficulty level"
      default: "intermediate"
      enum: ["beginner", "intermediate", "advanced"]

# Workflow Steps
steps:
  # Step 1: Draft Article Outline
  - id: "draft_article"
    name: "Draft Article Outline"
    prompt: ".github/prompts/draft-article.prompt.md"
    inputs:
      topic: "{{ inputs.topic }}"
      difficulty: "{{ inputs.difficulty }}"
    outputs:
      - name: "article_outline"
        path: "outline"
      - name: "learning_objectives"
        path: "learning_objectives"
    on_success: "generate_article_frontmatter"
    on_failure: "abort"

  # Step 2: Generate Article Front Matter
  - id: "generate_article_frontmatter"
    name: "Generate Article Front Matter"
    prompt: ".github/prompts/generate-frontmatter.prompt.md"
    inputs:
      content_type: "post"
      outline: "{{ steps.draft_article.outputs.article_outline }}"
      learning_objectives: "{{ steps.draft_article.outputs.learning_objectives }}"
      topic: "{{ inputs.topic }}"
      difficulty: "{{ inputs.difficulty }}"
    outputs:
      - name: "frontmatter"
        path: "frontmatter"
    on_success: "create_quest_outline"

  # Step 3: Create Related Quest Outline
  - id: "create_quest_outline"
    name: "Create Related Quest Outline"
    prompt: ".github/prompts/write-quest.prompt.md"
    inputs:
      topic: "{{ inputs.topic }}"
      level: "{{ inputs.level }}"
      related_article: "{{ steps.draft_article.outputs.article_outline }}"
      learning_objectives: "{{ steps.draft_article.outputs.learning_objectives }}"
    outputs:
      - name: "quest_outline"
        path: "quest_outline"
      - name: "quest_objectives"
        path: "quest_objectives"
    on_success: "generate_quest_frontmatter"

  # Step 4: Generate Quest Front Matter
  - id: "generate_quest_frontmatter"
    name: "Generate Quest Front Matter"
    prompt: ".github/prompts/generate-frontmatter.prompt.md"
    inputs:
      content_type: "quest"
      outline: "{{ steps.create_quest_outline.outputs.quest_outline }}"
      quest_objectives: "{{ steps.create_quest_outline.outputs.quest_objectives }}"
      level: "{{ inputs.level }}"
      topic: "{{ inputs.topic }}"
    outputs:
      - name: "quest_frontmatter"
        path: "frontmatter"
    on_success: "expand_article"

  # Step 5: Expand Article Content
  - id: "expand_article"
    name: "Expand Article with Examples"
    prompt: ".github/prompts/expand-content.prompt.md"
    inputs:
      content_type: "article"
      outline: "{{ steps.draft_article.outputs.article_outline }}"
      frontmatter: "{{ steps.generate_article_frontmatter.outputs.frontmatter }}"
    outputs:
      - name: "expanded_article"
        path: "expanded_content"
    on_success: "refine_quest"

  # Step 6: Refine Quest Content
  - id: "refine_quest"
    name: "Refine Quest with Challenges"
    prompt: ".github/prompts/refine-content.prompt.md"
    inputs:
      content_type: "quest"
      outline: "{{ steps.create_quest_outline.outputs.quest_outline }}"
      frontmatter: "{{ steps.generate_quest_frontmatter.outputs.quest_frontmatter }}"
    outputs:
      - name: "refined_quest"
        path: "refined_content"
    on_success: "improvement_loop"

  # Step 7: Improvement Iteration (Loop)
  - id: "improvement_loop"
    name: "Iterative Improvement Cycle"
    type: "loop"
    max_iterations: 3
    prompt: ".github/prompts/kaizen.prompt.md"
    inputs:
      article: "{{ steps.expand_article.outputs.expanded_article }}"
      quest: "{{ steps.refine_quest.outputs.refined_quest }}"
      iteration: "{{ loop.iteration }}"
    outputs:
      - name: "improved_article"
        path: "article"
      - name: "improved_quest"
        path: "quest"
    continue_if: "{{ loop.iteration < 3 }}"
    on_success: "publish_preparation"

  # Step 8: Prepare for Publishing
  - id: "publish_preparation"
    name: "Prepare Final Files for Publishing"
    prompt: ".github/prompts/publish-prep.prompt.md"
    inputs:
      article: "{{ steps.improvement_loop.outputs.improved_article }}"
      quest: "{{ steps.improvement_loop.outputs.improved_quest }}"
      article_frontmatter: "{{ steps.generate_article_frontmatter.outputs.frontmatter }}"
      quest_frontmatter: "{{ steps.generate_quest_frontmatter.outputs.quest_frontmatter }}"
    outputs:
      - name: "article_file"
        path: "final_article.md"
        save_to: "pages/_posts/"
      - name: "quest_file"
        path: "final_quest.md"
        save_to: "pages/_quests/"
    on_success: "complete"

# Workflow State Management
state:
  persistence: "file"
  location: "work/workflows/{{ workflow.name }}/{{ execution.id }}"
  checkpoints:
    - after: "generate_article_frontmatter"
    - after: "generate_quest_frontmatter"
    - after: "improvement_loop"
  
# Error Handling
error_handling:
  retry_on_failure: true
  max_retries: 2
  backoff: "exponential"
  cleanup_on_abort: true

# Notifications
notifications:
  on_start: true
  on_complete: true
  on_error: true
  channel: "terminal"  # or "webhook", "email"
```

## 🔧 Workflow Engine Commands

### Run Workflow

```bash
# Interactive mode
.crush/workflows/engine.sh run --interactive templates/article-quest-creation.yml

# With input file
.crush/workflows/engine.sh run templates/article-quest-creation.yml \
  --input-file work/workflows/my-inputs.json

# Resume from checkpoint
.crush/workflows/engine.sh resume work/workflows/article-quest/execution-123
```

### Validate Workflow

```bash
# Validate syntax and schema
.crush/workflows/engine.sh validate templates/article-quest-creation.yml

# Dry run (simulate without execution)
.crush/workflows/engine.sh dry-run templates/article-quest-creation.yml
```

### Manage Workflows

```bash
# List available workflows
.crush/workflows/engine.sh list

# Show workflow details
.crush/workflows/engine.sh info templates/article-quest-creation.yml

# List recent executions
.crush/workflows/engine.sh executions --recent 10
```

## 📊 State Management

Workflow state is managed in the `work/workflows/` directory:

```
work/workflows/
├── article-quest-creation/
│   ├── execution-20251120-143022/
│   │   ├── state.json              # Current workflow state
│   │   ├── inputs.json             # Initial inputs
│   │   ├── outputs/                # Step outputs
│   │   │   ├── draft_article/
│   │   │   │   ├── outline.md
│   │   │   │   └── learning_objectives.json
│   │   │   ├── generate_article_frontmatter/
│   │   │   │   └── frontmatter.yml
│   │   │   └── ...
│   │   ├── checkpoints/            # Saved checkpoints
│   │   │   ├── checkpoint-1.json
│   │   │   └── checkpoint-2.json
│   │   └── logs/                   # Execution logs
│   │       ├── workflow.log
│   │       └── steps/
│   └── execution-20251120-150345/
└── quest-only/
    └── ...
```

### State Structure

```json
{
  "workflow": {
    "name": "Article and Quest Creation",
    "version": "1.0.0",
    "execution_id": "execution-20251120-143022",
    "started_at": "2025-11-20T14:30:22Z",
    "current_step": "improvement_loop",
    "status": "running"
  },
  "inputs": {
    "topic": "Docker Containerization",
    "level": "0011",
    "difficulty": "intermediate"
  },
  "steps": {
    "draft_article": {
      "status": "completed",
      "started_at": "2025-11-20T14:30:23Z",
      "completed_at": "2025-11-20T14:32:15Z",
      "outputs": {
        "article_outline": "work/workflows/.../draft_article/outline.md",
        "learning_objectives": "work/workflows/.../draft_article/learning_objectives.json"
      }
    },
    "generate_article_frontmatter": {
      "status": "completed",
      "started_at": "2025-11-20T14:32:16Z",
      "completed_at": "2025-11-20T14:33:45Z",
      "outputs": {
        "frontmatter": "work/workflows/.../generate_article_frontmatter/frontmatter.yml"
      }
    },
    "improvement_loop": {
      "status": "running",
      "started_at": "2025-11-20T14:40:00Z",
      "current_iteration": 2,
      "max_iterations": 3
    }
  },
  "context": {
    "article_topic": "Docker Containerization",
    "quest_level": "0011",
    "iteration_count": 2
  }
}
```

## 🎮 Integration with Journey.sh

The workflow system integrates seamlessly with `journey.sh`:

```bash
# journey.sh menu option
🎯 Run Content Workflow
├── 📝 Article + Quest Creation
├── ⚔️ Quest Only
├── 📰 Article Only
├── 🔄 Resume Workflow
└── 📊 View Executions
```

Menu implementation in `journey.sh`:

```bash
# Add to journey.sh menu
run_workflow_menu() {
  local workflow_choice=$(gum choose \
    "📝 Article + Quest Creation" \
    "⚔️ Quest Only" \
    "📰 Article Only" \
    "🔄 Resume Workflow" \
    "📊 View Executions" \
    "🔙 Back")
  
  case "$workflow_choice" in
    "📝 Article + Quest Creation")
      .crush/workflows/engine.sh run --interactive templates/article-quest-creation.yml
      ;;
    "⚔️ Quest Only")
      .crush/workflows/engine.sh run --interactive templates/quest-only.yml
      ;;
    "📰 Article Only")
      .crush/workflows/engine.sh run --interactive templates/article-only.yml
      ;;
    "🔄 Resume Workflow")
      resume_workflow_interactive
      ;;
    "📊 View Executions")
      .crush/workflows/engine.sh executions --recent 10
      ;;
  esac
}
```

## 🔍 Prompt Integration

Workflows reference prompts from `.github/prompts/`:

- `write-quest.prompt.md` - Quest creation
- `kaizen.prompt.md` - Iterative improvement
- `bash-it.prompt.md` - Script generation
- `stackattack.prompt.md` - Stack analysis

Custom prompts can be added and referenced in workflow definitions.

## 📚 Example Workflows

### 1. Article + Quest Creation (Full Flow)

**Use Case**: Create educational article with complementary quest, iterate to refine, publish both.

**Steps**: Draft article → Generate frontmatter → Create quest → Generate quest frontmatter → Expand article → Refine quest → Improve (loop 3x) → Publish

**Template**: `templates/article-quest-creation.yml`

### 2. Quest Only

**Use Case**: Create standalone quest without article.

**Steps**: Draft quest → Generate frontmatter → Add challenges → Validate → Publish

**Template**: `templates/quest-only.yml`

### 3. Iterative Refinement

**Use Case**: Take existing content and improve through multiple cycles.

**Steps**: Load content → Analyze (Kaizen) → Improve → Expand → Refine → Repeat → Publish

**Template**: `templates/iterative-refinement.yml`

## 🛠️ Advanced Features

### Conditional Steps

```yaml
steps:
  - id: "validate_quest"
    name: "Validate Quest Structure"
    prompt: ".github/prompts/validate.prompt.md"
    inputs:
      content: "{{ steps.refine_quest.outputs.refined_quest }}"
    outputs:
      - name: "validation_result"
        path: "validation.json"
    on_success: "publish"
    on_failure: "fix_quest"
    condition: "{{ outputs.validation_result.score >= 80 }}"
```

### Parallel Steps

```yaml
steps:
  - id: "parallel_tasks"
    name: "Run Multiple Tasks in Parallel"
    type: "parallel"
    tasks:
      - id: "generate_diagrams"
        prompt: ".github/prompts/generate-diagrams.prompt.md"
      - id: "generate_code_examples"
        prompt: ".github/prompts/generate-code.prompt.md"
      - id: "generate_tests"
        prompt: ".github/prompts/generate-tests.prompt.md"
    wait_for_all: true
    on_success: "combine_results"
```

### Human-in-the-Loop

```yaml
steps:
  - id: "review_checkpoint"
    name: "Human Review Checkpoint"
    type: "human_review"
    inputs:
      article: "{{ steps.expand_article.outputs.expanded_article }}"
      quest: "{{ steps.refine_quest.outputs.refined_quest }}"
    prompt: "Review the generated content. Approve to continue or provide feedback for revision."
    outputs:
      - name: "approved"
        type: "boolean"
      - name: "feedback"
        type: "string"
    on_approve: "publish"
    on_reject: "improvement_loop"
```

## 📈 Monitoring and Metrics

Workflows track execution metrics:

```json
{
  "metrics": {
    "total_duration": "25m 43s",
    "step_count": 8,
    "iterations": 3,
    "checkpoints_saved": 3,
    "ai_tokens_used": 15420,
    "success_rate": 100,
    "average_step_duration": "3m 12s"
  }
}
```

## 🔒 Best Practices

1. **Modular Prompts**: Use reusable prompts from `.github/prompts/` instead of inline prompts
2. **State Checkpoints**: Save state after expensive steps for resumability
3. **Error Handling**: Always define `on_failure` paths
4. **Input Validation**: Validate inputs before starting workflow
5. **Output Persistence**: Save outputs to `work/workflows/` for debugging
6. **Iteration Limits**: Set `max_iterations` to prevent infinite loops
7. **README-First/Last**: Workflows should read/update READMEs appropriately
8. **Dry Runs**: Test workflows with `--dry-run` before real execution

## 🐛 Troubleshooting

### Workflow Fails Mid-Execution

```bash
# View logs
cat work/workflows/article-quest/execution-123/logs/workflow.log

# Resume from last checkpoint
.crush/workflows/engine.sh resume work/workflows/article-quest/execution-123
```

### State Corruption

```bash
# Validate state file
.crush/workflows/state-manager.sh validate work/workflows/article-quest/execution-123/state.json

# Restore from checkpoint
.crush/workflows/state-manager.sh restore work/workflows/article-quest/execution-123 checkpoint-2
```

### Prompt Not Found

```bash
# List available prompts
ls -la .github/prompts/

# Validate prompt reference in workflow
.crush/workflows/engine.sh validate templates/article-quest-creation.yml
```

## 📖 Related Documentation

- [Quest Instructions](.github/instructions/quest.instructions.md) - Quest creation standards
- [Post Instructions](.github/instructions/posts.instructions.md) - Article creation standards
- [Prompts README](.github/prompts/README.md) - Prompt catalog
- [Work Directory](.github/instructions/work.instructions.md) - Workspace organization

## 🤝 Contributing

To add new workflows:

1. Create workflow definition in `templates/`
2. Validate schema: `.crush/workflows/engine.sh validate <workflow.yml>`
3. Test with dry run: `.crush/workflows/engine.sh dry-run <workflow.yml>`
4. Document in this README
5. Add to `journey.sh` menu if appropriate
6. Update `lastmod` date

---

**Version**: 1.0.0  
**Last Modified**: 2025-11-20  
**Maintained by**: IT-Journey Automation Guild

**Questions?** [Open an issue](https://github.com/bamr87/it-journey/issues)
