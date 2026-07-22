---
title: 'GitHub Actions Basics: Workflow Automation for Modern DevOps'
author: IT-Journey Team
description: 'Build GitHub Actions workflows from scratch: master jobs, steps, triggers, runners, secrets, and matrix builds to automate your testing and deployment.'
excerpt: Master GitHub Actions workflow creation for automating your software development lifecycle
preview: images/previews/github-actions-basics-workflow-automation-descript.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0101'
difficulty: 🟡 Medium
estimated_time: 60-75 minutes
primary_technology: github-actions
quest_type: main_quest
quest_series: DevOps Pipeline Mastery
quest_line: The Forge of Automation
quest_arc: Wielding the Workflow
quest_dependencies:
  required_quests:
  - /quests/0101/cicd-fundamentals/
  recommended_quests: []
  unlocks_quests:
  - /quests/0101/testing-integration/
  - /quests/0101/secrets-management/
  - /quests/0101/workflow-optimization/
skill_focus: devops
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Understanding of the CI/CD build-test-deploy flow
  - Familiarity with Git and pull requests
  - Comfort reading YAML
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - A free GitHub account and a repository you can push to
  - Git installed locally
  skill_level_indicators:
  - You completed CI/CD Fundamentals or know the build-test-deploy flow
  - You can edit YAML without fear of indentation
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A repository with a working multi-job workflow including a matrix build
  skill_demonstrations:
  - Can explain the workflow / job / step hierarchy
  - Can configure triggers, runners, and secrets correctly
  knowledge_checks:
  - Understands the difference between an action and a step
  - Can read a matrix strategy and predict how many jobs it spawns
permalink: /quests/0101/github-actions-basics/
categories:
- Quests
- DevOps
- Medium
tags:
- '0101'
- github-actions
- main_quest
- devops
- hands-on
- gamified-learning
keywords:
  primary:
  - '0101'
  - github-actions
  - main_quest
  secondary:
  - devops
  - hands-on
  - gamified-learning
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0101 (5) Quest: Main Quest - GitHub Actions Basics'
rewards:
  badges:
  - 🏆 Workflow Weaver - Built a multi-job GitHub Actions pipeline
  - 🤖 Runner Whisperer - Commanded runners, triggers, and matrices
  skills_unlocked:
  - 🛠️ Workflow Authoring
  - 🧠 Event-Driven Automation
  progression_points: 50
  unlocks_features:
  - Ability to automate any task on GitHub events
layout: quest
---
*Greetings, brave adventurer! You have proven you understand the build-test-deploy flow. Now you must learn to **summon a tireless automaton** that runs it for you. The Forge of Automation hands you its most popular hammer: **GitHub Actions**, a workflow engine baked directly into the repository where your code already lives.*

*With a single YAML scroll committed beside your code, you can conjure runners that build, test, and deploy on every push, every pull request, every schedule, or any event you choose. This quest teaches the grammar of that scroll - workflows, jobs, steps, triggers, runners, actions, secrets, and the mighty matrix.*

## 📖 The Legend Behind This Quest

*Before GitHub Actions, automation lived on a separate server you had to feed and water - a CI box that broke at 3 a.m. and belonged to no one. When GitHub Actions arrived, the forge moved inside the keep. Your pipeline became a file in your repo, versioned alongside the code it tests, reviewed in the same pull requests, and runnable by anyone who clones the project.*

*This quest teaches you to read and write that file fluently, so that "automate this" becomes a reflex rather than a research project.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **The Workflow Hierarchy** - Explain how workflows contain jobs which contain steps
- [ ] **Triggers and Events** - Configure `on:` to run workflows on pushes, PRs, schedules, and manual dispatch
- [ ] **Runners and Actions** - Choose a runner and compose reusable actions into steps
- [ ] **Matrix Builds** - Test across multiple versions or OSes with one strategy block

### Secondary Objectives (Bonus Achievements)
- [ ] **Secrets** - Pass credentials into a workflow without committing them
- [ ] **Job Dependencies** - Order jobs with `needs:` and pass outputs between them
- [ ] **Permissions** - Scope the workflow's `GITHUB_TOKEN` to least privilege

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Sketch the workflow/job/step tree from memory
- [ ] Predict how many jobs a given matrix produces
- [ ] Read an unfamiliar workflow and explain what triggers it
- [ ] Add a secret and reference it correctly with `${% raw %}{{ secrets.NAME }}{% endraw %}`

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] The CI/CD build-test-deploy flow (see CI/CD Fundamentals)
- [ ] Basic Git and pull-request workflow
- [ ] Comfort reading YAML indentation

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] A free GitHub account and a repository you can push to
- [ ] Git installed locally and a text editor (VS Code recommended)

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You completed CI/CD Fundamentals or know the pipeline stages
- [ ] You can edit YAML without breaking indentation
- [ ] Ready for 60-75 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*GitHub Actions runs in GitHub's cloud, so your local platform only matters for editing files and pushing. The runner itself is a fresh virtual machine GitHub provides.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install the GitHub CLI to view runs from your terminal
brew install gh git
gh auth login

# Create the workflows directory in your repo
mkdir -p .github/workflows
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install the GitHub CLI and Git
winget install GitHub.cli
winget install Git.Git
gh auth login

# Create the workflows directory
New-Item -ItemType Directory -Force -Path .github\workflows
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Debian/Ubuntu: install gh and git
sudo apt update && sudo apt install -y gh git
gh auth login

# Create the workflows directory
mkdir -p .github/workflows
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# In a Codespace, gh and git are pre-installed and authenticated.
mkdir -p .github/workflows
gh run list   # see your workflow runs without leaving the terminal
```

> **Heads up:** `gh run list` only works from inside an authenticated repo context (a Codespace, or after `gh auth login` locally). Run it elsewhere and it exits with `gh: To use GitHub CLI ... set the GH_TOKEN environment variable.` — that's an auth issue, not a broken command.

> The runner that executes your workflow IS the cloud realm - GitHub spins up an `ubuntu-latest`, `windows-latest`, or `macos-latest` VM per job and destroys it when finished.

</details>

## 🧙‍♂️ Chapter 1: The Anatomy of a Workflow

*A workflow is a YAML file in `.github/workflows/`. Inside it, a nested hierarchy describes what to run, when, and where.*

### ⚔️ Skills You'll Forge in This Chapter
- The workflow → job → step hierarchy
- How runners host jobs
- The difference between an action and a `run` command

### 🏗️ The Hierarchy, Top to Bottom

```text
Workflow (one .yml file)
└── triggered by events (on:)
    └── Job (runs on a Runner; jobs run in parallel by default)
        └── Step (runs in order, top to bottom)
            ├── uses: an Action (reusable, e.g. actions/checkout@v4)
            └── run: a shell command
```

- A **workflow** is the whole file. It is triggered by events.
- A **job** runs on a fresh **runner** (a VM). Jobs run in parallel unless you order them with `needs:`.
- A **step** runs inside a job, in order. A step either `uses:` a reusable **action** or executes a `run:` command.

Here is a complete, runnable first workflow:

```yaml
name: Hello Actions
on:
  push:
    branches: [main]
  pull_request:
jobs:
  greet:
    runs-on: ubuntu-latest        # the runner
    steps:
      - name: Check out the code
        uses: actions/checkout@v4 # an action
      - name: Say hello
        run: echo "Hello from the runner, $GITHUB_ACTOR!"  # a run command
```

### 🔍 Knowledge Check: Anatomy
- [ ] What is the difference between a step that `uses:` and one that `run:`s?
- [ ] Where does a job actually execute?
- [ ] Do two jobs in the same workflow run in order or in parallel by default?

### ⚡ Quick Wins and Checkpoints
- [ ] **Committed a workflow**: The file lives in `.github/workflows/`
- [ ] **Saw it run**: The Actions tab shows a green run

## 🧙‍♂️ Chapter 2: Triggers, Secrets, and Job Ordering

*A workflow is only as useful as the events that wake it. And real pipelines need credentials they must never leak.*

### ⚔️ Skills You'll Forge in This Chapter
- Configuring `on:` for many event types
- Passing secrets safely
- Ordering jobs with `needs:` and scoping permissions

### 🏗️ Triggers - the `on:` Block

```yaml
on:
  push:                       # on any push
    branches: [main, 'release/**']
    paths: ['src/**']         # only when source files change
  pull_request:               # on PRs targeting this repo
  schedule:
    - cron: '0 6 * * 1'       # every Monday at 06:00 UTC
  workflow_dispatch:          # a manual "Run workflow" button
```

### 🏗️ Secrets and Permissions

Never commit a token. Store it in **Settings → Secrets and variables → Actions**, then reference it. Note that secrets are masked in logs automatically:

```yaml
permissions:
  contents: read              # least privilege for the built-in GITHUB_TOKEN
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Use a secret safely
        env:
          API_TOKEN: ${% raw %}{{ secrets.DEPLOY_TOKEN }}{% endraw %}   # never echo this directly
        run: |
          curl -fsS -H "Authorization: Bearer $API_TOKEN" https://example.com/ping
```

### 🏗️ Ordering Jobs with `needs:`

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "building" && npm ci && npm run build
  deploy:
    needs: build              # deploy waits for build to succeed
    runs-on: ubuntu-latest
    steps:
      - run: echo "deploying only after a successful build"
```

### 🔍 Knowledge Check: Triggers and Secrets
- [ ] How do you give a workflow a manual "Run" button?
- [ ] Why should you set `permissions:` explicitly?
- [ ] What happens to a deploy job whose `needs:` job fails?

## 🧙‍♂️ Chapter 3: Matrix Builds - Many Jobs from One Strategy

*Why test on one Node version when you could test on three across two operating systems with one block of YAML? The **matrix** multiplies a single job definition into a grid of parallel jobs.*

### ⚔️ Skills You'll Forge in This Chapter
- Defining a matrix strategy
- Predicting the number of jobs produced
- Controlling failures with `fail-fast`

### 🏗️ A Matrix Build

```yaml
name: Matrix CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ${% raw %}{{ matrix.os }}{% endraw %}
    strategy:
      fail-fast: false        # let every combo finish even if one fails
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: ['18', '20', '22']
        exclude:
          - os: windows-latest # skip one specific combination
            node: '18'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${% raw %}{{ matrix.node }}{% endraw %}
      - run: npm ci
      - run: npm test
```

A 2 × 3 grid is six jobs; the `exclude:` above drops one, leaving **five parallel jobs**. Each runs on its own runner. With `fail-fast: false`, a failure in one combination does not cancel the others, so you see exactly which combinations break.

### 🔍 Knowledge Check: Matrix
- [ ] How many jobs does a 2×3 matrix produce before any `exclude`?
- [ ] What does `fail-fast: false` change?
- [ ] How would you exclude one specific combination from the grid?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Your First Workflow
**Objective**: Commit the "Hello Actions" workflow and trigger it.

**Requirements**:
- [ ] File lives at `.github/workflows/hello.yml`
- [ ] Runs on both push and pull_request
- [ ] Produces a green run in the Actions tab

**Validation**: A push triggers the workflow and it succeeds.

### 🟡 Intermediate Challenge: Build, then Deploy
**Objective**: Create a two-job workflow where `deploy` runs only after `build` succeeds, using a repository secret.

**Requirements**:
- [ ] Two jobs ordered with `needs:`
- [ ] A secret referenced via `${% raw %}{{ secrets.NAME }}{% endraw %}`
- [ ] Explicit `permissions:` block set to least privilege

**Validation**: Deleting the secret makes the deploy step fail clearly; breaking build skips deploy.

### 🔴 Advanced Challenge: Matrix Across Versions
**Objective**: Test your project across three language versions and two operating systems.

**Requirements**:
- [ ] A matrix producing at least six jobs
- [ ] `fail-fast: false` so all combinations report
- [ ] One excluded combination using `exclude:`

**Validation**: The Actions tab shows the expected grid of parallel jobs.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Workflow Weaver** - You built a multi-job pipeline in YAML
- 🤖 **Runner Whisperer** - You commanded runners, triggers, and matrices

**🛠️ Skills Unlocked**:
- **Workflow Authoring** - Express any automation as a versioned YAML file
- **Event-Driven Automation** - Trigger work on exactly the right events

**🔓 Unlocked Quests**:
- Testing Integration - Make your workflow's test stages meaningful
- Secrets Management - Go beyond repo secrets to OIDC and vaults
- Workflow Optimization - Make these pipelines fast and cheap

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Testing Integration](/quests/0101/testing-integration/) - Add real test gates to your workflow

**Explore Side Adventures**:
- ⚔️ [Secrets Management](/quests/0101/secrets-management/) - Credentials done right
- ⚔️ [Workflow Optimization](/quests/0101/workflow-optimization/) - Make it fast

### Character Class Recommendations

**💻 Software Developer**: Continue to [Testing Integration](/quests/0101/testing-integration/)  
**🏗️ System Engineer**: Explore [Workflow Optimization](/quests/0101/workflow-optimization/)  
**🛡️ Security Specialist**: Check out [Secrets Management](/quests/0101/secrets-management/)

## 📚 Resources

### Official Documentation
- [GitHub Actions Documentation](https://docs.github.com/en/actions) - The complete reference
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) - Every key explained
- [Using a matrix for your jobs](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs) - Matrix deep dive

### Community Resources
- [GitHub Marketplace - Actions](https://github.com/marketplace?type=actions) - Thousands of reusable actions
- [awesome-actions](https://github.com/sdras/awesome-actions) - Curated list of actions and guides
- [GitHub Actions Community Discussions](https://github.com/orgs/community/discussions/categories/actions) - Ask questions

### Learning Materials
- [act - run Actions locally](https://github.com/nektos/act) - Test workflows on your machine
- [Encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) - Secrets done right

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Built a multi-job workflow with a matrix
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0101 - CI/CD & DevOps]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Prerequisites:** [[CI/CD Fundamentals: Continuous Integration and Continuous Deployment Essentials]] **Unlocks:** [[Testing Integration: Automated Quality Assurance in CI/CD Pipelines]] · [[Secrets Management: Secure Configuration and Credential Handling]] · [[Workflow Optimization: Caching Strategies and Pipeline Parallelization]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
