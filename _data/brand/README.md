# `_data/brand/` — IT-Journey brand store

The **single source of truth** for the brand's identity, values, voice, style, colors, and audience — and the per-section narrative guides that govern how collection content (**posts, quests, and docs**, including the devops-news *muse* format) is written.

It lives under `_data/` so it is **build-consumed** (`site.data.brand.*`, addressable in layouts/includes) and sits beside the other site data. The CMS engine (`scripts/cms/cms.py`) and the `brand-voice` skill read these files directly.

## What lives here

| Path | What | Layer |
|---|---|---|
| `identity.yml` | name, tagline, team, niche, motifs | facts (YAML) |
| `values.yml` | 7 principles + 3 approaches + mission, each with a `writing_implication` | facts (YAML) |
| `colors.yml` | the 24-token palette + per-section accent/icon | facts (YAML) |
| `voice.yml` | the voice-profile registry (authoritative profile names) | facts (YAML) |
| `glossary.yml` | canonical spellings, stylizations, discouraged terms | facts (YAML) |
| `personas.yml` | audience personas (referenced by guides) | facts (YAML) |
| `voice.md` | the voice-and-tone bible (prose) | narrative (MD) |
| `style.md` | prose/formatting rules (prose) | narrative (MD) |
| `sections/_registry.yml` | slug → {title, permalink, voice_profile, personas, icon, accent} + `collection_defaults` | facts (YAML) |
| `sections/<slug>.md` | 13 post-category guides + `devops-news-muse.md` + `quest.md` + `docs.md` | narrative (MD) |

## The one rule: facts here, thresholds in the engine config

- **Brand facts** (values, voice pillars, palette, personas, glossary) live
  **here**.
- **Brand enforcement thresholds** (banned/preferred terms toggles, emoji count
ranges, formality targets, required structural elements) live in **`.cms/config.yml` → `brand`**, keyed by section slug.

The engine reads the thresholds from config and uses this store only to resolve which section/profile governs a post and to validate profile names. Guides and `.github/instructions/*` **point at** this store; they never restate it (DRY).

## How content resolves to a guide

1. The file's `voice_profile:` frontmatter, if set; else
2. its `section_guide:` frontmatter → that guide's profile in `_registry.yml`; else
3. **posts:** the folder (`pages/_posts/<category>/`) → the `<category>` guide;
**quests/docs:** `_registry.yml › collection_defaults` (`quests → quest`, `docs → docs`); else
4. `voice.yml: default_profile` (`practitioner-chronicle`).

So the two frontmatter keys are **optional** — every existing post, quest, and doc already resolves via its folder/collection.

## Consumers

- `scripts/cms/cms.py` (`_check_brand`) — flags brand drift into the daily worklist.
- `.claude/skills/brand-voice/SKILL.md` — loads this store before drafting/editing.
- `.github/prompts/{draft-article,draft-muse,brand-audit,…}.prompt.md`.
- `.github/instructions/brand.instructions.md` (auto-applies to `pages/_posts/**`,
  `pages/_quests/**`, `pages/_docs/**`).
- The site (later): `site.data.brand.*` for on-page rendering.
