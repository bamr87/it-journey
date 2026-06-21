# IT-Journey — Branding & Content-Governance System (plan)

> Status: plan. This document specifies a central branding layer for collection
> content and how it wires into the existing CMS engine, skills, prompts, and
> editor instructions. Scope is **posts only** for the first iteration.

IT-Journey has rich brand raw material scattered across the repo — the mission and
seven core principles in `pages/_about/about.md`, the philosophy in
`pages/_about/purpose.md`, identity plus a 24-token color palette in `_config.yml`,
and the "Chronicles: From Zer0 to Her0" magazine framing in `pages/news.md` — but
**no single, loadable place that tells an author (human or agent) how the brand
sounds, what it values, who it writes for, and how each posts section differs.**
When drafting a new article or a short-form devops-news "muse," there is no governing
voice/tone/style guide to pull from, and no automated way to catch brand drift on
existing content.

This plan builds a **central brand store** (the source of truth for tone, style,
color, team, values, niche), a backbone of **per-section narrative guides**, three
**consumption surfaces** (a Claude skill, slash prompts, editor instructions), and an
**extension of the `.cms` engine** that scores brand drift in the daily worklist.

It is the branding counterpart to the content-health layer already documented in
[`EXTENSION_DESIGN.md`](EXTENSION_DESIGN.md): it reuses the same engine, lanes, and
loop rather than re-implementing them.

```
layer 1  Content model + index   →  scripts/cms/cms.py  →  .cms/
layer 2  Analysis & reporting     →  .cms/reports/, .cms/index/summary.json
layer 3  Daily agent loop         →  .claude/skills/cms-curator + CI workflow
─────────────────────────────────────────────────────────────────────────────
NEW      Brand store + guides     →  _data/brand/**  (facts)
NEW      Brand enforcement knobs   →  .cms/config.yml › brand:  (thresholds)
NEW      Brand validation          →  scripts/cms/cms.py › _check_brand
NEW      Authoring surfaces        →  brand-voice skill · /draft-muse · /brand-audit
                                       brand.instructions.md
```

## Scope decisions

1. **Granularity = Hybrid** — per-section guides as the backbone, anchored to one
   central store, plus an optional per-article frontmatter pointer.
2. **Enforcement = Guidance + automated validation** — extend `scripts/cms/cms.py`
   and `.cms/config.yml` to flag brand drift alongside the existing
   SEO/freshness/required-field checks.
3. **Mechanism = all three wired together** — central store → skill → slash prompts
   → instructions files.

**Posts only.** The 94 files in `pages/_posts/**` across 13 category folders, plus the
devops-news/muse format surfaced via `pages/news.md`. The `quest`/`docs`/`notes`
content types are untouched.

## Guiding principles (from the repo's own conventions)

- **DRY against one store.** Guides and instructions *point at* the store; they never
  restate values or voice pillars.
- **Two layers per artifact.** Machine-readable YAML core + human/narrative Markdown
  twin (mirrors `config.yml`+`instructions/*.md`, `frontmatter.json`+`FRONTMATTER.md`).
- **Detect, don't duplicate / don't rewrite.** Brand checks *score and flag*; they
  never rewrite prose — the same rule `cms.py` already follows.
- **Brand is advisory.** Brand issues are `lane=substantive` and never touch the
  health score or the mechanical auto-merge lane. The whole system is reversible via a
  `brand.enabled` flag.

---

## 1. Central brand store — `_data/brand/`

**Home:** `_data/brand/` (not a new `.brand/` top-level dir, not `.cms/brand/`).
Rationale: `_data/` is the canonical Jekyll data home, already build-consumed
(`navigation/`, `quests/`, `ui-text.yml`), so the store is `site.data.brand.*`
-addressable and can later drive on-page rendering (section color chips, a values
block) with zero duplication. The engine reads the files directly from disk (it
already does `REPO_ROOT / ...` reads).

**Split of concerns:** brand *facts* live in `_data/brand/`; brand *enforcement
thresholds* live in `.cms/config.yml` under a new `brand:` block (§7). A single
pointer key `brand.store_root: _data/brand` links them — mirroring how `enrich_from:`
already points the engine at external report paths.

**Files to create** (YAML core, sourced from existing material — do not invent values;
mine `pages/_about/about.md`, `pages/_about/purpose.md`, `_config.yml`):

| File | Contents |
|---|---|
| `_data/brand/identity.yml` | name, tagline `"From zer0 to her0"`, domain, founder (Amr / bamr87), location, theme, `default_author: bamr87`, `team_author_label: "IT-Journey Team"`, `level_motif` (binary 0000→1111, zer0→her0). |
| `_data/brand/values.yml` | 7 principles (DFF, DRY, KIS, REnO, MVP, COLAB, AIPD) + 3 approaches (PoLR, OSAP, KISS) + the mission line, each as `{code, name, one_liner, writing_implication}`. The `writing_implication` field is what makes this load-bearing for authoring (e.g. DRY → "link the canonical explanation, don't re-explain"; KIS → "clarity over cleverness in prose"). |
| `_data/brand/colors.yml` | the `theme_color` palette verbatim from `_config.yml` (24 tokens) + `theme_skin: dark` + a `section_accent` map (category → token + Bootstrap icon, reusing the icon map in `index-hub.instructions.md` §4). Cross-references (does not copy) the RPG tokens in `assets/css/quest-system.css` + `assets/css/contributor-profile.css`. |
| `_data/brand/voice.yml` | machine-readable profile registry the validator scores against: `default_profile: practitioner-chronicle` + a `profiles:` map, each `{name, formality band, person, emoji_intensity, sentence_length, banned_terms, preferred_terms}`. Includes `practitioner-chronicle` and `muse-opinion`. |
| `_data/brand/glossary.yml` | canonical spellings + term governance: `{term: GitHub, not: [Github, github]}`, `CI/CD`, the principle acronyms, zer0/her0 stylization, quest/chronicle/muse definitions. |
| `_data/brand/personas.yml` | audience personas from about.md "Get Involved" (Learners, Contributors, AI Enthusiasts, Educators) + the skill ladder (beginner/intermediate/advanced), each `{id, label, knows, wants, reading_for}`. |

**Narrative twin (Markdown — the prose an author reads when drafting):**

- `_data/brand/voice.md` — the voice-and-tone bible: expands each `voice.yml` profile
  into pillars + do/don't + example openings. The single place guides point to for
  "how we sound."
- `_data/brand/style.md` — prose/formatting rules (imperative for instructions, past
  tense for chronicles, one H1, no marketing fluff, language tags on code blocks,
  Mermaid for flows). **Absorbs the duplicated rules currently in
  `posts.instructions.md` §7**, which then shrinks to a pointer.
- `_data/brand/README.md` — explains authoritative-vs-derived and the "facts here,
  enforcement thresholds in `.cms/config.yml`" rule.

---

## 2. Per-section narrative guides — `_data/brand/sections/`

Co-located under the store so one `git` view shows the whole governance surface. One
file per category, **named by the existing folder slug** so resolution is mechanical:

```
_data/brand/sections/<slug>.md      # 13: ai-machine-learning, business,
                                    #   creative-experimental, culture-society,
                                    #   data-analytics, devops, learning,
                                    #   programming, system-administration,
                                    #   technology, tools-environment,
                                    #   trends-ideas, web-development
_data/brand/sections/devops-news-muse.md   # 14th: the distinct short-form guide
_data/brand/sections/_registry.yml  # slug -> {title, permalink, voice_profile,
                                    #   personas, icon, accent_color}
```

`_registry.yml` reuses the canonical category map in `index-hub.instructions.md` §4
(single source — that table then references the registry).

**Each guide is thin and pointer-based** (frontmatter declares pointers; prose holds
only section-specific *deltas* + examples — never restates voice/values):

```markdown
---
section: devops
title: DevOps
voice_profile: practitioner-chronicle   # -> _data/brand/voice.yml
personas: [contributor, ai-enthusiast]  # -> _data/brand/personas.yml
permalink: /news/devops/
accent: teal                            # -> _data/brand/colors.yml
---
# DevOps — Section Guide
> Voice/tone/values live in the central store. State only what is *specific* here.
## Audience  (link personas)
## Voice profile  (name profile + section delta)
## Tone / Structure  (deltas vs posts.instructions.md body skeleton)
## Do / Don't
## Example openings
## Section taxonomy  (preferred categories/tags from taxonomyDb.json)
```

`devops-news-muse.md` is structurally identical but declares
`voice_profile: muse-opinion` (shorter, first-person, opinion-forward, higher emoji
tolerance), references the `pages/news.md` "Chronicles" framing, sets a lower
word-count expectation, and uses a hook → take → one-link-out structure.

---

## 3. Hybrid frontmatter pointer (optional, zero churn on existing posts)

Two new **optional** keys on posts:

- `section_guide:` — guide slug (e.g. `devops`, `devops-news-muse`).
- `voice_profile:` — optional profile override (normally omitted; the guide wins).

**Resolution order** (deterministic, so all 94 existing posts resolve for free):

1. article `voice_profile:` → use it; else
2. article `section_guide:` → use that guide's profile from `_registry.yml`; else
3. infer from folder `pages/_posts/<category>/` → `<category>` guide; else
4. `voice.yml: default_profile` (`practitioner-chronicle`).

**Integration:**

- Register both keys as optional `choice` fields on the `default` content type in
  `frontmatter.json` (dropdowns: 14 slugs / profile names) — prevents typos, mirrors
  the taxonomy approach. **Do not** touch the `quest` content type.
- Add both to `collections.posts.recommended` in `.cms/config.yml` (a nudge, never a
  CI-blocking required field).
- Add `section_guide:` (pre-filled/commented) to the `.frontmatter/templates/` post
  template so new drafts start governed.

---

## 4. The skill — `.claude/skills/brand-voice/SKILL.md`

New skill `brand-voice`. Trigger (the `description:` frontmatter):

> "Load IT-Journey brand context (values, voice, style, section guide) before
> drafting or editing a post or muse. Use when writing a new article, writing a
> short-form devops-news muse, rewriting for voice/tone, or checking content matches
> a section's brand profile."

**Procedure:** (1) resolve section via §3 order; (2) load the store lean —
`identity.yml`, `values.yml` (read `writing_implication`), the resolved `voice.yml`
profile, `voice.md`, `style.md`, `glossary.yml`, then `sections/<slug>.md`; (3) hold
the profile as the active constraint while drafting/editing (preferred/banned terms,
formality band, emoji intensity, structure deltas, value writing-implications); (4)
self-check against the same knobs `_check_brand` uses so skill output and validator
agree; (5) hand off — do not write files unless asked, do not own git (mirrors
`draft-article`/`cms-curator`).

**Relationship:** composes with, doesn't overlap — `cms-curator` is the batch loop
(consumes worklist, packages PRs); `brand-voice` is the per-piece authoring/quality
loader. `/draft-article` stays the structural generator and *invokes* `brand-voice`
for voice.

---

## 5. Slash prompts — `.github/prompts/`

All follow the canonical `.prompt.md` schema (`mode: agent`, double-quoted
`description` ≤160, ISO-ms `date`/`lastmod`).

**New:**

- `draft-muse.prompt.md` (`/draft-muse`) — short-form sibling of `/draft-article`.
  Loads `brand-voice` with `section_guide: devops-news-muse`; emits a muse skeleton
  (hook → take → one-link → zer0-to-her0 tie-back), frontmatter with
  `section_guide: devops-news-muse`, a tighter word count, optional `featured`/
  `breaking` news keys. Targets `pages/_posts/devops/`.
- `brand-audit.prompt.md` (`/brand-audit`) — read-only reporter (like
  `/quest-permalink-audit`). Runs `make cms-all`, surfaces `brand_drift` issues from
  the index/worklist grouped by section, naming the offending term/metric + the rule.

**Extend** (each gains a "load brand-voice for the resolved section" step + a brand
item in its quality checklist; reference, don't restate):
`draft-article.prompt.md`, `expand-content.prompt.md`,
`generate-frontmatter.prompt.md`, `validate-content.prompt.md`.

---

## 6. Instructions files — `.github/instructions/`

Canonical `.instructions.md` schema (double-quoted `applyTo` glob + `description` ≤160
+ ISO-ms dates).

- **New `brand.instructions.md`**, `applyTo: "pages/_posts/**/*.md"` — auto-loads when
  a post is open. Pointer-form brand contract: the resolution rule, the two keys, the
  top banned terms, links to `voice.md`/`style.md`/section guides. One concern:
  *applying brand to posts* (structural rules stay in `posts.instructions.md`).
- **Extend `posts.instructions.md`** — replace the §7 "Style" body with a pointer to
  `_data/brand/style.md` + `brand.instructions.md` (DRY); add the two keys to §2
  Recommended.
- **Extend `index-hub.instructions.md`** — note §4's category map now mirrors
  `_data/brand/sections/_registry.yml` and must stay in sync (registry is the source).

---

## 7. Automated validation — extend `cms.py` + `.cms/config.yml`

**New `brand:` block in `.cms/config.yml`** (hand-edited knob-board; global rules +
per-section overrides keyed by guide slug):

```yaml
brand:
  enabled: true
  store_root: _data/brand
  advisory_only: true                 # never blocks CI, never auto-merges
  global:
    banned_terms: [comprehensive, powerful, seamless, cutting-edge, revolutionary]
    preferred_terms: { Github: GitHub, "ci/cd": CI/CD }
    emoji_intensity: { min: 0, max: 8 }
    formality_target: 55
  sections:
    devops:            { formality_target: 60, required_structural: ["Verify"] }
    devops-news-muse:  { emoji_intensity: {min: 1, max: 12}, formality_target: 45,
                         word_count: {min: 150, max_suggest: 600} }
    creative-experimental: { banned_terms_relax: [cutting-edge] }
```

**New `_check_brand(rec, fm, body, cfg)` in `scripts/cms/cms.py`** — called from
`analyze_file` only when `brand.enabled` and the record is a post (not
read-only/structural/generated). It:

1. Resolves the profile via §3 (reads `sections/_registry.yml` + `voice.yml`, cached at
   config-load like the existing `_GLOB_CACHE`).
2. Merges `brand.global` ← `brand.sections[<slug>]`.
3. Emits standard `Issue` records, **all `lane="substantive"`**, with a new `kind`
   family `brand_drift:<rule>` — `banned_term` (warning), `preferred_term` (info),
   `emoji_intensity` (info), `formality` (info, cheap heuristic), `missing_structural`
   (info), `guide_unresolved` (info). Reuse the existing `CODE_FENCE_RE` to strip code
   before term/emoji scanning (so commands aren't flagged), as `count_words` does.
4. `FileRecord` gains optional `section_guide`, `voice_profile`, and a
   `brand_issue_count` computed property (like the existing `error_count`).

**Scoring — advisory, NOT a health factor (recommended).** Do **not** add brand to
`_score` / `health_weights`. Voice/formality are heuristic and subjective; folding them
into the CI-aligned health number would make it noisy and silently re-rank the worklist
on soft signals. Brand issues are real `Issue`s (they appear in the index, the report's
"Top issue types," and the worklist's substantive lane via existing plumbing) but
`health` is unchanged. `advisory_only: true` + `enabled: false` make it fully
reversible. (If wanted later: add a 5–10% `brand` weight + a `brand_score` term.)

**Surfacing + curator pickup:**

- `cmd_analyze`: the existing "Top issue types" auto-counts `brand_drift`; optionally
  add a small "Brand drift by section" table (a few lines).
- `cmd_plan`: brand issues are substantive → already flow into Lane B (no planner
  change).
- `.claude/skills/cms-curator/SKILL.md`: add `_data/brand/` to its Phase 0 policy
  reads, and one Lane B bullet — "`brand_drift:*` → load `brand-voice`, resolve the
  guide, apply the smallest term/voice fix; never rewrite wholesale."

---

## 8. Sequencing (each phase independently shippable + CI-safe)

Branch first; **never commit to `main`**. New post keys are all optional and
`_data/brand/**` is non-rendered data, so `frontmatter-validation` + `make build-ci` +
`make content-audit` stay green throughout.

1. **Store (data only, zero behavior change).** Create the nine `_data/brand/*` files
   from `about.md`/`purpose.md`/`_config.yml`. Verify `make build-ci` still builds.
2. **Section guides + registry.** Create `_registry.yml` + 14 `sections/*.md` (13
   categories + `devops-news-muse.md`), thin/pointer-based; populate the registry from
   `index-hub.instructions.md` §4.
3. **Frontmatter pointer.** Edit `frontmatter.json` (2 optional choice fields),
   `.cms/config.yml` (`collections.posts.recommended`), `.frontmatter/templates/` post
   template. Verify `make content-validate` + `make build-ci`.
4. **Engine validation.** Edit `scripts/cms/cms.py` (`_check_brand`, `FileRecord`
   fields, cached store loader, `cmd_analyze` table; wire behind `brand.enabled`) +
   `.cms/config.yml` (`brand:` block + document the new `brand_drift` kinds as
   substantive). Run `make cms-all`; confirm issues emit and `health` is unchanged.
   (Blast radius: only `.cms/` outputs, which Jekyll ignores.)
5. **Authoring surface.** Create `.claude/skills/brand-voice/SKILL.md`, the
   `draft-muse`/`brand-audit` prompts, `brand.instructions.md`; extend the 4 prompts,
   trim `posts.instructions.md` §7, note `index-hub.instructions.md` §4, and add the
   brand bullet + policy read to `cms-curator/SKILL.md`. All `.prompt.md`/
   `.instructions.md` pass the `FRONTMATTER.md` four-key check.

**Reuse:** `Issue`/`FileRecord` dataclasses, the `lane` plumbing, `_GLOB_CACHE`/
`glob_match`, `CODE_FENCE_RE`, `cmd_plan` substantive routing, the worklist/report
writers, the `index-hub.instructions.md` §4 category map, `taxonomyDb.json`, the
SKILL/prompt/instruction conventions, `make cms-all`, the `cms-daily-loop` workflow.

**Build new:** `_data/brand/**`, the 14 guides + registry, `_check_brand` + the
`brand:` config block, the `brand-voice` skill, the `draft-muse`/`brand-audit` prompts,
`brand.instructions.md`.

## Critical files

**Modify:** `scripts/cms/cms.py`, `.cms/config.yml`, `frontmatter.json`,
`.github/instructions/posts.instructions.md`,
`.github/instructions/index-hub.instructions.md`,
`.claude/skills/cms-curator/SKILL.md`, the `.frontmatter/templates/` post template, and
the four prompts (`draft-article`, `expand-content`, `generate-frontmatter`,
`validate-content`).

**Create:** `_data/brand/{identity,values,colors,voice,glossary,personas}.yml`,
`_data/brand/{voice,style,README}.md`, `_data/brand/sections/_registry.yml` + 14
`sections/*.md`, `.claude/skills/brand-voice/SKILL.md`,
`.github/prompts/{draft-muse,brand-audit}.prompt.md`,
`.github/instructions/brand.instructions.md`.

**Mine for source material (read-only):** `pages/_about/about.md`,
`pages/_about/purpose.md`, `_config.yml`, `pages/news.md`,
`.github/instructions/index-hub.instructions.md`.

## Verification

- **Build stays green:** `make build-ci` and `make content-audit` after Phases 1–3 (and
  again at the end). `_data/brand/**` is data, so it cannot fail post frontmatter
  validation; the new post keys are optional.
- **Engine emits brand issues without perturbing health:** `make cms-all`, then check
  that `.cms/index/content-index.json` and `.cms/reports/<date>.md` show `brand_drift:*`
  issues in the substantive lane, and confirm collection `health` numbers are unchanged
  vs the pre-change `summary.json` (diff `index/summary.json`).
- **Resolution defaults work for legacy posts:** spot-check that a post in
  `pages/_posts/devops/` with no `section_guide` still resolves to the `devops` guide
  (it appears under devops in the new "Brand drift by section" table).
- **Skill loads end-to-end:** invoke `brand-voice` (or `/draft-muse`) on a sample
  devops topic and confirm it loads the store + the `devops-news-muse` guide and
  produces a draft honoring the `muse-opinion` profile (no banned terms, emoji in band,
  hook→take→link structure).
- **Audit reporter works:** run `/brand-audit` and confirm it lists drift grouped by
  section with the offending term + rule.
- **Reversibility:** set `brand.enabled: false` in `.cms/config.yml`, run
  `make cms-all`, and confirm `brand_drift` issues disappear and outputs match the
  pre-feature baseline.
