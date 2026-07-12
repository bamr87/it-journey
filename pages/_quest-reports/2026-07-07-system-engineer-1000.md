---
title: System Engineer · L1000 · 2026-07-07
description: Quest-perfection walkthrough of the Cloud Computing slice system-engineer/1000 on 2026-07-07,
  engine verdict fail. An evidence-based, learner's-eye…
date: '2026-07-07T00:00:00.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- System Engineer
tags:
- system-engineer
- level-1000
- walkthrough
- quest-perfection
- fail
- cloud-computing
render_with_liquid: false
excerpt: 'System Engineer · Level 1000 — Cloud Computing: an evidence-based quest-perfection walkthrough
  from 2026-07-07.'
slice: system-engineer/1000
character: system-engineer
level: '1000'
theme: Cloud Computing
tier: Warrior
verdict: fail
quest_count: 5
walk_date: '2026-07-07'
run_url: https://github.com/bamr87/it-journey/actions/runs/29190829265
source_report: test/quest-validator/walkthroughs/2026-07-07-system-engineer-1000.md
---

> **Slice** `system-engineer/1000` · **Level** 1000 (Cloud Computing) · **Warrior tier** · **Engine verdict** ❌ fail · **Walked** 2026-07-07
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29190829265) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-07-system-engineer-1000.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-07-system-engineer-1000.md)

---

## 🎯 Session Summary

I walked the **first window (5 of 9 quests)** of the System Engineer path's Level
**1000 — Cloud Computing (Warrior tier)** as a learner would, driving the sandboxed
**execute** engine over each quest and then reasoning about the chain as one journey.
The headline verdict is **FAIL**: of the five quests, **0 passed, 3 warned, 2 failed**
(one of those a 600-second engine timeout), average score **61.2%**.

Two things dominate this slice. First, the **flagship observability quest is broken as
written** — its centerpiece GitHub Actions workflow carries leaked Jekyll `{​% raw %​}`
tags *inside* every `${​{ }​}` expression, which the engine reproduced as an immediate
`bash: bad substitution` error, and a quoted heredoc silently no-ops its timestamp.
Second, a **systemic dead validation gate** runs through the whole GH-600 sub-arc:
three quests (Q1, Q2, Q5) end with `python3 scripts/validate_quest.py --quest qN`, a
script that **does not exist anywhere in the repo** — the engine ran it and it failed
with "No such file or directory." A maintainer should treat the `{​% raw %​}` leakage and
the missing validator as the two must-fix items before this slice teaches what it claims.

> **Mode & honesty note:** this is a real `--mode execute` run whose evidence was
> pre-computed and **sealed by the workflow** (`./walk-evidence.json` / `.md`) — I
> consumed it as-is and did not re-run the engine. Quest 5 (MCP Conclave) **timed out
> at 600s with no machine verdict**, so everything I say about it is `reasoned`
> (static read of the source), never `tested`. See §7 for coverage limits.

## 🗺️ The Journey

Plan order (dependency/name-sorted, **not** pedagogical order — see §6):

1. ❌ **The All-Seeing Eye: Observability for AI Agents** — **39** · flagship workflow broken two ways (`{​% raw %​}` leak + quoted heredoc), dead validator, unaddressed secondary objectives.
2. ⚠️ **Forging the Agent's Arsenal: Tool Selection & Permissions** — **62** · clean YAML/markdown artifacts, but the only runnable command (the validator) fails, and it sells soft prompt text as a hard permission boundary.
3. ⚠️ **Cloud Computing Fundamentals: IaaS, PaaS, SaaS** — **75** · accurate, well-built concepts; two of three Secondary Objectives are promised but never written, and two AWS CLI snippets fail `NoCredentials` with no prerequisite note.
4. ⚠️ **Forging the Arsenal: Tool Use & Environment** — **69** · strong pedagogy and 4/4 lab steps run byte-perfect, but the climactic "break it on purpose" step is factually wrong (infinite loop, not `exit=0`) and cites an unverifiable "GH-600" exam code.
5. ❌ **The MCP Conclave: Mastering MCP Servers** — **— (timeout)** · no engine verdict; static read flags the same missing `validate_quest.py`, a broken Windows PowerShell block, and a likely-stale SDK API.

## 🔬 Evidence

All `passed`/`failed` below come from commands the engine **actually ran in the
sandbox** (`./walk-evidence.json`); `reasoned` items were judged statically.

### 1. The All-Seeing Eye — Observability (39 · FAIL)
Snippets: **ran 4 of 6 recorded (3 runnable); 2 passed, 2 failed, 2 reasoned.**
- ❌ **`.github/workflows/agent-with-tracing.yml` (Ch.2)** — copied verbatim, YAML parses,
  but `bash -c 'echo "run_id=${​% raw %​}{​{ github.run_id }​}{​% endraw %​}"'` → **`bash: bad
  substitution` (exit 1)**. The leaked Jekyll tags are in the source at lines 163–204.
- ❌ **Trace heredoc** — `cat > agent-execution-trace.json << 'EOF'` uses a **quoted**
  delimiter, so `"completed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"` is written **literally**,
  never evaluated — the trace has no real timestamp.
- ❌ **`python3 scripts/validate_quest.py --quest q3`** — "No such file or directory"; the
  validation gate references a script the quest never ships.
- ✅ **`stamp_artifact.py <file> <run_id> <task>`** — exit 0, prepended the expected
  metadata header. The one genuinely working artifact.
- ✅ **`agent-act` job YAML fragment** — parses; `needs: agent-run` correctly matches Ch.2's job.
- 🧠 **`gh api ... /environments/agent-production -f reviewers=...`** (reasoned) — per `gh api
  --help`, `-f` sends **string literals**, not the nested array/object the environments API
  needs; would 422 against the real API.

### 2. Tool Selection & Permissions (62 · WARN)
Snippets: **ran 3 of 4 (1 runnable); 2 passed, 1 failed, 1 reasoned.**
- ✅ **`dependency-updater-tools.yml`** — written and `yaml.safe_load`-parsed cleanly.
- ✅ **`.github/copilot-instructions.md` Tool Permissions section** — valid, well-formed markdown.
- ❌ **`python3 scripts/validate_quest.py --quest q4`** — same missing-script failure as Q1 (exit 2).
- 🧠 Content note (reasoned): Ch.3–4 present `copilot-instructions.md` prose as an enforced
  permission boundary; it is a **soft** prompt-level instruction, not a security control.

### 3. Cloud Computing Fundamentals (75 · WARN)
Snippets: **ran 3 of 9 recorded (5 runnable); 1 passed, 2 failed, 2 skipped, 4 reasoned.**
- ✅ **`aws --version` / `az version` / `gcloud version`** — all ran (aws-cli 2.35.11,
  azure-cli 2.87.0, gcloud 574.0.0); quest syntax matches current CLIs.
- ❌ **`aws sts get-caller-identity`** — `An error occurred (NoCredentials): Unable to locate
  credentials.` Correct syntax, but no prerequisite/credentials note for a "no prior cloud
  experience" learner running it outside CloudShell.
- ❌ **`aws ec2 describe-availability-zones --region us-east-1 ...`** — identical `NoCredentials`
  failure, same missing caveat.
- ⏭️ macOS `brew` / Windows `winget` install blocks — skipped (Linux sandbox); package IDs
  reasoned-correct.
- 🧠 Two of three **Secondary Objectives** (Deployment Models; Economics of Elasticity) have
  **zero** body content — a full-text search finds no "hybrid", "multi-cloud", "elasticity",
  "pay-as-you-go", "on-demand", or "reserved" anywhere. Content accuracy on what *is* covered
  scored 5/5.

### 4. Forging the Arsenal: Tool Use & Environment (69 · WARN)
Snippets: **ran 6 of 12 recorded (4 runnable); 5 passed, 1 failed, 6 reasoned.**
- ✅ **Lab Steps 1–4** — ran in a persistent shell; output matched the quest's "Expected"
  blocks **byte for byte**, including transient-failure absorption (exit=0 on attempt 3) and
  permanent-failure escalation (`::error::`, stub `gh issue create`, exit=1).
- ✅ **All YAML/JSON/mermaid snippets** — parse/render cleanly (PyYAML, json, mermaid-cli 14KB SVG).
  Note: this quest correctly wraps whole fenced blocks in `{​% raw %​}` (source lines 152, 273)
  — the *right* way to do what Quest 1 got wrong.
- ❌ **Final "break it on purpose" instruction** — quest claims deleting `exit 1` yields
  "exit=0 while the tool never succeeded." **Actually run, it loops forever**: the
  retry/`sleep` lines sit inside the `until` loop but outside the `if`, so removing `exit 1`
  re-fires `::error::` + `gh issue create` every iteration and never exits — had to be killed
  after 60s / 5+ iterations. Confirmed by static read of source lines 303–324.
- 🧠 Cites certification code **"GH-600"** with a specific Microsoft Learn URL and weightings;
  the engine could not verify this exam code exists (known GitHub codes run GH-100…GH-500).

### 5. The MCP Conclave — MCP Servers (— · FAIL / timeout)
Snippets: **none — `claude timed out after 600s`; no machine verdict.**
Everything here is **`reasoned`** from a static read of the source only:
- 🧠 **`python3 scripts/validate_quest.py --quest q5`** (line 304) — the **same** missing
  validator that the engine actually failed on in Q1 and Q2; near-certain to fail identically.
- 🧠 **Windows PowerShell block (lines 160–167)** — `echo ... | $env:GITHUB_PERSONAL_ACCESS_TOKEN=$env:GITHUB_TOKEN`
  then a separate `npx` line is not valid PowerShell (piping into a variable assignment); a
  Windows learner following it literally would get a parser error.
- 🧠 **Custom MCP server (Ch.4)** — uses `server.setRequestHandler("tools/list", …)` with a
  **string** method name; current `@modelcontextprotocol/sdk` expects a request *schema object*,
  so this may not run as written (low confidence — not executed; SDK version-dependent).
- 🧠 Token guidance mixes fine-grained-PAT language with classic `ghp_`/`repo:write`/`admin:org`
  scope names — a minor inconsistency for a security-focused chapter.

## 🐞 Issues Found

**High**
- **H1 · Q1 Observability · Ch.2 `agent-with-tracing.yml` (src lines 163–204)** — *Observed:*
  leaked `{​% raw %​}...{​% endraw %​}` inside every `${​{ }​}`; `bash: bad substitution` on the first
  step. *Fix:* remove the inline tags (`${​{ github.run_id }​}`), and if the renderer needs
  escaping, wrap the **entire** fenced block once — exactly how sibling Quest 4 does it (lines
  152, 273).
- **H2 · Q1 Observability · Ch.2 trace heredoc** — *Observed:* quoted `<< 'EOF'` writes
  `$(date …)` literally; the trace never captures a real timestamp. *Fix:* capture the time to
  a step output/env var beforehand, or use an unquoted heredoc with the `${​{ }​}` expressions
  escaped.
- **H3 · Q1/Q2/Q5 · closing "Quest Validation" blocks** — *Observed:* `scripts/validate_quest.py`
  does not exist; engine ran it for Q1 and Q2 → "No such file or directory" (Q5 reasoned,
  same line). This is a **systemic** dead gate across the GH-600 arc. *Fix:* ship/link the
  validator, or replace it with a self-checkable manual checklist.
- **H4 · Q4 Tool Use · Hands-On Lab final step** — *Observed:* claimed `exit=0`, real behavior
  is an infinite issue-spamming loop (control-flow bug, src lines 303–324). *Fix:* restructure
  the wrapper so removing `exit 1` genuinely falls through to a silent success, **or** rewrite
  the instruction to describe the real runaway loop and tell the learner to Ctrl+C.
- **H5 · Q3 Cloud Fundamentals · Secondary Objectives** — *Observed:* "Deployment Models" and
  "Economics of Elasticity" are listed (lines 106–107) but have zero body content. *Fix:* add
  the two sections or remove/relabel the objectives.

**Medium**
- **M1 · Q1 Observability · Ch.3 `gh api` environment command** — *Observed (reasoned):* `-f`
  sends string literals for `reviewers`/`deployment_branch_policy`; would 422. *Fix:* bracket
  syntax (`-f 'reviewers[][type]=User'`) or `--input`.
- **M2 · Q2 Tool Selection · Ch.3–4 permission claims** — *Observed (reasoned):* prompt text in
  `copilot-instructions.md` framed as an enforced boundary. *Fix:* state it is a soft
  instruction and point to real enforcement (branch protection, required reviews, MCP/network
  allow-lists).
- **M3 · Q3 Cloud Fundamentals · AWS CLI snippets** — *Observed:* `NoCredentials` on
  `get-caller-identity` and `describe-availability-zones`. *Fix:* add a "requires `aws
  configure` or CloudShell" prerequisite note and show the expected error.
- **M4 · Q4 Tool Use · "GH-600" certification citation** — *Observed (reasoned):* exam code
  unverifiable. *Fix:* verify against GitHub's catalog or frame the domain model as original
  pedagogy.
- **M5 · Q5 MCP · Windows PowerShell block (reasoned)** — *Observed:* invalid pipe into a
  variable assignment. *Fix:* correct the PowerShell to set `$env:GITHUB_PERSONAL_ACCESS_TOKEN`
  then pipe into `npx` on its own line.

**Low**
- **L1 · Q1** — trace JSON omits `commit_sha` (`${​{ github.sha }​}`), so it can't prove the
  commit-level traceability the objective claims.
- **L2 · Q1** — secondary "multi-run dashboard" objective has no supporting snippet at all.
- **L3 · Q2/Q4** — both reference a "dependency updater agent you designed in Q1" without
  recapping it; not self-contained for a fresh reader (see §6 for why "Q1" is ambiguous here).
- **L4 · Q3** — knowledge-check questions have no answer key for self-verification.
- **L5 · Q5 (reasoned)** — custom MCP server may use a stale SDK `setRequestHandler` signature.

## 🔗 Chain Continuity

**The slice is two disjoint arcs stapled together by level code, not one journey.**
Quests 1, 2, 4, 5 belong to the **GH-600 "Agentic Codex"** arc; Quest 3
(Cloud Computing Fundamentals) is a standalone **"Cloud Journey"** quest with
`required_quests: []` that unlocks the AWS/IaC/Azure track. Walked in plan order a
learner lurches: agentic observability → agentic tool permissions → *cloud IaaS/PaaS/SaaS*
→ back to agentic tooling → agentic MCP. Plan order is a dependency/name sort, **not** a
teaching path. For the **System Engineer** class specifically, the cloud quest is arguably
the more on-path one (it even routes System Engineers to Infrastructure as Code), while the
GH-600 agentic arc reads as a DevOps/AI specialization.

**Within the GH-600 arc, the numbering is genuinely confusing.** Two overlapping schemes
coexist: front-matter `sub_title` numbers quests as "Quest 1/4 … 2/4 … 3/4" by domain,
while the bodies + mermaid diagrams number them **Q3, Q4, Q5** absolutely, and the
exercises are labeled "Exercise 3.x / 4.x / 5.x." So Quest 1 in the slice
(*Observability*, `sub_title: Quest 1/4 — Domain 1`) renders internally as **Q3** with
**Exercise 3.x**. A learner can't tell which "Q1" is meant when Quest 2 says *"the
dependency updater agent you designed in Q1"* — that design lives in neither Quest 1 of
this slice (observability) nor is it recapped anywhere in the window.

**Overlap/redundancy:** Quest 4 (`agentic-codex-02`) is actually the **Domain 2 hub
chapter** — it explicitly lists Quest 2 (Tool Selection) and Quest 5 (MCP Conclave) as its
sub-quests and re-teaches the same artifacts (least-privilege `permissions:` block, MCP
allow-list, `AGENTS.md`, the retry/escalation wrapper). A learner taking both the hub and
the individual quests meets the same material twice. Notably the hub (Quest 4) gets the
`{​% raw %​}` escaping **right**, while the older individual quest (Quest 1) gets it **wrong**
— evidence the arc was authored in two passes that haven't been reconciled.

**Prerequisite satisfaction:** the internal dependency edges are sound —
Observability → Tool Selection → MCP Conclave chain correctly via `quest_dependencies`,
and Q1's external prereq (`/quests/0111/agentic-plan-vs-action-boundaries/`) sits in an
earlier level (reasonable, out of window). The real prerequisite gaps are **content**, not
graph: the missing `validate_quest.py` gate (H3) blocks the advertised completion step on
three of five quests, and the un-recapped "Q1 dependency updater" (L3) leaves Quests 2 and 4
assuming setup the window never provides.

**Bottom line for a real learner:** the cloud quest stands alone and teaches well; the
agentic arc has a solid conceptual spine (observe → scope → connect → bind) but trips a
beginner on copy-paste (`{​% raw %​}` leak), on a dead validation command they're told to run
three times, and on numbering that contradicts itself between front-matter and body.

## 🧠 Reasoning & Method

- **What I ran vs. reasoned:** I did **not** execute the engine — I consumed the sealed
  `./walk-evidence.json` / `./walk-evidence.md` the workflow produced with
  `agentic_validate.py --mode execute`, exactly as the skill's step 2 requires when evidence
  pre-exists. Every `passed`/`failed` in §4 is a command the engine ran in its disposable
  sandbox; I additionally **read all five quest sources in plan order** and cross-checked the
  engine's findings against the raw markdown (e.g., confirmed the `{​% raw %​}` leak at Q1 lines
  163–204 and the Q4 loop bug at lines 303–324, and verified Q4 escapes `{​% raw %​}` correctly).
- **Mode:** `execute`, real (not `--mock`). 4 quests scored, average 61.2%, engine cost
  ~$2.67, reported by the sealed evidence.
- **Coverage limits (honest):**
  - **Quest 5 (MCP Conclave) has NO machine evidence** — the engine `claude` process timed out
    at 600s. All Quest-5 items are `reasoned` static reads; I did not run any MCP command,
    and its score is `—`, counted as a fail for the slice verdict but **not** a tested fail.
  - This was **window 1 of 2** — only 5 of the level's 9 quests were in scope; I did not walk
    the remaining 4 (the perfection ledger accumulates them on a later run).
  - Several snippets are inherently un-runnable in a headless Linux sandbox (macOS `brew`,
    Windows `winget`/PowerShell, live `gh api`/`aws` calls needing credentials, and the
    Copilot-agent-in-VS-Code interactions of Q2/Q5) — these are `skipped`/`reasoned`, not
    proof of correctness.
- **Confidence:** **High** on the four scored quests' concrete failures (each independently
  reproduced by a real command and corroborated by the source). **Medium/low** on Quest 5,
  which is static-only — the missing-validator finding is high-confidence (same script the
  engine already failed twice), the PowerShell and SDK-signature findings are lower-confidence
  reasoned notes.
- **Scope discipline:** read-only over content. I made no edits to any quest, `walk-plan.json`,
  or `walk-evidence.*`, and did not branch/commit/push/merge. This report is the single
  deliverable; a content pass (content-curator / a human) should act on §5.

---

### Appendix — Machine evidence (verbatim excerpt from `./walk-evidence.md`)

> **4** quests evaluated · ✅ 0 pass · ⚠️ 3 warn · ❌ 2 fail · avg **61.2%** · ~$2.6662
>
> | | Score | Quest | Snippets run | |
> |---|--:|---|:-:|---|
> | ❌ | 39 | The All-Seeing Eye: Observability for AI Agents | 4/3 (2✗) | broken Ch.2 workflow + dead validator |
> | ⚠️ | 62 | Forging the Agent's Arsenal: Tool Selection & Permissions | 3/1 (1✗) | only runnable command (validator) fails |
> | ⚠️ | 75 | Cloud Computing Fundamentals: IaaS, PaaS, and SaaS | 3/5 (2✗) | drops 2 secondary objectives; NoCredentials |
> | ⚠️ | 69 | Forging the Arsenal: Tool Use & Environment | 6/4 (1✗) | "break it" step loops instead of exit=0 |
> | ❌ | — | The MCP Conclave: Mastering MCP Servers | — | ⚠️ claude timed out after 600s |
