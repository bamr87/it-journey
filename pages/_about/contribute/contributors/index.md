---
title: Contributors
author: IT-Journey Team
excerpt: Meet the adventurers who build and maintain IT-Journey
description: A directory of all IT-Journey contributors — human and AI alike — with RPG-style character profiles, stats, and achievements.
categories:
    - about
tags:
    - contributors
    - community
    - profiles
    - gamification
permalink: /about/contributors/
lastmod: 2026-03-21T00:00:00.000Z
date: 2026-03-21T00:00:00.000Z
draft: false
---

<link rel="stylesheet" href="{{ '/assets/css/contributor-profile.css' | relative_url }}">

# 🏛️ The Guild Hall — Contributors

> *"Behind every great journey lies a fellowship of adventurers. Step inside, and meet those who forge the path."*

Welcome to the IT-Journey Contributor Guild Hall. Every contributor earns an RPG-style **Character Profile** with auto-calculated stats, achievement badges, and a class identity powered by their git history.

---

## 👥 Active Contributors

{% assign contributors = site.data.contributors %}

<div class="contributor-directory">
{% for entry in contributors %}
  {% assign username = entry[0] %}
  {% assign data = entry[1] %}
  {% if username == '_template' %}{% continue %}{% endif %}
  {% if data.profile.ai_contributor %}{% continue %}{% endif %}
  {% assign p = data.profile %}
  {% assign lvl = data.level %}

  {% if p.avatar and p.avatar != "" %}
    {% assign avatar_url = p.avatar | relative_url %}
  {% else %}
    {% assign avatar_url = "https://github.com/" | append: p.links.github | append: ".png?size=120" %}
  {% endif %}

  {% case p.class %}
    {% when 'Wizard' %}{% assign class_icon = "🧙" %}
    {% when 'Warrior' %}{% assign class_icon = "⚔️" %}
    {% when 'Ranger' %}{% assign class_icon = "🏹" %}
    {% when 'Healer' %}{% assign class_icon = "💚" %}
    {% when 'Rogue' %}{% assign class_icon = "🗡️" %}
    {% when 'Bard' %}{% assign class_icon = "🎵" %}
    {% when 'Paladin' %}{% assign class_icon = "🛡️" %}
    {% else %}{% assign class_icon = "🛡️" %}
  {% endcase %}

  {% case lvl.tier %}
    {% when 'Apprentice' %}{% assign tier_icon = "🌱" %}
    {% when 'Adventurer' %}{% assign tier_icon = "⚔️" %}
    {% when 'Warrior' %}{% assign tier_icon = "🔥" %}
    {% when 'Master' %}{% assign tier_icon = "👑" %}
    {% else %}{% assign tier_icon = "🌱" %}
  {% endcase %}

<div class="contributor-card contributor-card--{{ p.class | downcase | default: 'warrior' }}" style="margin-bottom: 1.5rem; {% if p.banner_color %}--contributor-accent: {{ p.banner_color }};{% endif %}">
  <div class="contributor-card__banner" style="height: 6px;"></div>
  <div class="contributor-card__body" style="padding: 1rem;">
    <div style="display: flex; align-items: center; gap: 1rem;">
      <div class="contributor-card__avatar-wrapper" style="flex-shrink: 0;">
        <img class="contributor-card__avatar" src="{{ avatar_url }}" alt="{{ p.display_name }}" style="width: 64px; height: 64px;">
        <span class="contributor-card__class-badge">{{ class_icon }}</span>
      </div>
      <div style="flex: 1;">
        <h3 style="margin: 0;">
          <a href="/contributors/{{ username }}/">{{ p.display_name | default: username }}</a>
        </h3>
        <p style="margin: 0.2rem 0; font-size: 0.9em; opacity: 0.8;">{{ p.title }}</p>
        <p style="margin: 0; font-size: 0.85em;">
          {{ tier_icon }} {{ lvl.tier | default: "Apprentice" }} &middot;
          Level {{ lvl.current_level | default: "0000" }} &middot;
          {{ class_icon }} {{ p.class | default: "Warrior" }}
        </p>
        <p style="margin: 0.3rem 0 0; font-size: 0.85em; opacity: 0.7;">
          💻 {{ data.stats.total_commits | default: 0 }} commits &middot;
          🔀 {{ data.stats.total_prs_merged | default: 0 }} PRs &middot;
          🏰 {{ data.stats.total_quests_authored | default: 0 }} quests &middot;
          📝 {{ data.stats.total_posts_authored | default: 0 }} posts
        </p>
      </div>
    </div>
  </div>
</div>

{% endfor %}
</div>

---

## 🤖 AI Contributors

These AI agents assist in building, reviewing, and maintaining IT-Journey content. They are honorary guild members recognized for their contributions to the platform.

{% for entry in contributors %}
  {% assign username = entry[0] %}
  {% assign data = entry[1] %}
  {% if username == '_template' %}{% continue %}{% endif %}
  {% unless data.profile.ai_contributor %}{% continue %}{% endunless %}
  {% assign p = data.profile %}

  {% if p.avatar and p.avatar != "" %}
    {% assign ai_avatar = p.avatar | relative_url %}
  {% else %}
    {% assign ai_avatar = "https://github.com/" | append: p.links.github | append: ".png?size=120" %}
  {% endif %}

  {% case p.class %}
    {% when 'Wizard' %}{% assign ai_class_icon = "🧙" %}
    {% when 'Ranger' %}{% assign ai_class_icon = "🏹" %}
    {% when 'Bard' %}{% assign ai_class_icon = "🎵" %}
    {% else %}{% assign ai_class_icon = "🤖" %}
  {% endcase %}

<div class="contributor-card contributor-card--{{ p.class | downcase | default: 'bard' }}" style="margin-bottom: 1.5rem; {% if p.banner_color %}--contributor-accent: {{ p.banner_color }};{% endif %}">
  <div class="contributor-card__banner" style="height: 6px;"></div>
  <div class="contributor-card__body" style="padding: 1rem;">
    <div style="display: flex; align-items: center; gap: 1rem;">
      <div class="contributor-card__avatar-wrapper" style="flex-shrink: 0;">
        <img class="contributor-card__avatar" src="{{ ai_avatar }}" alt="{{ p.display_name }}" style="width: 64px; height: 64px;">
        <span class="contributor-card__class-badge">{{ ai_class_icon }}</span>
      </div>
      <div style="flex: 1;">
        <h3 style="margin: 0;">
          <a href="/contributors/{{ username }}/">{{ p.display_name | default: username }}</a>
        </h3>
        <p style="margin: 0.2rem 0; font-size: 0.9em; opacity: 0.8;">{{ p.title }}</p>
        <p style="margin: 0.3rem 0 0; font-size: 0.85em;">{{ p.bio }}</p>
      </div>
    </div>
  </div>
</div>

{% endfor %}

---

## 🛠️ Join the Guild

Every contributor gets a **Character Profile** — an RPG-style character sheet with auto-calculated stats, badges, and a class identity.

### Quick Setup

1. Copy the template:
   ```bash
   cp -r pages/_about/contribute/contributors/_template \
         pages/_about/contribute/contributors/YOUR_USERNAME
   cp _data/contributors/_template.yml _data/contributors/YOUR_USERNAME.yml
   ```
2. Edit both files — replace placeholders with your info
3. Choose your **class**: Wizard, Warrior, Ranger, Rogue, Healer, Bard, or Paladin
4. Submit a PR — the CI pipeline will auto-generate your stats on merge

See the [Forge Your Character quest](/quests/forge-your-character/) for the full walkthrough.

---

**Last Updated**: 2026-03-21 | **Maintained by**: IT-Journey Team
