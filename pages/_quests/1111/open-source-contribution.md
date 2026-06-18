---
title: 'Open Source Contribution: Maintaining and Licensing'
author: IT-Journey Team
description: Contribute to and maintain open source. Learn the contribution workflow, community norms, reviewing and triaging issues, and the basics of software licensing.
excerpt: Contribute and maintain open source with good etiquette and license basics
preview: images/previews/open-source-contribution-contributing-maintaining.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1111'
difficulty: 🔴 Hard
estimated_time: 3-5 hours
primary_technology: git
quest_type: main_quest
quest_series: Leadership Mastery
quest_line: The Crown of Mastery
quest_arc: The Architect-King's Ascension
quest_dependencies:
  required_quests:
  - /quests/1111/tech-speaking-writing/
  recommended_quests:
  - /quests/1111/technical-leadership/
  unlocks_quests:
  - /quests/1111/building-technical-communities/
skill_focus: community
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Comfortable with Git branches, commits, and pull requests
  - A GitHub (or GitLab) account
  - Completion of Tech Speaking and Writing (recommended)
  system_requirements:
  - Git installed and configured
  - A terminal and a GitHub/GitLab account
  skill_level_indicators:
  - You can navigate a codebase you did not write
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - One real pull request opened to an open source project
  skill_demonstrations:
  - Can open a clean, well-described PR
  - Can read a license and state what it permits and requires
  knowledge_checks:
  - Understands permissive vs copyleft licenses
  - Can interpret a project's CONTRIBUTING and CODE_OF_CONDUCT
permalink: /quests/1111/open-source-contribution/
categories:
- Quests
- Community
- Hard
tags:
- '1111'
- git
- main_quest
- open-source
- licensing
- maintainership
- gamified-learning
keywords:
  primary:
  - '1111'
  - git
  - main_quest
  secondary:
  - open-source
  - licensing
  - maintainership
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1111 (15) Quest: Main Quest - Open Source'
rewards:
  badges:
  - 🏆 First Patch - Landed a contribution in someone else's project
  - 🛡️ Keeper of the Commons - Maintained a project for the good of all
  skills_unlocked:
  - 🛠️ Open Source Contribution Workflow
  - 🧠 Software Licensing Literacy
  progression_points: 90
  unlocks_features:
  - Continued progress through the Level 1111 Leadership & Innovation quest line
layout: quest
---
*Greetings, Master adventurer. The greatest works in our realm were not raised by lone heroes behind sealed gates - they were built in the open, stone by stone, by thousands of hands who never met. Linux, Git, Python, the very tools you wield: all are commons, tended by volunteers. This quest, **Open Source Contribution**, teaches you to give back to that commons and, in time, to tend it yourself as a maintainer.*

*Whether you have never opened a pull request to a stranger's repo or you already shepherd issues for your own library, this adventure forges the etiquette, workflow, and legal literacy of the open source citizen.*

## 📖 The Legend Behind This Quest

*In the days before the great sharing, knowledge was hoarded in locked towers - each guild guarding its secrets, each mage reinventing the same spells. Then a movement arose that declared: a spell shared is a spell multiplied. The Free and Open Source movement built a commons where any apprentice could read the master's source, learn from it, improve it, and pass it on.*

*That commons now powers nearly everything you build. To contribute to it is to repay a debt every developer owes. This quest teaches you to do so gracefully - and to understand the licenses that keep the commons free.*

## 🎯 Quest Objectives

By the time you complete this epic journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **The Contribution Workflow** - Fork, branch, commit, and open a clean pull request
- [ ] **Community Norms** - Read and honor CONTRIBUTING, CODE_OF_CONDUCT, and issue etiquette
- [ ] **Reviewing and Triaging** - Give helpful PR reviews and triage incoming issues as a maintainer
- [ ] **Licensing Basics** - Tell permissive from copyleft and know what each requires of you

### Secondary Objectives (Bonus Achievements)
- [ ] **Good First Contributions** - Find and complete a beginner-friendly issue
- [ ] **Maintainer Sustainability** - Set boundaries that prevent burnout
- [ ] **Releasing Responsibly** - Tag versions, write a changelog, follow semver

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain why a project chose its license to another person
- [ ] Open a PR a maintainer can merge without a dozen change requests
- [ ] Review someone else's PR with kind, specific, actionable comments
- [ ] Decline a feature request gracefully as a maintainer

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Comfortable with Git branches, commits, and pull requests
- [ ] A GitHub or GitLab account
- [ ] Completion of [Tech Speaking and Writing](/quests/1111/tech-speaking-writing/) (recommended)

### 🛠️ System Requirements
- [ ] Git installed and configured (`git config --global user.name/email`)
- [ ] A terminal and a code editor
- [ ] A GitHub or GitLab account with SSH or token auth set up

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can navigate a codebase you did not write
- [ ] You are ready to receive (and give) public code review
- [ ] Ready for 3-5 hours of focused, hands-on work

## 🌍 Choose Your Adventure Platform

*Open source runs on Git. Set up your environment, then we will contribute.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install Git and the GitHub CLI for a smooth contribution flow
brew install git gh
gh auth login                      # authenticate once
gh repo fork OWNER/REPO --clone    # fork + clone in one step
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
winget install Git.Git GitHub.cli
gh auth login
gh repo fork OWNER/REPO --clone
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y git
# Install the GitHub CLI (see cli.github.com for your distro)
gh auth login
gh repo fork OWNER/REPO --clone
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# GitHub Codespaces gives you a ready contribution environment in the browser
# Open any repo, press "." or create a Codespace, and gh is preinstalled.
gh repo fork OWNER/REPO --clone
```

</details>

## 🧙‍♂️ Chapter 1: The Contribution Workflow - From Fork to Merge

*Almost every open source project on GitHub uses the same dance: fork, branch, change, push, pull request. Learn it once and you can contribute anywhere.*

### ⚔️ Skills You'll Forge in This Chapter
- The fork-branch-PR workflow
- Writing commits and PR descriptions maintainers love
- Responding to review without ego

### 🏗️ The Standard Flow

```bash
# 1. Fork the project (creates your own copy), then clone it
gh repo fork OWNER/REPO --clone
cd REPO

# 2. Create a focused branch — one logical change per branch
git checkout -b fix/typo-in-readme

# 3. Make the change, then commit with a clear, imperative message
git add README.md
git commit -m "docs: fix broken install link in README"

# 4. Push to your fork and open a pull request
git push -u origin fix/typo-in-readme
gh pr create --fill   # then edit the description to explain WHY
```

A great PR is **small, focused, and explained**. Maintainers are volunteers reviewing in their spare time; a 2,000-line PR that "refactors everything" will rot unreviewed. The PR description should answer: *what does this change, why, and how did you test it?*

```text
PR description template:
  ## What
  One or two sentences on the change.
  ## Why
  The problem it solves (link the issue: "Closes #123").
  ## How tested
  The commands you ran / the case you verified.
  ## Notes for reviewers
  Anything tricky, or decisions you weren't sure about.
```

When a reviewer asks for changes, **assume good faith**. They are protecting a codebase they care about. Address each comment, push a new commit, and reply - do not take it personally.

### 🔍 Knowledge Check: Contribution Workflow
- [ ] Why should one branch contain one logical change?
- [ ] What three questions should a PR description answer?
- [ ] How do you respond when a maintainer requests changes?

### ⚡ Quick Wins and Checkpoints
- [ ] **Forked a repo**: You created your own copy and cloned it
- [ ] **Opened a PR**: You pushed a branch and created a pull request

## 🧙‍♂️ Chapter 2: Community Norms and Maintainership - Tending the Commons

*Code is the easy part. The norms - how you ask, how you disagree, how you say no - are what keep a project healthy. Read the project's documents before you type a word.*

### ⚔️ Skills You'll Forge in This Chapter
- Reading CONTRIBUTING, CODE_OF_CONDUCT, and issue templates
- Triaging issues as a maintainer
- Saying no gracefully and avoiding burnout

### 🏗️ The Citizen's Checklist

Before contributing, read the project's onboarding documents:

- [ ] **README** - what the project is and how to run it
- [ ] **CONTRIBUTING.md** - how this project wants PRs (style, tests, sign-off)
- [ ] **CODE_OF_CONDUCT.md** - the behavior expected of everyone
- [ ] **Existing issues** - search before filing; your bug may already be tracked
- [ ] **"good first issue" / "help wanted" labels** - the maintainer's invitation list

As a **maintainer**, your job flips from writing code to gardening: triaging issues, reviewing PRs, and protecting your own time. A triage rubric:

```text
Incoming issue triage:
  Is it reproducible?         -> ask for a minimal repro if not
  Is it in scope?             -> label "wontfix" with a kind explanation if not
  Is it a good first issue?   -> label it, invite a newcomer
  Is it urgent (security)?    -> escalate, may warrant a private disclosure path
```

Saying **no** is a core maintainer skill. "Thank you for this thoughtful proposal. It does not fit the project's scope of X, so I am going to decline - but you are welcome to maintain it as a plugin/fork." Boundaries prevent the burnout that kills open source projects. You owe users nothing; you maintain because you choose to.

### 🔍 Knowledge Check: Community Norms
- [ ] What four documents should you read before contributing?
- [ ] How do you decline a feature request without being unkind?
- [ ] Why is setting boundaries essential for a maintainer?

## 🧙‍♂️ Chapter 3: Licensing Basics - The Rules of the Commons

*Open source is "open" only because of licenses - legal spells that say what others may do with the code. Pick the wrong one (or ignore them) and you create real risk. You do not need to be a lawyer, but you must read.*

### ⚔️ Skills You'll Forge in This Chapter
- Permissive vs copyleft licenses
- What each license requires of you
- How license obligations flow into your own projects

### 🏗️ The License Map

| License | Type | You may | You must | Typical use |
| --- | --- | --- | --- | --- |
| **MIT / BSD / Apache-2.0** | Permissive | Use, modify, sell, keep private | Keep the copyright notice (Apache adds a patent grant) | Libraries that want max adoption |
| **GPL-2.0 / GPL-3.0** | Strong copyleft | Use, modify | Release your derivative under the same GPL, with source | Tools that must stay free |
| **LGPL** | Weak copyleft | Link from closed code | Share changes to the library itself | Libraries usable by proprietary apps |
| **AGPL-3.0** | Network copyleft | Use, modify | Share source even for networked/SaaS use | Server software resisting "SaaS loophole" |
| **(no license)** | All rights reserved | Almost nothing - default copyright | — | An unlicensed repo is NOT free to use |

```text
Two rules that save you:
  1. "No LICENSE file" does NOT mean "public domain." It means
     all rights reserved — you may not legally reuse it. Always add a license.
  2. Copyleft is "viral": if you bundle GPL code into your product,
     your product may have to be GPL too. Check before you depend.
```

The big distinction: **permissive** licenses (MIT, Apache) let anyone do almost anything, including building closed products on top. **Copyleft** licenses (GPL family) require that derivatives stay open. Choose based on whether you want maximum adoption (permissive) or a guarantee the work stays free (copyleft).

### 🔍 Knowledge Check: Licensing
- [ ] What does an MIT-licensed project require you to keep?
- [ ] Why is a repo with no LICENSE file *not* free to reuse?
- [ ] What problem does the AGPL try to close?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Land a Good First Issue
**Objective**: Find a "good first issue" and open a real pull request.

**Requirements**:
- [ ] Read the project's CONTRIBUTING and CODE_OF_CONDUCT first
- [ ] One focused branch, clear commit message
- [ ] A PR description answering what / why / how-tested

**Validation**: A maintainer can review your PR without confusion.

### 🟡 Intermediate Challenge: Review a PR
**Objective**: Review an open PR (yours or a peer's) with constructive comments.

**Requirements**:
- [ ] At least three specific, actionable comments
- [ ] Lead with something that works, not only criticism
- [ ] No "nit" left as a blocker - separate must-fix from nice-to-have

**Validation**: The author understands exactly what to change and why.

### 🔴 Advanced Challenge: License Your Own Project
**Objective**: Add a license to a project of yours and justify the choice.

**Requirements**:
- [ ] Choose permissive or copyleft with a stated reason
- [ ] Add a LICENSE file and a license header where appropriate
- [ ] Add a short CONTRIBUTING.md and CODE_OF_CONDUCT

**Validation**: A stranger could legally and confidently reuse and contribute to it.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **First Patch** - You landed a contribution in someone else's project
- 🛡️ **Keeper of the Commons** - You maintained a project for the good of all

**🛠️ Skills Unlocked**:
- **Open Source Contribution Workflow** - Fork to merge, gracefully
- **Software Licensing Literacy** - Know the rules of the commons

**🔓 Unlocked Quests**:
- Building Technical Communities - Grow the people around your project
- Innovation and R&D - Turn open source into a platform for new ideas

**📊 Progression Points**: +90 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Building Technical Communities](/quests/1111/building-technical-communities/) - Grow a community around your work

**Explore Side Adventures**:
- ⚔️ [Innovation and R&D](/quests/1111/innovation-rnd/) - Experiment in the open
- ⚔️ [Tech Speaking and Writing](/quests/1111/tech-speaking-writing/) - Document and evangelize your project

### Character Class Recommendations

**💻 Software Developer**: Continue to [Building Technical Communities](/quests/1111/building-technical-communities/)  
**🏗️ System Engineer**: Explore [Innovation and R&D](/quests/1111/innovation-rnd/)  
**🛡️ Security Specialist**: Advance to [Architecture Reviews](/quests/1111/architecture-reviews/)

## 📚 Resources

### Official Documentation
- [GitHub Open Source Guides](https://opensource.guide/) - The canonical how-to for contributing and maintaining
- [choosealicense.com](https://choosealicense.com/) - GitHub's plain-English license picker
- [Open Source Initiative - approved licenses](https://opensource.org/licenses/) - The authoritative license list

### Community Resources
- [First Contributions](https://github.com/firstcontributions/first-contributions) - A hands-on first-PR tutorial
- [CHAOSS - community health metrics](https://chaoss.community/) - How to measure a healthy project
- [Contributor Covenant](https://www.contributor-covenant.org/) - The widely-used code of conduct

### Learning Materials
- [Producing Open Source Software (Karl Fogel)](https://producingoss.com/) - The free, definitive book on running a project
- [Semantic Versioning](https://semver.org/) - The versioning contract for releases
- [Keep a Changelog](https://keepachangelog.com/) - How to document releases

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Opened a real pull request to an open source project
- [ ] ✅ Reviewed at least one pull request constructively
- [ ] ✅ Added a license (and justified it) to a project of your own
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1111: Leadership & Innovation]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Tech Speaking and Writing: RFCs, Design Docs, and Talks That Persuade]]
**Unlocks:** [[Building Technical Communities: Growing Developer Ecosystems]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
