<!-- kit: governance v0.1.0 -->
# 0004 — Missions

- **Status:** proposed
- **Date:** 2026-11-16
- **Proposed by:** Grok Bot (agent), at the maintainer's request
- **Ratified by:**
- **Affects:** constitution §1; PRD.md §1.1; FR-ITJ-018
- **Supersedes:** none
- **Related:** [PRD.md](../../PRD.md) §1.1

## Context

Constitution §1 was a single mission sentence or short paragraph, not one direction statement with exactly three numbered missions. The fleet rule is that every repo's constitution §1 uses that form, adopted through a numbered amendment the maintainer ratifies by merging. Mission 1 is the maintainer's own wording, adapted to this repo: provide data, tools, resources and transparency for all stakeholders, practitioners in the domain, and the general public. The ambition is the direction, not a claim that the work is already finished.

The earlier §1 text was:

> Build IT-Journey — an open-source educational platform that democratizes IT education through gamified quests, practical tutorials, and AI-enhanced learning experiences, transforming complete beginners into skilled IT professionals.

## Amendment

Retitle constitution §1 **Missions**. Replace the body of §1 with the following. Any invariants or other normative rules that already lived outside §1 are unchanged.

IT-Journey's direction is to become the ultimate open home for all things IT learning — data, tools, resources and transparency, gathered in one place that anyone can inspect and reuse.

1. **Provide data, tools, resources and transparency for all stakeholders, IT educators and professionals, and the general public.** Learners from zer0 to her0, mentors, contributors, educators, and the general public are first-class audiences. The aim is a shared, open commons: the same quests, the same tools, and the same trail of evidence for everyone.
2. **Make a complete, trusted path from complete beginner to skilled professional, taught through gamified quests, practical tutorials and AI-enhanced learning.** Hands-on adventures, a binary level path, and real commands that stay correct are the system of record; a wrong lesson is a defect, not a draft. Optional AI helps authors and learners without replacing the quest as the source of truth.
3. **Put that path in every learner's, teacher's and builder's hands.** Serve it through the open site, the quest collection, the CLI and the contributor lanes, so anyone can learn, teach, and add a quest — an open toolkit for working with all things IT learning.

These missions set the course; they do not claim the work is finished. They serve the PRD purpose in §0 and the MVP in §1: an open educational platform that democratizes IT education. The earlier mission — building IT-Journey as a gamified path from complete beginner to skilled IT professional — is absorbed into these three. Every feature must trace to them.

_Source: [../PRD.md](../PRD.md) §1.1._

## Consequences

Agents and reviewers judge fit against these three missions before inventing scope, treating them as the direction of the repo rather than a description of what already ships. The same text is added as PRD.md §1.1 so the constitution's `_Source:` line stays accurate. The PRD purpose, goals, feature catalog and invariants outside this addition are unchanged except for a new catalog entry (FR-ITJ-018) and a regenerated feature-catalog block where the repo already has one. This PR also aligns the README and AGENTS.md one-liners with the missions and links them to constitution §1.
