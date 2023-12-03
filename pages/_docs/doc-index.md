---
title: Docs Index (~)
author: null
layout: collection
permalink: /docs/
description: null
catagories:
  - docs
  - home
sidebar:
  nav: docs
toc: true
toc_sticky: true
date: 2021-09-24T19:32:44.876Z
lastmod: 2023-12-03T01:21:22.098Z
draft: true
---
These are the docs

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

```html
<!-- docs_version_badge.html -->
<span class="version-badge" title="This feature is available starting version {{ include.version }}">{{ include.version }}</span>
```


```html
<!-- docs_variables_table -->

<div class="mobile-side-scroller">
<table>
  <thead>
    <tr>
      <th>Variable</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
  {% for var in include.scope -%}
    <tr>
      <td><p><code>{{ var.name }}</code></p></td>
      <td><p>{{- var.description -}}</p></td>
    </tr>
  {% endfor -%}
  </tbody>
</table>
</div>

```



## Bootstrap

## Ruby

## Github Pages


