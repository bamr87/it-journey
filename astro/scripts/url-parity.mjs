#!/usr/bin/env node
/**
 * url-parity — does the Astro build serve every URL the Jekyll site serves?
 *
 * Reference set: the sitemap of the Jekyll build (the live site by default, or a
 * local `_site/sitemap.xml`), narrowed to one URL prefix. Compared against the
 * `index.html` files in `dist/`. Forwarding pages (redirect_from) are counted
 * apart from real pages.
 *
 *   node scripts/url-parity.mjs
 *   node scripts/url-parity.mjs --sitemap ../_site/sitemap.xml --prefix /quests/
 *
 * Exits 1 when a URL in the reference set is missing from the build.
 */
import { mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function option(name, fallback) {
  const index = process.argv.indexOf(`--${name}`);
  return index === -1 ? fallback : process.argv[index + 1];
}

const sitemap = option('sitemap', 'https://it-journey.dev/sitemap.xml');
const prefix = option('prefix', '/quests/');
const dist = path.resolve(root, option('dist', 'dist'));
const reportPath = path.resolve(root, option('report', 'reports/url-parity.json'));

async function walk(dir) {
  const out = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...(await walk(full)));
    else if (entry.name === 'index.html') out.push(full);
  }
  return out;
}

async function built() {
  const pages = new Set();
  const redirects = new Set();
  for (const file of await walk(dist)) {
    const url = `/${path.relative(dist, path.dirname(file)).split(path.sep).join('/')}/`.replace('//', '/');
    if (!url.startsWith(prefix)) continue;
    const html = await readFile(file, 'utf8');
    (/http-equiv="refresh"/i.test(html) ? redirects : pages).add(url);
  }
  return { pages, redirects };
}

async function reference() {
  const xml = /^https?:/.test(sitemap)
    ? await (async () => {
        const response = await fetch(sitemap);
        if (!response.ok) throw new Error(`${sitemap} answered ${response.status}`);
        return response.text();
      })()
    : await readFile(path.resolve(root, sitemap), 'utf8');
  const urls = new Set();
  for (const match of xml.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)) {
    const pathname = decodeURI(new URL(match[1]).pathname);
    if (pathname.startsWith(prefix)) urls.add(pathname);
  }
  return urls;
}

const [{ pages, redirects }, expected] = await Promise.all([built(), reference()]);

const missing = [...expected].filter((url) => !pages.has(url) && !redirects.has(url)).sort();
const nowRedirects = [...expected].filter((url) => redirects.has(url)).sort();
const extra = [...pages].filter((url) => !expected.has(url)).sort();
const matched = [...expected].filter((url) => pages.has(url)).length;

const report = {
  reference: sitemap,
  prefix,
  expected: expected.size,
  built: { pages: pages.size, redirects: redirects.size },
  matched,
  missing,
  servedAsRedirect: nowRedirects,
  onlyInBuild: extra,
};
await mkdir(path.dirname(reportPath), { recursive: true });
await writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`);

const list = (title, urls) => {
  if (!urls.length) return;
  console.log(`\n${title} (${urls.length})`);
  for (const url of urls) console.log(`  ${url}`);
};

console.log(`Reference: ${sitemap}  (prefix ${prefix})`);
console.log(`  ${expected.size} URLs in the Jekyll sitemap`);
console.log(`  ${pages.size} pages and ${redirects.size} redirects in the Astro build`);
console.log(`  ${matched} of ${expected.size} matched exactly`);
list('In the sitemap, missing from the build', missing);
list('In the sitemap, served as a redirect by the build', nowRedirects);
list('In the build, not in the sitemap', extra);
console.log(`\nReport: ${path.relative(process.cwd(), reportPath)}`);

process.exit(missing.length ? 1 : 0);
