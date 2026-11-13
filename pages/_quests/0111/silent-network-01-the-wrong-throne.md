---
title: 'The Wrong Throne: Prove Which System Booted'
description: 'Before you fix a machine, prove which system it is running. Read the root device, the A/B slot, and the firmware boot entry, and learn why an update fails on a recovery stick but works on the installed drive.'
excerpt: 'Four reboots, all from the wrong disk. Learn the three commands that end the argument about which system is running.'
date: '2026-11-13T00:00:00.000Z'
lastmod: '2026-11-13T00:00:00.000Z'
level: '0111'
difficulty: 🟡 Medium
estimated_time: 1-2 hours
primary_technology: steamos
quest_type: main_quest
quest_series: The Silent Network
quest_line: The Silent Network
quest_arc: The Wrong Throne
skill_focus: infrastructure
learning_style: hands-on
author: IT-Journey Team
permalink: /quests/0111/silent-network-01-the-wrong-throne/
fmContentType: quest
layout: quest
draft: false
comments: true
mermaid: true
categories:
- Quests
- Linux
- SteamOS
- Troubleshooting
tags:
- '0111'
- steamos
- uefi
- efibootmgr
- ab-updates
- main_quest
- hands-on
- gamified-learning
keywords:
  primary:
  - '0111'
  - uefi-boot-entries
  - ab-partitions
  secondary:
  - findmnt
  - efibootmgr
  - rauc
  - steamos
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Has read the campaign hub, The Silent Network
  - Knows what a partition and a mount point are
  system_requirements:
  - A PC with SteamOS installed, or any Linux system with UEFI
  - Valve's recovery stick, or any second bootable drive
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/codex/silent-network/
  - /quests/0111/twin-rigs-06-the-steam-rite/
  unlocks_quests:
  - /quests/1000/silent-network-02-the-deaf-gatekeeper/
rewards:
  badges:
  - 🧭 Throne Finder — proved which system was running before touching it
  skills_unlocked:
  - 🔎 Root device and boot entry forensics
  - 🪞 A/B system slots and why updates need them
  progression_points: 60
validation_criteria:
  completion_requirements:
  - A short note naming the running disk, slot, and boot entry, with the commands that showed them
  skill_demonstrations:
  - Can boot a specific entry once with efibootmgr --bootnext
  knowledge_checks:
  - Explains why an update failed on the recovery stick
environment:
  os:
  - linux
  - macos
  shell:
  - bash
  - zsh
  pkg:
  - brew
---
*A kingdom with two thrones is easy to rule badly. You issue decrees all night, and in the morning learn they went to the other throne room, where nobody was sitting. On this PC there were two SteamOS systems: Valve's recovery stick, and the real install on the NVMe drive. They look the same on screen. For four reboots, every command went to the stick.*

## 🎯 Quest Objectives

By the end of this chapter you will:

- [ ] **Name the disk your root filesystem lives on** with one command
- [ ] **Read the firmware's boot record** and say which entry started this boot
- [ ] **Explain A/B system slots** and why an update needs an empty one
- [ ] **Boot a chosen entry exactly once** without changing the boot order
- [ ] **Recognize host-key changes over SSH** as a sign you reached a different system

## 🗺️ Quest Prerequisites

- **[The campaign hub](/quests/codex/silent-network/)** — the story so far
- **A UEFI PC** with SteamOS on its NVMe drive and Valve's recovery stick (any Linux with two boot drives works too)
- **A terminal on that PC:** Desktop Mode → Konsole on SteamOS

## 🌍 Choose Your Adventure Platform

The commands run on the PC itself. From your fortress you only need SSH, which Chapter III sets up properly.

### 🍎 macOS

```bash
# Later chapters connect from here; check the client now.
ssh -V
```

### 🐧 Linux

```bash
# The same commands from this chapter work on any UEFI Linux.
findmnt -no SOURCE /
```

### 🪟 Windows

```powershell
# Windows 10 and 11 ship an OpenSSH client.
ssh -V
```

## 🧙‍♂️ Chapter 1: Which Disk Is the Root?

### ⚔️ Skills You'll Forge

- Finding the block device behind `/`
- Reading partition labels

The screen can't tell you where the operating system lives. The kernel can.

```bash
findmnt -no SOURCE /
lsblk -o NAME,SIZE,PARTLABEL,MOUNTPOINTS
```

On the night this campaign comes from, the answer was:

```text
/dev/sdc3
sdc        29.8G
|-sdc1       64M esp
|-sdc2      128M efi-A
|-sdc3        5G rootfs-A    /
nvme0n1     1.8T
|-nvme0n1p4   5G rootfs-A
|-nvme0n1p5   5G rootfs-B
`-nvme0n1p8 1.8T home
```

`sdc` is the SD card in a USB reader. The 2 TB NVMe drive had a complete install, but none of its partitions were mounted. Everything typed that evening had gone to the card.

### 🔍 Knowledge Check

- [ ] Which command tells you the root device in one line?
- [ ] On the listing above, which partitions belong to the installed system?

## 🧙‍♂️ Chapter 2: Which Door Did the Firmware Open?

### ⚔️ Skills You'll Forge

- Reading UEFI boot entries with `efibootmgr`
- Matching a boot entry to a partition by its PARTUUID

UEFI firmware keeps a numbered list of boot entries and records which one it used. Linux can read both.

```bash
efibootmgr | head -4
cat /proc/cmdline | tr ' ' '\n' | grep -i partuuid
lsblk -o NAME,PARTUUID,PARTLABEL
```

```text
BootCurrent: 0005
BootOrder: 0000,0007,0001,0002,0003,0004,0005,0006
Boot0000* SteamOS   HD(1,GPT,a2e7339d-…)/\EFI\steamos\steamcl.efi
Boot0005* UEFI: Generic MassStorageClass1539, Partition 1
steamos.efi=PARTUUID=c1c7e615-f0a6-4f7d-988e-c2f06afed580
```

`BootCurrent: 0005` is the USB card reader, even though `Boot0000` (the NVMe) is first in `BootOrder`. Firmware boot menus (often **F8** on ASUS boards) and "boot override" options pick an entry for one boot without changing the order, so it is easy to choose the stick by accident. The kernel line agrees: that PARTUUID belongs to the card's `efi-A`.

To boot a chosen entry once, ask the firmware directly:

```bash
sudo efibootmgr --bootnext 0000   # next boot only: the NVMe's SteamOS entry
sudo reboot
```

The simplest proof of all is physical: **pull the stick out**.

### 🔍 Knowledge Check

- [ ] What is the difference between `BootCurrent` and `BootOrder`?
- [ ] How do you confirm a boot entry points at the disk you think it does?

## 🧙‍♂️ Chapter 3: Twin Thrones — A/B Slots

### ⚔️ Skills You'll Forge

- Understanding image-based A/B updates
- Reading an update error as evidence

SteamOS doesn't update file by file. It writes a whole new system image into the **other** slot (rootfs-A ↔ rootfs-B), then switches to it at the next boot. If the new one fails, the old slot is still intact. That's why the installed drive has paired partitions: `efi-A/B`, `rootfs-A/B`, `var-A/B`.

Valve's recovery stick only needs one system, so it has only the A set. Running the update there produced this, with the update channel set to Beta:

```text
rauc: installing https://steamdeck-images.steamos.cloud/steamdeck/20261112.101/steamdeck-20261112.101-3.9.6.raucb
rauc: Installation error: Destination device '/dev/disk/by-partsets/B/rootfs' for slot 'rootfs.1' not found
```

That error looks like a broken updater. It was really a precise statement: *you're on a system with no B slot*. Read errors literally before reading them as bad luck.

```bash
# Where would the next update go? On the installed drive, the slot you're NOT on.
findmnt -no SOURCE /          # /dev/nvme0n1p5 → running B, so updates write A
journalctl -b -u rauc --no-pager | tail -20
```

### 🔍 Knowledge Check

- [ ] Why does the recovery stick have no B slot?
- [ ] If you're running `rootfs-B`, where does the next update land?

## 🧙‍♂️ Chapter 4: The Host Key Is a Witness

### ⚔️ Skills You'll Forge

- Reading SSH host-key warnings as evidence

Each installed system generates its own SSH host key. If the same address suddenly presents a different key, you're talking to a different system, or a reinstalled one. In this campaign, that warning appeared every time the PC switched between the stick and the drive. It's a free, independent witness to which throne is occupied.

```bash
ssh-keygen -F 192.168.1.50 -l        # the key you trusted before
ssh-keyscan -t ed25519 192.168.1.50 | ssh-keygen -lf -   # the key it shows now
```

Only remove an old key (`ssh-keygen -R <address>`) once you know *why* it changed.

### 🔍 Knowledge Check

- [ ] Name two reasons a host key can change at the same address.

## 🎮 Implementation Challenge

**Objective:** Write a five-line "throne report" that proves where you are.

```bash
#!/usr/bin/env bash
# throne.sh — which system, slot, and boot entry are running?
echo "root:  $(findmnt -no SOURCE /)"
echo "disk:  $(lsblk -no PKNAME "$(findmnt -no SOURCE /)")"
echo "boot:  $(efibootmgr | sed -n 's/^BootCurrent: //p')"
echo "os:    $(. /etc/os-release; echo "$NAME $VERSION_ID $BUILD_ID")"
echo "kernel: $(uname -r)"
```

**Success Criteria:**

- [ ] Run it from the stick and from the installed drive; the outputs differ in root, disk, and boot entry
- [ ] Use `efibootmgr --bootnext` to boot the installed drive once, and show it in the report
- [ ] Keep both outputs in your field report

## 🔍 Quest Network

```mermaid
graph LR
    Hub[👑 The Silent Network] --> C1[🧭 I The Wrong Throne]
    C1 --> C2[II The Deaf Gatekeeper]
```

## 🎁 Rewards & Progression

- 🧭 **Throne Finder** — proved which system was running before touching it
- ⚡ **Skills unlocked:** root device forensics, UEFI boot entries, A/B update slots
- 🏆 **60 XP** toward the campaign

## 🔮 Next Adventures

Knowing which system is running was step one. Next, the PC seemed to lose its network entirely, and the culprit was on the other side of the cable.

- ➡️ **Next chapter:** [Chapter II — The Deaf Gatekeeper](/quests/1000/silent-network-02-the-deaf-gatekeeper/)
- 👑 **Campaign hub:** [Epic Quest: The Silent Network](/quests/codex/silent-network/)

## 📚 Resource Codex

- [efibootmgr](https://github.com/rhboot/efibootmgr) — read and change UEFI boot entries
- [findmnt(8)](https://man7.org/linux/man-pages/man8/findmnt.8.html) — mount and root device lookups
- [RAUC](https://rauc.io/) — the A/B update framework SteamOS uses
- [SteamOS Installation and Repair](https://help.steampowered.com/en/faqs/view/65B4-2AA3-5F37-4227) — recovery stick, repair, and re-image

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Silent Network]] **Level hub:** [[Level 0111 (7) - API Development]] **Next:** [[The Deaf Gatekeeper: When Your Own Server Stops Listening]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
