// =============================================================================
// a11y.config.mjs — pages, viewports and known issues for the PR a11y checks
// -----------------------------------------------------------------------------
// Read by a11y-check.mjs (axe-core via Playwright) and contrast-check.mjs
// (pa11y / HTML_CodeSniffer). Paths are served from the local _site build.
// =============================================================================
export default {
  viewports: [
    { name: 'mobile-390', width: 390, height: 844, mobile: true },
    { name: 'desktop-1366', width: 1366, height: 768 },
  ],

  // Key pages: home, the quest index, one diagram-heavy quest, notes, about,
  // the quest-report index, and search.
  pages: ['/', '/quests/', '/quests/0000/hello-noob/', '/notes/', '/about/', '/quest-reports/', '/search/'],

  axe: {
    // Any critical/serious violation of these rules FAILS the job...
    blockingTags: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'],
    blockingImpacts: ['critical', 'serious'],
    // ...while WCAG 2.2 rules (in practice `target-size`: the nav
    // split-toggle is 20x36 px) are reported as warnings only.
    // TODO(error): move 'wcag22aa' into blockingTags once the zer0-mistakes nav
    // toggle is >= 24 px wide.
    warnTags: ['wcag22a', 'wcag22aa'],

    // Violations that already exist on main. Each one is downgraded to a
    // WARNING — still listed in the job summary and as an annotation — but only
    // for this rule, on these pages, on nodes matching `nodes` (a regex over the
    // node's selector + HTML). Anything else under the same rule still fails.
    // Delete an entry when its fix lands; the job prints a notice when an entry
    // stops reproducing.
    known: [
      {
        rule: 'label',
        pages: ['/quests/0000/hello-noob/'],
        nodes: 'task-list-item-checkbox',
        todo: 'TODO(it-journey fix): interactive quest-objective checkboxes (task lists made clickable by site JS) have no accessible name — wrap in <label> or set aria-label from the item text',
      },
      {
        rule: 'button-name',
        pages: ['*'],
        viewports: ['mobile-390'],
        nodes: 'shareDropdownBottom',
        todo: 'TODO(theme fix): intro "Share" dropdown is icon-only below 576 px (text is span.d-none.d-sm-inline) — zer0-mistakes _includes/content/intro.html',
      },
      {
        rule: 'link-name',
        pages: ['*'],
        viewports: ['mobile-390'],
        nodes: 'bd-intro-action-link',
        todo: 'TODO(theme fix): intro "Edit on GitHub" link is icon-only below 576 px — zer0-mistakes _includes/content/intro.html',
      },
    ],
  },

  contrast: {
    // it-journey has no /news/ or blog-post collection (old /posts/ URLs are
    // redirect stubs), so /notes/ (the notes index) and one note stand in for
    // "the news page" and "one post".
    // `max` = most contrast failures allowed before the page FAILS. Pages that
    // are clean today are pinned at 0; the rest are report-only for now.
    pages: [
      { path: '/notes/', max: 0 },
      { path: '/notes/cheatsheets/markdown/', max: 0 },
      // TODO(error): set max: 0 once the theme badge colours are fixed — today
      // ~615 sitemap badges fail (white on bg-info 1.96:1, bg-outline-primary 3.97:1).
      { path: '/search/' },
    ],
    // Gradient / image hero headings: htmlcs measures them against the flat
    // fallback colour and reports false 1:1 failures, so they're hidden first.
    hideElements: '.zer0-bg-hero h1, .zer0-bg-hero h2, .bd-intro h1, .bd-intro h2',
  },
};
