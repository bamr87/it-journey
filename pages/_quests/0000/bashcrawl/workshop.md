---
title: 'Bashcrawl Workshop: File Management Fundamentals'
description: 'Practice file management in the Workshop: mkdir, touch, rm, cp, mv, and I/O redirection. Build rooms, write scrolls, and clear debris to advance.'
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
- file-management
- '0000'
keywords:
  primary:
  - mkdir command
  - touch command
  - rm command
  - echo redirect
  secondary:
  - file creation
  - bash tutorial
  - shell scripting basics
quest_dependencies:
  required_quests:
  - /quests/0000/side-quests/entrance/
  unlocks_quests:
  - /quests/0000/side-quests/cellar/
quest_relationships:
  parent_quest: /quests/0000/bashcrawl/
  sequel_quests:
  - /quests/0000/side-quests/cellar/
validation_criteria:
- Create a directory and verify with ls
- Create a file with touch and write to it with echo
- Delete a file with rm
- Copy and move files between directories
prerequisites:
- Complete the Entrance side-quest
learning_paths:
- Terminal Mastery Path
rewards:
- Bashcrawl Workbench Tool
- File management proficiency
excerpt: Practice mkdir, touch, echo redirection, cp, mv, and rm to construct workshop artifacts and advance deeper into Bashcrawl.
draft: false
permalink: /quests/0000/side-quests/workshop/
layout: quest
---
*The Workshop smells of sawdust and old iron. Workbenches line the walls, covered in unfinished projects. Here, heroes learn the art of building — and destroying — the very fabric of the file system.*

## 🎯 Quest Objectives

- [ ] Create a new room with `mkdir`
- [ ] Create a blank scroll with `touch`
- [ ] Write words onto a scroll with `echo >`
- [ ] Append text to a scroll with `echo >>`
- [ ] Copy a file with `cp`
- [ ] Move/rename a file with `mv`
- [ ] Remove an item with `rm`
- [ ] Clean the workshop and advance to the cellar

## �️ Quest Prerequisites

- Complete the [Entrance side-quest](/quests/0000/side-quests/entrance/) first
- Comfortable with `ls`, `cd`, and `cat`

## ⚡ Command Cheatsheet

| Command | What It Does |
|---------|-------------|
| `mkdir name` | Make a new directory |
| `touch file` | Create an empty file (or update timestamp) |
| `echo "text"` | Print text to the terminal |
| `echo "text" > file` | Write text to file (overwrites) |
| `echo "text" >> file` | Append text to file |
| `cp src dest` | Copy a file |
| `mv src dest` | Move or rename a file |
| `rm file` | Remove a file (permanent — no trash) |
| `rm -r dir` | Remove a directory and its contents |

## 🗺️ Walkthrough

### Step 1 — Enter the Workshop

```bash
# From the entrance:
cd workshop   # path varies by game mode
ls -F
# Output: blueprint  tools/  debris  workbench/
```

### Step 2 — Read the blueprint

```bash
cat blueprint
```

The blueprint tells you what to build. Common workshop task: create a storage room and write a manifest.

### Step 3 — Create a new room

```bash
mkdir storage_room
ls -F
# storage_room/ appears
```

### Step 4 — Create and write a scroll

```bash
touch manifest
echo "Iron bars: 10" > manifest
cat manifest
# Output: Iron bars: 10

echo "Copper wire: 5" >> manifest
cat manifest
# Output: Iron bars: 10
#         Copper wire: 5
```

> `>` **overwrites** the file. `>>` **appends** without destroying existing content.

### Step 5 — Copy and move files

```bash
cp manifest storage_room/manifest_copy
mv manifest storage_room/manifest
ls storage_room/
# manifest  manifest_copy
```

### Step 6 — Clean up debris

```bash
rm debris
ls -F
# debris is gone
```

> `rm` is **permanent** — there is no Recycle Bin in the terminal. Double-check filenames before deleting.

### Step 7 — Leave the workshop

```bash
cd ..
# Back to entrance, then navigate to cellar
cd cellar
```

## 💡 Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `rm: directory: is a directory` | Trying `rm` on a dir | Use `rm -r dirname` |
| Accidental overwrite with `>` | Used `>` instead of `>>` | Recreate the file; always double-check |
| `No such file or directory` | Typo in filename | Use Tab to autocomplete |
| Created file in wrong place | Not in Workshop dir | `pwd` first; `cd` as needed |

## ✅ Validation

Before advancing:

- [ ] You can create directories and files from memory
- [ ] You understand the difference between `>` and `>>`
- [ ] You successfully cleaned the workshop
- [ ] You navigated back out to continue the main path

## ➡️ Next Steps

- **Main path** → [Cellar](/quests/0000/side-quests/cellar/)
- **Back to hub** → [Bashcrawl Hub](/quests/0000/bashcrawl/)

---

## 📚 External Resources

Continue your terminal adventure with these resources:

- [Bashcrawl Web Demo](https://bamr87.github.io/bashcrawl/) — Play in your browser, no installation required
- [Bashcrawl on GitHub](https://github.com/bamr87/bashcrawl) — Source code, setup, and open contributions
- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/) — Official Bash reference for heroes
- [IT-Journey Bashcrawl Hub](/quests/0000/bashcrawl/) — Full quest series and walkthroughs
- [The Linux Command Line](https://linuxcommand.org/tlcl.php) — Free book: mastery through adventure

---

*Every master builder started with a single `mkdir`. The workshop is behind you.* 🔨

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0000 - Foundation & Init World]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Bashcrawl Entrance: Your First Terminal Commands]]
**Unlocks:** [[Bashcrawl Cellar: File Types, Aliases, and Emerald Amulet]]
**Sequel quests:** [[Bashcrawl Cellar: File Types, Aliases, and Emerald Amulet]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]

