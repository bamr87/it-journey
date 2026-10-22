# Agent Instruction Changelog

> Every change to agent instructions and policy, with the observation that motivated it and the measured outcome.

Every change to agent behavior — `AGENTS.md`, `.claude/agents/*.md`, `.claude/skills/`, `.github/copilot-instructions.md`, or the policy data under `_data/agents/` — gets an entry: **what changed, why (the observation that motivated it), and the measured outcome**. One variable at a time. This is the GH-600 Domain 4 discipline of treating instructions like code; the format is taught in [Chapter IV — The Oracle Rubric](https://it-journey.dev/quests/1010/agentic-codex-04-evaluation-and-tuning/).

## 2026-10-22

### AGENTS.md

- **Changed:** restructured into the fleet docs framework's six headings (UPS-DOC-09, UPS-AGENT-07) and folded the "Claude Code notes — moved verbatim" block into them, keeping one copy of each rule (2,961 → ~1,910 words). The workflow-by-workflow fleet narrative is replaced by links to `scripts/ai/README.md` and the generated `docs/reference/workflows.md`.
  - **Reason:** every rule lived twice and the two copies had drifted (Ruby 3.2 vs the `ruby:3.4` Dockerfile; "all AI goes through one runner" vs the lanes that call `claude -p` or `claude-code-action`).
  - **Outcome:** TBD — the next weekly `agent-audit.yml` run should find no AGENTS.md/reality drift.

### Quest permalink rule (`.github/instructions/quest.instructions.md`, `.github/copilot-instructions.md`, prompts)

- **Fixed:** `quest.instructions.md` §3, copilot pitfall #11, `ai-content-review.instructions.md` and the `write-quest`, `generate-frontmatter`, `validate-content`, `publish-prep` and `quest-permalink-audit` prompts said side quests live at `/quests/XXXX/side-quests/slug/`. The validator and `quest_registry.canonical_permalink` flatten them to `/quests/XXXX/slug/`; every copy now says so.
  - **Reason:** AGENTS.md had to warn that §3 was stale, and the permalink-audit prompt would have "repaired" valid permalinks into invalid ones.
  - **Outcome:** TBD — `make quest-audit` permalink errors on newly authored side quests should stay at zero.

## 2026-07-01

### AGENTS.md

- **Added:** the "🚫 Forbidden Actions (the Warden Pact)" section — an explicit
list of actions no agent may take regardless of instructions, with the decline-comment-label-stop protocol.
  - **Reason:** the fleet's boundaries lived implicitly across nine workflow
    header comments and agent definitions; nothing stated them in the one file
    every agent reads first. GH-600 Domain 6 implementation surfaced the gap.
  - **Outcome:** TBD — first measure at the next weekly `agent-audit.yml`
    fleet audit (does the auditor find zero pact/reality drift?).

### _data/agents/ (new policy surface)

- **Added:** `registry.yml` (fleet roster: lane, kill switch, status,
review date per agent) and `autonomy-matrix.yml` (recurring action → L0–L4 autonomy level + the guardrails that justify it).
  - **Reason:** lifecycle management (D5) and risk-based autonomy (D6) need a
    machine-readable source of truth, not folklore; the weekly audit now has
    a contract to check the fleet against.
  - **Outcome:** TBD — measured by audit findings over the next quarter
    (`review_date: 2026-10-01` on every roster row).
