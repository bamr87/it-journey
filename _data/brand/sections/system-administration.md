---
section: system-administration
title: System Administration
voice_profile: practitioner-chronicle
personas: [practitioner]
permalink: /news/system-administration/
accent: brown
---

# System Administration — Section Guide

> Voice/values live in `_data/brand/`. State only sysadmin-specific deltas here.

## Audience

Practitioners configuring machines and environments — WSL, dual-boot, imaging,
desktop tooling — who need steps that actually work on the stated OS.

## Voice profile

`practitioner-chronicle` (see `../voice.md`). **Section delta:** be exact about
OS/version; setup steps are unforgiving, so precision beats prose.

## Tone

Methodical and precise. Call out where a step is destructive or irreversible
(DFF) — back up first, here's what can go wrong.

## Structure

Inherits the `posts.instructions.md` skeleton. **Required:** a **Verify** step (the
CMS engine flags sysadmin posts that omit it). Use Platform Notes for OS deltas.

## Do / Don't

- **Do:** state the exact OS/build; warn before destructive steps; give the
  verify/rollback.
- **Don't:** assume one platform; "effortless setup" claims; skip the prerequisite
  that everyone forgets.

## Example openings

- "Setting up WSL is easy — until the one networking setting that silently breaks
  everything. Here's how to get it right the first time."
- "Imaging a RetroPie SD card looks simple. These three verify steps save you a
  re-flash."

## Section taxonomy

Categories: `System Administration`, `Infrastructure`. Tags: `linux`, `windows`,
`macos`, `wsl`, `networking`, `configuration`, `cross-platform`.
