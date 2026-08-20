# Perfection loop vs. the video it produces — a side-by-side run

A record of running the quest-perfection loop over one main quest and comparing what the **loop** reports with what the **video** shows, so it is clear what each medium is for and where they must agree.

**Run:** slice `game-developer/0001` (the ledger's own priority pick), main quest **CSS Styling Basics: Selectors, the Box Model & Layout** (`pages/_quests/0001/css-styling-basics.md`), Linux path, 2026-08-20.

## The loop, stage by stage

| Stage | Tool | Result |
|---|---|---|
| Select | `ledger.py select --priority` | `game-developer/0001` — worst/oldest not-perfect slice |
| Plan | `walkthrough_plan.py --priority --window 5` | 5 linked quests, rotating window 1/6 of 26 |
| Step plan | `quest_steps.py --env os=linux` | 15 blocks → 12 applicable, 3 other-platform |
| Walk + capture | `stack_capture.mjs` | 12 executed (12 passed, 0 failed), 22 screenshots |
| Evidence | (emitted) | score 100%, verdict `pass`, `executed: true` |
| Ledger | `ledger.py update` | slice coverage 10/26; slice verdict stays `fail` (aggregate of earlier runs), `perfect: false` |
| Video | `walkthrough_video.mjs` | 109.8 s, 3-pane whole-stack recording |

The ledger update was run to exercise the loop and then **reverted** — this was a local session, not CI-sealed evidence, and the committed progress ledger should only record runs the workflow minted.

## Where the two agree — and must

Both sides derive from the *same* sealed evidence file, so their numbers are identical by construction:

| Fact | Loop evidence | Video |
|---|---|---|
| Steps executed | 12 | 12 (`12 ✓`) |
| Failures | 0 | 0 (`0 ✗`) |
| Not applicable | 3 (macOS, Windows, Cloud paths) | 3 (`3 ∅`), listed on the verdict card |
| Score / verdict | 100% · `pass` | shown on the verdict card |
| Findings | 3 skipped steps, each with its reason | same 3, in `findings.json` + the outro |

That parity is the point: the video can never flatter a run the evidence does not support, because it renders *from* the evidence rather than alongside it.

## Where they differ — and why you want both

| | The loop report | The video |
|---|---|---|
| **Audience** | maintainers, the fix lane | learners, and reviewers judging "does this quest work?" |
| **Shows** | verdicts, coverage math, per-quest history across runs | what actually happened, visually, in order |
| **Answers** | "is this slice converging toward perfect?" | "does the thing the quest promises actually appear on screen?" |
| **Scope** | the whole slice (5 quests, 26 in the level) | one quest, end to end |
| **Regression value** | ledger deltas over time | 22 screenshots — a visual diff of the built UI |

The sharpest example from this run: the loop reports `12 passed` for the CSS quest. Only the video shows **that the card grid actually reflows 1 → 2 → 3 columns** across mobile, tablet and desktop — the thing the chapter is *about*. Conversely, only the ledger knows this quest is 1 of 26 in a slice whose aggregate verdict is still `fail` from earlier runs. Neither medium replaces the other.

## What the video captures now (the whole stack)

Every applicable step is photographed in the sandbox, and the recording shows three surfaces at once:

- **Docs pane** — the rendered quest page from the live site, scrolling in step with the run.
- **Browser pane** — the frontend the learner is building, re-rendered after every step. 22 screenshots: 12 desktop, 5 tablet, 5 mobile — the responsive steps are captured at all three viewports and displayed side by side, because that *is* the lesson.
- **Terminal pane** — the real command, its real exit status, and a DOM/box-model probe (`.lead 300×62px, border-box, pad 16px`) standing in for the DevTools inspection the quest asks for.

Chapters come from the quest's own headings (17 of them), so the video's timeline matches the document's structure.

## Findings this run surfaced

1. **3 steps not applicable** — the macOS, Windows and Cloud paths on a Linux sandbox. Correctly classified rather than failed, with the reason recorded.
2. **Working-directory fidelity bug (fixed)** — the quest's `cd ~/css-quest` did not carry across steps, so files landed beside the project folder instead of inside it. `stack_capture.mjs` now propagates the shell's resulting directory, and the sandbox tree matches what the quest tells the learner to create.
3. **Corpus-wide rendering bug (fixed)** — fenced code inside `<details>` was never parsed (no `markdown="1"`), so every platform snippet rendered as literal backticks. See `ENVIRONMENT_MATRIX.md`.

Findings 2 and 3 are exactly the class of defect this framework exists to catch: both were invisible in the prose and obvious the moment a machine walked the quest and photographed the result.

## Reproducing

```bash
python3 scripts/quest/walkthrough_plan.py --priority --ledger .quests/ledger.json --window 5 --json walk-plan.json
python3 scripts/quest/quest_steps.py pages/_quests/0001/css-styling-basics.md --env os=linux --json steps.json
node scripts/quest/stack_capture.mjs --steps steps.json --sandbox .sandbox --out captures --evidence walk-evidence.json
node scripts/quest/walkthrough_video.mjs --plan walk-plan.json --evidence walk-evidence.json --out videos
```

In CI the same sequence runs inside `quest-video.yml`, with the evidence minted by the sealed execute-engine step.
