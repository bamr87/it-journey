// video.mjs — step the presentation's players and capture each frame as a PNG.
// Usage: node video.mjs <presentation/index.html> <out-dir>
// Writes <out-dir>/fs/00000.png… (the file-system film, one per week) and
// <out-dir>/fe/00000.png… (every front-end page version). ffmpeg stitches them.
import { mkdirSync } from 'node:fs';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const [, , deck, out] = process.argv;
const pad = (n) => String(n).padStart(5, '0');

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, colorScheme: 'light', deviceScaleFactor: 1 });
await page.route('**/*', (r) => (r.request().url().startsWith('file:') ? r.continue() : r.abort()));
await page.goto(pathToFileURL(deck).href);
await page.waitForFunction(() => window.chronicle);
await page.addStyleTag({ content: '.bar{display:none!important} *{transition:none!important}' });

mkdirSync(`${out}/fs`, { recursive: true });
const film = page.locator('.film');
await film.scrollIntoViewIfNeeded();
const frames = await page.evaluate(() => window.chronicle.frames);
for (let i = 0; i < frames; i += 1) {
  await page.evaluate((k) => window.chronicle.film.go(k, false), i);
  await page.waitForTimeout(30);
  await film.screenshot({ path: `${out}/fs/${pad(i)}.png` });
}

mkdirSync(`${out}/fe`, { recursive: true });
const flip = page.locator('.flip');
let n = 0;
const pages = await page.evaluate(() => window.chronicle.flip.count);
for (let p = 0; p < pages; p += 1) {
  await page.evaluate((k) => window.chronicle.flip.select(k), p);
  const count = await page.evaluate(() => +document.querySelector('#fe-range').max + 1);
  for (let i = 0; i < count; i += 1) {
    await page.evaluate((k) => { const r = document.querySelector('#fe-range'); r.value = k; r.dispatchEvent(new Event('input')); }, i);
    await page.waitForFunction(() => document.querySelector('#fe-img').complete);
    await flip.screenshot({ path: `${out}/fe/${pad(n)}.png` });
    n += 1;
  }
}
await browser.close();
console.log(JSON.stringify({ fs: frames, fe: n }));
