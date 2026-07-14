---
title: 'Quest Walkthrough — Security Specialist · Level 1110 (Architecture & Design Patterns)'
date: '2026-07-14T00:00:00.000Z'
character: security-specialist
level: '1110'
theme: Architecture & Design Patterns
tier: Master
quest_count: 5
mode: execute
overall_verdict: warn
session:
  window: 2 of 2 (offset 5, size 5)
  total_quests_in_level: 10
  average_score: 73.2
  counts: { pass: 3, warn: 1, fail: 1 }
  engine_cost_usd: 3.8083
  evidence: walk-evidence.json (sealed, agentic execute engine — consumed as-is)
---

## 🎯 Session Summary

Walked the **second window (5 of 10 quests)** of the Security Specialist's Master
tier — Level `1110`, *Architecture & Design Patterns* — end-to-end as a learner,
consuming the workflow-sealed execute-engine evidence and reading every quest source
in dependency order. Four of the five quests belong to one coherent chain
(**System Design Mastery / The Architect's Citadel**): API Gateway → Event-Driven
Design → Scaling Strategies → System Design Interviews. The fifth
(*Weaving the Whole*) is the finale of a **different** campaign (The Ouroboros Loop)
that merely shares the level code.

**Headline verdict: ⚠️ warn.** The slice's conceptual writing is consistently strong
and three quests pass cleanly (avg 73.2%), but the two *most hands-on* quests are
where a beginner gets stuck: **API Gateway Patterns fails (44%)** because its flagship
NGINX + FastAPI lab is broken as written — the container crash-loops on unprovisioned
upstreams and the edge-auth snippet returns **500 instead of the promised 401** — and
**Event-Driven Design warns (61%)** because the marquee producer/consumer lab **hangs
forever** in the natural order a learner runs it. Both failures were confirmed by
commands actually run in the sandbox, and both land squarely on the material a
*Security Specialist* cares most about (edge authentication, message integrity).

## 🗺️ The Journey

Plan order (dependency-sorted within the level; `walk-plan.json` window index 1 of 2):

1. ❌ **API Gateway Patterns: The Single Front Door** — 44% · The concepts are solid,
   but the Chapter 2 lab (NGINX config + FastAPI auth) cannot be completed as written;
   the invalid-token path returns 500, not 401.
2. ⚠️ **Event-Driven Design: Pub/Sub, Event Sourcing, and CQRS** — 61% · Real Redpanda
   broker starts and most snippets run, but the core produce→consume exercise hangs
   silently, and a tracked objective ("Ordering and Partitioning") has no content.
3. ✅ **Scaling Strategies: Horizontal Growth, Caching, and CAP** — 83% · Every runnable
   snippet executed and matched its claim; only the cache-aside example needs stub DB
   helpers and a redis-py deprecation fix.
4. ✅ **Weaving the Whole: The Serpent Closes the Circle** — 83% · Merge-warden and
   smuggle-guard logic stress-tested against a mocked `gh` and behaved exactly as
   documented; a capstone from a *different* campaign (chain outlier — see §6).
5. ✅ **System Design Interviews: A Framework for the Whiteboard** — 95% · Best in slice;
   estimation math, code generators, and both mermaid diagrams all executed and
   matched the prose exactly.

## 🔬 Evidence

All outcomes below come from the sealed `walk-evidence.json` (mode: **execute**,
non-mock) — commands actually run in the disposable runner sandbox. Snippet coverage
is reported as `ran / available-runnable`.

### 1. API Gateway Patterns — ❌ 44% (ran 5/6 runnable; 2 passed, 3 failed, 3 reasoned)
Per-dimension: commands_work **1**, content_accuracy 2, completeness 2, clarity 3,
structure 3, safety 5.
- **`docker run … -v nginx.conf … nginx:alpine` → FAILED.** Container crash-loops:
  `nginx: [emerg] host not found in upstream "users:8000"`. Confirmed via `docker logs`
  + `docker ps -a` (`Exited (1)`). The quest never provisions the `users`/`orders`
  upstreams the config references; the engine had to hand-create a network and stub
  containers to get NGINX to even start — none of that scaffolding is in the quest.
- **FastAPI edge-auth middleware → FAILED.** A live uvicorn instance of the exact
  Chapter 2 snippet, sent a tokenless request, returned **HTTP 500** with an unhandled
  `HTTPException` traceback — **not** the `401 invalid token` the prose and the
  Intermediate Challenge validation require. (Real Starlette `BaseHTTPMiddleware`
  gotcha: `raise HTTPException` inside `@app.middleware("http")` doesn't convert to a
  response.)
- **`nginx -t` on the config alone → FAILED** (same missing-upstream cause; directive
  syntax itself is valid).
- **Cloud path `docker run -d -p 8080:80 nginx:alpine` → PASSED** (serves default page;
  makes no routing claim). **Aggregation `asyncio.gather`+`httpx` snippet → PASSED**
  syntactically (fails only on DNS for nonexistent hosts, expected for a fragment).
- Both mermaid diagrams: `reasoned` (mermaid-cli blocked by sandbox Chromium sandbox
  restriction; static inspection = valid).

### 2. Event-Driven Design — ⚠️ 61% (ran 6/9 runnable; 5 passed, 1 failed, 2 reasoned)
Per-dimension: commands_work 2, content_accuracy 4, completeness 2, clarity 3,
structure 4, safety 5.
- **Redpanda broker `docker run … redpandadata/redpanda` → PASSED.** Image pulled and
  started; `docker logs` showed *"Successfully started Redpanda!"* and the Kafka API
  listening on 9092.
- **KafkaProducer `.send(...)` → PASSED** against the live broker (kafka-python 3.0.8).
- **KafkaConsumer loop → FAILED (hang).** Run exactly as written (no
  `auto_offset_reset`, no `consumer_timeout_ms`) immediately after the producer — the
  natural learner order — produced **zero output and an infinite hang** (killed
  externally). kafka-python defaults to `latest`, so a fresh group never sees the
  already-published message.
- Event-sourcing `apply()` fold → PASSED, printed `70` (matches the inline comment).
  Idempotency guard → PASSED (double-delivery of `evt-1` left `processed_ids` at one
  entry). CQRS mermaid → `reasoned` (valid syntax).

### 3. Scaling Strategies — ✅ 83% (ran 5/6 runnable; 5 passed, 0 failed, 2 reasoned)
Per-dimension: commands_work 4, content_accuracy 4, completeness 4, clarity 4,
structure 5, safety 5.
- **Redis `docker run … redis:7-alpine` → PASSED** (both Linux and Cloud paths).
- **Kubernetes Deployment+Service YAML → PASSED** (two valid docs via PyYAML;
  `kubectl --dry-run=client` limited by no API server, noted).
- **Cache-aside Python → PASSED** against live Redis, *after the engine supplied the
  missing `db_fetch_product`/`db_update_product` stubs* — produced the described
  MISS→DB then HIT-no-DB sequence.
- **Shard router `shard_for(1024)` → PASSED**, printed `db-shard-0` (1024 % 4 == 0),
  exactly as the inline comment states. CAP/PACELC text block → `reasoned` (accurate).

### 4. Weaving the Whole — ✅ 83% (ran 2/1 recorded; 2 passed, 0 failed, 2 reasoned)
Per-dimension: commands_work 4, content_accuracy 4, completeness 4, clarity 4,
structure 5, safety 5.
- **Merge-warden `auto-merge.yml` → PASSED.** Parsed cleanly; the wait-loop's four
  branches (fail-blocks / pending-waits / self-only-waits / all-green-merges) were
  extracted and exercised against a mocked `gh` and behaved exactly as documented.
- **Smuggle-guard step → PASSED.** A content-only diff (`potions/…`) passes silently;
  a diff also touching `scripts/check.sh` is correctly caught and labeled `needs-human`.
- **Chapter 3 end-to-end (`gh variable set …`, `gh workflow run first-turn.yml`) →
  SKIPPED.** Requires an authenticated `gh` session against a live pre-built repo; the
  sandbox has no GitHub auth. Reasonable for a series finale but limits verification.

### 5. System Design Interviews — ✅ 95% (ran 5/6 runnable; 5 passed, 0 failed, 2 reasoned)
Per-dimension: commands_work 5, content_accuracy 5, completeness 4, clarity 5,
structure 5, safety 4.
- **Estimation `estimate.py` → PASSED**, output *"Writes: ~40/s | Reads: ~4000/s"* and
  *"Storage: ~50 GB/month, ~3 TB / 5yr"* — exactly the quest's stated figures.
- **Short-code generators `codegen.py` → PASSED**: `code_by_hash(...)` → valid 7-char
  base62; `code_by_counter(0)`→`a`, `(12345)`→`dnh`, `(62**7-1)`→`9999999`.
- **Both mermaid diagrams → PASSED** (rendered to SVG via mermaid-cli with
  `--no-sandbox`). Cheat-sheet figures (`86,400 s/day`, `~2.5M s/month`, latency
  numbers) verified accurate. Platform install lines `skipped` (no brew/winget/sudo).

## 🐞 Issues Found

Grouped by severity; each cites the observed evidence. These are for a **content pass**
to act on — this session makes no edits.

**HIGH**
- **API Gateway · Ch.2 lab setup** — the documented `docker run … nginx.conf` **crash-
  loops** (`host not found in upstream "users:8000"`), and the Novice Challenge
  validation `curl localhost:8080/users/` is therefore unachievable. *Observed:* engine
  ran the exact command; container `Exited (1)`. *Fix:* ship a `docker-compose.yml` (or
  equivalent) that also starts trivial `users`/`orders` stubs on port 8000 on a shared
  network.
- **API Gateway · Ch.2 auth code** — invalid tokens produce **HTTP 500, not the claimed
  401**, contradicting both the prose and the Intermediate Challenge's explicit
  criterion. *Observed:* live uvicorn request returned 500 + unhandled `HTTPException`
  traceback. *Fix:* catch the exception and `return JSONResponse(..., status_code=401)`,
  or switch to a FastAPI `Depends()`-based auth dependency.
- **Event-Driven · Ch.1 consumer** — the flagship produce→consume lab **hangs forever
  with zero output** when run producer-then-consumer. *Observed:* consumer loop killed
  after an infinite hang. *Fix:* add `auto_offset_reset='earliest'` (and/or instruct
  starting the consumer first) plus a `consumer_timeout_ms` / "runs forever, Ctrl+C"
  note.
- **Event-Driven · secondary objective "Ordering and Partitioning"** — a *tracked
  learning objective* with **no supporting content anywhere** in the body. *Observed:*
  full read of source; skill listed (line 110, "Reasoning about ordering") but no
  partition-key/ordering section exists. *Fix:* add a short section, or drop the
  objective.

**MEDIUM**
- **API Gateway · identity forwarding** — prose + challenge require forwarding
  `X-User-Id` downstream, but no snippet does it; the `SERVICES` dict is defined and
  unused. *Fix:* add the httpx-forward-with-header call.
- **API Gateway · Mastery Challenges** — validation steps (`curl`, 401 rejection,
  X-User-Id) are unverifiable with the materials given; align them with what the quest
  actually provides or add the scaffolding.
- **Event-Driven · Intermediate Challenge (snapshots)** — challenge validates
  "snapshot + tail replay" but the body never demonstrates a snapshot object. *Fix:*
  add a short example.
- **Event-Driven · Novice Challenge (replay)** — the in-body idempotency snippet only
  guards in-process duplicates, not a real broker redelivery the challenge implies.
  *Fix:* show `rpk group seek --to start` / `consumer.seek()`.
- **Scaling · Ch.2 cache-aside** — snippet calls undefined `db_fetch_product` /
  `db_update_product` (a copy-paste `NameError`). *Observed:* engine had to add stubs
  to run it. *Fix:* define minimal stubs or comment that they stand in for the reader's
  DB layer.
- **Scaling · Mastery Challenges** — conceptual sections ship full code, but the "lab"
  challenges (3 replicas + LB, cache timing) have no starter code. *Fix:* add minimal
  scaffolding / a compose file.
- **Weaving the Whole · Ch.2 self-exclusion filter** — an undisclosed fragility: the
  merge warden assumes a check `link` always contains `/<RUN_ID>/`. *Fix:* anchor to
  `/actions/runs/${RUN_ID}(/|$)` or resolve via `gh api`, and probe it in a Knowledge
  Check.
- **System Design · "Two Worked Designs" / news-feed** — the objective promises a
  worked news-feed and the Intermediate Challenge validates "within 10x of a worked
  reference," but no news-feed reference numbers exist. *Fix:* add a short news-feed
  estimation or soften the wording.

**LOW**
- **Scaling · cache-aside** — `cache.setex(key, TTL, …)` raises a redis-py
  DeprecationWarning; prefer `cache.set(key, value, ex=TTL)`.
- **Scaling · CAP examples** — classifying DynamoDB as purely "AP" omits its optional
  strongly-consistent reads; add a caveat.
- **Event-Driven · deserializer** — kafka-python 3.x emits a DeprecationWarning for
  callable `value_(de)serializer`; note the current class-based interface.
- **Weaving the Whole · `first-turn.yml`** — Chapter 3 references it without defining
  it; add a sentence or link to the defining chapter.
- **System Design · Linux path** — `sudo apt install` assumes admin rights; offer a
  non-sudo alternative.
- **API Gateway / others · mermaid** — diagrams validated only by static inspection
  where headless-Chromium sandboxing was restricted (not a defect, a coverage note).

## 🔗 Chain Continuity

**The core four are a genuinely coherent learning path.** Read as one journey, the
System Design Mastery chain flows correctly by dependency:
`microservices-architecture` (prereq, **not in this window**) → **API Gateway** and
**Event-Driven** (both `require` microservices, both `unlock` scaling) → **Scaling
Strategies** (`unlocks` system-design) → **System Design Interviews** (`unlocks`
1111/technical-leadership). Concepts reinforce cleanly: cache-aside introduced in
Scaling Ch.2 reappears in the System Design URL-shortener; CAP/AP from Scaling Ch.3 is
exactly the trade-off the interview quest asks a candidate to articulate; the gateway
and event patterns are the "boxes and arrows" the capstone whiteboards. A learner who
finished Scaling is genuinely ready for System Design Interviews.

**Two continuity caveats a real learner would hit:**

1. **Windowing gap (not a content bug).** This is window **2 of 2** (offset 5). The
   `required_quests` foundation for all four Citadel quests — `microservices-
   architecture` — lives in the *other* window (offset 0), as does the recommended
   `domain-driven-design`. A learner dropped into this window alone lacks the assumed
   microservices grounding. The perfection-loop ledger accumulates coverage across
   both windows, so this is expected; flagging it for honesty, not as a defect.

2. **`Weaving the Whole` is a chain outlier.** It sits at `1110` only because it is
   thematically "Architecture & Design Patterns," but it belongs to a *different*
   campaign — `quest_series: The Autonomous Realm`, `quest_line: The Ouroboros Loop` —
   with `recommended_quests: /quests/1101/ouroboros-loop-06-…` and prose that assumes
   "Chapters I–VI complete and green." It does **not** connect to the System Design
   Mastery chain and is not a Security Specialist skill line. Within this slice it reads
   as a standalone finale for a learner who came via the Ouroboros track, not the
   Citadel track. Fine as-is, but a maintainer should know these two chains are
   interleaved at this level.

**Character-fit note (Security Specialist).** The most security-relevant material in
the slice — **edge authentication at the API gateway** — is precisely the part that is
broken (401→500) and unverifiable. For this character class specifically, fixing the
API Gateway auth lab should be the highest-value repair: it is both the biggest defect
and the most on-brand content for a security learner.

## 🧠 Reasoning & Method

- **Mode:** `execute` (non-mock), on the workflow-sealed `walk-evidence.json` — I did
  **not** run the engine (its child `claude` processes can't authenticate from the
  agent's Bash tool); I consumed the sealed evidence and `walk-evidence.md` verbatim
  and did not modify `walk-plan.json` or `walk-evidence.*`.
- **What I ran vs. reasoned:** All `passed`/`failed` outcomes above are commands the
  execute engine actually ran in the disposable sandbox (real Docker containers for
  NGINX, Redpanda, Redis; live uvicorn; live Python execution; mocked `gh`). I
  independently **read all five quest sources in plan order** and reasoned about the
  linked journey, prerequisite satisfaction, and character fit (§6) — that reasoning is
  labeled as reasoning, not as tested outcomes.
- **Coverage / limits, stated plainly:** This is **5 of 10** quests in the level (one
  rotating window) — I did **not** walk the other window (microservices-architecture,
  domain-driven-design, and the earlier chain members). Mermaid diagrams in several
  quests were `reasoned` only where the sandbox blocked headless Chromium. Several
  platform install lines (brew/winget/sudo apt) were `skipped` as non-applicable on the
  Linux sandbox — standard and plausible, but unexecuted. Chapter 3 of *Weaving the
  Whole* is legitimately unrunnable without a live authenticated GitHub repo and was
  skipped. No destructive commands were run; no network access beyond the images/broker
  the quests explicitly require.
- **Confidence:** **High** on the two blocking defects (API Gateway crash-loop + 401→500,
  and the Event-Driven consumer hang) — each was directly reproduced by an executed
  command with quoted output. **Medium-high** on the medium/low content-gap issues,
  which combine executed evidence with a source read. The three passing verdicts are
  well-supported by real snippet execution.

---

### Appendix — machine evidence (verbatim excerpt from `walk-evidence.md`)

> **5** quests evaluated · ✅ 3 pass · ⚠️ 1 warn · ❌ 1 fail · avg **73.2%** · ~$3.8083
>
> | | Score | Quest | Snippets run |
> |---|--:|---|:-:|
> | ❌ | 44 | API Gateway Patterns: The Single Front Door | 5/6 (3✗) |
> | ⚠️ | 61 | Event-Driven Design: Pub/Sub, Event Sourcing, and CQRS | 6/9 (1✗) |
> | ✅ | 83 | Scaling Strategies: Horizontal Growth, Caching, and CAP | 5/6 |
> | ✅ | 83 | Weaving the Whole: The Serpent Closes the Circle | 2/1 |
> | ✅ | 95 | System Design Interviews: A Framework for the Whiteboard | 5/6 |
