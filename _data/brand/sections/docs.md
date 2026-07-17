---
section: docs
title: Docs
voice_profile: reference
personas: [practitioner, learner]
permalink: /docs/
accent: secondary
collection: docs
---

# Docs — Section Guide

> Governs the `pages/_docs` collection (resolved via
> `_registry.yml › collection_defaults`), excluding vendored read-only content
> (any upstream content carrying `source_repo`/`source_url`, which is never
> rewritten). Voice/values live in `_data/brand/`. Structural rules:
> [`docs.instructions.md`](../../../.github/instructions/docs.instructions.md).

## Audience

Practitioners and learners who are mid-task and want the answer fast — a command, a config snippet, a cheatsheet row — not a narrative.

## Voice profile

`reference` (see `../voice.md`). Terse, scannable, answer-first. Minimal emoji (docs are looked up, not read cover to cover; the engine keeps a low emoji band).

## Tone

Neutral and precise. Correct and current beats exhaustive. State the command and its expected result; link the upstream source rather than reproducing it (DRY).

## Structure

Owned by `docs.instructions.md`. Favor tables, lists, and copy-paste-ready command blocks over prose. Every code block carries a language tag. Lead each section with the thing the reader is looking for.

## Do / Don't

- **Do:** put the answer first; show expected output; link the canonical source.
- **Don't:** narrative throat-clearing; hype adjectives ("comprehensive",
  "powerful", "seamless"); walls of prose where a table would do.

## Example openings

- "Reset a detached HEAD: `git switch -`. Below: when each recovery command
  applies."
- "Liquid date filters, with the format string each one expects."

## Section taxonomy

Follow the docs taxonomy in `.frontmatter/database/taxonomyDb.json` (`Guides`, `Cheatsheet`, `Reference`, technology tags). Vendored read-only docs (carrying `source_repo` / `source_url`) keep their upstream attribution and are out of scope.
