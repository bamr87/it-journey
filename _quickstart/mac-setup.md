---
title: mac
author: null
layout: default
description: null
categories:
    - quickstart
slug: mac
lastmod: '2021-12-09T16:59:33.004Z'
draft: false
---

Here's how to setup a mac

## Install Xcode Command Line Tools

```bash
xcode-select --install
```

Confirm that you have installed Xcode Command Line Tools by running the following command:

```bash
xcode-select -p
```

## Install Homebrew

Homebrew is a package manager for macOS. It is a fork of the original Homebrew package manager for Linux, and is developed and maintained by [Homebrew](https://brew.sh/).

[Install docs](https://docs.brew.sh/Installation)

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

confirm that you have installed Homebrew by running the following command:

```bash
brew -v
```

## Install Github Command Line Interface

```bash
brew install gh
```

Login to Github and confirm that you have installed the Github Command Line Interface by running the following command:

```bash
gh -v
```

## Install Software Packages

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


## 
