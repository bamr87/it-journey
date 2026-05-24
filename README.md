---
title: README - it-journey
description: IT-Journey - Your comprehensive learning platform with QuickStart tutorials, gamified quests, documentation library, and personal notebooks.
excerpt: IT-Journey combines quick tutorials, epic quests, comprehensive documentation, and personal notebooks in an interconnected learning ecosystem
version: 0.0.1
date-released: 2022-03-01
repo: https://github.com/bamr87/it-journey
tags:
    - it-journey
    - jekyll
    - gamified-learning
    - learning-path
    - tutorials
    - documentation
license: MIT
lastmod: 2026-05-24T19:12:05.000Z
created: 2022-03-01T12:00:00.000Z
draft: false
slug: readme
keywords:
    - readme
    - it-journey
    - learning-platform
    - tutorials
    - quests
    - documentation
    - jupyter-notebooks
permalink: /readme/
layout: home
date: 2020-07-30T10:19:45.000Z

---

# IT-Journey

**Open-source learning platform that takes you from `zer0` to `her0`** — built with Jekyll, gamified with quests, and maintained as a working example of modern documentation, automation, and AI-assisted workflows.

🌐 **Live site:** [it-journey.dev](https://it-journey.dev) · 📜 **License:** MIT · 🛠 **Theme:** [`bamr87/zer0-mistakes`](https://github.com/bamr87/zer0-mistakes)

The repository is two things at once:

1. **A learning platform** — gamified quests, blog posts, notes, Jupyter notebooks, and reference docs covering system administration, web development, DevOps, and AI integration.
2. **A reference project** — a real Jekyll site with CI/CD, content validation, link health monitoring, a TUI navigator, and a documented contributor workflow you can study and reuse.

---

## 🚀 Quick Start

### Browse with the TUI

```bash
brew install gum glow      # macOS (or see https://github.com/charmbracelet/gum)
./journey.sh               # interactive terminal navigator
```

### Run the site locally

```bash
# Ruby + Jekyll (matches the dev config used by Docker)
bundle install
make serve                                # bundle exec jekyll serve on port 4002
# → http://localhost:4002
```

Equivalent without `make`:

```bash
bundle exec jekyll serve --config _config.yml,_config_dev.yml --port 4002
```

### Run the site in Docker

```bash
docker compose up        # uses Dockerfile + docker-compose.yml
```

### Other common commands

| Task | Command |
|------|---------|
| Production-style build (remote theme) | `make build-prod` |
| CI smoke build (matches PR workflow) | `make build-ci` |
| Clean `_site` and Jekyll caches | `make clean` |
| Generate content statistics | `make stats` |
| Validate all quests | `make quest-validate` |
| Full quest audit (CI parity) | `make quest-audit-strict` |
| Rebuild quest dependency network | `make quest-build-network` |
| Regenerate sidebar quest navigation | `make quest-nav` |
| Check links locally | `python3 scripts/validation/link-checker.py --scope website` |
| Show all `make` targets | `make help` |

---

## 🗺 Repository Layout

```
it-journey/
├── pages/                  # All Jekyll-published content
│   ├── _quests/            # Gamified learning quests (binary-leveled 0000–1111 + codex)
│   ├── _posts/             # Blog posts: tutorials, chronicles, reviews
│   ├── _notes/             # Working notes, journals, code snippets
│   ├── _notebooks/         # Jupyter notebooks + writeups
│   ├── _docs/              # Learner-facing tool & technology references
│   ├── _about/             # Project info, features, contributor profiles
│   ├── _hobbies/           # Personal/hobby content
│   ├── _quickstart/        # Onboarding guides (incl. Charm tools setup)
│   └── _drafts/            # Work-in-progress drafts
├── docs/                   # Developer / maintainer documentation
├── scripts/                # Automation: validation, generation, deployment, tooling
├── _layouts/  _includes/  _data/  _plugins/   # Jekyll internals
├── assets/                 # CSS, JS, images, SVG, GIF
├── .github/                # Workflows, instructions, prompts, agents
├── TODO/                   # PDCA-style task tracking hub
├── features/               # Feature flag / catalog data
├── _config.yml             # Production Jekyll config (port 4002)
├── _config_dev.yml         # Local development overrides
├── _config_ci.yml          # CI smoke-build overrides
├── Makefile                # Stats + Jekyll build + quest tooling targets
├── journey.sh              # Gum/Glow TUI navigator
├── init_setup.sh           # First-time environment bootstrap
├── Dockerfile / docker-compose.yml
├── Gemfile / Gemfile.lock
├── PRD.md                  # Living product requirements (auto-generated)
├── roadmap.md              # Active and long-term direction
├── AGENTS.md               # Operating guide for AI agents in this repo
├── CONTRIBUTING.md / CODE_OF_CONDUCT.md / SECURITY.md / CHANGELOG.md
└── index.md                # Site landing page
```

---

## 📚 Content Collections

| Collection | Path | Purpose | Notable subdirs |
|------------|------|---------|-----------------|
| **Quests** | `pages/_quests/` | Gamified, step-by-step learning adventures | `0000/`–`1111/` (binary levels), `codex/`, `templates/`, `tools/`, `inventory/` |
| **Posts** | `pages/_posts/` | Tutorials, AI-session chronicles, technology reviews | Organized by topic |
| **Notes** | `pages/_notes/` | Short-form notes, journals, references | — |
| **Notebooks** | `pages/_notebooks/` | Jupyter `.ipynb` + Markdown writeups | — |
| **Learner Docs** | `pages/_docs/` | Tool, framework, and technology references | `jekyll/`, etc. |
| **About** | `pages/_about/` | Project info, features, profiles | — |
| **Quickstart** | `pages/_quickstart/` | Beginner onboarding | — |

### Quests in depth

Quests use a **binary level system** (`0000` → `1111`) to introduce computational thinking from day one. Each quest follows a fantasy / RPG narrative, declares explicit learning objectives, and is validated by `test/quest-validator/`.

- **Permalinks** follow a strict canonical form:
  - Main quest → `/quests/XXXX/slug/`
  - Side quest → `/quests/XXXX/side-quests/slug/`
  - Codex (epic/bonus) → `/quests/codex/slug/`
  - Level README → `/quests/XXXX/`
- **Validation** is enforced by CI (`.github/workflows/quest-validation.yml`); the local audit lives behind `make quest-audit` / `make quest-audit-strict`.
- **Templates** for new quests live in `pages/_quests/templates/`.

Start here: [`pages/_quests/0000/begin-your-it-journey.md`](pages/_quests/0000/begin-your-it-journey.md) · Full index: [`pages/_quests/home.md`](pages/_quests/home.md)

---

## 🛠 Development Tooling

### `scripts/` — automation toolbox

| Subdir | What's there |
|--------|--------------|
| `core/` | Environment setup, version management |
| `deployment/` | Azure Static Web Apps deployment, settings updates |
| `development/` | Build, content, and testing helpers |
| `generation/` | Statistics, contributor stats, preview images, zer0-to-her0 scripts |
| `validation/` | Frontmatter validator, content reviewer, link checker, CTR/SEO reports |
| `quest/` | Quest network builder, permalink migration, navigation generator, registry |
| `prd-machine/` | Auto-generates `PRD.md` from repository state |
| `docs-aggregator/` | Pulls developer docs together |
| `testing/` · `utils/` · `lib/` | Test helpers, shared utilities, Python libs |

### `_config_*` — three Jekyll configs

| File | Used for |
|------|----------|
| `_config.yml` | Production / GitHub Pages |
| `_config_dev.yml` | Local development (theme path, drafts, etc.) |
| `_config_ci.yml` | Faster CI smoke builds |

### Quest pipeline

```
write quest  →  make quest-validate   (frontmatter, structure, fantasy theme)
            →  make quest-build-network  (dependency graph → quest-network.json)
            →  make quest-audit-strict   (CI parity: errors + orphan warnings)
```

---

## ⚙️ CI/CD — GitHub Actions

Sixteen workflows live in [`.github/workflows/`](.github/workflows/):

| Workflow | Purpose |
|----------|---------|
| `build-validation.yml` | Jekyll build check on PRs |
| `frontmatter-validation.yml` | Required-field & format checks on Markdown |
| `quest-validation.yml` | Runs `quest_validator.py` + network checks |
| `posts-markdown-lint.yml` | Markdown lint for blog posts |
| `link-checker.yml` | Link Health Guardian (Lychee + Python, optional AI summaries) |
| `ai-content-review.yml` | AI-assisted content review issues |
| `codeql-analysis.yml` | Security scanning |
| `dependency-checker.yml` | Dependency drift / vulnerability checks |
| `azure-jekyll-deploy.yml` | Deploy to Azure Static Web Apps |
| `auto-pr.yml` | Automation around PR creation |
| `prd-sync.yml` | Regenerates `PRD.md` from repo state |
| `organize-posts-weekly.yml` | Scheduled post reorganization |
| `update-contributor-profiles.yml` | Refresh contributor data |
| `update-settings.yml` | Sync repository settings |
| `new-feature-request.yml` | Issue-to-feature scaffolding |
| `validate-solutions.yml` | Solution validation |

See [`.github/workflows/README.md`](.github/workflows/README.md) for full descriptions.

---

## 🤖 AI Workflows

This repo is built **with** AI agents, not just for them.

- **`AGENTS.md`** — operating guide for AI agents working in the repository (project overview, commands, gotchas).
- **`.github/copilot-instructions.md`** + **`.github/instructions/`** — file-scoped rules (quests, posts, scripts, prompts, READMEs, features, AI content review).
- **`.github/prompts/`** — reusable prompt files including `/retrospective` (folds session lessons back into instructions) and `/kaizen` (continuous code improvement).
- **`scripts/prd-machine/`** — generates the living `PRD.md`.
- **`ai-content-review.yml`** — opens issues with AI-assisted suggestions on Markdown content.
- Link Health Guardian can optionally use OpenAI or Anthropic keys to summarize broken-link clusters.

---

## 📊 Snapshot (as of 2026-05-24)

| What | Count |
|------|-------|
| Quest files (`pages/_quests/**/*.md`) | 223 |
| Posts (`pages/_posts/**/*.md`) | 95 |
| Notes (`pages/_notes/**/*.md`) | 40 |
| Notebooks (`.ipynb` + writeups) | 6 + 5 |
| Learner docs (`pages/_docs/**/*.md`) | 240 |
| Developer docs (`docs/**/*.md`) | 24 |
| About pages | 16 |
| Quickstart pages | 15 |
| Automation scripts (`.sh` + `.py`) | 57 |
| GitHub Actions workflows | 16 |

Live numbers are regenerated by `make stats` into [`_data/content_statistics.yml`](_data/content_statistics.yml).

---

## 📖 Where to Read Next

| If you want to… | Go to |
|-----------------|-------|
| Start learning | [`pages/_quests/0000/begin-your-it-journey.md`](pages/_quests/0000/begin-your-it-journey.md) |
| See the full quest map | [`pages/_quests/home.md`](pages/_quests/home.md) |
| Understand the dev environment | [`docs/setup/DEVELOPMENT_ENVIRONMENT.md`](docs/setup/DEVELOPMENT_ENVIRONMENT.md) |
| See the directory layout in detail | [`docs/architecture/REPOSITORY_STRUCTURE.md`](docs/architecture/REPOSITORY_STRUCTURE.md) |
| Read Jekyll implementation notes | [`docs/architecture/JEKYLL_IMPLEMENTATION.md`](docs/architecture/JEKYLL_IMPLEMENTATION.md) |
| Contribute | [`CONTRIBUTING.md`](CONTRIBUTING.md) + [`docs/CONTRIBUTING_DEVELOPER.md`](docs/CONTRIBUTING_DEVELOPER.md) |
| Follow content standards | [`docs/standards/CONTENT_GUIDELINES.md`](docs/standards/CONTENT_GUIDELINES.md), [`docs/standards/FRONTMATTER_STANDARDS.md`](docs/standards/FRONTMATTER_STANDARDS.md) |
| Run the automation scripts | [`scripts/README.md`](scripts/README.md) |
| Track project tasks | [`TODO/README.md`](TODO/README.md) |
| See the product direction | [`PRD.md`](PRD.md), [`roadmap.md`](roadmap.md) |
| Work as an AI agent | [`AGENTS.md`](AGENTS.md) + [`.github/copilot-instructions.md`](.github/copilot-instructions.md) |

---

## 🤝 Contributing

Contributions of every size are welcome — fixing a typo, adding a quest, improving validation tooling, or proposing a new collection.

- **Five-minute first PR:** see [CONTRIBUTING.md → First-Time Contributor Fast Track](CONTRIBUTING.md#-first-time-contributor-fast-track)
- **Branching & commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, …) with kebab-case prefixes (`feature/`, `bugfix/`, `docs/`, `chore/`)
- **README-First, README-Last:** every change reads the relevant `README.md` *before* and updates it *after* — see [`.github/instructions/README.instructions.md`](.github/instructions/README.instructions.md)
- **Community standards:** [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- **Security issues:** [SECURITY.md](SECURITY.md)

---

## 📞 Support

| Channel | Use for |
|---------|---------|
| [GitHub Issues](https://github.com/bamr87/it-journey/issues) | Bug reports, feature requests |
| [GitHub Discussions](https://github.com/bamr87/it-journey/discussions) | Questions, ideas, quest help |
| [CHANGELOG.md](CHANGELOG.md) | What changed, when, and by whom |

---

## 📄 License

[MIT](LICENSE) — free to use, fork, remix, and learn from. Attribution welcomed but not required.

---

*Ready to begin? Open the [first quest](pages/_quests/0000/begin-your-it-journey.md) or fire up [`./journey.sh`](journey.sh) and pick your path.*
