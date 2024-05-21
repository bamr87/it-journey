---
title: Docs (~) Index
author: Amr Abdel Eissa
layout: collection
permalink: /docs/
description: Index of all doc pages and instructions on how to add new doc sections
catagories:
    - docs
    - home
sidebar:
    nav: docs
toc_sticky: true
date: 2021-09-24T19:32:44.876Z
lastmod: 2024-05-21T18:27:46.013Z
draft: true
---

You have reached the documentation (library) section of this site, which will contain detailed information of various components of this site (e.g., jekyll, bootstrap, etc.). The ultimate goal is to house a documentation site that operates very similar to Microsoft's doc site [here](https://learn.microsoft.com/en-us/docs/).

These docs are sourced using the git module function, cleaned up with some scripts, and then generated using jekyll. In the future, these docs will have multiple engines to created (i.e., using Hugo to create the docs site).

Current, we have docs for the following applications:

- Ruby
- Jekyll
- Liquid
- Bootstrap
- 

To add to this collection, you need to run the following commands on your local development environment:

## Jekyll
[official docs](https://jekyllrb.com/docs/)

```sh
git submodule add https://github.com/jekyll/jekyll.git jekyll-docs
```

```sh
cd jekyll-docs/docs/_docs
git sparse-checkout init --cone
git sparse-checkout set jekyll-docs/docs/_docs
git sparse-checkout set docs/_docs
```
