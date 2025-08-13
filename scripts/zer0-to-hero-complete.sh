#!/bin/bash
# zer0-to-hero-complete.sh
# Self-contained script that builds the entire IT Journey from this markdown guide
# Usage: curl -fsSL https://raw.githubusercontent.com/bamr87/it-journey/main/scripts/zer0-to-hero-complete.sh | bash

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging function
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

# Header
echo -e "${PURPLE}"
cat << 'EOF'
🚀 IT-Journey: Zer0 to Her0 Complete Setup
==========================================
This script will:
- Install all required development tools
- Set up your GitHub repository  
- Create a complete Jekyll website
- Configure Docker environment
- Deploy to GitHub Pages

All in one automated run!
EOF
echo -e "${NC}"

# Validate prerequisites
log "Checking prerequisites..."

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    error "This script is designed for macOS. Please adapt for your OS."
fi

# Check for internet connection
if ! ping -c 1 google.com &> /dev/null; then
    error "Internet connection required. Please check your connection."
fi

success "Prerequisites validated"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Homebrew if needed
install_homebrew() {
    if ! command_exists brew; then
        log "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        success "Homebrew installed"
    else
        success "Homebrew already installed"
    fi
}

# Install essential tools
install_development_tools() {
    log "Installing development tools..."
    
    # Update Homebrew
    brew update
    
    # Install tools if missing
    tools=("git" "gh" "docker" "visual-studio-code")
    for tool in "${tools[@]}"; do
        if [[ "$tool" == "visual-studio-code" ]]; then
            if ! command_exists code; then
                log "Installing Visual Studio Code..."
                brew install --cask visual-studio-code
            fi
        elif [[ "$tool" == "docker" ]]; then
            if ! command_exists docker; then
                log "Installing Docker Desktop..."
                brew install --cask docker
                warning "Docker Desktop needs to be started manually"
            fi
        else
            if ! command_exists "$tool"; then
                log "Installing $tool..."
                brew install "$tool"
            fi
        fi
    done
    
    success "Development tools installed"
}

# Configure environment
setup_environment() {
    log "Setting up environment configuration..."
    
    # Default values
    export GITHOME=~/github
    
    # Interactive setup if not automated
    if [[ "${AUTOMATED:-false}" != "true" ]]; then
        echo ""
        echo -e "${CYAN}Please provide your GitHub information:${NC}"
        
        # Get GitHub username
        while [[ -z "${GHUSER:-}" ]]; do
            read -p "GitHub username: " GHUSER
            export GHUSER
        done
        
        # Get repository name
        echo ""
        echo -e "${CYAN}Repository name (lowercase, hyphens only):${NC}"
        read -p "Repository name [my-it-journey]: " GIT_REPO
        export GIT_REPO=${GIT_REPO:-my-it-journey}
    else
        # Use provided environment variables or defaults
        export GHUSER=${GHUSER:-$(whoami)}
        export GIT_REPO=${GIT_REPO:-my-it-journey}
    fi
    
    export ZREPO=$GITHOME/$GIT_REPO
    
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
    
    success "Environment configured: $GHUSER/$GIT_REPO"
}

# Authenticate with GitHub
github_authentication() {
    log "Configuring GitHub authentication..."
    
    if ! gh auth status &>/dev/null; then
        log "Authenticating with GitHub CLI..."
        gh auth login --web
    fi
    
    # Configure Git identity
    git config --global user.name "$GHUSER"
    git config --global user.email "$GHUSER@users.noreply.github.com"
    
    success "GitHub authentication configured"
}

# Create project structure
create_project_structure() {
    log "Creating project structure..."
    
    # Create directories
    mkdir -p "$GITHOME"
    cd "$GITHOME"
    
    # Remove existing directory if it exists
    if [[ -d "$GIT_REPO" ]]; then
        warning "Directory $GIT_REPO already exists. Backing up..."
        mv "$GIT_REPO" "${GIT_REPO}.backup.$(date +%s)"
    fi
    
    mkdir -p "$GIT_REPO"
    cd "$GIT_REPO"
    
    success "Project structure created at $ZREPO"
}

# Create GitHub repository
create_github_repository() {
    log "Creating GitHub repository..."
    
    # Check if repository already exists
    if gh repo view "$GHUSER/$GIT_REPO" &>/dev/null; then
        warning "Repository $GHUSER/$GIT_REPO already exists"
        
        # Clone existing repository
        git clone "https://github.com/$GHUSER/$GIT_REPO.git" .
    else
        # Create new repository
        gh repo create "$GIT_REPO" \
            --gitignore Jekyll \
            --license mit \
            --public \
            --description "My IT Journey - Building my first professional website"
        
        # Initialize local repository
        git init
        git remote add origin "https://github.com/$GHUSER/$GIT_REPO.git"
        git branch -M main
    fi
    
    success "GitHub repository configured"
}

# Create initial content
create_initial_content() {
    log "Creating initial content..."
    
    # Create README if it doesn't exist
    if [[ ! -f README.md ]]; then
        cat > README.md << EOF
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
EOF
    fi
    
    success "Initial content created"
}

# Install Jekyll theme and infrastructure
setup_jekyll_infrastructure() {
    log "Setting up Jekyll infrastructure..."
    
    # Download and run theme installer
    if ! curl -fsSL https://raw.githubusercontent.com/bamr87/zer0-mistakes/main/install.sh | bash; then
        warning "Theme installer failed, setting up manually..."
        
        # Manual Jekyll setup
        cat > Gemfile << 'EOF'
source "https://rubygems.org"

gem "github-pages", group: :jekyll_plugins

group :jekyll_plugins do
  gem "jekyll-remote-theme"
  gem "jekyll-feed"
  gem "jekyll-sitemap"
  gem "jekyll-seo-tag"
  gem "jekyll-paginate"
end
EOF

        cat > _config.yml << EOF
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

# Build settings
remote_theme: "bamr87/zer0-mistakes"
EOF
    fi
    
    success "Jekyll infrastructure configured"
}

# Create Docker environment
setup_docker_environment() {
    log "Setting up Docker environment..."
    
    # Create docker-compose.yml if it doesn't exist
    if [[ ! -f docker-compose.yml ]]; then
        cat > docker-compose.yml << 'EOF'
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
EOF
    fi
    
    # Create development configuration
    if [[ ! -f _config_dev.yml ]]; then
        cat > _config_dev.yml << EOF
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
EOF
    fi
    
    success "Docker environment configured"
}

# Build and start the website
build_and_start_website() {
    log "Building and starting website..."
    
    # Wait for Docker to be running
    while ! docker info &>/dev/null; do
        warning "Waiting for Docker to start... Please ensure Docker Desktop is running"
        sleep 5
    done
    
    # Build and start the container
    log "Starting Jekyll development server..."
    docker-compose up -d
    
    # Wait for server to start
    log "Waiting for server to start..."
    local attempts=0
    while ! curl -s http://localhost:4000 &>/dev/null && [[ $attempts -lt 30 ]]; do
        sleep 2
        ((attempts++))
    done
    
    if curl -s http://localhost:4000 &>/dev/null; then
        success "Website is running at http://localhost:4000"
        
        # Open browser (macOS)
        if command_exists open; then
            open http://localhost:4000
        fi
    else
        warning "Server may still be starting. Check with: docker-compose logs -f"
    fi
}

# Commit and deploy
deploy_to_github() {
    log "Deploying to GitHub..."
    
    # Add all files
    git add .
    
    # Commit changes
    git commit -m "🚀 Complete IT Journey setup

- Automated setup using zer0-to-hero script
- Jekyll infrastructure with zer0-mistakes theme
- Docker development environment
- GitHub Pages deployment ready

Built with IT-Journey automation script" || true
    
    # Push to GitHub
    git push -u origin main
    
    success "Deployed to GitHub: https://github.com/$GHUSER/$GIT_REPO"
    
    log "Enabling GitHub Pages..."
    echo ""
    echo -e "${CYAN}Your website will be live at: https://$GHUSER.github.io/$GIT_REPO${NC}"
    echo -e "${CYAN}Enable GitHub Pages at: https://github.com/$GHUSER/$GIT_REPO/settings/pages${NC}"
    
    # Open GitHub Pages settings
    if command_exists open; then
        open "https://github.com/$GHUSER/$GIT_REPO/settings/pages"
    fi
}

# Create completion summary
create_completion_summary() {
    log "Creating completion summary..."
    
    cat > completion-summary.md << EOF
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
- **GitHub Repository**: https://github.com/$GHUSER/$GIT_REPO
- **Live Website**: https://$GHUSER.github.io/$GIT_REPO (after enabling GitHub Pages)
- **Project Directory**: $ZREPO

## Next Steps

1. **Customize Your Site**: Edit _config.yml and add content in pages/
2. **Learn Markdown**: Create blog posts and documentation
3. **Explore Jekyll**: Add plugins and custom features
4. **Build Your Portfolio**: Document your learning journey

## Quick Commands

\`\`\`bash
# Start development server
cd $ZREPO && docker-compose up -d

# Stop development server
cd $ZREPO && docker-compose down

# View logs
cd $ZREPO && docker-compose logs -f

# Update and restart
cd $ZREPO && docker-compose down && docker-compose up --build -d
\`\`\`

---

**Congratulations! You're now a developer! 🚀**

*Generated on $(date) by the IT-Journey automation script*
EOF
    
    success "Completion summary created"
}

# Main execution flow
main() {
    log "Starting IT-Journey Zer0-to-Her0 Complete Setup..."
    
    # Execute all setup phases
    install_homebrew
    install_development_tools
    setup_environment
    github_authentication
    create_project_structure
    create_github_repository
    create_initial_content
    setup_jekyll_infrastructure
    setup_docker_environment
    build_and_start_website
    deploy_to_github
    create_completion_summary
    
    # Final success message
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
}

# Execute main function
main "$@"
