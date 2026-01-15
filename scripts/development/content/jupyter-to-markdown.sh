#!/bin/bash
#
# @file scripts/development/content/jupyter-to-markdown.sh
# @description Convert Jupyter notebooks to Jekyll markdown posts
# @author IT-Journey Team
# @created 2025-01-01
# @version 1.0.0
#
# Usage: ./scripts/development/content/jupyter-to-markdown.sh [OPTIONS]
#
# Options:
#   -h, --help          Show this help message
#   -d, --dir DIR       Posts directory (default: pages/_notebooks)
#   -o, --output DIR    Output directory (default: pages/_notebooks)
#   -v, --verbose       Enable verbose output
#
# Dependencies:
#   - jupyter nbconvert
#   - bash 4.0+

set -euo pipefail

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Default paths
POSTS_DIR="${PROJECT_ROOT}/pages/_notebooks"
VERBOSE=false

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

log_verbose() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${YELLOW}[VERBOSE]${NC} $*"
    fi
}

# Show help
show_help() {
    cat << EOF
Convert Jupyter notebooks to Jekyll markdown posts.

Usage: $0 [OPTIONS]

Options:
  -h, --help          Show this help message
  -d, --dir DIR       Posts directory (default: pages/_notebooks)
  -o, --output DIR    Output directory (default: pages/_notebooks)
  -v, --verbose       Enable verbose output

Examples:
  $0                          # Convert all notebooks in current directory
  $0 -d pages/_notebooks      # Specify custom posts directory
  $0 -v                       # Verbose output

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -d|--dir)
            POSTS_DIR="$2"
            shift 2
            ;;
        -o|--output)
            POSTS_DIR="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Validate dependencies
if ! command -v jupyter &> /dev/null; then
    log_error "jupyter command not found. Please install Jupyter."
    exit 1
fi

# Create posts directory if it doesn't exist
if [[ ! -d "$POSTS_DIR" ]]; then
    log_info "Creating posts directory: $POSTS_DIR"
    mkdir -p "$POSTS_DIR"
fi

# Get the current date in the format required by Jekyll
DATE=$(date +"%Y-%m-%d")

# Find all .ipynb files in the current directory and its subdirectories
log_info "Searching for Jupyter notebooks..."
notebooks=()
while IFS= read -r -d '' notebook; do
    notebooks+=("$notebook")
done < <(find . -name "*.ipynb" -type f -print0)

if [[ ${#notebooks[@]} -eq 0 ]]; then
    log_info "No Jupyter notebooks found in current directory."
    exit 0
fi

log_info "Found ${#notebooks[@]} notebook(s) to convert"

# Process each notebook
for notebook in "${notebooks[@]}"; do
    log_verbose "Processing: $notebook"
    
    # Convert the Jupyter notebook to a markdown file
    if ! jupyter nbconvert --to markdown "$notebook" --stdout > /dev/null 2>&1; then
        log_error "Failed to convert: $notebook"
        continue
    fi
    
    jupyter nbconvert --to markdown "$notebook" --output-dir="$(dirname "$notebook")"
    
    # Get the name of the markdown file
    md_file="${notebook%.ipynb}.md"
    md_file="$(dirname "$notebook")/${md_file##*/}"
    
    if [[ ! -f "$md_file" ]]; then
        log_error "Markdown file not created: $md_file"
        continue
    fi
    
    # Rename the markdown file to match Jekyll's naming convention
    jekyll_md_file="${DATE}-${md_file##*/}"
    jekyll_md_file="${POSTS_DIR}/${jekyll_md_file}"
    
    # Create a temporary file
    temp_file=$(mktemp)
    
    # Append the contents of the markdown file to the temporary file
    cat "$md_file" >> "$temp_file"
    
    # Replace the markdown file with the temporary file
    mv "$temp_file" "$jekyll_md_file"
    
    # Clean up original markdown file
    rm -f "$md_file"
    
    log_success "Converted: $notebook -> $jekyll_md_file"
done

log_success "Conversion complete!"