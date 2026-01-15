#!/usr/bin/env bash
# cleanup-placeholder-deps.sh
# Removes template placeholder dependencies from quest frontmatter

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
QUEST_DIR="${PROJECT_ROOT}/pages/_quests"

# Placeholder patterns to remove
PLACEHOLDER_PATTERNS=(
    "level-XXXX-side-quest-1"
    "level-XXXX-side-quest-2"
    "level-XXXX-alternative-path"
    "level-XXXX-continuation"
    "/quests/level-XXXX-"
    "level-0000-side-quest-1"
    "level-0000-side-quest-2"
    "level-0001-side-quest-1"
    "level-0001-side-quest-2"
    "level-0010-side-quest-1"
    "level-0010-side-quest-2"
    "level-0011-side-quest-1"
    "level-0011-side-quest-2"
)

# Function to display usage
usage() {
    cat <<EOF
Usage: $0 [options]

Remove template placeholder dependencies from quest frontmatter.

Options:
    --dry-run       Show what would be removed without making changes
    --backup        Create backup files before modifying
    -h, --help      Show this help message

Examples:
    $0 --dry-run              # Preview changes
    $0 --backup               # Remove placeholders with backup
    $0                        # Remove placeholders

EOF
    exit 1
}

DRY_RUN=false
BACKUP=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --backup)
            BACKUP=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            ;;
    esac
done

if [[ ! -d "$QUEST_DIR" ]]; then
    print_error "Quest directory not found: $QUEST_DIR"
    exit 1
fi

print_info "Quest directory: $QUEST_DIR"
print_info "Placeholder patterns to remove: ${#PLACEHOLDER_PATTERNS[@]}"
echo ""

if [[ "$DRY_RUN" = true ]]; then
    print_info "=== DRY RUN - No files will be modified ==="
fi

# Find all quest markdown files
FILES_MODIFIED=0
FILES_SCANNED=0

while IFS= read -r -d '' file; do
    FILES_SCANNED=$((FILES_SCANNED + 1))
    MODIFIED=false
    FILE_CONTENT=$(cat "$file")
    ORIGINAL_CONTENT="$FILE_CONTENT"
    
    # Check for placeholder patterns
    for pattern in "${PLACEHOLDER_PATTERNS[@]}"; do
        if echo "$FILE_CONTENT" | grep -q "$pattern"; then
            MODIFIED=true
            
            if [[ "$DRY_RUN" = true ]]; then
                print_warning "Would remove pattern '$pattern' from: $file"
            else
                # Remove lines containing placeholder patterns
                # This is a simple approach - for more complex YAML manipulation, use Python
                FILE_CONTENT=$(echo "$FILE_CONTENT" | grep -v "$pattern" || true)
            fi
        fi
    done
    
    if [[ "$MODIFIED" = true ]]; then
        if [[ "$DRY_RUN" = false ]]; then
            # Create backup if requested
            if [[ "$BACKUP" = true ]]; then
                cp "$file" "${file}.backup"
            fi
            
            # Write modified content
            echo "$FILE_CONTENT" > "$file"
            FILES_MODIFIED=$((FILES_MODIFIED + 1))
            print_success "Removed placeholders from: $file"
        fi
    fi
    
done < <(find "$QUEST_DIR" -name "*.md" -type f -not -path "*/templates/*" -not -path "*/docs/*" -not -path "*/codex/*" -print0)

echo ""
print_info "=== Summary ==="
print_info "Files scanned: $FILES_SCANNED"

if [[ "$DRY_RUN" = true ]]; then
    print_info "Files that would be modified: $FILES_MODIFIED"
    print_info "Run without --dry-run to apply changes"
else
    print_success "Files modified: $FILES_MODIFIED"
    if [[ "$BACKUP" = true ]]; then
        print_info "Backup files created with .backup extension"
    fi
fi

print_success "Cleanup complete!"
