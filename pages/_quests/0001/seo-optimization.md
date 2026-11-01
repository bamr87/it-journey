---
title: 'SEO & AI-Citability: Meta Tags, Structured Data & E-E-A-T'
author: IT-Journey Team
description: 'Master technical SEO and AI-citability for Jekyll: meta tags, sitemaps, JSON-LD structured data, E-E-A-T author signals, and a score-fix-rescore loop that makes any website AI-citable.'
excerpt: Make your Jekyll site discoverable with meta tags, sitemaps, structured data, and jekyll-seo-tag.
preview: /images/previews/seo-optimization-search-engine-visibility-descript.webp
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-11-01T00:00:00.000Z'
level: '0001'
difficulty: 🟡 Medium
estimated_time: 90-120 minutes
primary_technology: jekyll
quest_type: main_quest
quest_series: Jekyll Mastery
quest_line: The Web Fundamentals Codex
quest_arc: Publishing Your First Website
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/0001/advanced-markdown/
  unlocks_quests:
  - /quests/0001/analytics-integration/
  - /quests/0001/jekyll-plugins/
skill_focus: frontend
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Basic command line navigation
  - Familiarity with HTML and YAML frontmatter
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - A Jekyll site (or any static HTML site) to edit
  skill_level_indicators:
  - Some exposure to Jekyll or static sites is helpful
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A page with proper title, description, and structured data
  skill_demonstrations:
  - Can write effective title and meta description tags
  - Can generate a sitemap and configure jekyll-seo-tag
  knowledge_checks:
  - Understands the role of meta tags and structured data
  - Can explain what a sitemap and robots.txt do
permalink: /quests/0001/seo-optimization/
categories:
- Quests
- Frontend
- SEO
- Beginner
tags:
- '0001'
- jekyll
- seo
- main_quest
- frontend
- hands-on
- beginner
keywords:
  primary:
  - '0001'
  - jekyll
  - seo
  - ai-citability
  - json-ld
  secondary:
  - e-e-a-t
  - aieo
  - main_quest
  - frontend
  - hands-on
  - beginner
fmContentType: quest
draft: false
comments: true
mermaid: true
sub_title: 'Level 0001 (1) Quest: Main Quest - SEO'
rewards:
  badges:
  - 🏆 Beacon Keeper - Made a site search engines can find and understand
  - 🌱 Sprout of Discoverability - Internalized meta tags and structured data
  skills_unlocked:
  - 🛠️ Technical SEO for Static Sites
  - 🧠 Structured Data & Metadata
  progression_points: 50
  unlocks_features:
  - Access to the measurement quests of Level 0001 Web Fundamentals
layout: quest
redirect_from:
- /quests/0011/seo-optimization/
- /quickstart/optimization-maintenance/
environment:
  os:
  - macos
  - windows
  - linux
  - cloud
  shell:
  - zsh
  - bash
  - powershell
  variables:
    project_dir: my-site
---
*Greetings, brave adventurer! Welcome to **SEO Optimization** - the quest where you light a beacon so the search engines of the realm can find your work. You can forge the most beautiful site in the kingdom, but if no crawler can read it and no result links to it, it stands silent in the fog. Search Engine Optimization is the craft of making your pages discoverable, understandable, and shareable.*

*Whether you are publishing a portfolio, a blog, or documentation, this adventure will teach you the technical foundations - titles, descriptions, sitemaps, structured data, and the `jekyll-seo-tag` plugin - that help your pages rank and appear correctly when shared.*

## 📖 The Legend Behind This Quest

*Search engines send out tireless **crawlers** that read pages, follow links, and build an index of the web. When someone searches, the engine ranks pages from that index. For years people chased tricks, but the durable truth emerged: write good content and make it easy for machines to read. That means a clear `<title>`, a compelling meta description, a **sitemap** listing your pages, a `robots.txt` granting access, and **structured data** that spells out, in a format machines parse, exactly what a page is about. Get these right and your work surfaces where people are looking.*

*This quest teaches the technical SEO that static-site authors control, and how Jekyll plugins automate most of it.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Titles & Meta Descriptions** - Write the snippets that appear in search results
- [ ] **Meta & Open Graph Tags** - Control how pages look in search and social shares
- [ ] **Sitemaps & robots.txt** - Tell crawlers what to read and where to find it
- [ ] **Jekyll-seo-tag** - Automate metadata generation across a whole site

### Secondary Objectives (Bonus Achievements)
- [ ] **Structured Data** - Add JSON-LD so engines understand your content type
- [ ] **Canonical URLs** - Prevent duplicate-content confusion
- [ ] **Search Console** - Verify your site and watch how it is indexed
- [ ] **Performance & Accessibility** - Audit Core Web Vitals and WCAG basics that lift rank
- [ ] **AI-Citability** - Apply JSON-LD, E-E-A-T, and entity density, then score before and after

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Write a title and description that earn a click
- [ ] Explain what a sitemap and robots.txt each do
- [ ] Add JSON-LD structured data for an article
- [ ] Publish a before/after AI-citability delta for a real page

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Familiarity with HTML and YAML frontmatter
- [ ] Basic command line navigation (`cd`, `ls`)
- [ ] Recommended: completion of [Advanced Markdown](/quests/0001/advanced-markdown/)

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] A Jekyll site (or any static site) to edit
- [ ] A text editor or IDE (VS Code recommended)
- [ ] Internet connection for verification tools

### 🧠 Skill Level Indicators
This **🟢 Easy** quest expects:
- [ ] Beginner-friendly - some exposure to Jekyll helps but is not required
- [ ] Willingness to inspect a page's `<head>` in DevTools
- [ ] Ready for 45-60 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*SEO lives in your site's HTML and config. You will edit files and check the output. Pick your setup.*

### 🍎 macOS Kingdom Path

<details markdown="1">
<summary>Click to expand macOS instructions</summary>

```bash
# In an existing Jekyll site, add the SEO and sitemap plugins
cd ~/my-site
bundle add jekyll-seo-tag jekyll-sitemap
# `bundle add` only edits the Gemfile — Jekyll won't load the plugins until you
# also add them to the `plugins:` list in _config.yml (see Chapter 2). Without
# that step, /sitemap.xml is never generated.
bundle exec jekyll serve

# View the generated metadata
open http://127.0.0.1:4000/
```

**macOS-Specific Notes:**
- Open DevTools (`Cmd + Option + I`) and inspect the `<head>` to see generated tags.
- Visit `/sitemap.xml` and `/robots.txt` once the plugins are active.

</details>

### 🪟 Windows Empire Path

<details markdown="1">
<summary>Click to expand Windows instructions</summary>

```powershell
# In an existing Jekyll site, add the SEO and sitemap plugins
cd $HOME\my-site
bundle add jekyll-seo-tag jekyll-sitemap
# `bundle add` only edits the Gemfile — Jekyll won't load the plugins until you
# also add them to the `plugins:` list in _config.yml (see Chapter 2). Without
# that step, /sitemap.xml is never generated.
bundle exec jekyll serve

Start-Process http://127.0.0.1:4000/
```

**Windows-Specific Notes:**
- View source (`Ctrl + U`) to confirm the `<meta>` and `<title>` tags are present.
- Browse to `/sitemap.xml` to see every page the crawler will discover.

</details>

### 🐧 Linux Territory Path

<details markdown="1">
<summary>Click to expand Linux instructions</summary>

```bash
# In an existing Jekyll site, add the SEO and sitemap plugins
cd ~/my-site
bundle add jekyll-seo-tag jekyll-sitemap
# `bundle add` only edits the Gemfile — Jekyll won't load the plugins until you
# also add them to the `plugins:` list in _config.yml (see Chapter 2). Without
# that step, /sitemap.xml is never generated.
bundle exec jekyll serve
xdg-open http://127.0.0.1:4000/
```

**Linux-Specific Notes:**
- `curl -s http://127.0.0.1:4000/sitemap.xml | head` shows the generated sitemap.
- `curl -s http://127.0.0.1:4000/ | grep -i '<meta'` lists your meta tags.

</details>

### ☁️ Cloud Realms Path

<details markdown="1">
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# No local Jekyll? Edit on GitHub and let GitHub Pages build the site.
# GitHub Pages whitelists jekyll-seo-tag and jekyll-sitemap by default.
# Add them to _config.yml plugins and push; Pages builds with SEO enabled.
```

**Cloud-Specific Notes:**
- Use Google's Rich Results Test and the Facebook Sharing Debugger on the live URL.
- GitHub Pages includes both SEO plugins, so no extra build setup is required.

</details>

## 🧙‍♂️ Chapter 1: Titles, Descriptions & Meta Tags - The Search Snippet

*The blue link and gray summary you see in search results come straight from your page's `<title>` and meta description. These also drive how a link looks when shared on social media.*

### ⚔️ Skills You'll Forge in This Chapter
- Writing effective titles and descriptions
- The essential `<head>` meta tags
- Open Graph tags for social sharing

### 🏗️ The Tags That Matter

A search snippet is built from two tags in your `<head>`:

```html
<head>
  <!-- The clickable blue headline; aim for ~50-60 characters -->
  <title>SEO for Jekyll Sites: A Practical Beginner Guide</title>

  <!-- The gray summary under it; aim for ~150-160 characters -->
  <meta
    name="description"
    content="Learn the technical SEO every Jekyll author needs: meta tags, sitemaps, structured data, and the jekyll-seo-tag plugin."
  />

  <!-- Tells search engines which URL is the master copy of this page -->
  <link rel="canonical" href="https://example.com/seo-guide/" />
</head>
```

For **social sharing**, Open Graph tags control the preview card on platforms like LinkedIn and Slack:

```html
<meta property="og:title" content="SEO for Jekyll Sites" />
<meta property="og:description" content="A practical beginner guide." />
<meta property="og:image" content="https://example.com/preview.png" />
<meta property="og:type" content="article" />
```

Good titles are specific and front-load the keyword; good descriptions read like a one-sentence pitch, not a keyword stuffing. The description is not a ranking factor by itself, but it heavily influences whether someone clicks.

### 🔍 Knowledge Check: Titles & Meta
- [ ] What two tags form the snippet shown in search results?
- [ ] What does a canonical URL prevent?
- [ ] Which tags control how a link looks when shared on social media?

### ⚡ Quick Wins and Checkpoints
- [ ] **Wrote a title**: A concise, keyword-forward `<title>` is set
- [ ] **Wrote a description**: A compelling ~155-character description is set

## 🧙‍♂️ Chapter 2: Sitemaps, robots.txt & Jekyll-seo-tag - Helping the Crawler

*Crawlers need a map and a key. A **sitemap** lists your URLs; **robots.txt** grants or restricts access. And `jekyll-seo-tag` generates most of Chapter 1's tags for every page automatically.*

### ⚔️ Skills You'll Forge in This Chapter
- Generating a sitemap with a plugin
- Writing a sensible robots.txt
- Wiring up Jekyll-seo-tag site-wide

### 🏗️ Automating Metadata

Enable the plugins in `_config.yml`. These are on GitHub Pages' allowlist, so they work even without local builds:

```yaml
# _config.yml
title: My Quest Site
description: A static site forged in the Web Fundamentals tier
url: https://example.com   # full host, no trailing slash
author:
  name: Your Name
  twitter: yourhandle

plugins:
  - jekyll-seo-tag
  - jekyll-sitemap
  - jekyll-feed      # generates /feed.xml so readers and aggregators can subscribe
```

These three plugins forge your site's discoverability assets automatically - each is on GitHub Pages' allowlist:

| Plugin | Generates | Where |
|---|---|---|
| `jekyll-seo-tag` | Meta, Open Graph & JSON-LD tags | `<head>` of every page |
| `jekyll-sitemap` | XML sitemap | `/sitemap.xml` |
| `jekyll-feed` | RSS feed | `/feed.xml` |

Then place a single tag in your layout's `<head>`. It reads your `_config.yml` and each page's frontmatter and emits the title, description, canonical link, Open Graph, and JSON-LD all at once:


```liquid
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  {% raw %}{% seo %}{% endraw %}
</head>
```


`jekyll-sitemap` automatically generates `/sitemap.xml` - no work beyond adding the plugin. Add a `robots.txt` at your site root to point crawlers to it:

```text
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

`User-agent: *` addresses all crawlers; `Allow: /` permits the whole site; the `Sitemap:` line tells them where the map lives.

### 🔍 Knowledge Check: Sitemaps & Plugins
- [ ] What does the `{% raw %}{% seo %}{% endraw %}` tag generate?
- [ ] What is the purpose of a sitemap versus robots.txt?
- [ ] Why are these two plugins safe to use on GitHub Pages?

### ⚡ Quick Wins and Checkpoints
- [ ] **Sitemap live**: `/sitemap.xml` lists your pages
- [ ] **SEO tag working**: Page source shows generated meta tags

## 🧙‍♂️ Chapter 3: Structured Data & Verification - Speaking the Machine's Language

*Beyond plain meta tags, **structured data** (JSON-LD using schema.org vocabulary) tells engines precisely what a page is - an article, a recipe, a product - which can earn rich results.*

### ⚔️ Skills You'll Forge in This Chapter
- Adding JSON-LD structured data
- Validating it with Google's tools
- Verifying ownership in Search Console

### 🏗️ JSON-LD for an Article

`jekyll-seo-tag` emits basic JSON-LD for you, but you can add richer data by dropping a script into your page's head:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "SEO for Jekyll Sites",
  "description": "A practical beginner guide to technical SEO.",
  "author": { "@type": "Person", "name": "Your Name" },
  "datePublished": "2026-06-14",
  "image": "https://example.com/preview.png"
}
</script>
```

The `@type` tells the engine this is an `Article`; the fields map to schema.org's vocabulary. Search engines can use this to show a richer result with an author, date, and image.

To confirm everything works:
- Paste the live URL into Google's **Rich Results Test** to validate your structured data.
- Add the site to **Google Search Console**, verify ownership (a meta tag or DNS record), and submit your sitemap so Google indexes you faster.

### 🔍 Knowledge Check: Structured Data
- [ ] What format and vocabulary does structured data use here?
- [ ] What does the `@type` field communicate to a search engine?
- [ ] Which tool validates structured data, and which monitors indexing?

## 🧙‍♂️ Chapter 4: Performance & Accessibility - Signals That Lift the Rank

*Discoverability is only half the beacon. Search engines now weigh how **fast** a page loads (Core Web Vitals) and how **usable** it is. A slow or inaccessible page is demoted in results - and turns away the visitors your tags worked to attract. These signals are ranking factors and good craft at once.*

### ⚔️ Skills You'll Forge in This Chapter
- Trimming page weight for Core Web Vitals
- Auditing with Lighthouse
- Meeting baseline accessibility standards

### 🏗️ Make Pages Fast

Heavy images are the most common drag on a static site. Resize and compress them before they ship:

```bash
# Resize to a sane max width (macOS built-in)
sips --resampleWidth 1200 assets/images/large-photo.jpg

# Or compress in place across a folder with ImageOptim CLI
brew install imageoptim-cli
imageoptim assets/images/
```

Then tighten the rest of the page:

- [ ] **Lazy-load below-the-fold images** with `loading="lazy"`
- [ ] **Build for production** so Jekyll minifies output: `JEKYLL_ENV=production`
- [ ] **Ship only the JavaScript you need** - every extra script blocks render
- [ ] **Serve static assets from a CDN** when self-hosting
- [ ] **Audit with Lighthouse** - Chrome DevTools → Lighthouse tab - and chase the score up

### 🏗️ Make Pages Accessible

Accessible pages rank better, read better in screen readers, and are simply correct. Run this checklist over a page:

- [ ] Every image has descriptive `alt` text
- [ ] Text meets WCAG AA contrast (4.5:1 ratio)
- [ ] Interactive elements are keyboard-navigable with visible focus
- [ ] Heading hierarchy is logical (h1 → h2 → h3, no skips)
- [ ] Links use descriptive text, never "click here"
- [ ] The page sets a language attribute: `<html lang="en">`

Verify with a dedicated checker beyond Lighthouse:

| Tool | Type | Where |
|---|---|---|
| **Lighthouse** | Browser built-in | Chrome DevTools |
| **axe DevTools** | Browser extension | [deque.com/axe](https://www.deque.com/axe/) |
| **WAVE** | Online checker | [wave.webaim.org](https://wave.webaim.org/) |
| **Pa11y** | CLI | `npm install -g pa11y` |

### 🔍 Knowledge Check: Performance & Accessibility
- [ ] Which build environment makes Jekyll minify its output?
- [ ] What contrast ratio does WCAG AA require for body text?
- [ ] Name one tool that audits both performance and accessibility.

### ⚡ Quick Wins and Checkpoints
- [ ] **Lighthouse run**: You have a baseline score for a key page
- [ ] **Alt text pass**: Every image on one page has descriptive `alt` text

## 🧙‍♂️ Chapter 5: Making Any Website AI-Citable - The Oracle's Trifecta

*Search crawlers rank your page; AI assistants **quote** it. When an assistant answers a question, it reaches for sources it can parse, attribute, and trust. This chapter teaches that craft as a trifecta: the **Information** (what to put on the page), the **Process** (a repeatable score-fix-rescore loop), and the **Knowledge** (the patterns underneath, with real bamr87 sites as specimens).*

> **Source:** this chapter adapts the six-section outline of the lifehacker.dev article *"How to Make Any Website AI-Citable"*, backlog entry **POST-129** in [`_data/backlog.yml`](https://github.com/bamr87/lifehacker.dev/blob/main/_data/backlog.yml), added in [bamr87/lifehacker.dev#798](https://github.com/bamr87/lifehacker.dev/pull/798). The finished article will live on [lifehacker.dev](https://lifehacker.dev/).

### ⚔️ Skills You'll Forge in This Chapter
- Explain why an AI assistant cites one page and skips (or misquotes) another
- Apply the three pillars: JSON-LD structured data, E-E-A-T signals, and entity density
- Run a before/after citability audit and publish the delta

### 🔮 Part I - Information: The Six Scrolls

#### 1. The Hook: Why Assistants Cite Bad Sources (Exercise)

*This is a research exercise, not a recounted incident.* Ask two or three AI assistants a niche question in a field you know well, and record which sources they cite. You will often find a thin forum post or a scraped copy cited over the authoritative page. Write down, for each cited source, what made it easy to quote: a clear question-and-answer shape, a named author, machine-readable metadata, or simply being the only page that stated the fact plainly. Assistants cite what they can **parse, attribute, and match to the question** — not necessarily what is most correct. Your job is to make the correct page also the easiest to cite.

#### 2. The Three Pillars

| Pillar | What it means | How a machine sees it |
|---|---|---|
| **Structured data (JSON-LD)** | A `<script type="application/ld+json">` block describing the page as a schema.org entity (`Article`, `FAQPage`, `BreadcrumbList`, `Person`) | Unambiguous type, author, date, and Q&A pairs without guessing from layout |
| **E-E-A-T signals** | Experience, Expertise, Authoritativeness, Trust: a visible author bio, credentials, outbound citations, dates | A named, linkable `Person` behind the claims, and sources a model can cross-check |
| **Entity density** | Naming the specific things (tools, versions, organisations, files) the page is about, consistently | Clear subject entities to match a question against, instead of vague pronouns |

#### 3. Worked Example: zer0-mistakes, Section by Section

The [zer0-mistakes](https://github.com/bamr87/zer0-mistakes) Jekyll theme (which also powers this site) ships each pillar as an include. Read them in order:

| Include | Pillar | What it actually does |
|---|---|---|
| [`_includes/content/seo.html`](https://github.com/bamr87/zer0-mistakes/blob/main/_includes/content/seo.html) | Foundation | Supplements `jekyll-seo-tag` (which emits title, Open Graph, canonical and the base JSON-LD) with `og:image` path normalisation and non-Google verification tags — it deliberately avoids duplicating what the plugin already outputs |
| [`_includes/components/author-eeat.html`](https://github.com/bamr87/zer0-mistakes/blob/main/_includes/components/author-eeat.html) | E-E-A-T | Renders a **visible** author credibility block from `_data/authors.yml` (banner or card style); no person is hard-coded into the theme |
| [`_includes/content/jsonld-faq.html`](https://github.com/bamr87/zer0-mistakes/blob/main/_includes/content/jsonld-faq.html) | Structured data | Emits `FAQPage` JSON-LD only when a page defines `faq_items` in its front matter |
| [`_includes/content/jsonld-software.html`](https://github.com/bamr87/zer0-mistakes/blob/main/_includes/content/jsonld-software.html) | Structured data | `SoftwareApplication` + `WebPage` schema describing *the theme itself* — **opt-in only** (`jsonld_software_application: true`), because on a consumer site it would falsely claim that site is a Ruby gem |
| [`_includes/navigation/breadcrumbs.html`](https://github.com/bamr87/zer0-mistakes/blob/main/_includes/navigation/breadcrumbs.html) | Structured data | A visible breadcrumb trail marked up as `BreadcrumbList` microdata |

To enable the FAQ schema on a page, add front matter like this; the include turns it into `FAQPage` JSON-LD:

```yaml
faq_items:
  - question: "What makes a page AI-citable?"
    answer: "Machine-readable structured data, a named and credible author, and specific, consistently named entities."
  - question: "Does JSON-LD have to match the visible page?"
    answer: "Yes. Schema that describes content the reader cannot see is an anti-pattern."
```

The rendered output looks like this (trimmed):

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What makes a page AI-citable?",
      "acceptedAnswer": { "@type": "Answer", "text": "Machine-readable structured data, a named and credible author, and specific, consistently named entities." }
    }
  ]
}
```

#### 4. Anti-Patterns (Curses to Avoid)

- **Thin content** — a page that restates the question without facts, steps, or sources gives a model nothing worth quoting.
- **Missing author info** — no byline, no bio, no `Person` entity: the claim has no one standing behind it.
- **Schema not matching the page** — JSON-LD describing FAQs, ratings, or products the reader cannot see. zer0-mistakes' opt-in gate on `jsonld-software.html` exists precisely to stop this curse.

#### 5. The Checklist (Apply Today)

- [ ] Every page has a unique title, a 120–160 character description, and a canonical URL
- [ ] One JSON-LD block whose `@type` matches what the page really is
- [ ] A visible author byline linked to a bio page, mirrored as a `Person` entity
- [ ] Q&A content marked up as `FAQPage`, and only where the Q&A is visible
- [ ] Breadcrumbs marked up as `BreadcrumbList`
- [ ] Claims link to primary sources; pages show a published and updated date
- [ ] Key entities (tools, versions, files) named explicitly and consistently
- [ ] `robots.txt` does not block the crawlers you want to be cited by

#### 6. The Close: AIEO

**AIEO** (AI Engine Optimization) is the tool intended to automate this loop — scoring pages for citability and proposing refactors. At the time of writing there is **no AIEO tool in the [bamr87/bamr87 hub](https://github.com/bamr87/bamr87)** `tools/` directory (and no `bamr87/aieo` repository); the term currently appears in zer0-mistakes, where `author-eeat.html` is documented as an AIEO/E-E-A-T component. Link the tool here once it ships; until then, run the process below by hand.

### 🛠️ Part II - Process: Score, Fix, Rescore, Publish the Delta

```mermaid
flowchart LR
  A[Pick 3-5 pages] --> B[Score baseline]
  B --> C[Fix one pillar at a time]
  C --> D[Rescore]
  D --> E[Publish the delta]
  E --> A
```

1. **Pick** three to five representative pages (a home page, an article, a how-to).
2. **Score the baseline** with AIEO when available, or the manual rubric: one point per checklist item above (0–8).
3. **Fix one pillar at a time** so you can attribute the change (structured data, then author signals, then entity density).
4. **Rescore** and validate the JSON-LD with the [Schema Markup Validator](https://validator.schema.org/) or Google's Rich Results Test.
5. **Publish the delta** — a short before/after table in the PR or a changelog post, so the improvement is itself citable evidence.

A quick, tool-free baseline you can run against any live page:

```bash
# Count JSON-LD blocks and list the schema types a page declares
URL="https://it-journey.dev/"
curl -sL "$URL" | grep -c 'application/ld+json'
curl -sL "$URL" | grep -oE '"@type": ?"[A-Za-z]+"' | sort -u
# Check crawl-control files
for f in robots.txt llms.txt; do
  printf '%s %s\n' "$f" "$(curl -s -o /dev/null -w '%{http_code}' -L "${URL%/}/$f")"
done
```

### 📚 Part III - Knowledge: Specimens from the bamr87 Realm

These observations were checked against each repository and its live site on 2026-11-01. Describe what is real; note what is missing.

| Site / repo | What it demonstrates | What it lacks |
|---|---|---|
| [zer0-mistakes](https://github.com/bamr87/zer0-mistakes) · [zer0-mistakes.com](https://zer0-mistakes.com/) | Live JSON-LD for `WebSite`, `Organization`, `Person`, plus the opted-in `SoftwareApplication`/`WebPage`/`Offer`; `_data/authors.yml`; `robots.txt`; the includes above | No `llms.txt` |
| [lifehacker.dev](https://github.com/bamr87/lifehacker.dev) · [lifehacker.dev](https://lifehacker.dev/) | Home page JSON-LD (`WebSite`, `Organization`, `Person`); `_data/authors.yml` with per-author pages under `pages/_about/authors/` (strong E-E-A-T); `AGENTS.md`; `robots.txt`. Home of POST-129 | No `llms.txt` |
| [it-journey](https://github.com/bamr87/it-journey) · [it-journey.dev](https://it-journey.dev/) | Inherits the theme's JSON-LD (`WebSite`, `Organization`, `Person`); `robots.txt`; `AGENTS.md` | No `llms.txt` |
| [fredgar-ai](https://github.com/bamr87/fredgar-ai) | The **consumer** side: `src/enrichment/providers/webdiscovery.py` reads `ld+json` from company web pages (fixtures under `tests/enrichment/fixtures/`) — proof that machines really do harvest this markup; `AGENTS.md` | Its Pages site serves no JSON-LD and no `llms.txt` |
| [law-ai](https://github.com/bamr87/law-ai) | `AGENTS.md` (agent-readable repo instructions) | Pages site has no JSON-LD, `robots.txt`, or `llms.txt` |
| [gitorio](https://github.com/bamr87/gitorio) | `AGENTS.md`; JSON Schemas for its own data model (not schema.org) | Pages site has no JSON-LD, `robots.txt`, or `llms.txt` |
| [ragio-ai](https://github.com/bamr87/ragio-ai) | `AGENTS.md` | No live Pages site found; no JSON-LD |

**Patterns to remember:**
- `AGENTS.md` makes a *repository* legible to coding agents; JSON-LD and author pages make a *website* legible to answer engines. They are different audiences.
- `llms.txt` is an emerging convention for a curated, model-friendly site index. None of the specimens ship one yet — an easy first win.
- Schema must describe the page it sits on. Theme-level schema needs an opt-in gate, as zer0-mistakes does.

### 🔍 Knowledge Check: AI-Citability
- [ ] Can you name the three pillars and give one concrete markup for each?
- [ ] Why does `jsonld-software.html` render only on opt-in?
- [ ] What would you put in a before/after delta table for a PR?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: A Perfect Snippet
**Objective**: Give one page an optimized title and description.

**Requirements**:
- [ ] A `<title>` of roughly 50-60 characters
- [ ] A meta description of roughly 150-160 characters
- [ ] A canonical URL

**Validation**: View source and confirm all three tags render correctly.

### 🟡 Intermediate Challenge: Crawlable Site
**Objective**: Make a whole site crawlable and self-describing.

**Requirements**:
- [ ] Enable `jekyll-seo-tag` and `jekyll-sitemap`
- [ ] Add the `{% raw %}{% seo %}{% endraw %}` tag to your layout
- [ ] Add a `robots.txt` pointing at your sitemap

**Validation**: `/sitemap.xml` and `/robots.txt` both load and the head shows generated tags.

### 🔴 Advanced Challenge: Rich Results
**Objective**: Add and validate structured data.

**Requirements**:
- [ ] Add JSON-LD `Article` data to a page
- [ ] Validate it with Google's Rich Results Test
- [ ] Verify the site in Search Console and submit the sitemap

**Validation**: The Rich Results Test reports no errors for your structured data.

### 🟡 Bonus Challenge: Audit Speed & Access
**Objective**: Prove a page is fast and accessible.

**Requirements**:
- [ ] Run Lighthouse on a key page and record the Performance and Accessibility scores
- [ ] Add `alt` text to every image and `loading="lazy"` below the fold
- [ ] Fix the highest-impact issue Lighthouse or axe DevTools reports

**Validation**: A re-run of Lighthouse shows the score improve after your fix.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Beacon Keeper** - You made a site search engines can find and understand
- 🌱 **Sprout of Discoverability** - Meta tags and structured data are second nature

**🛠️ Skills Unlocked**:
- **Technical SEO for Static Sites** - Titles, sitemaps, and crawl control
- **Structured Data & Metadata** - Help machines understand your content

**🔓 Unlocked Quests**:
- Analytics Integration - Measure the traffic your SEO earns
- Jekyll Plugins - Automate more of your site's metadata

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Analytics Integration](/quests/0001/analytics-integration/) - Measure the visitors SEO brings

**Explore Side Adventures**:
- ⚔️ [Jekyll Plugins](/quests/0001/jekyll-plugins/) - The plugins that power SEO automation
- ⚔️ [Advanced Markdown](/quests/0001/advanced-markdown/) - Author the content you optimize

### Character Class Recommendations

**💻 Software Developer**: Continue to [Jekyll Plugins](/quests/0001/jekyll-plugins/)  
**🏗️ System Engineer**: Explore [Analytics Integration](/quests/0001/analytics-integration/)  
**🎨 Frontend Specialist**: Advance to [Analytics Integration](/quests/0001/analytics-integration/)  

## 📚 Resources

### Official Documentation
- [Google Search Central: SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) - The canonical guidance
- [Jekyll-seo-tag](https://github.com/jekyll/jekyll-seo-tag) - The metadata plugin
- [Jekyll-sitemap](https://github.com/jekyll/jekyll-sitemap) - Automatic sitemap generation

### Community Resources
- [schema.org](https://schema.org/) - The structured-data vocabulary
- [Google Rich Results Test](https://search.google.com/test/rich-results) - Validate JSON-LD
- [Open Graph protocol](https://ogp.me/) - The social-sharing meta standard

### Learning Materials
- [Google Search Console](https://search.google.com/search-console/about) - Monitor indexing and performance
- [Moz Beginner's Guide to SEO](https://moz.com/beginners-guide-to-seo) - A thorough primer

### AI-Citability
- [lifehacker.dev POST-129 backlog entry (PR #798)](https://github.com/bamr87/lifehacker.dev/pull/798) - Source outline for Chapter 5
- [zer0-mistakes](https://github.com/bamr87/zer0-mistakes) - Theme with FAQ, author E-E-A-T, and breadcrumb schema includes
- [bamr87/bamr87 hub](https://github.com/bamr87/bamr87) - Fleet hub (AIEO tool not yet published)
- [Schema Markup Validator](https://validator.schema.org/) - Validate any schema.org markup

### Performance & Accessibility
- [Google Lighthouse](https://developer.chrome.com/docs/lighthouse/) - Audit performance, accessibility, and SEO
- [WCAG Guidelines](https://www.w3.org/WAI/standards-guidelines/wcag/) - The accessibility standard
- [axe DevTools](https://www.deque.com/axe/) - In-browser accessibility checker

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Optimized a page's title, description, and structured data
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0001 - Web Fundamentals]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Unlocks:** [[Analytics Integration]] · [[Jekyll Plugins]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
