---
section: devops
title: DevOps
voice_profile: practitioner-chronicle
personas: [contributor, practitioner]
permalink: /news/devops/
accent: teal
---

# DevOps — Section Guide

> Voice, tone, and values live in the central store (`_data/brand/`). This guide
> states only what is *specific* to DevOps. Don't restate the brand values or
> voice pillars here.

## Audience

Contributors and working practitioners (see `../personas.yml`) who ship and
operate software — they arrive wanting reproducible steps and the gotcha nobody
documented, not a definition of CI/CD.

## Voice profile

`practitioner-chronicle` (see `../voice.md`). **Section delta:** lean harder on
reproducible commands; every claim shows the command and the result behind it.

## Tone

Pragmatic and evidence-first — "the deploy that didn't page anyone at 3am".
Past tense for session chronicles (debugging a workflow); imperative for runbooks.
Honest about what broke (DFF applied to writing): show the red build, the cause,
the fix.

## Structure

Inherits the `posts.instructions.md` body skeleton. **Required:** a **Verify**
step (a heading or **Verify** label with the expected output) — the CMS engine
flags devops posts that omit it. Emphasis lands on Implementation + Results.

## Do / Don't

- **Do:** name exact tool/runner versions; link the canonical doc once (DRY);
  show the failing output before the fix.
- **Don't:** marketing adjectives ("powerful CI"); unverified "fastest pipeline"
  claims; happy-path-only walkthroughs.

## Example openings

- "The Azure deploy failed three times before the workflow turned green. Here's
  the one setting that fixed it."
- "Our GitHub Actions cache was silently invalidating every run. Forty wasted
  minutes later, the fix was one line."

## Section taxonomy

Preferred categories: `DevOps`, `Infrastructure`, `Automation`, `CI/CD`.
Preferred tags: `ci-cd`, `github-actions`, `docker`, `azure`, `automation`,
`deployment` (from `.frontmatter/database/taxonomyDb.json`).
