// shot.mjs — screenshot rendered chronicle frames with Playwright.
// Usage: node shot.mjs <jobs.json>  ({width, height, jobs: [{html, png}]})
// Every non-file request is aborted, so a frame shows only what the commit held.
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const spec = JSON.parse(readFileSync(process.argv[2], 'utf8'));

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: spec.width, height: spec.height },
  deviceScaleFactor: 1,
  reducedMotion: 'reduce',
});
await context.route('**/*', (route) => {
  const url = route.request().url();
  if (url.startsWith('file:') || url.startsWith('data:') || url.startsWith('about:')) return route.continue();
  return route.abort();
});
const page = await context.newPage();
page.setDefaultTimeout(15000);
let done = 0;
for (const job of spec.jobs) {
  try {
    await page.goto(pathToFileURL(job.html).href, { waitUntil: 'load' });
    await page.waitForTimeout(250);
    await page.screenshot({ path: job.png, clip: { x: 0, y: 0, width: spec.width, height: spec.height } });
    done += 1;
  } catch (err) {
    console.error(`frame failed: ${job.html}: ${err.message}`);
  }
}
await browser.close();
console.log(`${done}/${spec.jobs.length} frames`);
