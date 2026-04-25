---
title: Terminal and Bash Learning Path
description: A complete guide to learning the terminal, Bash commands, Bash scripting, and Bashcrawl through IT-Journey quests, notes, and references.
date: 2026-04-25T00:00:00.000Z
lastmod: 2026-04-25T19:27:00.159Z
author: IT-Journey Team
permalink: /docs/terminal/
tags:
    - terminal
    - bash
    - bashcrawl
    - command-line
    - learning-path
    - reference
categories:
    - Documentation
    - Terminal
    - Learning Path
keywords:
    primary:
        - terminal learning path
        - bash learning path
        - bashcrawl guide
    secondary:
        - command line beginner guide
        - bash scripting resources
        - terminal quests
excerpt: Start with Bashcrawl online, build terminal fundamentals, use the Bash reference and cheatsheet, then write and extend real Bash scripts.
draft: false
sidebar:
    nav: docs
toc: true
toc_sticky: true
---

# Terminal and Bash Learning Path

This guide connects the terminal, Bash, command references, and Bashcrawl into one learner journey. Start in the browser, practice real commands, then move into local scripting when you are ready.

## Recommended Route

| Stage | Resource | Outcome |
|-------|----------|---------|
| 1 | [Play Bashcrawl Online](https://bamr87.github.io/bashcrawl/) | Try `pwd`, `ls`, `cd`, and `cat` without installing anything |
| 2 | [Terminal Fundamentals](/quests/level-0000-terminal-fundamentals/) | Learn navigation, files, pipes, redirection, and search |
| 3 | [Bashcrawl Terminal Adventure](/quests/bashcrawl-terminal-adventure/) | Turn command practice into a guided quest checklist |
| 4 | [Terminal Shortcuts Cheat Sheet](/docs/terminal-shortcuts-cheat-sheet/) | Build speed with history, completion, clearing, and editing shortcuts |
| 5 | [Bash Cheatsheet](/shell/) | Keep everyday commands and syntax close while practicing |
| 6 | [Complete BASH Reference](/docs/bash-complete-reference/) | Deepen your understanding of Bash built-ins, expansions, scripts, and patterns |
| 7 | [Bash Scripting Mastery](/quests/0010/bash-scripting/) | Write reusable scripts with functions, validation, error handling, and tests |
| 8 | [Bash-run Extension Quest](/quests/lvl_000/bash-run/) | Clone Bashcrawl and extend a real terminal learning game |

## Bashcrawl Paths

| Path | Use When | Link or Command |
|------|----------|-----------------|
| Online Web TUI | You are new, in a classroom, or on a locked-down machine | [bamr87.github.io/bashcrawl](https://bamr87.github.io/bashcrawl/) |
| Local interactive mode | You want the full local TUI | `./main.sh --interactive` |
| Classic mode | You want a pure Bash fallback | `./main.sh --classic` |
| Native terminal mode | You want the traditional filesystem adventure | `./main.sh --native` |
| Tutorial mode | You want guided onboarding | `./main.sh --tutorial` |
| Agent mode | You are testing, scripting, or capturing screenshots | `./main.sh --agent` |

Local setup uses the current IT-Journey Bashcrawl repository:

```bash
git clone https://github.com/bamr87/bashcrawl.git
cd bashcrawl
./setup.sh
./main.sh --interactive
```

## Command Practice Map

| Command | Practice in Bashcrawl | Reference |
|---------|-----------------------|-----------|
| `pwd` | Confirm your current room | [Terminal Fundamentals](/quests/level-0000-terminal-fundamentals/) |
| `ls -F` | Identify rooms, scrolls, and executable encounters | [Bashcrawl Quest](/quests/bashcrawl-terminal-adventure/) |
| `cat scroll` | Read room instructions and lore | [Bash Cheatsheet](/shell/) |
| `cd cellar` | Move through the dungeon | [Complete BASH Reference](/docs/bash-complete-reference/) |
| `less`, `head`, `tail` | Inspect longer scrolls and logs | [Terminal Shortcuts](/docs/terminal-shortcuts-cheat-sheet/) |
| `grep` | Search scrolls and code for clues | [Bash Scripting](/quests/0010/bash-scripting/) |

## For Different Learners

| Learner | Best First Step | Next Step |
|---------|-----------------|-----------|
| Absolute beginner | [Play online](https://bamr87.github.io/bashcrawl/) | [Terminal Fundamentals](/quests/level-0000-terminal-fundamentals/) |
| Finance or operations learner | [Finance terminal guide](/posts/terminal-bash-finance-accounting/) | [Bash Scripting Mastery](/quests/0010/bash-scripting/) |
| Developer or contributor | [Bashcrawl GitHub repo](https://github.com/bamr87/bashcrawl/) | [Bash-run Extension Quest](/quests/lvl_000/bash-run/) |
| Teacher or mentor | [Bashcrawl Web](https://bamr87.github.io/bashcrawl/) | [Bashcrawl Terminal Adventure](/quests/bashcrawl-terminal-adventure/) |

## Reference Shelf

- [Play Bashcrawl Online](https://bamr87.github.io/bashcrawl/) - No-install browser game with local browser saves.
- [Bashcrawl Repository](https://github.com/bamr87/bashcrawl/) - Current comprehensive repo with TUI, static web, agent, and tests.
- [Original Bashcrawl Upstream](https://gitlab.com/slackermedia/bashcrawl) - Historical upstream project.
- [Terminal Fundamentals](/quests/level-0000-terminal-fundamentals/) - Foundation command-line quest.
- [Bashcrawl Terminal Adventure](/quests/bashcrawl-terminal-adventure/) - Gamified Bashcrawl quest.
- [Bash-run Extension Quest](/quests/lvl_000/bash-run/) - Extend Bashcrawl locally.
- [Bash Scripting Mastery](/quests/0010/bash-scripting/) - Script automation quest.
- [Bash Cheatsheet](/shell/) - Quick command and syntax notes.
- [Complete BASH Reference](/docs/bash-complete-reference/) - Deep reference guide.
- [Terminal Shortcuts Cheat Sheet](/docs/terminal-shortcuts-cheat-sheet/) - Keyboard productivity guide.
