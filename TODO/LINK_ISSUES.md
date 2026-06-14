---
title: "Link Issues Summary"
description: "Quick reference summary of broken links across IT-Journey"
created: 2026-01-17T00:00:00.000Z
lastmod: 2026-06-13T00:00:00.000Z
status: "ISSUES_FOUND"
priority: "HIGH"
date: 2026-06-13T00:00:00.000Z

---

# Link Issues Summary

> Quick reference for link health status. See [TODO/links/](./links/) for detailed tracking.

---

## Current Status

| Metric | Value |
|--------|-------|
| **Last Scan** | 2026-06-13 |
| **Total Links** | 100+ relative .md checked (this iteration) |
| **Broken Links** | 15 (relative .md) + 4 external |
| **Success Rate** | — see notes |

> **Note (2026-06-13):** A large batch of broken relative `.md` links was fixed this iteration. 15 broken relative `.md` links remain across 5 files NOT edited this round — 9 of which are intentional template/code-fence placeholders (won't fix), leaving 6 actionable in `docs/scripts/CLEANUP_SUMMARY.md` and `docs/testing/TESTING_FRAMEWORKS.md`. Plus 4 external broken URLs from the 2026-03-07 lychee scan (link-check-results/). See [TODO/links/reports/scan-2026-06-13.md](./links/reports/scan-2026-06-13.md) and [TODO/CONTENT_WORKLIST-2026-06-13.md](./CONTENT_WORKLIST-2026-06-13.md).

---

## Quick Actions

Run a link scan to populate this summary:

```bash
python3 scripts/validation/link-checker.py --scope website
```

Or trigger via GitHub Actions:
1. Go to [Actions > Link Health Guardian](../.github/workflows/link-checker.yml)
2. Click "Run workflow"
3. Select scope and run

---

## Issue Categories

| Category | Count | Priority | Action |
|----------|-------|----------|--------|
| Internal broken .md (actionable) | 6 | Critical | Fix navigation |
| Internal broken .md (placeholders) | 9 | n/a | Won't fix (templates/examples) |
| External Broken | 4 | High | Update references |
| SSL Errors | 0 | Medium | Review certificates |
| Timeouts | 0 | Medium | Check slow sites |
| Rate Limited | 0 | Low | Usually false positives |

---

## Top Issues (2026-06-13)

1. `docs/scripts/CLEANUP_SUMMARY.md` — 4 broken script README links (also an obsolete doc; archiving resolves these).
2. `docs/testing/TESTING_FRAMEWORKS.md` — 2 dead `test/hyperlink-guardian/docs/*` links (tool moved to scripts/validation/).
3. `docs/CONTRIBUTING_DEVELOPER.md` — external placeholder URL `YOUR-USERNAME/it-journey.git`.
4. `docs/architecture/{JEKYLL_IMPLEMENTATION,REPOSITORY_STRUCTURE}.md` — broken external `bamr87/zer0-mistakes` (502).
5. `docs/workflows/ORGANIZE_POSTS_WORKFLOW.md` — placeholder `actions/runs/12345678` link.
6. Won't fix: `docs/standards/CONTENT_GUIDELINES.md` (code-fence examples), `.github/instructions/README.instructions.md` (template), `test/quest-solutions/_shared/templates/quest-solution-readme-template.md` (template).

---

## Detailed Reports

- **[Quick Actions](./links/QUICK_ACTIONS.md)** - Prioritized fix tasks
- **[Tracking](./links/TRACKING.md)** - Progress over time
- **[Data](./links/data/link-report.json)** - Machine-readable results

---

## Fix Workflow

1. **Scan**: Run link checker
2. **Review**: Check QUICK_ACTIONS.md for prioritized issues
3. **Fix**: Address critical internal links first
4. **Verify**: Re-run scan to confirm fixes
5. **Track**: Update TRACKING.md with progress

---

**Project**: [Link Health Management](./links/README.md)  
**Last Updated**: 2026-06-13
