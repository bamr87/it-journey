---
title: 'IT-Journey Blog Posts: Tutorials and Learning Articles'
author: Amr
description: Educational blog posts covering web development, DevOps, system administration, AI & ML, and emerging tech — documenting the IT journey from zero to hero.
excerpt: A complete, always-current index of posts documenting this journey, organized by category
date: '2025-12-17T19:56:57.000Z'
lastmod: '2026-06-13T00:00:00.000Z'
version: 3.0.0
draft: false
sidebar:
  nav: searchCats
categories:
- posts
- index
tags:
- journey
- guides
- articles
- documentation
- ai-development
- web-development
- devops
- system-administration
section: Home
permalink: /posts/
keywords:
- blog posts
- tutorials
- devops
- web development
- it journey
---
# IT-Journey Blog Posts

Practical tutorials, deep-dive technical articles, AI-assisted development chronicles, and professional insights — documenting the journey from zero to hero. This index is generated automatically from the post collection, so it always reflects what's actually published.

> 💡 Prefer a richer, visual layout? Browse the same content in the [**News magazine view**](/news/), or jump straight to [**Tags**](/tags/) and [**Archives**](/archives/).

{% assign all_posts = site.posts | where_exp: "post", "post.index != true" %}

## 📚 Browse by Category

| Category | Focus | Posts |
|----------|-------|------:|
{% for nav_item in site.data.navigation.posts -%}
{% assign section_slug = nav_item.url | remove: '/news/' | remove: '/' -%}
{% assign section_posts = all_posts | where_exp: "post", "post.path contains section_slug" -%}
{% if section_posts.size == 0 %}{% assign section_posts = all_posts | where_exp: "post", "post.categories contains nav_item.title" %}{% endif -%}
{% if section_posts.size > 0 %}| [{{ nav_item.title }}](#cat-{{ section_slug }}) | {{ nav_item.description }} | {{ section_posts.size }} |
{% endif -%}
{% endfor %}

_Total published posts: **{{ all_posts.size }}**_

---

{% for nav_item in site.data.navigation.posts -%}
{% assign section_slug = nav_item.url | remove: '/news/' | remove: '/' -%}
{% assign section_posts = all_posts | where_exp: "post", "post.path contains section_slug" -%}
{% if section_posts.size == 0 %}{% assign section_posts = all_posts | where_exp: "post", "post.categories contains nav_item.title" %}{% endif -%}
{% if section_posts.size > 0 %}
## {{ nav_item.title }}
{: #cat-{{ section_slug }} }

{% if nav_item.icon %}<i class="bi {{ nav_item.icon }}"></i> {% endif %}{{ nav_item.description }}

{% assign sorted_posts = section_posts | sort: "date" | reverse -%}
{% for post in sorted_posts -%}
- [{{ post.title | escape }}]({{ post.url | relative_url }}) · <span class="text-muted">{{ post.date | date: "%b %-d, %Y" }}</span>
{% endfor %}
{% endif -%}
{% endfor %}
---

## 🕒 Latest Posts

{% for post in all_posts limit: 12 -%}
- [{{ post.title | escape }}]({{ post.url | relative_url }}) · <span class="text-muted">{{ post.date | date: "%b %-d, %Y" }}</span>
{% endfor %}

---

## Other IT-Journey Collections

| Collection | What It Is |
|------------|------------|
| [📘 Quick Start Guide](/quickstart/) | Step-by-step setup — machine config, Jekyll, GitHub, VS Code, deployment, CI/CD |
| [🏰 Quest Map](/quests/home/) | Gamified quests across binary levels — from terminal basics to system architecture |
| [📚 Docs Library](/docs/) | Reference documentation — terminal shortcuts, Bash, Jekyll config, Liquid, Mermaid, MathJax |
| [📝 Notes](/notes/) | Working notes, code snippets, and quick references collected during development |
| [📰 News Magazine](/news/) | The same posts in a visual, category-driven magazine layout |

---

## 🤝 Contributing a Post

1. **Review guidelines**: see the [post creation instructions](https://github.com/bamr87/it-journey/blob/main/.github/instructions/posts.instructions.md)
2. **Choose topics**: focus on practical, educational content with clear value
3. **Follow templates**: use the established frontmatter and content structure
4. **Share knowledge**: ensure content helps others learn and solve real problems

Have a topic to suggest or a problem to report? Open a [GitHub Issue](https://github.com/bamr87/it-journey/issues) or start a [discussion](https://github.com/bamr87/it-journey/discussions).

---

*This index updates automatically as posts are added to the journey. Each post represents a step in the ongoing quest to master modern information technology.*
