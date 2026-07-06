---
title: 'The Mana Ledger: Budgets, Windows, and Coverage'
description: 'Teach your loop to survive its own appetite: mana budgets sized to real rate limits, date-rotated windows that sweep big sets a few items a day, cross-run coverage that certifies only a complete sweep, and a Watchtower digest to scry it all.'
date: '2026-07-06T00:00:00.000Z'
lastmod: '2026-07-06T00:00:00.000Z'
level: '1010'
difficulty: '🔴 Hard'
estimated_time: 2-3 hours
primary_technology: python
quest_type: main_quest
quest_series: The Autonomous Realm
quest_line: The Ouroboros Loop
quest_arc: 'The Mana Ledger'
skill_focus: devops
learning_style: hands-on
author: IT-Journey Team
permalink: /quests/1010/ouroboros-loop-05-the-mana-ledger/
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
- '1010'
- python
- main_quest
- monitoring
- automation
- gamified-learning
keywords:
  primary:
  - '1010'
  - rate-limits
  - rotating-windows
  secondary:
  - coverage
  - monitoring
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Sealed evidence in your loop (Chapters I–IV)
  - Python basics — dicts, dates, modulo
  system_requirements:
  - Your potion-book repository
  - Ten or more potions on the shelf (add filler recipes — the point is scale)
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/1011/ouroboros-loop-04-the-sealed-evidence/
  unlocks_quests:
  - /quests/1101/ouroboros-loop-06-the-fixers-oath/
rewards:
  badges:
  - ⏳ Mana Warden — the sweep fits the budget; coverage certifies the whole
  skills_unlocked:
  - ⏳ Budgeting iteration against real rate limits
  - 🌀 Date-rotated windows — sweep N items per turn, no gaps, no overlap
  - 🧾 Cross-run coverage — certify a set only when every member passed, fresh
  - 🔭 Watchtower digests — one consolidated report per run
  progression_points: 120
  unlocks_features:
  - Continue The Ouroboros Loop campaign
---
*Every spell draws mana, and every portal meters it. The realm's engine forgot this once: told to walk six curriculum slices, it planned **every** quest in each — 26 here, 26 there, 109 in one night — and three hours in, the mana ran dry. The trials began refusing mid-batch. Five of six slices died. The cure was not a bigger mana pool; it was an older discipline: **do less per turn, remember across turns, and certify only the whole.** Today your loop learns to budget, to sweep in windows, and to keep the kind of ledger that can honestly say "perfect".*

*The real-world skills: sizing autonomous work to rate limits and human review speed, date-rotated windowing over large sets, cross-run coverage accounting (the difference between "this run passed" and "everything is verified"), partial-result resilience, and consolidated reporting.*

> 🧭 **Campaign note:** Level `1010` is Monitoring & Observability — the Watchtower. A budget you cannot scry is a budget you will discover the hard way.

## 📖 The Legend Behind This Quest

*The post-mortem of the mana drought read like all good ones: no villain, just arithmetic. Six slices × up to 26 trials × minutes per trial, on a subscription token with an hourly allowance. The ninth trial of the first slice succeeded; the tenth was refused; every trial after was refused; the engine — back then — threw the nine good verdicts away with the batch. Three laws were carved that week: **a budget file the planner obeys** (walk at most N per slice per turn), **a rotating window** so tomorrow walks the next N, and **a coverage ledger** so a slice is only "perfect" when every member has passed, recently, across however many turns it took. And one mercy: a run interrupted mid-batch keeps the verdicts it already earned.*

## 🎯 Quest Objectives

By the end of this quest you will:

- [ ] **Write a budget file** — caps the loop reads, humans edit, and comments explain
- [ ] **Upgrade rotation to windows** — from "one item per day" to "the next N of M per day", gap-free
- [ ] **Accumulate cross-run coverage** — per-item verdicts with freshness, overwritten on re-check
- [ ] **Compute "perfect" honestly** — full coverage + all passing + fresh, in code, from the ledger
- [ ] **Raise a Watchtower digest** — one consolidated summary per run, not one report per item

## 🗺️ Quest Prerequisites

- 📋 Chapters I–IV complete
- 📋 Grow your shelf to 10+ potions so windowing has something to window

## 🧙‍♂️ Chapter 1: The Budget File and the Rotating Window

Budgets belong in a **file**, not in code — the knob-board a human tunes without touching Python:

```yaml
# budget.yml — the loop's mana policy (humans edit; the planner obeys)
caps:
  window_size: 3          # check at most N potions per turn — sized to your rate limit
  coverage_days: 21       # a verdict counts toward "perfect" only this long
```

Then upgrade Chapter I's picker from one item to a **window** — the same modular idea, one level up:

```python
# scripts/pick.py — print today's WINDOW of potions (date-rotated, deterministic).
import datetime
import math
import pathlib
import sys

import yaml

caps = yaml.safe_load(open("budget.yml"))["caps"]
n = caps["window_size"]
potions = sorted(pathlib.Path("potions").glob("*.md"))
if not potions:
    sys.exit("the shelf is empty")

num_windows = math.ceil(len(potions) / n)
index = datetime.date.today().toordinal() % num_windows
for p in potions[index * n:(index + 1) * n]:
    print(p)
```

Dry-run the sweep math before trusting it — `num_windows` consecutive days must cover every potion exactly once:

```bash
python3 - <<'PY'
import datetime, math, pathlib, subprocess
potions = sorted(pathlib.Path("potions").glob("*.md"))
n = 3
days = math.ceil(len(potions) / n)
seen = []
base = datetime.date.today().toordinal()
for d in range(days):
    idx = (base + d) % days
    seen += [str(p) for p in potions[idx*n:(idx+1)*n]]
print(f"{days} days sweep {len(set(seen))}/{len(potions)} potions, no overlap: {len(seen) == len(set(seen))}")
PY
```

One battle-note from the real build: the plan job and any re-planning job must use the **same date**, pinned once and passed along — two jobs computing "today" across a midnight boundary walk two different windows.

### 🔍 Knowledge Check
- [ ] Your shelf has 10 potions, window 3. Which window runs on ordinal day 40? On day 44?
- [ ] Why `% num_windows` on the day ordinal instead of `% len(potions)` like Chapter I?

## 🧙‍♂️ Chapter 2: Coverage — the Difference Between "Passed" and "Verified"

A windowed loop must never confuse *this turn passed* with *the shelf is verified*. Coverage is a per-item map with freshness; "perfect" is computed over the **whole set**:

```python
# scripts/ledger.py — merge today's verdicts; certify only the full, fresh sweep.
import datetime
import json
import pathlib
import sys

import yaml

caps = yaml.safe_load(open("budget.yml"))["caps"]
today = datetime.date.today()

p = pathlib.Path("ledger.json")
data = json.loads(p.read_text()) if p.exists() else {"coverage": {}}
cov = data["coverage"]

# argv: alternating potion/status pairs from today's window
pairs = sys.argv[1:]
for potion, status in zip(pairs[::2], pairs[1::2]):
    cov[potion] = {"status": status, "date": today.isoformat()}   # re-check OVERWRITES

# Prune stale verdicts — old truth is not truth:
fresh = {
    k: v for k, v in cov.items()
    if (today - datetime.date.fromisoformat(v["date"])).days <= caps["coverage_days"]
}
data["coverage"] = fresh

shelf = {str(x) for x in pathlib.Path("potions").glob("*.md")}
covered = shelf & set(fresh)
passing = {k for k in covered if fresh[k]["status"] == "pass"}
data["perfect"] = bool(shelf) and covered == shelf and passing == shelf
data["summary"] = f"{len(passing)}/{len(shelf)} passing, {len(covered)}/{len(shelf)} covered"

p.write_text(json.dumps(data, indent=2) + "\n")
print(data["summary"], "perfect:", data["perfect"])
```

The design rules hiding in those 30 lines — each one carved by a real failure:

- **Re-checks overwrite.** When Chapter VI's fixer repairs a potion, its next walk flips `fail → pass` and the fix *sticks* in the ledger.
- **Freshness expires.** A verdict from last season certifies nothing; `coverage_days` must comfortably exceed one full sweep (`num_windows` days) plus a fix cycle.
- **`perfect` is computed here** — in deterministic code, from sealed evidence, over the full denominator. Never from a golem's report, never from one good window.
- **Partial turns still count.** If a rate limit kills your turn after two of three checks, record the two — that is real coverage tomorrow's math builds on.

### 🔍 Knowledge Check
- [ ] Coverage says `9/10 covered, 9/9 passing`. Is the shelf perfect? What is the missing tenth telling you?
- [ ] Why must `coverage_days` exceed `num_windows` in days? What happens at exactly equal?

## 🧙‍♂️ Chapter 3: The Watchtower Digest

Six slices once meant six report pull requests — each carrying a sibling copy of the ledger, each conflicting with the other five the moment one merged. The cure: **one consolidated digest per run.** Yours, in miniature, appended to the run's summary page:

```bash
python3 - >> "$GITHUB_STEP_SUMMARY" <<'PY'
import json
d = json.load(open("ledger.json"))
print("### 🔭 Watchtower — this turn\n")
print("| potion | status | checked |")
print("|---|---|---|")
for k, v in sorted(d["coverage"].items()):
    icon = "✅" if v["status"] == "pass" else "❌"
    print(f"| `{k}` | {icon} {v['status']} | {v['date']} |")
print(f"\n**{d['summary']}** — perfect: {'🏆 yes' if d['perfect'] else '🔁 not yet'}")
PY
```

Scry the two numbers that matter every morning: **coverage climbing** toward the denominator, and **passing converging** toward coverage. When both meet the shelf size — 🏆.

## 🔁 Reproduce It

The full-scale battle and its cure:

- PR [#438](https://github.com/bamr87/it-journey/pull/438) — `bamr87/it-journey@dca271433` (+484/−53): `--window` in the planner, `caps.max_quests_per_slice` in `.quests/budget.yml`, per-quest coverage with `coverage_days` in the ledger, breaker discipline ("a mid-sweep turn is progress, not a failed round"), and partial-evidence-on-throttle in the engine
- PR [#444](https://github.com/bamr87/it-journey/pull/444) — `bamr87/it-journey@4eefc45d7`: a real consolidated digest — six slices, one PR, a window column (`4/6 (5q)`) and a coverage column (`4/26`) per slice
- The mana drought itself: the engine's 2026-07-05 run walked 109 quests for 3h17m and auth-failed five of six slices — the arithmetic your `budget.yml` now forbids

## 🎮 Mastery Challenge

**Objective:** prove convergence end-to-end.

**Success Criteria:**
- [ ] With 10 potions and window 3, dispatch daily (or fake the date) until `coverage` shows `10/10 covered` — verify no potion was checked twice before all were checked once
- [ ] Break one potion mid-sweep, watch `perfect` stay `false` with an exact summary naming why, fix it, and watch its next window flip the ledger to `perfect: true`
- [ ] Set `coverage_days: 2` and watch certification decay — then write one sentence on how you'd choose the real value for a 26-item shelf with window 5

## 🎁 Rewards & Progression

- ⏳ **Mana Warden** — earned when a full sweep certifies under budget
- ⚡ Skills unlocked: budget files · windowed iteration · coverage accounting · run digests
- 📊 **+120 XP**

## 🗺️ Quest Network

```mermaid
graph LR
    Prev[🧾 IV · The Sealed Evidence] --> Cur[⏳ V · The Mana Ledger]
    Cur --> Next[⚖️ VI · The Fixer's Oath]
    click Prev "/quests/1011/ouroboros-loop-04-the-sealed-evidence/"
    click Next "/quests/1101/ouroboros-loop-06-the-fixers-oath/"
```

## 🔮 Next Adventures

- ⚖️ [Chapter VI — The Fixer's Oath](/quests/1101/ouroboros-loop-06-the-fixers-oath/): the loop finally earns the right to *repair* what it witnessed break
- 👑 Campaign hub: [Epic Quest: The Ouroboros Loop](/quests/codex/ouroboros-loop/)

## 📚 Resource Codex

- [GitHub Actions: job summaries](https://docs.github.com/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions#adding-a-job-summary) — the Watchtower's cheapest window
- [Python `datetime.date.toordinal`](https://docs.python.org/3/library/datetime.html#datetime.date.toordinal) — the rotation's clockwork
- [Anthropic rate limits](https://docs.claude.com/en/api/rate-limits) — the mana meter behind the drought

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph.*

**Campaign hub:** [[Epic Quest: The Ouroboros Loop]]
**Previous:** [[The Sealed Evidence]] · **Next:** [[The Fixer's Oath]]
**Level home:** [[Level 1010 - Monitoring & Observability]]
