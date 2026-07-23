---
title: Data Scientist · L0110 · 2026-07-07
description: Quest-perfection walkthrough of the Database Mastery slice data-scientist/0110 on 2026-07-07,
  engine verdict warn (avg 70.2%). An evidence-based…
date: '2026-07-07T00:00:00.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Data Scientist
tags:
- data-scientist
- level-0110
- walkthrough
- quest-perfection
- warn
- database-mastery
render_with_liquid: false
excerpt: 'Data Scientist · Level 0110 — Database Mastery: an evidence-based quest-perfection walkthrough
  from 2026-07-07.'
slice: data-scientist/0110
character: data-scientist
level: '0110'
theme: Database Mastery
tier: Adventurer
verdict: warn
quest_count: 5
engine_average: 70.2
walk_date: '2026-07-07'
run_url: https://github.com/bamr87/it-journey/actions/runs/30003953368
source_report: test/quest-validator/walkthroughs/2026-07-07-data-scientist-0110.md
---

> **Slice** `data-scientist/0110` · **Level** 0110 (Database Mastery) · **Adventurer tier** · **Engine verdict** ⚠️ warn (avg 70.2%) · **Walked** 2026-07-07
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/30003953368) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-07-data-scientist-0110.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-07-data-scientist-0110.md)

---

## 🎯 Session Summary

I walked the **Data Scientist** path's first window of **Level 0110 — Database Mastery** (⚔️ Adventurer tier): five main quests played in dependency order — **Database Fundamentals → Data Modeling → SQL Mastery → Database Migrations → Database Security**. This is **window 1 of 2** the planner carved from the level's 8 quests; the remaining three (query-optimization, backup-recovery, connection-pooling) are out of scope for this run.

**Headline verdict: ⚠️ warn.** The teaching content across the slice is genuinely strong — the conceptual explanations of the relational model, normalization, JOIN semantics, ACID, and migration mechanics are technically accurate, and the *primary* worked examples run exactly as documented against a live PostgreSQL 16 instance in the sandbox. But the slice carries **one recurring, verified defect that shows up in three of the five quests**: worked code snippets reference tables (`accounts`, `orders`, `secrets`, `users`) or columns (`username`) that the quest **never has the learner create**, so a beginner typing along verbatim hits `relation "…" does not exist` at the exact moment the lesson is supposed to fire. **Database Security scored a ❌ fail (54)** because two of its three core snippets break this way *and* it also ships a Python example that calls a non-existent psycopg2 method. The engine ran in **execute mode** (sealed by the workflow); I consumed that evidence as-is and layered a static, source-level reasoning pass over the linked chain.

## 🗺️ The Journey

Per-quest line — `verdict · title · engine score · one-line takeaway`:

1. ⚠️ **Database Fundamentals: The Relational Model and ACID** — **70** · Three of
four SQL teaching blocks run verbatim and match documented output; the ACID example fails because the `accounts` table is never created.
2. ✅ **Data Modeling: Schema Design and Database Relationships** — **80** · The
core Chapter 2 schema (4 tables, composite-PK junction) executes flawlessly and the composite-key duplicate-rejection is empirically confirmed; only promised "Surrogate vs Natural Keys" content and Windows auth guidance are missing.
3. ⚠️ **SQL Mastery: Query Language Proficiency** — **75** · Every seed/query
snippet ran and matched the quest's inline expected output exactly; but Window Functions and RIGHT JOIN are promised and never taught, and two challenges demand a three-table join the two-table schema can't satisfy.
4. ⚠️ **Database Migrations: Schema Evolution and Version Control** — **72** ·
Alembic up/down and expand-contract mechanics work when run, but Chapter 2's migration alters an `orders` table the quest never creates, and the Cloud/Docker path fails on native Linux (missing `living_schema` DB + `host.docker.internal`).
5. ❌ **Database Security: Access Control and Data Encryption** — **54** ·
Least-privilege, injection-vs-parameterized, and pgcrypto claims all held up under direct execution, but the Python snippet calls a nonexistent `conn.execute()`, `users`/`secrets` tables are never created, and Auditing + two secondary objectives are asserted but never demonstrated.

**Engine roll-up:** 5 quests · 1 pass · 3 warn · 1 fail · avg **70.2%**.

## 🔬 Evidence

All `passed`/`failed` below come from commands the sealed execute engine actually ran in a disposable sandbox against PostgreSQL 16.14 (Docker `postgres:16` and/or a user-owned local cluster). Items I only judged from the source text are labeled `reasoned`.

### 1. Database Fundamentals — 70 (⚠️) · ran 5/8 runnable snippets (4 passed, 1 failed, 2 skipped, 2 reasoned)

- ✅ **Chapter 1** `CREATE TABLE members … INSERT … SELECT *` — *passed*. Produced
  exactly 2 rows matching the documented column layout.
- ✅ **Chapter 2** FK example — *passed*. Second insert failed with
`ERROR: insert or update on table "loans" violates foreign key constraint "loans_member_id_fkey"`, matching the quest's documented ERROR line.
- ❌ **Chapter 3 ACID block** `BEGIN; UPDATE accounts …` — *failed*.
`ERROR: relation "accounts" does not exist` — the `accounts` table is never created anywhere in the quest, so the atomicity lesson can't be observed as written.
- ✅ **Chapter 4** `CREATE TABLE authors/books/loans_3nf; \dt` — *passed*. All four
tables confirmed; Intermediate Challenge validated (rollback leaves `loans_3nf` count unchanged at 2).
- ✅ **Docker path** `postgres:16` — *passed* (image pulls and runs; version
16.14). macOS/Windows install blocks *skipped* (no OS); Linux `apt`/`sudo` path *reasoned* (package `postgresql` 16 confirmed available).

### 2. Data Modeling — 80 (✅) · ran 2/5 runnable snippets (2 passed, 2 skipped, 4 reasoned)

- ✅ **Chapter 2 schema** `departments/courses/students/enrolments` — *passed*.
All 4 `CREATE TABLE`s ran verbatim; `\d` confirmed every PK/FK/UNIQUE/CHECK/ composite-PK. Inserting a duplicate `(student_id, course_id)` correctly raised `duplicate key value violates unique constraint "enrolments_pkey"`, empirically proving the quest's "a student cannot enrol in the same course twice" claim.
- ✅ **Cloud/Docker path** — *passed* end-to-end (`select version()` → 16.14; only
  the literal `-it` flag fails in a non-TTY sandbox, not a quest defect).
- `reasoned` — Chapter 1/2/3 prose (entities, cardinality, 1NF→3NF) is accurate;
  Windows `winget` path and macOS `brew` path *skipped* (no OS).

### 3. SQL Mastery — 75 (⚠️) · ran 8/11 runnable snippets (8 passed, 2 skipped, 1 reasoned)

- ✅ **Seed schema + every chapter query** — *passed*, and each matched the quest's
inline expected output **exactly**: Chapter 1 `WHERE city='Rivenhold'` → Aria, Cora; Chapter 2 INNER JOIN 5 rows (Dorn absent) / LEFT JOIN 6 rows (Dorn, total NULL); Chapter 3 `GROUP BY … HAVING` → Aria 200.00 / Bram 200.00 / Cora 100.00; Chapter 4 subquery, `CREATE VIEW`, `CREATE INDEX`, and the `BEGIN…currval()…COMMIT` transaction all succeeded.
- ✅ **Docker path** — *passed*, but the container lands in the default `postgres`
database because this path (unlike macOS/Windows/Linux) never runs `createdb query_codex`.
- `reasoned` — Windows path likely fails as written (no role matching OS user,
  `psql`/`createdb` not on PATH after a fresh install).

### 4. Database Migrations — 72 (⚠️) · ran 14 snippets (11 passed, 3 failed, 2 skipped, 2 reasoned)

- ✅ **Chapter 1** `CREATE TABLE users`, **V2** `ALTER TABLE users ADD COLUMN
  display_name` — *passed*.
- ✅ `alembic init migrations`, `alembic revision -m "…"` — *passed* (correct file
  layout / skeleton generated).
- ❌ **Chapter 2 `upgrade()`** `op.add_column('orders', …)` then
`alembic upgrade head` — *failed*. `psycopg2.errors.UndefinedTable: relation "orders" does not exist`. Only after manually creating an `orders` table (a step the quest never mentions) did upgrade/downgrade succeed.
- ❌ **Cloud/Docker path** — *failed twice*: `docker run … postgres:16` never sets
`POSTGRES_DB`/`createdb`, so `living_schema` doesn't exist; and `docker run flyway/flyway -url=jdbc:postgresql://host.docker.internal/…` threw `java.net.UnknownHostException: host.docker.internal` (that hostname isn't auto-resolved on native Linux Docker Engine).
- ✅ **Chapter 3 expand-contract** (`ADD COLUMN handle`, backfill `UPDATE`,
`DROP COLUMN username`, `CREATE INDEX CONCURRENTLY`) — *passed*, **but** the `username` column was never added by Chapters 1–2, so it had to be created out-of-band to run the snippet.

### 5. Database Security — 54 (❌) · ran 4/8 runnable snippets (3 passed, 1 failed, 1 skipped, 3 reasoned)

- ✅ **Chapter 1 least-privilege** `CREATE ROLE app_login; GRANT SELECT,INSERT,
UPDATE …` — *passed*, and the Novice Challenge validation was empirically confirmed: as `app_login`, INSERT/SELECT succeeded while `DROP TABLE orders` failed with `ERROR: must be owner of table orders`.
- ❌ **Chapter 2 Python** `find_user`/`find_user_safe` — *failed*. Run against the
psycopg2 driver the quest itself names, `conn.execute(sql)` throws `AttributeError: 'psycopg2.extensions.connection' object has no attribute 'execute'` (psycopg2 needs a cursor). The parameterized `find_user_safe` logic is correct, but the shared `conn.execute()` call breaks *both* functions, and the `users` table + `conn` object are never created in the quest.
- ✅ **Chapter 3 pgcrypto** `CREATE EXTENSION pgcrypto; pgp_sym_encrypt/decrypt` —
*passed* (round-tripped to `super-secret-value`; on-disk payload confirmed binary ciphertext) — **but only after** manually creating a `secrets` table the quest never defines.
- `reasoned` — TLS connection string is intentionally illustrative (valid libpq
syntax, fails only on placeholder DNS). Auditing / Row-Level Security / Secrets Management objectives have **zero** runnable demonstration.

## 🐞 Issues Found

Grouped by severity. Every item cites a run command result or a quoted source line.

### High

- **high · Database Security · Chapter 2 Python snippet (lines ~245–257)** —
*Observed:* `conn.execute(sql)` raises `AttributeError: … connection object has no attribute 'execute'` under real psycopg2 (tested). *Fix:* use a cursor — `cur = conn.cursor(); cur.execute(sql, (name,)); return cur.fetchall()` — and show the `psycopg2.connect(...)` / `pip install psycopg2-binary` setup so the "runnable examples you can defend in a code review" promise holds.
- **high · Database Security · Chapters 2 & 3 missing schema** — *Observed:*
snippets depend on `users` and `secrets` tables that are never created; a straight-through learner hits `relation "…" does not exist` (pgcrypto block verified to fail until `secrets` was hand-created). *Fix:* add the `CREATE TABLE users (…)` and `CREATE TABLE secrets (label TEXT PRIMARY KEY, payload BYTEA)` statements before the snippets that use them.
- **high · Database Security · Auditing objective vs Advanced Challenge** —
*Observed:* Auditing is a primary objective and the Advanced Challenge demands "Show a log entry capturing who modified what and when," but the body never shows how to enable `log_statement='mod'`/pgaudit or produce a sample log line. *Fix:* add a runnable auditing example that enables logging, performs a write, and shows the resulting log entry.
- **high · Database Migrations · Chapter 2 Alembic example** — *Observed:*
`alembic upgrade head` fails with `UndefinedTable: relation "orders" does not exist` (tested). *Fix:* add a preceding step that creates `orders`, or retarget the migration at the `users` table built in Chapter 1.
- **high · Database Migrations · Cloud/Docker path** — *Observed:* two verified
failures — `living_schema` DB is never created (image defaults to `postgres`), and `host.docker.internal` doesn't resolve on native Linux Docker. *Fix:* set `POSTGRES_DB=living_schema` (or add a `createdb` step) and either drop the `host.docker.internal` example on Linux or add `--add-host=host.docker.internal:host-gateway` with a note it's Linux-required.
- **high · Database Fundamentals · Chapter 3 ACID example** — *Observed:*
`BEGIN; UPDATE accounts …` fails with `relation "accounts" does not exist` (tested). *Fix:* add `CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance NUMERIC NOT NULL)` + sample INSERTs before the transaction, or explicitly label the block as read-only pseudocode.
- **high · SQL Mastery · three-table join is unsatisfiable** — *Observed:* the
Intermediate Challenge ("Join all three relations and GROUP BY city") and the Completion Checklist ("Wrote a query joining at least three tables") require a third table, but the seed schema defines only `customers` and `orders`. *Fix:* add a third seed table (e.g. `products`/`order_items`) or rewrite the requirements to the actual two-table schema.

### Medium

- **medium · SQL Mastery · Window Functions never taught** — *Observed:* listed as
a Secondary Objective ("Rank and run totals…") and linked in Resources, but no `OVER()`/`RANK()`/`ROW_NUMBER()` content exists in the body. *Fix:* add a short window-functions example (a running total or per-city ranking fits the data), or drop the objective.
- **medium · SQL Mastery · RIGHT JOIN promised, not shown** — *Observed:* primary
objective promises "INNER, LEFT, and RIGHT" but only INNER/LEFT get examples; RIGHT JOIN appears only in a knowledge-check question. *Fix:* add a brief RIGHT JOIN example or reword the objective.
- **medium · SQL Mastery · Docker path lands in wrong database** — *Observed:* the
Docker path never runs `createdb query_codex`, so it connects to `postgres` unlike the other three paths (tested). *Fix:* add a `createdb query_codex` step.
- **medium · Data Modeling · "Surrogate vs Natural Keys" undelivered** —
*Observed (reasoned):* listed as a Secondary Objective but never discussed; the schema silently uses `SERIAL` surrogate keys without contrasting them with natural keys. *Fix:* add a short paragraph, or remove the objective.
- **medium · Database Fundamentals · secondary objectives undelivered** —
*Observed (reasoned):* `CHECK` constraint and primary-key indexing ("Indexes (preview)") are listed as objectives but never taught in the body. *Fix:* add a small `CHECK (balance >= 0)` example + one sentence on B-tree PK lookups, or soften the objectives.
- **medium · Database Security · pgcrypto key handling contradicts Chapter 2** —
*Observed (reasoned):* Chapter 3 embeds the passphrase directly in SQL text (`pgp_sym_encrypt('…','encryption-key')`), which leaks into logs/WAL — one chapter after preaching "never glue values into SQL text." *Fix:* bind the passphrase as a driver parameter and note the logging risk.

### Low

- **low · Windows path (all five quests)** — *Observed (reasoned):* the Windows
`winget` blocks omit `-U postgres`/password handling; after a fresh EDB install there is no role matching the OS user and `psql`/`createdb` aren't on PATH, so bare `createdb <db>` likely fails with `role "<user>" does not exist`. *Fix:* add `-U postgres`, note the install password, and mention adding the bin dir to PATH.
- **low · Database Migrations · Chapter 3 `username` continuity** — *Observed:*
the expand-contract snippet reads a `username` column the Chapter 1 `users` table never had (had to be added out-of-band to run). *Fix:* keep the `users` table consistent across chapters, or label the snippet as a standalone example.
- **low · Database Migrations · `CREATE INDEX CONCURRENTLY` overstated** —
*Observed (reasoned):* "without taking a write lock" is imprecise; CONCURRENTLY still takes a SHARE UPDATE EXCLUSIVE lock and can leave an INVALID index on failure. *Fix:* soften the phrasing.
- **low · Database Fundamentals · 2NF example** — *Observed (reasoned):* the 2NF
discussion uses a member-duplication example that really illustrates general redundancy/3NF rather than partial dependency on a composite key. *Fix:* use a genuine composite-key example.

## 🔗 Chain Continuity

The planner's ordering is dependency-clean, and I confirmed each quest's `quest_dependencies` are satisfied by earlier quests **in this window**:

- `database-fundamentals` → required: none (correct opener).
- `data-modeling` → required: `database-fundamentals` ✅ (position 2).
- `sql-mastery` → required: `database-fundamentals` ✅, recommended:
  `data-modeling` ✅ (both precede it).
- `database-migrations` → required: `data-modeling` ✅, recommended:
  `sql-mastery` ✅ (both precede it).
- `database-security` → required: `database-fundamentals` ✅, recommended:
  `sql-mastery` ✅.

**As a learning path it holds together conceptually.** Normalization is introduced in Fundamentals Ch4 and deliberately revisited in Data Modeling Ch3 (which even says "You met it briefly in Database Fundamentals") — good reinforcing continuity. JOIN/aggregation in SQL Mastery build naturally on the keys taught earlier. A Data Scientist reader accumulates relational modeling → querying → schema evolution → security in a sensible arc.

**But the slice is stitched from self-contained databases, not one shared state.** Each quest spins up its own DB (`datakeep`, `modeling_realm`, `query_codex`, `living_schema`, `warded_vault`) and its own schema, so nothing a learner builds in quest N carries into N+1. That's a defensible design, but it means the "linked journey" is conceptual rather than stateful — and it makes the biggest cross-cutting problem more visible:

**Systemic theme — "phantom tables."** Three of the five quests present a *headline* worked example that references an object the quest never creates:
- Fundamentals: the ACID demo needs `accounts` — never created.
- Migrations: the Alembic Ch2 demo alters `orders` — never created; Ch3 reads
  `username` — never added.
- Security: the injection demo needs `users`; the pgcrypto demo needs `secrets` —
  neither created.

Because each quest opens a psql session during platform setup and then invites the learner to "follow along," these gaps are not cosmetic — they are the exact points where a real beginner is stopped cold by `relation "…" does not exist`. This is a **level-wide authoring pattern** a content pass should sweep, not five unrelated one-offs.

**Second cross-cutting theme — objectives promised but not delivered.** Every quest except Data Modeling's core lists objectives with no body content: CHECK/index (Fundamentals), Window Functions/RIGHT JOIN (SQL Mastery), Surrogate-vs-Natural Keys (Data Modeling), Auditing/RLS/Secrets Management (Security). The Mastery Challenges then sometimes *test* the missing content (SQL Mastery's three-table join; Security's "show a log entry"), so a diligent learner is asked to demonstrate something the quest never taught.

**Ordering nit:** `database-security` sits after `database-migrations` in the walk order, but security only *requires* Fundamentals and *recommends* SQL Mastery — it has no dependency on Migrations, so its placement is arbitrary (harmless, since it's self-contained). Data Scientists are actually routed by the "Character Class Recommendations" toward Query Optimization rather than Security, so Security reads more as a Security-Specialist side-branch that this window happens to include.

## 🧠 Reasoning & Method

- **What I ran vs. reasoned:** I did **not** re-run the execute engine — per the
skill, `./walk-evidence.json` / `./walk-evidence.md` were pre-computed and **sealed by the workflow** (the engine's child `claude` processes can't authenticate from an agent's Bash tool). I consumed that sealed evidence verbatim. Every `passed`/`failed` in §4 traces to a command the engine actually ran in its disposable sandbox against PostgreSQL 16.14. I then performed the linked-journey pass myself by reading all five quest sources in plan order and reasoning about continuity, prerequisites, and beginner friction. Items I judged only from the source text (no execution) are labeled `reasoned`.
- **Mode:** `execute` (sealed). Snippet coverage per quest, from the evidence:
Fundamentals 5/8 runnable, Data Modeling 2/5, SQL Mastery 8/11, Migrations 14 recorded, Security 4/8. Un-run snippets were mostly OS-specific setup (macOS `brew`, Windows `winget`) that can't execute in a Linux sandbox, or `sudo`-gated Linux steps blocked by sandbox policy — validated by analogy against a non-sudo local cluster, not directly. Those are honest coverage gaps, not clean passes.
- **Scope/limits:** This is **window 1 of 2** — only 5 of the level's 8 quests were
walked. Query Optimization, Backup & Recovery, and Connection Pooling are **unwalked** and say nothing about this run's verdict. No macOS/Windows path was executed anywhere in the slice, so all Windows-auth issues are `reasoned` predictions of a well-known pitfall, not observed failures.
- **Confidence:** High on the executed findings (the phantom-table failures and the
psycopg2 `.execute()` bug were reproduced with concrete error messages). Medium on the reasoned findings (missing-objective coverage confirmed by reading the full body; Windows-path failures are strong-but-unverified predictions).
- **No content mutated.** My only write is this report. The issues above are for a
separate content pass (content-curator / a human) to act on; I did not branch, commit, or edit any quest.

---

_Appended machine summary (verbatim from `walk-evidence.md`):_

> **5** quests evaluated · ✅ 1 pass · ⚠️ 3 warn · ❌ 1 fail · avg **70.2%** ·
> ~$3.8777
