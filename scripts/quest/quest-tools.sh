#!/usr/bin/env bash
# quest-tools.sh
# Wrapper script to run quest tools via Docker

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

usage() {
    cat <<EOF
Usage: $0 <command> [options]

Quest management tools running in Docker containers.

Commands:
    generate <level> <slug> "<title>" [options]
        Generate a new placeholder quest
        Example: $0 generate 0110 sql-basics "SQL Basics" --difficulty medium

    validate
        Validate the quest network integrity
        Example: $0 validate

    build
        Build/rebuild the Docker images
        Example: $0 build

    shell
        Open a shell in the Jekyll container
        Example: $0 shell

Options for generate:
    --difficulty    Quest difficulty: easy, medium, hard, epic
    --type          Quest type: main_quest, side_quest, bonus_quest
    --time          Estimated time (e.g., "30-45 minutes")
    --tech          Primary technology
    --skill         Skill focus
    --dry-run       Preview without creating files

Examples:
    # Generate a quest
    $0 generate 0110 database-design "Database Design Fundamentals"

    # Generate with options
    $0 generate 0110 sql-mastery "SQL Mastery" --difficulty medium --tech sql

    # Validate quest network
    $0 validate

    # Build Docker images
    $0 build

EOF
    exit 1
}

if [[ $# -lt 1 ]]; then
    usage
fi

COMMAND="$1"
shift

case "$COMMAND" in
    generate)
        if [[ $# -lt 3 ]]; then
            print_error "Missing required arguments for generate"
            usage
        fi
        
        print_info "Generating quest via Docker..."
        docker-compose run --rm jekyll bash /app/scripts/quest/generate-placeholder-quest.sh "$@"
        ;;
    
    validate)
        print_info "Validating quest network via Docker..."
        docker-compose run --rm quest-network-validator
        ;;
    
    build)
        print_info "Building Docker images..."
        docker-compose build
        print_success "Docker images built successfully"
        ;;
    
    shell)
        print_info "Opening shell in Jekyll container..."
        docker-compose run --rm jekyll bash
        ;;
    
    *)
        print_error "Unknown command: $COMMAND"
        usage
        ;;
esac
