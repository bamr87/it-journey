---
title: 'Bashcrawl Rift: Pipes, Redirection, and the Final Boss'
description: Conquer Bashcrawl's final gauntlet — the Rift — by mastering pipes, &&, ||, and output redirection. Defeat the pit boss and satellite boss to complete.
date: '2026-05-22T00:00:00.000Z'
lastmod: '2026-05-23T02:30:23.000Z'
author: IT-Journey Team
level: '0000'
fmContentType: quest
quest_type: side_quest
quest_series: Bashcrawl Adventure Path
quest_arc: Terminal Mastery Arc
quest_line: Foundation Path
difficulty: 🔴 Hard
estimated_time: 40-50 minutes
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
- pipes
- redirection
- '0000'
keywords:
  primary:
  - bash pipes
  - output redirection bash
  - command chaining bash
  - tee command linux
  secondary:
  - bashcrawl rift
  - bash stdin stdout
  - linux pipes tutorial
quest_dependencies:
  required_quests:
  - /quests/0000/side-quests/chamber/
  - /quests/0000/side-quests/hidden-chapel/
  unlocks_quests:
  - /quests/0000/side-quests/agent-mode/
quest_relationships:
  parent_quest: /quests/0000/bashcrawl/
  sequel_quests:
  - /quests/0000/side-quests/agent-mode/
validation_criteria:
- Use | to pipe output between commands
- Chain commands with && and ||
- Redirect output to a file with > and >>
- Redirect stderr with 2>
- Defeat the pit boss
- Defeat the satellite boss
- Complete the dungeon
prerequisites:
- Complete Chamber plus at least one of Chapel/Vault/Scrap
learning_paths:
- Terminal Mastery Path
rewards:
- Rift Conquest Badge
- Pipes and redirection mastery
excerpt: Conquer the final Rift by chaining commands, piping output, and redirecting streams to defeat both bosses and finish Bashcrawl.
draft: false
permalink: /quests/0000/side-quests/rift/
layout: quest
---
*You stand at the edge of the Rift — a swirling chasm where data streams collide. The rules here are different: commands don't just run, they flow into each other. Master the pipe and you master the dungeon.*

## 🎯 Quest Objectives

- [ ] Pipe command output to another command using `|`
- [ ] Chain commands with `&&` (run next only if previous succeeds) and `||` (run next only if previous fails)
- [ ] Redirect stdout to a file with `>` and `>>`
- [ ] Redirect stderr with `2>` and combined with `2>&1`
- [ ] Use `tee` to split output to file and terminal
- [ ] Navigate arena → pit → spire → mezzanine → .elevator → .satellite
- [ ] Defeat the pit boss and the satellite boss
- [ ] Complete the Bashcrawl dungeon

## �️ Quest Prerequisites

All of these should be in your inventory before entering the Rift:

- [ ] Stone key fragment (from Chamber)
- [ ] Ancient tome (from Chapel)
- [ ] Vault key fragment (from Vault)
- [ ] Portal crystal (from Scrap)

## ⚡ Command Cheatsheet

| Syntax | What It Does |
|--------|-------------|
| `cmd1 \| cmd2` | Pipe stdout of cmd1 to stdin of cmd2 |
| `cmd1 && cmd2` | Run cmd2 only if cmd1 succeeds (exit 0) |
| `cmd1 \|\| cmd2` | Run cmd2 only if cmd1 fails (non-zero exit) |
| `cmd1 ; cmd2` | Run cmd2 always, regardless of cmd1 exit |
| `cmd > file` | Redirect stdout to file (overwrite) |
| `cmd >> file` | Redirect stdout to file (append) |
| `cmd 2> err.log` | Redirect stderr to file |
| `cmd 2>&1` | Redirect stderr to same destination as stdout |
| `cmd > out.log 2>&1` | Redirect both stdout and stderr to file |
| `cmd \| tee file` | Print to terminal AND write to file |

## 🗺️ Walkthrough

### Step 1 — Assemble the Rift Key

```bash
# The Rift gate requires all four fragments
ls -F
# arena/  rift_gate  key_assembler*

inventory
# stone key fragment, tome fragment, vault key fragment, portal crystal ✓

./key_assembler
# All fragments combined → Rift Key obtained.
```

### Step 2 — Arena — Master the pipe

```bash
cd arena
ls -F
# combatants  scoreboard  arena_boss*

cat combatants | sort | uniq
# Unique combatant list, sorted alphabetically

cat combatants | grep "elite" | wc -l
# Count of elite combatants

# Engage the arena boss
./arena_boss
```

The arena boss asks pipe-based puzzles. Answer by constructing the right pipeline.

### Step 3 — Pit — Command chaining

```bash
cd ../pit
cat instructions
# "Raise the drawbridge ONLY if the watchtower lights up. Fail gracefully."

./watchtower && ./raise_drawbridge
# If watchtower succeeds: drawbridge raised.
# If watchtower fails: drawbridge untouched.

./watchtower || echo "Watchtower failed — lighting torches instead."

./pit_boss
```

### Step 4 — Spire — Redirection

```bash
cd ../../spire
cat spire_challenge
# "Capture all output from the oracle — both wisdom and errors — into oracle.log"

./oracle > oracle.log 2>&1
cat oracle.log

# Also capture with tee so you still see it:
./oracle 2>&1 | tee oracle.log
```

### Step 5 — Mezzanine — Advanced chaining

```bash
cd mezzanine
# Combine all techniques:
ls -la | sort -k5 -rn | head -10 > biggest_files.txt
cat biggest_files.txt
```

### Step 6 — Hidden areas: .elevator and .satellite

```bash
ls -a
# .  ..  .elevator/  .satellite/

cd .elevator
ls -F
# control_panel  floor_select*

./floor_select
cd ../.satellite
ls -F
# transmitter*  signal_logs  satellite_boss*

cat signal_logs | grep "ERROR" | tee error_report.txt
cat error_report.txt

./satellite_boss
```

The satellite boss is the final encounter. It uses all skills: pipe a command through grep, redirect errors, chain with `&&`. Complete it to finish the dungeon.

## 💡 Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `|` not working | Wrong pipe character | Use `\|` in tables; actual `\|` is just `|` in shell |
| `2>&1` must come AFTER `>` | Order matters | Always: `> file 2>&1` not `2>&1 > file` |
| `&&` chain stops early | A command failed | Add `\|\|` fallback or check exit codes |
| Hidden dirs not found | Forgot `ls -a` | Always use `ls -a` in unfamiliar directories |

## ✅ Validation

- [ ] You can build a 3-command pipeline from memory
- [ ] You know the difference between `>` and `>>`
- [ ] You understand why `2>&1` must follow `>`
- [ ] Both pit boss and satellite boss are defeated
- [ ] `map` shows all chambers as complete

## ➡️ Next Steps

- **The dungeon is complete!** Celebrate your mastery.
- **Capstone** → [Agent Mode](/quests/0000/side-quests/agent-mode/) for advanced automation
- **Extend the dungeon** → [Bash Run](/quests/0000/side-quests/bash-run/)
- **Back to hub** → [Bashcrawl Hub](/quests/0000/bashcrawl/)

---

## 📚 External Resources

Continue your terminal adventure with these resources:

- [Bashcrawl Web Demo](https://bamr87.github.io/bashcrawl/) — Play in your browser, no installation required
- [Bashcrawl on GitHub](https://github.com/bamr87/bashcrawl) — Source code, setup, and open contributions
- [GNU Bash Manual — Pipelines](https://www.gnu.org/software/bash/manual/bash.html#Pipelines) — The adventurer's guide to command chaining
- [IT-Journey Bashcrawl Hub](/quests/0000/bashcrawl/) — Full quest series and walkthroughs
- [Bash Redirections Cheat Sheet](https://catonmat.net/bash-one-liners-explained-part-three) — Every spell for the master wizard

---

*The Rift closes behind you. The dungeon is conquered. Every command a spell — every pipe a portal.* 🌀⚔️✨

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0000 - Foundation & Init World]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Bashcrawl Chamber: Bash Arithmetic and the Statue Boss]] · [[Bashcrawl Hidden Chapel: Hidden Files and Man Pages]]
**Unlocks:** [[Bashcrawl Agent Mode: AI Automation and Contribution]]
**Sequel quests:** [[Bashcrawl Agent Mode: AI Automation and Contribution]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]

