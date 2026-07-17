---
title: System Engineer · L0101 · 2026-07-15
description: Quest-perfection walkthrough of the CI/CD & DevOps slice system-engineer/0101 on 2026-07-15,
  engine verdict warn. An evidence-based, learner's-eye session…
date: '2026-07-15T12:13:59.000Z'
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
  from 2026-07-15.'
slice: system-engineer/0101
character: system-engineer
level: '0101'
theme: CI/CD & DevOps
tier: Adventurer
verdict: warn
quest_count: 5
walk_date: '2026-07-15'
run_url: https://github.com/bamr87/it-journey/actions/runs/29412020762
source_report: test/quest-validator/walkthroughs/2026-07-15-system-engineer-0101.md
---

> **Slice** `system-engineer/0101` · **Level** 0101 (CI/CD & DevOps) · **Adventurer tier** · **Engine verdict** ⚠️ warn · **Walked** 2026-07-15
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29412020762) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-15-system-engineer-0101.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-15-system-engineer-0101.md)

---

## 🎯 Session Summary

- **Character / class:** 🏗️ System Engineer (Adventurer tier ⚔️)
- **Level:** `0101` — theme **CI/CD & DevOps**, permalink `/quests/0101/`
- **Quests walked:** 5 (window 1 of 3; the full level holds 13 quests — this is a
  rotating window, not the whole level)
- **Mode:** `execute` — quest commands were run for real in a disposable sandbox by
the agentic engine; I consumed the **workflow-sealed** `walk-evidence.json` / `walk-evidence.md` as-is (I did not and cannot re-run the engine from the agent).
- **Headline verdict:** ⚠️ **WARN** — 3 pass / 0 warn / 2 fail, average **60.8%**.

The three CI/CD-native quests in this slice — **CI/CD Fundamentals** (88), **GitHub Actions Basics** (80), and **The Warden's Gate** (83) — form a genuinely strong, correctly-ordered spine for a System Engineer: concepts → workflow syntax → production-grade kill-switch/permissions discipline. Their flaws are consistent and narrow (they teach a git/push rhythm but never show `git remote add origin` or an initial commit, so the "make it green in the Actions tab" challenges can't be completed from the document alone). The two failing quests are **not** part of that spine and drag the average down: **Docker Containerization Mastery** (12) is a verbatim unfilled scaffold — every code block is a placeholder and the one Docker-tagged block fails to build — and **Forging the La(zy)TeX CV** (41) promises a `cv.tex` it never provides and writes every LaTeX example with an invalid doubled backslash. A maintainer should treat Docker and LaTeX-CV as blocking content bugs and the spine's missing-git-remote gap as a shared, easily-fixed medium.

## 🗺️ The Journey

Walked in `walk-plan.json` order (dependency-sorted):

1. ✅ **CI/CD Fundamentals: The Build-Test-Deploy Pipeline** — **88** · the
package.json build/test/lint artifact runs exactly as documented; only the Chapter 3 git rhythm has a real gotcha (no initial commit, no remote).
2. ❌ **Docker Containerization Mastery: Level 0101 (5) Quest** — **12** · an
unfilled template; 6/6 code blocks are placeholders and the `docker` block fails to build. Teaches nothing about Docker despite the title.
3. ✅ **GitHub Actions Basics: Workflow Automation for Modern DevOps** — **80** ·
every YAML snippet valid, matrix math (2×3−1=5) and cron verified; gap is it never shows the git add/commit/push to actually trigger a run.
4. ❌ **Forging the La(zy)TeX CV: Binary Level 0101 (5) Quest** — **41** · the core
`cv.tex` artifact is never provided/linked, `latexmk -pdf cv.tex` fails, and every LaTeX example uses an invalid `\\` doubled backslash.
5. ✅ **The Warden's Gate: Kill Switches and Stage Gates** — **83** · the gate-job
kill-switch shell logic ran correctly armed/disarmed; caller-permission / `startup_failure` teaching is accurate. Live `gh` bits unverifiable without auth (inherent to the topic).

## 🔬 Evidence

All command outcomes below are from the sealed `walk-evidence.json` (execute mode, `mock: false`); I quote the engine's recorded findings, trimmed. Snippet coverage is `ran/total`.

### 1. CI/CD Fundamentals — score 88 · snippets 4/5 run (1 failed)
- **`passed`** — Linux setup `mkdir cicd-quest && cd cicd-quest && git init && npm init -y` ran cleanly.
- **`passed`** — Chapter 2 `package.json`: `npm run build` → `compiling... / build ok`; `npm test` (node --test) exited 0; `npm run lint` → `linting...` exit 0. *"worked exactly as written."*
- **`failed`** — Chapter 3 git rhythm: *"on a fresh repo (git init + npm init -y, no initial commit), if the learner's 'tiny change' is a new untracked file, `git commit -am` silently does nothing and exits 1 … Verified this by reproducing the exact sequence in a fresh repo."* And *"`git push -u origin add-greeting` fails with 'origin does not appear to be a git repository' … the quest never shows a `git remote add origin` step anywhere."*
- **`reasoned`** — both GitHub Actions YAML snippets (Ch2 CI, Ch4 deploy) parse as valid YAML and correct Actions syntax; not executed end-to-end (no `act` in sandbox).
- Dimensions: commands_work 4 · content_accuracy 5 · completeness 4 · clarity 4 · structure 5 · safety 5.

### 2. Docker Containerization Mastery — score 12 · snippets 6/6 run (1 failed) *(fail)*
- **`failed`** — Chapter 1 ```docker block (lines 113-122): *"contains no Dockerfile instructions — only comments and bracket placeholders … Running `docker build` … fails immediately with 'ERROR: failed to build: failed to solve: file with no instructions'."*
- **`passed` (as no-ops)** — the macOS/Linux/Cloud bash blocks (55-57, 71-73, 82-84), the PowerShell block (63-65) and the JS block (90-92) each contain only a single comment line: *"execute as a no-op (exit 0) but teach and do nothing."*
- Engine finding: *"None of the 6 code blocks contain a single real, copy-pasteable Docker command … anywhere in the document, despite the quest title and objectives being entirely about Docker."*
- Dimensions: commands_work 0 · content_accuracy 0 · completeness 0 · clarity 0 · structure 2 · safety 5.

### 3. GitHub Actions Basics — score 80 · snippets 8/? run (1 failed)
- **`passed`** — `mkdir -p .github/workflows` and the PowerShell `New-Item -ItemType Directory -Force -Path .github\workflows` (via `pwsh`) both succeeded cross-platform.
- **`passed`** — all 5 YAML snippets parsed valid; matrix math verified *"`os:[ubuntu,windows]` × `node:['18','20','22']` = 6, minus 1 exclude = 5 — exactly matches 'leaving five parallel jobs'"*; cron `0 6 * * 1` confirmed Monday 06:00 UTC.
- **`failed`** — Cloud Realms path `mkdir -p .github/workflows && gh run list`: *"`gh run list` … correctly fail[s] without authentication … expected outside a real GitHub Codespace and not a quest defect, but it means the Cloud Realms path's `gh run list` example cannot be end-to-end verified here."*
- Engine gap: *"the quest asks learners to 'commit and trigger' a workflow but never shows the git add/commit/push steps."*
- Dimensions: commands_work 4 · content_accuracy 4 · completeness 3 · clarity 4 · structure 5 · safety 5.

### 4. Forging the La(zy)TeX CV — score 41 · snippets 4/? run (2 failed) *(fail)*
- **`failed`** — `latexmk -pdf cv.tex`: *"failed with `latexmk: command not found`, and even if latexmk were installed, `cv.tex` does not exist anywhere — `find` … shows only QUEST.md."*
- **`failed`** — Chapter 3 ```tex example: *"written with doubled backslashes throughout: `\\resumeSubheading{...}`, `\\resumeItemListStart`, `\\resumeItem{...}` … verified via `grep -n` on the raw markdown … pasting this snippet verbatim would break the line and then print `resumeSubheading{Your Company}…` as literal text."* Same defect in `\\pdfgentounicode=1`, `\\includegraphics`, `\\href{}`, `\\linewidth`.
- **`passed`** — the VS Code `latex-workshop` settings JSON is valid JSON with real config keys.
- **`skipped`** — macOS/Linux install commands (`brew … mactex-no-gui`, `apt-get install texlive-full`, `tlmgr install …`) not safely runnable (no root/network/wrong OS); judged syntactically reasonable.
- Dimensions: commands_work 1 · content_accuracy 2 · completeness 2 · clarity 2 · structure 3 · safety 5.

### 5. The Warden's Gate — score 83 · snippets 4/? run (1 skipped)
- **`passed`** — Chapter 1 gate-job shell run with `ENABLED=true` → *"correctly printed `go=true` to $GITHUB_OUTPUT"*; with `ENABLED` unset → *"'loop idle (LOOP_ENABLED=) — flip the variable to arm.' and `go=false` — matches the quest's claimed disarmed behavior exactly."*
- **`passed`** — all three YAML snippets (gate addition, Ch2 trap, Ch2 fix) parse cleanly with PyYAML in a full workflow skeleton.
- **`skipped`** — the `gh variable set/delete … gh workflow run … gh run watch` bash block: *"gh v2.96.0 installed but not authenticated … no real GitHub repo/workflow to target — inherent to a CI/CD quest and not a defect, but … the live `startup_failure` message and `gh run watch` race behavior are unverified."*
- Dimensions: commands_work 4 · content_accuracy 4 · completeness 4 · clarity 4 · structure 5 · safety 5.

## 🐞 Issues Found

**High**

- **high** · *Docker Containerization Mastery* · whole document (code blocks lines
55-92, 113-122; objectives; resources) · **Observed:** every one of the 6 code blocks is placeholder comments/bracketed TODOs; the `docker` block fails to build (`file with no instructions`) when run; none of the four stated validation criteria (build/run containers, Docker Compose, security/optimization, cloud deploy) is taught anywhere — content_accuracy, completeness, commands_work all scored 0. **Fix:** author the actual tutorial: a minimal working Dockerfile + real `docker build`/`docker run` in Chapter 1, a `docker-compose.yml` with 2+ services, a security/optimization section (non-root `USER`, multi-stage, `.dockerignore`), one concrete cloud-deploy walkthrough, and real resource URLs. Until then this quest teaches nothing and should arguably be `draft: true`.
- **high** · *Forging the La(zy)TeX CV* · Chapter 2 "Summon the Template (Link to
cv.tex)" · **Observed:** the chapter title promises a link to `cv.tex` but no file or fetch command exists; `latexmk -pdf cv.tex` fails because the artifact is absent, so Chapter 1's "compile without errors" is impossible from the document alone. **Fix:** embed the full `cv.tex` in the quest or give an explicit fetch command (e.g. a `curl`/`git clone` URL to the repo path holding `cv/cv.tex`), plus a minimal bootstrap `.tex` fallback.
- **high** · *Forging the La(zy)TeX CV* · every LaTeX code/prose span (Chapters 2-4,
lines ~192-193, 223-227, 230) · **Observed:** doubled backslashes throughout (`\\resumeSubheading`, `\\resumeItem`, `\\resumeItemListStart/End`, `\\href`, `\\includegraphics`, `\\linewidth`, `\\pdfgentounicode=1`); in LaTeX `\\` is a line-break, so copy-pasting produces broken output. **Fix:** replace every `\\` with a single `\` in LaTeX contexts. (Note: this is a genuine content defect, not a Markdown-escaping artifact — the engine confirmed the doubling exists literally inside the fenced ```tex block via `grep -n` on the raw file.)

**Medium**

- **medium** · *CI/CD Fundamentals* · Chapter 3 git rhythm (lines 338-346) &
Intermediate Challenge · **Observed:** `git commit -am` silently no-ops on a new untracked file, and `git push -u origin add-greeting` fails because no `git remote add origin` is ever shown, yet the Intermediate Challenge requires a green run "visible in the Actions tab." **Fix:** add `git add .` (or an initial commit right after `npm init -y` in the setup paths) before `git commit`, and a `git remote add origin <url>` / "create a GitHub repo" step before `git push`.
- **medium** · *GitHub Actions Basics* · Novice/Intermediate Challenges & Cloud
Realms path (lines 194-198, 360-378) · **Observed:** learners are told to "commit and trigger" and to run `gh run list`, but the git add/commit/push steps are never shown and `gh run list` fails without auth outside a Codespace. **Fix:** add the explicit commit/push sequence, and note that `gh` needs `gh auth login` (or a Codespace) before `gh run list` works.
- **medium** · *Forging the La(zy)TeX CV* · macOS BasicTeX note (line 133) ·
**Observed:** `tlmgr install … CormorantGaramond` — package name unverified against CTAN (`cormorantgaramond` is the CTAN id). **Fix:** confirm the exact tlmgr package name before publishing to avoid a failed install.

**Low**

- **low** · *The Warden's Gate* · "Reproduce It" bash block (lines 136-139) ·
**Observed:** chaining `gh workflow run X && gh run watch` can race ahead of GitHub registering the new run (known `gh` gotcha); no fallback is mentioned. **Fix:** note a short retry/`--exit-status` fallback if `gh run watch` reports no in-progress run.
- **low** · *Cross-quest* · Knowledge-Graph "Level hub" wiki-links · **Observed:**
Docker and LaTeX-CV both link `[[Level 0101 - Advanced Docker & DevOps]]`, while CI/CD Fundamentals, GitHub Actions, and Warden's Gate link `[[Level 0101 - CI/CD & DevOps]]`. Two names for one level hub will split the graph. **Fix:** standardize on the level's canonical theme name (`CI/CD & DevOps`).

No fabricated issues: every item above cites a run command outcome or an exact quoted line from the quest source.

## 🔗 Chain Continuity

Reasoning about the five as one journey a System Engineer would actually take:

- **A strong, correctly-ordered spine exists.** `cicd-fundamentals` declares
`unlocks_quests: /quests/0101/github-actions-basics/`, and `github-actions-basics` declares `required_quests: /quests/0101/cicd-fundamentals/` — the dependency edge is reciprocal and honest. A learner finishing Fundamentals (CI/CD mental model, build-test-deploy stages, the `on: [push, pull_request]` workflow, secrets) is genuinely ready for GitHub Actions Basics (workflow/job/step hierarchy, triggers, matrix). The Warden's Gate then builds on Actions fluency to teach production-grade gate jobs, least-privilege permissions, and `startup_failure` forensics — the exact operational discipline a System Engineer needs. This trio is the real curriculum.
- **A shared, fixable prerequisite gap spans the spine.** Both Fundamentals and
GitHub Actions Basics assume the learner can push to a remote and see a green Actions run, but *neither* shows `git remote add origin` or the initial commit. A real beginner following either quest verbatim on a fresh repo hits the exact failure the sandbox reproduced (`git commit -am` no-op, then `push` to a missing origin). The chain never provides this step, so the hands-on "make it green" challenges stall at the same wall in two consecutive quests — worth fixing once, consistently.
- **The Warden's Gate points *out* of this slice for its prerequisite.** It lists
`recommended_quests: /quests/0000/ouroboros-loop-01-the-first-turn/` (Level 0000) and its body assumes "your `potion-book` repo with a green First Turn run." That prerequisite is **not** satisfied by any quest in this window — a System Engineer arriving from the CI/CD spine has a Node pipeline repo, not a First-Turn loop repo. The quest is self-contained enough to *read* and its patterns verified in isolation, but the hands-on Mastery Challenge assumes a repo the slice never built.
- **The two failing quests are off-spine and don't participate in the chain.** Neither
Docker Mastery nor the LaTeX CV is referenced by any `unlocks_quests`/ `required_quests` edge among the five; they're independent Level-0101 entries that happen to share the level. Docker's own frontmatter even points at Level 0001/0010 prerequisites and Level 0110 follow-ups that live outside this theme. So their failures don't *break* the CI/CD learning path — but a learner browsing the `/quests/0101/` hub will encounter a completely empty Docker "quest" and a LaTeX CV quest whose first command fails, which damages trust in the level as a whole.
- **Naming drift in the graph.** The level-hub wiki-link disagreement (`CI/CD &
DevOps` vs `Advanced Docker & DevOps`) is a small but real continuity defect: the Obsidian graph would render two separate hub nodes for one level.

Net: as a *System Engineer CI/CD path*, the slice's spine is coherent and recommendable once the git-remote gap is closed; as a *Level 0101 hub*, it currently exposes two quests (Docker, LaTeX-CV) that fail on first contact.

## 🧠 Reasoning & Method

- **What I ran vs. reasoned.** I ran **nothing** against the quests myself — the
agentic execute engine had already been run deterministically by the workflow and its results sealed into `walk-evidence.json` / `walk-evidence.md` before this session (the engine's child `claude` processes can't authenticate from the agent's Bash tool). I consumed that evidence verbatim and did **not** edit, regenerate, or hand-write it. Every `passed`/`failed`/`skipped`/`reasoned` above is the engine's recorded outcome; the linked-journey analysis in **Chain Continuity** is my own reasoning over the five quest sources, which I read in full in plan order.
- **Mode & sandbox.** `execute` mode, disposable sandbox, per-quest isolation
  (`mock: false`). Total engine cost ~$2.71, 5/5 quests scored, 0 errored.
- **Coverage limits (honest).**
  - This is **window 1 of 3** — only 5 of the level's **13** quests were walked. The
    other 8 (rotating windows) are **not** covered by this report.
  - Anything needing a **live authenticated GitHub repo** is unverified: the GitHub
    Actions Cloud-Realms `gh run list`, and The Warden's Gate's `gh variable`/`gh
    workflow run`/`gh run watch` sequence and its headline live `startup_failure`
    text. These are inherent to CI/CD topics, not defects — but the "green Actions
    tab" end state is `reasoned`, never witnessed.
  - LaTeX install commands (`brew`, `apt-get texlive-full`, `tlmgr`) were `skipped`
    (no root/network/correct OS); judged by static review only.
  - The GitHub Actions YAML deploy/CI workflows and the Warden's Gate YAML were
    validated as parse-correct, not executed by a runner (no `act`).
- **Confidence.** High on the two failures (Docker = template, LaTeX-CV = missing
artifact + `\\` defect — both reproduced by real sandbox commands) and on the git-remote gap (reproduced verbatim). Medium on the "green Actions tab" completion claims, which are reasoned rather than executed because they need live GitHub auth.
- **Scope discipline.** One slice, one report. I made no content edits, opened no PR,
and did not expand to other windows/levels/characters. Fixable bugs are captured in **Issues Found** for a content pass to act on.

---

*Machine evidence summary (verbatim from `walk-evidence.md`): "**5** quests evaluated · ✅ 3 pass · ⚠️ 0 warn · ❌ 2 fail · avg **60.8%** · ~$2.7137".*
