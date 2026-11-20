# Astro spike

> A time-boxed test of one question: can it-journey.dev move off Jekyll without touching its content, and does a quest-first shell fix the reading experience? Not the production site.

## What it is

An [Astro](https://astro.build) project that builds every page in `pages/_quests` straight from the Markdown Jekyll reads. Nothing under `pages/` is edited, so both builds run from one source and a migration can go page type by page type.

The Jekyll site is unaffected: `astro/` is listed under `exclude:` in `_config.yml`, and nothing here is deployed.

## Run it

Node 22.23.4 or newer.

```bash
cd astro && npm install --no-package-lock
```

```bash
npm run dev
```

```bash
npm run build
```

```bash
npm run preview
```

```bash
npm test
```

```bash
npm run check
```

```bash
npm run check:urls
```

`dev` and `preview` serve on <http://localhost:4321>. `test` runs the unit tests for the translation layer, `check` type-checks the project, and `check:urls` compares the built URLs with the live sitemap (pass `--sitemap ../_site/sitemap.xml` to compare with a local Jekyll build instead). The repository does not commit lockfiles, hence `--no-package-lock`.

## How it works

| Piece | File | Job |
| --- | --- | --- |
| Loader | `src/lib/jekyll-loader.ts` | Reads `../pages/_quests` in place, parses front matter as YAML 1.1, validates it, renders it, and writes `reports/compat-report.json` |
| Translation | `src/lib/jekyll-compat.ts` | Turns Jekyll and kramdown syntax into plain Markdown in memory: `raw` blocks, `<details markdown="1">`, attribute lists, wikilinks, relative `.md` links |
| Schema | `src/content.config.ts` | Types what the layouts read; also loads the generated `_data/quests/levels.yml` and `tiers.yml` as they are |
| Route | `src/pages/[...path].astro` | One route for the collection. The URL is each page's own `permalink`; `redirect_from` becomes forwarding pages |
| Templates | `src/templates/` | Quest, level, hub and plain document pages |
| Tokens | `src/styles/tokens.css` | Every colour, font and spacing value, as light and dark pairs. The seam where fleet tokens map in |
| Browser code | `src/scripts/site.ts` | Theme toggle, progress, copy buttons, Mermaid loaded only on pages with a diagram |
| Assets | `src/integrations/repo-assets.mjs` | Serves the repository's `assets/` at `/assets/` without copying or symlinking it into the project |

Progress uses the same `localStorage` key and shape as `assets/js/quest-progress.js`, so a learner's saved progress carries over.

## What the spike found

Measured on 2026-11-19 against `main` and the live site.

### Content

| | Result |
| --- | --- |
| Files in `pages/_quests` | 258 |
| Loaded and rendered | 255 |
| Left out, as Jekyll leaves them out | 3 (two authoring templates unpublished by a `_config.yml` default, one file with no front matter) |
| `raw` blocks unwrapped | 485 |
| `<details markdown="1">` fixed | 332 |
| Wikilinks resolved at build | 966 |
| Wikilinks unresolved | 322 in 136 files |
| Relative `.md` links resolved | 212 |
| Mermaid diagrams | 163 |
| Pages with Liquid that needs a component | 12 |

- The 12 pages are the 11 bashcrawl rooms (two includes each: the terminal and the play-locally panel) and the inventory page. Everything else in the collection needed no hand work.
- Unresolved wikilinks are reported at build time. On the one page spot-checked (`/quests/0000/character-building/`), the three unresolved targets are rendered as broken links on the live site too, where nothing reports them.
- 24 quests still write `prerequisites:` and `rewards:` as plain lists. The schema folds them into the current shape; the first build rejected them, which is how they were found.

### URLs

Compared with a Jekyll build of the same commit (`make build-ci` flags, run in Docker): Jekyll writes 324 URLs under `/quests/` (256 pages and 68 `redirect_from` pages) and this build serves 323 of them at the same address, with nothing extra. The one missing, `/quests/ideas/`, comes from `pages/quest-ideas.md`, which is outside this collection.

`npm run check:urls` makes the same comparison against the live sitemap: 255 of 256 match, with the same single exception.

### The quest page

Same quest (`/quests/0001/avatar-forge/`), live site against this build.

| | Jekyll + theme | Spike |
| --- | --- | --- |
| Screens before "Quest Objectives" on a phone | 3.3 | 0.8 |
| `<h1>` elements | 3 | 1 |
| Fixed or sticky layers on a phone | 12 | 1 |
| Text column at 1440px | 496px (34%) | 736px (51%) |
| HTML | 299 KB | 16 KB |
| Requests | 53 | 5 |
| JavaScript | 341 KB in 37 files | 6 KB in 1 file |
| CSS | 622 KB | 19 KB |
| DOM nodes | 2,063 | 300 |

Before and after screenshots are in `TODO/screenshots/astro-spike/`.

### Build

`astro build` produces all 353 pages (255 content pages, 97 redirects, one status page) in about 6 seconds on a laptop. The Jekyll build of the same commit took 124 seconds in Docker on the same machine.

## What is not done

- Only `pages/_quests` is covered. Notes, about, digs, quest reports, the home page and the loose pages are untouched.
- No search, comments, analytics consent, page feedback widget, feeds or sitemap. Each has a known static replacement; none was built.
- The 12 pages above show a notice where the Jekyll site renders a widget.
- Heading anchors were not compared with kramdown's. In-page `#links` written for the Jekyll site may point at a different id.
- Diagram pages load Mermaid in the browser (about 208 KB compressed). Rendering diagrams at build time would remove that.
- Quest order inside a level is main quests first, then dependencies, then title. The front matter has no explicit order, so most levels read alphabetically.
- Accessibility was designed for (one focus ring, labelled checkboxes, reduced motion, both themes) but not audited.
- Front matter defaults live in `_config.yml` under Jekyll. Only the one that decides whether a page exists (templates are unpublished) is mirrored, in `src/content.config.ts`.
- Nothing is wired into the `Makefile`, CI or the deploy. `make build-ci` still builds Jekyll only.

## If this goes ahead

1. Record the decision as an ADR in `docs/adr/`, and the stack change in the hub registry.
2. Switch Pages to a GitHub Actions deploy. That workflow change is the maintainer's to make.
3. Move the remaining collections onto the same loader, then port the 12 widget pages as components.
4. Replace search, feeds, sitemap, comments and consent.
5. Cut over, then delete the translation layer one rule at a time by fixing the source files it compensates for.
