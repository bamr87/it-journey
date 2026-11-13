---
title: 'The Deaf Gatekeeper: When Your Own Server Stops Listening'
description: 'A PC waits for a PXE server that says it is running. Learn to check sockets instead of status pages, why a Python thread can die silently, how to keep a listener alive through errors, and why firmware can boot from a port Linux cannot drive.'
excerpt: 'The server said running. One of its three listeners had died hours earlier. Check sockets, not status pages.'
date: '2026-11-13T00:00:00.000Z'
lastmod: '2026-11-13T00:00:00.000Z'
level: '1000'
difficulty: 🟡 Medium
estimated_time: 1-2 hours
primary_technology: python
quest_type: main_quest
quest_series: The Silent Network
quest_line: The Silent Network
quest_arc: The Deaf Gatekeeper
skill_focus: infrastructure
learning_style: hands-on
author: IT-Journey Team
permalink: /quests/1000/silent-network-02-the-deaf-gatekeeper/
fmContentType: quest
layout: quest
draft: false
comments: true
mermaid: true
categories:
- Quests
- Networking
- Python
- Troubleshooting
tags:
- '1000'
- pxe
- dhcp
- python
- sockets
- main_quest
- hands-on
- gamified-learning
keywords:
  primary:
  - '1000'
  - pxe
  - proxydhcp
  - health-checks
  secondary:
  - lsof
  - python-threading
  - udp
  - network-drivers
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Has completed Chapter I, The Wrong Throne
  - Knows what DHCP does and what a UDP port is
  system_requirements:
  - A fortress machine running macOS or Linux with Python 3
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/0111/silent-network-01-the-wrong-throne/
  - /quests/1000/pxe-boot-server/
  unlocks_quests:
  - /quests/1001/silent-network-03-the-rescue-lantern/
rewards:
  badges:
  - 👂 Gate Listener — caught a server that was running but not listening
  skills_unlocked:
  - 🔌 Socket-level health checks
  - 🧵 Error handling that keeps long-running loops alive
  progression_points: 60
validation_criteria:
  completion_requirements:
  - A UDP server that survives a failed send, with a log line proving it
  skill_demonstrations:
  - Can list a process's listening sockets on macOS and Linux
  knowledge_checks:
  - Explains why the status page said running while PXE was dead
environment:
  os:
  - linux
  - macos
  shell:
  - bash
  - zsh
  pkg:
  - brew
  - apt
---
*The gatekeeper stood at his post all night. His lantern was lit, his banner flew, and anyone who asked "is the gate manned?" got a cheerful yes. He had simply stopped hearing knocks at a quarter past four in the afternoon. Travelers waited outside until dawn, and everyone blamed the road.*

## 🎯 Quest Objectives

By the end of this chapter you will:

- [ ] **List the sockets a process is really listening on**, on macOS and Linux
- [ ] **Explain how one Python thread can die** while the rest of the program runs on
- [ ] **Keep a network loop alive through errors** and log what failed
- [ ] **Recognize a "running" status as a weak signal** and design a stronger one
- [ ] **Explain why firmware can network-boot from a port Linux can't use**

## 🗺️ Quest Prerequisites

- **[Chapter I](/quests/0111/silent-network-01-the-wrong-throne/)** — you know which system you're debugging
- **PXE basics** — [Summon Machines From the Wire](/quests/1000/pxe-boot-server/) explains ProxyDHCP, TFTP, and iPXE in depth
- **Python 3** on your fortress

## 🌍 Choose Your Adventure Platform

### 🍎 macOS

```bash
# Which UDP ports does a process hold?
lsof -nP -iUDP -a -p "$(pgrep -f server.py | head -1)"
```

### 🐧 Linux

```bash
# ss shows listening sockets with the owning process.
sudo ss -ulpn | grep -E ':(67|69|4011)\b'
```

### 🪟 Windows

```powershell
# UDP endpoints and their owning process IDs.
Get-NetUDPEndpoint | Where-Object LocalPort -in 67,69,4011
```

## 🧙‍♂️ Chapter 1: The Knock Nobody Heard

### ⚔️ Skills You'll Forge

- Telling "process alive" apart from "service working"

The setup: a small Python PXE server on a Mac. It runs three listeners in three threads: **ProxyDHCP** on UDP 67 (answers "where do I boot from?"), a boot-server port on UDP 4011, and **TFTP** on UDP 69, plus HTTP for the big files. The router still hands out addresses; the server only answers PCs that ask to network-boot.

The PC sat at *waiting for the PXE server*. The server's status said `running`. Its log showed nothing from the PC, so the conclusion came easily: the PC's network port must be broken. We checked cables, lights, and switch ports. A full power cycle. Nothing.

Then one more look at the log, at what was **missing**: the server normally notes every DHCP broadcast on the LAN, from phones and watches and vacuum robots. There had been none for six hours. The server wasn't ignoring the PC. It wasn't hearing anyone.

```bash
lsof -nP -iUDP -a -p "$(cat build/netboot/server.pid)"
```

```text
COMMAND   PID   USER  FD  TYPE  NODE NAME
Python  98890 hero     8u IPv4   UDP *:4011
Python  98890 hero     9u IPv4   UDP *:69
```

Port 67 was gone. The process was alive; one of its ears had fallen off.

### 🔍 Knowledge Check

- [ ] Which evidence pointed away from the PC and toward the server?
- [ ] What does a missing line in a socket list tell you that a status page can't?

## 🧙‍♂️ Chapter 2: Death of a Thread

### ⚔️ Skills You'll Forge

- Reading a thread traceback
- Knowing which exceptions a network loop must survive

The server wrote its uncaught errors to a separate file. The cause was there, from 16:16:

```text
Exception in thread Thread-2 (proxydhcp_loop):
  File "netboot/server.py", line 507, in proxydhcp_loop
    s.sendto(reply, (dest, 68))
OSError: [Errno 65] No route to host
```

A Wi-Fi blip on the Mac made one reply fail. In Python, an exception that escapes a thread's function ends **that thread only**. The main program and the other threads carry on, and `threading` prints the traceback to stderr once. Nothing restarts the thread.

Here's the shape of the bug and the fix:

```python
# Before: one failed send ends the listener for good.
while True:
    data, addr = s.recvfrom(4096)
    reply = build_reply(data)
    for dest in ("255.255.255.255", broadcast):
        s.sendto(reply, (dest, 68))

# After: a failed send is logged, and the loop keeps listening.
while True:
    data, addr = s.recvfrom(4096)
    reply = build_reply(data)
    for dest in ("255.255.255.255", broadcast):
        try:
            s.sendto(reply, (dest, 68))
        except OSError as e:   # EHOSTUNREACH, ENETDOWN, ENETUNREACH while the network blips
            log(f"offer to {dest} failed: {e}")
```

After the fix and a restart, the PC that had "no network" was answered within two seconds.

### 🔍 Knowledge Check

- [ ] Why did the HTTP and TFTP parts keep working?
- [ ] Which errors should a long-running network loop catch, and which should still crash it?

## 🧙‍♂️ Chapter 3: A Stronger Signal Than "Running"

### ⚔️ Skills You'll Forge

- Designing health checks that test function

A process check answers "does it exist?". You needed "does it answer?". Options, from weakest to strongest:

| Check | Catches a dead thread? |
|---|---|
| Process exists (`pgrep`, a pidfile) | ❌ |
| Status page served by the same process | ❌ — another thread serves it |
| Each expected socket is open (`lsof`, `ss`) | ✅ |
| A heartbeat each listener updates; alert when stale | ✅ |
| A synthetic client that sends a real request | ✅ and proves the whole path |

```bash
# A five-second socket check you can run from cron or a status script.
pid=$(cat build/netboot/server.pid)
for port in 67 69 4011; do
  lsof -nP -iUDP:"$port" -a -p "$pid" >/dev/null || echo "DOWN: udp/$port"
done
```

### 🔍 Knowledge Check

- [ ] Why can't a status page served by the same process prove a listener is alive?

## 🧙‍♂️ Chapter 4: The Port With No Driver

### ⚔️ Skills You'll Forge

- Separating firmware network support from operating-system support

An earlier trap from the same night belongs in this chapter. This board has two wired ports: 10 GbE (Realtek RTL8127) and 5 GbE (RTL8126). The firmware PXE-booted happily from the 10 GbE port, because firmware ships its own network driver. Then Linux started, and its kernel (6.12 at that time) had **no driver for the RTL8127**. It waited for a link on a port it couldn't see.

```bash
# Which ports does Linux see, and which driver runs each one?
ip -br link
lspci -nnk | grep -iA3 ethernet
```

The fix was physical (move the cable to the 5 GbE port), then structural (a newer kernel). The lesson: **firmware support and OS support are separate**. A boot that gets the kernel loaded proves only the firmware's driver.

### 🔍 Knowledge Check

- [ ] Why could the firmware boot from a port Linux couldn't use?

## 🎮 Implementation Challenge

**Objective:** Build a UDP listener that survives its own errors, and prove it.

```python
#!/usr/bin/env python3
"""echo_gate.py — a UDP echo that must survive failed sends."""
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 9999))
while True:
    data, addr = s.recvfrom(2048)
    for dest in (addr, ("192.0.2.1", 9)):   # 192.0.2.0/24 is reserved: sends may fail
        try:
            s.sendto(data, dest)
        except OSError as e:
            print(f"send to {dest} failed: {e}", flush=True)
```

**Success Criteria:**

- [ ] Send it packets (`nc -u 127.0.0.1 9999`) while a send fails; it keeps echoing
- [ ] Remove the `try`, provoke the failure, and watch `lsof` lose the socket
- [ ] Add a socket check to a status script and show it reporting `DOWN`

## 🔍 Quest Network

```mermaid
graph LR
    C1[I The Wrong Throne] --> C2[👂 II The Deaf Gatekeeper]
    C2 --> C3[III The Rescue Lantern]
```

## 🎁 Rewards & Progression

- 👂 **Gate Listener** — caught a server that was running but not listening
- ⚡ **Skills unlocked:** socket health checks, resilient network loops, firmware vs OS drivers
- 🏆 **60 XP** toward the campaign

## 🔮 Next Adventures

The gate listens again, and the PC can boot a rescue system over the network. Now you can finally look inside the broken install.

- ➡️ **Next chapter:** [Chapter III — The Rescue Lantern](/quests/1001/silent-network-03-the-rescue-lantern/)
- ⬅️ **Previous chapter:** [Chapter I — The Wrong Throne](/quests/0111/silent-network-01-the-wrong-throne/)
- 👑 **Campaign hub:** [Epic Quest: The Silent Network](/quests/codex/silent-network/)

## 📚 Resource Codex

- [Python `threading`](https://docs.python.org/3/library/threading.html) — how uncaught exceptions end a thread (`threading.excepthook`)
- [lsof(8)](https://man7.org/linux/man-pages/man8/lsof.8.html) and [ss(8)](https://man7.org/linux/man-pages/man8/ss.8.html) — socket inspection
- [RFC 4578](https://www.rfc-editor.org/rfc/rfc4578) — DHCP options for PXE
- [Summon Machines From the Wire](/quests/1000/pxe-boot-server/) — the full PXE quest

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Silent Network]] **Level hub:** [[Level 1000 (8) - Cloud Computing Fundamentals]] **Previous:** [[The Wrong Throne: Prove Which System Booted]] **Next:** [[The Rescue Lantern: Read the Logs of a System That Won't Talk]] **Related:** [[Summon Machines From the Wire: Build a PXE Boot Server]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
