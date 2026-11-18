---
title: 'The Silencing Script: Find What Stops the Network'
description: 'Trace a stopped NetworkManager to a D-Bus call and a helper script that fails halfway under set -e. Fix the installed system before its first boot through its /etc overlay, prove it with a log line, and take the evidence upstream.'
excerpt: 'A Wi-Fi helper stops NetworkManager, fails on a PC whose Wi-Fi has no driver, and never restarts it. Find the line, fix it before first boot, and tell Valve.'
date: '2026-11-13T00:00:00.000Z'
lastmod: '2026-11-13T00:00:00.000Z'
level: '1010'
difficulty: 🔴 Hard
estimated_time: 2-3 hours
primary_technology: systemd
quest_type: main_quest
quest_series: The Silent Network
quest_line: The Silent Network
quest_arc: The Silencing Script
skill_focus: infrastructure
learning_style: hands-on
author: IT-Journey Team
permalink: /quests/1010/silent-network-04-the-silencing-script/
fmContentType: quest
layout: quest
draft: false
comments: true
mermaid: true
categories:
- Quests
- Linux
- Systemd
- SteamOS
- Troubleshooting
tags:
- '1010'
- networkmanager
- systemd
- bash
- overlayfs
- steamos
- main_quest
- hands-on
- gamified-learning
keywords:
  primary:
  - '1010'
  - root-cause-analysis
  - networkmanager
  - systemd-units
  secondary:
  - set-e
  - overlayfs
  - d-bus
  - bug-reports
  - steamos
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Has completed Chapter III, The Rescue Lantern
  - Can read a Bash script, including set -euo pipefail
  - Knows what a systemd unit is
  system_requirements:
  - The rescue system from Chapter III, with root
  - A SteamOS install that has not completed first-time setup
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/1001/silent-network-03-the-rescue-lantern/
  unlocks_quests:
  - /quests/1010/silent-network-05-the-molten-core/
rewards:
  badges:
  - 🗝️ Script Breaker — found the exact line that silenced the network
  - 📜 Petition Bearer — took evidence upstream, not just a complaint
  skills_unlocked:
  - 🧩 Tracing a failure across systemd, D-Bus, and shell scripts
  - 🛡️ Pre-boot fixes through an /etc overlay
  - 🐛 Upstream bug etiquette
  progression_points: 120
validation_criteria:
  completion_requirements:
  - A guard unit installed before first boot, and the journal line proving it acted
  skill_demonstrations:
  - Can explain why the helper never restarted NetworkManager
  knowledge_checks:
  - Explains why changing the backend setting did not help
environment:
  os:
  - linux
  shell:
  - bash
  pkg:
  - pacman
---
*The silence had an author. It was not malice; it was a careful spell written for a different kind of machine. On every handheld it was written for, the spell stops the network, re-creates the Wi-Fi interface, and starts the network again. On this PC, the middle step failed, and the spell stopped right there, with the network still in its hands.*

## 🎯 Quest Objectives

By the end of this chapter you will:

- [ ] **Find who asked systemd to stop a service** from the journal
- [ ] **Trace a D-Bus method to the script it runs** and read that script's failure
- [ ] **Explain how `set -e` turned one failed command into a dead network**
- [ ] **Fix an installed system before its first boot** through its `/etc` overlay
- [ ] **Prove a fix with a log line**, not with a screen
- [ ] **Find the existing upstream bug and add evidence** that maintainers can use

## 🗺️ Quest Prerequisites

- **[Chapter III](/quests/1001/silent-network-03-the-rescue-lantern/)** — the journal line *Stopping Network Manager* three seconds after the link came up
- **Root on a rescue system** with the install's partitions available

## 🌍 Choose Your Adventure Platform

Everything in this chapter runs on the PC's rescue system, over SSH from your fortress.

### 🍎 macOS

```bash
ssh deck@<pc-address>
```

### 🐧 Linux

```bash
ssh deck@<pc-address>
```

### 🪟 Windows

```powershell
ssh deck@<pc-address>
```

## 🧙‍♂️ Chapter 1: Who Gave the Order?

### ⚔️ Skills You'll Forge

- Reading the seconds around an event, not just the event

`Stopping Network Manager` means systemd was asked to stop it. Look at everything else in the same second:

```bash
sudo journalctl -D "$J" -b 0 --no-pager -S "21:13:19" -U "21:13:22" \
  | grep -E "systemd\[1\]|pkexec|steamos-manager"
```

```text
21:13:20 pkexec: deck: Executing command [COMMAND=/usr/bin/steamos-polkit-helpers/jupiter-fan-control --disable]
21:13:20 systemd[1]: Stopping Network Manager...
21:13:20 systemd[1]: Stopped Network Manager.
21:13:20 steamos-manager: ERROR dispatch_call{… member: "SetWifiBackend" …}:
         steamos_manager::manager::root: Error setting wifi backend: Exited 254
```

The Steam client, starting first-time setup, called **`SetWifiBackend`** on the `steamos-manager` D-Bus service. That call failed with exit code 254, and NetworkManager stayed stopped. The same pattern was in every previous boot.

### 🔍 Knowledge Check

- [ ] Which process made the D-Bus call, and which one ran the privileged work?

## 🧙‍♂️ Chapter 2: Read the Spell

### ⚔️ Skills You'll Forge

- Following a call into a privileged helper
- Spotting the failure path in a `set -e` script

`steamos-manager` runs a polkit helper. Read it straight from the install's read-only system partition:

```bash
sudo mount -o ro /dev/disk/by-partlabel/rootfs-B /mnt/root
less /mnt/root/usr/bin/steamos-polkit-helpers/steamos-wifi-set-backend-privileged
```

The parts that matter, quoted briefly from Valve's script (LGPL-2.1):

```bash
set -euo pipefail
# …
ensure_default_interface() {
    if ! iw dev wlan0 info &>/dev/null; then
        iw phy phy0 interface add wlan0 type station
        # …
    fi
}
# …
    restart_units)
        systemctl stop NetworkManager
        systemctl disable --now "${other_backend}"
        ensure_default_interface
        systemctl restart NetworkManager
```

Walk it on this PC:

1. `systemctl stop NetworkManager` — wired networking goes down with it.
2. `iw dev wlan0 info` fails: there is no Wi-Fi interface.
3. `iw phy phy0 interface add wlan0` fails: there is no Wi-Fi **radio** (`phy0`), because the board's MediaTek MT7927 has no driver in this kernel (Chapter V).
4. `set -e` ends the script on that failure. **`systemctl restart NetworkManager` never runs.**

The workaround in that function exists for a real Steam Deck problem, as its comments explain. On a PC with no usable Wi-Fi, it becomes a trap.

### 🔍 Knowledge Check

- [ ] Which single line would never fail on a Steam Deck but always fails here?
- [ ] Rewrite `restart_units` so NetworkManager is restarted even if the middle fails.

## 🧙‍♂️ Chapter 3: A Plausible Ghost

### ⚔️ Skills You'll Forge

- Checking your fix against the real call path

The first fix looked clever. The wrapper script `steamos-wifi-set-backend` exits early with *"already set to … nothing to do"* when the requested backend matches the config file. The install was set to `iwd`, so we changed the file to `wpa_supplicant`, which SteamOS 3.9 uses anyway.

It made no difference. `stat` showed why:

```text
99-valve-wifi-backend.conf   modified 21:49:56   (9 s after the next boot started)
wifi.backend=iwd
```

`steamos-manager` calls the **privileged helper directly** (`write_config` then `restart_units`), skipping the wrapper and its check. It rewrote the setting and ran the same failing path. The fix was built on the script that *looked* relevant, not on the path the logs showed. That's the glossary's **Plausible Ghost**: confident, well reasoned, and wrong.

### 🔍 Knowledge Check

- [ ] What should you have confirmed before writing the first fix?

## 🧙‍♂️ Chapter 4: The Guard at the Door

### ⚔️ Skills You'll Forge

- Writing a small, removable systemd guard unit
- Changing an immutable OS through its `/etc` overlay before first boot

SteamOS's root is read-only, but its `/etc` is an overlay whose writable layer lives on the `var` partition at `lib/overlays/etc/upper/`. The boot hook creates that directory only if it's missing, so files you place there before the first boot appear in `/etc`. Put them in **both** `var-A` and `var-B`, so they survive whichever slot boots.

The fix doesn't patch Valve's script. It adds a guard that restarts NetworkManager whenever something leaves it stopped:

```ini
# /etc/systemd/system/oneusb-nm-guard.service
[Unit]
Description=one-usb: restart NetworkManager if it is left stopped
After=NetworkManager.service
Conflicts=shutdown.target
Before=shutdown.target

[Service]
ExecStart=/bin/sh -c 'while sleep 5; do case "$(systemctl is-system-running)" in stopping) exit 0;; esac; systemctl is-active -q NetworkManager || { echo "NetworkManager was stopped; starting it"; systemctl start NetworkManager; }; done'
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# From the rescue system, as root, before the install's first boot:
for p in var-A var-B; do
  mount /dev/disk/by-partlabel/$p /mnt
  U=/mnt/lib/overlays/etc/upper/systemd/system
  install -d -m 755 "$U/multi-user.target.wants"
  install -m 644 oneusb-nm-guard.service "$U/"
  ln -sf /etc/systemd/system/oneusb-nm-guard.service "$U/multi-user.target.wants/"
  umount /mnt
done
systemd-analyze verify oneusb-nm-guard.service   # catches unit syntax errors
```

The proof came from the first boot, read over SSH:

```text
oneusb-nm-guard: Started one-usb: restart NetworkManager if it is left stopped.
oneusb-nm-guard: NetworkManager was stopped; starting it
$ nmcli -t -f STATE,CONNECTIVITY general
connected:full
```

The guard acted once, setup continued over Ethernet, and the OS could update. Remove the two files once Wi-Fi works; they do nothing on a healthy system.

### 🔍 Knowledge Check

- [ ] Why both `var-A` and `var-B`?
- [ ] Why does the guard check `is-system-running` before starting NetworkManager?

## 🧙‍♂️ Chapter 5: Carry the Petition Upstream

### ⚔️ Skills You'll Forge

- Searching before filing
- Adding evidence instead of agreement

Before filing, search. Valve's tracker already had [SteamOS#2514](https://github.com/ValveSoftware/SteamOS/issues/2514), *OOBE Cannot Proceed on Ethernet-Only Systems Until a Wi-Fi Adapter Is Present*. A community member had traced the same lines in the same script, and a Valve developer replied that a fix was merged and would ship in a future recovery image. The newest image at the time, 3.8.14 from July, didn't have it yet.

```bash
gh issue list -R ValveSoftware/SteamOS --search "wifi backend NetworkManager"
gh issue view 2514 -R ValveSoftware/SteamOS --comments
```

So the useful contribution was not a new issue or a "+1". It was new **evidence**:

- **A new trigger:** Wi-Fi hardware that *exists* but has no driver in the kernel, as on new X870E boards with the MT7927, not just PCs with no Wi-Fi
- **A disproved workaround:** editing `99-valve-wifi-backend.conf` doesn't work, because Steam rewrites it
- **A workaround needing no extra hardware:** the guard unit, with the log line that proves it
- **A precise question:** when does a recovery image with the fix ship?

### 🔍 Knowledge Check

- [ ] What makes a comment on an existing issue useful to a maintainer?

## 🎮 Implementation Challenge

**Objective:** Reproduce the trap safely in a VM, then defeat it.

```bash
# In any systemd Linux VM with NetworkManager:
cat >/tmp/silence.sh <<'EOF'
#!/bin/bash
set -euo pipefail
systemctl stop NetworkManager
iw phy phy0 interface add wlan0 type station   # fails: no Wi-Fi radio in the VM
systemctl restart NetworkManager                # never reached
EOF
sudo bash /tmp/silence.sh; echo "exit=$?"; nmcli general status
```

**Success Criteria:**

- [ ] Show the network down after the script, with its non-zero exit code
- [ ] Install the guard unit and show it restoring NetworkManager within 5 seconds
- [ ] Write the `restart_units` fix (for example a `trap … EXIT` that restarts NetworkManager) and explain it

## 🔍 Quest Network

```mermaid
graph LR
    C3[III The Rescue Lantern] --> C4[🗝️ IV The Silencing Script]
    C4 --> C5[V The Molten Core]
```

## 🎁 Rewards & Progression

- 🗝️ **Script Breaker** — found the exact line that silenced the network
- 📜 **Petition Bearer** — took evidence upstream, not just a complaint
- ⚡ **Skills unlocked:** cross-layer tracing, `set -e` failure analysis, pre-boot overlay fixes, upstream etiquette
- 🏆 **120 XP** toward the campaign

## 🔮 Next Adventures

Ethernet works. But the root of the trap is still there: the Wi-Fi chip has no driver. The last chapter goes to the kernel.

- ➡️ **Next chapter:** [Chapter V — The Molten Core](/quests/1010/silent-network-05-the-molten-core/)
- ⬅️ **Previous chapter:** [Chapter III — The Rescue Lantern](/quests/1001/silent-network-03-the-rescue-lantern/)
- 👑 **Campaign hub:** [Epic Quest: The Silent Network](/quests/codex/silent-network/)

## 📚 Resource Codex

- [SteamOS issue #2514](https://github.com/ValveSoftware/SteamOS/issues/2514) — the upstream report, root-cause notes, and Valve's reply
- [systemd.service(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) — `Restart=`, `ExecStart=`, and unit dependencies
- [NetworkManager.conf(5)](https://networkmanager.dev/docs/api/latest/NetworkManager.conf.html) — `wifi.backend` and conf.d drop-ins
- [Bash `set` builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) — what `-e`, `-u`, and `-o pipefail` really do
- [overlayfs](https://docs.kernel.org/filesystems/overlayfs.html) — upper, lower, and work directories

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Silent Network]] **Level hub:** [[Level 1010 - Automation & Testing]] **Previous:** [[The Rescue Lantern: Read the Logs of a System That Won't Talk]] **Next:** [[The Molten Core: Match Drivers to Kernels]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
