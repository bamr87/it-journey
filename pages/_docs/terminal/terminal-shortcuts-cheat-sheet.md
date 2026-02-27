---
title: "Essential Terminal Shortcuts: macOS, Linux & Windows Cheat Sheet"
description: "Complete reference guide for terminal keyboard shortcuts across macOS, Linux, and Windows. Master command line navigation, editing, and productivity shortcuts for Bash, Zsh, and PowerShell."
date: 2025-12-20T00:00:00.000Z
lastmod: 2025-12-20T00:00:00.000Z
author: "IT-Journey Team"
permalink: /docs/terminal-shortcuts-cheat-sheet/
tags:
    - terminal
    - shortcuts
    - bash
    - zsh
    - powershell
    - command-line
    - productivity
    - reference
categories:
    - Documentation
    - Terminal
    - Reference
keywords:
    primary:
        - terminal shortcuts
        - command line shortcuts
        - bash shortcuts
    secondary:
        - zsh shortcuts
        - powershell shortcuts
        - keyboard shortcuts terminal
        - terminal navigation
        - it-journey
excerpt: "Master terminal productivity with this comprehensive keyboard shortcuts reference for macOS, Linux, and Windows command line interfaces."
preview: "Complete terminal shortcuts cheat sheet - boost your command line productivity across all platforms"
difficulty: "🟢 Easy"
estimated_time: "15 minutes to read"
draft: false
---

# ⌨️ Essential Terminal Shortcuts Cheat Sheet

> **Master the command line** with these essential keyboard shortcuts for macOS Terminal, Linux shells (Bash/Zsh), and Windows PowerShell/Command Prompt.

---

## 📋 Quick Reference Card

| Action | macOS/Linux | Windows PowerShell |
|--------|-------------|-------------------|
| **Clear screen** | `Ctrl + L` | `Ctrl + L` or `cls` |
| **Cancel command** | `Ctrl + C` | `Ctrl + C` |
| **Exit terminal** | `Ctrl + D` | `exit` |
| **Previous command** | `↑` or `Ctrl + P` | `↑` |
| **Search history** | `Ctrl + R` | `Ctrl + R` |

---

## 🍎 macOS & Linux Terminal Shortcuts

### Navigation Shortcuts

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl + A` | **Beginning of line** | Move cursor to start of command |
| `Ctrl + E` | **End of line** | Move cursor to end of command |
| `Ctrl + B` | **Back one character** | Move left (same as ← arrow) |
| `Ctrl + F` | **Forward one character** | Move right (same as → arrow) |
| `Alt + B` | **Back one word** | Jump to previous word |
| `Alt + F` | **Forward one word** | Jump to next word |
| `Ctrl + XX` | **Toggle position** | Switch between cursor and start |

### Editing Shortcuts

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl + U` | **Cut to beginning** | Delete from cursor to line start |
| `Ctrl + K` | **Cut to end** | Delete from cursor to line end |
| `Ctrl + W` | **Cut word before** | Delete word before cursor |
| `Alt + D` | **Cut word after** | Delete word after cursor |
| `Ctrl + Y` | **Paste (yank)** | Paste last cut text |
| `Ctrl + T` | **Transpose characters** | Swap character with previous |
| `Alt + T` | **Transpose words** | Swap word with previous |
| `Alt + U` | **Uppercase word** | Convert word to UPPERCASE |
| `Alt + L` | **Lowercase word** | Convert word to lowercase |
| `Alt + C` | **Capitalize word** | Capitalize first letter |

### History Shortcuts

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl + R` | **Reverse search** | Search command history backwards |
| `Ctrl + S` | **Forward search** | Search command history forwards |
| `Ctrl + G` | **Exit search** | Cancel history search |
| `Ctrl + P` | **Previous command** | Go to previous history entry |
| `Ctrl + N` | **Next command** | Go to next history entry |
| `!!` | **Repeat last** | Execute last command |
| `!$` | **Last argument** | Use last argument of previous command |
| `!*` | **All arguments** | Use all arguments of previous command |
| `!string` | **History match** | Run last command starting with "string" |

### Screen Control

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl + L` | **Clear screen** | Clear terminal (preserves current line) |
| `Ctrl + S` | **Pause output** | Freeze terminal output |
| `Ctrl + Q` | **Resume output** | Unfreeze terminal output |

### Process Control

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl + C` | **Cancel/Interrupt** | Stop current command |
| `Ctrl + Z` | **Suspend** | Suspend current process (use `fg` to resume) |
| `Ctrl + D` | **Exit/EOF** | Exit shell or send end-of-file |

---

## 🪟 Windows PowerShell Shortcuts

### Navigation Shortcuts

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Home` | **Beginning of line** | Move cursor to start |
| `End` | **End of line** | Move cursor to end |
| `Ctrl + ←` | **Back one word** | Jump to previous word |
| `Ctrl + →` | **Forward one word** | Jump to next word |

### Editing Shortcuts

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl + Backspace` | **Delete word before** | Delete word before cursor |
| `Ctrl + Delete` | **Delete word after** | Delete word after cursor |
| `Escape` | **Clear line** | Clear current input line |
| `Insert` | **Toggle insert mode** | Switch between insert/overwrite |

### History Shortcuts

| Shortcut | Action | Description |
|----------|--------|-------------|
| `↑` / `↓` | **Browse history** | Navigate through command history |
| `Ctrl + R` | **Reverse search** | Search history (PSReadLine) |
| `F7` | **History window** | Show command history popup |
| `F8` | **Search history** | Search history by prefix |
| `F9` | **Run by number** | Run command by history number |

### Screen Control

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl + L` | **Clear screen** | Clear terminal screen |
| `Ctrl + Home` | **Clear scroll** | Clear scrollback buffer |

---

## 🔥 Power User Tips

### Bash/Zsh Bang Commands

```bash
# Repeat last command
!!

# Repeat with sudo
sudo !!

# Last argument of previous command
cd !$

# All arguments of previous command
echo !*

# Run command #42 from history
!42

# Run last command starting with "git"
!git

# Run last command containing "docker"
!?docker?
```

### History Expansion

```bash
# Show history with line numbers
history

# Show last 10 commands
history 10

# Execute command by number
!123

# Replace and execute
^old^new^    # Replace 'old' with 'new' in last command
```

### Directory Navigation Shortcuts

```bash
# Go to home directory
cd ~
cd

# Go to previous directory
cd -

# Go up one level
cd ..

# Go up multiple levels
cd ../..
cd ../../..

# Push/Pop directories (Bash/Zsh)
pushd /some/path
popd
```

---

## 🎯 Platform-Specific Notes

### macOS Terminal

- **Option key**: Use `Option` instead of `Alt` for word navigation
- **Terminal app settings**: Enable "Use Option as Meta key" in Preferences → Profiles → Keyboard
- **iTerm2 users**: Most shortcuts work the same, with additional customization options

### Linux (Bash/Zsh)

- **Alt key shortcuts**: May require terminal emulator configuration
- **Zsh users**: Many shortcuts are the same, with additional Zsh-specific features
- **Tmux/Screen users**: Prefix key may intercept some shortcuts

### Windows PowerShell

- **PSReadLine module**: Enables Bash-like shortcuts in PowerShell
- **Windows Terminal**: Supports more shortcuts than legacy CMD
- **Install PSReadLine**: `Install-Module PSReadLine -Force`

---

## 📚 Additional Resources

### Learn More
- [GNU Readline Documentation](https://tiswww.case.edu/php/chet/readline/rltop.html)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
- [PowerShell PSReadLine](https://docs.microsoft.com/en-us/powershell/module/psreadline/)

### Related Quests
- [Terminal Fundamentals Quest](/quests/level-0000-terminal-fundamentals/)
- [Git Basics Quest](/quests/level-0000-git-basics/)
- [VS Code Mastery Quest](/quests/level-0000-vscode-mastery-quest/)

---

## 🖨️ Printable Cheat Sheet

**Download the printable PDF version**: [Coming Soon]

---

*Pro tip: Print this cheat sheet and keep it next to your keyboard until these shortcuts become muscle memory!*

---

**Last Updated**: December 2025 | **Author**: IT-Journey Team

*Found this helpful? Share it with fellow developers! 🚀*
