# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Updated Weekly Post Organization workflow to use PR-based approval instead of direct push
- Replaced `peter-evans/create-pull-request` third-party action with native GitHub CLI
- Split PR creation into two explicit steps: branch creation and PR creation
- Enhanced workflow summary to report PR creation status with PR number and URL

### Added
- Comprehensive documentation for organize-posts workflow in `docs/workflows/ORGANIZE_POSTS_WORKFLOW.md`
- Automated PR creation with labels (`automated`, `content-organization`, `posts`) and assignee
- Traceability: Each PR now links back to the workflow run that created it
- Review process: All automated post organization changes now go through PR review before merging

### Removed
- Direct push to main branch from organize-posts workflow
- Third-party dependency on `peter-evans/create-pull-request` action

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

[Unreleased]: https://github.com/bamr87/it-journey/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/bamr87/it-journey/releases/tag/v2.0.0
[1.0.0]: https://github.com/bamr87/it-journey/releases/tag/v1.0.0
