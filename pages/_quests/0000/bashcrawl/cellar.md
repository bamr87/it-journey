---
title: 'Bashcrawl Cellar: File Types, Aliases, and Emerald Amulet'
description: Master file types with ls -F, create alias shortcuts, and discover the emerald amulet in Bashcrawl's Cellar. Completing this chamber unlocks four deeper areas.
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
- aliases
- file-types
- '0000'
keywords:
  primary:
  - ls -F command
  - bash alias
  - file types terminal
  - emerald amulet bashcrawl
  secondary:
  - shell shortcuts
  - bash tutorial
  - terminal navigation
quest_dependencies:
  required_quests:
  - /quests/0000/side-quests/entrance/
  unlocks_quests:
  - /quests/0000/side-quests/armoury/
  - /quests/0000/side-quests/hidden-chapel/
  - /quests/0000/side-quests/vault/
  - /quests/0000/side-quests/scrap/
quest_relationships:
  parent_quest: /quests/0000/bashcrawl/
  sequel_quests:
  - /quests/0000/side-quests/armoury/
  - /quests/0000/side-quests/hidden-chapel/
  - /quests/0000/side-quests/vault/
  - /quests/0000/side-quests/scrap/
validation_criteria:
- Use ls -F and explain every symbol
- Create and use at least one alias
- Collect the emerald amulet
- Identify four exit paths from the cellar
prerequisites:
- Complete either the Entrance or Workshop side-quest
learning_paths:
- Terminal Mastery Path
rewards:
- Emerald Amulet
- Alias and file-type mastery
excerpt: Use ls -F, file, and aliases to map cellar artifacts, collect the emerald amulet, and unlock four branching dungeon paths.
draft: false
permalink: /quests/0000/side-quests/cellar/
layout: quest
---
*The cellar reeks of wine and secrets. Barrels line the walls; cobwebs drape the ceiling. Four iron doors lead deeper into the dungeon — armoury, chapel, vault, scrap. But first you must find the emerald amulet.*

## 🎯 Quest Objectives

- [ ] Identify every file type in the cellar using `ls -F`
- [ ] Use the `file` command to interrogate items
- [ ] Create a useful alias to speed up exploration
- [ ] Find and collect the emerald amulet
- [ ] Locate all four exits (armoury, chapel, vault, scrap)

## �️ Quest Prerequisites

- [Entrance side-quest](/quests/0000/side-quests/entrance/) complete
- Know how to use `ls`, `cd`, and `cat`

## ⚡ Command Cheatsheet

| Command | What It Does |
|---------|-------------|
| `ls -F` | List with type markers |
| `ls -la` | Long listing, including hidden files |
| `file filename` | Describe what type of file this is |
| `alias name='cmd'` | Create a command shortcut |
| `alias` | List all defined aliases |
| `unalias name` | Remove an alias |
| `type name` | Show how a name is resolved (builtin/alias/function/file) |

### `ls -F` Symbol Key

| Symbol | Meaning |
|--------|---------|
| `/` | Directory |
| `*` | Executable file |
| `@` | Symbolic link |
| `=` | Socket |
| `\|` | Named pipe (FIFO) |
| *(none)* | Regular file |

## 🗺️ Walkthrough

### Step 1 — Survey the cellar

```bash
ls -F
# Example output:
# emerald_amulet  armoury/  chapel/  vault/  scrap/  dusty_scroll  recipe*
```

Notice the variety: a regular file (`emerald_amulet`), directories (`/`), and an executable (`recipe*`).

### Step 2 — Investigate with `file`

```bash
file dusty_scroll
# dusty_scroll: ASCII text

file recipe
# recipe: Bourne-Again shell script, ASCII text executable
```

`file` reads the file's magic bytes — much more reliable than guessing from the name.

### Step 3 — Read the scroll

```bash
cat dusty_scroll
```

The scroll reveals a clue about the emerald amulet's location and warns about hidden traps in the deeper chambers.

### Step 4 — Collect the amulet

```bash
cat emerald_amulet
```

Reading it adds it to your inventory. Verify:

```bash
inventory
# Shows: emerald amulet ✓
```

### Step 5 — Create a helpful alias

```bash
# Quick inventory check shortcut
alias inv='inventory'

# Quick navigation shortcut
alias back='cd ..'

# Verify
alias
```

Aliases last only for the current session unless added to `~/.bashrc` or `~/.bash_profile`.

### Step 6 — Identify all four exits

```bash
ls -F
# armoury/  chapel/  vault/  scrap/
```

Each leads to a distinct area of the dungeon. You can tackle them in any order.

## 💡 Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `alias: bad alias name` | Space in alias name | Use underscores: `alias my_cmd='...'` |
| `inventory` not found | Not in game shell | Start with `./main.sh --interactive` |
| Can't find emerald amulet | Wrong directory | `pwd`; make sure you are in CELLAR |
| All four exits missing | Older game version | Run `./setup.sh --repair` |

## ✅ Validation

- [ ] You can explain every `ls -F` symbol from memory
- [ ] You created and tested at least one alias
- [ ] The emerald amulet is in your inventory
- [ ] You know which four chambers you can enter next

## ➡️ Next Steps

Choose your next chamber — all four are unlocked:

| Chamber | Skills | Link |
|---------|--------|------|
| ⚔️ Armoury | Permissions, `chmod`, combat | [Armoury](/quests/0000/side-quests/armoury/) |
| ⛪ Hidden Chapel | Hidden files, `man` pages | [Chapel](/quests/0000/side-quests/hidden-chapel/) |
| 🔒 Vault | Environment variables, `export` | [Vault](/quests/0000/side-quests/vault/) |
| 🗑️ Scrap Heap | Symbolic links, `ln -s` | [Scrap](/quests/0000/side-quests/scrap/) |

---

## 📚 External Resources

Continue your terminal adventure with these resources:

- [Bashcrawl Web Demo](https://bamr87.github.io/bashcrawl/) — Play in your browser, no installation required
- [Bashcrawl on GitHub](https://github.com/bamr87/bashcrawl) — Source code, setup, and open contributions
- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/) — Official Bash reference for every hero
- [IT-Journey Bashcrawl Hub](/quests/0000/bashcrawl/) — Full quest series and walkthroughs
- [Bash Aliases Guide](https://tldp.org/LDP/abs/html/aliases.html) — Alias mastery for the brave adventurer

---

*Emerald amulet secured. Four doors, four paths. The dungeon deepens.* 🍷

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0000 - Foundation & Init World]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Bashcrawl Entrance: Your First Terminal Commands]]
**Unlocks:** [[Bashcrawl Armoury: File Permissions and Script Execution]] · [[Bashcrawl Hidden Chapel: Hidden Files and Man Pages]] · [[Bashcrawl Vault: Environment Variables and the Goblet Puzzle]] · [[Bashcrawl Scrap Heap: Symbolic Links and Portal Creation]]
**Sequel quests:** [[Bashcrawl Armoury: File Permissions and Script Execution]] · [[Bashcrawl Hidden Chapel: Hidden Files and Man Pages]] · [[Bashcrawl Vault: Environment Variables and the Goblet Puzzle]] · [[Bashcrawl Scrap Heap: Symbolic Links and Portal Creation]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]

