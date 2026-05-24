---
title: 🎒 Inventory & Progress Vault
layout: default
description: Personal dashboard for tracking quest completion, XP, badges, and earned achievements across the IT-Journey realms.
preview: /images/previews/inventory-learner-collection-tracker.png
permalink: /quests/inventory/
lastmod: '2026-05-23T00:00:00.000Z'
draft: false
date: '2025-11-29T16:46:02.000Z'
sidebar:
  nav: quests
---
<link rel="stylesheet" href="{{ '/assets/css/quest-system.css' | relative_url }}">

# 🎒 Inventory & Progress Vault

*Welcome to your personal vault, brave adventurer. Every quest you complete, every objective you check off, and every badge you earn is recorded here — locally in your browser, ready for you to export to your portfolio whenever you wish.*

## Overall Progress

{% include quest/tier-progress-bar.html label="Total quests completed" %}

## Tier Progress

<div class="quest-hub__tiers">
  {% for tier_name in site.data.quests.order %}{% endfor %}
  {% assign tier_keys = "Apprentice|Adventurer|Warrior|Master" | split: "|" %}
  {% for tname in tier_keys %}
    {% assign tier = site.data.quests.tiers[tname] %}
    <div class="quest-hub__tier-card quest-hub__tier-card--{{ tname | downcase }}">
      <h3>{{ tier.emoji }} {{ tname }} Tier</h3>
      {% include quest/tier-progress-bar.html tier=tname label=tname %}
      <ul>
        {% for lvl in tier.levels %}
          <li><a href="{{ '/quests/' | append: lvl | append: '/' | relative_url }}">Lv {{ lvl }}</a></li>
        {% endfor %}
      </ul>
    </div>
  {% endfor %}
</div>

## Manage Your Progress

Your quest progress is stored locally in your browser. Use the buttons below to back it up or move it between devices.

<div class="quest-progress__actions" style="margin: 1rem 0;">
  <button type="button" class="quest-progress__toggle" onclick="window.QuestProgress.exportProgress()">
    💾 Export progress as JSON
  </button>
  <label class="quest-progress__toggle" for="quest-import">
    📂 Import progress…
    <input type="file" id="quest-import" accept="application/json" hidden onchange="(function(e){var f=e.target.files[0];if(!f)return;var r=new FileReader();r.onload=function(){if(window.QuestProgress.importProgress(r.result)){alert('Progress imported.');location.reload();}};r.readAsText(f);})(event)">
  </label>
  <button type="button" class="quest-progress__reset" onclick="window.QuestProgress.resetAll() && location.reload()">
    🗑️ Reset all progress
  </button>
</div>

## What's Tracked

| Item | How it's earned |
|------|------------------|
| 🏆 **Quest completion** | Click "Mark quest complete" or check every objective box on a quest page. |
| ⚡ **Objective progress** | Each `- [ ]` checkbox under a quest's Quest Objectives section persists. |
| 📊 **Tier % complete** | Aggregated from your completed quests, scoped by level or tier. |
| 🗺️ **Recommended paths** | Path trackers on quest pages light up as their entries are completed. |
| 🔒 **Locked quests** | Quests with unmet required prerequisites show a lock until you complete the prereq. |

## Roadmap

This dashboard currently runs entirely in your browser. Future iterations may add:

1. **Cloud sync** via your contributor profile (`_data/contributors/`).
2. **Badge gallery** rendering each unique badge earned across completed quests.
3. **Leaderboards** for opt-in community comparison.
4. **Portfolio export** that converts your inventory into a public showcase page.

---

*Continue your quests, and may your stack overflow with knowledge.* ⚔️✨

<script src="{{ '/assets/js/quest-progress.js' | relative_url }}" defer></script>
