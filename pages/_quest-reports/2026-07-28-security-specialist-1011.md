---
title: Security Specialist · L1011 · 2026-07-28
description: Quest-perfection walkthrough of the Security & Compliance slice security-specialist/1011
  on 2026-07-28, engine verdict warn. An evidence-based…
date: '2026-07-28T00:00:00.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Security Specialist
tags:
- security-specialist
- level-1011
- walkthrough
- quest-perfection
- warn
- security-compliance
render_with_liquid: false
excerpt: 'Security Specialist · Level 1011 — Security & Compliance: an evidence-based quest-perfection
  walkthrough from 2026-07-28.'
slice: security-specialist/1011
character: security-specialist
level: '1011'
theme: Security & Compliance
tier: Warrior 🔥
verdict: warn
quest_count: 5
walk_date: '2026-07-28'
run_url: https://github.com/bamr87/it-journey/actions/runs/30355858267
source_report: test/quest-validator/walkthroughs/2026-07-28-security-specialist-1011.md
---

> **Slice** `security-specialist/1011` · **Level** 1011 (Security & Compliance) · **Warrior 🔥 tier** · **Engine verdict** ⚠️ warn · **Walked** 2026-07-28
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/30355858267) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-28-security-specialist-1011.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-28-security-specialist-1011.md)

---

## 🎯 Session Summary

I walked the first **window of 5 quests (of 12)** in the Security Specialist's Level `1011` — "Security & Compliance," the Warrior tier — as a learner would, driving the sealed execute-mode evidence the workflow minted for me and reading every quest's source in plan order to reason about the linked journey.

**Headline: WARN.** The average is 75.0% (3 pass / 2 fail). The genuine security core of this level — **Secure Coding (94)** and **Threat Modeling (91)** — is excellent: technically accurate, safe, well-structured, and every runnable snippet was executed in the sandbox and behaved exactly as claimed. **The Sealed Evidence (83)** is a strong architecture lesson on evidence integrity. But **two of five quests fail on real, verified defects**: *AI Feature Pipeline Architect (50)* ships 4 of its 5 promised pipeline stages as unrunnable pseudocode (every Chapter 2–5 class raises `NameError`/`AttributeError` on instantiation — tested), and it is still flagged `draft: true` in frontmatter; *When Familiars Fall (57)* has a reproduced path-mismatch bug between its code-block header paths and its validation checks, plus a plausible GitHub Actions `continue-on-error` semantics bug that undercuts its core lesson.

A maintainer's highest-value action: treat the two failing quests as content-fix candidates (they carry concrete, cited defects below), and recognize that the slice is a **binary-level grouping, not a single character arc** — see Chain Continuity for why only 2 of the 5 form a true linked pair for this class.

## 🗺️ The Journey

Walked in planner order (`walk-plan.json`), all 🔴 Hard `main_quest`:

1. ❌ **When Familiars Fall: Multi-Agent Failure Recovery** — **57** — Standalone recovery coordinator runs correctly, but a *reproduced* file-path mismatch and a `continue-on-error`/`needs.result` semantics bug undermine the workflow; 3 of 5 objectives are unimplemented filenames.
2. ❌ **AI Feature Pipeline Architect: DevSecOps Mastery** — **50** — Chapter 1 (intake) is genuinely excellent and fully verified; Chapters 2–5 are unrunnable skeletons (undefined agents). Still `draft: true`.
3. ✅ **The Sealed Evidence: Slaying the Self-Grading Golem** — **83** — Mint→seal→tamper→restore chain simulated end-to-end and behaves exactly as claimed; one load-bearing security claim can't be verified offline.
4. ✅ **Secure Coding: Preventing the OWASP Top 10** — **94** — Every runnable snippet executed and matched the quest, including a subtle verified `detect-secrets` caveat. Best quest in the slice.
5. ✅ **Threat Modeling: STRIDE Framework and Attack Trees** — **91** — STRIDE/DREAD/attack-tree content all accurate, all 9 reference links live (HTTP 200), Mermaid DFD parses; mostly-conceptual so few runnable snippets.

## 🔬 Evidence

All per-quest verdicts, commands, and snippet counts below are from the **sealed `walk-evidence.json`** (execute mode, engine cost ~$3.53, not `--mock`). Quoted outcomes are the engine's real sandbox results; I did not re-run the engine (its child processes can't authenticate from my Bash tool).

### 1. When Familiars Fall — 57 ❌ (snippets: ran 4, passed 4, reasoned 2; 2 runnable of 4 available)
- `python3 recovery_coordinator.py … --agent1-status failure …` → **passed**. Ran twice with synthetic artifacts: emitted `retry_from_checkpoint` when a checkpoint existed and `redelegate` otherwise; correctly wrote `needs_redelegation=true` / `failed_tasks=sub-agent-1` to `$GITHUB_OUTPUT`.
- `test -f orchestrator-with-recovery.yml` → **passed at workspace root**, but the engine **reproduced exit code 1** when the file is placed at `.github/workflows/…` — the path the code block's own header comment specifies. Same for `recovery_coordinator.py` vs `work/gh-600/scripts/`.
- `grep -oiE "retry|fallback|escalat|compensat|checkpoint" recovery_coordinator.py … | wc -l` → **passed** (returned 5, as documented).
- Chapter 2 workflow YAML → **reasoned**: parses as valid YAML (PyYAML); no `act`/runner available, so the `continue-on-error` behavior was judged statically, not executed.

### 2. AI Feature Pipeline Architect — 50 ❌ (snippets: 14 total, 13 runnable, ran 11 — 6 passed, 5 failed, 3 skipped)
- `pip install langchain anthropic openai mcp` → **passed** (anthropic 0.120.0, mcp 1.28.1, langchain 1.3.14, openai 2.49.0).
- `intake_agent.py` / `RequirementProcessor` → **passed**: imports resolve; no-key run raises the documented `SystemExit`; a fake key reaches Anthropic and returns a real `401 invalid x-api-key` — proving the Chapter 1 path is correct end-to-end.
- `ImplementationOrchestrator()` → **failed**: `NameError: name 'CodeGenerationAgent' is not defined`.
- `DocumentationAgent.generate_docs(...)` → **failed**: `AttributeError … 'generate_openapi_spec'`.
- `TestingOrchestrator.run_testing_pipeline(...)` → **failed**: `AttributeError … 'unit_test_agent'`.
- `DeploymentOrchestrator.deploy_feature(...)` → **failed**: `AttributeError … 'risk_agent'`.
- Universal Web Path JS `aiPipeline.orchestrate('test')` → **failed**: `ReferenceError: processFeatureRequest is not defined`.
- macOS/Windows/Linux bootstrap blocks → **skipped** (OS-mismatched / require sudo).

### 3. The Sealed Evidence — 83 ✅ (snippets: 5 total, 0 standalone-runnable, ran 3, passed 3, skipped 2)
- Chapter 2 mint→seal→consume→restore YAML → **passed**: engine extracted the shell logic and simulated it — mint wrote `evidence.txt` + `status=fail`; seal copied to a stand-in `$RUNNER_TEMP/sealed/`; a forged `passed: true` overwrite was caught by `cmp -s`, fired the `::warning::`, and `cp -f` restored the true failing evidence. "Behavior matches the quest's claims exactly."
- Both Mermaid diagrams → **passed** (rendered via mermaid-cli).
- Chapter 1 diagnostic prompt + Boss-fight prompt → **skipped**: require a live golem/CI harness that doesn't exist in the sandbox (matches the stated "0 runnable").
- The central claim (harness scrubs `CLAUDE_CODE_OAUTH_TOKEN` from agent subprocesses) → **reasoned**: internally consistent and cited, but not independently verifiable offline.

### 4. Secure Coding — 94 ✅ (snippets: 14 total, 14 runnable, ran 12, passed 12, skipped 2)
- SQL injection demo → **passed**: concat query with `' OR '1'='1` leaked all rows; parameterized query returned zero.
- Command injection → **passed**: `shell=True` executed the injected `echo INJECTED`; list-form `subprocess.run` failed safely.
- XSS `innerHTML` vs `textContent` (jsdom) → **passed**; allowlist validator → **passed**; bcrypt hash/verify (bcrypt 5.0.0) → **passed**; Flask authz (stubbed) → 403 → **passed**.
- `detect-secrets scan` → **passed**, flagged the planted `sk_live_…` key; and the engine **reproduced the quest's own caveat** — run outside a git repo it produces `"results": {}` (clean-looking empty baseline) with only a stderr `fatal: not a git repository`.
- `pip-audit` / `npm audit` / `npm audit fix` (planted lodash@4.17.15) → **passed** (real CVEs reported, then fixed to 0); `bandit -r ./src` → **passed** (B602/B608 flagged as documented).

### 5. Threat Modeling — 91 ✅ (snippets: 8 total, 4 runnable, ran 2, passed 2, reasoned 3, skipped 3)
- Cloud `echo "Open https://www.threatdragon.com/ …"` → **passed** (exact expected output; URL verified HTTP 200).
- Mermaid DFD → **passed**: installed real `mermaid` npm package, `mermaid.parse()` succeeded as `flowchart-v2`.
- All 9 external documentation links checked live → **HTTP 200**; STRIDE/DREAD/attack-tree text → **reasoned** (illustrative, matches canonical definitions).
- macOS/Windows/Linux setup blocks → **skipped** (OS/sudo-gated — environmental, not a quest defect).

## 🐞 Issues Found

Everything below is either a sandbox-verified result or a static reading of the quest source (labeled `reasoned`). Grouped by quest, severity-ordered.

**When Familiars Fall (57):**
- **high · content/paths · Ch.2–3 code-block headers vs Quest Validation · tested** — The `.yml` header comment says `.github/workflows/orchestrator-with-recovery.yml` and the `.py` header says `work/gh-600/scripts/recovery_coordinator.py` (both are literally invoked at those nested paths inside the workflow), but the Validation block runs `test -f orchestrator-with-recovery.yml` / `test -f recovery_coordinator.py` at the **workspace root**. Engine reproduced exit 1 under the natural nested-path reading. *Fix:* make paths consistent — either check the nested paths or tell learners to place both files flat at the root and drop the header-comment paths.
- **high · content_accuracy · Ch.2 `continue-on-error: true` + `needs.sub-agent-1.result` · reasoned** — With `continue-on-error: true`, a failed job reports **`success`** to dependents, so `--agent1-status "${​{ needs.sub-agent-1.result }​}"` will read `success` even when sub-agent-1 truly failed — silently defeating the failure-detection that is the whole point (Objective 2). *Fix:* pass the job's own captured `steps.run.outputs.status` downstream, or drop `continue-on-error` and use `if: always()` + explicit step outputs.
- **medium · completeness · undefined scripts · reasoned** — `subtask.py`, `save_checkpoint.py`, `redelegate_tasks.py` are invoked at 5 call sites but never defined, so objectives "Apply a retry strategy (backoff)" and "Implement re-delegation" have no runnable implementation. *Fix:* provide minimal stubs or explicitly scope them out as assumed-from-a-prior-quest.
- **low · rendering · `{​% raw %​}` tags inline in Actions expressions · reasoned** — Copying from the raw `.md` yields invalid YAML/expression text until stripped. *Fix:* confirm the render pipeline strips them.
- **low · structure · validation depth · reasoned** — Validation only checks file presence + a keyword count; it never exercises the recovery logic, so it can't catch either bug above.

**AI Feature Pipeline Architect (50):**
- **high · commands/completeness · Chapters 2–5 unrunnable · tested** — `ImplementationOrchestrator/DocumentationAgent/TestingOrchestrator/DeploymentOrchestrator` all raise `NameError`/`AttributeError` on first instantiation/call because `CodeGenerationAgent`, `SecurityAgent`, `unit_test_agent`, `risk_agent`, etc. are never defined. 4 of the 5 promised pipeline stages are non-functional. *Fix:* provide minimal (even mocked) stubs, or clearly relabel these blocks as "architecture sketch / pseudocode — not runnable."
- **high · completeness · "5-stage pipeline" objective unmet · tested/reasoned** — Only Stage 1 is implemented. *Fix:* scale down the objective claim or add real Step-1/2/3 walkthroughs for stages 2–5.
- **medium · publication state · `draft: true` in frontmatter · reasoned** — This quest is still marked `draft: true` (line 51) yet is being served/planned at Level 1011. A maintainer should decide whether it should be in the walkable curriculum at all given its completeness gaps.
- **medium · content_accuracy · stale model id · reasoned** — `model="claude-3-5-sonnet-latest"` is a legacy alias. *Fix:* use a current identifier or an env-var placeholder.
- **medium · content_accuracy · `brew install copilot-cli` · reasoned** — Not a documented Homebrew formula. *Fix:* use `npm install -g @githubnext/github-copilot-cli` or `gh extension install github/gh-copilot`.
- **medium · completeness · ADR deliverable never shown · reasoned** — "Architectural Decision Records" is a required portfolio artifact but no template/example appears. *Fix:* add one.
- **low · commands · Universal Web Path JS · tested** — `processFeatureRequest` undefined → `ReferenceError`. *Fix:* define it or label as illustrative.
- **low · safety/clarity · Linux `newgrp docker` · reasoned** — Opens a subshell that won't chain with subsequent copy-pasted commands. *Fix:* add a note.

**The Sealed Evidence (83):**
- **medium · content_accuracy · unverifiable core claim · reasoned** — The `CLAUDE_CODE_OAUTH_TOKEN` subprocess-scrub claim (the quest's most load-bearing point) can't be verified from the quest alone offline. *Fix:* link/quote the specific security-doc section, not just the general page.
- **low · commands · no standalone repro · reasoned** — None of the 5 blocks run for a learner working alone. *Fix:* add a minimal `check.sh` + mint/seal/restore repro that needs no workflow/golem.
- **low · clarity · Ch.2 has no "before" snippet · reasoned**; **low · pedagogy · knowledge-check answer key absent · reasoned**.

**Secure Coding (94):**
- **medium · completeness · "Security Headers" secondary objective · reasoned** — Asserted in prose only; no CSP/HSTS code example unlike every other objective. *Fix:* add a Flask `after_request`/nginx/Express snippet.
- **medium · completeness · Advanced Challenge CI step · reasoned** — Challenge requires "Add a CI step that runs all three," but no CI YAML is shown anywhere. *Fix:* add a minimal GitHub Actions snippet.
- **low · content_accuracy · SQL `%s` vs sqlite3 `?` · tested** — The snippet uses `%s` (psycopg2/MySQLdb paramstyle); sqlite3 (common quick-start) uses `?`, so a copy-paste into sqlite3 errors. *Fix:* name the driver or note the difference.
- **low · clarity · unlabeled pseudocode · reasoned** — The intro SQL snippet and the authorization snippet use undefined `cursor`/`db`/`current_user`/`login_required`. *Fix:* one-line "illustrative fragment" note.

**Threat Modeling (91):**
- **medium · completeness · "Living Threat Models" objective never taught · reasoned** — Listed as a secondary objective but never discussed in any chapter body. *Fix:* add a short section (re-run STRIDE on DFD change, tie to PR/design review).
- **low · setup · winget package ID staleness · reasoned** (add a fallback download link); **low · setup · `sudo snap install code` alternative · reasoned** (offer apt/Flatpak); **low · pedagogy · no sample answers for knowledge checks · reasoned**.

**No blocking issue** exists in the three passing quests — their gaps are completeness/polish, not correctness. The two failing quests carry the real, actionable defects.

## 🔗 Chain Continuity

The most important finding of the linked-journey pass is that **this slice is a binary-level grouping, not a single character arc.** Level `1011` bundles every quest tagged `level: '1011'`, and the planner's window drew 5 of them from **four different quest series/lines**:

| # | Quest | quest_series / line | Its declared prerequisites | In this window? |
|---|---|---|---|---|
| 1 | When Familiars Fall | agentic-ai-mastery / gh-600 | `/quests/1011/agentic-multi-agent-observability/` (Q15) | ❌ no |
| 2 | AI Feature Pipeline Architect | AI-Enhanced Development Mastery | Level 1001 Backend, API/Testing tracks | ❌ no |
| 3 | The Sealed Evidence | The Autonomous Realm / Ouroboros Loop | `/quests/0011/ouroboros-loop-03-summon-the-golem/` | ❌ no |
| 4 | Secure Coding | Security Mastery / Warrior's Bastion | `/quests/1011/security-fundamentals/` | ❌ no (but same line) |
| 5 | Threat Modeling | Security Mastery / Warrior's Bastion | security-fundamentals; recommends secure-coding | ✅ **secure-coding is #4** |

**The one true linked pair is #4 → #5.** Secure Coding's frontmatter `unlocks_quests` lists `/quests/1011/threat-modeling/`, and Threat Modeling's `recommended_quests` lists `/quests/1011/secure-coding/`; the "Character Class Recommendations" and attack-tree leaves in Threat Modeling (SQL injection → parameterized queries, XSS → HttpOnly+CSP, IDOR → server-side authz) map cleanly onto the exact defenses Secure Coding just taught. A learner finishing Secure Coding is genuinely ready for Threat Modeling — strong continuity, and both are on the **Security Specialist's on-path Security Mastery line** (the class this session represents). This pair alone is a satisfying, coherent mini-journey.

**The other three are isolated members of arcs whose real prerequisites sit outside the window.** A Security Specialist dropped cold into *When Familiars Fall* is assumed to have completed *Multi-Agent Observability* (Q15) and to understand GitHub Actions `continue-on-error`; into *AI Feature Pipeline Architect*, to have completed a Level 1001 backend track; into *The Sealed Evidence*, to have "Chapters I–III" of the Ouroboros Loop with a working golem, an OAuth token, and an existing multi-chapter CI workflow. None of those setups are provided by earlier quests **in this slice**, so as a standalone linear read the window has three cold-starts. That is a *windowing/planner artifact* (level = binary code, not a curriculum path) rather than a defect in the quests — but it does mean the ledger should not treat these five as one dependency chain, and a real Security Specialist would experience this level as four parallel tracks, only one of which (Security Mastery) is squarely their class.

Character-fit note: #3–#5 are genuinely security-themed (`skill_focus: security`); #1 and #2 are agentic/DevSecOps and lean more DevOps than security-specialist core, though DevSecOps overlaps the class.

## 🧠 Reasoning & Method

- **What I ran vs. reasoned:** I did **not** run the execute engine — per the skill and the run instructions, the `quest-perfection`/`quest-walkthrough` workflow pre-computed and **sealed** `walk-evidence.json` (execute mode, real, non-mock, ~$3.53) because the engine's child `claude` processes can't authenticate from an agent's Bash tool. I consumed that evidence verbatim. Every `passed`/`failed` in §🔬 is the engine's real sandbox result. I then read all five quest sources in plan order and reasoned about the linked journey, frontmatter dependencies, and character fit (§🔗). Issues drawn from the engine's own runs are labeled `tested`; issues I derived by reading the source (undefined scripts, `draft: true`, `{​% raw %​}` tags, missing objectives, the Actions `continue-on-error` semantics) are labeled `reasoned`.
- **Sandbox/mode:** execute, disposable runner sandbox. Legitimate environmental caps: macOS/Windows/sudo/snap blocks were skipped (no such platform in a Linux sandbox), GitHub Actions workflows couldn't be truly executed (no `act`/runner), and one offline-unverifiable claim (token scrubbing) was reasoned — none of these are quest defects and I've marked them as such.
- **Coverage honesty:** This is **window 1 of 3** — 5 of the level's 12 quests. I did **not** walk the remaining 7; the ledger accumulates coverage across runs and should not certify Level 1011 `perfect` until the full sweep passes. Snippet coverage varied widely by quest (Secure Coding 12/14 executed; Threat Modeling only 2 of 4 runnable executed due to OS-gating; The Sealed Evidence 0 standalone-runnable by design). I made zero edits to any quest, plan, or evidence file, and I open no PR — this report is the sole artifact.
- **Confidence:** High on the two failing quests (their defects are directly reproduced/executed in the sealed evidence and corroborated by the source). High on the two Security Mastery passes. Medium on The Sealed Evidence's single unverifiable security claim. High on the Chain Continuity analysis (derived directly from each quest's frontmatter `quest_dependencies`/`prerequisites`).

**Overall verdict: WARN** — a strong, verified security core (Secure Coding, Threat Modeling, The Sealed Evidence) alongside two quests that fail on real, cited completeness/correctness defects (AI Feature Pipeline Architect, When Familiars Fall) that a content pass should repair.
