---
title: 'CI/CD Fundamentals: The Build-Test-Deploy Pipeline'
author: IT-Journey Team
description: 'Master CI/CD fundamentals: the build-test-deploy flow, how continuous integration, delivery, and deployment differ, pipeline stages, and fast feedback loops.'
excerpt: Learn the core concepts and practices of continuous integration and continuous deployment for automated software delivery
preview: images/previews/ci-cd-fundamentals-continuous-integration-quest-ti.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0101'
difficulty: 🟡 Medium
estimated_time: 75-90 minutes
primary_technology: cicd
quest_type: main_quest
quest_series: DevOps Pipeline Mastery
quest_line: The Forge of Automation
quest_arc: Foundations of the Pipeline
quest_dependencies:
  required_quests: []
  recommended_quests: []
  unlocks_quests:
  - /quests/0101/github-actions-basics/
  - /quests/0101/testing-integration/
  - /quests/0101/deployment-pipelines/
skill_focus: devops
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Basic command line navigation
  - Familiarity with Git (clone, commit, push, branches)
  - Comfort reading code in at least one language
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Git installed and a free GitHub account
  - A terminal and a text editor or IDE (VS Code recommended)
  skill_level_indicators:
  - You have committed code to a Git repository before
  - You are ready to think about software delivery as an automated system
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A repository with a working pipeline that builds and tests on every push
  skill_demonstrations:
  - Can explain the difference between CI, continuous delivery, and continuous deployment
  - Can describe each stage of a build-test-deploy pipeline
  knowledge_checks:
  - Understands why fast feedback matters
  - Can troubleshoot a failing pipeline stage
permalink: /quests/0101/cicd-fundamentals/
categories:
- Quests
- DevOps
- Medium
tags:
- '0101'
- cicd
- main_quest
- devops
- hands-on
- gamified-learning
keywords:
  primary:
  - '0101'
  - cicd
  - main_quest
  secondary:
  - devops
  - hands-on
  - gamified-learning
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0101 (5) Quest: Main Quest - CI/CD Fundamentals'
rewards:
  badges:
  - 🏆 Pipeline Initiate - Internalized the build-test-deploy flow
  - ⚙️ Keeper of the Green Build - Adopted a fast-feedback mindset
  skills_unlocked:
  - 🛠️ Pipeline Design
  - 🧠 Continuous Integration Discipline
  progression_points: 50
  unlocks_features:
  - Access to the rest of the Level 0101 CI/CD & DevOps quest line
layout: quest
---
*Greetings, brave adventurer! You have entered the **Adventurer tier**, and the great **Forge of Automation** roars before you. Here, the manual rituals of old - the late-night deploys, the "works on my machine" curses, the dread of release day - are melted down and reforged into a single, tireless machine. This quest, **CI/CD Fundamentals**, is the first hammer-strike. It teaches you to turn every commit into a verified, deployable artifact without lifting a finger.*

*Whether you have only ever pushed code and prayed, or you have wired together a few scripts and want to understand the discipline behind them, this adventure forges the mental model every DevOps practitioner needs: the build-test-deploy flow, the difference between integration, delivery, and deployment, and the relentless pursuit of fast feedback.*

## 📖 The Legend Behind This Quest

*In the early ages of software, teams would labor in isolation for months, hoarding their changes like dragons guard gold. When the day of reckoning came - "integration week" - they would slam their work together and watch it explode. Builds broke, tests that never existed could not save them, and releases slipped by quarters.*

*Then a new discipline arose. The masters declared: integrate small, integrate often, and let an automated forge prove the work after every single change. This is **Continuous Integration**. Extend that forge all the way to the gates of production, and you have **Continuous Delivery** and **Continuous Deployment**. Master this flow and you will never fear release day again.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **CI vs CD vs CD** - Explain Continuous Integration, Continuous Delivery, and Continuous Deployment and how they differ
- [ ] **The Build-Test-Deploy Flow** - Trace a change from commit through every pipeline stage to release
- [ ] **Pipeline Stages** - Identify the canonical stages and what each one proves
- [ ] **Fast Feedback** - Explain why short feedback loops are the core value of CI/CD

### Secondary Objectives (Bonus Achievements)
- [ ] **Trunk-Based Development** - Understand why small, frequent merges keep the build green
- [ ] **Pipeline as Code** - Recognize that pipelines live in version control beside the app
- [ ] **Fail Fast** - Order stages so cheap checks run before expensive ones

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain CI/CD to a teammate without notes
- [ ] Draw the stages of a pipeline and say what each gate protects
- [ ] Diagnose which stage failed from a pipeline log
- [ ] Justify why a broken build should block a merge

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Basic understanding of Git (commit, push, pull request)
- [ ] Familiarity with at least one programming language
- [ ] Comfort using a terminal

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Git installed and a free GitHub account
- [ ] A text editor or IDE (VS Code recommended)

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You have pushed code to a repository before
- [ ] You are ready to think about delivery as an automated system
- [ ] Ready for 75-90 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*CI/CD is platform-independent in theory, but you will practice with real tooling. Choose the path that fits your setup. Each path installs Git and a language runtime so you can build and test a tiny project locally before automating it.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install Git and a runtime using Homebrew
brew install git node

# Verify the tools that your pipeline will use
git --version
node --version

# Create a tiny project to automate later
mkdir cicd-quest && cd cicd-quest
git init
npm init -y
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install Git and Node with winget
winget install Git.Git
winget install OpenJS.NodeJS.LTS

# Verify
git --version
node --version

# Scaffold a tiny project
mkdir cicd-quest; cd cicd-quest
git init
npm init -y
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install -y git nodejs npm

# Verify
git --version
node --version

# Scaffold a tiny project
mkdir cicd-quest && cd cicd-quest
git init
npm init -y
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# A GitHub Codespace or any container already has Git and runtimes.
# Open your repo in a Codespace and the whole pipeline runs in the cloud.
git --version
node --version
```

> Cloud paths shine here: the same runner that builds your code in CI is one click away in a Codespace, so "works on my machine" becomes "works on the machine that ships it."

</details>

## 🧙‍♂️ Chapter 1: CI vs CD vs CD - Three Words, Three Disciplines

*The acronym hides a trap. "CD" means two different things, and confusing them confuses entire teams. Untangle them once and the whole field clicks.*

### ⚔️ Skills You'll Forge in This Chapter
- The precise meaning of CI, Continuous Delivery, and Continuous Deployment
- Why each builds on the previous one
- Where human approval lives in each model

### 🏗️ The Three Disciplines

| Term | What it automates | What it proves | Human in the loop? |
| --- | --- | --- | --- |
| **Continuous Integration (CI)** | Build + automated tests on every change | The code merges cleanly and passes its tests | No - it is fully automatic |
| **Continuous Delivery (CD)** | CI **plus** packaging a release that is always deployable | A button-press could ship to production at any time | Yes - a human clicks "deploy" |
| **Continuous Deployment (CD)** | Continuous Delivery **plus** the automatic deploy | Every green build reaches production by itself | No - it ships automatically |

The progression is additive: **Deployment ⊃ Delivery ⊃ Integration**. You cannot do continuous deployment without first having trustworthy continuous integration. Most teams live happily at continuous delivery, shipping on demand with a single approval.

### 🔍 Knowledge Check: The Three Disciplines
- [ ] Which discipline requires a human to click "deploy"?
- [ ] Why is continuous integration a prerequisite for the other two?
- [ ] A team merges often and tests automatically but releases manually once a sprint. Which level are they at?

### ⚡ Quick Wins and Checkpoints
- [ ] **Named the three**: You can define CI, Delivery, and Deployment in one sentence each
- [ ] **Placed the human**: You know where approval lives in each model

## 🧙‍♂️ Chapter 2: The Build-Test-Deploy Flow and Its Stages

*A pipeline is a conveyor belt. A change enters at one end and either falls off at a failed gate or emerges at the other end as a deployed release. Each stage is a guard that asks one question.*

### ⚔️ Skills You'll Forge in This Chapter
- The canonical stages of a pipeline
- Why cheap, fast checks run first
- How a stage "gates" the next

### 🏗️ The Canonical Pipeline

```text
Commit ─► Build ─► Unit Test ─► Integration Test ─► Package ─► Deploy (staging) ─► Deploy (prod)
   │        │          │               │               │            │                  │
 trigger  compiles   logic is       components      build an     verify in a       release to
  the     the code   correct in     work together   artifact     prod-like env     real users
 pipeline            isolation
```

The ordering is deliberate: a build takes seconds, unit tests take seconds-to-minutes, integration tests take longer, and deployment is the most expensive and risky. By running the cheapest checks first, a broken commit **fails fast** - you learn within a minute, not after a twenty-minute deploy.

Here is a minimal `package.json` whose scripts map directly onto pipeline stages:

```json
{
  "name": "cicd-quest",
  "version": "1.0.0",
  "scripts": {
    "build": "echo 'compiling...' && node -e \"console.log('build ok')\"",
    "test": "node --test",
    "lint": "echo 'linting...' && exit 0"
  }
}
```

And the simplest possible pipeline definition, expressed as GitHub Actions YAML, runs those stages on every push:

```yaml
name: CI
on: [push, pull_request]
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run lint   # cheapest check first
      - run: npm run build
      - run: npm test       # gate the rest of the pipeline
```

### 🔍 Knowledge Check: Pipeline Stages
- [ ] Why do unit tests run before integration tests?
- [ ] What does the "package" stage produce that "build" does not?
- [ ] Why is deploying to staging before production valuable?

### ⚡ Quick Wins and Checkpoints
- [ ] **Drew the belt**: You sketched the build-test-deploy flow
- [ ] **Ran it locally**: `npm run build && npm test` passes on your machine

## 🧙‍♂️ Chapter 3: Fast Feedback - The Real Reason CI/CD Exists

*Strip away the tooling and one principle remains: **the faster you learn that something is broken, the cheaper it is to fix.** Every CI/CD practice serves this single goal.*

### ⚔️ Skills You'll Forge in This Chapter
- Why feedback latency dominates everything
- Trunk-based development and small batches
- Keeping the build green as a team contract

### 🏗️ The Economics of Feedback

A bug caught by a unit test costs a developer one minute. The same bug caught in production costs an incident, a rollback, and a postmortem. Feedback loops, ordered from fastest to slowest:

```text
1. Editor / linter     (seconds)   ← cheapest place to catch a mistake
2. Local test run      (seconds)
3. CI on pull request  (minutes)   ← the safety net before merge
4. Staging deploy      (minutes)
5. Production incident  (hours+)   ← the most expensive place to learn
```

CI/CD pushes detection as far up that list as possible. Two practices make it work:

- **Small batches / trunk-based development**: merge tiny changes frequently so each pipeline run tests a small, understandable diff. A failed build points at a handful of lines, not a month of work.
- **The green-build contract**: a red pipeline blocks merges. The team's first job when the build breaks is to make it green again, before anyone adds more work on top of broken foundations.

```bash
# A healthy rhythm: small, frequent, verified commits
git checkout -b add-greeting
# ... make a tiny change ...
npm test                 # fast local feedback first
git commit -am "feat: add greeting"
git push -u origin add-greeting
# Open a PR; CI runs the pipeline; merge only when green.
```

### 🔍 Knowledge Check: Fast Feedback
- [ ] Where is the cheapest place to catch a bug, and where is the most expensive?
- [ ] Why do small batches make failed builds easier to diagnose?
- [ ] What should the whole team do the moment the build goes red?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Define the Trio
**Objective**: Without notes, write one-sentence definitions of CI, Continuous Delivery, and Continuous Deployment.

**Requirements**:
- [ ] All three defined clearly
- [ ] State where a human approval sits in each
- [ ] Give one real example of a team at each level

**Validation**: A teammate can tell the three apart from your definitions.

### 🟡 Intermediate Challenge: Wire a Real Pipeline
**Objective**: Add the GitHub Actions workflow from Chapter 2 to a real repository and watch it run.

**Requirements**:
- [ ] A repo with `lint`, `build`, and `test` scripts
- [ ] A workflow that runs all three on every push and pull request
- [ ] A passing green run visible in the Actions tab

**Validation**: Pushing a commit triggers a green pipeline; breaking a test turns it red.

### 🔴 Advanced Challenge: Order for Fail-Fast
**Objective**: Deliberately reorder your pipeline so the cheapest checks run first, and prove it fails fast.

**Requirements**:
- [ ] Lint runs before build, build before tests
- [ ] Introduce a lint error and confirm the pipeline fails in seconds
- [ ] Document how long each stage takes

**Validation**: A trivial mistake fails the pipeline at the earliest, cheapest stage.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Pipeline Initiate** - You internalized the build-test-deploy flow
- ⚙️ **Keeper of the Green Build** - You adopted the fast-feedback mindset

**🛠️ Skills Unlocked**:
- **Pipeline Design** - Sequence stages so failures surface cheaply
- **Continuous Integration Discipline** - Merge small, merge often, keep it green

**🔓 Unlocked Quests**:
- GitHub Actions Basics - Build pipelines with workflows, jobs, and steps
- Testing Integration - Add unit, integration, and E2E gates to your pipeline
- Deployment Pipelines - Promote releases safely to production

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [GitHub Actions Basics](/quests/0101/github-actions-basics/) - Turn the concepts into real workflows

**Explore Side Adventures**:
- ⚔️ [Testing Integration](/quests/0101/testing-integration/) - Make your gates meaningful
- ⚔️ [Deployment Pipelines](/quests/0101/deployment-pipelines/) - Ship safely

### Character Class Recommendations

**💻 Software Developer**: Continue to [GitHub Actions Basics](/quests/0101/github-actions-basics/)  
**🏗️ System Engineer**: Explore [Deployment Pipelines](/quests/0101/deployment-pipelines/)  
**🛡️ Security Specialist**: Check out [Secrets Management](/quests/0101/secrets-management/)

## 📚 Resources

### Official Documentation
- [GitHub Actions Documentation](https://docs.github.com/en/actions) - The runner you will use most
- [Martin Fowler: Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html) - The canonical essay
- [Martin Fowler: Continuous Delivery vs Deployment](https://martinfowler.com/bliki/ContinuousDelivery.html) - Untangles the two CDs

### Community Resources
- [The Continuous Delivery Foundation](https://cd.foundation/) - Vendor-neutral CD practices
- [Atlassian CI/CD Guide](https://www.atlassian.com/continuous-delivery/continuous-integration) - Practical introduction
- [GitHub Actions Community Forum](https://github.com/orgs/community/discussions/categories/actions) - Ask and answer

### Learning Materials
- [Trunk Based Development](https://trunkbaseddevelopment.com/) - Why small batches keep builds green
- [Accelerate (DORA metrics)](https://dora.dev/) - The research linking CI/CD to performance

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Built and ran a pipeline on a real repository
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0101 - CI/CD & DevOps]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Unlocks:** [[GitHub Actions Basics: Workflow Automation for Modern DevOps]] · [[Testing Integration: Automated Quality Assurance in CI/CD Pipelines]] · [[Deployment Pipelines: Production Release Automation Strategies]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
