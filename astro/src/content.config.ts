/**
 * Content collections for the spike.
 *
 * `quests` is read in place from the Jekyll collection (`../pages/_quests`).
 * `levels` and `tiers` are the files `make quest-data` already generates, loaded
 * as-is: the Python registry stays the source of truth.
 *
 * The quest schema is deliberately loose. `scripts/quest/quest_registry.py` and
 * the quest validator own the real rules; this one types what the layouts read
 * and catches a page that would render broken.
 */
import { readFile } from 'node:fs/promises';
import path from 'node:path';

import { defineCollection } from 'astro:content';
import { file } from 'astro/loaders';
import { z } from 'astro/zod';
import { parse as parseYaml } from 'yaml';

import { jekyllCollection } from './lib/jekyll-loader.ts';

const permalink = z.string().regex(/^\/(?:\S*\/)?$/, 'permalink must start and end with "/"');

/** YAML lists that are sometimes a bare scalar, sometimes missing. */
const list = z.preprocess(
  (value) => (value == null ? [] : Array.isArray(value) ? value : [value]),
  z.array(z.coerce.string()),
);
const text = z.coerce.string().optional();

/**
 * Older quests wrote `prerequisites:` and `rewards:` as a plain list. Fold that
 * into the current mapping shape so both generations render the same way.
 */
const legacyList = (key: string) => (value: unknown) => (Array.isArray(value) ? { [key]: value } : value);

interface NavItem {
  title?: string;
  url?: string;
  children?: NavItem[];
}

/** Navigation labels ("Level 0001 - Web Fundamentals") are how wikilinks name levels. */
async function navigationAliases(astroRoot: string) {
  const nav = parseYaml(await readFile(path.resolve(astroRoot, '../_data/navigation/quests.yml'), 'utf8')) as NavItem[];
  const out: Array<{ title: string; permalink: string }> = [];
  const visit = (items: NavItem[] = []) => {
    for (const item of items) {
      if (item.title && item.url?.startsWith('/')) out.push({ title: item.title, permalink: item.url });
      visit(item.children);
    }
  };
  visit(nav);
  return out;
}

const quests = defineCollection({
  loader: jekyllCollection({
    dir: '../pages/_quests',
    report: 'reports/compat-report.json',
    vars: { 'site.baseurl': '', 'site.url': 'https://it-journey.dev' },
    linkTargets: ['../pages'],
    aliases: navigationAliases,
    // Mirrors the one `defaults:` scope in _config.yml that decides whether a
    // page exists: authoring templates are scaffolds, not published pages.
    defaults: [{ path: 'pages/_quests/templates', values: { published: false } }],
  }),
  schema: z.looseObject({
    title: z.string().min(1),
    description: text,
    excerpt: text,
    permalink,
    layout: text,
    // Quoted 4-bit string on real quests; templates carry a placeholder.
    level: text,
    quest_type: text,
    fmContentType: text,
    difficulty: text,
    estimated_time: text,
    primary_technology: text,
    skill_focus: text,
    quest_series: text,
    draft: z.boolean().default(false),
    date: z.coerce.date().optional(),
    lastmod: z.coerce.date().optional(),
    tags: list,
    categories: list,
    redirect_from: list,
    prerequisites: z
      .preprocess(
        legacyList('knowledge_requirements'),
        z.looseObject({ knowledge_requirements: list, system_requirements: list }),
      )
      .optional(),
    quest_dependencies: z
      .looseObject({ required_quests: list, recommended_quests: list, unlocks_quests: list })
      .optional(),
    rewards: z
      .preprocess(
        legacyList('badges'),
        z.looseObject({ badges: list, skills_unlocked: list, progression_points: z.coerce.number().optional() }),
      )
      .optional(),
    // Added by the loader.
    source: z.string(),
    compat: z.object({
      issues: z.array(z.object({ kind: z.string(), detail: z.string() })),
      stats: z.record(z.string(), z.union([z.number(), z.boolean()])),
    }),
  }),
});

const yaml = { parser: (source: string) => parseYaml(source) };

const levels = defineCollection({
  loader: file('../_data/quests/levels.yml', yaml),
  schema: z.object({
    theme: z.string(),
    tier: z.string(),
    decimal: z.number(),
    xp_range: z.string(),
    permalink,
    tier_emoji: z.string(),
    icon: z.string().optional(),
  }),
});

const tiers = defineCollection({
  loader: file('../_data/quests/tiers.yml', yaml),
  schema: z.object({ emoji: z.string(), levels: z.array(z.string()) }),
});

export const collections = { quests, levels, tiers };
