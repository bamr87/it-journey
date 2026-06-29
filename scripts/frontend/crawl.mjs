#!/usr/bin/env node
/**
 * crawl.mjs — deterministic frontend crawler / tester for it-journey.dev.
 *
 * Drives a real headless browser over the configured routes at mobile + desktop
 * viewports and records UI/UX/a11y/theme problems to .frontend/findings.jsonl:
 *   - page-status / navigation-error — the route itself 4xx/5xx or failed to load
 *   - http-error — a sub-resource / link returned >= 400 (this is how the theme-
 *     injected-link 404s — /authors/, /tags/, /search.json, /sitemap/ — surface)
 *   - console-error — a JS error on the page (often a theme bundle)
 *   - horizontal-overflow — the page scrolls sideways (a mobile theme/layout bug)
 *   - img-missing-alt — an <img> with no alt text (a11y)
 *   - a11y — axe-core WCAG 2 A/AA violations (desktop pass)
 *
 * READ-ONLY: it never logs in, submits a form, or mutates anything; it only reads
 * the public site. The deterministic triager (triage_findings.py) classifies each
 * finding as theme vs content and dedups; the theme-scout agent files the theme
 * ones upstream. Exit 0 always (a collector, not a gate) unless it cannot start.
 *
 * Usage: BASE_URL=https://it-journey.dev node scripts/frontend/crawl.mjs
 * Deps (install in CI, --no-save): playwright @axe-core/playwright js-yaml
 */
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import yaml from 'js-yaml';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createHash } from 'node:crypto';

const CONFIG = '.frontend/config.yml';
const OUT = '.frontend/findings.jsonl';

const sig = (...p) => createHash('sha1').update(p.join('|')).digest('hex').slice(0, 12);

let cfg = {};
try { cfg = yaml.load(readFileSync(CONFIG, 'utf8')) || {}; }
catch (e) { console.error(`could not read ${CONFIG}: ${e}`); }

const baseUrl = (process.env.BASE_URL || cfg.base_url || 'https://it-journey.dev').replace(/\/+$/, '');
const routes = (cfg.routes && cfg.routes.length) ? cfg.routes : ['/'];
const viewports = (cfg.viewports && cfg.viewports.length) ? cfg.viewports
  : [{ name: 'mobile', width: 390, height: 844 }, { name: 'desktop', width: 1280, height: 900 }];

const findings = [];
const linkPaths = new Set();   // same-origin <a href> paths gathered across pages
const MAX_LINKS = 150;         // cap the active broken-link check
// Fingerprint is route-INDEPENDENT (kind + rule + normalized detail) so the same
// site-wide defect on many routes collapses to one signature the triager can
// recognize as "theme" (recurs everywhere).
const record = (f) => {
  const norm = (f.detail || '').replace(/\d+/g, '#');
  findings.push({ signature: sig(f.kind, f.rule || '', norm), ...f });
};

const browser = await chromium.launch();
try {
  for (const vp of viewports) {
    const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    for (const route of routes) {
      const url = baseUrl + route;
      const page = await context.newPage();
      const consoleErrors = [];
      const failed = [];
      page.on('console', (m) => { if (m.type() === 'error') consoleErrors.push(m.text()); });
      page.on('pageerror', (e) => consoleErrors.push(String(e)));
      page.on('response', (r) => { if (r.status() >= 400) failed.push({ url: r.url(), status: r.status() }); });

      let loaded = true;
      try {
        const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
        if (resp && resp.status() >= 400) {
          record({ route, viewport: vp.name, kind: 'page-status', severity: 'high', detail: `${route} returned HTTP ${resp.status()}` });
          loaded = false;
        }
      } catch (e) {
        record({ route, viewport: vp.name, kind: 'navigation-error', severity: 'high', detail: `${route}: ${String(e).slice(0, 200)}` });
        loaded = false;
      }

      if (loaded) {
        for (const fr of failed) {
          const path = fr.url.startsWith(baseUrl) ? fr.url.slice(baseUrl.length) : fr.url;
          record({ route, viewport: vp.name, kind: 'http-error', severity: fr.status >= 500 ? 'high' : 'medium', detail: `${fr.status} ${path}` });
        }
        for (const ce of [...new Set(consoleErrors)]) {
          record({ route, viewport: vp.name, kind: 'console-error', severity: 'medium', detail: ce.slice(0, 300) });
        }
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
        if (overflow > 4) {
          record({ route, viewport: vp.name, kind: 'horizontal-overflow', severity: vp.name === 'mobile' ? 'high' : 'low', detail: `horizontal overflow ${overflow}px at viewport ${vp.width}px` });
        }
        const noAlt = await page.evaluate(() =>
          Array.from(document.images).filter((i) => !i.alt || !i.alt.trim()).map((i) => i.currentSrc || i.src).slice(0, 10));
        for (const src of noAlt) {
          record({ route, viewport: vp.name, kind: 'img-missing-alt', severity: 'low', detail: `<img> missing alt: ${src.startsWith(baseUrl) ? src.slice(baseUrl.length) : src}` });
        }
        // Collect same-origin links to broken-link-check after the crawl. Theme
        // chrome (nav/footer/sidebar) emits hrefs like /tags/, /authors/ that
        // only 404 when followed — passive response monitoring never sees them.
        const hrefs = await page.evaluate((origin) =>
          Array.from(document.querySelectorAll('a[href]'))
            .map((a) => a.href)
            .filter((h) => h.startsWith(origin))
            .map((h) => { try { return new URL(h).pathname; } catch { return null; } })
            .filter(Boolean), baseUrl);
        for (const h of hrefs) linkPaths.add(h);
        if (vp.name === 'desktop') {
          try {
            const { violations } = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
            for (const v of violations) {
              record({ route, viewport: vp.name, kind: 'a11y', rule: v.id, severity: v.impact || 'minor', detail: `${v.id}: ${v.help} (${v.nodes.length} node(s))`, help_url: v.helpUrl });
            }
          } catch { /* axe is best-effort */ }
        }
      }
      await page.close();
    }
    await context.close();
  }

  // Active broken-link check — catches theme-injected 404 hrefs (/tags/,
  // /authors/, …) that are only fetched when followed, so passive response
  // monitoring above never sees them. One request context, deduped + capped.
  const linkCtx = await browser.newContext();
  let checked = 0;
  for (const path of linkPaths) {
    if (checked >= MAX_LINKS) break;
    checked++;
    try {
      const r = await linkCtx.request.get(baseUrl + path, { maxRedirects: 5, timeout: 15000 });
      if (r.status() >= 400) {
        record({ route: 'site-wide (linked)', viewport: 'all', kind: 'http-error', severity: r.status() >= 500 ? 'high' : 'medium', detail: `${r.status()} ${path}` });
      }
    } catch (e) {
      record({ route: 'site-wide (linked)', viewport: 'all', kind: 'http-error', severity: 'medium', detail: `link error ${path}: ${String(e).slice(0, 80)}` });
    }
  }
  await linkCtx.close();
  if (linkPaths.size > MAX_LINKS) console.log(`(checked ${MAX_LINKS}/${linkPaths.size} unique links)`);
} finally {
  await browser.close();
}

mkdirSync('.frontend', { recursive: true });
writeFileSync(OUT, findings.map((f) => JSON.stringify(f)).join('\n') + (findings.length ? '\n' : ''));
console.log(`crawl: ${findings.length} finding(s) across ${routes.length} route(s) × ${viewports.length} viewport(s) -> ${OUT}`);
