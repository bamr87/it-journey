---
title: Security Specialist · L1000 · 2026-07-07
description: Quest-perfection walkthrough of the Cloud Computing slice security-specialist/1000 on 2026-07-07,
  engine verdict fail. An evidence-based, learner's-eye…
date: '2026-07-07T00:00:00.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Security Specialist
tags:
- security-specialist
- level-1000
- walkthrough
- quest-perfection
- fail
- cloud-computing
render_with_liquid: false
excerpt: 'Security Specialist · Level 1000 — Cloud Computing: an evidence-based quest-perfection walkthrough
  from 2026-07-07.'
slice: security-specialist/1000
character: security-specialist
level: '1000'
theme: Cloud Computing
tier: Warrior
verdict: fail
quest_count: 5
walk_date: '2026-07-07'
run_url: https://github.com/bamr87/it-journey/actions/runs/29190829265
source_report: test/quest-validator/walkthroughs/2026-07-07-security-specialist-1000.md
---

> **Slice** `security-specialist/1000` · **Level** 1000 (Cloud Computing) · **Warrior tier** · **Engine verdict** ❌ fail · **Walked** 2026-07-07
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29190829265) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-07-security-specialist-1000.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-07-security-specialist-1000.md)

---

## 🎯 Session Summary

Walking the **Security Specialist** path at **Level 1000 (Cloud Computing, Warrior 🔥)**, this session played the first window (5 of 9 quests) of the level in the planner's order. Four of the five quests belong to the **GH-600 "Agentic Codex"** sub-line (agent observability, tool permissions, the Domain-2 field guide, and MCP servers); the fifth, **Cloud Computing Fundamentals**, is a conceptual primer from a *different* quest series that happens to share the level.

**Headline verdict: FAIL.** The sealed execute-engine evidence scored the slice at an average **56.2%** — 1 pass, 1 warn, 3 fail. The single conceptual quest (Cloud Fundamentals, 80%) is solid and technically accurate; the hands-on agentic quests are undermined by **verified, reproducible code defects**: a Jekyll `{​% raw %​}`-tag leak that breaks the flagship workflow in the very first quest, a factually-wrong "watch it exit=0" lab exercise that actually loops forever, a deprecated npm package plus a crashing SDK API in the MCP quest, and — most tellingly — **the same nonexistent `scripts/validate_quest.py` "validation" step at the end of three separate quests.** A learner following the agentic chain literally cannot complete the closing validation of any of those three quests, and would hit an immediate copy-paste failure on the first workflow they try. This slice needs a content-accuracy pass before it can be trusted; the concrete, evidenced fixes are in §Issues.

## 🗺️ The Journey

Plan order (window 1 of 2; `stats.total_quests` = 9):

1. ❌ **The All-Seeing Eye: Observability for AI Agents** — 40% · The flagship
tracing workflow is broken as written: `{​% raw %​}`/`{​% endraw %​}` tags leaked *inside* every `${​{ }​}` expression → immediate bash `bad substitution`.
2. ❌ **Forging the Agent's Arsenal: Tool Selection & Permissions** — 57% · Data
artifacts are clean, but the only runnable command (validation script) doesn't exist, and it frames markdown prompts as real least-privilege *enforcement*.
3. ✅ **Cloud Computing Fundamentals: IaaS, PaaS, SaaS** — 80% · Accurate, working
   verify commands across all three CLIs; two secondary objectives are never taught.
4. ⚠️ **Forging the Arsenal: Tool Use & Environment** (codex-02 hub) — 67% · Core
lab genuinely works and outputs matched exactly, but the closing "delete `exit 1`, watch exit=0" exercise actually causes an infinite loop.
5. ❌ **The MCP Conclave: Mastering Model Context Protocol Servers** — 37% · Deprecated
npm package, custom server crashes on the current SDK, broken PowerShell block, nonexistent validation script — the hands-on core is unusable as written.

## 🔬 Evidence

All results below are from the sealed `walk-evidence.json` (`--mode execute`, `executed: true` for every quest — commands actually ran in the disposable sandbox). I did not re-run the engine; I consumed the sealed evidence and reasoned over the quest sources.

### 1. The All-Seeing Eye — Observability (40%, fail) — ran 5/3 runnable snippets, 3 passed / 2 failed / 1 reasoned
- **`.github/workflows/agent-with-tracing.yml` → FAILED.** The engine extracted the
exact `run:` text and ran it: `run_id=${​% raw %​}{​{ github.run_id }​}{​% endraw %​}: bad substitution` (exit 1). Confirmed in source at lines 163–164, 170, 179–193, 203 — the Liquid `{​% raw %​}`/`{​% endraw %​}` tags leaked *inside* each expression (8 occurrences) instead of wrapping the block, so neither bash nor GitHub Actions would interpolate them.
- **`gh api ... /environments/agent-production` → REASONED (not run against live GitHub).**
`gh api --help` confirms `-f/--raw-field` always sends a *string*; the command uses it for `reviewers` (JSON array), `deployment_branch_policy` (JSON object), and `wait_timer` (integer), which the API would reject (422). Correct form is `--input -`.
- **`stamp_artifact.py` → PASSED.** Ran, prepended the metadata header, printed success.
- **Mermaid network diagram → PASSED** (rendered to SVG).
- **`python3 scripts/validate_quest.py --quest q3` → FAILED.** `No such file or
  directory` — script never provided or linked anywhere in the quest.

### 2. Forging the Agent's Arsenal — Tool Selection (57%, fail) — ran 3/1 runnable, 2 passed / 1 failed / 1 reasoned
- **`dependency-updater-tools.yml` → PASSED** (valid YAML, loaded into expected dict).
- **`.github/copilot-instructions.md` block → PASSED** (valid Markdown, drops in clean).
- **`python3 scripts/validate_quest.py --quest q4` → FAILED.** Same nonexistent script
  as quest 1; the *only* literally runnable command in the quest cannot run.
- Content-accuracy finding (score 2): the quest presents natural-language "Forbidden
Tools" prose in `copilot-instructions.md` as `least-privilege` *enforcement*; the engine flags this as a soft prompt guardrail, not a hard boundary — reasoned, not a command failure.

### 3. Cloud Computing Fundamentals (80%, pass) — ran 5/5 runnable, 3 passed / 2 failed / 4 skipped / 2 reasoned
- **`aws --version` / `az version` / `gcloud version` → PASSED** against real
  pre-installed CLIs (aws-cli 2.35.11, azure-cli 2.87.0, Google Cloud SDK 574.0.0).
- **`brew` / `winget` install blocks → SKIPPED** (macOS/Windows-only; correctly gated
  in collapsible OS sections). **Linux `curl … | sudo bash` / `sudo ./aws/install`
  → SKIPPED** per sandbox policy (needs sudo + network).
- **`aws sts get-caller-identity` and `aws ec2 describe-availability-zones …` → FAILED**
with `Unable to locate credentials` — syntax is correct AWS CLI v2, but no account is configured; the quest never warns this is expected without the optional free-tier account.
- Chapter sorting/service-mapping text blocks → REASONED correct.

### 4. Forging the Arsenal — Tool Use & Environment / codex-02 hub (67%, warn) — ran 11/4 runnable, 10 passed / 1 failed / 2 reasoned
- **Hands-On Lab Steps 1, 3, 4 → PASSED.** The engine ran every command and outputs
matched the documented "Expected" blocks **byte-for-byte** (two transient failures absorbed → success on attempt 3, exit=0; then permanent failure → escalation → exit=1). This is the strongest hands-on lab in the slice.
- **All config snippets → PASSED** (`.vscode/mcp.json` valid JSON; allow-list JSONC
valid; `permissions:` block + `agent-task.yml` valid GitHub Actions YAML). Note: this quest correctly wraps its YAML in `{​% raw %​}…{​% endraw %​}` blocks (lines 152–160, 273–299) — the exact pattern quest 1 got wrong.
- **Closing "break the wrapper — delete `exit 1`, watch exit=0" exercise → FAILED.**
The engine removed only the `exit 1` line and re-ran: the `until` loop ran **forever**, re-escalating on every pass, force-killed after 60s (exit 143). The quest's claimed `exit=0` is factually wrong — and this is the chapter's central safety lesson.
- Content-accuracy also flags the unverifiable **"GH-600"** certification identifier
  (exact "20–25%" domain weight, sub-skills 2.1–2.4) — reasoned, author should verify.

### 5. The MCP Conclave — MCP Servers (37%, fail) — ran 5/6 runnable, 1 passed / 4 failed / 2 skipped / 4 reasoned
- **`npx @modelcontextprotocol/server-github` (bash) → PASSED but DEPRECATED.** Returned
a valid `tools/list` response *and* printed `npm warn deprecated @modelcontextprotocol/server-github@2025.4.8: Package no longer supported.`
- **PowerShell block → FAILED.** Real pwsh threw `ParserError: Expressions are only
allowed as the first element of a pipeline` on `$env:GITHUB_PERSONAL_ACCESS_TOKEN=$env:GITHUB_TOKEN` (source lines 164–166) — invalid syntax; a Windows learner is blocked.
- **Custom `src/index.js` MCP server → FAILED.** Written verbatim, `npm install
@modelcontextprotocol/sdk` pulled current v1.29.0, `node src/index.js` crashed: `Error: Schema is missing a method literal` at `Server.setRequestHandler`. The string-based `setRequestHandler("tools/list", …)` API (source lines 224, 245) no longer exists in the SDK.
- **`.vscode/settings.json` `github.copilot.chat.mcpServers` key → REASONED wrong.**
Parses as JSON but the settings key doesn't match current VS Code MCP format (`mcp.servers` / `.vscode/mcp.json` `servers`).
- **`python3 scripts/validate_quest.py --quest q5` → FAILED** (nonexistent script, third
  occurrence). `gh secret set` correctly SKIPPED (not authenticated).

## 🐞 Issues Found

**High severity**

- **high · Observability (Q1) · Chapter 2, `agent-with-tracing.yml`, source lines
163–203** — Leaked `{​% raw %​}`/`{​% endraw %​}` tags *inside* every `${​{ }​}` expression (8×) produce `${​% raw %​}{​{ github.run_id }​}{​% endraw %​}`. *Observed:* engine reproduced `bad substitution` (exit 1); the workflow can never interpolate. *Fix:* wrap the whole `run:`/YAML block in a single `{​% raw %​} … {​% endraw %​}` pair (the pattern codex-02 uses correctly) so the rendered page shows plain `${​{ github.run_id }​}`.

- **high · Observability, Tool-Selection, MCP-Conclave · "Quest Validation" sections
(Q1 line 306, Q2 line 202, Q5 line 304)** — All three end with `python3 scripts/validate_quest.py --quest qN`. *Observed:* every invocation fails with `No such file / FileNotFoundError`; the script exists nowhere in the quest content. *Fix:* ship/link the script alongside the quest scaffold, or replace the block with concrete manual `test -f …` checks the learner can actually run.

- **high · codex-02 hub (Q4) · Hands-On Lab Step 4 closing exercise, source line 408** —
"delete the `exit 1` line and re-run — watch the run end `exit=0`" is false. *Observed:* removing only `exit 1` leaves the `until` loop unbounded → infinite retry
  + re-escalation, force-killed at 60s. *Fix:* have the learner also break the loop
(comment the retry / add `break`), or rewrite to a genuine false-green case, and warn a naive removal hangs and needs Ctrl+C.

- **high · MCP Conclave (Q5) · Chapter 2 + 4** — `npx @modelcontextprotocol/server-github`
is deprecated upstream (confirmed via npm warn) and Chapter 4's custom server crashes on the current SDK. *Observed:* deprecation warning on run; `Error: Schema is missing a method literal` on `node src/index.js`. *Fix:* move to the current `github/github-mcp-server` (remote `https://api.githubcopilot.com/mcp/` or Docker `ghcr.io/github/github-mcp-server`); update handlers to the schema-based API (`ListToolsRequestSchema` / `CallToolRequestSchema`) or pin the SDK version, and re-test end-to-end.

- **high · Tool-Selection (Q2) · Chapter 3, `copilot-instructions.md` permissions** —
Presents markdown "Forbidden Tools" prose as real least-privilege *enforcement*. *Observed (reasoned):* this is a prompt-level guardrail, bypassable by injection/drift; the actual enforcement surfaces (Copilot env/MCP allow-lists, branch protection, `GITHUB_TOKEN` scoping) are never mentioned. **This matters especially for the Security Specialist path** — the character whose whole premise is real boundaries. *Fix:* add an explicit caveat and point to the real enforcement mechanisms.

**Medium severity**

- **medium · Cloud Fundamentals (Q3) · Secondary Objectives, lines 106–107** — "Deployment
Models" and "The Economics of Elasticity" are listed but the terms never appear anywhere in the body (verified: reasoned + engine word-search). *Fix:* add short sections or remove the objectives so the quest doesn't promise untaught content.
- **medium · MCP Conclave (Q5) · Windows PowerShell block, lines 164–166** — Broken
pipe/assignment sequencing (ParserError) + missing `-y` on `npx`. *Fix:* set the env var as its own statement before the pipe; add `-y`.
- **medium · codex-02 (Q4) · "GH-600" certification claims** — Exact domain weight
("20–25%") and sub-skill numbering presented as verified exam fact but unverifiable. *Fix:* confirm against Microsoft Learn or label as illustrative.
- **medium · Cloud Fundamentals (Q3) · Linux install path, lines 187–188** —
  `curl … | sudo bash` and `sudo ./aws/install` shown with no safety caution for a
  beginner-facing quest. *Fix:* add a one-line "review before piping to sudo" note.

**Low severity**

- **low · Cloud Fundamentals (Q3) · Chapter 2 AWS commands** — `aws sts
get-caller-identity` and `describe-availability-zones` error with `Unable to locate credentials` for anyone without the optional account; no warning that this is expected.
- **low · Tool-Selection (Q2) · Exercise 4.1, line 116** — Depends on "the dependency
  updater agent you designed in Q1"; no inline fallback for a windowed learner.
- **low · MCP Conclave (Q5) · Chapter 5** — `export GITHUB_TOKEN=…` lands in shell
  history; suggest a git-ignored `.env` for local dev, not just "prod".

## 🔗 Chain Continuity

Reasoning about the window as one journey a Security Specialist learner would actually take:

1. **Two interleaved tracks, not one path.** Four quests are the GH-600 "Agentic Codex"
sub-line (`quest_series: agentic-ai-mastery` / `The Agentic Codex`, `quest_line: gh-600`), while **Cloud Computing Fundamentals** is a separate series (`Cloud Journey` / `The Warrior's Skybridge`, `required_quests: []`, unlocking AWS/Terraform/Azure). Walked in plan order the learner lurches from *agent tool permissions* → *IaaS/PaaS/SaaS* → back to *agent MCP servers*. Both tracks are legitimately Level-1000/Cloud-themed, but the window does not read as a single continuous story. Not a per-quest defect — a slice coherence observation.

2. **The agentic sub-chain is well linked, but the hub comes late.** `quest_dependencies`
wire observability → tool-selection → mcp-conclave cleanly. codex-02 ("Forging the Arsenal: Tool Use & Environment") is the **Domain-2 field guide/hub** — it explicitly lists tool-selection and mcp-conclave as "the quests of this domain, walk them in order." Yet the window presents the hub *fourth*, after the learner has already done tool-selection. Because codex-02 has `required_quests: []` it sorts loosely; ideally the field guide precedes its own sub-quests. Minor ordering friction.

3. **Inconsistent numbering will confuse a learner.** The three "Qn" quests use *two*
schemes at once: observability's `sub_title` says "Quest 1/4 — Domain 1" but its mermaid diagram and validation call it **Q3**; tool-selection is "Quest 2/4" but **Q4**; MCP is "Quest 3/4" but **Q5**. A learner cross-referencing "Q1" (as Exercise 4.1 in tool-selection asks them to) has no unambiguous anchor.

4. **A systemic validation dead-end across the sub-chain.** Three of the four agentic
quests close with the identical unrunnable `scripts/validate_quest.py`. The *one* that doesn't — codex-02 — instead teaches self-verification via observable exit codes, which is the model the others should follow. So the chain's own best quest already demonstrates the fix for its siblings. This is the clearest chain-level signal in the slice.

5. **A shared deprecated dependency propagates through the chain.** codex-02's
`.vscode/mcp.json` example *and* the MCP Conclave both reference `@modelcontextprotocol/server-github`. The engine only JSON-validated the hub's copy but actually *ran* the Conclave's and surfaced the deprecation warning — so the same soon-dead package is baked into two linked quests. Fixing one without the other leaves the chain half-broken.

6. **Prerequisite reality for a windowed learner.** observability assumes Domain-1 quests
(SDLC, Three Sigils) not in this window — acceptable for a rotating sweep — but tool-selection's Exercise 4.1 hard-depends on a Q1 artifact with no inline fallback, so that step is not self-contained for someone entering at this window.

**Net:** the agentic sub-chain *structurally* holds together (dependencies and unlocks are coherent), but three verified code defects and one systemic validation gap mean a learner walking it end-to-end would be blocked at the first workflow, misled by the safety lab's climax, and unable to run any of the three closing validations. The cloud primer stands on its own and is the healthiest link.

## 🧠 Reasoning & Method

- **Mode: execute, evidence sealed by the workflow.** I consumed `./walk-plan.json` and
`./walk-evidence.json` / `.md` exactly as provided — the deterministic workflow step ran `test/quest-validator/agentic_validate.py --mode execute` and sealed the results (the engine's child `claude` processes can't authenticate from an agent Bash tool). I did **not** re-run, regenerate, or edit any of those files, and I made **no** edits to quest content. My only write is this report.
- **What was tested vs. reasoned:** every `passed`/`failed` above comes from a command the
engine actually ran in the disposable sandbox (`executed: true` for all five quests). Items labelled REASONED were judged statically (illustrative diagrams/text, or commands unsafe/impossible to run in-sandbox: live `gh api` against a real repo, `sudo`/network installs, VS Code GUI Copilot Chat, authenticated `gh secret set`). My chain-continuity findings (§Chain Continuity) are my own static reasoning over the five quest sources read in plan order, cross-checked against the engine's per-quest findings — I cite source line numbers and the engine's real command outcomes, and invent nothing.
- **Coverage & limits:** this is **window 1 of 2** — 5 of the level's 9 quests
(`stats.windowed: true`). The remaining 4 quests are out of scope for this run and were not walked; the level cannot be certified from this session alone. Sandbox constraints meant OS-specific installers, live-cloud/live-GitHub mutations, and GUI steps were legitimately skipped rather than forced — noted per quest above. Engine cost for the sealed pass: **$3.0534**.
- **Confidence: high** on the reproduced code defects (bad-substitution, infinite loop,
SDK crash, PowerShell ParserError, missing validation script) — these were executed and are deterministic. **Medium** on the certification-identifier and enforcement-model accuracy points, which are reasoned and warrant author verification. **Overall slice verdict: FAIL**, driven by 3 failing quests and a systemic, chain-wide validation gap.
