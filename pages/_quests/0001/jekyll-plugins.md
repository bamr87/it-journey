---
title: 'Jekyll Plugins: Extend Your Static Site Safely'
author: IT-Journey Team
description: Master Jekyll plugins. Learn what plugins are, which are GitHub-Pages safe, how to configure common ones like SEO and sitemaps, and how to write a simple custom generator.
excerpt: Extend Jekyll with plugins - GitHub Pages safe gems, common extensions, and your own generator.
preview: images/previews/jekyll-plugins-extending-site-functionality-descri.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0001'
difficulty: 🟡 Medium
estimated_time: 60-75 minutes
primary_technology: jekyll
quest_type: main_quest
quest_series: Jekyll Mastery
quest_line: The Web Fundamentals Codex
quest_arc: Publishing Your First Website
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/0001/advanced-markdown/
  - /quests/0001/seo-optimization/
  unlocks_quests:
  - /quests/0001/analytics-integration/
skill_focus: backend
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Basic command line navigation
  - A working Jekyll site and familiarity with _config.yml
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Ruby 3.x, Jekyll, and Bundler installed
  skill_level_indicators:
  - Comfortable building and serving a Jekyll site
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A site configured with safe plugins and one working custom plugin
  skill_demonstrations:
  - Can add and configure GitHub-Pages safe plugins
  - Can write a simple generator or filter plugin
  knowledge_checks:
  - Understands why GitHub Pages restricts plugins
  - Can explain the difference between a generator and a filter
permalink: /quests/0001/jekyll-plugins/
categories:
- Quests
- Backend
- Jekyll
- Beginner
tags:
- '0001'
- jekyll
- plugins
- ruby
- main_quest
- hands-on
- beginner
keywords:
  primary:
  - '0001'
  - jekyll
  - plugins
  - ruby
  secondary:
  - main_quest
  - backend
  - hands-on
  - beginner
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0001 (1) Quest: Main Quest - Jekyll Plugins'
rewards:
  badges:
  - 🏆 Enchanter of the Build - Extended Jekyll with new powers
  - 🌱 Sprout of Automation - Internalized safe plugins and the build lifecycle
  skills_unlocked:
  - 🛠️ Jekyll Plugin Configuration
  - 🧠 Writing a Custom Generator
  progression_points: 50
  unlocks_features:
  - Completion of the Level 0001 Web Fundamentals quest line
layout: quest
redirect_from:
- /quests/0011/jekyll-plugins/
---
*Greetings, brave adventurer! Welcome to **Jekyll Plugins** - the quest where you teach the static-site engine new spells. Jekyll out of the box is powerful, but plugins are how it becomes truly yours: they add SEO tags, sitemaps, feeds, image processing, and any custom logic you can imagine. A plugin runs during the build, so the cost is paid once and your visitors still receive plain, fast files.*

*Whether you simply want to switch on the community's battle-tested gems or you are ready to write your own Ruby to generate pages, this adventure will teach you what plugins are, which ones GitHub Pages allows, how to configure the common ones, and how to forge a simple generator of your own.*

## 📖 The Legend Behind This Quest

*Jekyll's creators knew they could not anticipate every need, so they built a plugin system: hooks where your own code can run during the build. The community filled it with gems for nearly everything. But there is a catch in the kingdom of GitHub Pages - because it builds your site on its own servers, it only runs a **whitelist** of vetted, safe plugins. Step outside that list and you must build the site yourself (via Actions) and publish the output. Understanding this boundary - safe-by-default versus full-power-with-responsibility - is the heart of plugin mastery.*

*This quest teaches the plugin lifecycle, the GitHub-Pages safe set, common configurations, and how to write your own generator and filter.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **What Plugins Are** - Understand how plugins hook into the build
- [ ] **GitHub-Pages Safe Plugins** - Know the whitelist and why it exists
- [ ] **Configuring Common Plugins** - Enable SEO, sitemap, feed, and pagination
- [ ] **Writing a Generator** - Create a simple custom plugin in Ruby

### Secondary Objectives (Bonus Achievements)
- [ ] **Custom Liquid Filters** - Add your own template helpers
- [ ] **Building Beyond the Whitelist** - Deploy non-whitelisted plugins via Actions
- [ ] **Plugin Hygiene** - Pin versions and keep builds reproducible

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain why GitHub Pages restricts which plugins run
- [ ] Configure three common plugins from memory
- [ ] Write a generator that emits a page at build time

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] A working Jekyll site and familiarity with `_config.yml`
- [ ] Basic command line navigation (`cd`, `ls`)
- [ ] Recommended: completion of [SEO Optimization](/quests/0001/seo-optimization/)

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Ruby 3.x, Jekyll, and Bundler installed
- [ ] A text editor or IDE (VS Code recommended)
- [ ] Internet connection for installing gems

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You can already build and serve a Jekyll site
- [ ] You are comfortable editing `_config.yml` and the `Gemfile`
- [ ] Ready for 60-75 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*Plugins are Ruby gems that run during the Jekyll build, so you need a working Jekyll toolchain. Pick your path.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# In your Jekyll site, add a couple of safe plugins
cd ~/my-site
bundle add jekyll-seo-tag jekyll-sitemap jekyll-feed
bundle exec jekyll build --verbose
```

**macOS-Specific Notes:**
- `bundle add` updates both your `Gemfile` and `Gemfile.lock`.
- Custom plugins live in a `_plugins/` folder and load automatically on local builds.

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# In your Jekyll site, add a couple of safe plugins
cd $HOME\my-site
bundle add jekyll-seo-tag jekyll-sitemap jekyll-feed
bundle exec jekyll build --verbose
```

**Windows-Specific Notes:**
- WSL2 with Ubuntu gives the smoothest Ruby/Jekyll experience on Windows.
- The `_plugins/` folder only runs on local/Actions builds, never on stock Pages.

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# In your Jekyll site, add a couple of safe plugins
cd ~/my-site
bundle add jekyll-seo-tag jekyll-sitemap jekyll-feed
bundle exec jekyll build --verbose
```

**Linux-Specific Notes:**
- Install gems to your home directory to avoid needing `sudo`.
- Run `bundle exec jekyll build` so the exact pinned gem versions are used.

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# For non-whitelisted plugins, build with GitHub Actions instead of stock Pages.
# The official Jekyll Actions workflow runs `jekyll build` with ANY plugin
# in your Gemfile, then deploys the _site output to Pages.
docker run --rm -v "$PWD":/srv/jekyll jekyll/jekyll:4 jekyll build
```

**Cloud-Specific Notes:**
- Stock GitHub Pages runs only the whitelist; GitHub Actions runs anything.
- A Codespace ships Ruby, so `bundle add` and custom `_plugins/` work immediately.

</details>

## 🧙‍♂️ Chapter 1: What Plugins Are & the Safe Set - The Boundary

*A Jekyll plugin is Ruby code that runs at build time, hooking into stages of the build to transform content or generate new pages. Where it can run depends on who builds your site.*

### ⚔️ Skills You'll Forge in This Chapter
- The plugin types and the build lifecycle
- The GitHub-Pages whitelist and why it exists
- Where plugins are declared and loaded

### 🏗️ Plugins in the Build

There are a few plugin types: **generators** create new pages, **filters** and **tags** extend Liquid, **converters** add markup languages, and **hooks** run code at lifecycle moments. They are declared in `_config.yml` (for gems) or dropped into `_plugins/` (for local Ruby):

```yaml
# _config.yml — gem-based plugins, safe on GitHub Pages
plugins:
  - jekyll-seo-tag      # SEO meta + JSON-LD
  - jekyll-sitemap      # generates /sitemap.xml
  - jekyll-feed         # generates an Atom feed at /feed.xml
  - jekyll-paginate     # paginates a blog index
```

GitHub Pages builds your site on its own servers, so for security it only runs a fixed **whitelist** of plugins. The popular safe ones include:

| Plugin | What it does |
| --- | --- |
| `jekyll-seo-tag` | Title, description, Open Graph, JSON-LD |
| `jekyll-sitemap` | Automatic `sitemap.xml` |
| `jekyll-feed` | Atom/RSS feed |
| `jekyll-paginate` | Paginated post listings |
| `jekyll-redirect-from` | `redirect_from` frontmatter support |
| `jekyll-relative-links` | Resolve relative `.md` links |

Anything outside the list - including any code in your `_plugins/` folder - is ignored by stock Pages. To use it, you build the site yourself with **GitHub Actions** (or locally) and deploy the finished `_site`.

### 🔍 Knowledge Check: Plugins & the Whitelist
- [ ] Name three plugin types and what each does.
- [ ] Why does GitHub Pages run only a whitelist of plugins?
- [ ] Where do gem plugins go, and where do custom Ruby plugins go?

### ⚡ Quick Wins and Checkpoints
- [ ] **Plugins enabled**: Safe gems are listed in `_config.yml` and the `Gemfile`
- [ ] **Understood the boundary**: You can explain whitelist vs. Actions builds

## 🧙‍♂️ Chapter 2: Configuring Common Plugins - Switching On the Power

*Most of the value comes from configuring the community gems well. A few lines unlock SEO, a sitemap, a feed, and pagination.*

### ⚔️ Skills You'll Forge in This Chapter
- Wiring up jekyll-feed and pagination
- Placing plugin output tags in layouts
- Verifying plugin output

### 🏗️ Feeds, SEO, and Pagination

After adding the gems, place their output tags in your layout's `<head>`:


```liquid
<head>
  <meta charset="utf-8" />
  {% raw %}{% seo %}{% endraw %}          <!-- from jekyll-seo-tag: meta + JSON-LD -->
  {% raw %}{% feed_meta %}{% endraw %}    <!-- from jekyll-feed: links the Atom feed -->
</head>
```


`jekyll-sitemap` needs no tag - it just generates `/sitemap.xml`. For **pagination**, configure it in `_config.yml` and loop over `paginator.posts` in your index:

```yaml
# _config.yml
paginate: 5                # posts per page
paginate_path: "/page:num/"
```


```liquid
---
layout: default
---
{% raw %}{% for post in paginator.posts %}{% endraw %}
  <h2><a href="{% raw %}{{ post.url }}{% endraw %}">{% raw %}{{ post.title }}{% endraw %}</a></h2>
  <p>{% raw %}{{ post.excerpt }}{% endraw %}</p>
{% raw %}{% endfor %}{% endraw %}

{% raw %}{% if paginator.next_page %}{% endraw %}
  <a href="{% raw %}{{ paginator.next_page_path }}{% endraw %}">Older posts</a>
{% raw %}{% endif %}{% endraw %}
```


Build and verify: `/feed.xml`, `/sitemap.xml`, and `/page2/` should all exist. The `{% raw %}{% seo %}{% endraw %}` output appears in your page source as a block of meta tags.

### 🔍 Knowledge Check: Configuration
- [ ] Which plugin needs a layout tag, and which generates output silently?
- [ ] What two config keys enable pagination?
- [ ] How would you confirm `jekyll-feed` is working?

### ⚡ Quick Wins and Checkpoints
- [ ] **Feed live**: `/feed.xml` exists and validates
- [ ] **Pagination works**: A second page of posts is generated

## 🧙‍♂️ Chapter 3: Writing Your Own Plugin - Forging New Spells

*When no gem does what you need, write your own. A **generator** creates pages at build time; a **filter** adds a Liquid helper. Both are short Ruby files in `_plugins/`.*

### ⚔️ Skills You'll Forge in This Chapter
- Writing a custom Liquid filter
- Writing a generator that emits a page
- Knowing when a custom plugin requires an Actions build

### 🏗️ A Custom Liquid Filter

Create `_plugins/reading_time.rb`. This adds a `reading_time` filter you can use in any template:

```ruby
# _plugins/reading_time.rb
module Jekyll
  module ReadingTimeFilter
    # Usage in a template: {% raw %}{{ content | reading_time }}{% endraw %}
    def reading_time(input)
      words = input.to_s.split.size
      minutes = (words / 200.0).ceil   # ~200 words per minute
      "#{minutes} min read"
    end
  end
end

Liquid::Template.register_filter(Jekyll::ReadingTimeFilter)
```

Now any layout can call it:


```liquid
<p class="meta">{% raw %}{{ content | reading_time }}{% endraw %}</p>
```


### 🏗️ A Generator That Creates a Page

A **generator** runs once per build and can add pages to the site. This one emits a simple `stats.html` listing how many posts exist:

```ruby
# _plugins/stats_generator.rb
module Jekyll
  class StatsPage < Page
    def initialize(site, base)
      @site = site
      @base = base
      @dir  = "/"
      @name = "stats.html"
      process(@name)
      # Build the page content directly (no source file needed)
      self.data = { "layout" => "default", "title" => "Site Stats" }
      self.content = "<h1>Posts published: #{site.posts.docs.size}</h1>"
    end
  end

  class StatsGenerator < Generator
    safe true   # declare the plugin has no side effects
    def generate(site)
      site.pages << StatsPage.new(site, site.source)
    end
  end
end
```

After a build, visit `/stats.html` - a page that did not exist as a source file, conjured entirely by your generator. Because custom `_plugins/` code is not on the GitHub-Pages whitelist, deploy sites that use it with **GitHub Actions** (build, then publish `_site`) rather than stock Pages.

### 🔍 Knowledge Check: Custom Plugins
- [ ] What is the difference between a generator and a filter?
- [ ] Where must custom Ruby plugins live to load automatically?
- [ ] Why does a site with a custom generator need an Actions build for Pages?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Enable the Safe Set
**Objective**: Configure a site with the common GitHub-Pages safe plugins.

**Requirements**:
- [ ] Add `jekyll-seo-tag`, `jekyll-sitemap`, and `jekyll-feed`
- [ ] Place the required tags in your layout head
- [ ] Build and confirm `/sitemap.xml` and `/feed.xml`

**Validation**: Both generated files load in the browser after a build.

### 🟡 Intermediate Challenge: A Custom Filter
**Objective**: Write a Liquid filter and use it in a template.

**Requirements**:
- [ ] A Ruby file in `_plugins/` registering a filter
- [ ] The filter used in at least one layout or page
- [ ] A successful local build using the filter

**Validation**: The filter's output appears on the rendered page.

### 🔴 Advanced Challenge: A Generator + Actions Deploy
**Objective**: Write a generator and deploy it correctly.

**Requirements**:
- [ ] A generator in `_plugins/` that emits at least one new page
- [ ] A GitHub Actions workflow that runs `jekyll build`
- [ ] The generated page live on the deployed site

**Validation**: The generated page exists on the Actions-built, deployed site.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Enchanter of the Build** - You extended Jekyll with new powers
- 🌱 **Sprout of Automation** - Safe plugins and the build lifecycle are second nature

**🛠️ Skills Unlocked**:
- **Jekyll Plugin Configuration** - Wire up the community's best gems
- **Writing a Custom Generator** - Emit pages and helpers from your own Ruby

**🔓 Unlocked Quests**:
- Analytics Integration - Add measurement through includes and config
- SEO Optimization - The plugins behind automated metadata

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Analytics Integration](/quests/0001/analytics-integration/) - Measure your now-extensible site

**Explore Side Adventures**:
- ⚔️ [SEO Optimization](/quests/0001/seo-optimization/) - The SEO plugins in depth
- ⚔️ [Advanced Markdown](/quests/0001/advanced-markdown/) - The content your plugins process

### Character Class Recommendations

**💻 Software Developer**: Continue to [Analytics Integration](/quests/0001/analytics-integration/)  
**🏗️ System Engineer**: Explore building beyond the whitelist with Actions  
**🎨 Frontend Specialist**: Revisit [SEO Optimization](/quests/0001/seo-optimization/)  

## 📚 Resources

### Official Documentation
- [Jekyll Plugins Documentation](https://jekyllrb.com/docs/plugins/) - The canonical guide
- [GitHub Pages: Dependency versions](https://pages.github.com/versions/) - The plugin whitelist
- [Jekyll Generators](https://jekyllrb.com/docs/plugins/generators/) - Emitting pages in Ruby

### Community Resources
- [Jekyll Liquid Filters](https://jekyllrb.com/docs/liquid/filters/) - Built-in filters to extend
- [Awesome Jekyll Plugins](https://github.com/planetjekyll/awesome-jekyll-plugins) - A curated list
- [Jekyll Talk Forum](https://talk.jekyllrb.com/) - Ask plugin questions

### Learning Materials
- [Jekyll Actions](https://github.com/jekyll/actions) - Build with any plugin via GitHub Actions
- [Jekyll Hooks](https://jekyllrb.com/docs/plugins/hooks/) - Run code at lifecycle moments

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Configured safe plugins and wrote one custom plugin
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0001 - Web Fundamentals]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Unlocks:** [[Analytics Integration]] · [[SEO Optimization]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
