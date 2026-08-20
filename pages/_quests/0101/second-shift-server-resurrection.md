---
title: 'The Second Shift: Resurrect an Ancient Tower as Your Home Server'
author: IT-Journey Team
description: 'Repurpose a decade-old desktop into an always-available Docker host — Wake-on-LAN necromancy, a boot-to-tmux console, LAN-scoped firewalling, and the honest limits of old silicon.'
excerpt: Raise a retired PC from the closet and put it on the second shift as a wake-on-demand Docker home server.
preview: images/previews/second-shift-server-resurrection-quest.png
date: '2026-08-15T18:00:00.000Z'
lastmod: '2026-08-15T18:00:00.000Z'
level: '0101'
difficulty: 🟡 Medium
estimated_time: 90-120 minutes
primary_technology: docker
quest_type: main_quest
quest_series: Homelab Operations
quest_line: The Reforged Iron
quest_arc: The Second Shift
quest_dependencies:
  required_quests:
  - /quests/0101/docker-mastery/
  recommended_quests:
  - /quests/0101/environment-management/
  unlocks_quests:
  - /quests/0101/secrets-management/
skill_focus: devops
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Comfort in a Linux shell over ssh
  - Docker and docker compose basics (see Docker Mastery)
  system_requirements:
  - A retired desktop or tower PC (2010s-era is fine) with a wired NIC
  - Any laptop on the same LAN to act as your command seat
  - A USB stick for a Linux installer
  skill_level_indicators:
  - Can install a Linux distribution unassisted
  - Can edit config files in a terminal editor
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - The server wakes from a magic packet and serves a container over the LAN
  skill_demonstrations:
  - Can wake, connect to, and administer the box without touching its keyboard
  - Can explain why each firewall rule exists
  knowledge_checks:
  - Understands Wake-on-LAN, tmux session sharing, and LAN-scoped UFW rules
  - Can name two workloads old hardware handles well and two it cannot
permalink: /quests/0101/second-shift-server-resurrection/
categories:
- Quests
- DevOps
- Medium
tags:
- '0101'
- docker
- main_quest
- devops
- hands-on
- gamified-learning
keywords:
  primary:
  - '0101'
  - docker
  - main_quest
  secondary:
  - devops
  - homelab
  - wake-on-lan
  - tmux
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0101 (5) Quest: Main Quest - The Reforged Iron'
rewards:
  badges:
  - 🏆 Necromancer of Iron - Raised dead hardware into a working server
  - 🛡️ Warden of the Gate - Scoped every service to the LAN with UFW
  skills_unlocked:
  - 🛠️ Wake-on-LAN & headless server administration
  - 🧠 Workload-to-hardware matching
  progression_points: 75
  unlocks_features:
  - Secrets and environment quests hardened on your own always-on host
layout: quest
environment:
  os:
  - cloud
  shell:
  - bash
---

*Hark, adventurer! In every homestead there stands a tomb — a storage closet where a once-mighty tower sleeps beneath dust and cable-tangle. The merchants would have you believe only new iron can serve, that a machine of fourteen winters belongs to the scrapheap. They lie. This quest is an act of necromancy: you will raise that machine, bind it with containers, teach it to sleep without dying and wake at a whispered packet, and set it working the second shift — while learning more about servers than any cloud console will ever teach you.*

*The reference corpse for this quest was a 2012 Core i7 tower. By quest's end it ran ten containers and a monitoring stack. Yours will too.*

## 📖 The Legend Behind This Quest

*Old iron fails at exactly two things: single-thread bursts of modern compute, and anything demanding a current GPU. Everything else — holding databases, serving sites, watching networks, storing backups — is a memory-and-disk trade, and old towers are rich in both once their cheap DDR3 is maxed. The discipline this quest teaches is **matching the workload to the machine**: the same judgment that separates architects from shoppers. A server that costs nothing and teaches everything is the best training ground in the realm.*

## 🎯 Quest Objectives

By completing this quest, you will:

**Primary objectives (required for completion):**

- [ ] Install a minimal headless Linux on the old machine and mask every sleep target
- [ ] Arm Wake-on-LAN and wake the box from your laptop with a magic packet
- [ ] Boot the physical console into a shared tmux session that ssh attaches to
- [ ] Run at least one compose stack and reach it from another device on the LAN
- [ ] Scope every published port to your LAN subnet with UFW

**Secondary objectives (bonus mastery):**

- [ ] Add a monitoring pane (btop + a `docker ps` watch) to the console session
- [ ] Write a one-word shell function on your laptop that wakes and connects
- [ ] Benchmark one workload the machine is *bad* at, and write down why

## 🗺️ Quest Prerequisites

Meet the requirements in the front matter above — most importantly: a retired tower, a laptop, and the will to disturb the dead.

## 🧙‍♂️ Chapter 1: Raising the Dead (Install & Never Sleep)

Install a minimal Debian or similar — **no desktop environment**; this machine's face will be a terminal. Then perform the first rite, because consumer boards ship with treacherous power defaults:

```bash
sudo systemctl mask sleep.target suspend.target hibernate.target
```

A server that naps mid-`apt upgrade` will corrupt your trust before it corrupts anything else. The reference machine suspended itself on day one; masked targets ended that forever.

## 🧙‍♂️ Chapter 2: The Whispered Packet (Wake-on-LAN)

Enable WoL in the BIOS, then arm the NIC and persist it:

```bash
sudo ethtool -s eno1 wol g        # arm (persist with a small systemd unit)
```

From your laptop, the resurrection word:

```bash
wakeonlan aa:bb:cc:dd:ee:ff       # ~30 seconds to ssh-able
```

The box now has exactly two states — fully alive, or costing nothing — and you command the transition from your chair. Test it three times: cold boot, warm shutdown, and after a power cut.

## 🧙‍♂️ Chapter 3: A Face for the Headless (Shared tmux Console)

Attach that spare monitor and have tty1 auto-login into a tmux session named `console`. In your shell profile on the server, make interactive ssh logins attach to the same session. The spell's effect: your laptop terminal and the physical monitor become **one shared screen**. Work started at the desk glows on the monitor across the room; a crash-looping container is seen from the kitchen, not discovered next Tuesday.

## 🧙‍♂️ Chapter 4: The Container Workbench

Install Docker. Every workload lives under `~/dev/<project>/` as a compose file — nothing installs on the host itself. When two stacks demand the same port, do not edit upstream files; lay an override beside them:

```yaml
# docker-compose.override.yml
services:
  postgres:
    ports: !override
      - "5433:5432"
```

Then raise the gates, scoped to your own lands only:

```bash
sudo ufw allow ssh
sudo ufw allow from 192.168.4.0/24 to any port 4000 proto tcp
sudo ufw enable
```

Every rule answers to a service you can name. If you cannot name it, it does not get a rule.

## 🎮 Mastery Challenges

- **⚔️ The Honest Wall**: Run a quantized 7B language model on the old CPU (Ollama makes this easy). Record tokens/second. The reference tower managed 4.4 — a working miracle and a useless tool. Write three sentences on why (hint: AVX2), and name where that workload should live instead.
- **🛡️ The Observatory**: Stand up an ELK or similar stack in containers and ship the system journal into it. Old iron runs enterprise observability shockingly well — prove it with a dashboard.
- **🏹 One Word**: Build a `myserver` shell function with subcommands: bare = connect, `wake`, `ps`, `logs <container>`. Friction is the real final boss of every homelab.

## 🏆 Quest Rewards & Achievements

Completing this quest grants the badges and skills listed in the quest scroll above — and a server with a pulse, a second shift, and a zero-dollar invoice.

## 🗺️ Next Steps in Your Journey

With an always-available host of your own, carry your loot onward to [Secrets Management](/quests/0101/secrets-management/) — real machines demand real credential hygiene — and deepen the container craft in [Environment Management](/quests/0101/environment-management/).

## 🤝 Quest Completion Checklist

- [ ] Sleep targets masked; box survived a week without napping
- [ ] Woken from a magic packet three different ways
- [ ] Physical monitor and ssh share one tmux session
- [ ] A compose stack reachable from a second device on the LAN
- [ ] UFW rules scoped to the subnet, each one explainable
- [ ] The Honest Wall challenge written up: what this machine cannot do, and why
