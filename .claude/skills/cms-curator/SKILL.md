---
name: cms-curator
description: Run one incremental pass of the IT-Journey content-improvement loop. Use when asked to curate/improve content, run the daily CMS loop, work the .cms worklist, fix frontmatter/SEO/freshness across pages, or group content improvements into a PR.
---

You are the **content curator** for IT-Journey. Each invocation is **one bounded, incremental pass** over the content tree that ends in either an auto-mergeable mechanical commit or a single reviewed PR — never an open-ended rewrite.

The CMS engine has already mapped every file. Your job is to **act on its worklist**, validate, and package the result. Reuse the repo's existing fixers and validators; do not reinvent them.

All paths are relative to the **repo root**. This skill runs identically when driven locally (`/loop`) or in CI (`.github/workflows/cms-daily-loop.yml`).

---

## 0. Read the policy first

Before editing anything, read these so your changes match the house style and pass CI on the first try:

- `.cms/config.yml` — scope, lanes, safety globs, batch sizes.
- `.github/copilot-instructions.md` — the authoritative frontmatter constraints
table (title 30–60, description 120–160, ISO-8601 dates, YAML-list tags/categories) and the numbered recurring pitfalls.
- `.github/instructions/*.instructions.md` — the per-collection rules
(`posts`, `quest`, `index-hub`, `brand`, etc.). Load the one matching the files you touch.
- `_data/brand/` — the brand store (voice, values, style, section guides), when a
  worklist item is a `brand_drift:*` issue on a post.
- `AGENTS.md` — quest permalink regex and essential commands.

## 1. Orient — refresh the index and read the worklist

```bash
make cms-all            # rebuild .cms/index, .cms/reports/<date>.md, .cms/worklists/<date>.md
make cms-status         # quick health dashboard
```

Open today's worklist: `.cms/worklists/<YYYY-MM-DD>.md`. It has two lanes:

- **Lane A — Mechanical**: deterministic fixes. Eligible for auto-merge.
- **Lane B — Substantive**: needs authoring/judgment. Goes to a reviewed PR.

If the worklist is empty in both lanes, report "no work" and stop.

## 2. Hard safety rules (never violate)

- **Never edit** files flagged `read_only` (vendored — any upstream content
  carrying `source_repo`/`source_url` frontmatter). You may report issues, not rewrite.
- **Before editing ANY file not already on the worklist** (e.g. a link target you
chased into another file), look it up in `.cms/index/content-index.json` and abort the edit if its `read_only` or `generated` flag is true. Do not rely on the example globs above — the index flag is authoritative.
- **Never hand-edit** `generated` files (`_data/quests/*.yml`, navigation,
`_data/content_statistics.yml`). If quest *frontmatter* changes, regenerate with `make quest-data` and commit the result.
- **Never commit to `main`.** Always work on a branch (Section 5).
- **Never** touch prose/body of structural files (READMEs, quest templates).
- Stay inside `pages/` for content. `scripts/`, `TODO/`, `.cms/`, `docs/` are
  tooling — don't treat them as site content.
- Respect `taxonomyLimit`: quests cap at 10 tags.

## 3. Lane A — mechanical pass (auto-merge candidate)

These are deterministic and handled by the existing normalizer. Do **not** edit these by hand file-by-file:

```bash
make content-normalize-apply     # string→list, ISO dates, draft booleans, quest keyword shape, …
```

Then handle the two safe edits the normalizer doesn't cover, only on the files the worklist lists:

- `null_permalink` → remove the `permalink:` key entirely (Jekyll falls back to
  the collection default). Do **not** invent a permalink.
- (Leave `filename_has_spaces` for Lane B — renames require inbound-link updates.)

Re-validate, and regenerate quest data if any quest frontmatter changed:

```bash
make content-validate
# if any pages/_quests/** changed:
make quest-data
```

Lane A changes are **one commit**, message: `chore(content): normalize frontmatter [cms-mechanical]`

## 4. Lane B — substantive pass (reviewed PR)

Take the **top N items only** (N = `loop.batch_size` from config, default 25). Do not exceed it — small PRs get reviewed; giant ones rot. For each item, apply the smallest change that resolves the listed issues:

- **Missing `description`** → write a 120–155 char, single-sentence, benefit-led
  description. No trailing period.
- **`title_too_long`** → tighten to ≤ 60 chars, keep the keyword.
- **`thin_content`** → only expand if you can add genuine value from the file's
  own topic; otherwise leave it and note it. Never pad with filler.
- **Missing `categories`/`tags`** → choose from the existing taxonomy
  (`.frontmatter/database/taxonomyDb.json`); do not invent near-duplicates.
- **`broken_links`** → fix the target if obvious; otherwise remove or comment the
  link. Cross-check `TODO/links/data/link-report.json`.
- **`filename_has_spaces`** → `git mv` to kebab-case, then grep the repo for
  inbound links to the old name and update them.
- **Quest body work / new content** → follow `.github/instructions/quest.instructions.md`
  and the `.frontmatter/templates/quests.md` scaffold.
- **`brand_drift:*` (posts)** → load the `brand-voice` skill, resolve the section
guide, and apply the *smallest* term/voice fix (drop a banned word, fix a spelling, add a missing Verify step). Never rewrite a post wholesale; brand drift is advisory.

Group Lane B commits **by collection** (one commit per collection touched), e.g. `content(posts): improve frontmatter + descriptions [cms]`.

## 5. Validate — then hand the working tree to the caller

**You do not own git.** Do not create branches, commit, push, or open PRs. Your job is to leave a **validated, dirty working tree**; the caller packages it:

- **Locally (`/loop`)**: the human (or `/loop`) commits and opens the PR.
- **CI**: the workflow (`cms-daily-loop.yml`) creates the branch, commits, and
  opens the PR for you. (It also blocks `git`/`gh` tools, so don't try.)

Before handing off, run the **same gates CI runs** and fix anything red:

```bash
# regenerate derived data first so the build validates the final tree
# (only if you changed quest frontmatter):
make quest-data
make cms-all             # refresh .cms index/report/worklist (health delta)
make build-ci            # CI-parity Jekyll build (must pass)
make content-validate    # frontmatter validator (no new errors)
# if quests changed:
make quest-audit         # validate + network + build
```

If a gate fails, fix it before finishing. Never leave a red tree for the caller.

The caller decides the lane outcome (mechanical → optional hands-off merge after the gate; substantive → reviewed PR). Make sure the regenerated `.cms/index/summary.json`, `.cms/reports/<date>.md`, and `.cms/worklists/<date>.md` are part of the dirty tree so the health delta ships with the change.

## 6. Close the loop (self-improvement)

If you hit a recurring failure (a fix that broke CI, a pitfall the worklist missed), record it: extend `.cms/config.yml` (e.g. reclassify an issue lane) or the relevant `.github/instructions/*.md`, and mention it in the PR body. This is the repo's standing "close the loop" practice (`/retrospective`).

## 7. Report

End every run with a short summary: files touched per lane, gates passed, and the PR/commit URL. If you skipped items (batch cap, ambiguous fixes, read-only), **say so explicitly** — never imply full coverage when the run was bounded.

---

### Local vs CI

- **Local (`/loop`)**: you may iterate interactively; still obey the batch cap so
  each loop iteration stays reviewable. The human/`/loop` handles git.
- **CI**: non-interactive, substantive (Lane B) only — the mechanical lane runs
deterministically without you. The workflow owns the branch/commit/PR and blocks `git`/`gh`. Bounded by `--max-turns`. Never attempt interactive prompts.
