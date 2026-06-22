---
section: devops-news-muse
title: DevOps News & Muses
voice_profile: muse-opinion
personas: [practitioner, ai-enthusiast]
permalink: /news/devops/
accent: teal
overlay_of: devops
---

# DevOps News & Muses — Section Guide

> A **format overlay**, not a folder. Muses live in `pages/_posts/devops/` but are
> written in the `muse-opinion` voice and surfaced on the `/news/` magazine
> landing. A post opts in with `section_guide: devops-news-muse`. Voice/values
> live in `_data/brand/` — only the format specifics are here.

## Audience

Practitioners and AI-augmented builders skimming the magazine for a sharp take or
a quick "what just happened and why it matters".

## Voice profile

`muse-opinion` (see `../voice.md`). First person, punchy, opinion stated early.
Moderate emoji (fits the magazine framing).

## Tone

Confident and direct — own the take, don't hedge it to death. Still honest: if the
hot take has a caveat, say it in one line, don't bury it.

## Structure

**Hook → take → one piece of evidence / one link out → zer0-to-her0 tie-back.**
~150–700 words (the CMS engine flags muses outside this band). This is the one
section that does **not** use the full tutorial skeleton or require a Verify step.

## Do / Don't

- **Do:** state the opinion in the first two sentences; cite exactly one source;
  tie it back to the reader's own journey.
- **Don't:** turn it into a tutorial; bury the lede; stack ten links; produce a
  neutral news summary with no take.

## Example openings

- "Hot take: most CI pipelines are slow because nobody owns the cache. Here's the
  one-line fix that gave us 40 minutes a run back."
- "Everyone's adding AI to their pipeline. Almost nobody's adding the human review
  step that keeps it from shipping nonsense."

## Section taxonomy

Categories: `DevOps`. Tags: a tight 2–5 from `ci-cd`, `github-actions`, `devops`,
`ai`, `automation`. Optional frontmatter: `featured: true` / `breaking: true` to
surface in the magazine header (see `pages/news.md`).
