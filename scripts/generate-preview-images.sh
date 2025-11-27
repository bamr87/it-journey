#!/bin/bash
#
# Script Name: generate-preview-images.sh
# Description: AI-powered preview image generator for Jekyll posts/articles/quests
#              Scans content files, detects missing preview images, and generates
#              images using AI (OpenAI DALL-E, Stable Diffusion, or other providers)
#
# Usage: ./scripts/generate-preview-images.sh [options]
#
# Options:
#   -h, --help              Show this help message
#   -d, --dry-run           Preview what would be generated (no actual changes)
#   -v, --verbose           Enable verbose output
#   -f, --file FILE         Process a specific file only
#   -c, --collection NAME   Process specific collection (posts, quickstart, docs)
#   -p, --provider PROVIDER AI provider (openai, stability, local)
#   --output-dir DIR        Output directory for images (default: assets/images/previews)
#   --force                 Regenerate images even if preview exists
#   --list-missing          Only list files with missing previews
#
# Dependencies:
#   - bash 4.0+
#   - curl (for API calls)
#   - jq (for JSON processing)
#   - yq or python (for YAML parsing)
#
# Environment Variables:
#   OPENAI_API_KEY          OpenAI API key for DALL-E image generation
#   STABILITY_API_KEY       Stability AI API key for Stable Diffusion
#   IMAGE_STYLE             Default image style (default: "digital art, professional")
#   IMAGE_SIZE              Image dimensions (default: "1024x1024")
#
# Examples:
#   ./scripts/generate-preview-images.sh --dry-run
#   ./scripts/generate-preview-images.sh --collection posts
#   ./scripts/generate-preview-images.sh --file pages/_posts/my-post.md
#   ./scripts/generate-preview-images.sh --provider openai --verbose
#

set -euo pipefail

# Get script directory and source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load environment variables from .env file if it exists
if [[ -f "$PROJECT_ROOT/.env" ]]; then
    # Export variables from .env file, overriding any existing values
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ -z "$key" || "$key" =~ ^# ]] && continue
        # Remove surrounding quotes from value if present
        value="${value%\"}"
        value="${value#\"}"
        value="${value%\'}"
        value="${value#\'}"
        # Export the variable
        export "$key=$value"
    done < "$PROJECT_ROOT/.env"
fi

# Source common library if available
if [[ -f "$SCRIPT_DIR/lib/common.sh" ]]; then
    source "$SCRIPT_DIR/lib/common.sh"
else
    # Fallback logging functions
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    PURPLE='\033[0;35m'
    NC='\033[0m'
    
    log() { echo -e "${GREEN}[LOG]${NC} $1"; }
    info() { echo -e "${BLUE}[INFO]${NC} $1"; }
    step() { echo -e "${CYAN}[STEP]${NC} $1"; }
    success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
    warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
    error() { echo -e "${RED}[ERROR]${NC} $1" >&2; exit 1; }
    debug() { [[ "${VERBOSE:-false}" == "true" ]] && echo -e "${PURPLE}[DEBUG]${NC} $1" >&2 || true; }
    print_header() {
        echo ""
        echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
        echo -e "  ${GREEN}$1${NC}"
        echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
        echo ""
    }
fi

# =============================================================================
# Configuration Loading
# =============================================================================
# Priority: CLI args > Environment variables > _config.yml > Defaults

CONFIG_FILE="$PROJECT_ROOT/_config.yml"

# Function to read config value from _config.yml using grep (handles YAML anchors)
read_config() {
    local key="$1"
    local default="$2"
    
    if [[ -f "$CONFIG_FILE" ]]; then
        # Use grep to find the key under preview_images section
        # This is more robust than yq for files with anchors
        local in_section=false
        local value=""
        
        while IFS= read -r line; do
            # Check if we're entering the preview_images section
            if [[ "$line" =~ ^preview_images: ]]; then
                in_section=true
                continue
            fi
            
            # Check if we're leaving the section (new top-level key)
            if [[ "$in_section" == true && "$line" =~ ^[a-zA-Z_]+: && ! "$line" =~ ^[[:space:]] ]]; then
                break
            fi
            
            # Look for the key within the section
            if [[ "$in_section" == true && "$line" =~ ^[[:space:]]+${key}[[:space:]]*:[[:space:]]*(.*) ]]; then
                value="${BASH_REMATCH[1]}"
                # First, remove inline comments (only if not inside quotes)
                # Simple approach: if value starts with quote, find closing quote
                if [[ "$value" =~ ^\'([^\']*)\' ]]; then
                    value="${BASH_REMATCH[1]}"
                elif [[ "$value" =~ ^\"([^\"]*)\" ]]; then
                    value="${BASH_REMATCH[1]}"
                else
                    # No quotes, just trim and remove comment
                    value="${value%%#*}"
                    # Trim whitespace
                    value="${value%"${value##*[![:space:]]}"}"
                    value="${value#"${value%%[![:space:]]*}"}"
                fi
                if [[ -n "$value" ]]; then
                    echo "$value"
                    return
                fi
            fi
        done < "$CONFIG_FILE"
    fi
    echo "$default"
}

# Load defaults from _config.yml, with fallbacks
CONFIG_PROVIDER=$(read_config "provider" "openai")
CONFIG_MODEL=$(read_config "model" "dall-e-3")
CONFIG_SIZE=$(read_config "size" "1792x1024")
CONFIG_QUALITY=$(read_config "quality" "standard")
CONFIG_STYLE=$(read_config "style" "retro pixel art, 8-bit video game aesthetic, vibrant colors, nostalgic, clean pixel graphics")
CONFIG_STYLE_MODIFIERS=$(read_config "style_modifiers" "pixelated, retro gaming style, CRT screen glow effect, limited color palette")
CONFIG_OUTPUT_DIR=$(read_config "output_dir" "assets/images/previews")

# Default configuration (env vars override config file)
DRY_RUN="${DRY_RUN:-false}"
VERBOSE="${VERBOSE:-false}"
FORCE="${FORCE:-false}"
LIST_ONLY="${LIST_ONLY:-false}"
SPECIFIC_FILE=""
COLLECTION=""
AI_PROVIDER="${AI_PROVIDER:-$CONFIG_PROVIDER}"
OUTPUT_DIR="${OUTPUT_DIR:-$CONFIG_OUTPUT_DIR}"
IMAGE_STYLE="${IMAGE_STYLE:-$CONFIG_STYLE}"
IMAGE_STYLE_MODIFIERS="${IMAGE_STYLE_MODIFIERS:-$CONFIG_STYLE_MODIFIERS}"
IMAGE_SIZE="${IMAGE_SIZE:-$CONFIG_SIZE}"
IMAGE_QUALITY="${IMAGE_QUALITY:-$CONFIG_QUALITY}"
IMAGE_MODEL="${IMAGE_MODEL:-$CONFIG_MODEL}"

# Counters
PROCESSED=0
GENERATED=0
SKIPPED=0
ERRORS=0

# Print usage
show_help() {
    cat << 'EOF'
Usage: generate-preview-images.sh [OPTIONS]

AI-powered preview image generator for Jekyll posts and content.

OPTIONS:
    -h, --help              Show this help message
    -d, --dry-run           Preview what would be generated (no changes)
    -v, --verbose           Enable verbose output
    -f, --file FILE         Process a specific file only
    -c, --collection NAME   Process specific collection (posts, quickstart, docs)
    -p, --provider PROVIDER AI provider: openai, stability, local (default: openai)
    --output-dir DIR        Output directory for images (default: assets/images/previews)
    --force                 Regenerate images even if preview exists
    --list-missing          Only list files with missing previews

ENVIRONMENT VARIABLES:
    OPENAI_API_KEY          Required for OpenAI DALL-E provider
    STABILITY_API_KEY       Required for Stability AI provider
    IMAGE_STYLE             Override style from _config.yml
    IMAGE_SIZE              Override size (default: 1792x1024 landscape)
    IMAGE_MODEL             OpenAI model (default: dall-e-3)

CONFIGURATION:
    Default settings are loaded from _config.yml under 'preview_images' section.
    Environment variables override config file settings.

EXAMPLES:
    # List all files missing preview images
    ./scripts/generate-preview-images.sh --list-missing

    # Dry run to see what would be generated
    ./scripts/generate-preview-images.sh --dry-run --verbose

    # Generate images for posts collection
    ./scripts/generate-preview-images.sh --collection posts

    # Generate image for a specific file
    ./scripts/generate-preview-images.sh -f pages/_posts/my-article.md

    # Force regenerate all images
    ./scripts/generate-preview-images.sh --force

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -d|--dry-run)
                DRY_RUN="true"
                ;;
            -v|--verbose)
                VERBOSE="true"
                ;;
            -f|--file)
                SPECIFIC_FILE="$2"
                shift
                ;;
            -c|--collection)
                COLLECTION="$2"
                shift
                ;;
            -p|--provider)
                AI_PROVIDER="$2"
                shift
                ;;
            --output-dir)
                OUTPUT_DIR="$2"
                shift
                ;;
            --force)
                FORCE="true"
                ;;
            --list-missing)
                LIST_ONLY="true"
                ;;
            *)
                error "Unknown option: $1. Use --help for usage."
                ;;
        esac
        shift
    done
}

# Validate environment and dependencies
validate_environment() {
    step "Validating environment..."
    
    # Check for required commands
    local required_cmds=("curl" "jq")
    for cmd in "${required_cmds[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            error "Required command not found: $cmd"
        fi
    done
    
    # Check for YAML parser (prefer yq, fallback to python)
    if command -v yq &> /dev/null; then
        YAML_PARSER="yq"
        debug "Using yq for YAML parsing"
    elif command -v python3 &> /dev/null; then
        YAML_PARSER="python"
        debug "Using python for YAML parsing"
    else
        error "No YAML parser found. Install yq or python3."
    fi
    
    # Validate AI provider credentials (unless list-only or dry-run)
    if [[ "$LIST_ONLY" != "true" && "$DRY_RUN" != "true" ]]; then
        case "$AI_PROVIDER" in
            openai)
                if [[ -z "${OPENAI_API_KEY:-}" ]]; then
                    error "OPENAI_API_KEY environment variable is required for OpenAI provider"
                fi
                ;;
            stability)
                if [[ -z "${STABILITY_API_KEY:-}" ]]; then
                    error "STABILITY_API_KEY environment variable is required for Stability AI provider"
                fi
                ;;
            local)
                info "Using local provider - no API key required"
                ;;
            *)
                error "Unknown AI provider: $AI_PROVIDER"
                ;;
        esac
    fi
    
    # Ensure output directory exists
    local full_output_dir="$PROJECT_ROOT/$OUTPUT_DIR"
    if [[ ! -d "$full_output_dir" ]]; then
        if [[ "$DRY_RUN" != "true" ]]; then
            mkdir -p "$full_output_dir"
            debug "Created output directory: $full_output_dir"
        else
            debug "Would create output directory: $full_output_dir"
        fi
    fi
    
    success "Environment validation passed"
}

# Extract front matter from a markdown file
extract_front_matter() {
    local file="$1"
    
    # Extract content between --- markers
    sed -n '/^---$/,/^---$/p' "$file" | sed '1d;$d'
}

# Get YAML value using available parser
get_yaml_value() {
    local yaml="$1"
    local key="$2"
    local result=""
    
    if [[ "$YAML_PARSER" == "yq" ]]; then
        # yq v4 syntax - read from stdin and get specific key
        result=$(echo "$yaml" | yq eval ".$key" - 2>/dev/null | head -1)
        # Filter out null values
        if [[ "$result" == "null" || -z "$result" ]]; then
            result=""
        fi
    else
        # Python fallback
        result=$(python3 -c "
import yaml
import sys
try:
    data = yaml.safe_load('''$yaml''')
    if data and '$key' in data:
        val = data['$key']
        if val is not None:
            print(val)
except:
    pass
" 2>/dev/null || echo "")
    fi
    
    echo "$result"
}

# Extract post content (without front matter)
extract_content() {
    local file="$1"
    
    # Skip front matter and get content
    awk '/^---$/ { if (++count == 2) found=1; next } found { print }' "$file"
}

# Check if preview image exists
check_preview_exists() {
    local preview_path="$1"
    
    if [[ -z "$preview_path" ]]; then
        return 1
    fi
    
    # Handle paths starting with /
    local clean_path="${preview_path#/}"
    local full_path="$PROJECT_ROOT/$clean_path"
    
    # Also check in assets/images
    if [[ ! -f "$full_path" ]]; then
        full_path="$PROJECT_ROOT/assets/$clean_path"
    fi
    
    [[ -f "$full_path" ]]
}

# Generate image prompt from content
generate_prompt() {
    local title="$1"
    local description="$2"
    local categories="$3"
    local content="$4"
    
    # Build a meaningful prompt
    local prompt="Create a blog preview banner image for an article titled '$title'."
    
    if [[ -n "$description" ]]; then
        prompt="$prompt The article is about: $description."
    fi
    
    if [[ -n "$categories" ]]; then
        prompt="$prompt Categories: $categories."
    fi
    
    # Extract key themes from content (first 500 chars)
    local content_excerpt="${content:0:500}"
    if [[ -n "$content_excerpt" ]]; then
        prompt="$prompt Key themes from content: $content_excerpt"
    fi
    
    # Add style instructions and modifiers
    prompt="$prompt Art style: $IMAGE_STYLE."
    if [[ -n "$IMAGE_STYLE_MODIFIERS" ]]; then
        prompt="$prompt Additional style: $IMAGE_STYLE_MODIFIERS."
    fi
    prompt="$prompt The image should be suitable as a wide blog header/banner image with clean composition. No text or words in the image."
    
    echo "$prompt"
}

# Generate image using OpenAI DALL-E
generate_image_openai() {
    local prompt="$1"
    local output_file="$2"
    
    debug "Generating image with OpenAI DALL-E..."
    debug "Prompt: ${prompt:0:200}..."
    
    local response
    response=$(curl -s -X POST "https://api.openai.com/v1/images/generations" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$IMAGE_MODEL\",
            \"prompt\": $(echo "$prompt" | jq -Rs .),
            \"n\": 1,
            \"size\": \"$IMAGE_SIZE\",
            \"quality\": \"$IMAGE_QUALITY\"
        }")
    
    # Check for errors
    local error_msg
    error_msg=$(echo "$response" | jq -r '.error.message // empty')
    if [[ -n "$error_msg" ]]; then
        warn "OpenAI API error: $error_msg"
        return 1
    fi
    
    # Extract image URL
    local image_url
    image_url=$(echo "$response" | jq -r '.data[0].url // empty')
    
    if [[ -z "$image_url" ]]; then
        warn "No image URL in response"
        debug "Response: $response"
        return 1
    fi
    
    # Download image
    debug "Downloading image from: $image_url"
    curl -s -o "$output_file" "$image_url"
    
    if [[ -f "$output_file" ]]; then
        success "Image saved to: $output_file"
        return 0
    else
        warn "Failed to save image"
        return 1
    fi
}

# Generate image using Stability AI
generate_image_stability() {
    local prompt="$1"
    local output_file="$2"
    
    debug "Generating image with Stability AI..."
    
    local response
    response=$(curl -s -X POST "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image" \
        -H "Authorization: Bearer $STABILITY_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"text_prompts\": [{\"text\": $(echo "$prompt" | jq -Rs .)}],
            \"cfg_scale\": 7,
            \"height\": 1024,
            \"width\": 1024,
            \"samples\": 1,
            \"steps\": 30
        }")
    
    # Check for errors
    local error_msg
    error_msg=$(echo "$response" | jq -r '.message // empty')
    if [[ -n "$error_msg" ]]; then
        warn "Stability API error: $error_msg"
        return 1
    fi
    
    # Extract and decode base64 image
    local base64_image
    base64_image=$(echo "$response" | jq -r '.artifacts[0].base64 // empty')
    
    if [[ -z "$base64_image" ]]; then
        warn "No image data in response"
        return 1
    fi
    
    echo "$base64_image" | base64 -d > "$output_file"
    
    if [[ -f "$output_file" ]]; then
        success "Image saved to: $output_file"
        return 0
    else
        warn "Failed to save image"
        return 1
    fi
}

# Generate placeholder for local provider (for testing)
generate_image_local() {
    local prompt="$1"
    local output_file="$2"
    
    warn "Local provider: No actual image generation. Creating placeholder..."
    debug "Would generate image with prompt: ${prompt:0:200}..."
    
    # Create a simple placeholder file
    echo "PLACEHOLDER: $prompt" > "$output_file.txt"
    
    info "Placeholder created: $output_file.txt"
    return 0
}

# Generate image using selected provider
generate_image() {
    local prompt="$1"
    local output_file="$2"
    
    case "$AI_PROVIDER" in
        openai)
            generate_image_openai "$prompt" "$output_file"
            ;;
        stability)
            generate_image_stability "$prompt" "$output_file"
            ;;
        local)
            generate_image_local "$prompt" "$output_file"
            ;;
        *)
            error "Unknown provider: $AI_PROVIDER"
            ;;
    esac
}

# Update front matter with new preview path
update_front_matter() {
    local file="$1"
    local preview_path="$2"
    
    debug "Updating front matter in: $file"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        info "[DRY RUN] Would update preview in $file to: $preview_path"
        return 0
    fi
    
    # Create backup
    cp "$file" "$file.bak"
    
    # Always use sed for reliability (yq can fail on complex YAML)
    # Check if preview field exists
    if grep -q "^preview:" "$file"; then
        # Update existing preview field using sed
        if [[ "$(uname)" == "Darwin" ]]; then
            # macOS sed requires empty string for -i
            sed -i '' "s|^preview:.*|preview: $preview_path|" "$file"
        else
            sed -i "s|^preview:.*|preview: $preview_path|" "$file"
        fi
    else
        # Add preview field after description or title
        if grep -q "^description:" "$file"; then
            if [[ "$(uname)" == "Darwin" ]]; then
                sed -i '' "/^description:/a\\
preview: $preview_path" "$file"
            else
                sed -i "/^description:/a\\
preview: $preview_path" "$file"
            fi
        else
            if [[ "$(uname)" == "Darwin" ]]; then
                sed -i '' "/^title:/a\\
preview: $preview_path" "$file"
            else
                sed -i "/^title:/a\\
preview: $preview_path" "$file"
            fi
        fi
    fi
    
    # Remove backup on success
    rm -f "$file.bak"
    
    success "Updated front matter with preview: $preview_path"
}

# Process a single file
process_file() {
    local file="$1"
    
    PROCESSED=$((PROCESSED + 1))
    
    debug "Processing file: $file"
    
    # Extract front matter
    local front_matter
    front_matter=$(extract_front_matter "$file")
    
    if [[ -z "$front_matter" ]]; then
        debug "No front matter found in: $file"
        SKIPPED=$((SKIPPED + 1))
        return 0
    fi
    
    # Get metadata
    local title description categories preview
    title=$(get_yaml_value "$front_matter" "title")
    description=$(get_yaml_value "$front_matter" "description")
    categories=$(get_yaml_value "$front_matter" "categories")
    preview=$(get_yaml_value "$front_matter" "preview")
    
    debug "Title: $title"
    debug "Preview: $preview"
    
    # Check if preview exists and is valid
    if [[ -n "$preview" ]] && check_preview_exists "$preview"; then
        if [[ "$FORCE" != "true" ]]; then
            debug "Preview already exists and is valid: $preview"
            SKIPPED=$((SKIPPED + 1))
            return 0
        else
            info "Force mode: regenerating preview for $title"
        fi
    fi
    
    # Report missing preview
    if [[ "$LIST_ONLY" == "true" ]]; then
        echo -e "${YELLOW}Missing preview:${NC} $file"
        echo -e "  Title: $title"
        if [[ -n "$preview" ]]; then
            echo -e "  Current preview (not found): $preview"
        fi
        echo ""
        return 0
    fi
    
    info "Generating preview for: $title"
    
    # Generate filename from title
    local safe_filename
    safe_filename=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')
    safe_filename="${safe_filename:0:50}"  # Limit length
    
    local output_file="$PROJECT_ROOT/$OUTPUT_DIR/${safe_filename}.png"
    # Preview path should NOT include /assets/ prefix since the template adds it
    local preview_path="/images/previews/${safe_filename}.png"
    
    # Extract content for prompt generation
    local content
    content=$(extract_content "$file")
    
    # Generate prompt
    local prompt
    prompt=$(generate_prompt "$title" "$description" "$categories" "$content")
    
    debug "Generated prompt: ${prompt:0:500}..."
    
    if [[ "$DRY_RUN" == "true" ]]; then
        info "[DRY RUN] Would generate image:"
        echo "  Output: $output_file"
        echo "  Preview path: $preview_path"
        echo "  Prompt: ${prompt:0:400}..."
        echo ""
        GENERATED=$((GENERATED + 1))
        return 0
    fi
    
    # Generate image
    if generate_image "$prompt" "$output_file"; then
        # Update front matter with new preview path
        update_front_matter "$file" "$preview_path"
        GENERATED=$((GENERATED + 1))
    else
        warn "Failed to generate image for: $title"
        ERRORS=$((ERRORS + 1))
    fi
}

# Find and process content files
process_collection() {
    local collection_path="$1"
    local pattern="${2:-*.md}"
    
    debug "Processing collection: $collection_path with pattern: $pattern"
    
    if [[ ! -d "$collection_path" ]]; then
        warn "Collection directory not found: $collection_path"
        return 1
    fi
    
    while IFS= read -r -d '' file; do
        process_file "$file"
    done < <(find "$collection_path" -name "$pattern" -type f -print0)
}

# Main function
main() {
    print_header "🎨 Preview Image Generator"
    
    # Validate environment
    validate_environment
    
    # Display configuration
    info "Configuration:"
    echo "  AI Provider: $AI_PROVIDER"
    echo "  Output Dir: $OUTPUT_DIR"
    echo "  Image Size: $IMAGE_SIZE"
    echo "  Dry Run: $DRY_RUN"
    echo "  Force: $FORCE"
    echo "  List Only: $LIST_ONLY"
    echo ""
    
    # Get configured collections from _config.yml
    get_configured_collections() {
        local collections=()
        local in_preview_images=false
        local in_collections=false
        
        while IFS= read -r line; do
            if [[ "$line" =~ ^preview_images: ]]; then
                in_preview_images=true
                continue
            fi
            if [[ "$in_preview_images" == true && "$line" =~ ^[[:space:]]+collections: ]]; then
                in_collections=true
                continue
            fi
            if [[ "$in_collections" == true && "$line" =~ ^[[:space:]]+- ]]; then
                local collection="${line#*- }"
                collection="${collection%%#*}"
                collection="${collection%"${collection##*[![:space:]]}"}"
                collections+=("$collection")
            elif [[ "$in_collections" == true && ! "$line" =~ ^[[:space:]]+-  && ! "$line" =~ ^[[:space:]]*$ ]]; then
                break
            fi
            if [[ "$in_preview_images" == true && "$line" =~ ^[a-zA-Z_]+: && ! "$line" =~ ^[[:space:]] ]]; then
                break
            fi
        done < "$CONFIG_FILE"
        
        if [[ ${#collections[@]} -eq 0 ]]; then
            collections=("posts" "quickstart" "docs")
        fi
        
        echo "${collections[@]}"
    }
    
    # Process a collection by name
    process_collection_by_name() {
        local name="$1"
        local path="$PROJECT_ROOT/pages/_${name}"
        
        if [[ -d "$path" ]]; then
            step "Processing ${name} collection..."
            process_collection "$path"
        else
            warn "Collection directory not found: $path"
        fi
    }
    
    # Process files
    if [[ -n "$SPECIFIC_FILE" ]]; then
        # Process single file
        if [[ ! -f "$PROJECT_ROOT/$SPECIFIC_FILE" ]]; then
            error "File not found: $SPECIFIC_FILE"
        fi
        process_file "$PROJECT_ROOT/$SPECIFIC_FILE"
    elif [[ -n "$COLLECTION" ]]; then
        # Process specific collection
        if [[ "$COLLECTION" == "all" ]]; then
            step "Processing all configured collections..."
            for col in $(get_configured_collections); do
                process_collection_by_name "$col"
            done
        else
            # Check if collection directory exists
            local collection_path="$PROJECT_ROOT/pages/_${COLLECTION}"
            if [[ -d "$collection_path" ]]; then
                process_collection_by_name "$COLLECTION"
            else
                local available=$(get_configured_collections | tr ' ' ', ')
                error "Unknown collection: $COLLECTION. Available: $available, all"
            fi
        fi
    else
        # Process all configured collections by default
        step "Processing all configured collections..."
        for col in $(get_configured_collections); do
            process_collection_by_name "$col"
        done
    fi
    
    # Print summary
    echo ""
    print_header "📊 Summary"
    echo "  Files processed: $PROCESSED"
    echo "  Images generated: $GENERATED"
    echo "  Files skipped: $SKIPPED"
    echo "  Errors: $ERRORS"
    echo ""
    
    if [[ "$DRY_RUN" == "true" ]]; then
        info "This was a dry run. No actual changes were made."
    fi
    
    if [[ "$ERRORS" -gt 0 ]]; then
        warn "Some files had errors. Check the output above."
        exit 1
    fi
    
    success "Preview image generation complete!"
}

# Parse arguments and run
parse_args "$@"
main
