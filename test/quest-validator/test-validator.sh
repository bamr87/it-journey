#!/bin/bash
# Docker-based Test Script for Quest Validator Framework
# Uses Docker containers instead of virtual environments

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Docker Quest Validator Framework - Test     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Ensure we're in the project root
cd "${PROJECT_ROOT}"

# Build the Docker image if needed
echo -e "${YELLOW}→ Building Docker image for quest validation...${NC}"
if ! docker-compose build quest-validator; then
    echo -e "${RED}❌ Failed to build Docker image${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker image built successfully${NC}"
echo ""

# Test 1: Validate single quest
echo -e "\n${GREEN}TEST 1: Validate Single Quest${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
docker-compose run --rm quest-validator \
    /opt/venv/bin/python /app/test/quest-validator/quest_validator.py \
    /app/pages/_quests/testing-quests-with-recurrisive-questing.md

# Test 2: Validate with verbose output
echo -e "\n${GREEN}TEST 2: Validate with Verbose Output${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
docker-compose run --rm quest-validator \
    /opt/venv/bin/python /app/test/quest-validator/quest_validator.py \
    /app/pages/_quests/testing-quests-with-recurrisive-questing.md \
    -v

# Test 3: Generate JSON report
echo -e "\n${GREEN}TEST 3: Generate JSON Report${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
REPORT_FILE="/app/test/quest-validator/test-report-docker.json"
docker-compose run --rm quest-validator \
    /opt/venv/bin/python /app/test/quest-validator/quest_validator.py \
    /app/pages/_quests/testing-quests-with-recurrisive-questing.md \
    --report "${REPORT_FILE}"

# Check if report was generated
docker-compose run --rm quest-validator \
    bash -c "if [ -f '${REPORT_FILE}' ]; then echo '✓ Report generated successfully'; cat '${REPORT_FILE}' | /opt/venv/bin/python -m json.tool; else echo '⚠ Report file not found'; fi"

# Test 4: Validate directory (if other quests exist)
echo -e "\n${GREEN}TEST 4: Validate Quest Directory${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Count quest files
QUEST_COUNT=$(docker-compose run --rm quest-validator \
    bash -c "find /app/pages/_quests -name '*.md' -not -name 'README.md' -not -name 'home.md' | wc -l | tr -d ' '")

echo "Found ${QUEST_COUNT} quest files to validate"

if [ "$QUEST_COUNT" -gt 0 ]; then
    docker-compose run --rm quest-validator \
        /opt/venv/bin/python /app/test/quest-validator/quest_validator.py \
        -d /app/pages/_quests/
else
    echo "No quest files to validate"
fi

# Test 5: Batch validation with report
echo -e "\n${GREEN}TEST 5: Batch Validation with Full Report${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
BATCH_REPORT="/app/test/quest-validator/batch-report-docker.json"
docker-compose run --rm quest-validator \
    /opt/venv/bin/python /app/test/quest-validator/quest_validator.py \
    -d /app/pages/_quests/ \
    --report "${BATCH_REPORT}"

# Display batch report summary
docker-compose run --rm quest-validator \
    bash -c "if [ -f '${BATCH_REPORT}' ]; then echo '📊 Batch Report Summary:'; /opt/venv/bin/python -c \"
import json
try:
    with open('${BATCH_REPORT}', 'r') as f:
        data = json.load(f)
    print(f'Total Quests: {data[\"total\"]}')
    print(f'Passed: {data[\"passed\"]} ✅')
    print(f'Failed: {data[\"failed\"]} ❌')
    print(f'Average Score: {data[\"average_score\"]:.1f}%')
    print(f'Total Errors: {data[\"total_errors\"]}')
    print(f'Total Warnings: {data[\"total_warnings\"]}')
except Exception as e:
    print(f'Error reading report: {e}')
\"; else echo 'Batch report not found'; fi"

# Summary
echo -e "\n${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        Docker Test Suite Complete ✓           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo "🐳 All Docker-based tests completed successfully!"
echo ""
echo "Framework Features Demonstrated:"
echo "  ✓ Docker containerized validation"
echo "  ✓ Single quest validation"
echo "  ✓ Verbose output mode"
echo "  ✓ JSON report generation"
echo "  ✓ Directory batch validation"
echo "  ✓ Cross-platform compatibility"
echo ""
echo "Next Steps:"
echo "  1. Run validator on all quests: docker-compose run --rm quest-validator /opt/venv/bin/python /app/test/quest-validator/quest_validator.py -d /app/pages/_quests/"
echo "  2. Integrate with CI/CD pipeline using Docker"
echo "  3. Create pre-commit hooks with Docker execution"
echo "  4. Set up automated quality reporting"
echo ""
