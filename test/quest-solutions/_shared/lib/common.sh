#!/usr/bin/env bash
# =============================================================================
# Quest Solutions Framework — Common Library
# Shared functions for all quest validation and solution scripts
# =============================================================================

# Colors (guard against re-sourcing)
if [[ -z "${QS_RED:-}" ]]; then
    readonly QS_RED='\033[0;31m'
    readonly QS_GREEN='\033[0;32m'
    readonly QS_YELLOW='\033[1;33m'
    readonly QS_BLUE='\033[0;34m'
    readonly QS_CYAN='\033[0;36m'
    readonly QS_BOLD='\033[1m'
    readonly QS_NC='\033[0m'
fi

# State
_QS_PASSED=0
_QS_FAILED=0
_QS_SKIPPED=0
_QS_WARNINGS=0

# ---- Logging ----

qs_info()    { echo -e "${QS_GREEN}[INFO]${QS_NC}  $*"; }
qs_warn()    { echo -e "${QS_YELLOW}[WARN]${QS_NC}  $*"; ((_QS_WARNINGS++)) || true; }
qs_error()   { echo -e "${QS_RED}[ERROR]${QS_NC} $*"; }
qs_step()    { echo -e "${QS_BLUE}[STEP]${QS_NC}  $*"; }
qs_header()  { echo -e "\n${QS_BOLD}${QS_CYAN}=== $* ===${QS_NC}\n"; }

# ---- Assertions ----

# Check if a condition is true
# Usage: qs_check "description" <command_or_expression>
qs_check() {
    local desc="$1"
    shift
    if eval "$@" > /dev/null 2>&1; then
        echo -e "  ${QS_GREEN}✅${QS_NC} $desc"
        ((_QS_PASSED++)) || true
        return 0
    else
        echo -e "  ${QS_RED}❌${QS_NC} $desc"
        ((_QS_FAILED++)) || true
        return 1
    fi
}

# Check with points
# Usage: qs_check_scored "description" <points> <command_or_expression>
qs_check_scored() {
    local desc="$1"
    local points="$2"
    shift 2
    if eval "$@" > /dev/null 2>&1; then
        echo -e "  ${QS_GREEN}✅${QS_NC} $desc (+${points})"
        ((_QS_PASSED++)) || true
        return 0
    else
        echo -e "  ${QS_RED}❌${QS_NC} $desc"
        ((_QS_FAILED++)) || true
        return 1
    fi
}

# Skip a check with reason
qs_skip() {
    local desc="$1"
    local reason="${2:-skipped}"
    echo -e "  ${QS_YELLOW}⏭️${QS_NC}  $desc — $reason"
    ((_QS_SKIPPED++)) || true
}

# ---- File & Directory Checks ----

qs_file_exists()    { [[ -f "$1" ]]; }
qs_dir_exists()     { [[ -d "$1" ]]; }
qs_file_executable() { [[ -x "$1" ]]; }
qs_file_contains()  { grep -q "$2" "$1" 2>/dev/null; }
qs_file_line_count() {
    local file="$1" min="$2"
    local count
    count=$(wc -l < "$file" 2>/dev/null | tr -d ' ')
    [[ "$count" -ge "$min" ]]
}

# ---- Platform Detection ----

qs_detect_platform() {
    case "$(uname -s)" in
        Darwin*)  echo "macos" ;;
        Linux*)   echo "linux" ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*) echo "windows" ;;
        *) echo "unknown" ;;
    esac
}

# ---- Summary ----

qs_summary() {
    local total=$((_QS_PASSED + _QS_FAILED + _QS_SKIPPED))
    echo ""
    echo -e "${QS_BOLD}─────────────────────────────────${QS_NC}"
    echo -e "${QS_BOLD}  Results: ${QS_GREEN}${_QS_PASSED} passed${QS_NC}, ${QS_RED}${_QS_FAILED} failed${QS_NC}, ${QS_YELLOW}${_QS_SKIPPED} skipped${QS_NC}"
    if [[ $_QS_WARNINGS -gt 0 ]]; then
        echo -e "  ${QS_YELLOW}Warnings: ${_QS_WARNINGS}${QS_NC}"
    fi
    echo -e "${QS_BOLD}─────────────────────────────────${QS_NC}"
    echo ""
    return $_QS_FAILED
}

# Reset counters (for running multiple validation blocks)
qs_reset() {
    _QS_PASSED=0
    _QS_FAILED=0
    _QS_SKIPPED=0
    _QS_WARNINGS=0
}

# ---- Quest Detection ----

# Detect challenge pattern from a quest markdown file
# Returns: "template" (Novice/Intermediate/Advanced) or "implementation" (Challenge 1-N + Boss Battle)
qs_detect_challenge_pattern() {
    local quest_file="$1"
    if grep -q '## .*Boss Battle' "$quest_file" 2>/dev/null; then
        echo "implementation"
    elif grep -qE '### .*Novice|### .*Intermediate|### .*Advanced' "$quest_file" 2>/dev/null; then
        echo "template"
    else
        echo "unknown"
    fi
}

# Extract quest slug from a markdown filepath
# e.g., /path/to/oh-my-zsh-terminal-enchantment.md → oh-my-zsh-terminal-enchantment
qs_quest_slug() {
    local filepath="$1"
    basename "$filepath" .md
}

# Extract level from a quest solutions path
# e.g., test/quest-solutions/0010/my-quest/ → 0010
qs_quest_level() {
    local path="$1"
    echo "$path" | grep -oE '[01]{4}' | head -1
}
