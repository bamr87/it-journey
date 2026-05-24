---
title: 'Bashcrawl Chamber: Bash Arithmetic and the Statue Boss'
description: Defeat Bashcrawl's Statue Boss by solving arithmetic with let, expr, and $(( )). Mastering Bash math is the only weapon that can defeat this stone guardian.
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
- arithmetic
- variables
- '0000'
keywords:
  primary:
  - bash arithmetic
  - let command bash
  - shell arithmetic expansion
  - expr command
  secondary:
  - bashcrawl chamber
  - bash variables
  - shell scripting math
quest_dependencies:
  required_quests:
  - /quests/0000/side-quests/armoury/
  unlocks_quests:
  - /quests/0000/side-quests/rift/
quest_relationships:
  parent_quest: /quests/0000/bashcrawl/
  sequel_quests:
  - /quests/0000/side-quests/rift/
validation_criteria:
- Use let, expr, and $(( )) to compute values
- Assign arithmetic results to variables
- Defeat the Statue Boss
- Unlock the path to the Rift
prerequisites:
- Complete the Armoury side-quest
learning_paths:
- Terminal Mastery Path
rewards:
- Stone Key Fragment
- Bash arithmetic mastery
excerpt: Defeat the stone statue by using let, expr, and arithmetic expansion to solve Bash math challenges and unlock the Rift.
draft: false
permalink: /quests/0000/side-quests/chamber/
layout: quest
---
*A massive stone statue dominates the Chamber, its eyes glowing with arithmetic runes. It will not yield to a sword. Only correct calculations can break the enchantment — and wrong answers deal damage.*

## 🎯 Quest Objectives

- [ ] Compute values using `let`, `expr`, and `$(( ))`
- [ ] Assign arithmetic results to shell variables
- [ ] Solve the statue's puzzle correctly on the first attempt
- [ ] Run `./statue` to trigger and win the boss encounter
- [ ] Collect the Chamber's treasure and unlock the Rift path

## �️ Quest Prerequisites

- [Armoury side-quest](/quests/0000/side-quests/armoury/) complete
- Sword in inventory (from armoury `./sword`)

## ⚡ Command Cheatsheet

| Syntax | Example | Result |
|--------|---------|--------|
| `let "var=expr"` | `let "x=3*4"` | `x=12` |
| `expr a op b` | `expr 10 - 3` | `7` (printed) |
| `$((expr))` | `echo $((2**8))` | `256` |
| `$((var++))` | `echo $((n++))` | value then increment |

### Arithmetic Operators

| Operator | Meaning |
|----------|---------|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Integer division |
| `%` | Modulo (remainder) |
| `**` | Exponentiation |

## 🗺️ Walkthrough

### Step 1 — Enter the Chamber and read the runes

```bash
ls -F
# runes  statue*  chest
cat runes
```

The runes pose a riddle: *"To defeat me, compute the Vault Code: multiply the number of doors in the Cellar by the number of exits in the Entrance, then add 7."*

The numbers vary per game session. Example: 4 doors × 1 exit + 7 = **11**.

### Step 2 — Practice arithmetic first

```bash
# Method 1: let
let "vault_code = 4 * 1 + 7"
echo $vault_code     # 11

# Method 2: expr (each token must be a separate arg)
expr 4 \* 1 + 7     # 11  (escape * to avoid glob expansion)

# Method 3: arithmetic expansion (preferred modern style)
vault_code=$(( 4 * 1 + 7 ))
echo $vault_code     # 11
```

> **Recommendation:** Use `$(( ))` — it is cleaner, handles operator precedence correctly, and does not require `expr` to be installed.

### Step 3 — Compute your specific answer

Replace the example numbers with the values from YOUR runes:

```bash
# Template:
answer=$(( doors_in_cellar * exits_in_entrance + 7 ))
echo "My answer is: $answer"
```

### Step 4 — Face the statue

```bash
./statue
# The statue asks: "What is the Vault Code?"
# Enter your answer: 11
# CRACK! The statue crumbles. Victory!
```

Wrong answers reduce your HP. Make sure your math is right before running `./statue`.

### Step 5 — Loot the chest

```bash
cat chest
# Stone Key fragment obtained.
inventory
```

The stone key fragment is part of the multi-piece key that opens the Rift.

## 💡 Arithmetic Gotchas

| Problem | Cause | Fix |
|---------|-------|-----|
| `expr 4 * 1` → error | `*` glob-expanded | Escape: `expr 4 \* 1` |
| `let "x=5/2"` → `2` | Integer division | Use `bc` for floats: `echo "5/2" \| bc -l` |
| Variable not set | Missing `$` | Use `echo $var`, not `echo var` |
| Wrong answer, took damage | Calculation error | Recalculate carefully before `./statue` |

## ✅ Validation

- [ ] You computed the vault code using all three methods (let, expr, `$(( ))`)
- [ ] You solved the statue puzzle without taking damage
- [ ] The stone key fragment is in your inventory
- [ ] The Rift path is now unlocked (visible in `map`)

## ➡️ Next Steps

The stone key fragment is needed for the Rift — but you still need pieces from the other branches first.

Continue exploring:

- [Hidden Chapel](/quests/0000/side-quests/hidden-chapel/) — for the tome fragment
- [Vault](/quests/0000/side-quests/vault/) — for the goblet solution
- [Scrap Heap](/quests/0000/side-quests/scrap/) — for the portal link
- **When all four branches complete** → [The Rift](/quests/0000/side-quests/rift/)

---

## 📚 External Resources

Continue your terminal adventure with these resources:

- [Bashcrawl Web Demo](https://bamr87.github.io/bashcrawl/) — Play in your browser, no installation required
- [Bashcrawl on GitHub](https://github.com/bamr87/bashcrawl) — Source code, setup, and open contributions
- [GNU Bash Manual — Arithmetic](https://www.gnu.org/software/bash/manual/bash.html#Arithmetic-Expansion) — Shell arithmetic for the brave adventurer
- [IT-Journey Bashcrawl Hub](/quests/0000/bashcrawl/) — Full quest series and walkthroughs
- [Bash Arithmetic Guide](https://tldp.org/LDP/abs/html/arith-expansion.html) — Master the realm of numbers

---

*Stone dust settles. The Chamber is yours. Arithmetic — the ultimate weapon.* 🐉

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0000 - Foundation & Init World]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Bashcrawl Armoury: File Permissions and Script Execution]]
**Unlocks:** [[Bashcrawl Rift: Pipes, Redirection, and the Final Boss]]
**Sequel quests:** [[Bashcrawl Rift: Pipes, Redirection, and the Final Boss]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]

