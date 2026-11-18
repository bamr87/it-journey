---
title: 'The Molten Core: Match Drivers to Kernels'
description: 'A driver can exist upstream and still be missing on your machine. Identify every network chip, find which kernel first carried its driver, prove it on a newer live system, and reach that kernel through the update channel instead of fighting a read-only OS.'
excerpt: 'The Wi-Fi driver exists, just not in your kernel. Read PCI IDs, driver aliases, and release notes, prove it on a newer kernel, then update the right way.'
date: '2026-11-13T00:00:00.000Z'
lastmod: '2026-11-13T00:00:00.000Z'
level: '1010'
difficulty: 🔴 Hard
estimated_time: 2-3 hours
primary_technology: linux
quest_type: main_quest
quest_series: The Silent Network
quest_line: The Silent Network
quest_arc: The Molten Core
skill_focus: infrastructure
learning_style: hands-on
author: IT-Journey Team
permalink: /quests/1010/silent-network-05-the-molten-core/
fmContentType: quest
layout: quest
draft: false
comments: true
mermaid: true
categories:
- Quests
- Linux
- Kernel
- SteamOS
- Hardware
tags:
- '1010'
- linux-kernel
- drivers
- wifi
- steamos
- main_quest
- hands-on
- gamified-learning
keywords:
  primary:
  - '1010'
  - kernel-drivers
  - pci-ids
  - update-channels
  secondary:
  - lspci
  - modinfo
  - linux-firmware
  - dkms
  - mt7927
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Has completed Chapter IV, The Silencing Script
  - Knows what a kernel module is
  system_requirements:
  - The PC from this campaign, or any Linux PC with a recent network chip
  - A newer live system to test with (optional but recommended)
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/1010/silent-network-04-the-silencing-script/
  unlocks_quests: []
rewards:
  badges:
  - 🌋 Core Diver — matched every chip on the board to the kernel that drives it
  skills_unlocked:
  - 🔬 PCI ID and driver alias forensics
  - 📅 Reading kernel driver timelines
  - 🧭 Choosing update channels over hacks on an immutable OS
  progression_points: 100
validation_criteria:
  completion_requirements:
  - A table of every network chip, its driver, and the first kernel that supports it
  - Wi-Fi verified with a driver bound and networks visible
  skill_demonstrations:
  - Can show whether a module claims a PCI ID with modinfo
  knowledge_checks:
  - Explains why building a DKMS driver on SteamOS is a trap
environment:
  os:
  - linux
  shell:
  - bash
  pkg:
  - pacman
  - apt
---
*Deep under every realm burns the Molten Core, where the laws of the hardware are written. A new kind of creature had arrived on this board, a Wi-Fi 7 radio, and the Core's lawbook had no page for it. The law existed; it had been written that summer. It simply hadn't reached this world's copy yet. No amount of shouting at the surface would add the page. You go to the Core, or you wait for the new edition.*

## 🎯 Quest Objectives

By the end of this chapter you will:

- [ ] **Identify every network chip** by PCI vendor and device ID
- [ ] **Prove whether a kernel module claims a device** with `modinfo`
- [ ] **Find the first kernel version that drives a chip**, and the firmware it needs
- [ ] **Test a newer kernel without installing it**, from a live system
- [ ] **Move an immutable OS to a newer kernel** the supported way, and verify the result

## 🗺️ Quest Prerequisites

- **[Chapter IV](/quests/1010/silent-network-04-the-silencing-script/)** — wired networking survives first boot
- **A terminal on the PC** (Desktop Mode → Konsole) or SSH from your fortress

## 🌍 Choose Your Adventure Platform

### 🐧 Linux (on the PC)

```bash
lspci -nnk | grep -iA3 -E "ethernet|network"
uname -r
```

### 🍎 macOS (from your fortress)

```bash
ssh deck@<pc-address> 'lspci -nnk | grep -iA3 -E "ethernet|network"; uname -r'
```

### 🪟 Windows (from your fortress)

```powershell
ssh deck@<pc-address> "lspci -nnk | grep -iA3 -E 'ethernet|network'; uname -r"
```

## 🧙‍♂️ Chapter 1: Name Every Creature on the Board

### ⚔️ Skills You'll Forge

- Reading `lspci -nnk`
- Separating "device present" from "driver bound"

On SteamOS 3.8.14 (kernel 6.16.12), the board reported:

```text
09:00.0 Network controller [0280]: MEDIATEK Corp. Device [14c3:7927]
0d:00.0 Ethernet controller [0200]: Realtek … RTL8126 5GbE Controller [10ec:8126]
        Kernel driver in use: r8169
0e:00.0 Ethernet controller [0200]: Realtek … Device [10ec:8127]
        Kernel driver in use: r8169
```

Three chips, three stories. Both Realtek ports have `Kernel driver in use: r8169`. The MediaTek radio has **no driver line at all**. Linux sees it on the bus and has no idea how to talk to it. No driver means no `wlan0` and no `phy0`, which is exactly what tripped Chapter IV's script.

The kernel log adds detail even for working chips:

```text
r8169 0000:0e:00.0: Unable to load firmware rtl_nic/rtl8127a-1.fw (-2)
```

The RTL8127 works without that optional firmware patch, but a newer firmware package would supply it.

### 🔍 Knowledge Check

- [ ] Which line tells you a driver is bound, and which line tells you none is?
- [ ] What's the vendor:device ID of the Wi-Fi chip?

## 🧙‍♂️ Chapter 2: Does Any Module Claim It?

### ⚔️ Skills You'll Forge

- Reading module aliases
- Knowing which driver *family* a new chip belongs to

Each module declares the PCI IDs it handles. The MT7927 belongs to the `mt7925e` family:

```bash
modinfo mt7925e | grep -iE "^(alias|firmware)"
modinfo mt7925e | grep -i 7927 || echo "no module in this kernel claims 14c3:7927"
```

On kernel 6.16 the module exists, but it has no alias for `7927`. The chip is close kin to the MT7925, yet it needs a different DMA ring layout, interrupt mapping, and power handling. The support patches went through review on the `linux-wireless` list in spring 2026 and landed in **mainline Linux 7.2**, with firmware files merged into `linux-firmware` under `mediatek/mt7927/`.

| Chip | Driver | First kernel | Kernel 6.16 (SteamOS 3.8) | Kernel 7.2 (SteamOS 3.9) |
|---|---|---|---|---|
| RTL8126 5 GbE | `r8169` | 6.9 | ✅ | ✅ |
| RTL8127 10 GbE | `r8169` | 6.16 | ✅ | ✅ |
| MT7927 Wi-Fi 7 | `mt7925e` | 7.2 | ❌ | ✅ |

### 🔍 Knowledge Check

- [ ] Why can a module exist on your system and still not claim your chip?
- [ ] Where would you look to learn which kernel first supports a device?

## 🧙‍♂️ Chapter 3: Test the Future Without Installing It

### ⚔️ Skills You'll Forge

- Proving a hypothesis on a live system

"Kernel 7.2 drives it" was a claim from release notes. We proved it on the same PC by network-booting a Debian live system with a backports **7.2** kernel and newer firmware:

```bash
uname -r
ip -br link | grep -v ^lo
lspci -k -s 09:00.0 | tail -2
```

```text
7.2.12+deb13-amd64
eno1     UP    b0:82:…
wlp9s0   DOWN  06:d0:…
        Kernel driver in use: mt7925e
        Kernel modules: mt7925e
```

`wlp9s0` exists, and the `mt7925e` module drives it. Nothing was installed on the PC's drive to learn this. A live system is the cheapest experiment in the realm.

### 🔍 Knowledge Check

- [ ] Why test on a live system instead of building the driver on the installed OS?

## 🧙‍♂️ Chapter 4: Don't Forge Your Own Core on an Immutable OS

### ⚔️ Skills You'll Forge

- Recognizing when a "fix" fights the platform

The tempting route is an out-of-tree driver. A DKMS package exists for the MT7927, and SteamOS is based on Arch. On SteamOS 3.8 it's still a trap:

- The package supports **kernel 6.17 or newer**; SteamOS 3.8 runs 6.16
- The root filesystem is **read-only**; you'd unlock it with `steamos-readonly disable`
- Every OS update writes a **fresh image** into the other A/B slot (Chapter I) and discards your module, headers, and packages

Work that the next update erases isn't a fix. The platform's way forward is its update channel.

### 🔍 Knowledge Check

- [ ] List two reasons a DKMS driver on SteamOS 3.8 would fail or not last.

## 🧙‍♂️ Chapter 5: Reach the New Edition

### ⚔️ Skills You'll Forge

- Choosing an update channel
- Verifying a driver after an update

SteamOS ships the same OS on three channels: **Stable**, **Beta**, and **Preview**. The 3.9 series moved to Linux 7.2: it appeared in Preview at the end of August 2026, then in Beta, and was reported in Stable from 3.9.5 in late October. On the night of this campaign, the Beta channel offered **3.9.6** (build 20261112.101).

With Ethernet working (thanks to Chapter IV), set the channel and update, either in **Settings → System → Update Channel**, or in Desktop Mode:

```bash
steamos-select-branch -c                      # current channel
sudo steamos-select-branch beta               # or: stable, preview
sudo steamos-update                           # downloads into the other A/B slot
```

Reboot into the new slot, then verify, don't assume:

```bash
grep -E "^(VERSION_ID|BUILD_ID)=" /etc/os-release
uname -r                                       # expect 7.2.x
lspci -k -s 09:00.0 | grep "driver in use"     # expect mt7925e
nmcli device wifi list | head                  # expect your networks
```

Once Wi-Fi has a driver, the Wi-Fi helper from Chapter IV finds its radio, and the guard unit becomes unnecessary. Remove it and confirm first-time setup works from a clean state.

### 🔍 Knowledge Check

- [ ] Which channel would you pick for a machine you rely on, and why?
- [ ] Which four commands prove the update fixed Wi-Fi?

## 🎮 Implementation Challenge

**Objective:** Produce the driver table for your own machine, and close the campaign.

```bash
#!/usr/bin/env bash
# core-map.sh — every network chip, its ID, and its bound driver.
lspci -Dnn | grep -iE "ethernet|network" | while read -r slot rest; do
  id=$(lspci -n -s "$slot" | awk '{print $3}')
  drv=$(lspci -k -s "$slot" | sed -n 's/.*driver in use: //p')
  echo "$slot  $id  ${drv:-NO DRIVER}  ${rest#*: }"
done
echo "kernel: $(uname -r)"
```

**Success Criteria:**

- [ ] Your table names every network chip, its driver, and the first kernel that supports it
- [ ] A chip without a driver is proven to work on a newer kernel from a live system
- [ ] After the update, the four verification commands show Wi-Fi working
- [ ] Your field report (the Boss Gate on the [campaign hub](/quests/codex/silent-network/)) is complete

## 🔍 Quest Network

```mermaid
graph LR
    C4[IV The Silencing Script] --> C5[🌋 V The Molten Core]
    C5 --> Hub[👑 The Silent Network Boss Gate]
```

## 🎁 Rewards & Progression

- 🌋 **Core Diver** — matched every chip on the board to the kernel that drives it
- ⚡ **Skills unlocked:** PCI ID forensics, driver alias checks, kernel timelines, update channels
- 🏆 **100 XP** toward the campaign

## 🔮 Next Adventures

- 👑 **Return to the hub** and pass the Boss Gate: [Epic Quest: The Silent Network](/quests/codex/silent-network/)
- ⬅️ **Previous chapter:** [Chapter IV — The Silencing Script](/quests/1010/silent-network-04-the-silencing-script/)
- 🕹️ **Put the rig to work:** [The Free Stalls](/quests/1000/twin-rigs-07-the-free-stalls/)

## 📚 Resource Codex

- [The PCI ID repository](https://pci-ids.ucw.cz/) — vendor and device names behind `lspci -nn`
- [mediatek-mt7927-dkms](https://github.com/jetm/mediatek-mt7927-dkms) — the out-of-tree driver and its upstream tracking notes
- [MT7927 support series on LWN](https://lwn.net/Articles/1069678/) — the patches that brought the chip to `mt7925e`
- [SteamOS 3.9 Preview moves to Linux 7.2 (Phoronix)](https://phoronix.com/news/SteamOS-3.9-Preview) — the kernel change for this chapter
- [linux-firmware](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/) — where `mediatek/` and `rtl_nic/` firmware lives

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Silent Network]] **Level hub:** [[Level 1010 - Automation & Testing]] **Previous:** [[The Silencing Script: Find What Stops the Network]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
