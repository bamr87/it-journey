---
title: 'Walkthrough — Game Developer · Level 0001 (Web Fundamentals)'
date: '2026-08-25T00:00:00.000Z'
character: game-developer
level: '0001'
theme: Web Fundamentals
tier: Apprentice
quest_count: 1
mode: execute
overall_verdict: fail
session:
  window: '5 of 6 (offset 25, size 5)'
  total_quests_in_level: 26
  engine_average: 52.0
  engine_counts: '0 pass · 0 warn · 1 fail'
  cost_usd: 1.8348
  note: >-
    Sealed execute-mode evidence consumed as-is from walk-evidence.json /
    walk-evidence.md (workflow-minted). No engine re-run, no content edits.
---

## 🎯 Session Summary

I walked the **last window (5 of 6)** of the **Game Developer → Level 0001 "Web Fundamentals" (Apprentice 🌱)** path, backed by the workflow's sealed execute-mode engine evidence. The level holds **26 quests**; the planner's dependency-sorted window for this slot resolves to exactly **one** quest — `stack-attack` — so this session is a single-quest walkthrough by design, not a curtailed multi-quest run.

**Headline verdict: FAIL.** The quest scored **52.0%** (`commands_work 2 · content_accuracy 2 · completeness 3 · clarity 3 · structure 4 · safety 4`, out of 5 each). The engine actually ran the Chapter 4 Django bootstrap (venv → pip install → `startproject` → 7× `startapp` → `migrate`) and the Chapter 5 Vite/npm scaffold end-to-end successfully, and both Mermaid diagrams plus the `docker-compose.yml`/nginx config validated cleanly. But five of the quest's showcased "Sample Agent Output" code blocks — the parts a learner is most likely to copy-paste verbatim — are broken as written: a leaked Jekyll `{% raw %}{% endraw %}` template tag inside a TSX sample (6 real TypeScript compile errors), a missing `timedelta` import in the Django settings sample (`NameError` on use), and a Tailwind/shadcn setup sequence that no longer matches the currently published package versions (`tailwindcss init` was removed in v4; `shadcn init` now hangs on an undocumented interactive prompt). This is a hard/long quest (3–5 hrs, "🔴 Hard") whose scaffolding commands are genuinely solid, but whose "final answer" code samples need a real technical pass before they can be trusted for copy-paste use.

## 🗺️ The Journey

Plan order (dependency-sorted window; window 5 of 6 resolves to a single quest):

1. ❌ **Stack Attack: AI-Built Django + React Enterprise ERP** · *main* · **52%** · Backend/frontend scaffold commands genuinely work end-to-end; the flagship "sample agent output" code (Django settings, TSX data table, Tailwind/shadcn setup) is broken or stale as written, and two challenge checklists (health endpoints, `docker compose up`) can't be satisfied from what the quest actually provides.

## 🔬 Evidence

All figures below are from the sealed `walk-evidence.json` (mode: `execute`, real commands run in the disposable sandbox: 21 of 39 recorded commands actually run, 16 passed / 5 failed / 5 skipped / 13 reasoned against 20 identified runnable snippets out of 32 available blocks). Nothing here is hand-entered.

**stack-attack — 52% (fail).**

- ✅ **`passed`** — Chapter 4 backend bootstrap ran fully in the sandbox: `python3.12 -m venv .venv`, all 15 pinned packages (`django==5.1.*`, DRF, SimpleJWT, guardian, celery, etc.) installed cleanly, `django-admin startproject config .` + all 7 `manage.py startapp` calls succeeded, `python manage.py migrate` applied cleanly against SQLite. Django 5.1.15 confirmed installed.
- ✅ **`passed`** — Chapter 5 frontend bootstrap: `npm create vite@latest erp-frontend -- --template react-ts` scaffolded correctly, and `npm install @tanstack/react-query @tanstack/react-router @tanstack/react-table zustand axios react-hook-form zod @hookform/resolvers recharts date-fns clsx tailwind-merge` added 115 packages with 0 vulnerabilities.
- ✅ **`passed`** — Both Mermaid diagrams ("Quest Network Position", "Full ERP Stack Architecture") rendered cleanly via `mmdc`; `docker compose -f docker-compose.yml config` validated the 10-service compose file (only a benign `version: "3.9"` deprecation warning); the nginx `dev.conf` is syntactically valid (the only error seen — `host not found in upstream "django:8000"` — is expected outside the real Compose network, not a config bug).
- ❌ **`failed`** — `config/settings/base.py` sample: AST inspection confirms `SIMPLE_JWT` uses `timedelta(minutes=15)` / `timedelta(days=7)` but the file never imports `timedelta` (only `Csv`, `config`, `Path` from `decouple`/`pathlib`) — raises `NameError` if copy-pasted as-is.
- ❌ **`failed`** — `src/pages/sales/orders/index.tsx` sample (the flagship "ERP Sales Orders Page"): contains a literal leaked Jekyll/Liquid tag, `params={% raw %}{{ id: row.original.customer.id }}{% endraw %}>` (source line ~1296), which is not valid JSX. `tsc --noEmit` produced 6 real errors (`TS1109`, `TS1005` ×2, `TS1160` unterminated template literal).
- ❌ **`failed`** — `npm install -D tailwindcss postcss autoprefixer @types/node && npx tailwindcss init -p`: install succeeds but installs Tailwind **4.3.3** (current npm latest); v4 removed the `init` CLI subcommand entirely, so the command errors with `npm error could not determine executable to run`. The quest's documented flow is v3-only.
- ❌ **`failed`** — `npx shadcn@latest init`: did not run non-interactively as implied — hung on a new "Select a component library" prompt (Base UI/React Aria/Radix UI) not mentioned anywhere in the quest, and had to be killed after a 60s timeout.
- ❌ **`failed`** — Challenge 2 (`/health/`, `/api/schema/`, `/api/token/`): `migrate` succeeded, but none of these endpoints are ever wired into `urls.py` anywhere in the quest — only "sample settings" are shown, never the URL routing — so they would 404 on the project as actually built from the given commands.
- ⏭ **`skipped`** — `shadcn add <components>` (depends on `init` completing, which it didn't); `npm install -D openapi-typescript orval` and Challenge 4's `docker compose up -d` (skipped for turn budget / missing `Dockerfile.dev`, respectively — see Issues).
- 🧠 **`reasoned`** — ~13 blocks are natural-language `/stackattack` chat prompts mislabeled with unrelated fence languages (`sql`, `text`, `bash`, `jsx`), so they are not literally executable and were reasoned about, not run; Python model/view/task samples (`models.py`, `views.py`, `celery.py`, `tasks.py`, `orval.config.ts`, `axios-instance.ts`) were validated via `ast.parse()`/`tsc --noEmit` for syntax only (not independently runnable without the rest of the project) and are documented as such.

## 🐞 Issues Found

Every item cites what was actually observed by the engine in this run (`tested`) or read directly from the source (`reasoned`); severities as scored by the engine's own recommendations.

- **HIGH · stack-attack · Chapter 5 / `SalesOrdersPage.tsx` sample · `tested`** — Leaked Jekyll `{% raw %}{{ id: row.original.customer.id }}{% endraw %}` template tags inside `<Link params={...}>` (source ~line 1296) make the flagship frontend code sample fail to compile (6 TypeScript errors via `tsc --noEmit`). *Fix:* replace with plain JSX `params={{ id: row.original.customer.id }}`.
- **HIGH · stack-attack · Chapter 4 / `settings/base.py` sample · `tested`** — `SIMPLE_JWT` uses `timedelta(...)` without importing it (source ~line 869 imports only `Csv`, `config`, `Path`). Raises `NameError` if copy-pasted. *Fix:* add `from datetime import timedelta`.
- **HIGH · stack-attack · Chapter 5 / Tailwind CSS setup · `tested`** — `npx tailwindcss init -p` (source ~line 1131) no longer exists in Tailwind v4, which is what `npm install tailwindcss` currently resolves to. *Fix:* pin `tailwindcss@^3` explicitly if the v3 workflow is intended, or switch to the v4 flow (`@tailwindcss/vite` plugin, CSS-based config, no `init` command).
- **MEDIUM · stack-attack · Chapter 5 / shadcn/ui init · `tested`** — `npx shadcn@latest init` (source ~line 1134) now prompts for a base component library (Base UI/React Aria/Radix) that the quest never mentions and isn't fully silenced by any flag shown; the engine's run hung and had to be killed. *Fix:* document the exact non-interactive flag/answer, or walk through the prompt explicitly.
- **MEDIUM · stack-attack · Chapters 4–6 / missing `urls.py` and `Dockerfile.dev` · `tested`+`reasoned`** — Challenge 2 requires `/health/`, `/api/schema/`, `/api/schema/swagger-ui/`, `/api/token/` to work, but no `urls.py` wiring is ever given (only "sample settings"); `docker-compose.yml` (Challenge 4) references `dockerfile: Dockerfile.dev` for both `erp-backend` and `erp-frontend` build contexts, but no `Dockerfile.dev` content appears anywhere in the quest. Both challenges' own success criteria are unreachable from the material given. *Fix:* provide the missing `urls.py` routes and a sample `Dockerfile.dev` for each service.
- **MEDIUM · stack-attack · settings vs. frontend pagination mismatch · `reasoned`** — `settings/base.py` sets `DEFAULT_PAGINATION_CLASS: 'rest_framework.pagination.CursorPagination'`, but the `SalesOrdersPage` sample does page-number pagination (`useState` page counter, `Math.ceil((data?.count ?? 0)/50)`) — `CursorPagination` doesn't expose page numbers or a stable `count` the way `PageNumberPagination` does; the two "agent output" samples contradict each other. *Fix:* align both samples on one pagination strategy.
- **LOW · stack-attack · Chapter 1 / `stackattack.prompt.md` nested fence · `reasoned`** — The inner ` ```yaml ` block (source line 289) is closed with ` ```markdown ` (source line 330) instead of a bare ` ``` `, an invalid CommonMark closing fence — the prompt file a learner creates would contain a visibly malformed inner fence when opened in an editor. *Fix:* close with a bare fence.
- **LOW · stack-attack · fence language labels · `reasoned`** — Multiple `/stackattack` chat-prompt blocks are labeled with unrelated fence languages (`sql`, `text`, `bash`, `jsx` — e.g. source lines 380, 420, 445, 668, 840, 1150, 1248, 1390), making it hard for a learner to tell "type this in the terminal" from "paste this into chat." *Fix:* adopt one consistent label (e.g. a `prompt` convention) for AI-chat text.
- **LOW · stack-attack · `docker-compose.yml` default credentials · `reasoned`** — `MINIO_ROOT_PASSWORD`, `GRAFANA_PASSWORD`, `POSTGRES_PASSWORD` all default to weak, well-known values (`minioadmin`, `admin`, `erp_dev_pass`) with every port published to the host, and no explicit localhost-only warning. *Fix:* add a one-line caution to change these before any shared/network-exposed use.
- **LOW · stack-attack · frontmatter `environment.variables.project_dir: Library` · `reasoned`, not scored by the engine** — I noticed while reading the source that the quest's `environment:` frontmatter block sets `variables.project_dir: Library`, which reads like a stray fragment from the macOS prompts path (`~/Library/Application Support/Code/User/prompts/`) rather than a meaningful project directory name for this ERP quest. Flagging for a maintainer to check; not confirmed as user-facing since this environment block did not visibly drive the quest body in this pass.

**No blocking issue was found in the parts the engine actually ran successfully** — the Django/DRF backend bootstrap, the Vite/npm frontend bootstrap, both Mermaid diagrams, and the Docker Compose/nginx configs are all genuinely sound as written.

## 🔗 Chain Continuity

This window resolves to a single quest, so "chain continuity" here is about how `stack-attack` sits in the level rather than a multi-quest sequence:

- **Prerequisites are thin and honest about it.** `quest_dependencies.required_quests` is empty; only `terminal-fundamentals` (level 0000) is *recommended*, not required. The quest's own `prerequisites.knowledge_requirements` (Python fundamentals, JS/TS basics, REST familiarity, basic Docker) and `system_requirements` (VS Code + Copilot, Docker Desktop, Python 3.12+/Node 20+, Git) are listed explicitly up front — good practice — but nothing earlier in the level's dependency graph actually teaches Django, DRF, React, or Docker Compose at the depth this quest assumes. A true apprentice arriving here only with `terminal-fundamentals` behind them would be significantly under-prepared for a "🔴 Hard, 3–5 hour" quest that expects working knowledge of all four.
- **`unlocks_quests` is empty and "Next Epic Adventures" is prose-only.** The Quest Network Position Mermaid diagram (Chapter start) draws arrows from `Main` to `Mod`/`Sec`/`DevOps` ("ERP Module Development", "Enterprise Security Hardening", "Enterprise DevOps Epic"), and the closing "🔮 Your Next Epic Adventures" section names five follow-on quest ideas — but none of these are registered as real files (`unlocks_quests: []` in frontmatter, and none of the five closing bullets link to an actual `/quests/...` permalink). A learner who finishes this quest and looks for "what's next" hits a dead end in the registry even though the quest visually promises a continuation.
- **Self-contained but not scaffolded toward it.** Everything a learner needs to *attempt* the quest (agent prompt setup, bootstrap commands, sample code) lives inside this one file — it doesn't lean on earlier level-0001 quests for setup, which is good isolation. But because nothing upstream builds the Django/React/Docker foundation this quest assumes, and nothing downstream in the registry continues it, `stack-attack` currently functions as an isolated "boss quest" bolted onto Level 0001 rather than a link in a walkable chain — worth a maintainer decision on whether it belongs at a higher level or needs real prerequisite quests built under it.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sandboxed), from **sealed workflow-minted evidence** (`walk-plan.json` + `walk-evidence.json`/`.md`). I consumed them as-is — I did **not** re-run the engine (its child `claude` processes can't authenticate from my Bash tool) and made **zero** edits to the plan, the evidence, or any quest content. My only write is this report.
- **What I tested vs. reasoned:** All `passed`/`failed` calls above come from commands the engine actually ran in its disposable sandbox (backend/frontend bootstraps, `tsc --noEmit`, `ast.parse()`, `mmdc`, `docker compose config`, `nginx -t`). The ~13 `/stackattack` chat-prompt blocks and several reference-only sections (dependency-audit cheat sheet, `gh repo clone` third-party examples) are natural-language content, not executable commands, and were `reasoned` from source, not run. I read the entire quest file myself (front matter through the closing knowledge-graph block) to ground the chain-continuity findings — the `project_dir: Library` and empty-`unlocks_quests` observations are mine from that read, layered on top of the engine's evidence, not machine-scored.
- **Coverage limits (honest):** This is **window 5 of 6** of a 26-quest level, and it resolves to exactly **one** quest — this run does not (and was not meant to) sweep the rest of the level; the perfection ledger accumulates coverage of the other windows over separate runs. Within this single quest, the engine itself skipped a few blocks for turn budget (`openapi-typescript`/`orval` install, `shadcn add` components) and could not safely execute the interactive-prompt/background-server steps (`createsuperuser`, `runserver`, `docker compose up -d` with no `Dockerfile.dev`) — those are labeled `skipped`/`reasoned` above, not fabricated as `passed`.
- **Confidence:** High on everything reported as `passed`/`failed` — these are real command outputs (AST parses, `tsc` errors, `npm`/`pip` install logs, `docker compose config` validation) quoted from the sealed evidence, not inferred. Moderate on the chain-continuity read, since it depends on the registry's `unlocks_quests`/`quest_dependencies` fields being accurate reflections of what other quest files exist — I did not independently verify the full level-0001 quest graph beyond what's declared in this file's front matter.

---

*Machine evidence excerpt (verbatim from `walk-evidence.md`):*
> **1** quests evaluated · ✅ 0 pass · ⚠️ 0 warn · ❌ 1 fail · avg **52.0%** · ~$1.8348
>
> The backend Django bootstrap and frontend Vite scaffold both genuinely work end-to-end when actually run, and both mermaid diagrams and the docker-compose.yml/nginx config validate cleanly, but several of the quest's showcased 'sample agent output' code blocks are broken as written: the Sales Orders TSX page contains leaked Jekyll template tags that fail to compile, the settings.py sample is missing a `timedelta` import, and the Tailwind/shadcn setup instructions are stale against currently published package versions. Combined with missing urls.py/Dockerfile.dev wiring needed to satisfy its own challenge checklists, this quest needs a real technical pass before its code samples can be trusted for copy-paste use.
