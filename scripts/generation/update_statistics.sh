#!/bin/bash

# Automated Content Statistics Update Script
# This script can be used in CI/CD pipelines to automatically update content statistics

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
STATS_FILE="$PROJECT_ROOT/_data/content_statistics.yml"

# Colors for output (if terminal supports it)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

echo -e "${BLUE}🤖 Automated Content Statistics Update${NC}"
echo "========================================"

# Check if this is a CI environment
if [[ "${CI:-false}" == "true" ]]; then
    echo -e "${YELLOW}🔧 Running in CI environment${NC}"
    # Set git user for automated commits
    git config --global user.name "Content Statistics Bot"
    git config --global user.email "bot@it-journey.dev"
fi

# Store current statistics hash if file exists
CURRENT_HASH=""
if [[ -f "$STATS_FILE" ]]; then
    CURRENT_HASH=$(sha256sum "$STATS_FILE" | cut -d' ' -f1)
fi

# Generate new statistics
echo -e "${YELLOW}🔄 Generating updated statistics...${NC}"
if bash "$SCRIPT_DIR/generate_statistics.sh"; then
    echo -e "${GREEN}✅ Statistics generated successfully${NC}"
else
    echo -e "${RED}❌ Failed to generate statistics${NC}"
    exit 1
fi

# Check if statistics have changed
NEW_HASH=""
if [[ -f "$STATS_FILE" ]]; then
    NEW_HASH=$(sha256sum "$STATS_FILE" | cut -d' ' -f1)
fi

if [[ "$CURRENT_HASH" == "$NEW_HASH" ]]; then
    echo -e "${BLUE}ℹ️  No changes detected in content statistics${NC}"
    echo "Statistics are up to date."
    exit 0
fi

echo -e "${GREEN}📊 Content statistics have been updated${NC}"

# If running in CI, commit the changes
if [[ "${CI:-false}" == "true" ]]; then
    echo -e "${YELLOW}📝 Committing updated statistics...${NC}"
    
    cd "$PROJECT_ROOT"
    
    # Add the updated statistics file
    git add "$STATS_FILE"
    
    # Check if there are changes to commit
    if git diff --staged --quiet; then
        echo -e "${BLUE}ℹ️  No changes to commit${NC}"
    else
        # Create commit message with timestamp
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        COMMIT_MSG="🤖 Auto-update content statistics - $TIMESTAMP

- Total posts analyzed: $(yq '.total_posts' "$STATS_FILE" 2>/dev/null || echo 'N/A')
- Published posts: $(yq '.published' "$STATS_FILE" 2>/dev/null || echo 'N/A')
- Categories tracked: $(yq '.category_count' "$STATS_FILE" 2>/dev/null || echo 'N/A')

[skip ci]"
        
        git commit -m "$COMMIT_MSG"
        echo -e "${GREEN}✅ Statistics committed successfully${NC}"
        
        # Push if configured
        if [[ "${AUTO_PUSH:-false}" == "true" ]]; then
            echo -e "${YELLOW}🚀 Pushing changes...${NC}"
            git push origin HEAD
            echo -e "${GREEN}✅ Changes pushed to repository${NC}"
        fi
    fi
else
    echo -e "${BLUE}ℹ️  To commit these changes manually:${NC}"
    echo "   git add _data/content_statistics.yml"
    echo "   git commit -m '📊 Update content statistics'"
fi

echo "========================================"
echo -e "${GREEN}🎉 Content statistics update complete!${NC}"
