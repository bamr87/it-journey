---
title: 'Quest Walkthrough — System Engineer · Level 1000 (Cloud Computing / Warrior)'
date: '2026-07-11T11:56:34.000Z'
character: system-engineer
level: '1000'
theme: Cloud Computing
tier: Warrior
quest_count: 5
mode: execute
overall_verdict: fail
session:
  slice: system-engineer/1000
  window: '1 of 2 (quests 1–5 of 9)'
  engine_evaluated: 2
  engine_requested: 5
  auth_truncated: true
  reasoned_only: 3
  engine_average: 48.5
  engine_counts: '0 pass · 0 warn · 2 fail'
  note: >-
    Machine evidence covers only 2 of the 5 planned quests — the execute engine
    hit an OAuth rate-limit (auth_truncated) after quest 2. Quests 3–5 are
    reasoned-only from source, never run in the sandbox. Verdict is driven by
    the two machine-evaluated quests (both fail) plus static concerns in the
    remaining three; coverage is partial and labeled as such throughout.
---

## 🎯 Session Summary

I walked the **System Engineer → Level 1000 (Cloud Computing, 🔥 Warrior tier)**
slice as a learner. The planner selected a **window of 5 quests out of the level's 9**
(window 1 of 2), and the pre-sealed engine evidence (`walk-evidence.json`) covers
**only the first 2** of those five — the execute run stopped with `auth_truncated: true`
after ~$1.28 of spend, so quests 3–5 were **never executed**. I read all five in plan
order and reason about the linked journey below.

**Headline verdict: fail (partial coverage).** Both machine-evaluated quests failed
(42% and 55%), each for concrete, learner-blocking reasons the sandbox actually
reproduced: a flagship GitHub Actions snippet corrupted by leaked Jekyll `{% raw %}`
tags that produces invalid JSON, a `gh api` call that serializes nested JSON as
strings (422 from the real API), and a `scripts/validate_quest.py` completion gate
that references a script the quest never ships. That last defect is **systemic** — the
same nonexistent validation script is the closing gate of at least three quests in the
slice. Separately, this "slice" is not one coherent learning path: it splices the
**gh-600 Agentic Codex** line together with a standalone **Cloud Journey** conceptual
quest, and orders the Codex *field-guide hub* after two of the quests it is meant to
introduce.

## 🗺️ The Journey

Plan order (dependency-sorted by `walkthrough_plan.py`; `stats.windowed: true`):

1. ❌ **The All-Seeing Eye: Observability for AI Agents** — **42%** (execute) · flagship
   tracing workflow is broken by leaked `{% raw %}` Liquid tags → invalid JSON, plus a
   quoted-heredoc that drops the `completed_at` timestamp and a `gh api` call the real
   API would reject.
2. ❌ **Forging the Agent's Arsenal: Tool Selection & Permissions** — **55%** (execute) ·
   static artifacts are valid, but the closing `validate_quest.py` gate fails outright
   and the lesson conflates prose in `copilot-instructions.md` with a *technically
   enforced* permission boundary.
3. ⚪ **Cloud Computing Fundamentals: IaaS, PaaS, SaaS** — **reasoned only (not run)** ·
   well-structured conceptual quest; thematically the odd one out (Cloud Journey line,
   no agent content); AWS/AZ commands need real cloud credentials.
4. ⚪ **Forging the Arsenal: Tool Use & Environment** (Codex Ch. II hub) — **reasoned
   only (not run)** · strong field-guide; a self-contained zero-credential lab; uses the
   *correct* `{% raw %}` fence pattern (instructive contrast with quest 1).
5. ⚪ **The MCP Conclave: Mastering MCP Servers** — **reasoned only (not run)** · same
   missing `validate_quest.py` gate; a malformed PowerShell snippet and a possibly-stale
   MCP SDK API I flag but did **not** execute.

⚪ = no machine evidence; my notes are static reasoning from source, not sandbox results.

## 🔬 Evidence

### Quest 1 — Observability for AI Agents (execute · 42% · fail)
Snippet coverage: **ran 5 of 3 runnable** (6 recorded, 3 passed, 2 failed, 1 skipped).
Per-dimension: commands_work **1**, content_accuracy **2**, completeness **2**,
clarity **2**, structure **4**, safety **5**.

- ❌ **`agent-with-tracing.yml` (Exercise 3.1)** — engine wrote the file verbatim and
  found the literal string `{% raw %}` embedded in **12** GitHub Actions expressions
  (confirmed with `grep -c`). Simulating the unsubstituted output and feeding the trace
  JSON to `python3 json.load()` returned *"Expecting value: line 8 column 21"* — **invalid
  JSON**. The quest's flagship "machine-readable execution log artifact" does not parse.
- ❌ Independently verified: the trace JSON heredoc uses a **quoted delimiter**
  (`<< 'EOF'`), so `"completed_at": "$(date -u ...)"` is written **literally**, not
  substituted — even if the Liquid-tag bug were fixed.
- ❌ **`gh api ... environments/agent-production` (Exercise 3.2)** — run with a fake token
  under `--verbose`; `-f/--raw-field` serialized `reviewers` and `deployment_branch_policy`
  as **JSON-escaped strings**, not the array/object the real API requires → **422** against
  live GitHub.
- ✅ **`stamp_artifact.py` (Exercise 3.3)** — ran against a sample file; prepended the
  metadata header correctly and picked up `GITHUB_REPOSITORY`.
- ✅ **mermaid network diagram** — rendered to valid SVG via `mmdc` 11.16.0.
- ⏭️ **`scripts/validate_quest.py --quest q3`** — skipped: script not shipped with the quest.

### Quest 2 — Tool Selection & Permissions (execute · 55% · fail)
Snippet coverage: **ran 2 of 1 runnable** (4 recorded, 1 passed, 1 failed, 2 reasoned).
Per-dimension: commands_work **2**, content_accuracy **2**, completeness **3**,
clarity **4**, structure **4**, safety **4**.

- ✅ **`dependency-updater-tools.yml`** — written verbatim and parsed cleanly with
  `yaml.safe_load`; structure (required_tools/excluded_tools) is internally consistent.
- ❌ **`python3 scripts/validate_quest.py --quest q4`** — ran verbatim; failed with
  *"can't open file '.../scripts/validate_quest.py': [Errno 2] No such file or directory"*.
  The closing validation gate is not completable from the quest content.
- 🟰 **`copilot-instructions.md` tool-permissions block** — reasoned (prose, not
  executable); consistent with the YAML's forbidden-tools list.
- 🟰 **mermaid diagram** — reasoned; valid syntax, but headless-Chrome sandbox refused to
  launch (`No usable sandbox!`) so it wasn't rendered here (environment limit, not a defect).

### Quests 3–5 — no machine evidence
The engine stopped after quest 2 (`auth_truncated: true`; `evaluated: 2, requested: 5`).
I did **not** run any command from these three quests. Everything under Issues/Chain
below for them is `reasoned` from the quoted source lines — no `passed`/`failed` claim is
made for them.

Machine summary (verbatim from `walk-evidence.md`): *"2 quests evaluated · ✅ 0 pass ·
⚠️ 0 warn · ❌ 2 fail · avg 48.5% · ~$1.2792."*

## 🐞 Issues Found

**High**
- **[Q1 · Exercise 3.1 workflow YAML · lines 163–204] Leaked Jekyll `{% raw %}` tags
  corrupt every GH Actions expression** — *observed (execute):* literal `${% raw %}{{ ... }}{% endraw %}`
  in 12 expressions; simulated output is invalid JSON (`json.load` error line 8 col 21).
  *Fix:* strip the inline `{% raw %}…{% endraw %}` and either escape the braces per the
  quest instructions or wrap the whole fenced block in raw tags on their own lines (see
  how quest 4 does it correctly).
- **[Q1 · trace JSON heredoc · lines 176–197] Quoted heredoc drops the timestamp** —
  *observed (execute):* `<< 'EOF'` suppresses `$(date -u ...)`, so `completed_at` is
  literal text. *Fix:* compute the timestamp in a prior step output (like `trace_start`
  does) or use an unquoted delimiter.
- **[Q1 · Exercise 3.2 · lines 218–229] `gh api -f` sends nested JSON as strings** —
  *observed (execute):* request body carries `reviewers`/`deployment_branch_policy` as
  escaped strings → 422 live. *Fix:* use bracket syntax (`-f 'reviewers[][type]=User'`)
  or `--input environment.json`.
- **[Q2 · Quest Validation · lines 201–207] & [Q1 · lines 305–314] & [Q5 · lines 303–309]
  `scripts/validate_quest.py` is never shipped** — *observed (execute) for Q2:* command
  fails with "No such file or directory"; *reasoned* for Q1/Q5 (same command, same absent
  script). This is the **slice-wide** completion gate and it is unusable standalone.
  *Fix:* inline a minimal self-contained check per quest, or clearly state it requires the
  full IT-Journey repo checkout.
- **[Q2 · content accuracy · Chapters 3–4] Prose ≠ enforced permission boundary** —
  *observed (execute, content_accuracy=2):* the quest frames text in
  `copilot-instructions.md` as an enforced allow-list, but that is soft model guidance;
  real enforcement is App/PAT scoping, branch protection, and the agent network allowlist.
  *Fix:* add a note on the actual technical controls and mark the refusal as best-effort.

**Medium**
- **[Q1 · Secondary Objectives · line 103] "Dashboard a multi-run history" is listed but
  never taught** — *observed (execute, completeness=2):* no `gh run list`/API exercise
  anywhere. *Fix:* add the `gh run list --workflow … --json status,conclusion,createdAt`
  exercise.
- **[Q5 · Chapter 2 · Windows PowerShell · lines 160–167] Malformed pipeline** —
  *reasoned (not run):* `echo … | $env:GITHUB_PERSONAL_ACCESS_TOKEN=$env:GITHUB_TOKEN npx …`
  is not valid PowerShell (an assignment mid-pipeline). A Windows learner copy-pasting
  this gets a parse error. *Fix:* set the env var on its own line, then pipe into `npx`.
- **[Q5 · Chapter 4 · lines 216–264] Possibly-stale MCP SDK API** — *reasoned (not run,
  low confidence):* `new Server(...)` + `server.setRequestHandler("tools/list", …)` uses
  string method names; current `@modelcontextprotocol/sdk` registers handlers by request
  *schema* object, so this example may not run against a freshly `npm install`ed SDK. I did
  **not** execute it — flag for a maintainer to verify against the pinned SDK version.
- **[Q4 vs Q5] Two divergent MCP config conventions in the same domain** — *reasoned:*
  Q4 uses `.vscode/mcp.json` with a secure `${input:github-token}` prompt (lines 184–204);
  Q5 uses `.vscode/settings.json` → `github.copilot.chat.mcpServers` with a raw
  `${env:GITHUB_TOKEN}` PAT (lines 128–142). A learner walking both sees conflicting "the
  right way" guidance. *Fix:* cross-reference and standardize on the prompt-input pattern.

**Low**
- **[Q1 · Exercise 3.2 · line 225] `YOUR_GITHUB_USER_ID` placeholder unexplained** —
  *observed (execute, clarity=2):* no hint how to obtain it. *Fix:* add `gh api user --jq .id`.
- **[Q1 · line 208] "90 days is a common compliance minimum"** — *observed (execute,
  content_accuracy):* 90 days is GitHub's out-of-the-box *maximum* artifact retention, not
  a minimum; the framing muddies the guidance.
- **[Q2 · lines 84 vs 216] Diagram/Rewards mismatch** — *observed (execute, structure):*
  mermaid shows Q4 → Q5 **and** Q4 → Q6, but the Rewards "Unlocks" row lists only Q5.
- **[Q4 · line 59 & Q3 · line 18] Empty `required_quests` on chained content** —
  *reasoned:* Codex Ch. II declares `required_quests: []` (only a *recommended* Ch. I),
  which is why the planner floats it after quests it introduces — see Chain Continuity.

*Not an empty result — but note two of the failing signals (the missing
`validate_quest.py` and the un-renderable mermaid in Q2) are partly harness/tooling
artifacts of running a quest in isolation, not purely authoring defects.*

## 🔗 Chain Continuity

Reading the five in plan order as one learner's journey surfaces three structural
problems that the per-quest engine (which scores in isolation) cannot see:

1. **The slice is two unrelated quest lines stitched together.** Quests 1, 2, 4, 5 are
   the **gh-600 "Agentic Codex"** line (agents, MCP, permissions); quest 3,
   *Cloud Computing Fundamentals*, is the standalone **"Cloud Journey"** conceptual quest
   (`quest_series: Cloud Journey`, `required_quests: []`, lines 14–19). Dropped at
   position 3, it is a hard context switch — a learner goes from `gh api` agent tracing to
   IaaS/PaaS/SaaS pizza analogies and back to MCP servers. They co-exist at Level 1000 for
   the System Engineer path, but they are **not one linear learning path**, and nothing in
   the slice tells the learner they've changed tracks.

2. **The Codex field-guide hub is ordered after the quests it introduces.** Quest 4
   (*Forging the Arsenal: Tool Use & Environment*) is explicitly the Domain 2 *field guide*:
   "the four quests below are the forge… Walk them in order" (lines 414–421), and it lists
   quest 2 (Tool Selection) and quest 5 (MCP Conclave) as its children. Yet the plan places
   it at **position 4 — after** quest 2 and **before** quest 5. Because quest 4 declares
   `required_quests: []` (line 59), the deterministic dependency sort has nothing to anchor
   it, so it floats out of pedagogical order. A learner ideally reads the hub *first*; here
   they meet the overview only after already doing one of its sub-quests.

3. **A dangling cross-quest artifact reference.** Quest 2's Exercise 4.1 says *"For the
   'dependency updater' agent you designed in **Q1**"* (line 116), but no quest in this
   window designs that agent — "Q1" in the Codex numbering is *Initiation Rites*, outside
   this slice, and quest 1 here (Observability) never builds it. The engine flagged this as
   a completeness gap; as a chain issue it means the tool-inventory exercise assumes an
   artifact the walked path never produced.

**What holds together well:** within the pure agentic sub-chain, the *dependency
frontmatter* is sound — Observability `unlocks` Tool Selection `unlocks` MCP Conclave, and
each `required_quests` points back correctly (Q1 line 47, Q2 lines 44–47, Q5 lines 43–48).
The narrative arc (observe → scope tools → wire MCP) is a genuinely coherent progression.
And there's a useful **positive** contrast to mine for a fix: quest 4 demonstrates the
*correct* `{% raw %}` fence pattern (whole block wrapped, lines 152–160 / 273–299) that
quest 1 gets wrong inline — the fix for Q1 already exists elsewhere in the same slice.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sealed by the workflow) for quests 1–2; **reasoned-only** for
  quests 3–5. I consumed `walk-plan.json` + `walk-evidence.json` / `walk-evidence.md`
  as-is and did **not** run, regenerate, or edit the engine — per the skill, the engine's
  child processes can't authenticate from my Bash tool. I read all five quest sources in
  plan order.
- **Coverage is partial and that is the most important caveat.** The engine evaluated
  **2 of 5** requested quests before `auth_truncated: true` (OAuth rate-limit) stopped it —
  `evaluated: 2, requested: 5, average: 48.5`. **60% of the planned slice has no sandbox
  evidence.** Every claim about quests 3, 4, and 5 above is static reasoning from quoted
  source lines and is labeled `reasoned`; I made **no** `passed`/`failed` assertion for
  them and ran none of their commands.
- **What is machine-verified:** the two `fail` verdicts and every ✅/❌ under Q1/Q2 in the
  Evidence section come from commands the engine actually ran in its disposable sandbox
  (invalid-JSON reproduction, `gh api --verbose` body inspection, the `validate_quest.py`
  ENOENT). I quoted those outputs rather than re-deriving them.
- **What I reasoned, not ran:** the PowerShell malformation, the MCP SDK-API staleness
  (flagged *low confidence* — verify against the pinned SDK), the config-convention
  divergence, the two-line-splice and hub-ordering continuity findings, and Cloud
  Fundamentals overall (I ran none of its `brew`/`winget`/`aws`/`curl` commands — they need
  package managers or real cloud credentials a walkthrough shouldn't use).
- **Verdict rationale:** `fail`. The two quests with sandbox evidence both failed on
  learner-blocking defects, and a slice-wide broken completion gate compounds it. I did
  **not** upgrade to `warn` because the strongest single signal (Q1's flagship snippet
  producing invalid JSON) is verified, not inferred — but a maintainer should read this as
  *"fail on the 40% we could test; 60% unverified,"* not a clean full-slice fail. A
  re-run when the OAuth budget allows should evaluate quests 3–5 to close the gap.
- **Confidence:** high on Q1/Q2 (direct sandbox evidence); moderate on the continuity
  findings (frontmatter + source are unambiguous); low on the MCP SDK-staleness flag
  (unexecuted). No content was edited; this report is my only write.
