---
title: 'Walkthrough — Security Specialist · Level 1011 (Security & Compliance)'
date: '2026-07-16T00:00:00.000Z'
character: security-specialist
level: '1011'
theme: Security & Compliance
tier: Warrior
quest_count: 5
mode: execute
overall_verdict: warn
session:
  window: '1 of 3 (5 of 12 quests in the level)'
  average_score: 77.2
  counts: '2 pass · 2 warn · 1 fail'
  engine_cost_usd: 3.505
  evidence: walk-evidence.json / walk-evidence.md (sealed by the workflow; consumed as-is)
  note: >-
    Machine evidence was pre-computed and sealed by the quest-perfection workflow's
    deterministic execute-engine step; the walker consumed it read-only and added the
    linked-journey reasoning. No quest content was modified.
---

## 🎯 Session Summary

I walked a **5-quest rotating window** (window 1 of 3, quests 1–5 of the 12 in
`security-specialist` / level `1011` — *Security & Compliance*, Warrior tier 🔥) as a
learner, in the dependency-sorted order the planner fixed. Evidence comes from the
sealed agentic **execute** engine (commands actually run in a disposable sandbox);
I layered the linked-journey reasoning on top by reading each quest source in order.

**Headline verdict: ⚠️ warn.** Two quests are genuinely strong and verified end-to-end
(*The Sealed Evidence* 94, *Threat Modeling* 91); two are solid-but-flawed with
reproducible defects (*Failure Recovery* 65, *Secure Coding* 77); one **fails** (*AI
Feature Pipeline Architect* 59) because only its first chapter is runnable while
Chapters 2–5 are unrunnable sketches — and it is still `draft: true`. The bigger
story for a maintainer is **continuity**: this window is not one learning chain but a
*bundle of four unrelated quest-lines that merely share the level code*, and three of
the five assume prerequisite quests/scaffold that live **outside** the window.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|--:|:--:|---|--:|---|
| 1 | ⚠️ | When Familiars Fall: Multi-Agent Failure Recovery | 65 | Core `recovery_coordinator.py` verified across 3 scenarios, but a likely GitHub Actions `continue-on-error` logic bug and 3 missing referenced scripts undercut the objectives. |
| 2 | ❌ | AI Feature Pipeline Architect: DevSecOps Mastery Quest | 59 | Chapter 1 (Intake) works end-to-end; Chapters 2–5 of the promised "5-stage pipeline" are architecture sketches referencing undefined classes. Still `draft: true`. |
| 3 | ✅ | The Sealed Evidence: Slaying the Self-Grading Golem | 94 | Mint→seal→forge→restore→ledger chain reconstructed and executed — every step behaved exactly as documented; both Mermaid diagrams render. |
| 4 | ⚠️ | Secure Coding: Preventing the OWASP Top 10 | 77 | Most snippets (bcrypt, bandit, npm/pip-audit, allowlist, subprocess) run as documented; 3 reproducible defects: Docker `-it` in non-TTY, `detect-secrets` misses untracked files, SQL `%s` vs stdlib sqlite3. |
| 5 | ✅ | Threat Modeling: STRIDE Framework and Attack Trees Analysis | 91 | Clean, accurate Hard-level quest; the runnable snippet + Mermaid DFD executed and all 9 external links resolved. Only gap: "Living Threat Models" objective is checklisted, never taught. |

Average **77.2%** · 2 ✅ / 2 ⚠️ / 1 ❌ · engine cost ≈ $3.51.

## 🔬 Evidence

All statuses below are from the sealed execute run (`walk-evidence.json`). Coverage is
reported as *runnable snippets executed vs. reasoned/skipped*; installer blocks for
other OSes and network calls to external repos were correctly reasoned/skipped, not run.

### 1. When Familiars Fall: Multi-Agent Failure Recovery — ⚠️ 65
Dimensions: commands 3 · accuracy 3 · completeness 3 · clarity 3 · structure 4 · safety 5.
Coverage: 6 blocks — **4 executed (3 passed, 1 failed), 2 reasoned.**
- ✅ `python3 work/gh-600/scripts/recovery_coordinator.py …` — **passed in all three
  scenarios**: (1) sub-agent-1 failed + checkpoint present → `retry_from_checkpoint`,
  `needs_redelegation=false`; (2) failed + no checkpoint → `redelegate`,
  `needs_redelegation=true`; (3) both agents failed, zero result files → degraded
  gracefully to `task:'unknown'` instead of crashing on a missing key.
- ❌ `python3 scripts/validate_quest.py --quest q16` — **failed**: *"can't open file …
  scripts/validate_quest.py: [Errno 2] No such file or directory"*. The validator the
  quest tells the learner to run is never provided anywhere in the content.
- 🧠 (reasoned) The `orchestrator-with-recovery.yml` block only parses as valid YAML
  **after** stripping literal `{% raw %}…{% endraw %}` tags wrapped around every
  `${{ }}`; the engine flagged that `recover-and-report` reads `needs.sub-agent-1.result`
  while that job sets job-level `continue-on-error: true` — a documented GHA gotcha where
  the result reports `success` downstream, which would silently disable failure detection.

### 2. AI Feature Pipeline Architect — ❌ 59
Dimensions: commands 3 · accuracy 3 · completeness 2 · clarity 3 · structure 3 · safety 4.
Coverage: 14 blocks — **7 executed (6 passed, 1 failed), 3 skipped (other-OS installers), 4 reasoned.**
- ✅ `pip install langchain anthropic openai mcp`, the devcontainer JSON, the universal
  workflow object, the `user_story_schema.json`, and `intake_agent.py` imports all
  **passed** (compiles, imports cleanly).
- ❌ `echo "…" | python intake_agent.py` — **failed** without `ANTHROPIC_API_KEY`
  (unhandled `KeyError: 'ANTHROPIC_API_KEY'`, matching the quest's own warning). Re-run
  with a fake key **reached the real Anthropic API** → `anthropic.AuthenticationError:
  401 - invalid x-api-key`, confirming Chapter 1 wiring is real.
- 🧠 (reasoned) `ImplementationOrchestrator`, `DocumentationAgent`, `TestingOrchestrator`,
  `DeploymentOrchestrator` (Chapters 2–5) reference agent classes that are **never
  defined** and carry no save/run instructions — unrunnable as written.

### 3. The Sealed Evidence: Slaying the Self-Grading Golem — ✅ 94
Dimensions: commands 5 · accuracy 5 · completeness 4 · clarity 4 · structure 5 · safety 5.
Coverage: 11 blocks — **9 executed, all passed; 1 reasoned, 1 skipped (external `gh api`).**
- ✅ The full **mint → seal → forge → restore → ledger** chain was reconstructed and run:
  the mint step wrote `evidence.txt`, seal copied it to `$RUNNER_TEMP/sealed`, the
  boss-fight forgery edited `evidence.txt` to fake success, the restore step's
  `cmp -s` **caught the tamper** and restored the sealed copy, and the ledger `grep FAIL`
  parse then reflected the true result — *every step behaved exactly as documented.*
- ✅ Both Mermaid diagrams (architecture `graph TD`, quest-network `graph LR`) rendered
  without syntax errors.
- ⏭️ `gh api repos/bamr87/it-journey/pulls/433` skipped (external repo, not reproducible
  standalone) — the one completeness gap for an isolated learner.

### 4. Secure Coding: Preventing the OWASP Top 10 — ⚠️ 77
Dimensions: commands 3 · accuracy 4 · completeness 4 · clarity 4 · structure 5 · safety 5.
Coverage: 14 blocks — **9 executed (8 passed, 1 failed), 5 reasoned (incl. 3 other-OS installers).**
- ✅ Passed as documented: bcrypt (`gensalt(rounds=12)` / `checkpw`), the parameterized-vs-
  concat SQL contrast, `subprocess.run` list-form vs `shell=True`, the allowlist
  `re.fullmatch(r"[A-Z]{2}\d{6}", …)`, `os.environ["API_KEY"]`, `detect-secrets scan`,
  `pip-audit` / `npm audit` / `npm audit fix`, and `bandit -r ./src`.
- ❌ `docker run --rm -it python:3.12-slim bash -lc "…"` — **failed**: *"the input device
  is not a TTY"*. Re-running with `-it` removed **succeeded** and printed `Python 3.12.13`.
- 🧠 (reasoned) `detect-secrets scan` without `--all-files` only scans git-tracked files,
  so a freshly-created secret file the section is trying to catch produces a false
  all-clear; the SQL `%s` placeholder does not work with Python's stdlib `sqlite3`
  (qmark `?` style), so a learner testing it with the built-in module hits a syntax error.

### 5. Threat Modeling: STRIDE Framework and Attack Trees — ✅ 91
Dimensions: commands 4 · accuracy 5 · completeness 4 · clarity 5 · structure 5 · safety 5.
Coverage: 8 blocks — **2 executed passed, 3 skipped (other-OS installers), 3 reasoned.**
- ✅ The cloud-path echo snippet and the **Chapter 1 Mermaid DFD** (User → Web App → DB /
  Payment Provider with trust boundaries) executed/rendered successfully; all **nine
  external resource links resolved live**.
- 🧠 (reasoned) STRIDE walk-through, attack tree, and DREAD/priority table are prose/table
  teaching blocks (nothing to execute) and are internally consistent.

## 🐞 Issues Found

Grouped by quest, severity from the sealed engine's own recommendations, each tied to a
witnessed command result or a quoted source concern. These are **for a content pass** —
no fixes were made here.

**When Familiars Fall (⚠️ 65)**
- **high** · Ch. 2 recover-and-report job — `needs.sub-agent-1.result` is read while
  that job uses job-level `continue-on-error: true`; the known GHA behavior reports
  `success` downstream, silently defeating the "failure detection" objective. *Fix:*
  thread the custom `needs.sub-agent-1.outputs.status` (as sub-agent-2 already does) and
  align `recovery_coordinator.py`'s check (`failed` vs `failure`). *(reasoned)*
- **high** · Missing scripts — `subtask.py`, `save_checkpoint.py`, `redelegate_tasks.py`
  are referenced for the "retry/backoff" and "re-delegation" objectives but never shown.
  *Fix:* provide them or scope the quest to assessment/compensation only. *(reasoned)*
- **medium** · Quest Validation — `scripts/validate_quest.py` does not exist; the final
  step **fails outright** (tested). *Fix:* ship the script or use a manual checklist.
- **medium** · YAML block leaks literal `{% raw %}`/`{% endraw %}` into the fenced code —
  a learner copying from the raw `.md` gets invalid YAML (tested: only parses after
  stripping). *Fix:* pre-render or escape differently.
- **low** · Add a "before you begin" note stating the assumed `work/gh-600/scripts/`
  scaffold state from the prior quest. *(reasoned)*

**AI Feature Pipeline Architect (❌ 59)**
- **high** · Chapters 2–5 reference undefined agent classes with no save/run steps — the
  "5-stage pipeline" objective is not demonstrable. *Fix:* label as pseudocode **or**
  flesh out to Chapter-1 rigor. *(reasoned)*
- **high** · MCP is a Primary Objective but `self.mcp_session` stays `None`; add a minimal
  working transport/session example. *(reasoned)*
- **medium** · `model="claude-3-5-sonnet-latest"` is stale — update to a current alias.
- **medium** · `intake_agent.py` raises a raw `KeyError` on a missing `ANTHROPIC_API_KEY`
  (tested) — wrap with a friendly check.
- **medium** · macOS block: `brew install docker` installs only the CLI, not the daemon
  the stated requirement needs; add `brew install --cask docker`. *(reasoned)*
- **low** · Validation is self-assessed checkboxes only; add checkable success criteria.
- **low** · "Architectural Decision Records" artifact required but no ADR template shown.
- **process** · The quest is `draft: true` — either it should not appear in the learner
  path yet, or it needs to graduate; shipping a fail-scoring draft in the sweep is a
  mixed signal.

**The Sealed Evidence (✅ 94)**
- **medium** · Mastery Challenge points at an external repo's workflow file with no inline
  starting artifact — a learner outside `bamr87/it-journey` has nothing to extend. *(reasoned)*
- **low** · PR #433 reference is unverifiable offline (skipped) — add a short inline diff.
- **low** · Note that `uses: ./.github/actions/claude-run` and `.claude/agents/potion-scribe.md`
  are repo-specific so learners know which parts to swap. *(reasoned)*

**Secure Coding (⚠️ 77)**
- **high** · Cloud Realms Docker snippet uses `-it` and **fails** with "input device is not
  a TTY" non-interactively (tested; works with `-it` removed). *Fix:* drop `-it` or use `-i`.
- **medium** · `detect-secrets scan` without `--all-files` misses untracked files —
  undermines the very "never commit secrets" scenario. *Fix:* recommend `--all-files`. *(reasoned)*
- **medium** · SQL `%s` placeholder fails with stdlib `sqlite3` — specify a driver or use `?`. *(reasoned)*
- **low** · Two `@app.get("/invoices/<invoice_id>")` blocks would raise a Flask duplicate-
  endpoint error if pasted together — rename the secure version. *(reasoned)*
- **low** · XSS snippet is browser-only (Node has no DOM) — note it or add a jsdom variant. *(reasoned)*

**Threat Modeling (✅ 91)**
- **low** · "Living Threat Models" secondary objective is checklisted but never taught —
  add a short callout on revisiting the model as the design changes. *(reasoned)*
- **low** · Author double-check the `Microsoft.ThreatModelingTool` winget id still resolves
  (couldn't re-verify live from the sandbox). *(reasoned)*

**No blocking issues** exist for the two ✅ quests beyond the standalone-reproducibility
notes above; they are safe and accurate for a learner.

## 🔗 Chain Continuity

Read in plan order, this window does **not** behave like one linear learning chain — it
is a **date-rotated window (1 of 3) over the 12 quests that share level code `1011`**, and
those 12 span **four unrelated quest-lines**:

- *Failure Recovery* → `quest_series: agentic-ai-mastery` / `quest_line: gh-600`
- *AI Feature Pipeline Architect* → `AI-Enhanced Development Mastery Path`
- *Sealed Evidence* → `The Autonomous Realm` / `The Ouroboros Loop`
- *Secure Coding* & *Threat Modeling* → `Security Mastery` / `The Warrior's Bastion`

**Within-window continuity that holds (good):** *Secure Coding* (#4) declares
`unlocks_quests: /quests/1011/threat-modeling/` and *Threat Modeling* (#5)
`recommends /quests/1011/secure-coding/`. This adjacent pair is a real, coherent
sub-chain — a learner finishing Secure Coding is genuinely ready for Threat Modeling,
and both only require the same out-of-window `security-fundamentals`.

**Prerequisite gaps (three of five reach outside the window):**
- *Failure Recovery* (#1) requires `/quests/1011/agentic-multi-agent-observability/`
  (Q15, not in this window) and assumes a `work/gh-600/scripts/` scaffold already exists
  from a prior quest — a learner starting cold here has no scaffold and the final
  validation step fails.
- *AI Feature Pipeline Architect* (#2) lists prereq "Completion of Level 1001 (Backend)"
  and is `draft: true` — a learner browsing the published curriculum wouldn't normally
  reach it, and if they did, Chapters 2–5 dead-end.
- *Sealed Evidence* (#3) recommends `/quests/0011/ouroboros-loop-03-summon-the-golem/`
  and assumes a working "scribe golem" repo + a Claude Code OAuth token; it's excellent
  in isolation but its Mastery Challenge/PR reference need the external `it-journey` repo.

**Ordering observation:** the planner's dependency sort is fine *mechanically*, but the
learner-facing takeaway is that "level 1011 for security-specialist" is a **thematic
bucket, not a single path**. The Security Mastery pair is the true spine for this
character; the agentic/pipeline/ouroboros quests are cross-listed at the same tier and
each belong to their own campaign. A maintainer deciding "is 1011 perfect for
security-specialist" should weight the Security Mastery line most heavily — and there the
news is good (Secure Coding 77 with fixable defects, Threat Modeling 91).

## 🧠 Reasoning & Method

- **Mode:** `execute` (sandboxed). I did **not** run the engine — per the skill and the
  workflow design, `walk-evidence.json` / `walk-evidence.md` were pre-computed and
  **sealed** by a deterministic workflow step (the engine's child `claude` processes
  can't authenticate from an agent's Bash tool). I consumed them **read-only** and made
  no edits to the plan or evidence.
- **What I ran vs. reasoned:** every `passed`/`failed` above is a command the sealed
  engine **actually executed** in a disposable temp dir (quoted outputs are its real
  results). Items marked *(reasoned)* were judged statically — by me from the quest
  source, or by the engine where a block was prose, an other-OS installer, or an external
  network call it correctly declined to run. I ran **zero** commands myself; my
  contribution is the linked-journey reasoning (reading all five sources in plan order).
- **Coverage / limits:** this is window **1 of 3** — 5 of the 12 quests in the level. The
  perfection ledger accumulates the other two windows over subsequent runs; this report
  does **not** certify the whole level. Snippet coverage varied (2/8 executed on the
  conceptual Threat Modeling quest up to 9/11 on Sealed Evidence); other-OS installers and
  external-repo/network calls were skipped by design, not overlooked. No timeout occurred
  (engine ran to completion, ≈$3.51).
- **Confidence:** high on the two ✅ quests and on the tested defects (Docker `-it`,
  missing `validate_quest.py`, `intake_agent.py` KeyError — all reproduced live). Medium
  on the `continue-on-error` GHA bug and the "missing scripts" scope gaps, which were
  reasoned/statically flagged rather than executed end-to-end in a real multi-job run.
- **Scope discipline:** one slice, one report. No quest content, data, or config was
  modified; no branch/commit/PR was made. The caller handles git.

---

<details><summary>Appendix — machine evidence (verbatim from <code>walk-evidence.md</code>)</summary>

Sealed engine summary: **5 quests · ✅ 2 pass · ⚠️ 2 warn · ❌ 1 fail · avg 77.2% · ≈$3.505.**
See `walk-evidence.json` for full per-dimension scores, the exact commands the engine ran,
and its recommendations, all of which are cited inline above.

</details>
