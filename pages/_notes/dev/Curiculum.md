---
title: Curriculum
updated: 2026-06-13 00:00:00+00:00
created: 2024-02-13 19:49:02+00:00
date: '2024-02-20T09:39:19.000Z'
draft: false
description: 'The IT-Journey curriculum philosophy: you cannot teach what you do not know, so build to teach — and the sequence that follows from that.'
---

You don't know what you can't teach.

That's the governing constraint. If you cannot explain a concept clearly enough for someone else to act on it, you don't actually understand it — you've just memorized enough to get through the task.

## What This Means in Practice

The IT-Journey curriculum is built backwards from teaching. Every topic gets documented at the point where it could be explained to someone with one level less experience. That documentation becomes the evidence that understanding happened.

This creates a useful filter: if a topic can't be documented clearly, it's not finished yet. The guide becomes the test.

## The Sequence

The curriculum follows a rough progression:

```
Zero → Foundation → Tools → Projects → Specialization
```

**Zero** — The starting point. Identity, environment setup, and the mental model for how everything connects. No prerequisites. See [Start](/notes/zero/start/).

**Foundation** — The skills that underlie everything else:
- Command line (Bash basics, file system navigation, pipes)
- Version control (Git: commit, branch, merge, remote)
- Networking (IP, DNS, HTTP — enough to debug a connection issue)
- Text editing (at minimum, survive in Vim; preferably, configure VS Code)

**Tools** — The daily-driver environment:
- A terminal that doesn't slow you down
- An editor with language support
- A way to take and find notes
- A CI/CD pipeline for at least one project

**Projects** — The unit of learning. Topics studied without a project attached fade within weeks. Every section of the curriculum has at least one associated project.

**Specialization** — The branch points:
- System administration → infrastructure, monitoring, automation
- Development → languages, frameworks, design patterns
- Data & Analytics → Python, SQL, notebooks, pipelines
- Security → CTFs, wargames, defensive tooling

## What Gets Documented

Not everything makes it into the curriculum. The selection criteria:

1. **Used more than once** — one-off commands don't earn a page
2. **Non-obvious** — anything that required more than five minutes of debugging is worth documenting
3. **Teachable** — if the explanation would confuse a reader one level below, rewrite it

The backlog lives in [Project List](/notes/dev/projects/project-list/). Topics that clear all three criteria get promoted to draft posts and eventually published.

## Related

- [Notes: Take Good Notes](/notes/dev/take-good-notes/)
- [Notes: Start](/notes/zero/start/)
- [Notes: Project List](/notes/dev/projects/project-list/)
