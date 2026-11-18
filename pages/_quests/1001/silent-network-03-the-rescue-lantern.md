---
title: "The Rescue Lantern: Read the Logs of a System That Won't Talk"
description: 'The broken install has no network, so you cannot reach it. Boot a rescue system with your SSH key, mount the install read-only, and read its journal offline: every boot, every service, every error, without starting it.'
excerpt: 'When a system cannot reach you, go to its disk instead. Mount it read-only and read its journal from a rescue system over SSH.'
date: '2026-11-13T00:00:00.000Z'
lastmod: '2026-11-13T00:00:00.000Z'
level: '1001'
difficulty: 🔴 Hard
estimated_time: 2-3 hours
primary_technology: linux
quest_type: main_quest
quest_series: The Silent Network
quest_line: The Silent Network
quest_arc: The Rescue Lantern
skill_focus: infrastructure
learning_style: hands-on
author: IT-Journey Team
permalink: /quests/1001/silent-network-03-the-rescue-lantern/
fmContentType: quest
layout: quest
draft: false
comments: true
mermaid: true
categories:
- Quests
- Linux
- Troubleshooting
- Systemd
tags:
- '1001'
- journalctl
- ssh
- rescue-system
- ext4
- main_quest
- hands-on
- gamified-learning
keywords:
  primary:
  - '1001'
  - offline-journal
  - rescue-system
  - ssh-keys
  secondary:
  - journalctl
  - dumpe2fs
  - e2fsck
  - steamos
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Has completed Chapter II, The Deaf Gatekeeper
  - Comfortable with SSH keys and sudo
  system_requirements:
  - A rescue system for the PC — a live USB, a netbooted live system, or Valve's recovery stick
  - An SSH key pair on your fortress
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/1000/silent-network-02-the-deaf-gatekeeper/
  - /quests/0000/linux-fundamentals/
  unlocks_quests:
  - /quests/1010/silent-network-04-the-silencing-script/
rewards:
  badges:
  - 🏮 Lantern Bearer — read the logs of a system that could not speak for itself
  skills_unlocked:
  - 🔑 Key-only SSH into a rescue system
  - 📜 Offline journal reading with journalctl -D
  - 🧪 Read-only filesystem forensics
  progression_points: 100
validation_criteria:
  completion_requirements:
  - The boot list and network log lines of an installed system, read while it was not running
  skill_demonstrations:
  - Can mount a partition read-only and read its journal with journalctl -D
  knowledge_checks:
  - Explains why mounting read-only matters for evidence
environment:
  os:
  - linux
  - macos
  shell:
  - bash
  - zsh
  pkg:
  - apt
  - brew
---
*A hero who won't speak can still be read. Their journal sits in their pack, written in their own hand, every hour of every day. You can't wake them, but you can light a lantern beside them, open the pack carefully, and read without changing a word. The installed SteamOS couldn't reach the network, so it couldn't reach you. Its journal, though, was sitting on its disk.*

## 🎯 Quest Objectives

By the end of this chapter you will:

- [ ] **Boot a rescue system you can SSH into** with keys only
- [ ] **Mount an installed system's partitions read-only** without disturbing them
- [ ] **Read its journal offline** with `journalctl -D`: boots, units, and errors
- [ ] **Use filesystem metadata as a clock** for boots the journal didn't catch
- [ ] **Check for other writers** before trusting what a disk says

## 🗺️ Quest Prerequisites

- **[Chapter II](/quests/1000/silent-network-02-the-deaf-gatekeeper/)** — a network boot server that listens
- **A rescue system:** any live Linux works; this campaign used a netbooted Debian live system and Valve's recovery stick
- **Your SSH public key** (`~/.ssh/id_ed25519.pub`)

## 🌍 Choose Your Adventure Platform

### 🍎 macOS

```bash
# Make a key once, if you don't have one.
ssh-keygen -t ed25519 -C "rescue-key"
cat ~/.ssh/id_ed25519.pub
```

### 🐧 Linux

```bash
ssh-keygen -t ed25519 -C "rescue-key"
cat ~/.ssh/id_ed25519.pub
```

### 🪟 Windows

```powershell
ssh-keygen -t ed25519 -C "rescue-key"
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

## 🧙‍♂️ Chapter 1: Light the Lantern — A Rescue System You Can Reach

### ⚔️ Skills You'll Forge

- Enabling key-only SSH on a live system
- Granting temporary, reversible admin rights

Photographs of a screen are slow evidence. A shell is fast evidence. Whatever rescue system you boot, turn it into one you can reach:

```bash
# On the rescue system (once). The live password is often public, so refuse passwords.
mkdir -p ~/.ssh && chmod 700 ~/.ssh
curl -fs http://<your-fortress>:8780/ssh/authorized_keys >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
echo "PasswordAuthentication no" | sudo tee /etc/ssh/sshd_config.d/10-keys-only.conf
sudo systemctl enable --now sshd    # SteamOS calls it sshd; Debian calls it ssh
```

The service name tripped us once: `ssh.service does not exist` on SteamOS, where the unit is `sshd`. A one-letter typo did too (`authroized_keys`), and the server's log showed exactly that 404.

On Valve's recovery stick we also needed root without typing a password over SSH. That's a real security trade-off, so scope it: only on the throwaway rescue system, and remove it afterwards.

```bash
echo "deck ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/90-remote-admin
# when you're done:
sudo rm /etc/sudoers.d/90-remote-admin
```

### 🔍 Knowledge Check

- [ ] Why turn off password logins on a live system?
- [ ] Why is the `NOPASSWD` rule acceptable on the rescue stick but not on the installed system?

## 🧙‍♂️ Chapter 2: Open the Pack Without Changing It

### ⚔️ Skills You'll Forge

- Mapping an unfamiliar partition layout
- Read-only mounts for evidence

SteamOS spreads itself over eight partitions. The journal lives on `home`, under an "offload" directory that's bind-mounted to `/var/log` at runtime.

```bash
lsblk -o NAME,SIZE,PARTLABEL,FSTYPE /dev/nvme0n1
sudo mkdir -p /mnt/home /mnt/var
sudo mount -o ro /dev/disk/by-partlabel/home  /mnt/home
sudo mount -o ro /dev/disk/by-partlabel/var-B /mnt/var    # the slot that ran last
ls /mnt/home/.steamos/offload/var/log/journal/
```

Mount **read-only**. You're collecting evidence, and a read-write mount can replay a filesystem journal, update timestamps, and change the very thing you came to read.

### 🔍 Knowledge Check

- [ ] Where does SteamOS keep `/var/log` on disk?
- [ ] What can a read-write mount change on a filesystem you only meant to read?

## 🧙‍♂️ Chapter 3: Read the Journal Offline

### ⚔️ Skills You'll Forge

- `journalctl -D` against a foreign journal
- Narrowing a boot to the lines that matter

`journalctl` reads any journal directory you point it at. List the boots, then follow the network through the latest one:

```bash
J=$(ls -d /mnt/home/.steamos/offload/var/log/journal/*/ | head -1)
sudo journalctl -D "$J" --list-boots --no-pager | tail -4
sudo journalctl -D "$J" -b 0 --no-pager \
  | grep -E "eno1|dhcp4|NetworkManager.*(state|SIGTERM|exiting)|Stopping Network"
```

This is where the hunt turned. From the installed system's own words:

```text
21:13:17 kernel: r8169 0000:0d:00.0 eno1: Link is Up - 2.5Gbps/Full
21:13:17 NetworkManager: dhcp4 (eno1): activation: beginning transaction
21:13:20 systemd[1]: Stopping Network Manager...
21:13:20 NetworkManager: caught SIGTERM, shutting down normally.
21:13:20 NetworkManager: dhcp4 (eno1): canceled DHCP transaction
21:13:20 NetworkManager: exiting (success)
```

The driver worked. The cable worked. The link came up at 2.5 Gb/s and DHCP began. Three seconds later, **something stopped NetworkManager** and nothing started it again. Every earlier theory about cables, ports, and drivers died right here. Chapter IV finds the something.

### 🔍 Knowledge Check

- [ ] Which line rules out a driver problem? Which rules out a cable problem?
- [ ] Why does `systemd[1]: Stopping` mean someone *asked* for the stop?

## 🧙‍♂️ Chapter 4: When the Pages Don't Agree

### ⚔️ Skills You'll Forge

- Using filesystem metadata as a second clock
- Checking for concurrent writers

Two surprises came later. First, a boot was missing from the journal list, though we knew the PC had booted. The filesystem kept its own record:

```bash
sudo dumpe2fs -h /dev/disk/by-partlabel/var-B | grep -E "Last (mount|write) time"
ls -la --time-style=full-iso /mnt/home/.steamos/offload/var/log/journal/
```

The mount time showed the boot, and a **second machine-ID folder** in the journal directory held its log. A fresh first-boot system can generate a new machine ID, and `head -1` had picked the old folder.

Second, a minute later the same disk read as garbage: `Bad magic number in super-block`, and zeros where filesystems had been. It looked like a dying drive. It was a person: at the PC, Valve's **Wipe Device & Install** had just started.

```bash
ps -eo pid,etime,args | grep -E "repair|dd |mkfs|sfdisk" | grep -v grep
journalctl -b --no-pager | grep -iE "repair_device|sudo"
```

```text
3279  00:24 sudo /home/deck/tools/repair_device.sh all
3544  00:12 dd if=/dev/sdc3 of=/dev/nvme0n1p4 bs=128M status=progress oflag=sync
```

Before you call a disk corrupt, check who else is writing to it.

### 🔍 Knowledge Check

- [ ] Why might a journal directory hold two machine-ID folders?
- [ ] What two commands would you run before concluding a disk is failing?

## 🎮 Implementation Challenge

**Objective:** Read an installed Linux system's last boot from a rescue system, without booting it.

```bash
#!/usr/bin/env bash
# lantern.sh <home-partition> — summarize the last boot of an offline system.
set -euo pipefail
mnt=$(mktemp -d)
sudo mount -o ro "$1" "$mnt"
trap 'sudo umount "$mnt"; rmdir "$mnt"' EXIT
for J in $(sudo find "$mnt" -maxdepth 6 -type d -path "*/log/journal/*" -name "????????????????????????????????"); do
  echo "== $J"
  sudo journalctl -D "$J" --list-boots --no-pager | tail -2
  sudo journalctl -D "$J" -b 0 -p warning --no-pager | tail -15
done
```

**Success Criteria:**

- [ ] Run it over SSH from your fortress against a real system's disk
- [ ] Show the last boot's network lines (link, DHCP, NetworkManager state)
- [ ] Show the partition stayed unmodified (`dumpe2fs` mount count unchanged)

## 🔍 Quest Network

```mermaid
graph LR
    C2[II The Deaf Gatekeeper] --> C3[🏮 III The Rescue Lantern]
    C3 --> C4[IV The Silencing Script]
```

## 🎁 Rewards & Progression

- 🏮 **Lantern Bearer** — read the logs of a system that could not speak for itself
- ⚡ **Skills unlocked:** key-only rescue access, offline journals, read-only forensics
- 🏆 **100 XP** toward the campaign

## 🔮 Next Adventures

You know *what* happened: NetworkManager was stopped three seconds after it started. Next, find *who* stopped it, and why it never came back.

- ➡️ **Next chapter:** [Chapter IV — The Silencing Script](/quests/1010/silent-network-04-the-silencing-script/)
- ⬅️ **Previous chapter:** [Chapter II — The Deaf Gatekeeper](/quests/1000/silent-network-02-the-deaf-gatekeeper/)
- 👑 **Campaign hub:** [Epic Quest: The Silent Network](/quests/codex/silent-network/)

## 📚 Resource Codex

- [journalctl(1)](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html) — `-D`, `--list-boots`, `-b`, `-u`
- [dumpe2fs(8)](https://man7.org/linux/man-pages/man8/dumpe2fs.8.html) and [e2fsck(8)](https://man7.org/linux/man-pages/man8/e2fsck.8.html) — ext4 metadata, and `-n` for a read-only check
- [sshd_config(5)](https://man7.org/linux/man-pages/man5/sshd_config.5.html) — `PasswordAuthentication`, `AllowUsers`, `AuthorizedKeysFile`

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Silent Network]] **Level hub:** [[Level 1001 (9) - Kubernetes Orchestration]] **Previous:** [[The Deaf Gatekeeper: When Your Own Server Stops Listening]] **Next:** [[The Silencing Script: Find What Stops the Network]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
