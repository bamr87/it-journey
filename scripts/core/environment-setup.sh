#!/bin/bash
#
# @file scripts/core/environment-setup.sh
# @description Unified environment setup script for IT-Journey projects
# @author IT-Journey Team <team@it-journey.org>
# @created 2025-07-07
# @lastModified 2025-07-07
# @version 1.0.0
#
# @relatedIssues 
#   - Script consolidation: Merge setup scripts from multiple projects
#
# @relatedEvolutions
#   - v1.0.0: Initial unified environment setup combining all project setup needs
#
# @dependencies
#   - Homebrew (macOS package manager)
#   - Git (version control)
#   - Ruby (for Jekyll projects)
#
# @changelog
#   - 2025-07-07: Initial creation combining zer0.sh and setup.sh functionality - ITJ
#
# @usage ./scripts/core/environment-setup.sh [--project-type TYPE] [--interactive]
# @notes Supports multiple project types with intelligent detection
#

set -euo pipefail

# IT-Journey Development Principles Implementation:
# DFF: Comprehensive error handling and system validation
# DRY: Single script for all environment setup needs
# KIS: Clear workflow with helpful prompts and feedback
# COLAB: Consistent setup experience across all projects

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly NC='\033[0m' # No Color

# Configuration
PROJECT_TYPE="auto"
INTERACTIVE_MODE=false
DRY_RUN=false
SKIP_BREW_INSTALL=false
SETUP_GIT_CONFIG=true
SETUP_DOCKER=true
SETUP_VSC=true

# Detect OS
readonly OS_TYPE="$(uname -s)"
readonly IS_MACOS="$([[ "$OS_TYPE" == "Darwin" ]] && echo true || echo false)"

# Show help message
show_help() {
    cat << EOF
🚀 IT-Journey Unified Environment Setup

DESCRIPTION:
    Sets up development environment for IT-Journey projects with all necessary
    tools, configurations, and dependencies.

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --project-type TYPE     Project type (jekyll, node, ruby, auto) [default: auto]
    --interactive          Run in interactive mode with prompts
    --dry-run              Show what would be installed without making changes
    --skip-brew            Skip Homebrew package installations
    --no-git-config       Skip Git configuration setup
    --no-docker           Skip Docker installation
    --no-vscode           Skip Visual Studio Code installation
    --help                Show this help message

PROJECT TYPES:
    auto                  Automatically detect project type from files
    jekyll                Jekyll/Ruby static site projects
    node                  Node.js/JavaScript projects  
    ruby                  Ruby gem development projects
    general               Basic development tools only

FEATURES:
    ✅ System Information Detection
    ✅ Development Tools Installation (Git, Docker, VS Code)
    ✅ Language Environment Setup (Ruby, Node.js)
    ✅ Project-Specific Dependencies
    ✅ Git Configuration & SSH Setup
    ✅ GitHub CLI Configuration
    ✅ Environment Validation

EXAMPLES:
    $0                              # Auto-detect and setup
    $0 --interactive               # Interactive setup with prompts
    $0 --project-type jekyll       # Setup for Jekyll development
    $0 --dry-run                   # Preview what would be installed

Following IT-Journey Principles:
    DFF: Comprehensive validation and error recovery
    DRY: Single script for all environment setup needs
    KIS: Clear workflow with helpful feedback
    COLAB: Consistent development environment for all contributors
EOF
}

# Logging functions
log() {
    echo -e "${GREEN}[SETUP]${NC} $1"
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

step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --project-type)
                PROJECT_TYPE="$2"
                shift 2
                ;;
            --interactive)
                INTERACTIVE_MODE=true
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --skip-brew)
                SKIP_BREW_INSTALL=true
                shift
                ;;
            --no-git-config)
                SETUP_GIT_CONFIG=false
                shift
                ;;
            --no-docker)
                SETUP_DOCKER=false
                shift
                ;;
            --no-vscode)
                SETUP_VSC=false
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

# Display system information
show_system_info() {
    step "System Information Detection"
    
    if [[ "$IS_MACOS" == true ]]; then
        log "Detected macOS system"
        system_profiler SPHardwareDataType | awk '/Model Name:|Model Identifier:|Chip:|Memory:/ {print "  " $0}'
        system_profiler SPSoftwareDataType | awk '/System Version:|Kernel Version:/ {print "  " $0}'
    else
        log "Detected Linux system"
        info "OS: $(uname -a)"
        info "Memory: $(free -h | awk '/^Mem:/ {print $2}')"
        info "CPU: $(nproc) cores"
    fi
    
    echo
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Homebrew (macOS) or equivalent (Linux)
install_package_manager() {
    if [[ "$SKIP_BREW_INSTALL" == true ]]; then
        info "Skipping package manager installation"
        return 0
    fi

    step "Package Manager Setup"
    
    if [[ "$IS_MACOS" == true ]]; then
        if ! command_exists brew; then
            log "Installing Homebrew..."
            if [[ "$DRY_RUN" == true ]]; then
                info "Would install Homebrew"
                return 0
            fi
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        else
            log "Homebrew already installed"
        fi
    else
        # Linux package manager check
        if command_exists apt-get; then
            log "Using APT package manager"
        elif command_exists yum; then
            log "Using YUM package manager"
        elif command_exists pacman; then
            log "Using Pacman package manager"
        else
            warn "No supported package manager found"
        fi
    fi
}

# Install core development tools
install_core_tools() {
    step "Core Development Tools Installation"
    
    local tools=()
    
    # Git
    if ! command_exists git; then
        tools+=("git")
    else
        log "Git already installed: $(git --version)"
    fi
    
    # GitHub CLI
    if ! command_exists gh; then
        tools+=("gh")
    else
        log "GitHub CLI already installed: $(gh --version | head -n1)"
    fi
    
    # Docker
    if [[ "$SETUP_DOCKER" == true ]] && ! command_exists docker; then
        if [[ "$IS_MACOS" == true ]]; then
            tools+=("--cask docker")
        else
            tools+=("docker.io")
        fi
    elif command_exists docker; then
        log "Docker already installed: $(docker --version)"
    fi
    
    # Visual Studio Code
    if [[ "$SETUP_VSC" == true ]] && ! command_exists code; then
        if [[ "$IS_MACOS" == true ]]; then
            tools+=("--cask visual-studio-code")
        else
            tools+=("code")
        fi
    elif command_exists code; then
        log "Visual Studio Code already installed"
    fi
    
    # Install tools
    if [[ ${#tools[@]} -gt 0 ]]; then
        log "Installing: ${tools[*]}"
        
        if [[ "$DRY_RUN" == true ]]; then
            info "Would install: ${tools[*]}"
            return 0
        fi
        
        if [[ "$IS_MACOS" == true ]]; then
            brew install "${tools[@]}"
        else
            if command_exists apt-get; then
                sudo apt-get update && sudo apt-get install -y "${tools[@]}"
            elif command_exists yum; then
                sudo yum install -y "${tools[@]}"
            fi
        fi
    else
        log "All core tools already installed"
    fi
}

# Auto-detect project type
detect_project_type() {
    if [[ "$PROJECT_TYPE" != "auto" ]]; then
        return 0
    fi
    
    step "Project Type Detection"
    
    if [[ -f "Gemfile" ]] || [[ -f "_config.yml" ]] || [[ -f "*.gemspec" ]]; then
        PROJECT_TYPE="jekyll"
        log "Detected Jekyll/Ruby project"
    elif [[ -f "package.json" ]]; then
        PROJECT_TYPE="node"
        log "Detected Node.js project"
    elif [[ -f "Gemfile" ]] && [[ ! -f "_config.yml" ]]; then
        PROJECT_TYPE="ruby"
        log "Detected Ruby project"
    else
        PROJECT_TYPE="general"
        log "No specific project type detected, using general setup"
    fi
}

# Setup Ruby environment
setup_ruby_environment() {
    step "Ruby Environment Setup"
    
    # Check Ruby
    if ! command_exists ruby; then
        log "Installing Ruby..."
        if [[ "$DRY_RUN" == true ]]; then
            info "Would install Ruby"
            return 0
        fi
        
        if [[ "$IS_MACOS" == true ]]; then
            brew install ruby
        else
            if command_exists apt-get; then
                sudo apt-get install -y ruby-full build-essential
            fi
        fi
    else
        local ruby_version
        ruby_version=$(ruby --version | awk '{print $2}')
        log "Ruby already installed: $ruby_version"
    fi
    
    # Check Bundler
    if ! command_exists bundle; then
        log "Installing Bundler..."
        if [[ "$DRY_RUN" == true ]]; then
            info "Would install Bundler"
            return 0
        fi
        gem install bundler
    else
        log "Bundler already installed: $(bundle --version)"
    fi
    
    # Install Jekyll if it's a Jekyll project
    if [[ "$PROJECT_TYPE" == "jekyll" ]] && ! command_exists jekyll; then
        log "Installing Jekyll..."
        if [[ "$DRY_RUN" == true ]]; then
            info "Would install Jekyll"
            return 0
        fi
        gem install jekyll
    fi
}

# Setup Node.js environment
setup_node_environment() {
    step "Node.js Environment Setup"
    
    # Check Node.js
    if ! command_exists node; then
        log "Installing Node.js..."
        if [[ "$DRY_RUN" == true ]]; then
            info "Would install Node.js"
            return 0
        fi
        
        if [[ "$IS_MACOS" == true ]]; then
            brew install node
        else
            if command_exists apt-get; then
                curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
                sudo apt-get install -y nodejs
            fi
        fi
    else
        log "Node.js already installed: $(node --version)"
    fi
    
    # Check npm
    if command_exists npm; then
        log "npm already installed: $(npm --version)"
    fi
}

# Setup Git configuration
setup_git_configuration() {
    if [[ "$SETUP_GIT_CONFIG" == false ]]; then
        info "Skipping Git configuration"
        return 0
    fi

    step "Git Configuration Setup"
    
    # Check if Git is already configured
    local git_name
    local git_email
    git_name=$(git config --global user.name 2>/dev/null || echo "")
    git_email=$(git config --global user.email 2>/dev/null || echo "")
    
    if [[ -n "$git_name" ]] && [[ -n "$git_email" ]]; then
        log "Git already configured:"
        info "  Name: $git_name"
        info "  Email: $git_email"
        return 0
    fi
    
    # Interactive or default configuration
    if [[ "$INTERACTIVE_MODE" == true ]] || [[ "$DRY_RUN" == false ]]; then
        local github_user=""
        local github_email=""
        
        if [[ "$INTERACTIVE_MODE" == true ]]; then
            echo
            read -p "Enter your GitHub username: " github_user
            read -p "Enter your email address (or press Enter for GitHub noreply): " github_email
            
            if [[ -z "$github_email" ]]; then
                github_email="${github_user}@users.noreply.github.com"
            fi
        else
            warn "Interactive mode disabled. Skipping Git configuration."
            info "Run with --interactive to configure Git interactively"
            return 0
        fi
        
        if [[ -n "$github_user" ]]; then
            log "Configuring Git..."
            if [[ "$DRY_RUN" == true ]]; then
                info "Would configure Git with:"
                info "  Name: $github_user"
                info "  Email: $github_email"
                return 0
            fi
            
            git config --global user.name "$github_user"
            git config --global user.email "$github_email"
            log "Git configuration complete"
            
            # Log configuration to file
            {
                echo "$(date) - Git configuration updated"
                echo "Name: $github_user"
                echo "Email: $github_email"
            } >> env-variables.log
        fi
    fi
}

# Install project dependencies
install_project_dependencies() {
    step "Project Dependencies Installation"
    
    case $PROJECT_TYPE in
        jekyll)
            if [[ -f "Gemfile" ]]; then
                log "Installing Ruby gems..."
                if [[ "$DRY_RUN" == true ]]; then
                    info "Would run: bundle install"
                    return 0
                fi
                bundle install
            fi
            ;;
        node)
            if [[ -f "package.json" ]]; then
                log "Installing Node.js packages..."
                if [[ "$DRY_RUN" == true ]]; then
                    info "Would run: npm install"
                    return 0
                fi
                npm install
            fi
            ;;
        ruby)
            if [[ -f "Gemfile" ]]; then
                log "Installing Ruby gems..."
                if [[ "$DRY_RUN" == true ]]; then
                    info "Would run: bundle install"
                    return 0
                fi
                bundle install
            fi
            ;;
        *)
            info "No specific project dependencies to install"
            ;;
    esac
}

# Validate environment setup
validate_environment() {
    step "Environment Validation"
    
    local validation_passed=true
    
    # Check core tools
    local required_tools=("git")
    [[ "$SETUP_DOCKER" == true ]] && required_tools+=("docker")
    
    for tool in "${required_tools[@]}"; do
        if command_exists "$tool"; then
            log "✅ $tool is available"
        else
            error "❌ $tool is not available"
            validation_passed=false
        fi
    done
    
    # Check language environments
    case $PROJECT_TYPE in
        jekyll|ruby)
            if command_exists ruby && command_exists bundle; then
                log "✅ Ruby environment is ready"
            else
                error "❌ Ruby environment is not properly configured"
                validation_passed=false
            fi
            ;;
        node)
            if command_exists node && command_exists npm; then
                log "✅ Node.js environment is ready"
            else
                error "❌ Node.js environment is not properly configured"
                validation_passed=false
            fi
            ;;
    esac
    
    if [[ "$validation_passed" == true ]]; then
        log "🎉 Environment validation passed!"
    else
        error "Environment validation failed. Please check the errors above."
    fi
}

# Show next steps
show_next_steps() {
    step "Next Steps"
    
    cat << EOF

🎉 Environment setup complete!

Recommended next steps:
  1. Restart your terminal to ensure all tools are in PATH
  2. Authenticate with GitHub: gh auth login
  3. Clone or create your IT-Journey project
  4. Run project-specific setup commands

Project-specific commands:
EOF

    case $PROJECT_TYPE in
        jekyll)
            cat << EOF
  - bundle exec jekyll serve    # Start development server
  - bundle exec jekyll build    # Build static site
EOF
            ;;
        node)
            cat << EOF
  - npm start                   # Start development server
  - npm run build              # Build for production
  - npm test                   # Run tests
EOF
            ;;
        ruby)
            cat << EOF
  - bundle exec rake test      # Run tests
  - gem build *.gemspec       # Build gem
EOF
            ;;
    esac

    cat << EOF

Useful IT-Journey commands:
  - scripts/core/version-manager.sh  # Manage project versions
  - scripts/deployment/update-settings.sh  # Update configuration

For support, visit: https://github.com/bamr87/it-journey

EOF
}

# Main execution function
main() {
    echo -e "${PURPLE}"
    cat << 'EOF'
🚀 IT-Journey Environment Setup
===============================
Setting up your development environment following IT-Journey principles:
  DFF: Design for Failure - Comprehensive validation and error handling
  DRY: Don't Repeat Yourself - Single script for all setup needs
  KIS: Keep It Simple - Clear workflow with helpful feedback
  COLAB: Collaboration - Consistent environment for all contributors
EOF
    echo -e "${NC}"
    
    parse_arguments "$@"
    
    [[ "$DRY_RUN" == true ]] && warn "DRY RUN MODE - No changes will be made"
    
    show_system_info
    detect_project_type
    
    # Installation steps
    install_package_manager
    install_core_tools
    
    # Language environment setup
    case $PROJECT_TYPE in
        jekyll|ruby)
            setup_ruby_environment
            ;;
        node)
            setup_node_environment
            ;;
        general)
            info "General setup - skipping language-specific environments"
            ;;
    esac
    
    setup_git_configuration
    install_project_dependencies
    validate_environment
    show_next_steps
    
    log "🎉 Environment setup complete!"
}

# Execute main function with all arguments
main "$@"
