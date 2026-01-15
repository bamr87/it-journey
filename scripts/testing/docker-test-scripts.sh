#!/bin/bash
#
# Docker-based Script Testing
# Tests all scripts in an isolated Docker container
#
# Usage: ./scripts/testing/docker-test-scripts.sh [OPTIONS]
#
# Options:
#   --build        Rebuild Docker image
#   --verbose      Show detailed output
#   --category     Test specific category only

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

BUILD=false
VERBOSE=false
CATEGORY=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --build)
            BUILD=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --category)
            CATEGORY="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

# Build Docker image if needed
if [[ "$BUILD" == "true" ]] || ! docker images | grep -q "it-journey-scripts-test"; then
    log_info "Building Docker test image..."
    docker build -t it-journey-scripts-test -f - "$PROJECT_ROOT" << 'EOF'
FROM ruby:3.2.3

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    bash \
    shellcheck \
    jq \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project
COPY . /app

# Install Python dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r scripts/validation/requirements.txt 2>/dev/null || true

# Install Ruby dependencies
RUN bundle install || true

CMD ["/bin/bash"]
EOF
    log_success "Docker image built"
fi

# Run tests in container
log_info "Running script tests in Docker container..."

VERBOSE_FLAG=""
if [[ "$VERBOSE" == "true" ]]; then
    VERBOSE_FLAG="--verbose"
fi

CATEGORY_FLAG=""
if [[ -n "$CATEGORY" ]]; then
    CATEGORY_FLAG="--category $CATEGORY"
fi

docker run --rm -it \
    -v "$PROJECT_ROOT:/app" \
    -w /app \
    it-journey-scripts-test \
    bash -c "
        chmod +x scripts/testing/test-all-scripts.sh
        ./scripts/testing/test-all-scripts.sh $VERBOSE_FLAG $CATEGORY_FLAG
    "

log_success "Docker tests complete"
