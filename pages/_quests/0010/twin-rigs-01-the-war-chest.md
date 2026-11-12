---
title: 'The War Chest: Plan Two Rigs Before You Spend a Coin'
description: Learn what every part in a gaming PC and a Raspberry Pi does, choose a tier for each rig, and write a parts ledger that a Python script checks for costly mistakes before you buy anything.
excerpt: Plan a Raspberry Pi arcade and a SteamOS desktop on paper, then let a script catch the expensive mistakes.
date: '2026-11-06T00:00:00.000Z'
lastmod: '2026-11-06T00:00:00.000Z'
level: '0010'
difficulty: 🟢 Easy
estimated_time: 45-90 minutes
primary_technology: hardware
quest_type: main_quest
quest_series: The Twin Rigs
quest_line: The Twin Rigs
quest_arc: Plan the Rigs
skill_focus: infrastructure
learning_style: hands-on
author: IT-Journey Team
permalink: /quests/0010/twin-rigs-01-the-war-chest/
fmContentType: quest
layout: quest
draft: false
comments: true
mermaid: true
categories:
- Quests
- Hardware
- Planning
tags:
- '0010'
- hardware
- planning
- python
- main_quest
- hands-on
- gamified-learning
keywords:
  primary:
  - '0010'
  - hardware
  - gaming-rig
  secondary:
  - parts-list
  - budgeting
  - compatibility
  - python
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Can run a Python 3 script from a terminal
  - Knows basic Git commands
  system_requirements:
  - macOS, Windows, or Linux
  - Python 3, Git, and a text editor
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/codex/twin-rigs/
  unlocks_quests:
  - /quests/0011/twin-rigs-02-the-rewind-cabinet/
rewards:
  badges:
  - 📒 Ledger Keeper — planned two builds and proved them on paper
  skills_unlocked:
  - 📒 Reading spec sheets and part compatibility
  - 🧮 Budgeting a build as data
  progression_points: 40
validation_criteria:
  completion_requirements:
  - A ledger.json with real prices reports 0 problems
  - The ledger and checker are committed
  skill_demonstrations:
  - Can explain the job of each part in a build
  knowledge_checks:
  - Explains why the GPU is chosen before the other desktop parts
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
  - apt
  - brew
  - winget
---
*Every great forge starts with a ledger. Adventurers who skip this step buy a memory kit that will not seat, a power supply one rung too small, or a graphics card their chosen operating system cannot use. Those mistakes cost real coin and a week of returns. Yours will cost one failed line in a terminal.*

## 🎯 Quest Objectives

By the end of this chapter you will:

- [ ] **Explain what each part does** in a Raspberry Pi and in a desktop PC
- [ ] **Choose a tier for each rig** based on what you actually want to play
- [ ] **Write a parts ledger** as data, with real prices you looked up
- [ ] **Run a compatibility check** that catches expensive mistakes before you buy
- [ ] **Start your `twin-rigs` repository**, the chronicle for the whole campaign

## 🗺️ Quest Prerequisites

- **A terminal, Git, and Python 3** — the check script uses only the standard library
- **A rough budget** — no purchases happen in this chapter
- **No hardware knowledge** — learning it is the point

## 🌍 Choose Your Adventure Platform

*The chronicle is the same everywhere. Only the summoning of Python differs.*

### 🍎 macOS

```bash
brew install python git
python3 --version
```

### 🪟 Windows

```powershell
winget install Python.Python.3.12 Git.Git
python --version
```

Use `python` wherever this chapter says `python3`.

### 🐧 Linux

```bash
sudo apt update && sudo apt install -y python3 git
python3 --version
```

## 🧙‍♂️ Chapter 1: Know Your Gear

### ⚔️ Skills You'll Forge

- Naming the job of every part in a build
- Spotting which parts must match each other

A computer is a small party of specialists. Learn what each one does, and the spec sheets stop looking like a foreign tongue.

| Part | Its job | What must match |
|---|---|---|
| **CPU** | Runs game logic and the operating system | The motherboard socket |
| **GPU** | Draws every frame, and matters most for modern games | SteamOS needs an AMD discrete GPU |
| **Motherboard** | Connects everything | CPU socket, RAM type, case size |
| **RAM** | Short-term memory for running games | DDR4 or DDR5, as the board requires |
| **SSD** | Long-term storage, including the operating system | A free M.2 slot on the board |
| **PSU** | Turns wall power into clean power for the parts | Enough watts and the right GPU cables |
| **Cooler and fans** | Carry heat away | CPU socket, and height inside the case |
| **Case** | Holds it all and shapes the airflow | Board size, GPU length, cooler height |

The Raspberry Pi puts the CPU, GPU, and RAM on one board, so you choose far fewer parts. Two choices still matter a great deal: the power supply and the cooling.

### 🔍 Knowledge Check

- [ ] Which part matters most for modern game frame rates?
- [ ] Name two parts that must match the motherboard.

## 🧙‍♂️ Chapter 2: Choose Your Tiers

### ⚔️ Skills You'll Forge

- Sizing hardware to the games you will play
- Finding the requirement that limits your whole build

**The Rewind Cabinet.** Rewind Arcade's own documentation rates each board by what it can emulate comfortably:

| Board | Comfortable through | Verdict |
|---|---|---|
| Pi 5 | PS1, N64, some Dreamcast and PSP | ✅ The campaign's choice |
| Pi 4 | PS1 (N64 and Dreamcast need per-game tuning) | 👍 A fine budget build |
| Pi 3 | 16-bit consoles | ⚠️ Only for an 8-bit and 16-bit shelf |
| Pi Zero 2 W | 8-bit and light 16-bit | ⚠️ A pocket toy, not this campaign's rig |

For a Pi 5, 4GB of RAM runs the arcade well, and 8GB buys headroom. Budget for the official 27W USB-C power supply, an Active Cooler, a case that fits them, a micro-HDMI cable, a microSD card, and a USB gamepad. An M.2 HAT+ and NVMe SSD are a worthwhile upgrade, because SD cards are slow and wear out.

**The Great Rig.** One rule outranks all the others: **SteamOS on a custom PC means an AMD discrete GPU**, because that is what Valve lists under beta support. Pick the card first, using benchmarks for the games and resolution you actually play. Then build the rest around it:

- **Resolution sets the GPU budget.** 1080p asks far less of a card than 4K.
- **32GB of RAM** is a comfortable target, and 16GB is workable.
- **Give SteamOS its own SSD**, at least 1TB. The installer wipes the whole device, so never plan to share that drive with another operating system.
- **Buy the PSU your GPU maker recommends,** from a reputable brand. A cheap power supply can take other parts with it when it fails.

Use [PCPartPicker](https://pcpartpicker.com/) to cross-check your list and see current prices. Then look up your exact card in the [SteamOS issue tracker](https://github.com/ValveSoftware/SteamOS) before you buy it.

> 🧭 **Already own an NVIDIA card?** It is not on Valve's list. [Bazzite](https://bazzite.gg/) is a community Linux build with a similar console-style Steam mode and NVIDIA images. You can follow most of Chapters VI and VII on it, with its own install steps.

### 🔍 Knowledge Check

- [ ] Why do you pick the graphics card before the other desktop parts?
- [ ] Why does SteamOS need its own drive?

## 🧙‍♂️ Chapter 3: Inscribe the Ledger

### ⚔️ Skills You'll Forge

- Recording a design as data under version control
- Writing a check that fails loudly

Create the chronicle. Everything you build in this campaign gets recorded here.

```bash
mkdir twin-rigs && cd twin-rigs
git init
```

Save this as `ledger.json`. Each `cost` starts at zero on purpose, because prices move every week and a number copied from a quest is already wrong. Replace them with today's prices, and change the sample parts to match your own choices.

```json
{
  "pi": {
    "budget": 250,
    "board": "Raspberry Pi 5 8GB",
    "psu_watts": 27,
    "active_cooler": true,
    "os_storage": "nvme",
    "parts": [
      {"name": "Raspberry Pi 5 8GB", "cost": 0},
      {"name": "27W USB-C power supply", "cost": 0},
      {"name": "Active Cooler", "cost": 0},
      {"name": "M.2 HAT+ and NVMe SSD", "cost": 0},
      {"name": "Case, micro-HDMI cable, microSD", "cost": 0},
      {"name": "USB gamepad", "cost": 0}
    ]
  },
  "desktop": {
    "budget": 1500,
    "gpu_vendor": "amd",
    "gpu_watts": 300,
    "cpu_watts": 120,
    "psu_watts": 750,
    "cpu_socket": "AM5",
    "board_socket": "AM5",
    "ram_type": "DDR5",
    "board_ram_type": "DDR5",
    "os_drive_dedicated": true,
    "parts": [
      {"name": "CPU", "cost": 0},
      {"name": "CPU cooler", "cost": 0},
      {"name": "Motherboard", "cost": 0},
      {"name": "32GB RAM kit", "cost": 0},
      {"name": "AMD graphics card", "cost": 0},
      {"name": "1TB+ NVMe SSD", "cost": 0},
      {"name": "750W power supply", "cost": 0},
      {"name": "Case and fans", "cost": 0}
    ]
  }
}
```

Now save the checker as `rig_check.py`. It tests the rules from this chapter, and it exits with an error if any rule fails.

```python
#!/usr/bin/env python3
"""Check ledger.json for mistakes that are cheap on paper and costly in a box."""
import json
import sys

ledger = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "ledger.json"))
pi, desktop = ledger["pi"], ledger["desktop"]
failures = 0


def check(ok, label, fix):
    global failures
    print(f"{'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        failures += 1
        print(f"      fix: {fix}")


def total(rig):
    return sum(part["cost"] for part in rig["parts"])


check(all(part["cost"] > 0 for rig in (pi, desktop) for part in rig["parts"]),
      "every part has a real price", "replace each 0 with a price you looked up today")
check(total(pi) <= pi["budget"], f"Pi total {total(pi)} fits budget {pi['budget']}",
      "drop to a smaller board or reuse a gamepad and cables")
check(total(desktop) <= desktop["budget"],
      f"desktop total {total(desktop)} fits budget {desktop['budget']}",
      "spend less on the case and CPU before the GPU")
check(pi["psu_watts"] >= 27, "Pi 5 has its 27W (5V/5A) supply",
      "a phone charger starves USB devices and invites undervoltage")
check(pi["active_cooler"], "Pi has active cooling", "add the Active Cooler or a fan case")
check(desktop["gpu_vendor"].lower() == "amd", "GPU is on SteamOS's AMD path",
      "buy an AMD card, or plan on Bazzite instead of SteamOS")
check(desktop["cpu_socket"] == desktop["board_socket"], "CPU fits the motherboard socket",
      "match the socket printed on both product pages")
check(desktop["ram_type"] == desktop["board_ram_type"], "RAM matches the motherboard",
      "DDR4 and DDR5 are keyed differently and will not swap")
check(desktop["os_drive_dedicated"], "SteamOS gets a whole drive",
      "the installer wipes the device, so give it its own SSD")
# A rule of thumb only. The GPU maker's recommended PSU rating outranks this line.
need = round((desktop["cpu_watts"] + desktop["gpu_watts"] + 75) * 1.5)
check(desktop["psu_watts"] >= need, f"PSU {desktop['psu_watts']}W covers about {need}W",
      "buy the rating the GPU maker recommends, or more")

print(f"\n{failures} problem(s). Pi {total(pi)} + desktop {total(desktop)} = {total(pi) + total(desktop)}")
sys.exit(1 if failures else 0)
```

Cast it right away:

```bash
python3 rig_check.py
```

The first line should fail, because every price is still zero:

```text
FAIL  every part has a real price
      fix: replace each 0 with a price you looked up today
```

That failure is the script doing its job. Fill in your real prices and run it again until it reports `0 problem(s)`.

The power line is only a rule of thumb: CPU watts plus GPU watts plus 75 for everything else, then 50% headroom. If your GPU maker recommends a bigger supply, their number wins.

### 🔍 Knowledge Check

- [ ] What exit code does the script return when a rule fails?
- [ ] Why does the ledger start with zero prices instead of sample prices?

## 🎮 Implementation Challenge

**Objective:** Prove the checker catches a bad build, then record a good one.

Change `gpu_vendor` to `nvidia` and `ram_type` to `DDR4`, then run the check. Restore both values and run it once more.

**Success Criteria:**

- [ ] The sabotaged ledger fails on both lines and exits non-zero
- [ ] Your real ledger reports `0 problem(s)`
- [ ] Your ledger and script are committed

```bash
git add ledger.json rig_check.py
git commit -m "docs: record the parts ledger for both rigs"
```

Only now should you buy anything. If money or time is short, buy the Pi parts first and start Chapter II while you save for the desktop.

## 🔍 Quest Network

```mermaid
graph LR
    Hub[👑 The Twin Rigs] --> C1[📒 The War Chest]
    C1 --> C2[The Rewind Cabinet]
```

## 🎁 Rewards & Progression

- 📒 **Ledger Keeper** — planned two builds and proved them on paper
- ⚡ **Skills unlocked:** reading spec sheets, compatibility checks, budgeting as data
- 🏆 **40 XP** toward the campaign

*Chapters sit at different levels by design: the campaign uses the level number for progression, and each chapter also appears on its own level hub.*

## 🔮 Next Adventures

Your ledger is clean. Time to open the first box and raise a rig that fits in your hand.

- ➡️ **Next chapter:** [Chapter II — The Rewind Cabinet](/quests/0011/twin-rigs-02-the-rewind-cabinet/)
- 👑 **Campaign hub:** [Epic Quest: The Twin Rigs](/quests/codex/twin-rigs/)

## 📚 Resource Codex

- [Rewind Arcade Raspberry Pi guide](https://github.com/bamr87/rewind-arcade/blob/main/emulate/docs/raspberry-pi.md) — the board table used in this chapter
- [SteamOS Installation and Repair](https://help.steampowered.com/en/faqs/view/65B4-2AA3-5F37-4227) — Valve's current hardware support list
- [PCPartPicker](https://pcpartpicker.com/) — compatibility checks and live prices
- [Raspberry Pi 27W power supply](https://www.raspberrypi.com/products/27w-power-supply/) — the supply the Pi 5 is designed around

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Twin Rigs]] **Level hub:** [[Level 0010 - Terminal Enhancement & Shell Mastery]] **Previous:** none — first chapter **Next:** [[The Rewind Cabinet: Raise a Healthy Raspberry Pi]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
