---
title: 'Quest Walkthrough — System Engineer · Level 0101 (CI/CD & DevOps)'
date: '2026-07-27T00:00:00.000Z'
character: system-engineer
level: '0101'
theme: CI/CD & DevOps
tier: Adventurer
quest_count: 5
mode: execute
overall_verdict: warn
session:
  window: 1 of 3 (5 of 13 quests in the level)
  evidence_source: sealed walk-evidence.json (agentic execute engine, deterministic workflow step)
  scored: 4
  errored: 1
  average_score: 78.0
  counts:
    pass: 2
    warn: 2
    fail: 1
  engine_cost_usd: 2.8007
  notes: >-
    Machine evidence sealed by the workflow; the walker consumed it as-is and did not
    re-run the engine. One quest (LaTeX CV) hit the engine's max-turns limit and was
    not scored — it is reasoned about statically only, not tested.
---

## 🎯 Session Summary

I walked the first window (5 of 13 quests) of the **System Engineer** path at **Level 0101 — CI/CD & DevOps (Adventurer tier)**, playing each quest as a learner would while consuming the sealed execute-engine evidence. **Headline verdict: warn.** The two "spine" quests of the CI/CD line — *CI/CD Fundamentals* (83) and *The Warden's Gate* (89) — are accurate, safe, and hold together well; but *Docker Mastery* (63) and *GitHub Actions Basics* (77) each ship a defect a copy-pasting beginner will hit, and *LaTeX CV* could not be scored because the engine ran out of turns (heavy TeX toolchain + a network-restricted sandbox), so it stands only on my static reading.

The single most actionable pattern across the slice: **Jekyll `{% raw %}` handling is inconsistent between quests.** *CI/CD Fundamentals* and *The Warden's Gate* correctly wrap the **whole** fenced code block, so copied YAML is clean; *GitHub Actions Basics* wraps individual `${{ }}` expressions **inside** the fence, which leaks literal `{% raw %}`/`{% endraw %}` into the copy-pasteable code and silently breaks the secret and matrix expressions. Fixing that one quest to match the other two would remove the biggest learner trap in the slice.

## 🗺️ The Journey

| Verdict | Quest | Score | One-line takeaway |
|:--:|---|:--:|---|
| ✅ | CI/CD Fundamentals: The Build-Test-Deploy Pipeline | 83 | Conceptually solid and runnable, but Chapter 3's `git commit -am` silently commits nothing for a *new* file (no `git add`). |
| ⚠️ | Docker Containerization Mastery | 63 | Chapter 1 works great; Chapter 2's "web app" exits immediately, the multi-stage build has no app to build, Trivy is never installed, and "deploy to cloud" is asserted not walked. |
| ⚠️ | GitHub Actions Basics | 77 | Technically accurate and well-structured, but leaked `{% raw %}` tags break the secrets and matrix `${{ }}` expressions when copied from the raw file. |
| ❌ | Forging the La(zy)TeX CV | — | **Not scored** — engine hit max-turns (40) probing for a package manager / network. Reasoned statically only; content looks coherent and self-contained. |
| ✅ | The Warden's Gate: Kill Switches and Stage Gates | 89 | Best-in-slice: accurate reusable-workflow permission model, gate shell logic executed and behaved exactly as described. |

Average of the four scored quests: **78.0** (2 pass · 2 warn · 1 engine-fail).

## 🔬 Evidence

All `passed`/`failed` below come from commands the execute engine actually ran in the disposable sandbox (per `walk-evidence.json`). Items I only judged by reading are marked `reasoned`.

### ✅ CI/CD Fundamentals — 83 · ran 6/5 runnable snippets (5✓ 1✗)
- `git --version && node --version` → **passed** (`git 2.54.0`, `node v20.20.2`).
- `mkdir cicd-quest && git init && npm init -y` → **passed** (valid `package.json`).
- `package.json` scripts + `npm run build && npm test && npm run lint` → **passed**, all exit 0. But `npm test` (`node --test`) reports **"0 tests, 0 pass"** and still exits 0 — the Chapter 2 checkpoint "npm test passes" is a **vacuous** pass; no test file is ever created.
- Chapter 3 git snippet (`git checkout -b … ; git commit -am "feat: add greeting"`) → **failed**. Reproduced: creating a *new* file then `git commit -am` yields *"nothing added to commit but untracked files present"* because `-a` only stages **already-tracked** files and the snippet has no `git add`.
- Both GitHub Actions YAML blocks → **reasoned** (parse as valid Actions schema; not run — no runner in sandbox). `node-version: '20'` is now past LTS maintenance (Apr 2026).
- macOS/Windows/Linux install paths → **skipped** (no brew/winget; `sudo` blocked) — judged correct by inspection.

### ⚠️ Docker Mastery — 63 · ran 6/8 runnable snippets (3✓ 3✗)
- `docker --version && docker run --rm hello-world` → **passed** (Docker 28.0.4, standard welcome output).
- Chapter 1 `Dockerfile` build + run → **passed**, output *"Hello from your first Docker container!"* — an **exact** match to the quest's stated expected output.
- `docker compose up -d / ps / down` → **failed**. Commands ran without CLI error, but the `web` service (built from Chapter 1's echo-and-exit image) immediately `Exited (0)`; `docker compose ps` shows only redis running, contradicting the "small web app … port 8080" framing.
- Multi-stage security `Dockerfile` → **failed** at `RUN npm ci` — no `package.json`/app source exists and the quest never has the learner scaffold one.
- `trivy image my-first-image` → **skipped** — `trivy` not installed and **no install step anywhere** in the quest (confirmed `which trivy` → not found).
- `docker tag … YOUR_USERNAME/…` → **failed** verbatim (Docker requires lowercase repo names); works once a lowercase placeholder is substituted. `docker login`/`push` correctly not exercised (real creds / remote mutation).

### ⚠️ GitHub Actions Basics — 77 · ran 10/4 runnable snippets (8✓ 2✗)
- `mkdir -p .github/workflows` (macOS/Linux/Cloud) and `New-Item -ItemType Directory` (Windows, via pwsh) → **passed**.
- `gh run list` unauthenticated → **passed** as a *demonstration*: produced *"gh: To use GitHub CLI in a GitHub Actions workflow, set the GH_TOKEN environment variable."* — matching the quest's callout, which correctly frames it as an auth issue, not a broken command.
- "Hello Actions", `on:` triggers, and `needs:` YAML blocks → **passed** (parse cleanly; matrix math independently verified 2×3−1 = **5** jobs).
- Secrets block (line 293) and matrix block (lines 335/348) → **failed**. The literal source embeds `${% raw %}{{ secrets.DEPLOY_TOKEN }}{% endraw %}`; copy-pasted from the raw file it parses as YAML but yields the **string** `${% raw %}{{ … }}{% endraw %}` instead of a real `${{ }}` expression — GitHub Actions never substitutes the secret/matrix value.

### ❌ Forging the La(zy)TeX CV — not scored (engine error)
- The engine terminated at **max-turns (40)** while probing for a package manager and network reachability (`which conda mamba cargo pip npm node`, `curl -sI https://pypi.org`, `wget … https://www.google.com`). No dimension scores were produced. This quest installs a full TeX distribution (`texlive-full` / MacTeX / MiKTeX) and compiles `cv.tex` — heavy and network-dependent, which the disposable sandbox is not provisioned for.
- **Reasoned only:** on reading, the quest is coherent and, importantly, **self-contained** — Chapter 2 supplies a complete starter `cv.tex` and Chapter 1 explicitly forward-references it ("Don't have `cv.tex` yet? Create it first from … Chapter 2, then return here"). The BasicTeX note calls out `enumitem`/`titlesec` as extra installs to avoid a `File \`enumitem.sty' not found` failure. I did **not** execute any of it, so no pass/fail is claimed.

### ✅ The Warden's Gate — 89 · ran 4/1 runnable snippets (4✓ 0✗)
- Chapter 1 gate-job YAML → **passed** (yamllint + PyYAML, no errors).
- Extracted gate-check shell logic run against `ENABLED=true / '' / false` → **passed**: `go=true` only when `true`; "loop idle" printed otherwise — exactly the documented go/no-go behavior.
- Chapter 2 "trap" + "two-line cure" YAML → **passed** (parse individually and merged; matches the reusable-workflow permission-capping shape).
- Arm/disarm bash (`gh variable set … && gh workflow run … && gh run watch`) → **skipped** end-to-end (no `gh auth`, no repo, would mutate remote), but **reasoned** correct via `gh --help` syntax checks (gh v2.96.0).

## 🐞 Issues Found

- **HIGH · Docker Mastery · Chapter 2, Compose example (lines 241-252).** *Observed:* `docker compose ps` shows the `web` service `Exited (0)`; it reuses Chapter 1's echo-and-exit image so nothing listens on the mapped `8080:8080`, contradicting the "small web app alongside a Redis cache" framing. *Fix:* give `web` a real long-running process (a tiny HTTP server, or `sleep infinity` placeholder) so `ps` shows it running and the port mapping is meaningful.
- **HIGH · Docker Mastery · Chapter 2, multi-stage Dockerfile (lines 271-289).** *Observed:* `docker build` fails at `RUN npm ci` — no `package.json`/`src` exists and the quest never has the learner create one. *Fix:* provide a minimal scaffold to create first, or explicitly label the snippet "illustrative — apply to your own Node project."
- **HIGH · GitHub Actions Basics · Chapter 2 secrets (line 293) & Chapter 3 matrix (lines 335, 348).** *Observed:* `{% raw %}`/`{% endraw %}` is wrapped around *inner* expressions, leaking literal Jekyll tags into copy-pasteable YAML and breaking the `${{ }}` expressions from the raw file. *Fix:* wrap the **entire** fenced block in one `{% raw %}`/`{% endraw %}` pair at the Markdown level — the exact pattern *CI/CD Fundamentals* (lines 381-395) and *The Warden's Gate* (lines 96-130) already use correctly. (Same leak also appears in prose at line 116 and the mastery-challenge line 377.)
- **HIGH · CI/CD Fundamentals · Chapter 3 git snippet (lines 338-346).** *Observed:* reproduced — creating a new file then `git commit -am` commits nothing ("nothing added to commit but untracked files present"); `-a` ignores untracked files and there is no `git add`. A learner "adding a greeting" (a new file) silently commits an empty change with no error. *Fix:* add an explicit `git add .` (or `git add <file>`) before `git commit`.
- **MEDIUM · Docker Mastery · Chapter 2, Trivy scan (line 294).** *Observed:* `trivy` is not installed and no install step exists on any OS path; presented as directly runnable. *Fix:* add a one-line install (or mark optional / link install docs) before `trivy image …`.
- **MEDIUM · Docker Mastery · Objectives vs. body.** *Observed:* validation criterion "Deploy containerized applications to cloud platforms" is only a single sentence claiming any cloud runtime can pull the image — no ECS/Cloud Run/Fly.io steps are ever walked. *Fix:* add one concrete minimal deploy walkthrough, or soften the objective.
- **MEDIUM · CI/CD Fundamentals · Chapter 2 checkpoint (line 310).** *Observed:* `npm test` runs `node --test` with zero test files, so "npm test passes" is vacuously true (0 tests, exit 0), undercutting the CI-verification lesson. *Fix:* have the learner add one trivial `node:test` test file.
- **LOW · CI/CD Fundamentals & Docker Mastery · Node version.** *Observed:* both pin `node-version: '20'` / `node:20-alpine`; Node 20 exited LTS maintenance ~Apr 2026. *Fix:* bump to a maintained LTS (22/24) in "best practices" examples.
- **LOW · Docker Mastery · registry push (line 305).** *Observed:* `docker tag … YOUR_USERNAME/…` fails verbatim (repo names must be lowercase) on careless copy-paste. *Fix:* note that the substituted username must be lowercase.
- **LOW · Level-hub link inconsistency (cross-quest).** *Observed:* *CI/CD Fundamentals*, *GitHub Actions Basics*, and *The Warden's Gate* link `[[Level 0101 - CI/CD & DevOps]]`, but *Docker Mastery* and *LaTeX CV* link `[[Level 0101 - Advanced Docker & DevOps]]` — two different hub names for the same level. *Fix:* standardize the level-hub wiki-link.

**No blocking security issues** were found in any quest — all `safety` dimensions scored 4-5, no destructive commands, and secrets guidance is correct throughout. (Note for a content pass: Docker's Linux path pipes `curl … | sh` from Docker's official installer without a "review before running" caution — low, informational.)

## 🔗 Chain Continuity

- **The real dependency spine holds.** *CI/CD Fundamentals* declares it unlocks *GitHub Actions Basics*, and *GitHub Actions Basics* lists *CI/CD Fundamentals* as a required prerequisite. Walking them in this order works: Fundamentals teaches the build-test-deploy vocabulary, triggers, and the `${{ secrets.NAME }}` pattern, and GHA Basics builds directly on all of it. A learner finishing quest 1 is genuinely ready for quest 3.
- **The window is a level slice, not a single storyline.** The planner's window mixes three unrelated series: *DevOps Pipeline Mastery* (quests 1 & 3), *DevOps Fundamentals* (Docker, quest 2), *Professional Identity Path* (LaTeX CV, quest 4), and *The Autonomous Realm / Ouroboros Loop* (quest 5). That's expected for a date-rotated window over a 13-quest level, but a System Engineer reading top-to-bottom should know these are parallel tracks, not a linear chain. **LaTeX CV in particular is a career-artifact quest with no CI/CD relationship** and only sits here by level number.
- **Prerequisite gap in The Warden's Gate.** It is *Chapter II* of the Ouroboros Loop campaign and assumes a "working First Turn loop" and a `potion-book` repo built in *Ouroboros Loop 01* (level **0000**, `/quests/0000/ouroboros-loop-01-the-first-turn/`), which is **not** in this slice. Its Chapter 1 YAML is even labelled "(additions)" to a `first-turn.yml` the learner is assumed to already have. A learner who lands here from the level-0101 hub without the prior chapter has nothing to splice the gate job into. The quest recommends the prerequisite in frontmatter, but the on-page prose could link it more prominently (matching the engine's own low-priority recommendation).
- **`{% raw %}` consistency is a chain-level teaching signal.** Because three of the five quests wrap whole fenced blocks correctly and one (GHA Basics) does not, a learner comparing quests gets contradictory modelling of how to escape Actions expressions on a Jekyll site. Aligning GHA Basics with its siblings improves the *whole* line, not just one page.
- **Docker → GHA handoff is fine conceptually** but Docker's own broken Compose/multi-stage snippets mean a learner who tries the hands-on parts leaves with a shakier "it actually ran" confidence than the CI/CD spine provides.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sealed). I did **not** run the agentic engine — per the skill and the workflow contract, `walk-plan.json` and `walk-evidence.json`/`.md` were pre-computed and sealed by a deterministic workflow step (the engine's child `claude` processes can't authenticate from the agent's Bash tool). I consumed them verbatim and made **zero** edits to plan, evidence, or any quest.
- **What I ran vs. reasoned:** I ran no quest commands myself. Every `passed`/`failed`/`skipped` in §Evidence is quoted from the sealed engine output (4 quests executed in a disposable sandbox). The linked-journey analysis in §Chain Continuity is my own reasoning from reading all five quest sources in plan order — labelled as reasoning, not testing.
- **Coverage gaps (stated honestly):**
  - **LaTeX CV was never scored** — the engine hit its 40-turn cap while probing the environment; I only reasoned about it statically. Treat its "no defects found" as *unverified*, not *clean*.
  - The sandbox is **Linux-only and network-restricted**: macOS/Windows install paths, `sudo` installs, `gh auth login`, `docker push`, live GitHub Actions runs, and the full TeX build were all `skipped`/unreachable and judged by inspection, not execution.
  - This is **window 1 of 3** — only 5 of the level's 13 quests were walked; the remaining 8 are not covered here.
- **Confidence:** High for the four scored quests' concrete command outcomes (reproduced in-sandbox with quoted output). Medium for the cross-quest continuity claims (read-based). Low/none for the LaTeX CV quest's correctness (unexecuted).
- **Scope discipline:** One slice, one report. No content edited, no branch, no commit — the caller handles git. Fixable bugs are captured in §Issues for a downstream content pass.

---

*Machine evidence summary (verbatim from `walk-evidence.md`): 4 quests evaluated · ✅ 2 pass · ⚠️ 2 warn · ❌ 1 fail · avg 78.0% · ~$2.8007.*
