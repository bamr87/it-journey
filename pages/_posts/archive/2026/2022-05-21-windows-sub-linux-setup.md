---
title: Windows Subsystem for Linux (WSL) Setup Guide
author: IT-Journey Team
excerpt: Complete guide to setting up Windows Subsystem for Linux for development environments
description: Step-by-step instructions for installing and configuring WSL on Windows systems
snippet: Transform your Windows machine into a powerful Linux development environment
categories:
  - posts
  - system-administration
tags:
  - windows
  - linux
  - wsl
  - development-environment
  - system-administration
meta: null
draft: false
section: System Administration
lastmod: 2025-10-19T22:33:21.685Z
date: 2022-05-21T23:56:40.448Z
layout: journals
---

# Windows Subsystem for Linux (WSL) Setup Guide

This guide covers the installation and configuration of Windows Subsystem for Linux (WSL) to create a powerful Linux development environment on Windows systems.

## Prerequisites

- Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11
- Administrator privileges on your Windows machine

## Installation Steps

### 1. Install WSL

If WSL is not already installed, use the following commands:

```powershell
# Install WSL with the default Ubuntu distribution
wsl --install

# Update WSL to the latest version
wsl --update
```

### 2. Download and Install Specific Ubuntu Version

For Ubuntu 20.04 specifically:

```powershell
# Download Ubuntu 20.04 package
Invoke-WebRequest -Uri https://aka.ms/wslubuntu2004 -OutFile Ubuntu.appx -UseBasicParsing

# Set WSL version 2 as default (recommended)
wsl --set-default-version 2
```

### 3. Complete Installation

After installation:

1. **Restart your computer** if prompted
2. **Launch Ubuntu** from the Start menu
3. **Create a user account** when prompted
4. **Update the system**:

```bash
sudo apt update && sudo apt upgrade -y
```

## Verification

Verify your WSL installation:

```powershell
# List installed distributions
wsl --list --verbose

# Check WSL version
wsl --version
```

## Next Steps

- Install development tools (`git`, `curl`, `build-essential`)
- Configure your shell (zsh, oh-my-zsh)
- Set up your development environment
- Install Docker Desktop with WSL 2 backend

## Troubleshooting

### Common Issues

- **Virtualization not enabled**: Enable Virtualization in BIOS/UEFI
- **WSL feature not enabled**: Run `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux`
- **Version conflicts**: Use `wsl --set-version <distribution> 2` to upgrade to WSL 2

---

*This guide provides the foundation for setting up a Linux development environment on Windows. WSL 2 offers near-native Linux performance with full system call compatibility.*
