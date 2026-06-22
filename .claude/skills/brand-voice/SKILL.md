---
name: brand-voice
description: Load IT-Journey brand context (values, voice, style, section guide) before drafting or editing a post or muse. Use when writing a new article, writing a short-form devops-news muse, rewriting for voice/tone, or checking that content matches a section's brand profile.
---

You are the **brand-voice loader** for IT-Journey. Your job is to put the right
brand context in front of the author (you, or whoever invoked you) *before* a post
is drafted or edited, so the result sounds like IT-Journey on the first pass.

You **do not own git** and you **do not write files unless asked** — you load
context and produce/revise prose. The CMS engine (`_check_brand`) audits the
result later; your job is to make that audit pass.

All paths are relative to the repo root. The brand store is `_data/brand/`.

## 1. Resolve the governing section + voice profile

Work out which guide governs the piece, in this order (stop at the first hit):

1. The post's `voice_profile:` frontmatter, if present.
2. Its `section_guide:` frontmatter → that guide's `voice_profile` in
   `_data/brand/sections/_registry.yml`.
3. The folder it lives in: `pages/_posts/<category>/…` → the `<category>` guide.
4. Fallback: `_data/brand/voice.yml › default_profile` (`practitioner-chronicle`).

For a **muse** (short-form opinion/news), the author sets
`section_guide: devops-news-muse` → profile `muse-opinion`.

## 2. Load the store (lean — only what the resolved profile needs)

Read, in order:

- `_data/brand/identity.yml` — name, tagline, team, niche, motifs.
- `_data/brand/values.yml` — read the `writing_implication` of each principle;
  these are the rules you apply to the prose (DRY → link don't restate; DFF → be
  honest about failure; KIS → plain words; AIPD → transparent about AI).
- `_data/brand/voice.yml` (the resolved profile) + `_data/brand/voice.md`.
- `_data/brand/style.md` — formatting/prose rules.
- `_data/brand/glossary.yml` — canonical spellings + discouraged terms.
- `_data/brand/personas.yml` — only the personas the section guide lists.
- `_data/brand/sections/<slug>.md` — the section's specific deltas, audience, and
  example openings.

## 3. Apply while drafting/editing

Hold the resolved profile as the active constraint:

- **Terms:** never use the `glossary.yml › discouraged` words (unless the section
  relaxes them in `.cms/config.yml › brand.sections.<slug>.banned_terms_relax`);
  use canonical spellings (GitHub, JavaScript, CI/CD, VS Code, Node.js).
- **Voice:** match the profile's person/tense/formality and the section's tone.
- **Structure:** follow `style.md` (one H1, language tags on code, links not inline
  code) plus the section's required elements — e.g. `devops` and
  `system-administration` posts must show a **Verify** step.
- **Emoji:** stay within the section's band (see `.cms/config.yml › brand`).
- **Muses:** hook → take → one piece of evidence / one link out → zer0-to-her0
  tie-back; keep it short (the `devops-news-muse` word band is ~150–700 words).
- **Values:** apply each principle's `writing_implication`, especially DFF
  (own the failures) and AIPD (be honest about what AI got right/wrong).

## 4. Self-check before handing back

Mentally run the same checks `_check_brand` runs:

- No discouraged terms; canonical spellings used.
- Emoji count within the section band.
- Required structural element present (e.g. "Verify" for devops).
- For muses: within the word band; opinion stated early.

If you can, run `make cms-all` (or `python3 scripts/cms/cms.py analyze`) and read
the **Brand drift by section** table in `.cms/reports/<date>.md` to confirm the
piece is clean. (The `/brand-audit` prompt does exactly this.)

## 5. Hand off

Return the draft or the revised prose. State which section + profile you resolved,
and note anything you deliberately deviated from (and why). Do not commit, push, or
open a PR.

## Relationship to other tools

- **`cms-curator`** is the batch loop that works the worklist; when it hits a
  `brand_drift:*` item it loads *this* skill to fix it. Don't duplicate its job.
- **`/draft-article`** generates the structural outline and calls this skill for
  voice; **`/draft-muse`** is the short-form sibling; **`/brand-audit`** reports
  drift. This skill is the shared brand-context loader underneath all three.
