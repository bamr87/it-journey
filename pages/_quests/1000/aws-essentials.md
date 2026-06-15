---
title: 'AWS Essentials: Core Services and Cloud Architecture Patterns'
author: IT-Journey Team
description: Get hands-on with the core of AWS - IAM identities and policies, launching an EC2 instance, storing objects in S3, the building blocks of a VPC, the AWS CLI, and the Well-Architected Framework.
excerpt: Master the foundational AWS services - IAM, EC2, S3, VPC, and the AWS CLI - and the Well-Architected pillars
preview: images/previews/aws-essentials-core-services-quest-title-architect.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1000'
difficulty: 🔴 Hard
estimated_time: 120-150 minutes
primary_technology: aws
quest_type: main_quest
quest_series: Cloud Journey
quest_line: The Warrior's Skybridge
quest_arc: The AWS Citadel
quest_dependencies:
  required_quests:
  - /quests/1000/cloud-computing-fundamentals/
  recommended_quests:
  - /quests/1000/cloud-computing-fundamentals/
  unlocks_quests:
  - /quests/1000/infrastructure-as-code/
  - /quests/1001/kubernetes-fundamentals/
skill_focus: cloud
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Comfort with the terminal and basic shell commands
  - Understanding of cloud service models (complete Cloud Computing Fundamentals first)
  - Basic understanding of IP addresses and how a server listens on a port
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - An AWS account (the Free Tier covers everything in this quest)
  - The AWS CLI v2 installed and configured
  skill_level_indicators:
  - Ready to work in a live cloud console and clean up resources afterward
  - Comfortable reading JSON policy documents
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - An EC2 instance launched and then terminated, and an S3 bucket created and emptied
  skill_demonstrations:
  - Can create an IAM user with a least-privilege policy
  - Can launch, connect to, and terminate an EC2 instance from the CLI
  knowledge_checks:
  - Understands the difference between a security group and a subnet
  - Can name the pillars of the Well-Architected Framework
permalink: /quests/1000/aws-essentials/
categories:
- Quests
- Cloud-Engineering
- Hard
tags:
- '1000'
- aws
- main_quest
- cloud-engineering
- hands-on
- gamified-learning
keywords:
  primary:
  - '1000'
  - aws
  - main_quest
  secondary:
  - iam-ec2-s3-vpc
  - aws-cli
  - well-architected
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1000 (8) Quest: Main Quest - AWS Essentials'
rewards:
  badges:
  - 🏆 Citadel Initiate - Provisioned your first real AWS resources
  - 🗝️ Keymaster of IAM - Built least-privilege identities and policies
  skills_unlocked:
  - 🛠️ EC2 and S3 Provisioning
  - 🧠 VPC Network Reasoning
  progression_points: 100
  unlocks_features:
  - Access to the Infrastructure as Code quest, where you automate all of this
layout: quest
---
*Welcome to the Citadel, cloud Warrior. You have studied the map of the realm in **Cloud Computing Fundamentals** - now you set foot inside the largest kingdom of all: **Amazon Web Services**. Here you will not merely read about compute and storage; you will summon a running server, store treasure in an object vault, forge keys of identity, and learn the network walls that keep the kingdom safe.*

*This is a 🔴 Hard quest because it is hands-on with a live account that bills real money. Every spell you cast here, you will also dispel - launching and then terminating, creating and then deleting - so that you finish owing nothing. By the end you will have touched the four pillars every AWS architect stands on: **IAM, EC2, S3, and the VPC**, all driven from the **AWS CLI**, and judged against the **Well-Architected Framework**.*

## 📖 The Legend Behind This Quest

*AWS began in 2006 when Amazon realized the infrastructure it had built to run the world's largest store could be rented to everyone. Today it is the most widely used cloud, and its core services have become a shared vocabulary across the industry - even engineers on other clouds reason in terms of "the EC2 equivalent" or "an S3-like store."*

*Master these essentials and you hold the keys to that vocabulary. The quest teaches not just which buttons to press, but the "why" - why an instance lives inside a subnet, why a security group is not a firewall in the old sense, and why least privilege is the first law of the cloud.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **IAM Identities and Policies** - Create users, groups, roles, and least-privilege policies
- [ ] **EC2 Compute** - Launch, connect to, and terminate a virtual server from the CLI
- [ ] **S3 Object Storage** - Create a bucket, upload and download objects, and lock down access
- [ ] **VPC Networking Basics** - Explain subnets, route tables, internet gateways, and security groups

### Secondary Objectives (Bonus Achievements)
- [ ] **The AWS CLI** - Configure profiles and drive AWS entirely from the terminal
- [ ] **Well-Architected Thinking** - Apply the six pillars to a design decision
- [ ] **Cost Hygiene** - Tag resources and tear everything down to avoid charges

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Write an IAM policy that grants only the actions a task needs
- [ ] Launch and terminate an EC2 instance without touching the web console
- [ ] Explain why a public subnet needs an internet gateway and a route to it
- [ ] Name the Well-Architected pillars and give one practice from each

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Completion of [Cloud Computing Fundamentals](/quests/1000/cloud-computing-fundamentals/) (strongly recommended)
- [ ] Comfort with the terminal and editing files
- [ ] Basic understanding of IP addresses, ports, and SSH

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] An AWS account - the [Free Tier](https://aws.amazon.com/free/) covers this quest
- [ ] The AWS CLI v2 installed
- [ ] An SSH client (built into macOS/Linux; use OpenSSH or PuTTY on Windows)

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You are comfortable working in a live account that can incur charges
- [ ] You will diligently clean up every resource you create
- [ ] Ready for 120-150 minutes of focused, hands-on work

## 🌍 Choose Your Adventure Platform

*All you truly need is the AWS CLI and an account. Install the CLI for your OS, then configure it once.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install the AWS CLI v2
brew install awscli
aws --version   # expect aws-cli/2.x

# Configure credentials (create an access key in the IAM console first)
aws configure
# AWS Access Key ID:     <your key>
# AWS Secret Access Key: <your secret>
# Default region name:   us-east-1
# Default output format:  json
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install via winget
winget install Amazon.AWSCLI
aws --version

# Configure credentials
aws configure
# Provide your access key, secret, region (us-east-1), and json output
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip
unzip awscliv2.zip && sudo ./aws/install
aws --version

aws configure   # enter key, secret, region us-east-1, json
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# AWS CloudShell has the CLI pre-installed and pre-authenticated.
# Open it from the console toolbar and confirm your identity:
aws sts get-caller-identity
```

</details>

## 🧙‍♂️ Chapter 1: IAM - The Keys to the Kingdom

*Before you provision anything, you must answer: who are you, and what may you do? AWS Identity and Access Management (IAM) governs every action in the account. Get IAM right and the rest of the kingdom is defensible; get it wrong and a single leaked key can burn it down.*

### ⚔️ Skills You'll Forge in This Chapter
- The IAM vocabulary: users, groups, roles, and policies
- Writing a least-privilege policy
- Why roles beat long-lived access keys

### 🏗️ Identities and Policies

IAM has four core nouns:

- **Users** - a human or application identity with long-term credentials.
- **Groups** - a collection of users that share permissions (e.g., `developers`).
- **Roles** - an identity with *temporary* credentials that an entity can assume (an EC2 instance, a Lambda function, or a user from another account). Prefer roles over keys.
- **Policies** - JSON documents that grant or deny specific actions on specific resources.

The first law of the cloud is **least privilege**: grant only the actions a task needs. Here is a policy that lets a principal read from one S3 bucket and nothing else:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadOneBucket",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::my-quest-bucket",
        "arn:aws:s3:::my-quest-bucket/*"
      ]
    }
  ]
}
```

Create a group, attach a managed policy, and add a user from the CLI:

```bash
# Create a group and attach the AWS-managed read-only policy
aws iam create-group --group-name quest-readers
aws iam attach-group-policy \
  --group-name quest-readers \
  --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess

# Create a user and place it in the group
aws iam create-user --user-name quest-apprentice
aws iam add-user-to-group --user-name quest-apprentice --group-name quest-readers

# Confirm the user's group membership
aws iam list-groups-for-user --user-name quest-apprentice
```

> ⚠️ Never embed root account keys in code, and enable MFA on the root user. Day-to-day work should use IAM users or roles, never root.

### 🔍 Knowledge Check: IAM
- [ ] What is the difference between a user and a role?
- [ ] What does the `Effect: Allow` / `Deny` field control in a policy?
- [ ] Why is an IAM role safer for an EC2 instance than a stored access key?

### ⚡ Quick Wins and Checkpoints
- [ ] **Group created**: You created a group and attached a policy
- [ ] **Least privilege written**: You can read the read-only policy and say what it grants

## 🧙‍♂️ Chapter 2: EC2 and S3 - Compute and Storage

*With identity in hand, summon the two workhorses of AWS: an EC2 virtual server and an S3 object store.*

### ⚔️ Skills You'll Forge in This Chapter
- Launching and terminating an EC2 instance from the CLI
- Creating an S3 bucket and moving objects in and out
- Locking down public access on storage

### 🏗️ Launching an EC2 Instance

EC2 (Elastic Compute Cloud) rents virtual machines by the second. To launch one you need a key pair (for SSH), an AMI (a machine image), and an instance type (the size). The `t2.micro` / `t3.micro` types are Free-Tier eligible.

```bash
# 1. Create an SSH key pair and save the private key locally
aws ec2 create-key-pair --key-name quest-key \
  --query 'KeyMaterial' --output text > quest-key.pem
chmod 400 quest-key.pem

# 2. Launch a Free-Tier Amazon Linux 2023 instance
aws ec2 run-instances \
  --image-id resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
  --instance-type t3.micro \
  --key-name quest-key \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=quest-server}]' \
  --query 'Instances[0].InstanceId' --output text

# 3. When finished, ALWAYS terminate to stop billing
aws ec2 terminate-instances --instance-ids <instance-id>
```

### 🏗️ Storing Objects in S3

S3 (Simple Storage Service) holds objects (files) inside buckets, with effectively unlimited capacity and 11 nines of durability.

```bash
# Create a bucket (names are globally unique - add randomness)
aws s3 mb s3://my-quest-bucket-$RANDOM

# Upload and download an object
echo "treasure" > loot.txt
aws s3 cp loot.txt s3://my-quest-bucket-12345/
aws s3 cp s3://my-quest-bucket-12345/loot.txt downloaded-loot.txt

# Block ALL public access (the safe default for almost every bucket)
aws s3api put-public-access-block \
  --bucket my-quest-bucket-12345 \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Clean up: empty and delete the bucket
aws s3 rb s3://my-quest-bucket-12345 --force
```

> The single most common cloud breach is a publicly readable S3 bucket. Block public access by default and open it deliberately, never accidentally.

### 🔍 Knowledge Check: Compute and Storage
- [ ] What three things must you specify to launch an EC2 instance?
- [ ] Why must an S3 bucket name be globally unique?
- [ ] What command ensures a bucket cannot be made public?

## 🧙‍♂️ Chapter 3: The VPC and the Well-Architected Framework

*Your server does not float in the void - it lives inside a virtual network you control, the VPC. And every good design is measured against AWS's own rubric: the Well-Architected Framework.*

### ⚔️ Skills You'll Forge in This Chapter
- The anatomy of a VPC: subnets, route tables, gateways, security groups
- The six pillars of the Well-Architected Framework
- How to reason about a design, not just build it

### 🏗️ Anatomy of a VPC

A **VPC (Virtual Private Cloud)** is your own isolated network within a region, defined by a CIDR block such as `10.0.0.0/16`. Inside it:

```text
VPC  10.0.0.0/16
 ├── Public subnet   10.0.1.0/24  (in AZ us-east-1a)
 │     ├── Route table -> 0.0.0.0/0 via Internet Gateway   (reachable from the internet)
 │     └── EC2 web server, public IP
 └── Private subnet  10.0.2.0/24  (in AZ us-east-1b)
       ├── Route table -> 0.0.0.0/0 via NAT Gateway        (outbound only)
       └── Database, no public IP
```

- A **subnet** is a slice of the VPC's address range, pinned to one availability zone.
- A **route table** decides where traffic goes. A subnet is "public" because its route table sends internet-bound traffic to an **internet gateway**.
- A **security group** is a stateful, instance-level virtual firewall: you allow inbound rules (e.g., SSH on port 22 from your IP) and outbound is allowed by return. It is "deny by default" - if you do not allow it, it is blocked.

```bash
# Create a VPC and a security group that allows SSH only from your IP
aws ec2 create-vpc --cidr-block 10.0.0.0/16 \
  --query 'Vpc.VpcId' --output text

aws ec2 create-security-group \
  --group-name quest-sg --description "SSH from my IP" \
  --vpc-id <vpc-id>

aws ec2 authorize-security-group-ingress \
  --group-id <sg-id> --protocol tcp --port 22 --cidr <your-ip>/32
```

### 🏗️ The Well-Architected Framework

AWS distills good design into six pillars. Use them as a checklist for any architecture:

1. **Operational Excellence** - run and monitor systems; automate and improve.
2. **Security** - protect data and systems; apply least privilege and defense in depth.
3. **Reliability** - recover from failure; design for multi-AZ and graceful degradation.
4. **Performance Efficiency** - use resources efficiently; pick the right instance and storage type.
5. **Cost Optimization** - avoid unneeded spend; right-size, use reserved/spot, and turn things off.
6. **Sustainability** - minimize the environmental impact of your workloads.

### 🔍 Knowledge Check: Networking and Architecture
- [ ] What makes a subnet "public" rather than "private"?
- [ ] How does a security group differ from a traditional network firewall?
- [ ] Name three Well-Architected pillars and one practice from each.

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Forge an Identity
**Objective**: Create an IAM group with a least-privilege policy and add a user to it, entirely from the CLI.

**Requirements**:
- [ ] A group with an attached policy (managed or custom)
- [ ] A user added to the group
- [ ] Verify membership with `aws iam list-groups-for-user`

**Validation**: The user can perform only the actions the policy grants.

### 🟡 Intermediate Challenge: Launch and Land
**Objective**: Launch a Free-Tier EC2 instance, connect to it over SSH, then terminate it.

**Requirements**:
- [ ] Create a key pair and a security group allowing SSH from your IP only
- [ ] Launch a `t3.micro` Amazon Linux instance
- [ ] SSH in, run `uname -a`, then terminate the instance
- [ ] Confirm via `aws ec2 describe-instances` that it is terminated

**Validation**: The instance reaches `terminated` state and incurs no further charges.

### 🔴 Advanced Challenge: A Well-Architected Mini-Stack
**Objective**: Design (and optionally build) a two-subnet VPC hosting a web instance and a private datastore, then critique it against the Well-Architected pillars.

**Requirements**:
- [ ] A VPC with one public and one private subnet in different AZs
- [ ] A security group allowing only necessary ports
- [ ] An S3 bucket with public access blocked, tagged for cost tracking
- [ ] A one-paragraph review naming how your design addresses at least four pillars

**Validation**: Each design choice maps to a Well-Architected pillar, and you have torn every billable resource back down.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Citadel Initiate** - You provisioned and tore down real AWS resources
- 🗝️ **Keymaster of IAM** - You build least-privilege identities by reflex

**🛠️ Skills Unlocked**:
- **EC2 and S3 Provisioning** - Summon compute and storage from the CLI
- **VPC Network Reasoning** - Explain how cloud networks are wired

**🔓 Unlocked Quests**:
- Infrastructure as Code - Stop clicking and start declaring all of this in Terraform
- Kubernetes Fundamentals - Orchestrate containers on top of cloud compute

**📊 Progression Points**: +100 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Infrastructure as Code](/quests/1000/infrastructure-as-code/) - Provision everything you did here, declaratively and repeatably

**Explore Side Adventures**:
- ⚔️ [Azure Ascension](/quests/1000/azure-ascension-jekyll-deployment/) - See the same ideas on another cloud
- ⚔️ [Cloud Computing Fundamentals](/quests/1000/cloud-computing-fundamentals/) - Revisit the concepts if any felt shaky

### Character Class Recommendations

**💻 Software Developer**: Continue to [Infrastructure as Code](/quests/1000/infrastructure-as-code/)  
**🏗️ System Engineer**: Deepen VPC and networking mastery before [Infrastructure as Code](/quests/1000/infrastructure-as-code/)  
**🛡️ Security Specialist**: Audit your IAM policies against least privilege

## 📚 Resources

### Official Documentation
- [AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) - Identities, policies, and roles
- [Amazon EC2 Documentation](https://docs.aws.amazon.com/ec2/) - Launching and managing instances
- [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/) - Object storage and access control
- [Amazon VPC Documentation](https://docs.aws.amazon.com/vpc/) - Virtual networks, subnets, and gateways
- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/) - Every command used above

### Community Resources
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) - The six-pillar design rubric
- [AWS Free Tier](https://aws.amazon.com/free/) - What you can run at no cost
- [AWS Skill Builder](https://skillbuilder.aws/) - Free, official training

### Learning Materials
- [AWS Cloud Practitioner Essentials](https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/) - Free foundational course
- [Stack Overflow: amazon-web-services tag](https://stackoverflow.com/questions/tagged/amazon-web-services) - Community Q&A

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Launched and terminated an EC2 instance, created and emptied an S3 bucket
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Tore down every billable resource to avoid charges

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1000 (8) - Cloud Computing]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Cloud Computing Fundamentals: IaaS, PaaS, and SaaS Explained]]
**Unlocks:** [[Infrastructure as Code: Terraform and CloudFormation Fundamentals]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
