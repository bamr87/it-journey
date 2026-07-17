---
title: 'Secrets Management: Secure CI Credentials'
author: IT-Journey Team
description: Handle CI secrets securely. Learn OIDC versus long-lived credentials, vault systems, least privilege, scoping, and rotation for pipelines and applications.
excerpt: Implement secure secrets management practices for protecting sensitive credentials in your pipelines
preview: images/previews/secrets-management-secure-configuration-handling-d.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0101'
difficulty: 🟡 Medium
estimated_time: 45-60 minutes
primary_technology: security
quest_type: main_quest
quest_series: DevOps Pipeline Mastery
quest_line: The Forge of Automation
quest_arc: Gates of the Pipeline
quest_dependencies:
  required_quests:
  - /quests/0101/cicd-fundamentals/
  recommended_quests:
  - /quests/0101/environment-management/
  unlocks_quests:
  - /quests/0101/artifact-management/
  - /quests/0101/workflow-optimization/
skill_focus: security
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Understanding of environment variables and config
  - Familiarity with Git and pull requests
  - Comfort using a terminal
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Git installed and a free GitHub account
  - A text editor or IDE (VS Code recommended)
  skill_level_indicators:
  - You have configured a CI pipeline before
  - You are ready to think about how credentials leak
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A workflow that authenticates to a cloud provider with OIDC, no stored keys
  skill_demonstrations:
  - Can explain why long-lived credentials are risky
  - Can scope a secret to least privilege
  knowledge_checks:
  - Understands OIDC short-lived tokens
  - Can describe a secret rotation process
permalink: /quests/0101/secrets-management/
categories:
- Quests
- DevOps
- Medium
tags:
- '0101'
- security
- main_quest
- devops
- hands-on
- gamified-learning
keywords:
  primary:
  - '0101'
  - security
  - main_quest
  secondary:
  - devops
  - hands-on
  - gamified-learning
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0101 (5) Quest: Main Quest - Security'
rewards:
  badges:
  - 🏆 Keeper of Secrets - Stopped credentials from leaking
  - 🔐 Bearer of the Short-Lived Token - Replaced static keys with OIDC
  skills_unlocked:
  - 🛠️ Secret Scoping
  - 🧠 Credential Rotation
  progression_points: 50
  unlocks_features:
  - Artifact and optimization quests in Level 0101
layout: quest
---
*Greetings, brave adventurer! Every pipeline you build must hold keys - to databases, to cloud accounts, to registries. A single key dropped in the open can hand an attacker your entire kingdom. This quest, **Secrets Management**, teaches you to carry those keys without ever revealing them: where to store them, how to grant the least power that still works, and - the modern marvel - how to stop carrying long-lived keys at all.*

*Whether you have ever pasted a password into a config file (we have all done it) or you already manage a vault, this adventure forges the discipline that separates a hardened pipeline from a breach waiting to happen: least privilege, short-lived OIDC tokens over static credentials, central vaults, and disciplined rotation.*

## 📖 The Legend Behind This Quest

*In the early ages, the secret to the cloud kingdom was a long, all-powerful key, copied into config files, pasted into chat, and committed to repositories "just for now." Attackers learned to scour public code for these keys, and a single leaked credential could drain an entire account overnight. The graveyards of the internet are full of companies felled by one committed access key.*

*The masters of security answered with three principles. First: **grant the least privilege that still works**, so a stolen key opens few doors. Second: **prefer short-lived, identity-based tokens over long-lived secrets**, so a leak expires in minutes. Third: **rotate what you must keep**, so even a quiet compromise has a short life. Master these and a leaked secret becomes a footnote, not a funeral.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Never Commit Secrets** - Keep credentials out of code and out of Git history
- [ ] **OIDC vs Long-Lived Credentials** - Trade static keys for short-lived, identity-based tokens
- [ ] **Least Privilege** - Scope every secret to the minimum access it needs
- [ ] **Rotation** - Replace credentials on a schedule and after any suspected exposure

### Secondary Objectives (Bonus Achievements)
- [ ] **Secret Vaults** - Store and fetch secrets from a central, audited vault
- [ ] **Environment Scoping** - Bind production secrets to a protected environment
- [ ] **Leak Detection** - Scan history and CI logs for accidentally exposed secrets

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain why a long-lived cloud key is riskier than an OIDC token
- [ ] Scope a credential so a leak exposes one resource, not the account
- [ ] Configure a workflow that assumes a cloud role with no stored keys
- [ ] Describe a rotation procedure for a database password

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Understanding of environment variables and configuration
- [ ] Familiarity with Git, branches, and pull requests
- [ ] Comfort using a terminal

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Git installed and a free GitHub account
- [ ] A text editor or IDE (VS Code recommended)

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You have configured a CI pipeline before
- [ ] You are ready to think about how credentials leak
- [ ] Ready for 45-60 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*You will store a secret in CI, then graduate to keyless OIDC. The CI mechanics are platform-agnostic; the local tooling differs slightly.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install the GitHub CLI to manage repository secrets from the terminal
brew install gh
gh auth login

# Store a secret WITHOUT it ever touching your code or shell history file
gh secret set DATABASE_URL
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install the GitHub CLI
winget install GitHub.cli
gh auth login

gh secret set DATABASE_URL
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install -y gh
gh auth login

gh secret set DATABASE_URL
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# In the cloud, prefer the platform's identity over stored keys.
# Example: assume a role with OIDC rather than embedding an access key.
aws sts get-caller-identity   # shows WHICH identity you authenticated as
```

> The cloud-native mindset: your workload has an identity, and it borrows short-lived credentials on demand. Nothing long-lived needs to be stored at all.

</details>

## 🧙‍♂️ Chapter 1: Never Commit Secrets - The First Commandment

*The cheapest breach to prevent is the one you cause yourself by committing a key. This chapter builds the habits that keep secrets out of code forever.*

### ⚔️ Skills You'll Forge in This Chapter
- Keeping secrets out of source and Git history
- Storing secrets in CI instead of files
- Understanding that masked is not the same as safe

### 🏗️ Secrets Live Outside the Code

Hardcoding a credential commits it to history forever - even deleting the line later leaves it in every past commit. Instead, read it from the environment and store the value in your CI provider's secret store.

```bash
# ❌ Never: a key baked into code, now in Git history forever
# const apiKey = "sk_live_51H8...";

# ✅ Always: read from the environment, set the value in CI's secret store
gh secret set STRIPE_API_KEY          # prompts for the value; never logged
echo "STRIPE_API_KEY is stored in CI, not in the repo"
```

In a workflow, a stored secret is injected as a variable. GitHub automatically **masks** it in logs, but masking is a safety net, not a strategy - a secret echoed into a file or sent to a third party can still leak.


```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
        env:
          # Injected from the repo/environment secret store, masked in logs
          STRIPE_API_KEY: ${% raw %}{{ secrets.STRIPE_API_KEY }}{% endraw %}
```


A `.gitignore` for `.env` files plus a pre-commit secret scanner stops the accident before it ships.

### 🔍 Knowledge Check: Keeping Secrets Out
- [ ] Why does deleting a committed key fail to remove it from history?
- [ ] Where should a secret value live instead of in code?
- [ ] Why is log masking a safety net rather than a strategy?

### ⚡ Quick Wins and Checkpoints
- [ ] **Stored a secret**: A value lives in CI's store, not your repo
- [ ] **Ignored `.env`**: Your `.gitignore` blocks local secret files

## 🧙‍♂️ Chapter 2: OIDC vs Long-Lived Credentials

*The biggest modern leap in pipeline security is to stop storing cloud keys entirely. Instead of a static secret, your pipeline proves its identity and borrows a token that expires in minutes.*

### ⚔️ Skills You'll Forge in This Chapter
- Why long-lived credentials are dangerous
- How OIDC federation issues short-lived tokens
- Configuring keyless cloud authentication

### 🏗️ Static Keys vs Short-Lived Tokens

| | Long-lived credential | OIDC short-lived token |
| --- | --- | --- |
| **What it is** | A static access key stored as a secret | A token minted per run, valid minutes |
| **If leaked** | Works until someone notices and revokes it | Already expired; useless to an attacker |
| **Rotation** | Manual, error-prone, often forgotten | Automatic - every run gets a fresh token |
| **Storage** | Must be stored somewhere (risk) | Nothing to store |

With **OpenID Connect (OIDC)**, your CI provider issues a signed identity token for each run. The cloud provider is configured to trust that issuer and to exchange the token for temporary credentials scoped to a specific role. No access key ever exists to be stolen.


```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write        # allow the job to request an OIDC token
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          # No access keys! Assume a role via OIDC trust.
          role-to-assume: arn:aws:iam::123456789012:role/github-deploy
          aws-region: us-east-1
      - run: aws s3 sync ./dist s3://my-deploy-bucket
```


The AWS role's trust policy is configured to accept GitHub's OIDC issuer and to restrict which repository and branch may assume it - so even the trust itself is scoped.

### 🔍 Knowledge Check: OIDC
- [ ] Why is a leaked OIDC token far less dangerous than a leaked access key?
- [ ] What does `id-token: write` permission enable?
- [ ] How does the cloud role limit *which* repo can assume it?

### ⚡ Quick Wins and Checkpoints
- [ ] **Understood the trade**: You can argue OIDC over static keys
- [ ] **Removed a key**: One workflow now authenticates without a stored secret

## 🧙‍♂️ Chapter 3: Vaults, Least Privilege, and Rotation

*For the secrets you must keep, three disciplines keep them safe: store them centrally, grant the minimum power, and replace them regularly.*

### ⚔️ Skills You'll Forge in This Chapter
- Central, audited secret vaults
- Scoping a secret to least privilege
- A rotation procedure for unavoidable static secrets

### 🏗️ Least Privilege for Secrets

A credential should open exactly the doors it needs and no more. Compare two policies for a deploy that only uploads to one bucket:

```json
// ❌ Over-privileged: full access to every bucket in the account
{ "Effect": "Allow", "Action": "s3:*", "Resource": "*" }
```

```json
// ✅ Least privilege: write only to the one deploy bucket
{
  "Effect": "Allow",
  "Action": ["s3:PutObject", "s3:ListBucket"],
  "Resource": [
    "arn:aws:s3:::my-deploy-bucket",
    "arn:aws:s3:::my-deploy-bucket/*"
  ]
}
```

If the first credential leaks, the attacker owns all storage; if the second leaks, they can write to one bucket. Scope shrinks the blast radius.

### 🏗️ Vaults and Rotation

A **secret vault** (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault) centralizes secrets with access control, audit logs, and - crucially - automated rotation. **Rotation** replaces a credential on a schedule and immediately after any suspected exposure.

```bash
# Fetch a secret at run time from a vault instead of storing a copy
aws secretsmanager get-secret-value --secret-id prod/db/password \
  --query SecretString --output text

# Rotation procedure (manual illustration of the lifecycle):
# 1. Create a new credential alongside the old (both valid briefly)
# 2. Deploy services to use the new one
# 3. Verify nothing still uses the old one (check audit logs)
# 4. Revoke the old credential
```

The overlap window in step 1 means rotation causes zero downtime: nothing breaks because the old key still works until everything has moved to the new one.

### 🔍 Knowledge Check: Vaults and Rotation
- [ ] How does least privilege shrink the blast radius of a leak?
- [ ] What three things does a vault add over a plain secret file?
- [ ] Why does the overlap window make rotation zero-downtime?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Audit for Leaks
**Objective**: Hunt for secrets that should not be in a repo.

**Requirements**:
- [ ] Search the codebase and `.env` files for hardcoded credentials
- [ ] Confirm `.gitignore` blocks local secret files
- [ ] List which secrets belong in the CI store instead

**Validation**: No live secret remains in tracked files.

### 🟡 Intermediate Challenge: Scope a Secret
**Objective**: Rewrite an over-privileged policy to least privilege.

**Requirements**:
- [ ] Start from a wildcard policy granting broad access
- [ ] Restrict it to exactly the actions and resources used
- [ ] Explain the blast radius before and after

**Validation**: The scoped credential can do the job and nothing more.

### 🔴 Advanced Challenge: Go Keyless with OIDC
**Objective**: Replace a stored cloud key with OIDC authentication.

**Requirements**:
- [ ] A workflow with `id-token: write` that assumes a cloud role
- [ ] A role trust policy restricted to your repo and branch
- [ ] No long-lived access key stored anywhere

**Validation**: The pipeline deploys successfully with zero stored cloud credentials.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Keeper of Secrets** - You stopped credentials from leaking
- 🔐 **Bearer of the Short-Lived Token** - You replaced static keys with OIDC

**🛠️ Skills Unlocked**:
- **Secret Scoping** - Grant least privilege to every credential
- **Credential Rotation** - Replace secrets without downtime

**🔓 Unlocked Quests**:
- Artifact Management - Sign and store what your pipeline builds
- Workflow Optimization - Make secure pipelines fast too

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Artifact Management](/quests/0101/artifact-management/) - Provenance and signed builds

**Explore Side Adventures**:
- ⚔️ [Workflow Optimization](/quests/0101/workflow-optimization/) - Speed without sacrificing safety
- ⚔️ [Environment Management](/quests/0101/environment-management/) - Per-environment secret scoping

### Character Class Recommendations

**💻 Software Developer**: Continue to [Artifact Management](/quests/0101/artifact-management/)  
**🏗️ System Engineer**: Explore [Workflow Optimization](/quests/0101/workflow-optimization/)  
**🛡️ Security Specialist**: Advance to [Artifact Management](/quests/0101/artifact-management/)

## 📚 Resources

### Official Documentation
- [GitHub Actions: Security hardening with OpenID Connect](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect) - Keyless cloud auth
- [GitHub Actions: Using secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) - Storing and injecting secrets
- [HashiCorp Vault](https://developer.hashicorp.com/vault/docs) - Central secret management

### Community Resources
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) - Practical guidance
- [AWS: IAM least privilege](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) - Scoping policies
- [git-secrets](https://github.com/awslabs/git-secrets) - Prevent committing secrets

### Learning Materials
- [trufflehog](https://github.com/trufflesecurity/trufflehog) - Scan history for leaked secrets
- [Azure Key Vault overview](https://learn.microsoft.com/en-us/azure/key-vault/general/overview) - A managed vault example

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Configured a keyless OIDC deploy
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0101 - CI/CD & DevOps]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Requires:** [[CI/CD Fundamentals: Continuous Integration and Continuous Deployment Essentials]] **Unlocks:** [[Artifact Management: Build Output Storage and Dependency Caching]] · [[Workflow Optimization: Caching Strategies and Pipeline Parallelization]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
