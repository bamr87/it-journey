---
title: 'Jekyll Fundamentals: Build Static Sites with Ruby'
author: IT-Journey Team
description: 'Master Jekyll static site generation: install Ruby and Jekyll, learn the project structure and collections, then build and serve a fast, secure site.'
excerpt: Build fast, secure static websites with Jekyll - no databases or servers required.
preview: images/previews/jekyll-fundamentals-static-site-generation-descrip.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0001'
difficulty: 🟢 Easy
estimated_time: 75-90 minutes
primary_technology: jekyll
quest_type: main_quest
quest_series: Static Site Mastery
quest_line: The Web Fundamentals Codex
quest_arc: Forging Your First Website
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/0000/git-basics/
  unlocks_quests:
  - /quests/0001/github-pages-basics/
  - /quests/0001/liquid-templating/
  - /quests/0001/yaml-configuration/
skill_focus: frontend
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Basic command line navigation (cd, ls, mkdir)
  - Comfort editing text files in any editor
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Ruby 3.x and a terminal
  skill_level_indicators:
  - No prior Jekyll or Ruby experience required
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A working Jekyll site built and served locally
  skill_demonstrations:
  - Can explain what a static site generator does
  - Can build and serve a Jekyll site independently
  knowledge_checks:
  - Understands the role of the _site output folder
  - Can troubleshoot a failed build
permalink: /quests/0001/jekyll-fundamentals/
categories:
- Quests
- Frontend
- Static-Sites
- Beginner
tags:
- '0001'
- jekyll
- static-site-generator
- ruby
- web-development
- main_quest
- frontend
- hands-on
- beginner
keywords:
  primary:
  - '0001'
  - jekyll
  - static-site-generator
  - ruby
  secondary:
  - web-development
  - main_quest
  - frontend
  - hands-on
  - beginner
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0001 (1) Quest: Main Quest - Jekyll'
rewards:
  badges:
  - 🏆 Site Smith - Built your first static site from scratch
  - 🌱 Sprout of the Static Web - Internalized the build-and-serve loop
  skills_unlocked:
  - 🛠️ Jekyll Project Scaffolding
  - 🧠 Static Site Generation Concepts
  progression_points: 50
  unlocks_features:
  - Access to the rest of the Level 0001 Web Fundamentals quest line
layout: quest
---
*Greetings, brave adventurer! Welcome to **Jekyll Fundamentals** - your first true step into the realm of the web. In the previous tier you learned to wield the terminal and the version-control scrolls. Now you will forge something the whole world can visit: a website. And you will build it the wise way - as a fast, secure **static site** that needs no database and no fragile server to defend.*

*Whether you have never written a line of HTML or you are an old hand looking to ship sites without the weight of a content-management beast, this adventure will teach you the "how" and, more importantly, the "why" behind the static web.*

## 📖 The Legend Behind This Quest

*In the early days, every web page was conjured fresh on each visit - the server would wake a database, run code, assemble the page, and only then send it. Powerful, but slow, costly, and full of trap doors for attackers. Then a band of builders realized a simple truth: most pages do not change between visitors. Why rebuild the castle every time someone knocks? **Jekyll** was born from this insight - generate every page once, ahead of time, and serve plain files. The result is a site that loads instantly, costs nearly nothing to host, and has almost no attack surface.*

*Jekyll, written in Ruby, powers GitHub Pages and countless documentation sites, blogs, and portfolios across the kingdom. Master it, and you hold the foundation stone of the entire Web Fundamentals tier.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **What a Static Site Generator Is** - Explain how Jekyll turns source files into a finished website
- [ ] **The Jekyll Directory Structure** - Recognize every special folder and what it does
- [ ] **Collections & Content** - Add posts, pages, and a custom collection
- [ ] **The Build & Serve Loop** - Run `jekyll build` and `jekyll serve` and read the output

### Secondary Objectives (Bonus Achievements)
- [ ] **Bundler & Gemfile** - Manage Jekyll and plugins reproducibly
- [ ] **Front Matter Basics** - Add metadata to a page that controls how it renders
- [ ] **Drafts & Live Reload** - Use `--drafts` and `--livereload` to speed up authoring

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain to a friend why a static site is faster and safer than a dynamic one
- [ ] Scaffold a new Jekyll site and serve it without looking up the commands
- [ ] Point to the `_site` folder and say exactly what lives there and why

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Basic command line navigation (`cd`, `ls`, `mkdir`)
- [ ] Comfort creating and editing plain text files
- [ ] Recommended: completion of [Git Basics](/quests/0000/git-basics/)

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Ruby 3.x installed (we install it below)
- [ ] A text editor or IDE (VS Code recommended)
- [ ] Internet connection for downloading gems

### 🧠 Skill Level Indicators
This **🟢 Easy** quest expects:
- [ ] Beginner-friendly - no prior Jekyll or Ruby experience required
- [ ] Comfortable running commands you copy into a terminal
- [ ] Ready for 75-90 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*Jekyll needs Ruby and a couple of build tools. Pick the path that matches your machine.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install a modern Ruby with Homebrew (the system Ruby is too old)
brew install ruby

# Add the Homebrew Ruby to your PATH (zsh)
echo 'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Install Jekyll and Bundler
gem install jekyll bundler

# Verify
ruby --version
jekyll --version
```

**macOS-Specific Notes:**
- On Apple Silicon Homebrew lives in `/opt/homebrew`; on Intel Macs it is `/usr/local`.
- Never `sudo gem install` - it pollutes the system Ruby.

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install RubyInstaller with DevKit via winget
winget install RubyInstallerTeam.RubyWithDevKit.3.2

# Close and reopen the terminal, then install the toolchain when prompted
ridk install

# Install Jekyll and Bundler
gem install jekyll bundler

# Verify
ruby --version
jekyll --version
```

**Windows-Specific Notes:**
- Choose option 3 during `ridk install` to build native gems.
- WSL2 with Ubuntu is an excellent alternative - follow the Linux path inside it.

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install -y ruby-full build-essential zlib1g-dev

# Fedora / RHEL
# sudo dnf install -y ruby ruby-devel @development-tools

# Install gems to your home directory (no sudo)
echo 'export GEM_HOME="$HOME/.gems"' >> ~/.bashrc
echo 'export PATH="$HOME/.gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

gem install jekyll bundler
jekyll --version
```

**Linux-Specific Notes:**
- Installing gems to `$GEM_HOME` in your home directory avoids needing `sudo`.
- `build-essential` (or the dev tools group) is required to compile native gems.

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Run Jekyll in a container - zero local Ruby setup
docker run --rm -it -p 4000:4000 -v "$PWD":/srv/jekyll \
  jekyll/jekyll:4 jekyll serve --host 0.0.0.0

# Or use a GitHub Codespace, which ships Ruby preinstalled
```

**Cloud-Specific Notes:**
- The container mounts your current directory, so edits on your host appear instantly.
- `--host 0.0.0.0` is required so the forwarded port reaches your browser.

</details>

## 🧙‍♂️ Chapter 1: The Static Site Generator - What Jekyll Actually Does

*Before you build, understand the machine. A **static site generator** takes source files - Markdown, HTML templates, data, and config - and renders them once into a folder of plain HTML, CSS, and JS. That folder is your website. No database runs at request time; the server just hands over files.*

### ⚔️ Skills You'll Forge in This Chapter
- The difference between dynamic and static sites
- The Jekyll input-to-output pipeline
- Your first scaffolded site

### 🏗️ Build Your First Site

```bash
# Scaffold a brand-new Jekyll site
jekyll new my-castle

# Enter the new site and serve it locally
cd my-castle
bundle exec jekyll serve

# Jekyll prints something like:
#   Server address: http://127.0.0.1:4000/
#   Server running... press ctrl-c to stop.
```

Open `http://127.0.0.1:4000/` in your browser. You are looking at HTML that Jekyll generated from Markdown and templates. Press `Ctrl-C` to stop the server.

**Dynamic vs. static, at a glance:**

| | Dynamic site (e.g. WordPress) | Static site (Jekyll) |
| --- | --- | --- |
| When is the page built? | On every request | Once, ahead of time |
| Needs a database? | Yes | No |
| Attack surface | Large (DB, PHP, plugins) | Tiny (just files) |
| Hosting cost | Server + DB | Free file host (GitHub Pages) |
| Speed | Variable | Very fast |

### 🔍 Knowledge Check: Static Generation
- [ ] In your own words, when does a Jekyll page get built?
- [ ] Why does a static site have a smaller attack surface?
- [ ] What did `jekyll new` create that `jekyll serve` then rendered?

### ⚡ Quick Wins and Checkpoints
- [ ] **Setup Complete**: `jekyll --version` prints a version
- [ ] **First Success**: You viewed your scaffolded site at `localhost:4000`

## 🧙‍♂️ Chapter 2: The Directory Structure - A Map of Your Castle

*Every Jekyll site follows a layout of special folders. The leading underscore marks folders Jekyll treats specially.*

### ⚔️ Skills You'll Forge in This Chapter
- What each special folder and file is for
- The role of the `_site` output folder
- How `_config.yml` ties it together

### 🏗️ The Anatomy of a Jekyll Site

```text
my-castle/
├── _config.yml      # Global settings: title, baseurl, plugins, build options
├── Gemfile          # The Ruby gems this site depends on
├── index.md         # The home page (Markdown becomes HTML)
├── _posts/          # Blog posts, named YYYY-MM-DD-title.md
├── _layouts/        # Page skeletons (default.html, post.html)
├── _includes/       # Reusable HTML snippets (header.html, footer.html)
├── _data/           # YAML/JSON/CSV data files you can read in templates
├── assets/          # CSS, JS, images - copied through as-is
└── _site/           # GENERATED OUTPUT - never edit, never commit
```

The golden rule: **you edit the source, never `_site`.** Jekyll wipes and rebuilds `_site` on every run. Add it to `.gitignore`:

```bash
echo "_site/" >> .gitignore
echo ".jekyll-cache/" >> .gitignore
```

Here is what a minimal `_config.yml` looks like:

```yaml
title: My Castle
description: A site forged in the Web Fundamentals tier
baseurl: ""          # subpath, e.g. "/blog"
url: ""              # full host, e.g. "https://example.com"
markdown: kramdown
plugins:
  - jekyll-feed
```

### 🔍 Knowledge Check: Directory Structure
- [ ] Which folder holds the generated website you would deploy?
- [ ] Why should you never edit files inside `_site`?
- [ ] What naming pattern must files in `_posts/` follow?

### ⚡ Quick Wins and Checkpoints
- [ ] **Mapped the castle**: You can name what `_layouts`, `_includes`, and `_data` hold
- [ ] **Ignored the output**: `_site/` is in your `.gitignore`

## 🧙‍♂️ Chapter 3: Collections & the Build Loop - Bringing It to Life

*Posts are just the beginning. **Collections** let you group any kind of related content - quests, recipes, team members - and Jekyll will render each item with shared logic.*

### ⚔️ Skills You'll Forge in This Chapter
- Declaring and using a custom collection
- Adding content with front matter
- The full build-and-serve workflow

### 🏗️ Declare a Collection

Add a collection in `_config.yml`:

```yaml
collections:
  recipes:
    output: true          # generate a page for each recipe
    permalink: /recipes/:name/
```

Now create the folder and a first item:

```bash
mkdir _recipes
```

Create `_recipes/bread.md`. The block between the `---` lines is **front matter** - metadata that controls rendering:

```markdown
---
title: Hearth Bread
layout: default
prep_time: 20 minutes
---

A simple loaf forged in the castle hearth. Mix flour, water, salt, and yeast.
```

Now run the build and watch the loop:

```bash
# Build once into _site/, with verbose output
bundle exec jekyll build --verbose

# Or serve with live reload so the browser refreshes on every save
bundle exec jekyll serve --livereload --drafts
```

Visit `http://127.0.0.1:4000/recipes/bread/` - Jekyll generated that page from your Markdown plus the `default` layout. The `--drafts` flag also renders anything in a `_drafts/` folder so you can preview unfinished work.

### 🔍 Knowledge Check: Collections & Build
- [ ] What does `output: true` do for a collection?
- [ ] What is front matter, and where does it live in a file?
- [ ] What is the difference between `jekyll build` and `jekyll serve`?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Scaffold and Serve
**Objective**: Create a fresh Jekyll site and view it in your browser.

**Requirements**:
- [ ] Run `jekyll new my-site`
- [ ] Serve it with `bundle exec jekyll serve`
- [ ] Confirm it loads at `http://127.0.0.1:4000/`

**Validation**: Run `bundle exec jekyll build` and confirm a `_site/index.html` file exists.

### 🟡 Intermediate Challenge: Add a Custom Collection
**Objective**: Add a `recipes` (or `quests`) collection with at least two items.

**Requirements**:
- [ ] Declare the collection in `_config.yml`
- [ ] Create two Markdown files with front matter
- [ ] Confirm each renders at its own permalink

**Validation**: Both collection pages appear under `_site/` and open in the browser.

### 🔴 Advanced Challenge: Tame the Build
**Objective**: Configure a reproducible build and a custom home page.

**Requirements**:
- [ ] Pin Jekyll in the `Gemfile` and commit `Gemfile.lock`
- [ ] Edit `index.md` to list your collection items
- [ ] Add `_site/` and `.jekyll-cache/` to `.gitignore`

**Validation**: `bundle exec jekyll build` succeeds with no warnings and your home page lists the collection.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Site Smith** - You built a static site from nothing
- 🌱 **Sprout of the Static Web** - The build-and-serve loop is second nature

**🛠️ Skills Unlocked**:
- **Jekyll Project Scaffolding** - Stand up a new site in seconds
- **Static Site Generation Concepts** - Reason about source-to-output pipelines

**🔓 Unlocked Quests**:
- GitHub Pages Basics - Put your site online for free
- Liquid Templating - Make your pages dynamic at build time
- YAML Configuration - Master the config and data files

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [GitHub Pages Basics](/quests/0001/github-pages-basics/) - Host your Jekyll site for free

**Explore Side Adventures**:
- ⚔️ [Liquid Templating](/quests/0001/liquid-templating/) - The templating language Jekyll speaks
- ⚔️ [YAML Configuration](/quests/0001/yaml-configuration/) - Configure sites and store data

### Character Class Recommendations

**💻 Software Developer**: Continue to [GitHub Pages Basics](/quests/0001/github-pages-basics/)  
**🏗️ System Engineer**: Explore [YAML Configuration](/quests/0001/yaml-configuration/)  
**🎨 Frontend Specialist**: Advance to [Liquid Templating](/quests/0001/liquid-templating/)

## 📚 Resources

### Official Documentation
- [Jekyll Documentation](https://jekyllrb.com/docs/) - The canonical guide
- [Jekyll Step-by-Step Tutorial](https://jekyllrb.com/docs/step-by-step/01-setup/) - Build a site one concept at a time
- [Jekyll Collections](https://jekyllrb.com/docs/collections/) - Grouping related content

### Community Resources
- [Jekyll Talk Forum](https://talk.jekyllrb.com/) - Ask and answer questions
- [Jekyll on Stack Overflow](https://stackoverflow.com/questions/tagged/jekyll) - Tagged Q&A
- [Awesome Jekyll](https://github.com/planetjekyll/awesome-jekyll) - Curated themes and plugins

### Learning Materials
- [Ruby Installation Guide](https://www.ruby-lang.org/en/documentation/installation/) - Get Ruby on any OS
- [Bundler: The Gemfile](https://bundler.io/guides/gemfile.html) - Reproducible dependencies

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Built and served a Jekyll site locally
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0001 - Web Fundamentals]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Unlocks:** [[GitHub Pages Basics]] · [[Liquid Templating]] · [[YAML Configuration]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
