---
title: 'The Bard Forge: The Quest That Writes Quests'
description: 'Close the autonomy loop: a published retrospective triggers a read-only agent that mines merged-branch metadata and proposes a gamified quest to a separate repo — never mutating its source, never merging.'
date: '2026-06-28T00:00:00.000Z'
lastmod: '2026-06-28T00:00:00.000Z'
level: '1100'
difficulty: '🔴 Hard'
estimated_time: 3-4 hours
primary_technology: claude-code
quest_type: bonus_quest
quest_series: The Autonomous Realm
quest_line: The Self-Operating Website
quest_arc: 'The Bard Forge'
skill_focus: fullstack
learning_style: project-based
author: IT-Journey Team
permalink: /quests/codex/self-operating-website-10-the-bard-forge/
fmContentType: quest
layout: quest
draft: false
comments: true
mermaid: true
categories:
- Quests
- Automation
- DevOps
tags:
- '1100'
- claude-code
- bonus_quest
- automation
- ci-cd
- gamified-learning
keywords:
  primary:
  - '1100'
  - claude-code
  - automation
  secondary:
  - ci-cd
  - self-operating
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Completed Chapter IX — The Chronicle
  - Comfortable with Git, branches, and pull requests
  - Basic GitHub Actions familiarity
  system_requirements:
  - A GitHub repository you own
  - Git and a text editor or IDE
  - A Claude Code OAuth token to drive the agent steps
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/codex/self-operating-website-09-the-chronicle/
  unlocks_quests: []
rewards:
  badges:
  - 🪄 Loop Closer — turned project history into a learnable quest without mutating the project
  skills_unlocked:
  - 🪄 Metadata-mining quest proposal agent
  - 🧠 Propose-to-a-human-gate autonomy
  progression_points: 120
  unlocks_features:
  - Continue The Self-Operating Website campaign
---

*The realm has learned to watch itself, heal itself, and chronicle its own deeds. Now, in the deepest chamber of the keep, one last forge glows: the **Bard Forge**, where finished labors are hammered into stories that teach the next generation of adventurers. The Bard does not change history — it cannot wield the hammer on its own past. It can only read the runes left in the merged branches and **propose** a new quest, sliding the parchment under the door of a separate keep for a human hand to accept.*

*The real-world skill you are forging here is the most subtle automation move of all: an agent that **mines version-control metadata** (PR numbers, commit SHAs, diffstats) and emits a **proposal to a human gate in a different repository** — read-only at the source, write-nowhere-it-shouldn't, and incapable of inventing a fact it cannot cite.*

## 📖 The Legend Behind This Quest

Every quest in this campaign ended with a Chronicle — a retrospective committed to the project's history. The Bard Forge takes that Chronicle as a spark. When a retrospective lands, the Bard awakens, reads the *cold runes* of the merge (the metadata Git already recorded), and drafts a brand-new quest in a **second** repository so the original project is never touched. This is the autonomy loop closing on itself: the work a project did becomes the lesson a learner takes. The discipline that makes it safe is the same discipline a senior engineer practices — **separate the thing that proposes from the thing that decides**, and never let an automated author write a hash it didn't read.

## 🎯 Quest Objectives

### Primary Objectives

- [ ] Trigger a read-only agent from a merged retrospective using GitHub Actions `pull_request` (closed + merged) events
- [ ] Mine merged-branch metadata — PR number, head SHA, and diffstat — using only `git` and the GitHub API, never invented values
- [ ] Open a quest-proposal pull request in a **separate** repository, leaving the source repo unmodified
- [ ] Enforce a human gate so the agent proposes but never merges its own output

### Mastery Indicators

- [ ] You can explain why the agent must read its source with read-only credentials
- [ ] You can trace every fact in the proposed quest back to a real SHA or PR number
- [ ] You can describe the trust boundary between the source repo and the target repo

## 🧙‍♂️ Chapter 1: Reading the Cold Runes (Mining Merged-Branch Metadata)

### ⚔️ Skills You'll Forge

- Firing a workflow only when a PR is *actually merged*, not merely closed
- Extracting deterministic metadata from a merge with `git` and `gh`
- Treating version-control history as a read-only data source

A merge is a fact. Once a branch lands, Git has permanently recorded who changed what, the head SHA, and the diffstat. The Bard's first job is to **read** those runes — never to guess them. The cleanest trigger is the `pull_request` event filtered to the merged case, because a closed PR is not the same as a merged one.

{% raw %}
```yaml
# .github/workflows/bard-forge.yml (in the SOURCE repo)
name: Bard Forge — propose a quest
on:
  pull_request:
    types: [closed]
permissions:
  contents: read          # read-only at the source — we never write here
jobs:
  mine-and-propose:
    # Only fire when the PR was truly merged, not just closed.
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0    # full history so we can read the diffstat
      - name: Mine merged-branch metadata
        env:
          GH_TOKEN: ${{ github.token }}
        run: ./scripts/mine_merge.sh "${{ github.event.pull_request.number }}"
```
{% endraw %}

The `permissions: contents: read` line is the load-bearing rune: the source repo's token can read history but cannot push a commit, open a PR, or move a tag here. The script itself only *reads*.

```bash
#!/usr/bin/env bash
# scripts/mine_merge.sh — emit metadata as JSON. Reads only; writes nothing to the repo.
set -euo pipefail
PR_NUMBER="$1"

# The merge commit and head SHA are facts Git already recorded.
HEAD_SHA="$(gh pr view "$PR_NUMBER" --json headRefOid --jq '.headRefOid')"
MERGE_SHA="$(gh pr view "$PR_NUMBER" --json mergeCommit --jq '.mergeCommit.oid')"

# Diffstat for the merged range — also a recorded fact, never invented.
DIFFSTAT="$(git diff --shortstat "${MERGE_SHA}^" "${MERGE_SHA}")"

jq -n \
  --arg pr "$PR_NUMBER" \
  --arg head "$HEAD_SHA" \
  --arg merge "$MERGE_SHA" \
  --arg stat "$DIFFSTAT" \
  '{pr: $pr, head_sha: $head, merge_sha: $merge, diffstat: $stat}' \
  > merge_metadata.json
cat merge_metadata.json
```

Every value above came from `gh` or `git`. The Bard will later be *forbidden* to write a SHA the script did not produce — that is what makes the proposal trustworthy.

### 🔍 Knowledge Check

- [ ] Why does `if: github.event.pull_request.merged == true` matter when the event type is `closed`?
- [ ] Which `permissions:` setting guarantees the workflow cannot write to the source repo?
- [ ] Where do `head_sha` and `merge_sha` come from, and why must the agent never invent them?

## 🧙‍♂️ Chapter 2: Sliding the Parchment Under the Door (Propose to a Human Gate, Never Merge)

### ⚔️ Skills You'll Forge

- Authoring a quest from real metadata with a read-only Claude Code agent
- Opening a PR in a **separate** target repository with a scoped token
- Enforcing a human gate so the agent proposes but never decides

Now the Bard has clean runes. It drafts a quest — but the draft must live in a **different** keep. Pushing the proposal back into the source repo would let an automated author mutate the very history it just read; that loop must stay open. Instead, the agent uses a token scoped to the *target* repo (a forge repo for proposed quests) and opens a pull request there for a human to accept.

{% raw %}
```yaml
      - name: Forge a quest proposal (read-only authoring)
        uses: ./.github/actions/claude-run
        with:
          # The agent reads merge_metadata.json and the Chronicle; it may NOT
          # invent SHAs, PR numbers, or output it did not observe.
          prompt: >
            Read merge_metadata.json. Draft a gamified quest in Markdown that
            teaches what this merge accomplished. Cite ONLY the pr/head_sha/
            merge_sha present in the JSON. If a fact is missing, omit it.
          oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}

      - name: Open proposal PR in the SEPARATE quest-forge repo
        env:
          # A token scoped ONLY to the target repo — not the source.
          GH_TOKEN: ${{ secrets.QUEST_FORGE_TOKEN }}
        run: |
          gh repo clone bamr87/quest-forge target && cp quest.md target/proposed/
          cd target
          git checkout -b "proposal/pr-${PR_NUMBER}"
          git add proposed/ && git commit -m "Propose quest from merged PR #${PR_NUMBER}"
          git push origin "proposal/pr-${PR_NUMBER}"
          # Open the PR — but DO NOT merge it. A human gate decides.
          gh pr create --fill --base main --label "auto:quest-proposal"
```
{% endraw %}

Three rules make this safe, and they are the whole point of the chapter:

1. **Separate repos.** The agent reads `bamr87/lifehacker.dev`-style history and writes only to a distinct forge repo. The source is never mutated.
2. **Scoped credentials.** `QUEST_FORGE_TOKEN` can write to the target and nothing else; the source workflow's own `github.token` stays read-only.
3. **A human gate.** The agent calls `gh pr create`, never `gh pr merge`. Auto-merge is deliberately absent — a person reviews the proposed quest before it joins the codex.

This is the autonomy ceiling done right: the machine does the tedious mining and drafting; the human keeps the final say. *Propose, don't merge* is the same principle that keeps a self-healing pipeline from quietly shipping a bad fix.

### 🔍 Knowledge Check

- [ ] Why must the proposal land in a separate repository rather than the source repo?
- [ ] What is the difference between `QUEST_FORGE_TOKEN` and the source workflow's `github.token`?
- [ ] Which single missing command (`gh pr ...`) is what preserves the human gate?

## 🔁 Reproduce It

This chapter is anchored to a real merged branch in the campaign's reference build:

- **bamr87/lifehacker.dev#53** (`bamr87/lifehacker.dev@09046139b`) — the merge that wired the retrospective-to-proposal loop: a read-only mining step plus a proposal PR opened in a separate forge repo, with no auto-merge, closing the autonomy loop while keeping a human gate.

Read the squash-merge commit, find the metadata-mining step and the separate-repo proposal, and confirm for yourself that the source repository is never written to.

## 🎮 Mastery Challenge

**Objective:** Build a Bard Forge for one of your own repositories that proposes a quest from a merged PR without ever mutating the source repo.

- [ ] A merged PR triggers a workflow that produces a `merge_metadata.json` whose SHAs match `git`/`gh` output exactly
- [ ] The proposal PR is opened in a *different* repository, and `git log` on the source shows no new commits from the agent
- [ ] No `gh pr merge` exists anywhere in the workflow — every proposal waits on a human reviewer

## 🎁 Rewards & Progression

- **Badge:** 🪄 Loop Closer — turned project history into a learnable quest without mutating the project
- **Skills unlocked:** 🪄 Metadata-mining quest proposal agent · 🧠 Propose-to-a-human-gate autonomy
- **+120 XP**

You have closed the loop. The realm now teaches what it learns — and it does so without ever letting the machine rewrite its own past.

## 🗺️ Quest Network

```mermaid
graph LR
    A[IX — The Chronicle] --> B[X — The Bard Forge]
    B --> C[Campaign Hub:<br/>The Self-Operating Website]
    style B fill:#7c3aed,stroke:#4c1d95,color:#fff
```

## 🔮 Next Adventures

This is the final chapter of the campaign. Return to the hub to review the full arc, replay a chapter, or branch into a new epic:

- 🏰 **Campaign hub:** [The Self-Operating Website](/quests/codex/self-operating-website/)
- 📜 **Previous chapter:** [The Chronicle](/quests/codex/self-operating-website-09-the-chronicle/)

## 📚 Resource Codex

- [Events that trigger workflows — `pull_request`](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#pull_request) — the `closed` event and the `merged` field.
- [Assigning permissions to jobs (GitHub Actions)](https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs) — how to lock a workflow to `contents: read`.
- [GitHub CLI manual — `gh pr`](https://cli.github.com/manual/gh_pr) — `gh pr view`, `gh pr create`, and the merge command we deliberately avoid.
- [Claude Code documentation](https://docs.claude.com/en/docs/claude-code/overview) — driving the read-only authoring agent.

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Self-Operating Website]]
**Previous:** [[The Chronicle]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
