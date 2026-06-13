---
title: Take good notes
updated: 2026-06-13 00:00:00+00:00
created: 2024-02-03 19:42:48+00:00
date: '2024-02-20T09:39:19.000Z'
draft: false
description: 'Working note on note-taking: thoughts are materialized when written down, and centralizing them via Joplin, GitHub, and Jekyll keeps them findable.'
---

Notes are thoughts materialized. An idea that lives only in your head competes with every other thought you're having. An idea on paper — or in a markdown file — can be returned to, refined, and connected to other ideas.

## The Problem With Scattered Notes

Most people use at least three systems simultaneously without realizing it: a notes app, a chat history, a browser bookmark folder. The context for a decision made six months ago is split across all three, and none of them know about the others.

The goal of this stack is to make every note findable from a single place.

## The Stack: Joplin → GitHub → Jekyll

```
Capture → Sync → Publish (optional)
Joplin     GitHub    Jekyll
```

**Joplin** handles capture. It runs on desktop and mobile, stores everything as markdown, and syncs to an S3 bucket or Joplin Cloud. Notes go in as soon as you have them — rough, unformatted, doesn't matter.

**GitHub** is the ground truth. Joplin notes that graduate beyond personal scratch get committed to the repo. The git history becomes a timeline of your thinking.

**Jekyll** publishes what's worth sharing. A note in `_notes/` stays private by setting `draft: true`. Flip it to `false` and it appears on the site. The friction of "publishing" is almost zero, which makes it more likely to happen.

## What Makes a Note Worth Keeping

Three questions before committing anything:

1. **Will I search for this?** If you can reconstruct it faster than finding it, skip it.
2. **Does it contain a decision?** Decisions with context are the most valuable notes six months later.
3. **Is there a next action?** Notes without next steps are often just deferred thinking. Add one or file it as reference-only.

## Formatting Conventions

Consistency beats perfection. A few conventions that help:

- **Frontmatter always** — `title`, `date`, `draft`, `description`. Even scratch notes.
- **One idea per file** — long notes split at natural section breaks, not crammed together.
- **Link liberally** — `[[wikilinks]]` in Joplin, relative markdown links in the repo. The connections are the value.
- **Datestamp scratch notes** — `2024-02-03-rough-ideas.md` is sortable and self-describing.

## Jupyter Notebooks as Notes

Some notes are better as code. Jupyter notebooks in `_notebooks/` sit alongside markdown notes and follow the same rules: frontmatter at the top, one concept per file, committed to the repo when they're stable enough to find again.

The notebook format earns its weight when the note includes data, charts, or code you might want to re-run. Plain markdown earns its weight for everything else.

## Related

- [Notes: Project List](/notes/dev/projects/project-list/)
- [Notes: Curriculum](/notes/dev/curiculum/)
- [Docs: Jekyll Setup](/docs/jekyll/)
