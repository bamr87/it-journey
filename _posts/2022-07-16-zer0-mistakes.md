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
lastmod: 2022-07-24T05:05:34.218Z
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

## Building the theme

### Override default


https://jekyllrb.com/docs/themes/#overriding-theme-defaults

### Comment out the theme from config and Gemfile

```shell
#_config.yml
# Build settings
# theme: minima
plugins:
  - jekyll-feed
```

```shell
bundle remove minima --install
```

Restart jekyll
```shell
jekyll serve
```

## Build default page


```shell
{%- raw -%}
cd ~/$GITDIR/$GITREPO
mkdir _layout
cd _layout
echo "{{ content }}" >> default.html 
{% endraw %}
``` 

```shell
# find theme path
bundle info --path minima
JEKYLL_THEME=$(bundle info --path minima)
echo $JEKYLL_THEME
cd $JEKYLL_THEME
alias tree="find . -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'"
echo alias tree="find . -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'" >> ~/.zshrc

tree
cd -
```

### Copy theme repo

```shell
cp -R $JEKYLL_THEME ~/$GITDIR/$GITREPO
```

