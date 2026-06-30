# CLAUDE.md — Claude Code guide for IT-Journey

IT-Journey is a **Jekyll** site (GitHub Pages, custom domain `it-journey.dev`): a
gamified, open-source platform for learning IT and software development through
**quests** (zer0 → her0). ~280 Markdown content files live under `pages/` across 5
collections — **quests** (~204, the center of gravity), `docs` (~27), a slim
`notes` set (~16), `quickstart` (~15), and `about` (~19), plus a few loose
`pages/` files. The remote theme is `bamr87/zer0-mistakes`.

> **Recent overhaul:** the `_posts`/`_drafts` blog, `_notebooks`, and `_hobbies`
> collections were removed. General blog content moved to **lifehacker.dev**
> (`github.com/bamr87/lifehacker.dev`); the OverTheWire `wargames` docs (+
> `scripts/docs-aggregator/`) were extracted to **`github.com/bamr87/wargames`**.

This repo already has a deep instruction set written for Copilot/Cursor. **Read
the right file for the task** instead of guessing — they are authoritative.

## Read-by-task-type (do this before editing)

| Task | Read first |
|---|---|
| Anything | `AGENTS.md` (overview, commands, quest permalink regex, gotchas) |
| Frontmatter / content rules | `.github/copilot-instructions.md` (constraints table + numbered pitfalls), `.github/FRONTMATTER.md` |
| A specific collection | `.github/instructions/<name>.instructions.md` (quest, docs, notes, about, quickstart) |
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

## The AI content fleet (Claude-Code-OAuth, on-brand, continuous)

The substantive (Lane B) half of the CMS is executed by a **fleet of Claude Code
agents** modeled on lifehacker.dev. All AI goes through one runner
(`scripts/ai/run.sh` + `_data/ai.yml` + the `.github/actions/claude-run` step),
authenticated by a `CLAUDE_CODE_OAUTH_TOKEN` secret. Roles are in
`.claude/agents/*.md`; the `content-curator` skill composes the existing
`cms-curator` + `brand-voice` skills. See **`scripts/ai/README.md`** for the full
map and setup.

- `content-factory.yml` (daily) — `content-curator` improves one page per
  collection from the `.cms` worklist → one `auto:content` PR each.
- `content-review.yml` (content PR) — `content-reviewer` editorial pass.
- `content-quality.yml` — deterministic `scripts/ci/brand_lint.py` gate; **spelling
  drift fails the check** (blocks auto-merge).
- `content-auto-merge.yml` — smuggle-guard (`classify_changes.py`, content-only) +
  checks-green → squash-merge.
- `quest-forge.yml` (issue labeled `epic-quest` / `/forge-quest` comment) — the
  `quest-forge` agent collects an epic-quest **proposal issue** deterministically
  (`scripts/quest/forge_issue.py`) and authors a full `epic_quest` hub +
  `bonus_quest` chapters in `pages/_quests/codex/` → one `auto:quest` PR. Closes the
  loop with lifehacker.dev (its quest-forge hook files the proposal; this consumes it).
- `quest-walkthrough.yml` (daily) — the `quest-walker` agent picks one linked
  (character, level) quest slice via `scripts/quest/walkthrough_plan.py`, **plays it
  end-to-end in the runner sandbox as a learner** (reusing the
  `test/quest-validator/agentic_validate.py` execute engine), and opens one report PR
  with evidence/issues/reasoning under `test/quest-validator/walkthroughs/`. Also
  uploads session screenshots (rendered quest pages + a terminal render of the
  recorded transcript, via `scripts/quest/walkthrough_screenshots.mjs`) as run
  artifacts. Read-only over content; never merges.
- `quest-perfection.yml` (daily) — the **autonomous quest-perfection loop**. For
  every character path it walks the highest-priority not-yet-perfect (character,
  level) slice, then `quest-fix.yml` opens a **separate** content-only fix PR that
  repairs only that walkthrough's *verified* issues (kept solely on a deterministic
  signal — tier-1 score + brand lint + sandbox commands — never the model's own
  grade) → auto-merges when green → repeats "until perfect". A committed ledger +
  generated dashboard in `.quests/` are the source of truth; staged kill switches
  `QUEST_PERFECTION_ENABLED` (orchestrator) and `QUEST_FIX_ENABLED` (write lane).
- `agent-audit.yml` (weekly) — `agent-auditor` keeps the fleet accurate/least-privilege.

**OFF by default.** Each workflow gates on a `*_ENABLED` repo variable **and** the
auth secret, so nothing runs until you add `CLAUDE_CODE_OAUTH_TOKEN` and flip the
variables. The old heuristic `ai-content-review.yml` (per-collection advisory
issue spam) was **replaced** by this fleet + the deterministic brand gate.

## Essential commands

```bash
make serve            # local dev server (Docker via run-it-journey, port 4002)
make build-ci         # CI-parity Jekyll build — run before any PR
make content-audit    # frontmatter + quest + network validation
make content-normalize-apply   # deterministic frontmatter fixes (mechanical lane)
make quest-audit      # quest content + dependency network validation
make quest-data       # regenerate _data/quests/* after quest frontmatter edits
```

Host Ruby cannot build this site (the `jekyll-theme-zer0` gem ≥1.21 needs Ruby
≥3.2); use the Docker path documented in the `run-it-journey` skill.

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
- **Vendored content is read-only.** Any upstream content carrying
  `source_repo`/`source_url` frontmatter is synced, never rewritten.
- **Validate before you push.** `make build-ci` + `make content-audit` (+ `make
  quest-audit` if quests changed) must pass.
- **UI/UX changes ship with before/after screenshots.** Any change that alters
  rendered layout, styling, or interaction (CSS/SCSS, templates/includes, nav,
  JS that affects the DOM) must include **before** and **after** screenshots in
  the PR — at minimum a **mobile** viewport (≈390px), plus desktop when the
  change affects it. Capture them by driving the running site (see the
  `run-it-journey` skill); a labeled side-by-side comparison is preferred.
  Commit the images under `TODO/screenshots/` (build-excluded) and embed them in
  the PR body. State what to look for, and call out that no other viewport
  regressed.

## Repo map (quick)

- `pages/_<collection>/` — all site content (quests, docs, notes, quickstart,
  about; loose `pages/` files). The brand/voice system governs only `quests` and
  `docs` (`_data/brand/sections/` holds just `quest.md` + `docs.md`).
- `_data/` — site data (quests/*, navigation/*, statistics). Much is generated.
- `scripts/` — Python/Ruby/Bash tooling (cms, quest, validation, generation, …).
- `.cms/` — CMS index, schema, reports, worklists (Jekyll-ignored).
- `.github/` — workflows, instructions, prompts (see each directory), copilot config.
- `TODO/` — worklist hub (SEO, links, reports). Excluded from the build.
- `frontmatter.json` + `.frontmatter/` — the Front Matter CMS VS Code config
  (content types, taxonomy, templates) the new CMS extends.
