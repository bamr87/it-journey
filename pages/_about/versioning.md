---
title: "IT-Journey Versioning: Semver and Release Strategy"
author: bamr87
excerpt: How IT-Journey numbers its releases — semantic versioning driven by Conventional Commits, a changelog that release-please writes, and a theme versioned on its own.
description: How IT-Journey numbers its releases — semantic versioning from Conventional Commits, a changelog release-please writes, and a theme versioned on its own.
snippet: null
categories:
- about
tags:
- versioning
- semver
- changelog
- release-please
meta: null
keywords:
  - semantic versioning
  - semver
  - changelog
  - release-please
  - conventional commits
  - release strategy
permalink: /about/versioning/
redirect_from:
  - /about/posts/versioning/
draft: false
lastmod: '2026-11-15T00:00:00.000Z'
date: '2022-01-10T17:00:49.000Z'
---

## Why version a learning site

IT-Journey ships no binaries, but the site still changes in ways worth tracking: new quests and levels, layout and navigation changes, frontmatter schema migrations, moved permalinks, and tooling upgrades. A version number and a changelog answer "what changed between these two releases?" without digging through the commit history.

## How a release happens

1. Every change reaches `main` through a pull request whose commit messages follow [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:` and so on.
2. On each push to `main`, the `release.yml` workflow runs [release-please](https://github.com/googleapis/release-please). It reads the new commits and keeps one release pull request open with the next version number and the changelog entry it will add.
3. Merging that release pull request puts the new version and its changelog entry on `main`. release-please then tags the release (`vMAJOR.MINOR.PATCH`) and publishes it on the [releases page](https://github.com/bamr87/it-journey/releases).

No one picks a version number or pushes a tag by hand. The live site is published from `main` once its checks pass, on its own schedule, so a release records what changed; it does not deploy anything.

## Which number moves

Releases follow [semantic versioning](https://semver.org/), `MAJOR.MINOR.PATCH`, and the commit types decide which number moves:

| Segment | Moved by | For example |
|---|---|---|
| `MAJOR` | A breaking change: `!` after the type (`feat!:`) or a `BREAKING CHANGE:` footer | A new permalink scheme that breaks old links |
| `MINOR` | `feat:` | A new quest level or a new kind of page |
| `PATCH` | `fix:`, `docs:`, `perf:`, `refactor:`, `deps:` and `revert:` | A broken link fixed, a guide corrected |

While the major version is 0, a breaking change moves `MINOR` instead of `MAJOR`. Commits typed `chore:`, `ci:`, `test:`, `style:` or `build:` stay out of the changelog, so on their own they never cause a release. The [release-please configuration](https://github.com/bamr87/it-journey/blob/main/release-please-config.json) is the source of truth for these rules.

## The changelog

[CHANGELOG.md](https://github.com/bamr87/it-journey/blob/main/CHANGELOG.md) follows [Keep a Changelog](https://keepachangelog.com/) and is generated: release-please writes each entry from the commit messages, under Added, Fixed, Changed, Removed and Documentation. Never edit it, or a version number, by hand. The entries are the commit messages, so write each one for the person who will read the changelog.

## The theme versions on its own

The site has two parts, and each releases on its own schedule:

- **IT-Journey**: the quests, notes, digs, about pages, data and tooling in [this repository](https://github.com/bamr87/it-journey). Its releases are the ones described above.
- **zer0-mistakes**: the Jekyll theme that supplies the layouts, styles and includes. It is versioned and released in [its own repository](https://github.com/bamr87/zer0-mistakes/releases).

The site loads the theme as an unpinned `remote_theme`, so every build uses the theme's latest `main`, and a theme change reaches the site at its next build without an IT-Journey release. The theme files this site deliberately overrides are listed in [`.theme-overrides.yml`](https://github.com/bamr87/it-journey/blob/main/.theme-overrides.yml); theme bugs are fixed upstream.

## Related

- [CHANGELOG.md](https://github.com/bamr87/it-journey/blob/main/CHANGELOG.md): every release and what it changed
- [Releases](https://github.com/bamr87/it-journey/releases): the tagged releases on GitHub
- [Conventional Commits](https://www.conventionalcommits.org/) and [semver.org](https://semver.org/): the two specifications behind the numbers
- [Keep a Changelog](https://keepachangelog.com/): the changelog format
- [About: Contributing](/about/contributing/): how to get a change into the next release
