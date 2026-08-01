# `.quests/` — the autonomous quest-perfection loop's data layer

This directory is the **committed source of truth for "how perfect is every quest path?"** — the quest-side analogue of `.cms/` (content health) and `.issues/` (the open-issue queue). A deterministic ledger (`scripts/quest/ledger.py`) records, per **slice**, the most-recent walkthrough verdict and the running history, recomputes which slices are `perfect`, and selects the next not-yet-perfect slice to work. AI agents (the walker and the fixer) ACT on the ledger; they never re-decide the policy encoded here.

A **slice** is `"<character.key>/<level.code>"` — e.g. `"developer/0001"`. Character keys: `developer`, `system-engineer`, `security-specialist`, `data-scientist`, `digital-artist`, `game-developer`. `level.code` is a 4-bit string like `0001`. The slice id is the stable key everywhere; **never** the permalink.

## Why a dot-dir, and why *not* under `_data/quests/`

This is a dot-directory, so **Jekyll ignores it automatically** — the ledger and dashboard never ship to the built site. It deliberately lives **outside `_data/quests/`**: that directory is **registry-generated** from `scripts/quest/quest_registry.py` and is rewritten wholesale by `make quest-data`. Putting the ledger there would mean every `make quest-data` run **clobbers** it. `.quests/` is hand-/ledger-owned and survives regeneration.

## What lives here

| Path | Committed? | Produced by | Consumed by |
|---|---|---|---|
| `README.md` | ✅ | hand-edited | humans |
| `config.yml` | ✅ (source) | hand-edited | `ledger.py` (the perfect bar, selection, fix rounds) |
| `budget.yml` | ✅ (source) | hand-edited | the orchestrator (per-run backpressure) |
| `ledger.json` | ✅ | `ledger.py update` / `fix-update` | `ledger.py select` / `render`, dashboards |
| `DASHBOARD.md` | ✅ (generated) | `ledger.py render` | humans |
| `walk-plan.json` | ❌ (transient CI artifact) | `scripts/quest/walkthrough_plan.py` | the walk arm, `ledger.py update` |
| `walk-evidence.json` | ❌ (transient CI artifact) | `agentic_validate.py` `report.aggregate()` | `ledger.py update` |

**Committed vs transient.** `ledger.json`, `DASHBOARD.md`, `config.yml`, and `budget.yml` are tracked in git so progress and policy stay reviewable. `walk-plan.json` and `walk-evidence.json` are **per-run working state** — they are regenerated every run and uploaded as CI artifacts for the audit trail, not committed. (`.gitignore` here keeps the dir clean to the same effect as the `.issues/` convention.)

## The ledger (the one deterministic source of truth)

All certification math lives in **`scripts/quest/ledger.py`**. It is the only thing that decides `perfect`; agents and workflows feed it evidence and read its selections.

```bash
# Merge one slice's walk evidence, recompute perfect, append a walk event:
python3 scripts/quest/ledger.py update \
  --evidence walk-evidence.json --plan walk-plan.json \
  --mode execute|review --run-url URL --event walk

# Bump last_fixed + append a fix event (NEVER sets perfect):
python3 scripts/quest/ledger.py fix-update --slug <char>/<code> [--merged-pr N]

# Print one slice id (worst/oldest not-perfect):
python3 scripts/quest/ledger.py select --priority --json -

# Print a JSON list, one slice id per character path:
python3 scripts/quest/ledger.py select --all-paths --json -

# Rewrite .quests/DASHBOARD.md from the ledger:
python3 scripts/quest/ledger.py render

# Self-check the ledger invariants:
python3 scripts/quest/ledger.py selftest

# Reconcile two divergent ledgers (report-PR conflict resolution — the newer
# slice record wins wholesale, walk history unions, the breaker only tightens):
python3 scripts/quest/ledger.py merge --ours A.json --theirs B.json --output A.json
```

**Keeping an open report PR mergeable.** `ledger.json`, `DASHBOARD.md`, and `pages/_quest-reports/**` are rewritten wholesale by every run, so a report PR that misses its merge window conflicts with `main` the moment the next run lands. Git cannot line-merge them; the generators can:

```bash
# On the report branch — merge main and rebuild everything derived from it:
scripts/quest/refresh_report_branch.sh origin/main
```

It refuses to touch conflicts outside that generated set, so a real content conflict still reaches a human. `pr-freshness.yml` runs it automatically.

**Evidence** = the `report.aggregate()` JSON from `test/quest-validator/agentic_validate.py`: it carries `results[].quest{path,slug,level}`, `results[].verdict` (pass/warn/fail), `results[].overall`, `results[].verdict_obj{executed, commands[{command, status, detail}], recommendations[{priority, area, suggestion}], summary}`, and top-level `total / scored / errored / average / counts / truncated`.

## The loop (mirrors `cms-daily-loop` / `issue-autopilot`)

The loop runs as **two lanes on two cadences**, joined by this directory's committed ledger.

**Walk (measurement) — daily, `quest-perfection.yml`.** Walk THE single highest-priority not-yet-perfect `(character, level)` slice, record it, stop. Rotation covers the other paths over following days, because the ledger's selection key sorts by `last_run` ascending — a slice that just ran sorts last among its tier.

**Fix (repair) — every 2 days, `quest-fix-loop.yml`.** Rank the ledger, open **separate content-only fix PRs** addressing VERIFIED issues, auto-merge when green, repeat "until perfect".

These were one daily workflow that walked every path and fixed in the same run. Two things were wrong with that. The walk cost ~150 min/day (~75 h/month), and measurement showed it was almost entirely agentic engine rather than workflow overhead — setup, checkout and install were 3.9 min of a 158-minute run — so nothing but *asking for less AI work per run* could reduce it. Separately, the fix budget was recomputed on every walk only for backpressure to discard most of it, because patches were being generated far faster than one reviewer could read them. Split, measurement runs often and cheaply while repair stays paced to review speed.

1. **Plan** — `walkthrough_plan.py` picks the slice; `agentic_validate.py` plays it end-to-end in the sandbox and emits `walk-evidence.json`.
2. **Record** — `ledger.py update` merges the evidence, recomputes `perfect`, and (on the walkthrough report PR) commits `ledger.json` + `DASHBOARD.md`. The walk also uploads its sealed plan + evidence as an artifact.
3. **Fix** — on its own schedule, when not perfect and the budget allows, the fixer opens ONE `auto:content` quest-fix PR addressing only VERIFIED issues. It reuses the walk's sealed evidence **by run id** instead of re-deriving it, so a fix costs minutes rather than a second execute-engine pass. Evidence older than `caps.max_evidence_age_days` is skipped — the content may have moved under it — and left for the walk lane to re-measure.
4. **Merge** — `content-auto-merge.yml` squash-merges green content-only fix PRs.

### PR boundaries (M4)

The **fix PR** add-paths are ONLY `pages/_quests/**` + `_data/quests/**`. It carries EXACTLY `auto:content` (the string `content-auto-merge.yml` keys on) plus descriptive `auto:quest-fix` + `automated`. **`.quests/**` is NEVER added to a fix PR** — that would trip the content-only smuggle guard and could smuggle config/policy. Ledger + dashboard commits ride the **separate** read-only walkthrough report PR (labelled `quest-walkthrough` + `automated`, NOT `auto:content`).

## Staged kill switches (everything OFF by default)

The loop is dark until you opt in, switch by switch, plus Claude auth
(`CLAUDE_CODE_OAUTH_TOKEN || ANTHROPIC_API_KEY`). Each is a repo variable:

| Variable | Gates |
|---|---|
| `QUEST_PERFECTION_ENABLED` | the daily orchestrator (the whole loop) |
| `QUEST_FIX_ENABLED` | the write/fix lane (opening fix PRs) |
| `QUEST_WALKTHROUGH_ENABLED` | the walk arm (existing) |
| `CONTENT_AUTOMERGE_ENABLED` | hands-off merge of content PRs (existing) |

Turn them on in order: walkthrough → perfection (read + ledger) → fix (writes) → auto-merge (hands-off). Each later switch trusts more, so enable it only once you trust the prior stage's output.

### Why full hands-off fix auto-merge stays off

`result.verdict_obj.executed` is **model-supplied** — the model attests it ran the commands; nothing in the harness yet stamps an independent execution proof. Until a harness-stamped exec-proof exists, **full hands-off auto-merge of fix PRs stays gated** behind `CONTENT_AUTOMERGE_ENABLED` (off by default). The ledger still refuses to certify `perfect` for anything but an `execute`-mode, **non-truncated**, fully-scored run (M7) — but execute-mode alone is not a license to merge without a human in the loop.

## Safety mitigations baked into the contract

- **M1 (anti-self-grading)** — the fixer keeps an edit only when a
**deterministic** signal improves: the tier-1 structural score (`quest_validator.py`) rises or holds AND `brand_lint` stays clean AND no sandbox command regresses passed→failed. Never on the model's own "overall".
- **M2 (freshness)** — after any quest edit the fix workflow runs `make
  quest-data` and FAILS on a non-empty uncommitted `git diff _data/quests`.
- **M3 (vendored read-only)** — a deterministic step fails if any changed
  `pages/_quests/**/*.md` carries `source_repo:` / `source_url:` frontmatter.
- **M4 (.quests never in a content PR)** — see PR boundaries above.
- **M5 (PAT hard-fail)** — the fix workflow hard-fails without a PAT
  (`AUTO_PR_GITHUB_TOKEN || PAT_TOKEN`); it never falls back to `github.token`,
  so the fix PR's required checks actually fire.
- **M6 (circuit breaker)** — a slice fixed `config.fix.max_fix_rounds` times
(default 3) without becoming perfect is marked `stuck`/`needs_human` in the ledger and is no longer selected for fixing.
- **M7 (honest run)** — `perfect` requires `mode == execute` and a
non-truncated, fully-scored run; review-mode or truncated runs can never certify perfect.

## Editing the policy

- `config.yml` — the certification **bar** (`perfect.*`), `selection` strategy,
  `history.cap`, and the `fix.max_fix_rounds` circuit breaker.
- `budget.yml` — the per-run **backpressure** caps and the backlog-heavy vs
  normal behavior split.

Both are hand-edited; the ledger and dashboard are generated. Never hand-edit `ledger.json` or `DASHBOARD.md`.
