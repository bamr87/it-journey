---
title: "Your Style Guide Belongs in Git as Data, Not a PDF"
description: "Hot take: a brand style guide nobody can lint is a brand style guide nobody follows. Put voice, tone, and banned words in version control as data."
date: 2026-06-22T12:00:00.000Z
lastmod: 2026-06-22T12:00:00.000Z
author: bamr87
categories: [DevOps]
tags: [content-governance, devops, automation, brand]
keywords: [style guide as code, content governance, brand as data, docs as code]
section_guide: devops-news-muse
excerpt: "A style guide nobody can lint is a style guide nobody follows. Ship it as data, not a PDF."
permalink: /posts/style-guide-as-a-data-file/
draft: false
---

## 📄 The PDF nobody opens twice

Most teams write a brand style guide once, export it to a PDF, and never look at it
again. 🤷

Here's the take: **if a machine can't read your style guide, neither will your
team.** Tone, banned words, canonical spellings, per-section voice — those are
*data*, and data belongs in version control next to the content it governs.

We just moved IT-Journey's brand into a `_data/brand/` tree: values, voice
profiles, a glossary of discouraged words, and a guide per section. The CMS engine
reads it and flags drift in the daily worklist — a misspelled product name, a
banned hype word, a how-to that forgot its verify step — the same way a linter
flags an unused import. No meeting required, no PDF to remember.

The payoff isn't tidiness. It's that the rule and the enforcement live in the same
repo, so the guide can't quietly rot while the writing drifts.

Read how it's wired in the [branding governance plan](https://github.com/bamr87/it-journey/blob/main/docs/cms/BRANDING_GOVERNANCE_PLAN.md).

> From zer0 to her0: your first style guide can be a PDF. Your tenth should be a
> data file your tools actually enforce. ⚙️
