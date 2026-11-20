/**
 * jekyll-loader — an Astro content loader that reads a Jekyll collection where
 * it already lives (`../pages/_quests`), so one set of Markdown files feeds both
 * builds during a migration.
 *
 * Per file: parse the front matter as YAML 1.1 (what Jekyll's Psych reads),
 * translate the body with jekyll-compat, validate against the collection schema
 * and render with Astro's Markdown pipeline. Nothing is written back to `pages/`.
 *
 * Everything that could not be carried over is written to
 * `reports/compat-report.json` instead of failing the build: the report is the
 * spike's deliverable.
 */
import { mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

import type { Loader, LoaderContext } from 'astro/loaders';
import { parse as parseYaml } from 'yaml';

import { buildIndex, splitFrontmatter, translate, type CompatIssue, type CompatStats } from './jekyll-compat.ts';

export interface JekyllCollectionOptions {
  /** collection directory, relative to the Astro project root */
  dir: string;
  /** repository root, relative to the Astro project root */
  repoRoot?: string;
  /** where to write the compatibility report, relative to the Astro project root */
  report?: string;
  /** Liquid outputs with a fixed value for this site */
  vars?: Record<string, string>;
  /**
   * Other content directories whose pages can be link targets (wikilinks and
   * relative `.md` links cross collections). Only their front matter is read.
   */
  linkTargets?: string[];
  /**
   * Front matter defaults, as in Jekyll's `defaults:` config: values applied to
   * every file under `path` (repo-relative) unless the file sets its own.
   */
  defaults?: Array<{ path: string; values: Record<string, unknown> }>;
  /** Extra titles a page is known by, e.g. navigation labels. */
  aliases?: (astroRoot: string) => Promise<Array<{ title: string; permalink: string }>>;
}

interface Skipped {
  file: string;
  reason: string;
}

const toPosix = (p: string) => p.split(path.sep).join('/');

async function walk(dir: string): Promise<string[]> {
  const out: string[] = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...(await walk(full)));
    else if (entry.isFile() && entry.name.endsWith('.md')) out.push(full);
  }
  return out;
}

function firstLine(error: unknown): string {
  const message = error instanceof Error ? error.message : String(error);
  return message.split('\n').map((l) => l.trim()).filter(Boolean).slice(0, 3).join(' · ').slice(0, 240);
}

async function sync(context: LoaderContext, options: JekyllCollectionOptions): Promise<void> {
  const { config, store, parseData, renderMarkdown, generateDigest, logger } = context;
  const astroRoot = fileURLToPath(config.root);
  const dir = path.resolve(astroRoot, options.dir);
  const repoRoot = path.resolve(astroRoot, options.repoRoot ?? '..');
  const started = performance.now();

  const skipped: Skipped[] = [];
  const unpublished: string[] = [];
  const docs: Array<{ abs: string; rel: string; raw: string; body: string; data: Record<string, unknown> }> = [];

  for (const abs of (await walk(dir)).sort()) {
    const raw = await readFile(abs, 'utf8');
    const rel = toPosix(path.relative(repoRoot, abs));
    const { frontmatter, body } = splitFrontmatter(raw);
    if (frontmatter === null) {
      // Jekyll copies a file without front matter verbatim; it is not a page.
      skipped.push({ file: rel, reason: 'no front matter' });
      continue;
    }
    try {
      const own = (parseYaml(frontmatter, { version: '1.1' }) ?? {}) as Record<string, unknown>;
      const inherited = (options.defaults ?? [])
        .filter((scope) => rel.startsWith(`${scope.path.replace(/\/+$/, '')}/`))
        .reduce<Record<string, unknown>>((values, scope) => ({ ...values, ...scope.values }), {});
      const data = { ...inherited, ...own };
      if (data.published === false) {
        // Jekyll does not build an unpublished page; neither do we.
        unpublished.push(rel);
        continue;
      }
      docs.push({ abs, rel, raw, body, data });
    } catch (error) {
      skipped.push({ file: rel, reason: `front matter YAML: ${firstLine(error)}` });
    }
  }

  // Pages outside this collection are link targets too; read their front matter only.
  const targets: Array<{ file: string; permalink?: unknown; title?: unknown }> = docs.map((d) => ({
    file: d.rel,
    permalink: d.data.permalink,
    title: d.data.title,
  }));
  for (const extra of options.linkTargets ?? []) {
    for (const abs of await walk(path.resolve(astroRoot, extra))) {
      if (abs.startsWith(dir + path.sep)) continue;
      const { frontmatter } = splitFrontmatter(await readFile(abs, 'utf8'));
      if (frontmatter === null) continue;
      try {
        const data = (parseYaml(frontmatter, { version: '1.1' }) ?? {}) as Record<string, unknown>;
        targets.push({ file: toPosix(path.relative(repoRoot, abs)), permalink: data.permalink, title: data.title });
      } catch {
        // Not this collection's problem; its own loader will report it.
      }
    }
  }
  const index = buildIndex(targets, (await options.aliases?.(astroRoot)) ?? []);

  const permalinks = new Map<string, string>();
  const duplicates: Array<{ permalink: string; files: string[] }> = [];
  const entries: Array<{ file: string; permalink: string; issues: CompatIssue[]; stats: CompatStats }> = [];

  store.clear();
  for (const doc of docs) {
    const id = toPosix(path.relative(dir, doc.abs)).replace(/\.md$/, '');
    const translated = translate(doc.body, {
      file: doc.rel,
      index,
      stripLeadingH1: doc.data.layout === 'quest',
      vars: options.vars,
    });

    let data: Record<string, unknown>;
    try {
      data = await parseData({
        id,
        data: { ...doc.data, source: doc.rel, compat: { issues: translated.issues, stats: translated.stats } },
        filePath: doc.abs,
      });
    } catch (error) {
      skipped.push({ file: doc.rel, reason: `schema: ${firstLine(error)}` });
      continue;
    }

    const permalink = String(data.permalink);
    const clash = permalinks.get(permalink);
    if (clash) {
      duplicates.push({ permalink, files: [clash, doc.rel] });
      skipped.push({ file: doc.rel, reason: `duplicate permalink ${permalink} (kept ${clash})` });
      continue;
    }
    permalinks.set(permalink, doc.rel);

    let rendered;
    try {
      rendered = await renderMarkdown(translated.body, { fileURL: pathToFileURL(doc.abs) });
    } catch (error) {
      skipped.push({ file: doc.rel, reason: `render: ${firstLine(error)}` });
      continue;
    }

    store.set({
      id,
      data,
      body: translated.body,
      filePath: toPosix(path.relative(astroRoot, doc.abs)),
      digest: generateDigest(doc.raw),
      rendered,
    });
    entries.push({ file: doc.rel, permalink, issues: translated.issues, stats: translated.stats });
  }

  // --- report ---------------------------------------------------------------
  const sum = (pick: (s: CompatStats) => number) => entries.reduce((n, e) => n + pick(e.stats), 0);
  const byKind: Record<string, { occurrences: number; files: number }> = {};
  for (const entry of entries) {
    const seen = new Set<string>();
    for (const issue of entry.issues) {
      const bucket = (byKind[issue.kind] ??= { occurrences: 0, files: 0 });
      bucket.occurrences += 1;
      if (!seen.has(issue.kind)) {
        bucket.files += 1;
        seen.add(issue.kind);
      }
    }
  }
  const report = {
    collection: context.collection,
    source: toPosix(path.relative(repoRoot, dir)),
    totals: {
      files:
        docs.length +
        unpublished.length +
        skipped.filter((s) => s.reason === 'no front matter' || s.reason.startsWith('front matter')).length,
      unpublished: unpublished.length,
      loaded: entries.length,
      skipped: skipped.length,
      clean: entries.filter((e) => e.issues.length === 0).length,
      withIssues: entries.filter((e) => e.issues.length > 0).length,
    },
    translated: {
      rawBlocks: sum((s) => s.rawBlocks),
      liquidComments: sum((s) => s.liquidComments),
      highlightBlocks: sum((s) => s.highlightBlocks),
      liquidOutputsSubstituted: sum((s) => s.liquidOutputsSubstituted),
      detailsFixed: sum((s) => s.detailsFixed),
      attributeListsStripped: sum((s) => s.attributeListsStripped),
      wikilinksResolved: sum((s) => s.wikilinksResolved),
      relativeLinksResolved: sum((s) => s.relativeLinksResolved),
      mermaidFences: sum((s) => s.mermaidFences),
      leadingH1Stripped: entries.filter((e) => e.stats.leadingH1Stripped).length,
    },
    issuesByKind: byKind,
    skipped,
    unpublished,
    duplicates,
    entries: entries.filter((e) => e.issues.length > 0).map(({ file, permalink, issues }) => ({ file, permalink, issues })),
  };

  if (options.report) {
    const reportPath = path.resolve(astroRoot, options.report);
    await mkdir(path.dirname(reportPath), { recursive: true });
    await writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`);
  }

  const ms = Math.round(performance.now() - started);
  logger.info(
    `${report.totals.loaded}/${report.totals.files} files loaded from ${report.source} in ${ms}ms ` +
      `(${report.totals.clean} clean, ${report.totals.withIssues} with unported Jekyll features, ${report.totals.skipped} skipped)`,
  );
  for (const skip of skipped) logger.warn(`skipped ${skip.file}: ${skip.reason}`);
}

const watched = new Set<string>();

export function jekyllCollection(options: JekyllCollectionOptions): Loader {
  return {
    name: 'jekyll-collection',
    async load(context) {
      await sync(context, options);

      // Dev server: re-read the collection when a source file changes.
      const dir = path.resolve(fileURLToPath(context.config.root), options.dir);
      if (!context.watcher || watched.has(dir)) return;
      watched.add(dir);
      context.watcher.add(dir);
      const onChange = (file: string) => {
        if (file.startsWith(dir) && file.endsWith('.md')) {
          sync(context, options).catch((error) => context.logger.error(firstLine(error)));
        }
      };
      context.watcher.on('add', onChange).on('change', onChange).on('unlink', onChange);
    },
  };
}
