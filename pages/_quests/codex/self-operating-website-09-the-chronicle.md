---
title: 'The Chronicle: A SessionEnd Hook That Remembers'
description: 'Make the castle remember: a SessionEnd hook that writes down what each session cost, a queue and a durable ledger, and the to_yaml round-trip hazard that silently shreds comment headers.'
date: '2026-06-28T00:00:00.000Z'
lastmod: '2026-06-28T00:00:00.000Z'
level: '1110'
difficulty: '🔴 Hard'
estimated_time: 3-4 hours
primary_technology: bash
quest_type: bonus_quest
quest_series: The Autonomous Realm
quest_line: The Self-Operating Website
quest_arc: 'The Chronicle'
skill_focus: fullstack
learning_style: project-based
author: IT-Journey Team
permalink: /quests/codex/self-operating-website-09-the-chronicle/
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
- '1110'
- bash
- bonus_quest
- automation
- ci-cd
- gamified-learning
keywords:
  primary:
  - '1110'
  - bash
  - automation
  secondary:
  - ci-cd
  - self-operating
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Completed Chapter VIII — The Cartographer
  - Comfortable with Git, branches, and pull requests
  - Basic GitHub Actions familiarity
  system_requirements:
  - A GitHub repository you own
  - Git and a text editor or IDE
  - A Claude Code OAuth token to drive the agent steps
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/codex/self-operating-website-08-the-cartographer/
  unlocks_quests:
  - /quests/codex/self-operating-website-10-the-bard-forge/
rewards:
  badges:
  - 📜 Chronicler — the retrospective hook remembers every session
  skills_unlocked:
  - 📜 SessionEnd hook + durable ledger
  - 🧠 Safe YAML round-trips that preserve comments
  progression_points: 100
  unlocks_features:
  - Continue The Self-Operating Website campaign
---

*The castle could move now — it could survey its own walls and draw its own map. But every dawn it woke with no memory of the night before. The same wisp of the same agent had walked the same corridors a hundred times, and each time it cost candles, ink, and hours, and not one of those costs was ever written down. A realm that cannot remember what it spent cannot decide what to do next.*

*So you go down to the scriptorium and appoint a Chronicler: a hook that fires the instant a session ends, and writes — quietly, durably, before the lights go out — exactly what just happened. The real-world skill is **observability for autonomous agents**: SessionEnd hooks, an append-only ledger, and the quiet data-corruption trap that lurks in every careless YAML round-trip.*

## 📖 The Legend Behind This Quest

In the old stories, a chronicler is not a hero — they are the one who survives every hero. The castle's autonomy is only as trustworthy as its record of what it did, what it cost, and what went wrong. A **SessionEnd hook** is that chronicler: a script the agent runtime invokes as a session closes, your last guaranteed chance to capture truth before the context evaporates. We will route that truth through a fast **queue** (so the hook never blocks the session shutting down) and fold it into a durable **ledger** (so the realm has a permanent memory). And we will face the Chronicler's oldest curse — the `to_yaml` round-trip that politely rewrites your file and silently shreds every comment header you wrote at the top.

## 🎯 Quest Objectives

### Primary Objectives

- [ ] Register a **SessionEnd hook** that fires reliably when a Claude Code session terminates.
- [ ] Append each session's cost and metadata to a fast **queue file** without blocking shutdown.
- [ ] Fold the queue into a durable, append-only **ledger** that survives across sessions.
- [ ] Diagnose and avoid the **`to_yaml` round-trip hazard** that destroys comment headers.

### Mastery Indicators

- [ ] You can explain *why* writing the ledger inline in the hook is the wrong design.
- [ ] You can demonstrate a YAML edit that preserves a leading comment block byte-for-byte.
- [ ] You can read the ledger back and compute total spend across N sessions.

## 🧙‍♂️ Chapter 1: The SessionEnd Hook and the Queue

### ⚔️ Skills You'll Forge

- Wiring a `SessionEnd` hook in `.claude/settings.json`
- Reading the hook's JSON payload from `stdin`
- Writing to an append-only queue without blocking session teardown

A hook is just a command the agent runtime runs at a defined lifecycle moment. `SessionEnd` is the last one — it fires as the session closes, and the runtime pipes a small JSON object to your command's **stdin** describing the session that just ended. Your job is to read that, extract what matters, and get out of the way *fast*. If your hook is slow or fragile, you make every session slower or, worse, you make shutdown flaky.

Register the hook in `.claude/settings.json`. The `command` is whatever you want run; here we point it at a script in the repo.

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/chronicle.sh" }
        ]
      }
    ]
  }
}
```

The script reads the payload from stdin and appends **one line** to a queue file. The queue is deliberately dumb — newline-delimited JSON (`.jsonl`), append-only, no parsing, no locking gymnastics. The single most important rule: **the hook must not do the expensive work.** It enqueues; something else drains.

```bash
#!/usr/bin/env bash
# .claude/hooks/chronicle.sh — SessionEnd hook: enqueue, do not process.
set -euo pipefail

QUEUE="${CLAUDE_PROJECT_DIR:-.}/.chronicle/queue.jsonl"
mkdir -p "$(dirname "$QUEUE")"

# The runtime pipes a JSON payload on stdin. Capture it; never block on it.
payload="$(cat || true)"

# Pull a couple of fields defensively; missing keys must not crash the hook.
session_id="$(printf '%s' "$payload" | jq -r '.session_id // "unknown"')"
cost="$(printf '%s' "$payload" | jq -r '.cost.total_usd // 0')"

# Append exactly one line. `>>` is the whole durability story at this stage.
printf '{"ts":"%s","session_id":"%s","cost_usd":%s}\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$session_id" "$cost" >> "$QUEUE"
```

Two design choices are load-bearing. First, **`set -euo pipefail`** so a silent failure surfaces instead of writing garbage. Second, the `// default` fallbacks in `jq` — a SessionEnd payload that lacks a field you expected should still produce a valid ledger row, not an exception that kills shutdown. The hook's contract is "always append something true, never block." Everything heavier happens downstream.

### 🔍 Knowledge Check

- [ ] Why does the hook append to a `.jsonl` queue instead of writing the final ledger directly?
- [ ] What does `set -euo pipefail` protect you from inside a lifecycle hook?
- [ ] What happens to the ledger row if the payload is missing the `cost` field, and why is that acceptable?

## 🧙‍♂️ Chapter 2: The Durable Ledger and the to_yaml Curse

### ⚔️ Skills You'll Forge

- Draining a queue into an append-only durable ledger
- Recognizing the `to_yaml` round-trip data-loss hazard
- Editing YAML in place while preserving a comment header byte-for-byte

The queue is fast but flat. The **ledger** is the realm's real memory: a structured file you can read back, sum, and reason about. A drainer — run on a schedule or at the start of the next session — reads the queue, folds new rows into the ledger, and truncates the queue. Because both files are append-only at heart, a crash mid-drain costs you at most a re-processed line, never the whole archive.

{% raw %}
```python
#!/usr/bin/env python3
"""Drain .chronicle/queue.jsonl into a durable ledger.yml, preserving header."""
import json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2] / ".chronicle"
QUEUE = ROOT / "queue.jsonl"
LEDGER = ROOT / "ledger.yml"

HEADER = (
    "# DO NOT EDIT BY HAND — appended by the Chronicle drainer.\n"
    "# Each entry is one ended session. Totals are derived, never stored.\n"
)

def load_entries(text: str) -> list:
    # Skip the comment header; entries live below a `sessions:` marker.
    body = text.split("sessions:", 1)[-1] if "sessions:" in text else ""
    return [l for l in body.splitlines() if l.strip().startswith("- ")]

if QUEUE.exists():
    existing = LEDGER.read_text() if LEDGER.exists() else ""
    rows = load_entries(existing)
    for line in QUEUE.read_text().splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        rows.append(f"  - {{ ts: {e['ts']}, session: {e['session_id']}, cost_usd: {e['cost_usd']} }}")
    # Rebuild the file: header FIRST, then the data. The header is sacred.
    LEDGER.write_text(HEADER + "sessions:\n" + "\n".join(rows) + "\n")
    QUEUE.write_text("")  # truncate the queue only after a successful write
```
{% endraw %}

Now the curse. It is tempting to load the ledger with a YAML library, append a row to the parsed object, and write it back with `yaml.dump` (or, in Ruby, `to_yaml`). **Do not.** A round-trip through a standard YAML serializer parses your file into plain data structures — and comments are not data. The serializer has nothing to write them *from*, so your carefully worded `# DO NOT EDIT BY HAND` header vanishes on the very first automated write. The file is still valid YAML. It is still "correct." It has simply, silently, forgotten why it exists.

```ruby
# THE CURSE — never do this to a file with a comment header:
require "yaml"
data = YAML.load_file("ledger.yml")     # comments are dropped here, invisibly
data["sessions"] << { "ts" => Time.now.utc.iso8601, "cost_usd" => 0.12 }
File.write("ledger.yml", data.to_yaml)  # writes valid YAML with NO header
```

The cure is to treat the header as text you own and never feed through the serializer. Reconstruct the file by **concatenating a constant header string with the serialized body**, exactly as the Python drainer above does — header first, always, on every write. If you genuinely need a round-trip that keeps comments, reach for a comment-preserving library (`ruamel.yaml` in Python), but for an append-only ledger the concatenation pattern is simpler and bulletproof: the serializer never touches the header, so it can never shred it.

### 🔍 Knowledge Check

- [ ] What exactly does a standard `to_yaml` / `yaml.dump` round-trip lose, and why is the file still "valid" afterward?
- [ ] In the drainer, why is `QUEUE.write_text("")` placed *after* the ledger write succeeds?
- [ ] Name two cures for the comment-loss hazard and when you'd choose each.

## 🔁 Reproduce It

This chapter is anchored to a real merged branch on the reference build, where the Chronicle was forged session by session:

- **[bamr87/lifehacker.dev#47](https://github.com/bamr87/lifehacker.dev/pull/47)** (`bamr87/lifehacker.dev@dd3ad2996`) — introduced the SessionEnd hook that captures each session's cost on shutdown.
- **[bamr87/lifehacker.dev#50](https://github.com/bamr87/lifehacker.dev/pull/50)** (`bamr87/lifehacker.dev@35e2ed113`) — added the fast append-only queue so the hook enqueues instead of processing inline.
- **[bamr87/lifehacker.dev#51](https://github.com/bamr87/lifehacker.dev/pull/51)** (`bamr87/lifehacker.dev@acc508a1a`) — built the drainer that folds the queue into a durable ledger.
- **[bamr87/lifehacker.dev#52](https://github.com/bamr87/lifehacker.dev/pull/52)** (`bamr87/lifehacker.dev@542dee167`) — fixed the `to_yaml` round-trip hazard that was silently shredding the ledger's comment header.

## 🎮 Mastery Challenge

**Objective:** Run three sessions and prove the realm remembers all three — with its header intact.

- [ ] After three SessionEnd events, `ledger.yml` contains exactly three `- ` entries and the queue is empty.
- [ ] The `# DO NOT EDIT BY HAND` header survives every drain, byte-for-byte, after all three sessions.
- [ ] A one-line script reads the ledger and prints the correct **total** `cost_usd` across all sessions.

## 🎁 Rewards & Progression

- **Badge:** 📜 Chronicler — the retrospective hook remembers every session
- **Skills unlocked:** 📜 SessionEnd hook + durable ledger · 🧠 Safe YAML round-trips that preserve comments
- **+100 XP**

## 🗺️ Quest Network

```mermaid
graph LR
  A[VIII · The Cartographer] --> B[IX · The Chronicle]
  B --> C[X · The Bard Forge]
```

## 🔮 Next Adventures

- **Next chapter:** [The Bard Forge](/quests/codex/self-operating-website-10-the-bard-forge/) — the realm learns to compose, not just remember.
- **Campaign hub:** [The Self-Operating Website](/quests/codex/self-operating-website/)

## 📚 Resource Codex

- [Claude Code hooks reference](https://docs.claude.com/en/docs/claude-code/hooks) — the lifecycle events, including SessionEnd, and the JSON payload contract.
- [GitHub Actions: scheduled workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule) — for draining the queue on a cadence.
- [jq manual](https://jqlang.github.io/jq/manual/) — for the defensive `// default` field extraction in the hook.
- [ruamel.yaml documentation](https://yaml.readthedocs.io/en/latest/) — the comment-preserving alternative when you truly need a round-trip.

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Self-Operating Website]]
**Previous:** [[The Cartographer: A Map the Castle Draws Itself]]
**Next:** [[The Bard Forge: Where the Realm Composes]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
