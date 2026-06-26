---
title: "Start: IT-Journey Character Initialization Guide"
updated: 2026-06-13 00:00:00+00:00
created: 2024-02-01 18:05:31+00:00
date: '2024-02-20T09:39:19.000Z'
lastmod: '2026-06-13T00:00:00.000Z'
draft: false
author: bamr87
categories: [Learning]
tags:
  - onboarding
  - setup
  - environment
  - getting-started
excerpt: "The character sheet for the IT-Journey zero — identity, SSH/GPG keys, role-based class selection, and the WSL2 inventory checklist to complete before starting any quest."
description: Initialization scratch sheet for the IT-Journey 'zero' character — identity, class, inventory checklist, and onboarding setup.
keywords:
  - onboarding
  - developer setup
  - WSL2
  - SSH key
  - getting started
---

# Initialize

Every journey needs a starting state. This is the character sheet for the IT-Journey "zero" — the configuration you set once and rarely revisit, but which every subsequent step depends on.

## Identity / Character

Your digital identity is the set of handles and credentials that follow you across systems. Settle on them before you set up anything else — changing them later is expensive.

| Field | Notes |
|---|---|
| **Username** | Lowercase, no spaces. This becomes your GitHub handle, npm org, Docker Hub name. |
| **Email** | Use one for public/professional and one for service signups. |
| **SSH key** | Generate once: `ssh-keygen -t ed25519 -C "your@email.com"`. Add to GitHub, any remote server. |
| **GPG key** | Optional but recommended for signed commits: `gpg --full-generate-key`. |
| **Timezone** | Set your system clock and git config: `git config --global user.timezone "America/Denver"` |

```bash
# Set your git identity globally
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git config --global core.editor "code --wait"
```

## Class / Role

Your "class" is the lens you bring to the technical curriculum. Pick the one closest to where you are now — not where you want to be. You can reclass later.

| Class | Starting Strengths | First Quests |
|---|---|---|
| **Explorer** | Curious, broad exposure, no deep specialization | Bash basics, Git 101, spinning up a VM |
| **Developer** | Writes code, comfortable with one language | Git flow, CI/CD basics, containerization |
| **Admin** | Manages systems, comfortable with infrastructure | Scripting, monitoring, backup strategies |
| **Analyst** | Comfortable with data, Excel-level SQL | Python basics, pandas, Jupyter |
| **Security** | Curious about how things break | OverTheWire Bandit, CTF intro, network basics |

## Inventory

Checklist of tools to install before starting any quest. Each item links to setup docs when they exist.

### 1. Installation — Windows

- [ ] [Windows Subsystem for Linux (WSL2)](https://learn.microsoft.com/windows/wsl/install) — Linux environment on Windows
- [ ] [Windows Terminal](https://aka.ms/terminal) — tabbed terminal with profiles
- [ ] [Git for Windows](https://git-scm.com/download/win) — includes Git Bash as fallback
- [ ] [VS Code](https://code.visualstudio.com/) — editor with WSL2 integration built in

### 2. Create / Import Profile

- [ ] Generate SSH key and add to GitHub
- [ ] Clone your dotfiles repo (or start one): `git clone git@github.com:YOURNAME/dotfiles ~/.dotfiles`
- [ ] Set git global config (name, email, editor — see Identity section above)
- [ ] Install your preferred shell config: `.bashrc`, `.zshrc`, or PowerShell profile

### 3. Synchronize

- [ ] Set up cloud sync for notes (Joplin Cloud, S3, or Dropbox)
- [ ] Enable GitHub sync in VS Code settings
- [ ] Set up password manager if not already running
- [ ] Configure terminal color scheme and font ([Nerd Fonts](https://www.nerdfonts.com/) recommended)

## What Comes Next

Once the inventory is checked off, head to the first quest in the sequence:

- [Quest: Begin Your IT Journey](/quests/0000/begin-your-it-journey/)
- [Quest: Git Basics](/quests/0000/git-basics/)
- [Notes: Take Good Notes](/notes/dev/take-good-notes/)
