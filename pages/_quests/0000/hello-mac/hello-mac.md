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
skill_focus:
- macOS
- terminal
- package-management
- developer-tools
learning_style: hands-on
layout: journals
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
/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"
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
