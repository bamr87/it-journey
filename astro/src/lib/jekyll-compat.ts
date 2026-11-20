/**
 * jekyll-compat — translate one Jekyll/kramdown Markdown body into plain
 * CommonMark at load time, without touching the file on disk.
 *
 * Jekyll renders a page in two passes: Liquid over the raw file, then kramdown.
 * This module mirrors that order so the same source keeps building under Jekyll
 * while Astro reads it:
 *
 *   1. Liquid   raw blocks unwrapped, comments dropped, `highlight` turned into
 *               fences, known `{{ … }}` outputs substituted. Anything else is
 *               removed and reported: it is template logic that needs a port.
 *   2. kramdown `markdown="1"` on <details>, attribute lists (`{: .x}`),
 *               Obsidian wikilinks and relative `.md` links resolved to
 *               permalinks.
 *
 * Pure functions only (no fs, no Astro) so `node --test` can exercise them.
 */

export type IssueKind =
  | 'liquid-tag'
  | 'liquid-output'
  | 'liquid-in-code'
  | 'wikilink-unresolved'
  | 'relative-link-unresolved';

export interface CompatIssue {
  kind: IssueKind;
  detail: string;
}

export interface CompatStats {
  rawBlocks: number;
  liquidComments: number;
  highlightBlocks: number;
  liquidOutputsSubstituted: number;
  detailsFixed: number;
  attributeListsStripped: number;
  wikilinksResolved: number;
  relativeLinksResolved: number;
  mermaidFences: number;
  leadingH1Stripped: boolean;
}

export interface LinkIndex {
  /** normalized title → permalink */
  byTitle: Map<string, string>;
  /** repo-relative posix path (`pages/_quests/0001/foo.md`) → permalink */
  byPath: Map<string, string>;
  /** file basename without extension, lowercased → permalink */
  byBasename: Map<string, string>;
}

export interface TranslateContext {
  /** repo-relative posix path of the file being translated */
  file: string;
  index: LinkIndex;
  /** drop the body's first heading when it is an H1 (the layout renders the title) */
  stripLeadingH1?: boolean;
  /** Liquid outputs with a known value, e.g. `{ 'site.baseurl': '' }` */
  vars?: Record<string, string>;
}

export interface TranslateResult {
  body: string;
  issues: CompatIssue[];
  stats: CompatStats;
}

/** Stands in for `{` inside raw blocks so later passes do not read it as Liquid. */
const SENTINEL = '';

const FRONTMATTER_RE = /^﻿?---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)([\s\S]*)$/;

export function splitFrontmatter(raw: string): { frontmatter: string | null; body: string } {
  const match = FRONTMATTER_RE.exec(raw);
  if (!match) return { frontmatter: null, body: raw };
  return { frontmatter: match[1] ?? '', body: match[2] ?? '' };
}

export function normalizeTitle(title: string): string {
  return title.normalize('NFKC').toLowerCase().replace(/\s+/g, ' ').trim();
}

export function buildIndex(
  docs: Array<{ file: string; permalink?: unknown; title?: unknown }>,
  aliases: Array<{ title: string; permalink: string }> = [],
): LinkIndex {
  const index: LinkIndex = { byTitle: new Map(), byPath: new Map(), byBasename: new Map() };
  for (const doc of docs) {
    if (typeof doc.permalink !== 'string' || !doc.permalink) continue;
    index.byPath.set(doc.file, doc.permalink);
    const base = doc.file.split('/').pop()!.replace(/\.md$/i, '').toLowerCase();
    // README.md is every directory's index; it is only addressable by path or title.
    if (base !== 'readme' && !index.byBasename.has(base)) index.byBasename.set(base, doc.permalink);
    if (typeof doc.title === 'string' && doc.title) {
      const key = normalizeTitle(doc.title);
      if (!index.byTitle.has(key)) index.byTitle.set(key, doc.permalink);
    }
  }
  // Extra names a page is known by (navigation labels, say). Real titles win.
  for (const alias of aliases) {
    const key = normalizeTitle(alias.title);
    if (!index.byTitle.has(key)) index.byTitle.set(key, alias.permalink);
  }
  return index;
}

/* ------------------------------------------------------------------ */
/* Fences                                                              */
/* ------------------------------------------------------------------ */

interface Segment {
  code: boolean;
  /** info string of the opening fence (code segments only) */
  info: string;
  lines: string[];
}

const FENCE_RE = /^\s*(?:>\s*)*(`{3,}|~{3,})(.*)$/;

/** Split into fenced-code and prose segments. Good enough for kramdown/GFM input. */
function splitFences(text: string): Segment[] {
  const segments: Segment[] = [];
  let current: Segment = { code: false, info: '', lines: [] };
  let open: { char: string; length: number } | null = null;

  for (const line of text.split('\n')) {
    const match = FENCE_RE.exec(line);
    if (!open) {
      const marker = match?.[1];
      const info = match?.[2] ?? '';
      // A backtick fence cannot carry backticks in its info string (that is inline code).
      if (marker && !(marker[0] === '`' && info.includes('`'))) {
        if (current.lines.length) segments.push(current);
        current = { code: true, info: info.trim(), lines: [line] };
        open = { char: marker[0]!, length: marker.length };
        continue;
      }
      current.lines.push(line);
      continue;
    }
    current.lines.push(line);
    const marker = match?.[1];
    if (marker && marker[0] === open.char && marker.length >= open.length && !(match?.[2] ?? '').trim()) {
      segments.push(current);
      current = { code: false, info: '', lines: [] };
      open = null;
    }
  }
  if (current.lines.length) segments.push(current);
  return segments;
}

/** Apply `fn` to prose only, leaving inline code spans untouched. */
function outsideInlineCode(text: string, fn: (prose: string) => string): string {
  return text
    .split(/(``[^\n]*?``|`[^`\n]*`)/g)
    .map((part, i) => (i % 2 === 0 ? fn(part) : part))
    .join('');
}

/* ------------------------------------------------------------------ */
/* Pass 1 — Liquid                                                     */
/* ------------------------------------------------------------------ */

const RAW_RE = /\{%-?\s*raw\s*-?%\}([\s\S]*?)\{%-?\s*endraw\s*-?%\}/g;
const COMMENT_RE = /\{%-?\s*comment\s*-?%\}[\s\S]*?\{%-?\s*endcomment\s*-?%\}/g;
const HIGHLIGHT_RE = /\{%-?\s*highlight\s+([\w+#-]+)[^%]*%\}\n?([\s\S]*?)\n?\{%-?\s*endhighlight\s*-?%\}/g;
const OUTPUT_RE = /\{\{-?\s*([\s\S]*?)\s*-?\}\}/g;
const TAG_RE = /\{%-?\s*([a-z_]+)\s*([\s\S]*?)\s*-?%\}/g;
/** `{{ '/path' | relative_url }}` and friends: the literal is the value. */
const URL_LITERAL_RE = /^(['"])(.*?)\1\s*\|\s*(?:relative_url|absolute_url|prepend:\s*site\.baseurl)\s*$/;

function resolveOutput(expression: string, vars: Record<string, string>): string | null {
  const direct = vars[expression];
  if (direct !== undefined) return direct;
  const literal = URL_LITERAL_RE.exec(expression);
  if (literal) return literal[2] ?? '';
  return null;
}

/* ------------------------------------------------------------------ */
/* Pass 2 — kramdown                                                   */
/* ------------------------------------------------------------------ */

/** `{: .class}`, `{: #id}`, `{:toc}`, `{:target="_blank"}` */
const ATTR_LIST = String.raw`\{:\s*(?:[.#][\w-]+|toc\b|\w+=)[^}\n]*\}`;
const ATTR_LIST_LINE_RE = new RegExp(String.raw`^\s*${ATTR_LIST}\s*$`);
const ATTR_LIST_INLINE_RE = new RegExp(String.raw`[ \t]*${ATTR_LIST}`, 'g');
const TOC_MARKER_RE = /^\s*[*+-]\s+toc\s*$/i;

const WIKILINK_RE = /(!?)\[\[([^\s[\]|#][^[\]\n|#]*)(?:#([^[\]\n|]*))?(?:\|([^[\]\n]+))?\]\]/g;
const MD_LINK_RE = /(\]\()(<?)([^)\s<>]+?\.md)(#[^)\s<>]*)?(>?)(\s+"[^"]*")?(\))/gi;

const DETAILS_MD_OPEN_RE = /<details\b[^>]*\bmarkdown\s*=\s*(["'])(?:1|block)\1[^>]*>/i;
const MARKDOWN_ATTR_RE = /\s+markdown\s*=\s*(["'])(?:1|block|span)\1/gi;

function posixDirname(file: string): string {
  const i = file.lastIndexOf('/');
  return i === -1 ? '' : file.slice(0, i);
}

function posixResolve(fromDir: string, href: string): string {
  const out: string[] = href.startsWith('/') ? [] : fromDir.split('/').filter(Boolean);
  for (const part of href.split('/')) {
    if (!part || part === '.') continue;
    if (part === '..') out.pop();
    else out.push(part);
  }
  return out.join('/');
}

function safeDecode(value: string): string {
  try {
    return decodeURIComponent(value);
  } catch {
    return value;
  }
}

export function translate(source: string, ctx: TranslateContext): TranslateResult {
  const issues: CompatIssue[] = [];
  const stats: CompatStats = {
    rawBlocks: 0,
    liquidComments: 0,
    highlightBlocks: 0,
    liquidOutputsSubstituted: 0,
    detailsFixed: 0,
    attributeListsStripped: 0,
    wikilinksResolved: 0,
    relativeLinksResolved: 0,
    mermaidFences: 0,
    leadingH1Stripped: false,
  };
  const vars = ctx.vars ?? {};
  const dir = posixDirname(ctx.file);

  // --- Liquid, whole document -------------------------------------------------
  let text = source.replace(/\r\n?/g, '\n');

  // Raw blocks are literal text. Hide their `{` so nothing below reads it as Liquid.
  text = text.replace(RAW_RE, (_all, inner: string) => {
    stats.rawBlocks += 1;
    return inner.replace(/\{(?=[{%])/g, SENTINEL);
  });
  text = text.replace(COMMENT_RE, () => {
    stats.liquidComments += 1;
    return '';
  });
  text = text.replace(HIGHLIGHT_RE, (_all, lang: string, code: string) => {
    stats.highlightBlocks += 1;
    return `\n\`\`\`${lang}\n${code.replace(/\{(?=[{%])/g, SENTINEL)}\n\`\`\`\n`;
  });

  // --- Per segment: Liquid leftovers, then inline kramdown ------------------
  const segments = splitFences(text);
  for (const segment of segments) {
    if (segment.code) {
      if (/^\{?\.?mermaid\b/i.test(segment.info)) stats.mermaidFences += 1;
      const joined = segment.lines.join('\n');
      // Jekyll would evaluate these (usually to nothing). Keep them literal: it is a
      // code sample the author forgot to wrap in raw.
      const leftovers = joined.match(/\{\{[\s\S]*?\}\}|\{%[\s\S]*?%\}/g);
      for (const leftover of leftovers ?? []) {
        issues.push({ kind: 'liquid-in-code', detail: leftover.replace(/\s+/g, ' ').slice(0, 80) });
      }
      continue;
    }

    let prose = segment.lines.join('\n');

    prose = prose.replace(OUTPUT_RE, (_all, expression: string) => {
      const value = resolveOutput(expression.trim(), vars);
      if (value !== null) {
        stats.liquidOutputsSubstituted += 1;
        return value;
      }
      issues.push({ kind: 'liquid-output', detail: expression.replace(/\s+/g, ' ').trim().slice(0, 80) });
      return '';
    });
    prose = prose.replace(TAG_RE, (_all, name: string, args: string) => {
      issues.push({ kind: 'liquid-tag', detail: `${name} ${args.replace(/\s+/g, ' ')}`.trim().slice(0, 80) });
      return '';
    });

    prose = outsideInlineCode(prose, (part) => {
      let out = part.replace(WIKILINK_RE, (all, bang: string, target: string, _heading, alias?: string) => {
        const name = target.trim();
        const label = (alias ?? name).trim();
        const href =
          ctx.index.byTitle.get(normalizeTitle(name)) ??
          ctx.index.byBasename.get(name.split('/').pop()!.replace(/\.md$/i, '').toLowerCase());
        if (bang || !href) {
          issues.push({ kind: 'wikilink-unresolved', detail: all.slice(0, 80) });
          return label;
        }
        stats.wikilinksResolved += 1;
        // The label is literal text. Escape the backslash too, or a label ending in one would
        // escape the closing bracket and break the link.
        return `[${label.replace(/[\\[\]]/g, '\\$&')}](${href})`;
      });

      out = out.replace(MD_LINK_RE, (all, open: string, lt: string, href: string, hash = '', gt: string, title = '', close: string) => {
        if (/^[a-z][a-z0-9+.-]*:/i.test(href) || href.startsWith('//')) return all;
        const target = posixResolve(dir, safeDecode(href));
        const permalink = ctx.index.byPath.get(target);
        if (!permalink) {
          issues.push({ kind: 'relative-link-unresolved', detail: href.slice(0, 80) });
          return all;
        }
        stats.relativeLinksResolved += 1;
        return `${open}${lt}${permalink}${hash}${gt}${title}${close}`;
      });

      out = out.replace(ATTR_LIST_INLINE_RE, (match, offset: number, whole: string) => {
        // A line that is nothing but an attribute list is handled in the line pass.
        const lineStart = whole.lastIndexOf('\n', offset - 1) + 1;
        const lineEnd = whole.indexOf('\n', offset);
        const line = whole.slice(lineStart, lineEnd === -1 ? undefined : lineEnd);
        if (ATTR_LIST_LINE_RE.test(line)) return match;
        stats.attributeListsStripped += 1;
        return '';
      });
      return out;
    });

    segment.lines = prose.split('\n');
  }

  // --- Line pass: block-level kramdown, fence-aware --------------------------
  const out: string[] = [];
  let detailsDepth = 0;
  let sawHeading = false;
  const pushBlank = () => {
    if (out.length && out[out.length - 1]!.trim() !== '') out.push('');
  };

  // Flattened so a lookahead can see across a prose/fence boundary.
  const flat = segments.flatMap((segment) => segment.lines.map((text) => ({ text, code: segment.code })));
  const lines = flat.map((entry) => entry.text);

  for (let i = 0; i < flat.length; i += 1) {
    {
      let line = lines[i]!;
      if (flat[i]!.code) {
        out.push(line);
        continue;
      }

      if (ATTR_LIST_LINE_RE.test(line)) {
        stats.attributeListsStripped += 1;
        // `* TOC` + `{:toc}` is kramdown's table-of-contents marker; drop both.
        if (/\{:\s*toc\b/i.test(line) && out.length && TOC_MARKER_RE.test(out[out.length - 1]!)) out.pop();
        continue;
      }

      if (!sawHeading && /^#{1,6}\s+\S/.test(line)) {
        sawHeading = true;
        if (ctx.stripLeadingH1 && /^#\s+\S/.test(line)) {
          stats.leadingH1Stripped = true;
          if (lines[i + 1]?.trim() === '') i += 1;
          continue;
        }
      }

      const opensMarkdownDetails = DETAILS_MD_OPEN_RE.test(line);
      if (MARKDOWN_ATTR_RE.test(line)) line = line.replace(MARKDOWN_ATTR_RE, '');
      MARKDOWN_ATTR_RE.lastIndex = 0;

      if (opensMarkdownDetails) {
        detailsDepth += 1;
        stats.detailsFixed += 1;
        out.push(line);
        // CommonMark only parses Markdown inside an HTML block after a blank line.
        const next = lines[i + 1] ?? '';
        if (/<\/summary>/i.test(line) || !/^\s*<summary\b/i.test(next)) {
          if (next.trim() !== '') out.push('');
        }
        continue;
      }

      if (detailsDepth > 0) {
        if (/<\/details>/i.test(line)) {
          detailsDepth -= 1;
          if (/^\s*<\/details>/i.test(line)) pushBlank();
          out.push(line);
          continue;
        }
        if (/<\/summary>/i.test(line)) {
          out.push(line);
          if ((lines[i + 1] ?? '').trim() !== '') out.push('');
          continue;
        }
      }

      out.push(line);
    }
  }

  return {
    body: out.join('\n').replaceAll(SENTINEL, '{'),
    issues,
    stats,
  };
}
