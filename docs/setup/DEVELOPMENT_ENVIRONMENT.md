# Development Environment Setup

This guide provides step-by-step instructions for setting up a local development environment for the IT-Journey repository.

## Prerequisites

### Required Software

| Tool | Minimum Version | Purpose |
|------|----------------|---------|
| **Git** | 2.30+ | Version control |
| **Ruby** | 3.2.3 | Jekyll runtime |
| **Bundler** | 2.4+ | Dependency management |
| **Python** | 3.11+ | Automation scripts |
| **Docker** | 20.10+ (optional) | Containerized development |

### Operating System Support

- ✅ macOS 11+ (Big Sur and later)
- ✅ Ubuntu 20.04+ / Debian 11+
- ✅ Windows 10+ with WSL2
- ✅ Other Linux distributions (with package manager adjustments)

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/bamr87/it-journey.git
cd it-journey

# Run automated setup
./scripts/core/environment-setup.sh

# Start development server
bundle exec jekyll serve --config _config_dev.yml
```

### Option 2: Docker Setup (Easiest)

```bash
# Clone the repository
git clone https://github.com/bamr87/it-journey.git
cd it-journey

# Start with Docker Compose
docker-compose up

# Access at http://localhost:4002
```

### Option 3: Manual Setup

Follow the detailed instructions below for your operating system.

## Detailed Setup Instructions

### macOS Setup

#### 1. Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Install Ruby with rbenv

```bash
# Install rbenv and ruby-build
brew install rbenv ruby-build

# Initialize rbenv
echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc
source ~/.zshrc

# Install Ruby 3.2.3
rbenv install 3.2.3
rbenv global 3.2.3

# Verify installation
ruby --version  # Should show 3.2.3
```

#### 3. Install Bundler

```bash
gem install bundler
bundler --version  # Should show 2.4+
```

#### 4. Install Jekyll and Dependencies

```bash
cd it-journey
bundle install
```

#### 5. Install Python (for scripts)

```bash
# Python usually pre-installed on macOS
python3 --version  # Should show 3.11+

# If not, install via Homebrew
brew install python@3.11

# Install required packages
pip3 install requests pyyaml
```

#### 6. Install Docker (Optional)

```bash
# Download Docker Desktop for Mac
# https://www.docker.com/products/docker-desktop

# Or via Homebrew
brew install --cask docker
```

### Linux (Ubuntu/Debian) Setup

#### 1. Update System

```bash
sudo apt update
sudo apt upgrade -y
```

#### 2. Install Build Dependencies

```bash
sudo apt install -y \
    git \
    curl \
    build-essential \
    libssl-dev \
    libreadline-dev \
    zlib1g-dev \
    autoconf \
    bison \
    libyaml-dev \
    libffi-dev \
    libgdbm-dev \
    libncurses5-dev
```

#### 3. Install rbenv and Ruby

```bash
# Clone rbenv
git clone https://github.com/rbenv/rbenv.git ~/.rbenv

# Add to PATH
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
source ~/.bashrc

# Install ruby-build
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build

# Install Ruby 3.2.3
rbenv install 3.2.3
rbenv global 3.2.3

# Verify
ruby --version
```

#### 4. Install Bundler and Jekyll

```bash
gem install bundler

cd it-journey
bundle install
```

#### 5. Install Python

```bash
sudo apt install -y python3.11 python3-pip
pip3 install requests pyyaml
```

#### 6. Install Docker (Optional)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install -y docker-compose

# Log out and back in for group changes to take effect
```

### Windows (WSL2) Setup

#### 1. Install WSL2

```powershell
# Run in PowerShell as Administrator
wsl --install

# Restart computer
# Set WSL2 as default
wsl --set-default-version 2

# Install Ubuntu
wsl --install -d Ubuntu-22.04
```

#### 2. Open Ubuntu Terminal

```bash
# Update system
sudo apt update && sudo apt upgrade -y
```

#### 3. Follow Linux Setup Instructions

Continue with the Linux (Ubuntu/Debian) setup instructions above.

#### 4. Windows-Specific Configuration

```bash
# Configure Git line endings
git config --global core.autocrlf input

# Set default editor
git config --global core.editor "code --wait"  # If using VS Code
```

## Repository Setup

### 1. Clone Repository

```bash
# HTTPS
git clone https://github.com/bamr87/it-journey.git

# SSH (if configured)
git clone git@github.com:bamr87/it-journey.git

cd it-journey
```

### 2. Install Dependencies

```bash
# Ruby gems
bundle install

# Python packages (for scripts)
pip3 install requests pyyaml

# Verify Jekyll
bundle exec jekyll --version
```

### 3. Configure Environment

```bash
# Copy example environment file (if exists)
cp .env.example .env

# Edit with your settings
nano .env

# Set Jekyll environment
export JEKYLL_ENV=development
```

### 4. Build and Serve

```bash
# Development server
bundle exec jekyll serve --config _config_dev.yml

# Or use shortcut if configured
make serve  # If Makefile exists

# Access at http://localhost:4002
```

## Docker Development

### Setup Docker Environment

#### 1. Install Docker

Follow Docker installation instructions for your OS from [docker.com](https://www.docker.com/get-started).

#### 2. Verify Installation

```bash
docker --version
docker-compose --version
```

#### 3. Build and Run

```bash
# Build image (first time)
docker-compose build

# Start containers
docker-compose up

# Or in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### Docker Commands

```bash
# Rebuild after Gemfile changes
docker-compose build --no-cache

# Access container shell
docker-compose exec jekyll bash

# Run commands in container
docker-compose exec jekyll bundle update

# Clean up
docker-compose down -v  # Removes volumes too
```

### Docker Compose Configuration

**File:** `docker-compose.yml`

```yaml
version: '3.8'
services:
  jekyll:
    build: .
    volumes:
      - .:/usr/src/app
      - bundle_cache:/usr/local/bundle
    ports:
      - "4002:4002"
    command: bundle exec jekyll serve --host 0.0.0.0 --config _config_dev.yml

volumes:
  bundle_cache:
```

## IDE Setup

### VS Code (Recommended)

#### 1. Install Extensions

```bash
# Open VS Code
code it-journey

# Install recommended extensions (or click when prompted)
# See .vscode/extensions.json
```

**Recommended Extensions:**
- Jekyll Syntax Support
- Front Matter CMS
- YAML
- Markdown All in One
- Code Spell Checker
- Docker

#### 2. Configure Settings

**File:** `.vscode/settings.json`

```json
{
  "files.associations": {
    "*.html": "liquid"
  },
  "liquid.format.enable": true,
  "markdown.preview.breaks": true,
  "[markdown]": {
    "editor.wordWrap": "on",
    "editor.quickSuggestions": true
  }
}
```

#### 3. Configure Tasks

**File:** `.vscode/tasks.json`

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Serve Jekyll",
      "type": "shell",
      "command": "bundle exec jekyll serve --config _config_dev.yml",
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "problemMatcher": []
    }
  ]
}
```

### Other IDEs

#### RubyMine
- Import as Ruby project
- Configure Ruby SDK (3.2.3)
- Enable Jekyll support

#### Sublime Text
- Install Package Control
- Install Jekyll packages
- Configure build system

## Environment Variables

### Required Variables

```bash
# Add to ~/.bashrc or ~/.zshrc

# Jekyll environment
export JEKYLL_ENV=development

# Repository path
export IT_JOURNEY_HOME=~/path/to/it-journey

# Optional: OpenAI for AI features
export OPENAI_API_KEY=your-api-key-here
```

### Loading Variables

```bash
# Reload shell configuration
source ~/.bashrc  # or ~/.zshrc

# Verify
echo $JEKYLL_ENV
echo $IT_JOURNEY_HOME
```

## Common Development Tasks

### Starting Development Server

```bash
# Standard
bundle exec jekyll serve --config _config_dev.yml

# With live reload
bundle exec jekyll serve --config _config_dev.yml --livereload

# Incremental builds (faster)
bundle exec jekyll serve --config _config_dev.yml --incremental

# With drafts
bundle exec jekyll serve --config _config_dev.yml --drafts

# Specific port
bundle exec jekyll serve --config _config_dev.yml --port 4003
```

### Building Site

```bash
# Development build
bundle exec jekyll build --config _config_dev.yml

# Production build
JEKYLL_ENV=production bundle exec jekyll build

# Clean build
bundle exec jekyll clean
bundle exec jekyll build
```

### Updating Dependencies

```bash
# Update all gems
bundle update

# Update specific gem
bundle update jekyll

# Update GitHub Pages gems
bundle update github-pages

# Check for outdated gems
bundle outdated
```

### Running Scripts

```bash
# Link checker
python3 scripts/validation/link-checker.py --scope website

# Environment setup
./scripts/core/environment-setup.sh

# Build script
./scripts/development/build/build-site.sh
```

## Troubleshooting

### Common Issues

#### Issue: Port Already in Use

```bash
# Error: Address already in use - bind(2) for 127.0.0.1:4002

# Solution 1: Find and kill process
lsof -i :4002
kill -9 <PID>

# Solution 2: Use different port
bundle exec jekyll serve --config _config_dev.yml --port 4003
```

#### Issue: Bundle Install Fails

```bash
# Error: An error occurred while installing ffi

# Solution: Install system dependencies
# macOS
xcode-select --install

# Linux
sudo apt install build-essential libffi-dev

# Then retry
bundle install
```

#### Issue: Jekyll Command Not Found

```bash
# Error: command not found: jekyll

# Solution: Use bundle exec
bundle exec jekyll serve

# Or add to PATH
bundle install --binstubs
export PATH="./bin:$PATH"
```

#### Issue: Permission Denied

```bash
# Error: Permission denied

# Solution: Fix permissions
chmod +x scripts/**/*.sh

# Or run with bash
bash scripts/script-name.sh
```

#### Issue: Docker Build Fails

```bash
# Error: Docker build failed

# Solution 1: Clear cache and rebuild
docker-compose down -v
docker-compose build --no-cache

# Solution 2: Check Docker resources
# Increase memory/CPU in Docker Desktop settings
```

### Getting Help

1. **Check logs:**
   ```bash
   bundle exec jekyll serve --verbose
   ```

2. **Run doctor:**
   ```bash
   bundle exec jekyll doctor
   ```

3. **Search issues:**
   - [Jekyll Issues](https://github.com/jekyll/jekyll/issues)
   - [IT-Journey Issues](https://github.com/bamr87/it-journey/issues)

4. **Ask for help:**
   - Create issue in IT-Journey repository
   - Include error messages and system info

## Next Steps

After setup is complete:

1. **Read Documentation:**
   - [Repository Structure](../architecture/REPOSITORY_STRUCTURE.md)
   - [Jekyll Implementation](../architecture/JEKYLL_IMPLEMENTATION.md)
   - [Content Guidelines](../standards/CONTENT_GUIDELINES.md)

2. **Explore the Code:**
   - Browse `pages/` directory
   - Review existing posts and quests
   - Check out scripts in `scripts/`

3. **Make Your First Change:**
   - Create a test post
   - Modify a page
   - Run local tests

4. **Start Contributing:**
   - Read [Contributing Guide](../CONTRIBUTING_DEVELOPER.md)
   - Pick an issue to work on
   - Submit your first PR

## Additional Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Ruby Documentation](https://www.ruby-lang.org/en/documentation/)
- [Docker Documentation](https://docs.docker.com/)
- [Git Documentation](https://git-scm.com/doc)

---

**Last Updated**: 2025-10-13  
**Version**: 1.0.0

