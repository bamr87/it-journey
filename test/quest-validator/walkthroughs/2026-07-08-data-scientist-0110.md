---
title: 'Quest Walkthrough — Data Scientist · Level 0110 (Database Mastery)'
date: '2026-07-08T00:00:00.000Z'
character: data-scientist
level: '0110'
theme: Database Mastery
tier: Adventurer
quest_count: 3
mode: execute
overall_verdict: warn
session:
  window: '2 of 2 (offset 5, size 5)'
  level_total_quests: 8
  quests_walked: 3
  engine: agentic_validate.py --mode execute
  evidence: walk-evidence.json / walk-evidence.md (workflow-sealed)
  avg_score: 65.0
  verdicts: '0 pass · 2 warn · 1 fail'
  cost_usd: 2.8542
---

## 🎯 Session Summary

I walked the **Data Scientist** path through the tail window of **Level 0110 — Database Mastery** (⚔️ Adventurer tier): three linked main quests, in planner order **Backup & Recovery → Query Optimization → Connection Pooling**. This is window **2 of 2** of an 8-quest level (offset 5), so the four foundational quests (database-fundamentals, sql-mastery, data-modeling, database-security) were swept in a prior window and were **not** re-walked here.

**Headline verdict: ⚠️ warn.** The engine ran each quest's real commands in a disposable sandbox and scored an average of **65.0%** (0 pass · 2 warn · 1 fail). The *conceptual* teaching across all three is genuinely strong and mostly verified hands-on — pg_dump/pg_restore round-trips, EXPLAIN/index reasoning, and the pool-sizing math all held up under execution. But each quest ships at least one **copy-paste-and-it-breaks** defect a learner on the recommended "quickest" (Docker) path would hit immediately: an unreachable containerized DB and unwritable `/backups` path (Backup), a `users` table the seed script never creates (Query Optimization), and a PgBouncer Docker command + `pgbouncer.ini` that both fail to start plus a nonexistent psycopg2 API (Connection Pooling — the one **fail**). These are correctable content bugs, not design flaws; the chain is worth keeping and fixing.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|--:|:--:|---|--:|---|
| 1 | ⚠️ warn | Backup and Recovery: Data Protection for Databases | 70 | Logical backup + restore-drill round-trips ran flawlessly; physical backup (`pg_basebackup`/`/backups`) and the Docker path are broken as written. |
| 2 | ⚠️ warn | Query Optimization: Tuning Fast Database Queries | 73 | EXPLAIN/index/composite-index teaching verified live; the N+1 flagship rewrite references a `users` table the quest never seeds. |
| 3 | ❌ fail | Connection Pooling: Efficient Database Resource Management | 52 | Concepts sound and `pg_stat_activity` SQL works, but the "deploy PgBouncer" core (Docker cmd + `.ini`) and the Chapter 1 Python all fail on execution. |

## 🔬 Evidence

All statuses below come from commands the execute engine actually ran in the sandbox (`walk-evidence.json`), or are explicitly labelled `reasoned` where a step was judged statically (e.g. macOS/Windows paths on a Linux sandbox). I did not run any commands myself — I consumed the workflow-sealed evidence and reasoned about the linked journey over the quest sources.

### 1. Backup and Recovery — 70% (warn) · ran 4/7 runnable snippets (1✗), 6 reasoned

- ✅ **passed** · `pg_dump -Fc restoration_vault > vault_backup.dump; createdb restored_vault; pg_restore -d restored_vault vault_backup.dump`
— dump created (5314 bytes), restore succeeded, `SELECT * FROM treasure` returned the same 3 rows (gold/silver/gems). The Chapter 1 core works end to end.
- ✅ **passed** · Chapter 3 restore-drill script (`createdb drill_$(date +%Y%m%d); pg_restore …; psql … "SELECT count(*) FROM treasure;"`)
— produced `drill_20260708` with correct row count **3**. The flagship "prove your backup" habit is fully runnable.
- ✅ **passed** · Cloud/Docker `docker run --name restoration … postgres:16` — container
started and DB created (the `-it` variant failed only for lack of a TTY in the sandbox, a sandbox artifact, not counted against the quest).
- ❌ **failed** · `pg_basebackup -D /backups/base -Ft -z -P` — fails two ways: host→container
gives `FATAL: no pg_hba.conf entry for replication connection from host "172.17.0.1"`, and locally `mkdir /backups` returns **Permission denied** for a normal user. Only succeeded after re-running inside the container against the local socket into a writable path.
- 🧠 **reasoned** · macOS/Windows/Linux setup paths (standard, unrunnable on this
sandbox); `postgresql.conf` WAL config (verified `wal_level=replica` is already the PG16 default via `SHOW`); PITR recovery config (syntactically valid but omits the PG12+ `recovery.signal` requirement).

### 2. Query Optimization — 73% (warn) · ran 5/9 runnable snippets (2✗), 2 reasoned, 3 skipped

- ✅ **passed** · Seed script `CREATE TABLE events (…); INSERT … generate_series(1,100000); ANALYZE events;`
  — `INSERT 0 100000` on a local PG 16.14, exact match to expected.
- ✅ **passed** · `EXPLAIN ANALYZE SELECT * FROM events WHERE user_id = 42;` (pre-index) —
produced `Seq Scan … Rows Removed by Filter: 99983 … Execution Time: 5.555 ms`, matching the quest's described *shape* (absolute timing differs from the sample's 49.1 ms, expected hardware variance).
- ✅ **passed** · composite index `CREATE INDEX idx_events_user_action ON events(user_id, action)`
— verified the composite index serves `user_id + action` and `user_id` alone, and that `action`-only filtering falls back to Seq Scan, *exactly* as the quest claims (leftmost-prefix behaviour confirmed).
- ❌ **failed** · `CREATE INDEX idx_events_user_id …; EXPLAIN ANALYZE … WHERE user_id = 42;`
— index worked and query got ~40× faster (0.131 ms), but PG16 rendered a **Bitmap Heap Scan + Bitmap Index Scan**, not the `Index Scan using idx_events_user_id` the quest prints as sample output. Concept holds; the literal output does not reproduce.
- ❌ **failed** · Chapter 3 N+1 rewrite (JOIN/`IN` against `users`) — the embedded SQL
references a `users` table the quest's own seed script never creates; running it against the built schema fails with `ERROR: relation "users" does not exist`.
- 🧠 **reasoned / skipped** · macOS path (reasoned), Windows + Docker + illustrative
  EXPLAIN text block (skipped as unrunnable/conflicting-port).

### 3. Connection Pooling — 52% (fail) · ran 5/6 runnable snippets (3✗), 3 skipped

- ✅ **passed** · pool-sizing formula `(8*2)+1 = 17` — arithmetic verified; matches
  HikariCP's published guidance.
- ✅ **passed** · `SELECT pid, state, query, state_change FROM pg_stat_activity WHERE datname='gatekeeper' …`
  — ran verbatim against a real PG16 `gatekeeper` DB, returned the expected columns.
- ❌ **failed** · Cloud Realms `docker run --name pgbouncer … edoburu/pgbouncer` — container
exits immediately: `DB_HOST: … You must set DB_HOST env` (the image wants `DB_HOST/DB_USER/DB_PASSWORD`, not the `DATABASES_*` the quest uses); even after fixing env, `-p 6432:6432` fails because the image listens on 5432 internally.
- ❌ **failed** · `pgbouncer.ini` — loaded verbatim into real PgBouncer 1.25.2:
`FATAL cannot load config file` / `invalid value "transaction          ; return the connection after each transaction" for parameter pool_mode`. PgBouncer does **not** accept trailing same-line `;` comments; removing them made it start.
- ❌ **failed** · Chapter 1 Python — `conn.execute(query)` raises
`AttributeError: 'psycopg2.extensions.connection' object has no attribute 'execute'` (psycopg2 needs a cursor); and `ConnectionPool`/`pool.connection()` is psycopg3's API, imported nowhere.
- ⏭️ **skipped** · macOS/Windows/Linux package-manager setup paths (no sudo/brew/winget
  in sandbox; package IDs verified to exist via `apt-cache policy`).

## 🐞 Issues Found

Every issue below cites a command that actually ran or an exact line from the quest source. Severity mirrors the engine's own recommendation weighting.

**Backup and Recovery**
- **high** · *Cloud Realms / Docker path* (lines 178–188 + all of Chapter 1) — After
`docker run`/`docker exec createdb`, every later command (`pg_dump`, `createdb`, `pg_restore`, `psql`, `pg_basebackup`) is written as a bare local invocation with no `-h/-U/-P` or `docker exec` wrapper. **Observed:** a Docker-path learner has no way to reach the containerized DB. *Fix:* wrap subsequent commands in `docker exec restoration …` or export `PGHOST/PGUSER/PGPASSWORD` for host-side tools.
- **high** · *`pg_basebackup` path* (line 216) — `pg_basebackup -D /backups/base …`.
**Observed:** `mkdir /backups` → `Permission denied` for a normal user. *Fix:* have the learner `mkdir -p ~/pg_backups` (a writable path) first, and use it throughout.
- **medium** · *`pg_basebackup` prerequisites* — **Observed:** even against the quest's
own Docker container the physical backup fails with `no pg_hba.conf entry for replication connection`. *Fix:* note that pg_basebackup needs a REPLICATION role + a `pg_hba.conf` replication entry for the client address.
- **medium** · *Chapter 2 PITR recovery config* (lines 252–256) — **Observed (reasoned):**
the shown `restore_command`/`recovery_target_time` alone won't trigger recovery on the quest's stated PG14+ minimum. *Fix:* mention the PG12+ `recovery.signal` file.
- **low** · *Objectives vs body* (lines 105–106) — "Backup Automation" and "Backup
Encryption" are listed as objectives but taught nowhere. *Fix:* add a short cron/`gpg -c` example or drop the claims.
- **low** · *No teardown* — several scratch DBs + a container are created with no
  cleanup step. *Fix:* add a drop/`docker rm -f` teardown.

**Query Optimization**
- **high** · *Chapter 3 N+1 + Advanced Challenge* (lines 296–311, 342–350) — the rewrite
and the challenge's "returns identical data" validation depend on a `users` table. **Observed:** `ERROR: relation "users" does not exist` against the quest's own schema. *Fix:* seed a `users` table (e.g. `CREATE TABLE users(user_id INT PRIMARY KEY)` with the same 5000 ids), or rewrite the example to query `events` alone (`DISTINCT user_id`).
- **medium** · *Chapter 2 sample EXPLAIN output* (lines 265–267) — printed as
`Index Scan using idx_events_user_id`. **Observed:** PG16.14 chose a **Bitmap Heap Scan** instead. *Fix:* update the sample or add a caveat that a Bitmap scan is the normal PG16 choice for this selectivity (both mean the index is used).
- **medium** · *Objective vs body* (line 104) — "Composite & Covering Indexes" is
promised but `INCLUDE`/index-only scans are never shown. *Fix:* add a covering-index demo or trim the objective.
- **low** · Knowledge Check questions have no answer key; the accurate `LOWER(email)`
  sargability point (line 278) has no runnable snippet.

**Connection Pooling**
- **high** · *Cloud Realms Docker snippet* (lines 183–187) — **Observed:** container exits
with `You must set DB_HOST env`; port mapping also wrong. *Fix:* use `DB_HOST/DB_USER/DB_PASSWORD` (or `DATABASE_URL`) and `-p 6432:5432` (or add `-e LISTEN_PORT=6432`). This is the "quickest path" and it is the first thing a learner runs.
- **high** · *`pgbouncer.ini`* (lines 274–285) — **Observed:** PgBouncer 1.25.2 refuses
the file: `invalid value "transaction          ; …" for parameter pool_mode`. *Fix:* move the `;` comments to their own lines above each setting.
- **medium** · *Chapter 1 Python* (lines 203–217) — **Observed:**
`AttributeError: … no attribute 'execute'`; `ConnectionPool` is psycopg3 API. *Fix:* either label the block pseudocode, or make it runnable (psycopg2 `cursor().execute` + `ThreadedConnectionPool`, or switch consistently to psycopg3 `ConnectionPool`).
- **low** · Advanced "Catch a Leak" challenge gives no concrete leak-inducing sample;
  macOS `postgresql@16` is keg-only and may need `brew link` before `createdb`.

**No slice-wide blocking issue** prevents a knowledgeable reader from *learning* the material — every defect is a broken artifact inside an otherwise sound chapter.

## 🔗 Chain Continuity

Reading the three sources in plan order as a single learner journey:

- **The spine holds for the developer path, diverges for the Data Scientist.** The
"Continue the Main Story" links form a clean chain: Backup → Connection Pooling, Query Optimization → Connection Pooling, and Connection Pooling → *Level 0111* (it is the terminal quest, `unlocks_quests: []`, completing the level). But every quest's **Data Scientist** class recommendation points *away* from this window — Backup and Query Optimization both send the Data Scientist to `database-migrations` (a side quest not in this slice), and Connection Pooling says "Revisit Query Optimization." So a Data Scientist following their own class breadcrumbs would not naturally walk *this* three-quest order; the planner's dependency-sorted order is the coherent path, and the class recommendations feel bolted on rather than curated for this window. Worth aligning.
- **Prerequisite gaps are out-of-window, not missing.** All three quests require
`database-fundamentals` and/or `sql-mastery`, which live in window 1 of this level and were swept earlier — so the assumed SQL/JOIN/index literacy is satisfied by the level, just not by this slice. A learner dropping straight into this window cold would lack that grounding, but the frontmatter dependencies flag it correctly.
- **Setup is redundantly re-taught but consistent.** Each quest re-presents the full
four-platform (macOS/Windows/Linux/Docker) install block and uses a *distinct* scratch database (`restoration_vault`, `speed_sanctum`, `gatekeeper`) — so there is no cross-quest state collision and a learner can start any quest independently. Good isolation; mild repetition.
- **A recurring Docker-path weakness runs through the whole slice.** The same
friction — "you started a container, now how do you *reach* it for the next command" — appears in Backup (never explained) and is outright broken in Connection Pooling (bad env vars/ports). Since Docker is advertised as the "quickest" path in two of the three quests, this is the single highest-leverage fix for the slice's end-user experience: a learner picking the recommended path hits a wall in quest 1 and again in quest 3.
- **Conceptual continuity is strong.** Query Optimization explicitly motivates
Connection Pooling ("reduce the round-trip overhead you just measured"), and Backup/Pooling both frame themselves around keeping a recovered/served database healthy. The narrative arc (protect → speed up → serve efficiently → complete the Keep) is coherent and well-sequenced.

## 🧠 Reasoning & Method

- **Mode:** `execute` — the workflow pre-computed and **sealed** the evidence by
running `test/quest-validator/agentic_validate.py --mode execute` over exactly the three planned quest paths in a disposable sandbox (real PostgreSQL 16 + Docker + psycopg2). I consumed `walk-evidence.json`/`walk-evidence.md` as-is and did **not** re-run the engine (its child processes can't authenticate from my Bash tool) or modify the plan/evidence in any way.
- **What I ran vs. reasoned:** I ran **no** commands myself. Every ✅/❌ in the Evidence
section is a command the sealed engine actually executed; every 🧠 is a step judged statically (labelled `reasoned`) or `skipped` because the Linux sandbox lacks macOS/Windows/sudo. My own contribution is the **linked-journey reasoning** in Chain Continuity, derived from reading all three quest sources in plan order against the execution evidence.
- **Coverage / limits:** This is window **2 of 2** — 3 of the level's 8 quests. The
four foundational quests were **not** walked here (swept in a prior window). Snippet coverage per quest: Backup 4/7 runnable ran, Query Optimization 5/9, Connection Pooling 5/6; the remainder were `reasoned`/`skipped`, overwhelmingly OS-specific setup blocks that cannot run on a single Linux sandbox. Sample-output mismatches (Bitmap vs Index Scan) and version notes (recovery.signal) are version/selectivity dependent and are reported as such. No destructive commands were run; all work used freshly created scratch databases.
- **Confidence:** High on the concrete execution failures (each reproduced by the
engine against real tooling with quoted errors). High on continuity reasoning (drawn directly from quoted frontmatter/body). Medium on the two "sample output drift" items, which depend on PG version/selectivity and are correctly framed as caveats rather than hard bugs.

---

*One slice, one report. No quest content was modified; no branch, commit, or merge was performed. Fixable bugs are captured in Issues Found for a downstream content pass.*
