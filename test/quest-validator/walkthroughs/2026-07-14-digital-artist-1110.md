---
title: "Walkthrough — Digital Artist · Level 1110 (Architecture & Design Patterns)"
date: 2026-07-14T00:00:00.000Z
character: digital-artist
level: "1110"
theme: Architecture & Design Patterns
tier: Master
quest_count: 5
mode: execute
overall_verdict: warn
session:
  window: "1 of 2 (offset 5, size 5)"
  total_quests_in_level: 10
  engine_average: 85.5
  engine_counts: { pass: 2, warn: 2, fail: 1 }
  engine_cost_usd: 2.5573
  evidence: walk-evidence.json
---

## 🎯 Session Summary

Walked the second window (quests 6–10) of the **Digital Artist → Level 1110 "Architecture & Design Patterns" (Master ⚡)** slice — five `main_quest` pages, three 🔴 Hard and two ⚔️ Epic — as a learner, driven by the sealed execute-engine evidence in `walk-evidence.json` (I did **not** re-run the engine). Headline: **warn**. Four of the five quests are technically strong — the two Epic capstones scored **94** and **97** with every runnable snippet passing against real tooling, and the two Hard middle quests (**74**, **77**) run their actual teaching code correctly against live Redis/Redpanda containers. The blocking result is **quest 1, "API Gateway Patterns"**: its Chapter 2 lab is unrunnable as written, and the engine burned its full 40-turn budget trying to make the gateway serve a request before erroring out with no score.

A maintainer's two actionable takeaways: (1) the API Gateway lab needs the two upstream services (`users`, `orders`) it silently assumes — a beginner cannot get NGINX to start, let alone `curl localhost:8080/users/`; and (2) a recurring pattern across the whole slice is **secondary objectives promised but never taught in the body** (Ordering/Partitioning, Auto-Scaling, Bottleneck Analysis, Two Worked Designs, Write-the-runbook) — all fixable content gaps, not fundamental flaws.

## 🗺️ The Journey

Plan order (window 1 of 2, offset 5 of a 10-quest level):

1. ❌ **API Gateway Patterns: The Single Front Door** — *errored / no score* · engine hit
max-turns (40) and exited 1 trying to make the Chapter 2 NGINX gateway serve a route; the lab omits the two upstream services it proxies to, so the gateway can't come up.
2. ⚠️ **Event-Driven Design: Pub/Sub, Event Sourcing, and CQRS** — **74** · event-sourcing
fold, idempotency, producer, and live Redpanda all ran as documented; the Chapter 1 **consumer snippet hangs forever** as written (no `auto_offset_reset`, no timeout).
3. ⚠️ **Scaling Strategies: Horizontal Growth, Caching, and CAP** — **77** · cache-aside
and shard-router ran correctly against real Redis, K8s YAML valid, CAP/PACELC accurate; two secondary objectives are listed but only linked out, never taught.
4. ✅ **Weaving the Whole: The Serpent Closes the Circle** — **94** · capstone; every
YAML/bash/mermaid/`gh` artifact checked clean against yamllint, shellcheck, mermaid-cli, and `gh --help`; only pedagogical gaps (unscaffolded runbook, a cross-chapter reference).
5. ✅ **System Design Interviews: A Framework for the Whiteboard** — **97** · every runnable
snippet executed and matched the quest's own stated numbers exactly; one promised "worked design" (news feed) is left as a challenge instead of worked.

## 🔬 Evidence

All outcomes below come from the sealed `--mode execute` run (real commands in a disposable Linux sandbox). Root-cause diagnoses I derived by reading the quest source are labeled `reasoned`.

### 1. API Gateway Patterns — ❌ errored, no score (`overall: 0.0`, `verdict: fail`)
- The engine **reached its 40-turn ceiling and exited 1** — this is an *errored* run, not a
  genuine 0% quality verdict. `meta` is empty; there is no per-dimension score.
- What it actually ran (from the sealed error transcript): repeated
`docker logs gw-test2`, `curl -s -i localhost:8080/users/`, `curl -s -i http://127.0.0.1:8080/users/`, and a `wget` fallback — all trying and failing to get the gateway to answer, `terminal_reason: max_turns`. **`tested` evidence: the gateway never served a request in the sandbox.**
- **Root cause (`reasoned`, from source lines 241–267):** the Chapter 2 `nginx.conf`
declares `upstream users { server users:8000; }` and `upstream orders { server orders:8000; }`. Those hostnames only resolve inside a Docker network that has `users`/`orders` service containers — which **the quest never provides** (no compose file, no service stubs, no network). `nginx:alpine` refuses to start when an upstream host can't be resolved, so `docker run … -v "$PWD/nginx.conf:…"` exits immediately and the Novice Challenge validation (`curl localhost:8080/users/`, line 359) can never succeed. That is exactly the wall the engine spent 40 turns hitting.

### 2. Event-Driven Design — ⚠️ 74 (`commands 3, accuracy 4, completeness 3, clarity 4, structure 5, safety 5`)
- Snippet coverage: **ran 6/9 runnable** (5 passed, **1 failed**), 2 skipped (macOS/Windows
  installers), 2 reasoned (mermaid render blocked by Chromium sandbox; Linux apt path).
- `passed`: live Redpanda container started (`docker run … redpandadata/redpanda` → logs
"Successfully started Redpanda!"); `KafkaProducer.send('user-events', …)` → "Sent OK"; the event-sourcing fold printed `70`, **exactly** matching the inline `# 70` comment; the idempotency snippet correctly skipped the second delivery (`['applied','skipped']`).
- `failed`: the **Chapter 1 consumer** (`KafkaConsumer('user-events', …)`, lines 236–246)
run exactly as written against the broker with a matching event already published — **produced no output after 8s (timeout), then hung.** Cause: no `auto_offset_reset` (defaults to `latest`) and no `consumer_timeout_ms`.

### 3. Scaling Strategies — ⚠️ 77 (`commands 4, accuracy 4, completeness 3, clarity 4, structure 4, safety 4`)
- Snippet coverage: **ran 3/6 runnable** (3 passed, 0 failed), 3 skipped (macOS/Windows/
sudo-apt install paths), 3 reasoned (K8s YAML parsed valid but no live cluster to `kubectl apply`; mermaid; CAP text block).
- `passed`: `docker run … redis:7-alpine` came up; the cache-aside snippet (with DB stubs
supplied) showed the documented `MISS → HIT → invalidate-on-write → MISS` cycle against live Redis; `shard_for(1024)` printed `db-shard-0`, **matching** the inline `# db-shard-0`.
- `reasoned`: the Chapter 1 Deployment+Service YAML parsed as two valid docs (PyYAML);
  CAP/PACELC narrative reviewed and accurate.

### 4. Weaving the Whole (Ouroboros VII) — ✅ 94 (`commands 5, accuracy 5, completeness 4, clarity 4, structure 5, safety 5`)
- Snippet coverage: **ran 6, all 6 passed**, 3 skipped (require authenticated `gh` against a
  real repo), 0 reasoned.
- `passed`: both workflow YAMLs → `yamllint` 0 issues + `yaml.safe_load` clean; the
merge-warden wait loop and smuggle-guard step → `shellcheck` clean, and the four verdict branches (self-only→wait, real-fail→exit1+label, pending→wait, all-green→merge) were hand-simulated correctly; both mermaid diagrams rendered to SVG via mermaid-cli; the Chapter 3 `git add/commit` ran in a fresh sandbox repo.
- `skipped` (legitimately un-runnable in isolation, not broken): `gh variable set …`,
`gh workflow run first-turn.yml`, `gh run watch` — all need real auth/CI history; syntax verified via each command's `--help`.

### 5. System Design Interviews — ✅ 97 (`commands 5, accuracy 5, completeness 4, clarity 5, structure 5, safety 5`)
- Snippet coverage: **ran 9, all 9 passed**, 3 skipped (macOS/Windows installers, redundant
  apt), 1 reasoned (functional-vs-non-functional text block).
- `passed`: the URL-shortener estimation script printed
  `Writes: ~40/s | Reads: ~4000/s` and `Storage: ~50 GB/month, ~3 TB / 5yr` — **exactly** the
quest's stated numbers; `code_by_hash`/`code_by_counter` produced valid 7-char codes and `62**7 = 3,521,614,606,208 ≈ 3.5 trillion` confirmed; both mermaid diagrams rendered; the powers-of-two/ten cheat sheet's numbers verified (86,400 s/day ≈ 10^5).

## 🐞 Issues Found

- **HIGH · API Gateway Patterns · Ch. 2 lab (`nginx.conf`, lines 241–267 + Novice Challenge
line 359).** The gateway config proxies to `upstream users { server users:8000; }` and `upstream orders { server orders:8000; }`, but the quest never supplies those two services, a `docker-compose.yml`, or a Docker network. NGINX won't start (unresolvable upstream), so `docker run … -v nginx.conf` fails and `curl localhost:8080/users/` cannot pass — the engine spent all 40 turns proving this and errored with no score. *Fix:* add a minimal compose file (gateway + two tiny stub upstreams, e.g. `hashicorp/http-echo` or a 10-line FastAPI/Flask returning `{"service":"users"}`) on a shared network, or clearly mark the lab as concept-only and drop the `curl … hits the right service` validation claim.
- **HIGH · Event-Driven Design · Ch. 1 consumer snippet (lines 236–246).** Run verbatim after
the producer, the consumer emits nothing and hangs forever (engine: no output after 8s, timeout) because `auto_offset_reset` defaults to `latest` and there's no timeout. *Fix:* add `auto_offset_reset='earliest'` and either `consumer_timeout_ms=…` or an explicit "Ctrl+C to stop" note, plus one sentence that a brand-new consumer group won't see events published before it started. (Observed via engine `failed` command.)
- **MEDIUM · Event-Driven Design · Secondary objective "Ordering and Partitioning" (line 110).**
Listed as an objective and skill bullet but never taught in the body. *Fix:* add a short Chapter 3 subsection on partition keys / per-aggregate ordering, or soften the objective. (`reasoned` from source.)
- **MEDIUM · Event-Driven Design · Intermediate Challenge (line 365).** Requires "a snapshot to
avoid replaying from the beginning," but snapshots are only *mentioned as a cost* (line 286), never demonstrated. *Fix:* add a minimal snapshot example (cache `balance` + last event index).
- **MEDIUM · Scaling Strategies · Secondary objectives "Auto-Scaling" & "Bottleneck Analysis"
(lines 109–110).** Both listed but only appear as external doc links / narrative assertions, with no in-quest teaching. *Fix:* add a minimal `HorizontalPodAutoscaler` YAML and a concrete bottleneck checklist (CPU vs. DB wait vs. queue depth). (`reasoned` from source.)
- **MEDIUM · System Design Interviews · Secondary objective "Two Worked Designs" (line 108).**
Promises a URL shortener **and** a news feed worked end-to-end; only the URL shortener is worked (Ch. 3), the news feed is left as the Intermediate Challenge. *Fix:* either work the news feed briefly or reword the objective. (`reasoned` from source.)
- **MEDIUM · Weaving the Whole · Objective "Write the runbook" (line 87).** A top-level graded
objective that only reappears as an unscaffolded challenge bullet (line 245). *Fix:* add a 3–5-header skeleton so learners aren't inventing the format for a graded objective.
- **LOW · Scaling Strategies · Ch. 2 cache-aside snippet (lines 263–275).** Calls undefined
`db_fetch_product` / `db_update_product` (NameError on a verbatim paste) and uses the deprecated `cache.setex(...)`. *Fix:* a one-line "stand-in for your persistence layer" comment and switch to `cache.set(key, value, ex=TTL)`. (Engine supplied stubs to make it run.)
- **LOW · Weaving the Whole · Ch. 3 `first-turn.yml` (line 221).** Invoked via
`gh workflow run first-turn.yml` but never defined/referenced in this file. *Fix:* one-line pointer to the earlier chapter that defines it.
- **LOW · Event-Driven Design & others · macOS/Windows Docker setup.** After
`brew install --cask docker` / `winget install Docker.DockerDesktop`, Docker Desktop must be manually launched before `docker run` works — worth a one-line note (recurs in api-gateway and scaling too). (`reasoned`.)

No fabricated issues: every HIGH/failed item above is tied to a command the engine actually ran; every `reasoned` item is tied to a quoted source line.

## 🔗 Chain Continuity

**Dependency spine (System Design Mastery series).** Four of the five quests form a clean, correctly-ordered learning path: `microservices-architecture` (required prereq, in window 0 — not walked here) → **api-gateway** (unlocks scaling) → **event-driven** (side path, unlocks scaling) → **scaling** (unlocks system-design) → **system-design-interviews** (capstone, unlocks 1111 technical-leadership). Frontmatter `quest_dependencies` and the prose "Next Steps" links agree, and the capstone genuinely *reuses* earlier concepts: the System Design Interview's URL-shortener design pulls the load balancer + Redis cache-aside + sharded store straight from Scaling Strategies (lines 298–341), and its estimation invokes the exact CAP framing taught in Scaling Ch. 3. This is a well-woven chain — a learner finishing Scaling is genuinely ready for the capstone.

**Prerequisite gap at the window boundary.** All four series quests hard-require `/quests/1110/microservices-architecture/`, which lives in **window 0** (offset 0–4) and was not part of this walk. That's expected windowing, not a defect — but it means a learner dropped into this window cold is missing the assumed foundation. Nothing in *this* window re-establishes it.

**One quest is from a different campaign.** "Weaving the Whole" is **Ouroboros Loop VII** (`quest_series: The Autonomous Realm`, `quest_line: The Ouroboros Loop`), not the System Design Mastery arc. Its prereqs are "every prior chapter of this campaign" + "your potion-book repository with walk+fix lanes green" + a Claude Code OAuth token (lines 46–52) — none of which the other four quests provide. It's an excellent quest in isolation (94), but it does **not** chain to its neighbours here: a learner arriving from Scaling Strategies has no potion-book repo and no chapters I–VI. It reads as a co-located capstone from a parallel campaign that happens to share level 1110, not the next step in this path.

**Character-fit friction (digital-artist).** This is the **Digital Artist (UI/UX)** path's Master level, yet all five quests are backend/infrastructure/DevOps system-design content with no UI/UX angle, and every "Character Class Recommendations" block names only Software Developer, System Engineer, Security Specialist, and Data Scientist — **never Digital Artist**. A UI/UX learner who followed this class here would find no thread addressed to them and no next-step tailored to their class. That's a curriculum-mapping observation for a maintainer, not a bug in any single quest.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sealed). I consumed the workflow-minted `walk-evidence.json` /
`walk-evidence.md` verbatim and did **not** run, regenerate, or edit the engine — its child `claude` processes can't authenticate from my Bash tool. I did not modify `walk-plan.json` or either evidence file. My only write is this report.
- **What I ran vs. reasoned:** The `passed`/`failed`/`skipped` outcomes and all quoted command
output are the engine's real sandbox results (a disposable Linux host with Docker, Python 3.12, Redis, Redpanda, yamllint, shellcheck, mermaid-cli, `gh`). Everything I label `reasoned` — the API-gateway root cause, the missing-secondary-objective gaps, the cross-campaign continuity finding, and the character-fit note — I derived by reading the five quest sources in plan order (`Read` on each `path`), quoting line numbers.
- **Coverage & limits, stated honestly:**
  - This is **window 1 of 2** — I walked 5 of the level's 10 quests. Window 0 (microservices +
    the other four) was out of scope; I did not assess it.
  - **Quest 1 (API Gateway) has no engine score** — it errored on max-turns. I report it as
    *errored*, not as a 0% quality judgment, and my score-free diagnosis of *why* is `reasoned`
    from the config plus the engine's `tested` failed-curl transcript.
  - Several snippets were **skipped by design** (macOS/Windows installers, sudo-apt, and `gh`
    commands needing real auth) — these are honest environment limits, not quest defects; the
    engine verified their syntax via `--help`.
  - Two mermaid renders were **blocked by Chromium sandbox restrictions** in the engine
    environment (marked `reasoned`), though other mermaid diagrams in the same slice did render
    — so the diagrams themselves are not implicated.
- **Confidence:** High on the two capstones (94/97, full snippet pass) and on the two
HIGH-severity findings (both witnessed by a real failed/hung command). Medium on the completeness gaps (consistent across quests, source-verified, but judgment calls about what a quest "promises"). The overall **warn** reflects one genuinely blocking lab (API Gateway) and a recurring "objective promised, not taught" pattern against an otherwise technically excellent, well-sequenced slice.

---

### Appendix — machine evidence (verbatim excerpt from `walk-evidence.md`)

> **4** quests evaluated · ✅ 2 pass · ⚠️ 2 warn · ❌ 1 fail · avg **85.5%** · ~$2.5573
>
> - ❌ API Gateway Patterns — engine exited 1, `terminal_reason: max_turns` (reached 40 turns)
> - ⚠️ 74 · Event-Driven Design — ran 6/9 runnable (1✗ consumer hang)
> - ⚠️ 77 · Scaling Strategies — ran 3/6 runnable, cache-aside + shard-router passed on live Redis
> - ✅ 94 · Weaving the Whole — every YAML/bash/mermaid/gh artifact clean
> - ✅ 97 · System Design Interviews — all 9 runnable snippets passed, outputs matched exactly
