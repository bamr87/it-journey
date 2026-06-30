---
title: 'Git Workflow Mastery: Branches, Merging & Team Collaboration'
author: IT-Journey Team
description: 'Master a clean Git workflow: feature branches, focused commits, pull requests, merge vs rebase, and calmly resolving conflicts to collaborate confidently.'
excerpt: Master Git branching strategies, merging techniques, and pull request workflows for effective team collaboration.
preview: images/previews/git-workflow-mastery-branches-merging-quest-desc.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0001'
difficulty: 🟡 Medium
estimated_time: 75-90 minutes
primary_technology: git
quest_type: main_quest
quest_series: Static Site Mastery
quest_line: The Web Fundamentals Codex
quest_arc: Forging Your First Website
quest_dependencies:
  required_quests:
  - /quests/0000/git-basics/
  recommended_quests:
  - /quests/0001/github-pages-basics/
  unlocks_quests:
  - /quests/0001/jekyll-fundamentals/
skill_focus: devops
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Basic Git (init, add, commit, push)
  - Completion of Git Basics
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Git installed and a GitHub account
  skill_level_indicators:
  - Comfortable making and pushing commits
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A feature branch merged via a pull request
  skill_demonstrations:
  - Can create a feature branch and open a PR
  - Can resolve a merge conflict deliberately
  knowledge_checks:
  - Understands the difference between merge and rebase
  - Can read git log and git status to know the repo state
permalink: /quests/0001/git-workflow-mastery/
categories:
- Quests
- DevOps
- Version-Control
- Beginner
tags:
- '0001'
- git
- version-control
- collaboration
- pull-requests
- main_quest
- devops
- hands-on
- beginner
keywords:
  primary:
  - '0001'
  - git
  - version-control
  - collaboration
  secondary:
  - pull-requests
  - main_quest
  - devops
  - hands-on
  - beginner
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0001 (1) Quest: Main Quest - Git Workflow'
rewards:
  badges:
  - 🏆 Branch Warden - Mastered feature branches and pull requests
  - 🌱 Conflict Pacifier - Resolved a merge conflict without panic
  skills_unlocked:
  - 🛠️ Pull Request Workflow
  - 🧠 Merge and Rebase Strategy
  progression_points: 50
  unlocks_features:
  - A repeatable, safe workflow for every project you build
layout: quest
---
*Greetings, brave adventurer! You learned to commit and push in the Foundation tier - the first words of the version-control tongue. Now you will learn to speak it fluently. **Git Workflow Mastery** teaches the rituals real teams live by: branching off to work safely, opening pull requests for review, choosing between merge and rebase, and resolving conflicts with a steady hand instead of a racing heart.*

*This is the workflow that lets dozens of developers build on one codebase without overwriting each other. Master it, and you can contribute to any project in the realm - including this one.*

## 📖 The Legend Behind This Quest

*In the dark ages, a team shared one trunk of code, and every change risked clobbering another. A single careless save could undo a colleague's day of work, and there was no way to undo it. Then **Git** arrived, and with it a discipline: never work directly on the main line. Branch off, build in isolation, prove your change, and only then weave it back. The pull request turned merging into a conversation - a place to review, discuss, and improve before code joins the trunk.*

*This workflow is now the heartbeat of open source and every serious team. Learn it here, and you carry it for the rest of your journey.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Feature Branches** - Create and switch branches to isolate your work
- [ ] **Good Commits** - Write small, well-described commits
- [ ] **Pull Requests** - Propose changes for review and merge them
- [ ] **Conflict Resolution** - Resolve a merge conflict deliberately and correctly

### Secondary Objectives (Bonus Achievements)
- [ ] **Merge vs. Rebase** - Choose the right way to integrate history
- [ ] **Reading the Repo** - Use `git log`, `git status`, and `git diff` fluently
- [ ] **Undo Safely** - Recover with `git restore`, `git revert`, and `git reflog`

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain when to merge and when to rebase a branch
- [ ] Open, review, and merge a pull request without help
- [ ] Resolve a conflict and explain exactly which version you kept and why

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Basic Git: `init`, `add`, `commit`, `push`
- [ ] Completion of [Git Basics](/quests/0000/git-basics/)
- [ ] A GitHub account

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Git installed and configured with your name and email
- [ ] The GitHub CLI (`gh`) recommended for pull requests

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You can already make and push commits
- [ ] You are ready to think about history, not just snapshots
- [ ] Ready for 75-90 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*Git behaves the same on every OS; only the install differs. Confirm your setup, then the rest of the quest is identical everywhere.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install Git and the GitHub CLI
brew install git gh

# Set your identity (once per machine)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# A sane default: name the first branch "main"
git config --global init.defaultBranch main
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install Git and the GitHub CLI
winget install Git.Git GitHub.cli

# Configure your identity
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install -y git gh

# Configure your identity
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# GitHub Codespaces ships Git and gh, already authenticated.
git --version
gh auth status
```

</details>

## 🧙‍♂️ Chapter 1: Feature Branches - Working Without Fear

*The first rule of a clean workflow: **never commit straight to `main`.** Branch off, build in safety, and `main` stays always-working.*

### ⚔️ Skills You'll Forge in This Chapter
- Creating and switching branches
- Making focused commits
- Pushing a branch to the remote

### 🏗️ The Branch Loop

```bash
# Start from an up-to-date main
git switch main
git pull

# Create and switch to a feature branch in one step
git switch -c feature/add-about-page

# ...make your edits, then stage and commit in small steps
git add about.md
git commit -m "Add About page with site mission"

# Push the branch and set it to track the remote
git push -u origin feature/add-about-page
```

**What makes a good commit?** Small, focused, and described in the imperative mood:

```text
✅ Add About page with site mission
✅ Fix broken baseurl on project site
❌ stuff
❌ fixed things and also changed the header and updated config
```

Read the repo's state any time with these three commands:

```bash
git status      # what is staged, modified, or untracked
git log --oneline --graph --all   # the shape of your history
git diff        # exactly what changed since the last stage
```

### 🔍 Knowledge Check: Branches
- [ ] Why should you never commit directly to `main`?
- [ ] What does `git switch -c` do that `git switch` alone does not?
- [ ] What does the `-u` flag on `git push` set up?

### ⚡ Quick Wins and Checkpoints
- [ ] **Branched off**: You created a feature branch from a fresh `main`
- [ ] **Committed small**: Your commit message reads as a clear imperative

## 🧙‍♂️ Chapter 2: Pull Requests, Merge, and Rebase - Joining the Trunk

*Your branch is ready. Now you propose it back to `main` through a **pull request** (PR) - a place for review before code merges. And you must choose how history gets stitched together: **merge** or **rebase**.*

### ⚔️ Skills You'll Forge in This Chapter
- Opening and merging a pull request
- The difference between merge and rebase
- Keeping a branch up to date

### 🏗️ Open a Pull Request

```bash
# With your feature branch pushed, open a PR from the terminal
gh pr create --title "Add About page" \
  --body "Adds an About page describing the site's mission."

# Review the PR, then merge it (squash keeps main history tidy)
gh pr merge --squash --delete-branch
```

**Merge vs. rebase** - the most-asked Git question, answered simply:

```bash
# MERGE: keeps both histories, adds a merge commit. Honest, non-destructive.
git switch main
git merge feature/add-about-page
#   main:    A---B---------M
#   feature:      \---C---D/      (M ties the two together)

# REBASE: replays your commits on top of main. Linear, but rewrites history.
git switch feature/add-about-page
git rebase main
#   main:    A---B
#   feature:        \---C'---D'   (C and D are re-created on top of B)
```

| | Merge | Rebase |
| --- | --- | --- |
| History | Preserves the true branch shape | Linear, as if you started from latest |
| Safety | Non-destructive | Rewrites commits (new hashes) |
| Golden rule | Always safe | **Never rebase commits others have pulled** |

A practical habit: **rebase your own local branch** to stay current, but **merge (or squash-merge) into shared `main`.** Update a feature branch before opening the PR:

```bash
git switch feature/add-about-page
git fetch origin
git rebase origin/main      # replay your work atop the latest main
```

### 🔍 Knowledge Check: Integration
- [ ] What does a merge commit record that a rebase erases?
- [ ] Why must you never rebase commits others have already pulled?
- [ ] What does `--squash` do when merging a PR?

## 🧙‍♂️ Chapter 3: Conflict Resolution - Steady Hands at the Crossroads

*A conflict happens when two branches change the same lines. Git cannot guess your intent, so it stops and asks you to choose. This is normal - not an emergency.*

### ⚔️ Skills You'll Forge in This Chapter
- Reading conflict markers
- Resolving a conflict deliberately
- Finishing the merge or rebase

### 🏗️ Resolve a Conflict

When a conflict occurs, Git marks the clashing region inside the file:

```text
<<<<<<< HEAD
The castle was built in three days.
=======
The castle was forged over a single night.
>>>>>>> feature/add-about-page
```

- Everything between `<<<<<<< HEAD` and `=======` is the current branch's version.
- Everything between `=======` and `>>>>>>>` is the incoming branch's version.

Edit the file by hand to the correct final text, **delete all three marker lines**, then complete the operation:

```bash
# After editing the file to the desired final content:
git add about.md

# If you were merging:
git commit          # finishes the merge

# If you were rebasing:
git rebase --continue

# Lost or panicking? Abort and return to safety:
git merge --abort      # or: git rebase --abort
```

> ⚠️ Resolving a conflict is a decision, not a deletion. Read both sides, keep what is correct (sometimes a blend of both), and make sure the file still makes sense before you stage it. When in doubt, `git restore` an untouched copy and `git reflog` will help you recover any state you reach.

### 🔍 Knowledge Check: Conflicts
- [ ] Which side of the markers is `HEAD`, and which is incoming?
- [ ] What three lines must you remove when resolving?
- [ ] How do you back out of a conflicted merge entirely?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Branch and Commit
**Objective**: Make a change on a feature branch.

**Requirements**:
- [ ] Create a branch with `git switch -c`
- [ ] Make a small, clearly-described commit
- [ ] Push the branch with `-u`

**Validation**: `git log --oneline` on the branch shows your commit ahead of `main`.

### 🟡 Intermediate Challenge: Ship via Pull Request
**Objective**: Merge a change through a PR.

**Requirements**:
- [ ] Open a PR with `gh pr create`
- [ ] Merge it with `--squash --delete-branch`
- [ ] Confirm `main` contains your change

**Validation**: `git switch main && git pull` brings your change into `main`.

### 🔴 Advanced Challenge: Create and Resolve a Conflict
**Objective**: Deliberately cause and resolve a merge conflict.

**Requirements**:
- [ ] Edit the same line on two branches
- [ ] Merge or rebase to trigger the conflict
- [ ] Resolve it, remove all markers, and complete the operation

**Validation**: The merged file is correct and `git status` reports a clean tree.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Branch Warden** - Feature branches and pull requests are second nature
- 🌱 **Conflict Pacifier** - You resolve conflicts calmly and correctly

**🛠️ Skills Unlocked**:
- **Pull Request Workflow** - Propose, review, and merge with confidence
- **Merge and Rebase Strategy** - Shape history on purpose

**🔓 Unlocked Quests**:
- Jekyll Fundamentals - Build a site you can now version cleanly
- GitHub Pages Basics - Ship branches straight to a live URL

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Jekyll Fundamentals](/quests/0001/jekyll-fundamentals/) - Build the site this workflow will protect

**Explore Side Adventures**:
- ⚔️ [GitHub Pages Basics](/quests/0001/github-pages-basics/) - Deploy from your branches
- ⚔️ [YAML Configuration](/quests/0001/yaml-configuration/) - Version your config with care

### Character Class Recommendations

**💻 Software Developer**: Continue to [Jekyll Fundamentals](/quests/0001/jekyll-fundamentals/)  
**🏗️ System Engineer**: Explore [GitHub Pages Basics](/quests/0001/github-pages-basics/)  
**🛠️ DevOps Specialist**: Take this workflow into CI/CD in the Adventurer tier

## 📚 Resources

### Official Documentation
- [Pro Git Book (free)](https://git-scm.com/book/en/v2) - The definitive Git reference
- [Git Branching](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging) - Branch and merge chapter
- [GitHub: About Pull Requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) - The PR lifecycle

### Community Resources
- [Oh My Git! (interactive game)](https://ohmygit.org/) - Learn branching by playing
- [Git on Stack Overflow](https://stackoverflow.com/questions/tagged/git) - Tagged Q&A
- [Learn Git Branching (visual)](https://learngitbranching.js.org/) - Animated branch practice

### Learning Materials
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials) - Merge, rebase, and workflows explained
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow) - A simple branching model

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Merged a feature branch via a pull request
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0001 - Web Fundamentals]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Git Basics]]
**Unlocks:** [[Jekyll Fundamentals]] · [[GitHub Pages Basics]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
