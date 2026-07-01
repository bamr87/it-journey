---
title: 'Artifact Management: Versioned, Signed Build Output'
author: IT-Journey Team
description: Manage build artifacts in CI/CD. Learn registries, semantic versioning, immutable tags, and supply-chain provenance with SBOMs and signed builds.
excerpt: Learn to manage build artifacts and dependencies efficiently in your CI/CD pipelines
preview: images/previews/artifact-management-build-output-quest-title-depen.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0101'
difficulty: 🟡 Medium
estimated_time: 45-60 minutes
primary_technology: artifacts
quest_type: main_quest
quest_series: DevOps Pipeline Mastery
quest_line: The Forge of Automation
quest_arc: Gates of the Pipeline
quest_dependencies:
  required_quests:
  - /quests/0101/cicd-fundamentals/
  recommended_quests:
  - /quests/0101/deployment-pipelines/
  unlocks_quests:
  - /quests/0101/workflow-optimization/
skill_focus: devops
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Understanding of the build-test-deploy flow
  - Familiarity with Git tags and versioning
  - Comfort using a terminal
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Git installed and a free GitHub account
  - Docker installed for the container registry exercise
  skill_level_indicators:
  - You have produced a build output before
  - You are ready to version and store what you build
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A pipeline that builds, versions, and publishes a signed artifact with an SBOM
  skill_demonstrations:
  - Can explain semantic versioning and immutable tags
  - Can generate an SBOM for a build
  knowledge_checks:
  - Understands why artifacts must be immutable
  - Can describe build provenance
permalink: /quests/0101/artifact-management/
categories:
- Quests
- DevOps
- Medium
tags:
- '0101'
- artifacts
- main_quest
- devops
- hands-on
- gamified-learning
keywords:
  primary:
  - '0101'
  - artifacts
  - main_quest
  secondary:
  - devops
  - hands-on
  - gamified-learning
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0101 (5) Quest: Main Quest - Artifacts'
rewards:
  badges:
  - 🏆 Keeper of the Vault - Stored versioned, immutable artifacts
  - 📜 Scribe of Provenance - Proved where a build came from
  skills_unlocked:
  - 🛠️ Artifact Versioning
  - 🧠 Supply-Chain Provenance
  progression_points: 50
  unlocks_features:
  - Workflow optimization quest in Level 0101
layout: quest
---
*Greetings, brave adventurer! Your pipeline now builds, tests, and ships. But what exactly is the *thing* it ships, and where does it live between the forge and the gates of production? This quest, **Artifact Management**, teaches you to treat your build output as a sacred, versioned, tamper-proof relic - one you can store, trace, and trust all the way to production.*

*Whether you have only ever uploaded a zip to a server or you already push container images, this adventure forges the discipline behind the modern software supply chain: registries, semantic versioning, immutable tags, and the provenance trail - SBOMs and signatures - that proves a relic is genuine and unaltered.*

## 📖 The Legend Behind This Quest

*Once, builders shipped whatever was on the server at the time - rebuilding "the latest" on each machine and hoping the results matched. When two servers ran subtly different builds of "the same" version, the bugs that followed were maddening and untraceable. No one could say which exact bytes were running where.*

*The masters answered with a single relic-law: **build the artifact once, give it an immutable name, and promote that exact relic everywhere.** Later, as attackers learned to poison the supply chain itself, the masters added provenance - a signed bill of materials proving what is inside a relic and who forged it. Master this and "which version is in production?" becomes a question with a precise, verifiable answer.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Build Artifacts** - Recognize what a pipeline produces and why to keep it
- [ ] **Registries** - Publish and pull artifacts from package and container registries
- [ ] **Versioning** - Apply semantic versioning and immutable tags
- [ ] **Provenance & SBOM** - Generate a software bill of materials and sign a build

### Secondary Objectives (Bonus Achievements)
- [ ] **Immutable Tags** - Understand why `latest` is dangerous in production
- [ ] **Retention Policies** - Expire old artifacts to control cost
- [ ] **Dependency Caching** - Distinguish a cache from an artifact

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain why an artifact must be immutable once published
- [ ] Choose the right version bump for a change (major/minor/patch)
- [ ] Generate and read an SBOM for a build
- [ ] Verify a signed artifact's provenance

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Understanding of the build-test-deploy flow (see CI/CD Fundamentals)
- [ ] Familiarity with Git tags and versioning
- [ ] Comfort using a terminal

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Git installed and a free GitHub account
- [ ] Docker installed (for the container registry exercise)

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You have produced a build output before
- [ ] You are ready to version and store what you build
- [ ] Ready for 45-60 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*You will build an artifact, version it, and push it to a registry. The Docker workflow is identical everywhere; install steps differ.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install Docker to build and push a container artifact
brew install --cask docker

# Build an immutably-tagged image (the short commit SHA is unique)
docker build -t myapp:$(git rev-parse --short HEAD) .
docker images myapp
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install Docker Desktop
winget install Docker.DockerDesktop

docker build -t myapp:$(git rev-parse --short HEAD) .
docker images myapp
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install -y docker.io
sudo systemctl enable --now docker

sudo docker build -t myapp:$(git rev-parse --short HEAD) .
sudo docker images myapp
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Push to GitHub Container Registry (ghcr.io) from any container host
echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GITHUB_USER" --password-stdin
docker tag myapp:abc1234 ghcr.io/your-org/myapp:1.4.2
docker push ghcr.io/your-org/myapp:1.4.2
```

> A registry is the vault where relics live. Once pushed, that exact digest can be pulled identically into staging and production - the heart of "build once, promote everywhere."

</details>

## 🧙‍♂️ Chapter 1: Artifacts and Registries

*An artifact is the concrete output of a build - a container image, a jar, a wheel, a tarball. A registry is the catalogued vault where artifacts live so any environment can pull the exact same bytes.*

### ⚔️ Skills You'll Forge in This Chapter
- What counts as an artifact versus a transient cache
- The role of package and container registries
- Publishing and pulling by exact identity

### 🏗️ Artifacts vs Caches

These are often confused, but they serve opposite purposes:

| | Artifact | Cache |
| --- | --- | --- |
| **Purpose** | The thing you ship and keep | A speed-up you can throw away |
| **Lifetime** | Retained, versioned, traceable | Disposable; rebuilt if missing |
| **If lost** | A release is gone | The build just runs slower |
| **Example** | `myapp:1.4.2` image | `node_modules` restored from cache |

A registry catalogues artifacts so any consumer pulls the identical bytes. Publishing a build artifact from CI looks like this:


```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      # Keep the build output as a downloadable, versioned artifact
      - uses: actions/upload-artifact@v4
        with:
          name: web-dist-${% raw %}{{ github.sha }}{% endraw %}
          path: dist/
          retention-days: 30
```


### 🔍 Knowledge Check: Artifacts and Registries
- [ ] What is the difference between an artifact and a cache?
- [ ] Why does a registry let you "build once, promote everywhere"?
- [ ] If a cache is deleted, what happens? If an artifact is deleted?

### ⚡ Quick Wins and Checkpoints
- [ ] **Built an artifact**: A `dist/` or image exists
- [ ] **Published it**: It is downloadable from CI or a registry

## 🧙‍♂️ Chapter 2: Versioning and Immutable Tags

*A relic without a unique, permanent name is a relic you cannot trust. Versioning and immutability are what make "which build is in production?" answerable.*

### ⚔️ Skills You'll Forge in This Chapter
- Semantic versioning (MAJOR.MINOR.PATCH)
- Why published artifacts must be immutable
- The danger of mutable tags like `latest`

### 🏗️ Semantic Versioning

Semantic versioning encodes the *kind* of change in the number itself:

```text
  MAJOR . MINOR . PATCH      e.g.  2 . 4 . 1
    │       │       │
    │       │       └── PATCH: backward-compatible bug fix
    │       └────────── MINOR: backward-compatible new feature
    └────────────────── MAJOR: breaking change (consumers must adapt)
```

A consumer reading `2.4.1 → 2.5.0` knows to expect new features but no breakage; `2.4.1 → 3.0.0` warns them to read the migration notes.

### 🏗️ Immutable Tags

Once published, a versioned artifact must **never change**. If `myapp:1.4.2` means different bytes on different days, every guarantee collapses - you cannot reproduce a bug, roll back reliably, or trust that staging tested what production runs.

```bash
# ❌ Mutable: "latest" points at different bytes over time — unsafe in prod
docker pull myapp:latest

# ✅ Immutable: a specific version, or best of all, a content digest
docker pull myapp:1.4.2
docker pull myapp@sha256:9b2c...   # the digest can NEVER point elsewhere
```

The strongest form of immutability is a **content digest** (`@sha256:...`): it is derived from the bytes themselves, so it is physically impossible for it to refer to anything else. Production deploys should pin a digest, not a floating tag.

### 🔍 Knowledge Check: Versioning
- [ ] What does a bump from `2.4.1` to `3.0.0` signal to consumers?
- [ ] Why is deploying `:latest` to production dangerous?
- [ ] Why can a content digest never refer to different bytes?

## 🧙‍♂️ Chapter 3: Provenance and SBOMs - Trusting the Supply Chain

*Knowing an artifact's name is not enough; you must know what is inside it and who made it. Provenance is the chain of custody for software.*

### ⚔️ Skills You'll Forge in This Chapter
- The software bill of materials (SBOM)
- Build provenance and signing
- Verifying an artifact before you trust it

### 🏗️ The Software Bill of Materials

An **SBOM** is an itemized list of every component and dependency inside an artifact - the ingredient label for your software. When a new vulnerability is announced, an SBOM lets you instantly answer "are we affected?" by searching your bill of materials rather than guessing.

```bash
# Generate an SBOM for a container image (using Syft)
syft myapp:1.4.2 -o spdx-json > sbom.spdx.json

# Later, scan the SBOM against known vulnerabilities (using Grype)
grype sbom:sbom.spdx.json
```

**Build provenance** records *how* and *where* an artifact was built - which commit, which workflow, which runner. Signing the artifact and its provenance lets consumers verify it was produced by your pipeline and not swapped by an attacker.


```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      id-token: write          # for keyless signing via OIDC
      attestations: write      # to record build provenance
    steps:
      - uses: actions/checkout@v4
      - id: push
        run: |
          docker build -t ghcr.io/your-org/myapp:1.4.2 .
          docker push ghcr.io/your-org/myapp:1.4.2
      # Generate signed provenance attesting THIS build produced THIS image
      - uses: actions/attest-build-provenance@v1
        with:
          subject-name: ghcr.io/your-org/myapp
          subject-digest: ${% raw %}{{ steps.push.outputs.digest }}{% endraw %}
```


Now a consumer can verify provenance before deploying, closing the door on supply-chain tampering between your forge and their gates.

### 🔍 Knowledge Check: Provenance
- [ ] How does an SBOM help when a new CVE is announced?
- [ ] What does build provenance record about an artifact?
- [ ] Why does signing protect against supply-chain tampering?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Sort Artifacts from Caches
**Objective**: Classify pipeline outputs correctly.

**Requirements**:
- [ ] Label `node_modules`, a built `dist/`, a Docker image, and a compiler cache
- [ ] State which to keep/version and which are disposable
- [ ] Explain the consequence of losing each

**Validation**: Your classification matches the artifact-vs-cache table.

### 🟡 Intermediate Challenge: Version and Publish
**Objective**: Build, immutably tag, and publish an artifact.

**Requirements**:
- [ ] Build an image tagged with a semantic version (e.g. `1.0.0`)
- [ ] Push it to a registry (ghcr.io or similar)
- [ ] Pull it back by digest, not by `latest`

**Validation**: The exact digest you pushed is the digest you pull.

### 🔴 Advanced Challenge: Provenance and SBOM
**Objective**: Make a build verifiable end to end.

**Requirements**:
- [ ] Generate an SBOM for your artifact
- [ ] Attach signed build provenance in the pipeline
- [ ] Scan the SBOM for known vulnerabilities

**Validation**: The provenance verifies and the SBOM scan runs clean (or you triage findings).

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Keeper of the Vault** - You stored versioned, immutable artifacts
- 📜 **Scribe of Provenance** - You proved where a build came from

**🛠️ Skills Unlocked**:
- **Artifact Versioning** - Semantic versions and immutable digests
- **Supply-Chain Provenance** - SBOMs and signed builds

**🔓 Unlocked Quests**:
- Workflow Optimization - Cache and parallelize to build artifacts faster

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Workflow Optimization](/quests/0101/workflow-optimization/) - Build these artifacts faster

**Explore Side Adventures**:
- ⚔️ [Deployment Pipelines](/quests/0101/deployment-pipelines/) - Promote the artifact you signed
- ⚔️ [Secrets Management](/quests/0101/secrets-management/) - Authenticate to your registry safely

### Character Class Recommendations

**💻 Software Developer**: Continue to [Workflow Optimization](/quests/0101/workflow-optimization/)  
**🏗️ System Engineer**: Explore [Deployment Pipelines](/quests/0101/deployment-pipelines/)  
**🛡️ Security Specialist**: Check out [Secrets Management](/quests/0101/secrets-management/)

## 📚 Resources

### Official Documentation
- [GitHub Actions: Storing workflow artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts) - upload/download artifacts
- [GitHub: Build provenance attestations](https://docs.github.com/en/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds) - signed provenance
- [Semantic Versioning 2.0.0](https://semver.org/) - The MAJOR.MINOR.PATCH spec

### Community Resources
- [SLSA: Supply-chain Levels for Software Artifacts](https://slsa.dev/) - Provenance framework
- [Syft (SBOM generator)](https://github.com/anchore/syft) - Generate SBOMs
- [Grype (vulnerability scanner)](https://github.com/anchore/grype) - Scan SBOMs and images

### Learning Materials
- [Sigstore / cosign](https://www.sigstore.dev/) - Keyless artifact signing
- [SPDX SBOM standard](https://spdx.dev/) - A common SBOM format

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Published a versioned, immutable artifact
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0101 - CI/CD & DevOps]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Requires:** [[CI/CD Fundamentals: Continuous Integration and Continuous Deployment Essentials]]
**Unlocks:** [[Workflow Optimization: Caching Strategies and Pipeline Parallelization]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
