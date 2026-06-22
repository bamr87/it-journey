---
applyTo: "pages/_posts/**/*.md"
description: "Apply IT-Journey brand voice/tone/values to posts: resolve the section guide, honor the voice profile, and avoid banned terms"
date: 2026-06-21T00:00:00.000Z
lastmod: 2026-06-21T00:00:00.000Z
---

# Brand — applying voice & values to posts

Brand **facts** (identity, values, voice, style, colors, personas) live in the
central store `_data/brand/`. This file tells you how to **apply** them when
writing a post; it does not restate them (DRY). Structural post rules (frontmatter,
filenames, permalinks, CI gates) stay in [`posts.instructions.md`](posts.instructions.md).

## Which guide governs this post

Resolve in order (first hit wins):

1. the post's `voice_profile:` frontmatter; else
2. its `section_guide:` frontmatter → that guide's profile in `_data/brand/sections/_registry.yml`; else
3. the folder: `pages/_posts/<category>/…` → the `<category>` guide; else
4. `_data/brand/voice.yml › default_profile` (`practitioner-chronicle`).

Both frontmatter keys are **optional** — a post in `pages/_posts/devops/` is already
governed by the `devops` guide with no extra frontmatter. Add `section_guide:` only
to override (e.g. `devops-news-muse` for a short opinion piece).

## The two optional keys

```yaml
section_guide: devops            # a slug from _data/brand/sections/_registry.yml
voice_profile: practitioner-chronicle  # override; usually omit — the guide decides
```

## What to honor while writing

- **Voice:** read `_data/brand/voice.md` and the section's
  `_data/brand/sections/<slug>.md`. Match the resolved profile
  (`practitioner-chronicle` | `concept-essay` | `muse-opinion`).
- **Values:** apply each principle's `writing_implication` from
  `_data/brand/values.yml` — especially DFF (be honest about failures), DRY (link
  the canonical doc, don't re-explain), KIS (plain prose), AIPD (transparent about AI).
- **Style:** follow `_data/brand/style.md` (imperative for steps, past tense for
  chronicles, one H1, language tags on every code block, links not inline code).
- **Terms:** never use the discouraged words — **comprehensive, powerful, seamless,
  cutting-edge, revolutionary, game-changing, effortless** — and use canonical
  spellings: **GitHub, JavaScript, CI/CD, VS Code, Node.js, Docker Compose**.
- **Section requirements:** `devops` and `system-administration` posts must show a
  **Verify** step; **muses** (`devops-news-muse`) are ~150–700 words, opinion-first.

## How it's checked

The CMS engine flags drift as advisory `brand_drift:*` issues (see
`.cms/config.yml › brand`). It never blocks CI and never changes the health score.
Run `make cms-all` and read the **Brand drift by section** table in
`.cms/reports/<date>.md`, or use the `/brand-audit` prompt. To draft/revise with the
brand loaded, use the `brand-voice` skill.

---

**Related:** [`posts.instructions.md`](posts.instructions.md) · [`index-hub.instructions.md`](index-hub.instructions.md) · the store `_data/brand/` · canonical frontmatter rules in [`../FRONTMATTER.md`](../FRONTMATTER.md).
