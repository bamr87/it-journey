---
title: 'The Rewind Cabinet: Raise a Healthy Raspberry Pi'
description: Assemble a cooled Raspberry Pi, flash 64-bit Raspberry Pi OS with SSH ready, read its temperature and throttle flags, and hold a ten-minute stress vigil that proves the board can stand a long session.
excerpt: Assemble and flash a Raspberry Pi, then prove it healthy with throttle flags and a stress test.
date: '2026-11-06T00:00:00.000Z'
lastmod: '2026-11-06T00:00:00.000Z'
level: '0011'
difficulty: 🟡 Medium
estimated_time: 1-2 hours
primary_technology: raspberry-pi
quest_type: main_quest
quest_series: The Twin Rigs
quest_line: The Twin Rigs
quest_arc: The Rewind Cabinet
skill_focus: infrastructure
learning_style: hands-on
author: IT-Journey Team
permalink: /quests/0011/twin-rigs-02-the-rewind-cabinet/
fmContentType: quest
layout: quest
draft: false
comments: true
mermaid: true
categories:
- Quests
- Hardware
- Raspberry Pi
- Linux
tags:
- '0011'
- raspberry-pi
- hardware
- linux
- ssh
- main_quest
- hands-on
- gamified-learning
keywords:
  primary:
  - '0011'
  - raspberry-pi
  - gaming-rig
  secondary:
  - raspberry-pi-os
  - ssh
  - vcgencmd
  - stress-testing
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Can connect to a machine over SSH
  - Has completed Chapter I of The Twin Rigs
  system_requirements:
  - Raspberry Pi 4 or 5 with a proper power supply and cooling
  - A microSD card and a fortress machine
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/0010/twin-rigs-01-the-war-chest/
  unlocks_quests:
  - /quests/0100/twin-rigs-03-waking-the-arcade/
rewards:
  badges:
  - 🕹️ Cabinet Raiser — built a Pi and proved it healthy under load
  skills_unlocked:
  - 💾 Flashing images and headless SSH setup
  - 🌡️ Reading temperature and throttle flags
  progression_points: 60
validation_criteria:
  completion_requirements:
  - The Pi passes a ten-minute vigil with throttled=0x0
  - A health report is committed
  skill_demonstrations:
  - Can decode a vcgencmd get_throttled value
  knowledge_checks:
  - Explains why a long test finds what a short test misses
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
*The box is smaller than you expected. Inside sits a computer the size of a playing card, and it has one honest weakness: it will quietly slow itself down if you feed it poorly or let it run hot. Tonight you give it proper power, proper cooling, and an operating system. Then you hold a vigil to prove it can stand a long night.*

## 🎯 Quest Objectives

By the end of this chapter you will:

- [ ] **Assemble a Raspberry Pi** with active cooling and a proper power supply
- [ ] **Flash 64-bit Raspberry Pi OS** with SSH already set up
- [ ] **Reach the Pi from your fortress** over SSH with no monitor attached
- [ ] **Read its health** using temperature and throttle flags
- [ ] **Pass a 10-minute stress vigil** and record the result in your chronicle

## 🗺️ Quest Prerequisites

- **[Chapter I](/quests/0010/twin-rigs-01-the-war-chest/)** — your ledger and `twin-rigs` repository
- **The Pi parts** — board, 27W supply, Active Cooler, case, microSD card, and micro-HDMI cable
- **An SSH key on your fortress** — run `ssh-keygen -t ed25519` if you do not have one
- **A network** — Ethernet is best, and you will want it for streaming in Chapter VIII

## 🌍 Choose Your Adventure Platform

*Raspberry Pi Imager writes the operating system to your card. Summon it on your fortress.*

### 🍎 macOS

```bash
brew install --cask raspberry-pi-imager
```

### 🪟 Windows

```powershell
winget install RaspberryPiFoundation.RaspberryPiImager
```

### 🐧 Linux

```bash
sudo apt update && sudo apt install -y rpi-imager
```

## 🧙‍♂️ Chapter 1: Assemble the Cabinet

### ⚔️ Skills You'll Forge

- Handling a bare circuit board safely
- Fitting cooling and storage in the right order

Work on a clean, dry table, and unplug the Pi for every hardware change. Touch something metal first to discharge static, and hold the board by its edges.

1. **Fit the Active Cooler.** Remove the backing from the thermal pads, push its two spring pins through the board's mounting holes, then plug the fan cable into the four-pin fan header.
2. **Add the M.2 HAT+ if your ledger has one.** Follow the [official guide](https://www.raspberrypi.com/documentation/accessories/m2-hat-plus.html). The ribbon cable is delicate, so seat it gently.
3. **Close the case.** Make sure it does not block the fan.

Leave the microSD slot empty for now. The card comes next.

### 🔍 Knowledge Check

- [ ] Why should you touch metal before handling the board?
- [ ] What must stay clear when you close the case?

## 🧙‍♂️ Chapter 2: Flash the Operating System

### ⚔️ Skills You'll Forge

- Writing a bootable image to a storage card
- Pre-configuring a machine so it needs no monitor

Open Raspberry Pi Imager and make these choices:

| Setting | Choose |
|---|---|
| **Device** | Your Pi model |
| **Operating system** | **Raspberry Pi OS (64-bit)**, the desktop edition |
| **Storage** | Your microSD card (check the name and size carefully) |
| **Hostname** | `rewind` |
| **User** | `rig`, with a strong password |
| **Services** | Enable SSH with public-key login, and paste your public key |
| **Wi-Fi** | Only if you have no Ethernet cable |

Two of those choices are not optional. Rewind Arcade's frontend needs a **64-bit** operating system and a **graphical session**, so the Lite edition will not do.

> ⚠️ Imager erases the storage you select. Check the drive name and size twice before you confirm.

Put the card in the Pi, connect Ethernet, and connect the power supply last. Give the first boot a few minutes, then reach it from your fortress:

```bash
ssh rig@rewind.local
```

If the name does not resolve, find the Pi's IP address on your router's device list and use that instead. Once you are in, bring everything up to date:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### 💽 Optional: Move to NVMe

If you fitted an NVMe drive, run Raspberry Pi Imager on the Pi itself and write the same OS to the drive. Then set the boot order:

```bash
sudo raspi-config
# Advanced Options > Boot Order > NVMe/USB boot, then Finish
sudo reboot
```

Leave PCIe at its default speed. Gen 3 is faster, but Raspberry Pi warns that the Pi 5 is not certified for it and that connections might be unstable. Your retro library does not need that risk.

### 🔍 Knowledge Check

- [ ] Why is the Lite edition the wrong choice for this rig?
- [ ] What does the `.local` in `rewind.local` let you avoid looking up?

## 🧙‍♂️ Chapter 3: Read the Omens

### ⚔️ Skills You'll Forge

- Reading temperature and throttle state from firmware
- Decoding a hexadecimal status value

Two spells tell you how the Pi really feels:

```bash
vcgencmd measure_temp
vcgencmd get_throttled
```

A healthy idle Pi looks something like this:

```text
temp=45.2'C
throttled=0x0
```

`0x0` means nothing has gone wrong since boot. Any other value is a set of flags:

| Bit | Meaning | Likely cause |
|---|---|---|
| `0x1` | Undervoltage right now | Weak power supply or cable |
| `0x2` | Arm frequency capped right now | Heat |
| `0x4` | Throttled right now | Heat or power |
| `0x8` | Soft temperature limit active right now | Heat |
| `0x10000` | Undervoltage has happened since boot | Weak power supply or cable |
| `0x20000` | Frequency cap has happened since boot | Heat |
| `0x40000` | Throttling has happened since boot | Heat or power |
| `0x80000` | Soft temperature limit has happened since boot | Heat |

The flags add together, so `0x50000` means undervoltage and throttling have both happened since boot. Raspberry Pi's documentation says the Arm cores start to throttle progressively between 80°C and 85°C, and at 85°C both the cores and the GPU are throttled.

### 🔍 Knowledge Check

- [ ] What does `throttled=0x50005` tell you that `0x50000` does not?
- [ ] Which flag points at the power supply rather than heat?

## 🧙‍♂️ Chapter 4: Keep the Vigil

### ⚔️ Skills You'll Forge

- Running a sustained load test
- Capturing machine state as a repeatable report

A quick test proves nothing, because heat takes time to build. Install a stress tool and load all four cores for ten minutes:

```bash
sudo apt install -y stress-ng
stress-ng --cpu 4 --timeout 10m &
watch -n 10 'vcgencmd measure_temp; vcgencmd get_throttled'
```

Press `Ctrl+C` to leave `watch` when the run ends. You want the temperature to level off below 80°C and the throttle value to stay at `0x0`.

Now write a spell that records a machine's health. This same script runs on both rigs, so back on your fortress, in `twin-rigs`, save it as `rig-report.sh`:

```bash
#!/usr/bin/env bash
# Write one Markdown health report for the machine this runs on.
set -euo pipefail

mkdir -p reports
out="reports/$(hostname)-$(date +%Y-%m-%d).md"

section() {
  printf '\n## %s\n\n' "$1"
  shift
  "$@" 2>&1 | sed 's/^/    /' || true
}

{
  printf '# Rig report: %s\n\nTaken %s\n' "$(hostname)" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  section "Operating system" sh -c '. /etc/os-release && echo "$PRETTY_NAME"; uname -srm'
  section "Memory" free -h
  section "Drives" lsblk -o NAME,SIZE,TYPE,MOUNTPOINT
  if command -v vcgencmd >/dev/null; then
    section "Pi temperature" vcgencmd measure_temp
    section "Pi throttle flags" vcgencmd get_throttled
  else
    section "Graphics" sh -c 'lspci | grep -Ei "vga|3d|display"'
  fi
} > "$out"

echo "Wrote $out"
```

Send it to the Pi, run it, and bring the report home:

```bash
chmod +x rig-report.sh
scp rig-report.sh rig@rewind.local:
ssh rig@rewind.local ./rig-report.sh
mkdir -p reports
scp 'rig@rewind.local:reports/*.md' reports/
```

### 🔍 Knowledge Check

- [ ] Why does a ten-minute run tell you more than a one-minute run?
- [ ] If the vigil sets `0x10000`, what do you replace first?

## 🎮 Implementation Challenge

**Objective:** Finish the vigil with a clean result and record it.

**Success Criteria:**

- [ ] The temperature stays below 80°C for the full ten minutes
- [ ] `vcgencmd get_throttled` still reads `throttled=0x0` afterward
- [ ] Your report and script are committed

```bash
git add rig-report.sh reports
git commit -m "docs: record the Rewind Cabinet vigil"
```

If a flag appears, fix the cause and repeat the vigil. Reboot first, because the "since boot" flags only clear on a restart.

## 🔍 Quest Network

```mermaid
graph LR
    C1[The War Chest] --> C2[🕹️ The Rewind Cabinet]
    C2 --> C3[Waking the Arcade]
```

## 🎁 Rewards & Progression

- 🕹️ **Cabinet Raiser** — built a Pi and proved it healthy under load
- ⚡ **Skills unlocked:** image flashing, headless SSH setup, reading throttle flags, load testing
- 🏆 **60 XP** toward the campaign

*Chapters sit at different levels by design: the campaign uses the level number for progression, and each chapter also appears on its own level hub.*

## 🔮 Next Adventures

The cabinet is healthy but silent. Next you give it a library and a voice.

- ➡️ **Next chapter:** [Chapter III — Waking the Arcade](/quests/0100/twin-rigs-03-waking-the-arcade/)
- ⬅️ **Previous chapter:** [Chapter I — The War Chest](/quests/0010/twin-rigs-01-the-war-chest/)
- 👑 **Campaign hub:** [Epic Quest: The Twin Rigs](/quests/codex/twin-rigs/)

## 📚 Resource Codex

- [Raspberry Pi OS and Imager](https://www.raspberrypi.com/software/) — the official download
- [Raspberry Pi computer hardware docs](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html) — cooling and thermal limits
- [M.2 HAT+ guide](https://www.raspberrypi.com/documentation/accessories/m2-hat-plus.html) — NVMe fitting and boot steps

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Twin Rigs]] **Level hub:** [[Level 0011 - Development Tools & AI Integration]] **Previous:** [[The War Chest: Plan Two Rigs Before You Spend a Coin]] **Next:** [[Waking the Arcade: Bring Rewind Arcade to Life on the Pi]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
