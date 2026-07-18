---
title: Game Developer · L0111 · 2026-07-18
description: Quest-perfection walkthrough of the API Development slice game-developer/0111 on 2026-07-18,
  engine verdict warn. An evidence-based, learner's-eye session…
date: '2026-07-18T13:48:10.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Game Developer
tags:
- game-developer
- level-0111
- walkthrough
- quest-perfection
- warn
- api-development
render_with_liquid: false
excerpt: 'Game Developer · Level 0111 — API Development: an evidence-based quest-perfection walkthrough
  from 2026-07-18.'
slice: game-developer/0111
character: game-developer
level: '0111'
theme: API Development
tier: Adventurer
verdict: warn
quest_count: 5
walk_date: '2026-07-18'
run_url: https://github.com/bamr87/it-journey/actions/runs/29642483805
source_report: test/quest-validator/walkthroughs/2026-07-18-game-developer-0111.md
---

> **Slice** `game-developer/0111` · **Level** 0111 (API Development) · **Adventurer tier** · **Engine verdict** ⚠️ warn · **Walked** 2026-07-18
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29642483805) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-18-game-developer-0111.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-18-game-developer-0111.md)

---

## 🎯 Session Summary

I played the **Game Developer / Level 0111 (API Development, ⚔️ Adventurer)** slice
as a learner — specifically **window 2 of 2** (the level has 10 quests; this window
is the last 5). The five quests walked, in planned order, were: **API Authentication**
(🔴 Hard), **Error Handling**, **Rate Limiting**, **API Versioning**, and **API
Documentation** (all 🟡 Medium). The sealed execute-engine evidence scores them
**avg 84.2%** — **4 pass, 1 warn, 0 fail**.

**Headline verdict: WARN.** The slice is technically strong and holds together as a
learning path, but two things keep it from a clean pass: **Error Handling (76%)**
leans its primary hands-on lab on the public `httpbin.org`, which was returning
503s and then timing out during the run, with no in-quest pointer to the Docker
fallback that *does* work; and a recurring, chain-wide reliance on live network
(`curl` to `api.github.com`/`httpbin.org`) plus unlabeled `api.example.com`
placeholders creates repeated friction for a real beginner. None of these are
correctness bugs in the taught concepts — the code and claims that *could* be
executed checked out — they are resilience/clarity gaps a content pass can fix.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|--:|:--:|---|--:|---|
| 1 | ✅ pass | API Authentication: Keys, Tokens, OAuth2, and JWT | 86 | PyJWT + Docker snippets ran exactly as documented; a fragile `base64 -d` decode and a couple of doc nits are the only dents. |
| 2 | ⚠️ warn | Error Handling: Status Codes, Problem Details, and Retries | 76 | Concepts and JSON are accurate and the retry logic verified, but the httpbin.org lab was down and the retry lab silently needs `pip install requests`. |
| 3 | ✅ pass | Rate Limiting: Token Buckets, 429s, and Quotas | 88 | Token-bucket and polite-client code ran flawlessly against a local mock; gaps are an untaught "sliding window" objective and a code-less leaky bucket. |
| 4 | ✅ pass | API Versioning: URI, Headers, and Backward Compatibility | 83 | Live GitHub header-versioning verified; dinged for unlabeled `api.example.com` placeholders and an untaught semver objective. |
| 5 | ✅ pass | API Documentation: OpenAPI, Swagger, and Contract-First | 88 | Lint, build-docs, Swagger UI, and Python codegen all genuinely worked; one broken `redocly preview` aside and a Ch1→Ch2 merge ambiguity. |

## 🔬 Evidence

All results below come from the sealed `walk-evidence.json` (execute mode, `mock:false`).
"ran/runnable" = snippets executed vs. runnable snippets the engine identified.

### 1. API Authentication — ✅ 86 (ran 5/8 runnable · 5 passed, 0 failed, 3 skipped, 3 reasoned)
- **PyJWT encode/decode** (Ch2) — `passed`. Ran verbatim: produced a 3-part token and
  round-tripped `sub='user-42'`, `scope='read:profile'`. Tamper test (flip one payload
  char) raised PyJWT `Signature verification failed` — confirming the quest's claim.
- **`python3 -m pip install pyjwt`** (macOS/Linux) — `passed`. Installed pyjwt-2.13.0 cleanly.
- **Docker cloud snippet** — `passed`. `docker run --rm python:3.12-slim …` pulled and
  imported pyjwt 2.13.0 (dropped `-it`, which needs a TTY).
- **`echo "$JWT" | cut -d. -f2 | base64 -d`** (Ch2) — `passed` for the generated token,
  but the engine demonstrated it **fails on real-world base64url tokens**: a payload with
  `-`/`_` chars produced `base64: invalid input`.
- **GitHub `curl` calls** — `skipped` (curl denied by sandbox for all destinations).
  Equivalent Python urllib to `https://api.github.com/user` with no token returned **HTTP 401**,
  matching the quest's "unauthenticated call is rejected" claim.
- `api.example.com` / `auth.example.com` key & token-exchange snippets — `reasoned`
  (intentional placeholders; syntax correct).

### 2. Error Handling — ⚠️ 76 (ran 7/8 runnable · 4 passed, **3 failed**, 3 skipped, 2 reasoned)
- **`curl … https://httpbin.org/status/{404,429,503,400}`** — `failed`. curl denied by
  sandbox; the Python urllib equivalent got **HTTP 503** on the first pass and then
  **timed out** entirely on retry. The quest's primary hands-on mechanism was
  non-functional during the run.
- **Docker httpbin fallback** — `passed`. `docker run --rm -d -p 8080:80 kennethreitz/httpbin`
  pulled and correctly returned 418/404/503/429/400 locally. **This works and is the fix —
  but the quest never points learners to it when httpbin.org is down.**
- **Python retry lab** — `passed` against a local mock (503×2 then 200): correct retry,
  honored Retry-After, returned the eventual 200. But `import requests` raised
  **`ModuleNotFoundError`** on a bare Python 3 — `pip install requests` was required and is
  not listed in System Requirements.
- **problem+json examples** (both) — `passed`, valid JSON via `jq .`.
- `api.example.com` content-type / idempotency snippets — `reasoned` (non-resolving placeholder).

### 3. Rate Limiting — ✅ 88 (ran 3/7 runnable · 3 passed, 0 failed, 4 skipped, 1 reasoned)
- **TokenBucket** (Ch1) — `passed`. `python3 token_bucket.py` output exactly
  `[True, True, True, True, True, False, False]` as documented; refill test (sleep 1.05s → `True`) confirmed.
- **`polite_get` backoff** (Ch3) — `passed`. Against a local mock returning 429+Retry-After:1
  then 200, it slept ~1.0s and returned 200 — backoff/Retry-After logic correct.
- **Docker python image** — `passed` (non-interactive equivalent of the `-it` REPL step).
- **4× `curl https://api.github.com/…` header checks** — `skipped` (outbound network denied).
  Expected to work in a normal environment; the single "real API" exercise was unverifiable here.

### 4. API Versioning — ✅ 83 (ran 4/8 runnable · 4 passed, 0 failed, 4 skipped, 4 reasoned)
- **GitHub header versioning** — `passed` (via Python equivalent, curl blocked). Request with
  `X-GitHub-Api-Version: 2022-11-28` returned **HTTP 200** and header
  `x-github-api-version-selected: 2022-11-28`, matching the quest.
- **Docker curl image** — `passed`. `docker run --rm curlimages/curl:latest …` pulled and hit
  the GitHub API with the version header successfully.
- **`curl … jsonplaceholder…/users/1 | jq '{id,name}'`** — `passed`, returned
  `{"id":1,"name":"Leanne Graham"}`. **But** the real response has **no `nickname` field**
  (fields: address, company, email, id, name, phone, username, website) — the Ch1
  robustness-principle prose implies one exists.
- **RFC 9745 / RFC 8594** citations — both resolve (verified). Deprecation/Sunset content accurate.
- `api.example.com` v1/v2/header snippets — `skipped` (RFC 2606 placeholder, does not resolve).

### 5. API Documentation — ✅ 88 (ran 9/7 runnable · 8 passed, **1 failed**, 3 skipped, 2 reasoned)
- **`npm install -g @redocly/cli`** — `passed` (redocly 2.39.0).
- **Empty-dir lint** — `passed`. `redocly lint openapi.yaml` in an empty dir failed with
  "does not exist or is invalid" — **exact match** to the quest's warning.
- **`security: []` claim** — `passed` and verified **load-bearing**: removing it caused 2 real
  errors + exit 1; restoring it returned clean exit 0. The quest's precision here is correct.
- **`redocly build-docs`** — `passed`, produced a 47KB HTML with `<title>Bookstore API</title>`.
- **Swagger UI container** — `passed`, healthy on :8080, auto-removed.
- **`openapi-generator-cli generate -g python`** — `passed`, generated a full Python client
  (with a benign "OpenAPI 3.1 support is still in beta" warning).
- **`redocly preview openapi.yaml`** — `failed`. On CLI 2.39.0 it errors `Unknown argument:
  openapi.yaml`; `redocly preview` is now a project-level command. This aside appears in **all
  four** platform blocks.

## 🐞 Issues Found

Every item below is backed by a command actually run in the sandbox or an exact quoted line
from the quest source. Nothing here is fabricated; network-restricted steps are labeled.

**High**
- **error-handling** · Chapter 1 / platform setup (httpbin.org reliance) — *Observed:* the
  public `httpbin.org` returned **503 then timeouts** for every `/status/*` path during the
  run, making the quest's primary hands-on lab non-functional; the Docker path
  (`docker run --rm -d -p 8080:80 kennethreitz/httpbin`) was verified to return the correct
  codes but is not offered as the fallback. *Fix:* add a callout — "if httpbin.org is
  unreachable, use the Docker/Cloud Realms path" — and prefer it as the primary lab.

**Medium**
- **error-handling** · Chapter 3 retry lab / System Requirements — *Observed:* `import requests`
  raised `ModuleNotFoundError` on a bare Python 3; the requirement lists only "Optional: Python 3."
  *Fix:* state `pip install requests`, or rewrite the snippet on stdlib `urllib.request`.
- **api-authentication** · Chapter 2 JWT decode one-liner — *Observed:* `base64 -d` failed with
  `base64: invalid input` on a payload containing base64url `-`/`_`. *Fix:* use a base64url-safe
  decode (`tr '_-' '/+'` + padding, or `base64.urlsafe_b64decode` in Python).
- **rate-limiting** · Chapter 2 header naming — *Reasoned:* the 429 example uses `RateLimit-*`
  while the live GitHub call returns `X-RateLimit-*`; the quest notes it, but it's easy to miss.
  *Fix:* promote the distinction to a callout box.
- **rate-limiting** · network dependency — *Observed:* 3 of 4 bash snippets require reaching
  `api.github.com`; all were unverifiable when network was blocked. *Fix:* add a local
  `http.server` mock emitting `X-RateLimit-*` so the Novice Challenge is offline-completable.
- **api-versioning** · Chapter 2 `api.example.com` URLs — *Observed:* domain does not resolve
  ("No address associated with hostname"). *Fix:* label these as illustrative placeholders that
  won't run.
- **api-documentation** · `redocly preview` aside (all 4 platform blocks) — *Observed:*
  `redocly preview openapi.yaml` errors `Unknown argument: openapi.yaml` on CLI 2.39.0.
  *Fix:* drop or correct the aside; keep `build-docs` + Swagger UI as the live-preview path.
- **api-documentation** · Chapter 1 → Chapter 2 continuity — *Reasoned:* the Ch2 YAML redeclares
  top-level `paths:`/`components:` and adds `security: []`; the quest never states it *replaces*
  the Ch1 skeleton, so a learner must infer the merge. *Fix:* say it explicitly and/or show the
  single final merged file.

**Low**
- **api-authentication** · macOS setup — "Python ships with macOS" is outdated (no default python3
  since Catalina). Qualify it.
- **api-authentication** · "Get a token first" callout forward-references the GitHub PAT creation
  steps that only appear in the Novice Challenge near the end. Move earlier or inline a one-liner.
- **api-authentication** · Docker cloud snippet's `-it` needs a TTY; note the non-interactive form.
- **error-handling** · idempotency curl shown once but captioned "two identical requests… only ONE
  payment"; show it run twice.
- **error-handling** · `api.example.com` content-type/idempotency snippets unlabeled as illustrative.
- **error-handling** · `jq` installed in setup but never used in any snippet.
- **rate-limiting** · "Fixed vs Sliding Window" is a listed secondary objective but never explained.
- **rate-limiting** · leaky bucket is conceptual only (no code), unlike the fully-implemented token bucket.
- **api-versioning** · Chapter 1 "nickname field" claim doesn't match the real jsonplaceholder response.
- **api-versioning** · Semantic Versioning is a listed objective but only linked, not taught in-body.
- **api-documentation** · OpenAPI Generator's "3.1 support is still in beta" warning is unexplained.
- **api-documentation** · mastery challenges have no answer key / reference solution.

## 🔗 Chain Continuity

**Ordering matches the dependency DAG.** Reading the `quest_dependencies` frontmatter, the walked
order is internally consistent:
- `api-authentication` unlocks → error-handling, rate-limiting
- `error-handling` unlocks → rate-limiting, api-versioning
- `rate-limiting` unlocks → api-versioning, api-documentation
- `api-versioning` unlocks → api-documentation
- `api-documentation` unlocks → Level 1000 (Cloud Computing)

So each quest in the plan order is genuinely a prerequisite/recommended predecessor of the ones
after it — a clean linear spine with no forward-reference between the walked quests.

**Conceptual handoffs are real, not just declarative.** Authentication teaches 401; Error Handling
picks up 401/403/404/429/5xx and problem+json; Rate Limiting then builds directly on Error
Handling's 429 with Retry-After and token buckets. Versioning and Documentation shift from
runtime behavior to API contract/lifecycle. A learner finishing quest N is conceptually ready for
N+1 within this window.

**Window boundary — an assumed prerequisite I could not verify.** This is **window 2 of 2**. Every
quest's `required_quests` points at **api-fundamentals** and/or **rest-principles**, which live in
**window 1** (offset 0–4) and were **not** part of this walk. The chain assumes the learner already
completed them (HTTP headers, status codes, JSON, REST constraints). That is the expected design for
a windowed sweep, but I want to be explicit: I **reasoned** about that prerequisite, I did not walk
those quests, so I can't attest they actually deliver what this window assumes.

**On-ramp friction.** The hardest quest (API Authentication, 🔴 Hard) sits first in this window. A
learner who arrives fresh at window 2 hits the steepest quest immediately after the (unseen) window-1
foundation — worth noting for pacing, though the difficulty labels are honest.

**Chain-wide friction pattern (the most actionable cross-quest finding).** Three of the five quests
depend on live third-party network for their headline hands-on step (GitHub API, httpbin.org), and
two use unlabeled `api.example.com` placeholders. When network was restricted/flaky, this produced
repeated dead-ends. The **Docker "Cloud Realms" fallbacks worked consistently** across the slice
(httpbin container, curlimages/curl, swagger-ui, python images) — the curriculum already has the
robust pattern; it just isn't offered as the default when the public endpoint fails (most acutely in
Error Handling). Elevating the Docker path and labeling placeholders would harden the whole chain.

**Character-path observation (not a defect).** This is the *Game Developer* path, yet Level 0111 is
entirely generic API Development content (auth, errors, rate limits, versioning, docs). These are
shared cross-character quests the game-developer route passes through; nothing is game-specific, which
is fine but worth flagging so a maintainer knows the level isn't tailored to the character theme.

## 🧠 Reasoning & Method

- **Mode:** `execute` — real commands in the disposable runner sandbox, `mock:false` on all five
  quests (confirmed per-quest in `walk-evidence.json`). This is genuine evidence, not review-only.
- **What I ran vs. what was sealed:** I did **not** re-run the engine — per the procedure, the
  workflow pre-computed and sealed `walk-plan.json` + `walk-evidence.json/.md`, and I consumed them
  as-is (the engine's child `claude` processes can't authenticate from an agent's Bash tool). My own
  work was: read all five quest sources in plan order, map the dependency frontmatter, and reason
  about the linked journey. I edited nothing.
- **Sandbox limits (honest coverage):** the sandbox **denied `curl` outright** (every destination,
  confirmed even for `curl https://example.com`) and blocked general outbound network. So network
  snippets were either verified via **Python urllib equivalents**, executed via **Docker**, or marked
  `skipped`/`reasoned`. `sudo`/`brew`/`winget`/PowerShell steps were OS-mismatched and judged by
  inspection (`reasoned`). These are sandbox artifacts, **not** quest defects — except the
  **httpbin.org 503/timeout**, which is a real availability problem a learner can also hit.
- **Coverage caps:** this was a **windowed** walk — 5 of the level's 10 quests (window 2 of 2). I did
  not walk window 1 (api-fundamentals, rest-principles, etc.), so prerequisite satisfaction for this
  window is `reasoned`, not tested. Snippet coverage varied by quest (ran/runnable): auth 5/8,
  error-handling 7/8, rate-limiting 3/7, versioning 4/8, documentation 9/7 — the low rate-limiting
  and versioning ratios are driven almost entirely by the network-denied `curl` snippets.
- **Confidence:** **High** on everything actually executed (PyJWT, token bucket, retry logic,
  redocly lint/build-docs, Swagger UI, codegen, Docker fallbacks — these ran and matched claims).
  **Medium** on network snippets substituted with urllib/reasoning. The Error Handling httpbin outage
  may be partly transient, but "primary lab depends on an unreliable public service with no fallback
  note" is a real, reproducible learner risk regardless.
- **Aggregate:** avg **84.2%**, 4 pass / 1 warn / 0 fail, engine cost ~$3.66. Overall session verdict
  **WARN**, driven by the Error Handling high-severity dependency issue plus the chain-wide network
  friction — a targeted content pass (not a rewrite) would lift the slice to a clean pass.

_Machine evidence rendered verbatim in `walk-evidence.md`; per-quest scores, commands, and
recommendations in `walk-evidence.json`. This report is self-contained; the two evidence files are
the sealed source of truth for the numbers above._
