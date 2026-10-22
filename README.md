---
title: README - it-journey
description: IT-Journey is a gamified, open-source platform for learning IT and software development through quests — progressive, hands-on adventures from zer0 to her0.
excerpt: A gamified, open-source platform for learning IT and software development through quests — progressive, hands-on adventures from zer0 to her0.
version: 0.0.1
date-released: 2022-03-01
repo: https://github.com/bamr87/it-journey
tags:
    - it-journey
    - jekyll
    - gamified-learning
    - learning-path
    - quests
    - documentation
license: MIT
lastmod: 2026-10-22T00:00:00.000Z
created: 2022-03-01T12:00:00.000Z
draft: false
slug: readme
keywords:
    - readme
    - it-journey
    - learning-platform
    - quests
    - gamified-learning
    - documentation
permalink: /readme/
layout: home
date: 2020-07-30T10:19:45.000Z

---
# IT-Journey

> Gamified, open-source platform for learning IT and software development through hands-on quests, zer0 to her0.

[![CI](https://github.com/bamr87/it-journey/actions/workflows/ci.yml/badge.svg)](https://github.com/bamr87/it-journey/actions/workflows/ci.yml) [![License](https://img.shields.io/github/license/bamr87/it-journey)](LICENSE) [![Live site](https://img.shields.io/badge/live-it--journey.dev-2ea44f)](https://it-journey.dev/)

## Overview

IT-Journey turns IT and software-development learning into **quests**: fantasy-framed, hands-on lessons on a binary level path from Level `0000` (Apprentice: first terminal, first Git commit) to Level `1111` (Legend). Each quest has objectives you tick off, commands you actually run on macOS, Windows or Linux, and links to the quests it unlocks. The site is published at [it-journey.dev](https://it-journey.dev/).

This repository is both the learning site and a working example of the platform behind it: a Jekyll site on GitHub Pages, validation tooling that scores every quest, and opt-in AI agents that walk, review and repair the curriculum through pull requests a human merges.

> Looking for the blog? Articles, reflections, and devops news now live at **[lifehacker.dev](https://lifehacker.dev)**.

## Features

- **Quests on a binary level path** — `pages/_quests/0000/` through `1111/`, plus codex campaigns and templates; start with [Begin your IT Journey](pages/_quests/0000/begin-your-it-journey.md).
- **Six character paths** — Software Developer, System Engineer, Security Specialist, Data Scientist, Digital Artist (UI/UX) and Game Developer, each a curated chain of levels (`_data/quests/paths.yml`).
- **A quest dependency network** — every quest declares what it requires, recommends and unlocks; the graph is generated into `_data/quests/network.yml` and `assets/data/quest-network.json`.
- **Reader-configurable quests** — an environment control picks the reader's OS and folder and rewrites snippets to match (`assets/js/quest-env.js`); progress is kept in the browser (`assets/js/quest-progress.js`).
- **Quest Idea Forge** — a portal at [/quests/ideas/](https://it-journey.dev/quests/ideas/) that shapes a visitor's quest idea and files it as an issue for review.
- **Notes, digs and quest reports** — cheatsheets and a notes workbench (`/notes/`), Git-archaeology write-ups of this repository's history (`/digs/`), and the walkthrough reports the quest-perfection loop publishes (`/quest-reports/`).
- **Validation tooling** — a quest validator with a 70% quality floor, a dependency-network validator, a frontmatter validator, a brand-voice lint, a Lychee link checker, and Lighthouse/accessibility checks on pull requests.
- **Opt-in AI lanes** — Claude Code agents that improve content, review PRs, walk quests end-to-end in a sandbox and open fix PRs; each lane is off until its switch variable is set ([scripts/ai/README.md](scripts/ai/README.md)).

## Quick start

Read a quest on [it-journey.dev](https://it-journey.dev/), or run the site locally:

```bash
git clone https://github.com/bamr87/it-journey.git
cd it-journey
```

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

`make serve` needs host Ruby 3.2 or newer (stock macOS Ruby cannot build the site); the Docker path needs only Docker. Either way the site serves on port **4002**. Every `make` target is listed in [docs/reference/make-targets.md](docs/reference/make-targets.md).

## Documentation

- [docs/README.md](docs/README.md) — the index of every document in the repository, one line each.
- [AGENTS.md](AGENTS.md) — commands, layout, conventions and the rules agents and contributors follow.
- [scripts/ai/README.md](scripts/ai/README.md) — the AI runner and the content, issue and quest lanes.
- [.github/instructions/quest.instructions.md](.github/instructions/quest.instructions.md) — how to write a quest that passes validation.

## Project structure

| Path | What lives there |
| --- | --- |
| `pages/` | Site content: `_quests`, `_quest-reports` (generated), `_notes`, `_digs`, `_about`, plus loose pages |
| `_data/` | Site data: quest registry outputs, navigation, brand, agent policy |
| `_layouts/`, `_includes/`, `assets/` | Quest layouts, partials and CSS/JS layered over the `zer0-mistakes` remote theme |
| `scripts/` | Python, Ruby and Bash tooling for quests, the CMS loop, validation and the AI lanes |
| `test/` | The quest validator, the agentic quest engine, walkthrough reports and solution fixtures |
| `docs/` | Contributor documentation (not published on the site) |
| `.github/` | Workflows, Copilot instructions and prompts, issue templates |

## Development

Validate before you open a pull request: `make build-ci` and `make content-audit`, plus `make quest-audit` when quests changed (CI blocks a quest scoring below 70%). Markdown is one paragraph per line (`make prose-oneline-apply`). After changing quest frontmatter or dependencies, run `make quest-data` and commit the regenerated data. The full set of commands, the quest permalink rules and the frontmatter contract are in [AGENTS.md](AGENTS.md).

## Contributing

Contributions from learners and experts are welcome: fix a typo, improve a quest, or propose a new one through the [Quest Idea Forge](https://it-journey.dev/quests/ideas/). Start with [CONTRIBUTING.md](CONTRIBUTING.md), follow the [Code of Conduct](CODE_OF_CONDUCT.md), and read [AGENTS.md](AGENTS.md) before larger changes. Report bugs and ask questions through [GitHub Issues](https://github.com/bamr87/it-journey/issues).

## Related projects

| Project | Where | What |
| --- | --- | --- |
| **Blog** | [lifehacker.dev](https://lifehacker.dev) | Articles, tutorials, reflections, and devops news that used to live here |
| **Wargames** | [github.com/bamr87/wargames](https://github.com/bamr87/wargames) | The OverTheWire-style security wargame walkthroughs, extracted into their own repo |
| **Zer0-Mistakes Theme** | [github.com/bamr87/zer0-mistakes](https://github.com/bamr87/zer0-mistakes) | The Jekyll remote theme that powers this site |

## Changelog

Notable changes are recorded in [CHANGELOG.md](CHANGELOG.md). Tagged versions are on the [releases page](https://github.com/bamr87/it-journey/releases).

## License

Released under the [MIT License](LICENSE).

---

<!-- bamr87-portfolio-footer -->
Part of the [bamr87 portfolio](https://github.com/bamr87) — browse every project on [Amr's GitHub profile](https://github.com/bamr87).
