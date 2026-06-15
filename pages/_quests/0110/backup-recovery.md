---
title: 'Backup and Recovery: Data Protection for Databases'
author: IT-Journey Team
description: 'Guard against data loss with logical and physical backups, point-in-time recovery, RTO/RPO targets, and the restore drills that prove a backup actually works.'
excerpt: Master backup types, point-in-time recovery, RTO/RPO targets, and tested restore drills.
preview: images/previews/backup-and-recovery-data-protection-quest-title.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0110'
difficulty: 🟡 Medium
estimated_time: 60-75 minutes
primary_technology: postgresql
quest_type: main_quest
quest_series: Database Mastery
quest_line: The Adventurer's Data Keep
quest_arc: The Vault of Restoration
quest_dependencies:
  required_quests:
  - /quests/0110/database-fundamentals/
  recommended_quests:
  - /quests/0110/database-security/
  unlocks_quests:
  - /quests/0110/connection-pooling/
skill_focus: data-engineering
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Completion of Database Fundamentals (recommended)
  - Comfort running shell commands and SQL
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - PostgreSQL 14+ (or Docker to run it)
  skill_level_indicators:
  - Can run database tools from a terminal
  - Ready to plan for failure, not just success
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A backup taken and successfully restored
  skill_demonstrations:
  - Can take a logical backup with pg_dump and restore it
  - Can define RTO and RPO for a workload
  knowledge_checks:
  - Understands the difference between logical and physical backups
  - Can explain point-in-time recovery
permalink: /quests/0110/backup-recovery/
categories:
- Quests
- Data-Engineering
- Medium
tags:
- '0110'
- postgresql
- main_quest
- data-engineering
- hands-on
- gamified-learning
keywords:
  primary:
  - '0110'
  - postgresql
  - main_quest
  secondary:
  - data-engineering
  - backup
  - disaster-recovery
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0110 (6) Quest: Main Quest - The Vault of Restoration'
rewards:
  badges:
  - 🏆 Keeper of the Restore - Proved a backup with a real restore drill
  - 🛡️ Warden Against Loss - Set RTO/RPO targets and met them
  skills_unlocked:
  - 🛠️ Backup & Restore Operations
  - 🧠 Disaster Recovery Planning
  progression_points: 75
  unlocks_features:
  - Connection and resilience quests in the Database Mastery line
layout: quest
---
*Greetings, brave adventurer! Every kingdom falls eventually - a disk dies, a finger slips, a `DELETE` forgets its `WHERE` clause, ransomware locks the gates. The question is never *if* but *when*, and the only thing standing between disaster and a shrug is a backup you can actually restore. This quest, **Backup and Recovery**, teaches you to take backups that work, to rewind time with point-in-time recovery, and - most importantly - to *drill* your restores so you know they work before you need them.*

*A backup you have never tested is not a backup; it is a hope. This quest turns hope into certainty.*

## 📖 The Legend Behind This Quest

*The graveyard of dead companies is full of those who had backups that could not be restored - corrupted, incomplete, or for the wrong database. The discipline that saves kingdoms is not "take backups" but "test restores." Two numbers govern the whole craft: the **Recovery Point Objective (RPO)**, how much data you can afford to lose, and the **Recovery Time Objective (RTO)**, how long you can afford to be down. Every backup decision - frequency, type, storage, automation - flows from those two targets.*

*This quest teaches you to take both logical and physical backups, to recover to any second in time, and to define and meet your RTO and RPO.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Backup Types** - Distinguish logical, physical, full, and incremental backups
- [ ] **Point-in-Time Recovery (PITR)** - Rewind a database to any moment using WAL
- [ ] **RTO & RPO** - Define and reason about recovery time and recovery point targets
- [ ] **Restore Drills** - Prove a backup by restoring it, not by trusting it

### Secondary Objectives (Bonus Achievements)
- [ ] **The 3-2-1 Rule** - Three copies, two media, one offsite
- [ ] **Backup Automation** - Schedule and verify backups without manual steps
- [ ] **Backup Encryption** - Protect backups as carefully as the live database

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Choose logical vs physical backup for a given recovery need
- [ ] Explain how WAL enables recovery to a precise timestamp
- [ ] State an RPO and RTO and justify a backup schedule that meets them
- [ ] Restore a backup into a clean database and verify the data

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Comfort running shell commands and SQL
- [ ] Understanding of what a database stores
- [ ] Completion of [Database Fundamentals](/quests/0110/database-fundamentals/) (recommended)

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] PostgreSQL 14+ installed, or Docker to run it
- [ ] A terminal and some free disk space for backup files

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You can run command-line database tools
- [ ] You are ready to plan for failure as well as success
- [ ] Ready for 60-75 minutes of focused, hands-on learning

## 🌍 Choose Your Adventure Platform

*Run PostgreSQL, create some data, then practice backing it up and restoring it.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
brew install postgresql@16
brew services start postgresql@16
createdb restoration_vault
psql restoration_vault -c "CREATE TABLE treasure(id serial primary key, name text);"
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
winget install PostgreSQL.PostgreSQL.16
createdb restoration_vault
psql restoration_vault -c "CREATE TABLE treasure(id serial primary key, name text);"
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y postgresql
sudo systemctl enable --now postgresql
sudo -u postgres createdb restoration_vault
sudo -u postgres psql restoration_vault -c "CREATE TABLE treasure(id serial primary key, name text);"
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
docker run --name restoration -e POSTGRES_PASSWORD=quest -p 5432:5432 -d postgres:16
docker exec -it restoration psql -U postgres -c "CREATE DATABASE restoration_vault;"
```

</details>

## 🧙‍♂️ Chapter 1: Backup Types - Knowing Your Arsenal

*Not all backups are the same. The two great families are **logical** (a dump of SQL statements or data that can recreate the database) and **physical** (a byte-level copy of the actual data files). Each has its moment.*

### ⚔️ Skills You'll Forge in This Chapter
- Logical backups with `pg_dump` / `pg_restore`
- Physical backups with `pg_basebackup`
- Full vs incremental, and when each fits

### 🏗️ Taking a Logical Backup

```bash
# Logical backup: a portable file that can recreate the database anywhere.
# The custom format (-Fc) is compressed and restorable selectively.
pg_dump -Fc restoration_vault > vault_backup.dump

# Restore it into a fresh database.
createdb restored_vault
pg_restore -d restored_vault vault_backup.dump
```

Logical backups are portable across PostgreSQL versions and let you restore a single table, but they are slow for very large databases. **Physical backups** copy the data files directly and are far faster to restore at scale:

```bash
# Physical backup: a byte-level copy of the cluster, ideal for big databases
# and the foundation of point-in-time recovery.
pg_basebackup -D /backups/base -Ft -z -P
```

A **full** backup captures everything; an **incremental** backup captures only what changed since the last one, saving space and time at the cost of a more complex restore chain. Most real strategies combine periodic fulls with frequent incrementals or continuous WAL archiving (next chapter).

### 🔍 Knowledge Check: Backup Types
- [ ] When would you choose a logical backup over a physical one?
- [ ] What can a logical backup restore that a physical one cannot easily?
- [ ] Why are incremental backups faster but harder to restore from?

### ⚡ Quick Wins and Checkpoints
- [ ] **Backup taken**: You produced a `pg_dump` file
- [ ] **Restore done**: You restored it into a fresh database

## 🧙‍♂️ Chapter 2: Point-in-Time Recovery - Rewinding the Clock

*The deadliest disasters are subtle: someone ran a bad `UPDATE` at 14:32 and you only noticed at 15:00. A nightly backup loses everything since midnight. **Point-in-time recovery (PITR)** lets you restore to 14:31:59 - the moment before the mistake.*

### ⚔️ Skills You'll Forge in This Chapter
- How the Write-Ahead Log (WAL) records every change
- Combining a base backup with archived WAL
- Recovering to a precise target time

### 🏗️ How PITR Works

PostgreSQL writes every change to a **Write-Ahead Log** before applying it. If you archive those WAL files continuously alongside a periodic base backup, you can replay the log from the base backup up to any chosen instant.

```ini
# In postgresql.conf - turn on continuous WAL archiving:
wal_level = replica
archive_mode = on
archive_command = 'cp %p /backups/wal_archive/%f'
```

To recover to a specific moment, restore the base backup and tell PostgreSQL where to stop replaying:

```ini
# In the recovery configuration of the restored cluster:
restore_command = 'cp /backups/wal_archive/%f %p'
recovery_target_time = '2026-06-14 14:31:59'
```

PostgreSQL replays WAL from the base backup forward, stopping at 14:31:59 - just before the bad `UPDATE`. This is how your **RPO** can approach zero: with continuous WAL archiving you lose, at most, the seconds since the last archived segment.

### 🔍 Knowledge Check: PITR
- [ ] What does the Write-Ahead Log record, and when?
- [ ] What two ingredients does PITR combine to reach an exact timestamp?
- [ ] How does continuous WAL archiving shrink your RPO?

## 🧙‍♂️ Chapter 3: RTO, RPO, and the Restore Drill

*Two numbers and one habit define a real recovery strategy. **RPO** caps data loss; **RTO** caps downtime; the **restore drill** proves you can actually meet them.*

### ⚔️ Skills You'll Forge in This Chapter
- Defining RTO and RPO for a workload
- The 3-2-1 backup rule
- Running and timing a restore drill

### 🏗️ Setting Targets and Proving Them

```text
RPO (Recovery Point Objective): How much data can we afford to lose?
  - "At most 5 minutes" -> WAL archived every few minutes, or streaming replica.
  - "At most 24 hours"  -> a nightly backup may suffice.

RTO (Recovery Time Objective): How long can we be down?
  - "15 minutes" -> warm standby ready to promote.
  - "4 hours"    -> restore from backup is acceptable.
```

Choose backups that satisfy both numbers, then follow the **3-2-1 rule**: keep **3** copies of your data, on **2** different media types, with **1** copy offsite (a different region or provider). A fire, flood, or region outage must not destroy every copy.

The non-negotiable habit is the **restore drill** - regularly restoring a backup into a scratch environment and verifying it:

```bash
# A restore drill, scripted so it runs on a schedule.
createdb drill_$(date +%Y%m%d)
pg_restore -d drill_$(date +%Y%m%d) vault_backup.dump
psql drill_$(date +%Y%m%d) -c "SELECT count(*) FROM treasure;"  # verify row count
# Time how long the whole restore took -> that is your real RTO.
```

The drill answers three questions a real outage will ask: Does the backup restore at all? Is the data correct and complete? How long did it take (your true RTO)? Teams that skip drills discover the answers during the disaster.

### 🔍 Knowledge Check: RTO/RPO/Drills
- [ ] What is the difference between RTO and RPO?
- [ ] What does the "1" in the 3-2-1 rule protect against?
- [ ] Why is an untested backup not really a backup?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Backup and Restore
**Objective**: Take a logical backup of a database with data and restore it into a fresh one.

**Requirements**:
- [ ] Insert several rows, then `pg_dump`
- [ ] Restore into a new database with `pg_restore`
- [ ] Verify row counts match

**Validation**: The restored database has identical data to the original.

### 🟡 Intermediate Challenge: Define Targets
**Objective**: Write an RTO and RPO for a hypothetical service and design a backup schedule that meets them.

**Requirements**:
- [ ] State a concrete RPO and RTO with justification
- [ ] Pick backup types and frequency that satisfy both
- [ ] Apply the 3-2-1 rule to storage

**Validation**: Your schedule provably keeps loss under RPO and downtime under RTO.

### 🔴 Advanced Challenge: A Timed Restore Drill
**Objective**: Run a full restore drill, verify correctness, and record the elapsed time as your measured RTO.

**Requirements**:
- [ ] Restore into a clean scratch database
- [ ] Run verification queries (counts, checksums, spot checks)
- [ ] Record the total restore time

**Validation**: The drill produces a correct database and a measured RTO you can report.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Keeper of the Restore** - You proved a backup with a real restore drill
- 🛡️ **Warden Against Loss** - You set RTO/RPO targets and met them

**🛠️ Skills Unlocked**:
- **Backup & Restore Operations** - Take and restore logical and physical backups
- **Disaster Recovery Planning** - Translate business tolerance into a backup plan

**🔓 Unlocked Quests**:
- Connection Pooling - Keep a recovered database serving traffic efficiently
- Database Migrations - Evolve the schema you now know how to protect

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Connection Pooling](/quests/0110/connection-pooling/) - Manage connections efficiently

**Explore Side Adventures**:
- ⚔️ [Database Security](/quests/0110/database-security/) - Encrypt backups and control access
- ⚔️ [Database Migrations](/quests/0110/database-migrations/) - Evolve schemas safely

### Character Class Recommendations

**💻 Software Developer**: Continue to [Connection Pooling](/quests/0110/connection-pooling/)  
**🏗️ System Engineer**: Explore [Database Security](/quests/0110/database-security/)  
**📊 Data Scientist**: Advance to [Database Migrations](/quests/0110/database-migrations/)

## 📚 Resources

### Official Documentation
- [PostgreSQL Backup and Restore](https://www.postgresql.org/docs/current/backup.html) - The canonical guide
- [PostgreSQL Continuous Archiving & PITR](https://www.postgresql.org/docs/current/continuous-archiving.html) - WAL and point-in-time recovery
- [pg_dump Reference](https://www.postgresql.org/docs/current/app-pgdump.html) - Logical backup options

### Community Resources
- [pgBackRest](https://pgbackrest.org/) - Robust backup and PITR tooling for production
- [Stack Overflow: backup tag](https://stackoverflow.com/questions/tagged/backup) - Backup Q&A
- [Wikipedia: 3-2-1 Backup Rule](https://en.wikipedia.org/wiki/Backup) - Backup strategy fundamentals

### Learning Materials
- [Google SRE Book: Data Integrity](https://sre.google/sre-book/data-integrity/) - Why testing restores matters
- [AWS Disaster Recovery Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html) - RTO/RPO strategy patterns

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Took a backup and restored it successfully
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0110 - Database Mastery]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Database Fundamentals: The Relational Model and ACID]]
**Unlocks:** [[Connection Pooling: Efficient Database Resource Management]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
</content>
