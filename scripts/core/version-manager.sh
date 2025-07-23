#!/bin/bash
#
# @file scripts/core/version-manager.sh
# @description Unified version management script for IT-Journey projects
# @author IT-Journey Team <team@it-journey.org>
# @created 2025-07-07
# @lastModified 2025-07-07
# @version 1.0.0
#
# @relatedIssues 
#   - Script consolidation: Merge multiple version management approaches
#
# @relatedEvolutions
#   - v1.0.0: Initial unified version manager combining package.json and frontmatter versioning
#
# @dependencies
#   - git: Version control operations
#   - jq: JSON processing for package.json
#   - sed: Text processing for frontmatter
#
# @changelog
#   - 2025-07-07: Initial creation combining zer0-mistakes and it-journey version scripts - ITJ
#
# @usage ./scripts/core/version-manager.sh [TYPE] [OPTIONS]
# @notes Supports both package.json semantic versioning and markdown frontmatter versioning
#

set -euo pipefail

# IT-Journey Development Principles Implementation:
# DFF: Comprehensive error handling and validation
# DRY: Single source of truth for version management
# KIS: Clear, focused functionality with simple interface
# COLAB: Standardized logging and documentation

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Default values
VERSION_TYPE="${1:-patch}"
DRY_RUN=false
FRONTMATTER_ONLY=false
PACKAGE_ONLY=false
AUTO_COMMIT=false

# Show help message
show_help() {
    cat << EOF
🔢 IT-Journey Unified Version Manager

USAGE:
    $0 [TYPE] [OPTIONS]

VERSION TYPES:
    patch                    Increment patch version (0.1.0 → 0.1.1)
    minor                    Increment minor version (0.1.0 → 0.2.0)
    major                    Increment major version (0.1.0 → 1.0.0)
    frontmatter              Update only markdown frontmatter versions

OPTIONS:
    --dry-run               Preview changes without applying them
    --frontmatter-only      Only update markdown frontmatter versions
    --package-only          Only update package.json version
    --auto-commit           Automatically commit and tag changes
    --help                  Show this help message

EXAMPLES:
    $0 patch                # Increment patch version in all applicable files
    $0 minor --dry-run      # Preview minor version increment
    $0 frontmatter          # Update only staged markdown files
    $0 major --auto-commit  # Increment major version and auto-commit

SUPPORTED FILES:
    - package.json          Semantic versioning for Node.js projects
    - *.gemspec            Ruby gem versioning
    - *.md frontmatter     Markdown file version tracking
    - CHANGELOG.md         Automatic changelog updates

Following IT-Journey Principles:
    DFF: Comprehensive error handling and rollback capabilities
    DRY: Single script for all version management needs
    KIS: Simple interface with clear feedback
    COLAB: Consistent versioning across all project files
EOF
}

# Logging functions
log() {
    echo -e "${GREEN}[VERSION]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --frontmatter-only)
                FRONTMATTER_ONLY=true
                shift
                ;;
            --package-only)
                PACKAGE_ONLY=true
                shift
                ;;
            --auto-commit)
                AUTO_COMMIT=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            patch|minor|major|frontmatter)
                VERSION_TYPE="$1"
                shift
                ;;
            *)
                error "Unknown option: $1. Use --help for usage information."
                ;;
        esac
    done
}

# Validate environment
validate_environment() {
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        error "Not in a git repository"
    fi

    # Check required tools
    if [[ "$FRONTMATTER_ONLY" == false ]] && [[ "$VERSION_TYPE" != "frontmatter" ]]; then
        if ! command -v jq &> /dev/null && [[ -f "package.json" ]]; then
            error "jq is required for package.json version management. Install with: brew install jq"
        fi
    fi

    # For frontmatter updates, check if working directory is clean when auto-committing
    if [[ "$AUTO_COMMIT" == true ]] && [[ -n $(git status --porcelain) ]] && [[ "$VERSION_TYPE" != "frontmatter" ]]; then
        error "Working directory is not clean. Please commit or stash changes first when using --auto-commit."
    fi
}

# Update package.json version
update_package_version() {
    local new_version="$1"
    
    if [[ ! -f "package.json" ]]; then
        info "No package.json found, skipping package version update"
        return 0
    fi

    log "Updating package.json to version $new_version..."
    
    if [[ "$DRY_RUN" == true ]]; then
        info "Would update package.json version to $new_version"
        return 0
    fi

    # Create backup
    cp package.json package.json.backup

    # Update version
    if ! jq ".version = \"$new_version\"" package.json > package.json.tmp; then
        mv package.json.backup package.json
        error "Failed to update package.json"
    fi

    mv package.json.tmp package.json
    rm package.json.backup
}

# Update gemspec version (if exists)
update_gemspec_version() {
    local new_version="$1"
    local gemspec_file
    
    gemspec_file=$(find . -maxdepth 1 -name "*.gemspec" | head -n 1)
    
    if [[ -z "$gemspec_file" ]]; then
        info "No gemspec file found, skipping gem version update"
        return 0
    fi

    log "Updating $gemspec_file to version $new_version..."
    
    if [[ "$DRY_RUN" == true ]]; then
        info "Would update $gemspec_file version to $new_version"
        return 0
    fi

    # Validate gemspec can be built after update
    if ! gem build "$gemspec_file" > /dev/null 2>&1; then
        warn "Gemspec validation failed, but continuing..."
    fi

    # Clean up test gem file
    rm -f ./*.gem
}

# Update markdown frontmatter versions
update_frontmatter_versions() {
    local files_to_process=()
    
    if [[ "$VERSION_TYPE" == "frontmatter" ]]; then
        # Process only staged files for frontmatter-only updates
        mapfile -t files_to_process < <(git diff --cached --name-only | grep '\.md$' || true)
        
        if [[ ${#files_to_process[@]} -eq 0 ]]; then
            warn "No staged markdown files found for frontmatter version update"
            return 0
        fi
    else
        # Process all markdown files with version frontmatter
        mapfile -t files_to_process < <(find . -name "*.md" -not -path "./_site/*" -not -path "./node_modules/*" | head -20)
    fi

    local updated_count=0
    
    for file in "${files_to_process[@]}"; do
        if [[ ! -f "$file" ]]; then
            continue
        fi

        # Extract frontmatter
        local front_matter
        front_matter=$(sed -n '/^---$/,/^---$/p' "$file" 2>/dev/null || echo "")
        
        if [[ -z "$front_matter" ]]; then
            continue
        fi

        # Get current version from frontmatter
        local current_version
        current_version=$(echo "$front_matter" | grep -E '^version:' | sed 's/version: *//' | tr -d '"' | head -n 1 || echo "")

        if [[ -z "$current_version" ]]; then
            continue
        fi

        # Calculate new version
        local new_version
        if [[ "$VERSION_TYPE" == "frontmatter" ]]; then
            # For frontmatter-only updates, increment the last component
            IFS='.' read -ra version_parts <<< "$current_version"
            version_parts[-1]=$((version_parts[-1] + 1))
            new_version=$(IFS=. ; echo "${version_parts[*]}")
        else
            # Use the package version
            new_version="$1"
        fi

        log "Updating $file: $current_version → $new_version"
        
        if [[ "$DRY_RUN" == true ]]; then
            info "Would update $file version to $new_version"
            ((updated_count++))
            continue
        fi

        # Update the version in frontmatter
        if sed -i.backup -E "s/^version: .*$/version: $new_version/" "$file"; then
            rm -f "$file.backup"
            ((updated_count++))
            
            # Add to git if it was originally staged or if auto-committing
            if [[ "$VERSION_TYPE" == "frontmatter" ]] || [[ "$AUTO_COMMIT" == true ]]; then
                git add "$file"
            fi
        else
            error "Failed to update version in $file"
        fi
    done

    if [[ $updated_count -gt 0 ]]; then
        log "Updated $updated_count markdown files"
    else
        info "No markdown files required version updates"
    fi
}

# Update CHANGELOG.md
update_changelog() {
    local new_version="$1"
    
    if [[ ! -f "CHANGELOG.md" ]]; then
        info "No CHANGELOG.md found, skipping changelog update"
        return 0
    fi

    log "Updating CHANGELOG.md for version $new_version..."
    
    if [[ "$DRY_RUN" == true ]]; then
        info "Would update CHANGELOG.md with version $new_version"
        return 0
    fi

    local date_stamp
    date_stamp=$(date +"%Y-%m-%d")
    
    # Create backup
    cp CHANGELOG.md CHANGELOG.md.backup
    
    # Add new version entry at the top
    {
        echo "## [$new_version] - $date_stamp"
        echo ""
        echo "### Changed"
        echo "- Version bump to $new_version"
        echo ""
        cat CHANGELOG.md
    } > CHANGELOG.md.tmp
    
    mv CHANGELOG.md.tmp CHANGELOG.md
    rm CHANGELOG.md.backup
}

# Calculate new semantic version
calculate_new_version() {
    local current_version="$1"
    local version_type="$2"
    
    # Parse current version
    IFS='.' read -ra VERSION_PARTS <<< "$current_version"
    local major=${VERSION_PARTS[0]:-0}
    local minor=${VERSION_PARTS[1]:-0}
    local patch=${VERSION_PARTS[2]:-0}

    # Calculate new version based on type
    case $version_type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            error "Invalid version type: $version_type"
            ;;
    esac

    echo "$major.$minor.$patch"
}

# Commit and tag changes
commit_and_tag() {
    local new_version="$1"
    
    if [[ "$DRY_RUN" == true ]]; then
        info "Would commit changes and create tag v$new_version"
        return 0
    fi

    if [[ "$AUTO_COMMIT" == false ]]; then
        info "Skipping auto-commit. Use --auto-commit to automatically commit and tag."
        return 0
    fi

    log "Committing version changes..."
    
    # Add package.json and CHANGELOG.md if they exist and were modified
    [[ -f "package.json" ]] && git add package.json
    [[ -f "CHANGELOG.md" ]] && git add CHANGELOG.md
    
    # Commit with conventional commit message
    git commit -m "chore: bump version to $new_version" || {
        warn "No changes to commit"
        return 0
    }

    log "Creating git tag v$new_version..."
    git tag -a "v$new_version" -m "Release version $new_version"

    log "Version bump complete!"
    log "Next steps:"
    log "1. Run 'git push origin main --tags' to push changes and tags"
    log "2. Create a release on GitHub if desired"
}

# Main execution
main() {
    parse_arguments "$@"
    validate_environment

    log "🔢 IT-Journey Version Manager"
    log "Version type: $VERSION_TYPE"
    [[ "$DRY_RUN" == true ]] && log "Mode: DRY RUN"

    # Handle frontmatter-only updates
    if [[ "$VERSION_TYPE" == "frontmatter" ]] || [[ "$FRONTMATTER_ONLY" == true ]]; then
        update_frontmatter_versions
        [[ "$AUTO_COMMIT" == true ]] && git commit -m "chore: update markdown frontmatter versions" || true
        log "Frontmatter version update complete!"
        return 0
    fi

    # Get current version from package.json
    local current_version
    if [[ -f "package.json" ]]; then
        current_version=$(jq -r '.version' package.json 2>/dev/null || echo "0.0.0")
        if [[ "$current_version" == "null" ]]; then
            current_version="0.0.0"
        fi
    else
        current_version="0.0.0"
    fi

    # Calculate new version
    local new_version
    new_version=$(calculate_new_version "$current_version" "$VERSION_TYPE")

    log "Current version: $current_version"
    log "New version: $new_version"

    # Update versions based on flags
    if [[ "$FRONTMATTER_ONLY" == false ]]; then
        update_package_version "$new_version"
        update_gemspec_version "$new_version"
        update_changelog "$new_version"
    fi

    if [[ "$PACKAGE_ONLY" == false ]]; then
        update_frontmatter_versions "$new_version"
    fi

    # Commit and tag if requested
    commit_and_tag "$new_version"

    log "✅ Version management complete!"
}

# Execute main function with all arguments
main "$@"
