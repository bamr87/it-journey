---
title: 'The Great Forge: Assemble a Desktop from Bare Parts'
description: Build a desktop PC from bare parts in a safe order, reach a first boot and diagnose it if it stays dark, set the firmware options that gaming depends on, and prove the memory with a Memtest86+ pass.
excerpt: Assemble a gaming desktop from parts, troubleshoot the first boot, tune the firmware, and test the memory.
date: '2026-11-06T00:00:00.000Z'
lastmod: '2026-11-06T00:00:00.000Z'
level: '0110'
difficulty: 🔴 Hard
estimated_time: 3-4 hours
primary_technology: hardware
quest_type: main_quest
quest_series: The Twin Rigs
quest_line: The Twin Rigs
quest_arc: The Great Forge
skill_focus: infrastructure
learning_style: hands-on
author: IT-Journey Team
permalink: /quests/0110/twin-rigs-05-the-great-forge/
fmContentType: quest
layout: quest
draft: false
comments: true
mermaid: true
categories:
- Quests
- Hardware
- PC Building
tags:
- '0110'
- hardware
- pc-building
- uefi
- memtest
- main_quest
- hands-on
- gamified-learning
keywords:
  primary:
  - '0110'
  - hardware
  - gaming-rig
  secondary:
  - pc-assembly
  - uefi
  - memtest86
  - troubleshooting
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Has a ledger that passes every check from Chapter I
  - Can follow a motherboard manual
  system_requirements:
  - 'All desktop parts, a Phillips #2 screwdriver, and a clear table'
  - A USB drive and a fortress machine
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/0101/twin-rigs-04-the-caravan-road/
  unlocks_quests:
  - /quests/0111/twin-rigs-06-the-steam-rite/
rewards:
  badges:
  - 🔥 Forgehand — built a desktop from bare parts and proved it stable
  skills_unlocked:
  - 🔧 PC assembly and fault isolation
  - 🧪 UEFI setup and memory testing
  progression_points: 120
validation_criteria:
  completion_requirements:
  - The rig reaches firmware reliably
  - Memtest86+ finishes a pass with zero errors
  skill_demonstrations:
  - Can isolate a boot fault by changing one thing at a time
  knowledge_checks:
  - Explains why EXPO or XMP must be enabled
environment:
  os:
  - linux
  - macos
  - windows
  shell:
  - bash
  - zsh
  - powershell
  pkg:
  - brew
  - winget
---
*The boxes arrive, and the table is suddenly too small. Building a computer feels dangerous the first time, but it is closer to a careful set of building blocks: every connector is keyed, and most parts fit only one way. The real enemies are haste, static, and a screw left behind. Lay out your tools. Tonight the Great Rig takes shape.*

## 🎯 Quest Objectives

By the end of this chapter you will:

- [ ] **Assemble a desktop PC** from bare parts in a safe order
- [ ] **Reach a first boot** and diagnose it if it stays dark
- [ ] **Tune the firmware** so your memory and graphics card run as designed
- [ ] **Test the memory** with a full Memtest86+ pass
- [ ] **Log the build** in your chronicle, including anything that went wrong

## 🗺️ Quest Prerequisites

- **[Chapter I](/quests/0010/twin-rigs-01-the-war-chest/)** — a ledger that passes every check, and the parts it lists
- **A Phillips #2 screwdriver** and a clear, dry, well-lit table
- **Your motherboard manual** — open it now and keep it open, because it outranks this quest for your exact board
- **A USB drive** — for the memory test in Chapter 4
- **Your fortress** — to write that USB drive

> ⚠️ **Safety first:** Never open a power supply, even an unplugged one, because it can hold a dangerous charge. Switch off and unplug the PSU before you touch anything inside the case. Work on a hard surface rather than carpet, and touch bare metal on the case often to discharge static.

## 🌍 Choose Your Adventure Platform

*The build is the same everywhere. Your fortress only needs a way to write the Memtest86+ USB drive.*

### 🍎 macOS

```bash
brew install --cask balenaetcher
```

### 🪟 Windows

```powershell
winget install Rufus.Rufus
```

### 🐧 Linux

```bash
# Etcher's AppImage works here too, from https://etcher.balena.io/
lsblk -o NAME,SIZE,MODEL
```

## 🧙‍♂️ Chapter 1: Build Outside the Case

### ⚔️ Skills You'll Forge

- Installing the parts that are hard to reach later
- Handling a CPU without damaging it

Put the motherboard on its box, not on the anti-static bag, and work through this order. Each step is easier now than it will be once the board is inside the case.

1. **CPU.** Lift the socket's retention arm, line up the triangle on the CPU with the triangle on the socket, and lower it straight in. It should drop in with no force. Close the arm, which takes some pressure on many boards. That is normal.
2. **M.2 SSD.** Slide it into the top M.2 slot at an angle, press it flat, and secure it with the small screw or latch. Remove any plastic film from the slot's heatsink.
3. **RAM.** Open the clips and check the manual for the right slots, which is usually the second and fourth for two sticks. Line up the notch, then press firmly until the clips click.
4. **CPU cooler.** Follow its own guide. Most coolers need a pea-sized dot of thermal paste unless paste is already applied. Tighten the screws a little at a time in a cross pattern, and plug the fan into the `CPU_FAN` header.

### 🔍 Knowledge Check

- [ ] What should you do if the CPU does not drop in without force?
- [ ] Why does the manual decide which RAM slots to use?

## 🧙‍♂️ Chapter 2: Raise the Rig

### ⚔️ Skills You'll Forge

- Mounting a board without shorting it
- Reading front-panel and power connectors

1. **Prepare the case.** Remove both side panels, then fit the I/O shield if your board does not have one built in. Check that the standoffs match your board's holes. A stray standoff can short the board.
2. **Mount the PSU.** Point its fan toward the case's vent, usually downward, and fasten it with four screws.
3. **Mount the board.** Lower it onto the standoffs, line up the rear ports with the I/O opening, and tighten the screws until snug.
4. **Connect power.** Plug in the large 24-pin connector and the 4+4-pin CPU power connector at the top of the board.
5. **Connect the case.** Attach the front-panel pins using the manual's diagram, then the USB and audio headers, then the case fans.
6. **Fit the GPU last.** Remove the matching slot covers, press the card into the top long PCIe slot until the latch clicks, and screw it to the case. Connect every power cable it asks for, and push each one in fully.

Check for a loose screw before you close anything. Shake the case very gently. If it rattles, find out why.

### 🔍 Knowledge Check

- [ ] Why is the GPU installed last?
- [ ] What can an extra standoff do to a motherboard?

## 🧙‍♂️ Chapter 3: The First Spark

### ⚔️ Skills You'll Forge

- Diagnosing a machine that will not start
- Changing one thing at a time

Connect your monitor to the **graphics card**, not the motherboard. Plug in a keyboard, the power cord, and flip the PSU switch on. Press the power button.

A first boot can take a few minutes while the board trains its memory. The screen may stay black longer than you expect, so give it up to five minutes before you assume a fault. If you reach the firmware screen, you have won this fight.

If it does not, work down this table and change only one thing at a time:

| Symptom | Check first |
|---|---|
| Nothing happens at all | PSU switch, power cord, front-panel power pins, 24-pin connector |
| Fans spin, no picture | Monitor cable in the GPU, GPU power cables, RAM fully clicked in |
| A debug light stays on | Your manual's meaning for the CPU, DRAM, VGA, or BOOT light |
| Restarts over and over | CPU power connector, then try one RAM stick |
| Beep codes | Look up the pattern in your manual |

### 🔍 Knowledge Check

- [ ] Why plug the monitor into the graphics card?
- [ ] Why should you change only one thing between attempts?

## 🧙‍♂️ Chapter 4: Tune the Firmware and Test the Memory

### ⚔️ Skills You'll Forge

- Setting the firmware options that gaming depends on
- Proving memory stability with a dedicated tool

Press `Del` or `F2` during boot to enter the UEFI firmware. Names vary between brands, so look for these in your manual:

| Setting | Set it to | Why |
|---|---|---|
| **EXPO or XMP** | Enabled | RAM runs at a slower default speed until you turn this on |
| **Resizable BAR** | Enabled | Lets the CPU reach more of the GPU's memory at once |
| **Boot mode** | UEFI (CSM off) | SteamOS is a UEFI operating system |
| **Fan curves** | Default or Standard | A sensible starting point, and you will revisit it in Chapter VIII |
| **Secure Boot** | Leave it for now | You will turn it off in Chapter VI |

Memory faults look like random game crashes, and they are miserable to find later. Catch them now while the parts are still easy to return. Download the USB image from [memtest.org](https://www.memtest.org/), write it to your USB drive with Etcher or Rufus, then boot from it.

Let it run for at least one full pass. More passes are better, and running it overnight is a fine choice. Any error at all means something is wrong. Turn EXPO or XMP off and test again. If errors remain, test each stick by itself to find the bad one.

### 🔍 Knowledge Check

- [ ] What does your RAM do if you never enable EXPO or XMP?
- [ ] How many Memtest86+ errors are acceptable?

## 🎮 Implementation Challenge

**Objective:** Finish a stable, tested machine, then record the build.

**Success Criteria:**

- [ ] The rig reaches the firmware screen every time
- [ ] The firmware reports the correct RAM size and speed
- [ ] The SSD and GPU both appear in the firmware
- [ ] Memtest86+ finishes at least one pass with zero errors
- [ ] The build log is committed

Back on your fortress, in `twin-rigs`, write the log. Be honest about the mistakes, because they are the most useful part of it.

```bash
cat >> build-log.md <<'EOF'
# Great Rig build log

- Date:
- Firmware version:
- RAM speed after EXPO or XMP:
- Memtest86+ passes and errors:
- What went wrong and how I fixed it:
EOF
git add build-log.md
git commit -m "docs: record the Great Rig build"
```

## 🔍 Quest Network

```mermaid
graph LR
    C4[The Caravan Road] --> C5[🔥 The Great Forge]
    C5 --> C6[The Steam Rite]
```

## 🎁 Rewards & Progression

- 🔥 **Forgehand** — built a desktop from bare parts and proved it stable
- ⚡ **Skills unlocked:** PC assembly, fault isolation, UEFI configuration, memory testing
- 🏆 **120 XP** toward the campaign

*Chapters sit at different levels by design: the campaign uses the level number for progression, and each chapter also appears on its own level hub.*

## 🔮 Next Adventures

The rig stands ready, with an empty drive and a blank mind. Next you give it an operating system.

- ➡️ **Next chapter:** [Chapter VI — The Steam Rite](/quests/0111/twin-rigs-06-the-steam-rite/)
- ⬅️ **Previous chapter:** [Chapter IV — The Caravan Road](/quests/0101/twin-rigs-04-the-caravan-road/)
- 👑 **Campaign hub:** [Epic Quest: The Twin Rigs](/quests/codex/twin-rigs/)

## 📚 Resource Codex

- Your motherboard manual — the final authority on your exact board
- [Memtest86+](https://www.memtest.org/) — the open source memory tester used here
- [PCPartPicker build guides](https://pcpartpicker.com/guide/) — photo walkthroughs of finished builds

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Twin Rigs]] **Level hub:** [[Level 0110 (6) - Database Mastery]] **Previous:** [[The Caravan Road: Turn the Pi into a Console]] **Next:** [[The Steam Rite: Install SteamOS on the Great Rig]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
