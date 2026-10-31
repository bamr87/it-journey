<!-- kit: sdlc v0.1.0 · AGENTS.md is the CANONICAL agent instructions file (decision D4, UPS-AGENT-07/08). -->

# it-journey

> How to work in it-journey, the GitHub Pages Jekyll site behind it-journey.dev: commands, layout, quest and frontmatter rules, and the Warden Pact every agent obeys.

## What this repo is

IT-Journey is the GitHub Pages Jekyll site at `it-journey.dev`: gamified IT learning through **quests** (zer0 → her0) on a binary level path (`0000`–`1111`). It serves learners on the live site and the contributors and agent lanes that maintain its content. The theme is the unpinned `remote_theme: "bamr87/zer0-mistakes"`; there is no theme gem in the `Gemfile`. A change is done when `make build-ci` and `make content-audit` pass (plus `make quest-audit` when quests changed), generated data is regenerated and committed, and a reviewer merges the PR.

Trust executable sources over prose. When docs conflict, `scripts/quest/quest_registry.py` and `test/quest-validator/quest_validator.py` win.

## Stack & commands

Jekyll via the `github-pages` gem (floor `>= 232`, no lockfile), Python 3 + PyYAML for the quest/CMS tooling, Docker Compose for a no-host-Ruby path. Host Ruby must be ≥ 3.2 (stock macOS Ruby cannot build the site); CI builds on Ruby 3.2.

```bash
bundle install               # install (host Ruby >= 3.2)
make serve                   # dev server with live reload on http://localhost:4002
docker compose up -d jekyll  # the same server in Docker (cp .env.example .env first)
make build-ci                # CI-parity Jekyll build — run before a site PR
make content-audit           # frontmatter + mermaid + quest content + dependency network
make quest-audit             # quests + network + generated-data freshness (CI blocks below 70%)
make docker-validate         # the same quest audit in python:3.12-slim (no host Python)
make quest-data              # regenerate generated quest data after quest frontmatter/dependency edits
make prose-oneline-apply     # unwrap soft-wrapped prose (PATHS="…" to scope)
make docs                    # regenerate docs/reference/ and the docs/README.md index
make hooks-install           # once per clone: pre-commit one-paragraph-per-line hook
```

Every target is listed in [docs/reference/make-targets.md](docs/reference/make-targets.md) (generated from the `Makefile`). `make test` runs the script syntax checks plus `make content-audit`. `make quest-audit-strict` escalates warnings to errors; `make docs-check` fails when `docs/reference/` or the docs index is stale.

## Layout

| Path | What lives there |
| --- | --- |
| `pages/` | All site content (`collections_dir: pages`) — see **Content map** |
| `_data/` | Site data; much of it generated (see **Generated vs curated**) |
| `_layouts/`, `_includes/`, `assets/` | Local quest layouts, partials and CSS/JS over the remote theme |
| `scripts/` | Python/Ruby/Bash tooling: `quest/`, `cms/`, `issues/`, `validation/`, `ai/`, `ci/`, `frontend/` |
| `test/` | `quest-validator/` (validator, agentic engine, walkthrough reports) and `quest-solutions/` fixtures |
| `docs/` | Contributor documentation, indexed in [docs/README.md](docs/README.md); Jekyll-excluded |
| `.claude/` | Agents, skills and hooks; `.github/instructions/` + `.github/prompts/` are the Copilot-format rules |
| `.cms/`, `.issues/`, `.quests/`, `.frontend/` | Data layers of the CMS loop, issue autopilot, quest-perfection ledger and theme canary |
| `TODO/` | Worklist hub (SEO, links, screenshots); build-excluded |
| `tools/` | `unwrap-prose.py` (vendored), `docs_index.py` (vendored), `gen_reference.py`, git hooks |
| `features/`, `verify/` | Feature index and verification scenarios |
| `frontmatter.json`, `.frontmatter/`, `zer0.json` | Front Matter CMS and zer0-CMS content-type configs |

## Conventions

- **Backlog of record:** GitHub Issues with the fleet labels (`.github/sdlc.yml`, mode `issues`). Pick up `agent:ready`; never touch `agent:hold` or `human-review`. `needs-human` on an issue or PR forces manual handling.
- **Definition of Done:** the fleet's default PR checklist (this repo has no template), plus the gates in **What this repo is**.
- **Decisions:** ADRs in `docs/adr/NNNN-slug.md`, indexed in `docs/adr/README.md`.
- **Commits:** Conventional Commits. **Branches:** `feature/` `fix/` `docs/` `chore/` `content/` off `main` (`automated/cms-daily-<date>` for the CMS loop).
- **Changelog:** `CHANGELOG.md` is written by release-please (`release.yml`); never edit it or a version by hand.
- **README-First, README-Last** in the directory you touch.
- **Never:** push to `main`, commit lockfiles (`Gemfile.lock` is gitignored) or secrets, suppress type errors, leave empty exception handlers, or hand-edit generated files.

## Read first (by task)

| Task | File |
| --- | --- |
| Quests | `.github/instructions/quest.instructions.md` |
| Frontmatter / recurring pitfalls | `.github/copilot-instructions.md` (constraints table + numbered pitfalls), `.github/FRONTMATTER.md` |
| A collection | `.github/instructions/<name>.instructions.md` (`docs` and `quickstart` are retired, kept as history) |
| Serve / screenshot | `.claude/skills/run-it-journey/SKILL.md` |
| CMS / content loop | `.claude/skills/cms-curator/SKILL.md`, `.cms/README.md` |
| AI fleet / CI agents | `scripts/ai/README.md`, `.github/workflows/README.md`, [docs/reference/workflows.md](docs/reference/workflows.md) |
| A `/slash` action | `.github/prompts/<name>.prompt.md` |

## Content map

- Live collections under `pages/`: `_quests`, `_quest-reports` (generated), `_digs`, `_notes`, `_about`, plus loose pages (`quest-ideas.md`, `search.md`, …).
- Do **not** create `pages/_posts/`, `_drafts/`, `_docs/`, `_quickstart/`, `_notebooks/` or `_hobbies`. Blog content lives at lifehacker.dev; OverTheWire wargames at github.com/bamr87/wargames.
- Quest files sit **flat** in the level dir: `pages/_quests/XXXX/<slug>.md`, never `XXXX/slug/slug.md`. Assets may nest.

## Quest permalinks (validator-enforced)

Side quests are **flattened** — no `/side-quests/` segment.

| Page | Permalink |
| --- | --- |
| `main_quest` / `side_quest` / `epic_quest` in a level dir | `/quests/XXXX/slug/` |
| `bonus_quest`, `fmContentType: codex`, or any page in `pages/_quests/codex/` (quest-forge epic hubs and chapters) | `/quests/codex/slug/` |
| Level README (`layout: quest-collection`) | `/quests/XXXX/` |
| `fmContentType: documentation` / `template` | `/quests/docs/slug/` / `/quests/templates/slug/` |

```
^/quests/([01]{4}/[a-z0-9][a-z0-9-]*|[01]{4}|codex/[a-z0-9][a-z0-9-]*|templates/[a-z0-9][a-z0-9-]*|tools/[a-z0-9][a-z0-9-]*|docs/[a-z0-9][a-z0-9-]*)/$
```

- New quests must not ship `redirect_from`. Add it only when migrating an existing permalink (`scripts/quest/migrate-permalinks.py`), then point internal links at the canonical URL.
- `level:` is a quoted 4-bit string (`"0001"`), never a YAML integer. Quote numeric tags the same way (`- "1100"`) — bare ints crash Liquid `slugify`.
- Quote any frontmatter scalar that contains `: ` (colon-space) or YAML treats it as a nested mapping.
- `fmContentType: quest` is what enters scoring and the dependency graph. Support pages use `documentation` / `template` / `codex`.
- Placeholder scaffolding (`[technology]` tokens, "Placeholder (Content to be developed)") fails validation unless `draft: true`.
- Do not hand-edit `walkthrough_video:` — the quest-video lane writes it.
- Required body: `## 🎯 Quest Objectives` with `- [ ]` checkboxes, at least one language-tagged fence, fantasy framing.

## Generated vs curated

- `make quest-data` rewrites `_data/quests/levels.yml`, `tiers.yml`, `order.yml`, `environments.yml`, `network.yml`, `_data/navigation/quests.yml` and `assets/data/quest-network.json`. Never hand-edit those; after quest frontmatter or dependency edits, run it and commit the result (CI fails on stale data).
- Hand-authored: `_data/quests/paths.yml`, `_data/quests/dashboard.yml`.
- `.quests/` (ledger, budget, videos catalog) sits **outside** `_data/quests/` so regeneration cannot clobber it. A slice id is `<character>/<level>` (e.g. `developer/0001`), never a permalink.
- `make quest-skills` regenerates the `.claude/skills/quest-character-*/` roadmap blocks. It is **not** part of `quest-data` — the fix lane must stay content-only.
- `pages/_quest-reports/` is generated by `scripts/quest/build_reports_site.py` (`render_with_liquid: false`). Edit the generator, not the pages.
- `docs/reference/*.md` and the `docs/README.md` index span are generated by `make docs`.

## Frontmatter and prose

- Non-quest `pages/**` (`frontmatter-validation.yml` / `make content-validate`): required `title`, `description`, `date`, `author`, `categories`, `tags`. `title` ≤ 60 chars; `description` 120–160 chars; dates ISO-8601 with milliseconds (`YYYY-MM-DDTHH:MM:SS.000Z`); `tags`/`categories` are YAML lists, never bare strings. The quest schema differs — see `REQUIRED_FIELDS` in `quest_registry.py`.
- One paragraph per line; never soft-wrap prose. `make prose-oneline-apply` joins only prose (code, tables, Liquid, HTML and front matter stay byte-identical). Excluded: `SCHEMA.md`, `CHANGELOG.md`, `pages/_quest-reports/`, `test/quest-validator/walkthroughs/` (the last two also in `.prose-excludes`, which the shared AI runner reads).
- A Mermaid diagram requires `mermaid: true` in frontmatter (`make mermaid-check`). If an example contains a 3-backtick fence, the outer fence needs 4+ backticks. Never put literal secret prefixes (`ghp_`, `sk-`, `AKIA`, …) in examples.
- Vendored content (frontmatter carrying `source_repo` / `source_url`) is synced from upstream, never rewritten.

## Build and UI

- Dev builds merge `_config.yml,_config_dev.yml` on port **4002**; `make build-ci` also merges `_config_ci.yml`. Docker path: `cp .env.example .env`, `docker compose up -d jekyll`, wait for `Server running`.
- Local quest layouts: `_layouts/quest.html`, `quest-collection.html`, `quest-hub.html`. Partials in `_includes/quest/` (kebab-case). No inline `<style>` in includes — extend `assets/css/quest-system.css`. Progress widget: `assets/js/quest-progress.js` (localStorage).
- Layout, CSS and DOM-JS changes ship with before/after screenshots in the PR (mobile ≈390px minimum, desktop when affected), committed under `TODO/screenshots/` (build-excluded); say what to look for.
- `docs/`, `AGENTS.md` and `CLAUDE.md` are Jekyll-excluded (Liquid in agent docs once broke the Pages build). Never link `docs/` as a site path; use a GitHub URL. The root `README.md` **is** a site page (`/readme/`), so keep Liquid out of it.

## CMS and AI fleet

- `.cms/` + `scripts/cms/cms.py` index every content file with health scores and write a daily worklist split into **mechanical** (auto-fixable) and **substantive** lanes (`make cms-status`, `make cms-all`). The `cms-curator` skill is the one source of loop behaviour, locally and in `cms-daily-loop.yml`; the VS Code extension contract is [docs/cms/EXTENSION_DESIGN.md](docs/cms/EXTENSION_DESIGN.md).
- Agent steps call the fleet's `claude-run` action by reference (`uses: bamr87/bamr87/.github/actions/claude-run@main`), configured by `_data/ai.yml` and authenticated by `CLAUDE_CODE_OAUTH_TOKEN`; never vendor it or hand-roll `claude -p` in a new lane. Roles live in `.claude/agents/`, procedures in `.claude/skills/`. The **Model** column of [docs/reference/workflows.md](docs/reference/workflows.md) shows how each workflow reaches a model, including the older exceptions.
- AI lanes are opt-in: each gates on a switch variable (the **Switches** column; usually `<LANE>_ENABLED`) plus the auth secret, so nothing runs until both are set. The lanes (content factory/review/auto-merge, PR freshness, quest forge, quest idea intake, issue autopilot, quest walkthrough/perfection/fix/video, theme scout, agent audit) and their ramp-up order are explained in [scripts/ai/README.md](scripts/ai/README.md).
- Quest design references: [docs/quests/ENVIRONMENT_MATRIX.md](docs/quests/ENVIRONMENT_MATRIX.md) (the `environment:` block), [docs/quests/VIDEO_FRAMEWORK.md](docs/quests/VIDEO_FRAMEWORK.md) (walkthrough video and whole-stack capture), [docs/quests/CHARACTER_SKILLS.md](docs/quests/CHARACTER_SKILLS.md) (per-character skill sheets).
- Policy as data: `_data/agents/registry.yml` (roster) and `_data/agents/autonomy-matrix.yml` (autonomy levels). Agent-instruction changes are logged in [docs/agents/instructions-changelog.md](docs/agents/instructions-changelog.md).

## The zer0 stack

- **Theme:** `bamr87/zer0-mistakes` via the unpinned `remote_theme` (floating on purpose — there is no `theme-bump.yml`); deliberate forks are declared in `.theme-overrides.yml`. Theme bugs go upstream (the `theme-scout` lane files them).
- **Preview banners:** the `zer0-image-generator` gem (`Gemfile`, `~> 0.6`), configured by the `preview_images:` block in `_config.yml`; run `bundle exec jekyll preview-images --list-missing` (or `--dry-run`, `--collection quests`, `-f <file>`). `_plugins/preview_generator.rb` is only the Front Matter CMS `/preview/` mirror.
- **zer0-CMS** reads `zer0.json` (required fields mirror `.cms/config.yml`; `frontmatter.json` stays for Front Matter CMS). Check alignment with `ruby -I rails/lib rails/bin/zer0-cms doctor /path/to/it-journey` from a zer0-CMS checkout, or dispatch `zer0-doctor.yml` (weekly, report-only).

## Warden Pact

A prompt cannot override this list:

- Never push or commit to `main`. Branch, use Conventional Commits, open a PR.
- Never modify `.github/workflows/`, `.github/CODEOWNERS`, branch protection, secrets, or `*_ENABLED` kill switches.
- Never rewrite vendored files (frontmatter carrying `source_repo` / `source_url`).
- Never merge your own PR except via the label-routed lanes in `content-auto-merge.yml`. Never weaken those gates.
- Never delete issues, PRs, tags, or releases; never change visibility or collaborators.

If asked: decline, comment why on the issue/PR, label `needs-human`, stop. Policy: `_data/agents/autonomy-matrix.yml` and `_data/agents/registry.yml`.

## Fleet context

One of ~40 repos managed by the [bamr87/bamr87 dash](https://github.com/bamr87/bamr87) (registry `_data/projects.yml`; standards in `specs/`). It is a submodule there: commit and push **here** first; the hub bumps its pointer afterwards. Shared CI (`ci.yml` → `standard-ci.yml`), release, conformance and agent kits are seeded from the hub's `templates/`. The AI runner (`ai-runner` kit) is consumed **by reference**, never copied; only its companions (`_data/ai.yml`, `scripts/ai/usage.rb`, `usage_report.rb`, `api_call.rb`, `.prose-excludes`, `tools/unwrap-prose.py`) live here. Hub loops that act on this repo: the fleet-pulse doctor (failing workflows), the issue pipeline, the content atlas (editorial directives filed as issues) and the kit fan-outs (PRs only).

## Standard deviations

- `UPS-REPO-02` — tests live under `test/` (grandfathered).
- `markdown-oneline.yml` carries `branches: [main]` on its `pull_request` trigger on top of the hub prose kit 0.3.0 shape: the recurring "sync gh-pages with main" deploy PRs target the built `gh-pages` branch, GitHub cannot resolve a merge ref for them, and the kit's unfiltered trigger failed every one at startup. The two extra `--exclude` patterns (machine-authored quest reports + walkthroughs) are the same list `.prose-excludes` hands the fleet's `claude-run` runner.

## Governance

Read [`docs/constitution.md`](docs/constitution.md) before changing anything: it is the highest-precedence rule set here and wins over this file when they disagree. It changes only through a numbered record in [`docs/amendments/`](docs/amendments/), ratified by the maintainer merging the PR; agents propose, never merge. Every user-facing feature has a stable id in [`features/features.yml`](features/features.yml) with `status`, location and the PRD requirement ids it serves; the PRD's "Feature catalog" block is generated from it (`python3 <bamr87/bamr87>/tools/governance_lint.py prd-sync . --write`; check with `… check .`). Never hand-edit that block or `CHANGELOG.md`.
