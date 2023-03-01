---
title: Homebrew
categories: notes
sidebar:
    nav: quickstart
lastmod: '2022-05-22T20:55:23.521Z'
---
![brew](\brew.png)

# Brewfile

## Installation

Git

```bash
cd ~
git clone git@github.com:bamr87/hombrew.git ~/.brew
```

```bash
gh repo clone bamr87/hombrew.git ~/.brew
```

# Install all packages in `Brewfile` (required taps and packages)

```bash

brew bundle

# Selective packages by categories

# Fonts

brew bundle --file bundles/fonts

# CLI

brew bundle --file bundles/cli
brew bundle --file bundles/cli.git
brew bundle --file bundles/cli.terminals
brew bundle --file bundles/cli.shells
brew bundle --file bundles/cli.search
brew bundle --file bundles/cli.editors
brew bundle --file bundles/cli.media
brew bundle --file bundles/cli.monitoring
brew bundle --file bundles/cli.network

# Development

brew bundle --file bundles/dev.languages
brew bundle --file bundles/dev.db
brew bundle --file bundles/dev.ides
brew bundle --file bundles/dev.devops
brew bundle --file bundles/dev.ios
brew bundle --file bundles/dev.android
brew bundle --file bundles/dev.api
brew bundle --file bundles/dev.forensic
brew bundle --file bundles/dev.virtualization

# Apps

brew bundle --file bundles/apps.macos
brew bundle --file bundles/apps.browsers
brew bundle --file bundles/apps.design
brew bundle --file bundles/apps.office
brew bundle --file bundles/apps.sns
brew bundle --file bundles/apps.git
brew bundle --file bundles/apps.media

# Games

brew bundle --file bundles/games

```

### Avoiding dependencies

In order to avoid to install some dependencies (`mas` needs to have a valid `Apple ID account` in order to install from the `Mac App Store`), you can use the following environment variables separated by space before the commands:

- HOMEBREW_BUNDLE_TAP_SKIP
- HOMEBREW_BUNDLE_BREW_SKIP
- HOMEBREW_BUNDLE_CASK_SKIP
- HOMEBREW_BUNDLE_MAS_SKIP
- HOMEBREW_BUNDLE_WHALEBREW_SKIP

```bash
HOMEBREW_BUNDLE_MAS_SKIP brew bundle --file apps
```

## Packages dependencies

```bash
# Requires graphviz (dot, fdp)
brew install graphviz

brew graph --installed | dot -T png -o graph.png
brew graph --installed --highlight-leaves | fdp -T png -o graph.png
open graph.png
```

### Upstream dependencies

```bash
brew deps --installed | grep ':.*FORMULA' | awk -F':' '{print $1}'
```
