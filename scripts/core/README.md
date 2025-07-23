<!--
@file scripts/core/README.md
@description Documentation for core utility scripts
@author IT-Journey Team <team@it-journey.org>
@created 2025-07-07
@lastModified 2025-07-07
@version 1.0.0

@relatedIssues 
  - Script consolidation: Document core utilities

@relatedEvolutions
  - v1.0.0: Initial documentation for core scripts

@dependencies
  - ../version-manager.sh: Unified version management
  - ../environment-setup.sh: Environment configuration

@changelog
  - 2025-07-07: Initial creation - ITJ

@usage Reference documentation for core scripts
@notes Core utilities that provide foundational functionality
-->

# Core Utility Scripts

Essential scripts that provide foundational functionality across all IT-Journey projects.

## Scripts in this Directory

### `version-manager.sh`
Unified version management script that handles versioning across multiple file types and project formats.

**Capabilities:**
- Package.json semantic versioning (major.minor.patch)
- Ruby gemspec version updates
- Markdown frontmatter version tracking
- Automatic CHANGELOG.md updates
- Git commit and tagging automation

**Usage Examples:**
```bash
# Increment patch version across all files
./version-manager.sh patch

# Update only markdown frontmatter versions for staged files
./version-manager.sh frontmatter

# Preview major version bump without changes
./version-manager.sh major --dry-run

# Auto-commit version changes
./version-manager.sh minor --auto-commit
```

**Supported File Types:**
- `package.json` - Node.js projects
- `*.gemspec` - Ruby gems
- `*.md` - Markdown files with frontmatter
- `CHANGELOG.md` - Automatic changelog entries

### `environment-setup.sh`
Comprehensive development environment setup script with intelligent project type detection.

**Capabilities:**
- System information detection and display
- Package manager installation (Homebrew/APT/YUM)
- Core development tools (Git, Docker, VS Code, GitHub CLI)
- Language environment setup (Ruby, Node.js)
- Project-specific dependency installation
- Git configuration with GitHub integration
- Environment validation and verification

**Usage Examples:**
```bash
# Auto-detect project type and setup environment
./environment-setup.sh

# Interactive setup with user prompts
./environment-setup.sh --interactive

# Jekyll-specific environment setup
./environment-setup.sh --project-type jekyll

# Preview what would be installed
./environment-setup.sh --dry-run
```

**Supported Project Types:**
- `auto` - Automatic detection based on project files
- `jekyll` - Jekyll/Ruby static site projects
- `node` - Node.js/JavaScript applications
- `ruby` - Ruby gem development
- `general` - Basic development tools only

## Design Principles

### Design for Failure (DFF)
- Comprehensive error handling with meaningful messages
- Environment validation before making changes
- Rollback capabilities for failed operations
- Graceful degradation when optional tools are missing

### Don't Repeat Yourself (DRY)
- Single source of truth for version management
- Unified interface for environment setup
- Shared utility functions and error handling
- Configurable defaults with override options

### Keep It Simple (KIS)
- Clear command-line interfaces with help messages
- Intelligent defaults that work out-of-the-box
- Step-by-step progress feedback
- Self-documenting code with inline comments

### Collaboration (COLAB)
- Consistent logging and output formatting
- Standardized file headers with metadata
- Cross-platform compatibility (macOS/Linux)
- Integration with Git workflows

## Integration with Other Scripts

Core scripts are designed to be used by other scripts in the IT-Journey ecosystem:

```bash
# Build scripts can use version manager
./scripts/development/build/build-site.sh

# Deployment scripts can verify environment
./scripts/deployment/update-settings.sh
```

## Error Handling

All core scripts implement comprehensive error handling:

1. **Input Validation**: Check arguments and environment
2. **Dependency Verification**: Ensure required tools are available
3. **State Validation**: Verify system state before making changes
4. **Rollback Support**: Provide mechanisms to undo failed operations
5. **Meaningful Messages**: Clear error descriptions with suggested fixes

## Configuration

Core scripts respect environment variables and project-specific configurations:

### Environment Variables
- `JEKYLL_ENV`: Jekyll build environment
- `NODE_ENV`: Node.js environment
- `GIT_USER_NAME`: Git configuration override
- `GIT_USER_EMAIL`: Git configuration override

### Project Detection
Scripts automatically detect project types based on file presence:

- **Jekyll**: `_config.yml` + `Gemfile`
- **Node.js**: `package.json`
- **Ruby Gem**: `*.gemspec`
- **General**: Default fallback

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x scripts/core/*.sh
   ```

2. **Missing Dependencies**
   ```bash
   ./environment-setup.sh --interactive
   ```

3. **Git Not Configured**
   ```bash
   ./environment-setup.sh --interactive
   ```

### Debug Mode

Enable verbose output for debugging:
```bash
./version-manager.sh --help
./environment-setup.sh --dry-run
```

## Contributing

When adding new core scripts:

1. Follow the standardized file header format
2. Implement comprehensive error handling
3. Include help messages and examples
4. Add dry-run mode for testing
5. Update this README with documentation

## Related Documentation

- [Main Scripts README](../README.md)
- [Development Scripts](../development/README.md)
- [Deployment Scripts](../deployment/README.md)
