---
title: 'Quest Walkthrough — Security Specialist · Level 1000 (Cloud Computing, Warrior)'
date: '2026-07-08T00:00:00.000Z'
character: security-specialist
level: '1000'
theme: Cloud Computing
tier: Warrior
quest_count: 4
mode: execute
overall_verdict: fail
session:
  window: '2 of 2 (offset 5, size 5)'
  level_total_quests: 9
  quests_walked: 4
  average_score: 57.8
  verdicts: '1 pass · 1 warn · 2 fail'
  engine_cost_usd: 3.5946
  evidence_source: sealed walk-evidence.json (workflow-minted, agentic execute engine)
---

## 🎯 Session Summary

I walked a **4-quest window** (window 2 of 2, offset 5) of the **Security Specialist →
Level 1000 (Cloud Computing, 🔥 Warrior)** path as a learner: **AWS Essentials →
Azure Ascension → Infrastructure as Code → The War Machine**. The full level holds 9
quests; this run swept the second half, so the earlier foundational quests
(Cloud Computing Fundamentals and the rest of window 1) were **not** part of this
session. Evidence came from the sealed, workflow-minted `walk-evidence.json`
(agentic **execute** engine, real commands in a disposable sandbox); my own
contribution is the linked-journey reasoning across the chain, which is **`reasoned`**
(static read of each quest source), not re-executed.

**Headline verdict: fail.** The slice averages **57.8%** (1 pass, 1 warn, 2 fail).
Two quests are genuinely strong — *Infrastructure as Code* (81, pass) is
verifiably accurate end-to-end, and *AWS Essentials* (74, warn) is well-built save
for one copy-paste-breaking bug. But two quests fail hard for a Security Specialist
specifically: *Azure Ascension* (38) has **zero** of its runnable snippets succeed as
written, and *The War Machine* (38) makes a **verifiably false security claim** — its
git-ref CAS "no-double-lease" lock lets two racing runners both win, which the engine
reproduced directly. For the character class whose whole job is trusting security
guarantees, that false claim is the most important finding of the run.

## 🗺️ The Journey

Plan order (dependency-sorted window from `walk-plan.json`):

1. ⚠️ **AWS Essentials: Core Services and Architecture** — **74** · 🔴 Hard ·
   Accurate, safety-conscious IAM/EC2/S3/VPC tour, but the S3 section creates a
   `$RANDOM` bucket then hardcodes a different name — breaks on copy-paste.
2. ❌ **Azure Ascension: Deploying Jekyll to the Cloud Kingdom** — **38** · 🔴 Hard ·
   Sound chapter arc, but no snippet runs as written: missing repo/clone/`cd` setup,
   no Azure CLI prerequisite, and a deploy script referenced by an unverifiable path.
3. ✅ **Infrastructure as Code: Terraform Fundamentals and State** — **81** · 🔴 Hard ·
   The one clean pass: full init/plan/apply/destroy lifecycle, state, variables, and
   idempotency confirmed against real Terraform. Only minor gaps.
4. ❌ **The War Machine: Dispatch, Leasing, and a Fifty-Case Simulation** — **38** ·
   ⚔️ Epic · Clean OODA/RICE Chapter 1, but Chapter 2's core distributed-lock
   guarantee is false under the realistic same-HEAD race, plus a red-out-of-the-box
   CI pipeline.

## 🔬 Evidence

All results below are from the sealed execute-engine run (`mode: execute`,
`executed: true` on every quest). Snippet coverage and command outcomes are quoted
from `walk-evidence.json` / `walk-evidence.md`; I did not re-run the engine.

### 1. AWS Essentials — 74 (warn) · ran 3/8 runnable snippets (2✓ 1✗), 7 skipped, 1 reasoned
- **`aws s3 mb s3://my-quest-bucket-$RANDOM` then hardcoded `my-quest-bucket-12345`** →
  **failed**. Engine finding: "`$RANDOM` produced 26288, 13907 on two runs, but every
  following command hardcodes `my-quest-bucket-12345` — a bucket that was never
  created … a learner copy-pasting verbatim gets `NoSuchBucket`/`AccessDenied` on the
  very next line." Confirmed against quest source lines 309–323.
- **`aws ec2 run-instances … --dry-run`** → skipped/verified: "parsed successfully,
  failed only at NoCredentials stage, confirming valid CLI syntax including the
  `resolve:ssm:` AMI alias."
- **IAM least-privilege policy JSON** → **passed**: validated as syntactically valid
  JSON, grants match stated intent (`s3:GetObject`/`ListBucket` on one bucket).
- **`chmod 400 quest-key.pem`** → **passed** (file mechanics work locally).
- IAM/EC2/VPC provisioning sequences → skipped (need a live billable account, by the
  quest's own design), each subcommand's flags verified real via `aws <svc> <cmd> help`.
- Safety scored **5/5**: explicit live-billing warning, root-MFA warning, and the
  "most common cloud breach is a public S3 bucket" warning paired with
  `put-public-access-block`.

### 2. Azure Ascension — 38 (fail) · ran 4/3 recorded snippets, **0 passed, 4 failed**
- **`bundle install`** → **failed** (exit 127): "`bash: bundle: command not found` …
  and even if `bundle` were resolvable there is no Gemfile anywhere reachable, since
  the quest never instructs the learner to clone the repo or `cd` into the Jekyll site
  root before Chapter 1."
- **`bundle exec jekyll build`** → **failed** (same root cause, exit 127).
- **`../../scripts/deployment/azure-jekyll-deploy.sh setup`** → **failed** (exit 127):
  "`No such file or directory` … the quest never states from which directory the
  script should be invoked, so the relative path `../../` is only valid if the learner
  is standing in the exact quest markdown's own folder."
- **`… deploy --app-name <…> --github-repo <…>`** → **failed**: script not found; its
  flag contract "cannot be verified anywhere in this quest or its linked files."
- `commands_work` scored **1/5**. Safety still **4/5** (no destructive local commands).

### 3. Infrastructure as Code — 81 (pass) · ran 9/6 runnable snippets (7✓ 2✗), 2 skipped, 1 reasoned
- **`terraform init` + `terraform validate`** (Chapter 1 main.tf/data.tf) → **passed**:
  "downloaded hashicorp/aws v5.100.0 … `terraform validate` returned 'Success! The
  configuration is valid.'"
- **Full init/plan/apply/destroy lifecycle** → **passed** via a substitute
  `hashicorp/local` config (no AWS creds in sandbox): "plan showed '+ create … Plan: 1
  to add, 0 to change, 0 to destroy', apply succeeded, destroy produced 'Destroy
  complete! Resources: 1 destroyed.'" — matching the quest text verbatim.
- **Idempotency text** → **passed**: a second apply reproduced "No changes. Your
  infrastructure matches the configuration." verbatim.
- **variables.tf/outputs.tf + `-var` + `terraform output`** → **passed** end-to-end on
  the substitute config.
- **`docker run --rm -it … hashicorp/terraform:latest version`** → **failed**: "'the
  input device is not a TTY' … removing `-it` succeeded and printed 'Terraform
  v1.15.7'." A real gotcha for non-interactive/CI shells.
- **S3 remote-backend `terraform init`** → **failed** on "No valid credential sources
  found" (expected without live AWS), HCL syntax itself confirmed valid.

### 4. The War Machine — 38 (fail) · ran 9/7 runnable snippets (6✓ 3✗), 1 reasoned
- **`lease.sh` concurrent same-HEAD race** → **failed** (the headline): engine ran the
  exact `lease.sh` against a real local bare-repo remote with two independent clones on
  the identical HEAD SHA — "Runner C's push created the ref (exit 0). Runner D's
  identical push also returned exit 0 with 'Everything up-to-date' instead of being
  rejected … BOTH runners believe they won and would both call `work.sh` on the same
  task." Rejection only worked when SHAs were forced to differ.
- **`ruff check scripts/`** (CI lint tier) → **failed**: "`E401 Multiple imports on
  one line` on `import json, sys` in both build_backlog.py and decide.py … the lint
  tier would go red out of the box."
- **`pytest tests/unit -q`** (CI unit tier) → **failed**: "exits with code 5 ('no
  tests ran') because the quest never provides any content for `tests/unit/`."
- **`python3 scripts/build_backlog.py | python3 scripts/decide.py`** → **failed**:
  "`ModuleNotFoundError: No module named 'decide_core'` because the quest never states
  where to save the decide_core.py snippet" (no `# path` header). Worked only after
  guessing to place it in `scripts/`.
- **Fifty-case simulation `pytest tests/sim/test_dispatch_sim.py`** → **passed** 50/50,
  deterministic across 5 runs — **but** the Mastery Challenge's "prove the test has
  teeth" sabotage (remove `threading.Lock()`) still passed **20/20**, so the promised
  failure never reproduced (CPython GIL + tiny critical section).
- Chapter 1 (Task/rice_score/decide, build_backlog.py, dispatch.sh, work.sh single-run
  lease) all → **passed**.

## 🐞 Issues Found

Every item below is backed by a command the engine actually ran in the sandbox or an
exact line quoted from the quest source.

- **HIGH · War Machine · Chapter 2, `lease.sh` (source lines 234–248)** — The core
  security guarantee is **false in the common case**. `git push
  --force-with-lease=refs/leases/$TASK_ID:` returns success for **both** racing runners
  when they share the same HEAD SHA (reproduced: both exit 0, second says "Everything
  up-to-date"), so two runners double-lease the same task. The prose asserts "exactly
  one push is accepted." *Fix:* make the lease-ref target unique per attempt (an empty
  per-runner commit carrying a nonce/timestamp/runner-id) so the two pushes are never
  byte-identical, or explicitly document the loophole. **This is the run's most
  security-critical finding** — a Security Specialist is exactly the reader who would
  trust and reuse this "correct distributed lock."
- **HIGH · War Machine · CI lint tier** — `ruff check scripts/` fails on the quest's
  own `import json, sys` (E401) in build_backlog.py and decide.py; the first pipeline
  tier is red out of the box. *Fix:* split the imports or relax E401 in a noted config.
- **HIGH · War Machine · CI unit tier** — `pytest tests/unit -q` exits 5 (no tests
  collected); `tests/unit` is never populated. *Fix:* provide the decide()/RICE unit
  tests or remove that tier.
- **HIGH · Azure Ascension · Chapter 1 prerequisites (lines 59–71)** — No step to
  clone the repo or `cd` into the Jekyll site root before `bundle install`; both build
  snippets fail (exit 127). *Fix:* add an explicit clone + `cd <dir>` step and note the
  Ruby/Bundler version.
- **HIGH · Azure Ascension · Chapter 2 deploy script (lines 77–79)** — The whole
  deploy hinges on `../../scripts/deployment/azure-jekyll-deploy.sh`, not found at that
  relative path, with an undocumented working dir and unverifiable `setup`/`deploy`
  flag contract. *Fix:* state the invocation directory (not a bare `../../`), document
  `setup` vs `deploy`, and give the `--app-name`/`--github-repo` formats.
- **HIGH · Azure Ascension · System Requirements (lines 55–57)** — Chapter 2 needs
  Azure authentication but the CLI (`az login`) is never listed as a prerequisite.
  *Fix:* add Azure CLI install + `az login`.
- **HIGH · AWS Essentials · Chapter 2 S3 (lines 309–323)** — `$RANDOM` bucket created,
  then `my-quest-bucket-12345` hardcoded in every following command; copy-paste yields
  `NoSuchBucket`/`AccessDenied`. *Fix:* `BUCKET=my-quest-bucket-$RANDOM; aws s3 mb
  s3://$BUCKET` and reuse `$BUCKET`, or use a `<bucket-name>` placeholder like the rest
  of the quest.
- **MEDIUM · War Machine · Chapter 1 decide_core.py placement** — `decide.py` does
  `from decide_core import …` but the snippet (lines 115–137) has no `# path` header;
  running it raises `ModuleNotFoundError`. *Fix:* add a `# decide_core.py` header /
  save-location instruction.
- **MEDIUM · War Machine · Mastery Challenge "prove the test has teeth"** — Removing
  the lock did not reproduce a failure in 20/20 runs. *Fix:* add a small
  `time.sleep(0.001)` between read and write in the sabotaged `simulate_run` so the
  collision is observable.
- **MEDIUM · Azure Ascension · Chapter 3 secrets (lines 84–89) + Knowledge Graph
  (line 112)** — Secrets chapter names no actual secret (e.g.
  `AZURE_STATIC_WEB_APPS_API_TOKEN`); the "Level hub" wiki-link points to *Level 1001
  Kubernetes Orchestration*, unrelated to this Azure/Jekyll quest. *Fix:* name the
  secret and where to set it; repoint the Level hub link to Level 1000 Cloud Computing.
- **MEDIUM · AWS Essentials · Intermediate Challenge (lines 401–410)** — Says "SSH in,
  run `uname -a`" but never shows the SSH command, the `ec2-user` default login, or how
  to fetch the public IP. *Fix:* add `ssh -i quest-key.pem ec2-user@<public-ip>` and a
  `describe-instances --query` for the IP.
- **MEDIUM · Infrastructure as Code · Docker path (lines 199–203)** — `docker run
  --rm -it …` fails with "the input device is not a TTY" in non-interactive/CI shells;
  removing `-it` works. *Fix:* use `-i` only or add a caveat.
- **LOW · Infrastructure as Code · example bucket name (line 237)** —
  `iac-quest-bucket-change-me-12345` is globally unique and will collide across
  learners (`BucketAlreadyExists`); the "change-me" hint isn't an explicit callout.
- **LOW · AWS Essentials · Free Tier claim (line 283)** — `t2.micro`/`t3.micro`
  "Free-Tier eligible" is true for pre-2024 accounts; AWS's 2024 credit-based Free
  Tier revamp isn't mentioned.

No fabricated issues: every high/medium/low above traces to a sealed command result or
a quoted source line.

## 🔗 Chain Continuity

Reading the four quests as one Security Specialist journey (this is **`reasoned`**, a
static read of each source, not re-execution):

- **Windowing context.** This is window 2 of 2 (`offset 5` of a 9-quest level), so the
  learner arriving here is assumed to have cleared window 1 — including *Cloud
  Computing Fundamentals*, which AWS Essentials lists as a required prerequisite
  (frontmatter `required_quests: /quests/1000/cloud-computing-fundamentals/`). That
  prerequisite lives **outside this window**, so I could not witness whether it
  actually prepares the learner; I only confirmed AWS Essentials *declares* it.
- **The one clean internal link: AWS Essentials → Infrastructure as Code.** IaC's
  frontmatter requires `/quests/1000/aws-essentials/`, and the planner places AWS
  Essentials (pos 1) before IaC (pos 3) — correct order. IaC's narrative even opens by
  referencing "the previous quest [where] you clicked and typed through the AWS
  console," and reuses the same S3-bucket example. A learner finishing AWS Essentials
  *is* ready for IaC. This is the strongest, best-sequenced hop in the slice.
- **Azure Ascension is an interloper in the chain.** It declares no
  `quest_dependencies` and belongs to a different series ("Cloud Deployment Quests").
  Sequencing it at position 2 — *between* AWS Essentials and its declared successor
  IaC — is harmless ordering-wise (nothing depends on it), but pedagogically it drops a
  broken, self-contained deploy quest into the middle of an otherwise coherent AWS→IaC
  arc. A learner hitting its exit-127 wall at position 2 would lose momentum before
  reaching the strong IaC quest.
- **The War Machine is a campaign orphan here.** Its real prerequisite is
  `/quests/0100/self-operating-website-02-the-proving-grounds/` (Chapter II, level
  **0100**) — a quest from a completely different level and campaign ("The
  Self-Operating Website"). It even says "You need its self-survey worklist … because
  that ledger *is* the backlog this dispatcher observes." A Security Specialist walking
  Level 1000 top-to-bottom has **not** done Proving Grounds, so this Epic assumes state
  and context the level never provided. It reads as a mis-shelved chapter, not a
  Level-1000 Cloud Computing quest.
- **Security-specialist lens across the slice.** The security *framing* is genuinely
  good where it appears: AWS Essentials (IAM least-privilege, root-MFA, public-S3
  breach warning — safety 5/5), IaC (state-file secret rules, "never commit state with
  secrets"), and War Machine (strict allowlist regex sanitizing `TASK_ID` before it
  enters a ref name — good injection defense). The cruel irony is that the quest
  pitched hardest at *this* class — War Machine's "correct distributed lock without
  Redis" — is the one whose security guarantee the engine **disproved**. For a Security
  Specialist, a confidently-stated-but-false concurrency invariant is worse than an
  admitted gap, because the whole point of the class is knowing which guarantees hold.
- **Net:** the slice does **not** hold together as a clean linear path. One solid
  internal hop (AWS→IaC), one broken independent quest wedged in the middle (Azure),
  and one out-of-level campaign chapter (War Machine) whose prerequisite is unreachable
  from this level. A maintainer should consider whether Azure Ascension and War Machine
  belong in the Security Specialist / Level 1000 sequence at all, independent of fixing
  their in-quest bugs.

## 🧠 Reasoning & Method

- **What I ran vs. reasoned about.** I ran **nothing** myself. All command evidence in
  §🔬 and §🐞 comes from the sealed, workflow-minted `walk-evidence.json` (agentic
  **execute** engine, `mock: false`, `executed: true` on all 4 quests, ~$3.5946, real
  commands in a disposable sandbox). Per the skill, I consumed the sealed evidence
  as-is and did not re-run, edit, or regenerate it — the engine's child processes
  cannot authenticate from my Bash tool. My linked-journey analysis in §🔗 is
  **`reasoned`**: a static read of each quest's Markdown source in plan order, not
  re-execution.
- **Mode & sandbox.** Execute mode, disposable runner sandbox. The engine had **no
  live AWS/Azure credentials**, so most provisioning commands were correctly
  `skipped`/verified-for-syntax rather than run against real infrastructure — this is
  by design for Hard live-account quests and is **not** counted against them. Where the
  engine substituted a local provider (IaC's `hashicorp/local`) or a real local git
  remote (War Machine's `lease.sh`), I treated those as genuine executions because the
  evidence shows real output.
- **Coverage & limits.** This is a **partial** sweep of the level by design: 4 of 9
  quests (window 2 only). Window 1 and the declared cross-window prerequisite (Cloud
  Computing Fundamentals) were **not** walked, so any prerequisite-satisfaction claim
  about them is unverified. Snippet coverage was capped by the engine per quest (e.g.
  AWS Essentials ran 3/8 runnable snippets, 7 skipped for lack of a live account); I
  reported those caps honestly rather than implying full coverage. No network access
  beyond what the engine already exercised; no destructive commands.
- **Confidence.** High on the four flagged **failures/bugs** — each is a reproduced
  sandbox command or a directly quoted source line (the War Machine double-lease, the
  Azure exit-127 wall, the AWS bucket-name mismatch, the two red CI tiers). Medium on
  the chain-continuity judgments, since they are static reasoning over frontmatter and
  narrative, not executed. I did **not** verify the live-account provisioning paths in
  AWS Essentials or the Azure deploy against real clouds — those remain unproven either
  way.

_One slice, one report. No quest content was modified; findings above are for a
separate content pass or a human to act on._
