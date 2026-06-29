---
title: 'Bashcrawl Quest: Terminal Adventure RPG'
description: Explore nine Bashcrawl chambers to master navigation, permissions, environment variables, symlinks, and pipes in a gamified terminal RPG adventure.
preview: images/previews/bashcrawl-quest-terminal-adventure-rpg.png
date: '2025-07-05T12:12:17.000Z'
lastmod: '2026-05-23T02:30:23.000Z'
categories:
- Quests
- Terminal
- Gaming
- Education
tags:
- bashcrawl
- terminal
- command-line
- adventure-game
- bash
- '0000'
author: IT-Journey Team
level: '0000'
fmContentType: quest
quest_type: main_quest
quest_line: Foundation Path
quest_arc: Terminal Mastery Arc
difficulty: 🟢 Easy
estimated_time: 60-90 minutes
primary_technology: bash
skill_focus:
- Terminal
- Navigation
- File System
learning_style: hands-on
quest_series: Bashcrawl Adventure Path
keywords:
  primary:
  - bashcrawl
  - terminal adventure
  - bash commands
  - command line learning
  secondary:
  - dungeon game
  - shell scripting
  - terminal navigation
  - linux tutorial
prerequisites:
  knowledge_requirements:
  - Basic computer navigation
  - Terminal application access
  - Bash or compatible shell
rewards:
  badges:
  - 🏆 Terminal Explorer
  - 🗝️ Dungeon Master
  progression_points: 200
quest_dependencies:
  unlocks_quests:
  - /quests/0000/entrance/
  - /quests/0000/workshop/
  - /quests/0000/cellar/
  - /quests/0000/armoury/
  - /quests/0000/chamber/
  - /quests/0000/hidden-chapel/
  - /quests/0000/vault/
  - /quests/0000/scrap/
  - /quests/0000/rift/
  - /quests/0000/agent-mode/
validation_criteria:
- Navigate through the entrance and read the first scroll
- Navigate through at least five chambers
- Defeat at least one combat encounter
- Complete the Rift final boss
excerpt: Embark on an epic terminal adventure that teaches Bash commands through nine interconnected dungeon chambers, each a dedicated walkthrough side-quest
draft: false
permalink: /quests/0000/bashcrawl/
mermaid: true
---
*Welcome to the Bashcrawl Catacombs — an interactive terminal dungeon where every command is a spell and every directory a new realm to explore. Nine interconnected chambers await, each a side-quest that teaches a core set of Bash skills through gameplay.*

This hub is your **walkthrough and strategy guide** to the game. Play instantly in the browser below, use the nine chamber walkthroughs as your field manual, then graduate to the **advanced version** — [installing Bashcrawl](#play-locally) and playing it in a real shell.

## 🕹️ Play in Your Browser

The full game runs right here — no install required. Keep this guide open alongside it.

{% include bashcrawl-terminal.html %}

## 🗺️ Catacombs Map

```mermaid
flowchart TD
    HUB([🏰 Bashcrawl Hub]) --> ENT[🚪 Entrance]
    ENT --> WRK[🔨 Workshop]
    ENT --> CEL[🍷 Cellar]
    WRK --> CEL
    CEL --> ARM[⚔️ Armoury]
    CEL --> CHP[⛪ Hidden Chapel]
    CEL --> VLT[🔒 Vault]
    CEL --> SCR[🗑️ Scrap Heap]
    ARM --> CHM[🐉 Chamber]
    CHM --> RFT[🌀 The Rift]
    CHP --> RFT
    VLT --> RFT
    SCR --> RFT
    RFT --> AGT[🤖 Agent Mode]
    click ENT "/quests/0000/side-quests/entrance/"
    click WRK "/quests/0000/side-quests/workshop/"
    click CEL "/quests/0000/side-quests/cellar/"
    click ARM "/quests/0000/side-quests/armoury/"
    click CHM "/quests/0000/side-quests/chamber/"
    click CHP "/quests/0000/side-quests/hidden-chapel/"
    click VLT "/quests/0000/side-quests/vault/"
    click SCR "/quests/0000/side-quests/scrap/"
    click RFT "/quests/0000/side-quests/rift/"
    click AGT "/quests/0000/side-quests/agent-mode/"
```

## 📖 Chapter Guide

| # | Chamber | Difficulty | Key Commands | Walkthrough |
|---|---------|-----------|--------------|-------------|
| 1 | 🚪 Entrance | 🟢 Easy | `pwd` `ls` `cd` `cat` | [Start Here](/quests/0000/side-quests/entrance/) |
| 2 | 🔨 Workshop | 🟢 Easy | `mkdir` `touch` `rm` `echo >` | [Workshop](/quests/0000/side-quests/workshop/) |
| 3 | 🍷 Cellar | 🟢 Easy | `ls -F` `alias` `file` | [Cellar](/quests/0000/side-quests/cellar/) |
| 4 | ⚔️ Armoury | 🟡 Medium | `chmod` `./` permissions | [Armoury](/quests/0000/side-quests/armoury/) |
| 5 | 🐉 Chamber | 🟡 Medium | `let` `$(( ))` arithmetic | [Chamber](/quests/0000/side-quests/chamber/) |
| 6 | ⛪ Hidden Chapel | 🔴 Hard | `ls -a` `man` hidden dirs | [Chapel](/quests/0000/side-quests/hidden-chapel/) |
| 7 | 🔒 Vault | 🟡 Medium | `export` `$VAR` `env` | [Vault](/quests/0000/side-quests/vault/) |
| 8 | 🗑️ Scrap Heap | 🟡 Medium | `ln -s` `readlink` symlinks | [Scrap](/quests/0000/side-quests/scrap/) |
| 9 | 🌀 The Rift | 🔴 Hard | pipes `\|` `&&` redirection | [Rift](/quests/0000/side-quests/rift/) |
| ★ | 🤖 Agent Mode | 🔴 Hard | `--agent` `--batch` `--screenshot-dir` | [Agent](/quests/0000/side-quests/agent-mode/) |

{% include bashcrawl-play-local.html %}

## 🧙 In-Game Commands

| Command | Effect |
|---------|--------|
| `quest` | Show current quest objectives |
| `merlin` | Get a context-aware hint |
| `status` or `hp` | Show health and progress |
| `inventory` or `i` | List collected items |
| `map` | Display the dungeon map |
| `save` | Save current progress |
| `load` | Restore last save |
| `tutorial` | Toggle tutorial mode |
| `commands` | List all game commands |
| `help` | Show help screen |
| `reset` | Reset to a fresh start |

## ⚔️ Combat Commands

| Script | Chamber | Encounter |
|--------|---------|-----------|
| `./statue` | Chamber | Solve arithmetic to defeat the stone guardian |
| `./monster` | Chapel hall | Combat encounter — use weapon from Armoury |
| `./ghost` | Vault lab | Ghost encounter — environment variable skills required |
| `./goblet` | Vault stronghold | Solve the goblet puzzle; unlocks the path to the Rift |

## 🔧 Maintenance Commands

```bash
./setup.sh --verify        # Check installation health
./setup.sh --repair        # Fix common permission/setup issues
./main.sh --status         # Show current game progress
./main.sh --reset          # Reset for a fresh run
```

## 🧭 Learning Path Tips

- Start with **Entrance → Workshop → Cellar** to build confidence before branching.
- Keep a command journal: capture one new command and one mistake after each chamber.
- Replay one chamber in a different mode (Web, Classic, or Native) to reinforce transfer skills.

## 📚 External Resources

- [Bashcrawl — Play Online](https://bamr87.github.io/bashcrawl/)
- [Bashcrawl GitHub Repository](https://github.com/bamr87/bashcrawl/)
- [The Spellbook: Bash Cheatsheet](/shell/)
- [The Grand Grimoire: Complete Bash Reference](/docs/bash-complete-reference/)
- [Original Upstream — GitLab slackermedia/bashcrawl](https://gitlab.com/slackermedia/bashcrawl)

## 🗺️ Quest Network

**Quest Series**: Bashcrawl Adventure Path

**Prerequisites**: None — this hub is a perfect entry point.

**Child Quests**: All nine chamber walkthroughs above (see Chapter Guide).

**Sequel Quest**: [Bash Run and Beyond](/quests/0000/side-quests/bash-run/) — extend the dungeon with custom scripting.

---

*Ready? Run `./bash_crawl.sh` or open [Bashcrawl Online](https://bamr87.github.io/bashcrawl/) and type your first command.* ⚔️✨
