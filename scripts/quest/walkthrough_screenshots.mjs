#!/usr/bin/env node
/**
 * walkthrough_screenshots.mjs — capture visual evidence for a quest-walkthrough
 * session, saved as artifacts for review.
 *
 * For each quest in the planner's slice (walk-plan.json) it produces:
 *   pages/<slug>-mobile.png   — the rendered quest page at a ~390px mobile viewport
 *   pages/<slug>-desktop.png  — the rendered quest page at a 1440px desktop viewport
 *     (what a learner actually sees; driven off the quest permalink against a live
 *      site, default https://it-journey.dev — override with --base-url for a local
 *      server.)
 *   session/<slug>-terminal.png — a terminal-styled render of the SESSION transcript
 *     (the commands the walkthrough recorded for that quest + their pass/fail/
 *      skipped/reasoned outcome), read from the agentic execute engine's evidence
 *      JSON (walk-evidence.json). This is a faithful render of the recorded session
 *      transcript — NOT a raw TTY frame grab. (For Bashcrawl's TUI specifically,
 *      the game's own `--screenshot-dir` can capture true frames; if such PNGs are
 *      dropped into <out>/session/ before/after this runs they are kept alongside.)
 *
 * It is a COLLECTOR, not a gate: every capture is best-effort, per-quest failures
 * are recorded in <out>/manifest.json, and the process exits 0 unless the browser
 * itself cannot launch. Read-only over the site; never logs in or mutates anything.
 *
 * Usage:
 *   node scripts/quest/walkthrough_screenshots.mjs \
 *     --plan walk-plan.json [--evidence walk-evidence.json] \
 *     [--out screenshots] [--base-url https://it-journey.dev]
 *
 * Deps (install in CI, --no-save): playwright  (+ `npx playwright install chromium`).
 * Mirrors scripts/frontend/crawl.mjs so the two browser-driving tools stay aligned.
 */
import { chromium } from 'playwright';
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';

// ---- args -----------------------------------------------------------------
const args = process.argv.slice(2);
const opt = (name, dflt) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 && args[i + 1] ? args[i + 1] : dflt;
};
const PLAN = opt('plan', 'walk-plan.json');
const EVIDENCE = opt('evidence', 'walk-evidence.json');
const OUT = opt('out', 'screenshots');
const BASE_URL = (process.env.BASE_URL || opt('base-url', 'https://it-journey.dev'))
  .replace(/\/+$/, '');

const MOBILE = { width: 390, height: 844 };
const DESKTOP = { width: 1440, height: 900 };

// ---- load inputs ----------------------------------------------------------
let plan;
try {
  plan = JSON.parse(readFileSync(PLAN, 'utf8'));
} catch (e) {
  console.error(`❌ cannot read plan ${PLAN}: ${e.message}`);
  process.exit(2);
}
const quests = Array.isArray(plan.quests) ? plan.quests : [];
if (!quests.length) {
  console.error(`⚠️  plan ${PLAN} has no quests — nothing to screenshot.`);
  process.exit(0);
}

// Map evidence (the agentic execute engine's report) by quest slug, so we can
// render each quest's recorded command transcript. Tolerant of a missing file.
const evidenceBySlug = {};
try {
  const ev = JSON.parse(readFileSync(EVIDENCE, 'utf8'));
  for (const r of ev.results || []) {
    const slug = (r.quest && (r.quest.slug || basenameSlug(r.quest.path))) || '';
    if (slug) evidenceBySlug[slug] = r;
  }
} catch {
  console.error(`ℹ️  no readable evidence at ${EVIDENCE} — terminal captures will note "no recorded session".`);
}

function basenameSlug(p) {
  if (!p) return '';
  const base = p.split('/').pop() || '';
  return base.replace(/\.md$/, '');
}
function slugOf(q) {
  return basenameSlug(q.path) || (q.permalink || '').split('/').filter(Boolean).pop() || 'quest';
}
const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// ---- terminal transcript -> HTML ------------------------------------------
const STATUS = {
  passed:   { c: '#3fb950', m: '✓' },
  failed:   { c: '#f85149', m: '✗' },
  skipped:  { c: '#8b949e', m: '∅' },
  reasoned: { c: '#d29922', m: '~' },
};
function terminalHTML(quest, result) {
  const v = (result && result.verdict_obj) || {};
  const cmds = Array.isArray(v.commands) ? v.commands : [];
  const mode = (result && result.mode) || plan.modeHint || 'review';
  const score = result && typeof result.overall === 'number' ? `${result.overall.toFixed(0)}%` : '—';
  const verdict = (result && result.verdict) || '—';
  const rows = cmds.length
    ? cmds.map((c) => {
        const st = STATUS[c.status] || { c: '#c9d1d9', m: '·' };
        const detail = c.detail ? `<div class="detail">${esc(c.detail)}</div>` : '';
        return `<div class="line"><span class="prompt">$</span> <span class="cmd">${esc(c.command)}</span>`
             + ` <span class="st" style="color:${st.c}">${st.m} ${esc(c.status || '')}</span>${detail}</div>`;
      }).join('\n')
    : `<div class="line muted">— no recorded session transcript for this quest —</div>`;
  const summary = v.summary ? `<div class="summary">${esc(v.summary)}</div>` : '';
  return `<!doctype html><html><head><meta charset="utf-8"><style>
    :root { color-scheme: dark; }
    body { margin: 0; background: #0d1117; }
    .term { font: 14px/1.55 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
            color: #c9d1d9; padding: 20px 22px 26px; width: 900px; box-sizing: border-box; }
    .bar { display:flex; gap:7px; align-items:center; margin: -4px 0 14px; }
    .dot { width:12px; height:12px; border-radius:50%; }
    .title { margin-left: 10px; color:#8b949e; font-size:12px; }
    h1 { font-size: 15px; margin: 4px 0 2px; color:#58a6ff; }
    .meta { color:#8b949e; font-size:12px; margin-bottom: 14px; }
    .line { white-space: pre-wrap; word-break: break-word; margin: 2px 0; }
    .prompt { color:#3fb950; } .cmd { color:#e6edf3; } .st { font-size:12px; }
    .detail { color:#8b949e; font-size:12px; margin: 1px 0 6px 16px; }
    .muted { color:#6e7681; } .summary { margin-top: 16px; padding-top: 12px;
            border-top: 1px solid #21262d; color:#c9d1d9; font-size: 13px; }
  </style></head><body><div class="term">
    <div class="bar"><span class="dot" style="background:#f85149"></span>
      <span class="dot" style="background:#d29922"></span>
      <span class="dot" style="background:#3fb950"></span>
      <span class="title">quest-walkthrough session — ${esc(slugOf(quest))}</span></div>
    <h1>${esc(quest.title || slugOf(quest))}</h1>
    <div class="meta">level ${esc(quest.level || '')} · mode: ${esc(mode)} · score: ${esc(score)} · verdict: ${esc(verdict)}</div>
    ${rows}
    ${summary}
  </div></body></html>`;
}

// ---- capture --------------------------------------------------------------
mkdirSync(join(OUT, 'pages'), { recursive: true });
mkdirSync(join(OUT, 'session'), { recursive: true });

const manifest = { base_url: BASE_URL, character: plan.character, level: plan.level,
                   captured: [], failures: [] };

let browser;
try {
  // CI installs the matching browser via `npx playwright install chromium`.
  // Some environments pre-install Chromium at a fixed path instead — honor an
  // optional executablePath override so we use it rather than re-downloading.
  const exe = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
  browser = await chromium.launch(exe ? { executablePath: exe } : {});
} catch (e) {
  console.error(`❌ could not launch Chromium: ${e.message}\n   In CI: npm i --no-save playwright && npx playwright install chromium`);
  process.exit(2);
}

try {
  for (const q of quests) {
    const slug = slugOf(q);
    const url = `${BASE_URL}${q.permalink}`;
    const entry = { slug, title: q.title, permalink: q.permalink, url, shots: [] };

    // Rendered page at both viewports.
    for (const [name, vp] of [['mobile', MOBILE], ['desktop', DESKTOP]]) {
      const file = join(OUT, 'pages', `${slug}-${name}.png`);
      try {
        const ctx = await browser.newContext({ viewport: vp });
        const page = await ctx.newPage();
        const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
        await page.screenshot({ path: file, fullPage: true });
        await ctx.close();
        const status = resp ? resp.status() : 0;
        entry.shots.push({ kind: `page-${name}`, file, status });
        if (status >= 400) manifest.failures.push({ slug, kind: `page-${name}`, status, url });
        console.error(`📸 ${name.padEnd(7)} ${status} ${url} → ${file}`);
      } catch (e) {
        manifest.failures.push({ slug, kind: `page-${name}`, url, error: e.message });
        console.error(`⚠️  ${name} capture failed for ${url}: ${e.message}`);
      }
    }

    // Terminal render of the recorded session transcript.
    const tfile = join(OUT, 'session', `${slug}-terminal.png`);
    try {
      const ctx = await browser.newContext({ viewport: { width: 900, height: 600 } });
      const page = await ctx.newPage();
      await page.setContent(terminalHTML(q, evidenceBySlug[slug]), { waitUntil: 'load' });
      await page.locator('.term').screenshot({ path: tfile });
      await ctx.close();
      entry.shots.push({ kind: 'session-terminal', file: tfile,
                         hasEvidence: Boolean(evidenceBySlug[slug]) });
      console.error(`🖥️  terminal      ${tfile}${evidenceBySlug[slug] ? '' : ' (no recorded session)'}`);
    } catch (e) {
      manifest.failures.push({ slug, kind: 'session-terminal', error: e.message });
      console.error(`⚠️  terminal render failed for ${slug}: ${e.message}`);
    }

    manifest.captured.push(entry);
  }
} finally {
  await browser.close();
}

writeFileSync(join(OUT, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
const shots = manifest.captured.reduce((n, e) => n + e.shots.length, 0);
console.error(`\n✅ ${shots} screenshot(s) for ${quests.length} quest(s) → ${OUT}/ `
  + `(${manifest.failures.length} failure(s)). Manifest: ${join(OUT, 'manifest.json')}`);
process.exit(0);
