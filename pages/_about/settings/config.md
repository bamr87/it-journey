---
title: Jekyll Configuration & Site Structure
excerpt: Configuration file contents, site tree structure, and automated regeneration workflows.
lastmod: 2025-07-03T17:12:14.461Z
config-dir: pages/_about/settings
config-file: _config.yml
permalink: /about/config/
tags:
  - configuration
  - jekyll
  - automation
  - ci-cd
  - site-structure
---

## Overview

This page contains the Jekyll configuration file, site tree structure, and automated workflows for maintaining configuration synchronization across the IT-Journey platform.

## Configuration Management

### Automated Updates

The configuration files in this directory are automatically updated via GitHub Actions workflow whenever the root \`_config.yml\` file changes. This ensures consistency and reduces manual maintenance overhead.

**Trigger Events:**
- Push to main branch with changes to \`_config.yml\`
- Manual workflow dispatch

### Manual Regeneration

If you need to manually regenerate the configuration files, use these commands:

#### PowerShell (Windows)
```powershell
# Regenerate Config File
cd ~/github/{{ site.local_repo }}
cp {{ page.config-file }} {{ page.config-dir }}/config-utf16.txt
Get-Content {{ page.config-dir }}/config-utf16.txt | Set-Content -Encoding UTF8 {{ page.config-dir }}/{{ page.config-file }}

# Generate tree structure
tree /f > {{ page.config-dir }}/tree-utf16.txt
Get-Content {{ page.config-dir }}/tree-utf16.txt -Encoding Unicode | Set-Content -Encoding UTF8 {{ page.config-dir }}/tree.txt
```

#### Bash (Linux/macOS)
```bash
# Regenerate Config File
cd ~/github/{{ site.local_repo }}
cp {{ page.config-file }} {{ page.config-dir }}/{{ page.config-file }}

# Generate tree structure (respecting .gitignore)
# This will automatically exclude files/directories listed in .gitignore
if command -v tree >/dev/null 2>&1; then
  ignore_pattern=\$(generate_gitignore_pattern)
  tree -a -I "\$ignore_pattern" --dirsfirst --charset ascii > {{ page.config-dir }}/tree.txt
else
  # Fallback for systems without tree command
  find . -type d | grep -v -E "(\$(generate_gitignore_pattern))" | sort > {{ page.config-dir }}/tree.txt
fi
```

### Gitignore Integration

The tree structure and sitemap generation **automatically respect the \`.gitignore\` file**, ensuring that:

- Files and directories listed in \`.gitignore\` are excluded from the tree structure
- Sitemap generation skips ignored files
- Documentation remains clean and relevant
- Sensitive or build artifacts are not included in public documentation

**Current .gitignore patterns respected:**
```ignore
_site
.sass-cache
.jekyll-cache
.jekyll-metadata
_algolia_api_key
Gemfile.lock
.obsidian
pages/_notes/.DS_Store
*.DS_Store
.env
```

## Jekyll Configuration

Current configuration from \`{{ page.config-file }}\`:

```yml
{% include_relative {{ page.config-file }} %}
```

## Site Tree Structure

Current directory structure (auto-generated):

```
{% include_relative tree.txt %}
```

## Site Map Data

Site structure and page information:

```yml
{% include_relative sitemap-data.yml %}
```

## Related Files

- **[Tree Structure](tree.html)** - Detailed site tree visualization
- **[Sitemap](sitemap.html)** - Complete site navigation map
- **[Raw Config File]({{ page.config-file }})** - Direct access to configuration
- **[GitHub Workflow](/.github/workflows/update-settings.yml)** - Automation workflow

## Workflow Integration

This configuration management follows IT-Journey's core principles:

### Design for Failure (DFF)
- Automated backups of configuration files
- Fallback to manual regeneration processes
- Error handling in workflow steps

### Don't Repeat Yourself (DRY)
- Single source of truth for configuration
- Automated synchronization across settings
- Reusable workflow components

### AI-Powered Development (AIPD)
- AI-generated documentation updates
- Intelligent workflow optimization
- Automated content enhancement

### Release Early and Often (REnO)
- Continuous integration for configuration changes
- Automatic deployment of updates
- Incremental improvement processes

---

*Last updated: {{ page.lastmod }}*  
*Workflow: [update-settings.yml](/.github/workflows/update-settings.yml)*
