---
title: mac
author: null
layout: default
description: null
categories:
    - quickstart
slug: mac
lastmod: '2021-12-08T17:37:37.462Z'
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

[Install docs](https://docs.brew.sh/Installation)

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

confirm that you have installed Homebrew by running the following command:

```bash
brew -v
```

## Install git

```bash
brew install gh
```

## Install Software Packages

```bash
cd ~
git clone git@github.com:bamr87/brewfile.git ~/.brew
```


```bash
brew cask install atom \
 firefox \
 onedrive \
 iterm2 \
 google-cloud-sdk \
 inkscape \
 sonic-pi \
 postman \
 awscli \
 visual-studio-code
brew $parm1 wget \
 bash-completion \
 zsh \
 node \
 rdesktop \
 irssi \
 gh \
 tree \
 nmap \
 powershell \
```


## 
