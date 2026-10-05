#!/usr/bin/env node
// serve-site.mjs — serve a built Jekyll `_site` the way GitHub Pages does, so
// Lighthouse/axe/pa11y measure something close to production:
//   * gzip for text responses (Pages compresses; transfer-size budgets are
//     meaningless against uncompressed bytes),
//   * `/dir/` -> `/dir/index.html`, `/dir` -> 301 `/dir/`, `/page` -> `/page.html`,
//   * the site's own `404.html` with HTTP 404,
//   * `cache-control: max-age=600` (what Pages sends; the cache-policy audits are
//     switched off in lighthouserc.cjs because that header can't be changed).
// No dependencies (node:http + node:zlib) so it starts in milliseconds in CI.
//
// Usage: node serve-site.mjs [siteDir=_site] [port=4000]
import { createServer } from 'node:http';
import { createReadStream, statSync, existsSync } from 'node:fs';
import { extname, join, normalize, resolve, sep } from 'node:path';
import { createGzip } from 'node:zlib';

const root = resolve(process.argv[2] || '_site');
const port = Number(process.argv[3] || process.env.PORT || 4000);
const host = process.env.HOST || '127.0.0.1';

const TYPES = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp',
  '.avif': 'image/avif', '.ico': 'image/x-icon', '.woff': 'font/woff', '.woff2': 'font/woff2',
  '.ttf': 'font/ttf', '.otf': 'font/otf', '.webmanifest': 'application/manifest+json',
  '.map': 'application/json; charset=utf-8', '.pdf': 'application/pdf', '.mp4': 'video/mp4',
};
const COMPRESSIBLE = /^(text\/|application\/(json|xml|manifest\+json|javascript)|image\/svg\+xml)/;

if (!existsSync(root)) {
  console.error(`serve-site: ${root} does not exist — build the site first`);
  process.exit(2);
}

const isFile = (p) => { try { return statSync(p).isFile(); } catch { return false; } };
const isDir = (p) => { try { return statSync(p).isDirectory(); } catch { return false; } };

function send(req, res, file, status = 200) {
  const type = TYPES[extname(file).toLowerCase()] || 'application/octet-stream';
  const headers = { 'content-type': type, 'cache-control': 'max-age=600', vary: 'Accept-Encoding' };
  const gzip = COMPRESSIBLE.test(type) && /\bgzip\b/.test(req.headers['accept-encoding'] || '');
  if (gzip) headers['content-encoding'] = 'gzip';
  else headers['content-length'] = statSync(file).size;
  res.writeHead(status, headers);
  if (req.method === 'HEAD') return res.end();
  const stream = createReadStream(file);
  (gzip ? stream.pipe(createGzip()) : stream).pipe(res);
}

createServer((req, res) => {
  let pathname;
  try {
    pathname = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  } catch {
    res.writeHead(400).end('bad request');
    return;
  }
  const target = normalize(join(root, pathname));
  if (target !== root && !target.startsWith(root + sep)) {
    res.writeHead(403).end('forbidden');
    return;
  }
  if (isDir(target)) {
    if (!pathname.endsWith('/')) {
      const q = req.url.includes('?') ? req.url.slice(req.url.indexOf('?')) : '';
      res.writeHead(301, { location: `${pathname}/${q}` }).end();
      return;
    }
    if (isFile(join(target, 'index.html'))) return send(req, res, join(target, 'index.html'));
  } else if (isFile(target)) {
    return send(req, res, target);
  } else if (isFile(`${target}.html`)) {
    return send(req, res, `${target}.html`);
  }
  const notFound = join(root, '404.html');
  if (isFile(notFound)) return send(req, res, notFound, 404);
  res.writeHead(404, { 'content-type': 'text/plain' }).end('not found');
})
  .on('error', (e) => {
    console.error(`serve-site: ${e.code === 'EADDRINUSE' ? `port ${port} is already in use` : e.message}`);
    process.exit(1);
  })
  .listen(port, host, () => {
    console.log(`serve-site: ${root} on http://${host}:${port}/`);
  });
