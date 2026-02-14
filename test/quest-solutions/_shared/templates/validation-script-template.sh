#!/usr/bin/env bash
# =============================================================================
# [Quest Title] — Validation Script Template
# Quest: [Quest Title] — [Challenge/Phase Name]
# Purpose: [What this script validates]
# Usage: bash validate-[check-name].sh
# Expected: [Expected outcome, e.g., "8/8 checks pass"]
# =============================================================================
#
# Instructions for quest authors:
# 1. Copy this template to your quest's scripts/ directory
# 2. Rename to validate-<check-name>.sh
# 3. Replace placeholders with actual checks
# 4. Source the shared library for common functions
# =============================================================================

set -euo pipefail

# Source the shared validation library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_DIR="${SCRIPT_DIR}/../../../_shared"

if [[ -f "${FRAMEWORK_DIR}/lib/common.sh" ]]; then
    source "${FRAMEWORK_DIR}/lib/common.sh"
else
    # Fallback: minimal standalone mode
    echo "[WARN] Shared library not found — running in standalone mode"
    qs_check() {
        local desc="$1"; shift
        if eval "$@" > /dev/null 2>&1; then
            echo "✅ $desc"; return 0
        else
            echo "❌ $desc"; return 1
        fi
    }
    qs_header()  { echo "=== $* ==="; }
    qs_summary() { echo "Validation complete."; }
fi

# ---- Validation ----

qs_header "[Quest Title] — [Challenge/Phase] Validation"
echo "Date: $(date)"
echo ""

# --- Add your checks below ---

# Example: Check a file exists
# qs_check "Config file exists" qs_file_exists "$HOME/.some-config"

# Example: Check a file contains expected content
# qs_check "Theme is configured" qs_file_contains "$HOME/.zshrc" 'ZSH_THEME='

# Example: Check a command is available
# qs_check "Docker is installed" command -v docker

# Example: Check a directory exists
# qs_check "Project directory exists" qs_dir_exists "$HOME/my-project"

# --- End of checks ---

qs_summary
