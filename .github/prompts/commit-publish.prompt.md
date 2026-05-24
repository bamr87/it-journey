---
mode: agent
description: "Review changes, run tests, update docs, then commit and publish IT-Journey Jekyll site via PR"
date: 2025-11-26T22:17:42.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# Commit & Publish — IT-Journey

When invoked with `/commit-publish`, walk through the publish workflow: review → test → document → commit → PR. IT-Journey is a Jekyll site deployed via GitHub Pages on push to `main`.

## Steps

### 1. Review Changes

```bash
git status --short
git diff --stat
```

For each changed file, classify: `quest | post | doc | code | config | ci`.
Surface anything unexpected (large binaries, secrets, generated `_site/`).

Refuse to proceed if any file contains literal secret prefixes (`ghp_…`, `sk-…`, `AKIA…`).

### 2. Run Tests

Match tests to change types:

| Changed | Run |
|---|---|
| `pages/_quests/**` | `make quest-audit` (rebuilds network + validates content and dependencies) |
| `pages/_posts/**` or `pages/_docs/**` | `python3 scripts/validation/frontmatter-validator.py <paths>` |
| any `*.md` | `python3 scripts/link-checker.py --scope website --timeout 30` |
| `scripts/**`, `_includes/**`, `_layouts/**`, `_config*.yml` | `docker-compose exec -T jekyll bundle exec jekyll build` |

Stop if any test fails.

### 3. Update Documentation

For every directory touched, update its `README.md`:

- Add new files to file listings.
- Update `lastmod` in front matter.
- Cross-reference related quests/posts if relationships changed.

If a feature was added/changed, also update:

- Root `README.md` (only if user-visible)
- `pages/_about/features/index.md` (for major features)
- Related quest navigation (if quest progression affected)

### 4. Update CHANGELOG.md

Add to `## [Unreleased]` at top:

```markdown
### Added | Changed | Fixed | Removed | Security
- **<area>**: <one-line> ([#PR](url))
```

### 5. Validate Build

```bash
docker-compose up -d jekyll
docker-compose exec -T jekyll bundle exec jekyll build \
  --config '_config.yml,_config_dev.yml'
```

Fail = stop and report.

### 6. Commit

```bash
git add -A
git commit -m "<type>(<scope>): <imperative subject>

<body explaining why>

Closes #<n>"
```

Types: `feat fix docs refactor chore ci`.
Common scopes: `quest post docs scripts workflows config`.

### 7. Open PR to `main`

```bash
git push -u origin <branch>
gh pr create --base main --title "<same as commit subject>" \
  --body-file - <<EOF
## Summary
<2-3 sentences>

## Changes
- <bullet>
- <bullet>

## Testing
- <commands run>

## Checklist
- [x] Tests pass
- [x] Docs updated
- [x] CHANGELOG updated
- [x] No secrets / generated files committed
EOF
```

Deployment happens automatically on merge to `main` via GitHub Pages.

### 8. Verify Publication

After merge, give it 1-2 minutes, then:

```bash
curl -sI https://it-journey.dev/<changed-path>/ | head -1   # expect HTTP/2 200
```

Check `https://it-journey.dev` renders the change.

## Output to User

```markdown
## Release Summary — <YYYY-MM-DD>

### Changes
- <bullet>

### Tests
| Check | Result |
|---|---|
| Frontmatter | ✅ |
| Quest validator | ✅ |
| Link checker | ✅ |
| Jekyll build | ✅ |

### Files Modified
- N quests, N posts, N docs, N scripts

### Commit / PR
- Commit: <sha>
- PR: <url>

### Publication
- Branch pushed: ✅
- PR opened: ✅
- Deployment: pending merge
```

## Rollback

If a published change breaks the site:

```bash
git revert <bad-sha>
git push origin main
```

Then open a PR fixing the issue forward — never force-push to `main`.

## Hard Rules

- Never push directly to `main`. Always use PR.
- Never skip the build validation in step 5.
- Never commit `_site/`, `vendor/`, `.bundle/`, or `*.gem`.
- Never commit without updating relevant READMEs (README-First/Last).
- Never advance to next step on test failure.

---

**Related:** [`.github/instructions/contributing.instructions.md`](../instructions/contributing.instructions.md) · [`.github/instructions/README.instructions.md`](../instructions/README.instructions.md)
