# redirects/

Redirect stubs for content that moved off it-journey.dev. Each stub pins the page's **old** it-journey URL via `permalink:` and forwards to its new home via `redirect_to:` (rendered by the `jekyll-redirect-from` plugin, already enabled in `_config.yml`). All stubs set `sitemap: false` so search engines follow the redirect instead of indexing the shim.

## posts/

The blog was removed in the 2026-06 quest-refocus overhaul (PR #366); articles were rewritten into **lifehacker.dev**. These 42 stubs map every old `/posts/:year/:month/:day/:slug/` URL that has a confirmed lifehacker.dev destination, derived from lifehacker.dev's import ledger (`docs/content-import/triage.plan.json`, PR bamr87/lifehacker.dev#55: 42 `rewrite` verdicts out of 110 triaged posts). Destination URLs were verified live (HTTP 200) when generated on 2026-08-01.

Old posts with a `skip` verdict (opinion essays, superseded content) and posts relocated inside this repo (e.g. the GH-600 track, now under `pages/_docs/`) intentionally have **no** stub here — a deliberate 404 or their in-repo home is correct.

This directory sits outside `pages/` on purpose: the frontmatter-validation CI gate covers `pages/**/*.md`, and these shims carry only the minimal keys a redirect needs.
