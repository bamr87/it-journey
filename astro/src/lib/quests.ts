/**
 * Read-side helpers over the quest collection: ordering inside a level,
 * previous/next, and the small label lookups the templates share.
 */
import { getCollection, type CollectionEntry } from 'astro:content';

export type Quest = CollectionEntry<'quests'>;
export type Level = CollectionEntry<'levels'>;
export type Tier = CollectionEntry<'tiers'>;

export interface World {
  all: Quest[];
  byPermalink: Map<string, Quest>;
  /** real quests per level, in play order */
  byLevel: Map<string, Quest[]>;
  /** levels in path order (0000 → 1111) */
  levels: Level[];
  tiers: Tier[];
}

const LEVEL_RE = /^[01]{4}$/;
const TYPE_ORDER = ['main_quest', 'epic_quest', 'side_quest', 'bonus_quest'];
const TYPE_LABEL: Record<string, string> = {
  main_quest: 'Main quest',
  epic_quest: 'Epic quest',
  side_quest: 'Side quest',
  bonus_quest: 'Bonus quest',
};

export const REPO_URL = 'https://github.com/bamr87/it-journey';

export const isQuest = (entry: Quest): boolean =>
  entry.data.layout === 'quest' && LEVEL_RE.test(entry.data.level ?? '');

export const typeLabel = (entry: Quest): string => TYPE_LABEL[entry.data.quest_type ?? ''] ?? 'Quest';

export const xp = (entry: Quest): number | undefined => entry.data.rewards?.progression_points;

/** Dependency lists store permalinks, sometimes with a `#fragment`. */
export const stripHash = (url: string): string => url.split('#')[0]!.trim();

const typeRank = (entry: Quest): number => {
  const rank = TYPE_ORDER.indexOf(entry.data.quest_type ?? '');
  return rank === -1 ? TYPE_ORDER.length : rank;
};

/**
 * Play order for one level: main quests before side quests, and a quest after
 * the quests in the same level it requires. Title breaks ties, so the order is
 * stable from build to build.
 */
function orderLevel(quests: Quest[]): Quest[] {
  const seed = [...quests].sort(
    (a, b) => typeRank(a) - typeRank(b) || a.data.title.localeCompare(b.data.title),
  );
  const inLevel = new Map(seed.map((quest) => [quest.data.permalink, quest]));
  const placed = new Set<string>();
  const ordered: Quest[] = [];

  const visit = (quest: Quest, trail: Set<string>) => {
    const key = quest.data.permalink;
    if (placed.has(key) || trail.has(key)) return;
    trail.add(key);
    for (const required of quest.data.quest_dependencies?.required_quests ?? []) {
      const dependency = inLevel.get(stripHash(required));
      if (dependency && typeRank(dependency) <= typeRank(quest)) visit(dependency, trail);
    }
    placed.add(key);
    ordered.push(quest);
  };
  for (const quest of seed) visit(quest, new Set());
  return ordered;
}

async function load(): Promise<World> {
  const [all, levels, tiers] = await Promise.all([
    getCollection('quests'),
    getCollection('levels'),
    getCollection('tiers'),
  ]);
  const byPermalink = new Map(all.map((entry) => [entry.data.permalink, entry]));

  const grouped = new Map<string, Quest[]>();
  for (const entry of all) {
    if (!isQuest(entry)) continue;
    const level = entry.data.level!;
    grouped.set(level, [...(grouped.get(level) ?? []), entry]);
  }
  const byLevel = new Map([...grouped].map(([level, quests]) => [level, orderLevel(quests)]));

  return {
    all,
    byPermalink,
    byLevel,
    levels: [...levels].sort((a, b) => a.data.decimal - b.data.decimal),
    tiers,
  };
}

let cached: Promise<World> | undefined;

/** One read of the collections per build; always fresh on the dev server. */
export function world(): Promise<World> {
  if (import.meta.env.DEV) return load();
  return (cached ??= load());
}

export interface QuestLink {
  title: string;
  href: string;
}

const toLink = (entry: Quest | undefined): QuestLink | undefined =>
  entry && { title: entry.data.title, href: entry.data.permalink };

/**
 * Previous and next quest. Declared dependencies win (the first required quest,
 * the first quest this one unlocks); the level's play order fills the gaps so a
 * learner always has somewhere to go next.
 */
export function neighbours(entry: Quest, w: World): { prev?: QuestLink; next?: QuestLink } {
  const list = w.byLevel.get(entry.data.level ?? '') ?? [];
  const index = list.findIndex((quest) => quest.id === entry.id);
  const resolve = (urls: string[] = []) =>
    urls.map((url) => w.byPermalink.get(stripHash(url))).find((quest) => quest && quest.id !== entry.id);

  const deps = entry.data.quest_dependencies;
  return {
    prev: toLink(resolve(deps?.required_quests) ?? (index > 0 ? list[index - 1] : undefined)),
    next: toLink(resolve(deps?.unlocks_quests) ?? (index >= 0 ? list[index + 1] : undefined)),
  };
}

export function requiredQuests(entry: Quest, w: World): QuestLink[] {
  return (entry.data.quest_dependencies?.required_quests ?? []).map((url) => {
    const target = w.byPermalink.get(stripHash(url));
    return { title: target?.data.title ?? url, href: stripHash(url) };
  });
}

export const levelFor = (code: string | undefined, w: World): Level | undefined =>
  w.levels.find((level) => level.id === code);

export const tierSlug = (tier: string): string => tier.toLowerCase().replace(/[^a-z]+/g, '-');
