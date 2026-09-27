---
title: Digs
description: "Published Git archaeology: one bounded reading of a bamr87 repository's history, with the commits kept separate from the inference."
date: 2026-09-26T21:21:40.000Z
lastmod: 2026-09-26T21:21:40.000Z
author: bamr87
categories:
  - digs
tags:
  - git
  - archaeology
permalink: /digs/
excerpt: "A shelf for the repository's own history, one bounded dig at a time."
render_with_liquid: true
draft: false
---

A dig is a published reading of Git history. Each installment names one bamr87 repository and one commit range on or after 2020-01-01. The commits are the evidence. The prose may interpret them, but it has to say when it is inferring.

{% assign items = site.digs | where_exp: 'item', 'item.repository' | where_exp: 'item', 'item.draft != true' | sort: 'range_start' %}
{% if items.size > 0 %}
<ul>
{% for item in items %}
  <li><a href="{{ item.url | relative_url }}">{{ item.title | escape }}</a> — <code>{{ item.repository | escape }}</code>, {{ item.range_start | escape }} to {{ item.range_end | escape }}</li>
{% endfor %}
</ul>
{% else %}
No published digs yet.
{% endif %}
