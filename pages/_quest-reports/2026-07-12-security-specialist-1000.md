---
title: Security Specialist · L1000 · 2026-07-12
description: Quest-perfection walkthrough of the Cloud Computing slice security-specialist/1000 on 2026-07-12,
  engine verdict warn (avg 74.0%). An evidence-based…
date: '2026-07-12T00:00:00.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Security Specialist
tags:
- security-specialist
- level-1000
- walkthrough
- quest-perfection
- warn
- cloud-computing
render_with_liquid: false
excerpt: 'Security Specialist · Level 1000 — Cloud Computing: an evidence-based quest-perfection walkthrough
  from 2026-07-12.'
slice: security-specialist/1000
character: security-specialist
level: '1000'
theme: Cloud Computing
tier: Warrior
verdict: warn
quest_count: 4
engine_average: 74.0
walk_date: '2026-07-12'
run_url: https://github.com/bamr87/it-journey/actions/runs/29190829265
source_report: test/quest-validator/walkthroughs/2026-07-12-security-specialist-1000.md
---

> **Slice** `security-specialist/1000` · **Level** 1000 (Cloud Computing) · **Warrior tier** · **Engine verdict** ⚠️ warn (avg 74.0%) · **Walked** 2026-07-12
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29190829265) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-12-security-specialist-1000.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-12-security-specialist-1000.md)

---

## 🎯 Session Summary

I walked the **Security Specialist** path through **Level 1000 — Cloud Computing (Warrior 🔥)**, playing the planner-selected window of **4 main quests** (window 1 of 2; the full level holds 9): `aws-essentials` → `azure-ascension-jekyll-deployment` → `infrastructure-as-code` → `self-operating-website-03-the-war-machine`.

**Headline verdict: ⚠️ warn — and partial coverage.** The sealed execute engine produced machine evidence for **only the first quest** (`aws-essentials`, 74% / warn): the run hit `auth_truncated: true` and evaluated **1 of 4** requested quests before the OAuth budget ran out. I therefore have real, in-sandbox command evidence for AWS Essentials only; the other three quests I read as a learner and reason about statically (`reasoned`), with **no executed commands** — I do not report them as passing. The one scored quest is technically solid (every `aws` CLI invocation parsed against a live `aws-cli/2.35.15`), but is docked on **completeness**: it promises "connect to" an EC2 instance and asks the learner to SSH in, yet never shows the SSH command, the public-IP lookup, or how to attach a security group to the launch. A maintainer's most actionable next step is to (a) close that SSH gap in AWS Essentials and (b) re-run the sealed engine with more budget so quests 2–4 get real evidence rather than static reasoning.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|:--:|---|
| 1 | ⚠️ warn (tested) | AWS Essentials: Core Services and Architecture | 74% | CLI is accurate & runs, but the taught SSH "connect" step is never actually shown. |
| 2 | ◽ reasoned (no evidence) | Azure Ascension: Deploying Jekyll to the Cloud Kingdom | — | Self-contained but leans on a repo helper script + real Azure/GitHub accounts; unrunnable in sandbox. |
| 3 | ◽ reasoned (no evidence) | Infrastructure as Code: Terraform Fundamentals and State | — | Clean, well-sequenced HCL; explicitly continues from AWS Essentials. |
| 4 | ◽ reasoned (no evidence) | The War Machine: Dispatch, Leasing, and a 50-Case Simulation | — | Strong standalone Epic, but belongs to a different campaign whose real prerequisite is at Level 0100. |

Legend: **tested** = commands actually run by the sealed engine in-sandbox; **reasoned** = judged by reading the quest source only (auth budget truncated the engine before these quests).

## 🔬 Evidence

### Quest 1 — AWS Essentials *(execute mode, tested)*

- **Snippet coverage:** engine recorded 23 commands, **ran 18 / 8 runnable
  snippets, 18 passed, 0 failed, 3 skipped, 2 reasoned** (`executed: true`).
- **Per-dimension:** commands_work **4**, content_accuracy **4**, completeness
  **2**, clarity **4**, structure **4**, safety **4** → overall **74% (warn)**.
- **Real commands run in the sandbox** (all reached the `NoCredentials`/auth
boundary rather than an "unrecognized argument" error, confirming syntax is valid and current against `aws-cli/2.35.15`):
  - `aws --version` → **passed** — `aws-cli/2.35.15` pre-installed, matches the
    quest's expected `aws-cli/2.x`.
  - IAM chain — `create-group`, `attach-group-policy … arn:aws:iam::aws:policy/ReadOnlyAccess`,
    `create-user`, `add-user-to-group`, `list-groups-for-user` → all **passed**
    (parsed, reached NoCredentials).
  - The IAM least-privilege policy JSON block → **passed** — validated cleanly with
    both `python3 -m json.tool` and `jq .`.
  - EC2 — `create-key-pair … > quest-key.pem`, `run-instances` with the
    `resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64`
    alias, `terminate-instances` → all **passed**.
  - `chmod 400 quest-key.pem` → **passed** — resulting perms verified exactly
    `-r--------`.
  - S3 — `BUCKET=my-quest-bucket-$RANDOM` (produced e.g. `my-quest-bucket-32646`),
    `s3 mb`, `s3 cp` up/down, `s3api put-public-access-block` (4 Block/Ignore/Restrict
    flags, matched `aws s3api put-public-access-block help`), `s3 rb --force` → all
    **passed**.
  - VPC — `create-vpc`, `create-security-group`, `authorize-security-group-ingress`
    → all **passed** (with dummy IDs).
- **Skipped / reasoned (environment-inapplicable, honestly not run):**
  - Linux installer (`curl … awscli-exe-linux-x86_64.zip && unzip && sudo ./aws/install`)
    → **skipped** — outbound network denied by sandbox; URL matches AWS's official
    installer, `bash -n` passed.
  - macOS `brew install awscli` → **reasoned**; Windows `winget install Amazon.AWSCLI`
    → **skipped** — no macOS/Windows env; package identifiers confirmed correct.
  - CloudShell `aws sts get-caller-identity` → **reasoned** — ran, failed
    NoCredentials as expected (real CloudShell is pre-authenticated).

> Engine summary (verbatim): *"The quest's CLI commands are technically accurate and
> all parse correctly against a real aws-cli/2.35.15 install (verified live
> in-sandbox up to the credentials boundary) … The main weakness is completeness: it
> promises 'connect to' an EC2 instance and asks learners to SSH in, but never shows
> the SSH command, public-IP lookup, or how to attach the Chapter-3 security group to
> the Chapter-2 instance launch."*

### Quests 2–4 — *no machine evidence*

The sealed `walk-evidence.json` carries `total: 1`, `evaluated: 1`, `requested: 4`, `truncated: true`, `auth_truncated: true`. No commands were executed for Azure Ascension, Infrastructure as Code, or The War Machine. Everything I say about them below is **`reasoned` from reading the quest source**, not tested — and I have not run their Terraform/Azure/GitHub-Actions commands.

## 🐞 Issues Found

Issues for Quest 1 are **evidence-backed** (from executed commands / engine findings). Issues for Quests 2–4 are **`reasoned` from source** and flagged as such.

### Quest 1 — AWS Essentials

- **HIGH · AWS Essentials · Ch.2 EC2 + Intermediate Challenge (SSH "connect")** —
*Observed (tested):* Primary objective says "**Launch, connect to, and terminate** a virtual server" and the Intermediate Challenge requires "SSH in, run `uname -a`", but the engine confirmed **no SSH command, no public-IP lookup, and no `ec2-user` username appears anywhere** in the quest. The Ch.2 `run-instances` also attaches **no** security group, so an instance launched exactly as shown can't be SSH'd into until the reader independently backfills the Chapter-3 security group. *Fix:* add the SSH command (e.g. `ssh -i quest-key.pem ec2-user@$(aws ec2 describe-instances --instance-ids <id> --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)`) and wire the SG into launch via `--security-group-ids <sg-id>`.
- **MEDIUM · AWS Essentials · Ch.3 VPC anatomy** — *Observed (tested):* CLI is shown
only for `create-vpc`, `create-security-group`, `authorize-security-group-ingress`; the Advanced Challenge asks learners to build a two-subnet VPC with route tables and an internet gateway, but **subnet / IGW / route-table commands are never given** (only an ASCII diagram). *Fix:* add `create-subnet`, `create-internet-gateway` + `attach-internet-gateway`, and `create-route-table` / `associate-route-table`.
- **MEDIUM · AWS Essentials · Cleanup / cost hygiene** — *Observed (tested):*
Teardown is asymmetric — EC2 (`terminate-instances`) and S3 (`rb --force`) are shown, but the VPC, security group, IAM group/user, and both the AWS-side key pair and the local `.pem` are never cleaned up, contradicting the quest's own "finish owing nothing" promise. *Fix:* add `delete-security-group`, `delete-vpc`, `aws ec2 delete-key-pair --key-name quest-key`, and `rm quest-key.pem`.
- **LOW · AWS Essentials · Ch.3 placeholder consistency** — *Observed (tested):* S3
teaches capturing values into a variable (`BUCKET=…`), but the VPC section reverts to `<vpc-id>`/`<sg-id>` placeholders despite `--query 'Vpc.VpcId' --output text` implying capture. *Fix:* show `VPC_ID=$(aws ec2 create-vpc … --output text)` style capture for consistency.
- **LOW · AWS Essentials · Windows key permissions** — *Observed (tested):*
`chmod 400 quest-key.pem` is presented as universal but does nothing on native Windows shells (the Windows path only covers install/configure). *Fix:* add an `icacls` equivalent or point Windows users to WSL/OpenSSH.

### Quest 2 — Azure Ascension *(reasoned from source, not tested)*

- **MEDIUM · Azure Ascension · Ch.2 dependency on a repo script** — *Observed
(reasoned, lines 88–96):* the whole deploy hinges on `scripts/deployment/azure-jekyll-deploy.sh setup` / `deploy`. A learner who only reads the quest can't see what that script assumes or does; if the script path drifts, the quest silently breaks. I did **not** run it (needs a real Azure account
  + `az login`). *Fix:* at minimum note the script is repo-local to `it-journey` and
  summarise its prerequisites/effects, or link its source.
- **LOW · Azure Ascension · relative `.md` "Related Quests" links** — *Observed
(reasoned, lines 122–124):* links use raw markdown-relative paths (`../0001/github-pages-portal.md`, `../1010/link-to-the-future-...md`) instead of site permalinks like the other quests. On the rendered Jekyll site these may not resolve to the quest permalink. I did **not** build the site to confirm. *Fix:* switch to permalink-style links (`/quests/0001/github-pages-portal/`).

### Quest 3 — Infrastructure as Code *(reasoned from source, not tested)*

- No blocking issues found on read. *(reasoned)* HCL blocks, the
init→plan→apply→destroy lifecycle, state rules, and variables/outputs are internally consistent; the placeholder bucket name `iac-quest-bucket-change-me-12345` is explicitly signposted as change-me. Not executed (no Terraform run in sandbox).

### Quest 4 — The War Machine *(reasoned from source, not tested)*

- **LOW · War Machine · slice-level prerequisite is off-level** — *Observed
(reasoned, lines 95–99):* the quest's real backlog "*is* the ledger" from **Chapter II — The Proving Grounds** at **Level 0100**, which is not in this slice or this level. A `build_backlog.py` stub is provided so the quest still stands alone, but a learner arriving from the AWS/Azure/IaC chain has no Chapter-II worklist. This is a chain-continuity note, not a defect in the quest itself.

**No blocking issue was fabricated.** Every Quest-1 issue traces to an executed command or engine finding; every Quest 2–4 issue is explicitly labelled `reasoned` and cites a quoted source line.

## 🔗 Chain Continuity

Reasoning about the four quests as one learner's journey for the Security Specialist class:

1. **AWS Essentials → Infrastructure as Code is the strong spine.** IaC's frontmatter
lists `aws-essentials` as a `required_quest`, and its opening narrative explicitly calls back — *"In the previous quest you clicked and typed your way through the AWS console… This quest teaches you to inscribe your infrastructure into a spellbook."* IaC re-provisions the very S3 bucket concept AWS Essentials created by hand, and its `data "aws_ami" … al2023-ami-*-x86_64` mirrors the SSM alias from Essentials. A learner finishing quest 1 is genuinely ready for quest 3. **But they are not adjacent in plan order** — Azure Ascension sits between them, so a learner walking the plan top-to-bottom takes a detour to a different cloud before the payoff.
2. **Azure Ascension is a self-contained outlier.** Its prerequisites (Azure account,
`az login`, Ruby ≥3.2, GitHub secrets) don't chain from AWS Essentials, and it teaches deployment on a *different* cloud. It neither depends on nor unlocks the AWS spine. Fine as an optional side-quest (AWS Essentials even links it as one), but as the #2 step in a linear walk it breaks the AWS→IaC momentum.
3. **The War Machine is an Epic from a different campaign.** It belongs to *The
Self-Operating Website* line; its recommended prerequisite is `self-operating-website-02` at **Level 0100**, not any quest in this slice. It's a 4–6 hour GitHub-Actions/Python project with no cloud-provider dependency on quests 1–3. Strong on its own, but as the closing step of a "Cloud Computing" slice it's thematically adjacent at best.
4. **Security-Specialist fit.** For this class the standout is AWS Essentials: IAM
least-privilege, the S3 public-access-block ("the single most common cloud breach"), and deny-by-default security groups are exactly on-brand — and the engine scored `safety: 4`. IaC extends that into secret/state hygiene. Azure and War Machine are less security-specific. The security learner is well served by the spine but the slice as a whole reads as a **general Cloud-Computing level windowed across classes**, not a security-tailored arc.

**Net:** the pedagogically load-bearing pair (1→3) holds together well; quests 2 and 4 are legitimate level content but are side-branches, so the *ordered window* reads less like one arc and more like a sampler. This is expected for a date-rotated window (1 of 2) and is a planning/observation note, not a content bug.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sealed evidence), consumed as-is from `./walk-evidence.json`
and `./walk-evidence.md`. I did **not** re-run the engine and did **not** modify `walk-plan.json` or the evidence files.
- **What I actually have vs. what I reasoned:** Machine-checked, in-sandbox command
evidence exists for **exactly one** quest — AWS Essentials (18/8 runnable snippets run, 0 failed). For the other three quests the engine produced **no evidence** — `walk-evidence.json` reports `evaluated: 1`, `requested: 4`, `auth_truncated: true`, `truncated: true`. I read those three quests in plan order and reasoned about them statically; I label every such judgement `reasoned` and raise no `passed`/`failed` claim for them.
- **Why coverage is partial:** the OAuth budget truncated the deterministic engine
step after the first quest (this is the workflow's sealed evidence, which the agent cannot regenerate). This is the honest state of the run — **1 of 4 quests carry real evidence.** I did not substitute numbers for the missing three.
- **Sandbox limits reflected in the evidence:** outbound network was denied (Linux
AWS-CLI installer skipped); macOS/Windows install blocks weren't runnable on the Linux sandbox; all AWS API calls stopped at the `NoCredentials` boundary by design (no live account), which still verifies syntax/flags but not real resource creation. No SSH, Terraform apply, Azure deploy, or GitHub-Actions run was executed.
- **Confidence:** **High** on the AWS Essentials findings (each cites an executed
command or an engine dimension finding). **Moderate** on the chain-continuity and Quest 2–4 observations (source-based reasoning, unverified by execution). The two link/render concerns for Azure are explicitly *unconfirmed by a site build*.
- **Scope discipline:** one slice, one report. No quest content, data, or config was
  edited; no branch/commit/PR was made. The caller handles git.
