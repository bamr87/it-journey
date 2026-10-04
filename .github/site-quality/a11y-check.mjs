#!/usr/bin/env node
// =============================================================================
// a11y-check.mjs — axe-core (via Playwright) over the key pages, two viewports
// -----------------------------------------------------------------------------
// FAILS on any critical/serious violation of a WCAG 2.0/2.1 A/AA rule.
// WARNS (never fails, for now) on WCAG 2.2 rules — target-size in practice.
// Known, already-tracked violations listed in a11y.config.mjs `known` are
// reported as warnings instead of failures, but ONLY for the rule + page (+
// optional viewport / node selector) listed, so anything new still fails.
// A known entry that stops reproducing is called out so it can be deleted.
//
// Writes reports/a11y/axe-results.json + reports/a11y/axe-summary.md, appends
// the summary to $GITHUB_STEP_SUMMARY, and emits ::error/::warning annotations.
// Env: SITE_URL (default http://127.0.0.1:4000), PW_CHANNEL (default 'chrome' =
// the runner's installed Google Chrome; set PW_CHANNEL= to use Playwright's own).
// =============================================================================
import { chromium } from 'playwright';
import { AxeBuilder } from '@axe-core/playwright';
import { mkdirSync, writeFileSync, appendFileSync } from 'node:fs';
import config from './a11y.config.mjs';

const BASE = (process.env.SITE_URL || 'http://127.0.0.1:4000').replace(/\/$/, '');
const OUT = 'reports/a11y';
const { blockingTags, blockingImpacts, warnTags, known = [] } = config.axe;
mkdirSync(OUT, { recursive: true });

const gh = (level, title, msg) =>
  console.log(`::${level} title=${title.replace(/[:,\n]/g, ' ')}::${msg.replace(/\r?\n/g, '%0A')}`);
const nodeText = (n) => `${[].concat(n.target).flat().join(' ')} ${n.html || ''}`;

function knownEntry(v, page, viewport, node) {
  return known.find((k) =>
    k.rule === v.id &&
    (k.pages.includes('*') || k.pages.includes(page)) &&
    (!k.viewports || k.viewports.includes(viewport)) &&
    (!k.nodes || new RegExp(k.nodes).test(nodeText(node))));
}

const channel = process.env.PW_CHANNEL ?? 'chrome';
const browser = await chromium.launch({ channel: channel || undefined, args: ['--no-sandbox'] });
const results = [];
const knownSeen = new Set();

for (const vp of config.viewports) {
  const context = await browser.newContext({
    viewport: { width: vp.width, height: vp.height },
    isMobile: !!vp.mobile,
    hasTouch: !!vp.mobile,
    deviceScaleFactor: vp.mobile ? 3 : 1,
    reducedMotion: 'reduce',
  });
  for (const page of config.pages) {
    const tab = await context.newPage();
    const url = BASE + page;
    let resp;
    try {
      resp = await tab.goto(url, { waitUntil: 'load', timeout: 60_000 });
      await tab.waitForLoadState('networkidle', { timeout: 10_000 }).catch(() => {});
    } catch (e) {
      results.push({ page, viewport: vp.name, error: `navigation failed: ${e.message}` });
      await tab.close();
      continue;
    }
    if (!resp || resp.status() >= 400) {
      results.push({ page, viewport: vp.name, error: `HTTP ${resp ? resp.status() : 'no response'}` });
      await tab.close();
      continue;
    }
    const axe = await new AxeBuilder({ page: tab }).withTags([...blockingTags, ...warnTags]).analyze();
    for (const v of axe.violations) {
      const isBlockingRule = v.tags.some((t) => blockingTags.includes(t)) && blockingImpacts.includes(v.impact);
      const isWcag22 = !v.tags.some((t) => blockingTags.includes(t)) && v.tags.some((t) => warnTags.includes(t));
      const buckets = { fail: [], known: [], warn: [], info: [] };
      for (const n of v.nodes) {
        if (isBlockingRule) {
          const k = knownEntry(v, page, vp.name, n);
          if (k) { knownSeen.add(known.indexOf(k)); buckets.known.push({ n, k }); } else buckets.fail.push({ n });
        } else if (isWcag22) buckets.warn.push({ n });
        else buckets.info.push({ n });
      }
      for (const [level, items] of Object.entries(buckets)) {
        if (!items.length) continue;
        results.push({
          page, viewport: vp.name, level, rule: v.id, impact: v.impact, help: v.help, helpUrl: v.helpUrl,
          tags: v.tags.filter((t) => /^wcag/.test(t)), count: items.length,
          todo: items[0].k?.todo, examples: items.slice(0, 3).map(({ n }) => [].concat(n.target).flat().join(' ')),
        });
      }
    }
    await tab.close();
  }
  await context.close();
}
await browser.close();

// ---- report ------------------------------------------------------------------
const by = (lvl) => results.filter((r) => r.level === lvl);
const errors = results.filter((r) => r.error);
const fails = by('fail');
const row = (r) => `| \`${r.rule}\` | ${r.impact} | ${r.page} | ${r.viewport} | ${r.count} | ${r.todo || r.help} |`;
const table = (rows) => rows.length
  ? ['| Rule | Impact | Page | Viewport | Nodes | Note |', '|---|---|---|---|---|---|', ...rows.map(row)].join('\n')
  : '_none_';
const stale = known.filter((_, i) => !knownSeen.has(i));

const md = [
  '## ♿ axe-core (WCAG 2.0/2.1 A/AA; 2.2 as warning)',
  '',
  `${config.pages.length} pages × ${config.viewports.map((v) => `${v.width}px`).join(' + ')} · axe ${'4.13'} · ` +
    `**${fails.length ? '❌ FAIL' : '✅ PASS'}** — ${fails.length} blocking, ${by('known').length} known (warning), ` +
    `${by('warn').length} WCAG 2.2 warning, ${by('info').length} moderate/minor note(s)`,
  '',
  '### ❌ Blocking (critical/serious, WCAG 2.0/2.1 A/AA)', table(fails), '',
  '### ⚠️ Known issues — temporarily warnings (see TODO)', table(by('known')), '',
  '### ⚠️ WCAG 2.2 (warning only for now)', table(by('warn')), '',
  '### ℹ️ Moderate/minor WCAG violations (not gating)', table(by('info')), '',
  ...(errors.length ? ['### ❌ Pages that failed to load', ...errors.map((e) => `- ${e.page} (${e.viewport}): ${e.error}`), ''] : []),
  ...(stale.length ? ['### 🧹 Known entries that no longer reproduce — delete them from a11y.config.mjs so the rule gates again',
    ...stale.map((k) => `- \`${k.rule}\` on ${k.pages.join(', ')}${k.viewports ? ` (${k.viewports.join(', ')})` : ''}`), ''] : []),
].join('\n');

writeFileSync(`${OUT}/axe-results.json`, JSON.stringify(results, null, 2));
writeFileSync(`${OUT}/axe-summary.md`, md);
if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, md + '\n');
console.log(md);

for (const r of fails) gh('error', `axe ${r.rule} (${r.impact})`, `${r.page} @ ${r.viewport}: ${r.count} node(s) — ${r.help}. e.g. ${r.examples[0]}`);
for (const r of by('known')) gh('warning', `axe ${r.rule} (known)`, `${r.page} @ ${r.viewport}: ${r.count} node(s) — ${r.todo}`);
for (const r of by('warn')) gh('warning', `axe ${r.rule} (WCAG 2.2)`, `${r.page} @ ${r.viewport}: ${r.count} node(s) — ${r.help}`);
for (const e of errors) gh('error', 'axe page load', `${e.page} @ ${e.viewport}: ${e.error}`);
for (const k of stale) gh('notice', `axe ${k.rule} fixed?`, `known issue on ${k.pages.join(', ')} no longer reproduces — remove it from a11y.config.mjs`);

process.exit(fails.length || errors.length ? 1 : 0);
