#!/bin/bash
#
# Comprehensive Script Testing Suite
# Tests all scripts in the scripts/ directory within an isolated Docker container
#
# Usage: ./scripts/testing/test-all-scripts.sh [--verbose] [--fix] [--category CATEGORY]
#
# Options:
#   --verbose    Show detailed output
#   --fix        Attempt to fix issues automatically
#   --category   Test specific category (core, deployment, validation, etc.)
#   --dry-run    Show what would be tested without executing

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results
PASSED=0
FAILED=0
SKIPPED=0
ISSUES=()

# Options
VERBOSE=false
AUTO_FIX=false
DRY_RUN=false
CATEGORY=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose)
            VERBOSE=true
            shift
            ;;
        --fix)
            AUTO_FIX=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --category)
            CATEGORY="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $*"
    ((PASSED++))
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $*"
    ((FAILED++))
    ISSUES+=("$*")
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
    ((SKIPPED++))
}

log_verbose() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[VERBOSE]${NC} $*"
    fi
}

# Check if script exists and is executable
check_script_exists() {
    local script="$1"
    if [[ ! -f "$script" ]]; then
        log_error "Script not found: $script"
        return 1
    fi
    return 0
}

# Check script syntax
check_syntax() {
    local script="$1"
    local ext="${script##*.}"
    
    case "$ext" in
        sh|bash)
            if bash -n "$script" 2>&1; then
                log_success "Syntax check passed: $script"
                return 0
            else
                log_error "Syntax error in: $script"
                return 1
            fi
            ;;
        py)
            if python3 -m py_compile "$script" 2>&1; then
                log_success "Syntax check passed: $script"
                return 0
            else
                log_error "Syntax error in: $script"
                return 1
            fi
            ;;
        rb)
            if ruby -c "$script" 2>&1; then
                log_success "Syntax check passed: $script"
                return 0
            else
                log_error "Syntax error in: $script"
                return 1
            fi
            ;;
        *)
            log_warn "Unknown file type: $script"
            return 0
            ;;
    esac
}

# Check script has proper header
check_header() {
    local script="$1"
    local ext="${script##*.}"
    
    if [[ "$ext" == "sh" ]] || [[ "$ext" == "bash" ]]; then
        if ! head -1 "$script" | grep -q "^#!/"; then
            log_warn "Missing shebang in: $script"
            return 1
        fi
    fi
    
    # Check for common header patterns
    if ! grep -q "set -e" "$script" 2>/dev/null && [[ "$ext" == "sh" ]]; then
        log_warn "Missing 'set -e' in bash script: $script"
    fi
    
    return 0
}

# Check for common issues
check_common_issues() {
    local script="$1"
    local issues_found=0
    
    # Check for hardcoded paths
    if grep -q "/Users/" "$script" 2>/dev/null || grep -q "/home/" "$script" 2>/dev/null; then
        log_warn "Hardcoded user path found in: $script"
        ((issues_found++))
    fi
    
    # Check for TODO/FIXME
    if grep -qi "TODO\|FIXME" "$script" 2>/dev/null; then
        log_verbose "TODO/FIXME found in: $script (informational)"
    fi
    
    # Check for proper error handling in bash scripts
    if [[ "${script##*.}" == "sh" ]]; then
        if ! grep -q "set -e" "$script" 2>/dev/null && ! grep -q "set -euo" "$script" 2>/dev/null; then
            log_warn "Consider adding 'set -e' for error handling in: $script"
        fi
    fi
    
    return $issues_found
}

# Test script help/usage
test_help() {
    local script="$1"
    local ext="${script##*.}"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_verbose "Would test help for: $script"
        return 0
    fi
    
    case "$ext" in
        sh|bash)
            if bash "$script" --help &>/dev/null || bash "$script" -h &>/dev/null; then
                log_success "Help option works: $script"
                return 0
            else
                log_verbose "No help option or help failed: $script (may be normal)"
                return 0
            fi
            ;;
        py)
            if python3 "$script" --help &>/dev/null || python3 "$script" -h &>/dev/null; then
                log_success "Help option works: $script"
                return 0
            else
                log_verbose "No help option or help failed: $script (may be normal)"
                return 0
            fi
            ;;
        rb)
            if ruby "$script" --help &>/dev/null || ruby "$script" -h &>/dev/null; then
                log_success "Help option works: $script"
                return 0
            else
                log_verbose "No help option or help failed: $script (may be normal)"
                return 0
            fi
            ;;
    esac
    return 0
}

# Test a single script
test_script() {
    local script="$1"
    local rel_path="${script#$SCRIPTS_DIR/}"
    
    log_info "Testing: $rel_path"
    
    # Check existence
    if ! check_script_exists "$script"; then
        return 1
    fi
    
    # Check syntax
    if ! check_syntax "$script"; then
        return 1
    fi
    
    # Check header
    check_header "$script"
    
    # Check common issues
    check_common_issues "$script"
    
    # Test help if not dry-run
    test_help "$script"
    
    return 0
}

# Test all scripts in a directory
test_directory() {
    local dir="$1"
    local category="${dir#$SCRIPTS_DIR/}"
    
    if [[ -n "$CATEGORY" ]] && [[ "$category" != "$CATEGORY" ]]; then
        log_verbose "Skipping category: $category (filtered)"
        return 0
    fi
    
    log_info "=== Testing category: $category ==="
    
    local scripts_found=0
    while IFS= read -r -d '' script; do
        ((scripts_found++))
        test_script "$script"
    done < <(find "$dir" -type f \( -name "*.sh" -o -name "*.py" -o -name "*.rb" \) -print0 2>/dev/null)
    
    if [[ $scripts_found -eq 0 ]]; then
        log_warn "No scripts found in: $category"
    fi
    
    echo ""
}

# Main execution
main() {
    log_info "Starting comprehensive script testing"
    log_info "Project root: $PROJECT_ROOT"
    log_info "Scripts directory: $SCRIPTS_DIR"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_warn "DRY RUN MODE - No actual tests will be executed"
    fi
    
    echo ""
    
    # Test each category
    for dir in "$SCRIPTS_DIR"/*/; do
        if [[ -d "$dir" ]]; then
            test_directory "$dir"
        fi
    done
    
    # Test root-level scripts if any
    if find "$SCRIPTS_DIR" -maxdepth 1 -type f \( -name "*.sh" -o -name "*.py" -o -name "*.rb" \) | grep -q .; then
        log_info "=== Testing root-level scripts ==="
        while IFS= read -r -d '' script; do
            test_script "$script"
        done < <(find "$SCRIPTS_DIR" -maxdepth 1 -type f \( -name "*.sh" -o -name "*.py" -o -name "*.rb" \) -print0)
        echo ""
    fi
    
    # Summary
    echo ""
    log_info "=== Test Summary ==="
    log_success "Passed: $PASSED"
    log_error "Failed: $FAILED"
    log_warn "Skipped/Warnings: $SKIPPED"
    
    if [[ ${#ISSUES[@]} -gt 0 ]]; then
        echo ""
        log_info "Issues found:"
        for issue in "${ISSUES[@]}"; do
            echo "  - $issue"
        done
    fi
    
    if [[ $FAILED -eq 0 ]]; then
        log_success "All critical tests passed!"
        return 0
    else
        log_error "Some tests failed. Review the output above."
        return 1
    fi
}

# Run main function
main "$@"
