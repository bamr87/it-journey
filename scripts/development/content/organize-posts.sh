#!/bin/bash

# Bash wrapper script for the Post Organizer Python utility
# 
# This script helps organize Jekyll markdown posts based on frontmatter metadata.
# It provides an easy-to-use interface for the Python organizer script.

set -euo pipefail

# Script directory and paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/organize-posts.py"
REQUIREMENTS_FILE="${SCRIPT_DIR}/requirements.txt"

# Default paths (relative to IT-Journey root)
IT_JOURNEY_ROOT="$(cd "${SCRIPT_DIR}/../../../" && pwd)"
DEFAULT_POSTS_DIR="${IT_JOURNEY_ROOT}/pages/_posts"
DEFAULT_CONFIG_FILE="${IT_JOURNEY_ROOT}/_data/posts_organization.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Function to check if Python is available
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        error "Python is not installed or not in PATH"
        exit 1
    fi
    
    log "Using Python: $($PYTHON_CMD --version)"
}

# Function to install requirements
install_requirements() {
    log "Installing Python requirements..."
    
    if ! $PYTHON_CMD -m pip install -r "$REQUIREMENTS_FILE"; then
        error "Failed to install requirements"
        exit 1
    fi
    
    success "Requirements installed successfully"
}

# Function to check if requirements are installed
check_requirements() {
    local auto_confirm="${1:-false}"
    
    log "Checking if PyYAML is installed..."
    
    if ! $PYTHON_CMD -c "import yaml" 2>/dev/null; then
        warn "PyYAML is not installed"
        if [[ "$auto_confirm" == true ]]; then
            log "Auto-confirm enabled - installing requirements automatically"
            install_requirements
        else
            read -p "Install requirements now? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                install_requirements
            else
                error "PyYAML is required to run this script"
                echo "Install it with: pip install pyyaml"
                exit 1
            fi
        fi
    else
        success "PyYAML is installed"
    fi
}

# Function to display usage
usage() {
    cat << EOF
Post Organizer - Organize Jekyll posts based on frontmatter metadata

USAGE:
    $0 [OPTIONS]

OPTIONS:
    -d, --posts-dir PATH     Path to posts directory (default: $DEFAULT_POSTS_DIR)
    -c, --config-file PATH   Path to posts.yml config file (default: $DEFAULT_CONFIG_FILE)
    -n, --dry-run           Show what would be done without moving files
    -i, --install-deps      Install Python dependencies
    -y, --auto-confirm      Skip confirmation prompts (for automation)
    -h, --help              Show this help message

EXAMPLES:
    # Dry run to see what would happen
    $0 --dry-run
    
    # Organize posts with custom directory
    $0 --posts-dir /path/to/posts
    
    # Use custom config file
    $0 --config-file /path/to/posts.yml
    
    # Install dependencies only
    $0 --install-deps

REQUIREMENTS:
    - Python 3.6+
    - PyYAML library (will be installed automatically if needed)

The script will:
1. Scan all .md files in the posts directory
2. Extract 'section' and slug information from frontmatter
3. Create subdirectories based on section values
4. Move files to appropriate subdirectories with slug-based names
5. Log all operations and skipped files

Files are skipped if they:
- Don't have valid frontmatter
- Don't have a 'section' field with a valid value
- Don't have determinable slug information

EOF
}

# Main function
main() {
    local posts_dir="$DEFAULT_POSTS_DIR"
    local config_file="$DEFAULT_CONFIG_FILE"
    local dry_run=false
    local install_only=false
    local auto_confirm=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--posts-dir)
                posts_dir="$2"
                shift 2
                ;;
            -c|--config-file)
                config_file="$2"
                shift 2
                ;;
            -n|--dry-run)
                dry_run=true
                shift
                ;;
            -i|--install-deps)
                install_only=true
                shift
                ;;
            -y|--auto-confirm)
                auto_confirm=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    # Check Python availability
    check_python
    
    # Check and install requirements
    check_requirements "$auto_confirm"
    
    # If install-only mode, exit after installing dependencies
    if [[ "$install_only" == true ]]; then
        success "Dependencies check complete"
        exit 0
    fi
    
    # Validate paths
    if [[ ! -d "$posts_dir" ]]; then
        error "Posts directory does not exist: $posts_dir"
        exit 1
    fi
    
    if [[ ! -f "$config_file" ]]; then
        warn "Config file not found: $config_file (will use defaults)"
        config_file=""
    fi
    
    # Build Python command arguments
    local python_args=(
        "$PYTHON_SCRIPT"
        "--posts-dir" "$posts_dir"
    )
    
    if [[ -n "$config_file" ]]; then
        python_args+=("--config-file" "$config_file")
    fi
    
    if [[ "$dry_run" == true ]]; then
        python_args+=("--dry-run")
        warn "Running in DRY RUN mode - no files will be moved"
    fi
    
    # Display configuration
    log "Configuration:"
    log "  Posts Directory: $posts_dir"
    log "  Config File: ${config_file:-"(using defaults)"}"
    log "  Dry Run: $dry_run"
    log "  Python Script: $PYTHON_SCRIPT"
    
    # Ask for confirmation unless it's a dry run or auto-confirm is enabled
    if [[ "$dry_run" != true && "$auto_confirm" != true ]]; then
        echo
        warn "This will move files in your posts directory!"
        read -p "Continue? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log "Operation cancelled"
            exit 0
        fi
    elif [[ "$auto_confirm" == true && "$dry_run" != true ]]; then
        log "Auto-confirm enabled - proceeding without user confirmation"
    fi
    
    # Run the Python script
    log "Starting post organization..."
    
    if $PYTHON_CMD "${python_args[@]}"; then
        success "Post organization completed successfully"
    else
        error "Post organization failed"
        exit 1
    fi
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
