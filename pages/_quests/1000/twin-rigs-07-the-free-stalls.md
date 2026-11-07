---
title: 'The Free Stalls: Stock SteamOS with Open Source Games'
description: Use Flatpak and Flathub to fill SteamOS with open source games from a reproducible list, bring them into Game Mode with Steam Input, and add indie builds and the Rewind Arcade to your library.
excerpt: Build a reproducible library of open source and indie games on SteamOS, ready for the couch.
date: '2026-11-06T00:00:00.000Z'
lastmod: '2026-11-06T00:00:00.000Z'
level: '1000'
difficulty: 🟡 Medium
estimated_time: 1-2 hours
primary_technology: flatpak
quest_type: main_quest
quest_series: The Twin Rigs
quest_line: The Twin Rigs
quest_arc: The Free Stalls
skill_focus: infrastructure
learning_style: hands-on
author: IT-Journey Team
permalink: /quests/1000/twin-rigs-07-the-free-stalls/
fmContentType: quest
layout: quest
draft: false
comments: true
mermaid: true
categories:
- Quests
- SteamOS
- Open Source
- Gaming
tags:
- '1000'
- steamos
- flatpak
- open-source
- indie-games
- main_quest
- hands-on
- gamified-learning
keywords:
  primary:
  - '1000'
  - flatpak
  - gaming-rig
  secondary:
  - flathub
  - steam-input
  - supertuxkart
  - itch-io
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Has completed Chapter VI of The Twin Rigs
  - Can use a Linux terminal
  system_requirements:
  - SteamOS running on the Great Rig
  - A keyboard, mouse, and gamepad
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/0111/twin-rigs-06-the-steam-rite/
  unlocks_quests:
  - /quests/1001/twin-rigs-08-the-throttle-wraith/
rewards:
  badges:
  - 🛒 Stallkeeper — built a reproducible library of open source games
  skills_unlocked:
  - 📦 Flatpak on an immutable system
  - 📜 Reading software licences
  progression_points: 80
validation_criteria:
  completion_requirements:
  - Four open source games launch from Game Mode
  - The game list is committed
  skill_demonstrations:
  - Can rebuild the library from games.txt
  knowledge_checks:
  - Explains the difference between open source and free to play
environment:
  os:
  - linux
  shell:
  - bash
  pkg:
  - none
---
*Past the great storefront runs a quieter row of market stalls, where the goods cost nothing and every recipe is posted on the wall. Racers, strategy epics, voxel worlds, and dungeon crawlers wait here, built by volunteers and kept alive for decades. Nobody can delist them from your library. Fill your packs.*

## 🎯 Quest Objectives

By the end of this chapter you will:

- [ ] **Explain why Flatpak suits a read-only system** and where its apps live
- [ ] **Install open source games** from a list you keep under version control
- [ ] **Add those games to Steam** so that they launch from Game Mode
- [ ] **Set up gamepad controls** for a game with no built-in support
- [ ] **Add indie builds and the Rewind Arcade** to your library

## 🗺️ Quest Prerequisites

- **[Chapter VI](/quests/0111/twin-rigs-06-the-steam-rite/)** — SteamOS running on the Great Rig
- **Desktop Mode, a keyboard, and a mouse** — for the installs
- **A gamepad** — to test everything from the couch

## 🌍 Choose Your Adventure Platform

*Every spell here runs in Konsole, in Desktop Mode on the Great Rig.*

### 🐧 Linux

```bash
flatpak --version
flatpak remotes
```

If `flathub` is missing from the list, add it:

```bash
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

## 🧙‍♂️ Chapter 1: Why the Stalls Fit This Rig

### ⚔️ Skills You'll Forge

- Matching a packaging format to an operating system
- Separating free software from free-of-charge software

In Chapter VI you learned that the SteamOS root filesystem is read-only. Flatpak was made for this. Each app arrives with its own runtime, and lives outside the sealed system, so OS updates leave it alone. It also runs inside a sandbox, which limits what it can touch.

"Free" has two meanings at this market, and it pays to tell them apart:

| Kind | Example | You get |
|---|---|---|
| **Open source** | SuperTuxKart (GPL) | The game at no cost, plus the right to read, change, and share the code |
| **Free to play** | Many Steam titles | The game at no cost, but the code and rules stay with the publisher |
| **Paid indie** | A game on itch.io | A game you buy, often with no DRM |

### 🔍 Knowledge Check

- [ ] Why do Flatpak apps survive a SteamOS update?
- [ ] What does an open source licence give you beyond a free price?

## 🧙‍♂️ Chapter 2: Fill the Packs

### ⚔️ Skills You'll Forge

- Treating an install list as data
- Reproducing a setup with one command

These games cover a good spread of genres, and each one is available on Flathub:

| Game | Genre | Flathub ID | Licence |
|---|---|---|---|
| SuperTuxKart | Kart racing | `net.supertuxkart.SuperTuxKart` | GPL-3.0 |
| Battle for Wesnoth | Turn-based strategy | `org.wesnoth.Wesnoth` | GPL-2.0 |
| 0 A.D. | Historical real-time strategy | `com.play0ad.zeroad` | GPL-2.0, CC-BY-SA |
| Xonotic | Arena shooter | `org.xonotic.Xonotic` | GPL-3.0 |
| Luanti | Voxel sandbox | `org.luanti.luanti` | LGPL-2.1 and others |
| Veloren (through Airshipper) | Voxel RPG | `net.veloren.airshipper` | GPL-3.0 |
| OpenRA | Classic RTS engine | `net.openra.OpenRA` | GPL-3.0 |
| Shattered Pixel Dungeon | Roguelike | `com.shatteredpixel.shatteredpixeldungeon` | GPL-3.0 |

Keep your list in a file. That way, rebuilding this library on a fresh install takes one command.

```bash
cat > games.txt <<'EOF'
net.supertuxkart.SuperTuxKart
org.wesnoth.Wesnoth
com.play0ad.zeroad
org.xonotic.Xonotic
org.luanti.luanti
net.veloren.airshipper
net.openra.OpenRA
com.shatteredpixel.shatteredpixeldungeon
EOF
flatpak install --user -y flathub $(cat games.txt)
flatpak list --app --columns=name,application
```

Prefer clicking? The **Discover** app in Desktop Mode browses the same store. To update everything later:

```bash
flatpak update --user -y
```

### 🔍 Knowledge Check

- [ ] What does `--user` change about where the games are installed?
- [ ] How would you rebuild this library after a re-image?

## 🧙‍♂️ Chapter 3: Bring Them to the Couch

### ⚔️ Skills You'll Forge

- Adding outside apps to the Steam library
- Mapping a gamepad to keyboard and mouse controls

Flatpak games do not appear in Game Mode on their own. In Desktop Mode, open Steam, then choose **Games**, then **Add a Non-Steam Game to My Library**. Tick your games and click **Add Selected Programs**. Switch back to Game Mode, and you will find them in your library.

Many of these games were designed for a keyboard and mouse. **Steam Input** bridges that gap for any game in your library. Open a game's page in Game Mode, select the controller icon, and pick a template such as **Keyboard (WASD) and Mouse**, then adjust the buttons. SuperTuxKart supports gamepads natively, which makes it a good first test.

### 🔍 Knowledge Check

- [ ] Which mode do you use to add a non-Steam game?
- [ ] How can a gamepad drive a game with no controller support?

## 🧙‍♂️ Chapter 4: Beyond the Stalls

### ⚔️ Skills You'll Forge

- Running a portable Linux game build
- Launching a website as a full-screen app

**Indie builds.** [itch.io](https://itch.io/games/free/platform-linux) lists thousands of Linux games, and many indies ship a plain folder or an AppImage. Keep them in your home folder, where updates will not touch them:

```bash
mkdir -p ~/Games
# After downloading a game into ~/Games:
chmod +x ~/Games/your-game.AppImage
```

Add the file to Steam the same way, using the **Browse** button in the Add a Game window.

**Rewind Arcade, again.** The browser arcade you played on the Pi runs here too, and you can pin it to Game Mode. Install a browser, then add it as a non-Steam game:

```bash
flatpak install --user -y flathub org.mozilla.firefox
```

Add Firefox to Steam, open its **Properties**, and rename the entry to `Rewind Arcade`. Then add this to the end of its **Launch Options**, after any text that is already there:

```text
--kiosk https://bamr87.github.io/rewind-arcade/
```

Launch it from Game Mode, and your retro shelf opens full screen on the big rig.

### 🔍 Knowledge Check

- [ ] Why does `~/Games` survive a SteamOS update?
- [ ] What does the `--kiosk` flag change?

## 🎮 Implementation Challenge

**Objective:** Stock the rig, and keep the list in your chronicle.

**Success Criteria:**

- [ ] At least four open source games launch from Game Mode
- [ ] At least one uses a Steam Input template that you adjusted
- [ ] The Rewind Arcade opens full screen from Game Mode
- [ ] Your game list is committed to `twin-rigs`

On your fortress, in `twin-rigs`:

```bash
scp deck@<rig-ip>:games.txt .
git add games.txt
git commit -m "docs: record the open source game library"
```

SSH must be running on the rig for that copy. Start it the same way you did in Chapter VI, and stop it afterward.

## 🔍 Quest Network

```mermaid
graph LR
    C6[The Steam Rite] --> C7[🛒 The Free Stalls]
    C7 --> C8[The Throttle Wraith]
```

## 🎁 Rewards & Progression

- 🛒 **Stallkeeper** — built a reproducible library of open source games
- ⚡ **Skills unlocked:** Flatpak, reading software licences, Steam Input mapping, reproducible setups
- 🏆 **80 XP** toward the campaign

*Chapters sit at different levels by design: the campaign uses the level number for progression, and each chapter also appears on its own level hub.*

## 🔮 Next Adventures

Both rigs are full of games. One question remains: will they hold up when it counts?

- ➡️ **Next chapter:** [Chapter VIII — The Throttle Wraith](/quests/1001/twin-rigs-08-the-throttle-wraith/)
- ⬅️ **Previous chapter:** [Chapter VI — The Steam Rite](/quests/0111/twin-rigs-06-the-steam-rite/)
- 👑 **Campaign hub:** [Epic Quest: The Twin Rigs](/quests/codex/twin-rigs/)

## 📚 Resource Codex

- [Flathub](https://flathub.org/) — the app store used in this chapter, with licence details on each page
- [Flatpak documentation](https://docs.flatpak.org/) — how sandboxing and runtimes work
- [itch.io Linux games](https://itch.io/games/free/platform-linux) — free indie games for Linux
- [Rewind Arcade](https://bamr87.github.io/rewind-arcade/) — the live browser arcade

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Twin Rigs]] **Level hub:** [[Level 1000 (8) - Cloud Computing Fundamentals]] **Previous:** [[The Steam Rite: Install SteamOS on the Great Rig]] **Next:** [[The Throttle Wraith: Prove Both Rigs Under Sustained Load]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
