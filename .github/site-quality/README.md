# Site quality checks (Lighthouse CI + axe + pa11y)

Run on every PR to `main` that touches the site by [`site-quality.yml`](../workflows/site-quality.yml). The workflow builds `_site` with the same config as the `build-validation.yml` PR build (`_config.yml,_config_dev.yml,_config_ci.yml`), serves it on `127.0.0.1:4000` and checks it. Nothing here touches the live site, and nothing needs a secret.

| File | What it does |
|---|---|
| `serve-site.mjs` | Zero-dependency static server for `_site` that behaves like GitHub Pages: gzip, `/dir/` → `index.html`, `/dir` → 301, `404.html` with HTTP 404, `cache-control: max-age=600`. Without gzip the transfer-size budgets would be meaningless. |
| `lighthouserc.cjs` | Lighthouse CI: `/`, `/quests/`, `/quests/0000/hello-noob/`, mobile, 3 runs, assertions on the median. Category, Web Vitals, must-pass audit and resource-size assertions, with per-page overrides. |
| `a11y-check.mjs` | axe-core 4.13 through Playwright (the runner's Google Chrome) on the pages in `a11y.config.mjs`, at 390 px and 1366 px. |
| `contrast-check.mjs` | pa11y (HTML_CodeSniffer, WCAG2AA) keeping only the WCAG 1.4.3 contrast results, because axe reports most text on this theme as "incomplete". |
| `a11y.config.mjs` | Pages, viewports, the known-issue list for axe, and the per-page contrast limits. |
| `lhci-summary.mjs` | Writes the Lighthouse table and every failed assertion to the job summary. |

## What fails a PR and what only warns

- **Lighthouse, `error`:** accessibility, best-practices and SEO ≥ 0.95, plus the must-pass audits `errors-in-console`, `unsized-images`, `label`, `button-name` and `link-name`, on every page where they already pass on `main`.
- **Lighthouse, `warn`:** performance (≥ 0.70, or ≥ 0.60 on the diagram-heavy hello-noob quest), LCP ≤ 4.0 s, FCP ≤ 2.0 s, CLS ≤ 0.1, TBT ≤ 300 ms (≤ 600 ms on quest pages), and the size budgets (CSS ≤ 60 KiB, fonts ≤ 160 KiB, images ≤ 300 KiB, scripts ≤ 250 KiB with 1200 KiB on hello-noob until Mermaid is lazy-loaded, third-party ≤ 150 KiB, total ≤ 1000 KiB). The page-specific `warn` overrides for assertions that don't pass yet each carry a `TODO(error)` that names the fix.
- **Lighthouse, `off`:** `uses-long-cache-ttl` and `cache-insight`. GitHub Pages always sends `max-age=600`, and that can't be changed.
- **axe, fail:** any `critical` or `serious` violation of a `wcag2a`/`wcag2aa`/`wcag21a`/`wcag21aa` rule.
- **axe, warn:** WCAG 2.2 rules (`target-size`), plus the entries in `known` in `a11y.config.mjs`. Each entry is limited to one rule, the listed pages and viewports, and the nodes that match its regex, so a new violation under the same rule still fails.
- **Contrast:** a page with `max` fails when it has more contrast failures than that number. Pages that are clean today are pinned at `max: 0`. `/search/` is report-only until the badge colours are fixed.

## Tightening

When a fix lands, delete its `known` entry or its `warn` override, or add `max: 0`, in the same PR as the fix. The axe job prints a notice when a `known` entry stops reproducing. Run the checks locally against a build:

```bash
bundle exec jekyll build --config _config.yml,_config_dev.yml,_config_ci.yml
cd .github/site-quality && PUPPETEER_SKIP_DOWNLOAD=1 PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
node serve-site.mjs ../../_site 4000 &
npx lhci autorun --config=lighthouserc.cjs   # Lighthouse collect + assert
node a11y-check.mjs && node contrast-check.mjs
```

The scripts use the installed Google Chrome. Set `CHROME_PATH` for pa11y, or `PW_CHANNEL=` to use Playwright's own Chromium (`npx playwright install chromium`).
