---
title: 'Hello macOS: Setting Up the Apple Kingdom'
description: Set up a macOS development environment with Homebrew, Xcode Command Line Tools, and a modern terminal workflow.
author: IT-Journey Team
date: 2026-01-14
lastmod: 2026-01-14
level: '0000'
difficulty: 🟢 Easy
estimated_time: 60-90 minutes
primary_technology: macOS
quest_type: main_quest
quest_series: Init World - Platform Mastery
quest_line: Foundation Path
quest_arc: Platform Mastery Arc
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/init_world/hello-noob/
  - /quests/lvl_000/os-selection/
  unlocks_quests:
  - /quests/vscode-mastery/
  - /quests/level-0000-terminal-fundamentals/
quest_relationships:
  child_quests: []
  sequel_quests:
  - /quests/vscode-mastery/
  parallel_quests:
  - /quests/hello-windows/
  - /quests/hello-linux/linux-fundamentals/
learning_paths:
  primary_paths:
  - Software Development
  - iOS Development
  - Full-Stack Development
  character_classes:
  - 💻 Software Developer
  - 🎨 Digital Artist
  - 🏗️ System Engineer
  skill_trees:
  - macOS Administration
  - Package Management
skill_focus:
- macOS
- terminal
- package-management
- developer-tools
learning_style: hands-on
permalink: /quests/hello-macos/
categories:
- Quests
- Init-World
- macOS
- Development-Environment
tags:
- macos
- homebrew
- iterm2
- terminal
- developer-tools
keywords:
- macos
- homebrew
- terminal
- developer-tools
- init-world
fmContentType: quest
prerequisites:
  knowledge_requirements:
  - Comfortable using Finder and System Settings
  - Basic understanding of command line usage
  system_requirements:
  - macOS 12+ recommended
  - Administrator access for installs
  - Stable internet connection
  skill_level_indicators:
  - Familiar with macOS basics and ready to learn developer tooling
validation_criteria:
  completion_requirements:
  - Install Xcode Command Line Tools
  - Install and verify Homebrew
  - Configure a modern terminal (iTerm2 or similar)
  - Verify Git, SSH, and common utilities
  skill_demonstrations:
  - Can install packages via Homebrew
  - Can navigate the terminal confidently
  knowledge_checks:
  - Understands the role of Xcode CLI tools
  - Can explain what Homebrew does and why it is useful
rewards:
  badges:
  - 🏆 Apple Kingdom Badge
  - ⚡ Homebrew Mastery Achievement
  skills_unlocked:
  - 🛠️ macOS Package Management
  - 🎯 Terminal Configuration
  progression_points: 75
  unlocks_features:
  - Access to VS Code Mastery quest
  - Professional macOS development workflow
draft: false
---
*Welcome, macOS adventurer! This quest transforms your Mac into a professional-grade development workstation. You'll install core tooling, tune your terminal, and validate a clean, repeatable setup.*

## 🎯 Quest Objectives

### Primary Objectives (Required for Quest Completion)
- [ ] **Install Xcode Command Line Tools** - Unlock core developer tooling
- [ ] **Install Homebrew** - Your macOS package manager
- [ ] **Configure a Modern Terminal** - iTerm2 + shell enhancements
- [ ] **Verify Your Toolchain** - Confirm Git, SSH, and common utilities

### Bonus Objectives (Optional)
- [ ] **Shell Customization** - Prompt themes, aliases, and quality-of-life tweaks
- [ ] **Baseline Dev Tools** - VS Code, Node/Python toolchains, and git config

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Comfortable using Finder and System Settings
- [ ] Basic understanding of command line usage

### 🛠️ System Requirements
- [ ] macOS 12+ recommended
- [ ] Administrator access for installs
- [ ] Stable internet connection

## 🌍 Choose Your Adventure Platform

This quest is **macOS-only**. If you're on another OS, start with:
- [Hello Windows](../hello-win/hello-win.md)
- [Hello Linux](../hello-linux/linux-fundamentals.md)
- [Hello Cloud](../hello-cloud/hello-cloud.md)

## 🧙‍♂️ Chapter 1: Install Core Tooling

### ✅ Step 1: Xcode Command Line Tools

```bash
xcode-select --install
```

Verify after installation:

```bash
xcode-select -p
```

### ✅ Step 2: Install Homebrew

Run the official installer:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then validate:

```bash
brew --version
brew doctor
```

### ✅ Step 3: Install Essentials via Scripts

Use the provided helper scripts (review before running):

```bash
./hb-install.sh
./hb-packages.sh
```

## 🧰 Chapter 2: Terminal & Workflow Enhancements

### ✅ Step 4: Install iTerm2

```bash
./iterminate2.sh
```

### ✅ Step 5: Run the macOS setup helper

```bash
./hello-mac.sh
```

This script walks you through common dev tooling checks and config hints.

## 🧪 Chapter 3: Validate Your Setup

Run these checks to confirm your environment:

```bash
git --version
ssh -V
brew list
```

You should see valid versions for each command.

## 🏁 Quest Completion Checklist

- [ ] Xcode Command Line Tools installed
- [ ] Homebrew installed and healthy (`brew doctor`)
- [ ] Terminal upgraded (iTerm2 + shell config)
- [ ] Git/SSH verified

## 🔗 Related Quests

- [Hello n00b](../hello-noob.md)
- [OS Selection](../os-selection.md)
- [VS Code Mastery Quest](../vscode-mastery.md)

## 📚 References & Resources

- [Xcode Command Line Tools - Apple Developer](https://developer.apple.com/xcode/resources/)
- [Homebrew - The Missing Package Manager for macOS](https://brew.sh/)
- [iTerm2 - macOS Terminal Replacement](https://iterm2.com/)
- [Oh My Zsh - Zsh Framework](https://ohmyz.sh/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub SSH Key Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Apple macOS User Guide](https://support.apple.com/guide/mac-help/welcome/mac)
