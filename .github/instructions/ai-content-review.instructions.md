---
applyTo: "pages/**/*.md"
description: "Guide GitHub Copilot when resolving AI Content Review issues — per-collection scope, frontmatter rules, fix patterns, validation, and PR conventions"
date: 2026-05-22T14:55:00.000Z
lastmod: 2026-05-22T14:55:00.000Z
---

# AI Content Review — Resolution Instructions

This file governs **how Copilot (or any contributor) resolves issues opened by the
[`ai-content-review.yml`](../workflows/ai-content-review.yml) workflow**.

Each AI-review issue is **scoped to a single Jekyll collection** (e.g. `_posts`,
`_quests`, `_docs`, `_about`, `_notes`, `_notebooks`, `_quickstart`, `_hobbies`)
and lists the files in that collection that need improvement. **Stay inside the
collection named in the issue title — do not edit files in other collections in
the same PR.**

---

## 1. Triage Order

Work through the issue in this order. Skip steps that don't apply.

1. **Frontmatter fixes** (always cheap, always first)
2. **SEO improvements** (title / description length)
3. **Content quality** (structure, headings, length)
4. **Technical accuracy** (code blocks, commands, links)
5. **Accessibility** (alt text, heading hierarchy)

If a single file has many issues, fix it fully before moving on — partial fixes
across many files are harder to review than complete fixes on fewer files.

---

## 2. Frontmatter Rules (Hard Requirements)

CI enforces these via `.github/workflows/frontmatter-validation.yml` and
`scripts/validation/content-reviewer.py`:

| Field | Required | Constraint |
|-------|----------|------------|
| `title` | ✅ | 30–60 characters |
| `description` | ✅ | 120–160 characters (optimal 120–155) |
| `date` | ✅ | ISO 8601 (`YYYY-MM-DDTHH:MM:SS.sssZ`) |
| `categories` | ✅ | YAML list, not a bare string |
| `tags` | ✅ | YAML list, not a bare string |
| `author` | ✅ | String (default `bamr87`) |
| `excerpt` | recommended | Short preview/RSS summary |
| `lastmod` | recommended | ISO 8601 — **update on every edit** |
| `draft` | recommended | Boolean `true`/`false` |
| `keywords` | recommended | 5–10 search phrases as a YAML list |

### Common Pitfalls (do NOT repeat)
- ❌ `categories: blog` — must be `categories: [blog]`
- ❌ `description:` cut off mid-sentence to hit the length cap — rewrite tighter instead
- ❌ Removing `draft: false` when editing existing files
- ❌ Forgetting to update `lastmod` after content changes
- ❌ README.md files inside `pages/_<collection>/` without full frontmatter

### Collection-Specific Required Fields
- **Quests** (`pages/_quests/**`): add `learning_objectives`, `target_audience`,
  `hierarchy`, `level`, `quest_id`, `difficulty`, `estimated_time`,
  `prerequisites`. See [`quest.instructions.md`](quest.instructions.md).
- **Posts** (`pages/_posts/**`): see [`posts.instructions.md`](posts.instructions.md).

---

## 3. Permalink Rules

Do not use `redirect_from:`. When a permalink changes, update every internal reference to the new canonical URL globally — no redirect stubs.

### Quests
- `main_quest` → `/quests/XXXX/slug/`
- `side_quest` → `/quests/XXXX/side-quests/slug/`
- Level README → `/quests/XXXX/`
- `codex` → `/quests/codex/slug/`

Old `level-XXXX-slug` and flat `side-quest-slug` patterns are invalid.

---

## 4. Content Quality Standards

- **Word count**: 100–3000 words per file. Split long files instead of trimming
  meaningful content.
- **Headings**: at least one H2; never skip heading levels.
- **Code blocks**: always specify a language for syntax highlighting
  (` ```bash`, ` ```python`, etc.).
- **Nested fenced code blocks** need a longer outer fence (4 backticks if inner
  uses 3).
- **No literal secrets**: never paste strings starting with `ghp_`, `gho_`,
  `ghu_`, `ghs_`, `ghr_`, `sk-`, `AKIA`, `xoxb-`. Use placeholders like
  `${env:GITHUB_TOKEN}` or `${input:openai-key}`.

---

## 5. Cross-References & Links

- `pages/_docs/**` → links to repo `docs/` directory must use **full GitHub
  URLs**, not relative paths (the `docs/` directory is excluded from Jekyll).
- Posts linked from non-post content require an explicit `permalink:` override —
  the default `/:collection/:year/:month/:day/:slug/` will 404 otherwise.
- After any link change, run a quick check: `python scripts/link-checker.py --scope local`.

---

## 6. Validation Before Pushing

Run these locally (or rely on CI). All must pass:

```bash
# Frontmatter
python scripts/validation/frontmatter-validator.py pages/_<collection>/path/to/file.md

# Content review (local rules only, no AI key needed)
python scripts/validation/content-reviewer.py \
  --files pages/_<collection>/path/to/file.md \
  --dry-run

# Build the site (catches Liquid/YAML errors)
bundle exec jekyll build
```

---

## 7. Pull Request Conventions

- **One PR per issue** (or per logical group of issues in the same collection).
- **Branch name**: `fix/ai-review-<collection>-<short-slug>`
  (e.g. `fix/ai-review-posts-2025-docker-quickstart`).
- **Commit message** (Conventional Commits):
  ```
  fix(content): address AI review feedback for _<collection>

  - Fixes #<issue-number>
  - Updates frontmatter on <N> files
  - Tightens descriptions to 120–155 chars
  - Adds missing alt text on images

  Closes #<issue-number>
  ```
- **PR description**: link the issue, list files changed, note any items
  deliberately deferred and why.
- **Always update `lastmod`** on every file you touch.

---

## 8. Out of Scope (do NOT do in an AI-review PR)

- ❌ Restructuring directories or renaming files
- ❌ Editing files outside the collection named in the issue
- ❌ Changing the workflow itself (`ai-content-review.yml`) — open a separate PR
- ❌ Rewriting the AI reviewer logic — open a separate PR
- ❌ Touching `.github/instructions/*.md` — open a separate PR
- ❌ Bulk dependency upgrades

If the review flags something out of scope, leave a comment on the issue noting
it and open a follow-up issue.

---

## 9. When You Can't Resolve an Item

Mark the item with a checkbox in the issue and add a brief reason:

```markdown
- [ ] ~~Add learning_objectives to legacy post~~ — skipped: post predates schema, see #999
```

Then proceed with the rest. Don't block the entire issue on one ambiguous item.

---

## 10. Related Resources

- [`copilot-instructions.md`](../copilot-instructions.md) — core principles
- [`README.instructions.md`](README.instructions.md) — README-First / README-Last
- [`posts.instructions.md`](posts.instructions.md) — blog-post-specific rules
- [`quest.instructions.md`](quest.instructions.md) — quest-specific rules
- [`.github/content-review-config.yml`](../content-review-config.yml) — thresholds and tag keywords
- [`scripts/validation/content-reviewer.py`](../../scripts/validation/content-reviewer.py) — review engine
- [`scripts/validation/create-review-issues.py`](../../scripts/validation/create-review-issues.py) — issue grouping & assignment
