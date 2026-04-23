---
title: "AI-Assisted UI/UX Refactoring: Nanobar Modularization and Footer Fix"
description: "A chronicle of using AI-powered development to refactor a Jekyll theme's inline progress bar into a config-driven component and fix a full-width footer layout, from diagnosis through implementation and visual verification."
date: 2026-04-19T16:00:00.000Z
preview: ""
tags:
    - jekyll
    - tutorial
    - intermediate
    - web-development
    - ui-ux
    - refactoring
    - bootstrap
    - ai-development
categories:
    - Posts
    - Web-Development
    - Tutorials
sub-title: "From inline spaghetti to config-driven components in one AI session"
excerpt: "How an AI-assisted refactoring session turned 60 lines of hardcoded nanobar into a single configurable include—and fixed a Bootstrap footer layout along the way."
snippet: "Config-driven components beat hardcoded markup every time."
author: "IT-Journey Team"
layout: article
keywords:
    primary:
        - jekyll-theme-refactoring
        - config-driven-components
    secondary:
        - nanobar-progress-bar
        - bootstrap-footer-layout
        - liquid-templates
        - ai-assisted-development
        - css-scoping
lastmod: 2026-04-19T16:00:00.000Z
permalink: /posts/ai-assisted-nanobar-footer-refactoring/
attachments: ""
comments: true
difficulty: "🟡 Intermediate"
estimated_reading_time: "12-15 minutes"
prerequisites:
    - "Basic understanding of Jekyll templates and Liquid syntax"
    - "Familiarity with Bootstrap 5 grid system and utility classes"
    - "Experience with browser DevTools for layout debugging"
learning_outcomes:
    - "🎯 Refactor inline code into modular, config-driven Jekyll includes"
    - "⚡ Diagnose and fix Bootstrap container nesting issues"
    - "🛠️ Use CSS custom properties to bridge _config.yml values to stylesheets"
    - "🔗 Understand how AI agents diagnose UI bugs through systematic elimination"
content_series: "Zer0-Mistakes Theme Development"
related_posts:
    - "/posts/2025/11/20/using-crush-vscode-github-pages/"
validation_methods:
    - "Build the Jekyll site and verify nanobar renders at the configured position"
    - "Inspect footer in browser DevTools to confirm edge-to-edge dark background"
    - "Toggle nanobar.enabled in _config.yml and verify the bar appears/disappears"
section: Web Development
---

## Introduction

During a routine code review of the [Zer0-Mistakes Jekyll theme](https://github.com/bamr87/zer0-mistakes), we discovered that the page-loading progress bar (nanobar) was implemented as ~60 lines of hardcoded HTML, CSS, and JavaScript inlined directly in `head.html`. Values like colors, heights, and animation steps were scattered across three files with no central configuration.

At the same time, a screenshot revealed that the footer's dark section wasn't reaching the viewport edges—it was constrained by nested Bootstrap `.container` classes that had accumulated over multiple PRs.

This article chronicles how both issues were diagnosed and fixed in a single AI-assisted development session.

### 🌟 Why This Matters

Component modularization and config-driven design are foundational practices for maintainable theme development. This session demonstrates:

- **How to identify refactoring candidates** — inline code with magic numbers is a code smell
- **How to design config-driven components** — using `_config.yml` as a single source of truth
- **How to diagnose CSS layout bugs** — systematic elimination via DevTools and git history
- **How AI agents approach UI debugging** — screenshot analysis, DOM inspection, git archaeology

### 🎯 What You'll Learn

- Refactor inline HTML/CSS/JS into a modular Jekyll include
- Bridge `_config.yml` values to CSS custom properties via Liquid
- Diagnose nested Bootstrap container issues
- Verify changes with Docker-based Jekyll builds

### 📋 Before We Begin

**Prerequisites:**
- Jekyll 3.9+ or 4.x with a working Docker development environment
- Bootstrap 5.x integrated in your theme
- Basic Liquid template knowledge

---

## Phase 1: Diagnosing the Nanobar Problem

### 🔍 The Existing State

The nanobar was spread across three files:

| File | What it contained |
|------|-------------------|
| `head.html` | ~60 lines: inline `<style>`, inline `<script>`, hardcoded config |
| `header.html` | Hardcoded `<div class="nanobar" id="top-progress-bar">` inside the navbar |
| `nanobar.min.js` | Third-party library (with a stray `P` character prepended) |

**Problems identified:**

1. **No central configuration** — changing the bar color required editing HTML
2. **Tight coupling** — CSS, JS, and markup scattered across unrelated files
3. **Parse error** — a stray `P` character in `nanobar.min.js` caused a silent JS failure
4. **No positional flexibility** — the bar was hardcoded inside the navbar div

### 💡 The Design Decision

We chose a **config-driven single-include** pattern:

```
_config.yml (values) → nanobar.html (CSS + JS + bridge) → rendered page
```

One file owns the entire subsystem. All behavior is controlled by `site.nanobar.*` keys.

---

## Phase 2: Implementing the Nanobar Refactoring

### 🏗️ Step 1: Create the Config Block

```yaml
# _config.yml
nanobar:
  enabled       : true
  color         : "var(--bs-primary)"
  background    : "transparent"
  height        : "3px"
  position      : "navbar"        # top | bottom | navbar
  z_index       : 9999
  steps         : [20, 55, 85, 100]
  step_delay_ms : 180
  classname     : "nanobar"
  id            : "top-progress-bar"
  target        : ""
```

Every value that was previously hardcoded now lives here.

### 🔧 Step 2: Build the Include

`_includes/components/nanobar.html` contains three sections:

**CSS custom properties** — map config → CSS variables:
```liquid
<style id="nanobar-theme">
  :root {
    --nanobar-color: {{ site.nanobar.color | default: "var(--bs-primary)" }};
    --nanobar-bg:    {{ site.nanobar.background | default: "transparent" }};
    --nanobar-height:{{ site.nanobar.height | default: "3px" }};
    --nanobar-z:     {{ site.nanobar.z_index | default: 9999 }};
  }
</style>
```

**Config bridge** — pass values to JS:
```html
<script>
  window.zer0Nanobar = {
    position: "{{ site.nanobar.position | default: 'top' }}",
    steps: {{ site.nanobar.steps | default: "[20,55,85,100]" }},
    stepDelay: {{ site.nanobar.step_delay_ms | default: 0 }},
    classname: "{{ site.nanobar.classname | default: 'nanobar' }}",
    id: "{{ site.nanobar.id | default: 'top-progress-bar' }}",
    target: "{{ site.nanobar.target }}"
  };
</script>
```

**JS loading** — library + initializer:
```html
<script defer src="/assets/js/nanobar.min.js"></script>
<script defer src="/assets/js/nanobar-init.js"></script>
```

### ⚡ Step 3: Create the Initializer

`assets/js/nanobar-init.js` reads `window.zer0Nanobar` and:
1. Determines the mount target based on `position`
2. Instantiates `new Nanobar(opts)`
3. Runs the step animation on `DOMContentLoaded`

### 🎯 Step 4: Update the Mount Point

In `header.html`, removed the old hardcoded bar and added a conditional mount:

```liquid
{%- if site.nanobar.enabled != false and _nb_pos == "navbar" -%}
<div id="top-progress-target" class="nanobar-mount" aria-hidden="true"></div>
{%- endif -%}
```

### ✅ Step 5: Clean Up head.html

Replaced ~60 lines with one line:
```liquid
{% raw %}{% include components/nanobar.html %}{% endraw %}
```

---

## Phase 3: Diagnosing the Footer Problem

### 🔍 How the Issue Was Found

After completing the nanobar refactoring, a visual check revealed the footer's dark section had visible gaps on both sides—the dark background didn't reach the viewport edges.

### 🕵️ Root Cause Analysis

The AI agent used systematic elimination:

1. **Git archaeology** — `git log --oneline -5 -- _includes/core/footer.html` confirmed the file wasn't modified by the nanobar changes
2. **CSS audit** — searched nanobar styles for any selectors that could affect footer elements (none found)
3. **DOM inspection** — identified the real cause: four levels of width-constraining containers:

```html
<footer class="bd-footer container-xl border-top">      <!-- Level 1: max-width -->
  <div class="container row my-3">                       <!-- Level 2: max-width -->
    <div class="container bg-dark text-light rounded-3"> <!-- Level 3: max-width -->
      <div class="container">                            <!-- Level 4: max-width -->
```

Each Bootstrap `.container` class adds `max-width` + `auto` margins, preventing edge-to-edge rendering.

---

## Phase 4: Fixing the Footer

### The Fix

```html
<footer class="bd-footer border-top">            <!-- No container class -->
  <div class="container-xl my-3">                 <!-- Powered-by row, centered -->
    <!-- powered-by content -->
  </div>
  <div class="bg-dark text-light py-5">           <!-- Full-width dark bg -->
    <div class="container-xl">                    <!-- Content centered inside -->
      <!-- branding, links, social, subscribe -->
    </div>
  </div>
</footer>
```

**Key changes:**
- Removed `container-xl` from `<footer>` — the footer element now spans full viewport width
- Dark section uses `bg-dark` at full width with `container-xl` inside for content centering
- Reduced nesting from 4 levels to 2
- Removed `rounded-3` — edges should be flush, not rounded

---

## ✅ Validation

### Build Verification

```bash
docker-compose exec -T jekyll bundle exec jekyll build \
  --config '_config.yml,_config_dev.yml'
```

### Automated Checks

```bash
# Nanobar include present
grep -c 'nanobar-init.js' _site/index.html   # → 1

# Mount point renders
grep 'top-progress-target' _site/index.html  # → div.nanobar-mount

# Footer structure correct
grep '<footer' _site/index.html              # → class="bd-footer border-top"
```

### Visual Verification

Screenshots confirmed:
- Nanobar renders as a thin blue strip under the navbar
- Footer dark section extends edge-to-edge
- No CSS side-effects on other components

---

## 🧠 Key Takeaways

1. **Config-driven beats hardcoded** — a 22-line YAML block replaced 60+ lines of scattered HTML/CSS/JS
2. **CSS custom properties bridge config to styles** — Liquid injects values at build time, CSS consumes them at render time
3. **Nested Bootstrap containers compound width constraints** — each `.container` adds its own `max-width`
4. **Git archaeology is a debugging tool** — `git log -- <file>` and `git diff` help isolate when a bug was introduced
5. **AI agents debug systematically** — screenshot → DOM inspection → git history → CSS audit → targeted fix

---

## 🚀 Next Steps

### 📚 Further Learning
- [Bootstrap 5 Container docs](https://getbootstrap.com/docs/5.3/layout/containers/) — understand `container` vs `container-fluid` vs `container-xl`
- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties) — bridging config to styles
- [Jekyll Includes](https://jekyllrb.com/docs/includes/) — modular template composition

### 🎯 Apply It Yourself
- **Beginner**: Find an inline `<style>` block in your Jekyll theme and extract it into a separate include
- **Intermediate**: Create a config-driven component where all values come from `_config.yml`
- **Advanced**: Build a component with multiple position modes (like the nanobar's `top`/`bottom`/`navbar`)
