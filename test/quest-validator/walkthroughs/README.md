# Quest walkthrough session reports

This directory holds the **session reports** produced by the daily *quest walkthrough* routine — the quest-validation arm of the IT-Journey AI fleet.

Each report is the record of one `quest-walker` agent session that picked a coherent slice of the curriculum (**one character class at one binary level**), walked that *linked set of quests* end-to-end in a disposable sandbox **as if it were a learner**, ran their commands for real, and wrote down what it saw: **evidence, issues, and reasoning**. The reports are validation artifacts — they are **not published quest content** (this whole `test/` tree is Jekyll-excluded).

## How a report gets here

```
scripts/quest/walkthrough_plan.py   → picks the (character, level) slice + linked order  (deterministic)
test/quest-validator/agentic_validate.py --mode execute  → sandboxed, scored per-quest evidence
.claude/skills/quest-walkthrough    → the loop the agent follows (plan → execute → walk → report)
.claude/agents/quest-walker.md      → the agent role (read-only over content, never merges)
.github/workflows/quest-walkthrough.yml  → the daily routine (gated, opens a report PR)
```

Run it yourself:

```bash
make quest-walkthrough-plan CHARACTER=developer LEVEL=0001   # see the slice (no AI, no cost)
make quest-walkthrough     CHARACTER=developer LEVEL=0001    # full agentic walkthrough (needs claude login)
```

Omit `CHARACTER`/`LEVEL` to let the planner **date-rotate** the slice — that is how the daily workflow sweeps the whole curriculum over time.

## Session screenshots (CI artifacts)

Each CI run also captures **visual evidence** of the session and uploads it as the `quest-walkthrough-*` workflow artifact (not committed to the repo):

- `screenshots/pages/<slug>-mobile.png` + `-desktop.png` — each walked quest's
rendered page (what a learner sees), driven off the permalink with headless Chromium at a ~390px mobile and a 1440px desktop viewport.
- `screenshots/session/<slug>-terminal.png` — a terminal-styled render of the
recorded session transcript (the commands the walkthrough ran + their `passed`/`failed`/`skipped`/`reasoned` outcome), built from `walk-evidence.json`. This is a faithful render of the recorded transcript, not a raw TTY frame grab.

Produced by `scripts/quest/walkthrough_screenshots.mjs` (Playwright). Run it locally after a walkthrough with `make quest-walkthrough-screenshots` (set `BASE_URL` to a local server to screenshot un-published changes).

## File naming

```
<YYYY-MM-DD>-<character>-<level>.md
# e.g. 2026-06-29-developer-0001.md
```

## Report contract (sections every report keeps)

1. **Frontmatter** — `title`, `date`, `character`, `level`, `theme`, `tier`,
   `quest_count`, `mode` (`execute`/`review`), `overall_verdict`, `session` notes.
2. **🎯 Session Summary** — the slice, how many quests walked, headline verdict, why.
3. **🗺️ The Journey** — the ordered quest list, one line of verdict + takeaway each.
4. **🔬 Evidence** — per quest: commands actually run and their real outcome
   (`passed`/`failed`/`skipped`/`reasoned`) + snippet coverage. The proof.
5. **🐞 Issues Found** — each issue: severity · quest · where · what was observed ·
   suggested fix. "No blocking issues" is a valid, explicit result.
6. **🔗 Chain Continuity** — does the slice hold together as a learning path for this
   character: prerequisite gaps, ordering, does quest N set up quest N+1.
7. **🧠 Reasoning & Method** — what was run vs. reasoned about, the mode/limits, and
   the agent's confidence. Honest coverage is mandatory.

## Honesty rule

A report only ever claims what the session actually observed. A `passed`/`failed` comes from a command **run in the sandbox**; anything judged statically is `reasoned`. The routine is worthless the moment a report fabricates a green run — so it doesn't. Issues are reported here for a human or a content pass to act on; the walkthrough itself **never edits quest content and never merges**.
