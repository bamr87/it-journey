---
title: 'Bashcrawl Vault: Environment Variables and the Goblet Puzzle'
description: Master environment variables in Bashcrawl's Vault using export, echo $VAR, and env. Solve the goblet puzzle in the stronghold and survive a ghost encounter.
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
- environment-variables
- export
- '0000'
keywords:
  primary:
  - bash export command
  - environment variables linux
  - echo variable bash
  - env command
  secondary:
  - bashcrawl vault
  - shell environment
  - bash scripting variables
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
- Set a variable and access it with $VAR
- Export a variable and verify with env
- Solve the goblet puzzle using export
- Survive the ghost encounter using the correct environment variable
- Collect the vault key fragment
prerequisites:
- Complete the Cellar side-quest
learning_paths:
- Terminal Mastery Path
rewards:
- Vault Key Fragment
- Environment variables mastery
excerpt: Set, export, and inspect environment variables to solve the vault goblet puzzle, survive the ghost, and claim the key fragment.
draft: false
permalink: /quests/0000/side-quests/vault/
layout: quest
---
*Behind a heavy iron door, the Vault holds the dungeon's most powerful secrets — not gold and jewels, but the invisible variables that shape every shell. Set them correctly, or the ghost devours you.*

## 🎯 Quest Objectives

- [ ] Set and read shell variables with `=` and `$VAR`
- [ ] Export a variable with `export` so child processes see it
- [ ] Use `env` and `printenv` to inspect the shell environment
- [ ] Solve the goblet puzzle in the stronghold
- [ ] Survive the ghost encounter in the lab
- [ ] Collect the vault key fragment

## �️ Quest Prerequisites

- [Cellar side-quest](/quests/0000/side-quests/cellar/) complete
- Emerald amulet in inventory

## ⚡ Command Cheatsheet

| Command | What It Does |
|---------|-------------|
| `VAR=value` | Set a shell variable (local to current shell) |
| `export VAR=value` | Set and export to child processes |
| `echo $VAR` | Print a variable's value |
| `env` | Show all exported environment variables |
| `printenv VAR` | Print a specific env variable |
| `unset VAR` | Remove a variable |
| `export -p` | List all exports in a reusable format |

### Local vs Exported Variables

```bash
# Local — child scripts cannot see this:
SECRET=password

# Exported — child scripts and subshells inherit it:
export SECRET=password

# Verify inheritance:
export GREETING="Hello Dungeon"
bash -c 'echo $GREETING'   # prints: Hello Dungeon
```

## 🗺️ Walkthrough

### Step 1 — Enter the vault and read the stronghold scroll

```bash
cd .VAULT          # The vault may be hidden — use ls -a
ls -F
# stronghold/  nursery/  lab/  vault_scroll

cat vault_scroll
```

The scroll explains that each sub-area requires a specific environment variable to be set correctly.

### Step 2 — Stronghold: solve the goblet puzzle

```bash
cd stronghold
ls -F
# goblet*  inscription

cat inscription
# "The goblet demands the colour of magic. Set MAGIC_COLOR before running ./goblet."

export MAGIC_COLOR="purple"
./goblet
# The goblet glows purple. Correct!
# Vault door unlocked.
```

Different game sessions may demand different values. Read the inscription carefully.

### Step 3 — Nursery: learn about local variables

```bash
cd ../nursery
ls
# seeds  growth_chart  care_notes

cat care_notes
# "PLANT_NAME must be set to continue growing."

export PLANT_NAME="moonflower"
cat growth_chart
```

The nursery teaches that variables can store any string — command output, paths, names.

### Step 4 — Lab: the ghost encounter

```bash
cd ../lab
ls -a
# ghost*  .formula  beakers/

cat .formula
# "To banish the ghost: set GHOST_BANISH to the name found in the beakers."

ls beakers/
cat beakers/vial_7
# Value: "iron_salt"

export GHOST_BANISH="iron_salt"
./ghost
# Ghost banished! The lab is safe.
```

> If `GHOST_BANISH` is not set or wrong, `./ghost` reduces your HP substantially.

### Step 5 — Verify your environment

```bash
env | grep -E "MAGIC_COLOR|GHOST_BANISH|PLANT_NAME"
# MAGIC_COLOR=purple
# GHOST_BANISH=iron_salt
# PLANT_NAME=moonflower
```

### Step 6 — Collect the vault key fragment

```bash
cd ..
ls -F
# vault_key_fragment

cat vault_key_fragment
inventory
# vault key fragment ✓
```

## 💡 Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| `$VAR` prints empty | Variable not exported | Use `export VAR=value` |
| Ghost still attacks | Wrong value in `GHOST_BANISH` | Re-read `.formula` and beaker vial |
| `env` shows nothing | Non-exported variable | Use `export` or check with `set | grep VAR` |
| `./goblet` says "wrong" | Case mismatch | Variable values are case-sensitive |

## ✅ Validation

- [ ] You understand the difference between local and exported variables
- [ ] You ran `env` and found your variables in the output
- [ ] The goblet puzzle is solved
- [ ] The ghost is banished
- [ ] The vault key fragment is in your inventory

## ➡️ Next Steps

- **Complete other branches** → [Hidden Chapel](/quests/0000/side-quests/hidden-chapel/) · [Scrap](/quests/0000/side-quests/scrap/)
- **Enter the final gauntlet** → [The Rift](/quests/0000/side-quests/rift/)
- **Back to hub** → [Bashcrawl Hub](/quests/0000/bashcrawl/)

---

## 📚 External Resources

Continue your terminal adventure with these resources:

- [Bashcrawl Web Demo](https://bamr87.github.io/bashcrawl/) — Play in your browser, no installation required
- [Bashcrawl on GitHub](https://github.com/bamr87/bashcrawl) — Source code, setup, and open contributions
- [GNU Bash Manual — Environment](https://www.gnu.org/software/bash/manual/bash.html#Environment) — Variables and the shell realm
- [IT-Journey Bashcrawl Hub](/quests/0000/bashcrawl/) — Full quest series and walkthroughs
- [Linux Environment Variables](https://www.digitalocean.com/community/tutorials/how-to-read-and-set-environmental-and-shell-variables-on-linux) — Master the realm of variables

---

*The ghost dissolves. Variables mastered. The vault yields its secrets.* 🔒

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0000 - Foundation & Init World]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Bashcrawl Cellar: File Types, Aliases, and Emerald Amulet]]
**Unlocks:** [[Bashcrawl Rift: Pipes, Redirection, and the Final Boss]]
**Sequel quests:** [[Bashcrawl Rift: Pipes, Redirection, and the Final Boss]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]

