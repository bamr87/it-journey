# KIS / KISS fix (draft, not applied)

> A proposal, not yet applied: make KIS (Keep It Simple) the one simplicity pillar and drop KISS from the working approaches, with every occurrence found and the patch for the About page. Line references are as of 2026-10-29.

## Occurrences
**KIS = "Keep It Simple" (pillar):** `pages/_about/about.md:64,84`; `_data/brand/values.yml:32`; `_data/brand/voice.md:18`; `.github/instructions/brand.instructions.md:38`; `.github/instructions/README.md:85`; `pages/_about/README.md:94`; `pages/_about/features/index.md:124`; `pages/_about/contribute/contributing.md:226`; `docs/ROADMAP.md:253,450`; `docs/cms/BRANDING_GOVERNANCE_PLAN.md:82`; quests `0001/it-journey-stack-analysis.md:1145`, `1100/the-temple-of-templates.md:84`, `0011/prompt-crystal-mastery-vscode-copilot.md:713`.

**KISS = "Keep It Stupid Simple" (approach):** `about.md:69,110`; `_data/brand/values.yml:72-73`; `pages/_about/purpose.md:25`; `docs/purpose-page-rewrite.md:37`.

**Mixed:** `about.md:84-86` heading is "Keep It Simple — KIS" but the body links "The KISS principle".

`PRD.md` and `features/features.yml` contain neither KIS nor KISS (checked with `rg -w`), so they don't settle it.

## Decision: canonical = **KIS** (Keep It Simple)
- KIS is used in ~14 places, including the source of truth `_data/brand/values.yml` and the agent instructions. KISS appears in 4 places, all tied to the approaches list.
- The two are not really separate ideas. KIS = "clarity over cleverness"; KISS = "the most boring, reliable option", which is the same idea. Listing both makes the About page repeat itself (a DRY problem).
- Fix: keep KIS as the pillar and remove KISS from the approaches. The approaches become **PoLR · OSAP**. The "boring, reliable option" sentence moves into the KIS pillar. The link to Wikipedia's KISS article stays as a citation (that article is the industry name).

## Patch for `pages/_about/about.md`
```diff
--- a/pages/_about/about.md
+++ b/pages/_about/about.md
@@ -69 +69 @@
-  <div class="itj-pillar approach"><span class="code">PoLR · OSAP · KISS</span><h4>Three working approaches</h4><p>Path of least resistance, open source as possible, keep it stupid simple.</p></div>
+  <div class="itj-pillar approach"><span class="code">PoLR · OSAP</span><h4>Two working approaches</h4><p>Path of least resistance, open source as possible.</p></div>
@@ -86 +86 @@
-The [KISS principle](https://en.wikipedia.org/wiki/KISS_principle) is a bias toward the boring, readable solution over the clever one.
+Keep It Simple (KIS, our take on the [KISS principle](https://en.wikipedia.org/wiki/KISS_principle)) is a bias toward the boring, readable solution over the clever one.
@@ -110 +110 @@
-Beneath the principles sit three plain heuristics that decide the small calls: the **path of least resistance** (recommend the simplest route that works before reaching for the advanced one), **open source as possible** (prefer open tools and free tiers, and flag clearly when something is paid or proprietary), and **keep it stupid simple** (default to the most boring, reliable option that meets the need).
+Beneath the principles sit two plain heuristics that decide the small calls: the **path of least resistance** (recommend the simplest route that works before reaching for the advanced one) and **open source as possible** (prefer open tools and free tiers, and flag clearly when something is paid or proprietary). Simplicity itself is the KIS pillar above: default to the most boring, reliable option that meets the need.
```
(Line 86 hunk shows only the changed first sentence; the rest of the paragraph is unchanged.)

## Other files needing the same change (not edited)
- `_data/brand/values.yml:72-74`: remove the KISS approach and update the comment "three working approaches".
- `pages/_about/purpose.md:25`: "Keeping it stupid simple (KISS)" → drop, or point to KIS.
- `docs/cms/BRANDING_GOVERNANCE_PLAN.md:82`: "3 approaches (PoLR, OSAP, KISS)" → 2.
- `docs/purpose-page-rewrite.md:37`: KISS bullet.

## Alternative (if three approaches must stay)
Keep KISS but call it out explicitly on line 110 as "the KIS pillar applied to tool choice". This is less clean, so I don't recommend it.
