---
title: 'Bashcrawl Entrance: Your First Terminal Commands'
description: Learn pwd, ls, cd, and cat by exploring the Bashcrawl entrance — read the first scroll, get a hint from Merlin, and collect your brass key to proceed.
date: '2026-05-22T00:00:00.000Z'
lastmod: '2026-05-23T02:30:23.000Z'
author: IT-Journey Team
level: '0000'
fmContentType: quest
quest_type: side_quest
quest_series: Bashcrawl Adventure Path
quest_arc: Terminal Mastery Arc
quest_line: Foundation Path
difficulty: 🟢 Easy
estimated_time: 15-20 minutes
primary_technology: bash
skill_focus: fullstack
learning_style: hands-on
categories:
- Quests
- Terminal
- Bashcrawl
tags:
- bashcrawl
- terminal
- bash
- navigation
- '0000'
keywords:
  primary:
  - pwd command
  - ls command
  - cd command
  - cat command
  secondary:
  - terminal navigation
  - bash tutorial
  - command line basics
quest_dependencies:
  required_quests:
  - /quests/0000/bashcrawl/
  unlocks_quests:
  - /quests/0000/side-quests/workshop/
  - /quests/0000/side-quests/cellar/
quest_relationships:
  parent_quest: /quests/0000/bashcrawl/
  sequel_quests:
  - /quests/0000/side-quests/workshop/
  - /quests/0000/side-quests/cellar/
validation_criteria:
- Run pwd and explain the output
- List the entrance contents with ls and ls -F
- Read the entrance scroll with cat
- Navigate to the cellar directory
prerequisites:
- Complete the Bashcrawl Hub quest
learning_paths:
- Terminal Mastery Path
rewards:
- Bashcrawl Brass Key
- Terminal navigation proficiency
excerpt: Start Bashcrawl by using pwd, ls, cd, and cat to read the first scroll, collect the brass key, and enter the dungeon.
draft: false
permalink: /quests/0000/side-quests/entrance/
layout: quest
---
*The dungeon gate groans open. Cool air pours out carrying the scent of ancient scrolls. This is where every hero begins — four commands, a brass key, and the courage to type.*

## 🎯 Quest Objectives

- [ ] Print your current location with `pwd`
- [ ] List the dungeon entrance contents with `ls` and `ls -F`
- [ ] Read the entrance scroll with `cat`
- [ ] Ask Merlin for a hint with the `merlin` command
- [ ] Collect the brass key and move to the cellar

## �️ Quest Prerequisites

- A terminal with Bash (macOS, Linux, or WSL)
- Bashcrawl installed or running at [bamr87.github.io/bashcrawl](https://bamr87.github.io/bashcrawl/)

## ⚡ Command Cheatsheet

| Command | What It Does |
|---------|-------------|
| `pwd` | **P**rint **w**orking **d**irectory — shows where you are |
| `ls` | **L**i**s**t directory contents |
| `ls -F` | List with type markers: `/` = dir, `*` = executable, `@` = symlink |
| `cat file` | Print file contents to the terminal |
| `cd dir` | **C**hange **d**irectory |
| `cd ..` | Go up one level |
| `merlin` | Ask the wizard for a context-aware hint |
| `quest` | Display current objectives |

## 🗺️ Walkthrough

### Step 1 — Where am I?

```bash
pwd
# Output: /home/<user>/bashcrawl/ENTRANCE  (or similar)
```

`pwd` always shows your absolute path. Use it whenever you feel lost.

### Step 2 — What's here?

```bash
ls
# Output: scroll  cellar
```

```bash
ls -F
# Output: scroll  cellar/
```

The trailing `/` after `cellar` tells you it is a directory (a doorway to the next chamber). `scroll` has no marker — it is a plain text file.

### Step 3 — Read the scroll

```bash
cat scroll
```

The scroll contains the first piece of the dungeon's story and a clue about the brass key. Read it carefully — items and hints mentioned here matter later.

### Step 4 — Ask Merlin

```bash
merlin
```

Merlin reads your current location and delivers a context-sensitive hint. Whenever you are stuck, `merlin` is your first stop.

### Step 5 — Check your objectives

```bash
quest
```

The quest log shows what you need to do in the current chamber.

### Step 6 — Enter the cellar

```bash
cd cellar
pwd
# Output: .../ENTRANCE/cellar
```

Congratulations — you have left the entrance. Continue to the [Cellar walkthrough](/quests/0000/side-quests/cellar/) or explore the [Workshop](/quests/0000/side-quests/workshop/) first.

## 💡 Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `command not found: merlin` | Not in the game shell | Run `./main.sh --interactive` first |
| `No such file: scroll` | Wrong directory | Run `pwd`; navigate to ENTRANCE with `cd` |
| `ls` shows nothing | Empty directory | Make sure you are in ENTRANCE, not `/` |
| Path has spaces | Rare edge case | Wrap in quotes: `cd "my dir"` |

## ✅ Validation

Before marking this side-quest complete, verify:

- [ ] You can explain what `pwd` returns without running it
- [ ] You know the difference between `ls` and `ls -F`
- [ ] You read the scroll and understand its clue
- [ ] You successfully navigated into cellar

## ➡️ Next Steps

You are now ready to explore deeper. Choose your path:

- **Continue the main line** → [Cellar](/quests/0000/side-quests/cellar/)
- **Side trip first** → [Workshop](/quests/0000/side-quests/workshop/)
- **Back to hub** → [Bashcrawl Hub](/quests/0000/bashcrawl/)

---

## 📚 External Resources

Continue your terminal adventure with these resources:

- [Bashcrawl Web Demo](https://bamr87.github.io/bashcrawl/) — Play in your browser, no installation required
- [Bashcrawl on GitHub](https://github.com/bamr87/bashcrawl) — Source code, setup, and open contributions
- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/) — Official Bash reference for heroes
- [IT-Journey Bashcrawl Hub](/quests/0000/bashcrawl/) — Full quest series and walkthroughs
- [The Linux Command Line](https://linuxcommand.org/tlcl.php) — Free book covering every command you'll meet

---

*Four commands mastered. Hundreds to go. The dungeon opens before you.* 🗝️

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0000 - Foundation & Init World]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Unlocks:** [[Bashcrawl Workshop: File Management Fundamentals]] · [[Bashcrawl Cellar: File Types, Aliases, and Emerald Amulet]]
**Sequel quests:** [[Bashcrawl Workshop: File Management Fundamentals]] · [[Bashcrawl Cellar: File Types, Aliases, and Emerald Amulet]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]

