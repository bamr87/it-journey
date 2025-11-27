# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
