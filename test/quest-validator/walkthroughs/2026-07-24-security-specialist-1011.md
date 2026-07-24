---
title: 'Walkthrough — Security Specialist · Level 1011 (Security & Compliance / Warrior)'
date: '2026-07-24T00:00:00.000Z'
character: security-specialist
level: '1011'
theme: Security & Compliance
tier: Warrior
quest_count: 5
mode: execute
overall_verdict: warn
session: 'Windowed slice (window 1 of 3, 5 of 12 quests at level 1011). Sealed engine evidence consumed as-is (walk-evidence.json / walk-evidence.md); no engine re-run. Sandbox = disposable Linux runner; execute mode. Reasoned about the linked journey as a Security Specialist learner. Read-only over quest content.'
---

## 🎯 Session Summary

I played the first 5 of the 12 level-1011 quests on the **Security Specialist** path (Warrior tier, theme *Security & Compliance*), walking them in the planner's order as a learner would, and reasoning about the chain while consuming the workflow-sealed execute-engine evidence. The engine actually ran each quest's safe snippets in a disposable sandbox: **2 pass · 3 warn · 0 fail**, average **72.8%**.

Headline verdict: **⚠️ warn** — the slice is safe and pedagogically sound, and the genuinely hands-on lab material (the multi-agent tracing labs, the Juice Shop docker lab) was *verified to work end-to-end*. But four separate copy-paste-verbatim bugs were witnessed by real command execution: a MySQL 8.0 `GRANT` break, a `sha256sum --check` placeholder error, a silently-no-op trace `collect` glob, and — most serious — a GitHub Actions workflow whose expressions are corrupted by **leaked Jekyll `{% raw %}` tags** so it cannot be pasted into `.github/workflows/` as published.

The most important *chain* finding a maintainer should note: for the **Security Specialist** character specifically, only quest 1 (Security Fundamentals) is on-theme. Quests 2–5 are **GH-600 Agentic AI certification** content that happens to share the `1011` level code — a DevOps/AI track, not a security track. That is a coherence observation about the slice, not a defect in any single quest (details in §🔗 Chain Continuity).

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ⚠️ warn | Security Fundamentals: CIA Triad and Defense in Depth | 65 | Concepts accurate & Juice Shop lab works; two snippets (MySQL GRANT, sha256sum --check) break as written. |
| 2 | ⚠️ warn | Reforging the Agent's Mind: Tuning Behavior by Instruction | 68 | Safe, graceful scripts, but its core objective (editing `AGENTS.md`) is never exercised and the baseline loop has a per-task bug. |
| 3 | ✅ pass | The Council of Many: Multi-Agent Coordination | 83 | Best of the slice — the hands-on trace lab ran exactly as documented; two YAML-narrative gaps remain. |
| 4 | ✅ pass | The Council of Many: Multi-Agent Orchestration Patterns | 80 | Runnable self-check + YAMLs valid; honest about stub scripts; misses `download-artifact@v4` nesting behavior. |
| 5 | ⚠️ warn | The Scribe's Codex: Observability in Multi-Agent Systems | 68 | Python/jq artifacts all ran correctly, but Chapter 1's workflow is broken by leaked `{% raw %}` templating tags. |

## 🔬 Evidence

All results below come from commands the execute engine **actually ran** in the sandbox (per `walk-evidence.json`). Anything the engine could only judge statically is labelled `reasoned`.

### 1. Security Fundamentals — 65% ⚠️ (ran 4/6 runnable snippets · 2 passed · 2 failed · 2 skipped · 4 reasoned)
- ✅ **passed** — `docker run --rm -d -p 3000:3000 bkimminich/juice-shop`: container started, logs showed *"Server listening on port 3000"*, and an in-container HTTP GET to `localhost:3000` returned **STATUS 200**. The core hands-on lab genuinely works.
- ✅ **passed** — `sha256sum app-release.tar.gz` produces a valid hash as described.
- ❌ **failed** — `echo "EXPECTED_HASH  app-release.tar.gz" | sha256sum --check` errors with `sha256sum: 'standard input': no properly formatted checksum lines found` because `EXPECTED_HASH` is a placeholder, not a 64-hex digest. (Engine verified a real-format wrong hash correctly prints `FAILED … did NOT match`, confirming the intended behavior was never reached.)
- ❌ **failed** — `GRANT ALL PRIVILEGES ON shop.* TO 'app_user'@'%';` against a live **MySQL 8.0.46** instance fails with `ERROR 1410 (42000): You are not allowed to create a user with GRANT`. Succeeds only after a `CREATE USER …` the quest never shows.
- `reasoned` — macOS `brew install --cask docker` and Windows `winget install Docker.DockerDesktop` blocks not run (OS mismatch); Linux `sudo apt install` / `systemctl` not run (sudo blocked) — but the `docker run` line is identical to the verified Cloud path.

### 2. Reforging the Agent's Mind — 68% ⚠️ (ran 3 snippets · 3 passed · 0 failed · 2 reasoned)
- ✅ **passed** — `measure_agent_baseline.sh` ran with no `gh` auth and no repo, printing the documented degrade-gracefully warnings and exiting 1 exactly as described (good defensive scripting: `set -euo pipefail`, `|| true` guards).
- ✅ **passed** — the final Quest Validation self-check reported ❌ for the missing `baseline-results.jsonl` and ✅ once the doc files were created — behaves correctly.
- `reasoned` (logic bug) — inside `for TASK_NUM in 1 2 3`, `gh run list --workflow=agent-task.yml --limit=1` has **no per-task filter**, so with real auth it records the *identical* latest run for tasks 1/2/3. Witnessed by reading the script + confirming `gh` flags are valid for gh 2.96.0, not by a live authenticated run.

### 3. The Council of Many: Multi-Agent Coordination — 83% ✅ (ran 6/4 · 5 passed · 1 failed · 4 reasoned)
- ✅ **passed** — the Hands-On Lab's three bash steps (mint `$CID` + `trace()`, run the seeded-fault council, stitch with `jq -s 'sort_by(.seq)'`) ran flawlessly and produced output **matching the quest's "Expected" block exactly** in content and field order (only cosmetic: real `jq` output is tab-separated vs. the doc's space-aligned columns).
- ✅ **passed** — all four YAML snippets parse as valid YAML (PyYAML) and pass yamllint (line-length warnings only); the mermaid diagram renders via `mmdc` with no errors. Note this quest correctly wraps its Actions YAML in block-level `{% raw %}…{% endraw %}`, so `${{ }}` renders intact — the right pattern (contrast quest 5).
- ❌ **failed** — the Chapter 2 *collect step* `cat trace-*-"$cid"/*.jsonl | jq -s 'sort_by(.ts)…'` run verbatim **exits 0 with an empty output file**. It globs per-agent *directories*, but the naming shown two snippets earlier is a flat `trace-$CORRELATION_ID.jsonl` per job — a silent no-op with no error to debug.

### 4. Multi-Agent Orchestration Patterns — 80% ✅ (ran 4/1 · 4 passed · 0 failed · 1 reasoned)
- ✅ **passed** — the Quest Validation self-check ran verbatim after creating the three deliverables and printed exactly the promised three ✅ lines (fan-out workflow, chain workflow, valid sub-agent-contract.json).
- ✅ **passed** — both workflow YAMLs load with `yaml.safe_load`; the chain's research-agent `run:` block executed directly and produced the documented `findings={"files_to_modify": ["src/api.js"], "patterns": ["REST"]}`; the JSON schema is valid draft-07 (`python3 -m json.tool`).
- `reasoned` (latent bug) — `actions/download-artifact@v4` with a `pattern` and no `merge-multiple: true` nests each artifact in its own subdir, not flat into `./subtask-results/`; the aggregate step assumes flat. Full CI execution can't be run in-sandbox — honestly scoped by the quest, which limits its self-check to file-presence.

### 5. The Scribe's Codex: Observability — 68% ⚠️ (ran 6/4 · 5 passed · 1 failed · 1 skipped · 1 reasoned)
- ✅ **passed** — `trace_writer.py` printed its two `[TRACE]` lines and wrote a valid `trace-task-42-1001.jsonl`; `aggregate_traces.py` against 3 synthetic trace files produced a correct time-sorted `audit-log.json` (*"Found 3 trace files" / "Unified audit log written: 5 events across 3 agents" / "1 failure events detected"*); all three Chapter 4 `jq` queries produced exactly the described output.
- ❌ **failed** — the Chapter 1 workflow is broken as published: **5 occurrences** of leaked Liquid tags corrupt every Actions expression, e.g. `outputs: ${% raw %}{{ steps.init_trace.outputs.correlation_id }}{% endraw %}` instead of `${{ steps.init_trace.outputs.correlation_id }}` (confirmed by reading source lines 110, 116, 124, 137–138). Pasted verbatim into `.github/workflows/`, `correlation_id` / `env.CORRELATION_ID` / artifact names are all literal broken strings.
- ⚪ **skipped** — `python3 scripts/validate_quest.py --quest q15` references a platform script that exists nowhere in the quest or sandbox; could not be executed.

## 🐞 Issues Found

Every item below is backed by a command the engine ran (§Evidence) or an exact quoted line I read from the quest source. Grouped by severity.

**HIGH**
1. **high · Scribe's Codex (Observability) · Chapter 1 YAML workflow (source lines ~110, 116, 124, 137–138)** — *Observed:* 5 leaked `${% raw %}{{ … }}{% endraw %}` fragments; the central "correlation ID" workflow is non-functional if copied verbatim. *Fix:* wrap the entire fenced block in a single block-level `{% raw %}`/`{% endraw %}` pair (as sibling quest *Multi-Agent Coordination* correctly does) so it renders as plain `${{ … }}`.
2. **high · Security Fundamentals · Chapter 3 SQL least-privilege example** — *Observed:* `GRANT ALL PRIVILEGES … TO 'app_user'@'%'` fails on MySQL 8.0.46 with `ERROR 1410`. *Fix:* prepend `CREATE USER 'app_user'@'%' IDENTIFIED BY '…';` (and the `10.0.%` host), or note that GRANT no longer auto-creates users on MySQL 8.0+.
3. **high · Reforging the Agent's Mind · Objective 3 / Chapter 3** — *Observed:* the quest's core objective, "modify `copilot-instructions.md` and `AGENTS.md`", is never exercised or validated by any runnable step. *Fix:* add a runnable edit step (e.g. a `cat >> AGENTS.md <<'EOF' … EOF`) plus a Quest-Validation check that those files changed.

**MEDIUM**
4. **medium · Security Fundamentals · Chapter 1 `sha256sum --check`** — *Observed:* placeholder `EXPECTED_HASH` yields `no properly formatted checksum lines found`. *Fix:* use a real matching/non-matching digest, or instruct the learner to substitute the published hash first.
5. **medium · Multi-Agent Coordination · Chapter 2 collect-step snippet** — *Observed:* `cat trace-*-"$cid"/*.jsonl | jq …` silently produces an empty file (exit 0). *Fix:* show the preceding `actions/download-artifact@v4` step that creates the per-artifact subdirs, or rewrite the glob to match the flat `trace-$CORRELATION_ID.jsonl` naming used one snippet earlier.
6. **medium · Multi-Agent Orchestration Patterns · Chapter 2 aggregate job** — *Observed (reasoned):* `download-artifact@v4` with `pattern:` and no `merge-multiple: true` nests artifacts in subdirs; aggregate assumes flat. *Fix:* add `merge-multiple: true` or tell learners to walk subdirectories.
7. **medium · Reforging the Agent's Mind · Exercise 13.1 loop** — *Observed (reasoned):* `gh run list --limit=1` inside `for TASK_NUM in 1 2 3` records the same run three times. *Fix:* filter per task (branch pattern `copilot/issue-{N}-*` or a distinct workflow input).
8. **medium · Security Fundamentals · Risk Management objective** — *Observed:* listed as a secondary objective and a mastery indicator ("justify a fix-it-first decision using a simple risk rating") but likelihood×impact is never taught in the body. *Fix:* add a short 3×3/5×5 risk-matrix section.
9. **medium · Security Fundamentals · Safety-warning placement** — *Observed:* the "never expose intentionally vulnerable apps publicly" warning appears **only** under the Cloud Realms path; the identical `docker run … juice-shop` in the macOS/Windows/Linux paths carries no such caveat, and the Linux path uses `sudo docker run …` with no note on the added root risk. *Fix:* repeat or link the warning in each OS section.

**LOW**
10. **low · Scribe's Codex · Quest Validation** — `scripts/validate_quest.py --quest q15` is uninspectable platform infra; consider stating what it checks so learners can self-verify.
11. **low · Multi-Agent Orchestration / Coordination · YAML `on:` gotcha** — a generic YAML 1.1 linter coerces `on:` to boolean `True`; a one-line footnote would save newcomers a debugging detour.
12. **low · Security Fundamentals · OWASP currency** — "The current edition is the OWASP Top 10:2021" may go stale; phrase as "as of 2021, the most recent full edition at publication" or link owasp.org.

## 🔗 Chain Continuity

I read all five quests in plan order carrying prior state forward, as a Security Specialist learner would. Findings:

- **The slice is two disjoint tracks under one level code.** Quest 1 (*Security Fundamentals*) belongs to the **Security Mastery / The Warrior's Bastion** arc — the genuinely security-specialist content, with `required_quests: []` (a clean entry point). Quests 2–5 belong to the **Agentic Codex / GH-600 Agentic AI Certification** arc (`quest_series: agentic-ai-mastery`, `quest_line: gh-600`, `skill_focus: devops/ai-ml`). For a *Security Specialist* character, quests 2–5 are **off-theme**: they teach GitHub Actions multi-agent orchestration, not security. This is a coherence observation about how the planner windowed level 1011, not a bug in any quest — a maintainer may want the character→level mapping (or the windowing) to keep a security learner on security content.

- **The agentic sub-chain is internally well-ordered but reaches outside the window for its prerequisite.** Dependency edges: *Behavior Tuning (Q13)* → *Orchestration Patterns (Q14)* → *Observability (Q15)*, with *Multi-Agent Coordination* acting as the Domain-5 **overview/hub** that lists Q14/Q15 (and two unwalked quests) as its drill-down sub-skills. Placing the hub (quest 3) before its drill-downs (quests 4–5) is pedagogically reasonable. **But** *Behavior Tuning* declares `required_quests: [/quests/1010/agentic-failure-root-cause-analysis/]` — a **level-1010** quest not in this window — and its Chapter 1 tells the learner to "select the top 2 failure patterns **from RCA reports**." A learner who enters at 1011 without the 1010 RCA quest has no RCA reports to draw from. Expected for a windowed slice, but a real cross-level prerequisite gap worth noting.

- **Readiness hand-offs largely hold within the agentic track.** Coordination → Orchestration → Observability build cleanly: the correlation-ID concept introduced narratively in *Coordination* is implemented for real in *Observability* (`trace_writer.py` + `aggregate_traces.py`, both verified to run). The one seam that leaks: *Orchestration* and *Observability* both assume an implicit `actions/download-artifact` step to move per-agent trace artifacts into the local `traces_dir`/`subtask-results/` the next stage reads — never shown, so the "upload artifact → read from dir" hand-off is a gap a learner must invent (issues 5 & 6).

- **Real-world setup ceiling.** Quests 2–5 all assume a live GitHub repo with Actions + Copilot coding-agent access. The engine verified every *local* snippet (Python, `jq`, bash self-checks) but the Actions workflows themselves are `reasoned`, not executed — correct sandbox discipline, and the quests are honest that full CI execution is out of local scope.

## 🧠 Reasoning & Method

- **Mode:** `execute` (real commands in a disposable Linux runner sandbox), as sealed by the `quest-perfection`/`quest-walkthrough` workflow. I did **not** run the agentic engine — its child `claude` processes can't authenticate from my Bash tool — I consumed `walk-evidence.json` / `walk-evidence.md` **as-is** and did not edit, regenerate, or hand-write any evidence.
- **What I ran vs. reasoned:** all `passed`/`failed` verdicts above are commands the engine executed (Juice Shop docker, MySQL 8.0 GRANT, `sha256sum --check`, the trace labs, the self-checks). Items labelled `reasoned` (the `gh run list` per-task bug, the `download-artifact@v4` nesting, cross-quest prerequisite gaps) were judged statically — from reading the quest source or valid-flag verification — and are labelled as such, never asserted as tested. I independently re-read all five quest sources to confirm the templating-leak lines and the chain edges I report.
- **Coverage / limits:** this is a **windowed** walk — 5 of 12 level-1011 quests (window 1 of 3); the remaining 7 (including *Failure Recovery* and *Lifecycle Management*, referenced as unlocks) were **not** walked this run and accumulate in the perfection ledger over subsequent runs. OS-specific installs (brew/winget/apt+sudo) and live GitHub Actions runs could not be executed in the sandbox and are reasoned only. No destructive commands were run; no network beyond the safe pulls a quest explicitly needs.
- **Confidence:** high on the four witnessed copy-paste bugs (direct command output) and on the chain-coherence findings (direct source reads); medium on the reasoned logic/nesting bugs (plausible and flag-verified, but not exercised against live GitHub auth).
- **Engine cost/coverage for the record:** 5 quests scored, 0 errored, avg 72.8%, ~$3.43 (from `walk-evidence.json`).

---

*One slice, one report. No quest content was modified; fixable bugs live in §Issues for a content pass. Git is handled by the caller.*
