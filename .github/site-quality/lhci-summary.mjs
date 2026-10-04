#!/usr/bin/env node
// lhci-summary.mjs — render the Lighthouse CI run as a Markdown table (median
// run per URL: scores, Web Vitals, transfer sizes) plus every failed/warned
// assertion, and append it to $GITHUB_STEP_SUMMARY. Reads .lighthouseci/
// (lhr-*.json from `lhci collect`, assertion-results.json from `lhci assert`,
// links.json from `lhci upload --target=temporary-public-storage`).
import { readdirSync, readFileSync, existsSync, appendFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createRequire } from 'node:module';

// Same "representative (median) run" pick that `median-run` assertions use.
const { computeRepresentativeRuns } = createRequire(import.meta.url)('@lhci/utils/src/representative-runs.js');

const DIR = '.lighthouseci';
const read = (f) => JSON.parse(readFileSync(`${DIR}/${f}`, 'utf8'));
const lhrs = existsSync(DIR) ? readdirSync(DIR).filter((f) => /^lhr-.*\.json$/.test(f)).sort().map(read) : [];
const assertions = existsSync(`${DIR}/assertion-results.json`) ? read('assertion-results.json') : [];
const links = existsSync(`${DIR}/links.json`) ? read('links.json') : {};

const byUrl = {};
for (const l of lhrs) (byUrl[l.finalDisplayedUrl || l.requestedUrl] ||= []).push(l);
const median = (runs) => computeRepresentativeRuns([runs.map((l) => [l, l])])[0];
const pct = (c) => (c?.score == null ? '—' : Math.round(c.score * 100));
const ms = (a) => (a?.numericValue == null ? '—' : `${(a.numericValue / 1000).toFixed(2)} s`);
const kib = (items, type) => {
  const i = items.find((x) => x.resourceType === type);
  return i ? `${Math.round(i.transferSize / 1024)}` : '—';
};

const rows = Object.entries(byUrl).map(([url, runs]) => {
  const l = median(runs);
  const items = l.audits['resource-summary']?.details?.items || [];
  const path = new URL(url).pathname;
  const report = links[url] ? ` [report](${links[url]})` : '';
  return `| ${path}${report} | ${pct(l.categories.performance)} | ${pct(l.categories.accessibility)} | ${pct(l.categories['best-practices'])} | ${pct(l.categories.seo)} | ${ms(l.audits['largest-contentful-paint'])} | ${ms(l.audits['first-contentful-paint'])} | ${l.audits['cumulative-layout-shift']?.numericValue?.toFixed(3) ?? '—'} | ${Math.round(l.audits['total-blocking-time']?.numericValue ?? 0)} ms | ${kib(items, 'stylesheet')} / ${kib(items, 'script')} / ${kib(items, 'font')} / ${kib(items, 'image')} / ${kib(items, 'third-party')} / ${kib(items, 'total')} |`;
});

const failed = assertions.filter((a) => !a.passed);
const arow = (a) => `| ${a.level === 'error' ? '❌ error' : '⚠️ warn'} | ${new URL(a.url).pathname} | \`${a.auditId}${a.auditProperty ? ':' + a.auditProperty : ''}\` | ${a.operator} ${a.expected} | ${typeof a.actual === 'number' ? +a.actual.toFixed(3) : a.actual} |`;
const errs = failed.filter((a) => a.level === 'error');
const md = [
  '## 🚦 Lighthouse CI (mobile, median of 3 runs, local `_site`)',
  '',
  `**${errs.length ? `❌ ${errs.length} error assertion(s) failed` : '✅ all error-level assertions pass'}** · ${failed.length - errs.length} warning(s)`,
  '',
  '| Page | Perf | A11y | BP | SEO | LCP | FCP | CLS | TBT | KiB css / js / font / img / 3p / total |',
  '|---|---|---|---|---|---|---|---|---|---|',
  ...rows,
  '',
  ...(failed.length ? ['| Level | Page | Assertion | Expected | Actual (median) |', '|---|---|---|---|---|', ...failed.sort((a, b) => (a.level > b.level ? 1 : -1)).map(arow), ''] : []),
  'Full HTML/JSON reports (every run): `reports/lighthouse/` in the `site-quality-reports` artifact' + (Object.keys(links).length ? ' and the temporary-public-storage links above (kept ~7 days).' : '.'),
  '',
].join('\n');
mkdirSync('reports', { recursive: true });
writeFileSync('reports/lighthouse-summary.md', md);
if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, md + '\n');
console.log(md);
