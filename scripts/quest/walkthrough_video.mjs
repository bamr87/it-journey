#!/usr/bin/env node
/**
 * walkthrough_video.mjs — render a SIDE-BY-SIDE walkthrough video of a quest run
 * from the quest-perfection loop's sealed evidence.
 *
 * Composition (one continuous 1920×1080 recording per quest):
 *   left pane  — the RENDERED QUEST PAGE (captured off the live site, auto-
 *                scrolling in sync with the run) — what the learner reads.
 *   right pane — an animated TERMINAL REPLAY of the recorded session transcript
 *                (the commands the agentic execute engine actually ran in the
 *                sandbox, typed out with their pass/fail/skipped/reasoned
 *                outcome) — what the learner does.
 *   intro card — quest title, character/level/tier, difficulty, date.
 *   outro card — verdict + score, quest URL, provenance (CI run), CTA.
 *
 * The transcript comes from walk-evidence.json (agentic_validate.py --mode
 * execute), which the workflow MINTS AND SEALS before any agent runs — so the
 * video is a faithful replay of witnessed evidence, never a model's synthesis.
 * This script renders deterministically from (plan, evidence): no model calls.
 *
 * Like walkthrough_screenshots.mjs it is a COLLECTOR, not a gate: per-quest
 * failures land in <out>/manifest.json and the exit code stays 0 unless the
 * browser itself cannot launch (exit 2) or nothing at all could be rendered
 * when at least one quest was selected (exit 1).
 *
 * Usage:
 *   node scripts/quest/walkthrough_video.mjs \
 *     --plan walk-plan.json --evidence walk-evidence.json \
 *     [--out videos] [--base-url https://it-journey.dev] \
 *     [--quest <permalink|path|slug>] [--all-main] [--all] \
 *     [--max-seconds 300] [--max-commands 24] [--size 1920x1080] \
 *     [--allow-no-evidence] [--no-transcode] [--list] [--dry-run]
 *
 * Selection: by default the FIRST main_quest in plan order that has recorded
 * evidence (the plan is dependency-ordered, so that is the slice's main quest).
 * --all-main renders every evidenced main quest; --all every evidenced quest;
 * --quest pins one explicitly.
 *
 * Output per quest: <out>/<level>-<slug>.webm (Playwright's native recording),
 * plus <out>/<level>-<slug>.mp4 when ffmpeg is on PATH (H.264 yuv420p
 * +faststart — YouTube accepts either), and <out>/<level>-<slug>.chapters.json
 * (the timeline video_manifest.py turns into YouTube chapter lines). A global
 * <out>/manifest.json records everything for the upload/apply lane.
 *
 * Deps (install in CI, --no-save): playwright (+ `npx playwright install
 * chromium ffmpeg` — video recording needs Playwright's bundled ffmpeg).
 * Mirrors walkthrough_screenshots.mjs so the browser-driving tools stay aligned.
 */
import { execFileSync, spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync, renameSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';

// ---- args -----------------------------------------------------------------
const args = process.argv.slice(2);
const opt = (name, dflt) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 && args[i + 1] !== undefined ? args[i + 1] : dflt;
};
const flag = (name) => args.includes(`--${name}`);

const PLAN = opt('plan', 'walk-plan.json');
const EVIDENCE = opt('evidence', 'walk-evidence.json');
const OUT = opt('out', 'videos');
const BASE_URL = (process.env.BASE_URL || opt('base-url', 'https://it-journey.dev'))
  .replace(/\/+$/, '');
const QUEST_PIN = opt('quest', '');
const ALL_MAIN = flag('all-main');
const ALL = flag('all');
const MAX_SECONDS = Math.max(60, parseInt(opt('max-seconds', '300'), 10) || 300);
const MAX_COMMANDS = Math.max(1, parseInt(opt('max-commands', '24'), 10) || 24);
const ALLOW_NO_EVIDENCE = flag('allow-no-evidence');
const NO_TRANSCODE = flag('no-transcode');
const LIST_ONLY = flag('list');
const DRY_RUN = flag('dry-run');
const SIZE = (() => {
  const m = /^(\d+)x(\d+)$/.exec(opt('size', '1920x1080'));
  return m ? { width: +m[1], height: +m[2] } : { width: 1920, height: 1080 };
})();

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
  console.error(`⚠️  plan ${PLAN} has no quests — nothing to record.`);
  process.exit(0);
}

const evidenceBySlug = {};
let evidenceMeta = {};
try {
  const ev = JSON.parse(readFileSync(EVIDENCE, 'utf8'));
  evidenceMeta = { scored: ev.scored, total: ev.total, truncated: Boolean(ev.truncated) };
  for (const r of ev.results || []) {
    const slug = (r.quest && (r.quest.slug || basenameSlug(r.quest.path))) || '';
    if (slug) evidenceBySlug[slug] = r;
  }
} catch {
  console.error(`ℹ️  no readable evidence at ${EVIDENCE} — only --allow-no-evidence renders will work.`);
}

function basenameSlug(p) {
  if (!p) return '';
  const base = p.split('/').pop() || '';
  return base.replace(/\.md$/, '').replace(/^\d{4}-\d{2}-\d{2}-/, '');
}
function slugOf(q) {
  return basenameSlug(q.path) || (q.permalink || '').split('/').filter(Boolean).pop() || 'quest';
}
const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// ---- selection --------------------------------------------------------------
// Default: the slice's MAIN QUEST — the first main_quest in dependency order
// with recorded evidence. The flags widen or pin the set.
function selectQuests() {
  const hasEvidence = (q) => Boolean(evidenceBySlug[slugOf(q)]);
  if (QUEST_PIN) {
    const hit = quests.find((q) =>
      q.permalink === QUEST_PIN || q.path === QUEST_PIN || slugOf(q) === QUEST_PIN);
    if (!hit) {
      console.error(`❌ --quest "${QUEST_PIN}" matches nothing in the plan.`);
      process.exit(2);
    }
    return [hit];
  }
  const pool = ALL ? quests : quests.filter((q) => (q.type || '') === 'main_quest');
  const evidenced = pool.filter(hasEvidence);
  if (ALL || ALL_MAIN) return evidenced.length || !ALLOW_NO_EVIDENCE ? evidenced : pool;
  if (evidenced.length) return [evidenced[0]];
  // No evidenced main quest — fall back to the first evidenced quest of any
  // type so a windowed run that skipped the main quest still yields a video.
  const anyEvidenced = quests.filter(hasEvidence);
  if (anyEvidenced.length) return [anyEvidenced[0]];
  return ALLOW_NO_EVIDENCE && pool.length ? [pool[0]] : [];
}

const selected = selectQuests();
if (LIST_ONLY) {
  for (const q of selected) {
    const ev = evidenceBySlug[slugOf(q)];
    console.log(`${slugOf(q)}  ${q.type || '?'}  evidence=${ev ? 'yes' : 'no'}  ${q.permalink}`);
  }
  console.log(`\n${selected.length} quest(s) selected.`);
  process.exit(0);
}
if (!selected.length) {
  // Still leave a (video-less) manifest so downstream steps can count 0 videos
  // instead of crashing on a missing file — e.g. when reused evidence was a
  // truncated zero-scored run.
  mkdirSync(OUT, { recursive: true });
  writeFileSync(join(OUT, 'manifest.json'), JSON.stringify({
    schema_version: '1.0.0', base_url: BASE_URL,
    character: plan.character, level: plan.level, evidence: evidenceMeta,
    videos: [], failures: [],
    reason: 'no quest selected — no recorded evidence for any main quest '
      + '(pass --quest, --all, or --allow-no-evidence)',
  }, null, 2) + '\n');
  console.error('⚠️  no quest selected (no recorded evidence for any main quest — '
    + 'pass --quest, --all, or --allow-no-evidence).');
  process.exit(0);
}

// ---- timeline ----------------------------------------------------------------
// Deterministic schedule computed HERE (not in the page) so chapters in the
// manifest and the on-screen replay can never disagree.
const STATUS = {
  passed:   { color: '#3fb950', mark: '✓', label: 'passed' },
  failed:   { color: '#f85149', mark: '✗', label: 'failed' },
  skipped:  { color: '#8b949e', mark: '∅', label: 'skipped' },
  reasoned: { color: '#d29922', mark: '~', label: 'reasoned' },
};

function buildSchedule(quest, result) {
  const v = (result && result.verdict_obj) || {};
  let cmds = Array.isArray(v.commands) ? v.commands.slice(0, MAX_COMMANDS) : [];
  const dropped = Array.isArray(v.commands) ? v.commands.length - cmds.length : 0;
  const segs = [];
  segs.push({ kind: 'intro', label: 'Intro', dur: 5.0 });
  for (const [i, c] of cmds.entries()) {
    const cmd = String(c.command || '').slice(0, 220);
    const detail = String(c.detail || '').slice(0, 360);
    const type = Math.min(2.6, 0.35 + cmd.length * 0.045);
    const read = Math.min(3.2, 1.4 + detail.length * 0.012);
    segs.push({
      kind: 'cmd', index: i, cmd, detail,
      status: STATUS[c.status] ? c.status : 'reasoned',
      label: `$ ${cmd.length > 44 ? cmd.slice(0, 41) + '…' : cmd}`,
      dur: type + 0.7 + read,
      typeSecs: type,
    });
  }
  segs.push({ kind: 'outro', label: 'Verdict & next steps', dur: 6.5, dropped });
  // Clamp the whole video to MAX_SECONDS by scaling command segments (never the
  // intro/outro below a readable floor).
  let total = segs.reduce((s, x) => s + x.dur, 0);
  if (total > MAX_SECONDS) {
    const fixed = 5.0 + 6.5;
    const scale = Math.max(0.35, (MAX_SECONDS - fixed) / (total - fixed));
    for (const s of segs) {
      if (s.kind === 'cmd') {
        s.dur = Math.max(1.6, s.dur * scale);
        s.typeSecs = Math.min(s.typeSecs, s.dur * 0.55);
      }
    }
    total = segs.reduce((s, x) => s + x.dur, 0);
  }
  let t = 0;
  for (const s of segs) { s.start = Math.round(t * 10) / 10; t += s.dur; }
  return { segments: segs, duration: Math.round(t * 10) / 10, commands: cmds.length, dropped };
}

// ---- studio page --------------------------------------------------------------
// One self-driving HTML page: it receives the schedule + assets, plays the
// timeline in real time, and resolves window.__done when the outro finishes.
// Playwright records the whole context, so the recording IS the timeline.
function studioHTML(quest, result, schedule, leftPane) {
  const v = (result && result.verdict_obj) || {};
  const score = result && typeof result.overall === 'number' ? `${Math.round(result.overall)}%` : '—';
  const verdict = (result && result.verdict) || 'unreviewed';
  const summary = String(v.summary || '').slice(0, 420);
  const lvl = quest.level || plan.level.code;
  const tierEmoji = plan.level.tier_emoji || '';
  const character = plan.character || {};
  const payload = JSON.stringify({
    segments: schedule.segments,
    duration: schedule.duration,
    statusMap: STATUS,
  });
  const left = leftPane.dataUri
    ? `<div class="scroller"><img id="questpage" src="${leftPane.dataUri}" alt="Rendered quest page"></div>`
    : `<div class="fallback"><h2>${esc(quest.title)}</h2>
         <p class="perma">${esc(BASE_URL + quest.permalink)}</p>
         ${leftPane.objectives.length
           ? `<h3>Objectives</h3><ul>${leftPane.objectives.map((o) => `<li>${esc(o)}</li>`).join('')}</ul>`
           : '<p class="muted">Read the full quest on it-journey.dev</p>'}
       </div>`;
  return `<!doctype html><html><head><meta charset="utf-8"><style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body { margin:0; width:${SIZE.width}px; height:${SIZE.height}px; overflow:hidden;
         background:#0d1117; color:#e6edf3;
         font:16px/1.5 -apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; }
  header { height:64px; display:flex; align-items:center; gap:16px; padding:0 24px;
           background:#010409; border-bottom:1px solid #21262d; }
  header .brand { font-weight:700; color:#58a6ff; white-space:nowrap; }
  header .title { font-weight:600; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  header .badge { margin-left:auto; display:flex; gap:10px; align-items:center; white-space:nowrap;
                  color:#8b949e; font-size:14px; }
  header .badge b { color:#e6edf3; }
  main { display:flex; height:${SIZE.height - 64 - 56}px; }
  .pane-left { width:46%; border-right:1px solid #21262d; background:#ffffff; position:relative; overflow:hidden; }
  .scroller { position:absolute; inset:0; overflow:hidden; }
  .scroller img { width:100%; display:block; transform:translateY(0);
                  transition:transform 1.1s cubic-bezier(.4,0,.2,1); }
  .fallback { padding:40px; color:#24292f; background:#ffffff; height:100%; overflow:hidden; }
  .fallback h2 { margin:0 0 8px; } .fallback .perma { color:#57606a; font-size:14px; }
  .fallback .muted { color:#8b949e; }
  .pane-right { width:54%; background:#0d1117; display:flex; flex-direction:column; }
  .termbar { display:flex; gap:8px; align-items:center; padding:12px 18px 8px; }
  .dot { width:13px; height:13px; border-radius:50%; }
  .termbar .name { margin-left:10px; color:#8b949e; font-size:13px; }
  #term { flex:1; overflow:hidden; padding:6px 22px 18px;
          font:15px/1.6 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
  #term .line { white-space:pre-wrap; word-break:break-word; margin:3px 0; }
  #term .prompt { color:#3fb950; } #term .cmd { color:#e6edf3; }
  #term .st { font-size:13px; margin-left:8px; }
  #term .detail { color:#8b949e; font-size:13px; margin:1px 0 8px 18px; }
  #term .caret { display:inline-block; width:9px; height:17px; background:#e6edf3;
                 vertical-align:text-bottom; animation:blink 1s steps(1) infinite; }
  @keyframes blink { 50% { opacity:0; } }
  footer { height:56px; display:flex; align-items:center; gap:18px; padding:0 24px;
           background:#010409; border-top:1px solid #21262d; }
  .progress { flex:1; height:6px; border-radius:3px; background:#21262d; overflow:hidden; }
  .progress > div { height:100%; width:0%; background:linear-gradient(90deg,#1f6feb,#58a6ff); }
  footer .chapter { color:#8b949e; font-size:14px; max-width:46%; overflow:hidden;
                    text-overflow:ellipsis; white-space:nowrap; }
  footer .site { color:#58a6ff; font-weight:600; font-size:14px; }
  .overlay { position:fixed; inset:0; background:rgba(1,4,9,.96); display:flex;
             align-items:center; justify-content:center; text-align:center;
             transition:opacity .9s ease; z-index:10; }
  .overlay.hidden { opacity:0; pointer-events:none; }
  .card { max-width:1100px; padding:40px; }
  .card .kicker { color:#58a6ff; font-weight:700; letter-spacing:.12em;
                  text-transform:uppercase; font-size:15px; }
  .card h1 { font-size:44px; margin:14px 0 10px; }
  .card .meta { color:#8b949e; font-size:19px; margin-bottom:14px; }
  .card .note { color:#c9d1d9; font-size:17px; }
  .card .verdict { font-size:30px; margin:12px 0; }
  .card .url { color:#58a6ff; font-size:20px; font-weight:600; margin-top:10px; }
  </style></head><body>
  <header>
    <span class="brand">🎬 IT-Journey</span>
    <span class="title">${esc(quest.title)}</span>
    <span class="badge">${esc(tierEmoji)} <b>Level ${esc(lvl)}</b> · ${esc(plan.level.theme || '')}
      · ${esc(quest.difficulty || '')} · <b id="step">Intro</b></span>
  </header>
  <main>
    <div class="pane-left">${left}</div>
    <div class="pane-right">
      <div class="termbar">
        <span class="dot" style="background:#f85149"></span>
        <span class="dot" style="background:#d29922"></span>
        <span class="dot" style="background:#3fb950"></span>
        <span class="name">sandbox — recorded quest run (${esc((result && result.mode) || 'execute')} mode)</span>
      </div>
      <div id="term"><div class="line"><span class="prompt">$</span> <span class="caret"></span></div></div>
    </div>
  </main>
  <footer>
    <span class="chapter" id="chapter">Intro</span>
    <div class="progress"><div id="bar"></div></div>
    <span class="site">it-journey.dev</span>
  </footer>
  <div class="overlay" id="intro"><div class="card">
    <div class="kicker">Quest Walkthrough · Verified Run</div>
    <h1>${esc(quest.title)}</h1>
    <div class="meta">${esc(character.name || '')} path · ${esc(tierEmoji)} Level ${esc(lvl)} — ${esc(plan.level.theme || '')}
      · ${esc(quest.difficulty || '')}</div>
    <div class="note">Every command in this video was executed for real in a clean, disposable
      sandbox by IT-Journey's automated quest-perfection loop. Left: the quest as you read it.
      Right: the recorded session.</div>
  </div></div>
  <div class="overlay hidden" id="outro"><div class="card">
    <div class="kicker">Session verdict</div>
    <div class="verdict">${esc(verdict)} · score ${esc(score)}</div>
    ${summary ? `<div class="note">${esc(summary)}</div>` : ''}
    <div class="url">${esc(BASE_URL + quest.permalink)}</div>
    <div class="note" style="margin-top:14px">Take the quest yourself — start your journey at it-journey.dev ⚔️</div>
  </div></div>
  <script>
  const DATA = ${payload};
  const sleep = (s) => new Promise((r) => setTimeout(r, Math.max(0, s * 1000)));
  const term = document.getElementById('term');
  const img = document.getElementById('questpage');
  const bar = document.getElementById('bar');
  const stepEl = document.getElementById('step');
  const chapterEl = document.getElementById('chapter');
  const caretLine = term.lastElementChild;

  function scrollLeft(i, n) {
    if (!img) return;
    const pane = img.parentElement.getBoundingClientRect();
    const overflow = Math.max(0, img.naturalHeight * (pane.width / img.naturalWidth) - pane.height);
    img.style.transform = 'translateY(-' + Math.round(overflow * ((i + 1) / (n + 1))) + 'px)';
  }
  function keepTermBottom() { term.scrollTop = term.scrollHeight; }

  async function typeCommand(seg) {
    const line = document.createElement('div');
    line.className = 'line';
    line.innerHTML = '<span class="prompt">$</span> <span class="cmd"></span>';
    term.insertBefore(line, caretLine);
    const cmdEl = line.querySelector('.cmd');
    const per = seg.typeSecs / Math.max(1, seg.cmd.length);
    for (const ch of seg.cmd) {
      cmdEl.textContent += ch;
      keepTermBottom();
      await sleep(per);
    }
    await sleep(0.35);
    const st = DATA.statusMap[seg.status];
    const stEl = document.createElement('span');
    stEl.className = 'st';
    stEl.style.color = st.color;
    stEl.textContent = st.mark + ' ' + st.label;
    line.appendChild(stEl);
    if (seg.detail) {
      const d = document.createElement('div');
      d.className = 'detail';
      d.textContent = seg.detail;
      term.insertBefore(d, caretLine);
    }
    keepTermBottom();
  }

  window.__done = (async () => {
    // Give the recorder + image decode a beat before the clock starts.
    await new Promise((r) => (document.readyState === 'complete'
      ? r() : addEventListener('load', r)));
    await sleep(0.4);
    const cmds = DATA.segments.filter((s) => s.kind === 'cmd');
    for (const seg of DATA.segments) {
      chapterEl.textContent = seg.label;
      bar.style.transition = 'width ' + seg.dur + 's linear';
      bar.style.width = Math.min(100, ((seg.start + seg.dur) / DATA.duration) * 100) + '%';
      if (seg.kind === 'intro') {
        stepEl.textContent = 'Intro';
        await sleep(seg.dur);
        document.getElementById('intro').classList.add('hidden');
      } else if (seg.kind === 'cmd') {
        stepEl.textContent = 'Step ' + (seg.index + 1) + '/' + cmds.length;
        scrollLeft(seg.index, cmds.length);
        const t0 = performance.now();
        await typeCommand(seg);
        await sleep(seg.dur - (performance.now() - t0) / 1000);
      } else {
        stepEl.textContent = 'Verdict';
        document.getElementById('outro').classList.remove('hidden');
        await sleep(seg.dur);
      }
    }
    return true;
  })();
  </script></body></html>`;
}

// ---- left pane capture --------------------------------------------------------
async function captureQuestPage(browser, quest) {
  const url = `${BASE_URL}${quest.permalink}`;
  try {
    const ctx = await browser.newContext({ viewport: { width: 880, height: 1000 } });
    const page = await ctx.newPage();
    const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    if (!resp || resp.status() >= 400) throw new Error(`HTTP ${resp ? resp.status() : 0}`);
    const buf = await page.screenshot({ fullPage: true, type: 'jpeg', quality: 78 });
    await ctx.close();
    return { dataUri: `data:image/jpeg;base64,${buf.toString('base64')}`, objectives: [], url };
  } catch (e) {
    console.error(`⚠️  could not capture ${url} (${e.message}) — using text fallback pane.`);
    return { dataUri: '', objectives: readObjectives(quest), url };
  }
}

// Best-effort objective extraction from the quest markdown (fallback pane only).
function readObjectives(quest) {
  try {
    const text = readFileSync(quest.path, 'utf8');
    const m = /^---\n([\s\S]*?)\n---/.exec(text);
    if (!m) return [];
    for (const key of ['validation_criteria', 'learning_objectives']) {
      const block = new RegExp(`^${key}:\\n((?:\\s*-\\s.*\\n?)+)`, 'm').exec(m[1]);
      if (block) {
        return block[1].split('\n')
          .map((l) => l.replace(/^\s*-\s*/, '').trim())
          .filter(Boolean).slice(0, 6);
      }
    }
  } catch { /* fallback stays empty */ }
  return [];
}

// ---- transcode ------------------------------------------------------------------
function ffmpegAvailable() {
  return spawnSync('ffmpeg', ['-version'], { stdio: 'ignore' }).status === 0;
}
function transcode(webm, mp4) {
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', webm,
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '30',
    '-movflags', '+faststart', '-an', mp4]);
}

// ---- main -----------------------------------------------------------------------
mkdirSync(OUT, { recursive: true });
const manifest = {
  schema_version: '1.0.0',
  base_url: BASE_URL,
  character: plan.character,
  level: plan.level,
  evidence: evidenceMeta,
  size: SIZE,
  videos: [],
  failures: [],
};

if (DRY_RUN) {
  for (const q of selected) {
    const schedule = buildSchedule(q, evidenceBySlug[slugOf(q)]);
    console.log(`${slugOf(q)}: ${schedule.commands} command(s), ~${schedule.duration}s`);
    for (const s of schedule.segments) console.log(`  ${String(s.start).padStart(6)}s  ${s.label}`);
  }
  process.exit(0);
}

// playwright is imported lazily so the dependency-free modes (--list,
// --dry-run) work without it installed — e.g. `make quest-video-plan`.
let browser;
try {
  const { chromium } = await import('playwright');
  const exe = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
  browser = await chromium.launch(exe ? { executablePath: exe } : {});
} catch (e) {
  console.error(`❌ could not launch Chromium: ${e.message}\n   In CI: npm i --no-save playwright && npx playwright install chromium ffmpeg`);
  process.exit(2);
}

try {
  for (const q of selected) {
    const slug = slugOf(q);
    const name = `${q.level || plan.level.code}-${slug}`;
    const result = evidenceBySlug[slug];
    if (!result && !ALLOW_NO_EVIDENCE) {
      manifest.failures.push({ slug, error: 'no recorded evidence (pass --allow-no-evidence to render a read-only tour)' });
      continue;
    }
    const schedule = buildSchedule(q, result);
    const leftPane = await captureQuestPage(browser, q);
    console.error(`🎬 recording ${name} — ${schedule.commands} command(s), ~${schedule.duration}s …`);
    try {
      const ctx = await browser.newContext({
        viewport: SIZE,
        recordVideo: { dir: OUT, size: SIZE },
      });
      const page = await ctx.newPage();
      await page.setContent(studioHTML(q, result, schedule, leftPane),
        { waitUntil: 'load', timeout: 60000 });
      await page.waitForFunction(() => window.__done !== undefined, { timeout: 15000 });
      await page.evaluate(() => window.__done, { timeout: 0 })
        .catch(() => { throw new Error('timeline did not finish'); });
      await page.waitForTimeout(600); // let the last frame land in the recording
      const video = page.video();
      await ctx.close();
      const raw = await video.path();
      const webm = join(OUT, `${name}.webm`);
      renameSync(raw, webm);
      let file = webm, format = 'webm';
      if (!NO_TRANSCODE && ffmpegAvailable()) {
        try {
          const mp4 = join(OUT, `${name}.mp4`);
          transcode(webm, mp4);
          file = mp4; format = 'mp4';
        } catch (e) {
          console.error(`⚠️  ffmpeg transcode failed (${e.message}) — keeping webm.`);
        }
      }
      const chapters = schedule.segments.map((s) => ({ start: s.start, label: s.label }));
      writeFileSync(join(OUT, `${name}.chapters.json`),
        JSON.stringify({ slug, duration: schedule.duration, chapters }, null, 2) + '\n');
      manifest.videos.push({
        slug, name, file, format,
        webm,
        duration_s: schedule.duration,
        bytes: statSync(file).size,
        commands: schedule.commands,
        dropped_commands: schedule.dropped,
        chapters,
        page_capture: leftPane.dataUri ? 'live' : 'fallback',
        quest: {
          title: q.title, permalink: q.permalink, path: q.path,
          level: q.level || plan.level.code, type: q.type || '', difficulty: q.difficulty || '',
        },
        evidence: result ? {
          overall: result.overall, verdict: result.verdict, mode: result.mode,
          executed: Boolean(result.verdict_obj && result.verdict_obj.executed),
        } : null,
      });
      console.error(`✅ ${file} (${(statSync(file).size / 1e6).toFixed(1)} MB, ${schedule.duration}s)`);
    } catch (e) {
      manifest.failures.push({ slug, error: e.message });
      console.error(`⚠️  recording failed for ${slug}: ${e.message}`);
    }
  }
} finally {
  await browser.close();
}

writeFileSync(join(OUT, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
console.error(`\n🎞️  ${manifest.videos.length} video(s) → ${OUT}/ (${manifest.failures.length} failure(s)). Manifest: ${join(OUT, 'manifest.json')}`);
process.exit(manifest.videos.length === 0 && selected.length > 0 ? 1 : 0);
