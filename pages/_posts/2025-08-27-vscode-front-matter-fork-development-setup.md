---
title: "VSCode Front Matter: Complete Fork & Development Guide"
description: Comprehensive guide to forking, setting up, and extending the VSCode Front Matter CMS extension for content management and development
date: 2025-08-27T01:45:00.000Z
preview: Master the complete workflow for contributing to VSCode Front Matter - from forking to feature development
tags:
   - vscode-extension
   - front-matter-cms
   - development-setup
   - open-source-contribution
   - content-management
   - fork-workflow
   - typescript
   - webpack
categories:
   - Development
   - Guides
   - IDE-Setup
   - Open Source
   - Tools
sub-title: "From Fork to Feature: Your Complete Development Journey"
excerpt: Step-by-step guide to fork, setup, and extend the powerful VSCode Front Matter CMS extension for enhanced content management workflows
snippet: Transform your content management experience by contributing to the VSCode Front Matter ecosystem
author: IT-Journey Team
layout: journals
keywords:
   primary:
      - vscode-front-matter
      - extension-development
      - cms-setup
      - fork-workflow
   secondary:
      - typescript-development
      - webpack-configuration
      - content-management-system
      - open-source-contribution
      - development-environment
lastmod: 2025-09-27T19:59:13.800Z
permalink: /posts/vscode-front-matter-fork-development-setup/
attachments: ""
comments: true
difficulty: 🟡 Intermediate
estimated_reading_time: 20-25 minutes
prerequisites:
   - Basic Git and GitHub knowledge
   - Node.js and npm familiarity
   - VS Code extension development understanding
   - TypeScript/JavaScript experience
learning_outcomes:
   - 🎯 Successfully fork and setup VSCode Front Matter for development
   - ⚡ Master the development workflow and testing procedures
   - 🛠️ Understand the extension architecture and build system
   - 🔗 Contribute effectively to the open-source project
validation_methods:
   - Extension loads successfully in development mode
   - All build processes complete without errors
   - Dashboard and panel interfaces are accessible
   - Hot-reload development workflow functions properly
---

## Introduction

VSCode Front Matter is a powerful Content Management System (CMS) that runs directly within Visual Studio Code, transforming your editor into a comprehensive content management platform. Whether you're managing a blog, documentation site, or any markdown-based content, this extension provides an intuitive interface for creating, editing, and organizing your content.

### 🌟 Why Fork and Extend VSCode Front Matter?

The VSCode Front Matter extension offers incredible extensibility for content creators and developers who want to:

- **Customize Content Workflows**: Tailor the CMS to your specific content management needs
- **Add New Features**: Implement functionality that enhances your team's productivity
- **Fix Issues**: Contribute bug fixes and improvements to the community
- **Learn Extension Development**: Understand how complex VSCode extensions are architected

### 🎯 What You'll Accomplish

By the end of this guide, you'll have:

- A fully functional development environment for VSCode Front Matter
- Understanding of the extension's architecture and build system
- Ability to make changes and test them in real-time
- Knowledge of the contribution workflow for open-source projects

### 📋 Before We Begin

Ensure you have the following installed:

- **Node.js** (v18 or higher)
- **npm** or **yarn** package manager
- **Git** for version control
- **Visual Studio Code** with extension development capabilities
- **GitHub account** for forking and contributions

---

## 🍴 Phase 1: Forking and Initial Setup

### Step 1: Fork the Repository

**Objective**: Create your own copy of the VSCode Front Matter repository

**Implementation**:

1. **Navigate to the Original Repository**:

   ```bash
   # Visit the original repository
   open https://github.com/estruyf/vscode-front-matter
   ```

2. **Fork via GitHub Interface**:
   - Click the "Fork" button in the top-right corner
   - Select your GitHub account as the destination
   - Keep the repository name as `vscode-front-matter`
   - Ensure "Copy the main branch only" is checked

3. **Verify Fork Creation**:

   ```bash
   # Your fork will be available at:
   # https://github.com/YOUR_USERNAME/vscode-front-matter
   ```

**Expected Result**: You now have a personal fork of the repository under your GitHub account.

### Step 2: Clone Your Fork Locally

**Objective**: Set up the local development environment

**Implementation**:

```bash
# Clone your fork to your local machine
git clone https://github.com/YOUR_USERNAME/vscode-front-matter.git

# Navigate to the project directory
cd vscode-front-matter

# Verify the clone was successful
ls -la
```

**Expected Result**: A local copy of your forked repository with all project files.

### Step 3: Configure Git Remotes

**Objective**: Set up proper remote tracking for upstream synchronization

**Implementation**:

```bash
# Add the original repository as upstream
git remote add upstream https://github.com/estruyf/vscode-front-matter.git

# Verify remote configuration
git remote -v
```

**Expected Output**:

```bash
origin    https://github.com/YOUR_USERNAME/vscode-front-matter.git (fetch)
origin    https://github.com/YOUR_USERNAME/vscode-front-matter.git (push)
upstream  https://github.com/estruyf/vscode-front-matter.git (fetch)
upstream  https://github.com/estruyf/vscode-front-matter.git (push)
```

**Troubleshooting**: If you see authentication errors, ensure your GitHub credentials are properly configured.

---

## 🔧 Phase 2: Development Environment Configuration

### Step 4: Install Dependencies

**Objective**: Set up all required packages for development

**Implementation**:

```bash
# Install all project dependencies
npm install

# Alternative using yarn
# yarn install
```

**Expected Result**: All dependencies from `package.json` are installed in `node_modules/`.

**Common Issues**:

- **Node Version Mismatch**: Ensure you're using Node.js v18+
- **Network Issues**: Try `npm install --verbose` for detailed logging
- **Permission Errors**: Use `sudo` only if absolutely necessary (not recommended)

### Step 5: Understand Project Structure

**Objective**: Familiarize yourself with the codebase organization

**Project Architecture**:

```text
vscode-front-matter/
├── src/                    # Main source code
│   ├── commands/          # VS Code commands
│   ├── components/        # React components
│   ├── dashboard/         # Dashboard interface
│   ├── panels/           # Side panel components
│   ├── services/         # Core business logic
│   └── utils/            # Utility functions
├── webpack/              # Build configuration
│   ├── extension.config.js    # Extension build config
│   ├── dashboard.config.js    # Dashboard build config
│   └── panel.config.js        # Panel build config
├── public/               # Static assets
├── dist/                # Built extension files
├── package.json         # Project configuration
└── README.md           # Project documentation
```

### Step 6: Build System Overview

**Objective**: Understand the multi-target build system

**Build Targets**:

- **Extension**: The core VS Code extension (`src/extension.ts`)
- **Dashboard**: React-based CMS interface (`src/dashboard/`)
- **Panel**: Side panel React components (`src/panels/`)

**Key npm Scripts**:

```bash
# Development with hot reload
npm run dev:ext           # Start all development servers

# Individual builds
npm run dev:build:ext     # Build extension only
npm run dev:build:dashboard  # Build dashboard only
npm run dev:build:panel   # Build panel only

# Production builds
npm run vscode:prepublish # Full production build
npm run prod:ext         # Production extension build

# Utilities
npm run clean            # Clean dist directory
npm run lint             # Run ESLint
npm run prettier         # Format code
```

---

## ⚡ Phase 3: Development Workflow Setup

### Step 7: Start Development Environment

**Objective**: Launch the complete development environment with hot-reload

**Implementation**:

```bash
# Start the development environment
npm run dev:ext
```

**What This Does**:

1. **Cleans** the `dist/` directory
2. **Generates** localization files
3. **Starts** three parallel processes:
   - Extension build with watch mode
   - Dashboard development server (<http://localhost:9000/>)
   - Panel development server (<http://localhost:9001/>)

**Expected Output**:

```text
> vscode-front-matter-beta@10.9.0 dev:ext
> npm run clean && npm run localization:generate && npm-run-all --parallel watch:*

<i> [webpack-dev-server] Project is running at:
<i> [webpack-dev-server] Loopback: http://localhost:9000/
<i> [webpack-dev-server] Project is running at:
<i> [webpack-dev-server] Loopback: http://localhost:9001/

extension (webpack 5.90.1) compiled successfully
dashboard (webpack 5.90.1) compiled successfully  
panel (webpack 5.90.1) compiled successfully
```

### Step 8: Test Extension in Development Mode

**Objective**: Verify the extension loads and functions correctly

**Implementation**:

1. **Launch Extension Development Host**:
   - Press `F5` in VS Code **OR**
   - Go to Run and Debug (`Cmd+Shift+D`)
   - Select "Launch Extension" and click the play button

2. **Verify Extension Loading**:

   ```text
   # In the Extension Development Host window:
   # Press Cmd+Shift+P (macOS) or Ctrl+Shift+P (Windows/Linux)
   # Type: "Front Matter"
   # You should see multiple Front Matter commands
   ```

3. **Test Core Functionality**:
   - **Dashboard Access**: Command "Front Matter: Open dashboard"
   - **Panel Access**: Look for Front Matter icon in sidebar
   - **Direct URLs**:
     - Dashboard: <http://localhost:9000/>
     - Panel: <http://localhost:9001/>

**Success Criteria**:

- [ ] Extension Development Host opens without errors
- [ ] Front Matter commands appear in Command Palette
- [ ] Dashboard opens and displays interface
- [ ] Panel loads in sidebar
- [ ] Development servers respond on ports 9000 and 9001

---

## 🛠️ Phase 4: Development and Testing Workflow

### Step 9: Making Your First Change

**Objective**: Understand the development workflow by making a simple modification

**Example Change - Add a Custom Command**:

1. **Create a New Command File**:
   ```typescript
   // src/commands/myCustomCommand.ts
   import { window } from 'vscode';
   
   export const myCustomCommand = () => {
     window.showInformationMessage('Hello from my custom Front Matter command!');
   };
   ```

2. **Register the Command**:
   ```typescript
   // In src/extension.ts (find the activate function)
   import { myCustomCommand } from './commands/myCustomCommand';
   
   // Add to the commands registration section:
   const myCustomCmd = commands.registerCommand('frontMatter.myCustomCommand', myCustomCommand);
   subscriptions.push(myCustomCmd);
   ```

3. **Add Command to Package.json**:
   ```json
   // In package.json, find the "contributes.commands" section
   {
     "command": "frontMatter.myCustomCommand",
     "title": "My Custom Command",
     "category": "Front Matter"
   }
   ```

### Step 10: Testing Changes

**Objective**: Verify your modifications work correctly

**Testing Process**:

1. **Automatic Rebuild**: Webpack watch mode automatically rebuilds when you save files

2. **Reload Extension**: In the Extension Development Host:
   - Press `Cmd+R` (macOS) or `Ctrl+R` (Windows/Linux)
   - Or use Command Palette: "Developer: Reload Window"

3. **Test Your Change**:
   ```
   # In Extension Development Host:
   # Cmd+Shift+P → "Front Matter: My Custom Command"
   # Should show your custom message
   ```

**Debugging Tips**:
- **Breakpoints**: Set breakpoints in your TypeScript source files
- **Console Logging**: Use `console.log()` - output appears in the original VS Code's Debug Console
- **Error Inspection**: Check the Developer Tools in Extension Development Host (`Help → Toggle Developer Tools`)

### Step 11: Working with Dashboard and Panel

**Objective**: Understand how to modify the React-based interfaces

**Dashboard Development**:
```bash
# Dashboard runs at http://localhost:9000/
# Source files in: src/dashboard/
# Main entry point: src/dashboard/index.tsx
```

**Panel Development**:
```bash
# Panel runs at http://localhost:9001/  
# Source files in: src/panels/
# Main entry point: src/panels/index.tsx
```

**Hot Reload**: Both dashboard and panel support hot module replacement - changes appear immediately in the browser.

---

## 🔍 Phase 5: Advanced Development Techniques

### Step 12: Understanding the Build System

**Objective**: Master the webpack configuration for different targets

**Webpack Configurations**:

1. **Extension Config** (`webpack/extension.config.js`):
   - Builds the VS Code extension backend
   - Target: Node.js environment
   - Output: `dist/extension.js`

2. **Dashboard Config** (`webpack/dashboard.config.js`):
   - Builds the React dashboard app
   - Target: Browser environment  
   - Development server with HMR
   - Output: `dist/dashboard.main.js`

3. **Panel Config** (`webpack/panel.config.js`):
   - Builds the React panel components
   - Target: VS Code webview environment
   - Development server with HMR
   - Output: `dist/panel.main.js`

### Step 13: Localization Support

**Objective**: Understand and work with the extension's localization system

**Localization Workflow**:

```bash
# Generate localization enum
npm run localization:generate

# Find missing localization keys
npm run localization:find

# Sync localization files
npm run localization:sync
```

**Adding New Localizable Strings**:
1. Add key to `package.nls.json`
2. Add translations to language-specific files (`package.nls.de.json`, etc.)
3. Use in code: `vscode.l10n.t('your.key')`

### Step 14: Testing Strategies

**Objective**: Implement comprehensive testing for your changes

**Testing Approaches**:

1. **Unit Testing**: Test individual functions and components
2. **Integration Testing**: Test command interactions and workflows  
3. **Manual Testing**: Test in real VS Code environment
4. **User Scenario Testing**: Test complete user workflows

**Test File Structure**:
```
src/
├── commands/
│   ├── myCommand.ts
│   └── __tests__/
│       └── myCommand.test.ts
└── utils/
    ├── helper.ts
    └── __tests__/
        └── helper.test.ts
```

---

## 🚀 Phase 6: Production Build and Deployment

### Step 15: Production Build Process

**Objective**: Create optimized builds for distribution

**Production Build Commands**:

```bash
# Complete production build
npm run vscode:prepublish

# Individual production builds
npm run prod:ext         # Extension only
npm run prod:dashboard   # Dashboard only  
npm run prod:panel      # Panel only
```

**Build Verification**:
```bash
# Check build output
ls -la dist/

# Expected files:
# - extension.js (main extension)
# - dashboard.main.js (dashboard bundle)
# - panel.main.js (panel bundle)
# - Various asset files
```

### Step 16: Extension Packaging

**Objective**: Package the extension for installation or distribution

**Prerequisites**:
```bash
# Install VS Code Extension Manager
npm install -g vsce
```

**Packaging Process**:
```bash
# Package the extension
vsce package

# This creates a .vsix file that can be installed
# Output: vscode-front-matter-beta-X.X.X.vsix
```

**Testing Packaged Extension**:
```bash
# Install the packaged extension
code --install-extension vscode-front-matter-beta-X.X.X.vsix

# Uninstall when testing is complete
code --uninstall-extension eliostruyf.vscode-front-matter-beta
```

---

## 📚 Phase 7: Contributing Back to the Project

### Step 17: Preparing Your Contribution

**Objective**: Follow best practices for open-source contributions

**Pre-Contribution Checklist**:
- [ ] **Code Quality**: Run linting and formatting
  ```bash
  npm run lint
  npm run prettier
  ```
- [ ] **Testing**: Ensure all tests pass
- [ ] **Documentation**: Update relevant documentation
- [ ] **Commit Messages**: Follow conventional commit format

**Creating a Feature Branch**:
```bash
# Create and switch to a new feature branch
git checkout -b feature/your-feature-name

# Make your changes and commit
git add .
git commit -m "feat: add custom command functionality"

# Push to your fork
git push origin feature/your-feature-name
```

### Step 18: Keeping Your Fork Updated

**Objective**: Maintain synchronization with the upstream repository

**Sync Workflow**:
```bash
# Fetch latest changes from upstream
git fetch upstream

# Switch to main branch
git checkout main

# Merge upstream changes
git merge upstream/main

# Push updates to your fork
git push origin main

# Update your feature branch (if needed)
git checkout feature/your-feature-name
git rebase main
```

### Step 19: Creating Pull Requests

**Objective**: Submit your contributions for review

**Pull Request Process**:

1. **GitHub Interface**:
   - Navigate to your fork on GitHub
   - Click "Compare & pull request"
   - Select base: `estruyf/vscode-front-matter` main
   - Select compare: `bamr87/vscode-front-matter` feature-branch

2. **PR Description Template**:
   ```markdown
   ## Description
   Brief description of the changes made.

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Tested locally
   - [ ] Added/updated tests
   - [ ] Verified in Extension Development Host

   ## Screenshots (if applicable)
   Include screenshots for UI changes.
   ```

---

## ✅ Validation and Practice

### Knowledge Check

Before proceeding, ensure you understand:

- [ ] **Fork Workflow**: How to fork, clone, and sync repositories
- [ ] **Development Environment**: Setting up and running the dev servers
- [ ] **Build System**: Understanding webpack configurations and build targets
- [ ] **Testing Process**: How to test changes in Extension Development Host
- [ ] **Contribution Process**: Creating branches, commits, and pull requests

### 🎮 Practice Exercises

#### Exercise 1: Environment Setup Verification
**Objective**: Confirm your development environment is fully functional

**Challenge**: 
1. Fork the repository (if not already done)
2. Set up the development environment
3. Successfully launch the Extension Development Host
4. Access both dashboard (localhost:9000) and panel (localhost:9001)

**Success Criteria**:
- [ ] All webpack builds complete without errors
- [ ] Extension loads in Development Host
- [ ] Front Matter commands appear in Command Palette
- [ ] Dashboard interface is accessible and functional
- [ ] Panel loads correctly in sidebar

#### Exercise 2: Simple Feature Implementation
**Objective**: Implement a basic feature to understand the development workflow

**Challenge**: Create a new command that displays workspace statistics

**Requirements**:
1. Add a new command file: `src/commands/workspaceStats.ts`
2. Implement functionality to count files in workspace
3. Register the command in the extension
4. Add command definition to package.json
5. Test the feature in Extension Development Host

**Implementation Guidance**:
```typescript
// Example implementation structure
import { workspace, window } from 'vscode';

export const showWorkspaceStats = async () => {
  const workspaceFolders = workspace.workspaceFolders;
  if (!workspaceFolders) {
    window.showInformationMessage('No workspace folder found');
    return;
  }
  
  // Implement file counting logic
  // Display results to user
};
```

### 🔍 Self-Assessment Questions

1. **Architecture Understanding**: How do the three webpack configurations work together?
2. **Development Workflow**: What happens when you make a change to a TypeScript file?
3. **Testing Strategy**: How would you test a change that affects both the extension and dashboard?
4. **Contribution Workflow**: What steps are required to contribute a bug fix?

---

## 🔧 Troubleshooting Guide

### Common Issues and Solutions

#### Issue 1: Extension Fails to Load in Development Host
**Symptoms**: Extension Development Host opens but Front Matter commands don't appear
**Causes**: Build errors, configuration issues, or dependency problems
**Solutions**:
```bash
# Check for build errors
npm run dev:ext

# Clear and rebuild
npm run clean
npm run build:ext

# Check VS Code Developer Tools
# In Extension Development Host: Help → Toggle Developer Tools
```

#### Issue 2: Hot Reload Not Working
**Symptoms**: Changes to code don't reflect in the running extension
**Diagnosis**: Webpack watch mode issues or file permission problems
**Resolution**:
```bash
# Restart the development server
# Stop with Ctrl+C, then restart
npm run dev:ext

# Check file permissions
ls -la src/

# Manually reload Extension Development Host
# Press Cmd+R in the Extension Development Host window
```

#### Issue 3: Dashboard/Panel Not Loading
**Symptoms**: Localhost:9000 or localhost:9001 show errors or won't load
**Causes**: Port conflicts, webpack-dev-server issues, or build failures
**Solutions**:
```bash
# Check if ports are in use
lsof -i :9000
lsof -i :9001

# Kill conflicting processes
kill -9 <PID>

# Restart development servers
npm run dev:ext
```

#### Issue 4: TypeScript Compilation Errors
**Symptoms**: Build fails with TypeScript errors
**Causes**: Type mismatches, missing imports, or configuration issues
**Resolution**:
```bash
# Run TypeScript compiler directly
npx tsc --noEmit

# Check for missing dependencies
npm install

# Verify TypeScript configuration
cat tsconfig.json
```

#### Issue 5: Git Remote Issues
**Symptoms**: Cannot push to fork or sync with upstream
**Causes**: Authentication problems or incorrect remote configuration
**Solutions**:
```bash
# Verify remote configuration
git remote -v

# Reset origin to your fork
git remote set-url origin https://github.com/YOUR_USERNAME/vscode-front-matter.git

# Re-add upstream
git remote add upstream https://github.com/estruyf/vscode-front-matter.git

# Test authentication
git push origin main
```

### Performance Optimization Tips

#### Build Performance
- **Incremental Builds**: Use `npm run dev:ext` for development
- **Selective Building**: Use individual build commands when working on specific components
- **Clean Builds**: Run `npm run clean` when switching between development and production builds

#### Development Workflow
- **Extension Host Management**: Close unused Extension Development Host windows
- **Resource Monitoring**: Monitor memory usage during long development sessions
- **Code Organization**: Keep changes focused to minimize rebuild times

---

## 🚀 Next Steps and Advanced Topics

### Immediate Next Steps

After mastering this setup, consider exploring:

1. **Advanced Features**: Implement complex content management workflows
2. **Custom Themes**: Create custom dashboard themes and styling
3. **API Integration**: Connect to external content management systems
4. **Automation**: Build automated content deployment workflows

### 🔮 Advanced Development Paths

#### Path 1: Extension Architecture Mastery
- **Command System**: Deep dive into VS Code command architecture
- **Webview Communication**: Master extension-to-webview messaging
- **State Management**: Implement complex application state handling
- **Performance Optimization**: Optimize extension startup and runtime performance

#### Path 2: React Component Development
- **Component Library**: Build reusable UI components for the dashboard
- **State Management**: Implement Redux or Context API for complex state
- **Testing**: Add comprehensive React component testing
- **Accessibility**: Ensure WCAG compliance for all UI components

#### Path 3: Content Management Innovation
- **Workflow Automation**: Build automated content publishing pipelines
- **Integration Development**: Connect to headless CMS platforms
- **AI Enhancement**: Integrate AI-powered content suggestions
- **Analytics**: Implement content performance tracking

### 🌐 Community and Resources

#### Documentation and Learning
- **Official Docs**: [Front Matter Documentation](https://frontmatter.codes)
- **VS Code Extension API**: [Official Extension Documentation](https://code.visualstudio.com/api)
- **TypeScript**: [Official TypeScript Handbook](https://www.typescriptlang.org/docs/)
- **React**: [Official React Documentation](https://react.dev)

#### Community Support
- **GitHub Discussions**: Engage with the Front Matter community
- **Discord/Slack**: Join extension development communities
- **Stack Overflow**: Search for VS Code extension development questions
- **Reddit**: r/vscode and related development communities

#### Contributing Guidelines
- **Code Style**: Follow the project's ESLint and Prettier configurations
- **Testing Standards**: Include tests for new functionality
- **Documentation**: Update relevant documentation with changes
- **Issue Tracking**: Link pull requests to relevant GitHub issues

---

*This comprehensive guide provides the foundation for contributing to the VSCode Front Matter ecosystem. Each step builds upon previous knowledge while introducing new concepts and techniques essential for successful extension development. Remember that mastery comes through practice, experimentation, and active participation in the open-source community.*

## Summary

You've now learned how to:
- ✅ Fork and set up the VSCode Front Matter development environment
- ✅ Understand the multi-target build system architecture
- ✅ Implement changes and test them effectively
- ✅ Navigate the contribution workflow for open-source projects
- ✅ Troubleshoot common development issues
- ✅ Optimize your development workflow for productivity

The VSCode Front Matter extension represents the cutting edge of in-editor content management, and your contributions can help shape the future of developer productivity tools. Whether you're fixing bugs, adding features, or improving documentation, every contribution makes the tool better for the entire community.

Continue your journey by exploring advanced topics, engaging with the community, and building innovative solutions that leverage the power of this exceptional CMS platform.

## Tools & Environment

This section provides an overview of the tools and environment used in the development of the VSCode Front Matter extension.

### Development Tools

| Tool                | Purpose                                      |
|----------------------|----------------------------------------------|
| **Node.js**         | JavaScript runtime for building the extension |
| **npm** or **yarn** | Package managers for managing dependencies    |
| **Git**              | Version control for tracking changes         |
| **Visual Studio Code** | Code editor with extension development support |

### Recommended Extensions for VS Code

| Extension                       | Purpose                                      |
|---------------------------------|----------------------------------------------|
| **ESLint**                     | JavaScript and TypeScript linting            |
| **Prettier - Code formatter** | Code formatting for consistency              |
| **GitLens**                   | Enhanced Git capabilities                    |
| **Debugger for Chrome**       | Debugging JavaScript in Chrome               |
| **Path Intellisense**         | Autocompletes filenames in quotes            |

### Environment Variables

The extension may use the following environment variables:

| Variable                | Description                                   |
|-------------------------|-----------------------------------------------|
| `NODE_ENV`              | Set to `development` or `production`         |
| `PORT`                  | Port for the development server (default: 9000) |
| `DEBUG`                 | Enable debug logging                          |

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 4 GB, 8 GB or more recommended
- **Disk Space**: Minimum 100 MB free space for the project and dependencies

### Setting Up the Development Environment

1. **Install Node.js**: Download and install from [Node.js official website](https://nodejs.org/).
2. **Install Git**: Download and install from [Git official website](https://git-scm.com/).
3. **Clone the Repository**: Follow the instructions in Phase 1, Step 2.
4. **Install Dependencies**: Run `npm install` or `yarn install` in the project directory.
5. **Start the Development Server**: Run `npm run dev:ext` to start the development environment.

### Common Development Commands

| Command                        | Description                                   |
|-------------------------------|-----------------------------------------------|
| `npm run dev:ext`             | Start the development environment             |
| `npm run build:ext`          | Build the extension for development           |
| `npm run prod:ext`           | Build the extension for production            |
| `npm run clean`              | Clean the output directory                    |
| `npm run lint`               | Run the linter to check for code issues      |
| `npm run prettier`           | Format the codebase using Prettier           |

### Troubleshooting Environment Issues

- **Build Fails**: Ensure all dependencies are installed and the correct Node.js version is being used.
- **Extension Doesn't Load**: Check the Output and Debug Console in VS Code for error messages.
- **Port Conflicts**: If the development server port is in use, update the `PORT` environment variable and restart the server.

### Additional Resources

- **Node.js Documentation**: [Node.js Docs](https://nodejs.org/en/docs/)
- **npm Documentation**: [npm Docs](https://docs.npmjs.com/)
- **Git Documentation**: [Git Docs](https://git-scm.com/doc)
- **Visual Studio Code Documentation**: [VS Code Docs](https://code.visualstudio.com/docs)

---

This section provides essential information about the tools and environment used in the development of the VSCode Front Matter extension. Proper setup and understanding of these tools are crucial for effective development and contribution to the project.
