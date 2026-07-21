---
title: System Engineer · L0101 · 2026-07-21
description: Quest-perfection walkthrough of the CI/CD & DevOps slice system-engineer/0101 on 2026-07-21,
  engine verdict warn. An evidence-based, learner's-eye session…
date: '2026-07-21T00:00:00.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- System Engineer
tags:
- system-engineer
- level-0101
- walkthrough
- quest-perfection
- warn
- ci-cd-devops
render_with_liquid: false
excerpt: 'System Engineer · Level 0101 — CI/CD & DevOps: an evidence-based quest-perfection walkthrough
  from 2026-07-21.'
slice: system-engineer/0101
character: system-engineer
level: '0101'
theme: CI/CD & DevOps
tier: Adventurer
verdict: warn
quest_count: 5
walk_date: '2026-07-21'
run_url: https://github.com/bamr87/it-journey/actions/runs/29826801543
source_report: test/quest-validator/walkthroughs/2026-07-21-system-engineer-0101.md
---

> **Slice** `system-engineer/0101` · **Level** 0101 (CI/CD & DevOps) · **Adventurer tier** · **Engine verdict** ⚠️ warn · **Walked** 2026-07-21
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29826801543) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-21-system-engineer-0101.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-21-system-engineer-0101.md)

---

## 🎯 Session Summary

I walked the **first window (5 of 13 quests)** of the **System Engineer → Level 0101 · CI/CD & DevOps (Adventurer ⚔️)** slice as a learner, driving the sealed execute-engine evidence and reading each quest's source in plan order. **Headline verdict: WARN** — the slice teaches solid, mostly-accurate CI/CD fundamentals (avg **75.0%**, 2 pass / 2 warn / 1 fail), but it does not yet hold together as a *coherent linked journey* for this character.

Two concrete problems dominate. First, **one quest is effectively a shell**: *Docker Containerization Mastery* (**fail, 51%**) promises Compose, security hardening, and cloud deploy in its objectives and portfolio checklist but teaches only a single `hello-world` Dockerfile — every platform block is an empty placeholder. Second, the **window's ordering mixes two unrelated campaigns into the CI/CD line**: a LaTeX-CV quest (Professional Identity Path) and *The Warden's Gate* (the Ouroboros Loop campaign, which assumes a `potion-book` repo + green "First Turn" run from a level-0000 quest that is nowhere in this slice). A System Engineer expecting a build-test-deploy path hits a résumé-typesetting detour and a chapter-2-of-a-campaign whose chapter 1 was never provided. The genuinely strong spine is **CI/CD Fundamentals → GitHub Actions Basics → The Warden's Gate** — that sub-chain is accurate and, apart from a git-identity gap and templating-tag leakage, ready to play.

## 🗺️ The Journey

Walked in `walk-plan.json` order (dependency-sorted window, index 0 of 3):

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ✅ pass | CI/CD Fundamentals: The Build-Test-Deploy Pipeline | 85 | Accurate, well-built spine; only real defect is an unconfigured `git commit`/`git push` in the Ch.3 bash block. |
| 2 | ❌ fail | Docker Containerization Mastery: Level 0101 (5) Quest | 51 | One working Dockerfile surrounded by empty placeholders; objectives promise Compose/security/cloud that are never taught. |
| 3 | ⚠️ warn | GitHub Actions Basics: Workflow Automation for Modern DevOps | 74 | Concepts verified correct, but two YAML blocks carry inline `{​% raw %​}`/`{​% endraw %​}` tags that break copy-paste from source. |
| 4 | ⚠️ warn | Forging the La(zy)TeX CV: Binary Level 0101 (5) Quest | 77 | Template compiles + links work, but the "stock LaTeX install" claim is false (needs `enumitem`/`titlesec`); thematically off-path for this character. |
| 5 | ✅ pass | The Warden's Gate: Kill Switches and Stage Gates | 88 | Technically excellent gate/kill-switch/permissions lesson; assumes a prior "First Turn" repo the slice never builds. |

## 🔬 Evidence

All rows below are from the sealed `walk-evidence.json` (mode: **execute**, real commands run in the disposable sandbox). Quoted output is trimmed.

### 1 · CI/CD Fundamentals — ✅ 85 · ran 5/5 runnable snippets (4 passed, 1 failed)
Dimensions: commands_work 4 · content_accuracy 5 · completeness 4 · clarity 4 · structure 4 · safety 4.

- **passed** `git --version && node --version` → `git version 2.54.0`, `v20.20.2`.
- **passed** `mkdir cicd-quest && cd cicd-quest && git init && npm init -y` — scaffolded (only a harmless "master vs main default branch" hint).
- **passed** Chapter 2 `package.json` written verbatim: `npm run build` printed `compiling...` then `build ok`; `npm test` (node --test) ran 0 tests / 0 fail; `npm run lint` exited 0 — matches the quest's "Ran it locally" checkpoint exactly.
- **failed** Chapter 3 trunk-based bash block: `git checkout -b add-greeting` and `npm test` succeeded, but `git commit -am "feat: add greeting"` **hard-failed** on the fresh sandbox — reproduced directly: *"fatal: empty ident name … Please tell me who you are."* The quest never has the learner run `git config --global user.name/user.email`. The following `git push -u origin add-greeting` would also fail — no remote is ever configured in the quest.
- **reasoned** Both GitHub Actions YAML blocks (Ch.2 CI, Ch.4 Deploy) parse as valid YAML and use current syntax (`actions/checkout@v4`, `actions/setup-node@v4`, `workflow_dispatch`, `secrets` context). Not run against a live runner (no repo/remote in sandbox).

### 2 · Docker Containerization Mastery — ❌ 51 · ran 4/6 runnable (4 passed, 0 failed)
Dimensions: commands_work 3 · content_accuracy 3 · **completeness 0** · clarity 2 · structure 2 · safety 5.

- **passed** The one substantive exercise works flawlessly: `docker build -t my-first-image .` (from `FROM alpine:3.20` + exec-form `CMD`) built cleanly; `docker run --rm my-first-image` printed exactly `Hello from your first Docker container!` — verbatim match to the quest's stated expected output.
- **skipped** All 5 "Choose Your Adventure Platform" fences (macOS/Windows/Linux/Cloud/Web) contain **only a single comment line** (e.g. `# macOS-specific commands and setup`) — nothing runnable.
- Engine finding (grep-verified): *"'compose'/'security'/'cloud' appear only in objective/checklist lines, never in instructional prose or code."* The three non-hello-world "Portfolio Artifacts Created" items have nothing to build.

### 3 · GitHub Actions Basics — ⚠️ 74 · ran 10 snippets (7 passed, 3 failed)
Dimensions: commands_work 3 · content_accuracy 4 · completeness 4 · clarity 3 · structure 5 · safety 5.

- **passed** `mkdir -p .github/workflows` (macOS/Linux/Cloud paths) and the Windows `New-Item` equivalent.
- **passed** Ch.1 "Hello Actions" full workflow YAML, Ch.2 `on:` triggers block, Ch.2 `needs:` job-ordering YAML — all parse and match current GitHub Actions semantics; the matrix math (2×3 − 1 exclude = 5 jobs) checks out.
- **failed** `gh run list` (Cloud Realms path) — errored with no authenticated repo context in the sandbox (expected for a bare runner; a real Codespace would satisfy it).
- **failed** Ch.2 Secrets/Permissions YAML and Ch.3 Matrix YAML — contain **inline** literal `{​% raw %​}`/`{​% endraw %​}` tags mid-expression, e.g. `API_TOKEN: ${​% raw %​}{​{ secrets.DEPLOY_TOKEN }​}{​% endraw %​}` (line 291) and `runs-on: ${​% raw %​}{​{ matrix.os }​}{​% endraw %​}` (line 333). As raw source they are not valid GitHub Actions expression syntax.

### 4 · Forging the La(zy)TeX CV — ⚠️ 77 · ran 4/5 runnable (4 passed, 0 failed)
Dimensions: commands_work 4 · content_accuracy 3 · completeness 4 · clarity 4 · structure 4 · safety 5.

- **passed** Ch.2 `cv.tex` template + `latexmk -pdf cv.tex` — compiled cleanly in a TeX Live container and produced a PDF with **selectable text and three clickable links** (email/LinkedIn/GitHub), verified by direct execution.
- Engine content-accuracy gap: the quest's claim (line 176) that the template *"uses only base TeX Live packages … compiles cleanly with a stock LaTeX install"* is **false** on a minimal/BasicTeX install — `enumitem` and `titlesec` (used at lines 183–184) are absent there and would throw `File 'enumitem.sty' not found`. The macOS BasicTeX note (line 121) installs `latexmk fontawesome5 CormorantGaramond` but omits those two.

### 5 · The Warden's Gate — ✅ 88 · ran 3/1 runnable (3 passed, 0 failed)
Dimensions: commands_work 4 · content_accuracy 5 · completeness 4 · clarity 4 · structure 5 · safety 5.

- **passed** The gate + turn jobs YAML, the `startup_failure` trap YAML, and the two-line caller-permissions cure all parse and match GitHub's real documented behavior (caller job permissions **cap** every job in a called workflow, validated at trigger time).
- **skipped** `gh variable set LOOP_ENABLED … && gh workflow run … && gh run watch` — could not run end-to-end (no authenticated GitHub repo in the sandbox); the embedded shell logic was validated by inspection.

## 🐞 Issues Found

Grouped by severity; each cites what was observed (tested = command actually run; reasoned = judged statically from source).

**HIGH**
- **[Docker Mastery · Completeness]** *(tested — engine grep + snippet skips)* The objectives + "Portfolio Artifacts Created" checklist promise Docker Compose, security best practices, and cloud deployment, but the body teaches only a single `hello-world` Dockerfile; the 5 platform fences (lines 114–150) are empty placeholder comments. **Fix:** either add real runnable content for Compose (`docker-compose.yml` + `docker compose up`), a hardening example (non-root `USER`, multi-stage, `trivy`/`docker scan`), and a registry-push/deploy step — or remove those items from the objectives/checklist so the quest stops promising what it never teaches. Also fill Ch.1 steps 1/2/4 (lines 166–169), which currently just restate their titles.
- **[GitHub Actions Basics · Ch.2 & Ch.3 YAML]** *(tested — 2 failed YAML parses)* Inline `{​% raw %​}…{​% endraw %​}` tags mid-expression at lines 291 and 333 (and inline in prose at lines 116 and 375) are invalid GitHub Actions syntax **in the raw source**. A learner who copies from GitHub's source view / the `.md` gets a broken workflow. **Fix:** wrap the whole fenced block with the raw tags on their own lines (the pattern *CI/CD Fundamentals* uses at lines 381/395, which renders correctly), rather than embedding the tags inside the expression.
- **[CI/CD Fundamentals · Ch.3 bash block]** *(tested — reproduced fatal error)* `git commit -am` fails with *"empty ident name … Please tell me who you are"* on any fresh machine; the quest never teaches `git config --global user.name/user.email`. **Fix:** add a one-line git-identity setup in the platform section or immediately before the Ch.3 snippet.

**MEDIUM**
- **[LaTeX CV · Ch.2 claim]** *(tested — engine reasoned from a real TeX Live compile + package knowledge)* "Compiles cleanly with a stock LaTeX install" is untrue on BasicTeX/minimal installs (`enumitem`, `titlesec` missing). **Fix:** add `enumitem titlesec` to the BasicTeX `tlmgr install` line (121) or state the template needs a `texlive-latex-extra`-equivalent set; add a troubleshooting note for `File '<pkg>.sty' not found`.
- **[CI/CD Fundamentals · Ch.3 push line]** *(reasoned)* `git push -u origin add-greeting` (line 344) assumes a remote `origin` that no earlier step creates. **Fix:** add `git remote add origin <url>` context or explicitly label the push line illustrative.
- **[GitHub Actions Basics · Cloud path]** *(tested — `gh run list` failed)* `gh run list` (line 197) needs an authenticated repo/Codespace context. **Fix:** add a one-line note so learners outside a Codespace aren't confused by the `GH_TOKEN` error.

**LOW**
- **[Chain-wide · stale "Level hub" labels]** *(reasoned — read from source)* Knowledge-Graph "Level hub" links disagree: *CI/CD Fundamentals* (line 501), *GitHub Actions Basics* (451), and *Warden's Gate* (247) correctly say **"Level 0101 - CI/CD & DevOps"**, but *Docker Mastery* (316) and *LaTeX CV* (477) say **"Level 0101 - Advanced Docker & DevOps"** — a stale/inconsistent hub name. **Fix:** normalize to the level's canonical theme.
- **[Warden's Gate · Mastery Challenge]** *(reasoned)* The reusable-workflow stub (`potion-fix.yml`) has no starter snippet, unlike the rest of the quest. **Fix:** add a minimal stub so learners have a starting point.
- **[CI/CD Fundamentals · sudo]** *(reasoned)* The Linux path's `sudo apt install` (line 191) is unqualified. **Fix:** a brief note that it needs admin rights.

## 🔗 Chain Continuity

Reading the five quests as one linear journey a System Engineer would actually take:

- **The declared dependency inside the slice is satisfied and correctly ordered.** *GitHub Actions Basics* declares `required_quests: [/quests/0101/cicd-fundamentals/]`, and the planner places CI/CD Fundamentals (#1) before it (#3). A learner finishing #1 has the build-test-deploy mental model and the `on:`/`secrets`/`needs:` vocabulary that #3 builds on — genuinely good continuity. *Warden's Gate* (#5) then deepens the same GitHub Actions permissions/gate material. **This #1 → #3 → #5 sub-chain is the real CI/CD spine and it holds together.**

- **Two quests are thematic intruders in this window.** *LaTeX CV Forging* (#4) belongs to the **Professional Identity Path** (`primary_technology: latex`, `skill_focus: fullstack`) — it teaches résumé typesetting, not CI/CD or infrastructure. For a System Engineer walking a DevOps level it is a jarring detour with no incoming or outgoing link to the other four quests. It is a fine quest in isolation (77%), but it dilutes the level's identity.

- **The last quest assumes setup the slice never provides.** *Warden's Gate* is **Chapter II of the Ouroboros Loop campaign**: its prerequisites demand *"Chapter I's `potion-book` repo with a green First Turn run"* and its `recommended_quests` points to `/quests/0000/ouroboros-loop-01-the-first-turn/` — a **level-0000 quest absent from this slice**. Every command (`gh variable set LOOP_ENABLED`, `gh workflow run first-turn.yml`) targets a `first-turn.yml` the learner never created here. A learner walking only the 0101 window cannot complete its mastery challenge without first detouring to a different level. The concepts are still readable, but the hands-on arc is broken at the seam.

- **A recurring unstated prerequisite spans the DevOps quests: identity/auth setup.** #1 does `git commit` without ever configuring a git identity (verified fatal); #3 and #5 lean on `gh auth login` / an authenticated repo (verified `gh run list` failure). No quest in the window owns "configure your git identity and authenticate `gh` once." A first-timer hits the same class of wall in three of the five quests. This is the single highest-leverage continuity fix for the slice.

- **Ordering nit:** because the planner sorts by dependency graph, the two campaign-orphan quests (#4 LaTeX, #5 Warden's Gate) land *after* the tight #1→#3 pair, so the felt experience is "two great CI/CD quests, then a résumé, then chapter-two-of-a-different-story." Not a defect the quests can fix alone, but worth noting for how this character experiences the level.

## 🧠 Reasoning & Method

- **Mode:** `execute`. I did **not** run the engine — per the workflow contract, `walk-evidence.json` / `walk-evidence.md` were pre-computed and sealed by a deterministic engine step (the engine's child `claude` processes cannot authenticate from an agent's Bash tool). I consumed them verbatim.
- **What is tested vs. reasoned:** every `passed`/`failed`/`skipped` in §Evidence comes from a command the sandbox actually ran (per `walk-evidence.json`). Every item I derived by reading the quest source myself (stale hub labels, thematic-path mismatch, the cross-level prerequisite gap, the git/gh identity thread) is labelled **reasoned** — I read all five quest files in plan order but did not independently re-execute their commands.
- **Coverage & limits:**
  - This is **window 1 of 3** — I walked **5 of the 13** quests in the level. The other 8 are out of scope for this run and unassessed here.
  - Sandbox limits mean anything needing a live authenticated GitHub context (`gh run list`, `gh workflow run … && gh run watch`, running a workflow on a real runner) was **skipped/reasoned**, not tested — this affects the two GitHub-Actions-heavy quests (#3, #5) most. Their YAML was parse-validated and their logic inspected, but no end-to-end Actions run was observed.
  - Cross-OS blocks (macOS `brew`/`winget`, Windows PowerShell) were skipped because the sandbox is Linux; the Linux/Cloud equivalents were run where they exist.
  - On the `{​% raw %​}` finding I add nuance the engine (which reads raw `.md`) can't: Jekyll *strips* `{​% raw %​}`/`{​% endraw %​}` when rendering, so a learner copying from the **published page** likely gets valid syntax; the real hazard is copying from the **raw markdown / GitHub source view**. I did not render the page, so this rendered-vs-raw distinction is **reasoned**, while the failed YAML parse of the raw source is **tested**.
- **Confidence:** High on the per-quest verdicts (machine-checked, real commands). High on the chain-continuity findings, which come from directly quoted frontmatter/prerequisite lines. Medium on the exact learner impact of the templating tags, pending a rendered-page check.

---

### Appendix — Machine evidence (verbatim from `walk-evidence.md`)

> **5** quests evaluated · ✅ 2 pass · ⚠️ 2 warn · ❌ 1 fail · avg **75.0%** · ~$3.0902
>
> | | Score | Quest | Snippets run |
> |---|--:|---|:-:|
> | ✅ | 85 | CI/CD Fundamentals: The Build-Test-Deploy Pipeline | 5/5 (1✗) |
> | ❌ | 51 | Docker Containerization Mastery: Level 0101 (5) Quest | 4/6 |
> | ⚠️ | 74 | GitHub Actions Basics: Workflow Automation for Modern DevOps | 10/4 (3✗) |
> | ⚠️ | 77 | Forging the La(zy)TeX CV: Binary Level 0101 (5) Quest | 4/5 |
> | ✅ | 88 | The Warden's Gate: Kill Switches and Stage Gates | 3/1 |
