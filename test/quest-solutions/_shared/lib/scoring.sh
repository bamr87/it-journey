#!/usr/bin/env bash
# =============================================================================
# Quest Solutions Framework — Scoring Engine
# Provides point-based scoring and rank calculation for quest solutions
# =============================================================================

# Source common library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# ---- Scoring State ----

_QS_SCORE=0
_QS_MAX_SCORE=0

# ---- Scoring Functions ----

# Add points for a passing check
# Usage: qs_score "description" <points> <max_points> <command_or_expression>
qs_score() {
    local desc="$1"
    local points="$2"
    local max_points="${3:-$points}"
    shift 3

    _QS_MAX_SCORE=$((_QS_MAX_SCORE + max_points))

    if eval "$@" > /dev/null 2>&1; then
        echo -e "  ${QS_GREEN}✅${QS_NC} $desc (+${points}/${max_points})"
        _QS_SCORE=$((_QS_SCORE + points))
        ((_QS_PASSED++)) || true
        return 0
    else
        echo -e "  ${QS_RED}❌${QS_NC} $desc (0/${max_points})"
        ((_QS_FAILED++)) || true
        return 1
    fi
}

# Award partial credit
# Usage: qs_score_partial "description" <earned> <max_points>
qs_score_partial() {
    local desc="$1"
    local earned="$2"
    local max_points="$3"

    _QS_MAX_SCORE=$((_QS_MAX_SCORE + max_points))
    _QS_SCORE=$((_QS_SCORE + earned))

    if [[ $earned -eq $max_points ]]; then
        echo -e "  ${QS_GREEN}✅${QS_NC} $desc (+${earned}/${max_points})"
        ((_QS_PASSED++)) || true
    elif [[ $earned -gt 0 ]]; then
        echo -e "  ${QS_YELLOW}⚠️${QS_NC}  $desc (+${earned}/${max_points})"
        ((_QS_WARNINGS++)) || true
    else
        echo -e "  ${QS_RED}❌${QS_NC} $desc (0/${max_points})"
        ((_QS_FAILED++)) || true
    fi
}

# ---- Rank Determination ----

# Default rank thresholds (can be overridden per quest)
QS_RANK_LEGENDARY=95
QS_RANK_VICTORY=80
QS_RANK_GOOD_FIGHT=60

# Calculate percentage score
qs_score_percentage() {
    if [[ $_QS_MAX_SCORE -eq 0 ]]; then
        echo 0
        return
    fi
    echo $(( (_QS_SCORE * 100) / _QS_MAX_SCORE ))
}

# Get rank based on percentage
qs_rank() {
    local pct
    pct=$(qs_score_percentage)

    if [[ $pct -ge $QS_RANK_LEGENDARY ]]; then
        echo "LEGENDARY"
    elif [[ $pct -ge $QS_RANK_VICTORY ]]; then
        echo "VICTORY"
    elif [[ $pct -ge $QS_RANK_GOOD_FIGHT ]]; then
        echo "GOOD_FIGHT"
    else
        echo "KEEP_QUESTING"
    fi
}

# Get rank display with emoji
qs_rank_display() {
    local rank
    rank=$(qs_rank)

    case "$rank" in
        LEGENDARY)     echo "👑 LEGENDARY" ;;
        VICTORY)       echo "🏆 VICTORY" ;;
        GOOD_FIGHT)    echo "⚔️  Good Fight" ;;
        KEEP_QUESTING) echo "🛡️  Keep Questing" ;;
    esac
}

# ---- Score Summary ----

qs_score_summary() {
    local quest_name="${1:-Quest}"
    local pct
    pct=$(qs_score_percentage)
    local rank_display
    rank_display=$(qs_rank_display)

    echo ""
    echo -e "${QS_BOLD}${QS_CYAN}===========================================${QS_NC}"
    echo -e "${QS_BOLD}  ${quest_name}${QS_NC}"
    echo -e "${QS_BOLD}  FINAL SCORE: ${_QS_SCORE} / ${_QS_MAX_SCORE} (${pct}%)${QS_NC}"
    echo -e "${QS_BOLD}${QS_CYAN}===========================================${QS_NC}"
    echo -e "  ${rank_display}"
    echo ""

    if [[ $_QS_FAILED -gt 0 ]]; then
        echo -e "  ${QS_YELLOW}Review ${_QS_FAILED} failing check(s) above.${QS_NC}"
        echo ""
    fi
}

# Reset scoring (extends qs_reset from common.sh)
qs_score_reset() {
    qs_reset
    _QS_SCORE=0
    _QS_MAX_SCORE=0
}

# ---- JSON Report ----

# Generate a JSON report for CI consumption
qs_json_report() {
    local quest_name="${1:-Quest}"
    local quest_level="${2:-0000}"
    local pct
    pct=$(qs_score_percentage)
    local rank
    rank=$(qs_rank)

    cat <<EOF
{
  "quest": "${quest_name}",
  "level": "${quest_level}",
  "score": ${_QS_SCORE},
  "max_score": ${_QS_MAX_SCORE},
  "percentage": ${pct},
  "rank": "${rank}",
  "passed": ${_QS_PASSED},
  "failed": ${_QS_FAILED},
  "skipped": ${_QS_SKIPPED},
  "warnings": ${_QS_WARNINGS},
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
}
