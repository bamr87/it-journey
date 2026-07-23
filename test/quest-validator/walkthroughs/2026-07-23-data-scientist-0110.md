---
title: 'Walkthrough — Data Scientist · Level 0110 (Database Mastery)'
date: '2026-07-23T00:00:00.000Z'
character: data-scientist
level: '0110'
theme: Database Mastery
tier: Adventurer
quest_count: 5
mode: execute
overall_verdict: warn
session:
  window: '1 of 2 (quests 1–5 of 8)'
  scored: 4
  errored: 1
  average_score: 78.5
  engine_cost_usd: 2.8384
  evidence: walk-evidence.json (sealed by workflow, consumed as-is)
---

## 🎯 Session Summary

I walked the first window of the **Data Scientist → Level 0110 "Database Mastery"** arc as a learner: five linked `main_quest`s (Database Fundamentals → Data Modeling → SQL Mastery → Database Migrations → Database Security), all built on a single PostgreSQL 16 spine. The sealed execute-engine evidence scored **4 of 5** quests (2 pass, 2 warn) at an average **78.5%**; the fifth, **Database Migrations**, produced **no verdict** — the engine hit the sandbox's `sudo`/`docker` permission walls plus a `rm -rf` denial and ran out of turns (harness limitation, *not* a proven content failure).

Headline verdict: **warn**. The two foundational quests (Fundamentals 83, Data Modeling 86) are genuinely solid and verified end-to-end against a live Postgres 16. The two warns are earned by concrete, reproducible defects a beginner *will* hit: **SQL Mastery** over-promises (RIGHT JOIN and Window Functions are stated objectives never taught; its Intermediate Challenge demands "three relations" from a two-table schema), and **Database Security** ships two snippets that fail as literally written (a `secrets` table that is never created, and a `psycopg2` API that does not exist). The most valuable cross-quest finding is a **shared Docker-setup bug** that recurs in four of the five quests — and which the fifth quest (Migrations) already demonstrates the fix for.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ✅ pass | Database Fundamentals: The Relational Model and ACID | 83 | Every SQL snippet (incl. the intentional FK-violation and ROLLBACK demo) ran verbatim; only defect is the Docker-path database never being created. |
| 2 | ✅ pass | Data Modeling: Schema Design and Database Relationships | 86 | ER → normalization → 4-table schema verified live, composite-key uniqueness confirmed; loses points for an untaught "surrogate vs natural keys" objective. |
| 3 | ⚠️ warn | SQL Mastery: Query Language Proficiency | 71 | Teaching content is excellent and all 7 queries reproduce documented output — but RIGHT JOIN + Window Functions are promised and never delivered, and a challenge references a nonexistent third table. |
| 4 | ❌ no verdict | Database Migrations: Schema Evolution and Version Control | — | Engine exhausted its turns against `sudo`/`docker` permission denials before scoring; reasoned-only below. Biggest toolchain jump in the slice (Alembic/pip/Flyway). |
| 5 | ⚠️ warn | Database Security: Access Control and Data Encryption | 74 | Core security claims held up under live testing, but two snippets fail as written (`secrets` table never created; `conn.execute` isn't a psycopg2 method) and RLS is checklisted yet untaught. |

## 🔬 Evidence

All outcomes below are from the sealed `walk-evidence.json` — commands the execute engine actually ran in its disposable sandbox against a real PostgreSQL 16 server (verbatim quotes trimmed). I did **not** re-run the engine.

### 1. Database Fundamentals — 83 (pass) · ran 6/9 runnable snippets (6 passed, 0 failed, 2 skipped, 2 reasoned)
- **`CREATE TABLE members` / INSERT / SELECT** — `passed`: "produced the same 2-row, 4-column result shape as the documented sample output."
- **FK violation (Chapter 2)** — `passed`: second insert "failed with 'ERROR: insert or update on table "loans" violates foreign key constraint "loans_member_id_fkey"' — matches the quest's quoted error text exactly."
- **BEGIN/UPDATE/UPDATE/COMMIT transfer** — `passed`: "final balances were 50 and 150 as the narrative describes, correctly demonstrating atomicity."
- **Chapter 4 3NF tables + Intermediate Challenge** — `passed`: "\dt showed all four required tables … FK-violating insert inside BEGIN/ROLLBACK leaves loans_3nf count unchanged at 2."
- **Docker path** — `passed` but flagged: "no database named 'datakeep' is ever created — psql connects to the default 'postgres' database."
- **macOS / Windows / Linux install blocks** — `reasoned`/`skipped` (no macOS/Windows in a Linux sandbox; `sudo` blocked). Equivalent Postgres 16 behavior reproduced without sudo.

### 2. Data Modeling — 86 (pass) · ran 2/5 runnable snippets (2 passed, 0 failed, 3 skipped, 3 reasoned)
- **4-table schema (departments/courses/students/enrolments)** — `passed`: "All 4 CREATE TABLE statements succeeded … ran the 4-table JOIN (matches Intermediate Challenge's validation) and got correct output."
- **Composite PK uniqueness** — `passed`: duplicate `(student_id=1, course_id=1)` insert "failed with `duplicate key value violates unique constraint "enrolments_pkey"`," confirming the quest's claim.
- **Docker path** — `passed` (`-i` used because the sandbox shell has no TTY — a sandbox artifact, not a quest bug).
- **Install blocks + text/ER diagrams** — `skipped`/`reasoned` (OS-specific or illustrative, non-executable).

### 3. SQL Mastery — 71 (warn) · ran 7/11 runnable snippets (7 passed, 0 failed, 4 skipped)
- **Seed schema** — `passed`: "CREATE TABLE, CREATE TABLE, INSERT 0 4, INSERT 0 5 — no errors."
- **SELECT/WHERE/ORDER BY** — `passed`: returned "Aria/Rivenhold and Cora/Rivenhold, exactly matching the documented expected output."
- **INNER vs LEFT JOIN** — `passed`: "INNER JOIN returned 5 rows, no Dorn. LEFT JOIN returned 6 rows including Dorn with NULL total."
- **GROUP BY / HAVING aggregation** — `passed`: "Aria 2/200.00, Bram 1/200.00, Cora 2/100.00 — exact match to documented table."
- **Subquery + VIEW + INDEX + transaction (currval)** — all `passed`.
- **Not run:** the four platform-setup snippets (`skipped` — OS-specific or sudo-blocked).

### 4. Database Migrations — no verdict (engine error) · 0 snippets scored
- Engine terminated with `claude exited 1 … "terminal_reason":"max_turns" … "errors":["Reached maximum number of turns (40)"]`.
- Two `permission_denials` recorded: `sudo systemctl start postgresql …` and a `docker ps -a; rm -rf …/test_concurrent.py`. These are the sandbox's safety layer doing its job; the engine burned its 40 turns working around them and never emitted a scored verdict.
- **No `passed`/`failed` evidence exists for this quest.** Everything I say about it below is `reasoned` from reading the source only.

### 5. Database Security — 74 (warn) · ran 4/8 runnable snippets (2 passed, **2 failed**, 3 skipped, 1 reasoned)
- **Least-privilege role (Chapter 1)** — `passed`: `SET ROLE app_login; DROP TABLE orders;` → "ERROR: must be owner of table orders"; app_login could INSERT (sequence grant works) but `DELETE` → "ERROR: permission denied for table orders" — exactly the Novice Challenge validation.
- **Injection concept** — `passed`: with corrected cursor code, malicious `' OR '1'='1` "returned every row … the parameterized version returned `[]`."
- **Python "safe" snippet as written** — **`failed`**: "`conn.execute(sql, (name,))` raises `AttributeError: 'psycopg2.extensions.connection' object has no attribute 'execute'`."
- **pgcrypto block as written** — **`failed`**: "both the INSERT and SELECT fail with `ERROR: relation "secrets" does not exist`" (no `CREATE TABLE secrets` precedes it). Round-trip works only after the table is added manually.
- **TLS `sslmode=verify-full`** — `reasoned`: valid libpq syntax; only failure was DNS of the placeholder host, as expected.

## 🐞 Issues Found

Every item cites a command the engine actually ran (`tested`) or an exact line I read in the source (`reasoned`). This is not an empty result — there are two high-severity, reproducible content bugs.

**HIGH**

1. **`tested` · SQL Mastery · Chapter 2 / Primary Objectives & Knowledge Check** — RIGHT JOIN is promised ("Combine tables with `INNER`, `LEFT`, and `RIGHT` joins", line 99) and quizzed ("When would you reach for a `RIGHT JOIN`…?", line 283) but **never demonstrated** with code; only INNER/LEFT appear. Window Functions (line 106) is a bonus objective *with a dedicated resource link* yet has zero content. *Fix:* add a worked RIGHT JOIN and a short `RANK()/SUM() OVER` example over the existing customers/orders schema, or rewrite the objectives to only claim what is taught.

2. **`tested` · Database Security · Chapter 3 pgcrypto block (lines 293–297) & Chapter 2 Python (lines 246–257)** — Both fail as literally written. The pgcrypto INSERT/SELECT hit `relation "secrets" does not exist` (no `CREATE TABLE secrets` precedes them, unlike Chapter 1 which sets up `orders`); the "safe" example calls `conn.execute(...)`, which psycopg2 connections do not have (`AttributeError`) even though the prose names psycopg. *Fix:* add `CREATE TABLE secrets (label TEXT, payload BYTEA);` before the INSERT, and change to `cur = conn.cursor(); cur.execute(sql, (name,)); return cur.fetchall()`.

**MEDIUM**

3. **`tested` · SQL Mastery · Intermediate Challenge (line 390)** — "Join all three relations and `GROUP BY city`" is impossible: the seeded schema (lines 195–214) defines only `customers` and `orders`. This also contradicts the quest's own frontmatter (`completion_requirements: A multi-table query joining at least three tables`, and the `skill_demonstration` join-three-tables criterion). *Fix:* reword to "Join customers and orders" (revenue per city needs only those two), or add a third table.

4. **`tested`(1)/`reasoned`(3) · Shared Docker-setup bug · Fundamentals, SQL Mastery, Database Security (and latent in Data Modeling)** — Each Docker path names the container after the intended database but never creates that database, so `docker exec … psql -U postgres` lands the learner in the default `postgres` DB, diverging from the macOS/Windows/Linux paths and from later "in your `datakeep`/`query_codex`/`warded_vault` database" references. Confirmed live for Fundamentals (`\l` showed only postgres/template0/template1); read in the source for SQL Mastery (line 184) and Security (line 184). *Fix:* mirror what **Database Migrations already does correctly** — `docker run … -e POSTGRES_DB=<name> …` (line 189 of database-migrations.md) — across the other four quests, or add an explicit `createdb`.

5. **`reasoned` · Data Modeling · Secondary Objectives (line 106)** — "Surrogate vs Natural Keys" is listed but never discussed; every table silently uses a `SERIAL` surrogate with no trade-off explanation. *Fix:* add a short callout on why SERIAL over a natural key (e.g. email) and when a natural key wins.

6. **`reasoned` · Database Security · Secondary Objectives (line 106)** — "Row-Level Security" is checklisted but never mentioned; no `CREATE POLICY` / `ENABLE ROW LEVEL SECURITY` example exists. *Fix:* add a short RLS example on `orders`, or drop the objective.

**LOW**

7. **`reasoned` · Database Fundamentals · macOS path (lines 146–154)** — `postgresql@16` is a keg-only Homebrew formula, so `createdb`/`psql` may not be on `PATH` without `brew link`/a PATH export. The Windows section warns "adjust the path to psql if needed" (line 167); macOS has the same class of issue and no warning.

8. **`reasoned` · SQL Mastery & Data Modeling · Windows paths** — Unqualified `createdb query_codex` / `createdb modeling_realm` typically fail on a fresh winget/EDB install that only provisions a password-authed `postgres` role; a beginner may need `-U postgres`.

9. **`reasoned` · Database Migrations · Chapter 2 Alembic example (lines 266–274)** — `op.add_column('orders', …)` assumes an `orders` table, but the quest's `living_schema` only ever creates `users` (V1, line 214). A learner running the example verbatim hits "table orders does not exist." *Fix:* either seed an `orders` table or target `users` for consistency. (Not executed — engine errored before scoring this quest.)

10. **`reasoned` · Database Fundamentals · Chapter 3 ACID table (line 303)** — the Isolation row ("Two librarians issuing loans don't reuse a loan_id") conflates isolation with uniqueness/sequence generation; a concurrency example (two transfers not seeing each other's uncommitted balances) would be cleaner for a beginner.

## 🔗 Chain Continuity

Read in plan order, carrying each quest's state into the next:

- **Dependency graph is sound and matches the frontmatter.** Fundamentals has no prereqs and unlocks the rest; Data Modeling *requires* Fundamentals; SQL Mastery requires Fundamentals (recommends Data Modeling); Security requires Fundamentals (recommends SQL Mastery); Migrations requires Data Modeling (recommends SQL Mastery). A Data Scientist walking 1→2→3→5 never meets a step whose prerequisite the slice didn't already provide. The `unlocks_quests` and `[[wiki-link]]` graphs are internally consistent.

- **Concept hand-offs are deliberate and well-sequenced.** Fundamentals Ch4 teaches 1NF–3NF; Data Modeling Ch3 opens with "You met it briefly in Database Fundamentals; here you apply it as a modeling step" (line 289) — an explicit, correct callback. Keys/FKs from Fundamentals Ch2 are the exact prerequisite SQL Mastery's JOIN chapter leans on. The pedagogical arc holds.

- **Each quest is a fresh, self-contained environment — by design, but worth naming.** Every quest spins up a *different* database (`datakeep` → `modeling_realm` → `query_codex` → `living_schema` → `warded_vault`) and re-seeds its own schema, so no data carries across quests. That is good for isolation and lets a learner start anywhere, but it means the "members/loans" schema built in Fundamentals is never reused — SQL Mastery introduces a brand-new customers/orders world. No continuity break, just a note that the arc is a set of parallel sandboxes, not one growing database.

- **The one true cross-quest defect is the Docker setup pattern** (Issue #4). Four quests share the "container named X, database X never created" bug, and the *fifth* (Migrations) is the only one that does it right (`-e POSTGRES_DB=living_schema`). A learner who chose the Docker path in Fundamentals and hit the mismatch would carry that confusion through SQL Mastery and Security too — so fixing it once, consistently, pays off across the whole slice.

- **The difficulty/tooling cliff is at Migrations.** Quests 1–3 and 5 need only Postgres + `psql` (and psycopg2 for one Security snippet). Migrations abruptly demands `pip`, `alembic`, `psycopg2-binary`, optionally Docker'd Flyway, plus Git familiarity — a much heavier lift. Credit where due: the Linux path correctly handles PEP 668 with a venv (lines 174–177) and the Flyway `--add-host=host.docker.internal:host-gateway` note (line 193) is thoughtful. But this is exactly the spot the execute engine also stalled (sudo/docker walls), which mirrors where a real beginner on a locked-down machine would get stuck. This quest deserves its own dedicated re-walk once the harness can grant it a working Postgres + tool sandbox.

## 🧠 Reasoning & Method

- **Mode:** `execute` — the sealed evidence (`walk-evidence.json`) was pre-computed by the workflow's deterministic engine step against a real PostgreSQL 16 in a disposable sandbox. I consumed it **as-is** and did not (and cannot) re-run the engine from my Bash tool, per the skill and the auth constraint. I did not edit `walk-plan.json` or `walk-evidence.*`.
- **What is `tested`:** every `passed`/`failed` in §4 Evidence and Issues #1, #2, #3, and the Fundamentals half of #4 come from commands the engine actually ran (quoted, trimmed). Two real failures were observed in Database Security.
- **What is `reasoned`:** everything about **Database Migrations** (the engine errored out before scoring — no machine verdict exists), plus the OS-specific install paths (no macOS/Windows and no `sudo` in a Linux sandbox), the Windows-auth and Homebrew-PATH notes, the Docker-bug for SQL Mastery/Security (read in source, only Fundamentals was executed), and Issues #5–#10. These are labeled inline and are not counted as pass/fail.
- **Coverage I capped or could not reach:** This is **window 1 of 2** — 5 of the level's 8 quests. The remaining three (Query Optimization, Backup & Recovery, Connection Pooling) were *not* in my plan and were not walked; the ledger sweeps them in a later run. Within the window, one quest (Migrations) has **no scored evidence**. Snippet coverage per quest is stated in §4 (e.g. Fundamentals 6/9, SQL Mastery 7/11, Security 4/8); platform-install snippets are consistently `skipped` because the sandbox is a single non-sudo Linux host.
- **Confidence:** High on the two pass quests and on the four evidenced defects (Issues #1–#4 partial) — they were reproduced against a live server. Medium on the source-only reasoned issues. Low/none on Database Migrations' runtime behavior, which was never scored; treat its verdict as **unknown**, not passing.
- **Session verdict = warn**, driven by two earned warns and one unscored quest — not by any pass being downgraded. No quest content was modified; this report is my only write. Handing off to the caller for git.
