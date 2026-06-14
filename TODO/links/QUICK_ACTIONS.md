---
title: "Link Health Quick Actions"
description: "Prioritized broken link fixes"
lastmod: 2026-06-13T00:00:00.000Z
status: "ISSUES_FOUND"
date: 2026-06-13T00:00:00.000Z

---

# Link Health Quick Actions

> **Last Scan**: 2026-06-13
> **Total Issues**: 15 broken relative .md (6 actionable, 9 won't-fix) + 4 external
> **Success Rate**: see TODO/links/reports/scan-2026-06-13.md

---

## Critical - Internal broken .md links (6 actionable)

- `docs/scripts/CLEANUP_SUMMARY.md` — 4 broken script README links (`../scripts/README.md`, `../scripts/core/README.md`, `../scripts/development/README.md`, `../scripts/legacy/README.md`). Doc is also obsolete; archiving resolves these.
- `docs/testing/TESTING_FRAMEWORKS.md` — 2 dead links to `test/hyperlink-guardian/docs/{setup,usage}.md` (tool moved to scripts/validation/link-checker.py).

### Won't fix (intentional placeholders — 9)

- `docs/standards/CONTENT_GUIDELINES.md` (4) — illustrative links inside ```markdown code fences.
- `.github/instructions/README.instructions.md` (3) — README template skeleton placeholders.
- `test/quest-solutions/_shared/templates/quest-solution-readme-template.md` (2) — per-quest template placeholders.

---

## High Priority - External Broken (4 issues)

- `https://github.com/YOUR-USERNAME/it-journey.git` — docs/CONTRIBUTING_DEVELOPER.md (replace with real repo URL).
- `https://github.com/bamr87/zer0-mistakes` — docs/architecture/JEKYLL_IMPLEMENTATION.md, REPOSITORY_STRUCTURE.md (502).
- `https://github.com/bamr87/it-journey/actions/runs/12345678` — docs/workflows/ORGANIZE_POSTS_WORKFLOW.md (placeholder).

---

## Medium - SSL/Timeouts (0 issues)

## Low - Rate Limited (0 false positives)

---

**Last Updated**: 2026-06-13
