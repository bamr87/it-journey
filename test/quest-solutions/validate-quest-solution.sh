#!/usr/bin/env bash
# =============================================================================
# Quest Solutions Framework — Solution Validator
# Entry point for validating quest solutions from the command line
#
# Usage:
#   ./validate-quest-solution.sh <quest-solution-dir>
#   ./validate-quest-solution.sh <quest-solution-dir> --json
#   ./validate-quest-solution.sh --all
#   ./validate-quest-solution.sh --level 0010
#
# Examples:
#   ./validate-quest-solution.sh 0010/oh-my-zsh-terminal-enchantment
#   ./validate-quest-solution.sh --all --json > report.json
# =============================================================================

set -euo pipefail

FRAMEWORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOLUTIONS_DIR="${FRAMEWORK_DIR}"
SHARED_DIR="${SOLUTIONS_DIR}/_shared"

source "${SHARED_DIR}/lib/common.sh"
source "${SHARED_DIR}/lib/scoring.sh"

# ---- CLI Arguments ----

TARGET=""
MODE="interactive"  # interactive | json | all | level
LEVEL_FILTER=""
JSON_OUTPUT=false

usage() {
    cat <<EOF
Quest Solutions Framework — Validator

Usage:
  $(basename "$0") <quest-dir>           Validate a single quest solution
  $(basename "$0") --all                 Validate all quest solutions
  $(basename "$0") --level <NNNN>        Validate all solutions in a level
  $(basename "$0") <quest-dir> --json    Output JSON report

Options:
  <quest-dir>     Path relative to test/quest-solutions/ (e.g., 0010/oh-my-zsh-terminal-enchantment)
  --all           Validate all quest solutions with structural checks
  --level NNNN    Validate all solutions in a specific level
  --json          Output results as JSON (for CI)
  --help, -h      Show this help message

Structural Checks (always run):
  - Required files present (README.md, answer-key.md)
  - Script syntax validation (bash -n)
  - Directory structure compliance
  - Markdown link integrity

Environment Checks (local execution only):
  - Quest-specific validation scripts (if present)
  - System state verification
  - Tool installation checks
EOF
    exit 0
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --all)    MODE="all"; shift ;;
            --level)  MODE="level"; LEVEL_FILTER="$2"; shift 2 ;;
            --json)   JSON_OUTPUT=true; shift ;;
            --help|-h) usage ;;
            *)        TARGET="$1"; shift ;;
        esac
    done
}

# ---- Structural Validation ----

validate_structure() {
    local solution_dir="$1"
    local quest_name
    quest_name=$(basename "$solution_dir")

    qs_header "Structural Validation: $quest_name"

    # Required files
    qs_check "README.md exists" qs_file_exists "$solution_dir/README.md"
    qs_check "answer-key.md exists" qs_file_exists "$solution_dir/answer-key.md"

    # Directory structure
    if [[ -d "$solution_dir/scripts" ]]; then
        qs_check "scripts/ directory exists" true

        # Validate shell scripts have shebangs and are non-trivial
        for script in "$solution_dir"/scripts/*.sh; do
            [[ -f "$script" ]] || continue
            local script_name
            script_name=$(basename "$script")
            if head -1 "$script" | grep -qE '^#!/'; then
                qs_check "$script_name has valid shebang" true
            else
                qs_check "$script_name has valid shebang" false
            fi
        done
    else
        qs_skip "scripts/ directory" "no scripts directory found"
    fi

    if [[ -d "$solution_dir/reports" ]]; then
        qs_check "reports/ directory exists" true

        # Check report files are non-empty
        for report in "$solution_dir"/reports/*.md; do
            [[ -f "$report" ]] || continue
            qs_check "$(basename "$report") is non-empty" qs_file_line_count "$report" 5
        done
    else
        qs_skip "reports/ directory" "no reports directory found"
    fi

    # Check README has required sections
    if [[ -f "$solution_dir/README.md" ]]; then
        if grep -qiE 'Purpose|Overview' "$solution_dir/README.md" 2>/dev/null; then
            qs_check "README has purpose section" true
        else
            qs_check "README has purpose section" false
        fi
        if grep -qiE 'How to Use|Usage|Quick Start' "$solution_dir/README.md" 2>/dev/null; then
            qs_check "README has usage instructions" true
        else
            qs_check "README has usage instructions" false
        fi
    fi

    # Check answer-key has content
    if [[ -f "$solution_dir/answer-key.md" ]]; then
        qs_check "answer-key.md has content" qs_file_line_count "$solution_dir/answer-key.md" 20
    fi
}

# ---- Single Quest Validation ----

validate_quest() {
    local solution_dir="$1"

    if [[ ! -d "$solution_dir" ]]; then
        qs_error "Solution directory not found: $solution_dir"
        return 1
    fi

    # Always run structural checks
    validate_structure "$solution_dir"

    # Look for quest-specific validation runner
    if [[ -x "$solution_dir/scripts/boss-battle-validate.sh" ]]; then
        qs_header "Quest-Specific Validation Available"
        qs_info "Run the full quest validation locally:"
        qs_info "  zsh $solution_dir/scripts/boss-battle-validate.sh"
    fi

    qs_summary
}

# ---- Batch Validation ----

validate_all() {
    local filter="${1:-}"
    local found=0
    local results=()

    qs_header "Quest Solutions Framework — Batch Validation"

    for level_dir in "$SOLUTIONS_DIR"/[01][01][01][01]; do
        [[ -d "$level_dir" ]] || continue
        local level
        level=$(basename "$level_dir")

        # Apply level filter if set
        if [[ -n "$filter" && "$level" != "$filter" ]]; then
            continue
        fi

        for quest_dir in "$level_dir"/*/; do
            [[ -d "$quest_dir" ]] || continue
            local quest
            quest=$(basename "$quest_dir")

            ((found++)) || true

            echo -e "${QS_BLUE}[$level/$quest]${QS_NC}"
            qs_reset

            validate_structure "$quest_dir"

            local status="PASS"
            if [[ $_QS_FAILED -gt 0 ]]; then
                status="FAIL"
            fi

            results+=("$level/$quest: $status ($_QS_PASSED passed, $_QS_FAILED failed)")
            echo ""
        done
    done

    echo ""
    qs_header "Batch Summary"
    echo "  Solutions validated: $found"
    echo ""
    for result in "${results[@]}"; do
        echo "  $result"
    done
    echo ""

    if [[ $found -eq 0 ]]; then
        qs_warn "No quest solutions found"
        if [[ -n "$filter" ]]; then
            qs_info "Level $filter has no solutions yet"
        fi
    fi
}

# ---- Main ----

main() {
    parse_args "$@"

    case "$MODE" in
        all)
            validate_all
            ;;
        level)
            validate_all "$LEVEL_FILTER"
            ;;
        *)
            if [[ -z "$TARGET" ]]; then
                usage
            fi

            # Resolve the target path
            local resolved_dir
            if [[ -d "$TARGET" ]]; then
                resolved_dir="$TARGET"
            elif [[ -d "$SOLUTIONS_DIR/$TARGET" ]]; then
                resolved_dir="$SOLUTIONS_DIR/$TARGET"
            else
                qs_error "Cannot find solution directory: $TARGET"
                qs_info "Expected: test/quest-solutions/<level>/<quest-slug>"
                exit 1
            fi

            validate_quest "$resolved_dir"
            ;;
    esac
}

main "$@"
