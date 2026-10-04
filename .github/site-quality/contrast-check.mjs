#!/usr/bin/env node
// =============================================================================
// contrast-check.mjs — pa11y (HTML_CodeSniffer, WCAG2AA) colour-contrast check
// -----------------------------------------------------------------------------
// axe returns "incomplete" for most text on this theme (layered/gradient
// backgrounds), so it can't gate contrast. HTML_CodeSniffer does compute it;
// this keeps ONLY its WCAG 1.4.3 contrast results (G18 / G145) for the pages in
// a11y.config.mjs `contrast.pages`. Gradient hero headings are hidden first
// (`contrast.hideElements`) — htmlcs compares against the flat fallback colour
// there and reports false 1:1 failures.
//
// Gating: a page FAILS only when it has a `max` in a11y.config.mjs and its count
// exceeds it. Pages without `max` are report-only (warning annotation).
// Writes reports/a11y/contrast-results.json + contrast-summary.md and appends to
// $GITHUB_STEP_SUMMARY. Env: SITE_URL, CHROME_PATH (default /usr/bin/google-chrome).
// =============================================================================
import pa11y from 'pa11y';
import { mkdirSync, writeFileSync, appendFileSync, existsSync } from 'node:fs';
import config from './a11y.config.mjs';

const BASE = (process.env.SITE_URL || 'http://127.0.0.1:4000').replace(/\/$/, '');
const OUT = 'reports/a11y';
mkdirSync(OUT, { recursive: true });
const executablePath = process.env.CHROME_PATH || ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium']
  .find((p) => existsSync(p));
const CONTRAST = /Guideline1_4\.1_4_3\.(G18|G145)/;
const { pages, hideElements, viewport = { width: 1366, height: 768 } } = config.contrast;

const gh = (level, title, msg) => console.log(`::${level} title=${title}::${msg.replace(/\r?\n/g, '%0A')}`);
const results = [];
for (const { path, max } of pages) {
  let issues = [];
  let error;
  try {
    const r = await pa11y(BASE + path, {
      standard: 'WCAG2AA',
      runners: ['htmlcs'],
      includeWarnings: false,
      includeNotices: false,
      hideElements,
      viewport,
      timeout: 120_000,
      chromeLaunchConfig: { executablePath, args: ['--no-sandbox'] },
    });
    issues = r.issues.filter((i) => CONTRAST.test(i.code));
  } catch (e) {
    error = e.message;
  }
  // Group by selector "shape" (strip :nth-child) so 600 identical badges read as one line.
  const groups = {};
  for (const i of issues) {
    // e.g. "a.badge.bg-primary @ 1.45:1" — element + classes from the snippet, and the measured ratio.
    const tag = (i.context || '').match(/^<([a-z0-9-]+)/i)?.[1] || i.selector.split(' > ').pop().replace(/:nth-child\(\d+\)/g, '');
    const cls = ((i.context || '').match(/class="([^"]*)"/)?.[1] || '').trim().split(/\s+/).filter(Boolean).slice(0, 3).map((c) => '.' + c).join('');
    const ratio = i.message.match(/contrast ratio of ([\d.]+:1)\./)?.[1] || '?';
    const key = `${tag}${cls} @ ${ratio}`;
    groups[key] = (groups[key] || 0) + 1;
  }
  const top = Object.entries(groups).sort((a, b) => b[1] - a[1]).slice(0, 5);
  const failed = !!error || (typeof max === 'number' && issues.length > max);
  results.push({ path, count: issues.length, max: max ?? null, failed, error, top, issues });
}

const md = [
  '## 🎨 pa11y colour contrast (WCAG 2 AA 1.4.3, HTML_CodeSniffer)',
  '',
  '| Page | Contrast failures | Gate | Most common |',
  '|---|---|---|---|',
  ...results.map((r) => `| ${r.path} | ${r.error ? 'error' : r.count} | ${r.error ? '❌ ' + r.error : typeof r.max === 'number' ? (r.failed ? `❌ > ${r.max}` : `✅ ≤ ${r.max}`) : '⚠️ report-only'} | ${r.top.map(([k, n]) => `${n}× \`${k}\``).join('<br>') || '—'} |`),
  '',
  `_Hidden before checking (gradient hero headings — false positives): \`${hideElements}\`_`,
  '',
].join('\n');
writeFileSync(`${OUT}/contrast-results.json`, JSON.stringify(results, null, 2));
writeFileSync(`${OUT}/contrast-summary.md`, md);
if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, md + '\n');
console.log(md);
for (const r of results) {
  if (r.failed) gh('error', `contrast ${r.path}`, r.error || `${r.count} contrast failures (max ${r.max})`);
  else if (r.count) gh('warning', `contrast ${r.path}`, `${r.count} contrast failure(s), report-only for now — ${r.top[0]?.[0] || ''}`);
}
process.exit(results.some((r) => r.failed) ? 1 : 0);
