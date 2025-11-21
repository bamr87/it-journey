# AGENTS.md: Guide for AI Agents Working in IT-Journey Repository

This document provides essential information for AI agents (like Grok/Crush) to effectively understand, navigate, and contribute to the IT-Journey codebase. All information is based on direct observation of the repository structure, files, and configurations. No assumptions or inventions have been made.

## Project Overview

- **Type**: Jekyll-based static site generator for an educational IT platform.
- **Purpose**: Democratize IT education through open-source content, gamified quests, blog posts, and technical documentation. Focuses on learning journeys from beginner to advanced levels, with themes of fantasy and progression (e.g., "zer0 to her0").
- **Tech Stack**:
  - Ruby/Jekyll for site generation.
  - Markdown for content (posts, quests, notes).
  - YAML for configuration and data.
  - Bash and Python for automation scripts.
  - JavaScript for site assets and interactivity.
  - GitHub Actions for CI/CD, validation, and deployment.
  - Docker for containerization (observed in Dockerfile and docker-compose.yml).
- **Hosting**: GitHub Pages, with Azure Static Web Apps deployment options.
- **Key Themes**: Educational content with RPG/fantasy metaphors, progressive learning paths, multi-platform support (macOS, Windows, Linux, Cloud).
- **Standards**: Strict adherence to front matter in Markdown files, README-First/Last principle, conventional commits, and gamification elements.

## Directory Structure

Based on `ls` output with depth 3:

- **pages/**: Core content collections.
  - _about/: About pages, features, profiles.
  - _docs/: Documentation (e.g., Jekyll-related).
  - _hobbies/: Personal/hobby content.
  - _notes/: Notes, journals, code snippets.
  - _notebooks/: Jupyter notebooks and conversions.
  - _posts/: Blog posts organized by categories (e.g., ai & machine learning, devops).
  - _quests/: Educational quests with levels (e.g., lvl_000, lvl_001) and themes (e.g., init_world, frontend).
  - _quickstart/: Beginner guides (e.g., setup instructions).

- **scripts/**: Automation and utility scripts.
  - core/: Environment setup scripts (Bash).
  - development/: Content organization (Python, Bash).
  - deployment/: Update scripts (Bash).
  - examples/: Data examples.
  - Individual scripts: link-checker.py, azure-jekyll-deploy.sh, etc.

- **_data/**: YAML data files.
  - navigation/: Menu configurations.
  - Other: content_statistics.yml, prerequisites.yml, ui-text.yml.

- **assets/**: Static assets.
  - css/: Styles (SCSS, CSS).
  - images/: Site images, icons.
  - js/: Scripts (e.g., particles.js, color-modes.js).
  - gif/, svg/: Additional media.

- **.github/**: GitHub configurations.
  - workflows/: CI/CD YAML files (e.g., azure-jekyll-deploy.yml, link-checker.yml).
  - instructions/: Markdown guides (e.g., quest.instructions.md, posts.instructions.md).
  - prompts/: Prompt templates (Markdown, YAML).

- **test/**: Testing utilities.
  - quest-validator/: Python validator for quests.
  - hyperlink-guardian/: Link checking scripts.
  - test-results/: Output files (CSV, TXT).

- **docs/**: Additional documentation.
  - architecture/, standards/, workflows/, etc. (Markdown files).

- **Other Root Files/Dirs**:
  - Gemfile: Ruby dependencies.
  - Makefile: Commands for statistics generation.
  - _config.yml: Jekyll configuration.
  - Dockerfile, docker-compose.yml: Container setup.
  - README.md: Main repo README.
  - Various summaries (e.g., ABOUT_REORGANIZATION_SUMMARY.md).

## Essential Commands

Observed from Makefile, scripts, Gemfile, and workflows:

- **Jekyll Site Management** (from Gemfile and _config.yml):
  - Install dependencies: `bundle install`
  - Build site: `bundle exec jekyll build`
  - Serve locally: `bundle exec jekyll serve --port 4000` (port from _config.yml)
  - Clean: `bundle exec jekyll clean`

- **Content Statistics** (from Makefile in root):
  - Generate stats: `make stats` (runs _data/generate_statistics.sh)
  - Update and show: `make stats-update` (runs _data/update_statistics.sh)
  - Show current: `make stats-show`
  - Clean stats: `make stats-clean`
  - Show config: `make stats-config`
  - Test generator: `make test`

- **Deployment** (from scripts/azure-jekyll-deploy.sh):
  - Full deployment: `./scripts/azure-jekyll-deploy.sh deploy --app-name <name> --github-repo <url>`
  - Setup: `./scripts/azure-jekyll-deploy.sh setup`
  - Cleanup: `./scripts/azure-jekyll-deploy.sh cleanup --force`
  - Other subcommands: configure, azure-create, github-workflow, domain-setup.

- **Testing and Validation** (from test/ dir and scripts):
  - Validate quests: `python3 test/quest-validator/quest_validator.py <file.md>` or `-d pages/_quests/`
  - Link checker: `python3 scripts/link-checker.py --scope website --timeout 30`
  - Test validator: `./test/quest-validator/test-validator.sh`

- **Git and CI/CD** (from .github/workflows/):
  - Workflows include azure-jekyll-deploy.yml for deployment, link-checker.yml for validation.
  - Run locally if needed via act or manual execution.

- **Other Scripts** (from glob on *.sh and *.py):
  - Environment setup: `./scripts/core/environment-setup.sh`
  - Organize posts: `./scripts/development/content/organize-posts.sh`
  - Update settings: `./scripts/deployment/update-settings.sh`

## Code Organization and Patterns

- **Content Files** (Markdown in pages/):
  - Use YAML front matter with required fields (e.g., title, description, date, keywords, categories).
  - Fantasy/RPG theme: Sections like "Quest Objectives" (🎯), use of emojis, gamified language.
  - Structure: Headers with emojis, code blocks with language spec (e.g., ```bash), checkboxes for tasks.
  - Permalinks: /:collection/:categories/:name/ for quests/docs.

- **Scripts** (Bash/Python):
  - Bash: Strict mode (set -euo pipefail), logging, error handling, usage functions.
  - Python: Classes for validation (e.g., ValidationResult in quest_validator.py), regex for parsing.
  - Patterns: Modular functions, dry-run support, verbose logging.

- **JavaScript** (in assets/js/):
  - Simple utilities (e.g., adding classes to images in myScript.js).
  - Libraries: particles.js, halfmoon.js (likely for UI effects).

- **YAML Configurations**:
  - Navigation menus in _data/navigation/.
  - Jekyll config in _config.yml: Plugins, collections, defaults, exclude lists.

- **Testing Patterns**:
  - quest_validator.py checks front matter, content structure, fantasy theme, accessibility.
  - Scores based on completeness (e.g., required fields, code blocks).

## Naming Conventions and Style Patterns

- **Files**:
  - Markdown: kebab-case with dates (e.g., 2025-11-17-deploying-jekyll-sites-to-azure-cloud.md).
  - Scripts: kebab-case (e.g., azure-jekyll-deploy.sh, link-checker.py).
  - YAML: snake_case (e.g., content_statistics.yml).

- **Branches** (from copilot-instructions.md):
  - feature/, bugfix/, refactor/, docs/, etc.

- **Commits** (from copilot-instructions.md):
  - Conventional: feat:, fix:, refactor:, docs:, chore:.

- **Content Style**:
  - Fantasy theme: Quests use RPG language (e.g., "brave adventurer", emojis like 🎯, ⚔️).
  - Front matter: Consistent keys (title, description, lastmod, version).
  - Code: Language-specified blocks, checklists with - [ ].

## Testing Approach and Patterns

- **Quest Validation** (quest_validator.py):
  - Checks required front matter fields, hierarchy, level format (binary), difficulty.
  - Validates content: Sections, code blocks, checkboxes, fantasy theme, accessibility.
  - Scoring system: Percentage based on passed checks.

- **Link Checking** (link-checker.py):
  - Scans for broken links with timeout.

- **Other**:
  - Makefile test target checks syntax and directories.
  - GitHub Actions for frontmatter-validation.yml, build-validation.yml.

## Important Gotchas and Non-Obvious Patterns

- **README-First/Last Principle** (from copilot-instructions.md): Always read/update README.md before/after changes in any directory.
- **Front Matter Standards**: Required fields like title, description, learning_objectives; use YAML lists for arrays.
- **Excludes in _config.yml**: Many files/dirs excluded from Jekyll processing (e.g., scripts/, test/, *.sh).
- **Gamification**: Quests must include fantasy elements, objectives, prerequisites; use Mermaid diagrams for maps.
- **Multi-Platform**: Content often has sections for macOS/Windows/Linux/Cloud.
- **Dependencies**: Ruby 3.2+, Jekyll 3.9.5; specific versions in Gemfile.
- **Deployment**: Azure-specific; script handles login, resource creation, but requires manual GitHub secret setup if gh CLI absent.
- **Validation Scores**: Quests are scored; aim for 100% (e.g., all required fields, theme integration).

## Project-Specific Context from Rule Files

From .github/copilot-instructions.md (observed in memory and glob):
- **Principles**: README-First/Last, Front Matter for educational metadata (learning_objectives, target_audience).
- **Workflow**: GitHub Flow with specific branch naming, conventional commits.
- **Documentation**: Always update READMEs, use ADR for decisions.
- **AI Integration**: Use front matter for AI-assisted content; balance with human oversight.

This guide is derived solely from repository contents. Update it as the project evolves using similar discovery processes.
