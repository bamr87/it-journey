<!-- kit: governance v0.1.0 -->
# NEW — Editorial charter for quests

- **Status:** proposed
- **Number:** NEW
- **Date:** 2026-10-30
- **Proposed by:** agent (Grok Bot, on a branch opened under bamr87 at the maintainer's request)
- **Ratified by:** _(blank until the pull request is merged)_
- **Affects:** constitution § 9 (new); PRD § 4 (NFR), § 9 (Definition of Done); features FR-ITJ-016, FR-ITJ-017
- **Supersedes:** none
- **Related:** [features/features.yml](../../../features/features.yml), [PRD.md](../../../PRD.md), `.github/instructions/quest.instructions.md`

## Context

Quests are increasingly written and expanded by AI agents in automated lanes (quest forge, perfection, fix). The constitution says how changes land (§ 4, § 6–8), but not who may author learning content, what standard it must meet, or who checks it. A wrong command in a quest teaches a beginner something false and is costly to undo. This amendment sets the editorial rules for quests: authorization, quality standards, a review pipeline, reviewer independence and corrections.

## Amendment

Add a new § 9 to [the constitution](../../constitution.md), as follows:

### § 9. Editorial charter (quests)

_Proposed by the [editorial charter amendment](editorial-charter.md). Not in force until the maintainer merges it._

#### 9.1 Authorization

An agent creates or expands a quest only from an **approved quest brief**. That is a Fleet issue stating the goal, level, prerequisites and acceptance criteria. Updates are tiered:

| Tier | Examples | Who may make it | Gate |
| --- | --- | --- | --- |
| Minor | Typos, broken links, version bumps | Any authorized agent | Automated checks only |
| Substantive | Steps, commands, concepts | An agent working from a brief | Approved brief + the full review pipeline (§ 9.3) |
| Structural | New quest lines, levels or progression changes | Needs the maintainer (Amr) | Maintainer decision before work starts |

Every change goes through a pull request, and the maintainer merges it.

#### 9.2 Quality standards

Every quest must meet these standards:

- **Runs as written:** commands and code run in a pinned, clean container, and the quest shows the expected output.
- **Freshness:** front matter records the tested tool versions and a last-verified date. A quest past its freshness window (proposed: 6 months) is flagged for re-verification.
- **Sourced:** facts are sourced to official documentation. No invented flags, options or APIs.
- **Pedagogy:** objectives, prerequisites linked to earlier quests, a hands-on exercise, a check-your-work step, and a reading level suited to the quest's level.
- **Safe:** risky steps carry safety warnings. No secrets, real or realistic, appear in examples.
- **Original:** content is original and respects licenses. Vendored content stays read-only (§ 2).
- **AI disclosure:** front matter names the author, the model, and the verifier.

#### 9.3 Review pipeline

Each substantive or structural quest change passes these stages in order:

1. **Automated checks:** front matter schema, links, runnable code blocks, prerequisite links, readability.
2. **Technical review:** a reviewer who is not the author re-runs the quest end to end.
3. **Learner test:** a fresh agent with no prior context completes the quest as a learner would.
4. **Editor:** the Content & Comms editor reviews voice, framing and fit.
5. **Merge:** the maintainer merges.

#### 9.4 Independence

- The author cannot be the reviewer or the learner tester. At least one of them uses a different model family or a different role.
- An agent reviewing a quest about its own tooling discloses that, and a second reviewer is required.
- Every review has a required **"What could go wrong for a learner"** section.
- Merged quests are re-audited at random. Reviewers with unusually high approval rates are audited too.
- lifehacker.dev covers this work as an outside press, independent of the review chain.

#### 9.5 Corrections

- A reported error becomes a Fleet work item.
- A fix carries a dated change note on the quest.
- A badly wrong quest is pulled, with a published explanation, rather than silently edited.

## Consequences

- Agents in quest lanes must refuse substantive work without an approved brief, and must route structural changes to the maintainer.
- New front matter fields will be needed: tested versions, last-verified date, and AI disclosure (author, model, verifier). The quest validator and `REQUIRED_FIELDS` in `quest_registry.py` must be updated in a follow-up PR. This amendment does not change them.
- The catalog gains two **planned** features: FR-ITJ-016 (the charter itself) and FR-ITJ-017 (its CI checks). Both link to PRD § 4 and § 9.
- Follow-ups after ratification: AGENTS.md "Quests" guidance, `.github/instructions/quest.instructions.md`, a quest-brief issue template, and the review template's "What could go wrong for a learner" section.
- A shared AI content standard for every hub site would be a **separate hub amendment** in bamr87/bamr87. It is out of scope here.

## Open questions

1. **Freshness window:** is 6 months right? Should it be per level or per tool?
2. **Learner test:** should it run on every quest, or on a sample (for example, every structural change plus a random share of the rest)?
3. **Structural-change gate:** is "maintainer decides before work starts" enough, or should a written brief approval be required too?
4. **Hub standard:** do we need a shared AI content standard at the hub level, with this charter as its it-journey profile?
5. **Required approvals:** which repo settings (required reviews, CODEOWNERS for `pages/_quests/`) should enforce the pipeline? Only the maintainer changes settings.
