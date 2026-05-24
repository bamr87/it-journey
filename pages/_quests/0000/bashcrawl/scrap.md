---
title: 'Bashcrawl Scrap Heap: Symbolic Links and Portal Creation'
description: Learn symbolic links in Bashcrawl's Scrap Heap using ln -s, readlink, and ls -l. Create portal symlinks that warp you instantly to distant dungeon corners.
date: '2026-05-22T00:00:00.000Z'
lastmod: '2026-05-23T02:30:23.000Z'
author: IT-Journey Team
level: '0000'
fmContentType: quest
quest_type: side_quest
quest_series: Bashcrawl Adventure Path
quest_arc: Terminal Mastery Arc
quest_line: Foundation Path
difficulty: 🟡 Medium
estimated_time: 20-25 minutes
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
- symlinks
- ln
- '0000'
keywords:
  primary:
  - symbolic links linux
  - ln -s command
  - readlink command
  - symlink vs hardlink
  secondary:
  - bashcrawl scrap
  - bash file system
  - terminal shortcuts
quest_dependencies:
  required_quests:
  - /quests/0000/side-quests/cellar/
  unlocks_quests:
  - /quests/0000/side-quests/rift/
quest_relationships:
  parent_quest: /quests/0000/bashcrawl/
  sequel_quests:
  - /quests/0000/side-quests/rift/
validation_criteria:
- Create a symbolic link with ln -s
- Verify the symlink with ls -l
- Follow and resolve a symlink with readlink
- Navigate the scrap heap using symlink portals
- Collect the portal crystal
prerequisites:
- Complete the Cellar side-quest
learning_paths:
- Terminal Mastery Path
rewards:
- Portal Crystal
- Symbolic links mastery
excerpt: Build and inspect symbolic-link portals with ln -s, ls -l, and readlink to traverse the Scrap Heap and recover the portal crystal.
draft: false
permalink: /quests/0000/side-quests/scrap/
layout: quest
---
*The Scrap Heap is a wasteland of discarded objects — broken swords, empty potion bottles, shattered mirrors. But hidden among the junk are portal mirrors, and learning `ln -s` lets you build instant teleportation.*

## 🎯 Quest Objectives

- [ ] Understand the difference between hard links and symbolic links
- [ ] Create a symbolic link with `ln -s`
- [ ] Identify symlinks with `ls -l` (look for `->`)
- [ ] Resolve the target of a symlink with `readlink`
- [ ] Use the scrap's portal symlinks to shortcut navigation
- [ ] Collect the portal crystal

## �️ Quest Prerequisites

- [Cellar side-quest](/quests/0000/side-quests/cellar/) complete
- Comfortable with `ls -F`, `ls -l`, and `cd`

## ⚡ Command Cheatsheet

| Command | What It Does |
|---------|-------------|
| `ln -s target link_name` | Create a symbolic link pointing to `target` |
| `ls -l` | Long listing — symlinks show `link -> target` |
| `ls -F` | Symlinks show with `@` marker |
| `readlink link_name` | Print the target of a symlink |
| `readlink -f link_name` | Print the fully-resolved absolute path |
| `realpath path` | Same as `readlink -f` (more modern) |

### Hard Link vs Symbolic Link

| Property | Hard Link | Symbolic Link |
|----------|-----------|---------------|
| Points to | Inode (data) | Path (name) |
| Works across filesystems | No | Yes |
| Target deleted | Link still works | Broken link (dangling) |
| `ls -F` marker | none | `@` |

## 🗺️ Walkthrough

### Step 1 — Survey the scrap heap

```bash
ls -F
# broken_sword  empty_bottle  portal_mirror@  scrap_pile/  crystal_hint

ls -l portal_mirror
# lrwxrwxrwx  1 user group  12 Jan 01  portal_mirror -> /vault/lab
```

`portal_mirror` is already a symlink — it points to the vault's lab. You can `cd portal_mirror` and you will land directly in the lab.

### Step 2 — Navigate via the existing portal

```bash
cd portal_mirror
pwd
# .../vault/lab   ← teleported!
cd -             # Return to previous directory (the scrap heap)
pwd
# .../scrap
```

`cd -` takes you back to wherever you were last. Very useful.

### Step 3 — Read the hint

```bash
cat crystal_hint
# "Create a shortcut named 'quick_entrance' pointing to ../../ENTRANCE"
```

### Step 4 — Create your own portal

```bash
ln -s ../../ENTRANCE quick_entrance
ls -l quick_entrance
# lrwxrwxrwx  1 user group  20 Jan 01  quick_entrance -> ../../ENTRANCE

ls -F quick_entrance/
# scroll  cellar/          ← entrance contents, via symlink
```

### Step 5 — Inspect and resolve

```bash
readlink quick_entrance
# ../../ENTRANCE

readlink -f quick_entrance
# /home/user/bashcrawl/ENTRANCE  ← absolute, resolved path
```

### Step 6 — Collect the crystal

```bash
cat crystal_hint
inventory
# portal crystal ✓
```

## 💡 Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| Symlink shows broken (red in terminal) | Target path does not exist | Check relative path with `readlink` |
| `ln -s` with no arguments | Wrong order | Syntax: `ln -s TARGET LINK_NAME` |
| `cd symlink` goes somewhere unexpected | Relative path off | Use absolute path or `readlink -f` |
| Cannot delete directory via symlink | Symlink vs directory | `rm symlink` removes the link; `rm -r` removes the target |

> **Danger:** `rm -r symlink_to_dir` may behave unexpectedly depending on your shell version. Prefer `unlink symlink_name` to safely remove only the link.

## ✅ Validation

- [ ] You know the difference between `ls -F @` and a real directory
- [ ] You created `quick_entrance` and successfully `cd`'d through it
- [ ] You can resolve absolute target paths with `readlink -f`
- [ ] The portal crystal is in your inventory

## ➡️ Next Steps

- **Complete other branches** → [Hidden Chapel](/quests/0000/side-quests/hidden-chapel/) · [Vault](/quests/0000/side-quests/vault/)
- **Enter the final gauntlet** → [The Rift](/quests/0000/side-quests/rift/)
- **Back to hub** → [Bashcrawl Hub](/quests/0000/bashcrawl/)

---

## 📚 External Resources

Continue your terminal adventure with these resources:

- [Bashcrawl Web Demo](https://bamr87.github.io/bashcrawl/) — Play in your browser, no installation required
- [Bashcrawl on GitHub](https://github.com/bamr87/bashcrawl) — Source code, setup, and open contributions
- [GNU Bash Manual — Symbolic Links](https://www.gnu.org/software/bash/manual/bash.html) — Portal magic for brave adventurers
- [IT-Journey Bashcrawl Hub](/quests/0000/bashcrawl/) — Full quest series and walkthroughs
- [Linux Symlinks Guide](https://linuxize.com/post/how-to-create-symbolic-links-in-linux-using-the-ln-command/) — Master the art of magical portals

---

*Portals created. The dungeon's geography bends to your will.* 🗑️

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0000 - Foundation & Init World]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Bashcrawl Cellar: File Types, Aliases, and Emerald Amulet]]
**Unlocks:** [[Bashcrawl Rift: Pipes, Redirection, and the Final Boss]]
**Sequel quests:** [[Bashcrawl Rift: Pipes, Redirection, and the Final Boss]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]

