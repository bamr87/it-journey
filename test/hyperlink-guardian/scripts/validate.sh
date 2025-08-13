#!/bin/bash
# validate.sh - Guardian 2.0 Validation and Setup Script
# Local testing and environment validation for the Hyperlink Guardian

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
TEST_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Logging functions
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Configuration
DRY_RUN=false
SETUP_MODE=false
QUICK_TEST=false
VERBOSE=false

show_help() {
    cat << EOF
${CYAN}Guardian 2.0 Validation Script${NC}

${YELLOW}Usage:${NC} $0 [OPTIONS] [COMMAND]

${YELLOW}Commands:${NC}
    setup           Set up development environment
    validate        Validate Guardian 2.0 installation
    test            Run quick validation test
    dependencies    Check and install dependencies
    config          Validate configuration files
    help            Show this help message

${YELLOW}Options:${NC}
    -h, --help      Show this help message
    -v, --verbose   Enable verbose output
    -d, --dry-run   Show what would be done without executing
    -q, --quick     Run quick tests only

${YELLOW}Examples:${NC}
    $0 setup                    # Set up development environment
    $0 validate --verbose       # Full validation with verbose output
    $0 test --quick             # Quick functionality test
    $0 dependencies             # Check dependencies only
    $0 config                   # Validate configuration files
EOF
}

# Check system dependencies
check_dependencies() {
    log_info "Checking system dependencies..."
    local missing_deps=()
    
    # Required commands
    local required_commands=("curl" "jq" "bc" "python3")
    
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            missing_deps+=("$cmd")
            log_error "Missing required command: $cmd"
        else
            log_success "Found: $cmd"
        fi
    done
    
    # Check Python packages
    log_info "Checking Python packages..."
    if command -v python3 >/dev/null 2>&1; then
        local python_packages=("openai" "requests" "yaml")
        for package in "${python_packages[@]}"; do
            if ! python3 -c "import $package" 2>/dev/null; then
                log_warning "Missing Python package: $package"
                if [[ "$SETUP_MODE" == "true" ]]; then
                    log_info "Installing $package..."
                    if [[ "$DRY_RUN" == "false" ]]; then
                        pip3 install "$package" --break-system-packages || log_error "Failed to install $package"
                    fi
                fi
            else
                log_success "Found Python package: $package"
            fi
        done
    fi
    
    # Check Node.js packages (optional)
    if command -v npm >/dev/null 2>&1; then
        if ! npm list -g markdown-link-check >/dev/null 2>&1; then
            log_warning "Missing: markdown-link-check (optional)"
            if [[ "$SETUP_MODE" == "true" ]]; then
                log_info "Installing markdown-link-check globally..."
                if [[ "$DRY_RUN" == "false" ]]; then
                    npm install -g markdown-link-check || log_warning "Failed to install markdown-link-check"
                fi
            fi
        else
            log_success "Found: markdown-link-check"
        fi
    fi
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        log_info "Please install missing dependencies or run with --setup"
        return 1
    fi
    
    log_success "All dependencies satisfied"
    return 0
}

# Validate configuration files
validate_config() {
    log_info "Validating configuration files..."
    
    local config_dir="$TEST_DIR/config"
    local configs_valid=true
    
    # Check main config file
    local main_config="$config_dir/guardian-config.yml"
    if [[ -f "$main_config" ]]; then
        log_success "Found main configuration: guardian-config.yml"
        
        # Validate YAML syntax
        if command -v python3 >/dev/null 2>&1; then
            if python3 -c "import yaml; yaml.safe_load(open('$main_config'))" 2>/dev/null; then
                log_success "Configuration YAML syntax is valid"
            else
                log_error "Invalid YAML syntax in guardian-config.yml"
                configs_valid=false
            fi
        fi
    else
        log_warning "Main configuration file not found: guardian-config.yml"
    fi
    
    # Check exclusions file
    local exclusions_file="$config_dir/exclusions.txt"
    if [[ -f "$exclusions_file" ]]; then
        log_success "Found exclusions file: exclusions.txt"
        local exclusion_count
        exclusion_count=$(grep -v '^#' "$exclusions_file" | grep -v '^$' | wc -l)
        log_info "Found $exclusion_count exclusion patterns"
    else
        log_warning "Exclusions file not found: exclusions.txt"
    fi
    
    # Validate script permissions
    local scripts_dir="$TEST_DIR/scripts"
    for script in "$scripts_dir"/*.sh "$scripts_dir"/*.py; do
        if [[ -f "$script" ]]; then
            if [[ -x "$script" ]]; then
                log_success "Script is executable: $(basename "$script")"
            else
                log_warning "Script not executable: $(basename "$script")"
                if [[ "$SETUP_MODE" == "true" && "$DRY_RUN" == "false" ]]; then
                    chmod +x "$script"
                    log_info "Made executable: $(basename "$script")"
                fi
            fi
        fi
    done
    
    return $([[ "$configs_valid" == "true" ]] && echo 0 || echo 1)
}

# Run quick functionality test
run_quick_test() {
    log_info "Running quick Guardian 2.0 functionality test..."
    
    local test_output_dir="$PROJECT_ROOT/test-validation-results"
    mkdir -p "$test_output_dir"
    
    # Test basic script execution
    log_info "Testing Guardian script execution..."
    if [[ "$DRY_RUN" == "false" ]]; then
        local guardian_script="$TEST_DIR/scripts/guardian.sh"
        
        if "$guardian_script" --help >/dev/null 2>&1; then
            log_success "Guardian script help works"
        else
            log_error "Guardian script help failed"
            return 1
        fi
        
        # Test AI analyzer
        local ai_script="$TEST_DIR/scripts/ai-analyzer.py"
        if python3 "$ai_script" --help >/dev/null 2>&1; then
            log_success "AI analyzer help works"
        else
            log_error "AI analyzer help failed"
            return 1
        fi
        
        # Quick scan test (if not in quick mode, skip actual scanning)
        if [[ "$QUICK_TEST" == "false" ]]; then
            log_info "Running minimal link scan test..."
            
            # Create a test file with a few links
            local test_file="$test_output_dir/test-links.md"
            cat > "$test_file" << EOF
# Test Links
[Google](https://www.google.com)
[GitHub](https://github.com)
[Broken Link](https://this-should-not-exist-404.example.com)
EOF
            
            # Run guardian on just this test file
            cd "$PROJECT_ROOT"
            if OUTPUT_DIR="$test_output_dir" \
               MAX_PARALLEL=2 \
               TIMEOUT=10 \
               VERBOSE="$VERBOSE" \
               "$guardian_script" --verbose --timeout 10 --parallel 2 --output "$test_output_dir"; then
                log_success "Quick scan test completed"
                
                # Check if results were generated
                if [[ -f "$test_output_dir/summary.json" ]]; then
                    log_success "Summary file generated"
                    local total_links
                    total_links=$(jq -r '.summary_statistics.total_links // 0' "$test_output_dir/summary.json")
                    log_info "Test scanned $total_links links"
                else
                    log_warning "Summary file not generated"
                fi
            else
                log_error "Quick scan test failed"
                return 1
            fi
            
            # Cleanup test files
            rm -rf "$test_output_dir"
        fi
    else
        log_info "DRY RUN: Would test Guardian script execution"
    fi
    
    log_success "Quick functionality test completed"
    return 0
}

# Setup development environment
setup_environment() {
    log_info "Setting up Guardian 2.0 development environment..."
    
    # Create required directories
    local required_dirs=(
        "$PROJECT_ROOT/test-results"
        "$PROJECT_ROOT/test-results/artifacts"
        "$PROJECT_ROOT/test-results/reports"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            if [[ "$DRY_RUN" == "false" ]]; then
                mkdir -p "$dir"
                log_success "Created directory: ${dir#$PROJECT_ROOT/}"
            else
                log_info "DRY RUN: Would create directory: ${dir#$PROJECT_ROOT/}"
            fi
        else
            log_success "Directory exists: ${dir#$PROJECT_ROOT/}"
        fi
    done
    
    # Install dependencies
    SETUP_MODE=true
    check_dependencies
    
    # Validate and fix configurations
    validate_config
    
    # Set up git hooks (optional)
    local git_hooks_dir="$PROJECT_ROOT/.git/hooks"
    if [[ -d "$git_hooks_dir" ]]; then
        log_info "Git repository detected - setting up optional hooks..."
        # Could add pre-commit hooks here if desired
    fi
    
    log_success "Development environment setup completed"
}

# Full validation
run_full_validation() {
    log_info "Running full Guardian 2.0 validation..."
    
    local validation_failed=false
    
    # Check dependencies
    if ! check_dependencies; then
        validation_failed=true
    fi
    
    # Validate configuration
    if ! validate_config; then
        validation_failed=true
    fi
    
    # Run functionality test
    if ! run_quick_test; then
        validation_failed=true
    fi
    
    # Check project structure
    log_info "Validating project structure..."
    local required_files=(
        "$TEST_DIR/scripts/guardian.sh"
        "$TEST_DIR/scripts/ai-analyzer.py"
        "$TEST_DIR/config/guardian-config.yml"
        "$TEST_DIR/config/exclusions.txt"
        "$TEST_DIR/README.md"
    )
    
    for file in "${required_files[@]}"; do
        if [[ -f "$file" ]]; then
            log_success "Found required file: ${file#$TEST_DIR/}"
        else
            log_error "Missing required file: ${file#$TEST_DIR/}"
            validation_failed=true
        fi
    done
    
    if [[ "$validation_failed" == "true" ]]; then
        log_error "Validation failed - some issues need to be resolved"
        return 1
    else
        log_success "All validation checks passed!"
        return 0
    fi
}

# Parse arguments
parse_arguments() {
    local command=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -q|--quick)
                QUICK_TEST=true
                shift
                ;;
            setup|validate|test|dependencies|config|help)
                command="$1"
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Set verbose logging if requested
    if [[ "$VERBOSE" == "true" ]]; then
        set -x
    fi
    
    # Execute command
    case "$command" in
        setup)
            setup_environment
            ;;
        validate)
            run_full_validation
            ;;
        test)
            run_quick_test
            ;;
        dependencies)
            check_dependencies
            ;;
        config)
            validate_config
            ;;
        help|"")
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Main execution
main() {
    echo -e "${CYAN}"
    echo "🔗 ========================================== 🔗"
    echo "   Guardian 2.0 Validation & Setup"
    echo "   IT-Journey Testing Framework"
    echo "🔗 ========================================== 🔗"
    echo -e "${NC}"
    
    if [[ $# -eq 0 ]]; then
        show_help
        exit 0
    fi
    
    parse_arguments "$@"
}

# Execute if run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi 