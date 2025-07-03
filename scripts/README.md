# IT-Journey Scripts

This directory contains automation scripts and utilities for maintaining the IT-Journey platform.

## Scripts Overview

### `update-settings.sh`

Automated script for updating configuration files in the `pages/_about/settings/` directory.

**Purpose:**

- Synchronizes `_config.yml` from root to settings directory
- Generates current tree structure of the repository (respecting `.gitignore`)
- Creates sitemap data for all markdown and HTML files (gitignore-filtered)
- Updates documentation files with enhanced content

**Usage:**

```bash
# Run manually
./scripts/update-settings.sh

# Or with environment variables
SETTINGS_DIR="custom/path" CONFIG_FILE="custom-config.yml" ./scripts/update-settings.sh
```

**Automated Execution:**
This script is automatically executed by the GitHub Actions workflow `.github/workflows/update-settings.yml` whenever:
- Changes are pushed to `_config.yml` on the main branch
- The workflow is manually triggered

**Dependencies:**
- `tree` command (optional, but recommended for better output)
- `git` (for repository operations)
- Standard Unix utilities (`find`, `grep`, `sort`, etc.)

**Output Files:**
- `pages/_about/settings/_config.yml` - Copy of root configuration
- `pages/_about/settings/tree.txt` - Repository structure
- `pages/_about/settings/sitemap-data.yml` - Site navigation data
- `pages/_about/settings/config.md` - Enhanced configuration documentation
- `pages/_about/settings/tree.md` - Enhanced tree structure documentation
- `pages/_about/settings/sitemap.md` - Enhanced sitemap documentation

## Integration with IT-Journey Principles

### Design for Failure (DFF)
- Error handling with `set -e`
- Fallback mechanisms for missing dependencies
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
