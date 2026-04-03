---
title: "Deployment to GitHub Pages and Azure"
author: bamr87
description: Deploy your Jekyll site to GitHub Pages, Azure Static Web Apps, or any static hosting provider — with custom domain configuration.
excerpt: "Deploy your Jekyll site to GitHub Pages, Azure Static Web Apps, or a custom hosting provider, with optional custom domain configuration."
permalink: /quickstart/deployment/
categories:
  - quickstart
slug: deployment
lastmod: 2026-04-02T03:14:50.958Z
draft: false
date: 2026-04-01T00:00:00.000Z
difficulty: 🟡 Medium
estimatedTime: 20-30 minutes
prerequisites:
  - Site builds locally (see [Local Development](/quickstart/local-development/))
  - GitHub repository set up (see [GitHub Setup](/quickstart/github/))
tags:
  - deployment
  - github-pages
  - azure
  - hosting
keywords:
  primary:
    - jekyll deployment
    - github pages
    - azure static web apps
  secondary:
    - custom domain
    - CNAME
    - static hosting
sidebar:
  nav: quickstart
---

This guide covers **Phase 12** of the [Quick Start](/quickstart/) — deploying your Jekyll site to GitHub Pages, Azure, or any static hosting provider.

---

## GitHub Pages (Free — Recommended for Starters)

GitHub Pages is the simplest way to host a Jekyll site. It's free, automatic, and tightly integrated with your repository.

### Setup Steps

1. Push your repo to GitHub
2. Go to **Settings → Pages**
3. Set source to **GitHub Actions** (recommended) or the `gh-pages` branch
4. Your site will be live at `https://username.github.io/repo-name/`

### Custom Domain

To use your own domain:

**Step 1 — Configure Jekyll:**

```yaml
# In _config.yml
url: "https://yourdomain.com"
baseurl: ""
```

**Step 2 — Create CNAME file:**

Create a `CNAME` file at the repo root containing your domain:

```
yourdomain.com
```

**Step 3 — Configure DNS:**

Add these records with your domain registrar:

| Type | Name | Value |
|------|------|-------|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `username.github.io` |

**Step 4 — Enable HTTPS:**

In **Settings → Pages**, check **Enforce HTTPS** (available after DNS propagates).

---

## Azure Static Web Apps

For more control, use Azure Static Web Apps with the IT-Journey deployment script:

```bash
./scripts/azure-jekyll-deploy.sh deploy \
  --app-name my-jekyll-site \
  --github-repo https://github.com/username/repo
```

### Azure Configuration

| Setting | Value |
|---------|-------|
| App location | `/` |
| API location | `api/` |
| Output location | `_site/` |

The script handles:
- Azure resource creation
- GitHub Actions workflow generation
- Secret configuration
- Domain setup

### Script Subcommands

```bash
# Full deployment
./scripts/azure-jekyll-deploy.sh deploy --app-name <name> --github-repo <url>

# Setup only (configure without deploying)
./scripts/azure-jekyll-deploy.sh setup

# Clean up resources
./scripts/azure-jekyll-deploy.sh cleanup --force
```

---

## Manual Build + Any Host

Build the site and upload the output to any static hosting provider:

```bash
# Build the production site
JEKYLL_ENV=production bundle exec jekyll build

# The _site/ folder contains all static files
# Upload _site/ contents to your host
```

### Compatible Hosts

| Host | Method | Notes |
|------|--------|-------|
| **Netlify** | Git push or drag-and-drop | Auto-builds from repo |
| **Vercel** | Git push | Auto-builds from repo |
| **Cloudflare Pages** | Git push | Auto-builds from repo |
| **AWS S3 + CloudFront** | CLI upload | `aws s3 sync _site/ s3://bucket/` |
| **Any web server** | FTP/SCP upload | Upload `_site/` contents to docroot |

---

## Environment-Specific Builds

| Environment | Build Command | Config |
|-------------|---------------|--------|
| Development | `bundle exec jekyll serve --config _config.yml,_config_dev.yml` | Local theme, drafts visible |
| Production | `JEKYLL_ENV=production bundle exec jekyll build` | Remote theme, minified, no drafts |
| Docker | `docker-compose up -d` | Uses both configs automatically |

The `JEKYLL_ENV` variable controls environment-specific behavior:

```liquid
{% raw %}{% if jekyll.environment == "production" %}
  {% include analytics.html %}
{% endif %}{% endraw %}
```

---

## Deployment Checklist

- [ ] Site builds without errors locally
- [ ] `_config.yml` has correct `url` and `baseurl`
- [ ] `CNAME` file present (for custom domains)
- [ ] DNS records configured and propagated
- [ ] HTTPS enforced
- [ ] All images optimized
- [ ] No draft posts published accidentally
- [ ] `robots.txt` and `sitemap.xml` generated

---

## What's Next

| Next Step | Guide |
|-----------|-------|
| Set up CI/CD for automated deployment | [CI/CD & Automation](/quickstart/cicd-automation/) |
| Optimize for SEO, performance, and accessibility | [Optimization & Maintenance](/quickstart/optimization-maintenance/) |

> **IT-Journey Quests:** [GitHub Pages Basics](/quests/frontend/github-pages-basics/) · [Azure Ascension](/quests/azure-ascension-jekyll-deployment-quest/) · [CI/CD Fundamentals](/quests/cicd/cicd-fundamentals/)
>
> **External Docs:** [GitHub Pages Docs](https://docs.github.com/en/pages) · [Azure Static Web Apps](https://learn.microsoft.com/en-us/azure/static-web-apps/) · [Jekyll Deployment](https://jekyllrb.com/docs/deployment/)
