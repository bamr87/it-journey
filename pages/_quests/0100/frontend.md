---
title: 'Frontend Forests: Building a Jekyll Site with Bootstrap'
author: GPT and bamr87
description: 'Venture into the Frontend Forests to build a Jekyll site, weave in Bootstrap for styling and scripts, then preview and deploy your enchanted creation.'
excerpt: Embark on a quest to build a Jekyll site using Bootstrap 5 for CSS and JavaScript in the Frontend Forests
preview: /images/frontend-forests.png
date: '2024-03-12T19:51:39.000Z'
lastmod: '2024-05-28T04:03:05.000Z'
level: '0100'
difficulty: 🟡 Medium
estimated_time: 90-120 minutes
primary_technology: General
quest_type: main_quest
quest_series: Level 0100 Quest Line
skill_focus: fullstack
learning_style: hands-on
permalink: /quests/0100/frontend/
redirect_from:
- /quickstart/theme-architecture/
categories: []
tags: []
keywords:
  primary:
  - frontend
  - forests
  - building
  secondary:
  - a
  - jekyll
  - site
fmContentType: quest
draft: true
slug: frontend-forests
type: default
layout: quest
---
## 🎯 Quest Objectives

By the end of this quest, you will be able to:

- [ ] Understand the core concepts introduced in this quest
- [ ] Complete the hands-on exercises and verify the results
- [ ] Apply what you learned to a follow-up scenario of your own design

> *Note: objectives auto-seeded during framework alignment — authors should refine these to reflect this quest's specific skills.*

Embarking on the quest to build a Jekyll site using Bootstrap for CSS and JavaScript in the Frontend Forests requires a clear map and a set of steps to guide you through the enchanted woods. Below is an outline designed to navigate you through this journey, ensuring you leverage the magical powers of Jekyll and Bootstrap to create an enchanting website.

### 🌲 The Frontend Forests Quest: Crafting a Jekyll Site with Bootstrap

#### Step 1: Preparing Your Journey's Tools

- **Install Ruby**: Ensure you have Ruby installed on your machine, as it's the lifeblood of Jekyll.
- **Install Jekyll and Bundler**: Run `gem install jekyll bundler` in your command line to install Jekyll and Bundler, the map and compass of your quest.

#### Step 2: Initiating the Jekyll Site Creation Spell

- **Create Your New Jekyll Site**: Use `jekyll new your-site-name` to create a new Jekyll site. This spell conjures a new site structure in your chosen directory.
- **Enter Your Site's Directory**: Navigate into your site’s directory using `cd your-site-name`.

#### Step 3: Integrating Bootstrap for Styling Magic

- **Add Bootstrap**: There are multiple ways to add Bootstrap. For simplicity, you can use the Bootstrap CDN. Open your `_includes/head.html` and add the Bootstrap CSS link within the `<head>` tag.
- **JavaScript Integration**: To add Bootstrap’s JavaScript, include the necessary Bootstrap JS link before the closing `</body>` tag in your `_layouts/default.html`.

#### Step 4: Customizing Your Site's Layout

- **Modify Default Layout**: Edit the `_layouts/default.html` file to create a basic layout structure. Use Bootstrap’s grid system and components to design your layout.
- **Creating Pages**: Start adding pages to your site. Jekyll uses Markdown for content creation, making it simple to add and manage content.

#### Step 5: Crafting Posts with Enchanted Words

- **Creating Posts**: Add posts in the `_posts` directory. Use the format `YYYY-MM-DD-name-of-post.md` for post files.
- **Using Front Matter**: Utilize Jekyll's front matter to add metadata to your posts and pages, enhancing their magical properties.

#### Step 6: Applying Styling Spells with Bootstrap

- **Styling Your Content**: Use Bootstrap’s CSS classes to style your content directly in your Markdown files or within your site's HTML templates.

#### Step 7: Previewing Your Creation

- **Local Preview**: Run `bundle exec jekyll serve` to preview your site locally. Inspect your site to ensure the Bootstrap magic has been successfully applied.

#### Step 8: Publishing Your Site to the World

- **Deployment**: Once satisfied with your enchanted site, deploy it to GitHub Pages, Netlify, or another hosting service to share your creation with the world.

### 🚀 Additional Quests

- **Customize Your Theme**: Dive deeper into the forests to explore customizing your Jekyll theme with Bootstrap.
- **Explore Plugins**: Enhance your site's capabilities by exploring Jekyll plugins for added functionality.

This map will guide you through the Frontend Forests as you build your Jekyll site with Bootstrap. Remember, the path to mastery involves experimentation and continuous learning. May the winds of the Frontend Forests be ever in your favor!

## 🔮 Chapter 9: Reading the Theme's Spellbook

Before you start swapping CDN links and editing layouts, it helps to understand *how* Jekyll actually assembles a page. The IT-Journey site runs on the `zer0-mistakes` theme, and the same mechanics apply to any Jekyll site you build.

### 🪄 How Jekyll Builds a Page

Every page is woven together through this pipeline:

```text
Markdown file (content + frontmatter)
        ↓
Layout template (_layouts/article.html)
        ↓
Includes (_includes/header.html, sidebar.html, …)
        ↓
Theme base layout (root.html → default.html)
        ↓
Static HTML file (in _site/)
```

When you run `bundle exec jekyll build`, Jekyll reads each content file, merges it with its assigned layout, resolves every `{% raw %}{% include %}{% endraw %}` call, evaluates the Liquid expressions, and writes the finished HTML into `_site/`.

### 📜 Layouts and Inheritance

Layouts are HTML templates that wrap your content. You pick one in front matter:

```yaml
---
layout: article
title: "My Blog Post"
---
```

Layouts chain together, each one wrapping the next. The special `content` variable in a parent layout is replaced by its child:

```text
article.html   →  default.html  →  root.html
(post content)    (header/footer)   (HTML skeleton)
```

So `root` provides the bare `<head>`/`<body>` shell and scripts, `default` adds the header, footer, and sidebar, and `article` adds post-specific chrome like date, author, and reading time. Quest pages use a local `quest` layout that adds prerequisites, rewards, and the network graph.

### 🧩 Includes (Reusable Partials)

Includes are reusable HTML snippets injected into layouts:

```liquid
{% raw %}{% include component.html %}{% endraw %}
```

You can pass variables into an include and read them back via the `include` object:

```liquid
{% raw %}{% include quest-card.html quest=quest show_xp=true %}{% endraw %}
```

Inside `quest-card.html`, those arrive as `include.quest` and `include.show_xp`. This is how a single partial renders dozens of different cards.

### ✨ Liquid Templating

Jekyll uses the [Liquid](https://shopify.github.io/liquid/) templating language for dynamic content. There are three constructs to know:

```liquid
{% raw %}{{ page.title }}                              {# output a variable #}
{% if page.draft %}…{% endif %}              {# logic / control flow #}
{% for post in site.posts limit:5 %}…{% endfor %}  {# loop a collection #}{% endraw %}
```

Filters transform values on the way out — a few you will reach for constantly:

| Filter | Example | Result |
|--------|---------|--------|
| `date` | `{% raw %}{{ page.date \| date: "%B %d, %Y" }}{% endraw %}` | "March 31, 2026" |
| `slugify` | `{% raw %}{{ "My Title" \| slugify }}{% endraw %}` | "my-title" |
| `where` | `{% raw %}{{ site.quests \| where: "difficulty", "🟢 Easy" }}{% endraw %}` | Filtered array |
| `markdownify` | `{% raw %}{{ page.description \| markdownify }}{% endraw %}` | HTML from markdown |

### 🗄️ Data Files

YAML files in `_data/` are available everywhere as `site.data.*`, keeping structured data out of your templates. For example, `_data/navigation/main.yml` powers the primary menu via `site.data.navigation.main`:

```liquid
{% raw %}{% for item in site.data.navigation.main %}
  <a href="{{ item.url }}">{{ item.title }}</a>
{% endfor %}{% endraw %}
```

### 🛡️ Customizing a Theme Without Forking It

Because IT-Journey uses a *remote* theme gem, you do not edit the theme directly — you **override** it. Jekyll checks your own project first, then falls back to the gem:

```text
_layouts/default.html    ← your copy wins over the theme's
_includes/header.html    ← same override pattern
```

Drop a file with the same path into your project to replace the theme's version, or add entirely new files to `_layouts/`/`_includes/` to extend it. And remember: `_site/` is regenerated on every build and listed in `.gitignore` — never edit files there directly.

### 🔍 Knowledge Check

- [ ] Can you trace a page from its Markdown file through layouts to `_site/`?
- [ ] How do you override a theme layout without editing the gem?
- [ ] What does the `where` filter return, and where would you use it?

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0100 - Frontend Development & Docker]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]

