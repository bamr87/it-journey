---
title: 'Liquid Templating: Dynamic Content for Jekyll Sites'
author: IT-Journey Team
description: 'Master Liquid, the templating language behind Jekyll: variables, filters, loops, conditionals, includes, and layouts that render dynamic pages at build time.'
excerpt: Create dynamic content in Jekyll with Liquid - master variables, filters, and control flow.
preview: images/previews/liquid-templating-dynamic-content-jekyll-quest-de.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0001'
difficulty: 🟡 Medium
estimated_time: 75-90 minutes
primary_technology: liquid
quest_type: main_quest
quest_series: Static Site Mastery
quest_line: The Web Fundamentals Codex
quest_arc: Forging Your First Website
quest_dependencies:
  required_quests:
  - /quests/0001/jekyll-fundamentals/
  recommended_quests:
  - /quests/0001/yaml-configuration/
  unlocks_quests:
  - /quests/0001/github-pages-basics/
skill_focus: frontend
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Basic HTML
  - Completion of Jekyll Fundamentals
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - A working Jekyll site to experiment in
  skill_level_indicators:
  - Comfortable editing layouts and includes
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A page that loops over data and renders conditionally
  skill_demonstrations:
  - Can chain filters to transform a value
  - Can write a loop with a conditional inside it
  knowledge_checks:
  - Understands the difference between output and tag delimiters
  - Can include a partial and pass it parameters
permalink: /quests/0001/liquid-templating/
categories:
- Quests
- Frontend
- Static-Sites
- Beginner
tags:
- '0001'
- liquid
- jekyll
- templating
- web-development
- main_quest
- frontend
- hands-on
- beginner
keywords:
  primary:
  - '0001'
  - liquid
  - jekyll
  - templating
  secondary:
  - web-development
  - main_quest
  - frontend
  - hands-on
  - beginner
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0001 (1) Quest: Main Quest - Liquid'
rewards:
  badges:
  - 🏆 Loremaster of Liquid - Mastered variables, filters, and control flow
  - 🌱 Weaver of Templates - Composed pages from includes and layouts
  skills_unlocked:
  - 🛠️ Liquid Template Authoring
  - 🧠 Build-Time Templating Concepts
  progression_points: 50
  unlocks_features:
  - The ability to build data-driven pages in any later quest
layout: quest
---
*Greetings, brave adventurer! You can now scaffold and serve a Jekyll site - but every page is still hand-written and static. **Liquid Templating** teaches you the spoken magic of Jekyll: a templating language that lets one template render a hundred pages, pull in data, loop over lists, and decide what to show. This is where your site stops being a stack of files and starts being a living thing.*

*Liquid runs at build time, not in the browser, so all this power costs your visitors nothing. Learn it well, for every layout, include, and theme you ever touch in Jekyll speaks Liquid.*

## 📖 The Legend Behind This Quest

*Long ago, the merchants of Shopify needed a safe way to let shopkeepers customize their storefront pages without handing them the keys to the whole engine. So they forged **Liquid** - a templating language powerful enough to loop, filter, and decide, yet sandboxed so a careless incantation could never break the server. Jekyll adopted Liquid, and today it is the lingua franca of static templating.*

*With Liquid you write a page once and let the data fill it in - a blog index that lists every post, a navigation menu built from a data file, a card that changes colour based on a value. Master it, and you wield the heart of every Jekyll theme.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Objects & Variables** - Output values with the double-brace syntax
- [ ] **Filters** - Transform values by chaining filters with the pipe
- [ ] **Tags: Loops & Conditionals** - Use `for`, `if`, and `assign` to control logic
- [ ] **Includes & Layouts** - Compose pages from reusable partials and skeletons

### Secondary Objectives (Bonus Achievements)
- [ ] **Passing Parameters to Includes** - Make partials reusable with arguments
- [ ] **Whitespace Control** - Use `{% raw %}{%- -%}{% endraw %}` to keep generated HTML clean
- [ ] **Looping Over Site Data** - Read `_data` files in a template

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain the difference between output `{% raw %}{{ }}{% endraw %}` and tag `{% raw %}{% %}{% endraw %}` delimiters
- [ ] Chain three filters to format a value end to end
- [ ] Build a list page that loops over a collection with a conditional badge

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Basic HTML (tags, attributes)
- [ ] Completion of [Jekyll Fundamentals](/quests/0001/jekyll-fundamentals/)
- [ ] Recommended: [YAML Configuration](/quests/0001/yaml-configuration/) for data files

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] A working Jekyll site to experiment in
- [ ] A text editor or IDE (VS Code recommended)

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You can build and serve a Jekyll site already
- [ ] You are comfortable editing files in `_layouts` and `_includes`
- [ ] Ready for 75-90 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*Liquid lives inside your Jekyll site, so the only setup is a running site. Use `--livereload` so each edit shows instantly.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Serve your site with live reload so Liquid edits appear instantly
cd my-castle
bundle exec jekyll serve --livereload
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Serve with live reload
cd my-castle
bundle exec jekyll serve --livereload
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Serve with live reload
cd my-castle
bundle exec jekyll serve --livereload
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# In a container, bind the host so live reload reaches your browser
docker run --rm -it -p 4000:4000 -p 35729:35729 -v "$PWD":/srv/jekyll \
  jekyll/jekyll:4 jekyll serve --livereload --host 0.0.0.0
```

</details>

## 🧙‍♂️ Chapter 1: Objects, Tags, and Filters - The Three Words of Power

*Liquid has exactly three kinds of markup. Learn the three, and you can read any template.*

### ⚔️ Skills You'll Forge in This Chapter
- The output delimiter `{% raw %}{{ }}{% endraw %}` for printing values
- The tag delimiter `{% raw %}{% %}{% endraw %}` for logic
- Filters for transforming values

### 🏗️ The Three Delimiters

```liquid

{% raw %}{{ page.title }}{% endraw %}              <!-- OBJECT: prints a value into the page -->
{% raw %}{% assign greeting = "hi" %}{% endraw %}  <!-- TAG: runs logic, prints nothing -->
{% raw %}{{ greeting | upcase }}{% endraw %}       <!-- FILTER: transforms a value -> "HI" -->

```

- **Objects** `{% raw %}{{ ... }}{% endraw %}` output content - a variable, a string, a number.
- **Tags** `{% raw %}{% ... %}{% endraw %}` perform logic - assignments, loops, conditionals. They produce no visible output themselves.
- **Filters** appear inside objects after a pipe `|` and transform the value flowing through.

**Chaining filters** is where Liquid shines. Each filter feeds the next:

```liquid

{% raw %}{{ "the static web" | capitalize | replace: "web", "kingdom" }}{% endraw %}
<!-- Output: The static kingdom -->

{% raw %}{{ page.date | date: "%B %-d, %Y" }}{% endraw %}
<!-- Output: June 14, 2026 -->

{% raw %}{{ post.content | strip_html | truncatewords: 20 }}{% endraw %}
<!-- A 20-word plain-text preview of a post -->

```

Jekyll exposes useful global objects too: `site` (everything in `_config.yml` and `_data`), `page` (the current page's front matter), `content`, and inside loops, `post` / `item`.

### 🔍 Knowledge Check: The Three Words
- [ ] Which delimiter prints a value, and which runs logic?
- [ ] What does the pipe `|` do?
- [ ] What does `{% raw %}{{ site.title }}{% endraw %}` read from?

### ⚡ Quick Wins and Checkpoints
- [ ] **Printed a value**: You output `{% raw %}{{ page.title }}{% endraw %}` on a page
- [ ] **Chained a filter**: You transformed a string with at least two filters

## 🧙‍♂️ Chapter 2: Loops and Conditionals - Logic in the Template

*A blog index is just a `for` loop over posts. A "featured" badge is just an `if`. This chapter gives your templates a brain.*

### ⚔️ Skills You'll Forge in This Chapter
- Iterating with `for`
- Branching with `if` / `elsif` / `else`
- Filtering and limiting loops

### 🏗️ Looping and Branching

A list of the five most recent posts, each with an optional "New" badge:

```liquid

<ul class="post-list">
{% raw %}{% for post in site.posts limit:5 %}{% endraw %}
  <li>
    <a href="{% raw %}{{ post.url | relative_url }}{% endraw %}">{% raw %}{{ post.title }}{% endraw %}</a>
    {% raw %}{% if post.featured %}{% endraw %}
      <span class="badge">⭐ Featured</span>
    {% raw %}{% elsif post.date > site.time | date: "%s" | minus: 604800 %}{% endraw %}
      <span class="badge">New</span>
    {% raw %}{% endif %}{% endraw %}
  </li>
{% raw %}{% endfor %}{% endraw %}
</ul>

```

Useful loop helpers:

```liquid

{% raw %}{% for item in site.data.navigation %}{% endraw %}
  {% raw %}{{ forloop.index }}{% endraw %}. {% raw %}{{ item.name }}{% endraw %}   <!-- forloop.index is 1-based -->
{% raw %}{% endfor %}{% endraw %}

{% raw %}{% assign sorted = site.posts | sort: "title" %}{% endraw %}
{% raw %}{% for p in sorted reversed %}{% endraw %}
  {% raw %}{{ p.title }}{% endraw %}
{% raw %}{% endfor %}{% endraw %}

```

`if` understands `and`, `or`, `==`, `!=`, `>`, `<`, `contains`. Use `unless` for the negative case and `case`/`when` for many branches.

### 🔍 Knowledge Check: Logic
- [ ] How do you limit a `for` loop to the first five items?
- [ ] What variable gives you the current iteration number?
- [ ] When would you use `unless` instead of `if`?

## 🧙‍♂️ Chapter 3: Includes & Layouts - Composing Pages

*Repetition is the enemy. Liquid lets you write a header once as an **include**, and a page skeleton once as a **layout**, then reuse them everywhere.*

### ⚔️ Skills You'll Forge in This Chapter
- Pulling in partials with `include`
- Passing parameters to includes
- Wrapping content in layouts

### 🏗️ Reuse with Includes and Layouts

Create `_includes/card.html` - a reusable component that accepts parameters:

```html
<div class="card">
  <h3>{% raw %}{{ include.title }}{% endraw %}</h3>
  <p>{% raw %}{{ include.body }}{% endraw %}</p>
</div>
```

Use it anywhere, passing arguments by name:

```liquid

{% raw %}{% include card.html title="Static Sites" body="Fast and secure by design." %}{% endraw %}
{% raw %}{% include card.html title="Liquid" body="Templating without a server." %}{% endraw %}

```

**Layouts** wrap a page's content in shared chrome. Create `_layouts/default.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>{% raw %}{{ page.title }}{% endraw %} | {% raw %}{{ site.title }}{% endraw %}</title>
  </head>
  <body>
    {% raw %}{% include header.html %}{% endraw %}
    <main>{% raw %}{{ content }}{% endraw %}</main>
    {% raw %}{% include footer.html %}{% endraw %}
  </body>
</html>
```

Any page declaring `layout: default` in its front matter gets wrapped automatically; the special `{% raw %}{{ content }}{% endraw %}` object is where the page's own body lands. Layouts can even nest by giving a layout its own `layout:` front matter.

### 🔍 Knowledge Check: Composition
- [ ] How do you pass a value into an include?
- [ ] What object renders the page body inside a layout?
- [ ] How would you make every page share one footer?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Filter Chain
**Objective**: Print a formatted, transformed value on a page.

**Requirements**:
- [ ] Output `{% raw %}{{ page.title }}{% endraw %}` somewhere visible
- [ ] Chain at least two filters on one value
- [ ] Format a date with the `date` filter

**Validation**: The rendered page shows the transformed text and a formatted date.

### 🟡 Intermediate Challenge: Data-Driven List
**Objective**: Build a navigation menu from a `_data` file.

**Requirements**:
- [ ] Create `_data/navigation.yml` with a list of links
- [ ] Loop over it with `for`
- [ ] Mark the current page with an `if` comparison

**Validation**: The menu renders every entry and highlights the active page.

### 🔴 Advanced Challenge: Parameterized Component
**Objective**: Create a reusable card include and a layout that uses it.

**Requirements**:
- [ ] Build `_includes/card.html` that accepts `title` and `body`
- [ ] Render at least three cards from a loop over data
- [ ] Wrap the page in a custom layout

**Validation**: Cards render from data and the page is wrapped by your layout.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Loremaster of Liquid** - Variables, filters, and control flow are yours
- 🌱 **Weaver of Templates** - You compose pages from includes and layouts

**🛠️ Skills Unlocked**:
- **Liquid Template Authoring** - Write dynamic pages that render at build time
- **Build-Time Templating Concepts** - Reason about data-driven generation

**🔓 Unlocked Quests**:
- GitHub Pages Basics - Publish your dynamic site for free
- YAML Configuration - Feed your templates with structured data

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [GitHub Pages Basics](/quests/0001/github-pages-basics/) - Take your templated site live

**Explore Side Adventures**:
- ⚔️ [YAML Configuration](/quests/0001/yaml-configuration/) - The data your templates loop over
- ⚔️ [Git Workflow Mastery](/quests/0001/git-workflow-mastery/) - Ship template changes cleanly

### Character Class Recommendations

**💻 Software Developer**: Continue to [GitHub Pages Basics](/quests/0001/github-pages-basics/)  
**🏗️ System Engineer**: Explore [YAML Configuration](/quests/0001/yaml-configuration/)  
**🎨 Frontend Specialist**: Deepen your theming with custom layouts

## 📚 Resources

### Official Documentation
- [Liquid Reference (Shopify)](https://shopify.github.io/liquid/) - The canonical language reference
- [Jekyll Liquid Documentation](https://jekyllrb.com/docs/liquid/) - Liquid as Jekyll uses it
- [Jekyll Includes](https://jekyllrb.com/docs/includes/) - Reusable partials with parameters

### Community Resources
- [Jekyll Talk Forum](https://talk.jekyllrb.com/) - Ask Liquid questions
- [Liquid on Stack Overflow](https://stackoverflow.com/questions/tagged/liquid) - Tagged Q&A
- [Jekyll Cheat Sheet](https://devhints.io/jekyll) - Quick Liquid and Jekyll syntax

### Learning Materials
- [Jekyll Step-by-Step: Includes](https://jekyllrb.com/docs/step-by-step/05-includes/) - Hands-on include tutorial
- [Jekyll Variables](https://jekyllrb.com/docs/variables/) - Every object Liquid can read

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Built a page that loops over data with a conditional
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0001 - Web Fundamentals]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Jekyll Fundamentals]]
**Unlocks:** [[GitHub Pages Basics]] · [[YAML Configuration]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
