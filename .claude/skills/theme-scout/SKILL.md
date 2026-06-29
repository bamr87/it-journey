---
name: theme-scout
description: Run ONE pass of the IT-Journey frontend canary — crawl it-journey.dev for UI/UX/a11y/theme defects, classify theme-vs-content, dedup, and file the theme issues upstream to bamr87/zer0-mistakes. Use when asked to test the it-journey.dev frontend, scout for theme bugs, run the frontend canary, or file theme issues upstream. Drives the theme-scout agent.
---

# Theme Scout — one frontend-canary pass

it-journey.dev runs the `bamr87/zer0-mistakes` theme via `remote_theme`, so it is
a live canary for the theme. One pass: **test the frontend → classify findings →
dedup → file the theme ones upstream**. Deterministic spine, AI judgment at the
filing step. Runs identically locally (`/loop` / `make`) and in CI
(`theme-scout.yml`).

## 0. Read the policy

- `.frontend/config.yml` — routes, viewports, the theme-vs-content classification
  rules, the upstream repo, and the per-run cap.
- `.frontend/README.md` — the contract and how to run it.

## 1. Test the frontend (deterministic)

```bash
BASE_URL=https://it-journey.dev node scripts/frontend/crawl.mjs
```

The crawler drives a real browser over every configured route at mobile + desktop
and writes `.frontend/findings.jsonl`: page/HTTP errors (incl. the theme-injected
link 404s), console errors, mobile horizontal overflow, missing alt text, and
axe-core WCAG violations. It is read-only — it never logs in or submits anything.

## 2. Classify + dedup (deterministic)

```bash
python3 scripts/frontend/triage_findings.py
```

Groups findings by signature, decides which are **theme** (site-wide / theme-
injected) vs **content** (one page), dedups against existing upstream issues, and
writes `.frontend/upstream-candidates.json` (capped).

## 3. File theme issues upstream (the theme-scout agent)

The **theme-scout** agent reads the candidates, makes the final theme-vs-content
call, searches upstream once more to avoid paraphrased duplicates, and files each
genuine theme bug with `gh issue create --repo bamr87/zer0-mistakes` (title +
repro/evidence + `bug` + `area:*` labels). Filing upstream needs a PAT with
issues:write on the theme repo (the workflow provides it as `THEME_REPO_TOKEN`).

## 4. Safety rules (every pass)

- **Only theme issues go upstream.** Content/site-specific findings stay in
  it-journey (report them; don't file upstream). When unsure, don't file.
- **Dedup before every create** — never reopen a known open/closed upstream issue.
- **Respect the cap** (`dedup.max_new_issues_per_run`).
- **Honesty** — every issue claim comes from the crawler's real evidence.
- **Read-only on both repos otherwise** — never fix code, open PRs, or merge.

## 5. Report honestly

State what you filed (URLs), what you skipped as duplicates, and what you judged
content (for it-journey to handle). Never imply you found everything — this is one
bounded canary pass over a sample of routes.
