# Agent Failure RCA — <date> <short title>

> Copy this file to `docs/agents/rca/<YYYY-MM-DD>-<slug>.md` and fill it in
> before any re-run. Taxonomy and method are taught in
> [Chapter IV — The Oracle Rubric](https://it-journey.dev/quests/1010/agentic-codex-04-evaluation-and-tuning/).

## Incident

- **Run:** <Actions run URL>
- **Agent / workflow:** <name from `_data/agents/registry.yml`>
- **Task:** <issue/PR link or slice id>
- **Failure mode (one sentence):**

## Layer classification

Pick ONE primary layer (the fix differs entirely by layer):

- [ ] Reasoning / planning — the agent built the wrong thing
- [ ] Tool misuse — a tool was called with bad arguments
- [ ] Permissions — an API refused the token's scope
- [ ] Context drift — the world changed under the plan
- [ ] Environment — a file, secret, or dependency was missing
- [ ] Completion — success declared before the signals said so

**Evidence** (log lines, diff, trace excerpt):

## 5-Why

1. Why did it fail? →
2. Why? →
3. Why? →
4. Why? →
5. Why? →

## Root cause

<Almost always terminates at *our* system — instructions, tools, environment —
not at "the model is dumb". Name the file that owns the fix.>

## Prevention (shipped)

- <change + PR link>
- Recorded in [`instructions-changelog.md`](instructions-changelog.md): yes/no
