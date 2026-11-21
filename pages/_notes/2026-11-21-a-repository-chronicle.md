---
title: Replaying a repository's whole history
description: "How a once-per-commit ledger, a model used only for judgement, and two time-lapses turned six years of Git history into a presentation."
date: '2026-11-21T19:00:00.000Z'
lastmod: '2026-11-21T20:30:00.000Z'
author: bamr87
categories:
- notes
tags:
- git
- history
- archaeology
- ai
- visualization
keywords:
- git history visualization
- repository time-lapse
- git log numstat
- incremental processing
- claude code
- commit annotation
excerpt: Every commit read once, a model asked only what a commit meant, and a repository's growth played back as a file-system and front-end time-lapse.
permalink: /notes/git-archaeology/repository-chronicle/
draft: true
---
The request was simple to say and easy to get wrong: show how a repository actually evolved, from its Git history, as a presentation. Show the pages changing from a visitor's point of view and the file system growing underneath, explain the eras and what was learned, use AI where judgement is needed, and never process the same commit twice. This note records how that was built, what the first two runs found, and what worked when building it with an AI pair.

## Start from what already exists

This had been started before. IT-Journey already had [digs](/digs/): published readings of one bounded commit range each, with an evidence index per installment under `docs/git-archaeology/` and a `dig-reporter` agent. The hub's daily `git-digs.yml` workflow that fed it had been retired, with a note that if the idea came back it belonged in this repository. So the new tool lives beside the digs, in `scripts/digs/chronicle/`, and keeps their discipline: commits are the evidence, interpretation is labelled as interpretation.

Searching first saved a redesign. The facts-versus-inference rule, the "commit text is data, not instructions" rule and the place to keep evidence were all already decided.

## Read every commit once

The tool reads history with one `git log` pass that asks for both `--raw` (blob ids, statuses, renames) and `--numstat` (lines added and deleted), with merges diffed against their first parent:

```bash
git log --no-walk=unsorted --stdin -z --raw --numstat -M --root \
  --diff-merges=first-parent --no-abbrev --format='%x1e%H%x1f%P%x1f%an...'
```

One `git cat-file --batch-check` call then reads the size of every new blob. Each commit becomes one JSON line in a month shard, `commits/YYYY-MM.jsonl`, in a ledger committed under `docs/git-archaeology/chronicle/<owner>/<repo>/`. A re-run asks Git only for commits the ledger lacks. A closed month never changes, so the ledger diffs cleanly and survives the container it was built in.

Diffing merges against their first parent pays off later. Replaying the first-parent records in order rebuilds the exact tree at any mainline commit, with no further Git calls. That claim was tested, not assumed: at HEAD, the replayed tree matched `git ls-tree -r -l` for every path and blob size in both repositories, and line counts matched in a 300-file sample of each. The file-system time-lapse is built on that replay.

## Use the model only where judgement is needed

Counting lines, classifying a path by extension, spotting a `Co-Authored-By: Claude` trailer or a `[bot]` author: none of that needs a model. Saying what a commit meant does, and so does dividing six years into eras and naming what would have saved time. So the AI layer has two jobs:

- **Per-commit annotation.** Forty commits per call, each described by its subject, a body excerpt, its areas, languages and paths. The model returns a kind, an area, a one-line summary, a 0–3 significance and a few themes. Haiku read all 2,622 commits of the two repositories for about $0.41 API-equivalent (estimate).
- **The era reading.** One call per repository with a month-by-month digest built from the ledger and the annotations. Opus returns eras, transitions and hindsight lessons, each citing commits. About $0.48 for both.

Every answer is validated before it is filed. An unknown kind or a missing commit falls back to a deterministic reading labelled `heuristic`. A lesson that cites a commit the digest never showed loses the citation. Eras are made contiguous. Annotations are keyed by SHA, so a commit is annotated once, and a heuristic reading is upgraded when a model becomes available. The era reading is keyed by a hash of its input, so it is read again only when the history has grown.

The second full run of both repositories read 0 commits, made 0 model calls, rendered 0 frames and left the ledger byte-identical.

## The front end, as it was

The page time-lapse does not try to rebuild a 2021 Jekyll site with 2021 gems and a theme fetched at today's version. It renders each historical version of a page from that commit's own source: its Markdown or HTML, its front matter, the site title and navigation from that commit's `_config.yml` and `_data/navigation/`, and its images and stylesheets. Liquid is reduced to labelled placeholders. Playwright takes each screenshot with the network blocked, so a frame never depends on what a URL serves today. The result is labelled as a simulation, because it is one.

The home page needed one more idea. IT-Journey's home page today is `index.html`, born in 2026, so following that file back gives six versions. The tool asks instead which file served `/` just before the current one was born, and follows that one back too. The chain it found is `README.md` (2020) → `index.md` (2022) → `index.html` (2026): 90 versions, from a two-line README to the dark quest hero.

## The library, article by article

The file-system film shows directories. It does not show what a learning site cares about: the articles, what they are about, and the paths through them. So a second pass reads every mainline version of every article once (7,497 versions of 1,120 articles in IT-Journey's case) through one `git cat-file --batch` call, and keeps the front matter: title, tags, categories, quest level and quest type. Replaying those versions gives each article a lifeline: born, revised, moved, retired. The replay reproduces the 487 article files at HEAD exactly, and follows 633 moves, including the 2023 consolidation of the collections into `pages/`.

Tags are not topics. IT-Journey's tags were written by many hands over six years, so a model reads the tag counts and a sample of titles once and designs 11 topics for the site, from Security Wargames to AI & Agents. Haiku then files each article under one, once. That cost about $0.07, and a re-run files nothing.

The deck's Library section plays it back: every live article as a dot in its topic, colored by collection, with that week's new and retired articles beside it. Below that, the zer0-to-her0 level grid and the six character paths fill in as quests appear. Some of the history is easy to see in it: 219 wargame walkthroughs arriving in May 2026 and leaving for their own repository a month later, the last 92 posts retiring in June 2026, and 105 quest reports arriving in July 2026 once the walkthrough loop started.

## What the two histories showed

The model's headlines, which the computed numbers bear out:

- **it-journey:** "From dotfile scripts to an AI-tended, gamified IT learning quest site." 1,781 commits since 2020-07-30, active in 164 of 330 weeks, 1,999 files today. 74% of commits come from humans, 9% from humans with an AI co-author, 1% from AI agents and 16% from bots.
- **zer0-mistakes:** "A Jekyll theme grows into an AI-maintained site-building platform." 841 commits since 2024-06-05, active in 67 of 129 weeks, 2,624 files today.

Two of the lessons it drew, each tied to commits in the presentation:

- Choose a remote theme or a vendored theme up front. In it-journey, years of Sass and layout churn ended in a single deletion of about 8,000 lines when the site moved to the remote theme.
- Fix the layout of scripts and installers once, with tests first. In zer0-mistakes, the installer and scripts were each restructured two or three times.

## Working with AI on this

- **Search before you design.** Asking "has this been started before?" found the digs, their rules and a retired workflow's note about where the work belonged.
- **Put the expensive judgement behind a cache key.** A SHA for commit annotations, a hash of the input digest for the era reading. A model's reading is then data you keep, not a cost you pay again.
- **Make the cheap model do the volume.** Classifying 2,622 commits is Haiku work. Synthesis across six years is worth Opus. The split cost under a dollar in total.
- **Strip the session down for batch calls.** `claude -p` with a replaced system prompt, `--tools ""`, an empty working directory and `--max-budget-usd` cut each call's overhead to about 1,400 tokens.
- **Validate model output like user input.** Check the enum, drop citations to commits that do not exist, and fall back to something deterministic rather than failing the run.
- **Prove the replay against the source of truth.** Comparing the rebuilt tree to `git ls-tree` turned "should be right" into "is right" before anything was drawn on top of it.
- **Ask the model for the vocabulary once, then for the filing.** A taxonomy designed from the whole library, kept until you choose to redesign it, makes 1,120 small classification calls consistent with each other.
- **Read the model's JSON carefully.** An extractor that tried `[` before `{` parsed `{"topics": [...]}` as its inner array and fell back silently; a test now pins which bracket wins.
- **Label the simulation.** Saying plainly that a frame is the source rendered in a neutral shell keeps the presentation honest about what it shows.

## Try it

```bash
git fetch --unshallow                       # the chronicle needs full history
python3 scripts/digs/chronicle/chronicle.py run --repo ../your-repo --video
python3 scripts/digs/chronicle/chronicle.py show <sha> --repo ../your-repo
```

The tool, its tests and the ledger format are documented in `scripts/digs/chronicle/README.md`.
