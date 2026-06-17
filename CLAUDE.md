# CLAUDE.md — Claude Code guide for IT-Journey

IT-Journey is a large **Jekyll** site (GitHub Pages, custom domain
`it-journey.dev`) teaching IT through gamified quests, tutorials, docs, and notes.
~650 content files live under `pages/` across 9 collections. The remote theme is
`bamr87/zer0-mistakes`.

This repo already has a deep instruction set written for Copilot/Cursor. **Read
the right file for the task** instead of guessing — they are authoritative.

## Read-by-task-type (do this before editing)

| Task | Read first |
|---|---|
| Anything | `AGENTS.md` (overview, commands, quest permalink regex, gotchas) |
| Frontmatter / content rules | `.github/copilot-instructions.md` (constraints table + numbered pitfalls), `.github/FRONTMATTER.md` |
| A specific collection | `.github/instructions/<name>.instructions.md` (posts, quest, index-hub, about, …) |
| Content curation / the daily loop | `.claude/skills/cms-curator/SKILL.md` + `.cms/README.md` |
| Running/previewing the site | `.claude/skills/run-it-journey/SKILL.md` |
| A `/slash` action | `.github/prompts/<name>.prompt.md` (15 prompt-agents: write-quest, draft-article, validate-content, publish-prep, retrospective, …) |

## The AI-augmented CMS (this repo's content layer)

The `.cms/` directory + `scripts/cms/cms.py` are the **content management
system**: a full-coverage index of every content file with health scores,
issues, and a daily worklist that splits work into **mechanical** (auto-fixable)
and **substantive** (needs authoring) lanes.

```bash
make cms-status     # health dashboard by collection
make cms-all        # rebuild .cms/index + .cms/reports/<date>.md + .cms/worklists/<date>.md
```

To run an incremental content-improvement pass, **invoke the `cms-curator`
skill** — it is the single source of loop behavior, used by both `/loop`
locally and the daily CI workflow (`.github/workflows/cms-daily-loop.yml`).
The future VS Code CMS extension (separate repo) reads `.cms/` too; see
`docs/cms/EXTENSION_DESIGN.md` for the contract.

## Essential commands

```bash
make serve            # local dev server (Docker via run-it-journey, port 4002)
make build-ci         # CI-parity Jekyll build — run before any PR
make content-audit    # frontmatter + quest + network validation
make content-normalize-apply   # deterministic frontmatter fixes (mechanical lane)
make quest-audit      # quest content + dependency network validation
make quest-data       # regenerate _data/quests/* after quest frontmatter edits
```

Host Ruby cannot build this site (needs Ruby ≥3.1 via `github-pages`); use the
Docker path documented in the `run-it-journey` skill.

## Non-negotiable conventions

- **Frontmatter is CI-enforced.** Required: `title, description, date, author,
  categories, tags`. `title` ≤ 60 chars; `description` 120–160; dates ISO-8601
  with ms (`YYYY-MM-DDTHH:MM:SS.000Z`); `tags`/`categories` are YAML lists. The
  PR will fail `frontmatter-validation` otherwise.
- **Never commit to `main`.** Branch with the repo's prefixes
  (`feature/ fix/ docs/ chore/ content/`) or `automated/cms-daily-<date>` for the
  loop. Conventional Commits.
- **Quests are registry-governed.** `_data/quests/*.yml` is generated from
  `scripts/quest/quest_registry.py`; never hand-edit it. After changing quest
  frontmatter run `make quest-data` or `quest-validation` CI fails on stale data.
- **Vendored content is read-only.** ~220 `pages/_docs/wargames/**` files carry
  `source_repo`/`license`; sync, never rewrite.
- **Validate before you push.** `make build-ci` + `make content-audit` (+ `make
  quest-audit` if quests changed) must pass.

## Repo map (quick)

- `pages/_<collection>/` — all site content (posts, quests, docs, notes,
  quickstart, about, hobbies, notebooks; loose `pages/` files).
- `_data/` — site data (quests/*, navigation/*, statistics). Much is generated.
- `scripts/` — Python/Ruby/Bash tooling (cms, quest, validation, generation, …).
- `.cms/` — CMS index, schema, reports, worklists (Jekyll-ignored).
- `.github/` — workflows, instructions, prompts (see each directory), copilot config.
- `TODO/` — worklist hub (SEO, links, reports). Excluded from the build.
- `frontmatter.json` + `.frontmatter/` — the Front Matter CMS VS Code config
  (content types, taxonomy, templates) the new CMS extends.
