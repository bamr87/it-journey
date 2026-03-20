---
title: 'Hello Cloud: First Steps into the Sky Realm'
description: Create your first cloud account, install a cloud CLI, and deploy a simple resource safely.
author: IT-Journey Team
date: 2026-01-14
lastmod: 2026-01-14
level: '0000'
difficulty: ⚔️ Epic
estimated_time: 120-180 minutes
primary_technology: cloud
quest_type: main_quest
quest_series: Init World - Platform Mastery
quest_line: Foundation Path
quest_arc: Platform Mastery Arc
quest_dependencies:
  required_quests:
  - /quests/lvl_000/it-fundamentals/
  recommended_quests:
  - /quests/lvl_000/os-selection/
  unlocks_quests: []
quest_relationships:
  child_quests: []
  sequel_quests: []
  parallel_quests:
  - /quests/hello-windows/
  - /quests/hello-macos/
  - /quests/hello-linux/linux-fundamentals/
learning_paths:
  primary_paths:
  - Cloud Computing
  - DevOps
  - System Administration
  character_classes:
  - ☁️ Cloud Engineer
  - 🏗️ System Engineer
  - 💻 Software Developer
  skill_trees:
  - Cloud Fundamentals
  - CLI Mastery
skill_focus:
- cloud-fundamentals
- account-setup
- cli-tools
- security-basics
learning_style: hands-on
permalink: /quests/hello-cloud/
categories:
- Quests
- Init-World
- Cloud
- Development-Environment
tags:
- cloud
- aws
- azure
- gcp
- cli
- init-world
keywords:
- cloud
- account-setup
- cli
- gcp
- aws
- azure
fmContentType: quest
prerequisites:
  knowledge_requirements:
  - Basic command-line usage
  - Understanding of accounts and billing dashboards
  system_requirements:
  - Stable internet connection
  - Email and phone number for cloud signup
  - Terminal access (bash or PowerShell)
  skill_level_indicators:
  - Comfortable installing CLI tools and following web-based setup guides
validation_criteria:
  completion_requirements:
  - Successfully create a cloud account with MFA enabled
  - Install and authenticate a cloud CLI
  - Deploy at least one cloud resource
  - Tear down resources to avoid cost leaks
  skill_demonstrations:
  - Can authenticate via cloud CLI
  - Can provision and destroy basic cloud resources
  knowledge_checks:
  - Understands free-tier limits and billing alerts
  - Knows the difference between major cloud providers
rewards:
  badges:
  - 🏆 Cloud Explorer Badge
  - ⚡ Sky Realm Entry Achievement
  skills_unlocked:
  - 🛠️ Cloud CLI Proficiency
  - 🎯 Resource Provisioning Basics
  progression_points: 100
  unlocks_features:
  - Access to advanced cloud quests
  - Foundation for infrastructure-as-code learning
draft: false
---
*Welcome, skybound adventurer! You stand at the edge of the mortal realm, gazing up at the shimmering **Sky Realm** — a vast kingdom of infinite compute power, boundless storage vaults, and magical services that can scale from a whisper to a thunderclap. Today, you claim your first foothold in the clouds.*

*But beware: the Sky Realm's resources carry a cost. Careless adventurers have been bankrupted by forgotten resources left running in the mist. This quest teaches you to explore safely, provision wisely, and always clean up after your experiments.*

## 🎯 Quest Objectives

### Primary Objectives (Required for Quest Completion)
- [ ] **Claim Your Sky Realm Passport** — Create a cloud account with proper security wards (MFA)
- [ ] **Forge Your Cloud Wand (CLI)** — Install and authenticate a cloud command-line interface
- [ ] **Summon Your First Cloud Creature** — Provision a minimal VM or storage artifact
- [ ] **Banish Your Creation** — Destroy all resources to prevent gold drain (cost leaks)

### Bonus Objectives (Optional Achievements)
- [ ] Activate protective wards: MFA and billing alerts
- [ ] Scout the free-tier treasure map and catalog available services

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Basic command-line incantations (terminal usage)
- [ ] Familiarity with realm registries (accounts and billing dashboards)

### 🛠️ System Requirements
- [ ] Stable portal connection (internet)
- [ ] Communication crystal (email + phone) for cloud signup

## 🌍 Choose Your Sky Kingdom

Each Sky Kingdom offers unique powers. Pick one for your first expedition — you can explore others later on your journey.

| Kingdom | Strengths | Best For |
|---------|-----------|----------|
| **AWS** | Vast army of services, battle-tested | General-purpose cloud mastery |
| **Azure** | Strong Microsoft alliance, enterprise fortifications | Windows-integrated workflows |
| **GCP** | Elegant developer tools, powerful data magic | Data science and clean APIs |

This quest includes GCP helper scrolls (scripts) for a low-friction first adventure.

## 🧙‍♂️ Chapter 1: Account Setup & Protective Wards

Every wise cloud mage secures their realm before summoning resources:

1. **Create your account** with your chosen Sky Kingdom provider.
2. **Enable MFA** — your first defensive ward against intruders.
3. **Set a billing alert** — an alarm spell that warns you before gold is spent.
4. **Review free-tier limits** — know what treasures you can summon without cost.

## 🧰 Chapter 2: Forge Your Cloud Wand (CLI Installation)

The Cloud CLI is your wand — the tool through which you channel commands to the Sky Realm.

From this quest directory, review and run the helper scrolls (GCP example):

```bash
./gcp/gcp-start.sh
./gcp/gcloud-cs.sh
```

Verify your wand is attuned (authenticated):

```bash
gcloud auth list
gcloud config list
```

## ⚔️ Chapter 3: Summon Your First Cloud Creature

Time to test your power! Summon a tiny VM using the provided incantation script:

```bash
./gcp/vm-startup.sh
```

Validate that your creature has materialized and is running in the Sky Realm.

## 🧹 Chapter 4: Banish & Clean Up

*A careless mage leaves creatures roaming the clouds, draining gold with every passing hour.* Always banish what you summon:

```bash
gcloud compute instances list
gcloud compute instances delete <instance-name>
```

If you conjured other artifacts (storage buckets, networks), banish them now to avoid surprise charges.

## 🏁 Quest Completion Checklist

- [ ] Cloud account created with MFA ward activated
- [ ] Billing alert spell configured
- [ ] Cloud CLI wand forged and authenticated
- [ ] Cloud creature summoned and then properly banished

## 📚 References & Resources

- [AWS Free Tier](https://aws.amazon.com/free/)
- [Azure Free Account](https://azure.microsoft.com/free/)
- [GCP Free Tier](https://cloud.google.com/free)
- [Google Cloud CLI Documentation](https://cloud.google.com/sdk/docs)
- [AWS CLI Getting Started](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)

## 🔗 Related Quests

- [Hello n00b](../hello-noob.md)
- [OS Selection](../os-selection.md)
- [Hello Windows](../hello-win/hello-win.md)
- [Hello macOS](../hello-mac/hello-mac.md)
- [Hello Linux](../hello-linux/linux-fundamentals.md)
