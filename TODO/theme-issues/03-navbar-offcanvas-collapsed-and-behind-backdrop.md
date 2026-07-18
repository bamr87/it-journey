# Main-nav offcanvas (`#bdNavbar`) renders empty on mobile — collapsed panel + painted behind the backdrop

**Repo:** [bamr87/zer0-mistakes](https://github.com/bamr87/zer0-mistakes) **Severity:** High (mobile UX — the primary navigation menu is unusable) **Affects:** the responsive navbar offcanvas `#bdNavbar` on mobile (≤ 991.98px), most visibly on the home/landing header

## Symptom

Tapping the hamburger opens the menu chrome ("Main Navigation" title + × close), but the panel body is **empty/transparent**: you see the dimmed page content through it and none of the nav links. The menu is effectively unusable on mobile.

## Root cause

Two compounding problems:

1. **The panel collapses instead of expanding.** The offcanvas computes to the
navbar's height (~44px) with a transparent body — it never becomes a full-height slide-in panel — so its links overflow out of an 8px body and are not laid out as a menu.

2. **The menu paints behind the backdrop.** `#bdNavbar` is nested inside the
fixed `header#navbar` (z-index 1030). Bootstrap appends `.offcanvas-backdrop` to `<body>` at z-index 1040. Because the header's stacking context sits below the backdrop, the entire menu subtree — even at the offcanvas's own `z-index: 1045` — renders **beneath** the backdrop. `document.elementFromPoint` over a link returns `div.offcanvas-backdrop`.

## Suggested fix (theme side)

- Ensure the responsive offcanvas actually gets the Bootstrap "offcanvas mode"
box on mobile (full height, opaque `--bs-offcanvas-bg`, `transform`-based slide, scrollable `.offcanvas-body`) — verify the `.navbar-expand-lg .offcanvas` inline override is correctly gated to `@media (min-width: 992px)` and isn't leaking to smaller widths.
- Make the offcanvas escape the header's stacking context, or raise the header
above the backdrop **only while the menu is open**. A consumer-side override that works:

  ```css
  @media (max-width: 991.98px) {
    #bdNavbar.offcanvas-lg.show {
      position: fixed !important; inset: 0 0 0 auto !important;
      height: 100dvh !important; width: var(--bs-offcanvas-width, min(21rem, 86vw)) !important;
      background-color: var(--zer0-color-bg) !important; transform: none !important;
      z-index: 1046 !important; flex-direction: column !important;
    }
    #bdNavbar.offcanvas-lg.show .offcanvas-body { flex: 1 1 auto !important; overflow-y: auto !important; min-height: 0 !important; }
    body:has(#bdNavbar.offcanvas-lg.show) #navbar { z-index: 1047 !important; }
  }
  ```

## Reproduction

1. Open the home page at ≤ 768px width.
2. Tap the main-nav (hamburger / "···") toggle.
3. The menu chrome shows but the body is transparent with no usable links;
   `elementFromPoint` over a link returns the offcanvas backdrop.

## Downstream note

Worked around in `bamr87/it-journey` via `assets/css/user-overrides.css` (the snippet above). A theme-side fix would let it be removed. Companion issues: *"generic stacking rule causes 16px horizontal overflow"* and *"offcanvas nested in `<main>` opens behind the fixed header"* — same offcanvas/stacking area.
