---
title: "search"
author: null
description: null
categories:
  - search
slug: search
lastmod: 2023-03-11T01:12:55.441Z
draft: false
permalink: /search/
---

```html
<!-- Search Bar -->
<div id="search-searchbar"></div>

  <div class="post-list" id="search-hits">
  {%- raw -%}
    {% for post in site.posts %}
      <div class="post-item">
        {% assign date_format = site.minima.date_format | default: "%b %-d, %Y" %}
        <span class="post-meta">{{ post.date | date: date_format }}</span>

        <h2>
          <a class="post-link" href="{{ post.url | relative_url }}">
            {{ post.title | escape }}
          </a>
        </h2>

        <div class="post-snippet">{{ post.excerpt }}</div>
      </div>
    {% endfor %}
{% endraw %}
```
