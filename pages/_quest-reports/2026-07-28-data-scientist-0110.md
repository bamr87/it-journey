---
title: Data Scientist · L0110 · 2026-07-28
description: Quest-perfection walkthrough of the Database Mastery slice data-scientist/0110 on 2026-07-28,
  engine verdict warn. An evidence-based, learner's-eye…
date: '2026-07-28T00:00:00.000Z'
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
  from 2026-07-28.'
slice: data-scientist/0110
character: data-scientist
level: '0110'
theme: Database Mastery
tier: Adventurer
verdict: warn
quest_count: 3
walk_date: '2026-07-28'
run_url: https://github.com/bamr87/it-journey/actions/runs/30355858267
source_report: test/quest-validator/walkthroughs/2026-07-28-data-scientist-0110.md
---

> **Slice** `data-scientist/0110` · **Level** 0110 (Database Mastery) · **Adventurer tier** · **Engine verdict** ⚠️ warn · **Walked** 2026-07-28
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/30355858267) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-28-data-scientist-0110.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-28-data-scientist-0110.md)

---

## 🎯 Session Summary

I walked the **Data Scientist** path through **Level 0110 — Database Mastery (⚔️ Adventurer tier)**, playing the three quests in the planned window (the *tail* of an 8-quest level: window 2 of 2, offset 5): **Backup and Recovery → Query Optimization → Connection Pooling**. Evidence is from the sealed execute-mode engine (`walk-evidence.json`), which stood up real PostgreSQL 16 in Docker and actually ran each quest's safe snippets in a disposable sandbox.

**Headline verdict: ⚠️ warn.** The conceptual/technical writing across all three quests is strong and accurate, and Query Optimization's SQL runs cleanly end-to-end. But the slice ships **two genuinely broken copy-paste snippets** in Connection Pooling (both confirmed by execution), a **plan-type mismatch** in Query Optimization that could make a learner think they failed, and a third quest — **Backup and Recovery — that the engine could not score at all** (it exhausted its 40-turn budget wrestling with the physical-backup / PITR setup and returned `fail`/overall 0.0 by timeout, *not* by a content defect). Maintainer-actionable: fix the two Connection Pooling snippets first — they sit on the quest's own "quickest path."

Machine tally (`walk-evidence.md`): **2 scored · ✅ 1 pass · ⚠️ 1 warn · ❌ 1 fail (engine timeout) · avg 72.5% · ~$2.09**.

## 🗺️ The Journey

Plan order (from `walk-plan.json`), which also respects the dependency chain (Connection Pooling both *recommends* Query Optimization and is *unlocked by* the other two, so it correctly comes last):

1. ❌ **Backup and Recovery: Data Protection for Databases** — *no score (engine hit max-turns / 0.0)* · The logical-backup lesson is clean and runnable, but the engine never returned a verdict — it burned all 40 turns trying to stand up physical backup + PITR (which need `sudo`/server config the sandbox lacks). Treat as **inconclusive**, not failed content.
2. ✅ **Query Optimization: Tuning Fast Database Queries** — *80 / pass* · Core SQL reproduced exactly (Seq Scan → index speedup, composite leftmost-prefix, `LOWER()` sargability trap); gaps are a mismatched post-index plan node, a Docker path that skips `createdb`, and an N+1 example against a never-seeded `users` table.
3. ⚠️ **Connection Pooling: Efficient Database Resource Management** — *65 / warn* · Excellent concepts (connection cost, sizing math, pooling modes, leak diagnosis), but the recommended Docker PgBouncer command and the sample `pgbouncer.ini` both fail when actually run — real copy-paste stoppers.

## 🔬 Evidence

All `passed`/`failed` below are commands the execute engine actually ran in the sandbox. Items I judged only from the quest source (no run) are labeled `reasoned`.

### 1. Backup and Recovery — `pages/_quests/0110/backup-recovery.md` — ❌ no verdict (engine timeout)

- **Snippet coverage: none recorded.** The engine terminated with `terminal_reason: max_turns` — `["Reached maximum number of turns (40)"]` — so `verdict_obj` is empty and `overall` defaults to `0.0`. The trailing tool calls in the sealed error show it stuck on physical-backup setup:
  - `sudo -u postgres pg_ctlcluster 16 main start` and `sudo -u postgres createdb test_sudo_check` — sandbox has no working `sudo`, so cluster bring-up for a *second* server (port 5433) to demo `pg_basebackup`/PITR never succeeded.
  - `pg_basebackup -D .../backups/base2 -Ft -z -P` — attempted repeatedly.
- **Interpretation (`reasoned`):** This is an **engine-coverage failure, not a demonstrated content bug.** The logical-backup path — `pg_dump -Fc restoration_vault > vault_backup.dump` → `createdb restored_vault` → `pg_restore` (lines 201–209) and the restore-drill in Chapter 3 (lines 290–296) — is self-contained and standard, and is the quest's actual primary objective. The physical-backup and PITR sections (lines 213–258) are where a real learner *and* the engine get stuck (see Issues). No content defect was witnessed; I cannot report a score.

### 2. Query Optimization — `pages/_quests/0110/query-optimization.md` — ✅ 80 (pass)

Dimensions: commands_work 4 · content_accuracy 4 · completeness 3 · clarity 4 · structure 5 · safety 5. **Snippets: ran 5/9 runnable · 5 passed · 0 failed · 3 skipped · 2 reasoned.** `weight_covered: 1.0`.

- `passed` — Docker setup `docker run --name speed-sanctum ... postgres:16` produced a working PG16 instance.
- `passed` — Seed script created **exactly 100,000 rows** with all four `action` values present.
- `passed` — Ch.1 `EXPLAIN ANALYZE ... WHERE user_id = 42` → `Seq Scan` with large `Rows Removed by Filter` (actual 5.4ms vs. the doc's illustrative 49.1ms — shape matches).
- `passed` — Ch.2 composite index `(user_id, action)`: used for `user_id=42 AND action='login'`, **not** used for `action='login'` alone → leftmost-prefix rule confirmed precisely.
- `passed` (prose-claim check) — `LOWER(email)` sargability: plain index ignored under `WHERE LOWER(email)=...` (Seq Scan), expression index fixes it. Claim accurate.
- **Mismatch witnessed** — after `CREATE INDEX idx_events_user_id`, PG16 chose **`Bitmap Heap Scan` + `Bitmap Index Scan`**, not the doc's shown `Index Scan using idx_events_user_id` (lines 265–267). Speedup itself real and dramatic (5.4ms → 0.08ms).
- `reasoned` — Ch.3 N+1 Python is explicit pseudocode (`db.query(...)`) and references a `users` table the seed script never creates; the engine created its own `users` and confirmed the JOIN plans fine.
- `skipped` — macOS/Windows/native-Linux setup blocks (wrong OS / no sudo); syntactically standard, not line-verified.

### 3. Connection Pooling — `pages/_quests/0110/connection-pooling.md` — ⚠️ 65 (warn)

Dimensions: commands_work **2** · content_accuracy 3 · completeness 4 · clarity 4 · structure 4 · safety 5. **Snippets: ran 4/6 runnable · 2 passed · 2 failed · 2 skipped · 3 reasoned.** `weight_covered: 1.0`.

- **`failed`** — Docker PgBouncer command (lines 184–186) run verbatim: container **exited immediately (exit 2)** with `DB_HOST: Setup pgbouncer config error! You must set DB_HOST env`. The `edoburu/pgbouncer` image wants `DB_HOST`/`DB_USER`/`DB_PASSWORD`, not `DATABASES_*` (verified against the image's `/entrypoint.sh`). Even corrected, the default `listen_port` is 5432, so `-p 6432:6432` maps to nothing unless `-e LISTEN_PORT=6432` is added — engine confirmed both the failure and that the fix works.
- **`failed`** — Ch.3 `pgbouncer.ini` (lines 274–285) run against real PgBouncer 1.25.2: `FATAL cannot load config file` / `ERROR invalid value "transaction          ; return the connection after each transaction" for parameter pool_mode`. PgBouncer only treats `;`/`#` as comments at line-start; the trailing inline comments break it. Removing them makes the file load and pool successfully.
- `passed` — `SELECT pid, state, query, state_change FROM pg_stat_activity WHERE datname='gatekeeper' ORDER BY state_change;` ran against live PG16 and returned expected columns.
- `reasoned` — Ch.1 Python: `psycopg2.connect(...)` connections have **no `.execute()`** method (engine confirmed `AttributeError` with psycopg2-binary); that pattern is psycopg3's, which the snippet never names.
- `skipped` — brew/winget/native-apt setup blocks (no Homebrew/Windows, no sudo); `apt-cache policy` confirmed the package names exist on Ubuntu 24.04.

## 🐞 Issues Found

Every item below cites a witnessed run or an exact quoted line. Backup-and-Recovery items are `reasoned` (no engine score was produced).

- **HIGH · Connection Pooling · Cloud Realms Docker path (lines 184–186) · witnessed** — The `edoburu/pgbouncer` container exits with `You must set DB_HOST env` because the quest uses `DATABASES_HOST/USER/PASSWORD`; and even fixed it never listens on 6432. This is the path the quest calls "the quickest way to run both," so the recommended shortcut is the broken one. **Fix:** use `DB_HOST/DB_USER/DB_PASSWORD` (+ `DB_NAME`) and add `-e LISTEN_PORT=6432`.
- **HIGH · Connection Pooling · Ch.3 `pgbouncer.ini` (lines 282–284) · witnessed** — Trailing inline `;` comments after `pool_mode`, `max_client_conn`, `default_pool_size` make PgBouncer abort with a `FATAL`/`invalid value` error. **Fix:** drop the inline comments or move each to its own line above the setting.
- **MEDIUM · Connection Pooling · Ch.1 Python (lines 206–209) · witnessed (reasoned run)** — `conn = psycopg2.connect(...)` then `conn.execute(query)` raises `AttributeError` (psycopg2 has no connection-level `execute`). **Fix:** use `with conn.cursor() as cur: cur.execute(...)`, or switch both blocks to psycopg3 (`import psycopg`, `from psycopg_pool import ConnectionPool`) and add the missing imports.
- **MEDIUM · Query Optimization · Ch.2 (lines 265–267) + Novice Challenge (line 330) · witnessed** — Doc shows `Index Scan using idx_events_user_id`, but stock PG16 picks `Bitmap Heap Scan`/`Bitmap Index Scan`; the Novice validation "The plan changes from `Seq Scan` to `Index Scan`" reads as a literal string match a correct learner will fail. **Fix:** note that a bitmap index plan also counts as success (both are index-based, not sequential).
- **MEDIUM · Query Optimization · Cloud Realms path (lines 183–185) · reasoned** — The Docker path omits `createdb speed_sanctum` that the macOS/Windows/Linux paths all include, so `psql -U postgres` lands in the default `postgres` DB while the shared "Seed a Large Table" section assumes you're in `speed_sanctum`. **Fix:** add `createdb speed_sanctum` (or a `CREATE DATABASE`) to the Docker block.
- **MEDIUM · Query Optimization · Ch.3 N+1 example (lines 296–311) · reasoned** — The "fixed" JOIN queries a `users` table the quest's own seed script never creates, so a learner cannot run it against `speed_sanctum` as given. **Fix:** either label it illustrative-only or add a small `CREATE TABLE users (...)` + seed snippet.
- **MEDIUM · Backup and Recovery · Ch.1–2 physical backup / PITR (lines 216, 247, 254) · reasoned** — `pg_basebackup -D /backups/base` and `archive_command = 'cp %p /backups/wal_archive/%f'` reference `/backups/...` directories the quest never has the learner create, and physical backup + WAL archiving need server-config edits, a restart, and replication privileges that none of the four "Medium" platform setup blocks provide. This gap is almost certainly what stalled the engine into a max-turns timeout. **Fix:** add the `mkdir -p` steps and a short note that the physical-backup/PITR sections require superuser/server-config access beyond the logical-backup path (or scope them as read-only/optional for a Medium quest).
- **LOW · Query Optimization · Objectives (lines 104, 105) · reasoned** — "Covering Indexes" and "Statistics & ANALYZE" are named secondary objectives but never demonstrated (no `INCLUDE`/index-only-scan example; only a one-line `ANALYZE`). **Fix:** add short examples or trim the objective list.
- **LOW · Connection Pooling · Objectives + Advanced Challenge (lines 104, 333–339) · reasoned** — "Application Pools" (HikariCP/SQLAlchemy) is a listed bonus but never shown with code, and the Catch-a-Leak challenge gives no starter leak snippet. **Fix:** add a short SQLAlchemy/HikariCP config and a minimal "forgets to commit" leak example.

**No blocking issues in Query Optimization** — its verdict is a clean pass; the items above are refinements. Backup and Recovery has **no blocking content issue witnessed** — its `fail` is an engine-coverage artifact, called out honestly in §7.

## 🔗 Chain Continuity

- **This is the tail window of the level.** `walk-plan.json` gave me window 2 of 2 (offset 5) of an 8-quest level. The prerequisites these quests assume — `sql-mastery` (Query Optimization) and `database-fundamentals` (Backup, Pooling) — live in the *earlier* window I did not walk, so I can't verify those hand-offs first-hand; within this window the assumed knowledge (reading SQL, running psql, basic JOINs) is reasonable for an Adventurer-tier learner who reached quest 6.
- **Ordering is sound.** Connection Pooling both *recommends* Query Optimization and is *unlocked by* Backup/Query, so placing it last is correct. Query Optimization's N+1 / round-trip discussion (Ch.3) sets up Connection Pooling's whole premise ("reduce the round-trip overhead you just measured", line 363) — a genuinely nice thematic hand-off. Backup and Recovery sits somewhat independently (it protects data rather than building on query skills), which is fine.
- **Shared PostgreSQL-16-in-Docker spine works.** All three use the same `docker run ... postgres:16` pattern, so a learner who set it up once carries it forward — good continuity. The friction is that each quest's *pooler/second-server* extras (PgBouncer container, `/backups` dirs, a second cluster) are where the copy-paste path breaks, and those breaks cluster in exactly the two "quickest path" Docker blocks a beginner would reach for first.
- **Beginner sticking points, in order of likely pain:** (1) Connection Pooling's Docker PgBouncer command dies instantly — a real stall on the recommended path; (2) Backup's physical-backup/PITR needs privileges the setup never granted — a learner following the Medium platform block cannot complete Chapter 2 as written; (3) Query Optimization's post-index plan text won't literally match, risking a false "I did it wrong." None of these break the *conceptual* journey, but two would stop hands-on progress.

## 🧠 Reasoning & Method

- **What I ran vs. reasoned:** I did **not** run the engine — `walk-evidence.json`/`walk-evidence.md` were pre-sealed by the workflow (execute mode, real PostgreSQL 16 in a disposable Docker sandbox) and I consumed them verbatim, as the skill requires. Every `passed`/`failed` above is a command the engine actually executed; I read all three quest sources in plan order and added the linked-journey reasoning (§ Chain Continuity) and the `reasoned` labels myself.
- **Mode:** `execute`. Two quests returned full schema-constrained verdicts (Query Optimization 80/pass, Connection Pooling 65/warn, both `weight_covered: 1.0`). Backup and Recovery returned **no verdict** — `terminal_reason: max_turns`, so its `fail`/0.0 is a coverage timeout, not a graded outcome. I have deliberately **not** invented a score for it.
- **Coverage capped/limited:** OS-specific setup blocks (brew/winget/native apt+systemctl+sudo) were `skipped` on all quests — the Linux sandbox has no Homebrew/Windows and no working `sudo`; those are `reasoned` as syntactically standard but unverified. Snippet coverage was 5/9 (Query Optimization) and 4/6 (Connection Pooling) runnable snippets; Backup and Recovery has no recorded snippet run.
- **Confidence:** High on the two Connection Pooling HIGH issues and the Query Optimization plan-mismatch (directly executed and reproduced). Medium on the reasoned items (N+1 `users` table, Docker `createdb` omission, missing objectives). For Backup and Recovery I am confident only that the engine timed out on physical-backup setup; I am **not** claiming its content passes or fails — it is inconclusive and needs a re-run (or a scope note in the quest) to score.
- **Scope discipline:** One slice, one report. No quest content was edited; no git action taken. Fixable bugs are in § Issues for a content pass to act on.
