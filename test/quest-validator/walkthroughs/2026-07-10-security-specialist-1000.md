---
title: 'Quest Walkthrough — Security Specialist · Level 1000 (Cloud Computing)'
date: '2026-07-10T00:00:00.000Z'
character: security-specialist
level: '1000'
theme: Cloud Computing
tier: Warrior
quest_count: 4
mode: execute
overall_verdict: warn
session:
  window: 2 of 2 (offset 5, size 5) of a 9-quest level
  scored: 3 of 4 (1 quest un-scored — engine hit max_turns)
  counts: { pass: 2, warn: 1, fail: 1 }
  average_scored: 85.0
  engine_cost_usd: 2.3822
  evidence_source: ./walk-evidence.json (sealed by workflow, consumed as-is)
---

## 🎯 Session Summary

I walked the second window (4 quests) of the **Security Specialist → Level 1000 (Cloud Computing / Warrior 🔥)** slice as a learner, driving the sealed agentic **execute-mode** evidence and then reading each quest's source in plan order to reason about the linked journey. The technical core of this slice is strong: the **Infrastructure as Code** (87, pass) and **The War Machine** (97, pass) quests were *executed for real* in the sandbox and every documented command/output matched; **AWS Essentials** (71, warn) is technically sound but incomplete on its own cleanup promise; **Azure Ascension** could **not be scored** — the engine reached its 40-turn ceiling while probing the deploy script, so it is recorded as a `fail` (0) that is really an *unscored* result, not a proven content defect.

The headline for a maintainer: **the slice is two strong linked cloud quests plus two topical orphans.** AWS Essentials → Infrastructure as Code is a genuine, dependency-honest chain. Azure Ascension and The War Machine belong to *different series* and depend on quests **outside this window**, so as a single learning path the slice does not hold together — it is grouped by level theme, not by arc. I set the overall verdict to **warn** because one quest is unscored and one warns.

## 🗺️ The Journey

Walked in planner order (dependency-sorted within the level window):

1. ⚠️ **AWS Essentials: Core Services and Architecture** — **71** · Solid CLI/IAM/EC2/S3/VPC teaching; live-account commands fail only for lack of credentials (honest), but the quest breaks its own "cast then dispel" promise (no VPC/SG/IAM teardown).
2. ❌ **Azure Ascension: Deploying Jekyll to the Cloud Kingdom** — **— (unscored)** · Engine hit `max_turns` (40) while trying to get `azure-jekyll-deploy.sh --help` to emit output; no dimension scores produced. Recorded as fail; treat as *no verdict*, corroborated by a reasoned script issue below.
3. ✅ **Infrastructure as Code: Terraform Fundamentals and State** — **87** · Full `init→plan→apply→plan(idempotent)→destroy` lifecycle ran for real against a LocalStack backend; literal plan/"No changes" output matched exactly. Minor currency nits only.
4. ✅ **The War Machine: Dispatch, Leasing, and a Fifty-Case Simulation** — **97** · Every runnable snippet (decision core, dispatcher, git-ref CAS leasing, 50-case sim, a real two-runner race) executed as documented. One missing `tests/unit` example.

## 🔬 Evidence

All numbers below come from `./walk-evidence.json` (execute mode, `mock: false`), which the workflow pre-computed and sealed; I consumed it as-is and did not re-run the engine. Per-dimension scores are on a 1–5 scale.

### 1. AWS Essentials — ⚠️ 71 · execute · 12 turns · $0.54
- **Snippets:** ran **2 / 8** runnable (1 passed, 1 failed), 6 skipped, 2 reasoned (10 recorded total).
- **Dimensions:** commands_work 3 · content_accuracy 4 · completeness 3 · clarity 4 · structure 4 · safety 4. Weight covered 1.0.
- **What the engine witnessed:** CLI syntax, the JSON IAM policy, SSM AMI
resolution, and the S3/IAM/EC2/VPC command forms all check out; the failed/skipped commands fail *legitimately* because they need a live, credentialed AWS account, which the quest is explicit about. Deductions are for its own incomplete create-then-delete promise and a Windows gap in the key-pair permission step.

### 2. Azure Ascension — ❌ unscored · execute · engine error
- **Snippets:** none recorded. `weight_covered: null`. No per-dimension scores.
- **Engine error (verbatim, trimmed):** `claude exited 1: … "command":"… export
LOG_DIR=/tmp/quest-qa-…/logs; ./scripts/deployment/azure-jekyll-deploy.sh --help … EXIT: $?; … bash -x ./scripts/deployment/azure-jekyll-deploy.sh --help …"` → `"errors":["Reached maximum number of turns (40)"]`.
- **Reading:** the engine burned its whole turn budget trying to make the deploy
script's `--help` produce output (repeated `export LOG_DIR=/tmp/…` + `bash -x` tracing). This is a **coverage limitation**, not a scored content verdict. See the reasoned script issue in §Issues that explains *why* `--help` misbehaves.

### 3. Infrastructure as Code — ✅ 87 · execute · 41 turns · $1.08
- **Snippets:** ran **9** (8 passed, 1 failed), 1 skipped, 2 reasoned; 6 runnable / 12 recorded.
- **Dimensions:** commands_work 5 · content_accuracy 4 · completeness 4 · clarity 4 · structure 5 · safety 4. Weight covered 1.0.
- **What the engine witnessed:** the entire Terraform lifecycle ran against a
LocalStack-emulated AWS backend using the quest's exact HCL, and the documented output — including the literal `Plan: 1 to add, 0 to change, 0 to destroy.` and `No changes` — matched exactly. The single failed snippet lines up with the reasoned `docker -it` "input device is not a TTY" note (see §Issues). This is the most verifiable quest in the slice.

### 4. The War Machine — ✅ 97 · execute · 23 turns · $0.76
- **Snippets:** ran **7 / 7** (7 passed, 0 failed), 2 reasoned; 9 recorded.
- **Dimensions:** commands_work 5 · content_accuracy 5 · completeness 4 · clarity 5 · structure 5 · safety 5. Weight covered 1.0.
- **What the engine witnessed:** the Python decision core, backlog builder,
dispatcher, git-ref CAS leasing, work release, and the 50-case simulation all ran as documented against a real local git remote — including a genuine two-runner race that produced exactly one winner and one clean loser. Strong, direct evidence the core claims are accurate.

## 🐞 Issues Found

Severity · quest · where · observed · suggested fix. Items marked **reasoned** were judged from the quest/script source, not run; items marked **tested** cite a command the sealed engine actually executed.

- **HIGH** · AWS Essentials · *Chapter 3 VPC section* · **reasoned** — The quest
promises "every spell you cast, you will also dispel," but there is teardown for EC2 and S3 while the VPC and security group have none. A learner following it on a live account leaves billable/blocking resources behind. *Fix:* add explicit `aws ec2 delete-security-group` / `aws ec2 delete-vpc` steps mirroring the EC2/S3 teardown pattern.
- **HIGH** · Azure Ascension · *`scripts/deployment/azure-jekyll-deploy.sh` `main()`*
· **reasoned** — `main()` calls `safe_mkdir "$(dirname "${LOG_FILE}")"` (line ~1313) **before** `parse_args "$@"` (line ~1319), and `LOG_FILE` defaults to `/var/log/azure-jekyll-deploy/…` (lines 50–51). So even `--help` first tries to `mkdir -p /var/log/azure-jekyll-deploy`, which a non-root learner cannot create — this is almost certainly why the engine could not get `--help` to emit usage and spun to `max_turns`. *Fix:* handle `-h/--help`/`-v` before any logging setup, or default `LOG_DIR` to a user-writable path (e.g. `${TMPDIR:-/tmp}` or `$HOME/.cache`).
- **MEDIUM** · AWS Essentials · *Chapter 3 security-group ingress* · **reasoned** —
The `authorize-security-group-ingress` step uses a `<your-ip>` placeholder with no way to discover it, and doesn't capture `<vpc-id>`/`<sg-id>` into shell variables the way the S3 section captures `$BUCKET`. *Fix:* show `curl -s https://checkip.amazonaws.com` and variable capture.
- **MEDIUM** · AWS Essentials · *EC2 key-pair permissions* · **reasoned** — The
private-key step is Unix-only (`chmod 400`) though the quest advertises a Windows setup path. *Fix:* add the `icacls` equivalent for Windows.
- **MEDIUM** · AWS Essentials · *Chapter 1 IAM section* · **reasoned** — IAM
user/group/policy created for the exercise are never cleaned up. *Fix:* add optional teardown or explicitly note they're free to leave and why.
- **MEDIUM** · Infrastructure as Code · *Chapter 2 remote-backend snippet* ·
**reasoned** — The S3 backend example uses `dynamodb_table`, which current Terraform deprecates. *Fix:* use `use_lockfile = true` (native S3 locking, GA since TF 1.10).
- **MEDIUM** · Infrastructure as Code · *Chapter 3 variables.tf / main.tf* ·
**reasoned** — The `region` variable is declared but never wired into the provider block, so a learner copying literally gets a dead variable that undercuts the "parameterize a configuration" objective. *Fix:* wire `region = var.region` into the provider, or drop the variable.
- **MEDIUM** · The War Machine · *Chapter 2 CI workflow / `tests/unit`* · **reasoned**
— The workflow runs `pytest tests/unit -q` but the quest only ever shows `tests/sim/test_dispatch_sim.py`; a learner copying the pipeline hits an empty/missing `tests/unit`. *Fix:* add a short example unit test for `decide()`/`rice_score()`.
- **LOW** · Infrastructure as Code · *Cloud Realms Docker snippet* · **tested** — A
snippet failed in the sandbox; the engine's note attributes it to `docker … -it` emitting "the input device is not a TTY" in a non-interactive context. *Fix:* drop `-it` from the shown command (or note it's interactive-only).
- **LOW** · Infrastructure as Code · *Providers version constraint* · **reasoned** —
Pins `~> 5.0` while AWS provider v6.x is the current major. *Fix:* bump to `~> 6.0` or explain the deliberate pin.
- **LOW** · The War Machine · *`lease.sh` nonce* · **reasoned** — `date +%s%N` needs
GNU date; on BSD/macOS it yields a literal `N`. Fine on the documented `ubuntu-latest` runners; worth a one-line note for local macOS learners.
- **LOW** · The War Machine · *Reproduce It section* · **reasoned** — Three linked
lifehacker.dev commits could not be verified (no network browsing in sandbox); worth a maintainer link-check.
- **LOW** · AWS Essentials & War Machine · *Knowledge Check sections* · **reasoned**
— Conceptual questions have no in-quest answer key/self-check. *Fix:* add collapsible answers or doc links.
- **LOW** · AWS Essentials · *System Requirements / Free Tier* · **reasoned** — Does
not mention AWS's 2025 Free Tier restructuring (credit-based Free Plan vs. legacy 12-month always-free hours). *Fix:* add a note so newer accounts aren't surprised.

**No blocking content defect was *proven* by an executed command.** The AWS and Azure gaps are teardown/portability/harness issues, not broken instructions; the two executed quests (IaC, War Machine) ran clean end-to-end.

## 🔗 Chain Continuity

This window is **2 of 2** (offset 5) of a 9-quest level, so it is the tail of the Cloud Computing tier rather than a self-contained arc. Reading the four in order as a learner:

- **AWS Essentials → Infrastructure as Code is a genuine, dependency-honest chain.**
AWS Essentials' frontmatter `unlocks_quests` lists `/quests/1000/infrastructure-as-code/`, and IaC's `required_quests` lists `/quests/1000/aws-essentials/`. The pedagogy matches the metadata: the learner hand-provisions EC2/S3/VPC in AWS Essentials, then automates exactly that class of resource declaratively in IaC. A learner finishing quest 1 is genuinely *ready* for quest 3. This pair is the spine of the slice.
- **Azure Ascension is an orphan in this ordering.** It has **no `quest_dependencies`
block at all**, belongs to a different series ("Cloud Deployment Quests"), and its prerequisites point back to level-0001 Jekyll/GitHub-Pages work — not to the surrounding AWS/Terraform quests. A learner arriving from AWS Essentials finds no shared state, a different cloud, and a different toolchain (Azure CLI + a repo deploy script). It sits here because it shares the *Cloud Computing theme*, not because it continues the journey.
- **The War Machine is a second orphan, from a third series.** It is part of "The
Self-Operating Website" campaign; its real prerequisite is *Chapter II — The Proving Grounds* at level **0100** (`recommended_quests: /quests/0100/self-operating-website-02-the-proving-grounds/`), and it teaches GitHub-Actions work-orchestration — unrelated to cloud provisioning. Excellent in isolation (97), but it does not build on the three cloud quests before it.

**Net:** the planner windows by *level*, and this level bundles three distinct arcs (AWS Citadel, Azure deployment, Self-Operating Website) under one Cloud Computing banner. For the **Security Specialist** specifically, note that none of the four quests is security-focused — they are generic cloud/DevOps `main_quest`s shared across character paths, which is reasonable as *foundation* for a Warrior-tier security learner but worth flagging: a security specialist reaching level 1000 gets cloud fundamentals, not threat/hardening content, in this window.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sandboxed, `mock: false`), consumed from the workflow-sealed
`./walk-evidence.json` / `./walk-evidence.md`. Per the skill's step 2, I did **not** re-run the agentic engine (its child `claude` processes cannot authenticate from my Bash tool) and did **not** modify the plan or evidence files.
- **What I ran vs. reasoned:** I ran only *read-only inspection* commands on the host
to substantiate reasoned issues — reading the four quest sources and the `azure-jekyll-deploy.sh` script (confirming `main()` orders `safe_mkdir` before `parse_args` and that `LOG_FILE` defaults under `/var/log`). All `passed`/`failed` snippet outcomes in §Evidence are the sandbox engine's, not mine. Everything I derived from source is labeled **reasoned**; the one `docker -it` failure is labeled **tested** because the engine executed it.
- **Coverage & limits:**
  - AWS Essentials ran **2/8** runnable snippets — the rest legitimately need live
    AWS credentials the sandbox intentionally lacks, so completeness/teardown gaps
    are **reasoned**, not executed.
  - **Azure Ascension is unscored** — the engine hit `max_turns` (40) and produced no
    dimension scores or snippet coverage. I did **not** substitute a number; it is
    reported as a coverage gap plus one corroborating reasoned script issue. It needs
    a re-run (ideally with the deploy-script log path made user-writable, or the
    engine turn budget raised) before it can be scored.
  - IaC (9 ran) and War Machine (7/7) are the well-evidenced quests; my confidence in
    their pass verdicts is **high**.
- **Confidence:** High on the two executed passes; medium on the AWS warn (sound but
provably incomplete on teardown); the Azure fail is **not** a content judgment — confidence that it's a *harness/log-path* problem rather than broken content is medium, based on the script source I read.
- **Scope discipline:** one slice, one report. No quest content edited, no branch,
  commit, push, or merge — the workflow handles git. Read-only over all content.
