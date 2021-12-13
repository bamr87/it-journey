---
title: mac
author: null
layout: default
description: null
categories:
    - quickstart
slug: mac
lastmod: '2021-12-13T17:10:18.194Z'
draft: false
---

Here's how to setup a mac

## Base setup

- Xcode Command Line Tools
- Homebrew Package Manager
- Github CLI
- Jekyll

### Install Xcode Command Line Tools

```bash
xcode-select --install
```

Confirm that you have installed Xcode Command Line Tools by running the following command:

```bash
xcode-select -p
```

### Install Homebrew

Homebrew is a package manager for macOS. It is a fork of the original Homebrew package manager for Linux, and is developed and maintained by [Homebrew](https://brew.sh/).

[Install docs](https://docs.brew.sh/Installation)

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

confirm that you have installed Homebrew by running the following command:

```bash
brew -v
```

### Install Github Command Line Interface

```bash
brew install gh
```

Login to Github and confirm that you have installed the Github Command Line Interface by running the following command:

```bash
gh -v
```

Login to gh cli using your github credentials

```bash
gh auth login
```

### Install Software Packages (optional)

Detailed instructions for installing software packages can be found in the [Brewfile](/quickstart/homebrew/) section.

```bash
cd ~
gh repo clone bamr87/brewfile ~/.brew
```


```bash

cd ~/.brew

brew bundle

brew bundle --file bundles/core/

```

### Install VS Code

```bash
brew cask install visual-studio-code
```

Log into VS code using your github account

## Jekyll & ruby Setup

[Detailed instructions](https://jekyllrb.com/docs/installation/macos/)

### set SDKROOT (only macOS Catalina or later)

```bash
export SDKROOT=$(xcrun --show-sdk-path)
```

### Install Ruby

```bash
brew install ruby
```

#### If you're using Zsh

```bash
echo 'export PATH="/usr/local/opt/ruby/bin:/usr/local/lib/ruby/gems/3.0.0/bin:$PATH"' >> ~/.zshrc
```

#### If you're using Bash

```bash
echo 'export PATH="/usr/local/opt/ruby/bin:/usr/local/lib/ruby/gems/3.0.0/bin:$PATH"' >> ~/.bash_profile
```

#### Unsure which shell you are using? Type

```bash
echo $SHELL
```

### Install Jekyll

```bash
gem install --user-install bundler jekyll
```

### Append your path file

#### If you're using Zsh

echo 'export PATH="$HOME/.gem/ruby/X.X.0/bin:$PATH"' >> ~/.zshrc

#### If you're using Bash

echo 'export PATH="$HOME/.gem/ruby/X.X.0/bin:$PATH"' >> ~/.bash_profile

