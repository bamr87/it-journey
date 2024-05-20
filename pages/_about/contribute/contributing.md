---
title: contributing
author: Amr
username: $GITHUB_USERNAME
excerpt: null
description: null
snippet: null
categories:
  - about
tags:
  - contributing
meta: null
draft: true
lastmod: 2024-05-20T17:42:21.099Z
permalink: /about/contributing
---


https://opensource.guide/

TODO: Right contribution instructions.

Here's a list of contributors:

- [Amr](/contributors/bamr87/)

Start with Contribution framework

- Collaboration Too: [Github]
- Source Code Repo: [Github]
- DevOps Model: 
- Tech Stack Design
- Build instructions
- Automated testing harness
-  


## Add your github profile as a subtree

```shell

cd ~/github/it-journey

# Add the GitHub profile repository as a remote repository

git remote add {{ page.username | default: '$GITHUB_USERNAME' }} https://github.com/{{ page.username | default: '$GITHUB_USERNAME' }}/{{ page.username | default: '$GITHUB_USERNAME' }}.git

# Add the remote repository as a subtree

git subtree add --prefix=pages/_about/contributors/{{ page.username | default: '$GITHUB_USERNAME' }} {{ page.username | default: '$GITHUB_USERNAME' }} main

```