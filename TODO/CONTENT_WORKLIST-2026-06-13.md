---
title: "Content Cleanup Worklist - 2026-06-13"
description: "Prioritized, deduplicated queue for the next content-cleanup iteration (broken links, stubs, obsolete docs, duplicates, images)."
created: 2026-06-13
lastmod: 2026-06-13
status: "ACTIVE"
priority: "HIGH"
---

# Content Cleanup Worklist - 2026-06-13

Prioritized queue derived from this iteration's audit + link-fix results. Sorted: broken links -> incomplete/stub -> obsolete -> redundant/duplicate -> other (images/links). Confidence is high/medium/low. Items flagged **won't fix** are intentional placeholders.

---

## 1. Broken links remaining / unresolved

Actionable remaining broken relative .md links (6) plus 4 external broken URLs. (See TODO/links/reports/scan-2026-06-13.md.)

| Path | Action | Confidence |
|------|--------|-----------|
| docs/scripts/CLEANUP_SUMMARY.md | Fix/remove 4 broken script README links (`../scripts/README.md`, `core/`, `development/`, `legacy/`) — the doc itself is also obsolete; archiving it (see Obsolete) resolves these. | high |
| docs/testing/TESTING_FRAMEWORKS.md | Repoint or remove 2 dead `../../test/hyperlink-guardian/docs/{setup,usage}.md` links; real tool is scripts/validation/link-checker.py. | high |
| docs/CONTRIBUTING_DEVELOPER.md | Replace placeholder external URL `https://github.com/YOUR-USERNAME/it-journey.git` with the real repo URL. | high |
| docs/architecture/JEKYLL_IMPLEMENTATION.md, docs/architecture/REPOSITORY_STRUCTURE.md | Fix/remove broken external `https://github.com/bamr87/zer0-mistakes` (502). | high |
| docs/workflows/ORGANIZE_POSTS_WORKFLOW.md | Replace placeholder `.../actions/runs/12345678` link with a real run or remove it. | medium |
| docs/standards/CONTENT_GUIDELINES.md (4 links) | **won't fix** — illustrative links inside ```markdown code fences (teaching syntax). | n/a |
| .github/instructions/README.instructions.md (3 links: ../README.md, ../sibling/README.md x2) | **won't fix** — template skeleton placeholders. | n/a |
| test/quest-solutions/_shared/templates/quest-solution-readme-template.md (answer-key.md, reports/report-name.md) | **won't fix** — template placeholders authors fill per-quest. | n/a |
| pages/_quickstart/machine-setup.md `./advanced-jekyll.md` | RESOLVED this iteration (hyperlink removed, text kept). No target exists; create an "Advanced Jekyll" page if desired. | low |

---

## 2. Incomplete / stub content

### Published-but-empty (highest priority — render as blank live pages)

| Path | Action | Confidence |
|------|--------|-----------|
| pages/_posts/data-analytics/2024-05-01-doc-scraper.md | ✅ **DONE (2026-06-13)** — authored a full post (HTML→Markdown Python scraper) from the html_md_doc_scrapper.md note; links to the note for the full notebook. | high |
| pages/_posts/trends-ideas/2024-05-09-bootstrap-your-theme-and-character.md | ✅ **DONE (2026-06-13)** — set draft: true (no source material; reflective/personal piece left for the author to write). | high |

### Near-empty stubs / placeholders

| Path | Action | Confidence |
|------|--------|-----------|
| pages/_notes/code-snippets/test.md | ⏸️ **KEEP** — its own frontmatter states it's an intentional `draft: true` fixture ("kept as a draft so it does not surface in published indexes"); not published, no inbound refs. Left in place per its stated intent. | n/a |
| pages/_notes/Journal Entries/Github_s hidden gem.md | ✅ **DONE (2026-06-13)** — set draft: true (unpublished). Broken Joplin import (leaked frontmatter in body, no content); title duplicated the real github-pages-hidden-gem post. File kept for the author. | high |
| pages/_notes/Journal Entries/What is my PiDentity_.md | ✅ **DONE (2026-06-13)** — set draft: true (unpublished). Empty contact form that also published the author's lat/long; no inbound refs. | high |
| pages/_notes/dev/Curiculum.md | Expand or delete (one aphorism line; filename also misspelled). | high |
| pages/_drafts/2025-11-16-sharex.md | Expand into a full ShareX walkthrough or delete (fragment). | high |
| pages/_notes/zero/Start.md | ✅ **DONE (2026-06-13)** — set draft: true (unpublished; tagged 'test', half-empty scratch sheet). | high |
| pages/_notes/dev/Take good notes.md | Expand or delete; remove `&nbsp;` filler regardless. | medium |
| pages/_notes/dev/projects/Master_s Project.md | Expand the skeleton category list or delete. | medium |
| pages/_notes/dev/projects/Project List.md | Expand or delete; remove trailing empty `- [ ]` bullet. | medium |
| pages/_drafts/2024-05-16-dynamic-sidebar-tree.md | Rewrite (raw Copilot transcript) into a guide or delete; remove the FIXME frontmatter key. | medium |

### Empty / orphaned sections (heading followed by nothing)

| Path | Action | Confidence |
|------|--------|-----------|
| pages/_posts/web-development/2025-11-16-jekyll-and-travis.md | ✅ **DONE (2026-06-13)** — removed the empty trailing `## References` heading. | high |
| pages/_quests/0000/linux-fundamentals.md | ✅ **DONE (2026-06-13)** — removed the empty orphan `## Resources` heading (populated `## 📚 References & Resources` remains). | high |
| pages/_notes/index.md | ⚠️ **PARTIAL (2026-06-13)** — converted the visible body `TODO:` to a non-rendering HTML comment. Empty `### Linux` / `### Autoscale images` subsections LEFT (look like deliberate parallel-OS placeholders; fill or remove in a later pass). | medium |
| pages/_posts/data-analytics/2025-03-13-excel-gurus-are-the-most-valuable-programmers.md | Investigate empty `## Parody Version` divider; merge/demote following H2. | medium |
| pages/_quests/2025-11-29-prd-codex-mastering-product-reality-distillation.md | Convert empty `### Progression Points: +150 XP` label-heading to bold text. | low |
| pages/_quests/templates/README.md | Verify excluded from Jekyll rendering; add frontmatter only if meant to be published. | medium |

---

## 3. Obsolete content (stale status / superseded docs)

> **Reprioritized (2026-06-13):** `_config.yml` `exclude:` (L440) lists `TODO/`, `docs/`, `scripts/`, `test/` — so every item below is **build-excluded / internal repo housekeeping, NOT a published page**. Archiving/deleting them is pure repo tidiness with zero user-facing impact, and moving them risks re-breaking the repo-internal links fixed in iteration 1. Lower priority than user-facing content. When doing it, map the cross-reference web first and prefer deleting genuinely-empty/fabricated artifacts over archiving clutter.

| Path | Action | Confidence |
|------|--------|-----------|
| docs/scripts/CLEANUP_SUMMARY.md | Archive or correct — documents a nonexistent scripts/legacy/ dir and sibling-repo consolidation; layout has diverged. | high |
| docs/scripts/CONSOLIDATION_PLAN.md | Archive to docs/archive/ — completed/superseded plan referencing nonexistent legacy/ + sibling repos. | medium |
| docs/workflows/DEPENDENCY_UPDATE_SUMMARY.md | Update/archive — references nonexistent hyperlink-guardian.yml and stale pinned versions (Gemfile now unpinned). | high |
| docs/architecture/REPOSITORY_STRUCTURE.md | Update — replace scripts/hyperlink-guardian/ refs with scripts/validation/; fix broken zer0-mistakes link. | high |
| TODO/STATUS.md | Refresh or archive to TODO/ARCHIVE/ — frozen Dec-2025 SEO dashboard ~6 months overdue. | high |
| TODO/links/data/link-report.json | Update/delete — falsely claims 0 broken / 100%; superseded by link-check-results/ (4 broken). | high |
| TODO/links/TRACKING.md | Refresh with real numbers or merge into link-check-results/ — false 0-broken narrative. | high |
| TODO/links/reports/scan-2026-01-16.md | Archive as historical snapshot (claims 0 broken; superseded). | medium |
| TODO/links/README.md | Reconcile hub status with actual scan data; consider consolidating TODO/links/ into link-check-results/. | medium |
| TODO/seo/MONITORING_DASHBOARD.md | Archive to TODO/ARCHIVE/ — empty placeholder tables, fabricated baselines, never populated. | medium |
| TODO/seo/TRACKING.md | Mark status: paused/completed or archive — dormant since Dec 2025, no data entered. | medium |
| TODO/seo/reports/weekly-review-2025-12-20.md | Delete — empty template never filled in. | medium |
| TODO/seo/data/seo-metrics.json | Replace with real GSC export if resuming, else delete — fabricated placeholder numbers. | medium |
| TODO/seo/data/freshness-report.json | Delete — superseded by 2026-05 frontmatter remediation; regenerate on demand. | medium |
| TODO/seo/reports/content-freshness-2025-12-20.md | Delete — superseded freshness snapshot. | medium |
| RESOLUTION_REPORT.md (repo root) | Archive to docs/archive/ or delete — closed-PR artifact, no durable value. | medium |
| TODO/ARCHIVE/README.md | Keep but use it — move dormant SEO + link-tracking projects here. Low priority. | low |

---

## 4. Redundant / duplicate content

| Path | Action | Confidence |
|------|--------|-----------|
| pages/_notes/misc/cloud.md | ✅ **DONE (2026-06-13)** — deleted; byte-identical duplicate of AWS Practice Question Set.md (0 real inbound refs). | high |
| pages/_notes/cheetsheets/Windows Powershell Cheatsheet.md | ✅ **DONE (2026-06-13)** — deleted; byte-identical to 2022-10-07-powershell.md. | high |
| pages/_drafts/2025-11-16-desktop-widgets-windows.md | ✅ **DONE (2026-06-13)** — deleted; duplicate of published 2022-06-10-desktop-widgets-windows.md. | high |
| pages/_drafts/2025-11-16-raspberry-pi.md | ✅ **DONE (2026-06-13)** — deleted; duplicate stub of 2024-03-10-raspberry-pi-5-case-build.md (remaining stub flagged in Incomplete). | high |
| pages/_notes/2025-01-16-mastering-iterm-shortcuts-for-efficiency.md | ✅ **DONE (2026-06-13)** — deleted; iterm-tips-and-tricks.md (superset, has image) kept (0 inbound refs). | high |
| pages/_notes/cheetsheets/Shell and the CLI.md | ✅ **DONE (2026-06-13)** — deleted; command-line.md kept (its gh-fork example is the richer one, nothing to fold in). | high |
| pages/_posts/web-development/README.md | ⏸️ **DEFERRED** — redundant with dynamic 2000-01-01-index.md, but it's a live page (permalink /posts/web-development/) and its links were fixed this round. Decide whether to drop /posts/&lt;category&gt;/ pages before deleting. | high |
| docs/CONTRIBUTING_DEVELOPER.md vs pages/_docs/contributing/contributing-developer.md | Consolidate to single source — keep fuller pages/ version; stub/redirect docs/ copy (widely referenced). | medium |
| pages/_posts/data-analytics/2024-05-01-doc-scraper.md vs pages/_notes/html_md_doc_scrapper.md | Resolve via the empty-post action in Incomplete (build post from note or delete stub). | medium |

---

## 5. Other (images, {% link %}, absolute links)

| Path / scope | Action | Confidence |
|------|--------|-----------|
| ~~175 `preview:` frontmatter values~~ | ✅ **DONE (2026-06-13)** — normalized 175 preview paths (with existing target images) to canonical `/assets/images/previews/X.png`. NOTE: the theme's `preview-image.html` auto-prepends `/assets` but mishandles **bare** paths (`images/...` → `/assetsimages/...`), so the canonical full path is the only universally-correct form (works in cards AND og:image). 49 paths skipped because their target image does not exist — see next rows (need generation). | high |
| 7 GH-600 agentic-codex posts (pages/_posts/2026-05-17-*.md) + pages/news.md | Generate missing hero/preview PNGs into /assets/images/previews/ then fix prefix — currently broken hero images on /news/. | high |
| 13 category index posts (pages/_posts/*/2000-01-01-index.md) | Generate/assign category preview PNGs under /assets/images/previews/ and fix prefix, or point to a site default. | high |
| ~28 quest `preview:` values (pages/_quests/1000..1100, 0111) + level READMEs | Generate missing agentic-*/level-* preview PNGs into /assets/images/previews/ and fix prefix. | high |
| ~~Inline `../assets/...` images~~ | ✅ **DONE (2026-06-13)** — fence-aware rewrite of **33 inline image refs → `/assets/...`** across 5 files (penrose & chatgpt-triangle posts, _notes/index.md, bash-cheatsheet, sonic-pi draft). Skipped 1 code-fence example (notes/index.md "Gallery") and the 3 krita-config*.png refs whose target image is genuinely missing (krita draft — needs the image). Fence-aware scan now reports **0** real broken inline refs. | high |
| Individual missing previews (el-capitan, github-pages-hero, work-cicd, working-directory, planting-seeds, prd-codex, phase-6) | Create images (and assets/images/posts/ dir for el-capitan) or repoint to existing assets. | high |
| pages/_posts/devops/2025-11-17-deploying-jekyll-sites-to-azure-cloud.md, pages/_quests/codex/world_map.md | ✅ **DONE (2026-06-13)** — verified dead via live site (it-journey.dev): `dockering-your-it-journey` & `ai-powered-development-workflows` both 404. Repointed dockering → `/posts/docker-beginners-tutorial/` (200); removed the ai-powered bullet (no equivalent). In world_map also fixed `/about/theme/`→`/quickstart/theme-architecture/`, `/categories/`→`/posts/`, `/progress/`→`/notes/` (all verified 200). All other world_map `/quests/...` links verified valid via explicit permalinks. | high |
| pages/_docs/wargames/index.md:84, pages/_docs/index.md:92 | ✅ **DONE (2026-06-13)** — replaced `/it-journey/scripts/docs-aggregator/...` (hardcoded baseurl, raw paths) with GitHub blob/tree URLs on `main`. Also fixed a stray `blob/master`→`blob/main` in pages/posts.md (default branch is main). | high |
| ~~_layouts/news.html (preview-image.html include)~~ | ✅ **RESOLVED — not a bug.** `components/preview-image.html` and `components/post-type-badge.html` are provided by the **theme** (`remote_theme: bamr87/zer0-mistakes` in prod, `jekyll-theme-zer0` gem in dev), merged into `_includes` at build. Do not recreate them locally. | medium |
| docs/standards/CONTENT_GUIDELINES.md, TODO/seo/BEST_PRACTICES.md (diagram/dashboard/docker-architecture.png) | Mostly doc examples (keep). Annotate BEST_PRACTICES docker-architecture.png as a placeholder or add the image. | low |

---

## 6. Privacy / metadata (new — found 2026-06-13)

| Path / scope | Action | Confidence |
|------|--------|-----------|
| ~9 published notes under pages/_notes/** carrying `latitude:`/`longitude:`/`altitude:` in frontmatter (Joplin imports, e.g. 39.5480789, -104.9739333) | Review whether the author wants real geo-coordinates published. If not, strip `latitude`/`longitude`/`altitude` from those notes' frontmatter (mechanical). Two of the worst (empty form + scratch sheet) were unpublished this iteration; the rest remain published. | medium |

---

## 7. Dead absolute internal links — comprehensive sweep (2026-06-13)

Method: collected all `](/...)` links across content, subtracted the explicit-`permalink:` set, then live-verified each against https://it-journey.dev. Result: **26 OK · 57 "repo-exists-but-live-404" (NOT broken — just not-yet-deployed, DO NOT touch) · 43 truly dead** (no repo file + live 404).

✅ **Home page (root index.md) — DONE (2026-06-13):** fixed ~14 dead links — remapped old `/quests/init_world/*` & `/quests/lvl_001/*` to current `/quests/0000/*` & `/quests/0001/*` permalinks; `backend`/`devops` CTAs → `/quests/home/`; `/community/`→GitHub Discussions, `/resources/`→`/docs/`, `/about/profile/`→`/quests/home/`. Verified 0 broken absolute links remain on the home page.

Remaining truly-dead (queued):

| Source | Dead links | Action |
|--------|-----------|--------|
| roadmap.md (root, published /roadmap/) | Full live-check: **44 dead of 94 absolute links.** ✅ **9 FIXED (2026-06-13, iter 7):** renamed-content remaps (about/theme→/quickstart/theme-architecture/, hello-linux→linux-fundamentals, vscode-mastery-quest→vscode-mastery, bash-run→0000/side-quests/bash-run, 0001/personal-site→0001/side-quests/personal-site, codex/world_map→codex/world-map, 2024-04-02-dockering→docker-beginners-tutorial) + 2 category landings (/posts/devops/→/news/devops/, /posts/ai…→/news/ai-machine-learning/). | high (done) |
| roadmap.md — REMAINING ~35 (BUILD-GATED) | `/posts/tags/{ai,architecture,devops,frontend,performance,system-admin,web-dev}/` (8); `/notebooks/*.html` + `/notebooks/`(6); `/posts/ai%20&%20machine%20learning/<slug>/`(4); `/posts/devops/<slug>/` & `/posts/<date>-<slug>/` derived-post URLs(5); unbuilt/renamed quests `/quests/0010/jekyll-mermaid-integration-quest/`, `/quests/0011/{github-hidden-gem-code-search-quest,prompt-crystal-mastery-vscode-copilot-quest}/` (likely just drop the `-quest` suffix — files exist), `/quests/0001/terminal-illness/`, `/quests/0010/nerd-font-enchantment-side-quest/`; `/posts/2022-07-01-angular-tour-of-heros/` (draft DELETED → unlink); `/security/`,`/code-of-conduct/`,`/zer0/` (root files not published as pages). | **Needs a local Jekyll build** to resolve correctly — live-site verification is UNRELIABLE here (the deployed site lags the repo: `/tags/`, `/archives/`, `/notebooks/` all 404 live despite being theme/collection features). Don't guess; build then fix, or unlink the truly-unbuilt ones. |
| pages/_quickstart/{content-creation,site-configuration,cicd-automation,optimization-maintenance,local-development,jekyll-setup,github-setup}.md (published) | `/docs/<NAME>/` (DEVELOPMENT_ENVIRONMENT, INSTALLATION_UPDATE, CONTENT_GUIDELINES, FRONTMATTER_STANDARDS, SCRIPTS_GUIDE, GITHUB_ACTIONS, TESTING_FRAMEWORKS, REPOSITORY_STRUCTURE) | These target the **build-excluded** root `docs/` dir (not published). Decide: publish those docs into `pages/_docs/`, OR repoint to GitHub blob URLs, OR remove. Architectural. |
| pages/_docs/jekyll/jekyll-config.md | `/docs/configuration/incremental-regeneration/` | Should be external `https://jekyllrb.com/docs/configuration/incremental-regeneration/`. Quick fix. |
| pages/_docs/contributing/contributing-developer.md | `/docs/setup/development-environment/` | Repoint to a published doc or GitHub blob. |
| pages/_about/features/index.md | `/quests/ai-powered-learning/` | No such quest — repoint to a real 1000-level agentic/AI quest or remove. |
| pages/_posts/devops/2025-12-20-docker-beginners-tutorial.md | `/quests/0100/frontend-docker-lvl-000/` | Repoint to the real frontend-docker quest permalink or remove. |
| pages/_posts/ai-machine-learning/2025-11-26-mastering-prompt-engineering-vscode-copilot.md | `/quests/ai-assisted-development/` | No such quest — repoint or remove. |
| pages/_posts/tools-environment/2025-12-20-essential-vscode-extensions-developers.md, pages/_docs/terminal/terminal-shortcuts-cheat-sheet.md | `/quests/level-0000-vscode-mastery-quest/` | Repoint to `/quests/0000/vscode-mastery/`. |
| pages/_notes/html_md_doc_scrapper.md (+ _notebooks copy) | 6× `/docs/5.3/...` | Low priority — scraped Bootstrap-docs sample content; prefix with `https://getbootstrap.com` or leave as a scraping-demo artifact. |

---

## Not flagged (intentional / genuinely distinct — do not action)

- OverTheWire wargame walkthroughs (one-per-level, intentional).
- 2019 Django-on-AWS-Lambda drafts (distinct multi-part series).
- Two working-directory posts (general filesystem vs work/ CI-CD pattern).
- Two mermaid docs (usage guide vs migration note).
- gh-600 note vs docs sets (quick-ref/exam-overview vs study-hub/skills-breakdown).
- docs/archive/link-health-2025/* (correctly archived historical content).
- 3 already-deleted drafts (secs-edgar-database, angular-tour-of-heros, dual-boot-win-linux) — zero remaining references.
