---
title: 'Database Security: Access Control and Data Encryption'
author: IT-Journey Team
description: 'Defend the Data Keep with least-privilege grants, parameterized queries that stop SQL injection, encryption at rest and in transit, and audit logging.'
excerpt: Protect databases with least privilege, parameterized queries, encryption, and auditing.
preview: images/previews/database-security-access-control-quest-title-and.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0110'
difficulty: 🔴 Hard
estimated_time: 75-90 minutes
primary_technology: sql
quest_type: main_quest
quest_series: Database Mastery
quest_line: The Adventurer's Data Keep
quest_arc: The Warded Vault
quest_dependencies:
  required_quests:
  - /quests/0110/database-fundamentals/
  recommended_quests:
  - /quests/0110/sql-mastery/
  unlocks_quests:
  - /quests/0110/backup-recovery/
skill_focus: security
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Completion of Database Fundamentals (recommended)
  - Basic understanding of how applications connect to a database
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - PostgreSQL 14+ (or Docker to run it)
  skill_level_indicators:
  - Comfortable running SQL and editing application code
  - Ready to think adversarially about data access
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A least-privilege application role created with GRANT
  skill_demonstrations:
  - Can write a parameterized query that resists injection
  - Can configure TLS and encryption at rest conceptually
  knowledge_checks:
  - Understands the difference between authentication and authorization
  - Can explain why string concatenation enables SQL injection
permalink: /quests/0110/database-security/
categories:
- Quests
- Data-Engineering
- Hard
tags:
- '0110'
- sql
- main_quest
- security
- hands-on
- gamified-learning
keywords:
  primary:
  - '0110'
  - sql
  - main_quest
  secondary:
  - security
  - sql-injection
  - encryption
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0110 (6) Quest: Main Quest - The Warded Vault'
rewards:
  badges:
  - 🏆 Warden of the Vault - Locked down access with least privilege
  - 🛡️ Bane of the Injector - Stopped SQL injection with parameters
  skills_unlocked:
  - 🛠️ Database Access Control
  - 🧠 Secure Query Construction
  progression_points: 100
  unlocks_features:
  - Backup and disaster-recovery quests in the Database Mastery line
layout: quest
---
*Greetings, brave adventurer! Your Data Keep is full of treasure - customer secrets, credentials, the lifeblood of your kingdom - and treasure attracts thieves. This quest, **Database Security**, teaches you to ward the vault: to grant each visitor only the keys they need, to seal your queries against the injection curse, to encrypt your gold both in the chest and on the road, and to keep a ledger of every hand that reaches inside.*

*A database breach is rarely a single dramatic siege. More often it is a forgotten over-privileged account, a query built by gluing strings together, or an unencrypted backup left in a public bucket. This quest closes those doors one by one.*

## 📖 The Legend Behind This Quest

*The most infamous database attack, **SQL injection**, has topped vulnerability lists for over two decades. It is devastatingly simple: an application builds a query by concatenating user input, and an attacker supplies input that is itself SQL. The fix - parameterized queries - has existed just as long, yet the bug persists because developers keep reaching for string concatenation. Beyond injection lie the quieter disciplines: least privilege, encryption, and auditing, the unglamorous practices that separate a defended kingdom from a plundered one.*

*This quest teaches all four pillars, with runnable examples you can defend in a code review.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Least Privilege** - Create roles that can do exactly what they need and nothing more
- [ ] **Parameterized Queries** - Stop SQL injection at the source
- [ ] **Encryption** - Protect data at rest and in transit with TLS and disk/column encryption
- [ ] **Auditing** - Log who accessed what, so a breach cannot hide

### Secondary Objectives (Bonus Achievements)
- [ ] **Secrets Management** - Keep credentials out of code and config
- [ ] **Row-Level Security** - Restrict which rows a role can even see
- [ ] **Principle of Defense in Depth** - Layer controls so one failure is not a breach

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Rewrite a string-concatenated query as a parameterized one
- [ ] Grant an app role read/write on one table without `DROP` rights
- [ ] Explain the difference between encryption at rest and in transit
- [ ] Describe what an audit log must capture to be useful after a breach

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Understanding of how applications connect to and query a database
- [ ] Familiarity with at least one programming language
- [ ] Completion of [Database Fundamentals](/quests/0110/database-fundamentals/) (recommended)

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] PostgreSQL 14+ installed, or Docker to run it
- [ ] A terminal and a text editor or IDE (VS Code recommended)

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can run SQL and read application code
- [ ] You are ready to think like an attacker
- [ ] Ready for 75-90 minutes of focused, hands-on learning

## 🌍 Choose Your Adventure Platform

*Spin up PostgreSQL to practice roles, grants, and TLS configuration.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
brew install postgresql@16
brew services start postgresql@16
createdb warded_vault
psql warded_vault
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
winget install PostgreSQL.PostgreSQL.16
createdb warded_vault
psql warded_vault
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y postgresql
sudo systemctl enable --now postgresql
sudo -u postgres createdb warded_vault
sudo -u postgres psql warded_vault
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
docker run --name warded-vault -e POSTGRES_PASSWORD=quest -p 5432:5432 -d postgres:16
docker exec -it warded-vault psql -U postgres
```

> ⚠️ Never expose a practice database with a weak password to the public internet.

</details>

## 🧙‍♂️ Chapter 1: Least Privilege - Hand Out Only the Keys You Must

*The single most effective database control is also the cheapest: give every account exactly the access it needs and nothing more. An application login that can `DROP TABLE` is a catastrophe waiting for one injection flaw.*

### ⚔️ Skills You'll Forge in This Chapter
- Creating roles and granting narrow privileges
- The difference between authentication (who) and authorization (what)
- Separating an app role from an admin role

### 🏗️ Granting the Minimum

```sql
-- Set up a table the app will use.
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer TEXT NOT NULL,
    total    NUMERIC(10,2) NOT NULL
);

-- ❌ Over-privileged: this login can read, write, AND destroy.
-- GRANT ALL PRIVILEGES ON orders TO app_login;

-- ✅ Least privilege: a role that can only serve the rows it needs.
CREATE ROLE app_login LOGIN PASSWORD 'rotate-me-in-a-vault';
GRANT SELECT, INSERT, UPDATE ON orders TO app_login;
GRANT USAGE, SELECT ON SEQUENCE orders_order_id_seq TO app_login;
-- Note: no DELETE, no DROP, no schema-altering rights.
```

If an attacker ever hijacks `app_login`, the damage ceiling is "read and modify orders" - not "delete the entire database." This is **authorization** (what you may do), distinct from **authentication** (proving who you are with a password, certificate, or token).

### 🔍 Knowledge Check: Least Privilege
- [ ] What is the difference between authentication and authorization?
- [ ] Why should an app role usually lack `DROP` privileges?
- [ ] How does least privilege cap the blast radius of a stolen credential?

### ⚡ Quick Wins and Checkpoints
- [ ] **Role created**: You created `app_login` with a password
- [ ] **Scoped grants**: The role can read/write but not drop the table

## 🧙‍♂️ Chapter 2: Parameterized Queries - Sealing the Injection Curse

*SQL injection happens when user input is treated as SQL code. The cure is to send the query structure and the data **separately**, so the database can never confuse one for the other.*

### ⚔️ Skills You'll Forge in This Chapter
- Recognizing injectable string-concatenated queries
- Writing parameterized (prepared) queries
- Why parameters defeat injection by design

### 🏗️ The Curse and the Cure

```python
# ❌ VULNERABLE: user input is glued directly into the SQL string.
def find_user(conn, name):
    sql = "SELECT * FROM users WHERE name = '" + name + "'"
    return conn.execute(sql)

# An attacker passes name = "' OR '1'='1" turning the query into:
#   SELECT * FROM users WHERE name = '' OR '1'='1'
# ...which returns EVERY user. Or worse: "'; DROP TABLE users; --"

# ✅ SAFE: the query and the data travel separately. The driver binds
#    `name` as a value, never as executable SQL.
def find_user_safe(conn, name):
    sql = "SELECT * FROM users WHERE name = %s"   # placeholder, not concatenation
    return conn.execute(sql, (name,))             # data bound as a parameter
```

With a parameterized query, the string `' OR '1'='1` is searched for *literally* as a name - it is data, never code. This is not a filter you have to remember to apply; it is structural immunity. Every mature database driver supports it (`%s` in psycopg, `?` in SQLite/JDBC, `$1` in native PostgreSQL). ORMs do this for you - the danger is dropping to raw string-built SQL.

### 🔍 Knowledge Check: Injection
- [ ] Why does string concatenation let input become executable SQL?
- [ ] How does a parameter placeholder prevent injection structurally?
- [ ] What does the attacker input `' OR '1'='1` do to a concatenated query?

## 🧙‍♂️ Chapter 3: Encryption and Auditing - Gold in the Chest and on the Road

*Two final wards: encrypt the treasure so a stolen disk or sniffed connection reveals nothing, and keep a ledger so you can answer "who touched this?" after an incident.*

### ⚔️ Skills You'll Forge in This Chapter
- Encryption in transit (TLS) vs at rest (disk/column)
- When to encrypt at the column level
- What a useful audit log records

### 🏗️ Encrypt In Transit and At Rest

**In transit** means TLS between the application and the database, so a network eavesdropper sees ciphertext. Require it explicitly:

```bash
# Force every client connection to use TLS (in postgresql.conf):
#   ssl = on
# In the connection string, demand a verified certificate:
psql "host=db.example.com dbname=warded_vault sslmode=verify-full"
```

**At rest** means the data on disk is encrypted, so a stolen drive or backup file is useless. This is often handled by full-disk or filesystem encryption (LUKS, cloud-provider volume encryption). For especially sensitive fields, add **column-level encryption** with the `pgcrypto` extension:

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt a secret before it ever rests in a column.
INSERT INTO secrets (label, payload)
VALUES ('api-key', pgp_sym_encrypt('super-secret-value', 'encryption-key'));

-- Decrypt only when authorized to read it.
SELECT pgp_sym_decrypt(payload, 'encryption-key') FROM secrets WHERE label = 'api-key';
```

**Auditing** records access so a breach cannot hide. A useful audit trail captures *who* (role), *what* (statement/table), *when* (timestamp), and *from where* (client IP). PostgreSQL's `pgaudit` extension or `log_statement = 'mod'` gives you this. Store logs on a separate, append-only system so an attacker who owns the database cannot erase their tracks.

### 🔍 Knowledge Check: Encryption & Auditing
- [ ] What threat does encryption in transit stop that at-rest encryption does not?
- [ ] When would you reach for column-level encryption over full-disk?
- [ ] Why store audit logs on a separate system from the database?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Lock Down a Role
**Objective**: Create an application role that can read and write one table but cannot drop it.

**Requirements**:
- [ ] `CREATE ROLE` with a login and password
- [ ] Grant only `SELECT`, `INSERT`, `UPDATE`
- [ ] Verify the role cannot `DROP TABLE`

**Validation**: Attempting `DROP TABLE` as the app role fails with a permission error.

### 🟡 Intermediate Challenge: Disarm an Injectable Query
**Objective**: Take a vulnerable string-concatenated query and rewrite it parameterized.

**Requirements**:
- [ ] Demonstrate the injection on the vulnerable version (in a safe sandbox)
- [ ] Rewrite using placeholders and bound parameters
- [ ] Confirm the malicious input is now treated as literal data

**Validation**: The `' OR '1'='1` input returns zero rows against the safe version.

### 🔴 Advanced Challenge: Encrypt and Audit
**Objective**: Store a secret with `pgcrypto`, enable statement logging, and produce an audit trail.

**Requirements**:
- [ ] Encrypt a column value and decrypt it back
- [ ] Enable `log_statement` or `pgaudit` for modifications
- [ ] Show a log entry capturing who modified what and when

**Validation**: The plaintext never appears on disk, and the log records the change.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Warden of the Vault** - You enforced least privilege across roles
- 🛡️ **Bane of the Injector** - You sealed your queries against injection

**🛠️ Skills Unlocked**:
- **Database Access Control** - Grant precisely, deny by default
- **Secure Query Construction** - Parameterize everything, encrypt the sensitive

**🔓 Unlocked Quests**:
- Backup and Recovery - Protect data from loss as well as theft
- Database Migrations - Apply schema changes safely and auditably

**📊 Progression Points**: +100 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Backup and Recovery](/quests/0110/backup-recovery/) - Defend against data loss

**Explore Side Adventures**:
- ⚔️ [Database Migrations](/quests/0110/database-migrations/) - Change schemas safely
- ⚔️ [Security Fundamentals](/quests/1011/security-fundamentals/) - The CIA triad and defense in depth

### Character Class Recommendations

**💻 Software Developer**: Continue to [Backup and Recovery](/quests/0110/backup-recovery/)  
**🏗️ System Engineer**: Explore [Database Migrations](/quests/0110/database-migrations/)  
**🛡️ Security Specialist**: Advance to [Security Fundamentals](/quests/1011/security-fundamentals/)

## 📚 Resources

### Official Documentation
- [PostgreSQL GRANT Reference](https://www.postgresql.org/docs/current/sql-grant.html) - Privileges and roles
- [PostgreSQL SSL/TLS Setup](https://www.postgresql.org/docs/current/ssl-tcp.html) - Encryption in transit
- [PostgreSQL pgcrypto](https://www.postgresql.org/docs/current/pgcrypto.html) - Column-level encryption

### Community Resources
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) - The definitive guide
- [OWASP Top 10: A03 Injection](https://owasp.org/Top10/A03_2021-Injection/) - Why injection still tops the list
- [pgaudit project](https://www.pgaudit.org/) - PostgreSQL audit logging

### Learning Materials
- [PortSwigger SQL Injection Labs](https://portswigger.net/web-security/sql-injection) - Hands-on, safe practice
- [CISA Data Encryption Guidance](https://www.cisa.gov/) - At-rest and in-transit principles

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Created a least-privilege application role
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0110 - Database Mastery]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Prerequisites:** [[Database Fundamentals: The Relational Model and ACID]] **Unlocks:** [[Backup and Recovery: Data Protection Strategies for Databases]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
</content>
