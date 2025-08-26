#!/bin/bash

# Generate Content Statistics Script
# This script runs the Ruby statistics generator and provides feedback

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RUBY_SCRIPT="$SCRIPT_DIR/generate_statistics.rb"
OUTPUT_FILE="$SCRIPT_DIR/content_statistics.yml"

echo -e "${BLUE}📊 IT-Journey Content Statistics Generator${NC}"
echo "=================================================="

# Check if Ruby is available
if ! command -v ruby &> /dev/null; then
    echo -e "${RED}❌ Error: Ruby is not installed or not in PATH${NC}"
    echo "Please install Ruby to run the statistics generator."
    exit 1
fi

echo -e "${GREEN}✅ Ruby found: $(ruby --version)${NC}"

# Check if the Ruby script exists
if [[ ! -f "$RUBY_SCRIPT" ]]; then
    echo -e "${RED}❌ Error: Ruby script not found at $RUBY_SCRIPT${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Statistics generator script found${NC}"

# Check if posts directory exists
POSTS_DIR="$PROJECT_ROOT/pages/_posts"
if [[ ! -d "$POSTS_DIR" ]]; then
    echo -e "${RED}❌ Error: Posts directory not found at $POSTS_DIR${NC}"
    exit 1
fi

POST_COUNT=$(find "$POSTS_DIR" -name "*.md" -type f | grep -v "2000-01-01-index.md" | wc -l)
echo -e "${GREEN}✅ Found $POST_COUNT posts to analyze${NC}"

# Run the Ruby script
echo -e "${YELLOW}🔄 Generating statistics...${NC}"
if ruby "$RUBY_SCRIPT"; then
    echo -e "${GREEN}✅ Statistics generated successfully!${NC}"
else
    echo -e "${RED}❌ Error: Failed to generate statistics${NC}"
    exit 1
fi

# Check if output file was created
if [[ -f "$OUTPUT_FILE" ]]; then
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo -e "${GREEN}✅ Output file created: $OUTPUT_FILE ($FILE_SIZE)${NC}"
    
    # Show a preview of the generated statistics
    echo -e "${BLUE}📋 Statistics Preview:${NC}"
    echo "------------------------"
    if command -v yq &> /dev/null; then
        echo "Total Posts: $(yq '.total_posts' "$OUTPUT_FILE")"
        echo "Published: $(yq '.published' "$OUTPUT_FILE")"
        echo "Categories: $(yq '.category_count' "$OUTPUT_FILE")"
        echo "Date Range: $(yq '.date_range.earliest' "$OUTPUT_FILE")-$(yq '.date_range.latest' "$OUTPUT_FILE")"
    else
        # Fallback to grep if yq is not available
        echo "Preview of generated data:"
        head -20 "$OUTPUT_FILE" | grep -E "^(total_posts|published|category_count):" || true
    fi
else
    echo -e "${RED}❌ Error: Output file was not created${NC}"
    exit 1
fi

echo "=========================="
echo -e "${GREEN}🎉 Content statistics generation complete!${NC}"
echo ""
echo "📝 To use these statistics in your Jekyll site:"
echo "   1. The data is now available in _data/content_statistics.yml"
echo "   2. Use {% include content_statistics/simple.html %} for basic display"
echo "   3. Use {% include content_statistics/summary.html %} for detailed cards"
echo "   4. Use {% include content_statistics/detailed.html %} for full analysis"
echo ""
echo "🔄 To regenerate statistics, run this script again:"
echo "   bash _data/generate_statistics.sh"
