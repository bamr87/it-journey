---
title: 'Walkthrough — Data Scientist · Level 0110 (Database Mastery)'
date: '2026-07-10T00:00:00.000Z'
character: data-scientist
level: '0110'
theme: Database Mastery
tier: Adventurer
quest_count: 3
mode: execute
overall_verdict: fail
session:
  window: 2 of 2 (quests 6-8 of 8)
  quests_walked:
    - /quests/0110/backup-recovery/
    - /quests/0110/query-optimization/
    - /quests/0110/connection-pooling/
  average_score: 63.3
  verdicts: { pass: 0, warn: 2, fail: 1 }
  engine: agentic_validate.py --mode execute (PostgreSQL 16 sandbox)
  evidence: walk-evidence.json / walk-evidence.md (workflow-sealed)
  cost_usd: 2.5327
---

## 🎯 Session Summary

I walked the **closing window of the Data Scientist "Database Mastery" (0110) Adventurer** level as a learner: quests **6–8 of 8** — *Backup and Recovery*, *Query Optimization*, and *Connection Pooling* — in dependency order. Evidence is the workflow-sealed **execute-mode** run of the agentic engine, which provisioned a live PostgreSQL 16 sandbox and ran each quest's safe commands for real; I then re-read all three quests in plan order and reasoned about the linked journey.

The conceptual teaching across the slice is genuinely strong and mostly **verified true by running it** (pg_dump/pg_restore round-trips, a full end-to-end PITR rewind, the index speedup, the composite-index column-order rule, and the idle-in-transaction leak fingerprint all reproduced exactly). But the session verdict is **fail**, driven by one hard-failing capstone quest and a **systemic bug in every Docker path**: the containerized "quickest" route — the one a beginner is most likely to pick — is broken or divergent in all three quests. *Connection Pooling* (45%, the level's capstone) is the worst: its recommended pgbouncer container never starts and its Chapter 3 config file won't parse, so a learner hits three separate failures before reaching a working pooler. *Backup and Recovery* (75%) and *Query Optimization* (70%) each carry one high-severity, sandbox-reproduced defect on top of accurate cores.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 6 | ⚠️ warn | [Backup and Recovery](/quests/0110/backup-recovery/) | 75 | Cores work end-to-end (PITR really rewound), but the PITR snippet omits the mandatory `recovery.signal` → hard FATAL on startup. |
| 7 | ⚠️ warn | [Query Optimization](/quests/0110/query-optimization/) | 70 | Index/EXPLAIN teaching verified true, but the Docker path never creates/selects `speed_sanctum` and Ch2 asserts an `Index Scan` Postgres actually renders as a `Bitmap` scan. |
| 8 | ❌ fail | [Connection Pooling](/quests/0110/connection-pooling/) | 45 | Accurate concepts, but the two most safety-critical runnable artifacts — the pgbouncer container and the `pgbouncer.ini` — are both broken as written. |

**Slice:** 0 pass · 2 warn · 1 fail · avg **63.3%** · mode **execute** · **fail** overall.

## 🔬 Evidence

All statuses below come from commands the engine actually ran in the PostgreSQL 16 sandbox (`passed`/`failed`), or are `reasoned` where a step was OS-specific, sudo-gated, or illustrative pseudocode. Nothing here is asserted without a source.

### Quest 6 — Backup and Recovery — ran **6/7** runnable snippets (1 ✗)

- ✅ `passed` — `pg_dump -Fc restoration_vault > vault_backup.dump` → 5311-byte custom-format dump after 3 rows (gold, silver, gems).
- ✅ `passed` — `createdb restored_vault && pg_restore -d restored_vault vault_backup.dump` → restored cleanly; `SELECT * FROM treasure` returned all 3 original rows.
- ✅ `passed` (with caveat) — `pg_basebackup -D /backups/base -Ft -z -P` produced `base.tar.gz`/`pg_wal.tar.gz`/`backup_manifest`, **but hung on `waiting for checkpoint`** on an idle server until a manual `CHECKPOINT` was forced (no `-c fast` in the snippet).
- ✅ `passed` — WAL archiving block (`wal_level=replica`, `archive_mode=on`, `archive_command='cp %p ...'`) applied to a real `postgresql.conf`; after restart, WAL segments appeared in the archive dir. The full PITR was then driven end-to-end and **correctly rewound the cluster to just before a deliberately inserted `BAD_UPDATE_MISTAKE` row** — the mechanism the quest teaches is real.
- ❌ `failed` — recovery config (`restore_command` + `recovery_target_time` in `postgresql.conf`, no `recovery.signal`): restored cluster refused to start —
  > FATAL: could not locate required checkpoint record
  Adding `recovery.signal` (a step **absent from the quest**) made the exact same PITR succeed.
- ✅ `passed` (with caveat) — restore drill `createdb drill_$(date +%Y%m%d) …` worked first run (count = 3), but **failed on a second same-day run** (`database "drill_20260710" already exists`), conflicting with the quest's own "drill regularly" advice.
- 🧠 `reasoned` — macOS/Windows/Linux-sudo install paths not runnable in the Linux sandbox (sudo denied); SQL/CLI portion validated on an equivalent non-sudo PG16 instance.

### Quest 7 — Query Optimization — ran **5/9** runnable snippets (2 ✗, 3 skipped)

- ✅ `passed` — seed: `CREATE TABLE events … INSERT … generate_series(1,100000); ANALYZE` → `INSERT 0 100000`, `count = 100000`.
- ✅ `passed` — `EXPLAIN ANALYZE SELECT * FROM events WHERE user_id = 42` → `Seq Scan … Rows Removed by Filter: 99977`, matching the quest's hedged "something like" shape.
- ❌ `failed` — Cloud/Docker path: container pulled and ran (verified `pg_isready`, `SELECT version()`), **but this path never runs `createdb speed_sanctum` nor connects to it** — unlike all three other platform paths — leaving the learner in the default `postgres` DB.
- ❌ `failed` (mismatch) — `CREATE INDEX idx_events_user_id …; EXPLAIN ANALYZE …`: index created and query dropped to **0.084 ms vs 5.8 ms** (speedup claim holds), **but the real plan was `Bitmap Heap Scan` + `Bitmap Index Scan`, not the literal `Index Scan using idx_events_user_id`** the quest's code comment shows.
- ✅ `passed` — composite index `(user_id, action)`: used for `user_id = 42 AND action = 'login'`, and `WHERE action = 'login'` alone fell back to `Seq Scan` — the column-order rule verified exactly as taught.
- 🧠 `reasoned` — the Python N+1 vs JOIN block is pseudocode (undefined `db`); the underlying JOIN SQL was run directly against a built `users` table and returned correctly joined rows in one round trip.
- ⏭️ `skipped` — macOS/Windows/Linux-sudo install paths (OS-specific / sudo-gated).

### Quest 8 — Connection Pooling — ran **8/6** runnable snippets (3 ✗; includes corrected re-runs)

- ✅ `passed` — `docker run --name gatekeeper-db … postgres:16` → ready; `SELECT version()` = PostgreSQL 16.14.
- ❌ `failed` — recommended pgbouncer container (`-e DATABASES_HOST/USER/PASSWORD`, `-p 6432:6432`): **exits immediately (code 2)** —
  > DB_HOST: Setup pgbouncer config error! You must set DB_HOST env
  The `edoburu/pgbouncer` entrypoint expects `DB_HOST/DB_USER/DB_PASSWORD`, and the image listens on **5432** internally, not 6432.
- ✅ `passed` (corrected, not in quest) — with `DB_HOST/DB_USER/DB_PASSWORD`, `-p 6432:5432`, and `AUTH_TYPE=scram-sha-256` (to match PG16's default auth), `psql -h 127.0.0.1 -p 6432 … 'SELECT 1'` succeeded through PgBouncer.
- ❌ `failed` — Chapter 3 `pgbouncer.ini` with trailing inline `;` comments, loaded into real PgBouncer 1.25.2 —
  > ERROR invalid value "transaction          ; return the connection after each transaction" for parameter pool_mode … FATAL cannot load config file
  PgBouncer does not support same-line trailing comments.
- ✅ `passed` (corrected) — same `.ini` with comments removed → `listening on 127.0.0.1:6432`, `process up: PgBouncer 1.25.2`.
- ✅ `passed` — the leak query `SELECT … FROM pg_stat_activity WHERE datname = 'gatekeeper'` ran **only after `gatekeeper` was manually created** — the Docker path never creates it (macOS/Linux paths run `createdb gatekeeper`).
- ✅ `passed` — leak reproduction (psycopg2 `BEGIN` + `SELECT`, sleep, no commit) → `pg_stat_activity` showed state `idle in transaction`, exactly the quest's fingerprint.
- ❌ `failed` — lifecycle snippet `conn = psycopg2.connect(...); result = conn.execute(query)` → `AttributeError: 'psycopg2 … connection' object has no attribute 'execute'` (psycopg2 needs a cursor); mitigated by being pseudocode with no imports.
- 🧠 `reasoned` — HikariCP formula `(8*2)+1 = 17` checked by hand; macOS/Windows/Linux install paths plausible, not runnable.

## 🐞 Issues Found

Not a clean slice — **four high-severity, sandbox-reproduced defects** across the three quests, plus a repeating Docker-path pattern. Ordered by severity.

### High

1. **high · Connection Pooling · Cloud/Docker path (pgbouncer container) · `tested/failed`** — As written the container exits with code 2 (`You must set DB_HOST env`). *Fix:* use `-e DB_HOST=… -e DB_USER=… -e DB_PASSWORD=…` (not `DATABASES_*`), map `-p 6432:5432` (image listens on 5432 internally) or add `-e LISTEN_PORT=6432`, and add `-e AUTH_TYPE=scram-sha-256` to match PostgreSQL 16's default auth. This is the path the quest calls "the quickest way to run both."
2. **high · Connection Pooling · Chapter 3 `pgbouncer.ini` (lines 274–285) · `tested/failed`** — Trailing inline `;` comments on `pool_mode`, `max_client_conn`, `default_pool_size` make PgBouncer FATAL out (`cannot load config file`). *Fix:* move comments to their own lines or drop them.
3. **high · Backup and Recovery · Chapter 2 PITR recovery config (lines 252–256) · `tested/failed`** — The snippet places `restore_command`/`recovery_target_time` in `postgresql.conf` with no trigger file; PostgreSQL 12+ FATALs (`could not locate required checkpoint record`). *Fix:* add `touch $PGDATA/recovery.signal` before starting the restored cluster and note that `recovery.conf` was removed.
4. **high · Query Optimization · Cloud/Docker path (lines 183–185) · `tested/failed`** — Unlike the other three platform paths, the Docker path never runs `createdb speed_sanctum` and connects to the default `postgres` DB, so the learner is in the wrong database for the rest of the quest. *Fix:* add `docker exec speed-sanctum createdb -U postgres speed_sanctum` and connect with `psql -U postgres -d speed_sanctum`.

### Medium

5. **medium · Connection Pooling · Docker path / `gatekeeper` DB · `tested`** — `postgres:16` only creates the default DB, yet the `.ini` and the leak query both reference `gatekeeper`; the Docker path never creates it. *Fix:* add `docker exec gatekeeper-db createdb -U postgres gatekeeper`.
6. **medium · Query Optimization · Chapter 2 EXPLAIN output (lines 265–267) · `tested`** — The code comment asserts `Index Scan using idx_events_user_id`, but Postgres actually chose a `Bitmap Heap Scan`/`Bitmap Index Scan` for this row count. *Fix:* hedge as Chapter 1 does ("you may see …") and note both indicate the index is used.
7. **medium · Backup and Recovery · Chapter 1 `pg_basebackup` (line 216) · `tested`** — On an idle server it appears to hang at `waiting for checkpoint`. *Fix:* add `-c fast` or a one-line "this is normal on a quiet DB" note.
8. **medium · Backup and Recovery · Chapter 3 restore-drill (lines 292–294) · `tested`** — `date +%Y%m%d` suffix collides on a second same-day run (which the quest's own "drill regularly" advice invites). *Fix:* use `+%Y%m%d_%H%M%S` or drop/recreate first.
9. **medium · Connection Pooling · Advanced Challenge (leak) · `reasoned`** — Learners are told to "write code that borrows a connection without returning it" with no sample to adapt. *Fix:* add a minimal leaking psycopg2 snippet.
10. **medium · Query Optimization · Secondary objective "Covering Indexes" · `reasoned`** — Listed as an objective but never taught. *Fix:* add a short `INCLUDE`/index-only-scan demo, or drop the objective.

### Low

11. **low · Connection Pooling · Chapter 1 lifecycle snippet (line 207) · `tested`** — `conn.execute(query)` raises `AttributeError` on real psycopg2 (needs a cursor); harmless as pseudocode but silently misleading if copied. *Fix:* use a consistent, correct API and add imports.
12. **low · Backup and Recovery · Secondary objective "Backup Encryption" · `reasoned`** — Listed as an objective but only linked out, never demonstrated. *Fix:* add a minimal `pg_dump | gpg` example or remove the checkbox.
13. **low · Backup and Recovery · PITR · `reasoned`** — `recovery_target_action` (e.g. `promote`) unmentioned; learners may be confused that the recovered cluster is read-only.
14. **low · Query Optimization · Secondary objective "Statistics & ANALYZE" · `reasoned`** — Named objective covered only by a single inline comment.
15. **low · Connection Pooling · macOS/creds notes · `reasoned`** — `/opt/homebrew/etc/pgbouncer.ini` is Apple-Silicon-only (Intel uses `/usr/local/etc/…`); `POSTGRES_PASSWORD=quest` deserves a "local learning only" note.

## 🔗 Chain Continuity

**Window context.** This is **window 2 of 2** of the level (quests 6–8 of 8). The `required_quests` for all three — `database-fundamentals` and `sql-mastery` — live in window 1 and were **not** walked here; I reasoned about this slice assuming a learner arrives having completed them. Within the window the dependency order is correct: both *Backup and Recovery* and *Query Optimization* declare `unlocks_quests: /quests/0110/connection-pooling/`, and *Connection Pooling* is the capstone (`unlocks_quests: []`, "you have completed the Level 0110 quest line → Level 0111"). The planner placed the capstone last — right.

**State isolation is clean, but repetitive.** Each quest re-provisions its own database (`restoration_vault`, `speed_sanctum`, `gatekeeper`) and does **not** rely on the prior quest's running state, so there is no hidden cross-quest prerequisite gap inside the window. A learner can drop into any of the three cold.

**A systemic Docker-path bug spans the slice (the strongest linked-journey finding).** All three quests present the Docker/Cloud route as the "quickest" way, and in all three it is the broken or divergent one: *Query Optimization*'s Docker path never creates/selects `speed_sanctum` (#4), *Connection Pooling*'s Docker path never creates `gatekeeper` (#5) **and** its pgbouncer container won't start (#1). The macOS/Linux paths each run the matching `createdb`; only the Docker path drops it. A beginner who commits to Docker for the level — a very common choice — is consistently punished, quest after quest. This is one fix pattern (make each Docker path mirror its `createdb`/DB-selection to the other platforms) that would lift the whole slice.

**Cross-quest Docker port collision (`reasoned`, not tested — engine isolated each quest).** All three Docker paths map `-p 5432:5432` with distinct container names (`restoration`, `speed-sanctum`, `gatekeeper-db`). A learner who walks the window in one sitting without tearing down the previous container will hit `port is already allocated` on the next quest's `docker run`. Worth a one-line "stop the previous container first" note.

**Thematic continuity is a genuine strength.** *Query Optimization* closes with "fewer, faster queries need fewer connections" and *Connection Pooling* opens by measuring the round-trip cost the prior quest introduced — the two dovetail well, and *Backup and Recovery* → *Connection Pooling* ("keep a recovered database serving traffic efficiently") is coherent. The problem is never the narrative; it is that the capstone's hands-on artifacts fail, so a learner who followed the story faithfully cannot actually stand up the pooler the level is meant to end on.

## 🧠 Reasoning & Method

- **Mode:** `execute`. I consumed the workflow-sealed `walk-evidence.json` /
`walk-evidence.md` (the engine's child `claude` processes can't authenticate from my Bash tool, so per the skill I did **not** re-run the engine). I re-read all three quest sources in plan order to produce the chain-continuity analysis.
- **What was tested vs reasoned:** Every `passed`/`failed` above is a command the
engine ran in a live PostgreSQL 16 sandbox — including the four high-severity failures, which were each reproduced (FATAL logs / container exit codes quoted verbatim). Items marked `reasoned` are OS-specific install paths (sudo denied, no macOS/Windows in a Linux sandbox), illustrative pseudocode, or arithmetic (HikariCP formula) — I did not manufacture output for any of them.
- **Coverage / limits:**
  - Snippets actually run: Backup **6/7** runnable, Query Optimization **5/9**
    (3 install paths skipped as OS-specific), Connection Pooling **8/6** (the 8
    includes the engine's corrected re-runs proving each fix).
  - The macOS, Windows, and Linux-sudo install blocks in every quest are
    **`reasoned` only** — not executable in this sandbox — so platform-specific
    breakage on those paths could exist beyond what I observed.
  - `database-fundamentals` and `sql-mastery` (this window's declared
    prerequisites) were **outside the walked window** and not verified here.
  - The cross-quest Docker port collision is a **reasoned** chain observation; the
    engine scores each quest in isolation and did not run the three containers
    concurrently.
- **Confidence:** High on the four high-severity defects (sandbox-reproduced with
quoted failure output) and on the Docker-path pattern. Medium on the reasoned cross-quest and install-path observations. The **fail** session verdict is driven by the capstone quest failing (45%) with two broken safety-critical artifacts on the level's terminating quest, compounded by the systemic Docker-path defect.
- **Cost:** ~$2.53 across the three-quest execute run.

*One slice, one report. No quest content was edited; fixes above are for a follow-up content pass (content-curator / a human), not this session.*
