---
title: "Quest Walkthrough — System Engineer · Level 1000 (Cloud Computing)"
date: 2026-07-12T00:00:00.000Z
character: system-engineer
level: "1000"
theme: Cloud Computing
tier: Warrior
quest_count: 4
mode: execute
overall_verdict: warn
session:
  slice: system-engineer/1000
  window: "2 of 2 (offset 5, size 5)"
  total_quests_in_level: 9
  engine_average: 76.3
  engine_counts: { pass: 1, warn: 2, fail: 1 }
  engine_cost_usd: 2.7512
  evidence_source: walk-evidence.json (sealed by workflow; execute mode)
  note: >-
    One quest (Azure Ascension) has NO machine score — the execute engine
    exited 1 after hitting max_turns (40). Treated as no-evidence/tooling
    error, not a content failure. Reasoned about statically only.
---

## 🎯 Session Summary

I walked the **System Engineer** path through **Level 1000 (Cloud Computing,
Warrior tier 🔥)** — the second and final window of the level (4 of the level's 9
quests; the planner already swept window 1). This window is the level's **cloud
provisioning arc plus one detour**: `AWS Essentials` → `Infrastructure as Code`
form a tight linear pair, `Azure Ascension` is a side-branch alternate-cloud
deploy, and `The War Machine` is Chapter III of an unrelated automation campaign
that happens to live at this level.

**Headline verdict: ⚠️ warn.** The engine scored 3 of 4 quests (avg **76.3%**:
1 pass, 2 warn) and **errored** on the 4th (Azure) at max_turns, so that one has
no evidence. The two provisioning quests are technically sound — every AWS CLI and
Terraform snippet parsed and executed correctly in the sandbox, failing only at the
expected "no credentials" stage — but both carry **learner-blocking gaps a real
beginner would hit**: AWS Essentials teaches the SSH-enabling security group *after*
the EC2 launch that needs it (so the Intermediate Challenge's "SSH in" is
impossible as written), and The War Machine's own Mastery Challenge headline ("two
parallel runs claim two different tasks") is **not achievable with the shipped
code**. Terraform is the standout (89%, pass). A maintainer should prioritise the
two `high`-severity issues below.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ⚠️ warn | AWS Essentials: Core Services and Architecture | 72 | CLI syntax all correct, but EC2 launch never attaches the SSH security group taught a chapter later — Intermediate Challenge is unreachable as written. |
| 2 | ❌ no-evidence | Azure Ascension: Deploying Jekyll to the Cloud Kingdom | — | Engine errored (exited 1 at max_turns=40); **no machine score**. Reasoned statically: structurally the thinnest quest in the slice and leans entirely on a repo-specific deploy script + live Azure account. |
| 3 | ✅ pass | Infrastructure as Code: Terraform Fundamentals and State | 89 | Full init/plan/apply/destroy/idempotency lifecycle verified verbatim via Docker + a local-provider stand-in; only a deprecated backend param and two small clarity gaps. |
| 4 | ⚠️ warn | The War Machine: Dispatch, Leasing, and a Fifty-Case Simulation | 68 | Git-ref CAS leasing genuinely works end-to-end, but two of the three Mastery-Challenge claims don't hold with the shipped code, and the scripts don't run without an undocumented `chmod +x`. |

## 🔬 Evidence

All evidence below comes from `walk-evidence.json` (execute mode, sealed by the
workflow — the engine ran each quest's safe commands in a disposable sandbox).
Where I only reasoned from the quest source rather than a run, I label it
`reasoned`.

### 1. AWS Essentials — 72% ⚠️ (ran 2/8 runnable snippets: 1 passed, 1 failed, 8 skipped)
- **passed** · IAM least-privilege policy JSON — validated with `python3 -c "json.loads(...)"`; parses with correct `Version`/`Statement`/`Effect`/`Action`/`Resource`.
- **failed** · `aws sts get-caller-identity` (CloudShell block) — ran directly: `aws: [ERROR]: An error occurred (NoCredentials): Unable to locate credentials.` Expected off-CloudShell; syntax is correct.
- **skipped (syntax-verified)** · every `aws iam …`, `aws ec2 create-key-pair/run-instances/terminate-instances`, `aws s3 mb/cp/rb`, `aws s3api put-public-access-block` was executed against AWS CLI **v2.35.15** and failed **only** with `NoCredentials`/`NoRegion` — no parsing/usage errors. The `resolve:ssm:/aws/service/ami-amazon-linux-latest/...` AMI alias and the `BlockPublicAcls=true,...` shorthand both parsed cleanly.
- **skipped** · Local shell mechanics ran for real and worked: `BUCKET=my-quest-bucket-$RANDOM` → `my-quest-bucket-5138`, `echo "treasure" > loot.txt`, `chmod 400 quest-key.pem` → `-r--------`.
- **skipped** · OS install blocks (brew/winget/curl+sudo) — not runnable in the Linux sandbox; the curl download was network-denied and `sudo` is out of policy. Correctly skipped, not forced.
- **Key finding (tracing execution order):** `aws ec2 run-instances` in Chapter 2 has **no `--security-group-ids`**, so the instance lands in the VPC default SG (no inbound SSH). The SSH-allowing SG is only created in Chapter 3 and never wired back. Safety messaging (repeated "ALWAYS terminate", block-public-access, MFA on root) scored a perfect **5**.

### 2. Azure Ascension — NO SCORE ❌ (engine errored)
- The engine child process **exited 1 after reaching `max_turns` (40)**; `terminal_reason: max_turns`, `errors: ["Reached maximum number of turns (40)"]`. There is **no per-dimension score, no verdict, and no snippet coverage** for this quest.
- The only sandbox signal is a `permission_denials` entry: the engine tried `which jq curl; jq --version; curl --version | head -1` and Bash was denied — a **sandbox limitation**, not a quest defect.
- **I did not run this quest's commands.** Everything in §5/§6 about Azure is `reasoned` from the source only.

### 3. Infrastructure as Code — 89% ✅ (ran 7/6 runnable snippets: 7 passed, 0 failed, 2 reasoned, 3 skipped)
- **passed** · `docker run --rm ... hashicorp/terraform:latest version` → `Terraform v1.15.8 ... + provider ... aws v5.100.0`, matching the quest's "expect Terraform v1.x".
- **passed** · Chapter 1 `main.tf` (aws provider + `aws_s3_bucket`) — `terraform init` pulled `hashicorp/aws v5.100.0` (satisfies `~> 5.0`); `terraform validate` → `Success! The configuration is valid.`
- **passed** · `data "aws_ami" "al2023"` block — init + validate both succeeded.
- **reasoned** · init/plan/apply/destroy lifecycle — `plan`/`apply` against the real aws provider failed with `No valid credential sources found` (expected; quest needs a live account). **Functionally reproduced end-to-end with a credential-free `hashicorp/local` provider:** `Plan: 1 to add, 0 to change, 0 to destroy.`, a 2nd apply → `No changes...` / `0 added, 0 changed, 0 destroyed.`, `destroy` → `Destroy complete! Resources: 1 destroyed.` — all text matches the quest verbatim.
- **passed** · S3 remote backend block — `validate` succeeded, but `init` surfaced a **real deprecation warning**: `dynamodb_table` is deprecated in favour of `use_lockfile` in Terraform v1.15.8.
- **passed** · variables.tf/outputs.tf (Chapter 3) — syntax correct; note the shown `main.tf` excerpt never wires `var.region` into the provider block.

### 4. The War Machine — 68% ⚠️ (ran 13/7 runnable snippets: 10 passed, 3 failed, 1 reasoned)
- **passed** · Toolchain: Python 3.12.13, git 2.54.0, `pip install ruff pytest` (ruff 0.15.21, pytest 9.1.1).
- **passed** · `decide_core.py` + `build_backlog.py | decide.py` → printed `add-meta-description-home` (correct RICE ranking, 855 vs 144).
- **passed** · `dispatch.sh` end-to-end against a local bare `origin` — selected task, leased it via real git-push CAS, handed to `work.sh`; lease ref deleted on EXIT (confirmed via `git for-each-ref`).
- **passed** · `lease.sh` create-only CAS — two racer pushes to the same new ref: first `[new reference]`, second `! [rejected] ... stale info`. Exactly one winner, one clean stand-down.
- **passed** · `ruff check scripts/` → `All checks passed!`; `war-machine.yml` is valid YAML with a correct `needs:` graph.
- **failed** · Mastery Challenge "two parallel runs claim two different task ids" — pre-leasing the top-RICE task then re-running `dispatch.sh` just logs `already leased ... standing down`; it **never falls through** to the next task, because `decide.py` hardcodes `in_flight=set()` and `lease.sh` has no retry-on-loss.
- **failed** · Mastery Challenge "remove the atomic check to prove teeth" — de-indenting `with lock:` and running the test **30×: 30/30 passed** (CPython's GIL doesn't interleave the tiny window). Only reproduced a collision after inserting an artificial `time.sleep()` the quest never mentions.
- **failed** · `exec scripts/lease.sh` handoff — without a `chmod +x` (never mentioned), `bash scripts/dispatch.sh` fails `Permission denied` (exit 126), verified directly.
- **reasoned** · Mermaid quest-network diagram — mermaid-cli absent; statically valid `graph LR`.

## 🐞 Issues Found

Grouped by quest; every item is backed by a sandbox run (`tested`) or a quoted line
from the source (`reasoned`). Severity follows the recommendations in the sealed
evidence.

**AWS Essentials** (`pages/_quests/1000/aws-essentials.md`)
- **high** · Chapter 2 EC2 launch / Intermediate Challenge · `tested`+`reasoned` — `aws ec2 run-instances` (lines 292–297) has no `--security-group-ids`; the SG that opens SSH is created in Chapter 3 (lines 367–373) and never referenced back. A learner following top-to-bottom then attempting the Intermediate Challenge ("SSH in, run `uname -a`", line 409) is locked out. **Fix:** add `--security-group-ids <sg-id>` to the launch (or move SG creation before Ch2) and show the actual `ssh -i quest-key.pem ec2-user@<ip>` + how to fetch the public IP via `describe-instances --query`.
- **medium** · Advanced Challenge / VPC chapter · `reasoned` — the challenge (lines 414–423) requires "one public and one private subnet in different AZs" plus route tables/gateways, but the tutorial only shows `create-vpc`/`create-security-group`/`authorize-security-group-ingress` — no subnet/route-table/IGW commands. **Fix:** provide the CLI commands or state explicitly that they are a research exercise.
- **medium** · Secondary Objective "Configure profiles" · `reasoned` — listed (line 107) but `aws configure --profile <name>` is never demonstrated; only single-profile `aws configure`. **Fix:** add a one-line `aws configure --profile quest` example.
- **low** · EC2 termination validation · `reasoned` — Intermediate Challenge says "Confirm via `aws ec2 describe-instances` that it is terminated" (line 410) but no `describe-instances` example appears. **Fix:** show `aws ec2 describe-instances --instance-ids <id> --query 'Reservations[].Instances[].State.Name'`.
- **low** · Free-Tier framing · `reasoned` — "the Free Tier covers everything in this quest" / "`t3.micro` ... Free-Tier eligible" (lines 34, 283) may no longer hold uniformly after AWS's 2025 credit-based Free-Tier restructuring (today is 2026-07-12). **Fix:** add a note pointing at the current Free Tier terms.

**Azure Ascension** (`pages/_quests/1000/azure-ascension-jekyll-deployment.md`) — *no machine evidence; all `reasoned`*
- **info / not-a-content-issue** · Engine · the execute engine **exited 1 at max_turns (40)** with no score. This is a tooling/timeout outcome, **not** a judged quest failure. I could not gather sandbox evidence for this quest this session.
- **low** · Structure/completeness · `reasoned` — compared to the other three quests, this one is markedly thinner: no `rewards`/`quest_dependencies` frontmatter, no per-chapter "Skills You'll Forge", no Knowledge Checks, and no tiered Mastery Challenges. It reads more like a runbook than a platform quest. **Fix:** consider aligning it with the level's quest template for consistency (a maintainer/content pass should confirm).
- **low** · Related-Quests links · `reasoned` — lines 122–124 use relative `.md` paths (`../0001/github-pages-portal.md`) rather than permalinks like the rest of the curriculum. **Fix:** verify these resolve on the rendered site or convert to permalinks. *(Flagged for a content pass — not verified by a link check this session.)*
- *Note:* the repo-relative helper `scripts/deployment/azure-jekyll-deploy.sh` that Chapter 2 depends on **does exist** (37 KB, executable) — so this is not a missing-script defect; the quest's real friction is that it needs a live Azure account, `az login`, Ruby ≥3.2, and outbound network, none of which the sandbox provides.

**Infrastructure as Code** (`pages/_quests/1000/infrastructure-as-code.md`)
- **medium** · Chapter 2 remote backend · `tested` — `terraform init` on the `backend "s3"` block (lines 320–328) emits a real deprecation warning: `dynamodb_table` is deprecated in favour of `use_lockfile` (Terraform v1.15.8). **Fix:** update the example to `use_lockfile` (or note the deprecation).
- **low** · Chapter 3 unused variable · `tested`/`reasoned` — `variable "region"` (lines 367–372) is declared but the shown `main.tf`/`provider` excerpt never consumes it, so a learner copying the snippet gets an unused variable. **Fix:** wire `var.region` into the provider block or drop the variable from the excerpt.
- **low** · Chapter 1 bucket uniqueness · `reasoned` — the Ch1 `main.tf` hardcodes `bucket = "iac-quest-bucket-change-me-12345"` (line 237), which will collide globally; the `$RANDOM` pattern only appears later in Ch3. **Fix:** mention global-uniqueness at first use, as AWS Essentials already does for S3.

**The War Machine** (`pages/_quests/1000/self-operating-website-03-the-war-machine.md`)
- **high** · Mastery Challenge / `decide.py` `in_flight` · `tested` — the headline claim "Two parallel dispatch runs claim **different** work items" (line 88, 372) is not achievable as shipped: `decide.py` hardcodes `in_flight=set()` (line 182) and `lease.sh` has no retry-on-loss, so a losing runner claims **nothing**. **Fix:** fetch real open lease refs (`git ls-remote origin 'refs/leases/*'`) into `in_flight` and add a retry loop, or soften the claim to say only the *simulation* produces two different ids.
- **high** · Mastery Challenge / "remove the atomic check" · `tested` — de-indenting `with lock:` (lines 290–298) passed 30/30 under CPython's GIL; the "prove the test has teeth" step doesn't reliably fail as instructed. **Fix:** tell learners to insert a small `time.sleep()` / `os.sched_yield()` in the check-then-act gap (or run far more repetitions) so the collision is actually observable.
- **medium** · CI YAML / `tests/unit` · `tested` — `pytest tests/unit -q` (line 338) references a directory the quest never populates; it fails `file or directory not found: tests/unit`. **Fix:** ship an actual `tests/unit/test_decide_core.py` covering `rice_score`/`decide()`.
- **medium** · Script executability · `tested` — `dispatch.sh`/`lease.sh` use `exec scripts/lease.sh` / `exec scripts/work.sh`; without `chmod +x` (never mentioned) they fail `Permission denied` (exit 126). **Fix:** add a `chmod +x scripts/*.sh` step or note.
- **low** · 50-case simulation snippet · `tested` — copy-pasted literally the block raises `NameError`; it needs `from decide_core import Task, decide` prepended. **Fix:** add the import to the snippet so it runs standalone.

*No quest in this slice was clean of blocking issues, but the two `pass`/near-pass
quests (Terraform, AWS Essentials) are close — their fixes are small and local.*

## 🔗 Chain Continuity

Reasoning about the slice as one learner's path through the System Engineer's
Level 1000:

- **AWS Essentials → Infrastructure as Code is a genuinely strong link.** IaC's
  frontmatter declares `required_quests: [/quests/1000/aws-essentials/]`, and its
  opening line ("In the previous quest you clicked and typed your way through the
  AWS console...") explicitly picks up where AWS Essentials leaves off. Concepts
  carry cleanly: the S3 bucket, the `aws_ami`/Amazon Linux 2023 data source, and
  `aws sts get-caller-identity` all reappear in Terraform form. A learner finishing
  quest 1 is genuinely ready for quest 3. **This pair is the spine of the slice.**
- **Azure Ascension is a side-branch, not a rung.** It's an alternate-cloud
  (Azure Static Web Apps) deploy of the Jekyll site; nothing in AWS Essentials sets
  it up, and IaC doesn't depend on it. Walked in plan order (position 2) it reads as
  a detour between the two AWS quests. That's defensible (AWS Essentials itself lists
  Azure under "Explore Side Adventures"), but a learner should be told it's optional
  and orthogonal, not the next step after AWS.
- **The War Machine is a hard context switch.** It belongs to a *different campaign*
  (The Self-Operating Website / The Autonomous Realm), is **Chapter III**, and its
  prerequisites lean on **Chapter II — The Proving Grounds (a Level 0100 quest not in
  this slice)**: "You need its self-survey worklist ... because that ledger *is* the
  backlog this dispatcher observes." Its `quest_dependencies.required_quests` is
  empty, but the prose assumes Ch II's artifacts. For a learner arriving straight
  from Terraform, this is a jarring jump into GitHub-Actions/agent-fleet territory
  with an unstated cross-level prerequisite. **Ordering note:** it is correctly
  last, but the slice would read better if the level hub signposted it as a separate
  arc rather than the fourth cloud quest.
- **Net:** this window is not one linear journey — it's *the cloud-provisioning arc
  (AWS → Terraform) + an Azure side-branch + one chapter of an automation campaign*,
  bundled by level code. That's an acceptable level-hub composition, but a beginner
  would benefit from an explicit "these are three tracks, not four steps" cue.
- **Prerequisite satisfaction within the slice:** ✅ IaC's prerequisite (AWS
  Essentials) is present and precedes it. ⚠️ AWS Essentials' own prerequisite
  (Cloud Computing Fundamentals) sits in window 1, not here — expected under
  windowing. ⚠️ War Machine's real prerequisite (Proving Grounds, L0100) is
  out-of-slice and cross-level. Azure has no in-slice prerequisites but needs a live
  Azure account + `az login` + Ruby ≥3.2.

## 🧠 Reasoning & Method

- **Mode:** `execute` — the workflow pre-computed and **sealed** `walk-evidence.json`
  by running `test/quest-validator/agentic_validate.py --mode execute` in the
  disposable runner sandbox. I consumed that evidence as-is; I did **not** re-run the
  engine (its child `claude` processes can't authenticate from my Bash tool), and I
  did not edit `walk-plan.json` or `walk-evidence.*`.
- **What I ran vs. reasoned:** the *engine* ran the commands (AWS CLI v2.35.15,
  Terraform v1.15.8 via Docker with a local-provider stand-in, and the War Machine's
  Python/bash/git scripts against a local bare repo). I independently **read all four
  quest sources in plan order** and cross-checked the engine's findings against the
  actual lines, then reasoned about the linked journey (§6). Every issue is labelled
  `tested` (sandbox run) or `reasoned` (quoted source). I additionally verified on
  the host filesystem that the Azure quest's referenced deploy script exists.
- **Coverage & limits (honest):**
  - **Azure Ascension has NO machine score** — the engine exited 1 at max_turns(40).
    I report it as no-evidence/tooling-error and only reasoned statically; I did not
    fabricate a score or verdict for it. This is the single biggest coverage gap of
    the session.
  - Cloud provisioning could not be exercised for real (no AWS/Azure credentials,
    outbound network denied, `sudo` out of policy). AWS and Terraform commands were
    therefore **syntax/parse-verified** (they reached the expected `NoCredentials`
    stage) and, for Terraform, **functionally reproduced** with a credential-free
    local provider. This is strong evidence for correctness of syntax and lifecycle,
    but does **not** prove a live provision succeeds end-to-end.
  - Snippet coverage per quest: AWS 2/8 runnable ran; IaC 7/6 ran (some run more than
    once across substitutes); War Machine 13/7 ran; Azure 0 (errored).
  - No link-checking or rendered-site validation was performed; the Azure
    relative-link note is flagged for a content pass, not verified here.
- **Confidence:** High on Terraform (pass, reproduced verbatim) and on the two
  `high` War Machine findings (directly reproduced). High on the AWS security-group
  ordering gap (engine-traced + confirmed against source lines). **None** on Azure
  (no evidence). Medium on the Azure structural observations (source-only).
- **Scope discipline:** one slice, one report. No quest content was modified; no
  branch/commit/PR was made. Fixable bugs live in §5 for a content pass to act on.
