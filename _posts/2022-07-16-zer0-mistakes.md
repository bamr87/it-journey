---
title: zer0-mistakes
author: null
excerpt: null
description: null
snippet: null
categories:
  - posts
tags:
  - article
meta: null
draft: true
lastmod: 2022-07-22T21:56:21.083Z
---

{{ page.title }}

## Prerequsites

Github Account

[Signup](https://github.com/signup) or [Sign-in](https://github.com/login)

### Machine Setup

Install package manager:

- [Winget](https://docs.microsoft.com/en-us/windows/package-manager/winget/)

- [Homebrew](https://brew.sh)

Install Git
- Homebrew [git](https://formulae.brew.sh/formula/git#default)  
- Winget [git](https://winget.run/pkg/Git/Git) 

Install [Github cli](https://github.com/cli/cli#installation)

## Set your variables

```shell
export GITDIR=github
export GITREPO=zer0-mistakes-3
echo $GITDIR $GITREPO
```

## Initialize your new github repository

[gh cli docs](https://cli.github.com/manual/)

```shell
cd ~
mkdir $GITDIR
cd ~/$GITDIR
mkdir $GITREPO
git init
gh repo create $GITREPO --public --source=. --remote=upstream
```

```shell
echo "# $GITREPO" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/bamr87/$GITREPO.git
git push -u origin main
```

## Initialize Jekyll

Install [jekyll](https://jekyllrb.com/docs/installation/)

```shell
cd ~/$GITDIR/$GITREPO
jekyll new ./ --force
```

```shell
bundle add webrick
bundle install
```

```shell
jekyll serve
```
