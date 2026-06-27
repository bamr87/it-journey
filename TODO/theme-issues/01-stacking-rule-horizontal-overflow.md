# Generic `.zer0-bg-body > :not(...)` stacking rule causes 16px horizontal overflow on mobile

**Repo:** `bamr87/zer0-mistakes`
**Severity:** Medium (mobile UX — every content page scrolls sideways)
**Affects:** any page where `.obsidian-local-graph-fab` is rendered (i.e. not `display:none`)

## Symptom

On mobile widths, every content page scrolls **16px horizontally**. `scrollWidth`
is 406px in a 390px (iPhone 13) viewport. Landing/home pages are unaffected
because the FAB is `display:none` there.

## Root cause

`assets/css/main.css` defines a generic stacking rule:

```css
.zer0-bg-body > :not(.fixed-top):not(.offcanvas):not(.modal) {
  position: relative;
  z-index: 1;
}
```

Each `:not()` contributes its argument's specificity, so this selector is
**(0,4,0)** — higher than `.obsidian-local-graph-fab` **(0,1,0)**:

```css
.obsidian-local-graph-fab {
  position: fixed;            /* ← lost to the rule above */
  left: var(--zer0-space-fab-offset, 1rem);
  right: auto;
  bottom: var(--zer0-space-fab-offset, 1rem);
  z-index: var(--zer0-layer-fab-local-graph);
}
```

Because the FAB is a direct child of `.zer0-bg-body`, the generic rule wins for
`position`, dropping the FAB from `fixed` back into normal flow as a
**full-width block**. Its own `left: 1rem` offset then shifts it +16px to the
right, pushing the document 16px past the viewport.

## Suggested fix (theme side)

Exclude the FABs from the generic rule (mirrors the existing
`:not(.fixed-top):not(.offcanvas):not(.modal)` carve-outs), e.g.:

```css
.zer0-bg-body > :not(.fixed-top):not(.offcanvas):not(.modal):not(.obsidian-local-graph-fab):not(.bd-toc-fab) {
  position: relative;
  z-index: 1;
}
```

Or, more robustly, raise the FAB rules' specificity / mark the intended
position as authoritative so layout intent can't be silently overridden:

```css
.zer0-bg-body > .obsidian-local-graph-fab,
.zer0-bg-body > .bd-toc-fab {
  position: fixed;
}
```

## Reproduction

1. Open any docs/quest page at ≤ 768px width.
2. Observe `document.documentElement.scrollWidth > clientWidth` (16px) and a
   horizontal scrollbar / rubber-band.
3. Inspect `.obsidian-local-graph-fab` → computed `position` is `relative`, not
   `fixed`.

## Downstream note

Worked around in the consuming site (`bamr87/it-journey`) via
`assets/css/user-overrides.css`:

```css
.obsidian-local-graph-fab, .bd-toc-fab { position: fixed !important; width: auto !important; }
@media (max-width: 991.98px) { html, body { overflow-x: clip; } }
```

A theme-side fix would let that override be removed. See also the companion
issue: *"offcanvas nested in `<main>` opens behind the fixed header"* — same
stacking rule, different symptom.
