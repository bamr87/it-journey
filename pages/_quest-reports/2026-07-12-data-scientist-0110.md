---
title: Data Scientist · L0110 · 2026-07-12
description: Quest-perfection walkthrough of the Database Mastery slice data-scientist/0110 on 2026-07-12,
  engine verdict warn. An evidence-based, learner's-eye…
date: '2026-07-12T00:00:00.000Z'
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
  from 2026-07-12.'
slice: data-scientist/0110
character: data-scientist
level: '0110'
theme: Database Mastery
tier: Adventurer
verdict: warn
quest_count: 3
walk_date: '2026-07-12'
run_url: https://github.com/bamr87/it-journey/actions/runs/29190829265
source_report: test/quest-validator/walkthroughs/2026-07-12-data-scientist-0110.md
---

> **Slice** `data-scientist/0110` · **Level** 0110 (Database Mastery) · **Adventurer tier** · **Engine verdict** ⚠️ warn · **Walked** 2026-07-12
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29190829265) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-12-data-scientist-0110.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-12-data-scientist-0110.md)

---

## 🎯 Session Summary

I played the **Data Scientist** path's **Level 0110 — Database Mastery** (Adventurer ⚔️)
slice as a learner: the second and final rotating window of the level, covering its
last three main quests — **Backup and Recovery**, **Query Optimization**, and
**Connection Pooling**. All three were executed for real by the sealed agentic engine
in a disposable sandbox against a live PostgreSQL 16 (and PgBouncer 1.22.0) instance;
I then read each quest source in plan order and reasoned about the linked journey.

**Headline verdict: ⚠️ warn — the slice is *conceptually* strong but has verified,
learner-blocking code bugs, one of which fails a whole quest.** Average score 66.3%
(0 pass · 2 warn · 1 fail). The teaching content — backup types, PITR, RTO/RPO,
EXPLAIN plans, indexing, pool sizing, leak diagnosis — is accurate and was verified
byte-for-byte against a real server. What drags the slice down is a **recurring
Docker/Cloud-path defect**: across two of the three quests, the "Cloud Realms" path
gives commands that do not actually work (missing table creation, missing connection
flags, wrong env-var names), and Connection Pooling additionally ships a
`pgbouncer.ini` that a real PgBouncer refuses to load. A maintainer should treat
**Connection Pooling (52%, fail)** as the priority fix, then the two high-severity
Docker/index issues in the other two quests.

## 🗺️ The Journey

Plan order (dependency-sorted; this window is quests 6–8 of 8):

1. ⚠️ **Backup and Recovery: Data Protection for Databases** — **73%** ·
   native pg_dump/pg_restore/pg_basebackup/restore-drill all verified working on live
   PG16, but the Docker path is broken (no `treasure` table, no connection flags) and
   the "Backup Encryption" objective has zero supporting content.
2. ⚠️ **Query Optimization: Tuning Fast Database Queries** — **74%** ·
   seed script, composite-index and sargable-predicate claims all verified true, but
   the flagship "prove the index win" example claims a plain `Index Scan` when PG16
   reproducibly produces a `Bitmap Heap Scan` — a mismatch a learner hits immediately.
3. ❌ **Connection Pooling: Efficient Database Resource Management** — **52%** ·
   pool-sizing math and leak diagnosis verified accurate, but the two runnable
   artifacts (PgBouncer Docker command + `pgbouncer.ini`) both fail to run as written.

## 🔬 Evidence

All outcomes below are from commands the execute engine actually ran in the sandbox
(`executed: true` for every quest). Config/prose/pseudocode snippets it could not run
are labelled `reasoned`. Quoted output is trimmed from `walk-evidence.json`.

### 1. Backup and Recovery — 73% ⚠️ · ran 5/7 runnable snippets (3✓ / 2✗), 6 reasoned
- ✅ **`pg_dump -Fc … | createdb … | pg_restore …`** (with connection env set) —
  *passed*: "dump was 5314 bytes, restore succeeded, and `SELECT count(*) FROM treasure`
  on restored_vault returned 3, matching the 3 inserted rows."
- ✅ **`pg_basebackup -D /backups/base -Ft -z -P`** — *passed*, producing
  `base.tar.gz`, `pg_wal.tar.gz`, `backup_manifest` — **but only after** manually
  granting `host replication postgres all trust` in `pg_hba.conf`; the default
  `postgres:16` image blocks replication and the quest never mentions this.
- ✅ **Chapter 3 restore-drill script** (`createdb drill_$(date …); pg_restore …; psql … count`)
  — *passed*, "created drill_20260712, restored the dump, and returned count=3."
- ❌ **`docker exec -it restoration psql …`** — *failed* (`the input device is not a TTY`,
  a sandbox artifact) — but critically the Cloud path "never creates the `treasure`
  table (only the other 3 platform paths do)."
- ❌ **`pg_dump -Fc restoration_vault > vault_backup.dump`** (bare, Docker setup) —
  *failed*, exit 2: `connection to server on socket "/var/run/postgresql/.s.PGSQL.5432"
  failed: No such file or directory`. The Docker learner is never told to set
  `PGHOST/PGUSER/PGPASSWORD` or pass `-h/-U`.
- `reasoned`: macOS/Windows/Linux setup paths (no OS available), the `postgresql.conf`
  WAL-archiving and recovery snippets (config-only; GUC names verified real against a
  live PG16), and the RTO/RPO prose.

### 2. Query Optimization — 74% ⚠️ · ran 4/9 runnable snippets (3✓ / 1✗), 4 skipped, 2 reasoned
- ✅ **Seed script** (`CREATE TABLE events …; INSERT … generate_series(1,100000); ANALYZE`)
  — *passed*: "CREATE TABLE / INSERT 0 100000 / ANALYZE — exactly as expected."
- ✅ **Baseline `EXPLAIN ANALYZE … WHERE user_id = 42`** — *passed*: "`Seq Scan on
  events … Rows Removed by Filter: 99983 … Execution Time: 5.716 ms`" (the illustrative
  49.1 ms is just an example, acceptable).
- ✅ **Composite index** `(user_id, action)` — *passed*: used for `user_id=… AND action=…`,
  correctly **not** used for `action` alone (fell back to Seq Scan) — exactly as claimed.
- ❌ **`CREATE INDEX idx_events_user_id …; EXPLAIN ANALYZE …`** — *failed against the
  quest's stated output*: the index worked and time dropped 5.7 ms → 0.13 ms, "BUT the
  actual plan was `Bitmap Heap Scan` + `Bitmap Index Scan`, not the `Index Scan using
  idx_events_user_id on events` claimed in the quest's inline comment. Reproduced across
  4 different user_id values; only `SET enable_bitmapscan=off` produced the plain Index
  Scan the quest describes." This is quest source line 265.
- `skipped`: the four per-OS setup blocks (no macOS/Windows; sudo denied; port 5432
  already bound) — equivalent functionality was verified via native PG16 binaries.
- `reasoned`: the illustrative sample-output text block and the `db.query(...)` N+1
  **pseudocode** (its embedded SQL was extracted and run successfully; the wrapper API
  matches no real Python driver).

### 3. Connection Pooling — 52% ❌ · ran 6/6 runnable snippets (2✓ / 4✗), 1 skipped, 2 reasoned
- ✅ **Leak-hunt query** (`SELECT … FROM pg_stat_activity WHERE datname='gatekeeper'`) —
  *passed*: returned expected columns, "a leaked (idle in transaction) connection
  reproduced by a Python script correctly showed up."
- ✅ **Pooled psycopg3 pattern** (`with pool.connection() as conn: … conn.execute`) —
  *passed* when adapted with `psycopg_pool.ConnectionPool` — matches psycopg3's real API.
- ❌ **PgBouncer Docker command** (`docker run … edoburu/pgbouncer -e DATABASES_HOST=…`)
  — *failed*: "Container exits immediately with `DB_HOST: … You must set DB_HOST env` —
  the image needs `DB_HOST/DB_USER/DB_PASSWORD/DB_NAME`, not `DATABASES_*`. Even after
  fixing env var names, the image listens on 5432 by default, so `-p 6432:6432` also
  fails unless `LISTEN_PORT=6432` is added." This is quest source lines 184–186.
- ❌ **`pgbouncer.ini`** (Chapter 3) — *failed* to load in real PgBouncer 1.22.0:
  `ERROR invalid value "transaction          ; return the connection after each
  transaction" for parameter pool_mode` — PgBouncer treats the trailing inline `;`
  comment as part of the value. "Same failure reproduces for the max_client_conn and
  default_pool_size lines." This is quest source lines 282–284.
- ❌ **psycopg2 anti-pattern** (`conn = psycopg2.connect(...); conn.execute(query)`) —
  *failed*: "psycopg2 Connection objects have no `.execute()` method (verified
  `hasattr(conn,'execute')` is False); running this literally raises AttributeError."
  (Illustrative, but technically wrong for the named driver.)
- ❌ **`docker run … postgres:16 -p 5432:5432`** — *failed* on `port is already
  allocated` in the sandbox; succeeded on 5433 — base command is sound but fragile to a
  learner's existing local Postgres.
- `skipped`/`reasoned`: sudo-gated Linux setup (packages confirmed current on Ubuntu
  24.04 via non-root download) and the macOS/Windows brew/winget paths.

## 🐞 Issues Found

Every issue below cites an observed sandbox result or a quoted source line. Severities
mirror the engine's own recommendations, which I confirmed against the quest sources.

**Backup and Recovery** (`pages/_quests/0110/backup-recovery.md`)
- **high** · Cloud Realms Path (lines 178–188) · The Docker path never creates the
  `treasure` table (the other 3 paths do, line 146/159/173) and every later `pg_dump/
  createdb/psql/pg_restore/pg_basebackup` has no host/user/password flags. **Observed:**
  bare `pg_dump -Fc restoration_vault` against the container fails with a Unix-socket
  connection error. **Fix:** add the `CREATE TABLE treasure(...)` step to the Docker
  path and instruct `export PGHOST=localhost PGUSER=postgres PGPASSWORD=quest` (or add
  `-h localhost -U postgres` to every subsequent command).
- **medium** · Chapter 2 recovery config (lines 252–256) · The recovery snippet omits
  the `recovery.signal` file that PostgreSQL 12+ requires to enter recovery mode.
  **Observed (reasoned against a live PG16):** a learner copying only what's shown would
  not actually trigger PITR. **Fix:** mention `touch recovery.signal` in the data dir.
- **medium** · Secondary objective "Backup Encryption" (line 106) · **Observed:** zero
  supporting content anywhere in the quest body; only punted to a different quest under
  Next Steps. **Fix:** add a short `pg_dump … | gpg --symmetric` example or relabel the
  objective as out-of-scope.
- **low** · Chapter 1 `pg_basebackup` (line 216) · Requires replication privileges /
  `pg_hba.conf` entries absent by default (confirmed: `postgres:16` blocks it out of
  the box). **Fix:** note the prerequisite for containerized/managed Postgres.
- **low** · Windows Empire Path (lines 156–159) · Bare `createdb`/`psql` likely fail on
  the EDB installer, which does not map the OS user to a Postgres role. **Fix:** add
  `-U postgres` and a password note. *(reasoned — no Windows env.)*

**Query Optimization** (`pages/_quests/0110/query-optimization.md`)
- **high** · Chapter 2 "Add an Index and Prove the Win" (line 265) · The comment claims
  `Index Scan using idx_events_user_id on events`. **Observed:** PG16 reproducibly
  produces a `Bitmap Heap Scan`/`Bitmap Index Scan` pair at this selectivity (across 4
  user_id values); the plain Index Scan only appears with `enable_bitmapscan=off`. A
  learner comparing output will think they did it wrong. **Fix:** show the real
  bitmap-scan output and briefly explain bitmap vs plain index scans.
- **medium** · Secondary objective "Composite & Covering Indexes" (line 104) ·
  **Observed:** covering indexes / index-only scans (`INCLUDE`) are never taught in the
  body. **Fix:** add a short covering-index subsection or drop "Covering" from the title.
- **medium** · Secondary objective "Statistics & ANALYZE" (line 105) · **Observed:** only
  a one-line comment `-- refresh planner statistics` (line 207). **Fix:** show a
  stale-stats plan vs post-ANALYZE plan and mention autovacuum.
- **low** · Novice Challenge validation ("Seq Scan to Index Scan") · **Fix:** reword to
  "to an index-based scan (Index Scan or Bitmap Heap Scan)" to match real planner output.
- **low** · Chapter 3 `db.query(...)` snippet (lines 203–217 region) · **Observed:** the
  API matches no real Python driver. **Fix:** label as pseudocode or use psycopg2/SQLAlchemy.

**Connection Pooling** (`pages/_quests/0110/connection-pooling.md`) — *quest fails at 52%*
- **high** · Chapter 3 `pgbouncer.ini` (lines 282–284) · Trailing inline `; comment`
  annotations. **Observed:** PgBouncer 1.22.0 fails to start with a fatal `invalid value
  … for parameter pool_mode` because the `;` is parsed into the value (same for
  `max_client_conn`, `default_pool_size`). **Fix:** move `;` comments to their own lines
  above each setting, or drop them.
- **high** · Cloud Realms Path (lines 184–186) · Wrong env vars `DATABASES_HOST/USER/
  PASSWORD` and no `LISTEN_PORT`. **Observed:** container exits immediately demanding
  `DB_HOST`; even fixed, it listens on 5432 so `-p 6432:6432` doesn't route. **Fix:**
  use `DB_HOST/DB_USER/DB_PASSWORD/DB_NAME` (or `DATABASE_URL`) and add `-e LISTEN_PORT=6432`.
- **medium** · Chapter 3 `pgbouncer.ini` completeness · **Observed:** no `auth_type`/
  `auth_file`, which PgBouncer requires to authenticate any client. **Fix:** include
  them or explicitly note the omission with a pointer.
- **medium** · Chapter 1 Python (lines 203–209) · **Observed:** `conn.execute()` raises
  `AttributeError` on a psycopg2 connection. **Fix:** disambiguate the driver and use
  `cur = conn.cursor(); cur.execute(query)` for psycopg2.
- **low** · Intermediate Challenge validation (line 331) · No concrete way to observe
  "many clients → few server connections". **Fix:** point to PgBouncer's `SHOW POOLS;` /
  `SHOW CLIENTS;` admin console.
- **low** · Secondary objective "Application Pools" · **Observed:** never demonstrated.
  **Fix:** add a short HikariCP or SQLAlchemy pool config example.

## 🔗 Chain Continuity

**Where this window sits.** This is window **1 of 2** (offset 5) — the *tail* of the
8-quest level. The dependency graph places these three correctly last: both
Backup and Recovery and Query Optimization declare `unlocks_quests:
/quests/0110/connection-pooling/`, and Connection Pooling in turn `recommends`
Query Optimization — so Connection Pooling sitting third in plan order is coherent.
The hard prerequisites the three assume — `database-fundamentals` (backup, pooling) and
`sql-mastery` (query-opt) — live in the **earlier window (quests 1–5)**, so a learner
sweeping the whole level in order arrives here adequately prepared. Someone dropping
straight into *this window alone* would be missing that foundation, but that is by
design of the windowing, not a quest defect.

**Loose coupling between the three (good).** Each quest stands up its own database
(`restoration_vault`, `speed_sanctum`, `gatekeeper`) and carries no state forward, so
finishing quest N never leaves an artifact quest N+1 depends on. As a learning path
they read as three parallel arcs (Vault of Restoration → Speed Sanctum → Gatekeeper's
Discipline) rather than a single cumulative build. That is fine for isolation and means
no broken hand-off between quests — the friction is *within* each quest, not *between*.

**Systemic cross-quest defect: the Docker/Cloud path.** The most important
linked-journey finding is that the identical "Choose Your Adventure Platform" template
degrades the same way in **two of the three quests**. Backup and Recovery and
Connection Pooling both present the Cloud/Docker path as an equal peer of the native
paths, but the native paths implicitly rely on a Homebrew/Ubuntu setup where bare
`createdb`/`psql` "just work" against a local socket, while the Docker path exposes
Postgres only over TCP and never surfaces the connection env vars. A beginner who
picks Docker in quest 1 will hit a wall, pick it again in quest 3, and hit the same
wall plus a non-loading `pgbouncer.ini`. This is one root cause worth fixing once,
consistently, across the level's platform template — not three unrelated bugs.

**Difficulty pacing.** The ordering is reasonable but not monotonic: Medium (backup) →
Hard (query-opt) → Medium (pooling). The Hard middle quest is the most technically
accurate of the three; the Medium closer (pooling) is the one that fails. So a learner's
*experienced* difficulty spikes at the end for the wrong reason (broken artifacts, not
concept depth) — reinforcing that Connection Pooling's fixes are the highest-value work.

## 🧠 Reasoning & Method

- **Mode: execute (strong evidence).** I consumed the workflow-sealed
  `walk-evidence.json` / `walk-evidence.md` produced by the agentic execute engine
  (`mock: false`, `executed: true` for all three quests, ~$2.92, 3 sessions, PostgreSQL
  16.14 / PgBouncer 1.22.0). Per skill step 2 I did **not** re-run the engine (its child
  `claude` processes can't authenticate from my Bash tool) and did **not** modify the
  plan or evidence. Every `passed`/`failed` above is a command the engine actually ran;
  everything I could only judge statically is labelled `reasoned`.
- **What I ran vs. reasoned.** The engine ran the core DB commands live (dumps,
  restores, base backups, EXPLAIN plans, index creation, `pg_stat_activity`, PgBouncer
  config load, Docker containers). Per-OS setup for macOS/Windows was `reasoned` (no such
  environment); several Linux paths were `skipped` because the sandbox denies `sudo` but
  the same functionality was validated with native binaries. My own contribution was
  reading all three quest sources in plan order and cross-checking each machine finding
  against the exact quoted lines (178–188, 252–256, 265, 184–186, 282–284) — every issue
  in this report is anchored to both a run result and a source line.
- **Coverage & limits.** Snippet coverage: backup-recovery 5/7 runnable (6 reasoned),
  query-optimization 4/9 (4 skipped, 2 reasoned), connection-pooling 6/6 (1 skipped, 2
  reasoned). Uncovered surface is the non-Linux OS setup paths (can't be executed in a
  Linux sandbox) and pure prose/pseudocode — none of it invalidates the executed
  findings. The sandbox is network-restricted to what quests safely need; no destructive
  commands were run.
- **Confidence.** High on the executed findings (each reproduced, several across
  multiple inputs). Medium on the reasoned Windows/macOS claims (plausible but not run).
  The `overall_verdict: warn` reflects the aggregate honestly: two usable-with-caveats
  quests plus one genuine **fail** (Connection Pooling, 52%) that a learner cannot
  complete as written until its Docker command and `pgbouncer.ini` are fixed. No
  fabricated output, scores, or issues — all numbers trace to `walk-evidence.json`.

---

*Machine evidence summary (verbatim from `walk-evidence.md`): 3 quests · 0 pass ·
2 warn · 1 fail · avg 66.3% · ~$2.9223. Backup and Recovery 73 (5/7, 2✗) · Query
Optimization 74 (4/9, 1✗) · Connection Pooling 52 (6/6, 4✗).*
