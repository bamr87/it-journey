---
title: 'The Caravan Road: Turn the Pi into a Console'
description: Move your game library out of the repository, sync it safely from your fortress with rsync, set up gamepad hotkeys, boot straight to ES-DE, and protect your save files with backups and scheduled checks.
excerpt: Sync your library, map a gamepad, autostart ES-DE, and guard your saves until the Pi behaves like a console.
date: '2026-11-06T00:00:00.000Z'
lastmod: '2026-11-06T00:00:00.000Z'
level: '0101'
difficulty: 🟡 Medium
estimated_time: 1-2 hours
primary_technology: emulation
quest_type: main_quest
quest_series: The Twin Rigs
quest_line: The Twin Rigs
quest_arc: The Caravan Road
skill_focus: infrastructure
learning_style: hands-on
author: IT-Journey Team
permalink: /quests/0101/twin-rigs-04-the-caravan-road/
fmContentType: quest
layout: quest
draft: false
comments: true
mermaid: true
categories:
- Quests
- Raspberry Pi
- Emulation
- Automation
tags:
- '0101'
- raspberry-pi
- emulation
- rsync
- backups
- main_quest
- hands-on
- gamified-learning
keywords:
  primary:
  - '0101'
  - emulation
  - gaming-rig
  secondary:
  - rewind-arcade
  - autostart
  - cron
  - gamepad
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Has completed Chapter III of The Twin Rigs
  - Can edit a YAML file
  system_requirements:
  - Rewind Arcade running on the Pi
  - rsync on your fortress and a USB gamepad
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/0100/twin-rigs-03-waking-the-arcade/
  unlocks_quests:
  - /quests/0110/twin-rigs-05-the-great-forge/
rewards:
  badges:
  - 🐫 Caravan Master — turned a project into a console with safe saves
  skills_unlocked:
  - 🐫 Safe rsync workflows with dry runs
  - 🛡️ Backups and scheduled integrity checks
  progression_points: 80
validation_criteria:
  completion_requirements:
  - The Pi boots to ES-DE and plays with no keyboard
  - Saves reach the fortress with sync pull
  skill_demonstrations:
  - Can run a dry run and explain what it shows
  knowledge_checks:
  - Explains why saves are the data most worth protecting
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
---
*A machine that needs a keyboard to start a game is a project. A machine that wakes straight to its game list, answers a gamepad, and keeps your saves safe is a console. Between those two lies a short road: a caravan that carries your library from fortress to cabinet, and carries your saves home again.*

## 🎯 Quest Objectives

By the end of this chapter you will:

- [ ] **Separate your library from the code** so that the two can be replaced independently
- [ ] **Sync games from your fortress** with a dry run first, every time
- [ ] **Set up a gamepad and hotkeys** once, for every system
- [ ] **Boot straight into ES-DE** with no keyboard attached
- [ ] **Back up your saves** and check your library for corruption on a schedule

## 🗺️ Quest Prerequisites

- **[Chapter III](/quests/0100/twin-rigs-03-waking-the-arcade/)** — Rewind Arcade running on the Pi
- **`rsync` on your fortress** — it ships with macOS and most Linux systems
- **A USB gamepad** — the one from your ledger

## 🌍 Choose Your Adventure Platform

*The fortress side needs a copy of the tool and `rsync`. The Pi side is the same for everyone.*

### 🍎 macOS

```bash
git clone https://github.com/bamr87/rewind-arcade.git
cd rewind-arcade
./bin/retropi config init
```

### 🪟 Windows

```powershell
# rsync needs a Linux shell, so run this chapter's fortress steps inside WSL.
wsl --install -d Ubuntu
```

Then follow the Linux path in the Ubuntu shell.

### 🐧 Linux

```bash
sudo apt update && sudo apt install -y rsync git
git clone https://github.com/bamr87/rewind-arcade.git
cd rewind-arcade
./bin/retropi config init
```

## 🧙‍♂️ Chapter 1: Give the Library Its Own Home

### ⚔️ Skills You'll Forge

- Keeping data apart from the code that uses it
- Using absolute paths in configuration

Your games should not live inside a Git checkout. On the Pi, make a home for them and point the tool at it. The folder names are not a free choice: `retropi sync` writes to `roms`, `BIOS`, and `saves` under the target path, so the Pi's settings have to match.

```bash
ssh rig@rewind.local
mkdir -p ~/arcade/roms ~/arcade/BIOS ~/arcade/saves
cd ~/rewind-arcade
./bin/retropi config set paths.roms /home/rig/arcade/roms
./bin/retropi config set paths.bios /home/rig/arcade/BIOS
./bin/retropi config set paths.saves /home/rig/arcade/saves
./bin/retropi build
./bin/retropi roms add ~/nova.nes --system nes
./bin/retropi build
```

If your Pi boots from a microSD card, consider a USB SSD for this folder and use its mount point instead. SD cards are slow and wear out, and a save file is the last thing you want on a dying card.

### 🔍 Knowledge Check

- [ ] Why move games out of the repository?
- [ ] What breaks if the Pi's `paths.bios` does not match the sync target?

## 🧙‍♂️ Chapter 2: Send the Caravan

### ⚔️ Skills You'll Forge

- Describing a remote machine as configuration
- Making dry runs a habit

On your fortress, describe the Pi once. Run `./bin/retropi config edit` and add this to `emulate/config/local.yaml`:

```yaml
sync:
  targets:
    pi:
      host: rewind.local
      user: rig
      path: /home/rig/arcade
      include: [roms, bios]
```

Put a game you own in the fortress's `emulate/roms/<system-id>/` folder, or use `nova.nes` again. Look first, and only then send:

```bash
./bin/retropi sync push pi --dry-run
./bin/retropi sync push pi
ssh rig@rewind.local 'cd rewind-arcade && ./bin/retropi build'
```

Read the dry-run output every time. It shows exactly what `rsync` is about to do, and it is the cheapest safety check you will ever run.

### 🔍 Knowledge Check

- [ ] What does `--dry-run` protect you from?
- [ ] Why does the Pi need a `build` after new games arrive?

## 🧙‍♂️ Chapter 3: One Gamepad to Rule the Shelf

### ⚔️ Skills You'll Forge

- Setting input once and applying it everywhere
- Defining a safe way out of a running game

Plug the gamepad into the Pi, launch RetroArch from the frontend, and map it once. Then have the tool write the same hotkeys for every system. Add this to `emulate/config/local.yaml` on the Pi:

```yaml
controls:
  hotkey_enable: select
  hotkeys:
    exit: start
    menu: x
    save_state: r
    load_state: l
```

Apply it to your real RetroArch settings:

```bash
./bin/retropi build --apply-retroarch
```

Select plus Start now quits any game back to ES-DE. That one combination is what lets you put the keyboard away.

### 🔍 Knowledge Check

- [ ] Why is a quit hotkey essential on a machine with no keyboard?
- [ ] What does `--apply-retroarch` change?

## 🧙‍♂️ Chapter 4: Wake Straight to the Arcade

### ⚔️ Skills You'll Forge

- Starting a desktop application at login
- Setting a machine to log itself in

ES-DE needs a graphical session, so you autostart it inside the desktop. This is the same approach Rewind Arcade's own first-boot installer uses. Run it on the Pi:

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/rewind-arcade.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Rewind Arcade
Exec=$HOME/rewind-arcade/bin/retropi frontend launch
X-GNOME-Autostart-enabled=true
EOF
sudo raspi-config nonint do_boot_behaviour B4
sudo reboot
```

`B4` tells the Pi to boot to the desktop and log in automatically. Keep this rig on your home network only, since anyone at the keyboard reaches a logged-in session.

> 🧭 **The fast road:** on a fresh Raspberry Pi OS card mounted on a Mac or Linux fortress, `./bin/retropi provision` writes a first-boot installer that performs these setup steps by itself. Try it on your next build, now that you know what it automates.

### 🔍 Knowledge Check

- [ ] Why not start ES-DE from a bare console?
- [ ] What does `B4` change, and what is the risk?

## 🧙‍♂️ Chapter 5: Guard the Saves

### ⚔️ Skills You'll Forge

- Backing up the data you cannot download again
- Scheduling an integrity check

A game can be restored. Thirty hours of progress cannot. Bring saves home by adding them to the command, and do it before any big change:

```bash
./bin/retropi sync pull pi saves --dry-run
./bin/retropi sync pull pi saves
```

On the Pi, record a checksum for each game, then schedule a weekly check. `roms verify` exits non-zero when something is corrupt or missing, so a failure is easy to spot in the log.

```bash
./bin/retropi roms checksum
( crontab -l 2>/dev/null; echo '0 4 * * 0 cd $HOME/rewind-arcade && ./bin/retropi roms verify >> $HOME/arcade/verify.log 2>&1' ) | crontab -
```

Keep ROMs, BIOS files, and saves out of your `twin-rigs` repository. They are personal, and game files must never reach a public repository.

### 🔍 Knowledge Check

- [ ] Which direction do saves usually travel, and why?
- [ ] How would you notice that a game file went bad?

## 🎮 Implementation Challenge

**Objective:** Run the cabinet as a console, with no keyboard, for one full session.

**Success Criteria:**

- [ ] With the keyboard unplugged, the Pi boots to ES-DE
- [ ] A game launches, saves, and quits using only the gamepad
- [ ] After `sync pull`, that save exists on your fortress
- [ ] `./bin/retropi roms verify` passes on the Pi

Write down what you learned in your chronicle, and commit it:

```bash
git add README.md
git commit -m "docs: record the Pi console setup"
```

## 🔍 Quest Network

```mermaid
graph LR
    C3[Waking the Arcade] --> C4[🐫 The Caravan Road]
    C4 --> C5[The Great Forge]
```

## 🎁 Rewards & Progression

- 🐫 **Caravan Master** — turned a project into a console with safe saves
- ⚡ **Skills unlocked:** `rsync` workflows, autostart, scheduled integrity checks, backup discipline
- 🏆 **80 XP** toward the campaign

*Chapters sit at different levels by design: the campaign uses the level number for progression, and each chapter also appears on its own level hub.*

## 🔮 Next Adventures

The first rig is complete. The second one will not fit in your hand.

- ➡️ **Next chapter:** [Chapter V — The Great Forge](/quests/0110/twin-rigs-05-the-great-forge/)
- ⬅️ **Previous chapter:** [Chapter III — Waking the Arcade](/quests/0100/twin-rigs-03-waking-the-arcade/)
- 👑 **Campaign hub:** [Epic Quest: The Twin Rigs](/quests/codex/twin-rigs/)

## 📚 Resource Codex

- [Rewind Arcade Pi guide](https://github.com/bamr87/rewind-arcade/blob/main/emulate/docs/raspberry-pi.md) — storage, sync, autostart, and controllers
- [Rewind Arcade command reference](https://github.com/bamr87/rewind-arcade/blob/main/emulate/docs/commands.md) — every flag used here
- [Raspberry Pi configuration docs](https://www.raspberrypi.com/documentation/computers/configuration.html) — `raspi-config` in detail

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Twin Rigs]] **Level hub:** [[Level 0101 - Advanced Docker & DevOps]] **Previous:** [[Waking the Arcade: Bring Rewind Arcade to Life on the Pi]] **Next:** [[The Great Forge: Assemble a Desktop from Bare Parts]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
