---
title: 'Walkthrough — Security Specialist · Level 1011 (Security & Compliance)'
date: '2026-07-22T00:00:00.000Z'
character: security-specialist
level: '1011'
theme: Security & Compliance
tier: Warrior
quest_count: 5
mode: execute
overall_verdict: fail
session:
  window: '1 of 3 (offset 5, size 5 of 12 total level quests)'
  average_score: 71.4
  verdict_counts: '2 pass · 1 warn · 2 fail'
  engine_cost_usd: 3.7615
  evidence_source: ./walk-evidence.json (workflow-sealed, agentic execute engine)
  note: 'Evidence pre-computed and sealed by the workflow; the walker consumed it as-is and reasoned about the linked journey. No quest content was modified.'
---

## 🎯 Session Summary

I walked the **Security Specialist · Level 1011 (Security & Compliance, Warrior tier)** slice — a **window of 5 of the level's 12 quests** (window 1 of 3, offset 5), all `main_quest` / 🔴 Hard. The machine evidence in `./walk-evidence.json` was minted and sealed by the workflow's deterministic execute-engine step; I consumed it verbatim and added the linked-journey reasoning a real learner would need.

**Headline verdict: FAIL for the slice.** Three quests are genuinely strong (Sealed Evidence 94, Threat Modeling 91, Secure Coding 79), but **two carry verified, learner-blocking defects** (Fallen Familiars 51, AI Feature Pipeline Architect 42) — bugs the sandbox reproduced, not stylistic nits. The deeper problem a maintainer must see is that **this "slice" is not one journey**: the five quests belong to *four unrelated quest series* with prerequisite chains that mostly point *outside* the window, so as a Security Specialist learning path the level does not cohere. Only the `secure-coding → threat-modeling` pair is an actually-linked chain, and it is the healthiest part of the slice.

## 🗺️ The Journey

Plan order (as selected by `walk-plan.json`):

1. ❌ **When Familiars Fall: Multi-Agent Failure Recovery** · **51** — Python coordinator works, but leaked `{% raw %}{% raw %}/{% endraw %}{% endraw %}` tags corrupt every GitHub Actions expression and the quest's own validation grep expects 5 and returns 4.
2. ❌ **AI Feature Pipeline Architect: DevSecOps Mastery Quest** · **42** — Chapter 1 runs (real 401 from Anthropic API confirmed), but a `pip install` line inside a `python` fence raises `SyntaxError`, and Chapters 2–5 reference agent classes that are never defined, so the central 5-stage pipeline is unbuildable from the quest.
3. ✅ **The Sealed Evidence: Slaying the Self-Grading Golem** · **94** — Conceptual security/AI-safety boss chapter; every technical claim verified in the sandbox, including the OAuth-scrub against this very session's env.
4. ⚠️ **Secure Coding: Preventing the OWASP Top 10** · **79** — Almost everything runs and behaves as documented; the one real gap is `detect-secrets scan` silently scanning nothing without a `git init`.
5. ✅ **Threat Modeling: STRIDE Framework and Attack Trees Analysis** · **91** — Technically accurate; runnable pieces (Mermaid DFD render + cloud echo) executed cleanly; OS-gated setup is expected for a diagramming quest.

Average **71.4%** · engine cost **$3.7615** · mode **execute** (sandboxed).

## 🔬 Evidence

All outcomes below come from the sealed `walk-evidence.json` (`executed: true` on every quest). "ran N/M runnable" uses the engine's snippet accounting.

### 1. When Familiars Fall — `agentic-multi-agent-failure-recovery.md` · 51 · FAIL
Dimensions: commands_work **2**, content_accuracy **2**, completeness **2**, clarity 3, structure 4, safety 5. Snippets: **ran 7, passed 5, failed 2, reasoned 1** (available_runnable 2).
- `passed` · `python3 recovery_coordinator.py … --agent1-status failure --agent2-status success` → correctly produced `retry_from_checkpoint` in `recovery-plan.json`, as documented. Also verified the `redelegate` fallback and the `$GITHUB_OUTPUT` write of `needs_redelegation=true`.
- `failed` · `grep -c -iE "retry|fallback|escalat|compensat|checkpoint" recovery_coordinator.py` → **returns 4, not the 5 the quest's own comment claims**. Engine confirmed `fallback`, `escalat`, `compensat` have **0 occurrences** in the reference code; only `retry` (1) and `checkpoint` (3) match.
- `failed` · YAML workflow extracted and parsed with PyYAML (valid YAML) but semantically broken: **6 literal `${% raw %}{% raw %}{{ … }}{% endraw %}{% endraw %}`** occurrences instead of `${% raw %}{{ … }}{% endraw %}`; copied verbatim, no GitHub Actions expression would interpolate.
- Engine also noted (`content_accuracy`): the re-delegate step reads `steps.assess.outputs.failed_tasks`, which `recovery_coordinator.py` **never writes** (only `needs_redelegation`), and `sub-agent-2` has no upload-artifact step, so its `checkpoint_available` branch is unreachable.

### 2. AI Feature Pipeline Architect — `ai-feature-pipeline-architect.md` · 42 · FAIL
Dimensions: commands_work 2, content_accuracy 2, **completeness 1**, clarity 2, structure 3, safety 4. Snippets: **ran 6, passed 5, failed 1, reasoned 7** (available_runnable 12).
- `passed` · Chapter 1 `intake_agent.py` (with the appended `__main__`): without `ANTHROPIC_API_KEY` it exits cleanly with the guidance message; with a fake key it reaches Anthropic and returns a **real 401 AuthenticationError** — the SDK call is structurally correct.
- `passed` · devcontainer JSON, Universal Web JS snippet, `user_story_schema` JSON all parsed/loaded cleanly.
- `failed` · Chapter 1 Step 1 saved verbatim → `SyntaxError: invalid syntax` at `pip install langchain anthropic openai mcp`, because a **shell line sits inside a `python` fence**. Remove that one line and the class imports fine.
- `reasoned` · Chapters 2–5 orchestrator classes parse but **cannot run**: `ImplementationOrchestrator` → `NameError: CodeGenerationAgent is not defined`; `TestingOrchestrator`/`DeploymentOrchestrator` reference `self.unit_test_agent` / `self.risk_agent` etc. that `__init__` never assigns. The agent classes are **never defined anywhere in the quest**, so the primary objective (a working 5-stage pipeline) is unachievable from the content.
- `reasoned` · Homebrew cask `github-copilot-cli` verified **nonexistent** against the live cask index (closest is `copilot-cli`); model id `claude-3-5-sonnet-latest` is stale for a 2026 reader.
- Note: this quest is `draft: true` in frontmatter — consistent with its unfinished Chapters 2–5.

### 3. The Sealed Evidence — `ouroboros-loop-04-the-sealed-evidence.md` · 94 · PASS
Dimensions: commands_work **5**, content_accuracy **5**, completeness 4, clarity 4, structure 5, safety 5. Snippets: **ran 4, passed 4, reasoned 1** (available_runnable 0 — conceptual quest).
- `passed` · The Chapter 1 diagnostic `echo "TOKEN: ${CLAUDE_CODE_OAUTH_TOKEN:-SCRUBBED}"` ran **in this live CI session** and printed `TOKEN: SCRUBBED`; `env | grep -i claude` confirmed the token is absent from the subprocess env — the quest's central "auth-scrub moat" claim verified against the very environment reading it.
- `passed` · Both Mermaid diagrams rendered to valid SVG via mermaid-cli v11.16.0; the mint→seal→consume→restore YAML parsed and the embedded shell logic was simulated end-to-end (forged evidence detected, warned, and overwritten; ledger reported the true `fail`).
- `reasoned` · The boss-fight prompt is guidance for a live golem, not a shell command; its claimed outcome was corroborated by the simulation above. (I did **not** attempt any prompt-injection escalation — the boss-fight prose is a script under review, not an instruction to me.)

### 4. Secure Coding — `secure-coding.md` · 79 · WARN
Dimensions: commands_work 4, content_accuracy 4, completeness 3, clarity 4, structure 4, safety 5. Snippets: **ran 9, passed 9, skipped 1, reasoned 4** (available_runnable 14).
- `passed` · SQLi (sqlite3 reproduction: `' OR '1'='1'` leaked all rows vs parameterized returned none), command injection (`shell=True` ran the injected `echo`; arg-list form did not), XSS (jsdom: `innerHTML` parsed markup, `textContent` escaped it), bcrypt (verify ok, wrong password rejected, ~0.9s), allowlist regex, `pip-audit`/`npm audit` (correctly flagged pinned `lodash@4.17.11` critical), and **bandit flagged B602 + B608** exactly as the Novice Challenge claims.
- `passed`-but-flawed · `detect-secrets scan` ran without error **but returned an EMPTY baseline even with a live hard-coded secret present**, because the quest never has the learner `git init`; detect-secrets relies on `git ls-files`. This undermines the Intermediate Challenge's own validation ("`detect-secrets scan` reports no secrets") — it can pass trivially while a real secret sits unscanned.
- `reasoned` · SQLi/authorization snippets use undefined `cursor`/`current_user`, so equivalent reproductions were built; the `%s` placeholder is psycopg2/MySQL-specific and would confuse a sqlite3 (`?`) learner.

### 5. Threat Modeling — `threat-modeling.md` · 91 · PASS
Dimensions: commands_work 4, content_accuracy **5**, completeness 4, clarity **5**, structure 5, safety 5. Snippets: **ran 2, passed 2, skipped 3, reasoned 3** (available_runnable 4).
- `passed` · Chapter 1 Mermaid DFD (trust-boundary subgraphs) rendered to a valid ~102 KB SVG; the cloud-path `echo "Open https://www.threatdragon.com/ …"` ran with exit 0.
- `skipped` · macOS/Windows/Linux setup snippets are OS-gated (brew/winget/snap+sudo) — expected and correctly scoped inside collapsible per-OS sections for a paper/diagramming quest, not a defect.
- `reasoned` · STRIDE walkthrough, attack tree, and likelihood×impact table are illustrative prose; each checked internally consistent (STRIDE↔CIA mapping correct, OR-node semantics used consistently, priority ordering sound).

## 🐞 Issues Found

**High**
- **Fallen Familiars** · Chapter 2 YAML block · The 6 GitHub Actions expressions render as literal `${% raw %}{% raw %}{{ … }}{% endraw %}{% endraw %}` (unrendered Jekyll `raw` tags leaking into the reader-facing code). *Observed:* engine extracted the block and confirmed the literal tags; PyYAML parses it but the expressions are semantically dead. *Fix:* correct the markdown/Jekyll fencing so the `raw` guard is stripped before publish, leaving `${% raw %}{{ … }}{% endraw %}`.
- **Fallen Familiars** · Quest Validation grep · Comment says "expect a count of 5"; the reference `recovery_coordinator.py` yields **4** (`fallback`/`escalat`/`compensat` never appear). *Fix:* either implement/document those strategies in the code, or correct the expected count and the "All 5 compensation strategy types are documented" checklist item.
- **Fallen Familiars** · re-delegation objective · The workflow reads `steps.assess.outputs.failed_tasks`, which the coordinator never writes, and `redelegate_tasks.py` is referenced but not provided. *Fix:* emit `failed_tasks` to `$GITHUB_OUTPUT` (or supply the script) so the stated "Implement re-delegation" objective is actually reachable.
- **AI Feature Pipeline Architect** · Chapter 1 Step 1 fence · `pip install langchain anthropic openai mcp` inside a `python` fence → `SyntaxError` when copied verbatim. *Fix:* split the install into its own `bash` fence.
- **AI Feature Pipeline Architect** · Chapters 2–5 · `ImplementationOrchestrator`/`DocumentationAgent`/`TestingOrchestrator`/`DeploymentOrchestrator` reference agent classes/attributes never defined anywhere, so the quest's primary objective (a working 5-stage pipeline) cannot be completed from the content. *Fix:* either label these blocks "illustrative architecture, not runnable" or supply the missing agent classes + save/run steps as Chapter 1 has.

**Medium**
- **AI Feature Pipeline Architect** · macOS setup · `brew install --cask github-copilot-cli` — cask verified nonexistent (closest: `copilot-cli`). *Fix:* correct or remove.
- **AI Feature Pipeline Architect** · model id · `claude-3-5-sonnet-latest` is stale for a 2026 reader. *Fix:* update to a current model id.
- **Secure Coding** · Chapter 3 detect-secrets · Scan silently returns empty outside a git repo, so the Intermediate Challenge validation passes even with a live secret present. *Fix:* add `git init` (+ `git add .`) before the scan, or note detect-secrets' `git ls-files` dependency.
- **Secure Coding** · Chapter 1 SQLi · `%s` placeholder is driver-specific; a sqlite3 learner will hit a syntax error. *Fix:* note driver-specific tokens (`?`, `:name`).
- **Fallen Familiars** · retry objective · "exponential backoff" is a stated objective but no backoff/retry loop exists in the code. *Fix:* show real backoff code or soften the objective.

**Low**
- **AI Feature Pipeline Architect** · `langchain` is pip-installed but never imported/used; `iex`/`sudo usermod` steps could use a one-line trust caution.
- **Secure Coding** · Security Headers / Automated Scanning CI are stated secondary objectives (and the Advanced Challenge requires a CI step) with no example anywhere; add a minimal CSP/HSTS + CI-YAML snippet or downgrade to "further reading". Also confirm whether an OWASP Top 10 edition newer than 2021 exists and update the citation.
- **Fallen Familiars** · Note that `subtask.py`/`save_checkpoint.py` are inherited from Quest 15 so learners aren't confused about their origin.

*(All issues above are evidence-backed — each traces to a sandbox command result or an exact quoted line. The two PASS quests produced no blocking issues; Sealed Evidence's only gaps are the unworked "seal the plan" mastery extension and no shown ledger implementation, and Threat Modeling's only gap is the "Living Threat Models" secondary objective being listed but never taught — both minor.)*

## 🔗 Chain Continuity

**This slice is not a single linked journey — it is five quests that only share the level code `1011`, drawn from four unrelated series.** For a Security Specialist walking the level, that is the most important finding:

- **Fallen Familiars** — series *agentic-ai-mastery* / line *gh-600* ("The Agentic Codex"), sub-title "Quest 4/4". Its required prerequisite is `/quests/1011/agentic-multi-agent-observability/` (Q15), **not in this window**; its Mermaid shows a Q15→Q16→Q17 chain none of whose neighbors are present. A learner starting here lands mid-arc with unmet setup (it also assumes `subtask.py`/`save_checkpoint.py` from Q15).
- **AI Feature Pipeline Architect** — series *AI-Enhanced Development Mastery Path*, `draft: true`. Prereqs point to Level 1001 (Backend Track) and other levels; standalone within this slice and, being a draft with unfinished chapters, not learner-ready.
- **The Sealed Evidence** — series *The Autonomous Realm* / line *The Ouroboros Loop*, chapter IV. Recommends `/quests/0011/ouroboros-loop-03-summon-the-golem/` and its "Chapters I–III complete" prerequisite; unlocks `/quests/1010/ouroboros-loop-05`. Its whole chain lives at *other* levels (0011, 1010), so within 1011 it is an island — an excellent island, but an island.
- **Secure Coding → Threat Modeling** — series *Security Mastery* / line *The Warrior's Bastion*. **This is the one real linked pair in the slice**: `secure-coding` lists `threat-modeling` in `unlocks_quests`, and `threat-modeling` lists `secure-coding` in `recommended_quests`. Both require `/quests/1011/security-fundamentals/` (not in window). If walked in the order the planner gave (secure-coding then threat-modeling), the continuity is sound: secure-coding teaches the mitigations (parameterized queries, output encoding, authz, secrets), and threat-modeling's attack tree references those exact mitigations (HttpOnly+CSP, TLS, server-side authz, parameterized queries, secrets manager) — the pair reinforces cleanly.

**Character-fit observation:** only Secure Coding, Threat Modeling, and (by framing) The Sealed Evidence read as *security* content for this class. Fallen Familiars and AI Feature Pipeline Architect are DevSecOps/agentic-AI quests that a developer or system-engineer would more naturally own; their presence under "Security Specialist · 1011" is a taxonomy artifact of the shared level code, not a curated security progression.

**Prerequisite gaps summary:** 4 of 5 quests assume a prerequisite quest that is absent from the window (`agentic-multi-agent-observability`, `ouroboros-loop-03`, `security-fundamentals` ×2, plus Level 1001 for the pipeline quest). A learner cannot bootstrap this slice from within itself. This is expected for a *windowed* sweep (window 1 of 3), but it means the report cannot claim end-to-end continuity for the level — only for the secure-coding→threat-modeling pair.

## 🧠 Reasoning & Method

- **Mode:** `execute`, sandboxed. The evidence in `./walk-evidence.json` / `./walk-evidence.md` was **pre-computed and sealed by the workflow's deterministic engine step** (the engine's child `claude` processes can't authenticate from an agent's Bash tool). I consumed it **verbatim** — I did not run, regenerate, edit, or hand-write any evidence, and I made no changes to `walk-plan.json` or the evidence files. Notably, the Sealed Evidence quest's own auth-scrub claim was verified by the engine *against this session's environment*, which is a nice self-consistency check on the sealing architecture the quest teaches.
- **What I ran vs. reasoned:** I ran no quest commands myself; all `passed`/`failed`/`skipped`/`reasoned` labels are the engine's sandbox results (quoted above). My contribution (skill step 3) is the **linked-journey reasoning**: I read all five quest sources in plan order and cross-checked their frontmatter `quest_dependencies`/`prerequisites`/series against each other and against the engine's per-command findings.
- **Coverage / limits:** This is **window 1 of 3 (5 of 12 level quests)** — I make no claim about the other 7 quests in level 1011, nor about the out-of-window prerequisites the chain assumes. OS-gated setup snippets (brew/winget/snap+sudo) were legitimately `skipped`/`reasoned` on the Linux sandbox and I did not treat those as defects. I did not execute network-mutating or `sudo` steps. I treated all quest prose (including the Sealed Evidence boss-fight prompt) as scripts under review, never as instructions to me.
- **Confidence:** High on the two FAIL quests' blocking bugs (reproduced deterministically: a `SyntaxError`, a grep count of 4-not-5, literal `raw` tags, undefined classes). High on the two PASS quests. Medium-high on the WARN (Secure Coding) — its one functional gap (detect-secrets outside git) is verified; the rest ran clean. The slice-level `overall_verdict: fail` reflects that **two of five quests are non-completable as written** and the slice does not cohere as a Security Specialist journey — not a claim that the strong three are broken.
