#!/usr/bin/env bash
# scripts/theme-audit.sh — thin wrapper for zer0-mistakes audit-consumer
#
# Resolves the auditor from the installed gem or a local sibling clone and
# delegates all arguments to it.  Supports the same flags as audit-consumer.
#
# Usage:
#   ./scripts/theme-audit.sh [--strict] [--format text|json|github] [--fix]
#   make theme-audit
#   make theme-audit-strict

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ---------------------------------------------------------------------------
# Locate the audit-consumer binary
# ---------------------------------------------------------------------------
AUDITOR=""

# 1. Try installed gem path via Bundler
if command -v bundle >/dev/null 2>&1; then
    GEM_PATH="$(cd "$REPO_ROOT" && bundle show jekyll-theme-zer0 2>/dev/null || true)"
    if [[ -n "$GEM_PATH" && -f "$GEM_PATH/scripts/bin/audit-consumer" ]]; then
        AUDITOR="$GEM_PATH/scripts/bin/audit-consumer"
    fi
fi

# 2. Fall back to sibling clone (monorepo / local dev)
if [[ -z "$AUDITOR" ]]; then
    SIBLING="${REPO_ROOT}/../zer0-mistakes/scripts/bin/audit-consumer"
    if [[ -f "$SIBLING" ]]; then
        AUDITOR="$(cd "$(dirname "$SIBLING")" && pwd)/$(basename "$SIBLING")"
    fi
fi

# 3. Fall back to work/theme-cache/
if [[ -z "$AUDITOR" ]]; then
    CACHE_AUDITOR="$REPO_ROOT/work/theme-cache/zer0-mistakes/scripts/bin/audit-consumer"
    if [[ -f "$CACHE_AUDITOR" ]]; then
        AUDITOR="$CACHE_AUDITOR"
    fi
fi

if [[ -z "$AUDITOR" ]]; then
    echo "ERROR: Cannot find audit-consumer. Options:" >&2
    echo "  1. Run 'bundle install' so the jekyll-theme-zer0 gem is available." >&2
    echo "  2. Clone zer0-mistakes as a sibling directory: ../zer0-mistakes/" >&2
    echo "  3. Cache the theme: git clone https://github.com/bamr87/zer0-mistakes work/theme-cache/zer0-mistakes" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Resolve theme path for the --theme-path argument
# ---------------------------------------------------------------------------
THEME_PATH="$(dirname "$(dirname "$(dirname "$AUDITOR")")")"

# ---------------------------------------------------------------------------
# Run the auditor
# ---------------------------------------------------------------------------
exec "$AUDITOR" \
    --consumer-path "$REPO_ROOT" \
    --theme-path    "$THEME_PATH" \
    --mode          remote_theme \
    "$@"
