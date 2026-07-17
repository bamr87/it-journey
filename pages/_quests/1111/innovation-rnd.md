---
title: 'Innovation and R&D: Experimentation and Technical Bets'
author: IT-Journey Team
description: 'Drive engineering innovation. Learn structured experimentation, the three-horizons portfolio model, and how to manage risky technical bets responsibly.'
excerpt: Drive innovation with structured experiments and a balanced portfolio of bets
preview: images/previews/innovation-and-rnd-experimentation-tech-bets.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1111'
difficulty: ⚔️ Epic
estimated_time: 4-6 hours
primary_technology: leadership
quest_type: main_quest
quest_series: Leadership Mastery
quest_line: The Crown of Mastery
quest_arc: The Architect-King's Ascension
quest_dependencies:
  required_quests:
  - /quests/1111/building-technical-communities/
  recommended_quests:
  - /quests/1111/technical-leadership/
  unlocks_quests:
  - /quests/1111/architecture-reviews/
  - /quests/1111/career-advancement/
skill_focus: innovation
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Experience shipping production systems
  - Comfort reasoning about uncertainty and risk
  - Completion of Technical Leadership (recommended)
  system_requirements:
  - A document tool for experiment briefs and a bet portfolio
  - Access to a real problem space to run experiments against
  skill_level_indicators:
  - You want to create new value, not just maintain existing systems
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - One experiment brief and a three-horizons portfolio mapped
  skill_demonstrations:
  - Can write a falsifiable hypothesis with a kill criterion
  - Can balance a portfolio across the three horizons
  knowledge_checks:
  - Understands the build-measure-learn loop
  - Can distinguish a reversible bet from an irreversible one
permalink: /quests/1111/innovation-rnd/
categories:
- Quests
- Innovation
- Epic
tags:
- '1111'
- innovation
- main_quest
- experimentation
- research
- portfolio
- gamified-learning
keywords:
  primary:
  - '1111'
  - innovation
  - main_quest
  secondary:
  - experimentation
  - research-and-development
  - tech-bets
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1111 (15) Quest: Main Quest - Innovation and R&D'
rewards:
  badges:
  - 🏆 Arcane Researcher - Ran a disciplined experiment to a clear result
  - 🛡️ Master of the Gambit - Managed a portfolio of technical bets
  skills_unlocked:
  - 🛠️ Hypothesis-Driven Experimentation
  - 🧠 Innovation Portfolio Management
  progression_points: 100
  unlocks_features:
  - Continued progress through the Level 1111 Leadership & Innovation quest line
layout: quest
---
*Greetings, Master adventurer. You have mastered the known spells of the realm - but the frontier is dark, and the future belongs to those who venture into it deliberately. This quest, **Innovation and R&D**, teaches you to explore the unknown without gambling the kingdom: to run experiments that yield real answers, to balance safe bets against wild ones, and to kill your darlings when the evidence says so.*

*Whether you want to carve out 20% time for exploration, run a research spike, or steer a team's portfolio of risky bets, this adventure forges the alchemist's discipline - turning uncertainty into learning instead of expensive guessing.*

## 📖 The Legend Behind This Quest

*The alchemists of old are mocked now for chasing gold from lead - but the disciplined ones gave us chemistry. The difference between a crank and a scientist was never the wildness of the idea; it was the method. The scientist wrote down what they expected, ran the experiment, and believed the result even when it stung.*

*Innovation in engineering is the same craft. Anyone can have ideas; the master runs them through a loop of hypothesis, experiment, and honest measurement - and manages a whole portfolio of bets so that one failure never sinks the ship. This quest teaches that discipline.*

## 🎯 Quest Objectives

By the time you complete this epic journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Structured Experimentation** - Run a build-measure-learn loop with a real hypothesis
- [ ] **The Three Horizons** - Balance a portfolio across core, adjacent, and transformative bets
- [ ] **Managing Technical Bets** - Size, fund, and kill bets based on evidence, not ego
- [ ] **Creating Space for R&D** - Build the slack and psychological safety innovation needs

### Secondary Objectives (Bonus Achievements)
- [ ] **Writing a Falsifiable Hypothesis** - State what would prove you wrong before you start
- [ ] **Running a Hackathon or Spike** - Time-box exploration to produce learning fast
- [ ] **Killing a Project Well** - Stop a sunk-cost effort without shame

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain the build-measure-learn loop to another person
- [ ] Write an experiment brief with a clear kill criterion
- [ ] Map a set of initiatives onto the three horizons
- [ ] Decide to stop a project based on evidence, not feelings

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Experience shipping production systems
- [ ] Comfort reasoning about uncertainty and risk
- [ ] Completion of [Technical Leadership](/quests/1111/technical-leadership/) (recommended)

### 🛠️ System Requirements
- [ ] A document tool for experiment briefs and a bet portfolio
- [ ] A real problem space you can run experiments against
- [ ] Optional: a small budget of time (a spike, a hack day) to actually try one

### 🧠 Skill Level Indicators
This **⚔️ Epic** quest expects:
- [ ] You want to create new value, not just maintain existing systems
- [ ] You can tolerate being wrong in public and learning from it
- [ ] Ready for 4-6 hours of focused, hands-on work

## 🌍 Choose Your Adventure Platform

*Experiments need a lab notebook. Choose where you will record hypotheses and results - the record is what turns activity into learning.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# A versioned lab notebook keeps every experiment honest and reviewable
mkdir -p ~/rnd/{experiments,portfolio}
cd ~/rnd && git init
echo "# Experiment Brief: <title>" > experiments/exp-001.md
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
mkdir $HOME\rnd\experiments, $HOME\rnd\portfolio
Set-Location $HOME\rnd
git init
"# Experiment Brief: <title>" | Out-File experiments\exp-001.md
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
mkdir -p ~/rnd/{experiments,portfolio}
cd ~/rnd && git init
echo "# Experiment Brief: <title>" > experiments/exp-001.md
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Spin up throwaway environments for spikes so experiments don't touch prod
# Branch deploys, ephemeral containers, or a sandbox account keep blast radius small.
echo "Run spikes in an isolated sandbox; record results in the lab notebook."
```

</details>

## 🧙‍♂️ Chapter 1: Structured Experimentation - The Build-Measure-Learn Loop

*The enemy of innovation is not failure; it is failing without learning. A structured experiment converts a guess into knowledge by stating, before you start, exactly what would change your mind.*

### ⚔️ Skills You'll Forge in This Chapter
- The build-measure-learn loop
- Writing a falsifiable hypothesis
- Defining a kill criterion before you fall in love

### 🏗️ The Experiment Brief Template

```markdown
# Experiment: <short name>

## Hypothesis (falsifiable!)
We believe that <change> for <users> will result in <measurable outcome>.
We will know we are right if <specific, measurable signal>.

## Riskiest assumption
The one belief that, if wrong, sinks the whole idea. Test THIS first.

## The smallest test (build)
The cheapest thing that could produce a real signal — a prototype, a fake
door, a manual "wizard of oz", a single A/B cell. NOT the full feature.

## Metric (measure)
The ONE number that moves if the hypothesis is true. Define it up front so
you can't rationalize after the fact.

## Kill / pivot / persevere criteria (decide NOW)
- KILL if: <result that means stop>
- PIVOT if: <result that means try a variant>
- PERSEVERE if: <result that means invest more>

## Time box
We will spend at most <N days/weeks>, then decide.
```

The discipline is in writing the **kill criterion before you start**. Once you have invested effort, sunk-cost bias makes you reinterpret bad results as "promising." Pre-committing to "we stop if X" is how honest scientists protect themselves from their own optimism.

Test the **riskiest assumption first**. Most experiments waste weeks polishing the easy parts and never check the one belief the whole idea depends on. Find that belief; test it cheapest and soonest.

### 🔍 Knowledge Check: Experimentation
- [ ] What makes a hypothesis falsifiable?
- [ ] Why define the kill criterion before running the experiment?
- [ ] What is your current riskiest assumption, and how would you test it cheaply?

### ⚡ Quick Wins and Checkpoints
- [ ] **Wrote a hypothesis**: You stated a falsifiable belief and its signal
- [ ] **Set a kill criterion**: You pre-committed to what would make you stop

## 🧙‍♂️ Chapter 2: The Three Horizons - A Balanced Portfolio of Bets

*A team that only does safe work stagnates; a team that only chases moonshots starves. The Three Horizons model (McKinsey) keeps a portfolio balanced across time and risk.*

### ⚔️ Skills You'll Forge in This Chapter
- The three horizons of innovation
- Allocating effort across them
- Avoiding the all-eggs-one-basket trap

### 🏗️ The Three Horizons

```text
HORIZON 1 — Core (defend & extend)        ~70% of effort
   Incremental improvements to what pays the bills today.
   Low risk, near-term return. e.g. perf wins, reliability, paying down debt.

HORIZON 2 — Adjacent (emerging bets)      ~20% of effort
   New products/markets built on existing strengths. Medium risk,
   medium-term. e.g. a new service line, a platform play.

HORIZON 3 — Transformative (moonshots)    ~10% of effort
   Genuinely new, possibly disruptive. High risk, long-term, mostly fail —
   but the rare hit redefines the company. e.g. a bet on a new paradigm.
```

The exact percentages vary, but the principle holds: **fund all three.** A common failure is letting H1 (the urgent, safe work) consume 100% of capacity, leaving nothing for the future. Protect H2 and H3 capacity explicitly - because urgent always beats important if you let it.

Treat each horizon's bets differently. H1 bets are managed for delivery and efficiency. H2 and H3 bets are managed for **learning** - judge them by how much uncertainty they remove per dollar, not by whether they shipped on time.

### 🔍 Knowledge Check: Three Horizons
- [ ] Classify three current initiatives into H1, H2, or H3
- [ ] Why must H2/H3 capacity be protected explicitly?
- [ ] Why are H3 bets judged by learning rather than delivery?

## 🧙‍♂️ Chapter 3: Managing Bets and Making Space - The Long Game of Innovation

*Innovation is a portfolio, not a jackpot. The master's skill is in sizing each bet, funding it in stages, and creating the conditions where good ideas can surface and bad ones can die cheaply.*

### ⚔️ Skills You'll Forge in This Chapter
- Staged funding (real options thinking)
- Reversible vs irreversible bets
- Creating slack and safety for R&D

### 🏗️ Staged Funding and the Conditions for Innovation

Fund bets like a venture investor, in **stages tied to learning**, not all at once:

```text
Stage gate funding:
  SEED    — a few days: is the riskiest assumption even plausible?
  SERIES A— a few weeks: does a prototype move the metric?
  SERIES B— a quarter: does it work at small real scale?
  SCALE   — full investment: only after the bet has earned it.
Each gate is a real go/no-go. Most bets should die at SEED — cheaply.
```

Distinguish **reversible** bets (a new internal tool, an experiment behind a flag - bias to action, decide fast) from **irreversible** ones (a public API, a data-model commitment, a platform lock-in - slow down, demand more evidence). Spend your caution where undoing is expensive.

Innovation needs **conditions**, not just permission. The leader's job is to create:

- [ ] **Slack** - unscheduled time (20% time, hack days, "fix-it Fridays"). A team at 100% utilization cannot explore.
- [ ] **Psychological safety** - people must be able to propose a wild idea, or report a failed experiment, without punishment.
- [ ] **A learning culture** - celebrate the well-run experiment that failed as much as the one that succeeded. Punish only sloppiness, never honest negative results.
- [ ] **A killing ritual** - a blameless way to retire projects, so people stop pouring effort into the dead. Celebrate the decision to stop.

The hardest leadership act here is **killing a project well**: thanking the team, harvesting the learning, redeploying people with their heads high. Teams that cannot stop bad bets cannot afford to start good ones.

### 🔍 Knowledge Check: Managing Bets
- [ ] Why fund bets in stages rather than all at once?
- [ ] What two conditions must exist for a team to innovate?
- [ ] How do you kill a project without demoralizing the team?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Write an Experiment Brief
**Objective**: Write a full experiment brief for a real idea using the template.

**Requirements**:
- [ ] A falsifiable hypothesis with a measurable signal
- [ ] The riskiest assumption named and a cheap test for it
- [ ] Explicit kill / pivot / persevere criteria and a time box

**Validation**: A peer agrees the experiment could actually be wrong.

### 🟡 Intermediate Challenge: Map a Portfolio
**Objective**: Map your team's current work onto the three horizons.

**Requirements**:
- [ ] Each initiative placed in H1, H2, or H3
- [ ] An estimate of effort allocation across horizons
- [ ] Identification of any starved horizon and a fix

**Validation**: You can show whether the future is funded or starved.

### 🔴 Advanced Challenge: Run a Spike and Decide
**Objective**: Run a time-boxed spike on the riskiest assumption and make a real go/no-go.

**Requirements**:
- [ ] Build the smallest test that produces a signal
- [ ] Measure the pre-defined metric
- [ ] Make and record a kill / pivot / persevere decision honestly

**Validation**: You acted on the evidence, even if it killed your favorite idea.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Arcane Researcher** - You ran a disciplined experiment to a clear result
- 🛡️ **Master of the Gambit** - You managed a portfolio of technical bets

**🛠️ Skills Unlocked**:
- **Hypothesis-Driven Experimentation** - Turn guesses into learning
- **Innovation Portfolio Management** - Balance safe and wild bets

**🔓 Unlocked Quests**:
- Architecture Reviews - Pressure-test the bets that survive
- Career Advancement - Innovation is how senior engineers stand out

**📊 Progression Points**: +100 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Architecture Reviews](/quests/1111/architecture-reviews/) - Subject your bets to rigorous review

**Explore Side Adventures**:
- ⚔️ [Career Advancement](/quests/1111/career-advancement/) - Innovation as a career lever
- ⚔️ [Technical Leadership](/quests/1111/technical-leadership/) - Lead the teams that innovate

### Character Class Recommendations

**💻 Software Developer**: Continue to [Architecture Reviews](/quests/1111/architecture-reviews/)  
**🏗️ System Engineer**: Explore [Career Advancement](/quests/1111/career-advancement/)  
**🛡️ Security Specialist**: Advance to [Technical Leadership](/quests/1111/technical-leadership/)

## 📚 Resources

### Official Documentation
- [The Lean Startup methodology](http://theleanstartup.com/principles) - Build-measure-learn, from Eric Ries
- [McKinsey - The Three Horizons of Growth](https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/enduring-ideas-the-three-horizons-of-growth) - The portfolio model
- [Google's "20% time" and X moonshot factory](https://x.company/) - Innovation structure at scale

### Community Resources
- [Strategyzer - Testing Business Ideas](https://www.strategyzer.com/library/testing-business-ideas) - A library of experiment types
- [First Round Review - innovation essays](https://review.firstround.com/) - Practitioner stories on R&D
- [Atlassian ShipIt (hackathon playbook)](https://www.atlassian.com/company/shipit) - How to run a 24-hour innovation sprint

### Learning Materials
- [The Innovator's Dilemma - Clayton Christensen](https://www.hbs.edu/faculty/Pages/item.aspx?num=46) - Why incumbents miss disruption
- [Pretotyping - Alberto Savoia](https://www.pretotyping.org/) - The cheapest possible experiments

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Wrote an experiment brief with a kill criterion
- [ ] ✅ Mapped a portfolio across the three horizons
- [ ] ✅ Ran (or designed) a spike and made an honest decision
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1111: Leadership & Innovation]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Prerequisites:** [[Building Technical Communities: Events, Governance, and Inclusion]] **Unlocks:** [[Architecture Reviews: Running Reviews, ADRs, and Trade-off Facilitation]] · [[Career Advancement Strategies: Growing from Engineer to Leader]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
