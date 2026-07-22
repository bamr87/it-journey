---
title: "Making one-paragraph-per-line universal across repos"
description: "How the oneline prose rule is enforced everywhere — CI backstop, hub auto-fix, the shared AI runner, a Claude Code hook, and a pre-commit hook."
date: 2026-07-22T00:00:00.000Z
author: IT-Journey Team
categories: [docs, tooling]
tags: [ci, prose, markdown, agents, hooks]
---

## The problem

AI agents (and humans) soft-wrap markdown prose at ~80 cols by habit. The house rule is **one paragraph per line**, enforced by the `markdown-oneline` CI gate (`tools/unwrap-prose.py --check`). Wrapped prose fails the gate — e.g. the `quest-fix` PR #534. The check is already fanned out to every repo; what was missing is *enforcement at the source* so agents stop producing it and PRs stop going red.

There is no single switch that covers every markdown-producing path across every repo — it is defense-in-depth. This page maps each layer to the shared place it lives, so "universal" means "one edit in a shared layer," not "N edits × M repos."

## Distribution mechanisms you already have

The `bamr87/bamr87` hub distributes standards two ways:

1. **Reusable workflows** — `.github/workflows/ci.yml` is a thin caller: `uses: bamr87/bamr87/.github/workflows/standard-ci.yml@main`. Edit the hub once and every repo runs the new logic on its next PR.
2. **Fanout/seed** — `standardize-fanout.yml` + `tools/fanout.sh --kit prose` copies `markdown-oneline.yml` + `unwrap-prose.py` into each repo. Edit the hub kit, re-fanout, and every repo gets the new committed copy.

Plus a shared AI chokepoint: `scripts/ai/run.sh` + `.github/actions/claude-run` — *every* AI call flows through it, and it is ported to the sibling sites.

## The layers

| Layer | Covers | Lives in (one place) | Status |
|---|---|---|---|
| 0. CI check | any wrapped prose reaching a PR, all repos | fanned-out `markdown-oneline.yml` | shipped (the backstop) |
| 1. CI auto-fix | same, but self-heals instead of failing | hub prose kit — one edit | draft below |
| 2. AI runner sweep | all AI markdown in CI, all sibling repos | `scripts/ai/run.sh` (shared) | shipped in this repo; upstream it |
| 3. Claude Code hook | all Claude markdown, every repo + session | `~/.claude/settings.json` (global) or `.claude/settings.json` (project) | config + script below |
| 4. pre-commit hook | all commits, any author | `tools/hooks/` + `core.hooksPath` | shipped in this repo; kit it |

Layer 0 stays the hard gate. Layers 1 and 3 are the recommended pair: Claude's output is clean at the source (3), and everything else self-heals in CI (1).

---

## Layer 1 — hub CI auto-fix (draft to paste into `bamr87/bamr87`)

Replace the check-only step in the hub's prose-kit `markdown-oneline.yml` with an unwrap-and-commit step. On a same-repo PR it pushes the fix back to the branch; on a fork PR or push event it falls back to failing with instructions (it cannot push there). It converges in one extra run — after the fix the tree is clean, so the follow-up run finds nothing to commit.

```yaml
name: markdown-oneline
on:
  pull_request:
    paths: ["**/*.md", "**/*.markdown"]
  push:
    branches: [main]
    paths: ["**/*.md", "**/*.markdown"]
permissions:
  contents: write            # needed to push the auto-fix back to the PR branch
concurrency:
  group: markdown-oneline-${{ github.ref }}
  cancel-in-progress: true
jobs:
  oneline:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref }}        # the PR branch, not the merge ref
          # A PAT re-triggers CI on the fix push; GITHUB_TOKEN pushes do NOT
          # re-run checks (which also prevents loops). Pick per your needs.
          token: ${{ secrets.AUTO_PR_GITHUB_TOKEN || secrets.PAT_TOKEN || github.token }}
      - uses: actions/setup-python@v5
        with: { python-version: "3.x" }
      - name: Unwrap prose — auto-commit on same-repo PRs, else check-only
        env:
          EVENT: ${{ github.event_name }}
          HEAD_REPO: ${{ github.event.pull_request.head.repo.full_name }}
          THIS_REPO: ${{ github.repository }}
        run: |
          set -euo pipefail
          python3 tools/unwrap-prose.py --write \
            --exclude '(^|/)SCHEMA\.md$' --exclude '(^|/)CHANGELOG\.md$' \
            --exclude '(^|/)pages/_quest-reports/' \
            --exclude '(^|/)test/quest-validator/walkthroughs/'
          if git diff --quiet; then
            echo "prose already one paragraph per line."; exit 0
          fi
          if [ "$EVENT" = "pull_request" ] && [ "$HEAD_REPO" = "$THIS_REPO" ]; then
            git config user.name  "github-actions[bot]"
            git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
            git commit -am "style(prose): unwrap soft-wrapped markdown (one paragraph per line)"
            git push
            echo "::notice::Auto-unwrapped soft-wrapped prose and pushed the fix to this PR."
          else
            git --no-pager diff --stat
            echo "::error::Wrapped markdown prose found. Run: python3 tools/unwrap-prose.py --write"
            exit 1
          fi
```

Tradeoff: auto-committing edits the contributor's PR and can race other automation (auto-merge). If you would rather keep the current fail-fast behavior, leave `markdown-oneline.yml` as-is and rely on Layers 3 + 4 to prevent wrapped prose from ever being committed.

---

## Layer 2 — the shared AI runner sweep (shipped here)

`scripts/ai/run.sh` now normalizes any markdown the agent changed after a successful Claude Code run (`normalize_changed_markdown`). It is best-effort, skips the gate-excluded files, and is idempotent with `quest-fix.yml`'s M8 step. Because `run.sh` is ported to the sibling sites, upstream this change to `bamr87/bamr87` and `lifehacker.dev` so every repo's AI workflows inherit it.

This sweep catches *uncommitted* edits (the workflow-opens-PR flows). Agents that commit inside their own run — `content-factory`, `quest-forge`, the issue resolver — are covered by Layer 3, which fires per-edit *during* the run, before the agent commits.

---

## Layer 3 — Claude Code hook (all Claude markdown, every repo)

A `PostToolUse` hook on `Write|Edit|MultiEdit` runs the unwrapper on any `*.md` Claude writes. Committed project hooks (`.claude/settings.json`) also fire in the headless `claude -p` CI agents — there is no trust gate in CI — so this one config covers local contributors *and* the fleet.

The hook script is in this repo at `tools/hooks/unwrap-md-hook.sh` (jq-free, parses the event JSON with python3, acts only on markdown, always exits 0).

### Global install (all repos, including non-bamr87 — your machine)

The remote/web container is ephemeral, so install this on the machine that owns your `~/.claude`. Make the unwrapper available at a stable path, then add the hook:

```bash
mkdir -p ~/.claude/bin
curl -fsSL https://raw.githubusercontent.com/bamr87/it-journey/main/tools/unwrap-prose.py \
  -o ~/.claude/bin/unwrap-prose.py
```

Add to `~/.claude/settings.json` (merge with any existing `hooks` block):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c 'import json,sys,os,subprocess as s; d=json.load(sys.stdin); f=(d.get(\"tool_input\") or {}).get(\"file_path\") or \"\"; f.endswith((\".md\",\".markdown\")) or sys.exit(0); u=os.path.join(os.environ.get(\"CLAUDE_PROJECT_DIR\",\"\"),\"tools\",\"unwrap-prose.py\"); u=u if os.path.isfile(u) else os.path.expanduser(\"~/.claude/bin/unwrap-prose.py\"); os.path.isfile(u) and os.path.isfile(f) and s.run([\"python3\",u,\"--write\",f])'"
          }
        ]
      }
    ]
  }
}
```

The command prefers the repo's own `tools/unwrap-prose.py` (so a repo pins its version) and falls back to the global copy, so it is a clean no-op in repos that have neither.

### Project install (this repo / kit — team + CI, opt-in)

If you want it committed so the whole team and the CI agents get it, add `.claude/settings.json` (this is intentionally NOT committed by default — a committed hook auto-runs a shell command for every contributor, so it is your call):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR/tools/hooks/unwrap-md-hook.sh\"" }
        ]
      }
    ]
  }
}
```

To make it universal across bamr87 repos, add both `.claude/settings.json` and `tools/hooks/unwrap-md-hook.sh` to the hub's `--kit prose` fanout.

---

## Layer 4 — pre-commit hook (all commits, any author — shipped here)

`tools/hooks/pre-commit` runs the unwrapper on staged markdown and re-stages the result, so wrapped prose is fixed before it is ever committed — regardless of who or what created it. Install once per clone:

```bash
make hooks-install     # sets core.hooksPath=tools/hooks
```

Bypass a single commit with `git commit --no-verify`. To distribute it, add `tools/hooks/pre-commit` to the hub's `--kit prose` fanout; contributors still run `make hooks-install` once (git will not auto-enable a repo's hooks).

---

## Rollout checklist

- [x] Layer 0 — CI check fanned out (already in every repo).
- [ ] Layer 1 — paste the auto-fix `markdown-oneline.yml` into the hub's `--kit prose`, re-fanout (optional; tradeoff above).
- [x] Layer 2 — `scripts/ai/run.sh` sweep (this repo); upstream to `bamr87/bamr87` + `lifehacker.dev`.
- [ ] Layer 3 — add the global `~/.claude/settings.json` hook on your machine; optionally kit the project variant.
- [x] Layer 4 — `tools/hooks/pre-commit` + `make hooks-install` (this repo); kit it for the rest.

## Keep in lockstep

The exclude list appears in `markdown-oneline.yml`, the `Makefile` (`PROSE_ONELINE_EXCLUDES`), `scripts/ai/run.sh`, and both hook scripts. When it changes, update all of them. `tools/unwrap-prose.py` is the single engine everywhere.
