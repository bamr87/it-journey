---
title: Github Setup
author: null
layout: default
description: null
categories:
    - quickstart
    - github
slug: github
lastmod: '2022-01-11T01:03:40.511Z'
draft: false
---

## Base setup

- [Github CLI](https://cli.github.com/)

### Prerequisites

- Homebrew
- VSCode

confirm that you have installed Homebrew by running the following command:

```shell
# Confirm Homebrew installation
brew -v
```

### Install Github Command Line Interface

The Github CLI is a command line interface for the Github API. It is used to create and manage repositories. It is also used to create and manage issues and pull requests.

MacOS

```shell
# Install Github CLI
brew install gh
```

Windows

```powershell
# Install Github CLI
winget install git.git
winget install GitHub.cli
```

Confirm that you have installed the Github Command Line Interface by running the following command:

```shell
# Confirm Github CLI installation
gh --version
```

Login to gh cli using your github credentials

```bash
# Login to gh cli
gh auth login
```

In order for Github to recognize your user ID when commiting to your repository, you need to add a no-reply email id to git.

Replace `<username>` with your github user id.

```shell
git config --global user.email "<username>@users.noreply.github.com"
```

## Fork Github Repository

Now you can fork the repository from Github and start working on it.

```bash
# Navigate to your home directory, create a github folder, and fork the github repo
cd ~
mkdir github
cd github
gh repo fork bamr87/it-journey
```
