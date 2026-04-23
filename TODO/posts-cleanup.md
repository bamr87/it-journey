---
title: "Posts Mass-Cleanup Tracker"
description: "Live tracker for the chore/posts-mass-cleanup branch — baselines, decisions, and per-phase checklist."
date: 2026-04-22
lastmod: 2026-04-22
status: "in-progress"
branch: "chore/posts-mass-cleanup"
---

# Posts Mass-Cleanup Tracker

Branch: `chore/posts-mass-cleanup`. Plan saved in `/memories/session/plan.md`.
All scratch reports live under `work/posts-cleanup/` (gitignored).

## Phase 0 — Baseline (✅ done)

| Metric | Value | Source |
|--------|-------|--------|
| Total `.md` files in `pages/_posts/**` | **125** | `work/posts-cleanup/baseline/inventory.txt` |
| Files at root (excl. index) | **17** real + 1 index = 18 | inventory |
| Folders with `&` in name | **6** | `ai & machine learning`, `culture & society`, `creative & experimental`, `data & analytics`, `tools & environment`, `trends & ideas` |
| Folders with spaces only | **3** | `system administration`, `web development` (+ counted above) |
| Filenames with apostrophe | **2** | `2024-04-13-sec's-edgar-database.md`, `2024-06-18-aquaaid's-devastating-desert-mission.md` |
| Frontmatter validity | **73 valid / 51 invalid** (58.9 %) | `work/posts-cleanup/baseline/frontmatter.json` |
| Frontmatter errors / warnings | **102 / 168** | same |
| Avg SEO score | **54.5 / 100** | same |
| Lychee link check (posts only) | 340 links: 172 ok, 42 errors, 61 redirects, 16 files w/ errors | `work/posts-cleanup/baseline/links/lychee.json` |
| Real external 404 / 403 / timeout | 11 / 3 / 2 | same |
| Lychee local-path "errors" (Jekyll absolute paths) | 26 — *not real failures*, lychee can't resolve `/quests/...` without site base URL | same |
| Content freshness | 19 fresh, 18 stale, 87 critical (>90 d), avg age **431 d** | `work/posts-cleanup/baseline/freshness.md` |
| `organize-posts.sh --dry-run` | would auto-move **11** root files, **5** skipped (no `section:`), **1** target conflict | `work/posts-cleanup/baseline/organize-dryrun.log` |
| Jekyll build baseline | ⏳ pending — bundle install running in `it-journey-jekyll-run-*` | `work/posts-cleanup/baseline/build.log` (when ready) |

### Duplicate resolution (verified byte-identical via diff)

| Keep | Delete | Reason |
|------|--------|--------|
| `pages/_posts/creative & experimental/2024-06-18-aquaaids-devastating-desert-mission.md` | `pages/_posts/2024-06-18-aquaaid's-devastating-desert-mission.md` | identical bytes; root copy has problem char `'` |
| `pages/_posts/creative & experimental/2025-11-16-sonic-pi.md` | `pages/_posts/2022-01-09-sonic-pi.md` | identical bytes; older filename is misleading (lastmod=2022 but content & section newer) |
| `pages/_posts/data & analytics/2024-03-11-gpt-cv-analysis.md` | `pages/_posts/2024-03-11-cv-analysis.md` | identical bytes; categorized version wins |

### Decisions (chosen defaults — flag if any need to change)

1. **Drafts** (`draft: true` posts) → move to `pages/_drafts/` (excluded from build).
2. **Frontmatter strictness** → 8 required (`title, description, date, categories, tags, author, layout, lastmod`); rest recommended only.
3. **Folder rename `& ` → kebab-case** (e.g. `ai & machine learning/` → `ai-machine-learning/`) → **YES**, with `redirect_from:` for affected URLs.
4. **AI content review (Phase 6)** → defer to a follow-up branch.

### ⚠️ Phase 1 risks surfaced by `organize-posts.sh` dry-run

- The script renames files based on **frontmatter title** (e.g. `2024-03-10-raspberry-pi-5-case-build.md` → `2024-03-10-raspberry-pi.md`). That **loses information** in the URL slug.
  - Mitigation: tighten the title for those posts in Phase 2 *before* running organize-posts, OR pass a flag to keep original filename. Need to read the script logic.
- 5 root posts have **no `section:` frontmatter** and will be skipped by the auto-organizer:
  - `2025-11-22-flow.md`
  - `2025-11-17-deploying-jekyll-sites-to-azure-cloud.md`
  - `2025-11-20-using-crush-vscode-github-pages.md`
  - `2025-11-26-mastering-prompt-engineering-vscode-copilot.md`
  - `2026-04-19-ai-assisted-nanobar-footer-refactoring.md`
  - Action: add `section:` in Phase 2 (suggested mappings in checklist below).
- The `posts_organization.yml` "Valid sections" list includes ~50 aliases (incl. generic words like `tech`, `setup`, `tutorial`) — too permissive. Tighten in Phase 2.

## Phase 1 — Filename & structural normalization (⏳ next, awaiting confirmation)

- [ ] Delete 3 verified-duplicate root files (`git rm`).
- [ ] Manually assign `section:` to 5 root posts that auto-organizer can't classify.
- [ ] `git mv` rename: 6 `&`-folders → kebab-case; update `_data/posts_organization.yml` `directory:` values; add permalink `redirect_from:` for old URLs.
- [ ] `git mv` rename: 2 space-only folders (`system administration`, `web development`) → kebab-case; same redirect treatment.
- [ ] Decide per-post: accept `organize-posts.sh` slug renames or keep originals (suggest keeping originals; modify the script's slug generation to fall back to the existing filename slug).
- [ ] Run `organize-posts.sh` (real) to move remaining root posts into category folders.
- [ ] Re-run inventory to confirm 0 root posts remain (besides index).

## Phase 2 — Frontmatter normalization (depends on Phase 1)

- [ ] Author/layout/lastmod auto-fill via extended `frontmatter-validator.py --fix` (or a small wrapper).
- [ ] Generate `excerpt:` from first paragraph for posts missing it.
- [ ] Add `section:` to the 5 unclassified root posts.
- [ ] Drop empty `tags: []`, empty `meta:`, empty `attachments:`.
- [ ] Move `draft: true` posts to `pages/_drafts/`.
- [ ] Re-run validator; target **0 errors**, ≤ 50 warnings.

## Phase 3 — Content lint & body cleanup

- [ ] `markdownlint "pages/_posts/**/*.md" --fix`
- [ ] Strip invisible chars / smart quotes (small new helper if no existing tool found).
- [ ] `jekyll doctor` clean.

## Phase 4 — Link repair

- [ ] Configure lychee with proper base URL so `/quests/...` absolute paths resolve.
- [ ] Address real external 404/403/timeout (16 files affected).
- [ ] Update `link-check-results/broken_links_baseline.json`.

## Phase 5 — Preview images & SEO

- [ ] List posts missing `preview:`.
- [ ] Generate via `scripts/generation/generate-preview-images.sh` (needs `OPENAI_API_KEY`).

## Phase 7 — CI hardening

- [ ] `frontmatter-validation.yml` → required check on `pages/_posts/**`, fail on errors.
- [ ] Add `markdownlint` step to `build-validation.yml`.
- [ ] `organize-posts-weekly.yml` → open PRs not direct commits (verify).
- [ ] Author `pages/_posts/README.md` documenting standards.

## Phase 8 — Verify & merge

- [ ] All validators clean; build = 0 new warnings vs baseline.
- [ ] Smoke-test 5 renamed-post URLs locally on Jekyll.
- [ ] Open PR with before/after table.
