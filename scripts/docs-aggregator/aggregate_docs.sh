#!/usr/bin/env bash
# File: aggregate_docs.sh
# Description: Orchestrator for the docs aggregation pipeline
# Author: IT-Journey Team
# Created: 2025-01-27
# Version: 1.0.0
#
# Usage: ./aggregate_docs.sh [--config path] [--clean]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CONFIG="${SCRIPT_DIR}/docs_config.yml"
WORK_DIR="${REPO_ROOT}/work/docs-aggregator"
OUTPUT_DIR="${REPO_ROOT}/pages/_docs"
NAV_OUTPUT="${REPO_ROOT}/_data/navigation/docs_aggregated.yml"
CLEAN=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Aggregate external documentation into the it-journey _docs collection.

Options:
  --config PATH   Path to docs_config.yml (default: ${CONFIG})
  --clean         Remove work/ staging area before running
  --help          Show this help message

Pipeline:
  1. aggregate.py  — Clone repos and extract documentation files
  2. transform.py  — Add Jekyll frontmatter, rewrite links, stage output
  3. Navigation    — Generate sidebar navigation fragment

Output:
  pages/_docs/<category>/<source>/   — Transformed Jekyll pages (committed)
  work/docs-aggregator/              — Staging area (gitignored)
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --config) CONFIG="$2"; shift 2 ;;
        --clean)  CLEAN=true; shift ;;
        --help)   usage; exit 0 ;;
        *) log_error "Unknown option: $1"; usage; exit 1 ;;
    esac
done

# Validate
if [[ ! -f "$CONFIG" ]]; then
    log_error "Config not found: $CONFIG"
    exit 1
fi

command -v python3 >/dev/null 2>&1 || { log_error "python3 is required"; exit 1; }
python3 -c "import yaml" 2>/dev/null || { log_error "PyYAML is required: pip3 install pyyaml"; exit 1; }
command -v git >/dev/null 2>&1 || { log_error "git is required"; exit 1; }

# Clean if requested
if [[ "$CLEAN" == true ]] && [[ -d "$WORK_DIR" ]]; then
    log_warn "Cleaning work directory: $WORK_DIR"
    rm -rf "$WORK_DIR"
fi

# Setup work directory
mkdir -p "${WORK_DIR}"/{repos,raw}
log_info "Work directory: $WORK_DIR"

# Step 1: Aggregate
log_info "=== Step 1: Aggregating documentation ==="
python3 "${SCRIPT_DIR}/aggregate.py" \
    --config "$CONFIG" \
    --work-dir "$WORK_DIR"

# Step 2: Transform
log_info "=== Step 2: Transforming to Jekyll format ==="
python3 "${SCRIPT_DIR}/transform.py" \
    --work-dir "$WORK_DIR" \
    --output-dir "$OUTPUT_DIR" \
    --nav-output "$NAV_OUTPUT"

# Step 3: Summary
log_info "=== Pipeline Complete ==="
if [[ -d "$OUTPUT_DIR" ]]; then
    file_count=$(find "$OUTPUT_DIR" -name "*.md" -path "*/wargames/*" 2>/dev/null | wc -l | tr -d ' ')
    log_info "Aggregated files: $file_count"
fi

if [[ -f "$NAV_OUTPUT" ]]; then
    log_info "Navigation fragment: $NAV_OUTPUT"
    log_warn "To integrate navigation, merge $NAV_OUTPUT into _data/navigation/docs.yml"
fi

# Cleanup temp files (keep repos for incremental updates)
rm -rf "${WORK_DIR}/raw" 2>/dev/null || true

log_info "Done. Run 'bundle exec jekyll build' to verify the site builds."
