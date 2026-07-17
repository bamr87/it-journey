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
```

**Evidence** = the `report.aggregate()` JSON from `test/quest-validator/agentic_validate.py`: it carries `results[].quest{path,slug,level}`, `results[].verdict` (pass/warn/fail), `results[].overall`, `results[].verdict_obj{executed, commands[{command, status, detail}], recommendations[{priority, area, suggestion}], summary}`, and top-level `total / scored / errored / average / counts / truncated`.

## The loop (mirrors `cms-daily-loop` / `issue-autopilot`)

Daily, for every character path: walk the highest-priority not-yet-perfect `(character, level)` slice → open a **separate content-only fix PR** addressing the walkthrough's VERIFIED issues → auto-merge when green → track progress in the committed ledger → repeat "until perfect".

1. **Plan** — `walkthrough_plan.py` picks the slice; `agentic_validate.py` plays
   it end-to-end in the sandbox and emits `walk-evidence.json`.
2. **Record** — `ledger.py update` merges the evidence, recomputes `perfect`,
   and (on the walkthrough report PR) commits `ledger.json` + `DASHBOARD.md`.
3. **Fix** — when not perfect and the budget allows, the fixer opens ONE
   `auto:content` quest-fix PR addressing only VERIFIED issues.
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
