---
title: "Link Health Management"
description: "Central hub for tracking and resolving broken links across the IT-Journey platform"
created: 2026-01-17T00:00:00.000Z
lastmod: 2026-01-17T00:00:00.000Z
status: "ACTIVE"
priority: "HIGH"
category: "technical"
owner: "IT-Journey Team"
estimated_effort: "Ongoing"
expected_impact: "Improved user experience, better SEO, reduced 404 errors"
tags:
  - todo
  - links
  - maintenance
  - quality
---

# Link Health Management

> **Mission**: Maintain link integrity across all IT-Journey content to ensure seamless navigation and optimal user experience.

## Quick Status

| Metric | Value | Status |
|--------|-------|--------|
| **Total Links Scanned** | - | Pending scan |
| **Broken Links** | - | Pending scan |
| **Success Rate** | - | Pending scan |
| **Last Scan** | Never | - |

---

## Directory Structure

```
TODO/links/
├── README.md              # This file - Central hub
├── QUICK_ACTIONS.md       # Prioritized fix tasks
├── TRACKING.md            # Progress tracking
├── data/
│   └── link-report.json   # Machine-readable scan results
└── reports/
    └── scan-YYYY-MM-DD.md # Historical scan reports
```

---

## Key Files

| File | Purpose | Update Frequency |
|------|---------|-----------------|
| [QUICK_ACTIONS.md](./QUICK_ACTIONS.md) | Immediate fix tasks by priority | After each scan |
| [TRACKING.md](./TRACKING.md) | Progress on link fixes | Weekly |
| [data/link-report.json](./data/link-report.json) | Raw scan data for automation | After each scan |

---

## Link Categories

### By Error Type

| Category | Description | Priority |
|----------|-------------|----------|
| **Internal 404s** | Missing pages on it-journey.dev | Critical |
| **External Broken** | Third-party links that no longer work | High |
| **Rate Limited** | Links blocked during scanning (false positives) | Low |
| **Timeouts** | Slow external sites | Medium |
| **SSL/Certificate** | Security-related link issues | High |

### By Content Area

| Area | Path | Typical Issues |
|------|------|----------------|
| **Quests** | `pages/_quests/` | Internal navigation, resource links |
| **Posts** | `pages/_posts/` | External references, outdated tutorials |
| **Docs** | `pages/_docs/` | API links, tool documentation |
| **About** | `pages/_about/` | Social links, contact pages |

---

## Workflow

### Automated Scanning

The link checker runs automatically:
- **Scheduled**: Every Monday at 6 AM UTC
- **Manual**: Via GitHub Actions workflow dispatch

### Fix Process

1. Review [QUICK_ACTIONS.md](./QUICK_ACTIONS.md) for prioritized tasks
2. Fix critical internal links first
3. Update or remove broken external references
4. Mark completed items in tracking
5. Re-run scan to verify fixes

---

## Running the Link Checker

### Local Scan

```bash
# Full website scan
python3 scripts/validation/link-checker.py --scope website

# Scan specific content
python3 scripts/validation/link-checker.py --scope posts
python3 scripts/validation/link-checker.py --scope quests

# Quick scan with timeout
python3 scripts/validation/link-checker.py --scope website --timeout 15
```

### GitHub Actions

1. Go to [Actions > Link Health Guardian](../../actions/workflows/link-checker.yml)
2. Click "Run workflow"
3. Select scope and options
4. Review results in artifacts and this directory

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Success Rate | >95% | - |
| Internal 404s | 0 | - |
| Response Time | <48h for critical | - |

---

## Related Resources

- [TODO Hub](../README.md) - Central TODO directory
- [STATUS Dashboard](../STATUS.md) - Overall project status
- [Link Checker Workflow](../../.github/workflows/link-checker.yml) - Automation config
- [Link Checker Script](../../scripts/validation/link-checker.py) - Scan tool

---

**Project Owner**: IT-Journey Team  
**Created**: 2026-01-17  
**Last Updated**: 2026-01-17  
**Status**: Active
