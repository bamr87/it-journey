# IT-Journey Scripts Directory

This directory contains all automation scripts and utilities for the IT-Journey platform, organized by function and purpose.

## 📁 Directory Structure

```
scripts/
├── README.md                    # This file
├── core/                        # Core utility scripts
│   ├── version-manager.sh       # Unified version management
│   └── environment-setup.sh     # Environment configuration
├── development/                 # Development tools and utilities
│   ├── build/                   # Build automation scripts
│   ├── content/                 # Content processing tools
│   └── testing/                 # Testing and CI utilities
├── deployment/                  # Deployment automation
│   └── update-settings.sh       # Configuration sync
```

## 🚀 Quick Start

### Core Scripts

#### Version Management
```bash
# Increment patch version across all project files`
./scripts/core/version-manager.sh patch

# Update only markdown frontmatter versions
./scripts/core/version-manager.sh frontmatter

# Preview version changes without applying
./scripts/core/version-manager.sh minor --dry-run
```

#### Environment Setup
```bash
# Auto-detect and setup development environment
./scripts/core/environment-setup.sh

# Interactive setup with prompts
./scripts/core/environment-setup.sh --interactive

# Jekyll-specific setup
./scripts/core/environment-setup.sh --project-type jekyll
```

### Development Scripts

#### Building Projects
```bash
# Auto-detect and build for development
./scripts/development/build/build-site.sh

# Production Jekyll build
./scripts/development/build/build-site.sh --type jekyll --env production

# Clean build with development server
./scripts/development/build/build-site.sh --clean --serve
```

### Deployment Scripts

#### Configuration Updates
```bash
# Update settings and configuration files
./scripts/deployment/update-settings.sh

# With custom paths
SETTINGS_DIR="custom/path" ./scripts/deployment/update-settings.sh
```

## 🎯 Script Categories

### Core Utilities (`core/`)
Essential scripts that provide foundational functionality across all IT-Journey projects.

- **version-manager.sh**: Unified version management for package.json, gemspecs, and markdown frontmatter
- **environment-setup.sh**: Comprehensive development environment setup

### Development Tools (`development/`)
Scripts specifically for development workflows and content creation.

#### Build Tools (`development/build/`)
- **build-site.sh**: Unified build script for Jekyll, Node.js, and Docker projects
- **create-dockerfile.sh**: Docker configuration generation
- **create-gemfile.sh**: Ruby Gemfile generation

#### Content Tools (`development/content/`)
- **jupyter-to-markdown.sh**: Convert Jupyter notebooks to markdown
- **append_feature.py**: Add features to markdown files

#### Testing Tools (`development/testing/`)
- **cibuild**: Continuous integration build script

### Deployment Scripts (`deployment/`)
Automation for deploying and maintaining live environments.

- **update-settings.sh**: Synchronize configuration files and generate site metadata

### Legacy Scripts (`legacy/`)
Deprecated scripts maintained for reference and migration purposes.

## 🏗️ IT-Journey Principles Integration

All scripts follow the core IT-Journey development principles:

### Design for Failure (DFF)
- Comprehensive error handling with meaningful messages
- Graceful degradation when dependencies are missing
- Rollback capabilities for destructive operations
- Input validation and environment checks

### Don't Repeat Yourself (DRY)
- Shared functionality extracted into common utilities
- Single source of truth for version management
- Unified interfaces for similar operations
- Configurable templates and patterns

### Keep It Simple (KIS)
- Clear, descriptive help messages for all scripts
- Intelligent defaults with simple overrides
- Consistent command-line interfaces
- Self-documenting code with inline comments

### Collaboration (COLAB)
- Standardized file headers with metadata
- Consistent logging and output formatting
- Clear documentation and usage examples
- Version tracking and change attribution

### AI-Powered Development (AIPD)
- Scripts designed to work with AI-assisted workflows
- Structured output formats for AI consumption
- Automated documentation generation
- Integration with AI evolution engines

## 📋 Usage Patterns

### Daily Development Workflow
```bash
# 1. Setup environment (first time)
./scripts/core/environment-setup.sh --interactive

# 2. Build and test
./scripts/development/build/build-site.sh --clean --serve

# 3. Update versions when ready
./scripts/core/version-manager.sh patch --auto-commit

# 4. Deploy configuration updates
./scripts/deployment/update-settings.sh
```

### Production Release Workflow
```bash
# 1. Version bump for release
./scripts/core/version-manager.sh minor --auto-commit

# 2. Production build
./scripts/development/build/build-site.sh --env production

# 3. Final configuration sync
./scripts/deployment/update-settings.sh
```

## 🔧 Configuration

### Environment Variables
Scripts respect these environment variables when available:

- `SETTINGS_DIR`: Custom settings directory path
- `CONFIG_FILE`: Custom configuration file name
- `JEKYLL_ENV`: Jekyll environment (development/production)
- `NODE_ENV`: Node.js environment

### Project Detection
Scripts automatically detect project types based on:

- **Jekyll**: Presence of `_config.yml` and `Gemfile`
- **Node.js**: Presence of `package.json`
- **Ruby Gem**: Presence of `*.gemspec`
- **Docker**: Presence of `Dockerfile`

## 🧪 Testing

All scripts include dry-run modes for safe testing:

```bash
# Test version management without changes
./scripts/core/version-manager.sh major --dry-run

# Preview environment setup
./scripts/core/environment-setup.sh --dry-run

# Validate build configuration
./scripts/development/build/build-site.sh --dry-run
```

## 📚 Additional Resources

- [Script Consolidation Plan](../docs/script-consolidation-plan.md)
- [IT-Journey Development Principles](../README.md#principles)
- [Contributing Guidelines](../CONTRIBUTING.md)

## 🆘 Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure scripts are executable
   ```bash
   chmod +x scripts/**/*.sh
   ```

2. **Missing Dependencies**: Run environment setup
   ```bash
   ./scripts/core/environment-setup.sh
   ```

3. **Git Configuration**: Use interactive setup
   ```bash
   ./scripts/core/environment-setup.sh --interactive
   ```

For more help, check individual script help messages:
```bash
./scripts/core/version-manager.sh --help
```
- Clear error messages and logging

### Don't Repeat Yourself (DRY)
- Reusable functions for common operations
- Single source of truth for configuration
- Shared utilities across workflows

### Keep It Simple (KIS)
- Clear, readable script structure
- Simple command-line interface
- Minimal dependencies

### AI-Powered Development (AIPD)
- Scripts can be enhanced with AI-generated improvements
- Automated documentation generation
- Intelligent content organization

### Release Early and Often (REnO)
- Continuous integration support
- Automated deployment triggers
- Incremental improvement capabilities

## Contributing

When adding new scripts:

1. Follow the established naming convention (`kebab-case.sh`)
2. Include comprehensive error handling
3. Add documentation to this README
4. Make scripts executable (`chmod +x`)
5. Test on multiple platforms when possible
6. Follow IT-Journey coding principles

## Related Files

- **[GitHub Workflow](/.github/workflows/update-settings.yml)** - Automation trigger
- **[Configuration Documentation](/pages/_about/settings/config.md)** - Generated documentation
- **[Tree Structure](/pages/_about/settings/tree.md)** - Repository structure
- **[Sitemap](/pages/_about/settings/sitemap.md)** - Navigation map

---

*For questions or improvements, please open an issue or contribute via pull request.*
