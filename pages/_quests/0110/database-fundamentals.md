---
title: 'Database Fundamentals: The Relational Model and ACID'
author: IT-Journey Team
description: 'Master the relational model behind modern databases - tables, keys, ACID transactions, and normalization - then prove it with hands-on PostgreSQL SQL.'
excerpt: Learn how relational databases store and protect data through tables, keys, ACID transactions, and normalization.
preview: images/previews/database-fundamentals-data-storage-quest-title-ret.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0110'
difficulty: 🟡 Medium
estimated_time: 90-120 minutes
primary_technology: sql
quest_type: main_quest
quest_series: Database Mastery
quest_line: The Adventurer's Data Keep
quest_arc: Foundations of the Relational Realm
quest_dependencies:
  required_quests: []
  recommended_quests: []
  unlocks_quests:
  - /quests/0110/sql-mastery/
  - /quests/0110/data-modeling/
  - /quests/0110/database-security/
  - /quests/0110/query-optimization/
  - /quests/0110/backup-recovery/
  - /quests/0110/database-migrations/
  - /quests/0110/connection-pooling/
skill_focus: data-engineering
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Basic command line navigation
  - Comfort editing text files and running shell commands
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - PostgreSQL 14+ (or Docker to run it)
  skill_level_indicators:
  - Has built or used at least one small application
  - Ready to think in terms of structured data
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A working relational schema created with CREATE TABLE
  skill_demonstrations:
  - Can explain primary keys, foreign keys, and referential integrity
  - Can describe each ACID property with a concrete example
  knowledge_checks:
  - Understands the difference between 1NF, 2NF, and 3NF
  - Can identify a transaction that violates atomicity
permalink: /quests/0110/database-fundamentals/
categories:
- Quests
- Data-Engineering
- Medium
tags:
- '0110'
- sql
- main_quest
- data-engineering
- hands-on
- gamified-learning
keywords:
  primary:
  - '0110'
  - sql
  - main_quest
  secondary:
  - data-engineering
  - relational-model
  - acid
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0110 (6) Quest: Main Quest - The Relational Model & ACID'
rewards:
  badges:
  - 🏆 Keeper of the Relational Keep - Built a normalized schema from scratch
  - 🛡️ Guardian of Integrity - Understands ACID and referential integrity
  skills_unlocked:
  - 🛠️ Relational Schema Design
  - 🧠 Transaction Reasoning
  progression_points: 75
  unlocks_features:
  - Access to the rest of the Level 0110 Database Mastery quest line
layout: quest
---
*Greetings, brave adventurer! You have reached the gates of the **Data Keep**, the stronghold where every kingdom you will ever build stores its most precious treasure: its data. This quest, **Database Fundamentals**, is the foundation stone of the entire Level 0110 Database Mastery arc. Master it and the relational realm will obey your every command; skip it and your later spells - JOINs, indexes, migrations - will crumble for want of a footing.*

*Whether you have only ever poked at a spreadsheet or you have wired an app to a database without truly understanding what happened beneath, this adventure forges the bedrock: the relational model, keys, ACID guarantees, and the first rules of normalization.*

## 📖 The Legend Behind This Quest

*In 1970, a quiet sorcerer named Edgar F. Codd published a scroll titled "A Relational Model of Data for Large Shared Data Banks." Before it, data was trapped in rigid hierarchies and tangled networks that only their creators could navigate. Codd's insight was deceptively simple: store data in tables of rows and columns, and let a precise algebra retrieve any answer. That idea became SQL, and SQL became the lingua franca of nearly every serious system on Earth.*

*This quest teaches you the "why" beneath that scroll. Learn it well, and the rest of the Data Keep opens before you.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **The Relational Model** - Explain tables, rows, columns, and domains, and why structure matters
- [ ] **Keys & Referential Integrity** - Use primary keys and foreign keys to connect data safely
- [ ] **ACID Transactions** - Describe Atomicity, Consistency, Isolation, and Durability with real examples
- [ ] **Normalization Basics** - Reshape a messy table into 1NF, 2NF, and 3NF

### Secondary Objectives (Bonus Achievements)
- [ ] **Constraints** - Enforce rules with `NOT NULL`, `UNIQUE`, `CHECK`, and `DEFAULT`
- [ ] **Data Types** - Choose appropriate types and understand `NULL` semantics
- [ ] **Indexes (preview)** - Understand why a primary key is automatically fast to look up

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Draw a two-table schema and name the key that links them
- [ ] Explain what `ROLLBACK` protects you from in one sentence
- [ ] Spot a transitive dependency and remove it
- [ ] Predict whether a query returns rows when a `NULL` is involved

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Comfort running commands in a terminal
- [ ] Basic understanding that applications store data somewhere
- [ ] Willingness to type SQL and read error messages

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] PostgreSQL 14+ installed, or Docker to run it in a container
- [ ] A terminal and a text editor or IDE (VS Code recommended)

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You can follow multi-step setup instructions
- [ ] You are ready for 90-120 minutes of focused, hands-on learning
- [ ] You are comfortable experimenting and reading errors

## 🌍 Choose Your Adventure Platform

*Every example below runs on PostgreSQL, the open-source relational database trusted from hobby projects to planet-scale systems. Choose how you summon it.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install PostgreSQL with Homebrew
brew install postgresql@16
brew services start postgresql@16

# Create and enter a practice database
createdb datakeep
psql datakeep
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install PostgreSQL with winget
winget install PostgreSQL.PostgreSQL.16

# Create and enter a practice database (adjust the path to psql if needed)
createdb datakeep
psql datakeep
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install -y postgresql

# Fedora/RHEL: sudo dnf install -y postgresql-server && sudo postgresql-setup --initdb
sudo systemctl enable --now postgresql

# Create and enter a practice database
sudo -u postgres createdb datakeep
sudo -u postgres psql datakeep
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Run PostgreSQL in a throwaway container - perfect for practice
docker run --name datakeep -e POSTGRES_PASSWORD=quest -p 5432:5432 -d postgres:16

# Connect to it
docker exec -it datakeep psql -U postgres
```

</details>

## 🧙‍♂️ Chapter 1: The Relational Model - Tables, Rows, and Domains

*Every relational database is, at heart, a collection of **tables**. A table (formally a "relation") is a set of **rows** (tuples), each described by the same **columns** (attributes). Each column draws its values from a **domain** - a type such as integer, text, or date.*

### ⚔️ Skills You'll Forge in This Chapter
- The vocabulary of the relational model
- How to create a table with appropriate data types
- Why every column has a domain and what `NULL` means

### 🏗️ Building Your First Table

Picture a library. We need to track members and the books they borrow. Start with one table:

```sql
-- A column's type (its domain) constrains what values it may hold.
CREATE TABLE members (
    member_id    INTEGER PRIMARY KEY,   -- a number that uniquely identifies a member
    full_name    TEXT NOT NULL,         -- text that may never be empty
    email        TEXT UNIQUE,           -- no two members share an email
    joined_on    DATE DEFAULT CURRENT_DATE
);

INSERT INTO members (member_id, full_name, email)
VALUES (1, 'Aria the Archivist', 'aria@datakeep.io'),
       (2, 'Bram the Bold',      'bram@datakeep.io');

SELECT * FROM members;
-- member_id | full_name          | email            | joined_on
-- ----------+--------------------+------------------+-----------
--         1 | Aria the Archivist | aria@datakeep.io | 2026-06-14
--         2 | Bram the Bold      | bram@datakeep.io | 2026-06-14
```

A crucial subtlety: `NULL` means "unknown / not applicable," **not** zero or empty string. `NULL = NULL` is itself unknown, so it is neither true nor false - which is why you must write `IS NULL`, never `= NULL`.

### 🔍 Knowledge Check: The Relational Model
- [ ] What is the difference between a row and a column?
- [ ] Why does `email TEXT UNIQUE` prevent duplicate members from registering twice?
- [ ] Why can't you compare a value to `NULL` with `=`?

### ⚡ Quick Wins and Checkpoints
- [ ] **Table created**: You ran `CREATE TABLE members` without errors
- [ ] **Rows inserted**: `SELECT * FROM members` returns your two members

## 🧙‍♂️ Chapter 2: Keys and Referential Integrity - Linking the Realm

*A single table is a lonely island. The power of the relational model is in **connecting** tables through keys.*

### ⚔️ Skills You'll Forge in This Chapter
- Primary keys, candidate keys, and surrogate keys
- Foreign keys and referential integrity
- What the database does when integrity would be violated

### 🏗️ Connecting Two Tables

A **primary key** uniquely identifies each row (e.g., `member_id`). A **foreign key** is a column in one table that points at the primary key of another, creating a relationship the database will enforce.

```sql
CREATE TABLE loans (
    loan_id    INTEGER PRIMARY KEY,
    member_id  INTEGER NOT NULL REFERENCES members(member_id),  -- foreign key
    book_title TEXT NOT NULL,
    due_date   DATE NOT NULL
);

-- This succeeds: member 1 exists.
INSERT INTO loans VALUES (100, 1, 'The Codd Codex', DATE '2026-07-01');

-- This FAILS: there is no member 999. Referential integrity protects you.
INSERT INTO loans VALUES (101, 999, 'Ghost Book', DATE '2026-07-01');
-- ERROR: insert or update on table "loans" violates foreign key constraint
```

The foreign key guarantees a loan can never reference a member who does not exist. This is **referential integrity**, and it is the single most important reason to use a relational database over loose files.

### 🔍 Knowledge Check: Keys
- [ ] What is the difference between a primary key and a foreign key?
- [ ] Why does the database reject a loan for member 999?
- [ ] What might `ON DELETE CASCADE` do to loans when a member is deleted?

## 🧙‍♂️ Chapter 3: ACID - The Oath That Protects Your Data

*A **transaction** is a group of statements that must succeed or fail as one. The four ACID properties are the sacred oath every serious database swears.*

### ⚔️ Skills You'll Forge in This Chapter
- The meaning of Atomicity, Consistency, Isolation, Durability
- How to wrap statements in `BEGIN` / `COMMIT` / `ROLLBACK`
- Why ACID makes money transfers safe

### 🏗️ ACID Made Concrete

| Property | Promise | Example |
| --- | --- | --- |
| **Atomicity** | All statements commit, or none do | A bank transfer never debits without crediting |
| **Consistency** | Constraints always hold after a transaction | A foreign key is never left dangling |
| **Isolation** | Concurrent transactions don't corrupt each other | Two librarians issuing loans don't reuse a loan_id |
| **Durability** | Once committed, data survives a crash | A power cut after `COMMIT` does not lose the loan |

First, create the `accounts` table and seed two rows so the example runs as written. The `CHECK` constraint refuses any update that would drive a balance negative - a `CHECK` guards a rule *inside* a single row, the way a foreign key guards a rule *between* tables:

```sql
CREATE TABLE accounts (
    id      INTEGER PRIMARY KEY,
    balance NUMERIC NOT NULL CHECK (balance >= 0)   -- CHECK: no account may go negative
);
INSERT INTO accounts (id, balance) VALUES (1, 100), (2, 100);
```

Now watch atomicity protect a transfer between those two accounts:

```sql
BEGIN;                                              -- start the transaction
UPDATE accounts SET balance = balance - 50 WHERE id = 1;
UPDATE accounts SET balance = balance + 50 WHERE id = 2;
-- If the second UPDATE failed (e.g., account 2 vanished), we run:
ROLLBACK;   -- undoes BOTH updates - no money is lost or created
-- If both succeeded:
COMMIT;     -- makes the change permanent and durable
```

Without atomicity, a crash between the two `UPDATE`s would destroy 50 coins. The transaction guarantees the realm's books always balance.

### 🔍 Knowledge Check: ACID
- [ ] Which property guarantees a transfer never debits without crediting?
- [ ] What does `ROLLBACK` do to statements run since `BEGIN`?
- [ ] Which property guarantees committed data survives a power failure?

## 🧙‍♂️ Chapter 4: Normalization Basics - Taming the Chaotic Table

*Normalization is the discipline of organizing columns so each fact lives in exactly one place. Redundancy is the enemy: store a fact twice and the copies will eventually disagree.*

### ⚔️ Skills You'll Forge in This Chapter
- First, Second, and Third Normal Form
- How to spot and remove redundancy
- Why normalization prevents update anomalies

### 🏗️ From Chaos to Third Normal Form

Consider a flat, denormalized table:

```text
loans_flat(loan_id, member_name, member_email, book_title, author, author_country)
```

It repeats `member_email` for every loan and `author_country` for every book by that author. Update one copy and forget another, and your data lies.

**1NF (First Normal Form)** - atomic columns, no repeating groups. One value per cell, no `book1, book2, book3` columns.

**2NF (Second Normal Form)** - already 1NF, and every non-key column depends on the *whole* primary key (matters for composite keys). Member details belong in a `members` table keyed by `member_id`, not duplicated per loan.

**3NF (Third Normal Form)** - already 2NF, and no non-key column depends on another non-key column (no **transitive** dependencies). `author_country` depends on `author`, not on the book, so it belongs in an `authors` table.

```sql
-- Normalized to 3NF: each fact lives in exactly one place.
CREATE TABLE authors (
    author_id      INTEGER PRIMARY KEY,
    name           TEXT NOT NULL,
    country        TEXT
);

CREATE TABLE books (
    book_id   INTEGER PRIMARY KEY,
    title     TEXT NOT NULL,
    author_id INTEGER NOT NULL REFERENCES authors(author_id)
);

-- loans now references members and books by key - zero duplication.
CREATE TABLE loans_3nf (
    loan_id   INTEGER PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES members(member_id),
    book_id   INTEGER NOT NULL REFERENCES books(book_id),
    due_date  DATE NOT NULL
);
```

Now an author who moves countries is updated in exactly one row. No anomalies, no lies.

### 🔍 Knowledge Check: Normalization
- [ ] What update anomaly does 3NF prevent for `author_country`?
- [ ] What does "atomic column" mean in 1NF?
- [ ] Why is duplication dangerous even if disk is cheap?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Build the Schema
**Objective**: Create the `members`, `authors`, `books`, and `loans_3nf` tables in your `datakeep` database.

**Requirements**:
- [ ] All four tables created without errors
- [ ] Every foreign key references the correct primary key
- [ ] At least two rows inserted into each table

**Validation**: Run `\dt` in psql and confirm all four tables appear.

### 🟡 Intermediate Challenge: Prove ACID
**Objective**: Open a transaction that inserts a loan for a non-existent member, observe the failure, and `ROLLBACK`.

**Requirements**:
- [ ] Wrap the work in `BEGIN` ... `ROLLBACK`
- [ ] Show that no partial data remains afterward
- [ ] Explain in one sentence which property saved you

**Validation**: `SELECT count(*) FROM loans_3nf` is unchanged after the rollback.

### 🔴 Advanced Challenge: Normalize a Mess
**Objective**: Given a denormalized `loans_flat` table, redesign it into 3NF on paper and write the `CREATE TABLE` statements.

**Requirements**:
- [ ] Identify every transitive and partial dependency
- [ ] Produce at least three normalized tables
- [ ] Connect them with foreign keys

**Validation**: No fact is stored in more than one place.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Keeper of the Relational Keep** - You built a normalized schema from nothing
- 🛡️ **Guardian of Integrity** - You wield keys and ACID with confidence

**🛠️ Skills Unlocked**:
- **Relational Schema Design** - Model real entities as connected tables
- **Transaction Reasoning** - Predict what commits, what rolls back, and why

**🔓 Unlocked Quests**:
- SQL Mastery - Query the data you just learned to store
- Data Modeling - Turn requirements into rigorous schemas
- Database Security - Protect the keep from intruders

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [SQL Mastery](/quests/0110/sql-mastery/) - SELECT, JOIN, and transactions in depth

**Explore Side Adventures**:
- ⚔️ [Data Modeling](/quests/0110/data-modeling/) - ER diagrams and schema design
- ⚔️ [Query Optimization](/quests/0110/query-optimization/) - Make your queries fast

### Character Class Recommendations

**💻 Software Developer**: Continue to [SQL Mastery](/quests/0110/sql-mastery/)  
**🏗️ System Engineer**: Explore [Backup and Recovery](/quests/0110/backup-recovery/)  
**📊 Data Scientist**: Advance to [Data Modeling](/quests/0110/data-modeling/)

## 📚 Resources

### Official Documentation
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html) - The canonical hands-on intro
- [PostgreSQL Data Types](https://www.postgresql.org/docs/current/datatype.html) - Every domain you can use
- [SQL CREATE TABLE Reference](https://www.postgresql.org/docs/current/sql-createtable.html) - Constraints and keys

### Community Resources
- [Use The Index, Luke!](https://use-the-index-luke.com/) - SQL performance and indexing explained
- [Codd's 1970 Relational Model Paper](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf) - The original scroll
- [Stack Overflow: postgresql tag](https://stackoverflow.com/questions/tagged/postgresql) - Answers from the realm

### Learning Materials
- [PostgreSQL Exercises](https://pgexercises.com/) - Interactive practice problems
- [Wikipedia: Database Normalization](https://en.wikipedia.org/wiki/Database_normalization) - Forms explained with examples

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Built and populated the four-table schema
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0110 - Database Mastery]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Unlocks:** [[SQL Mastery: Query Language Proficiency for Data Professionals]] · [[Data Modeling: Schema Design and Database Relationships]] · [[Database Security: Access Control and Data Encryption]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
</content>
</invoke>
