---
title: 'Compliance Standards: SOC 2, ISO 27001, GDPR, and PCI-DSS'
author: IT-Journey Team
description: 'Navigate the major security compliance frameworks - SOC 2, ISO 27001, GDPR, and PCI-DSS - learning controls mapping, audit evidence, and audit prep.'
excerpt: Master SOC 2, ISO 27001, GDPR, and PCI-DSS - controls, audit evidence, and audit readiness
preview: images/previews/compliance-standards-soc-2-iso-27001-gdpr-pci-dss.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1011'
difficulty: 🟡 Medium
estimated_time: 90-120 minutes
primary_technology: compliance
quest_type: main_quest
quest_series: Security Mastery
quest_line: The Warrior's Bastion
quest_arc: The Scribe's Ledger of Trust
quest_dependencies:
  required_quests:
  - /quests/1011/security-fundamentals/
  recommended_quests:
  - /quests/1011/secure-coding/
  - /quests/1011/penetration-testing/
  unlocks_quests: []
skill_focus: security
learning_style: conceptual
prerequisites:
  knowledge_requirements:
  - Completion of Security Fundamentals (recommended)
  - Understanding of security controls and the CIA triad
  - General awareness of how organizations handle customer data
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - A spreadsheet or text editor for building a controls matrix
  skill_level_indicators:
  - Comfortable thinking about processes and evidence, not only code
  - Ready to map technical controls to framework requirements
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A small controls-mapping matrix linking one control to multiple frameworks
  skill_demonstrations:
  - Can explain the difference between SOC 2 and ISO 27001
  - Can describe what audit evidence demonstrates a control is operating
  knowledge_checks:
  - Understands GDPR lawful basis and data-subject rights at a high level
  - Knows the core intent of the PCI-DSS requirements
permalink: /quests/1011/compliance-standards/
categories:
- Quests
- Security
- Medium
tags:
- '1011'
- compliance
- main_quest
- soc2
- iso-27001
- conceptual
- gamified-learning
keywords:
  primary:
  - '1011'
  - compliance
  - main_quest
  secondary:
  - soc2
  - iso-27001
  - gdpr
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1011 (11) Quest: Main Quest - Compliance Standards'
rewards:
  badges:
  - 🏆 Scribe of Trust - Mapped controls to the great compliance frameworks
  - 🛡️ Keeper of the Ledger - Prepared evidence that satisfies auditors
  skills_unlocked:
  - 🛠️ Controls Mapping Across Frameworks
  - 📜 Audit Evidence Preparation
  progression_points: 90
  unlocks_features:
  - Ability to help an organization prepare for a real security audit
layout: quest
---
*Greetings, brave adventurer! You have built strong walls and tested them well - but in the wider world, strength is not enough. You must also **prove** it, in writing, to skeptical auditors and wary customers. This quest, **Compliance Standards**, teaches the scribe's discipline: mapping the controls you already have to the great frameworks of trust - SOC 2, ISO 27001, GDPR, and PCI-DSS - and gathering the evidence that shows they truly operate.*

*Compliance is where security meets the ledger. A control that works but cannot be evidenced is, to an auditor, a control that does not exist. Master this quest and you can translate technical defenses into the language of attestation, certification, and regulation.*

## 📖 The Legend Behind This Quest

*As commerce moved into the cloud, a problem of trust arose: how could one company rely on another to guard its data? The answer was independent frameworks and audits - SOC 2 attestations, ISO 27001 certifications, and laws like GDPR and PCI-DSS - that let an outside party vouch for a system's controls. The clever defender soon realized a secret: most of these frameworks ask for the same handful of controls under different names. Map once, satisfy many.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **SOC 2** - The five Trust Services Criteria and what a Type I vs Type II report means
- [ ] **ISO 27001** - An ISMS, Annex A controls, and how certification differs from attestation
- [ ] **GDPR** - Lawful basis, data-subject rights, and the core privacy obligations
- [ ] **PCI-DSS** - The intent of the requirements protecting cardholder data
- [ ] **Controls Mapping & Evidence** - Map one control to many frameworks and gather audit evidence

### Secondary Objectives (Bonus Achievements)
- [ ] **Gap Assessment** - Compare current state to a framework's requirements
- [ ] **Continuous Compliance** - Automate evidence collection rather than scrambling at audit time
- [ ] **Shared Responsibility** - Understand who owns which control in a cloud environment

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain how SOC 2 and ISO 27001 differ in form and outcome
- [ ] Describe two GDPR data-subject rights
- [ ] State what PCI-DSS exists to protect
- [ ] Build a row of a controls matrix that satisfies several frameworks at once

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Completion of [Security Fundamentals](/quests/1011/security-fundamentals/) (recommended)
- [ ] Understanding of security controls and the CIA triad
- [ ] General awareness of how organizations collect and store data

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] A spreadsheet tool or text editor for building a controls matrix
- [ ] A web browser to read framework references

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You can reason about processes and evidence, not just code
- [ ] You are ready to translate technical controls into framework language
- [ ] Ready for 90-120 minutes of focused study

## 🌍 Choose Your Adventure Platform

*This quest is documentation- and process-heavy. Your "tools" are a controls matrix and the framework references. Any platform works.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Build your controls matrix as version-controlled, plain-text Markdown/CSV
mkdir -p ~/compliance && cd ~/compliance
printf "Control,SOC2,ISO27001,GDPR,PCI-DSS,Evidence\n" > controls-matrix.csv
open -a "Numbers" controls-matrix.csv 2>/dev/null || cat controls-matrix.csv
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Start a controls matrix you can track in git
New-Item -ItemType Directory -Force -Path "$HOME\compliance" | Out-Null
Set-Content "$HOME\compliance\controls-matrix.csv" "Control,SOC2,ISO27001,GDPR,PCI-DSS,Evidence"
Get-Content "$HOME\compliance\controls-matrix.csv"
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Plain-text, version-controlled evidence beats a sprawling shared drive
mkdir -p ~/compliance && cd ~/compliance
echo "Control,SOC2,ISO27001,GDPR,PCI-DSS,Evidence" > controls-matrix.csv
git init -q && git add controls-matrix.csv
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Cloud providers publish their own attestations you inherit under the
# shared responsibility model. Pull them from the trust portals:
#   AWS Artifact, Azure Service Trust Portal, Google Cloud Compliance Reports.
echo "Inherit provider controls; you remain responsible for your config + data."
```

</details>

## 🧙‍♂️ Chapter 1: SOC 2 and ISO 27001 - Attestation vs Certification

*The two most common frameworks a software company meets are SOC 2 and ISO 27001. They overlap heavily but differ in form.*

### ⚔️ Skills You'll Forge in This Chapter
- The SOC 2 Trust Services Criteria and report types
- The ISO 27001 ISMS and Annex A controls
- When each is asked for

### 🏗️ SOC 2

SOC 2 is an **attestation** report produced by a licensed CPA firm, built around five **Trust Services Criteria (TSC)**:

| Criterion | Concern |
| --- | --- |
| **Security** (required) | Protection against unauthorized access |
| **Availability** | The system is available for operation as agreed |
| **Processing Integrity** | Processing is complete, valid, accurate, timely |
| **Confidentiality** | Confidential information is protected |
| **Privacy** | Personal information is handled per the privacy notice |

- A **Type I** report assesses control design at a point in time.
- A **Type II** report assesses operating effectiveness over a period (typically 3-12 months) - this is what customers usually demand.

### 🏗️ ISO 27001

ISO/IEC 27001 is an international standard for an **Information Security Management System (ISMS)**. Unlike SOC 2's attestation, ISO 27001 yields a formal **certification** from an accredited body. Its **Annex A** (revised in the 2022 edition to 93 controls across four themes - Organizational, People, Physical, Technological) is the control catalog.

```text
SOC 2                            ISO 27001
- US-centric, AICPA              - International standard
- Attestation report (CPA)       - Certification (accredited body)
- Trust Services Criteria        - ISMS + Annex A controls
- Type I (design) / Type II (op) - Stage 1 (docs) / Stage 2 (operation) audit
- Renewed annually               - 3-year cycle with surveillance audits
```

### 🔍 Knowledge Check: SOC 2 & ISO 27001
- [ ] Which SOC 2 criterion is always required?
- [ ] What does a Type II report add over a Type I?
- [ ] How does ISO 27001 certification differ from a SOC 2 attestation?

## 🧙‍♂️ Chapter 2: GDPR and PCI-DSS - Regulation and Mandate

*SOC 2 and ISO 27001 are voluntary frameworks. GDPR is law; PCI-DSS is a contractual mandate. Both carry real penalties.*

### ⚔️ Skills You'll Forge in This Chapter
- GDPR lawful basis and data-subject rights
- The intent behind PCI-DSS

### 🏗️ GDPR (General Data Protection Regulation)

The EU's GDPR governs the processing of personal data of people in the EU/EEA, regardless of where the processor is located. Core ideas:

- **Lawful basis** - you need a legal reason to process personal data (consent, contract, legal obligation, vital interests, public task, or legitimate interests).
- **Data-subject rights** - access, rectification, erasure ("right to be forgotten"), portability, objection, and restriction.
- **Principles** - data minimization, purpose limitation, storage limitation, and accountability.
- **Breach notification** - report qualifying breaches to the supervisory authority within **72 hours**.
- **Penalties** - up to €20 million or 4% of global annual turnover, whichever is higher.

### 🏗️ PCI-DSS (Payment Card Industry Data Security Standard)

PCI-DSS is mandated by the card brands for any organization that stores, processes, or transmits cardholder data. The current major version is **PCI-DSS v4.0**. Its requirements protect the **cardholder data environment (CDE)**:

```text
1–2  Build and maintain a secure network (firewalls, no vendor defaults)
3–4  Protect stored cardholder data and encrypt it in transit
5–6  Maintain a vulnerability program (anti-malware, secure development)
7–8  Strong access control (need-to-know, unique IDs, MFA)
9    Restrict physical access to cardholder data
10–11 Monitor and test networks (logging, scans, penetration tests)
12   Maintain an information security policy
```

The cheapest path to compliance is often to **reduce scope** - e.g., never store card numbers yourself; use a tokenizing payment processor so the CDE barely touches your systems.

### 🔍 Knowledge Check: GDPR & PCI-DSS
- [ ] Name two GDPR data-subject rights
- [ ] What is the GDPR breach-notification deadline?
- [ ] Why does reducing PCI scope reduce compliance burden?

## 🧙‍♂️ Chapter 3: Controls Mapping and Audit Evidence

*Here is the secret that makes compliance tractable: the frameworks overlap enormously. A single technical control - say, enforcing MFA - satisfies a requirement in every one of them. Map once, evidence once, satisfy many.*

### ⚔️ Skills You'll Forge in This Chapter
- Building a controls-mapping matrix
- Identifying valid audit evidence

### 🏗️ A Controls-Mapping Matrix

```text
Control: Multi-Factor Authentication on admin access
  SOC 2      -> CC6.1 (logical access security)
  ISO 27001  -> A.8.5 (secure authentication)
  GDPR       -> Art. 32 (security of processing — appropriate measures)
  PCI-DSS    -> Req. 8.4/8.5 (MFA for access to the CDE)
  Evidence   -> IdP config screenshot + MFA enrollment report + access log sample
```

One control, four frameworks. Maintain this matrix as the spine of your compliance program.

### 🏗️ What Counts as Audit Evidence

Auditors do not take your word for it; they want artifacts proving a control is **designed** and **operating** over time:

```text
Strong evidence types:
  - Configuration exports (IAM policies, firewall rules, encryption settings)
  - System-generated logs and reports (access reviews, vulnerability scans)
  - Tickets showing a process ran (offboarding, change approvals)
  - Signed policies and training completion records
  - Screenshots with timestamps (least preferred — easy to fake, hard to date)

For a Type II / certification: evidence must span the AUDIT PERIOD,
not just a single moment. One screenshot is design; a quarter of access
reviews is operation.
```

Mature teams pursue **continuous compliance** - automating evidence collection (e.g., with tools like Vanta, Drata, or custom scripts pulling cloud config) so an audit is a query, not a fire drill.

### 🔍 Knowledge Check: Mapping & Evidence
- [ ] How can one control satisfy multiple frameworks?
- [ ] Why must Type II evidence span a period, not a moment?
- [ ] What makes a configuration export stronger evidence than a screenshot?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Map One Control
**Objective**: Pick one control you actually use (encryption at rest, MFA, logging) and map it to all four frameworks.

**Requirements**:
- [ ] One control, four framework references
- [ ] One concrete piece of evidence that proves it
- [ ] Note which framework's wording is strictest

**Validation**: Each mapping cites a plausible requirement area.

### 🟡 Intermediate Challenge: Gap Assessment
**Objective**: Choose three SOC 2 Security criteria controls and assess whether a system you know meets them.

**Requirements**:
- [ ] State each control's intent
- [ ] Mark met / partial / gap with justification
- [ ] Propose how to close each gap

**Validation**: Each "met" claim has evidence behind it.

### 🔴 Advanced Challenge: Mini Audit Package
**Objective**: Assemble an evidence package for one control as if for a Type II audit.

**Requirements**:
- [ ] Document the control's design (the policy/config)
- [ ] Provide operating evidence spanning a period
- [ ] Map it across at least three frameworks
- [ ] Identify how the evidence could be collected automatically

**Validation**: An auditor could conclude the control operated for the period.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Scribe of Trust** - You mapped controls to the great frameworks
- 🛡️ **Keeper of the Ledger** - You prepared evidence auditors accept

**🛠️ Skills Unlocked**:
- **Controls Mapping Across Frameworks** - Satisfy many standards with one matrix
- **Audit Evidence Preparation** - Prove controls operate over time

**🔓 Unlocked Quests**:
- You have completed the core Security & Compliance arc - advance toward the Master tier

**📊 Progression Points**: +90 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 Advance to the Master tier (Level 1100+) - Data Engineering and beyond

**Explore Side Adventures**:
- ⚔️ [Penetration Testing](/quests/1011/penetration-testing/) - Often a required PCI/SOC 2 control
- ⚔️ [Threat Modeling](/quests/1011/threat-modeling/) - Evidence of risk assessment for auditors

### Character Class Recommendations

**💻 Software Developer**: Revisit [Secure Coding Practices](/quests/1011/secure-coding/)  
**🏗️ System Engineer**: Explore [Penetration Testing](/quests/1011/penetration-testing/)  
**🛡️ Security Specialist**: Deepen [Threat Modeling](/quests/1011/threat-modeling/)

## 📚 Resources

### Official Documentation
- [AICPA SOC 2 / Trust Services Criteria](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2) - The source of SOC 2
- [ISO/IEC 27001](https://www.iso.org/standard/27001) - The international ISMS standard
- [GDPR Full Text](https://gdpr-info.eu/) - Searchable articles and recitals
- [PCI Security Standards Council](https://www.pcisecuritystandards.org/) - PCI-DSS v4.0 and guidance

### Community Resources
- [NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) - A control catalog many frameworks map back to
- [Secure Controls Framework (SCF)](https://securecontrolsframework.com/) - A meta-framework that maps across standards
- [Cloud Security Alliance CCM](https://cloudsecurityalliance.org/research/cloud-controls-matrix) - Cloud controls matrix

### Tools & Utilities
- [AWS Artifact](https://aws.amazon.com/artifact/) / [Azure Service Trust Portal](https://servicetrust.microsoft.com/) - Inherit provider attestations
- [OpenSCAP](https://www.open-scap.org/) - Automated configuration compliance scanning
- [GDPR Checklist](https://gdpr.eu/checklist/) - A practical readiness list

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Built a controls-mapping matrix row across frameworks
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1011 - Security & Compliance]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Security Fundamentals: CIA Triad and Defense in Depth Strategies]]
**Related quests:** [[Penetration Testing: Tools and Ethical Hacking Methodologies]] · [[Threat Modeling: STRIDE Framework and Attack Trees Analysis]] · [[Secure Coding Practices: OWASP Top 10 Vulnerability Prevention]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
