# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Phase 5: Master Tier Quest Generation (Levels 1100-1111)
- **32 New Quests**: Complete Master Tier quest generation across 4 levels
  - **Level 1100 - Data Engineering** (5 new quests):
    - `apache-spark.md` - Big Data Processing with Spark
    - `data-quality.md` - Data Quality & Validation
    - `data-warehousing.md` - Data Warehouse Design
    - `etl-pipeline-design.md` - ETL Pipeline Architecture
    - `stream-processing.md` - Real-time Data Streams
  - **Level 1101 - Machine Learning & AI** (8 new quests):
    - `ai-ethics.md` - Responsible AI Development
    - `computer-vision.md` - Image & Video Analysis
    - `deep-learning-frameworks.md` - TensorFlow & PyTorch
    - `ml-fundamentals.md` - Machine Learning Basics
    - `mlops.md` - ML Operations & Deployment
    - `natural-language-processing.md` - NLP Fundamentals
    - `neural-networks.md` - Deep Learning Architecture
    - `python-data-science.md` - Python for Data Science
  - **Level 1110 - Architecture & Design** (7 new quests):
    - `api-gateway-patterns.md` - API Gateway Design
    - `design-patterns.md` - Software Design Patterns
    - `domain-driven-design.md` - DDD Principles
    - `event-driven-design.md` - Event-Driven Architecture
    - `microservices-architecture.md` - Microservices Design
    - `scaling-strategies.md` - Horizontal & Vertical Scaling
    - `system-design-interviews.md` - System Design Practice
  - **Level 1111 - Leadership & Innovation** (8 new quests):
    - `architecture-reviews.md` - Technical Review Process
    - `building-technical-communities.md` - Community Building
    - `career-advancement.md` - IT Career Growth
    - `innovation-rnd.md` - R&D Leadership
    - `mentorship-programs.md` - Mentoring Skills
    - `open-source-contribution.md` - OSS Contribution
    - `tech-speaking-writing.md` - Technical Communication
    - `technical-leadership.md` - Tech Lead Skills

#### Quest Validation Improvements
- **Quest Template Update**: Added `fmContentType: quest` field to `.frontmatter/templates/quests.md`
- **Validation Rules Documentation**: Added comprehensive validation rules section to `.github/instructions/quest.instructions.md` including:
  - Required frontmatter fields table
  - Enhanced fields table
  - Content structure validation requirements
  - Difficulty level guidelines
  - Binary level system reference
  - Validation commands and score thresholds
  - Common issues and fixes guide

### Fixed
- **fmContentType Field**: Added missing `fmContentType: quest` to 35 quest files:
  - All 32 new quests in levels 1100-1111
  - 3 existing quests: `edgar.md`, `sec-edgar.md`, `the-temple-of-templates.md`
- **Jekyll Build Error**: Fixed invalid `preview` field in 2 blog posts:
  - `2025-06-29-planting-seeds-software-evolution.md` - Changed text to image path
  - `2025-07-09-fixing-github-actions-bash-compatibility-ai-evolution-engine.md` - Changed text to image path

### Changed
- **Quest README**: Updated `pages/_quests/README.md`:
  - Removed "Coming Soon" labels from levels 1101 and 1111
  - Added links to all new quests in levels 1100-1111
  - Updated quest counts and completion status

#### Quest System Status Update
- **Total Quests**: 162 quests (130 previous + 32 new)
- **Levels Complete**: 16 of 16 levels (100%) ✅
- **Phases Complete**: 5 of 6 phases (83%)
  - Phase 5: Master Tier ✅ (NEW)

---

### Added

#### Phase 4: Expert Tier Quest Generation (Phases 1-4 Complete)
- **72 New Placeholder Quests**: Complete quest generation across 4 phases
  - **Phase 2 - Apprentice Tier** (Levels 0000-0011): 17 quests
    - Level 0000: `terminal-fundamentals.md`, `git-basics.md`, `markdown-mastery.md`
    - Level 0001: `github-pages-basics.md`, `jekyll-fundamentals.md`, `liquid-templating.md`, `yaml-configuration.md`, `git-workflow-mastery.md`
    - Level 0010: `advanced-markdown.md`, `css-styling-basics.md`, `javascript-fundamentals.md`, `bootstrap-framework.md`
    - Level 0011: `advanced-git-workflows.md`, `jekyll-plugins.md`, `seo-optimization.md`, `analytics-integration.md`, `custom-domains.md`
  - **Phase 3 - Journeyman Tier** (Levels 0100-0111): 36 quests
    - Level 0100: `container-fundamentals.md`, `docker-compose-orchestration.md`
    - Level 0101: 8 CI/CD quests (`cicd-fundamentals.md`, `github-actions-basics.md`, `testing-integration.md`, etc.)
    - Level 0110 (NEW): 8 database quests (`database-fundamentals.md`, `sql-mastery.md`, `data-modeling.md`, etc.)
    - Level 0111 (NEW): 7 API quests (`api-fundamentals.md`, `rest-principles.md`, `api-authentication.md`, etc.)
  - **Phase 4 - Expert Tier** (Levels 1000-1011): 19 quests
    - Level 1000 (NEW): 6 cloud quests (`cloud-computing-fundamentals.md`, `aws-essentials.md`, `infrastructure-as-code.md`)
    - Level 1001 (NEW): 4 Kubernetes quests (`kubernetes-fundamentals.md`, `k8s-pods-workloads.md`, `k8s-services-networking.md`, `k8s-config-secrets.md`)
    - Level 1010: 5 monitoring quests (`monitoring-fundamentals.md`, `prometheus-grafana.md`, `elk-stack.md`, `distributed-tracing.md`, `alerting-systems.md`)
    - Level 1011: 5 security quests (`security-fundamentals.md`, `threat-modeling.md`, `secure-coding.md`, `penetration-testing.md`, `compliance-standards.md`)

#### Quest Infrastructure & Automation
- **Quest Generation Script**: `scripts/generate-placeholder-quest.sh` - Automated quest file generation from templates
- **Quest Validator**: `scripts/validate-quest-network.py` - Python-based frontmatter and network validation
- **Quest Tools Wrapper**: `scripts/quest-tools.sh` - Docker wrapper for validation tools
- **Quest Templates**: `pages/_quests/templates/` directory with `main-quest-template.md` and `level-readme-template.md`
- **Docker Validation Environment**: Multi-service setup in `docker-compose.yml` with `quest-validator` and `quest-network-validator` services
- **Python Dependencies**: `scripts/requirements.txt` for PyYAML and validation tools

#### Quest Documentation
- **QUEST_BUILD_PLAN.md**: 14-week roadmap for complete quest system (6 phases, 97 quests)
- **PHASE1_COMPLETE.md**: Infrastructure phase documentation
- **PHASE2_COMPLETE.md**: Apprentice Tier (17 quests) completion summary
- **PHASE3_COMPLETE.md**: Journeyman Tier (36 quests) completion summary
- **PHASE4_COMPLETE.md**: Expert Tier (19 quests) completion summary with technical coverage breakdown
- **VALIDATION_FIXES_SUMMARY.md**: Documentation of 44 frontmatter validation fixes across 58 original quests

#### Other Additions
- Preview images for various quests in `assets/images/previews/`
- **README.md files**: Added README.md to all level directories (0000, 0001, 0010, 0011, 0100, 0101, 1010, 1011, 1100, 1110)
- **inventory/README.md**: New directory for learner progress tracking (future feature)
- **tools/README.md**: Collection documentation for cross-level tool quests
- **Directory Structure section**: Added comprehensive structure documentation to main quests README.md
- **Binary Level System table**: Complete 16-level table (0000-1111) with status indicators and reserved levels

### Changed

#### Quest Frontmatter Standardization
- **44 Frontmatter Validation Fixes**: Systematic fixes across 58 original quest files
  - Added missing `level` field to all quests following binary format (0000-1111)
  - Added missing `quest_type` field (main_quest, side_quest, bonus_quest, epic_quest, reference)
  - Added missing `difficulty` field (🟢 Easy, 🟡 Medium, 🔴 Hard, ⚔️ Epic, 📚 Reference)
  - Added missing `estimated_time` field with proper format
  - Standardized `permalink` field structure
  - Added missing `title` and `description` fields
  - Fixed invalid difficulty values and quest types
  - Fixed invalid level formats to 4-digit binary

#### Docker Infrastructure Updates
- **Dockerfile**: Added Python 3.11 venv setup at `/opt/venv` for quest validation
- **docker-compose.yml**: Added multi-service validation environment
  - `quest-validator` service for individual quest validation
  - `quest-network-validator` service for network-wide validation
  - Shared volume mounts for scripts and quest directories

#### Quest System Status
- **Total Quests**: 130 quests (58 original + 72 generated)
- **Levels Complete**: 12 of 16 levels (75%)
  - Original levels: 0000, 0001, 0010, 0011, 0100, 0101, 1100, 1110
  - New levels: 0110, 0111, 1000, 1001, 1010, 1011
- **Phases Complete**: 4 of 6 phases (67%)
  - Phase 1: Infrastructure ✅
  - Phase 2: Apprentice Tier ✅
  - Phase 3: Journeyman Tier ✅
  - Phase 4: Expert Tier ✅
  - Phase 5: Master Tier (pending)
  - Phase 6: Polish & Integration (pending)

#### Major Quest Reorganization
  - `init_world/` → `0000/` (Foundation & Init World)
  - `lvl_000/` → `0000/` (merged with init_world content)
  - `lvl_001/` → `0001/` (Journeyman Challenges)
  - `lvl_0010/` → `0010/` (Terminal Enhancement)
  - `frontend/` → `0100/` (Frontend & Docker)
  - Tool quests → `tools/` directory
  - Quest examples → `codex/` directory
- **File Naming**: Removed date prefixes from all quest files (e.g., `2024-05-28-bash-run.md` → `bash-run.md`)
- **Code Files**: Moved script/code examples from level root directories to subdirectories (`scripts/`, `examples/`)
- **Updated paths**: All internal quest links updated to new binary-coded paths in README.md and home.md
- Updated `scripts/lib/preview_generator.py` for enhanced preview generation
- Updated `test/quest-validator/requirements.txt` for validator dependencies

### Removed
- Legacy directory structure (`init_world/`, `lvl_000/`, `lvl_001/`, `lvl_0010/`, `frontend/`, `examples/`)
- Date prefixes from 75+ quest files
- Duplicate `0000/tools/` directory (consolidated to root `tools/`)

### Migration Notes
- Quest permalinks may have changed - update any external references
- Binary level directories (0000-1110) replace legacy naming convention
- Code examples now live in subdirectories within level folders

## [2.1.0] - 2025-11-26

### Added
- **New Quest**: `2025-11-26-prompt-crystal-mastery-vscode-copilot-quest.md` - Comprehensive VS Code Copilot prompt engineering quest with RCTF patterns, few-shot prompting, and reusable template creation
- **New Post**: `2025-11-26-mastering-prompt-engineering-vscode-copilot.md` - Tutorial companion to the prompt engineering quest
- **New Prompt Template**: `commit-publish.prompt.md` - Complete release pipeline workflow for semantic versioning and publishing
- **Enhanced Prompt**: `draft-article.prompt.md` v2.0.0 - Major upgrade with RCTF pattern, Kaizen-driven structure, intake checklists, and quality gates
- **CRUSH Workflow System**: Added `.crush/workflows/CRUSH_WORKFLOW_SYSTEM_SUMMARY.md` documentation

### Changed
- **Documentation Reorganization**: Moved summary files from repository root to organized `/docs/` subdirectories:
  - `ABOUT_REORGANIZATION_SUMMARY.md` → `docs/architecture/`
  - `QUEST_TEMPLATE_ENHANCEMENT_SUMMARY.md` → `docs/standards/`
  - `DEPENDENCY_UPDATE_SUMMARY.md` → `docs/workflows/`
  - `LINK_CONSOLIDATION_SUMMARY.md` → `docs/workflows/`
- Updated `docs/README.md` with links to newly organized documentation (v1.1.0)
- Updated `.gitignore` to exclude log files from root directory and `logs/*.log`

### Removed
- Cleaned up repository root:
  - Removed `.seed.md` (seed content moved to proper locations)
  - Removed `.github/workflows/blank.yml` (unused workflow)
  - Removed `prompts/seed.prompt.yml` and `prompts/seed_prompt.md` (consolidated)
  - Removed `test-mermaid.html` (moved to `test/` directory)
  - Removed various log files (`add-date-prefixes.log`, `post-organization.log`)

### Fixed
- Improved `.gitignore` patterns to prevent log file accumulation in repository

## [2.0.0] - 2025-11-16

### Changed
- **BREAKING**: Weekly Post Organization workflow now creates pull requests instead of directly committing to main branch
  - This change requires manual review and approval of automated post organization changes
  - PRs are automatically labeled and assigned for review
  - Provides safety and traceability for all automated content changes

### Migration Notes
- Existing workflow behavior: Posts were automatically organized and committed to main
- New workflow behavior: Posts are organized and a PR is created for review
- Action required: Review and merge PRs created by the workflow
- No script changes required: `organize-posts.py` and `organize-posts.sh` work as-is

### Technical Details
- Workflow: `.github/workflows/organize-posts-weekly.yml`
- Implementation: Uses standard GitHub Actions (git commands + GitHub CLI)
- Branch pattern: `automated/organize-posts-{run_id}`
- PR configuration:
  - Title: `🤖 Weekly Post Organization - {run_id}`
  - Labels: `automated`, `content-organization`, `posts`
  - Assignee: `bamr87`
  - Includes: Workflow link, change summary, next steps

### Documentation
- Consolidated workflow documentation in `docs/workflows/ORGANIZE_POSTS_WORKFLOW.md`
- Includes: Process flow, implementation details, testing guide, troubleshooting
- Removed temporary documentation files from repository root

## [1.0.0] - 2025-11-16

### Initial Release
- Weekly Post Organization workflow with direct commit to main branch
- Automated organization of posts by section using frontmatter metadata
- Automated archiving of posts older than configurable threshold
- Scheduled execution every Sunday at 2 AM UTC
- Manual trigger with dry-run option

---

## Changelog Maintenance

This changelog is manually maintained. When making changes:

1. Add new entries under `[Unreleased]` section
2. Use categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`
3. Include migration notes for breaking changes
4. Link to relevant documentation
5. Move `[Unreleased]` items to a new version section when releasing

### Version Numbering

- **Major version** (X.0.0): Breaking changes that require user action
- **Minor version** (0.X.0): New features, non-breaking changes
- **Patch version** (0.0.X): Bug fixes, documentation updates

[Unreleased]: https://github.com/bamr87/it-journey/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/bamr87/it-journey/releases/tag/v2.1.0
[2.0.0]: https://github.com/bamr87/it-journey/releases/tag/v2.0.0
[1.0.0]: https://github.com/bamr87/it-journey/releases/tag/v1.0.0
