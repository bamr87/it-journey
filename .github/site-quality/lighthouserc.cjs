// =============================================================================
// lighthouserc.cjs — Lighthouse CI budgets for it-journey.dev (PR gate)
// -----------------------------------------------------------------------------
// Run by .github/workflows/site-quality.yml against the locally built _site
// (the same `_config.yml,_config_dev.yml,_config_ci.yml` build as the
// build-validation PR job), served by serve-site.mjs (gzip + GitHub Pages-style
// URLs) on 127.0.0.1:4000. Mobile (Lighthouse's default form factor + simulated
// 4G/CPU throttling), 3 runs per URL, every assertion on the MEDIAN of the 3.
//
// Levels — read this before tightening:
//   * Category scores (a11y / best-practices / SEO >= 0.95) and the must-pass
//     audits are 'error' on every page where they ALREADY pass, so the gate is
//     green on arrival and blocks regressions. Where a page doesn't pass yet the
//     override below says so, as 'warn' with a TODO(error) naming the fix.
//   * Performance, Web-Vitals metrics and resource-size budgets start at 'warn'
//     (eager Mermaid/Cytoscape, render-blocking CSS + Google Fonts @import, large
//     hero images). Flip them to 'error' as each fix lands.
//   * Cache-policy audits are OFF: GitHub Pages always sends max-age=600.
// Sizes are transfer bytes (gzip), KiB * 1024.
// =============================================================================
const BASE = process.env.SITE_URL || 'http://127.0.0.1:4000';
const KiB = 1024;

const PAGES = {
  home: '/',
  quests: '/quests/',
  helloNoob: '/quests/0000/hello-noob/', // diagram-heavy (Mermaid) quest page
};

// 'median' (not 'median-run'): LHCI applies median-run to audits but not to
// category scores, which silently fall back to the best run.
const median = { aggregationMethod: 'median' };
const min = (level, minScore) => [level, { ...median, minScore }];
const max = (level, maxNumericValue) => [level, { ...median, maxNumericValue }];

const base = {
  // --- categories ----------------------------------------------------------
  'categories:accessibility': min('error', 0.95),
  'categories:best-practices': min('error', 0.95),
  'categories:seo': min('error', 0.95),
  // TODO(error): after Mermaid/Cytoscape lazy-load + the CSS/font fixes.
  'categories:performance': min('warn', 0.7),

  // --- metrics (mobile, simulated) — TODO(error) after the perf fixes -------
  'largest-contentful-paint': max('warn', 4000),
  'first-contentful-paint': max('warn', 2000),
  'cumulative-layout-shift': max('warn', 0.1),
  'total-blocking-time': max('warn', 300),

  // --- must-pass audits ----------------------------------------------------
  'errors-in-console': min('error', 1),
  'unsized-images': min('error', 1),
  label: min('error', 1),
  'button-name': min('error', 1),
  'link-name': min('error', 1),

  // --- size budgets (transfer bytes) — warn; TODO(error) per line as each
  // passes (purged CSS, subset icon font, resized hero images). --------------
  'resource-summary:stylesheet:size': max('warn', 60 * KiB),
  'resource-summary:font:size': max('warn', 160 * KiB),
  'resource-summary:image:size': max('warn', 300 * KiB),
  'resource-summary:script:size': max('warn', 250 * KiB),
  'resource-summary:third-party:size': max('warn', 150 * KiB),
  'resource-summary:total:size': max('warn', 1000 * KiB),

  // --- off: GitHub Pages cache headers are fixed (max-age=600) -------------
  'uses-long-cache-ttl': 'off',
  'cache-insight': 'off',
};

// Per-page exceptions to `base`. Every 'warn' that would otherwise be 'error'
// carries a TODO(error) naming the fix that lets it go back to 'error'.
const overrides = {
  home: {
    // TODO(error): index.html hard-codes 8 preview *.png files that only exist
    // as .webp -> 404s in the console (it-journey fix PR).
    'errors-in-console': min('warn', 1),
  },
  quests: {
    'total-blocking-time': max('warn', 600), // quest pages: 600 ms budget
    // TODO(error): 0.90 today. The theme intro's Share button and Edit link are
    // icon-only on mobile (button-name / link-name) — zer0-mistakes intro.html fix.
    'categories:accessibility': min('warn', 0.95),
    'button-name': min('warn', 1),
    'link-name': min('warn', 1),
  },
  helloNoob: {
    // Diagram-heavy quest page: lower perf bar, 600 ms TBT, and a temporary
    // script budget until Mermaid is lazy-loaded or pre-rendered (then 250 KiB).
    'categories:performance': min('warn', 0.6),
    'total-blocking-time': max('warn', 600),
    'resource-summary:script:size': max('warn', 1200 * KiB),
    // TODO(error): 0.87 today — the label fix (it-journey) + the intro
    // button/link names (theme) bring it back over 0.95.
    'categories:accessibility': min('warn', 0.95),
    // TODO(error): 29 unlabelled quest-objective checkboxes (it-journey fix).
    label: min('warn', 1),
    // TODO(error): icon-only Share button / Edit link on mobile (theme fix).
    'button-name': min('warn', 1),
    'link-name': min('warn', 1),
    // TODO(error): content screenshots (github-fork-it-journey.webp,
    // github-login.webp) have no width/height (it-journey fix).
    'unsized-images': min('warn', 1),
    // TODO(error): hero background resolves to /assetsimages/previews/... (404)
    // because front matter `preview:` has no leading slash (it-journey fix).
    'errors-in-console': min('warn', 1),
  },
};

const escape = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

module.exports = {
  ci: {
    collect: {
      url: Object.values(PAGES).map((p) => BASE + p),
      numberOfRuns: 3,
      settings: {
        formFactor: 'mobile', // Lighthouse default; `preset` only offers desktop/perf/experimental
        throttlingMethod: 'simulate',
        skipAudits: ['uses-long-cache-ttl', 'cache-insight'],
        chromeFlags: '--no-sandbox',
      },
    },
    assert: {
      assertMatrix: Object.entries(PAGES).map(([key, path]) => ({
        matchingUrlPattern: `^${escape(BASE + path)}$`,
        assertions: { ...base, ...overrides[key] },
      })),
    },
    upload: {
      target: 'filesystem',
      outputDir: 'reports/lighthouse',
    },
  },
};
