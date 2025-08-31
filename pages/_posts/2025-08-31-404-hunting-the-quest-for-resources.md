---
title: "404 Hunting: The Quest for Resources"
description: "Mystical Jekyll + GitHub Actions guide to banish 404s: stable permalinks, redirects, CI link checks, and organic resource endpoints."
date: 2025-08-31T12:00:00.000Z
preview: /images/post-preview-image.png
tags:
    - jekyll
    - tutorial
    - intermediate
    - devops
    - github-actions
categories:
    - Posts
    - DevOps
    - Tutorials
sub-title: A fantasy-themed, practical guide to links that always resolve
excerpt: Tame 404 wraiths in your Jekyll realm with permalink magic, redirect runes, automated link guardians, and living resource endpoints—all powered by GitHub CI/CD.
snippet: May your links never stray and your redirects never loop.
author: IT-Journey Team
layout: journals
keywords:
    primary:
        - jekyll-404
        - link-integrity
    secondary:
        - redirects
        - sitemap
        - link-checking
        - htmlproofer
lastmod: 2025-08-31T23:09:28.442Z
permalink: /posts/404-hunting-quest/
attachments: ""
comments: true
difficulty: 🟡 Intermediate
estimated_reading_time: 25-35 minutes
prerequisites:
    - Basic familiarity with Jekyll and front matter
    - A GitHub repository with GitHub Actions enabled
    - Local dev via Ruby/Bundler or Docker (optional but recommended)
learning_outcomes:
    - 🎯 Design a robust permalink strategy that avoids dead ends
    - ⚡ Add redirects that preserve SEO and muscle memory
    - 🛠️ Automate link checking in CI to catch regressions early
    - 🔗 Grow missing resources organically from your 404 page and build logs
content_series: Site Reliability for Static Sites
related_posts:
    - 2025-03-19-open-ai-future-features-with-github-action.md
    - 2025-08-27-vscode-front-matter-fork-development-setup.md
    - 2024-06-16-unwavering-joy-of-fetch.md
validation_methods:
    - CI link checks pass green across internal and external links
    - 404 page yields helpful suggestions and valid redirects
    - Manual crawl of navigation produces no dead links
---

## Introduction

In the twilight between build and deploy, a wraith roams the static valleys: the dreaded 404. It haunts broken trails, whispers through refactored slugs, and skulks in the shadows where old URLs once stood. Today, we don the mantle of Link Wardens and weave binary incantations to bind the 404, forging a realm where every path resolves and every seeker arrives.

This epic is both tale and toolkit—a comprehensive Jekyll tutorial powered by GitHub CI/CD. You’ll learn to craft stable permalinks, etch redirect runes, summon automated hyperlink guardians, and grow living resource endpoints so your content network strengthens with every release.

### 🌟 Why This Matters

Dead links erode trust, sink SEO, and fracture the learning journey. In a knowledge guild, continuity is kindness: stable URLs honor readers’ time, and redirects carry the torch of history forward. A resilient link architecture turns your site from a maze of pitfalls into a well-lit waystation.

### 🎯 What You’ll Learn

- Design permalink patterns that survive refactors
- Add redirects without server magic (pure Jekyll + GitHub Pages/Actions)
- Automate link checks in CI to catch regressions before release
- Empower your 404 page to suggest, route, and inspire

### 📋 Before We Begin

- A Jekyll site (this repository qualifies)
- GitHub Actions enabled in your repo
- Optional local dev: Ruby/Bundler or Docker

Tip: This repository already includes helpful workflows like `link-checker.yml` and `hyperlink-guardian.yml`. We’ll show how to use and adapt them.

---

## Step-by-Step Implementation

### 🏗️ Phase 1: Forge Unbreakable Paths (Permalinks & Sitemaps)

The first spell of stability is consistency. Give every artifact a predictable trail.

#### Step 1: Set sane permalinks
 
**Objective**: Ensure URLs remain stable and readable.

Add or confirm in `_config.yml`:

```yaml
permalink: pretty  # /path/ not /path.html
url: https://your-domain.example  # production canonical
baseurl: ""  # "/repo" for project pages; "" for root
plugins:
  - jekyll-sitemap
  - jekyll-feed
  - jekyll-redirect-from
```

Why: Pretty permalinks reduce duplication; `jekyll-sitemap` helps crawlers rediscover moved content; `jekyll-redirect-from` enables serverless redirects.

Troubleshooting:

- 404 on subpaths in project pages? Set `baseurl: "/your-repo"` and use `{{ site.baseurl }}` in links.
- Mixed trailing slashes? Standardize on trailing slashes to align with `pretty`.

#### Step 2: Establish a purposeful 404 page
 
**Objective**: Turn a dead end into a guidepost.

Your repo already has `404.html`. Enhance it with helpful trails:

```html
---
permalink: /404.html
layout: default
---
<main class="not-found">
  <h1>🧭 Lost in the Linkwood</h1>
  <p>The path you sought fades into mist. Try these routes:</p>
  <ul>
    <li><a href="{{ site.baseurl }}/">Return to camp (home)</a></li>
    <li><a href="{{ site.baseurl }}/sitemap.xml">Consult the star map (sitemap)</a></li>
  </ul>
  <h2>Recent beacons</h2>
  <ul>
    {% for post in site.posts limit:5 %}
      <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
  <script>
    // Optional: suggest a likely match if only a slug differs
    (function() {
      var q = location.pathname.toLowerCase().replace(/\/$/, '');
      var hints = document.querySelector('.hints');
      // You can embed a small client-side map or fetch /assets/redirects.json
    })();
  </script>
  <p>If you believe this is an error, please <a href="https://github.com/{{ site.github.repository_nwo }}/issues/new?title=404:%20{{ page.url }}">open a scroll (issue)</a>.</p>
  <div class="hints"></div>
  <style>.not-found{max-width:720px;margin:3rem auto;padding:0 1rem}</style>
  </main>
```

Expected Result: A friendly 404 with clear exits and recent content.

---

### 🔧 Phase 2: Tame the Wraith (Redirects & Canonicals)

Refactors happen. Preserve the old trails.

#### Step 3: Enable `jekyll-redirect-from`
 
**Objective**: Add redirects without a server.

1. In `Gemfile` (GitHub Pages supports this gem):

```ruby
gem "jekyll-redirect-from"
```

1. In `_config.yml`:

```yaml
plugins:
  - jekyll-redirect-from
```

1. On moved content, add in the new file’s front matter:

```yaml
redirect_from:
  - /old-path/
  - /2024/03/10/old-slug/
```

Or create a dedicated redirect file:

```markdown
---
layout: redirect
redirect_to: /posts/new-canonical-path/
permalink: /legacy-path/
---
```

SEO Note: Keep content canonicalized (one true URL) and use redirects sparingly but decisively.

#### Step 4: Maintain a realm-wide redirect map (optional)
 
**Objective**: Centralize migrations.

Create `_data/redirects.yml`:

```yaml
- from: /docs/guide/
  to:   /posts/guide/
- from: /faq/
  to:   /posts/faq/
```

Then generate stub redirect pages during build using a small plugin or a pre-build script (if your hosting permits custom plugins). On GitHub Pages, use data to generate pages within the normal site (no custom plugin needed) by iterating over the data in a generator page.

---

### ⚡ Phase 3: Summon Hyperlink Guardians (CI Link Checks)

Automation is your warding circle. This repository already includes link checking workflows (`.github/workflows/link-checker.yml` and `hyperlink-guardian.yml`). If you’re setting this up from scratch, use one of these patterns:

#### Option A: Lychee Link Checker (fast and generous)

```yaml
name: Hyperlink Guardian
on:
  pull_request:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 3 * * 1'  # weekly sweep
jobs:
  lychee:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run lychee
        uses: lycheeverse/lychee-action@v1
        with:
          args: >-
            --verbose --no-progress --cache --max-cache-age 1d
            --accept 200,204,206,301,302,308
            --exclude-mail
            --timeout 20
            **/*.md **/*.html
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### Option B: HTMLProofer after a build (strict and thorough)

```yaml
name: Link Checker
on: [push, pull_request]
jobs:
  htmlproofer:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
      - name: Build Jekyll
        run: |
          bundle install --path vendor/bundle
          bundle exec jekyll build --trace
      - name: HTMLProofer
        run: |
          gem install html-proofer
          htmlproofer ./_site \
            --assume-extension \
            --check-external-hash \
            --enforce-https \
            --typhoeus-config 'timeout:20' \
            --url-ignore "^https://localhost,https://127.0.0.1" \
            --http-status-ignore '0,429'
```

Tips:

- Ignore flaky hosts with `--url-ignore` or Lychee’s `--exclude` patterns.
- Schedule a weekly sweep to catch bit-rot.

---

### 🌱 Phase 4: Grow Endpoints Organically (Build What’s Missing)

When guardians report a missing path, harvest the error and plant a resource.

Playbook:
 
1. If it’s a moved article: add `redirect_from` on the new canonical.
1. If it’s a true gap: scaffold a stub page with clear TODOs and publish a minimal viable resource (MVR) to de-404 the link.
1. If it’s external: switch to the canonical source, or mirror a citation with context.

Optional Enhancement: Add a small script to parse link-check logs and open templated issues for each unique broken link. Over time, this turns 404s into a queue of content seeds.

---

## 🌍 Platform-Specific Guidance

### 🍎 macOS Implementation

```bash
# Recommended: rbenv + Bundler
brew install rbenv ruby-build
rbenv install 3.2.4
rbenv local 3.2.4
gem install bundler
bundle install
bundle exec jekyll serve --livereload
```

### 🪟 Windows (WSL) Notes

```powershell
# Use WSL2 Ubuntu and follow Linux steps
```

### 🐧 Linux Implementation

```bash
sudo apt-get update && sudo apt-get install -y ruby-full build-essential zlib1g-dev
gem install bundler
bundle install
bundle exec jekyll serve
```

### ☁️ GitHub CI/CD

- Use the provided link-check workflows on PR and schedule.
- Add a build-validation workflow to ensure Jekyll builds cleanly before merge.

---

## 💻 Technical Implementation

### 🔧 Example: A redirected post that moved

```markdown
---
title: "New Canonical Title"
date: 2025-08-01T00:00:00.000Z
redirect_from:
  - /2023/11/04/old-title/
  - /posts/old-title/
permalink: /posts/new-canonical-title/
layout: journals
---

Your updated content lives here.
```

Expected Output:

```text
Visiting /posts/old-title/ (or the old dated path) redirects to /posts/new-canonical-title/
```

Testing & Validation:

```bash
bundle exec jekyll build && npx serve _site  # quick local check
# Or rely on CI link checks after PR push
```

---

## ✅ Validation and Practice

### 🧠 Knowledge Check

- [ ] Can you explain how `pretty` permalinks influence trailing slashes?
- [ ] Can you add a `redirect_from` to a moved article?
- [ ] Can you configure Lychee or HTMLProofer to ignore a flaky host?

### 🎮 Practice Exercises

1) Create a test page, link to it, then rename the file. Add a redirect and verify CI stays green.
2) Add one CI link check on PRs and a scheduled weekly sweep. Prove it catches a seeded bad link.

---

## 🔧 Troubleshooting Guide

### 404 on project pages

Symptoms: Everything 404s after deploy to `user.github.io/repo`.
Fix: Set `baseurl: "/repo"` and use `{{ site.baseurl }}`/`relative_url` filters.

### Redirect loops

Cause: Multiple conflicting redirect rules.
Fix: Canonicalize one permalink per artifact; remove redundant redirect targets.

### External link flakes (429/timeout)

Fix: Add `--http-status-ignore '429'`, increase `timeout`, or swap to a canonical mirror.

### Case sensitivity (macOS vs Linux)

Fix: Normalize slugs to lowercase; ensure links match exactly.

---

## 🚀 Next Steps and Advanced Topics

- Add a nightly content crawl and auto-open issues for new 404s
- Build a `/links/` dashboard page sourced from CI artifacts
- Introduce content guardians: pre-commit link hooks for authors
- Expand your 404 with fuzzy search (lunr.js) and popular paths

---

## 📚 Resources and References

- Jekyll Permalinks: <https://jekyllrb.com/docs/permalinks/>
- jekyll-redirect-from: <https://github.com/jekyll/jekyll-redirect-from>
- jekyll-sitemap: <https://github.com/jekyll/jekyll-sitemap>
- HTMLProofer: <https://github.com/gjtorikian/html-proofer>
- Lychee Action: <https://github.com/lycheeverse/lychee-action>
- GitHub Pages 404s: <https://docs.github.com/pages/configuring-a-custom-404-page-for-your-github-pages-site>
- GitHub Actions: <https://docs.github.com/actions>

---

When the build runes glow and the hyperlink guardians sing, the 404 wraith fades. Keep the trails lit, redirect the old roads with honor, and let your content forest grow—alive, discoverable, and kind to every traveler.
