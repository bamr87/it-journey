---
title: Data Scientist · L0110 · 2026-07-27
description: Quest-perfection walkthrough of the Database Mastery slice data-scientist/0110 on 2026-07-27,
  engine verdict warn. An evidence-based, learner's-eye…
date: '2026-07-27T13:31:17.000Z'
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
  from 2026-07-27.'
slice: data-scientist/0110
character: data-scientist
level: '0110'
theme: Database Mastery
tier: Adventurer
verdict: warn
quest_count: 5
walk_date: '2026-07-27'
run_url: https://github.com/bamr87/it-journey/actions/runs/30264458312
source_report: test/quest-validator/walkthroughs/2026-07-27-data-scientist-0110.md
---

> **Slice** `data-scientist/0110` · **Level** 0110 (Database Mastery) · **Adventurer tier** · **Engine verdict** ⚠️ warn · **Walked** 2026-07-27
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/30264458312) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-27-data-scientist-0110.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-27-data-scientist-0110.md)

---

## 🎯 Session Summary

I walked the first window of the **Data Scientist → Level 0110 "Database Mastery"** arc — 5 of the level's 8 quests, in the dependency-sorted order the planner fixed: **Database Fundamentals → Data Modeling → SQL Mastery → Database Migrations → Database Security**. Evidence is the sealed `walk-evidence.json` the workflow pre-computed with the execute engine (real commands run against a live **PostgreSQL 16** container in the disposable sandbox); I consumed it as-is and then re-read every quest source to reason about the linked journey.

**Headline verdict: ⚠️ warn.** The SQL teaching in this slice is genuinely strong — the first three quests scored 85/91/93, and every runnable SQL snippet the engine executed produced output matching the quest text *character-for-character* (FK-violation error text, composite-key rejection, HAVING/COALESCE aggregates, currval transaction semantics). The two 🔴 Hard quests at the end (**Migrations 73**, **Security 66**) each contain a **reproducible hard failure** for a learner following top-to-bottom: a table the quest tells you to alter/insert into is never created (`orders` in Migrations Ch.2; `secrets` in Security Ch.3). Layered on top is a recurring **objectives-vs-content gap** (objectives promise topics — Indexes preview, Surrogate keys, RIGHT JOIN, Window Functions, RLS, Secrets Management — that the body never teaches) and a slice-wide cosmetic defect: **all five files end with a stray `</content>` authoring artifact**. None of these block the *learning*, but the two Hard quests are not copy-paste-runnable as written, which is what pulls the slice to warn.

## 🗺️ The Journey

| # | Quest | Verdict | Score | One-line takeaway |
|---|---|:--:|--:|---|
| 1 | Database Fundamentals: The Relational Model and ACID | ✅ pass | 85 | Rock-solid relational foundation; SQL runs verbatim, but "Indexes (preview)" objective is never taught and the ACID block isn't copy-paste-clean. |
| 2 | Data Modeling: Schema Design and Database Relationships | ✅ pass | 91 | Excellent ER/junction-table teaching that ran clean; only gap is the un-taught "Surrogate vs Natural Keys" objective. |
| 3 | SQL Mastery: Query Language Proficiency | ✅ pass | 93 | Best quest of the slice — every SELECT/JOIN/GROUP BY/subquery/view matched documented output; RIGHT JOIN + Window Functions listed but not covered. |
| 4 | Database Migrations: Schema Evolution and Version Control | ⚠️ warn | 73 | Conceptually strong, but Ch.2 Alembic revision alters an `orders` table the quest never creates → real `UndefinedTable` failure; CONCURRENTLY-in-transaction caveat missing. |
| 5 | Database Security: Access Control and Data Encryption | ⚠️ warn | 66 | Least-privilege + injection lessons are accurate and ran live, but Ch.3 pgcrypto block fails (`secrets` table never created) and 2 bonus objectives are unbuilt. |

**Aggregate:** 5 quests · ✅ 3 pass · ⚠️ 2 warn · ❌ 0 fail · avg **81.6%** · engine cost ~$3.60.

## 🔬 Evidence

All command results below are from the sealed execute-mode evidence (`walk-evidence.json`), where each quest was sandboxed and its safe commands run against a real Postgres 16 instance. `reasoned` = the engine judged the step statically (prose or a platform path it didn't execute); `skipped` = a setup command it declined to run (e.g. `sudo apt`/`brew`/`winget` host installs). Snippet coverage is quoted from `walk-evidence.md`.

### 1. Database Fundamentals — 85 · ran 8/9 runnable snippets
- **passed** — Ch.1 `CREATE TABLE members` + INSERT + SELECT ran in psql 16 and produced the exact shape shown (dates differ only because `CURRENT_DATE` = today).
- **passed** — Ch.2 FK failing insert reproduced the **exact** quoted error: `ERROR: insert or update on table "loans" violates foreign key constraint "loans_member_id_fkey"`.
- **passed** — Ch.3 `accounts` CHECK(balance >= 0): a manual negative-balance UPDATE was rejected with `violates check constraint "accounts_balance_check"` (behavior the quest asserts but never demonstrates).
- **passed** — Novice Challenge: `\dt` confirmed all four required tables; Intermediate Challenge: `BEGIN; INSERT … member_id 999; ROLLBACK;` failed on FK then left `count(*)` unchanged (2 → 2), exactly as the validation criterion demands.
- **reasoned** — macOS/Windows install paths; the `loans_flat` denormalization is a `text` block, not runnable.
- **skipped** — Linux `sudo apt install postgresql`.
- Engine note: the literal ACID block (source lines 318-326) prints `ROLLBACK` **and** `COMMIT` in sequence; pasted whole it triggers `WARNING: there is no transaction in progress`.

### 2. Data Modeling — 91 · ran 2/5 runnable snippets
- **passed** — Docker path launched; the full Ch.2 schema (`departments`/`courses`/`students`/`enrolments` with SERIAL PKs, FK REFERENCES, and the composite PK on the junction table) created cleanly, and the composite-key duplicate-enrolment rejection held exactly as described.
- **reasoned** — Ch.1 entity/attribute notation and Ch.3 normalization are `text` illustrations (correctly judged, not executed).
- **skipped** — macOS/Windows/Linux install paths.

### 3. SQL Mastery — 93 · ran 8/11 runnable snippets
- **passed** — seed schema (`customers`/`orders`) + Ch.1 `WHERE city='Rivenhold' ORDER BY name LIMIT 10` returned Aria, Cora as printed.
- **passed** — INNER vs LEFT JOIN: Dorn (no orders) absent from INNER, present with NULL total in LEFT, matching the quest's annotations.
- **passed** — Ch.3 `GROUP BY … HAVING COALESCE(SUM(o.total),0) >= 100 ORDER BY lifetime_value DESC` produced the exact leaderboard (Aria 200 / Bram 200 / Cora 100).
- **passed** — Ch.4 subquery, `CREATE VIEW customer_value`, `CREATE INDEX idx_orders_customer_id`, and the `currval('customers_customer_id_seq')` transaction all ran successfully.
- **skipped** — macOS/Windows/Linux installs.

### 4. Database Migrations — 73 · ran 9/10, **1 failed**
- **passed** — Docker path with `-e POSTGRES_DB=living_schema`; Flyway-via-Docker `info`; Ch.1 `CREATE TABLE users` + `ALTER TABLE … ADD COLUMN display_name`; `alembic init` + `alembic revision`; `alembic upgrade head`/`downgrade -1`; Ch.3 expand-contract `ADD COLUMN handle` → backfill → `DROP COLUMN username`; and `CREATE INDEX CONCURRENTLY idx_users_handle` (run standalone in psql).
- **❌ failed** — Ch.2 Alembic `upgrade()`/`downgrade()` for `orders.status`. Engine detail: *"Code itself is syntactically and semantically correct, but running it via `alembic upgrade head` fails because the quest never has the learner create the `orders` table — reproduced UndefinedTable error when following the quest literally from a clean Chapter-1 state."*
- **reasoned** — macOS/Windows install paths; `flyway_schema_history` illustration.
- Engine caveat: `CREATE INDEX CONCURRENTLY` ran fine in raw psql, but inside a default Alembic migration it would fail (Alembic wraps migrations in a transaction; CONCURRENTLY can't run in one) — unmentioned in the quest.

### 5. Database Security — 66 · ran 3/8, **1 failed**
- **passed** — Ch.1 `CREATE TABLE orders` + `CREATE ROLE app_login LOGIN PASSWORD …` + scoped `GRANT SELECT, INSERT, UPDATE` (+ sequence USAGE) executed exactly as written; least-privilege behavior confirmed.
- **passed** — Ch.2 vulnerable `find_user` vs parameterized `find_user_safe` snippet judged accurate.
- **❌ failed** — Ch.3 pgcrypto block. Engine detail: *"CREATE EXTENSION succeeded, but both INSERT and SELECT failed with 'ERROR: relation "secrets" does not exist' because the quest never shows a CREATE TABLE secrets statement anywhere. Only succeeds if the learner independently guesses a table schema (I added `CREATE TABLE secrets (label TEXT, payload BYTEA)` myself, after which the block worked correctly and the payload column stored ciphertext, not plaintext)."*
- **reasoned** — the `sslmode=verify-full` TLS connection string (needs a real remote host + cert).
- **skipped** — all four platform install paths (macOS/Windows/Linux/Docker).

## 🐞 Issues Found

Each item cites what was witnessed — a sandbox command result from the sealed evidence (`tested`) or an exact line I read in the quest source (`reasoned`). Severity reflects learner impact.

**HIGH**
1. **[high · database-migrations · Ch.2, source lines 261-274 · tested]** The Alembic revision runs `op.add_column('orders', …)` but no chapter ever creates an `orders` table (Ch.1 creates only `users`). Engine reproduced `UndefinedTable` on `alembic upgrade head` from a clean state. **Fix:** add an explicit `CREATE TABLE orders (order_id SERIAL PRIMARY KEY);` (or a prior Alembic revision that creates it) before the "add status to orders" step.
2. **[high · database-security · Ch.3, source lines 289-298 · tested]** The pgcrypto block does `INSERT INTO secrets …` / `SELECT … FROM secrets` but there is no `CREATE TABLE secrets` anywhere in the file; engine hit `relation "secrets" does not exist`. **Fix:** add `CREATE TABLE secrets (label TEXT PRIMARY KEY, payload BYTEA);` before the INSERT.
3. **[high · database-migrations · Ch.3, source lines 318-321 · reasoned]** `CREATE INDEX CONCURRENTLY` is presented right after Alembic content, but CONCURRENTLY cannot run inside a transaction block and Alembic wraps migrations in one by default — the most common real failure when a learner applies this via the tool they were just taught. **Fix:** add a caveat + the `op.get_context().autocommit_block()` (or `transactional_ddl = False`) escape hatch.
4. **[high · sql-mastery · Primary Objectives, source line 99 · reasoned]** Primary objective lists `INNER, LEFT, and RIGHT joins` but Chapter 2 teaches only INNER and LEFT; RIGHT JOIN appears only as a Knowledge-Check question (line 283). A required objective promises coverage the body never delivers. **Fix:** add a RIGHT JOIN example or drop it from the *primary* objective.
5. **[high · database-security · Secondary Objectives, source line 106 · reasoned]** "Row-Level Security" is listed as a bonus objective but never taught (no `CREATE POLICY` / `ENABLE ROW LEVEL SECURITY` anywhere). **Fix:** add a short RLS section or remove the objective.

**MEDIUM**
6. **[medium · database-fundamentals · Secondary Objectives, source line 110 · reasoned]** "Indexes (preview) — Understand why a primary key is automatically fast to look up" is a stated objective with zero supporting content in the body. **Fix:** add a sentence noting a PK auto-creates a unique B-tree index, or drop the objective.
7. **[medium · database-fundamentals · Ch.3 ACID block, source lines 318-326 · tested]** The block prints both `ROLLBACK;` and `COMMIT;` in sequence; pasted verbatim it yields `WARNING: there is no transaction in progress`. It *is* commented "choose one branch," but it isn't copy-paste-clean. **Fix:** split into two labeled snippets (failure branch vs success branch).
8. **[medium · data-modeling · Secondary Objectives, source line 105 · reasoned]** "Surrogate vs Natural Keys" is listed but never taught — the schema uses SERIAL surrogate keys throughout with no natural-key contrast. **Fix:** add a short comparison paragraph or drop the objective.
9. **[medium · sql-mastery · Secondary Objectives, source line 106 · reasoned]** "Window Functions" is a listed bonus objective but appears only as an external resource link (line 442), with no in-quest example. **Fix:** add a small `RANK() OVER (…)` or running-total example.
10. **[medium · database-security · Secondary Objectives + Advanced Challenge, source lines 104, 329-337 · reasoned]** "Secrets Management" is listed but only gestured at via the `'rotate-me-in-a-vault'` string; the Advanced Challenge asks the learner to "show a log entry capturing who modified what and when" with no command to enable logging. **Fix:** add a concrete secrets example and an `ALTER SYSTEM SET log_statement='mod'` + sample log line.
11. **[medium · database-migrations · macOS + Windows setup, source lines 142-161 · reasoned]** macOS path runs a bare `pip install alembic psycopg2-binary` without the PEP 668/venv caveat the Linux path (lines 174-177) correctly includes; Windows `createdb living_schema` gives no auth context. **Fix:** mirror the Linux venv note on macOS; clarify `-U postgres`/auth on Windows.

**LOW**
12. **[low · ALL FIVE quests · end of file · reasoned]** Every file ends with a stray `</content>` authoring/tool-call artifact (`database-fundamentals.md` line 485 also has `</invoke>`; `data-modeling.md` L413, `sql-mastery.md` L467, `database-migrations.md` L421, `database-security.md` L400). Confirmed by reading each source. Cosmetic but published. **Fix:** delete the trailing artifact lines (a slice-wide sweep).
13. **[low · database-fundamentals / data-modeling / sql-mastery · Cloud/Docker setup · reasoned]** The Docker paths `docker exec … psql -U postgres` land in the default `postgres` database, while the macOS/Windows/Linux paths create and enter a named DB (`datakeep` / `modeling_realm` / `query_codex`). Harmless (SQL still runs) but silently inconsistent. **Fix:** add a `createdb`/`CREATE DATABASE` step to the Docker path so all four platforms converge on the same DB name.
14. **[low · database-security · Ch.2 Python snippet, source lines 243-258 · reasoned]** The injection example uses `conn.execute(...)` with no imports/connection and an undefined `users` table — presented as illustrative, but a beginner may try to run it. **Fix:** label it explicit pseudocode or make it a runnable script.

**No fabricated issues.** Everything above is either a sandbox result in the sealed evidence or a line I read directly in the quest source; nothing is inferred beyond what is cited.

## 🔗 Chain Continuity

Read as one journey a Data Scientist would actually take, the slice holds together conceptually but has two concrete continuity breaks:

- **Prerequisite metadata is coherent.** `quest_dependencies` form a clean DAG: Fundamentals (no deps) → unlocks the rest; Data Modeling requires Fundamentals; SQL Mastery requires Fundamentals (recommends Data Modeling); Migrations requires Data Modeling (recommends SQL Mastery); Security requires Fundamentals (recommends SQL Mastery). A learner walking in plan order always has the declared prerequisite in hand. Vocabulary compounds naturally — Fundamentals teaches keys/FKs/ACID, Data Modeling reuses them for ER/junction tables, SQL Mastery queries exactly that shape.

- **Break #1 — each quest uses its own throwaway database, so cross-quest state never carries.** Fundamentals builds `datakeep`, Data Modeling `modeling_realm`, SQL Mastery `query_codex`, Migrations `living_schema`, Security `warded_vault`. That's fine pedagogically (each quest is self-contained), **but** it means the two "missing table" failures cannot be rescued by an earlier quest. Migrations Ch.2 alters `orders`, and SQL Mastery *did* create an `orders` table — but in a *different* database (`query_codex`), so a learner in `living_schema` still hits `UndefinedTable`. The quest must create its own `orders`. Same logic for Security's `secrets`. These are true in-quest breaks, not just isolation artifacts.

- **Break #2 — the "objectives promise more than the body teaches" pattern recurs across the whole slice** (Indexes preview, Surrogate keys, RIGHT JOIN, Window Functions, RLS, Secrets Management). A diligent learner who treats the objective checklist as a contract will finish each quest with unchecked boxes and no content to check them against. This is the single most consistent friction across the five quests and would erode trust in the checklist as a completion signal.

- **Ordering is sound.** Nothing in a later quest silently assumes a skill an earlier quest skipped; the difficulty ramp (Medium → Medium → Hard → Hard → Hard) tracks the actual cognitive load. The **remaining 3 quests of the level** (this was window 1 of 2 — `total_quests: 8`) were not walked; a future run should sweep them before the level is certified.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sandboxed, real PostgreSQL 16 via Docker). I did **not** run the engine — per the skill and the workflow contract, `walk-evidence.json` + `walk-evidence.md` were sealed by a deterministic workflow step (the engine's child `claude` processes can't authenticate from an agent's Bash tool). I consumed them **verbatim** and did not edit, regenerate, or hand-write any evidence, plan, or score.
- **What I ran vs. reasoned:** I ran no quest commands myself. All `passed`/`failed`/`skipped` verdicts and quoted outputs come from the sealed evidence. My own contribution is the **linked-journey analysis** — I `Read` all five quest sources in plan order and verified, by direct reading, the objectives-vs-content gaps, the cross-database continuity breaks, and the trailing `</content>` artifacts (confirmed with a repo grep across the five files). Items labeled `reasoned` were judged statically against the source; items labeled `tested` cite a sandbox command result.
- **Coverage & limits:** 5 of 8 quests (window 1 of 2) — I did **not** expand beyond the planned window. Snippet execution was partial by design: platform install commands (`sudo apt`/`brew`/`winget`) were `skipped` as unsafe/host-mutating, and prose/diagram blocks were `reasoned`. TLS (`sslmode=verify-full`) and pgaudit steps require external infrastructure and were not executed. Engine line numbers in a couple of recommendations were approximate; where I cite a line I used the number I verified in the source, not the engine's.
- **Confidence:** High on the two HIGH failures (both reproduced by the engine against a live instance and independently confirmed by reading the source — the referenced tables genuinely do not exist in-quest). High on the objectives-vs-content and trailing-artifact findings (directly read). Medium on the CONCURRENTLY-in-transaction caveat (reasoned about Alembic's default transaction behavior, not executed inside a migration). This is a genuine execute-mode walkthrough of a real learner path, not a mock or review-only pass.

---

### Appendix — machine evidence (verbatim from `walk-evidence.md`)

> **5** quests evaluated · ✅ 3 pass · ⚠️ 2 warn · ❌ 0 fail · avg **81.6%** · ~$3.6009
>
> | | Score | Quest | Snippets run |
> |---|--:|---|:-:|
> | ✅ | 85 | Database Fundamentals: The Relational Model and ACID | 8/9 |
> | ✅ | 91 | Data Modeling: Schema Design and Database Relationships | 2/5 |
> | ✅ | 93 | SQL Mastery: Query Language Proficiency | 8/11 |
> | ⚠️ | 73 | Database Migrations: Schema Evolution and Version Control | 9/10 (1✗) |
> | ⚠️ | 66 | Database Security: Access Control and Data Encryption | 3/8 (1✗) |
