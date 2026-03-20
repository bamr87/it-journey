---
title: 'bashrun and Beyond: Building an Advanced Terminal Game'
author: IT-Journey Team
description: Starting with bashrun as a base and building upon it is a great way to
  create an advanced terminal-based game. bashrun is typically built using shell scripts,
  which can be a bit limiting but also provides a good foundation for learning and
  expanding.
excerpt: Starting with bashrun as a base and building upon it is a great way to create
  an advanced terminal-based game. bashrun is typically built using shell scripts,
  which can be a bit limiting but also provides a good foundation for learning and
  expanding.
snippet: Transform basic shell commands into an interactive gaming experience
preview: images/previews/bashrun-and-beyond-building-an-advanced-terminal-g.png
date: 2024-05-28 00:00:00+00:00
lastmod: 2025-11-30 05:46:59.326000+00:00
level: '0000'
difficulty: 🟡 Medium
estimated_time: 90-120 minutes
primary_technology: bash
quest_type: side_quest
quest_series: Level 000 - Foundation Skills
quest_line: Foundation Path
quest_arc: Terminal Mastery Arc
quest_dependencies:
  required_quests:
  - /quests/bashcrawl-terminal-adventure/
  - /quests/hello-linux/linux-fundamentals/
  recommended_quests:
  - /quests/level-0000-terminal-fundamentals/
  unlocks_quests: []
quest_relationships:
  child_quests: []
  sequel_quests: []
  parallel_quests: []
learning_paths:
  primary_paths:
  - Software Development
  - System Administration
  character_classes:
  - 💻 Software Developer
  - 🏗️ System Engineer
  skill_trees:
  - Terminal Mastery
  - Shell Scripting
skill_focus:
- Quests
- Terminal
- Level-000
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Basic bash command knowledge
  - Terminal navigation skills
  - Text editor familiarity (nano, vim, or VS Code)
  system_requirements:
  - Unix/Linux terminal (or WSL on Windows)
  - Bash shell installed
  skill_level_indicators:
  - Comfortable running commands in the terminal
  - Can create and edit files from the command line
validation_criteria:
- Complete the terminal game development
- Successfully run the enhanced bashrun game
- Demonstrate understanding of shell scripting concepts
permalink: /quests/lvl_000/bash-run/
categories:
- Quests
- Terminal
- Level-000
tags:
- bash
- terminal
- game-development
- shell-scripting
- lvl-000
keywords:
- bash
- terminal
- game-development
- shell-scripting
- lvl-000
fmContentType: quest
draft: false
sub-title: 'Level 000 Quest: Advanced Terminal Game Development'
rewards:
  badges:
  - 🏆 Bash Scripting Badge
  - ⚡ Advanced Terminal Skills
  skills_unlocked:
  - 🛠️ Game Development Foundation
  - 🎯 Shell Programming Mastery
  progression_points: 100
  unlocks_features:
  - Advanced scripting quest access
  - Terminal automation capabilities
related_quests:
- bashcrawl/README.md - Terminal Adventure RPG
- hello-noob.md - Beginner's IT Journey
---
*Greetings, aspiring script mage! In this side quest, you will forge a terminal-based game using the arcane arts of Bash scripting. Starting with bashrun as your foundation, you will enhance and expand it into a fully interactive adventure — complete with inventory, combat, and save systems.*

## 🎯 Quest Objectives

### Primary Objectives (Required for Quest Completion)
- [ ] **Clone and explore the bashrun repository** — Understand the game's structure and components
- [ ] **Enhance the storyline and levels** — Add new levels with puzzles and objectives
- [ ] **Implement an inventory system** — Create item collection and management mechanics
- [ ] **Add save/load functionality** — Allow players to preserve and restore progress

### Secondary Objectives (Bonus Achievements)
- [ ] **Build a combat system** — Create enemy encounters with attack/run mechanics
- [ ] **Add ASCII art and UI polish** — Improve the visual presentation of the game
- [ ] **Create a comprehensive tutorial** — Help new players learn the game mechanics
- [ ] **Write unit tests for game functions** — Validate game logic with automated tests

### Mastery Indicators
- [ ] Can explain Bash function syntax and variable scoping
- [ ] Can create interactive terminal applications from scratch
- [ ] Can implement file-based persistence in shell scripts
- [ ] Can debug and troubleshoot Bash scripts independently

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Basic bash command knowledge (`cd`, `ls`, `cat`, `echo`)
- [ ] Terminal navigation skills
- [ ] Text editor familiarity (nano, vim, or VS Code)

### 🛠️ System Requirements
- [ ] macOS, Linux, or WSL on Windows
- [ ] Git installed and configured
- [ ] Bash shell access

---

Starting with bashrun as a base and building upon it is a great way to create an advanced terminal-based game. bashrun is typically built using shell scripts, which can be a bit limiting but also provides a good foundation for learning and expanding.

Here's a step-by-step guide to start with bashrun and build upon it:

### Step 1: Setting Up bashrun

1. **Clone the bashrun Repository:**
   If bashrun is hosted on a repository, you can clone it using:
   ```bash
   git clone https://github.com/commandlineadventure/bashrun.git bashrun
   cd bashrun
   ```

   > **Note**: If the above repository is unavailable, you can create your own bashrun project from scratch using the code examples below, or search for "bash text adventure" on GitHub for similar projects.

2. **Understand the Structure:**
   Explore the directory structure and understand how the game is organized. Typically, it might include directories for maps, scripts for different levels, and resources for the game.

### Step 2: Basic Improvements

1. **Enhance Storyline and Levels:**
   - Add new levels with more complex puzzles and objectives.
   - Create more detailed and engaging storylines.

   Example of adding a new level (`level2.sh`):
   ```bash
   #!/bin/bash
   echo "Welcome to Level 2!"
   echo "You need to find the hidden key to unlock the treasure."

   # Player actions and logic here
   ```

2. **Improve Navigation and Interaction:**
   Add more commands for interaction, such as examining objects or using items.

   Example of an interaction command:
   ```bash
   function examine {
       case $1 in
           "key")
               echo "It's a shiny golden key. It might unlock something."
               ;;
           "door")
               echo "It's a sturdy wooden door. It seems to be locked."
               ;;
           *)
               echo "You can't examine that."
               ;;
       esac
   }
   ```

3. **Add an Inventory System:**
   Implement a simple inventory system to manage items collected by the player.

   Example inventory system:
   ```bash
   inventory=()

   function add_to_inventory {
       inventory+=("$1")
       echo "$1 added to your inventory."
   }

   function show_inventory {
       echo "Your inventory: ${inventory[@]}"
   }
   ```

### Step 3: Advanced Features

1. **Implement Save/Load Functionality:**
   Allow players to save their progress and load it later.

   Example save/load system:
   ```bash
   function save_game {
       echo "${inventory[@]}" > savefile.txt
       echo "Game saved."
   }

   function load_game {
       if [ -f savefile.txt ]; then
           inventory=($(cat savefile.txt))
           echo "Game loaded."
       else
           echo "No saved game found."
       fi
   }
   ```

2. **Add a Combat System:**
   Create a simple combat system where players can encounter enemies and engage in battles.

   Example combat system:
   ```bash
   function combat {
       local enemy_health=10
       local player_health=20

       echo "You encounter an enemy!"

       while [ $enemy_health -gt 0 ] && [ $player_health -gt 0 ]; do
           echo "Choose an action: [attack/run]"
           read action
           case $action in
               "attack")
                   enemy_health=$((enemy_health - 2))
                   player_health=$((player_health - 1))
                   echo "You attack the enemy. Enemy health: $enemy_health"
                   echo "The enemy attacks you. Your health: $player_health"
                   ;;
               "run")
                   echo "You run away!"
                   return
                   ;;
               *)
                   echo "Invalid action."
                   ;;
           esac
       done

       if [ $player_health -le 0 ]; then
           echo "You have been defeated."
       else
           echo "You defeated the enemy!"
       fi
   }
   ```

### Step 4: Polish and Expand

1. **Enhance User Interface:**
   Improve the display and user interface to make the game more visually appealing. Use ASCII art for maps and objects.

2. **Add More Interactions and Puzzles:**
   Introduce complex puzzles and more interactive elements to keep the game engaging.

3. **Create a Comprehensive Tutorial:**
   Provide a detailed tutorial at the beginning to help new players understand the game mechanics.

4. **Test and Iterate:**
   Continuously test your game and gather feedback. Use this feedback to make iterative improvements.

### Example Directory Structure

```text
bashrun/
├── maps/
│   ├── level1.txt
│   ├── level2.txt
├── scripts/
│   ├── level1.sh
│   ├── level2.sh
│   ├── common.sh  # Contains common functions like inventory and combat
├── resources/
│   ├── ascii_art/
│   ├── items.txt
├── savefile.txt
└── README.md
```

### Example `common.sh`

```bash
#!/bin/bash

# Inventory system
inventory=()

function add_to_inventory {
    inventory+=("$1")
    echo "$1 added to your inventory."
}

function show_inventory {
    echo "Your inventory: ${inventory[@]}"
}

# Combat system
function combat {
    local enemy_health=10
    local player_health=20

    echo "You encounter an enemy!"

    while [ $enemy_health -gt 0 ] && [ $player_health -gt 0 ]; do
        echo "Choose an action: [attack/run]"
        read action
        case $action in
            "attack")
                enemy_health=$((enemy_health - 2))
                player_health=$((player_health - 1))
                echo "You attack the enemy. Enemy health: $enemy_health"
                echo "The enemy attacks you. Your health: $player_health"
                ;;
            "run")
                echo "You run away!"
                return
                ;;
            *)
                echo "Invalid action."
                ;;
        esac
    done

    if [ $player_health -le 0 ]; then
        echo "You have been defeated."
    else
        echo "You defeated the enemy!"
    fi
}

# Save/Load system
function save_game {
    echo "${inventory[@]}" > savefile.txt
    echo "Game saved."
}

function load_game {
    if [ -f savefile.txt ]; then
        inventory=($(cat savefile.txt))
        echo "Game loaded."
    else
        echo "No saved game found."
    fi
}
```

This guide should help you get started with building upon bashrun to create a more advanced and engaging terminal game. Enjoy the process and happy coding!

## 🏆 Quest Completion Validation

### Portfolio Artifacts Created
- [ ] **Enhanced bashrun game** — Working game with multiple levels and features
- [ ] **Inventory system** — Functional item collection and management
- [ ] **Combat system** — Enemy encounter mechanics
- [ ] **Save/load system** — File-based game state persistence

### Skills Demonstrated
- [ ] **Bash Scripting Proficiency** — Functions, variables, control flow, and I/O
- [ ] **Game Design Thinking** — Level progression, mechanics, and player engagement
- [ ] **File System Interaction** — Reading and writing game data
- [ ] **Code Organization** — Modular script structure with reusable functions

## 📚 References & Resources

- [The Spellbook: Bash Cheatsheet](/shell/) - Quick reference for essential commands and scripting techniques.
- [The Grand Grimoire: Complete BASH Reference](/docs/bash-complete-reference/) - Exhaustive guide covering every aspect of GNU Bash.
- [Bash Reference Manual (GNU)](https://www.gnu.org/software/bash/manual/bash.html)
- [Advanced Bash-Scripting Guide (TLDP)](https://tldp.org/LDP/abs/html/)
- [bashrun on GitLab](https://gitlab.com/slackermedia/bashrun)
- [bashcrawl — Learn Bash through a dungeon adventure](https://gitlab.com/slackermedia/bashcrawl)
- [ShellCheck — Shell script linter](https://www.shellcheck.net/)