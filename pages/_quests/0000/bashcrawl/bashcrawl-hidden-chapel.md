---
title: 'Bashcrawl Hidden Chapel: Hidden Files and Man Pages'
description: "Uncover the Hidden Chapel with ls -a, explore the courtyard, aviary,
  hall, and graveyard. Use man pages and --help to defeat the monster and claim the tome."
date: 2026-05-22T00:00:00.000Z
lastmod: 2026-05-22T00:00:00.000Z
author: IT-Journey Team
level: '0000'
layout: journals
fmContentType: quest
quest_type: side_quest
quest_series: Bashcrawl Adventure Path
quest_arc: Terminal Mastery Arc
quest_line: Foundation Path
difficulty: 🔴 Hard
estimated_time: 35-45 minutes
primary_technology: bash
skill_focus:
- Hidden Files
- Man Pages
- Help Systems
learning_style: hands-on
tags:
- bashcrawl
- terminal
- bash
- hidden-files
- man-pages
- lvl-0000
keywords:
  primary:
  - ls -a hidden files
  - man command linux
  - bash help system
  - hidden directories linux
  secondary:
  - bashcrawl chapel
  - dotfiles linux
  - terminal documentation
quest_dependencies:
  required_quests:
  - /quests/0000/side-quests/bashcrawl-cellar/
  unlocks_quests:
  - /quests/0000/side-quests/bashcrawl-rift/
quest_relationships:
  parent_quest: /quests/0000/bashcrawl/
  sequel_quests:
  - /quests/0000/side-quests/bashcrawl-rift/
validation_criteria:
- Use ls -a to find hidden directories
- Successfully navigate to .CHAPEL
- Look up a command in man pages
- Defeat the hall monster using knowledge from a man page
- Collect the ancient tome
prerequisites:
- Complete the Cellar side-quest
learning_paths:
- Terminal Mastery Path
rewards:
- Ancient Tome Fragment
- Man page and hidden file mastery
permalink: /quests/0000/side-quests/bashcrawl-hidden-chapel/
---

*The wine cellar wall flickers. A hidden door appears — but only `ls -a` can see it. Beyond the false stone lies a chapel with five secret areas, guarded by a monster who fears knowledge.*

## 🎯 Quest Objectives

- [ ] Use `ls -a` to reveal the hidden `.CHAPEL` directory
- [ ] Navigate into `.CHAPEL` and explore the courtyard
- [ ] Reach the aviary and find the feather clue
- [ ] Consult `man` pages to learn the monster's weakness
- [ ] Navigate to the hall and defeat `./monster`
- [ ] Enter the library and collect the ancient tome
- [ ] Explore the graveyard — optional but rewarding

## �️ Quest Prerequisites

- [Cellar side-quest](/quests/0000/side-quests/bashcrawl-cellar/) complete
- Comfortable with `ls`, `cd`, and basic file reading

## ⚡ Command Cheatsheet

| Command | What It Does |
|---------|-------------|
| `ls -a` | List **all** files, including hidden ones (names starting with `.`) |
| `ls -la` | Long format + all files |
| `man command` | Open the manual page for a command |
| `info command` | Alternative documentation viewer |
| `command --help` | Quick built-in help |
| `q` | Quit the `man` pager |
| `/keyword` | Search inside `man` — then `n` for next match |

### About Dotfiles and Hidden Directories

Any file or directory whose name begins with `.` is **hidden** from `ls` by default. Use `ls -a` to see them.

```bash
ls
# regular_file  visible_dir/

ls -a
# .  ..  .CHAPEL/  .hidden_scroll  regular_file  visible_dir/
```

`.` is the current directory. `..` is the parent. Do not delete either.

## 🗺️ Walkthrough

### Step 1 — Reveal the hidden chapel

From the cellar:

```bash
ls -a
# .  ..  armoury/  .CHAPEL/  emerald_amulet  dusty_scroll  recipe*  scrap/  vault/
```

`.CHAPEL/` is invisible with plain `ls` — only `ls -a` shows it.

### Step 2 — Enter and explore the courtyard

```bash
cd .CHAPEL
ls -F
# courtyard/  hall/  library/  graveyard/

cd courtyard
ls -F
# aviary/  birdbath  stone_bench
cat birdbath
# "Birds know the secret. Look to the aviary."
```

### Step 3 — The aviary clue

```bash
cd aviary
ls -F
# eagle*  feather  perch/
cat feather
# "The monster fears: man grep"
```

This tells you to consult `man grep` — the solution to defeating the monster is hidden in the grep manual.

### Step 4 — Study the man page

```bash
man grep
# Opens the pager. Search with /pattern
# Press / then type "line number" and press Enter
# Press q to quit
```

> Tip: `man grep | grep "\-n"` pipes the manual through grep to find the `-n` flag quickly.

The relevant knowledge: `grep -n` prints line numbers. The hall monster demands you specify which line contains the incantation.

### Step 5 — Navigate to the hall and fight

```bash
cd ../hall
ls -F
# inscription  monster*  locked_door

cat inscription
# "Invoke grep with the flag that shows line numbers."

./monster
# The monster demands: "Which grep flag shows line numbers?"
# Your answer: -n
# The monster falls!
```

### Step 6 — Collect the tome from the library

```bash
cd ../library
ls -F
# tome  reading_nook/

cat tome
# The Ancient Tome of Shell Knowledge — tome fragment obtained.
inventory
```

### Step 7 (Optional) — Explore the graveyard

```bash
cd ../graveyard
ls -a
# columbarium/  .mausoleum/  royal_tombs/  epitaph

cat epitaph
# "Here lie commands executed without --help."
```

The mausoleum is another hidden directory. Explore it for bonus lore and a secret item.

## 💡 Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `No such directory: .CHAPEL` | Used `ls` instead of `ls -a` | Always use `ls -a` when searching |
| `man` opens strange pager | Default pager not `less` | Press `q` to quit; or `export PAGER=less` |
| Monster won't accept answer | Case sensitivity | Try both `n` and `-n` |
| Tome not in inventory | Used `less` instead of `cat` | `cat tome` adds it to inventory |

## ✅ Validation

- [ ] You can explain why `ls -a` is needed to see `.CHAPEL`
- [ ] You know how to search inside a `man` page
- [ ] The monster is defeated
- [ ] The ancient tome is in your inventory
- [ ] You explored at least four of the five chapel sub-areas

## ➡️ Next Steps

- **Complete other branches** → [Vault](/quests/0000/side-quests/bashcrawl-vault/) · [Scrap](/quests/0000/side-quests/bashcrawl-scrap/)
- **Enter the final gauntlet** → [The Rift](/quests/0000/side-quests/bashcrawl-rift/)
- **Back to hub** → [Bashcrawl Hub](/quests/0000/bashcrawl/)

---

## 📚 External Resources

Continue your terminal adventure with these resources:

- [Bashcrawl Web Demo](https://bamr87.github.io/bashcrawl/) — Play in your browser, no installation required
- [Bashcrawl on GitHub](https://github.com/bamr87/bashcrawl) — Source code, setup, and open contributions
- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/) — Official Bash reference: knowledge for every hero
- [IT-Journey Bashcrawl Hub](/quests/0000/bashcrawl/) — Full quest series and walkthroughs
- [ExplainShell](https://explainshell.com/) — Instantly decode any command in the realm

---

*Knowledge defeats what swords cannot. The chapel's secrets are yours.* ⛪
