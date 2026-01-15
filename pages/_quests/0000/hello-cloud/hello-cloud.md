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
skill_focus:
- cloud-fundamentals
- account-setup
- cli-tools
- security-basics
learning_style: hands-on
layout: journals
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
draft: false
---
*Welcome, skybound adventurer! This quest sets up your first cloud account, installs a cloud CLI, and teaches safe, low-cost exploration techniques so you can start building without surprise bills.*

## 🎯 Quest Objectives

### Primary Objectives (Required for Quest Completion)
- [ ] **Create a Cloud Account** - Choose AWS, Azure, or GCP
- [ ] **Install a Cloud CLI** - Authenticate and verify your access
- [ ] **Deploy a Tiny Resource** - Provision a minimal VM or storage bucket
- [ ] **Tear It Down Safely** - Avoid cost leaks by cleaning up

### Bonus Objectives (Optional)
- [ ] Remember to enable MFA and alerts
- [ ] Explore free-tier services and limits

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Basic command-line usage
- [ ] Familiarity with accounts and billing dashboards

### 🛠️ System Requirements
- [ ] Stable internet connection
- [ ] Email + phone number for cloud signup

## 🌍 Choose Your Adventure Platform

Pick one provider for your first run. You can expand later.

- **AWS**: Great general-purpose cloud with rich services
- **Azure**: Strong Microsoft ecosystem + enterprise focus
- **GCP**: Clean developer experience + strong data tooling

This quest includes GCP helper scripts for a low-friction start.

## 🧙‍♂️ Chapter 1: Account Setup & Safety

1. Create your account in your chosen provider.
2. Enable **MFA** and set a **billing alert**.
3. Confirm free-tier services and limits.

## 🧰 Chapter 2: Install a Cloud CLI (GCP Example)

From this directory, review and run the helper scripts:

```bash
./gcp/gcp-start.sh
./gcp/gcloud-cs.sh
```

Verify authentication:

```bash
gcloud auth list
gcloud config list
```

## ⚔️ Chapter 3: Launch a Tiny Resource

Use the provided VM startup script (GCP example):

```bash
./gcp/vm-startup.sh
```

Validate that the VM is created and running.

## 🧹 Chapter 4: Tear Down & Clean Up

Always remove the resources you created:

```bash
gcloud compute instances list
gcloud compute instances delete <instance-name>
```

If you created other resources, remove them now to avoid charges.

## 🏁 Quest Completion Checklist

- [ ] Cloud account created with MFA enabled
- [ ] Billing alerts configured
- [ ] CLI installed and authenticated
- [ ] Small resource created and deleted

## 🔗 Related Quests

- [Hello n00b](../hello-noob.md)
- [OS Selection](../os-selection.md)
- [Hello Windows](../hello-win/hello-win.md)
- [Hello macOS](../hello-mac/hello-mac.md)
- [Hello Linux](../hello-linux/linux-fundamentals.md)
