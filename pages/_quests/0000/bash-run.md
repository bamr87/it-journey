---
title: "bashcrawl and Beyond: Extending a Terminal Dungeon Adventure"
author: IT-Journey Team
description: Starting with bashcrawl as a base and building upon it is a great way to learn advanced shell scripting. bashcrawl uses directories as rooms, text files as scrolls, and executable scripts as interactive items — a brilliant architecture for learning and expanding.
excerpt: Starting with bashcrawl as a base and building upon it is a great way to learn advanced shell scripting. bashcrawl uses directories as rooms, text files as scrolls, and executable scripts as interactive items — a brilliant architecture for learning and expanding.
snippet: Transform basic shell commands into an interactive gaming experience
preview: images/previews/bashrun-and-beyond-building-an-advanced-terminal-g.png
date: 2024-05-29T10:39:06.000Z
lastmod: 2026-03-21T20:13:00.576Z
level: "0000"
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
    - Add a new room with a scroll and interactive treasure to bashcrawl
    - Create a hidden room mechanic using dot-prefixed directories
    - Demonstrate understanding of bashcrawl patterns (env vars, executables, shared functions)
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
sub-title: "Level 000 Quest: Extending bashcrawl's Terminal Dungeon"
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
*Greetings, aspiring script mage! In this side quest, you will study how [bashcrawl](https://github.com/bamr87/bashcrawl) is built and then extend it with new rooms, encounters, and game mechanics. bashcrawl is an elegant dungeon crawler that uses the file system itself as the game world — directories are rooms, text files are scrolls, and executable scripts are interactive items. By the end, you will have forged your own additions to this adventure.*

## 🎯 Quest Objectives

### Primary Objectives (Required for Quest Completion)
- [ ] **Clone and explore the bashcrawl repository** — Understand how directories, scrolls, and executables form the game
- [ ] **Add a new room with a scroll and treasure** — Extend the dungeon with your own content
- [ ] **Create an interactive encounter script** — Build an executable item using `read`, `case`, and environment variables
- [ ] **Implement a hidden room mechanic** — Use dot-prefixed directories to create discoverable secrets

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

Bashcrawl is a terminal adventure game where **the file system is the game world**. Instead of a traditional game engine, it uses a brilliant architecture built entirely from standard Unix concepts:

- **Directories = Rooms** — Players navigate with `cd`
- **Text files (`scroll`) = Knowledge** — Players read with `cat`
- **Executable scripts (`treasure`, `potion`, `statue`) = Interactive items** — Players run with `./`
- **Environment variables (`$I`, `$HP`) = Player state** — Inventory and health persist in the shell session
- **Hidden directories (`.chapel`, `.vault`, `.rift`) = Secret areas** — Discoverable with `ls -a`

Here's a step-by-step guide to understanding bashcrawl's design and building upon it.

### Step 1: Setting Up bashcrawl

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/bamr87/bashcrawl.git
   cd bashcrawl
   ```

2. **Run the Setup and Start Playing:**
   ```bash
   ./setup.sh       # One-time setup: sets permissions, creates game state
   ./main.sh        # Launch the game (multiple modes available)
   ```

   > **Tip**: Before modifying anything, play through the game first! Navigate with `cd`, read scrolls with `cat scroll`, and run items with `./treasure`. Understanding the player experience is essential before extending it.

3. **Understand the Architecture:**

   The game world lives inside the `entrance/` directory. Each subdirectory is a room:

   ```text
   bashcrawl/
   ├── entrance/                # The starting room
   │   ├── scroll               # Text file — read with `cat scroll`
   │   ├── .functions            # Shared game functions (gameover, etc.)
   │   ├── cellar/               # A visible room — enter with `cd cellar`
   │   │   ├── scroll            # Teaches `ls -F` and aliases
   │   │   ├── treasure*         # Executable — run with `./treasure`
   │   │   └── armoury/          # Deeper room
   │   │       ├── scroll        # Teaches chmod and executables
   │   │       ├── treasure*     # Collects a sword into $I
   │   │       ├── potion*       # Interactive — sets $HP variable
   │   │       ├── chamber/      # Deepest standard room
   │   │       │   ├── scroll    # Teaches environment variables
   │   │       │   ├── statue*   # Combat encounter using $HP and $I
   │   │       │   ├── spell*    # Creates shell aliases
   │   │       │   └── treasure* # Collects diamonds
   │   │       └── workshop/     # Teaches mkdir and touch
   │   ├── .chapel/              # Hidden room — revealed by treasure scripts
   │   ├── .vault/               # Hidden room — revealed by treasure scripts
   │   ├── .scrap/               # Hidden room — revealed by treasure scripts
   │   └── .rift/                # Hidden advanced area
   │       ├── scroll            # Teaches pipes, chaining, and find
   │       ├── arena/            # Combat challenges
   │       └── spire/            # Advanced puzzles
   ├── lib/                      # Game engine support scripts
   │   ├── state.sh              # JSON save/load system
   │   ├── quests.sh             # Quest progression and tracking
   │   ├── colors.sh             # Terminal color constants
   │   └── config.sh             # Game configuration
   ├── setup.sh                  # One-time installation script
   ├── main.sh                   # Game launcher (multiple modes)
   └── help.sh                   # Help system
   ```

### Step 2: Understanding bashcrawl's Core Patterns

Before adding new content, study the patterns bashcrawl uses:

1. **How Rooms Work — Directories with Scrolls:**

   Every room is a directory containing a `scroll` (plain text file) that teaches a command:

   ```text
   entrance/scroll        → Teaches ls, cd, pwd, cat
   entrance/cellar/scroll → Teaches ls -F and aliases
   entrance/cellar/armoury/scroll → Teaches chmod and ./execution
   ```

   The scroll format uses ASCII box-drawing for section headers:
   ```text
   ################################################################################
   #                  🗡️  THE GRAND ARMOURY                                      #
   ################################################################################

   ANCIENT WISDOM: The Art of Execution
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   [Educational content about the command being taught...]
   ```

2. **How Inventory Works — Environment Variables:**

   bashcrawl uses shell environment variables instead of files for player state:

   ```bash
   # Inventory is stored in the $I variable (comma-separated)
   export I=amulet,$I      # Collecting treasure adds to $I
   echo $I                  # Check what you're carrying

   # Health points in $HP
   export HP=15             # Set by drinking a potion
   let "HP=HP-5"            # Damage from combat encounters
   echo $HP                 # Check your health
   ```

   This is a teaching tool — players learn `export`, `echo`, `let`, and variable expansion by playing the game.

3. **How Items Work — Executable Scripts:**

   Interactive items are bash scripts marked executable. Here's how the `cellar/treasure` works:

   ```bash
   #!/usr/bin/env bash
   # Check if player already has the amulet
   if ! grep --only-matching amulet <<< $I &> /dev/null; then
       cat << EOF
   You have found an emerald **amulet**!

   To collect treasure, create an inventory variable:

   export I=amulet,\$I
   EOF
       # Reveal hidden rooms when treasure is collected!
       mv ../.chapel ../chapel 2>/dev/null
       mv ../.vault ../vault 2>/dev/null
       mv ../.scrap ../scrap 2>/dev/null
   else
       echo "This treasure has already been taken."
   fi
   ```

   Key patterns:
   - Uses `grep` on `$I` to check if the item was already collected
   - Teaches the player the `export` command to collect the item
   - Uses `mv` to rename hidden dot-directories into visible ones, unlocking new areas

4. **How Combat Works — The Statue Encounter:**

   The `chamber/statue` script demonstrates interactive combat:

   ```bash
   #!/usr/bin/env bash
   # Import shared functions (gameover, etc.)
   FUNCTIONS="$(pwd)"
   FUNCTIONS="${FUNCTIONS%entrance*}entrance/.functions"
   . "$FUNCTIONS"

   cat << EOF
   A rugged statue stands in the corner of the room.
   EOF
   printf "Do you approach it? y/n  "
   read RESP

   if [ "$RESP" = "y" -o "$RESP" = "Y" ]; then
       let "HP=HP-5"           # Deals 5 damage
       if [ "$HP" -le 0 ]; then
           echo "You have been slain by the statue."
           gameover             # Calls shared function
           exit 1
       fi
       # Check if player has a sword in inventory
       if grep --quiet --only-matching 'sword' <<< "$I"; then
           echo "You strike the statue and it breaks to pieces!"
       else
           echo "You have no weapon to fight with!"
       fi
   fi
   ```

5. **Shared Functions — The `.functions` File:**

   The `entrance/.functions` file defines reusable game mechanics:

   ```bash
   # The gameover function creates a lootable corpse file
   gameover () {
       CORPSE="$(mktemp corpse.XXX)"
       # Write the corpse as an executable script containing
       # the dead player's inventory
       cat << EOF2 > "$CORPSE"
   #!/bin/bash
   echo "You see the corpse of a slain adventurer."
   echo "You find: ${I}"
   EOF2
       chmod +x "$CORPSE"
       echo "Your adventure has come to an end."
   }
   ```

   This is sourced with `. "$FUNCTIONS"` from encounter scripts that need it.

### Step 3: Adding Your Own Room

Now that you understand the patterns, create a new room:

1. **Create the room directory and scroll:**
   ```bash
   cd entrance/cellar/armoury
   mkdir library
   ```

2. **Write a scroll that teaches a new command** (e.g., `grep`):
   ```bash
   cat > library/scroll << 'SCROLL'
   ################################################################################
   #                  📚 THE ARCANE LIBRARY                                        #
   ################################################################################

   ANCIENT WISDOM: Searching Through Knowledge
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   Dusty shelves line the walls, filled with countless tomes.
   The sheer volume of knowledge is overwhelming — but the
   grep spell can search through text to find what you need.

   COMMAND            PURPOSE
   --------           --------
   grep word file     Search for "word" inside a file
   grep -i word file  Case-insensitive search
   grep -r word .     Search all files in current directory

   Try searching this very scroll:

       grep "spell" scroll

   A mysterious tome sits on a pedestal.  Examine it with:

       cat tome
   SCROLL
   ```

3. **Add a readable item:**
   ```bash
   cat > library/tome << 'TOME'
   The Tome of Pattern Matching
   ============================

   To find lines that do NOT contain a word:

       grep -v "word" file

   To count how many lines match:

       grep -c "word" file

   To show line numbers:

       grep -n "word" file

   A treasure chest sits in the corner of the library...
   TOME
   ```

4. **Create a treasure script:**
   ```bash
   cat > library/treasure << 'TREASURE'
   #!/usr/bin/env bash
   if ! grep --only-matching "tome" <<< $I &> /dev/null; then
       cat << EOF
   You found an ancient **tome** of knowledge!

   Add it to your inventory:

       export I=tome,\$I

   EOF
   else
       echo "You have already claimed this treasure."
   fi
   TREASURE
   chmod +x library/treasure
   ```

### Step 4: Adding a Hidden Room

bashcrawl's cleverest mechanic is hidden rooms — directories prefixed with `.` (dot) that are invisible to plain `ls` but revealed by `ls -a`. Some treasure scripts unlock hidden rooms by renaming them:

```bash
# Inside a treasure script, reveal a hidden room:
mv ../.secret-chamber ../secret-chamber 2>/dev/null
```

Create your own hidden area:

```bash
# Create the hidden room (dot-prefix makes it invisible to `ls`)
mkdir entrance/cellar/armoury/library/.study

cat > entrance/cellar/armoury/library/.study/scroll << 'SCROLL'
################################################################################
#                  🔮 THE HIDDEN STUDY                                         #
################################################################################

You found a secret chamber behind a bookshelf!

Here, ancient mages practiced the art of REDIRECTION
— channeling the output of spells into files.

COMMAND              PURPOSE
--------             --------
echo "text" > file   Write text to a file (overwrites)
echo "text" >> file  Append text to a file
cat file1 file2      Combine files together

Try creating a note:

    echo "I was here" > note.txt
    cat note.txt
SCROLL
```

Then update your library treasure to reveal it:
```bash
# Add this line inside library/treasure, after the export instruction:
echo ""
echo "You hear stone grinding... a hidden passage has opened!"
mv ../.study ../study 2>/dev/null
```

### Step 5: Adding a Combat Encounter

Create an encounter that checks player state:

```bash
cat > entrance/cellar/armoury/library/guardian << 'GUARDIAN'
#!/usr/bin/env bash

# Import shared functions
FUNCTIONS="$(pwd)"
FUNCTIONS="${FUNCTIONS%entrance*}entrance/.functions"
. "$FUNCTIONS"

if [ -f .guardian_defeated ]; then
    echo "The guardian has already been vanquished."
    exit 0
fi

cat << EOF
A spectral guardian materializes before you!

"Only those who carry the tome may pass," it whispers.
EOF

if grep --quiet --only-matching 'tome' <<< "$I"; then
    cat << EOF

The guardian recognizes the tome and bows.
"You are worthy. Pass in peace."

The guardian fades, leaving behind a magic ring.

    export I=ring,\$I

EOF
    touch .guardian_defeated
else
    cat << EOF

The guardian strikes you for 5 damage!

    let "HP=HP-5"

You should find the tome first before facing this guardian.
EOF
fi
GUARDIAN
chmod +x entrance/cellar/armoury/library/guardian
```

### Step 6: The Quest System and Save State

bashcrawl includes a quest tracking system (`lib/quests.sh`) and JSON-based save/load (`lib/state.sh`):

- **Quest progression** tracks which commands the player has used (`pwd`, `ls`, `cd`, `cat`, `mkdir`, `touch`, `grep`, `source`)
- **State persistence** saves inventory, HP, location, XP, and completed quests to `.bashcrawl_save.json`
- **Multiple game modes**: Interactive emulator (safe sandbox), Native terminal (real shell), Tutorial mode, and Agent mode (for AI playtesters)

Study these files to understand how to integrate your new rooms into the broader game:

```bash
# Read the quest system
cat lib/quests.sh

# Read the state management
cat lib/state.sh

# Check the current save file
cat .bashcrawl_save.json
```

## 🏆 Quest Completion Validation

### Portfolio Artifacts Created
- [ ] **New dungeon room** — A directory with scroll, treasure, and optional encounters
- [ ] **Interactive encounter** — An executable script using `read`, `case`, and `$I`/`$HP`
- [ ] **Hidden room mechanic** — A dot-prefixed directory revealed by a game event
- [ ] **Extended game content** — Your additions integrate cleanly with the existing dungeon

### Skills Demonstrated
- [ ] **Bash Scripting Proficiency** — Functions, variables, `read`, `case`, heredocs, and `grep`
- [ ] **File System as Architecture** — Using directories, files, and permissions as game design
- [ ] **Environment Variables** — Using `export`, `echo`, `let` for persistent player state
- [ ] **Code Organization** — Sourcing shared functions, modular script structure

## 📚 References & Resources

- [The Spellbook: Bash Cheatsheet](/shell/) - Quick reference for essential commands and scripting techniques.
- [The Grand Grimoire: Complete BASH Reference](/docs/bash-complete-reference/) - Exhaustive guide covering every aspect of GNU Bash.
- [bashcrawl on GitHub](https://github.com/bamr87/bashcrawl) — The game repository this quest is based on
- [Bash Reference Manual (GNU)](https://www.gnu.org/software/bash/manual/bash.html)
- [Advanced Bash-Scripting Guide (TLDP)](https://tldp.org/LDP/abs/html/)
- [ShellCheck — Shell script linter](https://www.shellcheck.net/)