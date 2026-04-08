---
title: Wargames — Security Challenges
description: Curated security wargames from the OverTheWire community. Learn and practice security concepts through gamified challenges.
permalink: /docs/wargames/
date: 2025-01-27T00:00:00.000Z
lastmod: 2026-04-07T02:46:45.136Z
categories:
  - wargames
tags:
  - security
  - wargames
  - linux
  - ctf
  - cybersecurity
toc_sticky: true
source_repo: https://github.com/OverTheWireOrg/OverTheWire-website
source_name: overthewire
license: MIT
---

# Wargames — Security Challenges

> **Source:** This section aggregates content from the [OverTheWire](https://overthewire.org/wargames/) community project ([MIT License](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original site to play the games live via SSH.

## What Are Wargames?

Wargames are a series of security-focused challenges offered by the [OverTheWire](https://overthewire.org/) community. They teach security concepts in a gamified, progressive format — starting from basic Unix/Linux commands and building up to advanced exploitation techniques.

Each wargame consists of levels that must be completed in order. You connect via SSH to a server and use your skills to find the password for the next level.

## Available Games

### Beginner

| Game | Focus | Description |
|------|-------|-------------|
| **Bandit** | Linux Basics | Learn basic Unix commands, SSH, and file manipulation |
| **Leviathan** | Basic Exploitation | Simple setuid binaries and reverse engineering |
| **Krypton** | Cryptography | Classical ciphers (Caesar, Vigenere, frequency analysis) |

### Intermediate

| Game | Focus | Description |
|------|-------|-------------|
| **Natas** | Web Security | Server-side web vulnerabilities (injection, auth bypass) |
| **Narnia** | Buffer Overflows | Stack-based buffer overflow exploitation |
| **Behemoth** | Binary Analysis | More advanced binary exploitation |

### Advanced

| Game | Focus | Description |
|------|-------|-------------|
| **Utumno** | Advanced Exploitation | Complex binary challenges |
| **Maze** | Advanced Topics | Maze-like binary challenges |
| **Vortex** | Systems Programming | Low-level systems and exploitation |
| **Manpage** | Documentation Skills | Reading and understanding man pages |

## How to Get Started

1. **Start with Bandit** — It teaches the basics you'll need for every other game
2. **Connect via SSH**: `ssh bandit0@bandit.labs.overthewire.org -p 2220` (password: `bandit0`)
3. **Progress through levels** — Each level's password unlocks the next
4. **Take notes** — Document your approach for each level as a learning exercise

## About This Content

This documentation is automatically aggregated from the [OverTheWire-website repository](https://github.com/OverTheWireOrg/OverTheWire-website) using the IT-Journey docs aggregation pipeline. The content is transformed to fit the IT-Journey theme while preserving the original educational material.

To update this content, run:

```bash
bash scripts/docs-aggregator/aggregate_docs.sh
```

See the [aggregator documentation](/it-journey/scripts/docs-aggregator/README.md) for details.
