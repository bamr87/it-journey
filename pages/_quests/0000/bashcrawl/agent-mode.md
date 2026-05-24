---
title: 'Bashcrawl Agent Mode: AI Automation and Contribution'
description: Explore Bashcrawl's Agent Mode for AI playtesting, screenshot capture, batch automation, and upstream contribution. The capstone quest for dungeon masters.
date: '2026-05-22T00:00:00.000Z'
lastmod: '2026-05-23T02:30:23.000Z'
author: IT-Journey Team
level: '0000'
fmContentType: quest
quest_type: side_quest
quest_series: Bashcrawl Adventure Path
quest_arc: Terminal Mastery Arc
quest_line: Foundation Path
difficulty: 🔴 Hard
estimated_time: 45-60 minutes
primary_technology: bash
skill_focus: devops
learning_style: hands-on
categories:
- Quests
- Terminal
- Bashcrawl
tags:
- bashcrawl
- terminal
- bash
- automation
- ai
- contribution
- '0000'
keywords:
  primary:
  - bashcrawl agent mode
  - bash automation
  - ai playtest
  - screenshot automation
  secondary:
  - open source contribution
  - bash scripting advanced
  - dungeon automation
quest_dependencies:
  required_quests:
  - /quests/0000/side-quests/rift/
  unlocks_quests: []
quest_relationships:
  parent_quest: /quests/0000/bashcrawl/
  sequel_quests: []
validation_criteria:
- Launch Bashcrawl in agent mode
- Capture a screenshot sequence to a directory
- Write a batch command file and run it
- Use --status to report dungeon completion
- Fork and make a contribution (optional)
prerequisites:
- Complete the Rift side-quest
learning_paths:
- Terminal Mastery Path
- Open Source Contribution Path
rewards:
- Dungeon Master Badge
- Bashcrawl automation mastery
excerpt: Automate Bashcrawl runs with agent mode, scripted commands, screenshot capture, and an optional open-source contribution finale.
draft: false
permalink: /quests/0000/side-quests/agent-mode/
layout: quest
---
*You have conquered the Rift. But the dungeon holds one final secret — a mode where an AI plays alongside you, a mode where you automate the entire journey, a mode where you become the dungeon master. Welcome to Agent Mode.*

## 🎯 Quest Objectives

- [ ] Launch Bashcrawl using `./main.sh --agent`
- [ ] Capture a walkthrough screenshot sequence to a directory
- [ ] Create and run a batch command file with `--batch`
- [ ] Use `--status` to generate a dungeon completion report
- [ ] (Optional) Fork the upstream repo and submit an improvement

## �️ Quest Prerequisites

- All 9 dungeon areas explored
- Comfortable with shell scripting and pipes
- (Optional) GitHub account for contribution track

## ⚡ Command Reference

| Mode | What It Does |
|------|-------------|
| `./main.sh --agent` | AI playtesting mode — AI navigates autonomously |
| `./main.sh --agent-bash` | Agent mode in classic bash-only interface |
| `./main.sh --batch commands.txt` | Execute a list of commands from a file |
| `./main.sh --command "cmd"` | Run a single command inside the dungeon |
| `./main.sh --screenshot-dir ./shots/` | Capture terminal screenshots while playing |
| `./main.sh --status` | Print dungeon completion status |
| `./main.sh --demo` | Run the built-in demo walkthrough |
| `./main.sh --reset` | Reset the dungeon to initial state |

Or use the IT-Journey launcher from the hub directory:

```bash
./bash_crawl.sh agent    # Launches --agent mode
./bash_crawl.sh tutorial # Launches --tutorial mode
```

## 🤖 Walkthrough

### Part 1 — Watch the AI play

```bash
cd bashcrawl
./main.sh --agent
```

The Textual TUI launches. An AI agent (powered by `llm` if installed, otherwise heuristic-based) navigates the dungeon:

- Reads each room description
- Executes appropriate commands
- Collects items
- Defeats bosses

Watch to see if the AI takes different paths than you did. Note: the AI makes mistakes too.

**Exit at any point:** `Ctrl+C` or type `quit`.

### Part 2 — Screenshot capture for teaching

```bash
mkdir -p ./walkthrough_screenshots

./main.sh --screenshot-dir ./walkthrough_screenshots --classic
# Play through the dungeon normally
# Screenshots auto-saved at each room

ls ./walkthrough_screenshots/
# entrance_01.png  workshop_01.png  cellar_01.png  ...
```

This is the fastest way to create tutorial screenshots for blog posts, slide decks, or wiki contributions.

### Part 3 — Batch automation

Create a file of commands to execute automatically:

```bash
cat > my_walkthrough.txt << 'EOF'
ls
cat scroll
cd ENTRANCE
ls -F
cat quest
cd WORKSHOP
ls -F
mkdir backpack
touch map.txt
echo "Items: sword, potion" > map.txt
cat map.txt
EOF

./main.sh --batch my_walkthrough.txt
```

Batch mode is ideal for:
- Regression testing after dungeon changes
- Creating automated demo videos
- Scripted teaching demonstrations

### Part 4 — Status report

```bash
./main.sh --status
```

Output example:

```text
Bashcrawl Status
================
Version: 3.0.0
Areas Explored: 9/9 (100%)
Items Collected: sword, potion, emerald_amulet, stone_key, tome, vault_key, crystal
Bosses Defeated: guardian, monster, ghost, pit_boss, satellite_boss, statue
Completion: DUNGEON CLEARED ✓
```

Pipe it to a file:

```bash
./main.sh --status > my_completion.txt
cat my_completion.txt
```

### Part 5 — Demo mode walkthrough

```bash
./main.sh --demo
```

Demo mode runs a curated, annotated walkthrough that explains each command while executing it. Use this to:
- Onboard new players
- Refresh memory on commands
- Create tutorial material

### Part 6 (Optional) — Contributing upstream

The upstream Bashcrawl repo is open source and welcomes contributions:

```bash
# Fork on GitHub then:
git clone https://github.com/YOUR_USERNAME/bashcrawl.git
cd bashcrawl

git checkout -b feature/my-improvement

# Make changes (new rooms, better documentation, bug fixes)
# Example: add a new combat command
echo 'cast_spell() { echo "You cast $1!"; }' >> lib/combat.sh

git add .
git commit -m "feat(combat): add cast_spell helper function"
git push origin feature/my-improvement
# Open a Pull Request on GitHub
```

Ideas for contributions:
- New dungeon rooms or branches
- Better error messages
- Translations
- Windows/PowerShell compatibility
- New agent strategies

## 💡 Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `--agent` fails | `llm` not installed | Install: `pip install llm` |
| Screenshots are blank | Terminal not supported | Try `--classic` mode with `--screenshot-dir` |
| Batch file hangs | A command waiting for input | Add `\n` for interactive prompts or use non-interactive commands |
| `--status` shows incomplete | Some area not fully explored | Check `map` inside the game |

## ✅ Validation

- [ ] You watched the AI agent navigate at least 3 rooms
- [ ] You captured at least 5 screenshots to a directory
- [ ] You created a batch file and ran it successfully
- [ ] `--status` shows all areas explored
- [ ] (Optional) You submitted or drafted a contribution

## 🏆 Dungeon Master Certificate

Complete all 10 side-quests and you have earned the right to call yourself a Bashcrawl Dungeon Master:

| Badge | Criteria |
|-------|----------|
| 🏰 Explorer | All 9 chambers explored |
| ⚔️ Combatant | All bosses defeated |
| 📚 Scholar | All man pages consulted |
| 🤖 Automator | Batch file run successfully |
| 🌐 Contributor | Pull request submitted upstream |

## ➡️ What's Next?

- **Share your completion** → Post in the IT-Journey Discussions
- **Teach others** → Use your screenshots to write a blog post
- **Advanced Shell** → Try `awk`, `sed`, `find`, `xargs` quests at level 0001
- **Back to hub** → [Bashcrawl Hub](/quests/0000/bashcrawl/)

---

## 📚 External Resources

Continue your terminal adventure with these resources:

- [Bashcrawl Web Demo](https://bamr87.github.io/bashcrawl/) — Play in your browser, no installation required
- [Bashcrawl on GitHub](https://github.com/bamr87/bashcrawl) — Source code, setup, and open contributions
- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/) — Official Bash reference for every master wizard
- [IT-Journey Bashcrawl Hub](/quests/0000/bashcrawl/) — Full quest series and walkthroughs
- [GitHub CLI Documentation](https://cli.github.com/manual/) — Become a hero contributor

---

*The dungeon is complete. The AI learned. The bash shell is your wand. Go forth and automate.* 🤖🏰✨

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0000 - Foundation & Init World]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Bashcrawl Rift: Pipes, Redirection, and the Final Boss]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]

