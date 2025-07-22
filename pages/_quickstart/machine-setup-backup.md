---
title: "Complete Machine Setup Guide: Jekyll Development Environment"
author: bamr87
description: "Comprehensive step-by-step guide to setting up your development machine for Jekyll static site generation, covering Windows, macOS, and Linux with automated installation scripts and troubleshooting."
excerpt: "Master the complete setup process for Jekyll development across all major operating systems with our comprehensive, platform-specific guide."
layout: default
keywords:
  primary:
    - machine setup
    - jekyll development
    - development environment
    - cross-platform setup
  secondary:
    - ruby installation
    - github setup
    - visual studio code
    - package managers
    - homebrew
    - winget
    - apt
lastmod: 2025-07-21T18:00:00.000Z
draft: false
slug: machine-setup
comments: true
fmContentType: default
preview: /assets/images/building-machines.png
tags:
  - development
  - Jekyll
  - machine-setup
  - Ruby
  - Visual-Studio-Code
  - cross-platform
  - automation
categories:
  - Development
  - Guides
  - Jekyll
  - Programming
  - Web-Development
difficulty: "🟡 Medium"
estimatedTime: "60-90 minutes"
prerequisites:
  - "Basic familiarity with command line/terminal"
  - "Administrator access to your computer"
  - "Internet connection for downloads"
relatedDocs:
  - title: "Jekyll Quickstart Guide"
    url: "./jekyll-quickstart.md"
  - title: "Git Configuration Guide"
    url: "./git-setup.md"
  - title: "VS Code Extensions for Jekyll"
    url: "./vscode-extensions.md"
---

## 🎯 Mission Overview

Welcome to your journey in setting up a professional Jekyll development environment! This comprehensive guide will transform your machine into a powerful static site generation workstation. Whether you're using Windows, macOS, or Linux, you'll have everything needed to create, develop, and deploy Jekyll websites.

**What You'll Accomplish:**
- ✅ Install and configure essential development tools
- ✅ Set up package managers for streamlined software management
- ✅ Configure Git and GitHub for version control
- ✅ Install Ruby and Jekyll with proper environment configuration
- ✅ Set up Visual Studio Code with Jekyll-optimized extensions
- ✅ Create your first Jekyll project
- ✅ Establish automated backup and deployment workflows

**Time Investment:** 60-90 minutes for complete setup
**Skill Level:** Beginner to Intermediate
**End Result:** A fully functional Jekyll development environment ready for professional web development

---
title: "Complete Machine Setup Guide: Jekyll Development Environment"
author: bamr87
description: "Step-by-step guide to setting up Jekyll development environment across Windows, macOS, and Linux with automation scripts."
excerpt: "Master the complete setup process for Jekyll development across all major operating systems with our comprehensive, platform-specific guide."
layout: default
keywords:
  primary:
    - machine setup
    - jekyll development
    - development environment
    - cross-platform setup
  secondary:
    - ruby installation
    - github setup
    - visual studio code
    - package managers
    - homebrew
    - winget
    - apt
lastmod: 2025-07-21T18:00:00.000Z
draft: false
slug: machine-setup
comments: true
fmContentType: default
preview: /assets/images/building-machines.png
tags:
  - development
  - Jekyll
  - machine-setup
  - Ruby
  - Visual-Studio-Code
  - cross-platform
  - automation
categories:
  - Development
  - Guides
  - Jekyll
  - Programming
  - Web-Development
difficulty: "🟡 Medium"
estimatedTime: "60-90 minutes"
prerequisites:
  - "Basic familiarity with command line/terminal"
  - "Administrator access to your computer"
  - "Internet connection for downloads"
relatedDocs:
  - title: "Jekyll Quickstart Guide"
    url: "./jekyll-quickstart.md"
  - title: "Git Configuration Guide"
    url: "./git-setup.md"
  - title: "VS Code Extensions for Jekyll"
    url: "./vscode-extensions.md"
---

## 🎯 Mission Overview

Welcome to your journey in setting up a professional Jekyll development environment! This comprehensive guide will transform your machine into a powerful static site generation workstation. Whether you're using Windows, macOS, or Linux, you'll have everything needed to create, develop, and deploy Jekyll websites.

**What You'll Accomplish:**

- ✅ Install and configure essential development tools
- ✅ Set up package managers for streamlined software management
- ✅ Configure Git and GitHub for version control
- ✅ Install Ruby and Jekyll with proper environment configuration
- ✅ Set up Visual Studio Code with Jekyll-optimized extensions
- ✅ Create your first Jekyll project
- ✅ Establish automated backup and deployment workflows

**Time Investment:** 60-90 minutes for complete setup
**Skill Level:** Beginner to Intermediate
**End Result:** A fully functional Jekyll development environment ready for professional web development

## 📋 Table of Contents

- [Prerequisites Check](#prerequisites-check)
- [Choose Your Platform Path](#choose-your-platform-path)
- [Phase 1: Package Manager Setup](#phase-1-package-manager-setup)
- [Phase 2: Development Tools Installation](#phase-2-development-tools-installation)
- [Phase 3: Ruby and Jekyll Setup](#phase-3-ruby-and-jekyll-setup)
- [Phase 4: Project Creation and Testing](#phase-4-project-creation-and-testing)
- [Phase 5: Advanced Configuration](#phase-5-advanced-configuration)
- [Troubleshooting Guide](#troubleshooting-guide)
- [Next Steps](#next-steps)

## ✅ Prerequisites Check

Before we begin, ensure you have:

- [ ] **Administrator/Sudo Access**: Required for installing system packages
- [ ] **Internet Connection**: For downloading software and packages
- [ ] **Minimum 4GB Available Storage**: For development tools and dependencies
- [ ] **Basic Terminal Knowledge**: Comfort with running command-line instructions
- [ ] **GitHub Account**: Create one at [github.com](https://github.com) if you don't have it

### System Requirements

| Operating System | Minimum Version | Recommended Version | RAM | Storage |
|------------------|-----------------|---------------------|-----|---------|
| **Windows** | Windows 10 Build 19041 | Windows 11 | 8GB | 20GB |
| **macOS** | macOS 10.15 Catalina | macOS 12 Monterey or later | 8GB | 20GB |
| **Linux** | Ubuntu 18.04+ / Debian 10+ | Ubuntu 22.04+ / Debian 12+ | 4GB | 15GB |

## 🌍 Choose Your Platform Path

Select your operating system to begin the setup journey:

### 🍎 macOS Setup Path
Perfect for Mac users who want a streamlined development experience with Homebrew.

### 🪟 Windows Setup Path  
Comprehensive Windows setup using Winget and PowerShell, with WSL2 support.

### 🐧 Linux Setup Path
Native Linux development using APT, YUM, or other distribution package managers.

---

## Phase 1: Package Manager Setup

Package managers are essential tools that automate software installation, updates, and dependency management. They're like app stores for developers, providing secure, trusted software repositories.

### Benefits of Package Managers

- **Automated Dependency Resolution**: Automatically installs required dependencies
- **Secure Software Sources**: Packages are verified and signed for security
- **Easy Updates**: Update all installed software with single commands
- **Consistent Environments**: Reproducible setups across different machines
- **Version Management**: Install specific versions and manage upgrades

### 🍎 macOS: Homebrew Installation

Homebrew is the premier package manager for macOS, providing access to thousands of open-source packages.

#### Install Homebrew

```zsh
# Install Homebrew (copy and paste this entire command)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Verify Installation

```zsh
# Check Homebrew version
brew --version

# Update Homebrew to latest version
brew update

# Verify Homebrew installation health
brew doctor
```

#### Configure Shell Integration

```zsh
# Add Homebrew to your PATH (for Apple Silicon Macs)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# For Intel Macs, use this instead:
# echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
# eval "$(/usr/local/bin/brew shellenv)"
```

### 🪟 Windows: Winget and Package Management

Winget is Microsoft's official package manager for Windows, providing command-line installation of applications.

#### Install Winget (Windows 10/11)

Winget comes pre-installed on Windows 11 and newer Windows 10 builds. If not available:

```powershell
# Check if Winget is available
winget --version

# If not available, install from Microsoft Store:
# Search for "App Installer" in Microsoft Store and install
```

#### Enable Developer Mode (Recommended)

```powershell
# Enable Developer Mode for better development experience
# Run as Administrator
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" -Name "AllowDevelopmentWithoutDevLicense" -Value 1
```

#### Configure PowerShell Execution Policy

```powershell
# Allow local script execution (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```

### 🐧 Linux: APT and Package Management

Most Linux distributions come with built-in package managers. We'll focus on APT (Debian/Ubuntu) with notes for other distributions.

#### Update Package Lists

```bash
# Update package lists (Ubuntu/Debian)
sudo apt update && sudo apt upgrade -y

# For Red Hat/CentOS/Fedora users:
# sudo dnf update -y

# For Arch Linux users:
# sudo pacman -Syu
```

#### Install Essential Build Tools

```bash
# Install build essentials (Ubuntu/Debian)
sudo apt install -y build-essential curl file git

# For Red Hat/CentOS/Fedora:
# sudo dnf groupinstall "Development Tools" && sudo dnf install curl file git

# For Arch Linux:
# sudo pacman -S base-devel curl file git
```

---

## Phase 2: Development Tools Installation

Now we'll install the core development tools needed for Jekyll development.

### Git Version Control System

Git is essential for version control and collaborating on projects.

#### 🍎 macOS Git Installation

```zsh
# Install Git via Homebrew
brew install git

# Verify installation
git --version
```

#### 🪟 Windows Git Installation

```powershell
# Install Git via Winget
winget install Git.Git

# Alternative: Install with additional tools
winget install Git.Git --source winget

# Verify installation (restart terminal first)
git --version
```

#### 🐧 Linux Git Installation

```bash
# Install Git (Ubuntu/Debian)
sudo apt install -y git

# For Red Hat/CentOS/Fedora:
# sudo dnf install git

# For Arch Linux:
# sudo pacman -S git

# Verify installation
git --version
```

### GitHub CLI Setup

The GitHub CLI enables seamless interaction with GitHub repositories from the command line.

#### 🍎 macOS GitHub CLI

```zsh
# Install GitHub CLI via Homebrew
brew install gh

# Verify installation
gh --version
```

#### 🪟 Windows GitHub CLI

```powershell
# Install GitHub CLI via Winget
winget install GitHub.cli

# Verify installation
gh --version
```

#### 🐧 Linux GitHub CLI

```bash
# Install GitHub CLI (Ubuntu/Debian)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Verify installation
gh --version
```

### Configure Git and GitHub

#### Set Up Git Identity

```bash
# Configure your Git identity
git config --global user.name "Your Full Name"
git config --global user.email "your-email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Verify configuration
git config --list
```

#### Authenticate with GitHub

```bash
# Login to GitHub CLI (follow the prompts)
gh auth login

# Test GitHub CLI connection
gh auth status
```

### Visual Studio Code Installation

VS Code is the recommended IDE for Jekyll development with excellent extensions and integrated terminal.

#### 🍎 macOS VS Code

```zsh
# Install VS Code via Homebrew
brew install --cask visual-studio-code

# Alternative: Download from https://code.visualstudio.com/
```

#### 🪟 Windows VS Code

```powershell
# Install VS Code via Winget
winget install Microsoft.VisualStudioCode

# Alternative: Download from https://code.visualstudio.com/
```

#### 🐧 Linux VS Code

```bash
# Install VS Code (Ubuntu/Debian)
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code

# Alternative: Use Snap
# sudo snap install --classic code
```

---

## Phase 3: Ruby and Jekyll Setup

Ruby is the programming language that powers Jekyll. We'll install Ruby and configure it properly for Jekyll development.

### Ruby Installation

#### 🍎 macOS Ruby Setup

```zsh
# Install Ruby via Homebrew (recommended version for Jekyll)
brew install ruby@3.1

# Add Ruby to your PATH
echo 'export PATH="/opt/homebrew/opt/ruby@3.1/bin:$PATH"' >> ~/.zshrc
echo 'export PATH="/opt/homebrew/lib/ruby/gems/3.1.0/bin:$PATH"' >> ~/.zshrc

# For Intel Macs, use:
# echo 'export PATH="/usr/local/opt/ruby@3.1/bin:$PATH"' >> ~/.zshrc
# echo 'export PATH="/usr/local/lib/ruby/gems/3.1.0/bin:$PATH"' >> ~/.zshrc

# Reload shell configuration
source ~/.zshrc

# Verify Ruby installation
ruby --version
gem --version
```

#### 🪟 Windows Ruby Setup

```powershell
# Install Ruby via Winget (Ruby+Devkit version recommended)
winget install RubyInstallerTeam.RubyWithDevKit.3.1

# Restart your terminal or PowerShell session

# Verify Ruby installation
ruby --version
gem --version

# Install MSYS2 development toolchain (if prompted during Ruby installation)
# Follow the installer prompts to complete the setup
```

#### 🐧 Linux Ruby Setup

```bash
# Install Ruby and development headers (Ubuntu/Debian)
sudo apt install -y ruby-full build-essential zlib1g-dev

# Configure gem installation directory
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc

# Reload shell configuration
source ~/.bashrc

# Verify Ruby installation
ruby --version
gem --version
```

### Jekyll and Bundler Installation

```bash
# Install Jekyll and Bundler globally
gem install bundler jekyll

# Verify installations
jekyll --version
bundler --version
```

### Test Jekyll Installation

```bash
# Create a test Jekyll site
jekyll new my-test-site
cd my-test-site

# Build and serve the site
bundle install
bundle exec jekyll serve

# Open your browser to http://localhost:4000 to see your site
```

---

## Phase 4: Project Creation and Testing

Now let's set up the IT-Journey repository and test everything works correctly.

### Clone the IT-Journey Repository

```bash
# Navigate to your development directory
cd ~
mkdir -p github
cd github

# Fork and clone the IT-Journey repository
gh repo fork bamr87/it-journey --clone

# Navigate into the repository
cd it-journey
```

### Install Project Dependencies

```bash
# Install Jekyll dependencies for the project
bundle install

# If you encounter permission issues on Linux/macOS:
# bundle install --path vendor/bundle
```

### Test Local Development Server

```bash
# Build and serve the site locally
bundle exec jekyll serve --config _config_dev.yml

# Or use the development configuration
bundle exec jekyll serve --host 0.0.0.0 --port 4000 --livereload
```

**Expected Output:**
```
Configuration file: _config_dev.yml
            Source: /path/to/it-journey
       Destination: /path/to/it-journey/_site
 Incremental build: disabled. Enable with --incremental
      Generating...
                    done in X.X seconds.
 Auto-regeneration: enabled for '/path/to/it-journey'
    Server address: http://127.0.0.1:4000/
  Server running... press ctrl-c to stop.
```

### Verify Setup Checklist

- [ ] **Local server runs**: Site loads at `http://localhost:4000`
- [ ] **Live reload works**: Changes to files automatically refresh the browser
- [ ] **No build errors**: Jekyll builds without warnings or errors
- [ ] **Git works**: Can commit and push changes
- [ ] **GitHub CLI works**: Can interact with GitHub repositories

---

## Phase 5: Advanced Configuration

### Essential VS Code Extensions

Install these extensions for an optimal Jekyll development experience:

```bash
# Install extensions via command line
code --install-extension sissel.shopify-liquid
code --install-extension yzhang.markdown-all-in-one
code --install-extension DavidAnson.vscode-markdownlint
code --install-extension esbenp.prettier-vscode
code --install-extension ms-vscode.vscode-yaml
code --install-extension bradlc.vscode-tailwindcss
code --install-extension formulahendry.auto-rename-tag
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension GitHub.copilot
```

### VS Code Workspace Configuration

Create a `.vscode/settings.json` file in your project:

```json
{
  "files.associations": {
    "*.html": "liquid",
    "*.md": "markdown"
  },
  "emmet.includeLanguages": {
    "liquid": "html"
  },
  "liquid.format.enable": true,
  "markdownlint.config": {
    "MD013": false,
    "MD033": false
  },
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "jekyll.preview.port": 4000
}
```

### Advanced Ruby Configuration

#### rbenv (Alternative Ruby Version Manager)

For more advanced Ruby version management:

```bash
# Install rbenv (macOS)
brew install rbenv

# Install rbenv (Linux)
curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash

# Add to shell configuration
echo 'eval "$(rbenv init -)"' >> ~/.zshrc  # or ~/.bashrc

# Install and set Ruby version
rbenv install 3.1.0
rbenv global 3.1.0
```

### Docker Development Environment (Optional)

For containerized development:

```dockerfile
# Dockerfile for Jekyll development
FROM ruby:3.1-alpine

WORKDIR /site

# Install Jekyll dependencies
RUN apk add --no-cache \
    build-base \
    git \
    nodejs \
    npm

# Install Jekyll and Bundler
RUN gem install bundler jekyll

# Expose port
EXPOSE 4000

# Default command
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  jekyll:
    build: .
    ports:
      - "4000:4000"
    volumes:
      - .:/site
      - /site/vendor
    environment:
      - JEKYLL_ENV=development
```

---

## 🚨 Troubleshooting Guide

### Common Issues and Solutions

#### Ruby Installation Problems

**Problem:** `gem install` fails with permission errors

**Solution:**
```bash
# Use user installation directory
gem install --user-install bundler jekyll

# Or configure gem home
export GEM_HOME="$HOME/gems"
export PATH="$HOME/gems/bin:$PATH"
```

**Problem:** Multiple Ruby versions causing conflicts

**Solution:**
```bash
# Check which Ruby is being used
which ruby
ruby --version

# Use rbenv or similar version manager
rbenv versions
rbenv local 3.1.0
```

#### Jekyll Build Errors

**Problem:** `bundle install` fails

**Solution:**
```bash
# Clear bundle cache
bundle clean --force

# Reinstall dependencies
rm Gemfile.lock
bundle install

# Check for platform-specific issues
bundle lock --add-platform x86_64-linux
bundle lock --add-platform ruby
```

**Problem:** Port already in use

**Solution:**
```bash
# Kill process using port 4000
lsof -ti:4000 | xargs kill -9

# Use different port
bundle exec jekyll serve --port 4001
```

#### Git Configuration Issues

**Problem:** Git push fails with authentication errors

**Solution:**
```bash
# Re-authenticate with GitHub CLI
gh auth logout
gh auth login

# Or configure SSH keys
ssh-keygen -t ed25519 -C "your_email@example.com"
gh ssh-key add ~/.ssh/id_ed25519.pub
```

#### Platform-Specific Issues

#### 🍎 macOS Troubleshooting

**Xcode Command Line Tools:**
```zsh
# Install if missing
xcode-select --install

# Reset if corrupted
sudo xcode-select --reset
```

**Path Issues:**
```zsh
# Check your PATH
echo $PATH

# Reset PATH in ~/.zshrc
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
```

#### 🪟 Windows Troubleshooting

**PowerShell Execution Policy:**
```powershell
# Check current policy
Get-ExecutionPolicy

# Set to allow local scripts
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows Subsystem for Linux (WSL2) Setup:**
```powershell
# Enable WSL2 (run as Administrator)
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Install Ubuntu from Microsoft Store
# Set WSL2 as default
wsl --set-default-version 2
```

#### 🐧 Linux Troubleshooting

**Permission Issues:**
```bash
# Fix gem permissions
sudo chown -R $(whoami) ~/.gem

# Add user to necessary groups
sudo usermod -a -G sudo $(whoami)
```

**Missing Dependencies:**
```bash
# Install additional build tools if needed
sudo apt install -y libffi-dev libssl-dev libxml2-dev libxslt-dev
```

### Performance Optimization

#### Faster Bundle Installation

```bash
# Use parallel jobs
bundle install --jobs 4

# Cache gems globally
bundle config set cache_all true
```

#### Jekyll Build Optimization

```bash
# Incremental builds
bundle exec jekyll serve --incremental

# Limit posts in development
bundle exec jekyll serve --limit_posts 10

# Exclude unnecessary files
# Add to _config.yml:
# exclude: [vendor, node_modules, README.md]
```

---

## 🎉 Verification and Next Steps

### Final Verification Checklist

Run through this checklist to ensure everything is working:

- [ ] **Package Manager**: `brew --version` (macOS) or `winget --version` (Windows) or `apt --version` (Linux)
- [ ] **Git**: `git --version` shows version 2.30+
- [ ] **GitHub CLI**: `gh --version` and `gh auth status` shows authenticated
- [ ] **Ruby**: `ruby --version` shows version 3.0+
- [ ] **Jekyll**: `jekyll --version` shows version 4.2+
- [ ] **Bundler**: `bundler --version` shows version 2.0+
- [ ] **VS Code**: Opens and shows extensions installed
- [ ] **Local Server**: `bundle exec jekyll serve` runs without errors
- [ ] **Browser Access**: Site loads at `http://localhost:4000`

### Create Your First Post

```bash
# Navigate to your IT-Journey repository
cd ~/github/it-journey

# Create a new post
cat > pages/_posts/$(date +%Y-%m-%d)-my-first-post.md << 'EOF'
---
title: "My First Jekyll Post"
date: 2025-07-21
categories: [Blog, Jekyll]
tags: [first-post, jekyll, setup]
---

# Welcome to My Jekyll Journey!

This is my first post created after setting up my Jekyll development environment.

## What I've Accomplished

- ✅ Set up my development environment
- ✅ Installed all necessary tools
- ✅ Created my first post
- ✅ Ready to start building amazing static sites!

## Next Steps

- Learn about Jekyll's folder structure
- Explore Liquid templating
- Customize the theme
- Add more content

Happy coding! 🚀
EOF

# Commit your first post
git add .
git commit -m "Add my first Jekyll post"
git push origin main
```

### Recommended Learning Path

Now that your environment is set up, here's your suggested learning journey:

#### Week 1: Jekyll Fundamentals
- [ ] **[Jekyll Documentation](https://jekyllrb.com/docs/)**: Official getting started guide
- [ ] **[Liquid Templating](https://shopify.github.io/liquid/)**: Learn the templating language
- [ ] **[Markdown Guide](https://www.markdownguide.org/)**: Master Markdown syntax
- [ ] **Practice**: Create 3-5 blog posts with different layouts

#### Week 2: Advanced Features
- [ ] **[Collections](https://jekyllrb.com/docs/collections/)**: Organize content beyond posts
- [ ] **[Data Files](https://jekyllrb.com/docs/datafiles/)**: Use YAML/JSON data
- [ ] **[Plugins](https://jekyllrb.com/docs/plugins/)**: Extend Jekyll functionality
- [ ] **Practice**: Build a portfolio section

#### Week 3: Customization and Deployment
- [ ] **[Themes](https://jekyllrb.com/docs/themes/)**: Customize appearance
- [ ] **[GitHub Pages](https://docs.github.com/en/pages)**: Deploy your site
- [ ] **[Custom Domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)**: Set up your own domain
- [ ] **Practice**: Deploy your completed site

### Additional Resources

#### Official Documentation
- **[Jekyll Documentation](https://jekyllrb.com/docs/)**: Comprehensive official guide
- **[GitHub Pages Documentation](https://docs.github.com/en/pages)**: Hosting and deployment
- **[Liquid Documentation](https://shopify.github.io/liquid/)**: Templating language reference

#### Community Resources
- **[Jekyll Talk Forum](https://talk.jekyllrb.com/)**: Community support and discussions
- **[Jekyll Themes](https://jekyllthemes.org/)**: Free and premium themes
- **[Awesome Jekyll](https://github.com/planetjekyll/awesome-jekyll)**: Curated list of Jekyll resources

#### Tools and Extensions
- **[Jekyll Admin](https://github.com/jekyll/jekyll-admin)**: Web-based administration
- **[Jekyll Feed](https://github.com/jekyll/jekyll-feed)**: RSS feed generation
- **[Jekyll SEO Tag](https://github.com/jekyll/jekyll-seo-tag)**: SEO optimization

### Support and Community

If you encounter issues or have questions:

1. **Check the [IT-Journey Issues](https://github.com/bamr87/it-journey/issues)** for known problems
2. **Search [Jekyll Talk Forum](https://talk.jekyllrb.com/)** for community solutions
3. **Create an issue** in the IT-Journey repository with detailed error information
4. **Join our community discussions** in the repository's discussion section

---

## 🏆 Congratulations!

You've successfully set up a professional Jekyll development environment! You now have:

- ✅ **Package management** for easy software installation
- ✅ **Version control** with Git and GitHub integration
- ✅ **Ruby and Jekyll** properly configured
- ✅ **VS Code** optimized for Jekyll development
- ✅ **Local development server** for testing
- ✅ **Troubleshooting knowledge** for common issues

Your machine is now ready for professional static site development. The tools you've installed will serve you well beyond Jekyll - you now have a solid foundation for web development, automation, and collaboration.

**What's Next?** Head over to our [Jekyll Quickstart Guide](./jekyll-quickstart.md) to start building your first real Jekyll project, or explore our [Advanced Jekyll Techniques](./advanced-jekyll.md) guide when you're ready to level up your skills.

Welcome to the Jekyll development community! 🎉

---

*Last updated: July 21, 2025 | For updates to this guide, check the [IT-Journey repository](https://github.com/bamr87/it-journey)*
