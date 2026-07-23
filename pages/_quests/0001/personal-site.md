---
title: 'Build a Personal Website with GitHub Pages'
author: IT-Journey Team
description: 'Discover the services and tools behind a personal website built on GitHub Pages, from Jekyll hosting and CDN to analytics, search, and comments.'
preview: images/previews/personal-site.png
date: '2023-12-03T01:47:51.000Z'
lastmod: '2025-11-30T05:46:59.000Z'
level: '0001'
difficulty: 🟢 Easy
estimated_time: 45-60 minutes
primary_technology: Personal Site
quest_type: side_quest
quest_series: Level 0001 Quest Line
skill_focus: devops
learning_style: hands-on
permalink: /quests/0001/personal-site/
categories:
- Quests
- GitHub-Pages
tags:
- Personal Site
- '0001'
- github-pages
keywords:
  primary:
  - Personal Site
  secondary:
  - '0001'
  - github-pages
fmContentType: quest
key: tutorial
index: 8199
subcategory: jekyll
quest_line: Site Building Series
quest_arc: Personal portfolio arc
prerequisites:
  knowledge_requirements: []
  system_requirements: []
quest_dependencies:
  required_quests: []
  recommended_quests: []
  unlocks_quests: []
rewards:
  badges: []
  progression_points: 0
  skills_unlocked: []
validation_criteria:
  completion_requirements: []
  skill_demonstrations: []
layout: quest
redirect_from:
- /quests/0001/side-quests/personal-site/
draft: false
---
## 🎯 Quest Objectives

By the end of this quest, you will be able to:

- [ ] Understand the core concepts introduced in this quest
- [ ] Complete the hands-on exercises and verify the results
- [ ] Apply what you learned to a follow-up scenario of your own design

> *Note: objectives auto-seeded during framework alignment — authors should refine these to reflect this quest's specific skills.*

> Services/tools used for building personal site.

## 1. Personal Site

My personal website can be accessed through following domains. These sites are all using the same source files.

* [{% raw %}{{ site.github_base_url }}{% endraw %}](https://{% raw %}{{ site.github_base_url }}{% endraw %})

 No. | URL                                                | Description
-----|----------------------------------------------------|----------------------------------------
 1   | https://github.com/{% raw %}{{ site.github_user }}{% endraw %}/{% raw %}{{ site.github_user }}{% endraw %}.github.io | Source code repository
 2   | https://{% raw %}{{ site.github_user }}{% endraw %}.github.io/                      | `Domain 1`, hosted by GitHub Pages
 3   | <https://travis-ci.org/>                             | CI/CD for {% raw %}{{ site.github_user }}{% endraw %}.github.io
 4   | https://{% raw %}{{ site.github_user }}{% endraw %}.netlify.app/                    | `Domain 2`, hosted by Netlify
 5   | <https://www.netlify.com/>                           | CI/CD for {% raw %}{{ site.github_user }}{% endraw %}.netlify.app
 6   | https://{% raw %}{{ site.github_user }}{% endraw %}.github.io/                             | `Domain 3`, hosted by Cloudflare
 7   | <https://www.cloudflare.com/>                        | CDN for {% raw %}{{ site.github_user }}{% endraw %}.github.io
 8   | <https://www.godaddy.com/>                           | Domain service for {% raw %}{{ site.github_user }}{% endraw %}.github.io
 9   | <https://sharethis.com/>                             | Share buttons
 10  | <https://disqus.com/>                                | Comments service
 11  | <https://analytics.google.com>                       | Track website traffic
 12  | <https://jekyllrb.com/>                              | Static site generator
 13  | <https://highlightjs.org/>                           | Syntax highlighting
 14  | <https://www.mathjax.org/>                           | JS engine for mathematics
 15  | <https://mermaidjs.github.io/>                       | Charts generated from text via JavaScript
 16  | <https://lunrjs.com/>                                | Lightweight full-text offline search
 17  | <http://nanobar.jacoborus.codes/>                    | Lightweight progress bars
 18  | <https://www.google.com/adsense/>                    | Google Ads

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 001 - Journeyman Challenges]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]

