# IT-Journey Repository Structure

This document provides a comprehensive overview of the IT-Journey repository structure, explaining the purpose of each directory and major component.

## Directory Tree Overview

```
it-journey/
├── .github/                    # GitHub configuration and workflows
│   ├── workflows/             # CI/CD automation workflows
│   ├── instructions/          # AI assistant instructions
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   └── copilot-instructions.md
├── _config.yml                # Main Jekyll configuration
├── _config_dev.yml           # Development configuration
├── _data/                    # Site data files
│   ├── navigation/           # Navigation configurations
│   └── ui-text.yml          # UI text and translations
├── _includes/                # Reusable HTML components
├── _layouts/                 # Page layout templates
├── assets/                   # Static assets
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript files
│   ├── images/              # Image files
│   └── svg/                 # SVG graphics
├── docs/                     # Developer documentation (THIS)
│   ├── architecture/        # System design and structure
│   ├── setup/              # Installation and configuration
│   ├── workflows/          # CI/CD documentation
│   ├── scripts/            # Script documentation
│   ├── testing/            # Testing framework docs
│   └── standards/          # Coding and content standards
├── pages/                    # Content collections
│   ├── _posts/             # Blog posts and journals
│   ├── _docs/              # Learning resources
│   ├── _quests/            # Gamified learning experiences
│   ├── _notebooks/         # Jupyter notebooks
│   ├── _notes/             # Personal notes
│   ├── _about/             # About pages
│   └── _quickstart/        # Quick start guides
├── scripts/                  # Automation scripts
│   ├── core/               # Core utilities
│   ├── development/        # Development tools
│   └── deployment/         # Deployment automation
├── test/                     # Testing infrastructure
│   ├── hyperlink-guardian/ # Link validation system
│   └── quest-validator/    # Quest content validator
├── Gemfile                   # Ruby dependencies
├── package.json             # Node.js dependencies (if any)
├── docker-compose.yml       # Docker development setup
├── Dockerfile              # Container image definition
└── README.md               # Main project README
```

## Core Directories

### `.github/`
GitHub-specific configuration and automation.

**Key Files:**
- `workflows/*.yml` - GitHub Actions workflows for CI/CD
- `instructions/*.md` - AI assistant context and guidelines
- `ISSUE_TEMPLATE/*.md` - Structured issue templates
- `copilot-instructions.md` - GitHub Copilot configuration

**Purpose:** Automates testing, validation, deployment, and provides context for AI tools.

### `_config.yml` & `_config_dev.yml`
Jekyll configuration files defining site structure, collections, and behavior.

**_config.yml:**
- Production configuration
- Remote theme: `bamr87/zer0-mistakes`
- Collections definitions
- Plugin configuration
- Site metadata

**_config_dev.yml:**
- Development-specific settings
- Local server configuration
- Development-friendly defaults

### `_data/`
Structured data files for site content that isn't posts or pages.

**Contents:**
- `navigation/*.yml` - Site navigation structures
- `ui-text.yml` - Interface text and translations
- `prerequisites.yml` - Learning prerequisites data
- `statistics_config.yml` - Content statistics configuration

**Usage:** Accessible via `site.data` in Liquid templates.

### `_includes/`
Reusable HTML/Liquid components included in layouts and pages.

**Contents:**
- `content_statistics/` - Content metrics displays
- `content_stats_direct.html` - Direct statistics integration

**Purpose:** DRY principle - write once, include anywhere.

### `_layouts/`
Page templates that define structure and presentation.

**Key Layouts:**
- `javascript.html` - JavaScript-heavy pages
- (Most layouts inherited from zer0-mistakes theme)

**Purpose:** Consistent page structure across the site.

### `assets/`
Static files served to browsers.

**Structure:**
- `css/` - Custom stylesheets (main.scss, custom.css)
- `js/` - JavaScript files (12 files)
- `images/` - Images (177 files: PNG, GIF, XCF)
- `svg/` - SVG graphics (22 files)
- `gif/` - Animated GIFs
- `particles.json` - Particle.js configuration

**Asset Management:**
- Images: Use descriptive names, optimize before committing
- CSS: Compile SCSS to CSS via Jekyll
- JS: Modular approach, minimize dependencies

## Content Collections (`pages/`)

All user-facing content lives in the `pages/` directory, organized into Jekyll collections.

### `pages/_posts/`
Blog posts and journal entries following Jekyll conventions.

**Naming Convention:** `YYYY-MM-DD-title-slug.md`

**Purpose:** 
- Technical articles
- Learning reflections
- Project updates
- Tutorial content

**Current Count:** 85 markdown files

### `pages/_docs/`
Reference documentation and learning resources for external tools.

**Structure:**
- `jekyll/` - Jekyll-specific documentation
- `index.md` - Documentation library index

**Purpose:**
- Tool and technology references
- External documentation summaries
- Learning resources for IT-Journey platform users

**Note:** This is separate from `docs/` (developer documentation).

### `pages/_quests/`
Gamified learning experiences with fantasy themes and progressive difficulty.

**Key Features:**
- Binary level system (0000, 0001, 0010, 0011, 0100, 0101, 0110, 0111, 1000, etc.)
- RPG-style narratives
- Hands-on projects
- Achievement tracking

**Contents:** 53 markdown files + supporting scripts (14 .sh, 3 .ps1, 2 .ipynb, 2 .yml)

**Purpose:** Transform technical learning into engaging adventures.

### `pages/_notebooks/`
Jupyter notebooks for interactive code examples and data analysis.

**Contents:** 6 .ipynb files + 5 markdown files

**Purpose:**
- Runnable code demonstrations
- Data science examples
- Interactive tutorials

### `pages/_notes/`
Personal development notes and work-in-progress content.

**Contents:** 33 markdown + 2 Python + 2 Ruby files

**Purpose:**
- Draft content
- Research notes
- Development documentation

### `pages/_about/`
Information about the IT-Journey project and site.

**Contents:** 12 markdown + 2 YAML + 1 text file

**Purpose:**
- Project information
- Feature descriptions
- Site documentation
- Contributor profiles

### `pages/_quickstart/`
Quick reference guides for rapid learning.

**Contents:** 6 markdown files

**Purpose:**
- Fast onboarding
- Common task references
- Cheat sheets

## Development Infrastructure

### `docs/` (Developer Documentation)
**YOU ARE HERE** - Technical documentation for contributors and AI agents.

**Structure:**
- `architecture/` - System design and structure docs
- `setup/` - Installation and environment setup
- `workflows/` - CI/CD and automation docs
- `scripts/` - Script documentation
- `testing/` - Testing framework references
- `standards/` - Coding and content standards

**Purpose:** Enable effective contribution by developers and AI agents.

### `scripts/`
Automation tools and development utilities.

**Organization:**
- `core/` - Essential utilities (environment-setup.sh, version-manager.sh)
- `development/` - Development tools (build, content, testing)
- `deployment/` - Deployment automation
- `link-checker.py` - Unified link health monitoring

**Purpose:** Automate repetitive tasks, ensure quality, streamline development.

### `test/`
Testing frameworks and validation tools.

**Components:**
- `hyperlink-guardian/` - Link validation with AI analysis
- `quest-validator/` - Quest content structure validation
- `test-results/` - Test output artifacts

**Purpose:** Automated quality assurance and proactive monitoring.

## Configuration Files

### `Gemfile`
Ruby gem dependencies for Jekyll and plugins.

**Key Dependencies:**
- `github-pages` ~> 231 (includes Jekyll)
- `jekyll-theme-zer0` (theme gem)
- `ffi` ~> 1.17.0 (system library bindings)
- `webrick` ~> 1.8 (development server)

### `docker-compose.yml` & `Dockerfile`
Container-based development environment.

**Benefits:**
- Consistent development environment
- No local Ruby installation required
- Easy onboarding for new contributors

### `frontmatter.json`
Frontmatter schema definitions for content validation.

**Purpose:** Define required and optional fields for different content types.

## File Naming Conventions

### Posts
**Format:** `YYYY-MM-DD-slug-with-hyphens.md`

**Example:** `2025-10-13-el-capitan-boot-loader.md`

### Quests
**Format:** `descriptive-quest-name.md`

**Example:** `link-to-the-future-automated-hyperlink-checking-and-error-reporting.md`

### Docs
**Format:** `tool-topic-description.md` or `tool-specific-feature.md`

**Example:** `jekyll-diagram-with-mermaid.md`

### Scripts
**Format:** `descriptive-action-name.sh` or `descriptive-action-name.py`

**Example:** `environment-setup.sh`, `link-checker.py`

### Documentation
**Format:** `UPPERCASE_TOPIC.md` for main docs, `descriptive-name.md` for guides

**Example:** `REPOSITORY_STRUCTURE.md`, `setup-guide.md`

## Content Organization Principles

### Separation of Concerns
- **Developer docs** (`docs/`) - Technical repository information
- **Learning resources** (`pages/_docs/`) - Educational external references
- **Active content** (`pages/_posts/`, `pages/_quests/`) - Published content
- **Work in progress** (`pages/_notes/`) - Draft and experimental content

### Collection-Based Organization
- Use Jekyll collections for logical content grouping
- Each collection has specific purpose and frontmatter requirements
- Collections enable flexible querying and display

### Asset Management
- Keep assets close to content when possible
- Use descriptive, hyphenated filenames
- Optimize images before committing
- Prefer SVG for icons and graphics

### Version Control
- Main branch: `main`
- Automated deployments on push to main
- Feature branches for development
- Pull requests required for changes

## Build Process

### Static Site Generation
1. Jekyll reads `_config.yml` configuration
2. Processes collections from `pages/` directory
3. Applies layouts from `_layouts/` (theme + local)
4. Includes components from `_includes/`
5. Compiles SCSS to CSS
6. Generates static HTML in `_site/`

### Local Development
```bash
bundle exec jekyll serve --config _config_dev.yml
```

### Production Build
```bash
JEKYLL_ENV=production bundle exec jekyll build
```

### Docker Development
```bash
docker-compose up
```

## Navigation Structure

Navigation is defined in `_data/navigation/*.yml` files:
- `main.yml` - Primary site navigation
- `about.yml` - About section navigation
- `docs.yml` - Documentation navigation
- `posts.yml` - Blog post navigation
- `quickstart.yml` - Quick start navigation

These are referenced in `_config.yml` and used by layouts to generate navigation menus.

## Remote Theme Integration

IT-Journey uses the `zer0-mistakes` theme as a remote theme:
- Theme repo: https://github.com/bamr87/zer0-mistakes
- Specified in `_config.yml`: `remote_theme: "bamr87/zer0-mistakes"`
- Local files override theme files when present
- Theme provides base layouts, includes, and styles

## Next Steps

- **For architecture details:** See [JEKYLL_IMPLEMENTATION.md](JEKYLL_IMPLEMENTATION.md)
- **For content standards:** See [../standards/FRONTMATTER_STANDARDS.md](../standards/FRONTMATTER_STANDARDS.md)
- **For development setup:** See [../setup/DEVELOPMENT_ENVIRONMENT.md](../setup/DEVELOPMENT_ENVIRONMENT.md)
- **For contribution workflow:** See [../CONTRIBUTING_DEVELOPER.md](../CONTRIBUTING_DEVELOPER.md)

---

**Last Updated**: 2025-10-13  
**Version**: 1.0.0

