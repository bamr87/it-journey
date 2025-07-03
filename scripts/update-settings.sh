#!/bin/bash

# Helper script for updating settings configuration files
# This script is used by the GitHub Actions workflow and can also be run manually
# 
# Following IT-Journey principles:
# - DRY: Single source of truth for update logic
# - DFF: Error handling and graceful degradation  
# - KIS: Clear, simple functions with single responsibilities
# - AIPD: AI-enhanced automation with human oversight

set -e

# Configuration
SETTINGS_DIR="${SETTINGS_DIR:-pages/_about/settings}"
CONFIG_FILE="${CONFIG_FILE:-_config.yml}"
REPO_ROOT="$(git rev-parse --show-toplevel)"

echo "🚀 Starting settings update process..."
echo "📁 Settings directory: $SETTINGS_DIR"
echo "⚙️ Config file: $CONFIG_FILE"

# Create settings directory if it doesn't exist
mkdir -p "$SETTINGS_DIR"

# Function to generate current timestamp
get_timestamp() {
    date -u '+%Y-%m-%dT%H:%M:%S.000Z'
}

# Function to copy config file
copy_config() {
    echo "📋 Copying configuration file..."
    cp "$CONFIG_FILE" "$SETTINGS_DIR/$CONFIG_FILE"
    echo "✅ Configuration file copied successfully"
}

# Function to generate gitignore pattern for tree command
generate_gitignore_pattern() {
    local pattern=""
    local separator=""
    
    # Default exclusions
    local default_exclusions=".git|.github|node_modules|vendor|.bundle"
    pattern="$default_exclusions"
    separator="|"
    
    # Parse .gitignore file if it exists
    if [ -f ".gitignore" ]; then
        while IFS= read -r line; do
            # Skip empty lines and comments
            if [ -n "$line" ] && [[ ! "$line" =~ ^[[:space:]]*# ]]; then
                # Remove leading/trailing whitespace
                line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
                
                # Handle different gitignore patterns
                if [[ "$line" == */ ]]; then
                    # Directory pattern - remove trailing slash
                    dir_pattern="${line%/}"
                    pattern="${pattern}${separator}${dir_pattern}"
                elif [[ "$line" == *.* ]]; then
                    # File extension pattern
                    pattern="${pattern}${separator}${line}"
                else
                    # General pattern (files or directories)
                    pattern="${pattern}${separator}${line}"
                fi
                separator="|"
            fi
        done < ".gitignore"
    fi
    
    echo "$pattern"
}

# Function to generate tree structure
generate_tree() {
    echo "🌳 Generating tree structure..."
    
    # Get gitignore pattern
    local ignore_pattern
    ignore_pattern=$(generate_gitignore_pattern)
    
    if command -v tree >/dev/null 2>&1; then
        echo "📋 Using tree command with gitignore patterns..."
        echo "🚫 Ignoring: $ignore_pattern"
        tree -a -I "$ignore_pattern" --dirsfirst --charset ascii > "$SETTINGS_DIR/tree.txt"
    else
        echo "⚠️ Tree command not available, generating basic structure with gitignore filtering..."
        # Use find with gitignore patterns
        find . -type d | grep -v -E "($ignore_pattern)" | sort > "$SETTINGS_DIR/tree.txt"
    fi
    echo "✅ Tree structure generated successfully"
}

# Function to check if file should be ignored based on gitignore
should_ignore_file() {
    local file="$1"
    
    # Remove leading ./ if present for consistent matching
    file="${file#./}"
    
    # Use git check-ignore if available (most reliable method)
    if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
        # Use git check-ignore to check if file should be ignored
        if git check-ignore "$file" >/dev/null 2>&1; then
            return 0  # ignore
        fi
    else
        # Fallback to manual checking
        # Default ignores - check for exact patterns and path components
        # Dynamically match patterns from .gitignore
        if [ -f ".gitignore" ]; then
            while IFS= read -r line; do
                # Skip empty lines and comments
                if [ -n "$line" ] && [[ ! "$line" =~ ^[[:space:]]*# ]]; then
                    # Remove leading/trailing whitespace
                    line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
                    
                    # Use globbing to match patterns
                    if [[ "$file" == $line ]]; then
                        return 0  # ignore
                    fi
                fi
            done < ".gitignore"
        fi
        
        # Check against gitignore patterns if file exists
        if [ -f ".gitignore" ]; then
            while IFS= read -r line; do
                # Skip empty lines and comments
                if [ -n "$line" ] && [[ ! "$line" =~ ^[[:space:]]*# ]]; then
                    # Remove leading/trailing whitespace
                    line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
                    
                    # Check if file matches gitignore pattern
                    if [[ "$line" == */ ]]; then
                        # Directory pattern - remove trailing slash and check if file is in that directory
                        dir_pattern="${line%/}"
                        if [[ "$file" == "$dir_pattern"/* ]] || [[ "$file" == "$dir_pattern" ]]; then
                            return 0  # ignore
                        fi
                    elif [[ "$line" == *.* ]]; then
                        # File extension pattern
                        if [[ "$file" == *"$line" ]]; then
                            return 0  # ignore
                        fi
                    else
                        # General pattern - check for directory or file match
                        if [[ "$file" == "$line"/* ]] || [[ "$file" == "$line" ]]; then
                            return 0  # ignore
                        fi
                        # Also check if it's a file that matches the pattern
                        if [[ "$(basename "$file")" == "$line" ]]; then
                            return 0  # ignore
                        fi
                    fi
                fi
            done < ".gitignore"
        fi
    fi
    
    return 1  # don't ignore
}

# Function to generate sitemap data
generate_sitemap() {
    echo "🗺️ Generating sitemap data..."
    
    cat > "$SETTINGS_DIR/sitemap-data.yml" << EOF
---
generated_date: $(get_timestamp)
generator: update-settings-script
respects_gitignore: true
pages:
EOF

    # Find all markdown and HTML files, filtering by gitignore
    find . -name "*.md" -o -name "*.html" | \
        while read -r file; do
            # Check if file should be ignored
            if ! should_ignore_file "$file"; then
                # Extract title from front matter if available
                title=$(head -20 "$file" | grep -i "^title:" | head -1 | cut -d':' -f2- | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//' || echo "$(basename "$file" .md)")
                
                # Clean title of quotes
                title=$(echo "$title" | sed 's/^["'\'']//' | sed 's/["'\'']$//')
                
                echo "  - file: $file" >> "$SETTINGS_DIR/sitemap-data.yml"
                echo "    title: \"$title\"" >> "$SETTINGS_DIR/sitemap-data.yml"
            fi
        done | sort
    
    echo "✅ Sitemap data generated successfully (gitignore-filtered)"
}

# Function to update config.md
update_config_md() {
    echo "📝 Updating config.md..."
    
    cat > "$SETTINGS_DIR/config.md" << 'EOF'
---
title: Jekyll Configuration & Site Structure
excerpt: Configuration file contents, site tree structure, and automated regeneration workflows.
lastmod: TIMESTAMP_PLACEHOLDER
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
\`\`\`powershell
# Regenerate Config File
cd ~/github/{{ site.local_repo }}
cp {{ page.config-file }} {{ page.config-dir }}/config-utf16.txt
Get-Content {{ page.config-dir }}/config-utf16.txt | Set-Content -Encoding UTF8 {{ page.config-dir }}/{{ page.config-file }}

# Generate tree structure
tree /f > {{ page.config-dir }}/tree-utf16.txt
Get-Content {{ page.config-dir }}/tree-utf16.txt -Encoding Unicode | Set-Content -Encoding UTF8 {{ page.config-dir }}/tree.txt
\`\`\`

#### Bash (Linux/macOS)
\`\`\`bash
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
\`\`\`

### Gitignore Integration

The tree structure and sitemap generation **automatically respect the \`.gitignore\` file**, ensuring that:

- Files and directories listed in \`.gitignore\` are excluded from the tree structure
- Sitemap generation skips ignored files
- Documentation remains clean and relevant
- Sensitive or build artifacts are not included in public documentation

**Current .gitignore patterns respected:**
\`\`\`ignore
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
\`\`\`

## Jekyll Configuration

Current configuration from \`{{ page.config-file }}\`:

\`\`\`yml
{% include_relative {{ page.config-file }} %}
\`\`\`

## Site Tree Structure

Current directory structure (auto-generated):

\`\`\`
{% include_relative tree.txt %}
\`\`\`

## Site Map Data

Site structure and page information:

\`\`\`yml
{% include_relative sitemap-data.yml %}
\`\`\`

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
EOF

    # Replace the timestamp placeholder
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS sed requires backup extension
        sed -i '' "s/TIMESTAMP_PLACEHOLDER/$(get_timestamp)/" "$SETTINGS_DIR/config.md"
    else
        # Linux sed
        sed -i "s/TIMESTAMP_PLACEHOLDER/$(get_timestamp)/" "$SETTINGS_DIR/config.md"
    fi
    
    echo "✅ config.md updated successfully"
}

# Function to update tree.md
update_tree_md() {
    echo "🌳 Updating tree.md..."
    
    cat > "$SETTINGS_DIR/tree.md" << 'EOF'
---
title: Site Tree Structure
excerpt: Complete directory structure and file organization of the IT-Journey platform.
lastmod: TIMESTAMP_PLACEHOLDER2
permalink: /about/tree/
tags:
  - structure
  - organization
  - navigation
  - automation
---

## Site Structure Overview

This page displays the complete directory structure of the IT-Journey platform, automatically generated and updated via our CI/CD workflow.

### Current Tree Structure

\`\`\`
{% include_relative tree.txt %}
\`\`\`

### Structure Guidelines

Our directory organization follows these principles:

#### **Core Directories**
- \`pages/\` - Main content pages organized by section
- \`_data/\` - YAML data files for navigation and configuration
- \`assets/\` - Static resources (CSS, JavaScript, images)
- \`_site/\` - Generated site files (excluded from version control)

#### **Content Organization**
- \`_about/\` - About pages and documentation
- \`_docs/\` - Technical documentation and guides
- \`_posts/\` - Blog posts and articles
- \`_notebooks/\` - Jupyter notebooks and interactive content
- \`_quests/\` - Learning challenges and exercises

#### **Configuration Files**
- \`_config.yml\` - Main Jekyll configuration
- \`Gemfile\` - Ruby dependencies
- \`package.json\` - Node.js dependencies (if applicable)

### Automation Features

- **Auto-generated**: Updated automatically when repository structure changes
- **CI/CD Integration**: Part of the update-settings workflow
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Gitignore Aware**: Automatically excludes files and directories listed in \`.gitignore\`
- **Clean Output**: Only shows relevant project files and structure

### Gitignore Integration

This tree structure respects the project's \`.gitignore\` file, automatically excluding:

- Build artifacts and generated files
- IDE-specific directories (e.g., `.obsidian`, `.vscode`)
- Dependency directories (e.g., `node_modules`, `.venv`)
- Cache directories (e.g., `.sass-cache`, `.jekyll-cache`)
- Sensitive files (e.g., `.env`, API keys)

This ensures the documentation shows only the meaningful project structure without clutter from temporary or generated files.

**Common excluded patterns:**
- Build artifacts: _site/, .sass-cache/, .jekyll-cache/
- IDE configs: .obsidian/, .vscode/, .idea/
- Dependencies: node_modules/, .venv/, vendor/
- Temporary files: *.DS_Store, .env, .tmp

---

*Last updated: {{ page.lastmod }}*  
*Generated by: [update-settings.yml](/.github/workflows/update-settings.yml)*
EOF

    # Replace the timestamp placeholder
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS sed requires backup extension
        sed -i '' "s/TIMESTAMP_PLACEHOLDER2/$(get_timestamp)/" "$SETTINGS_DIR/tree.md"
    else
        # Linux sed
        sed -i "s/TIMESTAMP_PLACEHOLDER2/$(get_timestamp)/" "$SETTINGS_DIR/tree.md"
    fi
    
    echo "✅ tree.md updated successfully"
}

# Function to update sitemap.md
update_sitemap_md() {
    echo "🗺️ Updating sitemap.md..."
    
    cat > "$SETTINGS_DIR/sitemap.md" << 'EOF'
---
title: Site Navigation Map
excerpt: Complete sitemap and navigation structure for the IT-Journey platform.
lastmod: TIMESTAMP_PLACEHOLDER3
permalink: /about/sitemap/
tags:
  - navigation
  - sitemap
  - structure
  - automation
---

## Site Navigation Overview

This page provides a comprehensive map of all pages and content available on the IT-Journey platform, automatically generated and maintained through our automation workflows.

### Page Structure Data

\`\`\`yml
{% include_relative sitemap-data.yml %}
\`\`\`

### Navigation Sections

#### **Main Sections**
- **[Home](/)** - Platform introduction and getting started
- **[About](/about/)** - Mission, principles, and platform information
- **[Documentation](/docs/)** - Technical guides and tutorials
- **[Quickstart](/quickstart/)** - Fast-track learning paths
- **[Notebooks](/notebooks/)** - Interactive learning materials

#### **Learning Paths**
- **Frontend Development** - HTML, CSS, JavaScript, and modern frameworks
- **Backend Development** - Server-side technologies and databases
- **DevOps & Deployment** - CI/CD, containerization, and cloud platforms
- **AI Integration** - AI-powered development tools and practices

#### **Community & Contribution**
- **[Contributing](/contributing/)** - How to contribute to the platform
- **[Code of Conduct](/code-of-conduct/)** - Community guidelines
- **[GitHub Repository](https://github.com/bamr87/it-journey)** - Source code and issues

### Automation Features

This sitemap is maintained through:
- **Automated Discovery**: Scans repository for all markdown and HTML files
- **Gitignore Filtering**: Respects \`.gitignore\` patterns to exclude irrelevant files
- **Metadata Extraction**: Captures titles, descriptions, and lastmod dates
- **CI/CD Integration**: Updates automatically on content changes
- **Cross-reference Validation**: Ensures all links and references are valid
- **Clean Navigation**: Only includes user-facing content and documentation

### Content Filtering

The sitemap generation intelligently filters content based on:

1. **Gitignore Patterns**: Automatically excludes files listed in \`.gitignore\`
2. **Build Artifacts**: Skips generated files like `_site/` contents
3. **Development Files**: Excludes IDE configs, caches, and temporary files
4. **Sensitive Content**: Filters out environment files and API keys

This ensures the sitemap contains only relevant, public-facing content that users should navigate to.

**Filtering Examples:**
- Excluded: .venv/, _site/, .sass-cache/, .obsidian/
- Included: pages/, docs/, about/, posts/
- Logic: Respects .gitignore + additional intelligent filtering

### Manual Generation Commands

If you need to manually regenerate the sitemap:

\`\`\`bash
# Generate sitemap data
find . -name "*.md" -o -name "*.html" | grep -v "_site\\|\\.git\\|node_modules" | sort > sitemap-files.txt

# Create tree structure
tree -a -I '.git|.github|_site|node_modules|vendor|.bundle|.sass-cache|*.gem' \\
  --dirsfirst --charset ascii > tree.txt
\`\`\`

---

*Last updated: {{ page.lastmod }}*  
*Generated by: [update-settings.yml](/.github/workflows/update-settings.yml)*
EOF

    # Replace the timestamp placeholder
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS sed requires backup extension
        sed -i '' "s/TIMESTAMP_PLACEHOLDER3/$(get_timestamp)/" "$SETTINGS_DIR/sitemap.md"
    else
        # Linux sed
        sed -i "s/TIMESTAMP_PLACEHOLDER3/$(get_timestamp)/" "$SETTINGS_DIR/sitemap.md"
    fi

    echo "✅ sitemap.md updated successfully"
}

# Main execution
main() {
    echo "🎯 IT-Journey Settings Update Script"
    echo "======================================"
    
    # Change to repository root
    cd "$REPO_ROOT"
    
    # Execute all update functions
    copy_config
    generate_tree
    generate_sitemap
    update_config_md
    update_tree_md
    update_sitemap_md
    
    echo ""
    echo "🎉 Settings update completed successfully!"
    echo "📁 Updated files in: $SETTINGS_DIR"
    echo "⏰ Timestamp: $(get_timestamp)"
}

# Run the script
main "$@"
