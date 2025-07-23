#!/bin/bash
#
# @file scripts/development/build/build-site.sh
# @description Unified build script for IT-Journey projects
# @author IT-Journey Team <team@it-journey.org>
# @created 2025-07-07
# @lastModified 2025-07-07
# @version 1.0.0
#
# @relatedIssues 
#   - Script consolidation: Create unified build interface
#
# @relatedEvolutions
#   - v1.0.0: Initial unified build script supporting multiple project types
#
# @dependencies
#   - jekyll: For Jekyll/Ruby projects
#   - npm/node: For Node.js projects
#   - docker: For containerized builds
#
# @changelog
#   - 2025-07-07: Initial creation with multi-project support - ITJ
#
# @usage ./scripts/development/build/build-site.sh [--type TYPE] [--env ENV]
# @notes Automatically detects project type and builds accordingly
#

set -euo pipefail

# IT-Journey Development Principles Implementation:
# DFF: Comprehensive error handling and build validation
# DRY: Single build script for all project types
# KIS: Simple interface with intelligent defaults
# COLAB: Consistent build process across projects

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Configuration
PROJECT_TYPE="auto"
BUILD_ENV="development"
OUTPUT_DIR=""
CLEAN_BUILD=false
SERVE_AFTER_BUILD=false
DOCKER_BUILD=false
VERBOSE=false

# Show help message
show_help() {
    cat << EOF
🔨 IT-Journey Unified Build Script

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --type TYPE             Project type (auto, jekyll, node, docker) [default: auto]
    --env ENV              Build environment (development, production) [default: development]
    --output DIR           Output directory (overrides defaults)
    --clean                Clean build artifacts before building
    --serve                Start development server after build
    --docker               Build using Docker container
    --verbose              Enable verbose output
    --help                 Show this help message

PROJECT TYPES:
    auto                   Automatically detect project type
    jekyll                 Jekyll static site generator
    node                   Node.js application
    docker                 Docker containerized build

ENVIRONMENTS:
    development           Development build with debugging enabled
    production            Production build optimized for deployment

EXAMPLES:
    $0                              # Auto-detect and build for development
    $0 --type jekyll --env production  # Production Jekyll build
    $0 --clean --serve             # Clean build and start dev server
    $0 --docker --env production   # Docker production build

Following IT-Journey Principles:
    DFF: Comprehensive build validation and error recovery
    DRY: Single build interface for all project types
    KIS: Intelligent defaults with simple overrides
    COLAB: Consistent build experience across projects
EOF
}

# Logging functions
log() {
    echo -e "${GREEN}[BUILD]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --type)
                PROJECT_TYPE="$2"
                shift 2
                ;;
            --env)
                BUILD_ENV="$2"
                shift 2
                ;;
            --output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            --clean)
                CLEAN_BUILD=true
                shift
                ;;
            --serve)
                SERVE_AFTER_BUILD=true
                shift
                ;;
            --docker)
                DOCKER_BUILD=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                error "Unknown option: $1. Use --help for usage information."
                ;;
        esac
    done
}

# Auto-detect project type
detect_project_type() {
    if [[ "$PROJECT_TYPE" != "auto" ]]; then
        return 0
    fi
    
    log "Auto-detecting project type..."
    
    if [[ -f "_config.yml" ]] && [[ -f "Gemfile" ]]; then
        PROJECT_TYPE="jekyll"
        log "Detected Jekyll project"
    elif [[ -f "package.json" ]]; then
        PROJECT_TYPE="node"
        log "Detected Node.js project"
    elif [[ -f "Dockerfile" ]]; then
        PROJECT_TYPE="docker"
        log "Detected Docker project"
    else
        error "Unable to detect project type. Please specify with --type"
    fi
}

# Set default output directory based on project type
set_output_directory() {
    if [[ -n "$OUTPUT_DIR" ]]; then
        return 0
    fi
    
    case $PROJECT_TYPE in
        jekyll)
            OUTPUT_DIR="_site"
            ;;
        node)
            OUTPUT_DIR="dist"
            ;;
        docker)
            OUTPUT_DIR="build"
            ;;
        *)
            OUTPUT_DIR="build"
            ;;
    esac
    
    info "Using output directory: $OUTPUT_DIR"
}

# Clean build artifacts
clean_build_artifacts() {
    if [[ "$CLEAN_BUILD" == false ]]; then
        return 0
    fi
    
    log "Cleaning build artifacts..."
    
    # Remove output directory
    if [[ -d "$OUTPUT_DIR" ]]; then
        rm -rf "$OUTPUT_DIR"
        info "Removed $OUTPUT_DIR"
    fi
    
    # Project-specific cleanup
    case $PROJECT_TYPE in
        jekyll)
            [[ -d ".jekyll-cache" ]] && rm -rf ".jekyll-cache"
            [[ -d ".sass-cache" ]] && rm -rf ".sass-cache"
            ;;
        node)
            [[ -d "node_modules/.cache" ]] && rm -rf "node_modules/.cache"
            ;;
    esac
    
    log "Clean complete"
}

# Build Jekyll project
build_jekyll() {
    log "Building Jekyll project for $BUILD_ENV environment..."
    
    # Check dependencies
    if ! command -v bundle >/dev/null 2>&1; then
        error "Bundler not found. Please install with: gem install bundler"
    fi
    
    # Install dependencies if needed
    if [[ ! -d "vendor/bundle" ]]; then
        log "Installing Ruby dependencies..."
        bundle install
    fi
    
    # Build command
    local build_cmd="bundle exec jekyll build"
    
    # Add environment-specific options
    if [[ "$BUILD_ENV" == "production" ]]; then
        export JEKYLL_ENV=production
        build_cmd+=" --config _config.yml"
    else
        build_cmd+=" --config _config_dev.yml,_config.yml"
    fi
    
    # Add output directory
    build_cmd+=" --destination $OUTPUT_DIR"
    
    # Add verbose flag if requested
    [[ "$VERBOSE" == true ]] && build_cmd+=" --verbose"
    
    log "Running: $build_cmd"
    eval "$build_cmd"
    
    log "Jekyll build complete"
    
    # Start development server if requested
    if [[ "$SERVE_AFTER_BUILD" == true ]] && [[ "$BUILD_ENV" == "development" ]]; then
        log "Starting Jekyll development server..."
        bundle exec jekyll serve --config _config_dev.yml,_config.yml --livereload
    fi
}

# Build Node.js project
build_node() {
    log "Building Node.js project for $BUILD_ENV environment..."
    
    # Check dependencies
    if ! command -v npm >/dev/null 2>&1; then
        error "npm not found. Please install Node.js"
    fi
    
    # Install dependencies if needed
    if [[ ! -d "node_modules" ]]; then
        log "Installing Node.js dependencies..."
        npm install
    fi
    
    # Build command
    local build_cmd
    if [[ "$BUILD_ENV" == "production" ]]; then
        build_cmd="npm run build:prod"
    else
        build_cmd="npm run build"
    fi
    
    # Check if build script exists
    if ! npm run --silent 2>/dev/null | grep -q "build"; then
        warn "No build script found in package.json"
        return 0
    fi
    
    log "Running: $build_cmd"
    eval "$build_cmd"
    
    log "Node.js build complete"
    
    # Start development server if requested
    if [[ "$SERVE_AFTER_BUILD" == true ]] && [[ "$BUILD_ENV" == "development" ]]; then
        log "Starting development server..."
        npm start
    fi
}

# Build Docker project
build_docker() {
    log "Building Docker project for $BUILD_ENV environment..."
    
    # Check dependencies
    if ! command -v docker >/dev/null 2>&1; then
        error "Docker not found. Please install Docker"
    fi
    
    # Determine Dockerfile
    local dockerfile="Dockerfile"
    if [[ "$BUILD_ENV" == "production" ]] && [[ -f "Dockerfile.prod" ]]; then
        dockerfile="Dockerfile.prod"
    elif [[ "$BUILD_ENV" == "development" ]] && [[ -f "Dockerfile.dev" ]]; then
        dockerfile="Dockerfile.dev"
    fi
    
    # Build image
    local image_tag="it-journey:$BUILD_ENV"
    log "Building Docker image: $image_tag"
    
    docker build -f "$dockerfile" -t "$image_tag" .
    
    log "Docker build complete: $image_tag"
    
    # Run container if requested
    if [[ "$SERVE_AFTER_BUILD" == true ]]; then
        log "Starting Docker container..."
        docker run -p 4000:4000 "$image_tag"
    fi
}

# Validate build output
validate_build() {
    log "Validating build output..."
    
    if [[ ! -d "$OUTPUT_DIR" ]]; then
        error "Build output directory not found: $OUTPUT_DIR"
    fi
    
    # Check if output directory has content
    if [[ -z "$(ls -A "$OUTPUT_DIR")" ]]; then
        error "Build output directory is empty: $OUTPUT_DIR"
    fi
    
    # Project-specific validation
    case $PROJECT_TYPE in
        jekyll)
            if [[ ! -f "$OUTPUT_DIR/index.html" ]]; then
                warn "No index.html found in Jekyll build output"
            fi
            ;;
        node)
            info "Node.js build validation passed"
            ;;
    esac
    
    log "Build validation passed"
}

# Show build summary
show_build_summary() {
    log "🎉 Build Summary"
    info "Project Type: $PROJECT_TYPE"
    info "Environment: $BUILD_ENV"
    info "Output Directory: $OUTPUT_DIR"
    
    if [[ -d "$OUTPUT_DIR" ]]; then
        local file_count
        file_count=$(find "$OUTPUT_DIR" -type f | wc -l | tr -d ' ')
        info "Generated Files: $file_count"
        
        if command -v du >/dev/null 2>&1; then
            local size
            size=$(du -sh "$OUTPUT_DIR" | cut -f1)
            info "Total Size: $size"
        fi
    fi
    
    echo
    log "Next steps:"
    info "1. Review build output in $OUTPUT_DIR"
    info "2. Test the built application"
    info "3. Deploy using appropriate deployment scripts"
    
    if [[ "$BUILD_ENV" == "development" ]]; then
        info "4. Use --serve to start a development server"
    fi
}

# Main execution function
main() {
    log "🔨 IT-Journey Unified Build Script"
    
    parse_arguments "$@"
    detect_project_type
    set_output_directory
    clean_build_artifacts
    
    # Execute build based on project type
    case $PROJECT_TYPE in
        jekyll)
            build_jekyll
            ;;
        node)
            build_node
            ;;
        docker)
            build_docker
            ;;
        *)
            error "Unsupported project type: $PROJECT_TYPE"
            ;;
    esac
    
    # Validate and summarize if not serving
    if [[ "$SERVE_AFTER_BUILD" == false ]]; then
        validate_build
        show_build_summary
    fi
    
    log "✅ Build process complete!"
}

# Execute main function with all arguments
main "$@"
