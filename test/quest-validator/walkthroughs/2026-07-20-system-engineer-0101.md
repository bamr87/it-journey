---
title: 'Quest Walkthrough — System Engineer · Level 0101 (CI/CD & DevOps)'
date: '2026-07-20T00:00:00.000Z'
character: system-engineer
level: '0101'
theme: CI/CD & DevOps
tier: Adventurer
quest_count: 3
mode: execute
overall_verdict: warn
session:
  window: '2 of 3 (offset 10, size 5)'
  level_total_quests: 13
  engine_average: 81.5
  engine_counts: '2 pass · 0 warn · 1 fail (engine timeout, no verdict)'
  evidence_source: sealed walk-evidence.json (workflow-minted, consumed as-is)
---

## 🎯 Session Summary

Walked a **windowed** slice of the System Engineer path at Level **0101 — CI/CD & DevOps** (Adventurer tier): the last 3 of the level's 13 quests (window 2 of 3, offset 10). The slice is **two CI/CD main quests** — *Artifact Management* and *Workflow Optimization* — plus one thematically-adjacent Hard **side quest**, *Jekyll Quest Tracking*.

Headline: **warn.** The two main quests were executed for real in the sandbox and both **passed** (83 and 80), with their core commands actually running as described. But I cannot certify the slice clean because (a) the third quest produced **zero evidence** — the execute engine hit its 40-turn cap and errored out (`claude exited 1 … Reached maximum number of turns`), so there is nothing to judge it on, and (b) a **recurring documentation defect** shows up in both main quests: Jekyll `{% raw %}…{% endraw %}` tags leak into the raw YAML of every GitHub Actions snippet, so code copied from the raw markdown source is not valid Actions syntax. A maintainer can act on the raw-tag leak and the stale Node 18 reference today; the side quest needs a re-run (or a higher turn budget) before it can be judged at all.

## 🗺️ The Journey

| # | Verdict | Quest | Type · Difficulty | Score | One-line takeaway |
|---|:---:|---|---|:---:|---|
| 1 | ✅ pass | Artifact Management: Versioned, Signed Build Output | main · 🟡 Medium | **83** | Core Docker build/tag/digest commands ran and worked; YAML snippets carry the raw-tag leak and no starter Dockerfile is provided. |
| 2 | ✅ pass | Workflow Optimization: Caching and Parallel CI/CD | main · 🟡 Medium | **80** | All 7 YAML snippets valid; `npm ci` fails in an empty dir (assumes an existing project); Node 18 is EOL; same raw-tag leak. |
| 3 | ❌ fail | Jekyll Quest Tracking: Building Dynamic Collection Layouts | side · 🔴 Hard | **—** | **No evidence** — execute engine hit the 40-turn cap and errored; verdict is a harness timeout, not a proven content defect. |

*Scores and pass/fail come verbatim from the sealed `walk-evidence.json`. I did not re-run the engine.*

## 🔬 Evidence

All command-level results below are quoted from the sealed engine evidence (execute mode, disposable sandbox). I add the linked-journey reasoning in §6; I did **not** myself execute any quest commands.

### 1. Artifact Management — ✅ 83 (`ran 3/6 runnable snippets`, 3 passed / 0 failed)

Per-dimension: commands_work **4**, content_accuracy **4**, completeness **4**, clarity **4**, structure **5**, safety **5**.

- **`docker build -t myapp:$(git rev-parse --short HEAD) .` → passed.** The engine ran `git init`, committed a README + a `FROM alpine:3.19` Dockerfile, built, and got `myapp:7f68204`; `docker images myapp` listed it — matching the quest's claimed output.
- **`docker pull myapp:latest` → passed (as illustrative failure).** Ran for real and correctly failed with *"pull access denied … repository does not exist"*, confirming the mutable-vs-immutable contrast is pseudocode, not a literal runnable step.
- **`syft … / grype …` → skipped.** Neither tool installed; sandbox denied the `curl | sh` network install. CLI syntax judged correct (`reasoned`).
- **GHCR login/tag/push, macOS `brew`, Windows `winget`, Linux `apt` → skipped/reasoned.** Require secrets / other OSes / system-package mutation — correctly not run in a Linux sandbox.
- **Both Actions YAML snippets → reasoned.** They parse structurally (`yaml.safe_load`), and `actions/checkout@v4`, `actions/upload-artifact@v4`, `actions/attest-build-provenance@v1`, and the OIDC permissions block are current and correct — **but** the raw source contains literal `name: web-dist-${% raw %}{{ github.sha }}{% endraw %}` and `subject-digest: ${% raw %}{{ steps.push.outputs.digest }}{% endraw %}` (confirmed at quest lines 235 and 336).

### 2. Workflow Optimization — ✅ 80 (`ran 1/4 runnable snippets`, 0 passed / **1 failed**)

Per-dimension: commands_work **4**, content_accuracy **4**, completeness **4**, clarity **3**, structure **5**, safety **5**.

- **`time npm ci` (Cloud/Codespace path) → FAILED.** Run in an empty directory as a fresh learner would find it: *"npm error A complete lockfile…"* because there is no `package.json`/`package-lock.json`. After the engine manually created a lockfile, `npm ci` succeeded in 0.638s. The quest never says "run this inside your existing pipeline project" before the baseline command (lines 144–187) — it leans entirely on the prerequisite checkbox *"You have a working multi-stage pipeline."*
- **Linux `sudo apt install -y nodejs npm` → skipped (sudo disallowed).** The engine checked `apt-cache policy nodejs` on the Ubuntu 24.04 sandbox: candidate `18.19.1+dfsg-6ubuntu5` — **Node 18 is past its April-2025 EOL**, so this command installs a stale runtime, inconsistent with the Node 20/22 used elsewhere in the quest.
- **All 7 YAML snippets → reasoned/valid.** Caching (`hashFiles`, `restore-keys`), the 2-OS × 3-Node matrix (= 6 jobs, matches text), `concurrency`/`cancel-in-progress`, `workflow_call` reusable workflows, and `paths-ignore` all parse and match current Actions semantics — in both the literal Jekyll-escaped form and the rendered `${{ }}` form.
- **Recurring raw-tag leak** (clarity dropped to 3): e.g. `key: npm-${% raw %}{{ runner.os }}{% endraw %}-${% raw %}{{ hashFiles('**/package-lock.json') }}{% endraw %}` (line 232), the matrix `runs-on` (line 267), concurrency `group` (line 292), and the reusable-workflow inputs (line 337).

### 3. Jekyll Quest Tracking — ❌ no evidence (engine error)

The engine returned **no verdict object**. The raw error:

> `claude exited 1: … "terminal_reason":"max_turns" … "errors":["Reached maximum number of turns (40)"]`

The engine consumed ~$1.78 and ~29k output tokens before hitting the 40-turn cap on this quest. **This is a harness/budget failure, not a demonstrated content defect.** No command was recorded as run, no dimension was scored, and the `fail`/`0.0` in the evidence reflects the abort, not the quest's quality. Reading the source (a 1,161-line Hard side quest with five chapters of Liquid layouts, includes, a JS filter, and a Python automation script — far more surface area than the two Medium main quests) makes the turn-cap exhaustion unsurprising. **This quest remains unevaluated and should be re-walked with a higher turn budget or on its own.**

## 🐞 Issues Found

- **medium · Artifact Management + Workflow Optimization · every Actions YAML snippet (artifact lines 235, 336; workflow lines 232, 267, 276, 292, 337) · observed:** literal `{% raw %}…{% endraw %}` tags appear inside `${{ }}` expressions in the raw markdown. The engine verified these parse only *after* Jekyll rendering strips them; copied verbatim from the raw file (GitHub raw view, direct copy-paste) they are **not valid GitHub Actions syntax** and would break the artifact name / digest reference / cache key. **Suggested fix (for a content pass — not this session):** confirm the site pipeline renders these to `${{ … }}`, and/or adopt a copy-paste-safe escaping form, or add an explicit note that these are template escapes. This is a *systemic* level-0101 pattern (see Chain Continuity).
- **medium · Workflow Optimization · Linux platform path, line 172 · observed:** `sudo apt install -y nodejs npm` resolves to Node `18.19.1` on Ubuntu 24.04 (checked via `apt-cache policy`), which is EOL as of the current date and inconsistent with the Node 20/22 used throughout the quest. **Suggested fix:** switch to NodeSource/nvm instructions or add a caveat.
- **medium · Workflow Optimization · Chapter 2 matrix, line 272 · observed:** the matrix advertises `node: ['18', '20', '22']` as live test targets; Node 18 reached EOL April 2025. **Suggested fix:** rotate to a current trio (e.g. `'20','22','24'`).
- **low · Workflow Optimization · platform baseline, lines 144–187 · observed:** the baseline `time npm ci` **failed** in a fresh/empty directory because there is no lockfile; the quest never states to `cd` into the existing pipeline project first, relying only on a prerequisite checkbox. **Suggested fix:** one sentence — "run these inside your existing pipeline project from the prior quests."
- **low · Artifact Management · Intermediate/Advanced challenges · observed:** no starter Dockerfile/scaffold is provided ("your app" is assumed to exist), so a first-timer without a container project can only follow along conceptually. **Suggested fix:** link a minimal scaffold repo.
- **low · Artifact Management · Retention Policies secondary objective · observed:** covered only by the inline `retention-days: 30` parameter despite being a named objective. **Suggested fix:** a short paragraph on registry/artifact expiry.
- **low (process, not content) · Jekyll Quest Tracking · execute engine · observed:** engine aborted at the 40-turn cap with no verdict. Not a content bug. **Suggested fix:** re-run this Hard, high-surface-area quest with a raised `--max-turns` or in isolation so it can actually be scored.

*No high-severity blocking issues were witnessed. No destructive or unsafe commands appear in either evaluated quest (both scored safety 5).*

## 🔗 Chain Continuity

**Does the walked window hold together for a System Engineer?** Partly — with one clear seam and one outlier.

- **Main-quest spine is coherent.** *Artifact Management* declares `unlocks_quests: /quests/0101/workflow-optimization/`, and *Workflow Optimization* is next in plan order — a learner finishing artifacts (build once, immutable tags, provenance) is naturally set up to then make those same builds fast (caching, matrix, reuse). The narrative framing ("the forge") is consistent across both.
- **Prerequisite lives *outside* this window — acceptable but worth noting.** Both main quests assume *"You have a working multi-stage pipeline"* and require `cicd-fundamentals` (+ `testing-integration`). Those quests sit earlier in Level 0101 (this is window **2 of 3**, offset 10), so within *this* walked slice that pipeline is never built — which is exactly why *Workflow Optimization*'s baseline `npm ci` failed when the engine ran it in an empty dir. For a learner sweeping the level in order this is fine; for anyone dropping into this window cold it is a silent assumption. The windowing (not the quests) creates the gap.
- **Systemic defect, not a one-off.** The `{% raw %}…{% endraw %}` leak appears in **both** main quests and in every Actions YAML block. This is a level-wide (likely repo-wide) source pattern in how CI/CD quests escape Liquid inside fenced YAML, so a fix should be applied consistently across Level 0101, not patched quest-by-quest.
- **The side quest is an outlier in this theme.** *Jekyll Quest Tracking* has empty `quest_dependencies`, a different `quest_series` ("Static Site Mastery"), `skill_focus: frontend`, and its knowledge-graph footer even labels the level *"Level 0101 - Advanced Docker & DevOps"* (line 1161) — while the two main quests label it *"Level 0101 - CI/CD & DevOps"*. For a **System Engineer** on a CI/CD track it does not chain from the artifact→workflow spine at all; it reads as a parallel frontend side adventure. Not a defect per se (side quests are meant to branch), but a learner following the System-Engineer thread would find it tonally and topically disconnected, and the inconsistent level-hub name is a small continuity wart worth flagging to a content pass.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sealed evidence). The workflow pre-computed and sealed `walk-plan.json` + `walk-evidence.json`/`.md`; I consumed them **as-is** and did **not** re-run the engine (its child `claude` processes can't authenticate from my Bash tool). I did not edit the plan or evidence.
- **What I ran vs. reasoned:** I ran **no quest commands myself** — every `passed`/`failed`/`skipped`/`reasoned` in §4 is quoted from the sandboxed engine's recorded commands. My own contribution (§6, and the issue framing) is **`reasoned`** static analysis: I read all three quest sources in plan order and cited exact line numbers for each claim.
- **Coverage honesty:**
  - Quests 1 & 2 were executed and have real command evidence — but with **limited snippet coverage** (3/6 and 1/4 runnable snippets actually ran; the rest were skipped as OS-gated, secret-gated, network-blocked, or reasoned). Both `pass` verdicts rest on partial execution plus static verification of the YAML.
  - Quest 3 has **no evidence at all** — the engine timed out at 40 turns. I did **not** substitute a judgment for it; its `fail` reflects the harness abort, and it is flagged for re-walk. Treating this slice as "2 of 3 quests actually evaluated" is the honest framing.
  - Sandbox limits observed in the evidence: no macOS/Windows hosts, `sudo` disallowed, network installs (`curl|sh`) denied, no real registry/secrets. These caused legitimate skips, not content faults.
- **Overall verdict — `warn`, not `pass`:** two clean passes, but one quest wholly unevaluated plus a recurring medium documentation defect and a stale-runtime reference mean the slice can't be certified clean. **Confidence:** high on the two executed main quests' verdicts and on the raw-tag/Node-18 findings (line-cited); **none** on Jekyll Quest Tracking, which needs a re-run before any claim can be made.

---

<details>
<summary>Appendix: machine evidence summary (verbatim from <code>walk-evidence.md</code>)</summary>

> **2** quests evaluated · ✅ 2 pass · ⚠️ 0 warn · ❌ 1 fail · avg **81.5%** · ~$1.1837
>
> - ✅ 83 — Artifact Management: Versioned, Signed Build Output — 0101 — snippets 3/6
> - ✅ 80 — Workflow Optimization: Caching and Parallel CI/CD — 0101 — snippets 1/4 (1✗)
> - ❌ — Jekyll Quest Tracking: Building Dynamic Collection Layouts — 0101 — `claude exited 1 … Reached maximum number of turns (40)`

</details>
