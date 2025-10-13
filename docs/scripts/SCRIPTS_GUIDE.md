# Scripts Guide

This document provides comprehensive documentation for all automation scripts in the IT-Journey repository.

## Overview

The `scripts/` directory contains automation tools, development utilities, and deployment scripts that streamline development workflows and maintain repository quality.

## Directory Structure

```
scripts/
├── core/                        # Core utilities
│   ├── environment-setup.sh     # Development environment configuration
│   ├── version-manager.sh       # Version management
│   └── README.md
├── development/                 # Development tools
│   ├── build/                   # Build-related scripts
│   │   ├── build-site.sh        # Unified Jekyll build
│   │   ├── create-dockerfile.sh # Docker image creation
│   │   └── create-gemfile.sh    # Gemfile generation
│   ├── content/                 # Content management
│   │   ├── jupyter-to-markdown.sh    # Notebook conversion
│   │   ├── append_feature.py         # Feature addition
│   │   ├── organize-posts.py         # Post organization
│   │   └── requirements.txt          # Python dependencies
│   └── testing/                 # Testing utilities
│       └── cibuild               # CI build script
├── deployment/                  # Deployment automation
│   └── update-settings.sh       # Settings management
├── link-checker.py              # Link health monitoring
├── extract-script.sh            # Script extraction utility
├── generate-zer0-script.sh      # Script generation
└── README.md                    # Scripts overview
```

## Core Scripts

### Environment Setup

**File:** `scripts/core/environment-setup.sh`

**Purpose:** Configure development environment for IT-Journey.

**Features:**
- Cross-platform support (macOS/Linux)
- Auto-detection of project types (Jekyll/Node.js/Docker)
- Interactive configuration mode
- Dependency installation and validation
- Environment variable setup

**Usage:**
```bash
# Interactive setup
./scripts/core/environment-setup.sh

# Non-interactive with defaults
./scripts/core/environment-setup.sh --auto

# Specific environment
./scripts/core/environment-setup.sh --type jekyll

# Dry run (preview without changes)
./scripts/core/environment-setup.sh --dry-run
```

**What It Sets Up:**
- Ruby and Jekyll environment
- Bundler and gem dependencies
- Docker and Docker Compose
- Git configuration
- Development tools

**Environment Variables:**
```bash
# Created in ~/.bashrc or ~/.zshrc
export JEKYLL_ENV=development
export IT_JOURNEY_HOME=/path/to/repo
```

### Version Manager

**File:** `scripts/core/version-manager.sh`

**Purpose:** Unified version management across multiple file formats.

**Features:**
- Multi-format support (package.json, gemspec, markdown frontmatter)
- Semantic versioning (major.minor.patch)
- Auto-commit and tagging
- CHANGELOG.md integration
- Dry-run mode for testing

**Usage:**
```bash
# Bump patch version
./scripts/core/version-manager.sh patch

# Bump minor version
./scripts/core/version-manager.sh minor

# Bump major version
./scripts/core/version-manager.sh major

# Set specific version
./scripts/core/version-manager.sh set 1.2.3

# Dry run (preview changes)
./scripts/core/version-manager.sh patch --dry-run

# With auto-commit and tag
./scripts/core/version-manager.sh patch --commit --tag
```

**Supported Files:**
- `package.json` - Node.js version
- `jekyll-theme-zer0.gemspec` - Ruby gem version
- `_config.yml` - Jekyll site version
- Frontmatter in markdown files

**Version Format:**
```
major.minor.patch[-prerelease][+build]

Examples:
1.0.0
1.2.3-beta
1.2.3-alpha.1
1.2.3+20240101
```

## Development Scripts

### Build Site

**File:** `scripts/development/build/build-site.sh`

**Purpose:** Unified build script for Jekyll site.

**Features:**
- Auto-detection of environment (dev/production)
- Clean build option
- Development server integration
- Build validation
- Error reporting

**Usage:**
```bash
# Development build with server
./scripts/development/build/build-site.sh

# Production build
./scripts/development/build/build-site.sh --production

# Clean build (remove _site first)
./scripts/development/build/build-site.sh --clean

# Build only (no server)
./scripts/development/build/build-site.sh --build-only
```

**Environment Detection:**
```bash
# Checks for:
- JEKYLL_ENV variable
- _config_dev.yml presence
- Docker environment
```

### Create Dockerfile

**File:** `scripts/development/build/create-dockerfile.sh`

**Purpose:** Generate Dockerfile for Jekyll development.

**Usage:**
```bash
# Create Dockerfile in current directory
./scripts/development/build/create-dockerfile.sh

# Create in specific directory
./scripts/development/build/create-dockerfile.sh /path/to/project

# With specific Ruby version
./scripts/development/build/create-dockerfile.sh --ruby 3.2.3
```

**Generated Dockerfile:**
```dockerfile
FROM ruby:3.2.3
WORKDIR /usr/src/app
COPY Gemfile Gemfile.lock ./
RUN bundle install
EXPOSE 4002
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]
```

### Create Gemfile

**File:** `scripts/development/build/create-gemfile.sh`

**Purpose:** Generate Gemfile with standard dependencies.

**Usage:**
```bash
# Create Gemfile in current directory
./scripts/development/build/create-gemfile.sh

# With specific Jekyll version
./scripts/development/build/create-gemfile.sh --jekyll 3.9.5

# With GitHub Pages gem
./scripts/development/build/create-gemfile.sh --github-pages
```

### Jupyter to Markdown

**File:** `scripts/development/content/jupyter-to-markdown.sh`

**Purpose:** Convert Jupyter notebooks to Jekyll-compatible markdown.

**Features:**
- Preserve code blocks and output
- Extract frontmatter from notebook metadata
- Handle images and assets
- Clean output for Jekyll

**Usage:**
```bash
# Convert single notebook
./scripts/development/content/jupyter-to-markdown.sh notebook.ipynb

# Convert all notebooks in directory
./scripts/development/content/jupyter-to-markdown.sh pages/_notebooks/

# With custom output directory
./scripts/development/content/jupyter-to-markdown.sh notebook.ipynb --output pages/_posts/
```

**Requirements:**
```bash
pip install nbconvert jupyter
```

### Append Feature

**File:** `scripts/development/content/append_feature.py`

**Purpose:** Add features to existing content files.

**Usage:**
```python
# Python script usage
python3 scripts/development/content/append_feature.py \
  --file pages/_posts/2025-10-13-my-post.md \
  --feature "toc: true"

# Add multiple features
python3 scripts/development/content/append_feature.py \
  --file pages/_posts/2025-10-13-my-post.md \
  --features "toc: true" "mermaid: true"
```

### Organize Posts

**File:** `scripts/development/content/organize-posts.py`

**Purpose:** Automated organization of blog posts by categories.

**Features:**
- Category-based directory organization
- Frontmatter preservation
- Dry-run mode
- Backup creation

**Usage:**
```bash
# Organize all posts
python3 scripts/development/content/organize-posts.py

# Dry run (preview only)
python3 scripts/development/content/organize-posts.py --dry-run

# Specific source directory
python3 scripts/development/content/organize-posts.py \
  --source pages/_posts/

# With backup
python3 scripts/development/content/organize-posts.py --backup
```

**Organization Structure:**
```
pages/_posts/
├── development/
│   └── 2025-10-13-dev-topic.md
├── automation/
│   └── 2025-10-12-automation-topic.md
└── jekyll/
    └── 2025-10-11-jekyll-topic.md
```

## Link Checker

**File:** `scripts/link-checker.py`

**Purpose:** Comprehensive link validation with AI analysis.

**Features:**
- Multiple scope options
- AI-powered failure analysis
- GitHub issue creation
- Configurable timeouts
- Detailed reporting

**Usage:**
```bash
# Basic website check
python3 scripts/link-checker.py --scope website

# Comprehensive with AI
python3 scripts/link-checker.py \
  --scope website \
  --analysis-level comprehensive \
  --timeout 30

# Create GitHub issue
python3 scripts/link-checker.py \
  --scope website \
  --create-issue \
  --repository bamr87/it-journey

# Check specific content
python3 scripts/link-checker.py --scope posts
python3 scripts/link-checker.py --scope quests
python3 scripts/link-checker.py --scope docs
```

**See Also:** [Testing Frameworks](../testing/TESTING_FRAMEWORKS.md)

## Deployment Scripts

### Update Settings

**File:** `scripts/deployment/update-settings.sh`

**Purpose:** Update repository settings and configurations.

**Usage:**
```bash
# Update all settings
./scripts/deployment/update-settings.sh

# Update specific setting
./scripts/deployment/update-settings.sh --setting branch_protection

# Dry run
./scripts/deployment/update-settings.sh --dry-run
```

## Generated Scripts

### Zer0 to Hero Scripts

**Files:**
- `scripts/zer0-to-hero-complete.sh` - Complete setup script
- `scripts/zer0-to-hero-generated.sh` - Auto-generated version

**Purpose:** Complete environment setup for new contributors.

**Usage:**
```bash
# Run complete setup
./scripts/zer0-to-hero-complete.sh

# With specific options
./scripts/zer0-to-hero-complete.sh --docker-only
```

**What It Does:**
1. Checks system prerequisites
2. Installs required dependencies
3. Clones repository
4. Sets up development environment
5. Runs initial build
6. Validates setup

## Script Development Guidelines

### Script Standards

**File Headers:**
```bash
#!/usr/bin/env bash
#
# @file scripts/category/script-name.sh
# @description Brief description of what the script does
# @author IT-Journey Team
# @created 2025-10-13
# @version 1.0.0
#
# @usage
#   ./script-name.sh [options]
#
# @example
#   ./script-name.sh --dry-run
```

**Error Handling:**
```bash
# Exit on error
set -e

# Exit on undefined variable
set -u

# Pipe failure detection
set -o pipefail

# Custom error handler
error_exit() {
    echo "Error: $1" >&2
    exit 1
}

# Usage
command || error_exit "Command failed"
```

**Logging:**
```bash
# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}
```

**Dry Run Support:**
```bash
DRY_RUN=false

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Use in commands
if [ "$DRY_RUN" = true ]; then
    echo "Would run: command"
else
    command
fi
```

### Testing Scripts

**Local Testing:**
```bash
# Test with dry run
./script-name.sh --dry-run

# Test with verbose output
./script-name.sh --verbose

# Test error handling
./script-name.sh --invalid-option  # Should show error
```

**CI Testing:**
```bash
# Include in CI workflow
- name: Test Scripts
  run: |
    chmod +x scripts/**/*.sh
    shellcheck scripts/**/*.sh
    ./scripts/test-all.sh
```

### Documentation

**README for Each Directory:**
```markdown
# Directory Name

Description of scripts in this directory.

## Scripts

### script-name.sh

Description, usage, and examples.

## Dependencies

List of required tools and libraries.

## Related

Links to related documentation.
```

## Common Tasks

### Adding New Script

1. **Create script file:**
```bash
touch scripts/category/new-script.sh
chmod +x scripts/category/new-script.sh
```

2. **Add standard header:**
```bash
# Copy template header
# Update metadata fields
```

3. **Implement functionality:**
```bash
# Add error handling
# Add logging
# Add dry-run support
```

4. **Test locally:**
```bash
./scripts/category/new-script.sh --dry-run
```

5. **Update documentation:**
```bash
# Update this file
# Update category README
```

### Debugging Scripts

**Enable Debug Mode:**
```bash
# Add to script
set -x  # Print commands as executed

# Or run with bash -x
bash -x scripts/category/script-name.sh
```

**Check Syntax:**
```bash
# Use shellcheck
shellcheck scripts/category/script-name.sh

# Check all scripts
find scripts -name "*.sh" -exec shellcheck {} \;
```

## Best Practices

### Security

- Never commit secrets or credentials
- Use environment variables for sensitive data
- Validate all user inputs
- Use quotes around variables
- Check file permissions

### Performance

- Cache expensive operations
- Minimize external command calls
- Use built-in bash features when possible
- Parallel processing for independent tasks

### Maintainability

- Clear, descriptive names
- Comprehensive comments
- Consistent formatting
- Modular design
- Version control

## Additional Resources

- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)
- [ShellCheck](https://www.shellcheck.net/)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)

---

**Last Updated**: 2025-10-13  
**Version**: 1.0.0

