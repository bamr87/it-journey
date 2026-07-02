---
section: quest
title: Quests
voice_profile: quest-fantasy
personas: [learner, contributor]
permalink: /quests/
accent: purple
collection: quests
---

# Quests — Section Guide

> Governs the whole `pages/_quests` collection (resolved via
> `_registry.yml › collection_defaults`). Voice/values live in `_data/brand/`.
> **Structure** is owned by [`quest.instructions.md`](../../../.github/instructions/quest.instructions.md)
> and enforced by `quest_validator.py` — this guide is the *voice* layer only.

## Audience

Learners climbing the 4-bit ladder (0000 → 1111) and contributors authoring new
quests. They want an adventure that still teaches a real, verifiable skill.

## Voice profile

`quest-fantasy` (see `../voice.md`). Second person, imperative, playful, heavily
fantasy-framed ("wield", "spell", "rank up"). **Emoji are on-brand and are not
policed for quests** — the fantasy framing (🎯 ⚔️ 🏆 🧙) is expected.
Fantasy vocabulary comes from the [Codex Glossary](/quests/codex/glossary/) —
the naming canon: no synonyms for terms it already names; new coinages land
there first.

## Tone

Energetic and motivating; never gatekeeping. A `n00b` should feel invited. Keep the
fantasy in service of the skill — the learner must finish able to *do* the thing,
not just enjoy the story.

## Structure

Owned by `quest.instructions.md` + `.frontmatter/templates/quests.md`: the
`## 🎯 Quest Objectives` section, platform paths, chapters, validation criteria,
rewards, and the quest-network position. Don't restate those rules here — follow
them.

## Do / Don't

- **Do:** frame real commands as spells/abilities; give checkpoints and clear
  "you've leveled up" moments; keep code blocks language-tagged and runnable.
- **Don't:** let flavor bury the task; gatekeep; use empty hype as if it were
  flavor. ("comprehensive", "seamless", "revolutionary" still read as hype even in
  a fantasy — `powerful` is relaxed for quests as genuine flavor.)

## Example openings

- "Your terminal is a spellbook you haven't opened yet. This quest teaches your
  first five incantations — and what each one really does."
- "Level 0100 unlocked. Time to containerize your first app and earn the
  Shipwright badge."

## Section taxonomy

Categories/tags follow the quest taxonomy in `.frontmatter/database/taxonomyDb.json`
(binary `lvl-XXXX` tags, technology tags). Quests cap at 10 tags.
