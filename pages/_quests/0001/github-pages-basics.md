---
title: 'GitHub Pages Basics: Host Your Jekyll Site for Free'
author: IT-Journey Team
description: 'Publish a Jekyll site to the world with GitHub Pages: repository setup, the _config.yml url and baseurl, deployment, and wiring a custom domain.'
excerpt: Take your Jekyll site live for free with GitHub Pages - repo setup, config, and custom domains.
preview: images/previews/github-pages-basics-free-hosting-quest-descriptio.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-30T00:00:00.000Z'
level: '0001'
difficulty: 🟢 Easy
estimated_time: 60-75 minutes
primary_technology: github-pages
quest_type: main_quest
quest_series: Static Site Mastery
quest_line: The Web Fundamentals Codex
quest_arc: Forging Your First Website
quest_dependencies:
  required_quests:
  - /quests/0001/jekyll-fundamentals/
  recommended_quests:
  - /quests/0000/git-basics/
  unlocks_quests:
  - /quests/0001/git-workflow-mastery/
skill_focus: frontend
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Basic Git commands (commit, push)
  - Completion of Jekyll Fundamentals
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Git installed and a free GitHub account
  skill_level_indicators:
  - Comfortable building a Jekyll site locally
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A Jekyll site published at a github.io URL
  skill_demonstrations:
  - Can configure url and baseurl correctly
  - Can deploy a site by pushing to GitHub
  knowledge_checks:
  - Understands when baseurl must be set
  - Can diagnose a 404 caused by a wrong baseurl
permalink: /quests/0001/github-pages-basics/
redirect_from:
- /quickstart/deployment/
categories:
- Quests
- Frontend
- Static-Sites
- Beginner
tags:
- '0001'
- github-pages
- jekyll
- hosting
- web-development
- main_quest
- frontend
- hands-on
- beginner
keywords:
  primary:
  - '0001'
  - github-pages
  - jekyll
  - hosting
  secondary:
  - web-development
  - main_quest
  - frontend
  - hands-on
  - beginner
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0001 (1) Quest: Main Quest - GitHub Pages'
rewards:
  badges:
  - 🏆 Herald of the Web - Published your first live website
  - 🌱 Keeper of the Domain - Configured url, baseurl, and a custom domain
  skills_unlocked:
  - 🛠️ GitHub Pages Deployment
  - 🧠 Site URL Configuration
  progression_points: 50
  unlocks_features:
  - The ability to ship every later Web Fundamentals quest to a live URL
layout: quest
---
*Greetings, brave adventurer! You forged a Jekyll site in the workshop - but a website hidden on your own machine helps no one. **GitHub Pages Basics** is the quest where your creation leaves the castle walls and joins the wider web, hosted for free and reachable from anywhere in the realm.*

*This adventure teaches you to publish a static site, configure its address correctly, and even claim a custom domain of your own. By the end, you will have a real URL you can share with the world.*

## 📖 The Legend Behind This Quest

*For ages, putting a website online meant renting a server, configuring it, securing it, and paying for it month after month. Then the great forge of GitHub opened a gate: **GitHub Pages** - free hosting for static sites, served straight from a Git repository. Push your files, and minutes later the world can visit them, complete with HTTPS, all at no cost. It is the natural home for a Jekyll site, because GitHub Pages can even build Jekyll for you.*

*Master this quest and you gain a permanent place to publish everything you build in the Web Fundamentals tier and beyond.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Repository Setup** - Create a GitHub repo and enable Pages
- [ ] **Deployment** - Publish a Jekyll site by pushing to GitHub
- [ ] **url and baseurl** - Configure `_config.yml` so every link resolves
- [ ] **Verify the Live Site** - Confirm your site at its `github.io` address

### Secondary Objectives (Bonus Achievements)
- [ ] **Custom Domain** - Point your own domain at GitHub Pages
- [ ] **HTTPS Enforcement** - Turn on enforced HTTPS for your site
- [ ] **GitHub Actions Build** - Understand how Pages can build Jekyll automatically

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain when `baseurl` must be set and when it must be empty
- [ ] Diagnose a broken-CSS page caused by a wrong `baseurl`
- [ ] Walk someone else through publishing their first site

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Basic Git: `add`, `commit`, `push`
- [ ] Completion of [Jekyll Fundamentals](/quests/0001/jekyll-fundamentals/)
- [ ] Recommended: [Git Basics](/quests/0000/git-basics/)

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Git installed and configured with your name and email
- [ ] A free GitHub account
- [ ] A working Jekyll site from the previous quest

### 🧠 Skill Level Indicators
This **🟢 Easy** quest expects:
- [ ] Beginner-friendly - basic Git is all you need
- [ ] Comfortable building a Jekyll site locally
- [ ] Ready for 60-75 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*Deployment happens on GitHub's servers, so the local commands are nearly identical everywhere. Pick your shell.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Authenticate the GitHub CLI (one-time)
brew install gh
gh auth login

# Create a repo from your existing site folder and push it
cd my-castle
git init && git add . && git commit -m "Initial site"
gh repo create my-castle --public --source=. --push
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install and authenticate the GitHub CLI
winget install GitHub.cli
gh auth login

# Initialize, commit, and push your site
cd my-castle
git init; git add .; git commit -m "Initial site"
gh repo create my-castle --public --source=. --push
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Install the GitHub CLI (Debian/Ubuntu example)
sudo apt update && sudo apt install -y gh
gh auth login

# Push your site to a new public repo
cd my-castle
git init && git add . && git commit -m "Initial site"
gh repo create my-castle --public --source=. --push
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# In a GitHub Codespace, gh is preinstalled and already authenticated.
git add . && git commit -m "Initial site"
git branch -M main
git push -u origin main
# Then enable Pages from the repo Settings UI.
```

</details>

## 🧙‍♂️ Chapter 1: The Repository - Your Site's New Home

*GitHub Pages serves a site directly from a repository. There are two flavours, and choosing correctly saves you a world of broken links later.*

### ⚔️ Skills You'll Forge in This Chapter
- The two kinds of Pages sites and how they differ
- Creating the repo and enabling Pages
- Where your site will live

### 🏗️ Two Kinds of Pages Sites

| Type | Repo name | Lives at | `baseurl` |
| --- | --- | --- | --- |
| **User/Org site** | `username.github.io` | `https://username.github.io/` | `""` (empty) |
| **Project site** | `any-name` | `https://username.github.io/any-name/` | `"/any-name"` |

This distinction matters because it determines your `baseurl` in Chapter 2.

**Enable Pages** after pushing your repo. Either use the web UI (Settings -> Pages -> Source: *Deploy from a branch* -> `main` / `/ (root)`) or the CLI:

```bash
# Enable Pages from the main branch, root folder
gh api -X POST repos/:owner/my-castle/pages \
  -f "source[branch]=main" -f "source[path]=/"
```

GitHub will build your Jekyll site and publish it within a minute or two.

### 🔍 Knowledge Check: The Repository
- [ ] What repo name gives you a site at the root `username.github.io`?
- [ ] Where does a project site named `blog` get published?
- [ ] What does "Deploy from a branch" mean?

### ⚡ Quick Wins and Checkpoints
- [ ] **Repo created**: Your site is pushed to GitHub
- [ ] **Pages enabled**: The Settings -> Pages panel shows a build in progress

## 🧙‍♂️ Chapter 2: url and baseurl - The Address Spell

*The single most common Pages bug is a site where the HTML loads but all the CSS and links are broken. The cause is almost always a mismatched `baseurl`. Learn this and you have learned the hard part.*

### ⚔️ Skills You'll Forge in This Chapter
- What `url` and `baseurl` mean
- Setting them for user vs. project sites
- Why links break and how to fix them

### 🏗️ Configure the Address

In `_config.yml`:

```yaml
# For a PROJECT site published at username.github.io/my-castle/
url: "https://username.github.io"   # the protocol + host, no trailing slash
baseurl: "/my-castle"               # the subpath, with a leading slash

# For a USER site published at username.github.io/
# url: "https://username.github.io"
# baseurl: ""                       # empty - the site is at the root
```

The rule: **`baseurl` is the subpath your site sits under.** A project site lives under `/my-castle/`, so links must include that prefix. Use the `relative_url` filter in templates so links respect `baseurl` automatically:

```liquid
<!-- Correct: respects baseurl on both user and project sites -->
<link rel="stylesheet" href="{% raw %}{{ '/assets/css/style.css' | relative_url }}{% endraw %}">
<a href="{% raw %}{{ '/about/' | relative_url }}{% endraw %}">About</a>

<!-- Wrong: hard-coded path breaks on project sites -->
<link rel="stylesheet" href="/assets/css/style.css">
```

Test the exact production configuration locally before pushing:

```bash
# Serve as GitHub Pages will, honoring baseurl
bundle exec jekyll serve --baseurl "/my-castle"
# Visit http://127.0.0.1:4000/my-castle/
```

### 🔍 Knowledge Check: Addressing
- [ ] If your site loads but CSS is missing, what should you check first?
- [ ] What `baseurl` does a user site (`username.github.io`) need?
- [ ] Why is `relative_url` safer than hard-coding `/assets/...`?

## 🧙‍♂️ Chapter 3: Custom Domains & HTTPS - Claiming Your Banner

*A `github.io` address works, but a domain of your own - `mysite.dev` - is a banner worth raising. GitHub Pages supports custom domains with free, automatic HTTPS.*

### ⚔️ Skills You'll Forge in This Chapter
- Pointing a domain at GitHub Pages with DNS
- The CNAME file
- Enforcing HTTPS

### 🏗️ Wire Up a Custom Domain

Add a `CNAME` file (no extension) to your site source containing only your domain:

```text
www.mysite.dev
```

Then configure DNS at your registrar. For a `www` subdomain, add a CNAME record:

```text
Type    Name    Value
CNAME   www     username.github.io
```

For the apex domain (`mysite.dev` with no `www`), add A records to GitHub's IPs instead:

```text
Type    Name    Value
A       @       185.199.108.153
A       @       185.199.109.153
A       @       185.199.110.153
A       @       185.199.111.153
```

In **Settings -> Pages**, enter the custom domain, wait for the DNS check to pass, then tick **Enforce HTTPS**. GitHub provisions a free TLS certificate automatically.

> ⚠️ DNS changes can take minutes to hours to propagate. If the domain check fails, wait and retry rather than reconfiguring.

### 🔍 Knowledge Check: Domains
- [ ] What file must your repo contain for a custom domain to stick?
- [ ] Which record type points a `www` subdomain at GitHub Pages?
- [ ] What does "Enforce HTTPS" give you, and what provides the certificate?

## 🧙‍♂️ Chapter 4: Beyond GitHub Pages - Other Realms & the Production Build

*GitHub Pages is the gentlest gate to the web, but it is not the only one. Sometimes you want a different host, or you simply have the finished `_site/` and want to drop it anywhere. The secret is that Jekyll's output is just plain static files - any host that serves files can serve your site.*

### ⚔️ Skills You'll Forge in This Chapter
- Building a production site by hand
- Shipping that build to any static host
- Guarding production-only behavior with `JEKYLL_ENV`

### 🏗️ The Production Build Incantation

Build the optimized site yourself, then upload the resulting `_site/` folder anywhere:

```bash
# Build the production site - JEKYLL_ENV unlocks production-only behavior
JEKYLL_ENV=production bundle exec jekyll build

# Everything the browser needs is now in _site/ - upload its contents to your host
```

The `JEKYLL_ENV` variable lets templates behave differently in production - for example, only loading analytics on the live site:

```liquid
{% raw %}{% if jekyll.environment == "production" %}
  {% include analytics.html %}
{% endif %}{% endraw %}
```

### 🌐 Hosts That Serve a `_site/` Folder

Any of these realms will happily host the same static output:

| Host | How to deploy | Notes |
| --- | --- | --- |
| **Netlify** | Git push or drag-and-drop | Auto-builds from your repo |
| **Vercel** | Git push | Auto-builds from your repo |
| **Cloudflare Pages** | Git push | Auto-builds from your repo |
| **AWS S3 + CloudFront** | `aws s3 sync _site/ s3://bucket/` | Upload then serve via CDN |
| **Any web server** | FTP/SCP upload | Copy `_site/` contents into the docroot |

> 🔮 For a heavier-duty deployment with managed CI/CD on Microsoft's cloud, see the [Azure Ascension](/quests/1000/azure-ascension-jekyll-deployment/) quest - it scripts the whole Azure Static Web Apps setup.

### 🔍 Knowledge Check: The Production Build
- [ ] What command produces an optimized, deployable `_site/` folder?
- [ ] What does `JEKYLL_ENV=production` change about the build?
- [ ] Name two hosts besides GitHub Pages that can serve your `_site/` output.

### 🧾 Pre-Launch Checklist

Before you summon your site to a live URL, walk this final checklist:

- [ ] Site builds without errors locally
- [ ] `_config.yml` has the correct `url` and `baseurl`
- [ ] `CNAME` file present (only if using a custom domain)
- [ ] DNS records configured and propagated
- [ ] HTTPS enforced
- [ ] Images optimized
- [ ] No draft content published by accident
- [ ] `robots.txt` and `sitemap.xml` generated

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Go Live
**Objective**: Publish your Jekyll site to a `github.io` URL.

**Requirements**:
- [ ] Push your site to a public GitHub repo
- [ ] Enable Pages from the `main` branch
- [ ] Confirm the published URL loads

**Validation**: Visiting your `github.io` URL shows your home page with working styles.

### 🟡 Intermediate Challenge: Fix the baseurl
**Objective**: Deploy as a project site with a correct `baseurl`.

**Requirements**:
- [ ] Set `url` and `baseurl` for a project site in `_config.yml`
- [ ] Replace any hard-coded paths with `relative_url`
- [ ] Verify locally with `--baseurl`

**Validation**: CSS and internal links work at `username.github.io/repo-name/`.

### 🔴 Advanced Challenge: Custom Domain with HTTPS
**Objective**: Serve your site from a domain you control with enforced HTTPS.

**Requirements**:
- [ ] Add a `CNAME` file and configure DNS records
- [ ] Pass the GitHub Pages domain verification
- [ ] Enable Enforce HTTPS

**Validation**: `https://yourdomain` loads the site with a valid certificate.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Herald of the Web** - Your first site is live for the world
- 🌱 **Keeper of the Domain** - You command url, baseurl, and DNS

**🛠️ Skills Unlocked**:
- **GitHub Pages Deployment** - Ship a site by pushing to Git
- **Site URL Configuration** - Never ship a broken-link site again

**🔓 Unlocked Quests**:
- Git Workflow Mastery - Collaborate and ship changes cleanly
- Liquid Templating - Make those pages dynamic at build time

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Git Workflow Mastery](/quests/0001/git-workflow-mastery/) - Branch, review, and merge like a pro

**Explore Side Adventures**:
- ⚔️ [Liquid Templating](/quests/0001/liquid-templating/) - Power up your templates
- ⚔️ [YAML Configuration](/quests/0001/yaml-configuration/) - Master `_config.yml`

### Character Class Recommendations

**💻 Software Developer**: Continue to [Git Workflow Mastery](/quests/0001/git-workflow-mastery/)  
**🏗️ System Engineer**: Explore [YAML Configuration](/quests/0001/yaml-configuration/)  
**🎨 Frontend Specialist**: Advance to [Liquid Templating](/quests/0001/liquid-templating/)

## 📚 Resources

### Official Documentation
- [GitHub Pages Documentation](https://docs.github.com/en/pages) - The canonical guide
- [Configuring a Custom Domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site) - DNS and CNAME setup
- [Jekyll on GitHub Pages](https://jekyllrb.com/docs/github-pages/) - How the two fit together

### Community Resources
- [GitHub Community Discussions](https://github.com/orgs/community/discussions) - Ask questions
- [GitHub Pages on Stack Overflow](https://stackoverflow.com/questions/tagged/github-pages) - Tagged Q&A
- [Let's Encrypt](https://letsencrypt.org/) - How free HTTPS certificates work

### Learning Materials
- [Understanding GitHub Actions](https://docs.github.com/en/actions/learn-github-actions) - The newer build path for Pages
- [DNS Records Explained (Cloudflare)](https://www.cloudflare.com/learning/dns/dns-records/) - A, CNAME, and friends

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Published a Jekyll site to GitHub Pages
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0001 - Web Fundamentals]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Jekyll Fundamentals]]
**Unlocks:** [[Git Workflow Mastery]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
