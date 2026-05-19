---
applyTo: "**/*"
description: "Guide AI agents in assisting human contributors to IT-Journey (content, code, docs, community)"
date: 2025-11-07T16:47:19.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# Contributing Instructions for AI Agents

How AI agents help humans contribute to IT-Journey. Goal: lower friction, raise quality, preserve human authorship.

## Agent Role

- ✅ Detect intent, route to the right workflow, scaffold structure.
- ✅ Validate against checklists before suggesting commit.
- ✅ Generate commit messages and PR descriptions.
- ❌ Never push, merge, or comment on behalf of the user.
- ❌ Never decide product/editorial direction — surface options, let the human choose.

## Contribution Type Detection

Read the user's intent against this table; ask one clarifying question only if ambiguous.

| Signal | Type | Route to |
|---|---|---|
| "new quest" / files under `pages/_quests/` | Quest | `quest.instructions.md` |
| "blog post" / files under `pages/_posts/` | Post | `posts.instructions.md` |
| "fix doc" / `README.md`, `docs/**` edit | Documentation | `README.instructions.md` |
| "feature" / source under `scripts/`, `_includes/`, `assets/` | Code | `features.instructions.md` |
| "fix" / single-file edit + bug report | Bug fix | `features.instructions.md` |
| `.github/workflows/**` edit | CI/CD | `features.instructions.md` |

## Workflows

### Content (Quest / Post)

1. Confirm: title, audience level, learning objectives (or article angle).
2. Scaffold front matter per `quest.instructions.md` or `posts.instructions.md`.
3. Draft structure (sections + checkpoints, no filler prose).
4. User authors the actual prose. Agent assists with examples, code, validation.
5. Run validation (`scripts/validation/frontmatter-validator.py` etc.).
6. Generate commit message + PR description.

### Code (Feature / Fix)

1. Locate relevant files — read them before suggesting changes.
2. Confirm change scope and acceptance criteria.
3. Branch: `feature/<slug>` or `bugfix/<slug>`.
4. Implement minimum viable change. No unrelated refactors.
5. Add/update tests. Run them.
6. Update `CHANGELOG.md` and any touched READMEs (README-First/Last).
7. Generate commit + PR.

### Documentation

1. Read existing doc + linked docs to understand context.
2. Apply edits with conservative scope.
3. Verify links, frontmatter, `lastmod`.
4. Cross-update sibling docs if relationships changed.

## Pre-Submission Checklist

Run before suggesting commit:

- [ ] Front matter complete & valid (see file-specific instructions)
- [ ] `lastmod` updated on every edited file
- [ ] Links tested (`markdown-link-check` or equivalent)
- [ ] No literal secrets (`ghp_…`, `sk-…`, `AKIA…`)
- [ ] Tests pass (if code change)
- [ ] CHANGELOG entry added (user-visible changes)
- [ ] Related READMEs updated (README-First / README-Last)
- [ ] Branch name follows convention
- [ ] One logical change per PR

## Commit Message Generation

Conventional Commits, scopes match repo areas:

```
<type>(<scope>): <imperative subject ≤ 50>

<body explaining WHY, wrapped at 72>

Closes #<issue>
```

Types: `feat fix docs style refactor perf test chore ci`.
Common scopes: `quest post docs scripts workflows config`.

Example:

```
feat(quest): add docker-fundamentals quest at level 1010

Introduces 6-checkpoint quest covering image vs container,
volume mounts, and compose. Links to existing devcontainer post.

Closes #234
```

## Pull Request Template

```markdown
## Description
<what & why in 2-3 sentences>

## Type
- [ ] Feature
- [ ] Fix
- [ ] Docs
- [ ] Refactor
- [ ] CI

## Changes
- <bullet 1>
- <bullet 2>

## Related Issues
Closes #<n>

## Testing
- How verified
- Commands run

## Checklist
- [ ] Tests pass
- [ ] Docs/README updated
- [ ] CHANGELOG updated
- [ ] Lighthouse / a11y unchanged or improved (UI)
```

## PR Review Assistance

When asked to review a PR:

1. Read changed files in full, not just the diff.
2. Check against the relevant file-specific instructions.
3. Surface: missing tests, broken cross-refs, frontmatter issues, security risks.
4. Distinguish ❗ blocking from 💡 suggestion.

## Community Engagement

When directing users to community resources:

- Link to issues for bugs, discussions for questions, PRs for proposals.
- Reference `CODE_OF_CONDUCT.md` when behaviour issues arise.
- Suggest "good first issue" labelled items for newcomers.

## Continuous Improvement

After any contribution session, if a recurring friction is detected:

1. Suggest invoking `/retrospective` to capture the lesson.
2. Propose a one-line update to the relevant `.instructions.md` file.
3. Never modify instructions silently — always get user confirmation.

## Key Resources

- `.github/copilot-instructions.md` — core principles
- `.github/instructions/` — file-scoped rules
- `.github/prompts/` — reusable workflows
- `CONTRIBUTING.md` — human-facing contribution guide
- `CODE_OF_CONDUCT.md` — community standards

## Hard Rules

- Never assume push permissions — always produce a PR.
- Never auto-resolve review threads.
- Never edit files outside the declared scope of the PR.
- Never bypass the pre-submission checklist.

---

**Related:** [`README.instructions.md`](README.instructions.md) · [`features.instructions.md`](features.instructions.md) · [`quest.instructions.md`](quest.instructions.md) · [`posts.instructions.md`](posts.instructions.md)
