#!/bin/bash

# IT-Journey Evolution Engine - Universal Setup Initializer v2.1
# Sacred initialization script for the mystical IT-Journey repository

set -euo pipefail

# Color codes for mystical output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🌟 IT-Journey Evolution Engine Initializing...${NC}"
echo -e "${CYAN}Preparing the sacred development environment${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo -e "${BLUE}🔮 Detected operating system: ${OS}${NC}"

# Check for required dependencies
echo -e "${YELLOW}⚔️ Verifying sacred artifacts (dependencies)...${NC}"

MISSING_DEPS=()

if ! command_exists ruby; then
    MISSING_DEPS+=("ruby")
    echo -e "${RED}❌ Ruby not found - The crimson gem is missing${NC}"
else
    RUBY_VERSION=$(ruby --version | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
    echo -e "${GREEN}✅ Ruby ${RUBY_VERSION} - The crimson gem is present${NC}"
fi

if ! command_exists jekyll; then
    MISSING_DEPS+=("jekyll")
    echo -e "${RED}❌ Jekyll not found - The static site sorcerer is absent${NC}"
else
    JEKYLL_VERSION=$(jekyll --version | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
    echo -e "${GREEN}✅ Jekyll ${JEKYLL_VERSION} - The static site sorcerer is ready${NC}"
fi

if ! command_exists git; then
    MISSING_DEPS+=("git")
    echo -e "${RED}❌ Git not found - The version control deity is missing${NC}"
else
    GIT_VERSION=$(git --version | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
    echo -e "${GREEN}✅ Git ${GIT_VERSION} - The version control deity watches over us${NC}"
fi

if ! command_exists gh; then
    echo -e "${YELLOW}⚠️ GitHub CLI not found - Communication with the repository gods will be limited${NC}"
else
    GH_VERSION=$(gh --version | grep gh | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
    echo -e "${GREEN}✅ GitHub CLI ${GH_VERSION} - Ready to commune with repository gods${NC}"
fi

if ! command_exists docker; then
    echo -e "${YELLOW}⚠️ Docker not found - Container sorcery will be unavailable${NC}"
else
    DOCKER_VERSION=$(docker --version | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
    echo -e "${GREEN}✅ Docker ${DOCKER_VERSION} - Container spirits are ready${NC}"
fi

# Handle missing dependencies
if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo ""
    echo -e "${RED}🚫 Missing critical dependencies: ${MISSING_DEPS[*]}${NC}"
    echo -e "${YELLOW}Please install the missing artifacts before proceeding with the ritual${NC}"
    
    case $OS in
        "macos")
            echo -e "${BLUE}🍺 For macOS, consider using Homebrew:${NC}"
            echo "  brew install ruby git"
            echo "  gem install jekyll bundler"
            ;;
        "linux")
            echo -e "${BLUE}🐧 For Linux, use your package manager:${NC}"
            echo "  sudo apt-get install ruby-full git (Ubuntu/Debian)"
            echo "  sudo yum install ruby git (CentOS/RHEL)"
            echo "  gem install jekyll bundler"
            ;;
        "windows")
            echo -e "${BLUE}🪟 For Windows, consider using:${NC}"
            echo "  - RubyInstaller: https://rubyinstaller.org/"
            echo "  - Git for Windows: https://git-scm.com/download/win"
            echo "  - Then run: gem install jekyll bundler"
            ;;
    esac
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 All sacred artifacts are present! The ritual may proceed.${NC}"

# Initialize repository if needed
if [ ! -d ".git" ]; then
    echo -e "${BLUE}🔄 Initializing the sacred repository...${NC}"
    git init
    echo -e "${GREEN}✅ Repository initialized${NC}"
fi

# Install Jekyll dependencies
if [ -f "Gemfile" ]; then
    echo -e "${BLUE}💎 Installing Ruby gems from the sacred Gemfile...${NC}"
    if command_exists bundle; then
        bundle install
    else
        echo -e "${YELLOW}⚠️ Bundler not found, installing gems individually...${NC}"
        gem install jekyll
    fi
    echo -e "${GREEN}✅ Ruby gems installed${NC}"
fi

# Create necessary directories
echo -e "${BLUE}📁 Ensuring sacred directory structure...${NC}"
mkdir -p _site
mkdir -p assets
mkdir -p pages
mkdir -p _posts
echo -e "${GREEN}✅ Directory structure verified${NC}"

# Set up universal environment variables
echo -e "${BLUE}🔧 Configuring universal environment...${NC}"

# Create or update .env file with universal paths
cat > .env << EOF
# IT-Journey Universal Environment Configuration
# Generated on $(date)

# Universal path configurations (works across platforms)
IT_JOURNEY_HOME=\${HOME}/github/it-journey
DOCKER_MOUNT_PATH=~/github/it-journey:/app

# Jekyll configuration
JEKYLL_ENV=development
JEKYLL_PORT=4002
JEKYLL_HOST=0.0.0.0

# Platform detection
OS_TYPE=${OS}
EOF

echo -e "${GREEN}✅ Universal environment configured${NC}"

echo ""
echo -e "${PURPLE}🚀 IT-Journey Evolution Engine initialization complete!${NC}"
echo -e "${CYAN}You are now ready to embark on your mystical coding journey.${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo -e "  1. ${BLUE}Start the Jekyll development server:${NC} bundle exec jekyll serve --port 4002"
echo -e "  2. ${BLUE}Or use Docker magic:${NC} docker build -t it-journey . && docker run -p 4002:4002 -v ~/github/it-journey:/app it-journey"
echo -e "  3. ${BLUE}Visit your local sanctuary:${NC} http://localhost:4002"
echo ""
echo -e "${GREEN}May your code compile and your documentation be accurate! 🙏${NC}"
