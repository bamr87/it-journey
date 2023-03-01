---
title: Github Setup
author: null
layout: default
description: null
categories:
    - github
slug: github
lastmod: '2022-01-25T04:36:34.355Z'
draft: false
---

## Base setup

- [Github CLI](https://cli.github.com/)

### Prerequisites

- Master Setup
- VSCode

Confirm that you have a package manager installed by running the following command:

**Mac OS**

```shell
brew -v
```

**Windows**

```powershell
winget -v
```

### Install Github CLI

The Github CLI is a command line interface for the Github API. It is used to create and manage repositories. It is also used to create and manage issues and pull requests.

**MacOS**

```shell
brew install gh
```

**Windows**

```powershell
winget install git.git
winget install GitHub.cli
```

Confirm that you have installed the Github Command Line Interface by running the following command:

```shell
gh --version
```

### Login to gh cli

Before you can begin using the CLI, you need to first log in to your account by running the following command:

```shell
gh auth login
```

In order for Github to recognize your user ID when committing to your repository, you need to add a no-reply email id to git.

Replace `<username>` with your github user id.

```shell
git config --global user.email "<username>@users.noreply.github.com"
```

## Fork Github Repository

Now you can fork the repository from Github and start working on it.

The following command will create a new directory in your home folder (enter `echo $HOME` in the terminal to find it) and then clone the repository into that new directory. The last command `gh repo fork bamr87/it-journey` is all you really need to get started.

```bash
# Navigate to your home directory, create a github folder, and fork the github repo
cd ~
mkdir github
cd github
gh repo fork bamr87/it-journey
```

### Add [Submodules](http://git-scm.com/book/en/v2/Git-Tools-Submodules) 

```shell
git submodule add https://github.com/bamr87/winget-packages.git winget

# if the submodule is empty, run the following command to initialize it

git submodule update --init

```
### Github Pages

