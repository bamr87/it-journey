#!/bin/bash

# Generate Contributor Statistics Script
# Runs the Ruby contributor stats generator and provides feedback

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
RUBY_SCRIPT="$SCRIPT_DIR/generate_contributor_stats.rb"
CONTRIBUTORS_DIR="$PROJECT_ROOT/_data/contributors"

echo -e "${BLUE}🧙 IT-Journey Contributor Stats Generator${NC}"
echo "=================================================="

# Check dependencies
if ! command -v ruby &> /dev/null; then
    echo -e "${RED}❌ Error: Ruby is not installed or not in PATH${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Ruby found: $(ruby --version)${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Error: Git is not installed or not in PATH${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Git found: $(git --version)${NC}"

if [[ ! -f "$RUBY_SCRIPT" ]]; then
    echo -e "${RED}❌ Error: Ruby script not found at $RUBY_SCRIPT${NC}"
    exit 1
fi

if [[ ! -d "$CONTRIBUTORS_DIR" ]]; then
    echo -e "${RED}❌ Error: Contributors directory not found at $CONTRIBUTORS_DIR${NC}"
    exit 1
fi

# Parse arguments
USERNAME=""
ALL_MODE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --all)
            ALL_MODE=true
            shift
            ;;
        --username)
            USERNAME="$2"
            shift 2
            ;;
        *)
            USERNAME="$1"
            shift
            ;;
    esac
done

# Run generator
if [[ "$ALL_MODE" == "true" ]]; then
    CONTRIBUTOR_COUNT=$(find "$CONTRIBUTORS_DIR" -name "*.yml" ! -name "_*" | wc -l | tr -d ' ')
    echo -e "${YELLOW}🔄 Generating stats for all $CONTRIBUTOR_COUNT contributor(s)...${NC}"
    ruby "$RUBY_SCRIPT" --all
elif [[ -n "$USERNAME" ]]; then
    if [[ ! -f "$CONTRIBUTORS_DIR/$USERNAME.yml" ]]; then
        echo -e "${RED}❌ Error: Contributor file not found: $CONTRIBUTORS_DIR/$USERNAME.yml${NC}"
        exit 1
    fi
    echo -e "${YELLOW}🔄 Generating stats for contributor: $USERNAME${NC}"
    ruby "$RUBY_SCRIPT" "$USERNAME"
else
    echo -e "${RED}❌ Error: No username specified${NC}"
    echo ""
    echo "Usage:"
    echo "  bash generate_contributor_stats.sh <username>"
    echo "  bash generate_contributor_stats.sh --username <username>"
    echo "  bash generate_contributor_stats.sh --all"
    exit 1
fi

echo ""
echo "=========================="
echo -e "${GREEN}🎉 Contributor stats generation complete!${NC}"
