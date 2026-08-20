#!/usr/bin/env node
/**
 * stack_capture.mjs — walk EVERY step of a quest in an isolated sandbox and
 * capture the WHOLE STACK it exercises, step by step.
 *
 * The execute engine records *what commands did*. A learner's reality is wider
 * than a transcript: they type in a terminal, they write files, and then they
 * LOOK at something in a browser — a page they built, a dev server, a rendered
 * document. This tool walks the deterministic step plan (quest_steps.py) and,
 * after every step, photographs that whole surface:
 *
 *   terminal   — the command, its stdout/stderr and exit status
 *   filesystem — the file the step wrote, appended to, or inserted into
 *   browser    — the built artifact rendered in headless Chromium, at the
 *                viewports the step is about (a @media step is captured at
 *                mobile + tablet + desktop, because that IS the lesson)
 *   DOM/box    — a box-model probe (size, padding, border, margin, computed
 *                display) for the classes the quest's own CSS defines, plus any
 *                page console errors — the DevTools evidence the quest teaches
 *
 * Output:
 *   <out>/step-NN-<viewport>.png     per-step screenshots of the built UI
 *   <out>/manifest.json              every capture, keyed by step
 *   <evidence>                       an agentic-compatible walk-evidence.json
 *                                    (report.aggregate() shape) whose commands
 *                                    carry captures[] — so the ledger, the fix
 *                                    lane and the video recorder all consume it
 *                                    unchanged.
 *
 * Honest by construction: statuses come from real exit codes and real render
 * results, never from a judgement. A step the platform does not apply to is
 * `skipped` with the reason; a GUI opener in a sandbox is not a failure — it is
 * the moment the learner looks, and the screenshot is what they would see.
 *
 * Usage:
 *   node scripts/quest/stack_capture.mjs --steps steps.json \
 *     [--sandbox .sandbox] [--out captures] [--evidence walk-evidence.json] \
 *     [--keep-sandbox] [--timeout 60]
 *
 * Deps: playwright (+ `npx playwright install chromium`).
 */
import { execFileSync } from 'node:child_process';
import {
  readFileSync, writeFileSync, mkdirSync, existsSync, rmSync, statSync,
} from 'node:fs';
import { join, dirname, resolve, basename } from 'node:path';

// ---- args -----------------------------------------------------------------
const args = process.argv.slice(2);
const opt = (n, d) => {
  const i = args.indexOf(`--${n}`);
  return i >= 0 && args[i + 1] !== undefined ? args[i + 1] : d;
};
const flag = (n) => args.includes(`--${n}`);

const STEPS = opt('steps', 'steps.json');
const SANDBOX = resolve(opt('sandbox', '.sandbox'));
const OUT = opt('out', 'captures');
const EVIDENCE = opt('evidence', 'walk-evidence.json');
const KEEP = flag('keep-sandbox');
const TIMEOUT = Math.max(5, parseInt(opt('timeout', '60'), 10) || 60) * 1000;

const VIEWPORTS = {
  mobile: { width: 390, height: 844 },
  tablet: { width: 768, height: 1024 },
  desktop: { width: 1280, height: 800 },
};

let plan;
try {
  plan = JSON.parse(readFileSync(STEPS, 'utf8'));
} catch (e) {
  console.error(`❌ cannot read step plan ${STEPS}: ${e.message}`);
  process.exit(2);
}
const steps = Array.isArray(plan.steps) ? plan.steps : [];
if (!steps.length) {
  console.error(`⚠️  step plan ${STEPS} has no steps.`);
  process.exit(0);
}

// ---- sandbox --------------------------------------------------------------
if (existsSync(SANDBOX)) rmSync(SANDBOX, { recursive: true, force: true });
mkdirSync(SANDBOX, { recursive: true });
mkdirSync(OUT, { recursive: true });

// The quests say `cd ~/project`; HOME points at the sandbox so that lands
// inside it and the walk cannot touch anything outside.
const ENV = { ...process.env, HOME: SANDBOX, PWD: SANDBOX, TMPDIR: join(SANDBOX, '.tmp') };
mkdirSync(ENV.TMPDIR, { recursive: true });

// Commands a sandboxed walk must never run for real (they need a GUI, network,
// or would escape the box). Recorded as skipped with the reason, not failed.
const UNSAFE = [/\bsudo\b/, /\brm\s+-rf\s+\/(?!\w)/, /\bshutdown\b/, /\breboot\b/];

const CWD_MARK = '<<<QUEST_CWD>>>';

function splitCwd(stdout) {
  const at = stdout.lastIndexOf(CWD_MARK);
  if (at < 0) return { out: stdout, cwd: null };
  return {
    out: stdout.slice(0, at),
    cwd: stdout.slice(at + CWD_MARK.length).trim() || null,
  };
}

function runShell(lines, cwd) {
  // Wrap so the script's own exit code survives while we still learn the
  // directory it left us in — a quest that says `cd ~/css-quest` expects every
  // later step to happen THERE, and so does the learner.
  const script = `{ ${lines.join('\n')}
} ; __quest_ec=$?
printf '\\n${CWD_MARK}%s' "$PWD"
exit $__quest_ec`;
  const started = Date.now();
  try {
    const raw = execFileSync('bash', ['-lc', script], {
      cwd, env: { ...ENV, PWD: cwd }, timeout: TIMEOUT, encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    const { out, cwd: next } = splitCwd(raw || '');
    return { ok: true, code: 0, stdout: out, stderr: '', cwd: next, ms: Date.now() - started };
  } catch (e) {
    const { out, cwd: next } = splitCwd((e.stdout || '').toString());
    return {
      ok: false,
      code: typeof e.status === 'number' ? e.status : -1,
      stdout: out,
      stderr: (e.stderr || e.message || '').toString(),
      cwd: next,
      ms: Date.now() - started,
    };
  }
}

// ---- file steps -----------------------------------------------------------
function applyFileStep(step, cwd) {
  const file = join(cwd, step.target);
  mkdirSync(dirname(file), { recursive: true });
  const body = step.code.endsWith('\n') ? step.code : `${step.code}\n`;
  if (step.mode === 'write' || !existsSync(file)) {
    writeFileSync(file, body);
    return { action: 'wrote', bytes: body.length };
  }
  if (step.mode === 'insert' && step.anchor) {
    const cur = readFileSync(file, 'utf8');
    const close = `</${step.anchor}>`;
    const at = cur.lastIndexOf(close);
    if (at >= 0) {
      writeFileSync(file, cur.slice(0, at) + body + cur.slice(at));
      return { action: `inserted before ${close}`, bytes: body.length };
    }
  }
  writeFileSync(file, readFileSync(file, 'utf8') + '\n' + body);
  return { action: 'appended', bytes: body.length };
}

// ---- browser capture ------------------------------------------------------
// Which viewports to shoot for a step: always desktop; the full responsive set
// when the step is *about* responsiveness (or is the final built state), since
// that is precisely what the learner is meant to see.
function viewportsFor(step, isLast) {
  const responsive = /@media|grid-template-columns|minmax\(|flex|prefers-color-scheme/i
    .test(step.code || '');
  return (responsive || isLast) ? ['mobile', 'tablet', 'desktop'] : ['desktop'];
}

// Box-model + health probe: the DevTools evidence the quest talks about.
async function probe(page) {
  return page.evaluate(() => {
    const out = { title: document.title || '', elements: document.querySelectorAll('*').length,
                  styleSheets: document.styleSheets.length, boxes: [] };
    const seen = new Set();
    for (const sheet of Array.from(document.styleSheets)) {
      let rules = [];
      try { rules = Array.from(sheet.cssRules || []); } catch { /* cross-origin */ }
      for (const r of rules) {
        const sel = r.selectorText;
        if (!sel || seen.has(sel) || !/^[.#][\w-]+$/.test(sel)) continue;
        const el = document.querySelector(sel);
        if (!el) continue;
        seen.add(sel);
        const cs = getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        out.boxes.push({
          selector: sel,
          width: Math.round(rect.width), height: Math.round(rect.height),
          display: cs.display,
          padding: cs.padding, border: cs.borderWidth, margin: cs.margin,
          boxSizing: cs.boxSizing,
        });
        if (out.boxes.length >= 6) break;
      }
      if (out.boxes.length >= 6) break;
    }
    return out;
  });
}

// ---- main -----------------------------------------------------------------
let browser;
try {
  const { chromium } = await import('playwright');
  const exe = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
  browser = await chromium.launch(exe ? { executablePath: exe } : {});
} catch (e) {
  console.error(`❌ could not launch Chromium: ${e.message}\n   npm i --no-save playwright && npx playwright install chromium`);
  process.exit(2);
}

const captures = [];
const commands = [];
// The directory the quest has walked us into (its `cd ~/project`), and the
// artifact the learner is currently looking at, as an absolute path.
let cwd = SANDBOX;
let currentHtml = null;
let passed = 0, failed = 0, skipped = 0;

try {
  for (const [i, step] of steps.entries()) {
    const isLast = i === steps.length - 1;
    const label = `${String(step.index).padStart(2, '0')}`;
    if (step.kind === 'display') continue;

    const cmdSummary = (step.kind === 'file')
      ? `# ${step.mode} ${step.code.split('\n').length} line(s) → ${step.target}`
      : (step.code.split('\n').find((l) => l.trim() && !l.trim().startsWith('#')) || step.code)
          .trim().slice(0, 200);

    // --- not applicable to this platform: honest skip, no execution --------
    if (!step.applicable) {
      skipped += 1;
      commands.push({
        command: cmdSummary, status: 'skipped',
        detail: `${step.platform || 'other'} path — not applicable on this ${plan.platform} sandbox`,
        step: step.index, chapter: step.chapter, kind: step.kind, captures: [],
      });
      console.error(`∅  ${label} skipped (${step.platform} path)`);
      continue;
    }

    let status = 'passed';
    let detail = '';

    if (step.kind === 'shell' || step.kind === 'open') {
      const lines = step.code.split('\n')
        .map((l) => l.trim())
        .filter((l) => l && !l.startsWith('#'));
      const openers = lines.filter((l) => /^(xdg-open|open |start |start-process|code |subl |gnome-open|firefox |chromium |google-chrome )/i.test(l));
      const runnable = lines.filter((l) => !openers.includes(l));
      const unsafe = runnable.filter((l) => UNSAFE.some((rx) => rx.test(l)));
      const toRun = runnable.filter((l) => !unsafe.includes(l));

      if (toRun.length) {
        const r = runShell(toRun, cwd);
        if (r.cwd && existsSync(r.cwd)) cwd = r.cwd;
        status = r.ok ? 'passed' : 'failed';
        detail = r.ok
          ? `exit 0 · ${toRun.length} command(s)${r.stdout.trim() ? ` · ${r.stdout.trim().split('\n').slice(-1)[0].slice(0, 120)}` : ''}`
          : `exit ${r.code}: ${(r.stderr || r.stdout).trim().split('\n').slice(-1)[0].slice(0, 160)}`;
      }
      if (unsafe.length) {
        detail += `${detail ? ' · ' : ''}${unsafe.length} line(s) withheld (sandbox safety)`;
      }
      if (openers.length) {
        detail += `${detail ? ' · ' : ''}opens ${step.opens || 'a viewer'} → captured in the browser below`;
      }
      if (!toRun.length && openers.length) status = 'passed';
    } else if (step.kind === 'file') {
      try {
        const r = applyFileStep(step, cwd);
        detail = `${r.action} ${r.bytes} bytes → ${step.target}`;
      } catch (e) {
        status = 'failed';
        detail = `could not write ${step.target}: ${e.message}`;
      }
    }

    // --- what is the learner looking at now? ------------------------------
    const named = (step.opens && step.opens.endsWith('.html') && step.opens)
      || (step.target && step.target.endsWith('.html') && step.target)
      || null;
    if (named && existsSync(join(cwd, named))) currentHtml = join(cwd, named);
    else if (named && existsSync(join(SANDBOX, named))) currentHtml = join(SANDBOX, named);

    const stepCaptures = [];
    if (currentHtml && existsSync(currentHtml)) {
      const url = `file://${currentHtml}`;
      for (const vp of viewportsFor(step, isLast)) {
        const file = join(OUT, `step-${label}-${vp}.png`);
        try {
          const ctx = await browser.newContext({ viewport: VIEWPORTS[vp] });
          const page = await ctx.newPage();
          const errors = [];
          page.on('pageerror', (err) => errors.push(String(err).slice(0, 120)));
          await page.goto(url, { waitUntil: 'load', timeout: 20000 });
          await page.waitForTimeout(120);
          await page.screenshot({ path: file });
          const p = vp === 'desktop' ? await probe(page) : null;
          await ctx.close();
          const cap = {
            kind: 'browser', viewport: vp, file, url,
            artifact: basename(currentHtml),
            label: `${basename(currentHtml)} @ ${vp}`,
            probe: p || undefined,
            page_errors: errors.length ? errors : undefined,
          };
          stepCaptures.push(cap);
          captures.push({ step: step.index, ...cap });
          if (errors.length && status === 'passed') {
            detail += `${detail ? ' · ' : ''}page error: ${errors[0]}`;
            status = 'failed';
          }
        } catch (e) {
          console.error(`⚠️  capture failed for step ${label} @ ${vp}: ${e.message}`);
        }
      }
      if (stepCaptures.length) {
        const p = stepCaptures.find((c) => c.probe)?.probe;
        if (p) {
          detail += `${detail ? ' · ' : ''}rendered: ${p.elements} elements, `
            + `${p.styleSheets} stylesheet(s)`
            + (p.boxes.length ? `, ${p.boxes[0].selector} ${p.boxes[0].width}×${p.boxes[0].height}px `
              + `(${p.boxes[0].boxSizing}, pad ${p.boxes[0].padding})` : '');
        }
      }
    }

    if (status === 'passed') passed += 1; else failed += 1;
    commands.push({
      command: cmdSummary, status, detail,
      step: step.index, chapter: step.chapter, kind: step.kind,
      captures: stepCaptures.map(({ kind, viewport, file, label: l, artifact }) =>
        ({ kind, viewport, file, label: l, artifact })),
    });
    console.error(`${status === 'passed' ? '✓' : '✗'}  ${label} ${step.kind.padEnd(6)} `
      + `${stepCaptures.length} capture(s) — ${detail.slice(0, 100)}`);
  }
} finally {
  await browser.close();
}

// ---- evidence (agentic report.aggregate() shape) --------------------------
const attempted = passed + failed;
const overall = attempted ? Math.round((passed / attempted) * 1000) / 10 : 0;
const verdict = overall >= 85 ? 'pass' : (overall >= 70 ? 'warn' : 'fail');
const recommendations = commands
  .filter((c) => c.status === 'failed')
  .map((c) => ({ priority: 'high', issue: `Step ${c.step} failed: ${c.command}`,
                 fix: c.detail }));

const evidence = {
  schema_version: '1.0.0',
  total: 1, scored: 1, errored: 0,
  average: overall,
  counts: { pass: verdict === 'pass' ? 1 : 0, warn: verdict === 'warn' ? 1 : 0,
            fail: verdict === 'fail' ? 1 : 0 },
  cost_usd: 0,
  capture: {
    tool: 'scripts/quest/stack_capture.mjs',
    sandbox: SANDBOX, out: OUT,
    quest_dir: cwd,
    platform: plan.platform,
    steps_total: steps.length,
    steps_executed: attempted,
    steps_skipped: skipped,
    screenshots: captures.length,
  },
  results: [{
    quest: plan.quest,
    mode: 'execute',
    meta: { cost_usd: 0, tool: 'stack_capture' },
    overall,
    verdict,
    verdict_obj: {
      executed: true,
      summary: `Walked ${attempted} applicable step(s) of ${steps.length} in an isolated sandbox `
        + `(${plan.platform} path): ${passed} passed, ${failed} failed, ${skipped} not applicable. `
        + `Captured ${captures.length} browser screenshot(s) of the built UI across `
        + `${[...new Set(captures.map((c) => c.viewport))].join('/')} viewports.`,
      commands,
      recommendations,
    },
  }],
};
writeFileSync(EVIDENCE, JSON.stringify(evidence, null, 2) + '\n');
writeFileSync(join(OUT, 'manifest.json'), JSON.stringify({
  schema_version: '1.0.0', quest: plan.quest, platform: plan.platform,
  sandbox: SANDBOX, captures,
}, null, 2) + '\n');

if (!KEEP) {
  // Keep the built artifacts (they are the learner's output) but drop temp.
  rmSync(join(SANDBOX, '.tmp'), { recursive: true, force: true });
}
console.error(`\n📸 ${captures.length} screenshot(s) over ${attempted} executed step(s) `
  + `(${skipped} not applicable) → ${OUT}/`);
console.error(`📄 evidence → ${EVIDENCE}  (score ${overall}%, verdict ${verdict})`);
process.exit(0);
