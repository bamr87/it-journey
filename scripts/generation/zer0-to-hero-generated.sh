#!/bin/bash
# zer0-to-hero-generated.sh
# AUTO-GENERATED script from zer0.md markdown file
# This script contains all commands from the IT-Journey Zer0-to-Her0 guide

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to execute commands safely
safe_execute() {
    local description="$1"
    shift
    local cmd="$*"
    
    log "$description"
    echo -e "${CYAN}Executing: $cmd${NC}"
    
    if eval "$cmd"; then
        success "Completed: $description"
        return 0
    else
        warning "Failed: $description (continuing...)"
        return 1
    fi
}

# Main execution function
main() {
    echo -e "${PURPLE}"
    cat << 'HEADER'
🚀 IT-Journey: Generated Zer0-to-Her0 Script
============================================
This auto-generated script executes all commands
from the zer0.md guide in sequence.

WARNING: This script will:
- Install software on your system
- Create directories and files
- Configure Git and GitHub
- Start Docker containers
- Make network requests

Press Ctrl+C now if you want to exit.
HEADER
    echo -e "${NC}"
    
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Exiting..."
        exit 0
    fi
    
    log "Starting automated IT-Journey setup..."
    
    # Environment setup
    setup_environment
    
    # Install tools
    install_development_tools
    
    # GitHub setup
    setup_github
    
    # Project creation
    create_project
    
    # Jekyll setup
    setup_jekyll
    
    # Docker setup
    setup_docker
    
    # Final deployment
    deploy_site
    
    success "IT-Journey automation complete!"
}

# Environment setup phase
setup_environment() {
    log "Phase 1: Environment Setup"
    
    # System information gathering
    safe_execute "Getting system information" \
        "system_profiler SPHardwareDataType | awk '/Model Name:|Model Identifier:|Model Number:|Chip:|System Firmware Version:/ {print \$0}' || echo 'System info not available'"
    
    # Environment variable setup
    export GITHOME=~/github
    export GHUSER=${GHUSER:-$(whoami)}
    export GIT_REPO=${GIT_REPO:-my-it-journey}
    export ZREPO=$GITHOME/$GIT_REPO
    
    log "Environment configured: $GHUSER/$GIT_REPO"
    
    # Create environment log
    {
        echo "$(date) - IT Journey Configuration Log"
        echo "======================================="
        echo "GITHOME: $GITHOME"
        echo "GHUSER: $GHUSER"
        echo "GIT_REPO: $GIT_REPO"
        echo "ZREPO: $ZREPO"
        echo "======================================="
    } > env-variables.log
}

# Development tools installation
install_development_tools() {
    log "Phase 2: Installing Development Tools"
    
    # Install Homebrew
    if ! command_exists brew; then
        safe_execute "Installing Homebrew" \
            '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    else
        success "Homebrew already installed"
    fi
    
    # Update Homebrew
    safe_execute "Updating Homebrew" "brew update"
    
    # Install essential tools
    local tools=("git" "gh")
    for tool in "${tools[@]}"; do
        if ! command_exists "$tool"; then
            safe_execute "Installing $tool" "brew install $tool"
        else
            success "$tool already installed"
        fi
    done
    
    # Install cask applications
    if ! command_exists code; then
        safe_execute "Installing Visual Studio Code" "brew install --cask visual-studio-code"
    else
        success "Visual Studio Code already installed"
    fi
    
    if ! command_exists docker; then
        safe_execute "Installing Docker Desktop" "brew install --cask docker"
        warning "Docker Desktop needs to be started manually"
    else
        success "Docker already installed"
    fi
}

# GitHub setup phase
setup_github() {
    log "Phase 3: GitHub Setup"
    
    # Authenticate with GitHub
    if ! gh auth status &>/dev/null; then
        safe_execute "Authenticating with GitHub" "gh auth login --web"
    else
        success "GitHub CLI already authenticated"
    fi
    
    # Configure Git identity
    safe_execute "Configuring Git identity" \
        "git config --global user.name '$GHUSER' && git config --global user.email '$GHUSER@users.noreply.github.com'"
}

# Project creation phase
create_project() {
    log "Phase 4: Creating Project"
    
    # Create project directories
    safe_execute "Creating project directories" "mkdir -p $GITHOME"
    
    cd "$GITHOME" || error "Cannot navigate to $GITHOME"
    
    # Handle existing directory
    if [[ -d "$GIT_REPO" ]]; then
        warning "Directory $GIT_REPO already exists. Backing up..."
        mv "$GIT_REPO" "${GIT_REPO}.backup.$(date +%s)" || true
    fi
    
    # Create or clone repository
    if gh repo view "$GHUSER/$GIT_REPO" &>/dev/null; then
        safe_execute "Cloning existing repository" \
            "git clone https://github.com/$GHUSER/$GIT_REPO.git"
    else
        safe_execute "Creating GitHub repository" \
            "gh repo create $GIT_REPO --gitignore Jekyll --license mit --public --description 'My IT Journey - Building my first professional website'"
        
        safe_execute "Setting up local repository" \
            "mkdir -p $GIT_REPO && cd $GIT_REPO && git init && git remote add origin https://github.com/$GHUSER/$GIT_REPO.git && git branch -M main"
    fi
    
    cd "$ZREPO" || error "Cannot navigate to $ZREPO"
}

# Jekyll setup phase
setup_jekyll() {
    log "Phase 5: Jekyll Setup"
    
    # Create README if it doesn't exist
    if [[ ! -f README.md ]]; then
        cat > README.md << READMEEOF
# $GIT_REPO

Welcome to my IT Journey! This repository contains my first professional website built following the Zer0-to-Her0 guide.

## What I'm Building

- 🌐 A modern static website using Jekyll
- 🐳 Docker-based development environment
- 🚀 Automated deployment pipeline
- 📚 Documentation of my learning journey

## Live Site

🔗 [Visit my website](https://$GHUSER.github.io/$GIT_REPO)

## Development

This project was built using the IT-Journey Zer0-to-Her0 automated setup script.

### Local Development

\`\`\`bash
# Start development server
docker-compose up -d

# View site at http://localhost:4000
\`\`\`

### Built With

- [Jekyll](https://jekyllrb.com/) - Static site generator
- [zer0-mistakes](https://github.com/bamr87/zer0-mistakes) - Jekyll theme
- [Docker](https://www.docker.com/) - Containerization
- [GitHub Pages](https://pages.github.com/) - Hosting

---

*Built with ❤️ following the [IT-Journey](https://github.com/bamr87/it-journey) guide*
READMEEOF
    fi
    
    # Install theme
    if curl -fsSL https://raw.githubusercontent.com/bamr87/zer0-mistakes/main/install.sh | bash; then
        success "zer0-mistakes theme installed successfully"
    else
        warning "Theme installer failed, setting up manually..."
        setup_jekyll_manual
    fi
}

# Manual Jekyll setup fallback
setup_jekyll_manual() {
    log "Setting up Jekyll manually..."
    
    cat > Gemfile << 'GEMFILEEOF'
source "https://rubygems.org"

gem "github-pages", group: :jekyll_plugins

group :jekyll_plugins do
  gem "jekyll-remote-theme"
  gem "jekyll-feed"
  gem "jekyll-sitemap"
  gem "jekyll-seo-tag"
  gem "jekyll-paginate"
end
GEMFILEEOF

    cat > _config.yml << CONFIGEOF
title: "My IT Journey"
description: "Building my first professional website"
url: "https://$GHUSER.github.io"
baseurl: "/$GIT_REPO"

markdown: kramdown
highlighter: rouge
permalink: /:categories/:title/

plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag
  - jekyll-paginate

remote_theme: "bamr87/zer0-mistakes"
CONFIGEOF

    success "Manual Jekyll setup complete"
}

# Docker setup phase
setup_docker() {
    log "Phase 6: Docker Setup"
    
    # Create docker-compose.yml if it doesn't exist
    if [[ ! -f docker-compose.yml ]]; then
        cat > docker-compose.yml << 'DOCKEREOF'
version: '3.8'

services:
  jekyll:
    image: jekyll/jekyll:latest
    container_name: jekyll-dev
    environment:
      - JEKYLL_ENV=development
    ports:
      - "4000:4000"
      - "35729:35729"
    volumes:
      - .:/srv/jekyll
      - bundle_cache:/usr/local/bundle
    command: >
      bash -c "bundle install &&
               bundle exec jekyll serve 
               --host 0.0.0.0 
               --incremental 
               --livereload"

volumes:
  bundle_cache:
DOCKEREOF
        success "Docker configuration created"
    fi
    
    # Create development configuration
    if [[ ! -f _config_dev.yml ]]; then
        cat > _config_dev.yml << 'DEVEOF'
# Development overrides
url: "http://localhost:4000"
baseurl: ""

# Development settings
incremental: true
livereload: true
open_url: true

# Show drafts and future posts
show_drafts: true
future: true
DEVEOF
        success "Development configuration created"
    fi
    
    # Wait for Docker to be running
    while ! docker info &>/dev/null; do
        warning "Waiting for Docker to start... Please ensure Docker Desktop is running"
        sleep 5
    done
    
    # Start Docker container
    safe_execute "Starting Docker development server" "docker-compose up -d"
    
    # Wait for server
    log "Waiting for development server to start..."
    local attempts=0
    while ! curl -s http://localhost:4000 &>/dev/null && [[ $attempts -lt 30 ]]; do
        sleep 2
        ((attempts++))
    done
    
    if curl -s http://localhost:4000 &>/dev/null; then
        success "Development server running at http://localhost:4000"
        
        # Open browser if possible
        if command_exists open; then
            open http://localhost:4000 &
        fi
    else
        warning "Server may still be starting. Check logs with: docker-compose logs -f"
    fi
}

# Site deployment phase
deploy_site() {
    log "Phase 7: Deploying Site"
    
    # Add all files
    safe_execute "Adding all files to Git" "git add ."
    
    # Commit changes
    safe_execute "Committing changes" \
        'git commit -m "🚀 Automated IT Journey setup - Generated from zer0.md

- Complete development environment setup
- Jekyll infrastructure with zer0-mistakes theme
- Docker development environment
- Ready for GitHub Pages deployment

Generated by: zer0-to-hero-generated.sh" || true'
    
    # Push to GitHub
    safe_execute "Pushing to GitHub" "git push -u origin main"
    
    # Create completion summary
    cat > completion-summary.md << 'SUMMARYEOF'
# 🎉 IT Journey Complete!

## What You've Accomplished

You've successfully completed your journey from Zer0 to Her0! Here's what you now have:

### ✅ Development Environment
- Visual Studio Code
- Git version control
- Docker containerization
- GitHub CLI

### ✅ Live Website Infrastructure
- Jekyll static site generator
- Professional theme (zer0-mistakes)
- Docker development environment
- GitHub repository with version control

### ✅ Deployment Pipeline
- Automated GitHub Pages deployment
- Local development server
- Container-based development

## Your Resources

- **Local Website**: http://localhost:4000
- **GitHub Repository**: https://github.com/%s/%s
- **Live Website**: https://%s.github.io/%s (after enabling GitHub Pages)
- **Project Directory**: %s

## Next Steps

1. **Customize Your Site**: Edit _config.yml and add content in pages/
2. **Learn Markdown**: Create blog posts and documentation
3. **Explore Jekyll**: Add plugins and custom features
4. **Build Your Portfolio**: Document your learning journey

## Quick Commands

```bash
# Start development server
cd %s && docker-compose up -d

# Stop development server
cd %s && docker-compose down

# View logs
cd %s && docker-compose logs -f

# Update and restart
cd %s && docker-compose down && docker-compose up --build -d
```

---

**Congratulations! You're now a developer! 🚀**
SUMMARYEOF
    
    # Fill in the placeholders using printf
    printf "$(cat completion-summary.md)" "$GHUSER" "$GIT_REPO" "$GHUSER" "$GIT_REPO" "$ZREPO" "$ZREPO" "$ZREPO" "$ZREPO" "$ZREPO" > completion-summary.md
    
    success "Completion summary created"
    
    echo ""
    echo -e "${GREEN}🎉 SUCCESS! Your IT Journey is complete!${NC}"
    echo ""
    echo -e "${CYAN}📍 Your website is running at: http://localhost:4000${NC}"
    echo -e "${CYAN}📍 Your repository: https://github.com/$GHUSER/$GIT_REPO${NC}"
    echo -e "${CYAN}📍 Your project: $ZREPO${NC}"
    echo ""
    echo -e "${PURPLE}Next: Enable GitHub Pages to make your site live on the internet!${NC}"
    echo -e "${PURPLE}Visit: https://github.com/$GHUSER/$GIT_REPO/settings/pages${NC}"
    echo ""
    echo -e "${YELLOW}Welcome to the developer community! 🚀${NC}"
    
    # Open GitHub Pages settings
    if command_exists open; then
        open "https://github.com/$GHUSER/$GIT_REPO/settings/pages" &
    fi
}

# Execute main function if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
