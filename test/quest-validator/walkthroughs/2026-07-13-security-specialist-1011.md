---
title: 'Walkthrough — Security Specialist · Level 1011 (Security & Compliance) · Window 1/3'
date: '2026-07-13T13:11:26.000Z'
character: security-specialist
level: '1011'
theme: Security & Compliance
tier: Warrior
quest_count: 5
mode: execute
overall_verdict: fail
session:
  planner_window: '1 of 3 (offset 5, size 5)'
  total_level_quests: 12
  windowed: true
  engine_average: 66.0
  engine_counts: '2 pass · 1 warn · 2 fail'
  engine_cost_usd: 3.4591
  evidence_source: ./walk-evidence.json (sealed by workflow; consumed as-is)
---

## 🎯 Session Summary

I walked a **5-quest window** (window 1 of 3, offset 5) of the Security Specialist's Level **1011 — Security & Compliance (Warrior tier)** as a learner, using the sealed machine evidence the workflow pre-computed in `--mode execute` (I did **not** re-run the engine). The window is a bimodal slice: the genuine security line (**Secure Coding**, 82% ✅ and **Threat Modeling**, 91% ✅) is technically sound and its runnable snippets behave as claimed, but the three AI/agentic quests that share the `1011` level code — **Multi-Agent Failure Recovery** (50% ❌), **AI Feature Pipeline Architect** (30% ❌, and `draft: true`), and **The Sealed Evidence** (77% ⚠️) — range from partially-broken to almost-entirely-non-functional when their code is actually executed.

The headline verdict is **fail** for the slice as a walkable path: two of five quests have code that does not run as written (verified in the sandbox — a leaked Jekyll `{% raw %}` template in Actions YAML, a checkpoint-key naming mismatch, a nonexistent PyPI package, and five unimplemented stub classes), and a learner following the level in order hits those walls. The core Security-Mastery arc a security specialist would actually take is healthy; the failures are cross-listed non-security content swept in by level code. A maintainer's highest-value action is to fix (or de-list) the two failing quests and decide whether they belong on this character's path at all.

## 🗺️ The Journey

Quests in planner order (each: verdict · title · score · one-line takeaway):

1. ❌ **When Familiars Fall: Multi-Agent Failure Recovery** — **50** — solid narrative, but both runnable artifacts fail in the sandbox (leaked `{% raw %}` tags, checkpoint-key mismatch, deprecated `::set-output`) and 3 referenced scripts are never provided.
2. ❌ **AI Feature Pipeline Architect: DevSecOps Mastery Quest** — **30** — `draft: true`; reads well but 8 of its runnable snippets fail — nonexistent `mcp-client` package, wrong imports, and five unimplemented orchestrator stub classes. No working artifact is obtainable.
3. ⚠️ **The Sealed Evidence: Slaying the Self-Grading Golem** — **77** — conceptually excellent security architecture (mint→seal→consume→restore) that hand-simulates correctly, but has **no runnable local lab** and one under-cited platform claim.
4. ✅ **Secure Coding: Preventing the OWASP Top 10** — **82** — strongest hands-on quest; bcrypt/bandit/pip-audit/allowlist/command-injection snippets all run and behave as claimed. Two real bugs: `detect-secrets` scans only tracked files, and a `%s` SQL placeholder that fails on stdlib sqlite3.
5. ✅ **Threat Modeling: STRIDE Framework and Attack Trees Analysis** — **91** — accurate, well-structured conceptual quest; STRIDE/CIA/DREAD/attack-tree semantics all correct, and the one runnable snippet executed as described.

## 🔬 Evidence

All outcomes below come from the sealed `walk-evidence.json` (`executed: true`, `mock: false`, mode `execute`), where the engine ran each quest's safe snippets in a disposable sandbox. Verbatim summary from `walk-evidence.md`: **5 quests · ✅ 2 pass · ⚠️ 1 warn · ❌ 2 fail · avg 66.0% · ~$3.4591**.

### 1. When Familiars Fall: Multi-Agent Failure Recovery — 50% (fail)
Dimensions: commands_work **2**, content_accuracy **2**, completeness **2**, clarity 3, structure 3, safety 5. Snippets run: **4/2 (2✗)**.
- `passed` · mermaid Quest Network diagram parses.
- **`failed`** · yaml `orchestrator-with-recovery.yml` — parses, but contains literal
`${% raw %}{{ steps.run.outputs.status }}{% endraw %}` (×3): leaked Liquid templating that would land verbatim in a learner's `.github/workflows/*.yml` and silently break step-output interpolation.
- **`failed`** · `python recovery_coordinator.py --results-dir ./results/ --task-id test-task-123`
— with realistic downloaded-artifact JSON (`subtask1-result/subtask1-analysis.json`, `checkpoint_available=true`) the script produced strategy `redelegate`/task `unknown` instead of the expected `retry_from_checkpoint`, because `results.get(f"{agent_id}-result")` builds key `sub-agent-1-result` which never matches the `subtask1-*` naming used everywhere else in the same quest. Reproducible naming-mismatch bug that defeats the quest's core checkpoint-recovery objective even though the script exits 0.
- `passed` · same script with empty results dir + both agents failed (degenerate path runs).
- `skipped` · `python3 scripts/validate_quest.py --quest q16` — script not present in
  quest content (parent-repo infra), FileNotFoundError; not runnable from the quest alone.
- Also verified statically: the script emits deprecated `print("::set-output name=…")`
(disabled on GitHub runners since mid-2023) rather than writing `$GITHUB_OUTPUT`, so the downstream `if: fromJSON(steps.assess.outputs.needs_redelegation)` step never fires.
- `subtask.py`, `save_checkpoint.py`, `redelegate_tasks.py` are invoked in YAML but never
  defined — the workflow cannot run end-to-end even after the templating/output fixes.

### 2. AI Feature Pipeline Architect: DevSecOps Mastery Quest — 30% (fail)
Dimensions: commands_work **1**, content_accuracy **1**, completeness **1**, clarity 2, structure 2, safety 4. Snippets run: **10/11 (8✗)**. Frontmatter `draft: true`.
- `passed` · devcontainer.json `echo` write; `passed` · requirement schema JSON block.
- **`failed`** · `pip install langchain anthropic openai mcp-client` + `RequirementProcessor`
— `mcp-client` is not a real PyPI package; `from langchain.agents import Agent` and `from mcp import MCPClient` are not real exports; `Anthropic` is used but never imported.
- **`failed`** · `echo "…reset their passwords…" | python intake_agent.py` — `intake_agent.py`
  is never provided, so the "Expected output" claim is unreachable.
- **`failed` ×4** · Chapter 2–5 orchestrator classes (`ImplementationOrchestrator`,
`DocumentationAgent`, `TestingOrchestrator`, `DeploymentOrchestrator`) all reference undefined agent classes → NameError/AttributeError the instant they're exercised.
- **`failed`** · Windows Chocolatey bootstrap; `reasoned` · Linux apt block; `skipped` ·
macOS brew block (includes `brew install --cask github-copilot-cli`, which appears not to be a real cask). A learner cannot extract a single working artifact from this quest.

### 3. The Sealed Evidence: Slaying the Self-Grading Golem — 77% (warn)
Dimensions: commands_work 3, content_accuracy 4, completeness 4, clarity 4, structure 5, safety 5. Snippets run: conceptual (no directly-runnable learner snippets).
- `passed` · Chapter 1 diagnostic `echo "TOKEN: ${CLAUDE_CODE_OAUTH_TOKEN:-SCRUBBED}"`.
- `passed` · Chapter 2 MINT / SEAL / RESTORE shell steps hand-simulated with stub scripts:
  the `cmp -s` tamper guard + sealed-copy-wins restore logic behaves exactly as taught.
- `skipped` · CONSUME step (needs a live `claude-run` action + credentials — correctly
not exercised in-sandbox). `reasoned` · design/network mermaid diagrams and Boss-Fight adversarial prompt block.
- Gaps: no hands-on local lab (a learner only reads a CI-bound YAML fragment), and the
"agent harnesses scrub their own credentials" line reads as a platform-wide truth but is really describing a specific CI/action design choice.

### 4. Secure Coding: Preventing the OWASP Top 10 — 82% (pass)
Dimensions: commands_work 4, content_accuracy 4, completeness 4, clarity 4, structure 4, safety 5. Snippets run: **11/14 (2✗)**.
- `passed` · venv + `pip install bcrypt bandit pip-audit detect-secrets flask`; bcrypt
`hash_password`/`verify_password` (rounds=12); allowlist `re.fullmatch(r"[A-Z]{2}\d{6}", …)`; command-injection contrast (`subprocess.run(["cat", filename])`); Flask owner_id/`abort(403)` authz; `API_KEY = os.environ["API_KEY"]`; `pip-audit`; `npm audit`/`npm audit fix`; `bandit -r ./src` — all behave as the quest claims.
- **`failed`** · SQL-injection "fix": `cursor.execute("… %s", (username,))` — the `%s`
placeholder fails on Python's stdlib `sqlite3` driver (which uses `?`); the quest never names which driver `%s` targets.
- **`failed`** · `detect-secrets scan > .secrets.baseline` — silently scans only
git-tracked files, so the untracked-`.env` scenario the quest walks through reports "no secrets found", undermining the quest's own challenge validation criterion.
- `reasoned` · JS XSS `innerHTML` vs `textContent` contrast (correct as written).
- Platform setup blocks (brew/winget/apt/docker) `skipped` — legitimately OS-gated.

### 5. Threat Modeling: STRIDE Framework and Attack Trees Analysis — 91% (pass)
Dimensions: commands_work 4, content_accuracy 5, completeness 4, clarity 5, structure 5, safety 5. Snippets run: **1/4**.
- `passed` · Cloud-Realms `echo "Open https://www.threatdragon.com/ …"` executed as described.
- `reasoned` · Mermaid DFD with trust-boundary subgraphs, STRIDE walkthrough table, attack
  tree, and likelihood×impact priority table — all technically accurate.
- `skipped` · macOS/Windows/Linux editor-install blocks — legitimately OS-gated, not broken.
- Gap: the "Living Threat Models" secondary objective is listed (line 108) but never
  covered in a chapter; knowledge-check questions have no answer keys.

## 🐞 Issues Found

Every issue below is backed by a sandbox command result (`tested`) or an exact quoted line from the quest source (`reasoned`).

**HIGH** · *Multi-Agent Failure Recovery* · Ch.2 YAML `orchestrator-with-recovery.yml` (lines 126, 161, 191–193) · **tested** — leaked `${% raw %}{{ … }}{% endraw %}` Jekyll tags sit inside GitHub Actions expressions; copy-pasted verbatim they break step-output interpolation. *Fix:* strip the `{% raw %}`/`{% endraw %}` wrappers so learners get clean `${{ … }}` syntax.

**HIGH** · *Multi-Agent Failure Recovery* · Ch.3 `recovery_coordinator.py` line 245 · **tested** — `results.get(f"{agent_id}-result")` builds key `sub-agent-1-result` which never matches the `subtask1-result` artifact / `subtask1-*.json` path / `subtask1-analysis` stem used elsewhere, so checkpoint detection always falls through to `redelegate`. *Fix:* reconcile the artifact name, path glob, and lookup key on one scheme; verify with a fixture.

**HIGH** · *Multi-Agent Failure Recovery* · Ch.3 `recovery_coordinator.py` line 271 · **reasoned** — `print(f"::set-output name=needs_redelegation::…")` uses the deprecated (disabled) workflow command, so `steps.assess.outputs.needs_redelegation` is never set. *Fix:* write to `$GITHUB_OUTPUT` (e.g. via `os.environ['GITHUB_OUTPUT']`).

**HIGH** · *AI Feature Pipeline Architect* · Ch.1 Step 1 (lines 222–240) · **tested** — `pip install … mcp-client` (nonexistent package), `from mcp import MCPClient` / `from langchain.agents import Agent` (nonexistent exports), and `Anthropic(...)` used without import. *Fix:* `pip install mcp`; use the real `mcp`/`langchain` APIs; add `from anthropic import Anthropic`.

**HIGH** · *AI Feature Pipeline Architect* · Chapters 2–5 code blocks (lines 294–399) · **tested** — every orchestrator class instantiates undefined agent classes (`CodeGenerationAgent`, `SecurityAgent`, etc.) → NameError/AttributeError on execution. *Fix:* replace with one actually-runnable minimal example and clearly label the rest as architectural pseudocode.

**MEDIUM** · *AI Feature Pipeline Architect* · frontmatter (line 51) · **reasoned** — `draft: true`. A draft quest scoring 30% is being swept into a learner-facing level window. *Fix:* keep it out of walkable slices until it's promoted, or finish it.

**MEDIUM** · *AI Feature Pipeline Architect* · Ch.1 Step 3 (line 265) · **tested** —
`echo … | python intake_agent.py` references a file the quest never provides; its
"Expected output" claim is unreachable. *Fix:* provide `intake_agent.py` or drop the claim.

**MEDIUM** · *Secure Coding* · Ch.1 SQL example (line 214) · **tested** — the "secure" `cursor.execute("… %s", (username,))` fails on Python's stdlib `sqlite3` (`?` paramstyle); the driver is never named. *Fix:* state the target driver, or show both `?` and `%s` paramstyles with a note on which driver uses which.

**MEDIUM** · *Secure Coding* · Ch.3 secrets scan (line 349) + Intermediate Challenge (line 405) · **tested** — `detect-secrets scan` only scans git-tracked files, so the untracked-`.env` scenario reports no secrets, contradicting the challenge's validation. *Fix:* note that files must be tracked (or use `--all-files` / `git add -N`) before scanning.

**MEDIUM** · *The Sealed Evidence* · Ch.2 hands-on (lines 126–165) · **reasoned** — the mint/seal/restore logic is only presented as a CI-bound YAML fragment; there is no local lab to run. *Fix:* add an optional shell script with a fake `$RUNNER_TEMP` + `evidence.txt` so a learner can watch the tamper warning fire outside a live Actions run.

**MEDIUM** · *The Sealed Evidence* · Ch.1 credential-scrub claim (line 71/103) · **reasoned** — "agent harnesses scrub their own credentials" is stated as a blanket platform truth but describes a specific CI/action design choice. *Fix:* cite the concrete mechanism responsible for not exporting `CLAUDE_CODE_OAUTH_TOKEN` to subprocesses.

**LOW** · *Multi-Agent Failure Recovery* · completeness (lines 133/141) · **reasoned** — `subtask.py`, `save_checkpoint.py`, `redelegate_tasks.py` are referenced but never provided; 2 of 5 objectives (retry-with-backoff, re-delegation) have no code. *Fix:* provide minimal implementations or mark them explicitly out of scope.

**LOW** · *Threat Modeling* · Secondary objective (line 108) + knowledge checks · **reasoned** — "Living Threat Models" is listed but never covered; knowledge-check questions have no answer keys. *Fix:* add a short section (or drop the objective) and collapsed answer hints.

**LOW** · *AI Feature Pipeline Architect* · macOS setup (line 130) · **reasoned** — `brew install --cask github-copilot-cli` appears not to be a real cask; `docker-compose` (v1) is EOL. *Fix:* correct/remove the cask; prefer `docker compose` v2.

## 🔗 Chain Continuity

This window does **not** read as one linear chain — it is a level-code grouping, and that is the most important learner-facing finding:

- **Three different quest series share the `1011` level code.** The five quests belong
to (a) *Security Mastery / The Warrior's Bastion* (Secure Coding, Threat Modeling), (b) *agentic-ai-mastery / gh-600 / The Agentic Codex* (Multi-Agent Failure Recovery), (c) *AI-Enhanced Development Mastery Path* (AI Feature Pipeline Architect), and (d) *The Autonomous Realm / The Ouroboros Loop* (The Sealed Evidence). A Security Specialist walking the level in window order jumps between four unrelated storylines.

- **The only genuine internal link in this window is Secure Coding → Threat Modeling.**
`secure-coding` frontmatter `unlocks_quests` includes `/quests/1011/threat-modeling/`, and `threat-modeling` lists `secure-coding` as a recommended prerequisite. These two form the coherent, self-consistent security path — and, not coincidentally, they are the two passing quests (82, 91). This is the real Warrior's-Bastion arc for the class.

- **The other three quests depend on quests *outside* this window.** Multi-Agent Failure
Recovery requires `agentic-multi-agent-observability` (Q15, not in the window); AI Feature Pipeline Architect's prerequisites point at "Level 1001 Backend Development"; The Sealed Evidence recommends `ouroboros-loop-03-summon-the-golem` (level 0011). A learner arriving here mid-window has no in-window on-ramp to any of the three — each assumes setup the security path never provided.

- **Prerequisite realism for the security line:** Both Secure Coding and Threat Modeling
require `security-fundamentals` (level 1011), which is not in this window — it would fall in window 0/2. That's acceptable for a rotating window whose ledger accumulates coverage, but the level's *first* window should establish `security-fundamentals` before these two are walkable in earnest.

- **Draft leakage:** AI Feature Pipeline Architect is `draft: true` yet appears in the
learner-facing window; combined with its 30% score, it is the weakest link and does not belong on a certified path in its current state.

Net: the security specialist's *actual* Security & Compliance journey (fundamentals → secure coding → threat modeling → pen-testing) is coherent and tested-healthy. The window's fail-grade comes entirely from AI/agentic quests that are level-1011-coded but narratively and prerequisite-wise off this character's path.

## 🧠 Reasoning & Method

- **Mode / evidence:** `execute`, consumed from the workflow-sealed
`./walk-evidence.json` (`schema_version 1.0.0`, `mock: false`, `executed: true` for all 5). I did **not** run the engine (its child `claude` processes can't authenticate from the agent Bash tool) and I did not edit `walk-plan.json` or `walk-evidence.*`. All `passed`/`failed`/`skipped` labels are the engine's sandbox results; anything I judged from the source alone I marked `reasoned`.
- **What I ran vs. reasoned:** The engine executed 49 command entries across the 5 quests
(2/5 fail, 1 warn, 2 pass; avg 66%, ~$3.46). I additionally **read all five quest sources in planner order** and reasoned about the linked journey, prerequisites, series membership, and draft status — the chain-continuity section is my value-add on top of the per-quest isolation scores.
- **Coverage / limits:** This is **window 1 of 3** (offset 5) of a 12-quest level, so I
saw 5 of 12 quests; `security-fundamentals` and the rest sit in other windows and were **not** walked here. OS-gated setup blocks (brew/winget/apt/snap) and credentialed CI steps (the `claude-run` CONSUME step) were correctly `skipped`, not failed — I did not treat those as defects. Conceptual quests (Threat Modeling, The Sealed Evidence) have few runnable snippets, so their scores lean more on `reasoned`/hand-simulated evidence than executed commands; I weighted their issues accordingly.
- **Confidence:** High on the two executed failures (the naming-mismatch bug, the leaked
`{% raw %}` tags, the nonexistent package, and the stub classes are concrete, reproducible sandbox results). Medium on the conceptual-quest gaps, which rest on static reasoning. I introduced no scores of my own and invented no output.

_(Machine summary quoted verbatim from `./walk-evidence.md`: "5 quests evaluated · ✅ 2 pass · ⚠️ 1 warn · ❌ 2 fail · avg 66.0% · ~$3.4591".)_
