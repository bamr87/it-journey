---
applyTo: "**/*.py,**/*.js,**/*.ts,**/*.jsx,**/*.tsx,**/*.sh,**/*.bash,.github/workflows/*.yml,.github/workflows/*.yaml"
description: "Feature-building pipeline with end-to-end CI/CD conventions for IT-Journey source and workflow files"
date: 2025-10-17T17:25:30.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# Feature Pipeline & CI/CD

Standards for source code and GitHub Actions workflows that ship features in IT-Journey.

## 1. Feature Lifecycle (PDCA)

| Stage | Output |
|---|---|
| **PLAN** | Issue or RFC with goal, scope, acceptance criteria, prereqs |
| **DO** | Branch `feature/<slug>`, code + tests + docs in same PR |
| **CHECK** | CI green (lint + test + build + security scan), peer review |
| **ACT** | Merge → tag → release → monitor → retro note |

Every feature ships with: code, tests, docs update, frontmatter (if content), changelog entry.

## 2. Commit & Branch Conventions

```
<type>(<scope>): <imperative summary, ≤72 chars>

<body explaining why, not what>

Closes #<issue>
```

| Type | Use for | Branch |
|---|---|---|
| `feat` | New capability | `feature/<slug>` |
| `fix` | Bug fix | `bugfix/<slug>` |
| `docs` | Docs only | `docs/<slug>` |
| `refactor` | No behavior change | `refactor/<slug>` |
| `perf` | Speed/memory improvement | `perf/<slug>` |
| `test` | Tests only | `test/<slug>` |
| `chore` | Tooling, deps, CI | `chore/<slug>` |
| `ci` | Workflow changes | `ci/<slug>` |

Use `BREAKING CHANGE:` footer for incompatible changes (triggers MAJOR bump).

## 3. Source Code Standards

- **Languages used here:** Python 3.10+, Node 18+, Bash 3.2+ (with `set -euo pipefail`).
- **Lint:** Ruff (Python), ESLint (JS/TS), ShellCheck (bash). Zero warnings.
- **Format:** Black/Ruff format, Prettier, `shfmt`.
- **Types:** Required in Python (`from __future__ import annotations` + hints) and TypeScript.
- **Tests:** pytest, Jest/Vitest, Bats. Co-locate tests with code or under `test/`.
- **Coverage:** aim ≥ 80% on new code; never drop overall coverage by > 1%.

## 4. Required CI Jobs

Every workflow that builds a feature must run:

1. **Lint** — language-appropriate linter
2. **Test** — unit + integration; report coverage
3. **Build** — produce artifact under `work/output/` (see [`work.instructions.md`](work.instructions.md))
4. **Security scan** — `pip-audit`, `npm audit --production`, or `bundle audit`
5. **Secret scan** — `gitleaks` or `trufflehog`
6. **Frontmatter validation** — for content PRs (see `.github/workflows/frontmatter-validation.yml`)

CI must fail closed on any of these.

## 5. Minimal Workflow Skeleton

```yaml
name: ci
on:
  push:    { branches: [main] }
  pull_request:
permissions:
  contents: read
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  WORK_DIR: ${{ github.workspace }}/work

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: mkdir -p work/{cache,output,temp}
      - uses: actions/cache@v4
        with:
          path: work/cache
          key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - run: npm run build -- --out-dir=work/output
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: build, path: work/output/ }
```

Hardening rules: pin `actions/*` by major (`@v4`); never use `pull_request_target` unless absolutely required and reviewed; least-privilege `permissions:` block; `concurrency:` to cancel superseded runs.

## 6. Release Process

Semantic versioning driven by conventional commits:

| Commit footer / type | Bump |
|---|---|
| `BREAKING CHANGE:` | MAJOR |
| `feat:` | MINOR |
| `fix:`, `perf:`, `chore(deps):` | PATCH |
| `docs:`, `test:`, `chore:` | none |

Flow: merge → CI green → tag `vX.Y.Z` → GitHub Release with auto-generated notes → deploy.

## 7. Deployment

- **Continuous deploy** to GitHub Pages from `main` after CI green.
- **Manual gate** for production data-mutating workflows.
- **Rollback:** keep last 3 release tags; revert tag points to previous artifact.
- **Observability:** every deploy logs commit SHA, tag, environment, actor.

## 8. Documentation Requirements

A feature PR is incomplete without:

- [ ] README updated in affected directories (README-First/Last)
- [ ] `CHANGELOG.md` entry under `## [Unreleased]`
- [ ] Inline docstrings / JSDoc on new public API
- [ ] Quest, post, or doc page if the feature is user-facing
- [ ] Migration note if behavior changed

See [`README.instructions.md`](README.instructions.md), [`posts.instructions.md`](posts.instructions.md), [`quest.instructions.md`](quest.instructions.md).

## 9. PR Checklist

- [ ] Branch name follows convention
- [ ] Commits follow conventional format
- [ ] CI green (lint + test + build + security)
- [ ] Tests cover new behavior
- [ ] Docs updated (READMEs, CHANGELOG, frontmatter)
- [ ] No secrets, no `.env` files committed
- [ ] No `console.log`/`print` debug leftovers
- [ ] PR description references issue + lists user-visible changes

## 10. Security Non-Negotiables

- Never log secrets. Redact tokens, keys, passwords before logging.
- Validate all external input at the boundary.
- Pin dependencies; review Dependabot PRs weekly.
- Run `gitleaks detect` locally before pushing if you've touched config/env files.
- Use `${{ secrets.* }}` for credentials in workflows — never inline.

---

**Related:** [`scripts.instructions.md`](scripts.instructions.md) · [`work.instructions.md`](work.instructions.md) · [`contributing.instructions.md`](contributing.instructions.md).
