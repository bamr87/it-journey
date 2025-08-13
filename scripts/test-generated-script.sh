#!/bin/bash
# test-generated-script.sh
# Test the generated zer0-to-hero script in a safe way
# Usage: ./test-generated-script.sh [dry-run|validate|help]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATED_SCRIPT="$SCRIPT_DIR/zer0-to-hero-generated.sh"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

show_help() {
    cat << EOF
🧪 Generated Script Tester

Usage: $0 [command]

Commands:
  validate    - Check if generated script is valid
  dry-run     - Show what the script would do (safe)
  help        - Show this help message

Examples:
  $0 validate         # Check script syntax and structure
  $0 dry-run          # Preview script execution
  $0                  # Interactive mode

The generated script is located at:
  $GENERATED_SCRIPT
EOF
}

validate_script() {
    log "Validating generated script..."
    
    if [[ ! -f "$GENERATED_SCRIPT" ]]; then
        error "Generated script not found. Run ./generate-zer0-script.sh first"
        return 1
    fi
    
    if [[ ! -x "$GENERATED_SCRIPT" ]]; then
        error "Generated script is not executable"
        return 1
    fi
    
    # Check bash syntax
    if bash -n "$GENERATED_SCRIPT"; then
        success "Script syntax is valid"
    else
        error "Script has syntax errors"
        return 1
    fi
    
    # Check for required functions
    local required_functions=("main" "setup_environment" "install_development_tools" "setup_github" "create_project")
    for func in "${required_functions[@]}"; do
        if grep -q "^${func}()" "$GENERATED_SCRIPT"; then
            success "Function $func found"
        else
            warning "Function $func not found"
        fi
    done
    
    # Show script info
    echo ""
    echo "📊 Script Information:"
    echo "  Size: $(wc -l < "$GENERATED_SCRIPT") lines"
    echo "  Executable: $(if [[ -x "$GENERATED_SCRIPT" ]]; then echo "Yes"; else echo "No"; fi)"
    echo "  Created: $(stat -f "%Sm" "$GENERATED_SCRIPT")"
    
    success "Script validation complete"
}

dry_run() {
    log "Performing dry run analysis..."
    
    if [[ ! -f "$GENERATED_SCRIPT" ]]; then
        error "Generated script not found. Run ./generate-zer0-script.sh first"
        return 1
    fi
    
    echo ""
    echo "🔍 Script Analysis (Dry Run):"
    echo "================================"
    
    # Show main phases
    echo ""
    echo "📋 Execution Phases:"
    grep -n "log.*Phase" "$GENERATED_SCRIPT" | while IFS= read -r line; do
        echo "  $line"
    done
    
    # Show safe_execute calls
    echo ""
    echo "🔧 Operations to be performed:"
    grep -n "safe_execute" "$GENERATED_SCRIPT" | head -10 | while IFS= read -r line; do
        echo "  $line"
    done
    
    if [[ $(grep -c "safe_execute" "$GENERATED_SCRIPT") -gt 10 ]]; then
        echo "  ... and $(( $(grep -c "safe_execute" "$GENERATED_SCRIPT") - 10 )) more operations"
    fi
    
    # Show external dependencies
    echo ""
    echo "🌐 External Dependencies:"
    grep -oE "curl.*https://[^[:space:]]+" "$GENERATED_SCRIPT" | head -5 | while IFS= read -r url; do
        echo "  $url"
    done
    
    # Show file operations
    echo ""
    echo "📁 File Operations:"
    grep -E "mkdir|cat >|echo.*>" "$GENERATED_SCRIPT" | head -5 | while IFS= read -r op; do
        echo "  $(echo "$op" | cut -c1-80)..."
    done
    
    echo ""
    warning "This is a DRY RUN - no actual changes would be made"
    echo "To run the actual script: $GENERATED_SCRIPT"
}

interactive_mode() {
    echo "🧪 Generated Script Tester"
    echo "========================="
    echo ""
    
    if [[ ! -f "$GENERATED_SCRIPT" ]]; then
        warning "Generated script not found."
        echo "Run ./generate-zer0-script.sh to create it first."
        return 1
    fi
    
    echo "Options:"
    echo "1. Validate script"
    echo "2. Dry run analysis"
    echo "3. View script content"
    echo "4. Run the actual script"
    echo "5. Help"
    echo ""
    
    read -p "Choose an option (1-5): " choice
    
    case $choice in
        1)
            validate_script
            ;;
        2)
            dry_run
            ;;
        3)
            echo "📄 Script Content:"
            echo "=================="
            cat "$GENERATED_SCRIPT" | head -50
            echo ""
            echo "... (showing first 50 lines)"
            echo "Full script: $GENERATED_SCRIPT"
            ;;
        4)
            warning "About to run the actual script!"
            echo "This will make real changes to your system."
            read -p "Are you sure? (y/N): " confirm
            if [[ $confirm =~ ^[Yy]$ ]]; then
                log "Running generated script..."
                exec "$GENERATED_SCRIPT"
            else
                echo "Cancelled."
            fi
            ;;
        5)
            show_help
            ;;
        *)
            error "Invalid option"
            ;;
    esac
}

main() {
    case "${1:-interactive}" in
        validate)
            validate_script
            ;;
        dry-run)
            dry_run
            ;;
        help|--help|-h)
            show_help
            ;;
        interactive)
            interactive_mode
            ;;
        *)
            error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
