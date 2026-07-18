# IT-Journey Theme Scout — the `.frontend/` frontend canary

it-journey.dev runs the **`bamr87/zer0-mistakes`** theme via `remote_theme`, so it is a live canary for the theme. This directory drives a routine that **tests the it-journey.dev frontend** and **files theme bugs upstream** to zer0-mistakes — deterministic spine, AI judgment only at the filing step.

```
.frontend/config.yml            # routes, viewports, theme-vs-content rules, upstream repo (hand-edited)
.frontend/findings.jsonl        # generated, NOT committed — raw crawler findings
.frontend/upstream-candidates.json  # generated, NOT committed — the deduped theme shortlist
scripts/frontend/crawl.mjs       # the browser tester (Playwright + axe-core)
scripts/frontend/triage_findings.py  # classify theme-vs-content + dedup
```

## The loop (mirrors lifehacker.dev's site-explorer → theme-scout)

1. **Test** — `crawl.mjs` drives a real headless browser over every configured
route at mobile + desktop and records: page/HTTP errors (incl. theme-injected link 404s — `/authors/`, `/tags/`, `/search.json`, `/sitemap/`), console errors, mobile horizontal overflow, missing `alt` text, and axe-core WCAG 2 A/AA violations. Read-only — it never logs in or submits anything.
2. **Triage** — `triage_findings.py` groups findings by a route-independent
signature, classifies each as **theme** (site-wide / theme-injected → belongs upstream) vs **content** (one page → stays in it-journey), and dedups against existing zer0-mistakes issues → `upstream-candidates.json` (capped).
3. **File** — the **`theme-scout`** agent makes the final theme-vs-content call,
dedups once more, and files the genuine theme bugs upstream with `gh issue create --repo bamr87/zer0-mistakes`. Only theme issues; never content.

The scheduled routine is `.github/workflows/theme-scout.yml` (weekly + dispatch).

## Why "theme vs content" matters

A 404 on `/tags/` or a nav a11y violation appears on **every** page because the theme injects it — that's a theme bug every remote-theme consumer hits, so it goes upstream. A dead link in one quest, or one page's missing alt text, is **content** — it stays in it-journey (the content fleet / CMS handles it). The triager is conservative: when it isn't confident a finding is theme-wide, it keeps it local.

## Run it locally

```bash
make theme-crawl     # BASE_URL=https://it-journey.dev node scripts/frontend/crawl.mjs
make theme-triage    # classify + dedup -> .frontend/upstream-candidates.json
```

Needs Node 20 + `npm install --no-save playwright @axe-core/playwright js-yaml` and `npx playwright install chromium`, plus Python 3.12 + PyYAML and an authenticated `gh`. (CI installs all of this.)

## Turn it on (OFF by default)

1. `gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo bamr87/it-journey`
2. **Cross-repo PAT** — a token with `issues:write` on bamr87/zer0-mistakes:
`gh secret set THEME_REPO_TOKEN --repo bamr87/it-journey`. Without it, the crawl + triage still run and the candidates are uploaded as a workflow artifact for manual filing — nothing is filed automatically.
3. `gh variable set THEME_SCOUT_ENABLED --body true --repo bamr87/it-journey`

Tune the routes, viewports, classification rules, and the per-run cap (`dedup.max_new_issues_per_run`) in `config.yml`.
