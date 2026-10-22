---
title: Contributing
description: How to contribute to IT-Journey — the five-minute first pull request, the branch-commit-PR workflow, the local gates to run first, and where the detailed standards live.
slug: contributing
lastmod: 2026-10-22T00:00:00.000Z
date: 2021-09-03T18:09:27.000Z

---

# Contributing to IT-Journey

Thank you for your interest in contributing to IT-Journey! We welcome contributions from developers, content creators, and learners of all experience levels. The user-facing version of this guide is the [contributing page](https://it-journey.dev/about/contributing/) on it-journey.dev.

## 🚀 First-Time Contributor Fast Track

**New here? Make your first contribution in under 5 minutes!**

Perfect first contributions that require no setup:
- Fix a typo in a quest or a README
- Clarify a confusing step in a quest
- Add a comment to a code example

```bash
# 1. Fork this repo on GitHub (click "Fork" button)

# 2. Clone and create branch (replace YOUR-USERNAME)
git clone https://github.com/YOUR-USERNAME/it-journey.git
cd it-journey
git checkout -b fix/my-first-contribution

# 3. Make your change (example: fix typo in this file)

# 4. Commit and push
git add .
git commit -m "docs: fix typo in CONTRIBUTING.md"
git push origin fix/my-first-contribution

# 5. Create Pull Request on GitHub
```

Have an idea for a whole new quest? Shape it in the [Quest Idea Forge](https://it-journey.dev/quests/ideas/), which files it as an issue for review.

## Types of Contributions

- **Quests** — write a new quest or improve an existing one under `pages/_quests/` (see the [quest instructions](.github/instructions/quest.instructions.md)).
- **Notes** — cheatsheets and reference notes under `pages/_notes/`.
- **Code** — the validation, CMS and quest tooling under `scripts/` and `test/`.
- **Documentation** — the contributor docs indexed in [docs/README.md](docs/README.md).
- **Community** — answer questions, review pull requests, report what confused you.

Blog posts now belong to [lifehacker.dev](https://lifehacker.dev), not this repository.

## Contribution Workflow

```bash
# 1. Fork and clone
git clone https://github.com/YOUR-USERNAME/it-journey.git
cd it-journey

# 2. Create a branch: feature/, fix/, docs/, chore/ or content/
git checkout -b feature/your-feature-name

# 3. Preview your change at http://localhost:4002
make serve                    # host Ruby >= 3.2, after `bundle install`
docker compose up -d jekyll   # or in Docker (cp .env.example .env first)

# 4. Run the gates CI runs
make build-ci
make content-audit            # plus `make quest-audit` when quests changed
make prose-oneline-apply      # one paragraph per line in markdown

# 5. Commit with a conventional message, push, and open a pull request
git commit -m "feat(quest): add docker basics quest"
git push origin feature/your-feature-name
```

**Commit Message Format**: `<type>(<scope>): <description>`
- **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- **Scope**: Component affected (quest, notes, ci, scripts, etc.)
- **Description**: Brief summary in present tense

Layout, CSS or JavaScript changes need before/after screenshots in the pull request. The full rules — quest permalinks, the frontmatter contract, generated files you must not edit — are in [AGENTS.md](AGENTS.md).

## Documentation

### For Human Contributors
- **[Developer Contributing Guide](docs/CONTRIBUTING_DEVELOPER.md)** - Complete contribution workflow
- **[Development Environment](docs/setup/DEVELOPMENT_ENVIRONMENT.md)** - Setup instructions
- **[Content Guidelines](docs/standards/CONTENT_GUIDELINES.md)** - Writing standards
- **[Frontmatter Standards](docs/standards/FRONTMATTER_STANDARDS.md)** - Metadata requirements
- **[Documentation index](docs/README.md)** - Every document in the repository, one line each

### For AI Agents
- **[AGENTS.md](AGENTS.md)** - The canonical instructions every agent reads first
- **[Contributing Instructions](.github/instructions/contributing.instructions.md)** - How agents assist human contributors
- **[README Instructions](.github/instructions/README.instructions.md)** - Documentation standards
- **[Quest Instructions](.github/instructions/quest.instructions.md)** - Quest creation patterns
- **[Feature Instructions](.github/instructions/features.instructions.md)** - Feature development

### Reference
- **[Jekyll Implementation](docs/architecture/JEKYLL_IMPLEMENTATION.md)** - Jekyll details
- **[Workflow reference](docs/reference/workflows.md)** - CI/CD workflows (generated)
- **[Make targets](docs/reference/make-targets.md)** - Every `make` command (generated)
- **[Scripts Guide](docs/scripts/SCRIPTS_GUIDE.md)** - Automation tools
- **[Testing Frameworks](docs/testing/TESTING_FRAMEWORKS.md)** - Quality assurance

## Code of Conduct

Everyone taking part follows the [Code of Conduct](CODE_OF_CONDUCT.md): be respectful and inclusive, welcome newcomers, and keep feedback about the work, not the person.

## Getting Help

- Check the [documentation index](docs/README.md) first
- Search existing [issues](https://github.com/bamr87/it-journey/issues)
- Ask in [GitHub Discussions](https://github.com/bamr87/it-journey/discussions) or in your pull request
- Bug reports and feature requests: [open an issue](https://github.com/bamr87/it-journey/issues/new/choose)

## Recognition

Contributors are recognized through:
- Repository contributors page
- Release notes acknowledgments
- About page (for significant contributions)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
