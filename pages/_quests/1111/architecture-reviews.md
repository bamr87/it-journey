---
title: 'Architecture Reviews: ADRs and Trade-off Facilitation'
author: IT-Journey Team
description: Run effective architecture and design reviews. Learn to facilitate trade-off discussions, write Architecture Decision Records, and lead reviews without ego.
excerpt: Facilitate design reviews, write ADRs, and lead trade-off discussions well
preview: images/previews/architecture-reviews-adrs-trade-off-facilitation.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1111'
difficulty: 🔴 Hard
estimated_time: 3-4 hours
primary_technology: architecture
quest_type: main_quest
quest_series: Leadership Mastery
quest_line: The Crown of Mastery
quest_arc: The Architect-King's Ascension
quest_dependencies:
  required_quests:
  - /quests/1111/career-advancement/
  recommended_quests:
  - /quests/1111/tech-speaking-writing/
  - /quests/1011/security-fundamentals/
  unlocks_quests: []
skill_focus: architecture
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Experience designing or building non-trivial systems
  - Comfort reasoning about trade-offs (latency, cost, complexity)
  - Completion of Tech Speaking and Writing (recommended)
  system_requirements:
  - A Markdown editor for ADRs and review notes
  - A real or recent design to review
  skill_level_indicators:
  - You can hold an architecture in your head and critique it fairly
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - One ADR written and one review agenda prepared
  skill_demonstrations:
  - Can write an ADR with context, decision, and consequences
  - Can facilitate a review that critiques the design, not the author
  knowledge_checks:
  - Understands what belongs in an ADR
  - Can name trade-off axes for a system design
permalink: /quests/1111/architecture-reviews/
categories:
- Quests
- Architecture
- Hard
tags:
- '1111'
- architecture
- main_quest
- adr
- design-review
- trade-offs
- gamified-learning
keywords:
  primary:
  - '1111'
  - architecture
  - main_quest
  secondary:
  - adr
  - design-review
  - trade-offs
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1111 (15) Quest: Main Quest - Architecture Reviews'
rewards:
  badges:
  - 🏆 Keeper of the Blueprints - Recorded decisions future builders will thank you for
  - 🛡️ Master of the Round Table - Facilitated a review that critiqued ideas, not people
  skills_unlocked:
  - 🛠️ Architecture Decision Records (ADRs)
  - 🧠 Trade-off Facilitation
  progression_points: 90
  unlocks_features:
  - Completion of the Level 1111 Leadership & Innovation quest line
layout: quest
---
*Greetings, Master adventurer. You stand at the capstone of the Crown. The grandest fortresses in the realm were never raised on a single mind's whim - they were debated at a round table where the wisest builders weighed every wall, every gate, every trade of stone for speed. This final quest, **Architecture Reviews**, teaches you to lead that round table: to facilitate a design review that makes the design stronger, to record decisions so future builders need not relitigate them, and to do it all without your ego on the table.*

*Whether you are reviewing a teammate's proposal or chairing a design forum for a whole org, this adventure forges the architect-king's most subtle art - making a group of smart, opinionated people arrive at a better answer together.*

## 📖 The Legend Behind This Quest

*The legendary round tables of old were not about the strongest knight winning the argument. They were about the kingdom getting the wisest decision - one that survived after the knights who made it had ridden on. The kingdoms that endured wrote their decrees down, with the reasons, so that a century later no one tore down a wall without knowing why it was built.*

*An architecture review is that round table; an Architecture Decision Record (ADR) is that durable decree. This quest teaches you to facilitate the conversation and to capture the decision so it outlives the meeting - and the team.*

## 🎯 Quest Objectives

By the time you complete this epic journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Running a Design Review** - Facilitate a review that improves the design and respects the author
- [ ] **Writing ADRs** - Record context, the decision, and its consequences durably
- [ ] **Trade-off Facilitation** - Surface the real trade-offs and drive the group to a choice
- [ ] **Reviewing Without Ego** - Critique ideas, not people, and let the best idea win

### Secondary Objectives (Bonus Achievements)
- [ ] **Pre-Reads That Work** - Run reviews where people arrive having actually read
- [ ] **Asking, Not Telling** - Use questions to lead authors to see issues themselves
- [ ] **Tracking ADR Status** - Manage decisions through accepted, deprecated, and superseded

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain what belongs in an ADR (and what doesn't)
- [ ] Facilitate a review that ends in a clear, recorded decision
- [ ] Name the trade-off axes for a given system design
- [ ] Give hard design feedback the author thanks you for

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Experience designing or building non-trivial systems
- [ ] Comfort reasoning about trade-offs (latency, cost, complexity, consistency)
- [ ] Completion of [Tech Speaking and Writing](/quests/1111/tech-speaking-writing/) (recommended)

### 🛠️ System Requirements
- [ ] A Markdown editor for ADRs and review notes
- [ ] A real or recent design you can review
- [ ] Optional: a `docs/adr/` directory in a repo to store decisions

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can hold an architecture in your head and critique it fairly
- [ ] You can disagree with a design without attacking its author
- [ ] Ready for 3-4 hours of focused, hands-on work

## 🌍 Choose Your Adventure Platform

*Decisions belong in version control, next to the code they govern. Set up an ADR home.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Store ADRs in the repo; adr-tools automates numbering and templating
brew install adr-tools
adr init docs/adr
adr new "Use PostgreSQL for the primary datastore"
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Without adr-tools, a simple convention works fine
New-Item -ItemType Directory -Force docs\adr
"# ADR-0001: <title>" | Out-File docs\adr\0001-record-architecture-decisions.md
git add docs\adr; git commit -m "docs: start ADR log"
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Install adr-tools or just use a numbered-file convention
sudo apt install -y npm && npm install -g adr-log   # optional tooling
mkdir -p docs/adr
echo "# ADR-0001: Record architecture decisions" > docs/adr/0001-record-architecture-decisions.md
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Keep ADRs in the same repo as the code so they're reviewed in PRs
# A pull request IS your async architecture review — comment on the ADR.
git add docs/adr && git commit -m "docs: propose ADR-0002 for review"
```

</details>

## 🧙‍♂️ Chapter 1: Running the Review - Facilitation, Not Domination

*A design review is a facilitation problem disguised as a technical one. The goal is the best decision for the system, not the loudest voice in the room. Your job as facilitator is to make the design better while keeping the author whole.*

### ⚔️ Skills You'll Forge in This Chapter
- Running a review with a pre-read and an agenda
- Critiquing the design, not the designer
- Driving to a clear, recorded outcome

### 🏗️ The Review Playbook

```text
BEFORE (the pre-read does most of the work):
  - Author circulates the design doc/ADR 48h ahead.
  - Reviewers read it AND leave async comments before the meeting.
  - Meeting is for the disagreements, not for reading aloud.

DURING (a tight agenda):
  1. Author states the problem + the decision they propose (5 min, no slides war)
  2. Walk the OPEN QUESTIONS and the contested comments (the bulk of the time)
  3. Surface trade-offs explicitly — "what do we give up if we pick this?"
  4. Drive to one of: ACCEPT / ACCEPT-WITH-CHANGES / NEEDS-REWORK
  5. Name the decision-maker and record the decision before you leave

AFTER:
  - Update the ADR with the decision and the dissent.
  - Track action items with owners.
```

The cardinal rule: **critique the design, not the designer.** "This caching layer adds a consistency risk" is feedback; "you didn't think about consistency" is an attack. Frame everything as about the artifact:

```text
❌ "You always over-engineer this."
✅ "This design has three moving parts where one might do — what does the
    extra complexity buy us?"
❌ "That won't scale."
✅ "At 10x today's traffic, where does this design hit its first wall?"
```

Lead with **questions, not verdicts.** Asking "what happens to in-flight requests during a deploy?" lets the author discover the gap themselves - far more durable than you announcing it. A review where the author leaves owning the improvements is a review that worked.

### 🔍 Knowledge Check: Running the Review
- [ ] Why does the pre-read do most of the work?
- [ ] Rewrite "that won't scale" as a question about the design
- [ ] What three outcomes should a review drive toward?

### ⚡ Quick Wins and Checkpoints
- [ ] **Reframed feedback**: You turned one "you" critique into an "it" critique
- [ ] **Built an agenda**: You wrote a review agenda centered on open questions

## 🧙‍♂️ Chapter 2: Architecture Decision Records - Decisions That Outlive the Meeting

*The decision is worthless if it evaporates when the meeting ends. An ADR is a small, immutable record of one architecturally significant decision: the context, the choice, and the consequences. Six months later it answers "why on earth did we do it this way?"*

### ⚔️ Skills You'll Forge in This Chapter
- The ADR format
- What is "architecturally significant"
- Managing ADR status over time

### 🏗️ The ADR Template

The widely-used Michael Nygard format - keep each ADR short and immutable (supersede, never edit):

```markdown
# ADR-0007: Use event sourcing for the orders service

- Status: Proposed | Accepted | Deprecated | Superseded by ADR-0012
- Date: 2026-06-14
- Deciders: <names>

## Context
The forces at play: requirements, constraints, and the problem. State the
facts and pressures that make a decision necessary — NOT the solution yet.
"We need a full audit trail of every order state change for compliance, and
our current CRUD model loses history on update."

## Decision
The choice, in active voice: "We will use event sourcing for the orders
service, storing each state change as an immutable event."

## Consequences
The results — good AND bad. Be honest about the costs.
- (+) Complete, queryable audit trail; time-travel debugging.
- (+) Natural fit for the read/write split we already planned.
- (-) Higher complexity; team must learn event-sourcing patterns.
- (-) Eventual consistency on read models; rebuilds are slow at scale.

## Alternatives considered
- Plain CRUD + audit table: simpler, but audit drifts from truth.
- Temporal tables: less code, but weaker for complex projections.
```

**Architecturally significant** means the decision is *costly to reverse* and *affects multiple components or teams*: your datastore, a public API contract, a language or framework, a consistency model, an auth approach. Do not ADR trivia ("we named the variable `x`"); do ADR the doors that are hard to walk back through.

Manage **status** over time. ADRs are immutable history: when a decision changes, you do not edit ADR-0007 - you write ADR-0012 that *supersedes* it, and mark 0007 "Superseded." The chain of ADRs becomes the architecture's memory.

### 🔍 Knowledge Check: ADRs
- [ ] What three sections form the heart of an ADR?
- [ ] What makes a decision "architecturally significant"?
- [ ] Why supersede an ADR instead of editing it?

## 🧙‍♂️ Chapter 3: Trade-off Facilitation - Making the Costs Visible

*Every architecture decision is a trade. The facilitator's highest skill is making the trade *explicit* - so the group chooses with eyes open instead of arguing past each other about unstated priorities.*

### ⚔️ Skills You'll Forge in This Chapter
- Naming the trade-off axes
- Surfacing hidden priorities
- Driving a contested decision to a fair close

### 🏗️ The Trade-off Toolkit

Most architecture arguments are really disagreements about *which axis matters most*. Make the axes explicit:

```text
Common trade-off axes:
  Latency        vs  Throughput
  Consistency    vs  Availability        (the CAP reality)
  Simplicity     vs  Flexibility
  Cost           vs  Performance
  Speed-to-ship  vs  Long-term maintainability
  Build          vs  Buy
  Coupling       vs  Duplication
```

When a review stalls, it is usually because two people are silently optimizing different axes. Surface it: *"It sounds like you're prioritizing time-to-ship and you're prioritizing maintainability. Which does THIS project actually need most?"* The argument dissolves once the real priority is named.

A lightweight **trade-off matrix** turns opinion into a comparable choice:

```text
Option   | Latency | Cost | Complexity | Team familiarity | Reversible?
---------|---------|------|------------|------------------|------------
A (chosen)|  Good   | Med  |   Low      |     High         |   Yes
B        |  Best   | High |   High     |     Low          |   No
C        |  OK     | Low  |   Low      |     High         |   Yes
```

Then connect it back to the vision and the reversibility rule from earlier quests: spend the group's deliberation budget on the irreversible, high-stakes choices; let the reversible ones be decided fast and revisited if wrong. End every contested decision by naming the decision-maker, recording the choice and the dissent in the ADR, and asking everyone to **disagree and commit**.

### 🔍 Knowledge Check: Trade-offs
- [ ] Name two trade-off axes for a system you've built
- [ ] How do you unstick a review where two people argue past each other?
- [ ] Why record the dissent in the ADR, not just the decision?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Write an ADR
**Objective**: Write a complete ADR for a real decision using the template.

**Requirements**:
- [ ] Context that states the forces, not the solution
- [ ] A decision in active voice
- [ ] Honest consequences, both positive and negative

**Validation**: Someone reading it in a year would understand why you chose this.

### 🟡 Intermediate Challenge: Facilitate a Review
**Objective**: Run (or design) a design review for a real proposal.

**Requirements**:
- [ ] A pre-read circulated in advance with async comments
- [ ] An agenda built around open questions and trade-offs
- [ ] A recorded outcome: accept / accept-with-changes / needs-rework

**Validation**: The author leaves owning the improvements, not bruised by them.

### 🔴 Advanced Challenge: Facilitate a Contested Trade-off
**Objective**: Drive a genuinely contested architecture decision to a fair close.

**Requirements**:
- [ ] A trade-off matrix comparing at least three options
- [ ] The competing priorities named out loud
- [ ] A recorded decision with the dissent captured and a disagree-and-commit

**Validation**: The losing side commits fully, because the trade-off was made fairly and visibly.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Keeper of the Blueprints** - You recorded decisions future builders will thank you for
- 🛡️ **Master of the Round Table** - You facilitated a review that critiqued ideas, not people

**🛠️ Skills Unlocked**:
- **Architecture Decision Records (ADRs)** - Decisions that outlive the meeting
- **Trade-off Facilitation** - Make the costs visible, then choose

**🔓 Unlocked Quests**:
- You have reached the capstone of Level 1111. Loop back to deepen any pillar of the Crown of Mastery.

**📊 Progression Points**: +90 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 You have completed the Leadership & Innovation quest line - the highest keep of the realm. Revisit any quest to go deeper.

**Explore Side Adventures**:
- ⚔️ [Technical Leadership](/quests/1111/technical-leadership/) - Apply reviews to a team you lead
- ⚔️ [Tech Speaking and Writing](/quests/1111/tech-speaking-writing/) - Sharpen the docs your reviews depend on

### Character Class Recommendations

**💻 Software Developer**: Revisit [Innovation and R&D](/quests/1111/innovation-rnd/) to pressure-test new bets  
**🏗️ System Engineer**: Return to [Technical Leadership](/quests/1111/technical-leadership/) to lead design forums  
**🛡️ Security Specialist**: Apply reviews to [Security Fundamentals](/quests/1011/security-fundamentals/) threat models

## 📚 Resources

### Official Documentation
- [Michael Nygard - Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) - The original ADR format
- [adr.github.io - ADR organization](https://adr.github.io/) - Tooling, templates, and the community
- [AWS - the ADR process (prescriptive guidance)](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/welcome.html) - A cloud vendor's ADR playbook

### Community Resources
- [Architecture Decision Records (adr-tools)](https://github.com/npryce/adr-tools) - CLI for managing ADRs
- [ThoughtWorks Technology Radar on ADRs](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records) - Why lightweight ADRs work
- [Will Larson - Architecture review processes](https://lethain.com/scaling-consistency/) - Scaling reviews across an org

### Learning Materials
- [Fundamentals of Software Architecture - Richards & Ford](https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/) - Trade-off thinking in depth
- [The art of the design review (Square/Block engineering)](https://developer.squareup.com/blog/) - Real-world review culture

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Wrote a complete ADR with honest consequences
- [ ] ✅ Facilitated (or designed) a design review with a recorded outcome
- [ ] ✅ Built a trade-off matrix for a contested decision
- [ ] ✅ Explored the resource library
- [ ] ✅ Completed the Level 1111 Leadership & Innovation quest line

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1111: Leadership & Innovation]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Career Advancement: IC vs Management Tracks, Leveling, and Negotiation]]
**Related quests:** [[Technical Leadership: Leading Without Authority and Setting Tech Vision]] · [[Tech Speaking and Writing: RFCs, Design Docs, and Talks That Persuade]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
