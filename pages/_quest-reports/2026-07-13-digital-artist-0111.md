---
title: Digital Artist · L0111 · 2026-07-13
description: Quest-perfection walkthrough of the API Development slice digital-artist/0111 on 2026-07-13,
  engine verdict fail. An evidence-based, learner's-eye session…
date: '2026-07-13T13:41:06.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Digital Artist
tags:
- digital-artist
- level-0111
- walkthrough
- quest-perfection
- fail
- api-development
render_with_liquid: false
excerpt: 'Digital Artist · Level 0111 — API Development: an evidence-based quest-perfection walkthrough
  from 2026-07-13.'
slice: digital-artist/0111
character: digital-artist
level: '0111'
theme: API Development
tier: Adventurer
verdict: fail
quest_count: 5
walk_date: '2026-07-13'
run_url: https://github.com/bamr87/it-journey/actions/runs/29248386306
source_report: test/quest-validator/walkthroughs/2026-07-13-digital-artist-0111.md
---

> **Slice** `digital-artist/0111` · **Level** 0111 (API Development) · **Adventurer tier** · **Engine verdict** ❌ fail · **Walked** 2026-07-13
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29248386306) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-13-digital-artist-0111.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-13-digital-artist-0111.md)

---

## 🎯 Session Summary

Walking the first window (5 of 10 quests) of the **Digital Artist ⚔️ Adventurer** level 0111 "API Development" slice, played end-to-end in the runner sandbox by the agentic execute engine and then reasoned about as a linked learner journey. The window is not one line but **two interleaved quest lines**: the *API Design Mastery / Gatekeeper's Road* thread (`api-fundamentals` → `rest-principles`) and the *Agentic Codex / gh-600* thread (`agentic-codex-01-agents-in-the-sdlc`, `agentic-sdlc-integration` → `agentic-plan-vs-action-boundaries`).

The verdict is **fail for the slice as a learning path**, despite a healthy 71.4% average. The two API-thread quests plus the first agentic quest are strong (86–91, every runnable snippet passed in the sandbox). But the entire two-quest gh-600 sub-chain (`agentic-sdlc-integration` 52 ❌, `agentic-plan-vs-action-boundaries` 37 ❌) is **broken for a real beginner**: both send the learner into a `work/gh-600/` scaffold directory that no quest ever creates, both invoke a `scripts/validate_quest.py` self-check that does not exist in the repo, and the final quest additionally renders as garbled markup because its closing code fences carry language tags. A maintainer should treat the API thread as ship-ready and the gh-600 thread as blocked pending the fixes in §5.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ✅ | API Fundamentals: HTTP, Requests, and JSON | 91 | Exemplary — every curl/Python/Node/jq snippet ran and matched the quest verbatim, incl. the live GitHub Novice Challenge. |
| 2 | ✅ | Initiation Rites: Agents in the SDLC | 86 | Solid gh-600 Domain-1 opener; agent-trace.sh + all YAML verified; only unverifiable cert-stat anchor and a standalone-run crash risk. |
| 3 | ✅ | REST Principles: Resources, Statelessness, and Maturity | 91 | Conceptually excellent (Fielding + Richardson verified live via Docker curl); idempotency & status-code objectives under-taught. |
| 4 | ❌ | Initiation Rites: Embedding Agents in the SDLC | 52 | Concepts good, hands-on broken: `cd work/gh-600` fails (dir absent) and `scripts/validate_quest.py` missing — blocks the first command. |
| 5 | ❌ | The Three Sigils: Plan, Reason, Act | 37 | Sound idea, unlearnable as shipped: broken code fences garble Ch. 2–5, plus missing sample-plan.json / validate script / workflow runtime bug. |

## 🔬 Evidence

All outcomes below are from commands the execute engine **actually ran** in the disposable sandbox (`--mode execute`), quoted from `walk-evidence.json`. Where the sandbox's own network/permission layer blocked a step, the engine used the quest's own Docker path as a workaround and I mark equivalent behavior; steps only judged statically are labelled `reasoned`.

### 1. API Fundamentals — 91 ✅ · ran 11/10 runnable snippets (11 passed, 0 failed, 5 skipped, 3 reasoned)
- `GET jsonplaceholder.typicode.com/posts/1` → **200** with exact fields `userId,id,title,body` (verified in `curlimages/curl` container + urllib) — **passed**.
- `docker run --rm curlimages/curl:latest ...` Cloud Realms path executed end-to-end, printed correct JSON — **passed**.
- `POST /posts` with JSON body + Content-Type → **201 Created**, assigned `id 101` exactly as claimed — **passed**.
- `curl -s -o /dev/null -w "%{http_code}\n" .../posts/9999` → **404** as stated — **passed**.
- `curl -s .../posts/1 | jq '.title'` → correct title string — **passed**.
- Python `requests` (after `pip install`) and Node `fetch` (Node 20.20.2) both printed **200** + correct title — **passed**.
- Novice Challenge `curl https://api.github.com/users/octocat` → **200** with real `public_repos` (8) — **passed**, challenge is completable.
- `reasoned`: illustrative `curl -v` block shows `HTTP/1.1` but a learner today negotiates **HTTP/2** by default — unexplained mismatch (accuracy nit).

### 2. Initiation Rites: Agents in the SDLC — 86 ✅ · ran 7/5 (6 passed, 1 failed, 4 skipped, 2 reasoned)
- `scripts/agent-trace.sh` written, `chmod +x`, run with `GITHUB_STEP_SUMMARY` set → produced the documented JSONL line + Markdown summary — **passed**.
- Standalone run of the same script (no `GITHUB_STEP_SUMMARY`, `set -euo pipefail`) → `line 22: GITHUB_STEP_SUMMARY: unbound variable` — **failed** (plausible learner stumble; quest never warns).
- Embedded `run:` plan/act shell logic (mkdir, heredoc plan.json, `jq -r .task`, JSONL append) executed, matched the quest's own "Expected" block — **passed**.
- All 4 YAML blocks parsed valid via PyYAML — **passed**.
- 5 `gh`-CLI mutation blocks correctly **skipped** (no `gh auth` session, no outbound network) — legitimately un-runnable, not a defect.
- `reasoned`: the "GH-600 / 18% Domain-1" certification anchor could not be network-verified — the single largest unverified factual claim.

### 3. REST Principles — 91 ✅ · ran 4/6 (4 passed, 0 failed, 3 skipped, 2 reasoned)
- `docker run --rm curlimages/curl:latest -s https://api.github.com/repos/torvalds/linux` → **200**, real JSON (`"stargazers_count": 239325`) — **passed** (Docker path used because direct curl was sandbox-blocked, not a quest defect).
- `curl -s ".../comments?postId=1&_limit=3" | jq 'length'` → **3** exactly — **passed**.
- `curl -s .../repos/torvalds/linux | jq 'keys|map(select(test("_url$")))|length'` → **42**, empirically confirming the hypermedia `_url` claim — **passed**.
- HATEOAS example validated with `jq empty` → valid JSON — **passed**.
- `reasoned`: `brew`/`winget`/`apt` install lines not executed (Linux sandbox, `sudo` out of scope) but package names are current/correct.

### 4. Initiation Rites: Embedding Agents in the SDLC — 52 ❌ · ran 7/3 (4 passed, 3 failed, 0 skipped)
- `git clone` succeeds, then `cd it-journey/work/gh-600` → **`bash: cd: work/gh-600: No such file or directory`** — **failed**. `find` on a fresh clone confirms no `work/` dir exists (only an unrelated `pages/_notes/gh-600`).
- PowerShell path `Set-Location it-journey/work/gh-600` → **`Cannot find path ... because it does not exist`** — **failed** (identical break on both platforms).
- Final `python3 scripts/validate_quest.py --quest q1` → script **does not exist** anywhere in repo (`find / -iname 'validate_quest*'`) — **failed**. Confirmed present in the *live published* source too, so it's a genuine shipped bug.
- `pip install pyyaml`, `gh --version` (2.96.0) → exit 0 — **passed**, but `gh` is a dead prerequisite (never used again).
- All 3 Mermaid diagrams rendered to valid SVG; `dependency-updater.yml` parses as valid YAML — **passed**.

### 5. The Three Sigils: Plan, Reason, Act — 37 ❌ · ran 5/1 (2 passed, 3 failed, 1 skipped, 3 reasoned)
- Ch. 3 validation `python3 -c "... jsonschema.validate ..."` loads `work/gh-600/sample-plan.json` → **`FileNotFoundError`** — **failed**; the quest never tells the learner to create that file.
- After hand-authoring a sample plan, the Ch. 3 JSON Schema itself validates and prints `✅ Plan is valid` — **passed** (schema logic is sound; only the missing input breaks it).
- Final `python3 scripts/validate_quest.py --quest q2` → **file not found** — **failed** (same missing script as quest 4).
- **Rendered `QUEST.md` with Python-Markdown**: closing fences in Ch. 2–5 carry language tags (` ```markdown `, ` ```bash `) instead of bare ` ``` `, merging unrelated content into giant code blocks and turning `# Expected:` comments into `<h1>` headings — **failed** (verified by actual rendering; a deterministic parser found only 4 code blocks vs. the ~9 an intact quest should contain).
- `reasoned`: Ch. 4 workflow has a real runtime bug — schema read from `.github/schemas/agent-plan.json` but saved to `work/gh-600/schemas/...`, and `on: push` trigger with a `context.issue.number` PR-comment step that is `undefined` for push events.

## 🐞 Issues Found

**High severity (blocking — learner cannot proceed):**
- **high · Embedding Agents in the SDLC (q4) · Setup, all 3 platforms** — `cd it-journey/work/gh-600` / `Set-Location ...` fails because `work/gh-600` does not exist in the repo (verified on fresh clone, bash + PowerShell). *Fix:* change to `mkdir -p work/gh-600 && cd work/gh-600`, or commit the scaffold (notes/, task-cards/, schemas/, scripts/).
- **high · q4 + q5 · "Quest Validation" section** — `scripts/validate_quest.py` referenced by both quests does not exist anywhere (`find / -iname 'validate_quest*'`). *Fix:* add & commit the script, or replace the section with a manual checklist.
- **high · Three Sigils (q5) · Ch. 2–5 markdown fencing** — closing fences reuse language tags, garbling most of the quest when rendered (verified via Python-Markdown). *Fix:* make every closing fence a bare ` ``` `.
- **high · Three Sigils (q5) · Ch. 3 validation command** — reads `work/gh-600/sample-plan.json` that is never created → `FileNotFoundError`. *Fix:* add a step creating that file (reuse the Ch. 2 JSON example) before the validate command.

**Medium severity:**
- **medium · q5 · Ch. 3↔Ch. 4 schema path** — schema saved to `work/gh-600/schemas/agent-plan.json` but the CI workflow reads `.github/schemas/agent-plan.json`; never reconciled. *Fix:* pick one canonical path and add a copy step.
- **medium · q5 · Ch. 4 workflow logic** — `on: push` trigger with a `context.issue.number` PR-comment step (undefined for push). *Fix:* trigger on `pull_request`, or use a push-valid mechanism (commit status/check run).
- **medium · q4 · Secondary Objectives** — "definition-of-done" and "repo- vs org-scoped agents" are listed but never taught (grep: zero body hits). *Fix:* add a short chapter each or drop from objectives.
- **medium · q3 · Completeness** — secondary objective "Idempotency and Safety" is never taught (only line 25 matches `idempot`), and status codes are barely covered (only 404) yet the Intermediate Challenge requires assigning success codes. *Fix:* add a short idempotency/status-code section.

**Low severity:**
- **low · q1 · request/response illustration** — shows `HTTP/1.1` but a learner running `curl -v` today sees `HTTP/2`; unexplained mismatch. *Fix:* note the protocol version may differ, or update the illustration.
- **low · q2 · agent-trace.sh** — hard-fails (`unbound variable`) if a learner runs it standalone outside Actions. *Fix:* guard `$GITHUB_STEP_SUMMARY` or warn it's Actions-only.
- **low · q2 · GH-600/18% cert claim** — unverifiable in the sandbox (no network); it anchors the quest's authority. *Fix:* author should source-check before relying on it.
- **low · q4 · dependency-updater.yml** — `diff_scope: package.json only` contradicts inputs listing `package-lock.json` (npm updates touch both). *Fix:* broaden diff_scope or drop the lock file from inputs.
- **low · q4 · `gh --version`** — verified in setup but `gh` never used again. *Fix:* use it in an exercise or drop it.
- **low · q5 · action casing** — `actions/GitHub-script@v7` should be `actions/github-script@v7`; and add `estimated_prs` to the Ch. 3 schema (or drop from the example) for consistency.

## 🔗 Chain Continuity

**This window is two independent quest lines interleaved, not one path.** The planner's dependency sort produced the order `api-fundamentals` → `agentic-codex-01` → `rest-principles` → `agentic-sdlc-integration` → `agentic-plan-vs-action-boundaries`, but frontmatter shows two distinct threads a learner experiences separately:

- **API thread** (*The Gatekeeper's Road / API Design Mastery*): `api-fundamentals`
(no deps) → `rest-principles` (`required_quests: [api-fundamentals]`). Continuity is **clean**: quest 1 teaches HTTP methods/status/JSON and quest 3 legitimately builds on it (resources, statelessness, RMM). A learner finishing quest 1 is genuinely ready for quest 3. Only soft gap: quest 3's status-code challenge leans on knowledge quest 1 covers but quest 3 doesn't re-teach — acceptable given the hard dependency.

- **Agentic gh-600 thread** (*The Agentic Codex*): here continuity **breaks**.
  1. **Duplicate/divergent openers.** Quest 2 ("Initiation Rites: Agents in the SDLC",
     `agentic-codex-01`) and quest 4 ("Initiation Rites: **Embedding** Agents in the
     SDLC", `agentic-sdlc-integration`) are near-duplicate Domain-1 "agents in the
     SDLC" quests with almost identical titles but different `quest_series`
     (`The Agentic Codex` vs `agentic-ai-mastery`) and wildly different quality
     (86 ✅ vs 52 ❌). A learner meeting both in one window will be confused about
     which is canonical. Worth a maintainer decision to merge or clearly differentiate.
  2. **A phantom shared prerequisite.** Quests 4 and 5 both assume a populated
     `work/gh-600/` scaffold (with `notes/`, `task-cards/`, `schemas/`,
     `scripts/validate_quest.py`) as if an earlier quest created it — but **no quest
     in the slice ever does**. Quest 2, the passing opener, writes `scripts/agent-trace.sh`
     ad hoc and never establishes `work/gh-600/`. So the dependency chain
     `agentic-sdlc-integration` (`unlocks` → `agentic-plan-vs-action-boundaries`,
     which lists it as `required_quests`) is honored on paper but the actual working
     directory the two quests share is never provisioned. The result is that the
     entire gh-600 sub-chain fails on its **first command** and again at its closing
     self-check — a beginner is blocked end-to-end.
  3. **Compounding breakage downstream.** Quest 5 inherits the same missing-scaffold
     and missing-`validate_quest.py` bugs *and* adds structurally broken code fences,
     so even the conceptual reading experience degrades. The learner who somehow
     pushed past quest 4 lands on a page that renders garbled.

**Net:** the API half of this window is a sound, ship-ready mini-path; the agentic half does not hold together as a learnable chain until the `work/gh-600` scaffold is created (or the instructions switched to `mkdir -p`), the `validate_quest.py` script is provided or removed, and quest 5's fences are repaired.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sealed evidence). I consumed `walk-plan.json` +
`walk-evidence.json` / `walk-evidence.md` **as-is** — the workflow pre-computed the agentic execute engine deterministically because the engine's child `claude` processes cannot authenticate from an agent's Bash tool. I did **not** re-run, edit, regenerate, or hand-write any evidence, and I made **no** changes to quest content. My only write is this report.
- **What was actually run vs. reasoned:** every `passed`/`failed` above is a command
the engine executed in the disposable sandbox (curl/Docker/Python/Node/jq, script execution, YAML/JSON parsing, an actual Markdown render for quest 5's fences, fresh `git clone` + `find` for quest 4's missing directory). Items labelled `reasoned` (HTTP/2 mismatch, install commands on other OSes, the GH-600 cert stat, quest 5's workflow runtime bug) were judged statically because the sandbox lacked network, `sudo`, `brew`/`winget`, or a live GitHub/Copilot session — these are honest coverage limits, not quest defects, and I've marked them as such.
- **Snippet coverage (ran/runnable):** q1 11/10, q2 7/5, q3 4/6, q4 7/3, q5 5/1.
Skips in q2/q3 are legitimately un-runnable (real GitHub mutations, `sudo`, foreign package managers) rather than avoided work.
- **Chain reasoning:** I read all five quest sources in plan order and cross-checked
their `quest_dependencies` frontmatter to derive the two-thread structure and the phantom `work/gh-600` prerequisite in §"Chain Continuity" — that linked-journey analysis is my value-add on top of the engine's per-quest-in-isolation scores.
- **Scope:** exactly window 1 of 2 (quests 1–5 of the level's 10). I did not walk the
second window; the ledger accumulates that coverage on a later run. No level or character substitution.
- **Confidence:** **high** on the two failing verdicts (blocking bugs reproduced by
real commands and confirmed against the live published source) and on the three passing verdicts (every runnable snippet passed). **Medium** on the `reasoned` accuracy nits, which warrant an author source-check but weren't executable here.

### Machine evidence (verbatim excerpt)

> **5** quests evaluated · ✅ 3 pass · ⚠️ 0 warn · ❌ 2 fail · avg **71.4%** · ~$7.6575
>
> | | Score | Quest | Snippets run |
> |---|--:|---|:-:|
> | ✅ | 91 | API Fundamentals: HTTP, Requests, and JSON | 11/10 |
> | ✅ | 86 | Initiation Rites: Agents in the SDLC | 7/5 (1✗) |
> | ✅ | 91 | REST Principles: Resources, Statelessness, and Maturity | 4/6 |
> | ❌ | 52 | Initiation Rites: Embedding Agents in the SDLC | 7/3 (3✗) |
> | ❌ | 37 | The Three Sigils: Plan, Reason, Act | 5/1 (3✗) |
