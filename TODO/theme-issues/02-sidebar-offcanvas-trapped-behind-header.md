# Sidebar offcanvas (`#bdSidebar`) opens behind the fixed header on mobile — close button unreachable

**Repo:** [bamr87/zer0-mistakes](https://github.com/bamr87/zer0-mistakes)
**Severity:** High (mobile UX — the sidebar nav cannot be closed by tapping ×)
**Affects:** any layout that renders the `#bdSidebar` offcanvas inside `<main>`

## Symptom

On mobile, opening the docs/quest **sidebar nav** (`#bdSidebar`) works, but the
offcanvas opens **behind the fixed site header**: its "Browse docs" title bar and
its `×` close button render *under* the navbar. A touch user has no Esc key, so
there is no visible affordance to dismiss the menu (only a backdrop tap, which is
undiscoverable and partially obscured).

The main-nav offcanvas (`#bdNavbar`) is **not** affected — it lives in the
header, not in `<main>`.

## Root cause

Same generic stacking rule as the companion overflow issue:

```css
.zer0-bg-body > :not(.fixed-top):not(.offcanvas):not(.modal) {
  position: relative;
  z-index: 1;
}
```

`<main>` matches this rule and becomes a **stacking context at `z-index: 1`**.
`#bdSidebar` is nested inside `<main>` (`<main> … <aside class="bd-sidebar"> …
<div id="bdSidebar" class="offcanvas-lg offcanvas-start">`). Its own
`z-index: 1045` only orders it *within* main's context — so the entire offcanvas
is capped at main's `z-index: 1`, which is **below the fixed header**
(`header.fixed-top`, a body-level child at `z-index: 1030`).

Result: the header paints over the top ~62px of the offcanvas, covering its
header row and close button.

The `:not(.offcanvas)` carve-out in the rule doesn't help here because it only
exempts offcanvases that are *direct children of `.zer0-bg-body`* — this one is
nested several levels deep inside `<main>`.

## Suggested fix (theme side)

Pick whichever fits the theme's architecture:

1. **Render the sidebar offcanvas outside `<main>`** (as a body-level sibling of
   the header, like `#bdNavbar`). Cleanest — the offcanvas then participates in
   the root stacking context and its `z-index: 1045` wins naturally.

2. **Don't let `<main>` trap descendant overlays.** If `<main>` doesn't actually
   need `z-index: 1`, drop it (keep `position: relative` only where required), or
   exclude structural landmarks from the rule.

3. **Offset the open offcanvas below the fixed header** (pragmatic, what the
   downstream site does):

   ```css
   @media (max-width: 991.98px) {
     #bdSidebar.offcanvas-lg.show {
       top: var(--zer0-header-height, 62px);
       height: calc(100% - var(--zer0-header-height, 62px));
     }
   }
   ```

   Bonus: exposing a `--zer0-header-height` token (the header height is currently
   reflected only in `body { padding-top: 62px }`) would let consumers align with
   it instead of hard-coding.

## Reproduction

1. Open a docs/quest page at ≤ 768px width.
2. Tap the sidebar toggle (`button[data-bs-target="#bdSidebar"]`).
3. The offcanvas opens but its title bar + `×` are hidden behind the header;
   `document.elementFromPoint()` at the close button's center returns a header
   element (e.g. `span.site-title-text`), not the button.

## Downstream note

Worked around in `bamr87/it-journey` via `assets/css/user-overrides.css` using
option 3 above. A theme-side fix (preferably option 1 or 2) would let that be
removed. Companion issue: *"generic stacking rule causes 16px horizontal
overflow"* — same rule, different symptom.
