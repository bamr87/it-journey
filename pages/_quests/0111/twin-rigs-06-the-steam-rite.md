---
title: 'The Steam Rite: Install SteamOS on the Great Rig'
description: Write Valve's recovery image to a USB drive, protect your other drives, install SteamOS on a dedicated SSD, learn Game Mode, Desktop Mode, and the read-only root, then run a game through Proton.
excerpt: Install SteamOS on your custom desktop safely, learn its two modes, and play through Proton.
date: '2026-11-06T00:00:00.000Z'
lastmod: '2026-11-06T00:00:00.000Z'
level: '0111'
difficulty: 🔴 Hard
estimated_time: 2-3 hours
primary_technology: steamos
quest_type: main_quest
quest_series: The Twin Rigs
quest_line: The Twin Rigs
quest_arc: The Steam Rite
skill_focus: infrastructure
learning_style: hands-on
author: IT-Journey Team
permalink: /quests/0111/twin-rigs-06-the-steam-rite/
fmContentType: quest
layout: quest
draft: false
comments: true
mermaid: true
categories:
- Quests
- SteamOS
- Linux
- Gaming
tags:
- '0111'
- steamos
- linux
- proton
- gaming
- main_quest
- hands-on
- gamified-learning
keywords:
  primary:
  - '0111'
  - steamos
  - gaming-rig
  secondary:
  - steam
  - immutable-os
  - amd-gpu
  - recovery-image
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Has completed Chapter V of The Twin Rigs
  - Can identify a disk with lsblk or a flashing tool
  system_requirements:
  - A desktop with an AMD discrete GPU and a dedicated SSD
  - A USB drive of at least 8GB and a Steam account
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/0110/twin-rigs-05-the-great-forge/
  unlocks_quests:
  - /quests/1000/twin-rigs-07-the-free-stalls/
rewards:
  badges:
  - ♨️ Rite Keeper — installed an immutable gaming OS on hardware you built
  skills_unlocked:
  - 💿 Safe disk imaging
  - 🔒 Working with an immutable operating system
  progression_points: 120
validation_criteria:
  completion_requirements:
  - SteamOS boots without the USB drive
  - A report from the rig is committed
  skill_demonstrations:
  - Can explain the difference between Repair SteamOS and Re-image Device
  knowledge_checks:
  - Explains why changes belong in the home folder
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
*This rite has one irreversible step, and it says so on the button: Wipe Device. SteamOS does not ask which partition you would like. It takes the whole drive, and in exchange it gives you an operating system that updates itself as one sealed piece and can be repaired from a USB key. Prepare the circle with care, and the rest of the spell is easy for any hero in the realm.*

## 🎯 Quest Objectives

By the end of this chapter you will:

- [ ] **Write Valve's recovery image** to a USB drive using the right tool for your fortress
- [ ] **Protect any other drives** before the installer runs
- [ ] **Install SteamOS** on your dedicated SSD
- [ ] **Explain Game Mode, Desktop Mode, and the read-only root** and why you should not fight them
- [ ] **Run a Windows game through Proton** and read a compatibility report
- [ ] **Generate a health report** from the Great Rig

## 🗺️ Quest Prerequisites

- **[Chapter V](/quests/0110/twin-rigs-05-the-great-forge/)** — a stable, memory-tested desktop with an AMD discrete GPU
- **A USB drive of at least 8GB** — it will be erased
- **Wired Ethernet** if you can manage it, plus a keyboard and mouse
- **A Steam account**

> ⚠️ **Beta territory:** Valve lists AMD discrete GPUs under *Beta SteamOS Support*, and says Steam Support may have limited ability to help with hardware beyond its official devices. Expect some rough edges, and report what you find to the [SteamOS issue tracker](https://github.com/ValveSoftware/SteamOS).

## 🌍 Choose Your Adventure Platform

*Download the image for Deck, Machine, and PC from [Valve's install page](https://help.steampowered.com/en/faqs/view/65B4-2AA3-5F37-4227). Only use Valve's own link, because third-party copies of an operating system are not worth the risk. Then write it to your USB drive.*

### 🍎 macOS

```bash
brew install --cask balenaetcher
# Open Etcher, choose the recovery file, choose your USB drive, then Flash.
```

### 🪟 Windows

```powershell
winget install Rufus.Rufus
# Open Rufus, select the recovery file, write it to your USB drive, then Close and eject.
```

### 🐧 Linux

Etcher works here too, or you can write it directly. First identify the USB drive, because `dd` will overwrite whatever you point it at without asking.

```bash
lsblk -o NAME,SIZE,MODEL
# Use your real file name, and replace sdX with your USB drive.
bzcat steamdeck-recovery-4.img.bz2 | sudo dd if=/dev/stdin of=/dev/sdX oflag=sync status=progress bs=128M
```

## 🧙‍♂️ Chapter 1: Prepare the Circle

### ⚔️ Skills You'll Forge

- Reducing the blast radius of a destructive operation
- Changing firmware boot settings

The installer's job is to wipe a device, so make sure there is only one device it can reach.

1. **Shut down and unplug the rig.** Physically disconnect every drive except the SteamOS SSD. Unplug other SATA cables, remove extra NVMe drives, and pull any external drives. It takes five minutes, and it is the only guarantee you get.
2. **Plug the rig in and enter the firmware** with `Del` or `F2`.
3. **Disable Secure Boot.** Valve notes that most devices need this in order to boot from USB. Look under the Boot or Security tab.
4. **Save and exit,** with the USB drive plugged in.

### 🔍 Knowledge Check

- [ ] Why unplug other drives instead of just being careful in the installer?
- [ ] Which firmware setting usually blocks booting from the USB drive?

## 🧙‍♂️ Chapter 2: Perform the Rite

### ⚔️ Skills You'll Forge

- Booting from an external installer
- Following a destructive procedure step by step

1. **Open the boot menu** as the rig starts. The key varies by board, and it is often `F8`, `F11`, or `F12`.
2. **Choose your USB drive,** picking the UEFI entry.
3. **Wait.** The screen goes dark while it boots, so give it a minute.
4. **Use the mouse** on the desktop that appears, and select **Wipe Device & Install SteamOS**.
5. **Reboot when it finishes,** and remove the USB drive.

You will land in the SteamOS welcome experience. Connect to your network, sign in to Steam, and let it update.

Keep that USB drive. It also offers **Repair SteamOS**, which reinstalls the system while attempting to keep your games and personal content. That recovery path is one of the best reasons to use this operating system.

### 🔍 Knowledge Check

- [ ] Which recovery option tries to keep your games?
- [ ] What does the Re-image Device option do to your data?

## 🧙‍♂️ Chapter 3: Learn the Two Faces

### ⚔️ Skills You'll Forge

- Moving between console and desktop environments
- Working with an immutable operating system

SteamOS has two faces, and you will use both:

| | 🎮 Game Mode | 🖥️ Desktop Mode |
|---|---|---|
| **Feels like** | A game console | A KDE Plasma Linux desktop |
| **Best with** | A gamepad | A keyboard and mouse |
| **Use it for** | Playing | Installing apps and maintenance |
| **Get there** | Return to Gaming Mode icon | Steam menu, Power, Switch to Desktop |

Switch to Desktop Mode, open the **Konsole** terminal, and look around. Set a password first, because `sudo` needs one:

```bash
passwd
cat /etc/os-release
sudo steamos-readonly status
df -h /home
```

The third line is the important one. The core of SteamOS is **read-only**. Each update replaces the whole system image, which is why updates are so dependable. It also means that anything you force onto the root filesystem with `pacman` can vanish at the next update. So follow one rule: **keep your changes in your home folder, and install apps with Flatpak.** You will do exactly that in Chapter VII.

### 🔍 Knowledge Check

- [ ] Why might a package installed with `pacman` disappear?
- [ ] What makes the read-only design a strength?

## 🧙‍♂️ Chapter 4: Meet Proton

### ⚔️ Skills You'll Forge

- Running Windows games on Linux
- Judging compatibility from evidence

Most Steam games target Windows. **Proton** is the compatibility layer, built on Wine, that translates their Windows calls into Linux ones as they run. Back in Game Mode, install a game from your library and launch it. If a game has no native Linux version, Steam uses Proton automatically.

Not every game works. Before you buy one, check its report on [ProtonDB](https://www.protondb.com/). Anti-cheat is the usual problem, because some online games refuse to run on Linux at all.

If a game misbehaves, open its **Properties**, then **Compatibility**, and try a different Proton version.

### 🔍 Knowledge Check

- [ ] What does Proton translate?
- [ ] What is the most common reason an online game will not run?

## 🎮 Implementation Challenge

**Objective:** Prove the install works, and record a report from the rig.

Your `rig-report.sh` from Chapter II works here too. In Desktop Mode, open Konsole, enable SSH for now, and find the rig's address:

```bash
sudo systemctl start sshd
ip -brief address
```

From your fortress, in `twin-rigs`, send the script over and bring the report back. The default SteamOS user is `deck`, and `<rig-ip>` is the address you just found.

```bash
scp rig-report.sh deck@<rig-ip>:
ssh deck@<rig-ip> ./rig-report.sh
scp 'deck@<rig-ip>:reports/*.md' reports/
git add reports
git commit -m "docs: record the Great Rig running SteamOS"
```

Then stop the SSH daemon on the rig, since you do not need it left running:

```bash
sudo systemctl stop sshd
```

**Success Criteria:**

- [ ] The rig boots into SteamOS with the USB drive removed
- [ ] The report shows your AMD GPU and the correct RAM
- [ ] A game launches and plays through Proton or natively
- [ ] Your other drives are reconnected and untouched

## 🔍 Quest Network

```mermaid
graph LR
    C5[The Great Forge] --> C6[♨️ The Steam Rite]
    C6 --> C7[The Free Stalls]
```

## 🎁 Rewards & Progression

- ♨️ **Rite Keeper** — installed an immutable gaming operating system on hardware you built
- ⚡ **Skills unlocked:** safe disk imaging, immutable OS operation, Proton troubleshooting
- 🏆 **120 XP** toward the campaign

*Chapters sit at different levels by design: the campaign uses the level number for progression, and each chapter also appears on its own level hub.*

## 🔮 Next Adventures

The Steam store is one door. The next chapter opens a much freer market.

- ➡️ **Next chapter:** [Chapter VII — The Free Stalls](/quests/1000/twin-rigs-07-the-free-stalls/)
- ⬅️ **Previous chapter:** [Chapter V — The Great Forge](/quests/0110/twin-rigs-05-the-great-forge/)
- 👑 **Campaign hub:** [Epic Quest: The Twin Rigs](/quests/codex/twin-rigs/)

## 📚 Resource Codex

- [SteamOS Installation and Repair](https://help.steampowered.com/en/faqs/view/65B4-2AA3-5F37-4227) — the authoritative guide, and it may be newer than this quest
- [SteamOS issue tracker](https://github.com/ValveSoftware/SteamOS) — compatibility reports and bugs
- [ProtonDB](https://www.protondb.com/) — community compatibility reports
- [Proton](https://github.com/ValveSoftware/Proton) — source code and release notes
- [Bazzite](https://bazzite.gg/) — a community alternative if your GPU is not supported

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Twin Rigs]] **Level hub:** [[Level 0111 (7) - API Development]] **Previous:** [[The Great Forge: Assemble a Desktop from Bare Parts]] **Next:** [[The Free Stalls: Stock SteamOS with Open Source Games]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
