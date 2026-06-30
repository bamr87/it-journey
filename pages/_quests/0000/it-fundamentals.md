---
title: 'IT Fundamentals: Your Digital Awakening Quest'
author: IT-Journey Team
description: 'Build core IT skills hands-on: file management, operating systems, networking basics, scripting, cloud, containers, and Git version control.'
excerpt: Learn the core principles of IT infrastructure, networking, and computing
preview: images/previews/it-fundamentals.png
date: '2023-11-25T14:12:43.000Z'
lastmod: '2025-11-29T21:40:00.000Z'
level: '0000'
difficulty: 🟢 Easy
estimated_time: 60-90 minutes
primary_technology: fundamentals
quest_type: main_quest
quest_series: Level 0000 Quest Line
quest_line: Foundation Path
quest_arc: Digital Awakening Arc
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/0000/hello-noob/
  - /quests/0000/begin-your-it-journey/
  unlocks_quests:
  - /quests/0000/os-selection/
skill_focus: fullstack
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Basic computer operation (turning on, using mouse and keyboard)
  - Familiarity with using a web browser
  system_requirements:
  - Computer with internet access
  - Any operating system (Windows, macOS, or Linux)
  skill_level_indicators:
  - Absolute beginner with curiosity about how computers work
validation_criteria:
  completion_requirements:
  - Complete all 9 hands-on exercises
  - Demonstrate understanding of basic networking concepts
  - Successfully run basic commands on your operating system
  skill_demonstrations:
  - Can explain what an IP address and DNS are
  - Can navigate the file system and organize files
  knowledge_checks:
  - Understands the role of operating systems
  - Can describe the basics of networking (IP, DNS, DHCP)
rewards:
  badges:
  - 🏆 IT Foundations Badge
  - ⚡ Digital Literacy Achievement
  skills_unlocked:
  - 🛠️ Computer Architecture Awareness
  - 🎯 Networking Fundamentals
  progression_points: 75
  unlocks_features:
  - Access to OS Selection quest
  - Foundation for all technical quests
permalink: /quests/0000/it-fundamentals/
categories: []
tags:
- fundamentals
- it-basics
- '0000'
keywords:
  primary:
  - fundamentals
  secondary:
  - it-basics
  - '0000'
fmContentType: quest
draft: false
slug: fundamentals
layout: quest
---
*Welcome, aspiring IT adventurer! Before you can cast your first spells or build grand digital fortresses, you must understand the fundamental building blocks of the IT realm. This quest covers the essential skills every technology professional needs — from organizing files to understanding networks and cloud computing.*

## 🎯 Quest Objectives

### Primary Objectives (Required for Quest Completion)
- [ ] **Master Basic Computer Skills** — Organize files and navigate your operating system
- [ ] **Understand OS Fundamentals** — Explore system tools and practice basic commands
- [ ] **Learn Networking Basics** — Discover IP addresses, DNS, and home network configuration
- [ ] **Write Your First Script** — Create a simple automation script

### Secondary Objectives (Bonus Achievements)
- [ ] **Set Up a Virtual Machine** — Install a Linux VM using VirtualBox
- [ ] **Explore Cloud Computing** — Create a free cloud account and deploy a Hello World app
- [ ] **Create a Docker Container** — Pull and run your first container image
- [ ] **Configure Version Control** — Install Git and practice basic commands

### Mastery Indicators
- [ ] Can explain what an IP address, DNS, and DHCP do
- [ ] Can navigate the file system using command-line tools
- [ ] Can write a basic script to automate a simple task
- [ ] Understands the basics of virtualization and containers

## 🗺️ Quest Prerequisites

*Every adventurer must pack the right supplies before setting out. Gather these before you begin so no exercise leaves you stranded:*

- **A modern operating system** — Windows 10/11, macOS, or a Linux distribution. Any of them works for this quest.
- **Internet access** — for downloading tools, reaching cloud platforms, and a couple of online exercises.
- **Administrator / install rights** — you'll install Python, Git, VirtualBox, and Docker, which require permission to install software on your machine.
- **~20 GB free disk space** — the Linux virtual machine and container images need room to live (the VM alone can take 10+ GB).

> 🧭 **No admin rights?** If you're on a locked-down school or work computer, you can still complete the file-management, networking-exploration, and Python exercises. Save the VM and Docker secondary objectives for a machine you fully control.

---

Absolutely! Hands-on exercises are like spells and incantations – they're best learned by doing. Let's start with some foundational IT skills and practical exercises to get you going:

### 1. **Basic Computer Skills**

- **Exercise**: Organize your files and folders.
  - Create a new folder structure on your computer.
  - Organize your documents, images, and other files into these folders.
  - **Prefer the terminal?** On macOS or Linux, conjure the whole structure in one command:

    ```bash
    mkdir -p ~/projects/my-quest/{docs,scripts,images}
    ```

    This creates `my-quest` with three sub-folders in one stroke (`-p` makes parent folders as needed; the `{...}` brace expansion creates all three at once). Verify it with `ls ~/projects/my-quest`.

### 2. **Operating Systems (OS) Basics**

- **Exercise for Windows**: Learn to navigate the Control Panel and Task Manager.
  - Explore different settings in the Control Panel.
  - Open the Task Manager and familiarize yourself with different tabs like Processes, Performance, and Services.
- **Exercise for Linux**: Install a Linux distribution (like Ubuntu) on a virtual machine.
  - Use software like VirtualBox to create a virtual machine.
  - Download the Ubuntu ISO and install it on your virtual machine.
  - Practice basic Linux commands: `pwd`, `ls`, `cd`, `mkdir`, `rm`.

  > ⚠️ **Handle `rm` with care.** Unlike dragging a file to the trash, `rm` permanently deletes files — there is **no recycle bin** and no undo. Practice on throwaway files you created (like a test folder), and use `rm -i` to make the shell ask for confirmation before each deletion. Never run `rm -rf` on a path you don't fully understand.

### 3. **Networking Fundamentals**

- **Exercise**: Explore your home network.
  - Find out your computer’s IP address and default gateway. Open your terminal and run the command for your realm:

    **Windows** (Command Prompt or PowerShell) — your IPv4 address is the `IPv4 Address` line; the gateway is `Default Gateway`:

    ```powershell
    ipconfig
    ```

    **Linux** — the first command lists your addresses; the second shows the gateway (the IP after `default via`):

    ```bash
    ip addr show
    ip route show
    ```

    **macOS** — `ifconfig` lists everything; the shortcut prints just your Wi‑Fi IP, and `route` reveals the gateway:

    ```bash
    ipconfig getifaddr en0
    ifconfig
    netstat -nr | grep default
    ```

  - Log into your router’s admin page by typing the default gateway IP (for example `192.168.1.1`) into your browser’s address bar.
  - Explore settings and understand terms like DHCP, DNS, and NAT.

### 4. **Basic Programming with Python**

- **Exercise**: Write a simple Python script.
  - Install Python on your computer (download from [python.org](https://www.python.org/downloads/) and check the box to add Python to your PATH on Windows).
  - Verify the install by running `python --version` (or `python3 --version` on macOS/Linux) in your terminal.
  - Write a script that takes user input and prints a personalized greeting. Save this as `greet.py`:

    ```python
    name = input("What is your name, adventurer? ")
    print(f"Welcome to the IT realm, {name}! 🧙")
    ```

    Run it with `python greet.py` (or `python3 greet.py`).

- **Bonus — explore a library**: Fetch the current weather using a public endpoint that needs **no API key or sign-up**. First install the `requests` library:

  ```bash
  pip install requests
  ```

  On macOS or Linux, use `pip3` (or invoke pip through the interpreter to be sure you're installing into the right Python):

  ```bash
  pip3 install requests
  python3 -m pip install requests
  ```

  Then save this as `weather.py` and run it with `python weather.py`:

  ```python
  import requests

  # wttr.in is a free weather service — no API key required.
  # "?format=3" returns one short line, e.g. "London: ⛅️ +15°C"
  response = requests.get("https://wttr.in/?format=3")
  print(response.text)
  ```

  Try changing the URL to `https://wttr.in/Tokyo?format=3` to check another city. You've just made your first program talk to the internet! 🌦️

### 5. **Scripting and Automation**

- **Exercise for Windows**: Write a basic Batch script.
  - Open Notepad, paste the script below, and save it as `hello.bat` (choose "All Files" as the file type so it doesn't become `hello.bat.txt`). Double-click the file, or run it from Command Prompt with `hello.bat`.

    ```batch
    @echo off
    echo Hello from your first Batch script!
    echo The current date and time is: %date% %time%
    echo Files in this folder:
    dir /b
    pause
    ```

- **Exercise for Linux** (also works on macOS): Write a Bash script.
  - First, give your scripts a home and move into it (keeping with the file-organization habit from Exercise 1):

    ```bash
    mkdir -p ~/scripts
    cd ~/scripts
    ```

  - Save the script below as `list_by_size.sh`. Make it runnable with `chmod +x list_by_size.sh`, then run it with `./list_by_size.sh`.

    ```bash
    #!/bin/bash
    echo "Hello from your first Bash script!"
    echo "Files in this directory, largest first:"
    # -l = long listing, -S = sort by size, -h = human-readable sizes
    ls -lSh
    ```

### 6. **Introduction to Cloud Computing**

- **Exercise**: Create a free account on a cloud platform like Google Cloud Platform (GCP) or AWS.
  - Explore the dashboard and familiarize yourself with the interface.
  - Follow a guided "Hello World" quickstart so the cloud stops being abstract. Pick one:
    - **Google Cloud Run** — deploy a sample container with the [Cloud Run quickstart](https://cloud.google.com/run/docs/quickstarts/deploy-container). On your own machine you can start the CLI with `gcloud init` after installing the [gcloud CLI](https://cloud.google.com/sdk/docs/install).
    - **AWS CloudShell** — open a free browser terminal already signed in to your account from the [CloudShell guide](https://docs.aws.amazon.com/cloudshell/latest/userguide/getting-started.html); run `aws --version` to confirm you're talking to AWS.

    > 💡 Both platforms have a free tier, but always check what counts as free before deploying — spinning down resources when you're done keeps your bill at zero.

### 7. **Virtualization and Containers**

- **Exercise**: Create a Docker container.
  - Install Docker on your machine ([Docker Desktop](https://www.docker.com/products/docker-desktop/) is the easiest way on Windows and macOS). Confirm it works with `docker --version`. For a deeper dive later, see the [Frontend Docker quest](/quests/0100/frontend-docker/).
  - **Run your very first container** — this pulls the image and prints a welcome message, then exits:

    ```bash
    docker run hello-world
    ```

  - **Run a real web server** you can visit in your browser. This starts the `nginx` web server and maps it to port 8080 on your computer:

    ```bash
    docker run -d -p 8080:80 --name my-web nginx
    ```

    Now open **<http://localhost:8080>** in your browser — you'll see the nginx welcome page being served from inside the container. 🎉
  - **Stop and clean up** when you're done:

    ```bash
    docker stop my-web
    docker rm my-web
    ```

### 8. **Basic System Security**

- **Exercise**: Install and use an antivirus software.
  - Perform a full system scan.
  - Explore the settings and schedule regular scans.
- **Exercise**: Check your system for pending updates. Outdated software is one of the most common ways attackers break in — patching closes known holes before someone walks through them. See what's waiting to be updated on your realm:

  **Windows** (PowerShell) — list what's upgradable first (review before installing):

  ```powershell
  winget upgrade
  ```

  > ⚠️ `winget upgrade --all` **installs every available upgrade immediately** — it is not a preview. Run plain `winget upgrade` to review the list, then add `--all` only when you're ready to apply them all.

  **Linux** (Debian/Ubuntu) — refresh the package list, then see what can be upgraded:

  ```bash
  sudo apt update
  apt list --upgradable
  ```

  **macOS** — list available system updates:

  ```bash
  softwareupdate -l
  ```

### 9. **Version Control with Git**

- **Exercise**: Set up Git and practice basic commands.
  - Install Git from [git-scm.com/downloads](https://git-scm.com/downloads), then confirm it's ready with `git --version`.
  - Create your first repository and make your first commit. Run these one at a time:

    ```bash
    git config --global user.name "Your Name"
    git config --global user.email "you@example.com"
    git init my-repo
    cd my-repo
    echo "# My first repo" > README.md
    git add .
    git commit -m "first commit"
    ```

    The two `git config` lines set your identity — Git refuses to commit without them on a fresh install. `git init` creates the repo, `git add .` stages your new file, and `git commit` records a snapshot. Run `git log` to see your commit in the project's history. 🎉
  - Clone an existing repository from GitHub and explore its contents:

    ```bash
    git clone https://github.com/bamr87/it-journey.git
    ```

  - **Want to go deeper?** This is just the spark — the dedicated [Git Basics quest](/quests/0000/git-basics/) walks you through version control end-to-end.

These exercises are your first steps. As you complete each one, you'll build a strong foundation in IT. Remember, the key is to practice regularly and keep challenging yourself with more complex tasks as you grow. Happy learning! 🌟💻🔧

## 🏆 Quest Completion Validation

### Portfolio Artifacts Created
- [ ] **Organized File System** — Well-structured folder hierarchy on your computer
- [ ] **First Script** — A working Bash or Batch script that automates a task
- [ ] **Network Notes** — Documentation of your home network configuration

### Skills Demonstrated
- [ ] **File Management** — Creating, organizing, and navigating directories
- [ ] **System Exploration** — Using OS tools like Task Manager or System Monitor
- [ ] **Networking Awareness** — Finding IP addresses and understanding router settings
- [ ] **Scripting Basics** — Writing and executing simple automation scripts

## 📚 References & Resources

- [CompTIA IT Fundamentals Certification](https://www.comptia.org/certifications/it-fundamentals)
- [Cisco Networking Academy — Introduction to Networks](https://www.netacad.com/)
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Docker Getting Started Guide](https://docs.docker.com/get-started/)
- [Git Official Documentation](https://git-scm.com/doc)
- [VirtualBox User Manual](https://www.virtualbox.org/manual/)

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0000 - Foundation & Init World]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Recommended:** [[Hello n00b: Your First Steps into the IT Journey]]
**Unlocks:** [[OS Selection]]
**Sequel quests:** [[OS Selection]]
**Parallel quests:** [[Begin your IT Journey]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]

