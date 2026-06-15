---
title: 'Security Fundamentals: CIA Triad and Defense in Depth'
author: IT-Journey Team
description: Master information security fundamentals including the CIA triad, the OWASP Top 10, defense in depth, secure-by-design thinking, and practical risk management.
excerpt: Learn foundational security concepts including the CIA triad, the OWASP Top 10, defense in depth, and a security mindset
preview: images/previews/security-fundamentals-cia-triad-quest-title-defens.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1011'
difficulty: 🟡 Medium
estimated_time: 90-120 minutes
primary_technology: security
quest_type: main_quest
quest_series: Security Mastery
quest_line: The Warrior's Bastion
quest_arc: Foundations of the Shieldwall
quest_dependencies:
  required_quests: []
  recommended_quests: []
  unlocks_quests:
  - /quests/1011/secure-coding/
  - /quests/1011/threat-modeling/
  - /quests/1011/penetration-testing/
  - /quests/1011/compliance-standards/
skill_focus: security
learning_style: conceptual
prerequisites:
  knowledge_requirements:
  - Basic command line navigation
  - Comfort reading code in at least one language (examples use Python and Bash)
  - General understanding of how web applications and networks work
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - A terminal and a text editor or IDE (VS Code recommended)
  - Optional Docker for the hands-on lab
  skill_level_indicators:
  - Comfortable building or running small applications
  - Ready to think adversarially about systems you build
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A personal threat-and-control map for one application you know
  skill_demonstrations:
  - Can explain the CIA triad and map controls to each property
  - Can identify which OWASP Top 10 category a given flaw belongs to
  knowledge_checks:
  - Understands defense in depth and least privilege
  - Can describe secure-by-design and shift-left security
permalink: /quests/1011/security-fundamentals/
categories:
- Quests
- Security
- Medium
tags:
- '1011'
- security
- main_quest
- cia-triad
- owasp
- conceptual
- gamified-learning
keywords:
  primary:
  - '1011'
  - security
  - main_quest
  secondary:
  - cia-triad
  - owasp-top-10
  - defense-in-depth
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1011 (11) Quest: Main Quest - Security Fundamentals'
rewards:
  badges:
  - 🏆 Shieldbearer - Internalized the CIA triad and defense in depth
  - 🛡️ Mind of the Defender - Adopted an adversarial security mindset
  skills_unlocked:
  - 🛠️ Security Risk Assessment
  - 🧠 Threat-and-Control Mapping
  progression_points: 75
  unlocks_features:
  - Access to the rest of the Level 1011 Security & Compliance quest line
layout: quest
---
*Greetings, brave adventurer! You have crossed into the **Warrior tier**, and the gates of the Bastion stand before you. Beyond them lies the realm of **Security & Compliance** - a land where every kingdom you have built in earlier quests can be defended... or breached. This quest, **Security Fundamentals**, is the oath you swear before taking up the shieldwall. It teaches you to think like both the builder and the besieger.*

*Whether you are a developer who has never once asked "how would an attacker abuse this?" or a seasoned engineer formalizing instincts you already half-trust, this adventure forges the mental armor every Warrior needs: the CIA triad, the OWASP Top 10, defense in depth, and the discipline of secure-by-design.*

## 📖 The Legend Behind This Quest

*In the early ages of computing, systems were built behind castle walls - air-gapped, trusted, and rarely attacked. When the great bridges of the internet were raised, every fortress became reachable from every other, and the old assumption of trust shattered. The defenders who survived were those who learned a single truth: security is not a feature you bolt on at the end, it is a property you design in from the first stone.*

*This quest teaches you the "why" behind every control you will ever configure. Master it, and the remaining quests of the Bastion - secure coding, threat modeling, penetration testing, and compliance - become incantations you can actually understand rather than rituals you merely repeat.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **The CIA Triad** - Explain Confidentiality, Integrity, and Availability and map real controls to each
- [ ] **The OWASP Top 10** - Recognize the most common web application risk categories and what causes them
- [ ] **Defense in Depth** - Design layered controls so that one failure does not become a breach
- [ ] **The Security Mindset** - Reason adversarially about a system you built and find its weak points

### Secondary Objectives (Bonus Achievements)
- [ ] **Least Privilege & Zero Trust** - Apply the principle of minimal access to accounts and services
- [ ] **Risk Management** - Reason about likelihood × impact and prioritize what to fix first
- [ ] **Secure-by-Design / Shift Left** - Move security decisions earlier in the development lifecycle

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain the CIA triad to another person without notes
- [ ] Classify a newly discovered bug into the correct OWASP Top 10 category
- [ ] Describe how two independent controls protect a single asset
- [ ] Justify a fix-it-first decision using a simple risk rating

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Basic understanding of how web requests, servers, and databases interact
- [ ] Familiarity with at least one programming language
- [ ] Comfort using a terminal

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] A terminal and a text editor or IDE (VS Code recommended)
- [ ] Optional: Docker, for the local hands-on lab

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You have built or maintained at least one small application
- [ ] You are ready to think about how systems fail, not just how they work
- [ ] Ready for 90-120 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*The concepts here are platform-independent, but the optional lab uses a deliberately vulnerable app. Choose the path that fits your setup.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install Docker Desktop (or use colima) to run the practice lab
brew install --cask docker

# Run OWASP Juice Shop, a safe, intentionally vulnerable training app
docker run --rm -d -p 3000:3000 bkimminich/juice-shop

# Open http://localhost:3000 in your browser
open http://localhost:3000
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install Docker Desktop
winget install Docker.DockerDesktop

# Run the OWASP Juice Shop training target
docker run --rm -d -p 3000:3000 bkimminich/juice-shop

# Open the app
start http://localhost:3000
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Install Docker via your distribution
sudo apt update && sudo apt install -y docker.io   # Debian/Ubuntu
# sudo dnf install -y docker                        # Fedora/RHEL

sudo systemctl enable --now docker

# Launch the deliberately vulnerable training app
sudo docker run --rm -d -p 3000:3000 bkimminich/juice-shop
xdg-open http://localhost:3000
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# In a Codespace or any container runtime, the same image works.
docker run --rm -d -p 3000:3000 bkimminich/juice-shop
# Forward port 3000 to your browser via your platform's port forwarding.
```

> ⚠️ Only ever run intentionally vulnerable apps on isolated, local, or throwaway environments. Never expose them to the public internet.

</details>

## 🧙‍♂️ Chapter 1: The CIA Triad - The Three Pillars of the Bastion

*Every security decision you will ever make protects one or more of three properties. Memorize them, and you have a lens for the entire field.*

### ⚔️ Skills You'll Forge in This Chapter
- The meaning of Confidentiality, Integrity, and Availability
- How concrete controls map to each pillar
- The trade-offs between the three

### 🏗️ The Three Pillars

| Pillar | Question it answers | Example controls | Example attack it stops |
| --- | --- | --- | --- |
| **Confidentiality** | Can only authorized parties read this? | Encryption (TLS, AES), access control, MFA | Data theft, eavesdropping |
| **Integrity** | Is the data exactly what it should be, unaltered? | Hashing, digital signatures, checksums, input validation | Tampering, man-in-the-middle modification |
| **Availability** | Can authorized users reach it when needed? | Redundancy, backups, rate limiting, DDoS protection | Ransomware, denial of service |

A useful sibling concept is **AAA**: **Authentication** (who are you?), **Authorization** (what may you do?), and **Accounting / Auditing** (what did you do?). Non-repudiation - proof that an actor performed an action - rounds out the model.

Here is the integrity pillar made concrete. A checksum lets you detect if a file was altered in transit:

```bash
# Compute a SHA-256 hash of a downloaded artifact
sha256sum app-release.tar.gz

# Compare it to the publisher's published hash. If they differ,
# the file's integrity is compromised - do not trust it.
echo "EXPECTED_HASH  app-release.tar.gz" | sha256sum --check
```

### 🔍 Knowledge Check: The Triad
- [ ] Which pillar does TLS primarily protect, and which does it also support?
- [ ] A backup restores which pillar after a ransomware attack?
- [ ] Why can maximizing one pillar sometimes weaken another?

### ⚡ Quick Wins and Checkpoints
- [ ] **Mapped a control to a pillar**: You named one control for each of C, I, and A
- [ ] **Ran a checksum**: You verified a file's integrity from the terminal

## 🧙‍♂️ Chapter 2: The OWASP Top 10 - Knowing Your Enemy

*The Open Worldwide Application Security Project (OWASP) maintains a famous, data-driven list of the most critical web application security risks. The current edition is the **OWASP Top 10:2021**. Learn these categories and you will recognize most real-world web flaws on sight.*

### ⚔️ Skills You'll Forge in This Chapter
- The ten risk categories and the root cause behind each
- How to classify a finding into the right category

### 🏗️ The Ten Categories (2021 edition)

1. **A01 Broken Access Control** - users can act outside their intended permissions (e.g., changing `/account?id=123` to another user's id).
2. **A02 Cryptographic Failures** - sensitive data exposed through weak or missing encryption (formerly "Sensitive Data Exposure").
3. **A03 Injection** - untrusted input is interpreted as a command (SQL, OS, LDAP, and cross-site scripting now live here).
4. **A04 Insecure Design** - flaws baked into the architecture, fixable only by re-design, not patching.
5. **A05 Security Misconfiguration** - default credentials, verbose errors, open cloud buckets, unnecessary features enabled.
6. **A06 Vulnerable and Outdated Components** - using libraries with known CVEs.
7. **A07 Identification and Authentication Failures** - weak passwords, broken session handling, missing MFA.
8. **A08 Software and Data Integrity Failures** - trusting unsigned updates, insecure deserialization, compromised CI/CD pipelines.
9. **A09 Security Logging and Monitoring Failures** - breaches that go undetected because nothing was logged or watched.
10. **A10 Server-Side Request Forgery (SSRF)** - the server is tricked into making requests to internal or unintended destinations.

```text
Mapping practice — given a finding, name the category:
  "An API returns another customer's invoice when I change the ID"  -> A01 Broken Access Control
  "The login page accepts ' OR '1'='1 and logs me in"               -> A03 Injection
  "The app still ships log4j 2.14"                                   -> A06 Vulnerable Components
  "S3 bucket is world-readable"                                      -> A05 Security Misconfiguration
```

### 🔍 Knowledge Check: OWASP Top 10
- [ ] Which category absorbed XSS in the 2021 edition?
- [ ] What distinguishes A04 Insecure Design from A05 Misconfiguration?
- [ ] Why did SSRF earn its own category?

## 🧙‍♂️ Chapter 3: Defense in Depth, Least Privilege, and Secure-by-Design

*A single wall can be breached. A fortress with a moat, an outer wall, an inner keep, and vigilant guards survives the failure of any one layer. This is **defense in depth**.*

### ⚔️ Skills You'll Forge in This Chapter
- Layering independent controls
- Applying least privilege and zero trust
- Designing security in from the start (shift left)

### 🏗️ Layered Defense in Practice

Consider protecting a single database of customer records. Defense in depth stacks independent controls:

```text
Layer 1 (Network):    Firewall + private subnet — the DB has no public IP
Layer 2 (Identity):   MFA + least-privilege IAM roles for anyone reaching it
Layer 3 (Transport):  TLS everywhere, certificate validation enforced
Layer 4 (App):        Parameterized queries, input validation, output encoding
Layer 5 (Data):       Encryption at rest, column-level encryption for PII
Layer 6 (Detect):     Logging, alerting on anomalous queries, audit trails
Layer 7 (Recover):    Tested backups, an incident response runbook
```

If an attacker defeats the firewall, identity and encryption still stand. No single failure becomes a breach.

**Least privilege** means every account, process, and service gets exactly the access it needs and nothing more. Compare these two database grants:

```sql
-- ❌ Over-privileged: the app login can read AND drop tables
GRANT ALL PRIVILEGES ON shop.* TO 'app_user'@'%';

-- ✅ Least privilege: the app can only read and write the rows it serves
GRANT SELECT, INSERT, UPDATE, DELETE ON shop.orders TO 'app_user'@'10.0.%';
GRANT SELECT ON shop.products TO 'app_user'@'10.0.%';
```

**Zero trust** extends least privilege across the whole network: never trust a request just because it came from "inside." Authenticate and authorize every call.

**Secure-by-design / shift left** moves these decisions to the earliest possible moment. Fixing a design flaw on a whiteboard costs minutes; fixing it in production after a breach costs reputations.

### 🔍 Knowledge Check: Layered Defense
- [ ] Name two layers that protect a database independently of the firewall
- [ ] Rewrite an over-privileged grant to follow least privilege
- [ ] Why is "shift left" cheaper than patching in production?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Map Your Own App
**Objective**: Pick an application you have built or use daily. Identify one asset (e.g., user passwords) and write one control for each CIA pillar protecting it.

**Requirements**:
- [ ] Name the asset
- [ ] One Confidentiality control, one Integrity control, one Availability control
- [ ] State which OWASP category would apply if each control were missing

**Validation**: You can defend each choice in one sentence.

### 🟡 Intermediate Challenge: Threat-and-Control Map
**Objective**: For the same app, draw a defense-in-depth diagram with at least four independent layers.

**Requirements**:
- [ ] At least four layers, each an independent control
- [ ] Identify which OWASP Top 10 risks each layer mitigates
- [ ] Mark which single layer, if removed, would be most dangerous and why

**Validation**: Removing any single layer should not, by itself, equal a breach.

### 🔴 Advanced Challenge: Break the Juice Shop
**Objective**: Using the local OWASP Juice Shop lab, find one Broken Access Control issue and one Injection issue, and classify each.

**Requirements**:
- [ ] Document the request that triggers each flaw
- [ ] Identify the exact OWASP Top 10 category
- [ ] Propose the control that would prevent it

**Validation**: Each finding maps cleanly to a category and a concrete fix.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Shieldbearer** - You internalized the CIA triad and defense in depth
- 🛡️ **Mind of the Defender** - You can reason adversarially about your own systems

**🛠️ Skills Unlocked**:
- **Security Risk Assessment** - Rank issues by likelihood and impact
- **Threat-and-Control Mapping** - Connect assets to controls to attacks

**🔓 Unlocked Quests**:
- Secure Coding Practices - Stop the OWASP Top 10 at the code level
- Threat Modeling - Find flaws systematically before attackers do
- Compliance Standards - Map these controls to SOC 2, ISO 27001, and more

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Secure Coding Practices](/quests/1011/secure-coding/) - Turn principles into hardened code

**Explore Side Adventures**:
- ⚔️ [Threat Modeling](/quests/1011/threat-modeling/) - STRIDE and attack trees
- ⚔️ [Penetration Testing](/quests/1011/penetration-testing/) - Ethical hacking methodology

### Character Class Recommendations

**💻 Software Developer**: Continue to [Secure Coding Practices](/quests/1011/secure-coding/)  
**🏗️ System Engineer**: Explore [Threat Modeling](/quests/1011/threat-modeling/)  
**🛡️ Security Specialist**: Advance to [Penetration Testing](/quests/1011/penetration-testing/)

## 📚 Resources

### Official Documentation
- [OWASP Top 10 (2021)](https://owasp.org/www-project-top-ten/) - The canonical risk list
- [NIST SP 800-53 Security and Privacy Controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) - Control catalog
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) - Identify, Protect, Detect, Respond, Recover

### Community Resources
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) - Practical, concise guidance
- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) - The training app used above
- [CISA Secure by Design](https://www.cisa.gov/securebydesign) - Government guidance on building it in

### Learning Materials
- [Defense in Depth (CISA)](https://www.cisa.gov/) - Layered security guidance
- [MITRE ATT&CK](https://attack.mitre.org/) - A knowledge base of real attacker techniques

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Mapped CIA controls to one of your own applications
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1011 - Security & Compliance]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Unlocks:** [[Secure Coding Practices: OWASP Top 10 Vulnerability Prevention]] · [[Threat Modeling: STRIDE Framework and Attack Trees Analysis]] · [[Penetration Testing: Tools and Ethical Hacking Methodologies]] · [[Compliance Standards: SOC 2, GDPR, and HIPAA Requirements]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
