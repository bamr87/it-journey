---
title: 'Azure Ascension: Deploying Jekyll to the Cloud Kingdom'
description: Deploy the IT-Journey Jekyll site to Azure Static Web Apps with a clean CI/CD pipeline and safe secrets handling.
author: IT-Journey Team
date: 2025-11-17
lastmod: 2026-01-14
level: '1001'
difficulty: 🔴 Hard
estimated_time: 90-120 minutes
primary_technology: Azure Static Web Apps
quest_type: main_quest
quest_series: Cloud Deployment Quests
skill_focus:
- cloud-deployment
- ci-cd
- static-sites
- azure
learning_style: hands-on
permalink: /quests/azure-ascension-jekyll-deployment/
categories:
- Quests
- Cloud
- Azure
- Deployment
tags:
- azure
- jekyll
- static-web-apps
- ci-cd
keywords:
- azure
- jekyll
- static-web-apps
- deployment
- ci-cd
fmContentType: quest
draft: false
---
*Rise, cloud wanderer! This quest guides you through deploying the IT-Journey Jekyll site to Azure Static Web Apps, wiring up CI/CD, and verifying a clean production build.*

## 🎯 Quest Objectives

### Primary Objectives
- [ ] **Provision Azure Static Web Apps** - Create the app and link to GitHub
- [ ] **Configure Build & Deploy** - Ensure Jekyll build works in CI
- [ ] **Secure Secrets** - Store keys safely in GitHub
- [ ] **Verify Production** - Confirm the deployed site loads correctly

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Basic GitHub workflow familiarity
- [ ] Comfort with terminal commands
- [ ] Understanding of static sites

### 🛠️ System Requirements
- [ ] Azure account with permissions to create Static Web Apps
- [ ] GitHub account with repo access

## 🧙‍♂️ Chapter 1: Prepare the Repository

Ensure dependencies are installed:

```bash
bundle install
```

Verify local build:

```bash
bundle exec jekyll build
```

## ☁️ Chapter 2: Deploy with the Azure Helper Script

Use the built-in deployment script:

```bash
../../scripts/deployment/azure-jekyll-deploy.sh setup
../../scripts/deployment/azure-jekyll-deploy.sh deploy --app-name <your-app-name> --github-repo <your-repo-url>
```

Follow the prompts for Azure authentication and GitHub workflow setup.

## 🔐 Chapter 3: Secrets & Workflow Verification

1. Confirm required GitHub secrets are set.
2. Open the generated workflow in `.github/workflows/`.
3. Trigger a deploy by pushing a small change.

## ✅ Chapter 4: Validate the Deployment

- [ ] Visit the Azure-provided URL
- [ ] Confirm `/quests/` loads correctly
- [ ] Check logs for a successful build

## 🏁 Quest Completion Checklist

- [ ] Azure Static Web App created and linked
- [ ] CI/CD pipeline runs successfully
- [ ] Site is accessible in production

## 🔗 Related Quests

- [GitHub Pages Portal](0001/github-pages-portal.md)
- [Jekyll Fundamentals](0001/jekyll-fundamentals.md)
- [Link to the Future: Hyperlink Checking](1010/link-to-the-future-automated-hyperlink-checking-and-error-reporting.md)
