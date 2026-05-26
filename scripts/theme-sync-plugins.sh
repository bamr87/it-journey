#!/usr/bin/env bash
# scripts/theme-sync-plugins.sh — thin wrapper for zer0-mistakes sync-plugins
#
# Resolves the sync-plugins binary from the installed gem or a local sibling
# clone and delegates all arguments to it.  Supports the same flags as
# sync-plugins.
#
# Usage:
#   ./scripts/theme-sync-plugins.sh [--plugins required|optional|all|<name>]
#                                    [--dry-run] [--force] [--format text|github]
#   make theme-sync-plugins          # install/update required plugins
#   make theme-sync-plugins-all      # install/update all plugins
#   make theme-sync-plugins-preview  # dry-run for all plugins

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ---------------------------------------------------------------------------
# Locate the sync-plugins binary
# ---------------------------------------------------------------------------
SYNCER=""

# 1. Try installed gem path via Bundler
if command -v bundle >/dev/null 2>&1; then
    GEM_PATH="$(cd "$REPO_ROOT" && bundle show jekyll-theme-zer0 2>/dev/null || true)"
    if [[ -n "$GEM_PATH" && -f "$GEM_PATH/scripts/bin/sync-plugins" ]]; then
        SYNCER="$GEM_PATH/scripts/bin/sync-plugins"
    fi
fi

# 2. Fall back to sibling clone (monorepo / local dev)
if [[ -z "$SYNCER" ]]; then
    SIBLING="${REPO_ROOT}/../zer0-mistakes/scripts/bin/sync-plugins"
    if [[ -f "$SIBLING" ]]; then
        SYNCER="$(cd "$(dirname "$SIBLING")" && pwd)/$(basename "$SIBLING")"
    fi
fi

# 3. Fall back to work/theme-cache/
if [[ -z "$SYNCER" ]]; then
    CACHE_SYNCER="$REPO_ROOT/work/theme-cache/zer0-mistakes/scripts/bin/sync-plugins"
    if [[ -f "$CACHE_SYNCER" ]]; then
        SYNCER="$CACHE_SYNCER"
    fi
fi

if [[ -z "$SYNCER" ]]; then
    echo "ERROR: Cannot find sync-plugins binary. Options:" >&2
    echo "  1. Run 'bundle install' so the jekyll-theme-zer0 gem is available." >&2
    echo "  2. Clone zer0-mistakes as a sibling directory: ../zer0-mistakes/" >&2
    echo "  3. Cache the theme: git clone https://github.com/bamr87/zer0-mistakes work/theme-cache/zer0-mistakes" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Resolve theme path for the --theme-path argument
# ---------------------------------------------------------------------------
THEME_PATH="$(dirname "$(dirname "$(dirname "$SYNCER")")")"

# ---------------------------------------------------------------------------
# Run the syncer
# ---------------------------------------------------------------------------
exec "$SYNCER" \
    --consumer-path "$REPO_ROOT" \
    --theme-path    "$THEME_PATH" \
    "$@"
