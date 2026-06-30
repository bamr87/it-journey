---
title: 'Bashcrawl Armoury: File Permissions and Script Execution'
description: Learn chmod, file permissions, and script execution in Bashcrawl's Armoury. Brew a health potion and wield a sword for your first combat encounter.
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
estimated_time: 25-30 minutes
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
- permissions
- chmod
- '0000'
keywords:
  primary:
  - chmod command
  - file permissions linux
  - bash script execution
  - permission denied fix
  secondary:
  - octal permissions
  - bashcrawl armoury
  - executable scripts
quest_dependencies:
  required_quests:
  - /quests/0000/cellar/
  - /quests/0000/bashcrawl/
  unlocks_quests:
  - /quests/0000/chamber/
  recommended_quests: []
validation_criteria:
- Read ls -l permissions output correctly
- Use chmod to make a script executable
- Run ./potion and ./sword scripts successfully
- Advance to the Chamber
prerequisites:
- Complete the Cellar side-quest
rewards:
- Enchanted Sword
- File permissions mastery
excerpt: Master chmod, read permission bits, and execute armoury scripts to brew potions, equip your sword, and unlock the next chamber.
draft: false
permalink: /quests/0000/armoury/
layout: quest
redirect_from:
- /quests/0000/side-quests/armoury/
---
*Racks of weapons line the walls. Suits of armour stand at attention. But every sword and potion is locked behind a permission barrier — you must learn `chmod` before you can equip a single item.*

## 🕹️ Play This Chamber

This page is your **walkthrough and strategy guide** — play right here in the browser, then follow the steps below.

{% include bashcrawl-terminal.html room="Armoury" %}

## 🎯 Quest Objectives

- [ ] Read `ls -l` output and interpret permission bits
- [ ] Use `chmod` to make scripts executable
- [ ] Run `./potion` to restore health
- [ ] Run `./sword` to equip your weapon
- [ ] Defeat the armoury guardian
- [ ] Proceed to the Chamber

## 🗺️ Quest Prerequisites

- [Cellar side-quest](/quests/0000/side-quests/cellar/) complete
- Comfortable with `ls -F`, `cat`, and file navigation

## ⚡ Command Cheatsheet

| Command | What It Does |
|---------|-------------|
| `ls -l` | Long listing — shows permissions, owner, size |
| `chmod +x file` | Add execute permission for everyone |
| `chmod 755 file` | `rwxr-xr-x` — owner can all; others can read+execute |
| `chmod 644 file` | `rw-r--r--` — owner can read+write; others read only |
| `./script` | Execute a script in the current directory |

### Permission String Decoder

```text
-  rwx  r-x  r-x
│   │    │    │
│   │    │    └── others (o)
│   │    └─────── group (g)
│   └──────────── user / owner (u)
└──────────────── file type: - = regular, d = dir, l = link
```

Each group: `r` = read (4), `w` = write (2), `x` = execute (1)

Octal shorthand: `755` = `rwx r-x r-x`, `644` = `rw- r-- r--`

## 🗺️ Walkthrough

### Step 1 — Inspect the armoury

```bash
ls -l
# -rw-r--r-- 1 user group  512 Jan  1 00:00 potion
# -rw-r--r-- 1 user group 1024 Jan  1 00:00 sword
# -rwxr-xr-x 1 user group  256 Jan  1 00:00 guardian
```

`potion` and `sword` lack the `x` bit — they are **not yet executable**. You cannot run them.

### Step 2 — Try running a locked script

```bash
./potion
# bash: ./potion: Permission denied
```

This is the expected result. Now fix it.

### Step 3 — Grant execute permission

```bash
chmod +x potion
chmod +x sword
ls -l potion sword
# -rwxr-xr-x 1 user group  512 Jan  1 00:00 potion
# -rwxr-xr-x 1 user group 1024 Jan  1 00:00 sword
```

> **Why the `./`?** When you type `./potion`, the `./` tells the shell to run
> the script in the **current directory**. Without it, the shell only searches
> the directories in your `PATH` — and `.` (the current directory) is **not** in
> `PATH` by default, so `potion` alone would fail with "command not found".

### Step 4 — Drink the potion

```bash
./potion
# HP restored: 50 → 100
```

### Step 5 — Pick up the sword

```bash
./sword
# Sword of Echoes added to inventory.
```

### Step 6 — Face the guardian

```bash
./guardian
# A stone golem steps forward...
# You raise your sword...
# Guardian defeated! The door creaks open.
```

With the sword equipped, the guardian falls and the door to the Chamber opens.
List the room (`ls`) to find the path onward, then step through into the
Chamber's directory (for example, `cd ../chamber`).

> **Low on health?** Your HP carries over between rooms. If a fight leaves you
> weakened, re-run `./potion` (if a potion is still available) before moving on.

## 💡 Understanding Octal Permissions

| Octal | Symbolic | Who Can Do What |
|-------|----------|----------------|
| `777` | `rwxrwxrwx` | Everyone can read, write, execute ⚠️ |
| `755` | `rwxr-xr-x` | Owner: all; others: read + execute ✅ |
| `644` | `rw-r--r--` | Owner: read + write; others: read only ✅ |
| `600` | `rw-------` | Owner only — private files 🔒 |
| `400` | `r--------` | Read-only, even for owner |

> **Security note:** Never use `chmod 777` on scripts or sensitive files. Use `755` for scripts and `644` for data.

## 💡 Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `Permission denied` after chmod | Not the file owner | Use `ls -l` to check owner |
| Script does nothing | Missing shebang line | Add `#!/usr/bin/env bash` as line 1 |
| `No such file: ./sword` | Wrong directory | `pwd` and `ls` first |
| Health still low after potion | Stale game state | Re-run the bashcrawl setup or restart the game from the entrance, then revisit the room |

## ✅ Validation

- [ ] You can read a permission string like `rwxr-xr--` without looking it up
- [ ] You understand why `./` is needed to run a script
- [ ] You ran both `./potion` and `./sword` successfully
- [ ] The guardian is defeated and the Chamber door is open

## ➡️ Next Steps

- **Continue main line** → [Chamber](/quests/0000/side-quests/chamber/)
- **Explore other branches** → [Chapel](/quests/0000/side-quests/hidden-chapel/) · [Vault](/quests/0000/side-quests/vault/) · [Scrap](/quests/0000/side-quests/scrap/)
- **Back to hub** → [Bashcrawl Hub](/quests/0000/bashcrawl/)

---

{% include bashcrawl-play-local.html %}

## 📚 External Resources

Continue your terminal adventure with these resources:

- [Bashcrawl Web Demo](https://bamr87.github.io/bashcrawl/) — Play in your browser, no installation required
- [Bashcrawl on GitHub](https://github.com/bamr87/bashcrawl) — Source code, setup, and open contributions
- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/) — Official Bash reference for brave heroes
- [IT-Journey Bashcrawl Hub](/quests/0000/bashcrawl/) — Full quest series and walkthroughs
- [chmod Calculator](https://chmod-calculator.com/) — Permission wizard for every adventurer

---

*Sword in hand, potion consumed. The Chamber awaits.* ⚔️

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0000 - Foundation & Init World]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Bashcrawl Cellar: File Types, Aliases, and Emerald Amulet]]
**Unlocks:** [[Bashcrawl Chamber: Bash Arithmetic and the Statue Boss]]
**Sequel quests:** [[Bashcrawl Chamber: Bash Arithmetic and the Statue Boss]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]

