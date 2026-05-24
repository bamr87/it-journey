---
title: Certifications
description: Study guides, quest lines, and reference materials for IT certifications mapped to IT-Journey's learning system.
permalink: /docs/certifications/
layout: default
categories:
- Docs
- Certifications
tags:
- certifications
- study-guide
- github
- microsoft
draft: false
lastmod: '2026-05-17T00:00:00.000Z'
date: '2026-05-17T00:00:00.000Z'
toc: true
author: IT-Journey Team
keywords:
- certifications
- study-guide
- github
- microsoft
- docs
---
# 🏆 Certification Tracks

*The Guild Hall of Credentials — where adventurers transform proven mastery into recognized titles.*

Each certification track is a curated set of quests, chronicle posts, and reference notes mapped 1:1 to official exam objectives. Study materials emphasize hands-on practice over memorization, using the same tools you'd use in production.

## Available Tracks

| Certification | Exam | Level | Quests | Posts | Notes | Status |
|---|---|---|---|---|---|---|
| [Developing in Agentic AI Systems](gh-600/) | GH-600 | Expert 🔥 | 20 | 7 | 8 | ✅ Active |

## How Certification Tracks Work

1. **Start at the hub** — each cert has a landing page with exam overview, Mermaid quest map, and ordered learning path.
2. **Follow the quest line** — quests are tagged `quest_line: <cert>` and link forward/backward. Complete them in order for maximum context.
3. **Chronicle your progress** — linked posts document real build sessions so you see the material in action.
4. **Reference the notes** — cheat-sheets, glossaries, and decision matrices live in `_notes/<cert>/`.
5. **Run the capstone** — each track ends with a capstone quest that integrates all domains and includes a self-assessment exam.

## How to Choose a Track

| If you are… | Start with… |
|---|---|
| New to AI agents but comfortable with GitHub | [GH-600 — Domain 1](gh-600/#domain-1) |
| Already shipping with Copilot and want depth | [GH-600 — Domain 2 → 5](gh-600/#domain-2) |
| Preparing for exam day in 6 weeks | [GH-600 Week-by-Week Learning Path](gh-600/learning-path/) |

## Contribute a Track

New tracks are welcome. The minimum content set is:

- A hub `index.md` with a Mermaid quest map, domain weights, and `mermaid: true` in frontmatter
- One quest per official sub-skill, placed under `pages/_quests/<level>/<slug>.md`
- A `learning-path.md`, `skills-measured.md`, and `recommended-resources.md`
- One chronicle post per domain documenting a real build session
- Quick-reference notes under `pages/_notes/<cert>/`

Open a [tracking issue](https://github.com/bamr87/it-journey/issues/new) describing the certification before submitting a PR.
