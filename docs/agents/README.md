# Agent Evaluation & Tuning (GH-600 Domain 4, implemented)

How this repository grades its agents with **machine-verifiable signals**,
diagnoses failures instead of re-running them, and tunes instructions like
code. This directory is the Domain 4 convention the fleet operates under;
the campaign that teaches it is
[Chapter IV — The Oracle Rubric](https://it-journey.dev/quests/1010/agentic-codex-04-evaluation-and-tuning/),
and the full domain→artifact map is
[GH-600 in the Wild](https://it-journey.dev/notes/gh-600/implemented-in-it-journey/).

## The rubric: machine-verifiable gates (no vibes)

Every agent-produced change is graded by deterministic signals — never by the
model's own opinion of its work:

| Signal | Source | Gate |
|---|---|---|
| Quest content quality ≥ 70% | `scripts/quest/quest_audit.py` (tier-1 score) | `quest-validation` required check |
| Brand voice / no spelling drift | `scripts/ci/brand_lint.py` | `brand-gate` required check — drift **blocks auto-merge** |
| Content-only diff (no smuggling) | `scripts/ci/classify_changes.py` | `content-auto-merge` refuses mixed PRs |
| Frontmatter contract | `scripts/validation/frontmatter-validator.py` | `frontmatter-validation` required check |
| Generated data freshness | `make quest-data` diff check | `quest-fix` M2 safety rail hard-fails on stale data |
| Fix actually helped | tier-1 score + brand lint + sandbox commands, before vs after | quest-fix **deterministic keep/revert gate** |

The keep/revert gate is the purest Domain 4 artifact in the repo: the
quest-fixer's edit is kept **only** if the deterministic signal improved —
the model never grades its own work.

## Failure handling: RCA before re-run

Re-running a failed agent without understanding it manufactures intermittent
failures that never get fixed. When a fleet run fails:

1. Pull the forensic trail: `gh run download <RUN_ID> --dir ./forensics/run-<RUN_ID>`
2. Classify the failure by **layer** (reasoning / tool misuse / permissions /
   context drift / environment / completion).
3. Drive it to a root cause with 5-Why using [`rca-template.md`](rca-template.md).
4. Ship the prevention, and record it in the instruction changelog below.

## Tuning: instructions are code

Changes to agent behavior land in `.claude/agents/*.md`, `.claude/skills/`,
`AGENTS.md`, or `.github/copilot-instructions.md` — versioned, reviewed, and
logged in [`instructions-changelog.md`](instructions-changelog.md) with the
reason and the measured (or pending) outcome. One variable at a time;
baseline before, measure after. The weekly `agent-audit.yml` fleet audit is
the standing review that keeps instructions, registry, and reality aligned.
