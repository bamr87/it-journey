/**
 * repo-assets — serve the repository's existing `assets/` folder at `/assets/`
 * without copying it into this project or symlinking it (a tracked symlink
 * would break the legacy branch-based Pages build).
 *
 * dev:   a small static middleware reads straight from `../assets`.
 * build: the folder is copied into `dist/assets` once the build is done.
 */
import { createReadStream } from 'node:fs';
import { cp, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const MIME = {
  '.avif': 'image/avif',
  '.css': 'text/css; charset=utf-8',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
  '.jpeg': 'image/jpeg',
  '.jpg': 'image/jpeg',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.mp4': 'video/mp4',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.webm': 'video/webm',
  '.webp': 'image/webp',
  '.woff2': 'font/woff2',
};

/** @returns {import('astro').AstroIntegration} */
export function repoAssets({ from = '../assets', mount = '/assets' } = {}) {
  let source = '';
  return {
    name: 'repo-assets',
    hooks: {
      'astro:config:done': ({ config }) => {
        source = path.resolve(fileURLToPath(config.root), from);
      },
      'astro:server:setup': ({ server }) => {
        server.middlewares.use(mount, async (req, res, next) => {
          const pathname = decodeURIComponent((req.url ?? '/').split('?')[0]);
          const target = path.join(source, pathname);
          // Never serve anything outside the assets folder.
          if (!target.startsWith(source + path.sep)) return next();
          try {
            const info = await stat(target);
            if (!info.isFile()) return next();
            res.setHeader('Content-Type', MIME[path.extname(target).toLowerCase()] ?? 'application/octet-stream');
            res.setHeader('Content-Length', String(info.size));
            createReadStream(target).pipe(res);
          } catch {
            next();
          }
        });
      },
      'astro:build:done': async ({ dir, logger }) => {
        const destination = path.join(fileURLToPath(dir), mount);
        await cp(source, destination, { recursive: true });
        logger.info(`copied ${path.relative(process.cwd(), source)} → ${path.relative(process.cwd(), destination)}`);
      },
    },
  };
}
