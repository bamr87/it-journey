#!/bin/bash
# extract-script.sh
# Extracts the automation script from the zer0.md markdown file
# Usage: ./extract-script.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
MARKDOWN_FILE="$PROJECT_ROOT/zer0.md"
OUTPUT_SCRIPT="$SCRIPT_DIR/zer0-to-hero-extracted.sh"

echo "🔧 Extracting automation script from zer0.md..."

if [[ ! -f "$MARKDOWN_FILE" ]]; then
    echo "❌ Error: zer0.md not found at $MARKDOWN_FILE"
    exit 1
fi

# Extract the script between the specific bash code block markers
# Looking for the complete automation script in the markdown
awk '
    /^```bash$/ && /zer0-to-hero-complete.sh/ { in_script=1; next }
    /^```$/ && in_script { in_script=0; next }
    in_script { print }
' "$MARKDOWN_FILE" > "$OUTPUT_SCRIPT"

# Verify we extracted something
if [[ ! -s "$OUTPUT_SCRIPT" ]]; then
    echo "❌ Error: No script content extracted from markdown"
    exit 1
fi

# Make it executable
chmod +x "$OUTPUT_SCRIPT"

echo "✅ Script extracted to: $OUTPUT_SCRIPT"
echo "📏 Script size: $(wc -l < "$OUTPUT_SCRIPT") lines"
echo ""
echo "🚀 You can now run the extracted script:"
echo "   $OUTPUT_SCRIPT"
echo ""
echo "Or test it first:"
echo "   cat $OUTPUT_SCRIPT | head -20"
