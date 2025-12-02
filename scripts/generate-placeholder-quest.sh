#!/usr/bin/env bash
# generate-placeholder-quest.sh
# Generate a placeholder quest file with proper structure and frontmatter
# Usage: ./scripts/generate-placeholder-quest.sh <level> <quest-slug> "<quest-title>"

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
QUEST_DIR="${PROJECT_ROOT}/pages/_quests"
TEMPLATE_DIR="${QUEST_DIR}/templates"
TEMPLATE_FILE="${TEMPLATE_DIR}/main-quest-template.md"

# Function to print colored output
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Function to display usage
usage() {
    cat <<EOF
Usage: $0 <level> <quest-slug> "<quest-title>" [options]

Generate a placeholder quest file with proper structure and frontmatter.

Arguments:
    level           Binary level (e.g., 0000, 0001, 0010, 0110, 1111)
    quest-slug      URL-friendly quest identifier (e.g., docker-fundamentals)
    quest-title     Human-readable quest title (use quotes if contains spaces)

Options:
    --difficulty    Quest difficulty: easy, medium, hard, epic (default: easy)
    --type          Quest type: main_quest, side_quest, bonus_quest (default: main_quest)
    --time          Estimated time (e.g., "30-45 minutes", default: "30-45 minutes")
    --tech          Primary technology (e.g., docker, react, python)
    --skill         Skill focus (e.g., frontend, backend, devops)
    --dry-run       Show what would be created without creating files
    -h, --help      Show this help message

Examples:
    $0 0110 database-design-fundamentals "Database Design Fundamentals"
    $0 0110 sql-sorcery "SQL Sorcery" --difficulty medium --time "45-60 minutes"
    $0 1101 ml-fundamentals "ML Fundamentals" --tech python --skill data-science --difficulty hard

EOF
    exit 1
}

# Function to convert binary level to decimal
binary_to_decimal() {
    local binary=$1
    echo $((2#$binary))
}

# Function to get difficulty emoji
get_difficulty_emoji() {
    case "$1" in
        easy)   echo "🟢 Easy" ;;
        medium) echo "🟡 Medium" ;;
        hard)   echo "🔴 Hard" ;;
        epic)   echo "⚔️ Epic" ;;
        *)      echo "🟢 Easy" ;;
    esac
}

# Parse arguments
if [[ $# -lt 3 ]]; then
    print_error "Missing required arguments"
    usage
fi

LEVEL="$1"
QUEST_SLUG="$2"
QUEST_TITLE="$3"
shift 3

# Default options
DIFFICULTY="easy"
QUEST_TYPE="main_quest"
ESTIMATED_TIME="30-45 minutes"
PRIMARY_TECH=""
SKILL_FOCUS=""
DRY_RUN=false

# Parse optional arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --difficulty)
            DIFFICULTY="$2"
            shift 2
            ;;
        --type)
            QUEST_TYPE="$2"
            shift 2
            ;;
        --time)
            ESTIMATED_TIME="$2"
            shift 2
            ;;
        --tech)
            PRIMARY_TECH="$2"
            shift 2
            ;;
        --skill)
            SKILL_FOCUS="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
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

# Validate level format (should be 4 binary digits)
if ! [[ "$LEVEL" =~ ^[01]{4}$ ]]; then
    print_error "Level must be 4 binary digits (e.g., 0000, 0001, 1111)"
    exit 1
fi

# Calculate decimal level
DECIMAL_LEVEL=$(binary_to_decimal "$LEVEL")
DIFFICULTY_EMOJI=$(get_difficulty_emoji "$DIFFICULTY")

# Generate file paths
LEVEL_DIR="${QUEST_DIR}/${LEVEL}"
QUEST_FILE="${LEVEL_DIR}/${QUEST_SLUG}.md"
LEVEL_README="${LEVEL_DIR}/README.md"

# Current timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")

print_info "=== Quest Generation Configuration ==="
print_info "Level: ${LEVEL} (Decimal: ${DECIMAL_LEVEL})"
print_info "Quest Slug: ${QUEST_SLUG}"
print_info "Quest Title: ${QUEST_TITLE}"
print_info "Difficulty: ${DIFFICULTY_EMOJI}"
print_info "Quest Type: ${QUEST_TYPE}"
print_info "Estimated Time: ${ESTIMATED_TIME}"
[[ -n "$PRIMARY_TECH" ]] && print_info "Primary Tech: ${PRIMARY_TECH}"
[[ -n "$SKILL_FOCUS" ]] && print_info "Skill Focus: ${SKILL_FOCUS}"
print_info "Output File: ${QUEST_FILE}"
echo ""

# Check if template exists
if [[ ! -f "$TEMPLATE_FILE" ]]; then
    print_error "Template file not found: ${TEMPLATE_FILE}"
    exit 1
fi

# Check if quest file already exists
if [[ -f "$QUEST_FILE" ]]; then
    print_warning "Quest file already exists: ${QUEST_FILE}"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Operation cancelled"
        exit 0
    fi
fi

# Dry run - show what would be created
if [[ "$DRY_RUN" = true ]]; then
    print_info "=== DRY RUN - No files will be created ==="
    print_info "Would create directory: ${LEVEL_DIR}"
    print_info "Would create file: ${QUEST_FILE}"
    print_info "Would update: ${LEVEL_README}"
    exit 0
fi

# Create level directory if it doesn't exist
if [[ ! -d "$LEVEL_DIR" ]]; then
    print_info "Creating level directory: ${LEVEL_DIR}"
    mkdir -p "$LEVEL_DIR"
fi

# Generate quest file from template
print_info "Generating quest file from template..."

# Read template and replace placeholders
quest_content=$(cat "$TEMPLATE_FILE")

# Replace placeholders
quest_content="${quest_content//\[Quest Title\]/$QUEST_TITLE}"
quest_content="${quest_content//\[quest-slug\]/$QUEST_SLUG}"
quest_content="${quest_content//XXXX/$LEVEL}"
quest_content="${quest_content//XX/$DECIMAL_LEVEL}"
quest_content="${quest_content//🟢 Easy/$DIFFICULTY_EMOJI}"
quest_content="${quest_content//30-45 minutes/$ESTIMATED_TIME}"
quest_content="${quest_content//main_quest/$QUEST_TYPE}"
quest_content="${quest_content//2025-11-29T00:00:00.000Z/$TIMESTAMP}"

# Replace technology and skill if provided
if [[ -n "$PRIMARY_TECH" ]]; then
    quest_content="${quest_content//\[main-tech\]/$PRIMARY_TECH}"
    quest_content="${quest_content//\[primary-technology\]/$PRIMARY_TECH}"
fi

if [[ -n "$SKILL_FOCUS" ]]; then
    quest_content="${quest_content//\[skill-category\]/$SKILL_FOCUS}"
    quest_content="${quest_content//\[skill-focus\]/$SKILL_FOCUS}"
fi

# Write quest file
echo "$quest_content" > "$QUEST_FILE"
print_success "Created quest file: ${QUEST_FILE}"

# Update level README if it exists
if [[ -f "$LEVEL_README" ]]; then
    print_info "Updating level README: ${LEVEL_README}"
    
    # Add quest to the appropriate section in README
    # This is a placeholder - in practice, you'd want more sophisticated parsing
    print_warning "Manual README update recommended"
    print_info "Add this line to ${LEVEL_README}:"
    echo ""
    echo "| [${QUEST_TITLE}](${QUEST_SLUG}.md) | ${DIFFICULTY_EMOJI} | ${ESTIMATED_TIME} | [XP] | 🔮 | [tech] |"
    echo ""
else
    print_warning "Level README not found: ${LEVEL_README}"
    print_info "Consider creating one using the level-readme-template.md"
fi

# Summary
print_success "=== Quest Generation Complete ==="
print_info "Next steps:"
print_info "1. Edit ${QUEST_FILE} to fill in content"
print_info "2. Update level README: ${LEVEL_README}"
print_info "3. Update main quest index: ${QUEST_DIR}/README.md"
print_info "4. Update overworld map: ${QUEST_DIR}/home.md"
print_info "5. Set draft: false when quest is ready"
print_info "6. Run validation: ./scripts/validate-quest-network.py"

# Git integration (optional)
read -p "Create git commit? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd "$PROJECT_ROOT"
    git add "$QUEST_FILE"
    [[ -f "$LEVEL_README" ]] && git add "$LEVEL_README"
    git commit -m "feat(quest): add placeholder for ${QUEST_TITLE} (Level ${LEVEL})"
    print_success "Git commit created"
fi

print_success "All done! Happy quest building! 🎮"
