---
title: 'Tech Speaking and Writing: RFCs, Docs, and Talks'
author: IT-Journey Team
description: Communicate technical ideas with impact. Learn technical writing, design docs and RFCs, structuring a conference talk, and persuading an audience to act.
excerpt: Write design docs and RFCs and give talks that move an audience to act
preview: images/previews/tech-speaking-and-writing-rfcs-and-talks.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1111'
difficulty: 🔴 Hard
estimated_time: 3-4 hours
primary_technology: markdown
quest_type: main_quest
quest_series: Leadership Mastery
quest_line: The Crown of Mastery
quest_arc: The Architect-King's Ascension
quest_dependencies:
  required_quests:
  - /quests/1111/technical-leadership/
  recommended_quests: []
  unlocks_quests:
  - /quests/1111/open-source-contribution/
  - /quests/1111/building-technical-communities/
skill_focus: communication
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Real technical experience to write and speak about
  - Comfort writing in Markdown
  - Completion of Technical Leadership (recommended)
  system_requirements:
  - A Markdown editor for design docs and RFCs
  - Slides tool and a way to record yourself (optional but recommended)
  skill_level_indicators:
  - You have ideas worth sharing and want them to land
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - One design doc or RFC drafted and one talk outline written
  skill_demonstrations:
  - Can structure an RFC that drives a decision
  - Can outline a talk with a single clear takeaway
  knowledge_checks:
  - Understands the BLUF principle
  - Can distinguish a design doc from an RFC
permalink: /quests/1111/tech-speaking-writing/
categories:
- Quests
- Communication
- Hard
tags:
- '1111'
- communication
- main_quest
- technical-writing
- rfc
- public-speaking
- gamified-learning
keywords:
  primary:
  - '1111'
  - communication
  - main_quest
  secondary:
  - technical-writing
  - design-docs
  - public-speaking
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1111 (15) Quest: Main Quest - Tech Speaking and Writing'
rewards:
  badges:
  - 🏆 Wordsmith of the Realm - Wrote a doc that changed a decision
  - 🛡️ Voice That Carries - Gave a talk an audience remembered
  skills_unlocked:
  - 🛠️ RFC and Design-Doc Authoring
  - 🧠 Talk Structuring
  progression_points: 90
  unlocks_features:
  - Continued progress through the Level 1111 Leadership & Innovation quest line
layout: quest
---
*Greetings, Master adventurer. You have built systems few can match - but a brilliant idea trapped inside one head changes nothing. The leaders whose names echo through the realm are those who could make others SEE what they saw. This quest, **Tech Speaking and Writing**, teaches you to turn knowledge into influence: to write a design doc that wins the room, an RFC that closes a debate, and a talk an audience actually remembers.*

*Whether you freeze at the thought of a stage or merely want your design docs to stop being ignored, this adventure forges the communicator's craft - the highest-leverage skill at the top of the technical ladder.*

## 📖 The Legend Behind This Quest

*In every age, the most powerful figures were rarely the strongest warriors - they were the ones who could stand before a council and make a hundred minds move as one. The scribe who wrote the clearest decree shaped more of the realm than the soldier who guarded the gate. Words, well-ordered, are a force multiplier no sword can match.*

*Engineering is the same. A staff engineer's leverage is mostly prose: the design docs, RFCs, and talks that align dozens of people before a single line of code is written. This quest teaches you to wield that quiet, decisive power.*

## 🎯 Quest Objectives

By the time you complete this epic journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Technical Writing Fundamentals** - Write clearly, lead with the point, and respect the reader's time
- [ ] **Design Docs and RFCs** - Structure a proposal that drives a real decision
- [ ] **Structuring a Talk** - Build a talk around one takeaway with a strong arc
- [ ] **Persuasion** - Move an audience from "interesting" to "let's do it"

### Secondary Objectives (Bonus Achievements)
- [ ] **Writing for Skim-Readers** - Make docs work for people who only read headings
- [ ] **Handling Q&A** - Field hard questions without losing the room
- [ ] **Building a Body of Work** - Turn one talk or post into a durable technical brand

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain the BLUF principle and apply it to your own writing
- [ ] Draft an RFC that gets people to agree or disagree clearly
- [ ] Outline a talk a stranger can summarize in one sentence
- [ ] Rewrite a wall of text so a skim-reader still gets it

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Real technical experience worth writing and speaking about
- [ ] Comfort writing in Markdown
- [ ] Completion of [Technical Leadership](/quests/1111/technical-leadership/) (recommended)

### 🛠️ System Requirements
- [ ] A Markdown editor for design docs and RFCs
- [ ] A slides tool (Google Slides, Keynote, reveal.js, or similar)
- [ ] A way to record yourself speaking (phone camera is fine)

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You have ideas worth sharing and want them to actually land
- [ ] You are willing to cut your own clever sentences for clarity
- [ ] Ready for 3-4 hours of focused work

## 🌍 Choose Your Adventure Platform

*Your words need a durable home. Choose where you will draft and publish.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# A versioned writing folder makes your drafts reviewable and reusable
mkdir -p ~/writing/{rfcs,design-docs,talks}
cd ~/writing && git init
echo "# RFC-001: <title>" > rfcs/rfc-001.md
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
mkdir $HOME\writing\rfcs, $HOME\writing\design-docs, $HOME\writing\talks
Set-Location $HOME\writing
git init
"# RFC-001: <title>" | Out-File rfcs\rfc-001.md
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
mkdir -p ~/writing/{rfcs,design-docs,talks}
cd ~/writing && git init
echo "# RFC-001: <title>" > rfcs/rfc-001.md
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Publish in the open: a blog repo gives your writing a public, lasting home
# reveal.js or Slidev let you keep slides in version control beside your notes.
echo "Use a static-site repo (Jekyll, Astro) for posts; reveal.js for talks."
```

</details>

## 🧙‍♂️ Chapter 1: Technical Writing - Respecting the Reader's Time

*The number-one mistake in technical writing is burying the point. Readers are busy, skeptical, and skimming. Write for them, not for the joy of your own prose.*

### ⚔️ Skills You'll Forge in This Chapter
- BLUF: Bottom Line Up Front
- Writing for skim-readers
- Cutting words without losing meaning

### 🏗️ The Core Principles

**BLUF (Bottom Line Up Front):** state your conclusion or ask in the first two sentences. Everything after is justification for those who want it. A reader should be able to act after the first paragraph.

```text
❌ Buried:  "We evaluated three queues over two weeks, considering throughput,
            operational burden, and cost. After much analysis... [400 words]
            ...therefore we recommend SQS."

✅ BLUF:    "Recommendation: adopt SQS for the events pipeline.
            It is the cheapest option that meets our throughput needs with the
            least operational burden. Details and alternatives below."
```

**Write for skim-readers.** Most people read your headings and the first sentence of each paragraph, then decide whether to slow down. Make those load-bearing:

- [ ] Headings say *what the section concludes*, not just its topic
- [ ] The first sentence of each paragraph carries the point
- [ ] Bullets and tables replace dense paragraphs where possible
- [ ] You can delete 20% of the words and lose no meaning - so do

**The omit-needless-words pass:** after drafting, hunt for "in order to" (-> "to"), "due to the fact that" (-> "because"), and every hedge ("I think maybe we could possibly"). Confidence is clarity.

### 🔍 Knowledge Check: Technical Writing
- [ ] Rewrite a buried recommendation as a BLUF
- [ ] What should a heading do beyond naming a topic?
- [ ] Which three filler phrases will you hunt and delete?

### ⚡ Quick Wins and Checkpoints
- [ ] **BLUF applied**: You moved your conclusion to the top of one doc
- [ ] **Trimmed 20%**: You deleted a fifth of the words from a paragraph

## 🧙‍♂️ Chapter 2: Design Docs and RFCs - Driving Decisions on Paper

*An RFC (Request for Comments) or design doc is how senior engineers think out loud and align a team before building. A good one turns a hallway argument into a written, reviewable, durable decision.*

### ⚔️ Skills You'll Forge in This Chapter
- The standard RFC structure
- Surfacing alternatives and trade-offs honestly
- Inviting dissent so the decision is real

### 🏗️ The RFC Template

```markdown
# RFC-NNN: <Short, declarative title>

- Status: Draft | In Review | Accepted | Rejected | Superseded
- Author(s): <name>      Reviewers: <names>
- Created: <date>        Decision by: <date>

## Summary (BLUF)
One paragraph: what we propose and why, decision-ready.

## Problem / Motivation
What hurts today, in concrete terms. Who feels it. Why now.

## Goals and Non-Goals
- Goals: <what success looks like, measurable if possible>
- Non-Goals: <what we are explicitly NOT solving here>

## Proposal
The recommended approach, in enough detail to estimate and critique.

## Alternatives Considered
| Option | Pros | Cons | Why not chosen |
| --- | --- | --- | --- |
| A (chosen) | ... | ... | — |
| B | ... | ... | ... |

## Trade-offs and Risks
What we give up, what could go wrong, how we'd detect/mitigate it.

## Rollout / Migration
How we ship it safely, and how we'd roll back.

## Open Questions
The things we genuinely don't know yet — invite the reader to weigh in.
```

The "Alternatives Considered" and "Open Questions" sections are what separate an RFC from a sales pitch. A doc that only argues for one option invites suspicion; one that honestly weighs the rejected paths earns trust - and gets approved faster.

A **design doc** is the close cousin: it leans more on architecture (diagrams, data models, sequence flows) and less on "should we?" Use an RFC when the decision is contested; a design doc when the decision is largely made and you need to align on the *how*.

### 🔍 Knowledge Check: Design Docs and RFCs
- [ ] Why include alternatives you rejected?
- [ ] When do you write an RFC vs a design doc?
- [ ] What belongs in "Non-Goals" and why does it matter?

## 🧙‍♂️ Chapter 3: Talks That Persuade - One Idea, Well Delivered

*A talk is not a document read aloud. Its constraint is brutal: the audience hears it once, in order, with no rewind. So a talk must do one thing - land a single, memorable idea.*

### ⚔️ Skills You'll Forge in This Chapter
- The single-takeaway rule
- The problem-tension-resolution arc
- Handling Q&A without losing the room

### 🏗️ The Talk Outline Template

```text
TITLE: <promises the takeaway>

THE ONE TAKEAWAY (finish this sentence):
  "If the audience remembers ONE thing, it's: ___________"

OPEN (hook, ~10%):
  A story, a surprising number, or a painful problem the audience shares.
  Goal: make them lean in within 60 seconds.

TENSION (the problem, ~25%):
  Make the problem vivid and relatable BEFORE offering the solution.
  No one cares about your answer until they feel the question.

RESOLUTION (your idea, ~45%):
  The insight/approach. 2-3 supporting points, each with a concrete example
  or demo. One idea per slide; slides are billboards, not teleprompters.

CLOSE (~10%, callback to the open):
  Restate the ONE takeaway. End with a clear "go do this Monday" action.

Q&A:
  Repeat each question before answering (for remote/recording + clarity).
  "I don't know, but here's how I'd find out" beats bluffing every time.
```

The most common talk failure is *too much content*. Cut ruthlessly: a talk that lands one idea beats a talk that mentions ten. Rehearse out loud, on a timer, at least three times - your slides will change once you hear yourself.

### 🔍 Knowledge Check: Talks
- [ ] State the single takeaway for a talk you could give today
- [ ] Why must tension come before resolution?
- [ ] What is the best way to answer a question you can't answer?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: BLUF a Real Doc
**Objective**: Take a real message, doc, or PR description you wrote and rewrite it BLUF-first.

**Requirements**:
- [ ] Conclusion or ask in the first two sentences
- [ ] Headings that state conclusions
- [ ] 20% fewer words than the original

**Validation**: A reader can act after the first paragraph.

### 🟡 Intermediate Challenge: Draft an RFC
**Objective**: Write a real RFC for a decision your team faces, using the template.

**Requirements**:
- [ ] At least two honestly-weighed alternatives
- [ ] Explicit non-goals and open questions
- [ ] Circulated to at least one reviewer for comments

**Validation**: A reviewer can agree or disagree clearly because the trade-offs are explicit.

### 🔴 Advanced Challenge: Outline and Record a Talk
**Objective**: Build a talk outline with one takeaway, then record a 5-minute version.

**Requirements**:
- [ ] A single, written takeaway sentence
- [ ] Problem-tension-resolution arc
- [ ] Recorded once and watched back for pacing

**Validation**: A friend who watches can state your takeaway in one sentence.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Wordsmith of the Realm** - You wrote a doc that changed a decision
- 🛡️ **Voice That Carries** - You delivered a talk an audience remembered

**🛠️ Skills Unlocked**:
- **RFC and Design-Doc Authoring** - Drive decisions on paper
- **Talk Structuring** - One idea, well delivered

**🔓 Unlocked Quests**:
- Open Source Contribution - Communicate across a public project
- Building Technical Communities - Speak and write to grow an ecosystem

**📊 Progression Points**: +90 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Open Source Contribution](/quests/1111/open-source-contribution/) - Put your writing to work in public

**Explore Side Adventures**:
- ⚔️ [Building Technical Communities](/quests/1111/building-technical-communities/) - Reach a wider audience
- ⚔️ [Architecture Reviews](/quests/1111/architecture-reviews/) - Where design docs meet live debate

### Character Class Recommendations

**💻 Software Developer**: Continue to [Open Source Contribution](/quests/1111/open-source-contribution/)  
**🏗️ System Engineer**: Explore [Architecture Reviews](/quests/1111/architecture-reviews/)  
**🛡️ Security Specialist**: Advance to [Building Technical Communities](/quests/1111/building-technical-communities/)

## 📚 Resources

### Official Documentation
- [Google Technical Writing Courses](https://developers.google.com/tech-writing) - Free, excellent fundamentals
- [Google's design doc practice (industrysketch)](https://www.industrialempathy.com/posts/design-docs-at-google/) - How a large org uses design docs
- [Rust RFC process](https://github.com/rust-lang/rfcs) - A public, mature RFC workflow to learn from

### Community Resources
- [Write the Docs community](https://www.writethedocs.org/) - The home of documentation practitioners
- [Speaking.io by Zach Holman](https://speaking.io/) - A practical guide to conference talks
- [The Architecture of Open Source Applications](https://aosabook.org/) - Models of clear technical explanation

### Learning Materials
- [On Writing Well by William Zinsser](https://www.harpercollins.com/products/on-writing-well-william-zinsser) - The classic on clear nonfiction
- [Made to Stick - Heath brothers](https://heathbrothers.com/books/made-to-stick/) - Why some ideas survive and others die

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Rewrote one doc BLUF-first
- [ ] ✅ Drafted an RFC with honest alternatives
- [ ] ✅ Outlined (and ideally recorded) a talk with one takeaway
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1111: Leadership & Innovation]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Technical Leadership: Leading Without Authority and Setting Tech Vision]]
**Unlocks:** [[Open Source Contribution: Leading and Maintaining Projects]] · [[Building Technical Communities: Growing Developer Ecosystems]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
