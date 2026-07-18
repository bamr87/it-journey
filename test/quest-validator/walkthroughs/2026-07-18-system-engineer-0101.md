---
title: 'Walkthrough — System Engineer · Level 0101 (CI/CD & DevOps)'
date: '2026-07-18T12:11:40.000Z'
character: system-engineer
level: '0101'
theme: CI/CD & DevOps
tier: Adventurer
quest_count: 5
mode: execute
overall_verdict: fail
session:
  window: '1 of 3 (offset 0, size 5)'
  level_total_quests: 13
  scored: 4
  errored: 1
  average_score: 67.2
  counts: { pass: 0, warn: 3, fail: 2 }
  engine_cost_usd: 2.284
  evidence: walk-evidence.json (sealed by workflow — consumed as-is, not regenerated)
---

## 🎯 Session Summary

I walked a **5-quest window** (window 1 of 3; the full level holds 13 quests) of the
**System Engineer** path at **Level 0101 — CI/CD & DevOps (Adventurer tier)**, as a learner
would, in the runner's disposable sandbox using the sealed **execute-mode** evidence the
workflow pre-computed. Four quests scored (avg **67.2%**, 0 pass / 3 warn / 2 fail); the fifth
(the LaTeX CV quest) **errored out** in the engine (hit the 40-turn limit after its toolchain
installs were denied network/sudo), so it carries **no machine verdict** and I could only reason
statically about it.

The headline: the **conceptual spine of this level is strong and accurate**, but two of the five
quests would actively strand a learner who follows them literally. **CI/CD Fundamentals** teaches
a workflow whose `npm ci` step is verified to fail because the setup never creates a
`package-lock.json`, and **Docker Mastery** is unfinished template scaffolding — 5 of 6 "runnable"
blocks are empty comments and its headline objectives (Compose, security, cloud deploy) are never
taught. I mark the **slice `fail`**: two fails plus a broken flagship first quest is enough to
block a beginner, even though the CI→GitHub-Actions→Warden's-Gate thread is otherwise sound.

## 🗺️ The Journey

Walked in planner order (dependency-sorted window):

1. ⚠️ **CI/CD Fundamentals: The Build-Test-Deploy Pipeline** — **76** · Accurate, well-structured
   concepts and working npm scripts, but a verified `npm ci` failure and a silent `git commit -am`
   no-op would trip a literal follower.
2. ❌ **Docker Containerization Mastery** — **48** · One working hello-world container; everything
   else is empty placeholder scaffolding and the promised Compose/security/cloud content is absent.
3. ⚠️ **GitHub Actions Basics** — **68** · Solid, well-verified concepts, but leaked Jekyll
   `{% raw %}{% raw %}{% endraw %}`/`{% raw %}{% endraw %}{% endraw %}` tags produce broken copy-paste YAML in the raw source, including in a required Mastery Indicator.
4. ❓ **Forging the La(zy)TeX CV** — **— (errored)** · No engine verdict — the run hit the 40-turn
   cap after `sudo`/network installs were denied. Thematic outlier for a CI/CD level; static read
   only (see §7).
5. ⚠️ **The Warden's Gate: Kill Switches and Stage Gates** — **77** · Technically accurate and
   well-structured; its one true hands-on block needs a pre-existing authenticated repo from an
   earlier campaign chapter, an inherent genre limit rather than a defect.

## 🔬 Evidence

All outcomes below come from commands the execute engine actually ran in the sandbox (`tested`),
or are explicitly labelled `reasoned` where a step was judged from source without execution.
Dimension scores are on the engine's 1–5 scale.

### 1. CI/CD Fundamentals — 76% ⚠️ (ran 5/5 runnable snippets, 2 ✗)
Dimensions: commands_work **3**, content_accuracy **4**, completeness **4**, clarity **4**, structure **4**, safety **5**.

- ✅ **Linux setup path passed** — `sudo apt … git nodejs npm`, `git --version`, `node --version`,
  `mkdir cicd-quest && cd cicd-quest`, `git init`, `npm init -y` all ran clean; Cloud path
  (`git/node --version`) passed too. macOS/Windows paths `skipped` (wrong OS, correctly out of scope).
- ✅ **`package.json` scripts passed** — `npm run build` prints `compiling…` then `build ok` (exit 0),
  `npm test` runs `node --test` (0 tests, exit 0), `npm run lint` exits 0. Maps cleanly to stages.
- ❌ **Chapter 2 CI workflow FAILED (tested).** The workflow's `run: npm ci` fails because the quest's
  own setup only runs `npm init -y` — no lockfile is ever generated: *"`npm ci` fails with `npm error
  code EUSAGE … can only install with an existing package-lock.json`."* A learner completing the
  Intermediate Challenge ("a passing green run in the Actions tab") hits this on a fresh repo.
- ❌ **Chapter 3 fast-feedback snippet FAILED (tested).** `git commit -am "feat: add greeting"` after
  the `# … make a tiny change …` placeholder silently commits nothing for the natural reading (a new
  file): *"`git commit -am` on an untracked new file returns 'nothing added to commit but untracked
  files present' (exit 1)"*. No `git add` is shown.
- 🟰 Pipeline diagram + feedback-loop list judged `reasoned` (accurate). `git push -u origin …` not run
  (needs a real remote) — correctly out of sandbox scope.

### 2. Docker Containerization Mastery — 48% ❌ (ran 3/6 runnable snippets)
Dimensions: commands_work **2**, content_accuracy **3**, completeness **1**, clarity **2**, structure **2**, safety **5**.

- ✅ **The one real snippet passed** — the minimal `Dockerfile` (`FROM alpine:3.20` + `CMD ["echo", …]`),
  `docker build -t my-first-image .` and `docker run --rm my-first-image` produce exactly the documented
  `Hello from your first Docker container!`.
- ❌ **5 of 6 "runnable" blocks are empty placeholders (tested → skipped).** Every platform block is a
  single comment — `# macOS-specific commands and setup`, `# PowerShell and Windows-specific commands`,
  `# Linux distribution-specific commands`, `# Cloud platform commands and configurations`,
  `// Cross-platform web technologies` — with bracketed prose like *"[Detailed instructions including
  Homebrew installations …]"*. Nothing executable, nothing to learn.
- ❌ **completeness = 1.** The objectives and completion checklist promise Docker Compose,
  security/optimization, and cloud deployment; **none of it exists anywhere in the body.** As shipped a
  learner gets one hello-world container backing a "Container Orchestration Mastery" reward.

### 3. GitHub Actions Basics — 68% ⚠️ (ran 8/4, 3 ✗)
Dimensions: commands_work **3**, content_accuracy **3**, completeness **4**, clarity **3**, structure **4**, safety **5**.

- ✅ **Setup + concept snippets passed** — Windows (`winget … ; New-Item … .github\workflows`) and Linux
  (`apt … gh git; mkdir -p .github/workflows`) blocks ran; the "Hello Actions" workflow and the `on:`
  trigger block (push/paths, pull_request, cron, workflow_dispatch) parse correctly; the `needs: build`
  ordering block passed.
- ❌ **Leaked Jekyll raw-tags FAILED (tested) on the secrets and matrix blocks.** The source literally
  contains `${% raw %}{% raw %}{% endraw %}{{ secrets.DEPLOY_TOKEN }}{% raw %}{% endraw %}{% endraw %}`, `${% raw %}{% raw %}{% endraw %}{{ matrix.os }}{% raw %}{% endraw %}{% endraw %}` and
  `${% raw %}{% raw %}{% endraw %}{{ matrix.node }}{% raw %}{% endraw %}{% endraw %}` (lines 291, 333, 346), plus the same artifact in the **Mastery
  Indicator** (line 116) and **Intermediate Challenge** (line 375). Any raw-markdown consumer (GitHub
  file view, `git clone`, IDE preview) sees broken Actions syntax if copied as-is — the exact channel
  this review encountered it through. This is *reproducible in the source*, whatever the rendered site does.
- ❌ **Cloud block `gh run list` FAILED (tested).** It reads as universally runnable but errors outside an
  authenticated Codespace attached to a repo with existing runs.

### 4. Forging the La(zy)TeX CV — no verdict ❓ (engine errored, 0 snippets scored)
- The engine run **exited 1 / "Reached maximum number of turns (40)"** after its Bash attempts were
  denied (`sudo -n true` and a `curl` to `conda.anaconda.org`). No dimensions, no score, **no machine
  evidence** for this quest. Treat everything I say about it as `reasoned` static reading only (see §7).

### 5. The Warden's Gate — 77% ⚠️ (ran 2/1 runnable snippets)
Dimensions (per summary): technically accurate, well-structured; safety fine.

- ✅ **YAML passed (tested)** — the `first-turn.yml` gate-job additions (read-only `permissions:` floor,
  `gate` job emitting `go`, `turn` job gated on `needs.gate.outputs.go`) and the two-line caller-permissions
  fix (`contents: write` + `pull-requests: write`) parse and the gate shell logic runs as documented.
- 🟰 **arm/disarm demo `skipped`** — `gh variable set/delete` + `gh workflow run … && gh run watch` needs a
  live authenticated GitHub repo; correctly not exercised in an isolated sandbox.
- 🟰 The `startup_failure` trap YAML + its error text + the mermaid diagram judged `reasoned` — the
  claims (caller permissions cap called-workflow jobs, `startup_failure` has no logs, `gh run
  view --log-failed` returns nothing) check out against current GitHub Actions semantics.

## 🐞 Issues Found

**High**
- **high · Docker Mastery · body (lines ~114-150 + objectives) · tested.** 5 of 6 runnable blocks are
  empty comment stubs and the promised Docker Compose / security-optimization / cloud-deploy content is
  never authored (completeness = 1). *Fix:* author real chapters/snippets (a two-service `docker-compose.yml`,
  a multi-stage Dockerfile with non-root `USER` + `HEALTHCHECK`, a concrete `docker push`/cloud-run deploy)
  or remove those claims from objectives, checklist, and rewards so the quest doesn't over-promise.
- **high · Docker Mastery · platform path stubs (lines 114-150) · tested.** Replace the placeholder blocks
  and bracketed "[Detailed instructions …]" text with actual per-OS commands, or drop the section — it
  currently ships as unfinished template output.
- **high · CI/CD Fundamentals · Chapter 2 workflow `run: npm ci` (line 297) · tested.** Verified EUSAGE
  failure — the setup never generates/commits `package-lock.json`. *Fix:* either add `npm install` to the
  setup (and commit the lockfile) before the workflow is introduced, or change the workflow to `npm install`.
- **high · GitHub Actions Basics · secrets/matrix/Mastery-Indicator/Challenge (lines 116, 291, 333, 346, 375)
  · tested.** Leaked `{% raw %}{% raw %}{% endraw %}…{% raw %}{% endraw %}{% endraw %}` tags render broken `${% raw %}{{ … }}{% endraw %}` expressions in raw markdown. *Fix:*
  correct the escaping so raw consumers see clean `${% raw %}{{ secrets.DEPLOY_TOKEN }}{% endraw %}` / `${% raw %}{{ matrix.os }}{% endraw %}` /
  `${% raw %}{{ matrix.node }}{% endraw %}`; especially important since the secrets form is a *required Mastery Indicator*.

**Medium**
- **medium · CI/CD Fundamentals · Chapter 3 `git commit -am` (lines 340-343) · tested.** Silently no-ops for
  a new file. *Fix:* replace `# … make a tiny change …` with a concrete step that either creates and
  `git add`s a file, or edits an existing tracked one.
- **medium · Warden's Gate · Chapter 1 arm/disarm bash (lines 135-139) · reasoned.** `gh workflow run
  first-turn.yml && gh run watch` — `gh workflow run` returns no run id, so `gh run watch` may pop an
  interactive picker. *Fix:* `gh run watch $(gh run list --workflow=first-turn.yml --limit=1 --json
  databaseId --jq '.[0].databaseId')`, or tell the learner to pick the top run.
- **medium · Docker Mastery · chapter depth · reasoned.** One trivial echo-only Alpine container for a
  billed 60-90 min Medium quest. *Fix:* add at least one real worked build (copy app code, install deps,
  expose a port).

**Low**
- **low · GitHub Actions Basics · Cloud block `gh run list` (line 197) · tested.** Clarify it only works in
  an authenticated Codespace attached to a repo with existing runs.
- **low · CI/CD + GitHub Actions · Knowledge Check sections · reasoned.** No answer keys anywhere; add
  collapsible model answers so learners can self-verify.
- **low · Warden's Gate · Reproduce It PR #422 (line 204) · reasoned.** External +24/−2 diff unverifiable
  offline; consider inlining the actual diff so it can't go stale.
- **low · Docker & LaTeX CV · Knowledge-Graph level-hub label · reasoned.** Both wiki-link
  `[[Level 0101 - Advanced Docker & DevOps]]`, but the level's actual theme (and the other three quests'
  hubs) is **CI/CD & DevOps**. Align the label for consistent navigation.

*No issue here is fabricated — each cites a run command result or an exact quoted source line. The LaTeX
CV quest is deliberately absent from the high/medium bug list because I have no execution evidence for it.*

## 🔗 Chain Continuity

Reading the five in plan order as one journey for a System Engineer at this level:

- **The mainline CI/CD thread is genuinely well-linked.** *CI/CD Fundamentals* → *GitHub Actions Basics*
  is a real, declared prerequisite chain (`github-actions-basics` frontmatter lists
  `required_quests: /quests/0101/cicd-fundamentals/`). Fundamentals leaves the learner with exactly the
  mental model (build-test-deploy, triggers, secrets) that Actions Basics builds on — good continuity, and
  the `${% raw %}{{ secrets.NAME }}{% endraw %}` concept even recurs across both quests reinforcing it.
- **…but the same lockfile assumption threads through both quests.** Fundamentals never creates a
  `package-lock.json`, yet *both* it (Ch2) and Actions Basics (`npm ci` in the `needs:` and matrix blocks)
  assume one exists. A learner carrying Fundamentals' scaffolded repo into Actions Basics hits the identical
  `npm ci` wall twice — a real cross-quest prerequisite gap, not just a per-quest bug.
- **Docker Mastery does not belong in this learning line as written.** It shares the level code but has no
  dependency edge to the CI/CD thread, its stated prerequisites point at Command-Line/Git quests, and its
  body is unfinished. A beginner who reaches it after Fundamentals gets no CI/CD continuity and one working
  container — it breaks the journey's momentum rather than advancing it.
- **The LaTeX CV quest is a thematic outlier.** It's a "Professional Identity Path" CV-forging quest sitting
  inside a **CI/CD & DevOps** level. For a System Engineer sweeping this level it reads as an unrelated
  detour; nothing before it sets it up and nothing after it depends on it. Its own Chapter 1 sensibly warns
  "Don't have `cv.tex` yet? Create it first from Chapter 2, then return here," so its internal ordering is
  fine — it's the *level placement* that breaks continuity.
- **Warden's Gate assumes state this window never provides.** It recommends
  `/quests/0000/ouroboros-loop-01-the-first-turn/` and requires "your `potion-book` repo from Chapter I" with
  an authenticated `gh`. None of the four earlier quests in this window builds that repo, so a learner
  arriving here cold is missing the prerequisite artifact — the engine's inability to run its one hands-on
  block is a direct symptom. It's a strong quest, but it presumes a prior campaign chapter outside the slice.

**Net:** the slice does *not* hold together as a single System-Engineer learning path. Two coherent
sub-threads exist (the CI/CD → GitHub-Actions mainline, and the Ouroboros campaign chapter) interleaved with
two off-thread quests (Docker stub, LaTeX CV), and the mainline itself carries a shared `npm ci` prerequisite
gap. A learner following the window top-to-bottom would experience it as four unrelated starts, not one arc.

## 🧠 Reasoning & Method

- **Mode:** `execute`, in the workflow's disposable sandbox. I **consumed the sealed
  `walk-evidence.json`/`.md` as-is** — I did not run, regenerate, or edit the engine (its child `claude`
  processes can't authenticate from my Bash tool), and I did not touch `walk-plan.json`. Every
  `passed`/`failed` above is an engine-run command; everything labelled `reasoned` I judged from the quest
  source, which I read in full in plan order.
- **What I ran vs. reasoned:** the engine executed real snippets for 4 of 5 quests (setup commands, npm
  scripts, Docker build/run, YAML parsing, gate shell logic). I reasoned about: all placeholder/empty blocks,
  network/remote-dependent steps (`git push`, `gh run watch`, `gh run list`), the caller-permissions/
  startup_failure YAML, and the level-hub label inconsistency.
- **Coverage gaps I'm being honest about:**
  - **LaTeX CV quest has ZERO execution evidence** — the engine hit the 40-turn cap after `sudo`/network
    installs (`texlive-full`, conda) were denied. I did not fabricate a score for it; its journey/§4 lines are
    static reading only. Its self-contained Chapter 2 `cv.tex` (base packages + locally-defined
    `\resumeSubheading`/`\resumeItem`) *looks* like it would compile with a stock TeX Live, but that is
    **unverified**.
  - Snippet coverage per the sealed table: CI/CD 5/5 (2✗), Docker 3/6, GitHub Actions 8/4 (3✗),
    LaTeX —, Warden's Gate 2/1.
  - This is **window 1 of 3** — I walked 5 of the level's 13 quests. I did not expand beyond the planned
    window; the remaining 8 quests are for later runs and the ledger accumulates coverage across them.
  - No destructive commands, no host-repo mutation, no network beyond what a quest's own safe setup needed.
- **Confidence:** High on the four scored verdicts and their cited command outcomes; the two high-severity
  content bugs (`npm ci` lockfile, Docker scaffolding) are directly reproduced. Low/none on the LaTeX quest —
  flagged as unwalked. Overall slice verdict **`fail`** reflects two failing quests plus a blocking first-quest
  bug in an otherwise conceptually sound level.

---

<details><summary>Sealed machine evidence (quoted from <code>walk-evidence.md</code>)</summary>

> **4** quests evaluated · ✅ 0 pass · ⚠️ 3 warn · ❌ 2 fail · avg **67.2%** · ~$2.284
>
> - ⚠️ 76 — CI/CD Fundamentals — 5/5 (2✗)
> - ❌ 48 — Docker Containerization Mastery — 3/6
> - ⚠️ 68 — GitHub Actions Basics — 8/4 (3✗)
> - ❌ — — Forging the La(zy)TeX CV — engine exited 1: "Reached maximum number of turns (40)"
> - ⚠️ 77 — The Warden's Gate — 2/1

</details>
