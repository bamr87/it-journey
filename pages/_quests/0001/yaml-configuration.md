---
title: 'YAML Configuration: Site Settings Mastery'
author: IT-Journey Team
description: 'Master YAML for Jekyll: write front matter, configure _config.yml, build _data files, and dodge the indentation, quoting, and type pitfalls beginners hit.'
excerpt: Learn YAML syntax and Jekyll configuration to build and customize professional static websites.
preview: images/previews/yaml-configuration-site-settings-quest-descripti.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0001'
difficulty: 🟢 Easy
estimated_time: 45-60 minutes
primary_technology: yaml
quest_type: main_quest
quest_series: Static Site Mastery
quest_line: The Web Fundamentals Codex
quest_arc: Forging Your First Website
quest_dependencies:
  required_quests:
  - /quests/0001/jekyll-fundamentals/
  recommended_quests: []
  unlocks_quests:
  - /quests/0001/liquid-templating/
  - /quests/0001/github-pages-basics/
skill_focus: frontend
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Comfort editing plain text files
  - Completion of Jekyll Fundamentals
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - A text editor and a working Jekyll site
  skill_level_indicators:
  - No prior YAML experience required
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A custom _config.yml and a _data file in use
  skill_demonstrations:
  - Can write valid YAML mappings, lists, and nested data
  - Can configure a Jekyll site through _config.yml
  knowledge_checks:
  - Understands why indentation must be spaces, not tabs
  - Can spot and fix a common quoting error
permalink: /quests/0001/yaml-configuration/
redirect_from:
- /quickstart/site-configuration/
- /docs/jekyll/jekyll-config/
- /docs/jekyll-config/
categories:
- Quests
- Frontend
- Static-Sites
- Beginner
tags:
- '0001'
- yaml
- jekyll
- configuration
- web-development
- main_quest
- frontend
- hands-on
- beginner
keywords:
  primary:
  - '0001'
  - yaml
  - jekyll
  - configuration
  secondary:
  - web-development
  - main_quest
  - frontend
  - hands-on
  - beginner
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0001 (1) Quest: Main Quest - YAML'
rewards:
  badges:
  - 🏆 Keeper of the Config - Mastered _config.yml and front matter
  - 🌱 Scribe of Structured Data - Authored clean YAML data files
  skills_unlocked:
  - 🛠️ Jekyll Configuration
  - 🧠 Structured Data Modeling
  progression_points: 50
  unlocks_features:
  - Structured data files that power data-driven Liquid templates
layout: quest
---
*Greetings, brave adventurer! Beneath every Jekyll site lies a quiet language of settings and data: **YAML**. It is the ink in which `_config.yml` is written, the metadata atop every page, and the format of the data files your templates loop over. Master YAML and you control the entire behaviour of your site - without touching a single line of Ruby.*

*This is a short but vital quest. YAML is simple to read and easy to get subtly wrong, and a single stray tab or unquoted colon can break a whole build. Learn its rules and its traps here, and you will never fear the config file again.*

## 📖 The Legend Behind This Quest

*The elders of computing grew weary of formats that were powerful but unreadable - XML with its endless angle brackets, JSON with its strict commas and braces. They wanted a config language a human could read at a glance and write without ceremony. So **YAML** - "YAML Ain't Markup Language" - was forged: indentation for structure, plain words for keys and values, almost no punctuation. Today it configures Jekyll, GitHub Actions, Docker Compose, Kubernetes, and half the tools you will ever use.*

*Learn YAML once, here, and you carry the skill into every future quest in the realm.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **YAML Syntax** - Write mappings, lists, and nested structures correctly
- [ ] **Front Matter** - Use the `---` block to set per-page metadata
- [ ] **The `_config.yml` File** - Configure a Jekyll site's global behaviour
- [ ] **Data Files** - Store structured data in `_data` and read it in templates

### Secondary Objectives (Bonus Achievements)
- [ ] **Types & Quoting** - Control strings, numbers, booleans, and null
- [ ] **Multi-line Strings** - Use block scalars (`|` and `>`)
- [ ] **Validate Before You Ship** - Lint YAML to catch errors early

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain why YAML uses spaces, never tabs, for indentation
- [ ] Spot the bug in a value like `version: 1.20` vs `version: "1.20"`
- [ ] Model a small nested dataset and read it from a Liquid template

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Comfort creating and editing plain text files
- [ ] Completion of [Jekyll Fundamentals](/quests/0001/jekyll-fundamentals/)
- [ ] No prior YAML experience required

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] A text editor or IDE (VS Code recommended)
- [ ] A working Jekyll site to edit

### 🧠 Skill Level Indicators
This **🟢 Easy** quest expects:
- [ ] Beginner-friendly - no prior YAML experience required
- [ ] You can serve a Jekyll site locally
- [ ] Ready for 45-60 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*YAML is just text, so editing is identical everywhere. What differs is the linter you install to catch mistakes.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install yamllint to validate your YAML
brew install yamllint

# Check a file
yamllint _config.yml
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install yamllint via pip (Python required)
pip install yamllint

# Check a file
yamllint _config.yml
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install -y yamllint

# Validate
yamllint _config.yml
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Lint without installing anything locally
docker run --rm -v "$PWD":/data cytopia/yamllint _config.yml
```

In VS Code, the **YAML** extension by Red Hat highlights errors as you type.

</details>

## 🧙‍♂️ Chapter 1: YAML Syntax - Mappings, Lists, and Nesting

*YAML structures data with just two shapes: **mappings** (key-value pairs) and **sequences** (lists). Indentation - always spaces - shows what belongs to what.*

### ⚔️ Skills You'll Forge in This Chapter
- Writing mappings and lists
- Nesting structures with indentation
- Mixing the two

### 🏗️ The Core Shapes

```yaml
# A mapping: key, colon, space, value
title: My Castle
published: true
post_count: 42

# A sequence (list): each item on a dashed line
authors:
  - Ada
  - Linus
  - Grace

# Nesting: indent (with SPACES) to show containment
social:
  github: octocat
  links:
    - https://example.com
    - https://it-journey.dev

# A list of mappings - extremely common in data files
navigation:
  - name: Home
    url: /
  - name: Quests
    url: /quests/
```

The two iron rules of YAML:

1. **Indentation is spaces, never tabs.** A single tab anywhere will break the parse.
2. **A space follows every colon.** `key:value` is wrong; `key: value` is right.

### 🔍 Knowledge Check: Syntax
- [ ] What two shapes does all YAML reduce to?
- [ ] What character is forbidden for indentation?
- [ ] How do you write a list where each item is itself a mapping?

### ⚡ Quick Wins and Checkpoints
- [ ] **Wrote a mapping**: You created a valid key-value file
- [ ] **Nested a list**: You indented a list under a key with spaces

## 🧙‍♂️ Chapter 2: Front Matter and _config.yml - Configuring Jekyll

*Two YAML files run your Jekyll site. **Front matter** - the YAML block at the top of a page between `---` lines - sets per-page metadata. **`_config.yml`** sets site-wide behaviour.*

### ⚔️ Skills You'll Forge in This Chapter
- Reading and writing front matter
- Configuring a site in `_config.yml`
- Setting collection and default behaviour

### 🏗️ Front Matter and Global Config

Front matter at the top of `about.md`:

```yaml
---
layout: default
title: About the Castle
nav_order: 2
tags:
  - meta
  - about
---
```

Everything between the fences is YAML, and Jekyll exposes it to Liquid as `page.title`, `page.tags`, and so on.

A practical `_config.yml`:

```yaml
# Site identity
title: My Castle
description: A site forged in the Web Fundamentals tier
url: "https://username.github.io"
baseurl: ""

# Build behaviour
markdown: kramdown
permalink: /:categories/:title/

# Collections
collections:
  recipes:
    output: true
    permalink: /recipes/:name/

# Front-matter defaults - apply layout to all posts automatically
defaults:
  - scope:
      path: ""
      type: posts
    values:
      layout: post

# Files Jekyll should ignore
exclude:
  - Gemfile
  - Gemfile.lock
  - README.md
```

> ⚠️ Jekyll only re-reads `_config.yml` on restart. After editing it, stop and restart `jekyll serve` - live reload will not pick up config changes.

### 🔍 Knowledge Check: Configuration
- [ ] Where does front matter live in a page, and what wraps it?
- [ ] What does the `defaults` block let you avoid repeating?
- [ ] Why must you restart the server after editing `_config.yml`?

## 🧙‍♂️ Chapter 3: Data Files & Common Pitfalls - The Subtle Traps

*The `_data` folder turns YAML into a tiny database. And because YAML guesses types, a handful of classic traps await the careless scribe.*

### ⚔️ Skills You'll Forge in This Chapter
- Storing data in `_data` and reading it
- Controlling types with quoting
- Avoiding the famous YAML gotchas

### 🏗️ Data Files in Action

Create `_data/team.yml`:

```yaml
- name: Ada Lovelace
  role: Architect
  active: true
- name: Grace Hopper
  role: Compiler Smith
  active: true
```

Read it in any template - the file name becomes the key under `site.data`:

```liquid

{% raw %}{% for member in site.data.team %}{% endraw %}
  {% raw %}{% if member.active %}{% endraw %}
    <p>{% raw %}{{ member.name }}{% endraw %} - {% raw %}{{ member.role }}{% endraw %}</p>
  {% raw %}{% endif %}{% endraw %}
{% raw %}{% endfor %}{% endraw %}

```

**The common pitfalls** - memorize these and you will dodge most YAML bugs:

```yaml
# 1. Unquoted booleans: these become true/false, not strings!
answer: yes        # -> boolean true (!)  use: answer: "yes"
state: on          # -> boolean true (!)  use: state: "on"

# 2. Numbers that should be strings (versions, zip codes)
version: 1.20      # -> the number 1.2 (trailing zero lost!)
version: "1.20"    # -> the string "1.20"  ✅

# 3. Colons inside values must be quoted
title: Jekyll: a static generator     # ❌ parse error
title: "Jekyll: a static generator"   # ✅

# 4. Leading zeros and special chars need quotes
zip: 01234         # ❌ may be read as octal
zip: "01234"       # ✅

# 5. Block scalars for multi-line text
summary: |         # literal: keeps newlines
  Line one.
  Line two.
tagline: >         # folded: joins lines with spaces
  This long line will be
  folded into one paragraph.
```

Always lint before you commit:

```bash
yamllint _config.yml _data/team.yml
```

### 🔍 Knowledge Check: Data & Pitfalls
- [ ] Why does `version: 1.20` lose its trailing zero?
- [ ] How do you keep `yes` as the string "yes"?
- [ ] What is the difference between the `|` and `>` block scalars?

## 🔮 Chapter 4: Production-Ready Config - Plugins, Environments & Strict Validation

*A real `_config.yml` does more than name your site. It summons **plugins** that generate feeds and sitemaps, layers a **development override** so localhost and production never collide, and turns on a switch that makes a build **fail loudly** on a single bad YAML character.*

### ⚔️ Skills You'll Forge in This Chapter
- Loading plugins and knowing what each one generates
- Layering configs with `_config_dev.yml` for safe local development
- Forcing the build to reject malformed front matter

### 🏗️ Plugins - Generators You Enable in YAML

Plugins are listed as a YAML sequence. Each one quietly produces files you would otherwise hand-write:

```yaml
plugins:
  - jekyll-feed       # RSS feed at /feed.xml
  - jekyll-sitemap    # sitemap.xml for search engines
  - jekyll-seo-tag    # <meta> tags for SEO and social sharing
  - jekyll-remote-theme  # load a theme straight from GitHub
```

| Plugin | What it generates |
|---|---|
| `jekyll-feed` | An RSS feed at `/feed.xml` |
| `jekyll-sitemap` | A `sitemap.xml` so crawlers find every page |
| `jekyll-seo-tag` | SEO and social `<meta>` tags in your `<head>` |
| `jekyll-remote-theme` | Loads a theme (like `bamr87/zer0-mistakes`) from a GitHub repo |

### 🏗️ Environment Layering - One Site, Two Configs

Jekyll can read **several config files in order**, with later files overriding earlier ones. Keep production values in `_config.yml` and local-only values in a `_config_dev.yml`:

```yaml
# _config_dev.yml - local overrides only
url: "http://localhost:4002"
```

Serve with both, comma-separated and **no spaces**:

```bash
bundle exec jekyll serve --config _config.yml,_config_dev.yml
```

Now `url` points at localhost while you develop, but production still publishes the real domain - you never accidentally ship a `localhost` link. Pair this with `JEKYLL_ENV=production` to switch on analytics and other production-only behaviour:

```bash
JEKYLL_ENV=production bundle exec jekyll build
```

### 🏗️ Fail Fast on Bad YAML

By default Jekyll silently ignores front matter it cannot parse. Flip one switch and a malformed `---` block becomes a hard build error instead of a mystery:

```yaml
# _config.yml
strict_front_matter: true
```

> ⚠️ **Tabs are forbidden in config files too.** A stray tab in `_config.yml` will either throw a parse error or - worse - make Jekyll silently revert to defaults. Use spaces everywhere, and let `yamllint` catch the tab before Jekyll does.

### 🔍 Knowledge Check: Production Config
- [ ] Which plugin produces `sitemap.xml`, and why does it matter for SEO?
- [ ] How does `_config_dev.yml` stop a `localhost` URL reaching production?
- [ ] What does `strict_front_matter: true` change about a build with bad YAML?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Valid YAML
**Objective**: Write a small, valid YAML document.

**Requirements**:
- [ ] Include at least one mapping, one list, and one nested structure
- [ ] Use spaces only for indentation
- [ ] Pass `yamllint` with no errors

**Validation**: `yamllint yourfile.yml` reports no errors.

### 🟡 Intermediate Challenge: Configure the Site
**Objective**: Customize your Jekyll site through `_config.yml`.

**Requirements**:
- [ ] Set `title`, `description`, and a `permalink` pattern
- [ ] Add a `defaults` block that applies a layout automatically
- [ ] Restart the server and confirm the changes took effect

**Validation**: The site reflects your new title and default layout.

### 🔴 Advanced Challenge: Data-Driven Page
**Objective**: Drive a page from a `_data` file, dodging the type traps.

**Requirements**:
- [ ] Create a `_data` file with a list of mappings
- [ ] Quote at least one value that would otherwise mistype
- [ ] Loop over it in a template with a conditional

**Validation**: The page renders the data and no value is mistyped.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Keeper of the Config** - `_config.yml` and front matter hold no fear
- 🌱 **Scribe of Structured Data** - You author clean, correct YAML

**🛠️ Skills Unlocked**:
- **Jekyll Configuration** - Bend a site's behaviour to your will
- **Structured Data Modeling** - Shape data for templates to consume

**🔓 Unlocked Quests**:
- Liquid Templating - Loop over the data you just modeled
- GitHub Pages Basics - Configure url and baseurl for production

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Liquid Templating](/quests/0001/liquid-templating/) - Turn data into pages

**Explore Side Adventures**:
- ⚔️ [GitHub Pages Basics](/quests/0001/github-pages-basics/) - Config for the live web
- ⚔️ [Git Workflow Mastery](/quests/0001/git-workflow-mastery/) - Version your config safely

### Character Class Recommendations

**💻 Software Developer**: Continue to [Liquid Templating](/quests/0001/liquid-templating/)  
**🏗️ System Engineer**: Explore [GitHub Pages Basics](/quests/0001/github-pages-basics/)  
**🎨 Frontend Specialist**: Model richer data files for your theme

## 📚 Resources

### Official Documentation
- [YAML Specification](https://yaml.org/spec/1.2.2/) - The authoritative reference
- [Jekyll Configuration Options](https://jekyllrb.com/docs/configuration/options/) - Every build, serve, and global setting and flag
- [Jekyll Front-matter Defaults](https://jekyllrb.com/docs/configuration/front-matter-defaults/) - The `defaults` block in depth
- [Jekyll Data Files](https://jekyllrb.com/docs/datafiles/) - Using the `_data` folder

### Community Resources
- [Learn YAML in Y Minutes](https://learnxinyminutes.com/docs/yaml/) - A fast, complete tour
- [YAML on Stack Overflow](https://stackoverflow.com/questions/tagged/yaml) - Tagged Q&A
- [The Norway Problem](https://hitchdev.com/strictyaml/why/implicit-typing-removed/) - The famous `NO` -> false gotcha

### Tools & Utilities
- [yamllint](https://yamllint.readthedocs.io/) - Catch errors before they ship
- [YAML Validator (online)](https://www.yamllint.com/) - Paste and check in your browser

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Configured a site and used a data file
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0001 - Web Fundamentals]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Jekyll Fundamentals]]
**Unlocks:** [[Liquid Templating]] · [[GitHub Pages Basics]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
