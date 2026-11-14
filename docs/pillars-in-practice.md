# IT-Journey Pillars in Practice

> What each IT-Journey pillar and working approach means in day-to-day work, with the files that show it and the gaps where nothing does yet. Line references are as of 2026-10-29.

Source of the pillars: `pages/_about/about.md:62-69` (cards) and `:72-110` (prose). Canonical data: `_data/brand/values.yml`. Evidence below is from files in this checkout; gaps are stated.

## Pillars

### DFF: Design for Failure
**In practice:** assume steps will break; make breakage visible, recoverable and non-fatal. **Evidence:**
- `continue-on-error` in many workflows: `quest-perfection.yml` (5), `quest-fix.yml` (3), `site-quality.yml` (3), `quest-video.yml` (3), plus `link-checker.yml`, `issue-autopilot.yml`, `content-factory.yml`, `agentic-quest-review.yml` (all in `.github/workflows/`).
- `.github/workflows/quest-fix.yml:604` warns rather than fails when the fix PR can't be opened.
- Scheduled health checks: `link-checker.yml:13-14` (weekly), `zer0-doctor.yml:33` (theme doctor).
- Gates: `AGENTS.md:9` (done = `make build-ci` + `make content-audit` pass), `AGENTS.md:97` (placeholder content fails validation), `AGENTS.md:103` (CI fails on stale generated data).
- Brand voice: `.github/instructions/brand.instructions.md:38` ("DFF (honest about failures)").
**Strength:** strong.

### DRY: Don't Repeat Yourself
**In practice:** one authoritative source; reference it, don't copy it. **Evidence:**
- Reusable fleet workflows: `.github/workflows/ci.yml:28` → `bamr87/bamr87/.github/workflows/standard-ci.yml@v2`; `conformance.yml:23` → `fleet-conformance.yml@main`; `zer0-doctor.yml:47` → `bamr87/zer0-CMS/...`; shared `claude-run` action used by `issue-autopilot.yml:113,248`, `agent-audit.yml:71`, `content-factory.yml:113`, `theme-scout.yml:120`, `quest-walkthrough.yml:190`, `quest-idea-intake.yml:180`.
- `AGENTS.md:152`: the AI runner is "consumed by reference, never copied"; CI/release/conformance are seeded from the hub's `templates/`.
- Theme: `_config.yml:36` `remote_theme: "bamr87/zer0-mistakes"` (referenced, **not vendored**; no theme gem per `AGENTS.md:9`).
- Generated data instead of hand copies: `AGENTS.md:103` (`make quest-data` produces `_data/quests/*.yml`, `_data/navigation/quests.yml`); `docs/reference/make-targets.md` generated from the `Makefile` (`AGENTS.md:31`).
- Content: `_data/brand/values.yml:30-31` ("Guides point at this store; they never restate the values").
**Gap:** the pillar list itself is still restated by hand in several places (`pages/_about/README.md:94`, `pages/_about/features/index.md:124`, `contributing.md:226`, `docs/ROADMAP.md:253,450`) rather than rendered from `values.yml`, which is how the KIS/KISS drift happened. **Strength:** strong.

### KIS: Keep It Simple
**In practice:** plain, readable solutions and prose; clarity over cleverness. **Evidence:** `_data/brand/values.yml:32-37`; `_data/brand/voice.md:18` ("Plain over clever (KIS)"); `brand.instructions.md:38`; `AGENTS.md:9` (one-line definition of done); `markdown-oneline.yml` prose kit. **Gap:** mostly a writing rule. On the code side the system is not simple: ~38 workflows in `.github/workflows/` and many `scripts/` subdirs. Nothing measures simplicity. **Strength:** moderate (strong for prose, weak for engineering).

### REnO: Release Early and Often
**In practice:** small increments shipped continuously, with feedback. **Evidence:** `.github/workflows/release.yml:3-6` (release-please, fleet kit); `AGENTS.md:56` (CHANGELOG written only by release-please); `sync-gh-pages.yml:146` (recurring deploy PRs main → gh-pages); `content-auto-merge.yml`, `dependabot-auto-merge.yml`; `values.yml` REnO entry ("A working tutorial beats an unfinished epic"). **Strength:** strong.

### MVP: Minimum Viable Product
**In practice:** ship the smallest valuable slice first, then expand. **Evidence:** `PRD.md:25` "## 1. MVP (Minimum Viable Promise)" with ✅/🔄/🔜 scope (`PRD.md:29-36`); `features/features.yml` entries tied to PRD sections (`prd: ["§1", "§3"]`) with `status: shipped`; `values.yml` MVP writing implication. **Gap:** the PRD expands MVP as "Minimum Viable **Promise**", not "Product" as about.md says. The PRD content table (`PRD.md` "Current Content Status", e.g. 6 quests) looks stale. **Strength:** moderate.

### COLAB: Collaboration
**In practice:** people and agents propose; people review and merge; everything happens in public. **Evidence:**
- Agent lanes: `claude.yml`, `issue-autopilot.yml`, `agent-plan-then-act.yml`, `agent-audit.yml`, `content-factory.yml`, `quest-fix.yml:570` (`peter-evans/create-pull-request@v8`), opt-in per `AGENTS.md:128` and `scripts/ai/README.md`.
- Human gate: `AGENTS.md:9` ("a reviewer merges the PR"), `AGENTS.md:52` (`human-review`/`needs-human` labels), `AGENTS.md:148` and `_data/agents/autonomy-matrix.yml`, `_data/agents/registry.yml`.
- Community: `CONTRIBUTING.md`, `docs/CONTRIBUTING_DEVELOPER.md`, `pages/_about/contribute/contributing.md`, `update-contributor-profiles.yml`.
**Strength:** strong.

### AIPD: AI-Powered Development
**In practice:** AI does drafting/review/fixing under policy and human review; transparent about it. **Evidence:** the lanes listed under COLAB; `_data/ai.yml` and `scripts/ai/` (usage/cost tracking, `AGENTS.md:152`); `.github/instructions/` (AI agent instructions; `README.md:85` "AI assists while following IT-Journey principles"); `about.md:116` (describes this pipeline); `brand.instructions.md:38` ("AIPD (transparent about AI)"). **Strength:** strong.

## Dual readings: DFF and REnO

about.md uses only one reading for each pillar: **DFF = "Design for Failure"** (`pages/_about/about.md:62,72-74`) and **REnO = "Release Early and Often"** (`about.md:65,90-92`). It does not mention "Don't Forget the Fundamentals" or "Reduce, Eliminate, Normalize, Optimize". *Suggestion (not applied):* the About page could present both readings for each pillar.

### DFF, reading (a): Don't Forget the Fundamentals (hygiene)
- **IT systems management (monitoring and scheduled checks):** `.github/workflows/link-checker.yml:13-14` (weekly cron), `.github/workflows/zer0-doctor.yml:33-34` (weekly theme health check). The "Pages sentinel" only shows up as a contributor role (`_data/contributors/github-actions-bot.yml:29,101`); I found no workflow named that.
- **Runbooks:** none for the site itself. `docs/ROADMAP.md:554` lists "Troubleshooting guides and runbooks" as planned, and runbooks are only taught as quest content (`_data/quests/network.yml:696`). *Gap; idea:* add a `docs/runbooks/` page for "deploy red / gh-pages stale / Claude token broken".
- **Backups:** no repo or site backup process. The only hits are local `mv … .backup.$(date)` in generator scripts (`scripts/generation/generate-zer0-script.sh:297`) and an in-memory rollback in `scripts/quest/quest_audit.py:195-209`. *Gap; idea:* a scheduled export of Issues and `_data` to a release asset, or treat git plus gh-pages as the explicit backup in docs.
- **Pinned dependencies (software development):** `ci.yml:28` pins `standard-ci.yml@v2`, and the theme is deliberately unpinned (`_config.yml:30-36`). 17 workflow files reference `@main` (e.g. `conformance.yml:23`, the `claude-run@main` callers), and none use SHA pins. That floating-ref gap is the subject of issue #873, but the issue is not referenced anywhere in the checkout, so I couldn't verify it locally. *Idea:* pin fleet refs to tags or SHAs and let Dependabot bump them.
- **Warn-don't-fail steps (DevOps):** `continue-on-error` in 8 workflows (e.g. `quest-perfection.yml` ×5). `quest-fix.yml:604` warns rather than fails. `quest-video.yml:298` soft-skips on rate limits. `quest-perfection.yml:201` idles green on broken credentials "so the red doesn't withhold the gh-pages deploy".

### DFF, reading (b): Designed for Failure (resilience)
- **Graceful degradation:** `.github/workflows/README.md:19` (a run with no credentials is a clean no-op). AI lanes are opt-in behind switches (`AGENTS.md:128`). The about page falls back to a default contact address when `site.email` is unset (`pages/_about/about.md:151`; other Liquid `{% else %}` branches at `:136,147`).
- **Retries and failure-tolerant design:** `quest-fix-loop.yml:146` ("Green by design: the next schedule retries"), `sync-gh-pages.yml:189` (retry on next run), `dependabot-auto-merge.yml:130` (rebase and retry after a merge race), and `content-auto-merge.yml:39-42` (polls checks instead of trusting `--auto`).
- **Gates that fail closed:** `AGENTS.md:97,103` (placeholders and stale generated data fail CI).
- **Chaos engineering:** no evidence (the only "chaos" hits are quest and game flavour text). *Gap; idea:* a scheduled workflow that deliberately breaks a link or a frontmatter field on a scratch branch and checks that the validators catch it.

### REnO, reading (a): Reduce, Eliminate, Normalize, Optimize (improvement loop)
- **Reduce:** `content-auto-merge.yml:4-5` merged three copy-pasted auto-merge workflows into one lane.
- **Eliminate:** `_posts` and the blog were retired to lifehacker.dev (`README.md:44,113`). `_config.yml:636-638` drops the `posts` collection from preview scanning because the folder no longer exists. `AGENTS.md:31` notes `make test` is stale because `pages/_posts/` was removed (that loose end hasn't been eliminated yet).
- **Normalize:** `Makefile:79-80` (`content-normalize`, `content-normalize-apply` frontmatter normalizer) and `Makefile:242-243` (`quest-normalize`: relationships and retired fields).
- **Optimize:** cron spacing in `zer0-doctor.yml:34` ("off the hour, clear of the Monday crons") and preview scans no longer hitting a dead folder (`_config.yml:636`). There's no explicit performance budget. *Gap; idea:* track build time or Lighthouse scores in `site-quality.yml` as the Optimize metric.
- Across domains: in IT ops it's pruning dead jobs and config; in development it's deduplicating code and normalizing data; in DevOps it's consolidating pipelines. The repo shows all three, but as one-off cleanups rather than a named, repeated loop.

### REnO, reading (b): Release Early and Often (cadence)
- **Release cadence:** `release.yml:3-6` (release-please; CHANGELOG is written only by the bot, `AGENTS.md:56`).
- **Small PRs and auto-merge:** `content-auto-merge.yml:2` (merges green, in-scope automated PRs) and `dependabot-auto-merge.yml`. Agents open single-purpose PRs (`quest-fix.yml:570`).
- **Trunk-based delivery:** everything merges to `main` and deploys via `sync-gh-pages.yml:146` (main → gh-pages PRs). `pr-freshness.yml` keeps branches current.
- **Content:** `about.md:92` ("a tight, useful quest published today beats a sprawling, perfect one").

## Approaches (`about.md:69,110`; `purpose.md:21-25`; `values.yml` `approaches:`)

### PoLR: Path of Least Resistance
**In practice:** recommend the simplest working route before the advanced one. **Evidence:** `values.yml` PoLR writing implication; GitHub Pages + Jekyll hosting (`PRD.md:33`, `features.yml` FR-ITJ-001); one-command `make` entry points (`AGENTS.md:9,31`). **Gap:** no explicit enforcement or guidance beyond the values file. **Strength:** weak to moderate.

### OSAP: Open Source As Possible
**In practice:** open tools and free tiers; flag paid ones. **Evidence:** `LICENSE` (MIT); `README.md:3,15,34` ("open-source platform", `license: MIT`); Jekyll/GitHub Pages stack. **Gap:** AI lanes depend on proprietary services (Claude via `claude-run`); Algolia search (`features.yml` FR-ITJ-002) is a hosted service. No check that content flags paid tools. **Strength:** moderate.

### KISS: Keep It Stupid Simple
**In practice:** default to the most boring, reliable option. **Evidence:** `values.yml:72-74`; `about.md:110`; `purpose.md:25`. **Gap:** effectively the same idea as the KIS pillar; no separate evidence. See `docs/kis-kiss-fix.md`. **Strength:** weak (as a distinct idea).

## Summary

| Principle | Evidence | Key files |
|---|---|---|
| DFF (a) Fundamentals | Moderate: monitoring and warn-don't-fail are strong; backups and runbooks missing; `@main` pins float | `link-checker.yml`, `zer0-doctor.yml`, `ci.yml:28`, `quest-perfection.yml` |
| DFF (b) Designed for Failure (about.md) | Strong for degradation and retries; no chaos engineering | `quest-fix-loop.yml:146`, `sync-gh-pages.yml:189`, `workflows/README.md:19`, `about.md:151` |
| DRY | Strong (pillar-list drift is a gap) | `ci.yml`, `conformance.yml`, `_config.yml:36`, `AGENTS.md:152`, `_data/brand/values.yml` |
| KIS | Moderate | `_data/brand/values.yml`, `_data/brand/voice.md:18` |
| REnO (a) Reduce/Eliminate/Normalize/Optimize | Moderate: one-off cleanups, no named loop; Optimize weakest | `content-auto-merge.yml:4`, `README.md:44`, `_config.yml:636`, `Makefile:79,242` |
| REnO (b) Release Early and Often (about.md) | Strong | `release.yml`, `content-auto-merge.yml`, `sync-gh-pages.yml`, `AGENTS.md:56` |
| MVP | Moderate | `PRD.md:25`, `features/features.yml` |
| COLAB | Strong | `issue-autopilot.yml`, `claude.yml`, `_data/agents/autonomy-matrix.yml`, `CONTRIBUTING.md` |
| AIPD | Strong | `scripts/ai/`, `_data/ai.yml`, `.github/instructions/` |
| PoLR | Weak–moderate | `values.yml`, `Makefile` |
| OSAP | Moderate | `LICENSE`, `README.md` |
| KISS | Weak (duplicates KIS) | `values.yml:72`, `purpose.md:25` |
