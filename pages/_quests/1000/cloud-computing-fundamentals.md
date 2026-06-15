---
title: 'Cloud Computing Fundamentals: IaaS, PaaS, and SaaS Explained'
author: IT-Journey Team
description: Master cloud computing fundamentals - the IaaS, PaaS, and SaaS service models, regions and availability zones, the shared responsibility model, and the core services every provider offers.
excerpt: Understand cloud service models, regions and availability zones, shared responsibility, and the core building blocks of every cloud provider
preview: images/previews/cloud-computing-fundamentals-iaas-paas-quest-title.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1000'
difficulty: 🟡 Medium
estimated_time: 75-105 minutes
primary_technology: cloud
quest_type: main_quest
quest_series: Cloud Journey
quest_line: The Warrior's Skybridge
quest_arc: Foundations of the Cloud Realm
quest_dependencies:
  required_quests: []
  recommended_quests: []
  unlocks_quests:
  - /quests/1000/aws-essentials/
  - /quests/1000/infrastructure-as-code/
  - /quests/1000/azure-ascension-jekyll-deployment/
  - /quests/1001/kubernetes-fundamentals/
skill_focus: cloud
learning_style: conceptual
prerequisites:
  knowledge_requirements:
  - Basic command line navigation
  - General understanding of how servers, networks, and the internet work
  - Familiarity with the idea of a web application talking to a server
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - A web browser and a free-tier account with one cloud provider (optional but recommended)
  skill_level_indicators:
  - Comfortable reading technical diagrams and following step-by-step instructions
  - Ready to reason about trade-offs rather than memorize a single right answer
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A one-page comparison of IaaS, PaaS, and SaaS for a workload you choose
  skill_demonstrations:
  - Can place a given service into the correct IaaS / PaaS / SaaS tier
  - Can explain who is responsible for what under the shared responsibility model
  knowledge_checks:
  - Understands the difference between a region and an availability zone
  - Can describe why multi-AZ deployment improves availability
permalink: /quests/1000/cloud-computing-fundamentals/
categories:
- Quests
- Cloud-Engineering
- Medium
tags:
- '1000'
- cloud
- main_quest
- cloud-engineering
- conceptual
- gamified-learning
keywords:
  primary:
  - '1000'
  - cloud
  - main_quest
  secondary:
  - iaas-paas-saas
  - shared-responsibility
  - regions-availability-zones
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1000 (8) Quest: Main Quest - Cloud Fundamentals'
rewards:
  badges:
  - 🏆 Skywalker - Internalized the cloud service models
  - ☁️ Keeper of the Shared Pact - Understands the shared responsibility model
  skills_unlocked:
  - 🛠️ Cloud Service Model Selection
  - 🧠 Region and Availability-Zone Architecture
  progression_points: 75
  unlocks_features:
  - Access to the hands-on AWS, Terraform, and Azure quests of Level 1000
layout: quest
---
*Greetings, brave adventurer! You have crossed the threshold into the **Warrior tier**, and a vast new realm opens above you - the **Cloud**. Where earlier quests taught you to build kingdoms on a single machine, this realm teaches you to summon computing power from a sky of shared, on-demand resources that span the whole planet. This quest, **Cloud Computing Fundamentals**, is the map you study before you ever cast a spell in someone else's datacenter.*

*Whether you have never touched a cloud console or you have clicked through one without truly understanding what you were renting, this adventure forges the mental model every cloud Warrior needs: the three service models, the geography of regions and availability zones, the shared responsibility pact, and the core services that appear - under different names - in every provider's kingdom.*

## 📖 The Legend Behind This Quest

*In the old age of computing, every guild ran its own datacenter - racks of humming iron that had to be bought months in advance, cooled, patched, and guarded. To launch a new venture you first had to predict, fund, and assemble an army of servers, and woe to the guild that guessed wrong. Too few machines and your castle fell under load; too many and your gold drained into idle silicon.*

*Then came the cloud: providers built planet-spanning datacenters and rented their capacity by the minute. Suddenly a single adventurer could conjure a hundred servers in seconds and dismiss them just as fast, paying only for what they used. This quest teaches you the "why" behind that power - so that when you provision real infrastructure in the quests ahead, you understand exactly what you are renting, where it lives, and who is responsible when something breaks.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **The Three Service Models** - Explain IaaS, PaaS, and SaaS and place real services into each tier
- [ ] **Regions and Availability Zones** - Describe how providers structure the globe and why it matters for latency and resilience
- [ ] **The Shared Responsibility Model** - State precisely who secures what between you and the provider
- [ ] **Core Cloud Service Categories** - Recognize compute, storage, networking, and database services across providers

### Secondary Objectives (Bonus Achievements)
- [ ] **Deployment Models** - Distinguish public, private, hybrid, and multi-cloud
- [ ] **The Economics of Elasticity** - Explain pay-as-you-go, on-demand vs. reserved capacity, and why elasticity changes cost decisions
- [ ] **Provider Translation** - Map equivalent services across AWS, Azure, and Google Cloud

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Sort a list of unfamiliar products into IaaS, PaaS, or SaaS with confidence
- [ ] Explain to a teammate why you would deploy across multiple availability zones
- [ ] Decide who is at fault for a misconfigured storage bucket - you or the provider
- [ ] Recommend a service model for a new project and defend the trade-off

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Basic understanding of how a web request reaches a server
- [ ] Comfort using a terminal and a web browser
- [ ] No prior cloud experience required - this is the on-ramp

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] A web browser
- [ ] Optional: a free-tier account on AWS, Azure, or Google Cloud to explore a real console

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You have built or run at least one small application on a single machine
- [ ] You are ready to reason about trade-offs, not just memorize definitions
- [ ] Ready for 75-105 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*This quest is mostly conceptual, but exploring a real cloud console cements the ideas. Each major provider offers a free tier and a command-line tool you can install. Pick the kingdom you want to explore.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install the CLI for the provider you want to explore (pick one or more)
brew install awscli              # Amazon Web Services
brew install azure-cli           # Microsoft Azure
brew install --cask google-cloud-sdk  # Google Cloud

# Verify your chosen tool is installed
aws --version
az version
gcloud version
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install via winget (pick the provider you want to explore)
winget install Amazon.AWSCLI
winget install Microsoft.AzureCLI
winget install Google.CloudSDK

# Verify installation
aws --version
az version
gcloud version
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# AWS CLI v2 (works on most distributions)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip
unzip awscliv2.zip && sudo ./aws/install

# Azure CLI (Debian/Ubuntu)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Verify
aws --version
az version
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Every provider ships a browser-based shell with the CLI pre-installed -
# no local install required:
#   AWS    -> CloudShell      (console toolbar)
#   Azure  -> Cloud Shell     (console toolbar)
#   GCP    -> Cloud Shell     (console toolbar)
# Open one and try a read-only command, e.g.:
aws sts get-caller-identity   # who am I, on AWS?
```

</details>

## 🧙‍♂️ Chapter 1: The Three Service Models - IaaS, PaaS, and SaaS

*Every cloud offering sits somewhere on a ladder of abstraction. The higher you climb, the more the provider manages for you - and the less control you retain. Master this ladder and you have a lens for the entire cloud.*

### ⚔️ Skills You'll Forge in This Chapter
- The meaning of Infrastructure, Platform, and Software as a Service
- How much of the stack each model hands to the provider
- How to place a real product into the right tier

### 🏗️ The Ladder of Abstraction

A useful way to think about it: with traditional on-premises hosting, *you* manage everything from the building to the application. Each service model hands more of that stack to the provider.

| Layer (top = your app) | On-Premises | IaaS | PaaS | SaaS |
| --- | --- | --- | --- | --- |
| Application / Data | You | You | You | Provider |
| Runtime / Middleware | You | You | Provider | Provider |
| OS / Virtualization | You | Provider | Provider | Provider |
| Servers / Storage / Network | You | Provider | Provider | Provider |
| Datacenter / Power / Cooling | You | Provider | Provider | Provider |

- **IaaS (Infrastructure as a Service)** rents you raw virtual machines, disks, and networks. You install the OS, patch it, and run whatever you like. *Examples: AWS EC2, Azure Virtual Machines, Google Compute Engine.* Maximum control, maximum responsibility.
- **PaaS (Platform as a Service)** gives you a managed runtime - push your code and the platform handles the OS, scaling, and patching. *Examples: AWS Elastic Beanstalk, Azure App Service, Google App Engine, Heroku.* Less control, far less toil.
- **SaaS (Software as a Service)** is finished software you simply use through a browser. You manage only your data and settings. *Examples: Gmail, Microsoft 365, Salesforce, Dropbox.*

A handy analogy is pizza: on-premises is making it from scratch in your own kitchen; IaaS is take-and-bake (they supply the kitchen, you cook); PaaS is delivery (you supply the table); SaaS is dining out (you just eat).

```text
Sorting practice — place each product into a tier:
  "I rent a bare Ubuntu VM and install my own database"  -> IaaS
  "I 'git push' and the platform runs my Node app"       -> PaaS
  "My team uses Salesforce in the browser"               -> SaaS
  "A managed PostgreSQL I connect to but never patch"    -> PaaS (managed service)
```

### 🔍 Knowledge Check: Service Models
- [ ] Who patches the operating system under IaaS vs. PaaS?
- [ ] Why might a small team prefer PaaS over IaaS for a first launch?
- [ ] What is the only layer you manage under SaaS?

### ⚡ Quick Wins and Checkpoints
- [ ] **Sorted three products**: You placed three real services into the correct tier
- [ ] **Explained the trade-off**: You stated what you gain and lose climbing the ladder

## 🧙‍♂️ Chapter 2: Geography of the Cloud - Regions and Availability Zones

*The cloud is not a vague mist - it is concrete buildings full of servers, scattered across the planet. How a provider organizes that geography determines your latency, your resilience, and even which laws govern your data.*

### ⚔️ Skills You'll Forge in This Chapter
- The difference between a region and an availability zone
- Why you deploy across multiple zones
- How geography affects latency, resilience, and compliance

### 🏗️ Regions, Zones, and Edge Locations

- A **region** is a geographic area (e.g., `us-east-1` in Virginia, `eu-west-1` in Ireland). You choose a region to be close to your users, to meet data-residency laws, or to control cost.
- An **availability zone (AZ)** is one or more discrete datacenters *within* a region, each with independent power, cooling, and networking. A single region typically has three or more AZs, isolated enough that a fire or flood in one will not take down another.
- An **edge location** (or point of presence) is a smaller site, far more numerous than regions, used by content delivery networks to cache data close to users.

The golden rule of resilience: **deploy across multiple availability zones**. If your app runs in only one AZ and that datacenter loses power, you are down. Spread identical copies across two or three AZs behind a load balancer, and the failure of any single zone barely registers.

```bash
# Ask AWS which availability zones exist in a region
aws ec2 describe-availability-zones \
  --region us-east-1 \
  --query "AvailabilityZones[].ZoneName" \
  --output table

# Expected output: a table listing us-east-1a, us-east-1b, us-east-1c, ...
```

Choosing a region is a real engineering decision. Pick one far from your users and every request pays a latency tax measured in tens of milliseconds. Store EU citizens' data outside the EU and you may violate GDPR. Geography is not a detail - it is architecture.

### 🔍 Knowledge Check: Cloud Geography
- [ ] What independent resources does each availability zone have?
- [ ] Why does deploying to two AZs improve availability over one?
- [ ] Name two reasons - other than latency - to choose a particular region.

### ⚡ Quick Wins and Checkpoints
- [ ] **Listed real AZs**: You queried or looked up the zones in one region
- [ ] **Justified multi-AZ**: You explained why one zone is not enough for production

## 🧙‍♂️ Chapter 3: The Shared Responsibility Pact and the Core Services

*Moving to the cloud does not make security someone else's problem - it splits the problem in two. And underneath every provider's hundreds of products lie the same four building blocks. Learn the split and the blocks, and any cloud console becomes legible.*

### ⚔️ Skills You'll Forge in This Chapter
- Exactly who secures what under the shared responsibility model
- The four core service categories every provider offers
- How equivalent services map across AWS, Azure, and GCP

### 🏗️ The Shared Responsibility Model

Cloud providers draw a famous line: they are responsible for the security **of** the cloud, and you are responsible for security **in** the cloud.

| The provider secures... | You secure... |
| --- | --- |
| Physical datacenters and hardware | Your data and how it is classified |
| The host hypervisor and network fabric | Operating-system patches (on IaaS) and configuration |
| Managed-service infrastructure | Identity, access management, and credentials |
| Global infrastructure availability | Network and firewall rules you define |

The line **moves with the service model**: under IaaS you patch the guest OS; under PaaS the provider does, but you still own your code and data; under SaaS you own essentially only your data and account settings. The most common breaches are not the provider failing - they are a customer leaving a storage bucket world-readable or a credential checked into a public repository. Those are squarely on your side of the line.

### 🏗️ The Four Core Service Categories

Strip away the marketing and every provider sells the same four primitives:

```text
Compute   — run code: virtual machines, containers, serverless functions
            AWS EC2 / Lambda  |  Azure VMs / Functions  |  GCP Compute Engine / Cloud Functions
Storage   — keep bytes: object stores, block disks, file shares
            AWS S3 / EBS      |  Azure Blob / Disk      |  GCP Cloud Storage / Persistent Disk
Networking— connect things: virtual networks, load balancers, DNS, CDN
            AWS VPC / ELB      |  Azure VNet / Load Bal. |  GCP VPC / Cloud Load Balancing
Database  — managed data: relational and NoSQL engines run for you
            AWS RDS / DynamoDB |  Azure SQL / Cosmos DB  |  GCP Cloud SQL / Firestore
```

Once you can name the category a service belongs to, you can learn any new product by asking a single question: which of the four primitives is this, and what does it manage for me?

### 🔍 Knowledge Check: Responsibility and Building Blocks
- [ ] If an S3 bucket is left public and data leaks, whose responsibility is it?
- [ ] Name the four core service categories and one AWS service in each.
- [ ] How does the responsibility line shift between IaaS and SaaS?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Sort the Service Zoo
**Objective**: Given a list of ten real cloud products (mix of EC2, Lambda, S3, Gmail, App Service, Salesforce, RDS, Dropbox, Compute Engine, Heroku), classify each as IaaS, PaaS, or SaaS.

**Requirements**:
- [ ] Every product placed in a tier
- [ ] One sentence of justification per item
- [ ] At least one "managed service" correctly identified as PaaS-like

**Validation**: You can defend each placement using the ladder-of-abstraction table.

### 🟡 Intermediate Challenge: Design for Resilience
**Objective**: Sketch a deployment for a small web app that survives the loss of an entire availability zone.

**Requirements**:
- [ ] Choose a region and justify it (users, latency, compliance)
- [ ] Place application instances across at least two AZs
- [ ] Add a load balancer and a managed database, noting which AZ pattern each uses
- [ ] Mark which single failure your design now survives

**Validation**: Removing any one AZ from your diagram still leaves a serving path.

### 🔴 Advanced Challenge: Map the Three Kingdoms
**Objective**: Build a translation table mapping ten services across AWS, Azure, and Google Cloud, grouped by the four core categories.

**Requirements**:
- [ ] At least two services per core category
- [ ] The correct equivalent named in all three providers
- [ ] A note on one place where the mapping is imperfect (services that do not line up cleanly)

**Validation**: A teammate could use your table to find the equivalent service in an unfamiliar provider.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Skywalker** - You internalized the IaaS / PaaS / SaaS ladder
- ☁️ **Keeper of the Shared Pact** - You can divide responsibility between provider and customer

**🛠️ Skills Unlocked**:
- **Cloud Service Model Selection** - Choose the right abstraction for a workload
- **Region and Availability-Zone Architecture** - Design for latency and resilience

**🔓 Unlocked Quests**:
- AWS Essentials - Get hands-on with IAM, EC2, S3, and the VPC
- Infrastructure as Code - Provision all of this declaratively with Terraform
- Azure Ascension - Deploy a real site to a managed cloud platform

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [AWS Essentials](/quests/1000/aws-essentials/) - Turn these concepts into real provisioned services

**Explore Side Adventures**:
- ⚔️ [Infrastructure as Code](/quests/1000/infrastructure-as-code/) - Define cloud resources in version-controlled code
- ⚔️ [Azure Ascension](/quests/1000/azure-ascension-jekyll-deployment/) - Ship a site to a managed platform

### Character Class Recommendations

**💻 Software Developer**: Continue to [AWS Essentials](/quests/1000/aws-essentials/)  
**🏗️ System Engineer**: Explore [Infrastructure as Code](/quests/1000/infrastructure-as-code/)  
**🛡️ Security Specialist**: Revisit the shared responsibility model before [AWS Essentials](/quests/1000/aws-essentials/)

## 📚 Resources

### Official Documentation
- [AWS - Types of Cloud Computing](https://aws.amazon.com/types-of-cloud-computing/) - IaaS, PaaS, SaaS from a major provider
- [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) - The canonical responsibility diagram
- [AWS Global Infrastructure: Regions and Availability Zones](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/) - How the geography is structured
- [Microsoft Azure - What is Cloud Computing?](https://azure.microsoft.com/en-us/resources/cloud-computing-dictionary/what-is-cloud-computing/) - Provider-neutral primer

### Community Resources
- [NIST Definition of Cloud Computing (SP 800-145)](https://csrc.nist.gov/pubs/sp/800/145/final) - The standards-body definition of the service and deployment models
- [Google Cloud - Geography and Regions](https://cloud.google.com/docs/geography-and-regions) - A second provider's view of regions and zones

### Learning Materials
- [Microsoft Learn: Cloud Concepts](https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/) - Free, structured fundamentals path
- [AWS Cloud Practitioner Essentials](https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/) - Free foundational course

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Sorted real services into IaaS, PaaS, and SaaS
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1000 (8) - Cloud Computing]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Unlocks:** [[AWS Essentials: Core Services and Cloud Architecture Patterns]] · [[Infrastructure as Code: Terraform and CloudFormation Fundamentals]] · [[Azure Ascension: Deploying Jekyll to the Cloud Kingdom]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
