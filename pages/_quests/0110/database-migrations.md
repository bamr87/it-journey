---
title: 'Database Migrations: Schema Evolution and Version Control'
author: IT-Journey Team
description: 'Evolve a live database safely: write versioned up/down migrations, use Flyway, Liquibase, or Alembic, and ship zero-downtime schema changes.'
excerpt: Master versioned migrations, rollbacks, migration tools, and zero-downtime schema changes.
preview: images/previews/database-migrations-schema-evolution-quest-title.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0110'
difficulty: 🔴 Hard
estimated_time: 60-75 minutes
primary_technology: sql
quest_type: main_quest
quest_series: Database Mastery
quest_line: The Adventurer's Data Keep
quest_arc: The Living Schema
quest_dependencies:
  required_quests:
  - /quests/0110/data-modeling/
  recommended_quests:
  - /quests/0110/sql-mastery/
  unlocks_quests:
  - /quests/0110/backup-recovery/
skill_focus: data-engineering
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Completion of Data Modeling (recommended)
  - Comfort with CREATE TABLE and ALTER TABLE
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - PostgreSQL 14+ and one migration tool (Flyway, Liquibase, or Alembic)
  skill_level_indicators:
  - Understands schemas and version control basics
  - Ready to manage change over time
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A reversible migration applied and rolled back
  skill_demonstrations:
  - Can write paired up and down migrations
  - Can describe the expand-contract zero-downtime pattern
  knowledge_checks:
  - Understands why migrations are versioned and ordered
  - Can explain why dropping a column needs a multi-step deploy
permalink: /quests/0110/database-migrations/
categories:
- Quests
- Data-Engineering
- Hard
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
  - migrations
  - zero-downtime
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0110 (6) Quest: Main Quest - The Living Schema'
rewards:
  badges:
  - 🏆 Keeper of the Living Schema - Versioned and reversed a migration
  - 🛡️ Master of the Seamless Shift - Shipped a zero-downtime change
  skills_unlocked:
  - 🛠️ Versioned Migrations
  - 🧠 Expand-Contract Deployments
  progression_points: 100
  unlocks_features:
  - Backup and recovery quests in the Database Mastery line
layout: quest
---
*Greetings, brave adventurer! A schema is not carved in stone - it lives, grows, and occasionally must change while the kingdom keeps running. This quest, **Database Migrations**, teaches you to evolve a database the way you evolve code: in small, versioned, reversible steps that every teammate and every environment applies in the exact same order. By the end you will change a live schema without dropping a single request.*

*Migrations are where database knowledge meets software engineering discipline. Edit a table by hand in production and you have an undocumented, irreproducible change. Write a migration and you have a tested, version-controlled, replayable history that promotes cleanly from your laptop to staging to production.*

## 📖 The Legend Behind This Quest

*In the dark ages, teams shared schema changes by emailing SQL scripts and praying everyone ran them in order. Inevitably, environments drifted: a column existed in staging but not production, a constraint was added twice, a deploy failed at 3 a.m. The migration tool was the answer - a ledger table inside the database itself recording exactly which changes have been applied, so the tool can compute and apply only what is missing. Flyway, Liquibase, and Alembic each implement this idea, turning schema evolution from folklore into engineering.*

*This quest teaches the universal pattern beneath all three tools, then the zero-downtime techniques that let you change a schema serving live traffic.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Versioned Migrations** - Write ordered, immutable change scripts tracked in version control
- [ ] **Up and Down** - Pair every forward migration with a reversal
- [ ] **Migration Tools** - Run migrations with Flyway, Liquibase, or Alembic
- [ ] **Zero-Downtime Changes** - Apply the expand-contract pattern to live schemas

### Secondary Objectives (Bonus Achievements)
- [ ] **The Schema History Table** - Understand how a tool tracks applied versions
- [ ] **Backfilling Data** - Migrate data, not just structure, safely
- [ ] **Safe Index Creation** - Add indexes concurrently without locking writes

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain why migrations must be ordered and immutable once shipped
- [ ] Write a down migration that exactly reverses an up migration
- [ ] Sequence a column rename across multiple deploys without downtime
- [ ] Describe what `CREATE INDEX CONCURRENTLY` buys you

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Comfort with `CREATE TABLE` and `ALTER TABLE`
- [ ] Basic familiarity with Git and version control
- [ ] Completion of [Data Modeling](/quests/0110/data-modeling/) (recommended)

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] PostgreSQL 14+ installed, or Docker to run it
- [ ] One migration tool installed (Alembic via pip is easiest to start)

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can alter a schema and use Git
- [ ] You are ready to think about change over time and across environments
- [ ] Ready for 60-75 minutes of focused, hands-on learning

## 🌍 Choose Your Adventure Platform

*Run PostgreSQL, then install a migration tool. Alembic (Python) is shown as the primary example; Flyway and Liquibase are demonstrated too.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
brew install postgresql@16
brew services start postgresql@16
createdb living_schema
# Install Alembic (Python migration tool)
pip install alembic psycopg2-binary
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
winget install PostgreSQL.PostgreSQL.16
createdb living_schema
pip install alembic psycopg2-binary
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y postgresql python3-pip
sudo systemctl enable --now postgresql
sudo -u postgres createdb living_schema
pip install alembic psycopg2-binary
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
docker run --name living-schema -e POSTGRES_PASSWORD=quest -p 5432:5432 -d postgres:16
# Flyway via Docker - no local install needed:
docker run --rm flyway/flyway -url=jdbc:postgresql://host.docker.internal/living_schema info
```

</details>

## 🧙‍♂️ Chapter 1: Versioned Migrations and the Schema History

*A migration is a single, ordered, immutable change script. The tool records each applied migration in a hidden history table, so it always knows the exact state of any database and can apply only the missing steps.*

### ⚔️ Skills You'll Forge in This Chapter
- Writing ordered migration files
- Understanding the schema history table
- Why a shipped migration must never be edited

### 🏗️ Anatomy of a Migration

Most tools use a numbered or timestamped file. Flyway uses plain SQL files named by version:

```sql
-- V1__create_users.sql  (the "up" / forward migration)
CREATE TABLE users (
    user_id  SERIAL PRIMARY KEY,
    email    TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- V2__add_display_name.sql
ALTER TABLE users ADD COLUMN display_name TEXT;
```

When you run `flyway migrate`, it consults its `flyway_schema_history` table, sees that V1 and V2 are unapplied, runs them in order, and records each with a checksum. The checksum is why you must **never edit a migration that has shipped**: changing V1 after it ran in production makes the checksums diverge and the tool refuses to proceed. To fix a mistake, you write a *new* migration (V3) that corrects it.

```text
flyway_schema_history:
  version | description       | checksum   | success
  --------+-------------------+------------+--------
  1       | create users      | 8841...    | true
  2       | add display name  | 1097...    | true
```

### 🔍 Knowledge Check: Versioning
- [ ] What does the schema history table let the tool compute?
- [ ] Why must a shipped migration never be edited in place?
- [ ] How do you correct a mistake in an already-applied migration?

### ⚡ Quick Wins and Checkpoints
- [ ] **Migration written**: You created a versioned `CREATE TABLE` migration
- [ ] **History understood**: You can name what the history table records

## 🧙‍♂️ Chapter 2: Up and Down with Alembic

*Reversibility is a superpower. A **down** (downgrade) migration exactly reverses an **up** (upgrade), so a bad deploy can be rolled back. Alembic generates paired functions for this.*

### ⚔️ Skills You'll Forge in This Chapter
- Initializing Alembic and creating a revision
- Writing matching `upgrade()` and `downgrade()` functions
- Applying and reverting a migration

### 🏗️ A Reversible Alembic Migration

```bash
alembic init migrations                # one-time setup
alembic revision -m "add status to orders"   # creates a new revision file
```

The generated revision file holds two functions you fill in:

```python
# migrations/versions/abc123_add_status_to_orders.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Forward: add the column with a safe default.
    op.add_column('orders', sa.Column('status', sa.String(), nullable=False,
                                       server_default='pending'))

def downgrade():
    # Reverse: remove exactly what upgrade added.
    op.drop_column('orders', 'status')
```

```bash
alembic upgrade head      # apply all pending migrations
alembic downgrade -1      # roll back the most recent one
```

The discipline: `downgrade()` must undo precisely what `upgrade()` did, in reverse. If `upgrade` adds a column with a default and backfills data, `downgrade` drops that column. A migration without a working downgrade is a one-way door - sometimes acceptable, but always a deliberate choice.

### 🔍 Knowledge Check: Up/Down
- [ ] What must `downgrade()` do relative to `upgrade()`?
- [ ] What does `alembic downgrade -1` do?
- [ ] When is a one-way (no downgrade) migration acceptable?

## 🧙‍♂️ Chapter 3: Zero-Downtime Changes with Expand-Contract

*The hard part is changing a schema while the application keeps serving traffic. A naive `ALTER TABLE ... DROP COLUMN` or `RENAME` can break the running app the instant it lands. The **expand-contract** (parallel change) pattern solves this by splitting one risky change into safe steps across multiple deploys.*

### ⚔️ Skills You'll Forge in This Chapter
- The expand-contract / parallel-change pattern
- Sequencing a column rename without downtime
- Adding indexes without locking writes

### 🏗️ Renaming a Column Without Downtime

You cannot just rename `username` to `handle` in one shot - old app code still reads `username`. Instead, expand, migrate, then contract:

```sql
-- Step 1 (EXPAND): add the new column. Old code still uses the old one.
ALTER TABLE users ADD COLUMN handle TEXT;

-- Step 2 (MIGRATE): backfill, then deploy app code that WRITES BOTH
-- columns and READS the new one. Keep them in sync via app or trigger.
UPDATE users SET handle = username WHERE handle IS NULL;

-- Step 3 (CONTRACT): once all app instances use `handle`, drop the old column
-- in a LATER deploy.
ALTER TABLE users DROP COLUMN username;
```

Each step is independently safe: at no point does running code reference a column that does not exist. The same pattern covers splitting tables, changing types, and adding `NOT NULL` constraints.

Adding an index on a large table normally locks out writes. PostgreSQL offers a non-blocking variant:

```sql
-- Builds the index without taking a write lock - safe on a live table.
CREATE INDEX CONCURRENTLY idx_users_handle ON users(handle);
```

### 🔍 Knowledge Check: Zero-Downtime
- [ ] Why can't you rename a column in a single deploy without risk?
- [ ] What are the three phases of expand-contract?
- [ ] What does `CREATE INDEX CONCURRENTLY` avoid?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Write a Reversible Migration
**Objective**: Create a migration that adds a table, then write its exact reversal.

**Requirements**:
- [ ] An `upgrade` that creates a table
- [ ] A `downgrade` that drops it
- [ ] Apply with the tool, then roll back

**Validation**: After downgrade, the table is gone and the history reflects it.

### 🟡 Intermediate Challenge: Apply and Roll Back
**Objective**: Use Alembic (or Flyway/Liquibase) to apply two migrations and then revert one.

**Requirements**:
- [ ] Two ordered migrations applied with `upgrade head`
- [ ] Revert the latest with `downgrade -1`
- [ ] Inspect the schema history to confirm state

**Validation**: The database matches exactly what the history table claims.

### 🔴 Advanced Challenge: Zero-Downtime Column Rename
**Objective**: Rename a column using expand-contract across three migration steps.

**Requirements**:
- [ ] Step 1 adds the new column (expand)
- [ ] Step 2 backfills and dual-writes (migrate)
- [ ] Step 3 drops the old column (contract)

**Validation**: At every step, a query using the "current" column name succeeds - no broken intermediate state.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Keeper of the Living Schema** - You versioned and reversed a migration
- 🛡️ **Master of the Zero-Downtime Shift** - You changed a live schema with zero downtime

**🛠️ Skills Unlocked**:
- **Versioned Migrations** - Reproducible, ordered schema change
- **Expand-Contract Deployments** - Evolve schemas under live traffic

**🔓 Unlocked Quests**:
- Backup and Recovery - Safeguard the schema you can now evolve
- Connection Pooling - Keep connections healthy across deploys

**📊 Progression Points**: +100 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Backup and Recovery](/quests/0110/backup-recovery/) - Protect against data loss

**Explore Side Adventures**:
- ⚔️ [Connection Pooling](/quests/0110/connection-pooling/) - Manage connections efficiently
- ⚔️ [Query Optimization](/quests/0110/query-optimization/) - Add indexes the safe way

### Character Class Recommendations

**💻 Software Developer**: Continue to [Backup and Recovery](/quests/0110/backup-recovery/)  
**🏗️ System Engineer**: Explore [Connection Pooling](/quests/0110/connection-pooling/)  
**📊 Data Scientist**: Advance to [Query Optimization](/quests/0110/query-optimization/)

## 📚 Resources

### Official Documentation
- [Flyway Documentation](https://documentation.red-gate.com/flyway) - SQL-first migrations
- [Liquibase Documentation](https://docs.liquibase.com/) - Changelog-driven migrations
- [Alembic Documentation](https://alembic.sqlalchemy.org/) - Python/SQLAlchemy migrations

### Community Resources
- [PostgreSQL ALTER TABLE Reference](https://www.postgresql.org/docs/current/sql-altertable.html) - The DDL behind migrations
- [Stack Overflow: database-migration tag](https://stackoverflow.com/questions/tagged/database-migration) - Migration Q&A
- [GitLab Database Migration Style Guide](https://docs.gitlab.com/ee/development/migration_style_guide.html) - Battle-tested practices

### Learning Materials
- [Martin Fowler: Evolutionary Database Design](https://martinfowler.com/articles/evodb.html) - The foundational essay
- [Expand-Contract / Parallel Change](https://martinfowler.com/bliki/ParallelChange.html) - The zero-downtime pattern explained

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Applied and rolled back a reversible migration
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0110 - Database Mastery]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Data Modeling: Schema Design and Database Relationships]]
**Unlocks:** [[Backup and Recovery: Data Protection Strategies for Databases]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
</content>
