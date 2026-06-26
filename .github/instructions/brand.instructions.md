---
applyTo: "pages/_posts/**/*.md,pages/_quests/**/*.md,pages/_docs/**/*.md"
description: "Apply IT-Journey brand voice/tone/values to posts, quests, and docs: resolve the section guide, honor the voice profile, avoid banned terms"
date: 2026-06-21T00:00:00.000Z
lastmod: 2026-06-22T00:00:00.000Z
---

# Brand — applying voice & values to collection content

Brand **facts** (identity, values, voice, style, colors, personas) live in the
central store `_data/brand/`. This file tells you how to **apply** them when writing
**posts, quests, and docs**; it does not restate them (DRY). Structural rules stay
in each collection's own instructions
([`posts`](posts.instructions.md) · [`quest`](quest.instructions.md) · [`docs`](docs.instructions.md)).

## Which guide governs this file

Resolve in order (first hit wins):

1. the file's `voice_profile:` frontmatter; else
2. its `section_guide:` frontmatter → that guide's profile in `_data/brand/sections/_registry.yml`; else
3. **posts:** the folder `pages/_posts/<category>/…` → the `<category>` guide;
   **quests/docs:** the collection default in `_registry.yml › collection_defaults`
   (`quests → quest`, `docs → docs`); else
4. `_data/brand/voice.yml › default_profile` (`practitioner-chronicle`).

Both frontmatter keys are **optional** — a post in `pages/_posts/devops/`, any
quest, and any doc are already governed with no extra frontmatter. Add
`section_guide:` only to override (e.g. `devops-news-muse` for a short muse).

## The five voice profiles

| Profile | Used by |
|---|---|
| `practitioner-chronicle` | most posts (tutorials, AI-session chronicles) |
| `concept-essay` | idea/trend/business/culture posts |
| `muse-opinion` | short-form devops-news muses |
| `quest-fantasy` | the quest collection (gamified, emoji-rich) |
| `reference` | the docs collection (terse, scannable) |

## What to honor while writing

- **Voice:** read `_data/brand/voice.md` and the resolved
  `_data/brand/sections/<slug>.md`.
- **Values:** apply each principle's `writing_implication` from
  `_data/brand/values.yml` — DFF (honest about failures), DRY (link, don't
  re-explain), KIS (plain prose), AIPD (transparent about AI).
- **Style:** follow `_data/brand/style.md` (one H1, language tags on code, links
  not inline code).
- **Terms:** avoid the discouraged words — **comprehensive, powerful, seamless,
  cutting-edge, revolutionary, game-changing, effortless** — and use canonical
  spellings: **GitHub, JavaScript, CI/CD, VS Code, Node.js, Docker Compose**.
  (Some sections relax specific terms — e.g. quests relax `powerful` as fantasy
  flavor; see `.cms/config.yml › brand`.)
- **Section requirements:**
  - `devops` / `system-administration` posts must show a **Verify** step.
  - **muses** (`devops-news-muse`) are ~150–700 words, opinion-first.
  - **quests** keep the fantasy framing and the structure in
    `quest.instructions.md`; emoji density is not policed.
  - **docs** stay terse and low-emoji; answer-first, tables over prose.

## How it's checked

The CMS engine flags drift as advisory `brand_drift:*` issues for the collections
in `.cms/config.yml › brand.collections` (posts, quests, docs). It never blocks CI
and never changes the health score. Run `make cms-all` and read the **Brand drift by
section** table in `.cms/reports/<date>.md`, or use the `/brand-audit` prompt. To
draft/revise with the brand loaded, use the `brand-voice` skill. Vendored read-only
docs (any upstream content carrying `source_repo`/`source_url` frontmatter) are always skipped.

---

**Related:** [`posts.instructions.md`](posts.instructions.md) · [`quest.instructions.md`](quest.instructions.md) · [`docs.instructions.md`](docs.instructions.md) · the store `_data/brand/` · canonical frontmatter rules in [`../FRONTMATTER.md`](../FRONTMATTER.md).
