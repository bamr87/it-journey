---
title: "Stats Dashboard: Enhancing Your Data Visualization"
author: Quest Master IT-Journey Team
keywords:
    - stats dashboard
    - charts
    - data visualization
    - JavaScript
description: Extend the contributor stats panel with charts, graphs, and enhanced data visualizations
excerpt: The Data Sage reveals deeper patterns in your contribution history.
snippet: Numbers tell tales — learn to read the runes of data
date: 2026-03-20T00:00:00.000Z
lastmod: 2026-03-21T15:12:32.246Z
level: "0010"
difficulty: 🟡 Medium
estimated_time: 45-60 minutes
primary_technology: javascript
quest_type: side_quest
skill_focus:
    - frontend
learning_style: project-based
quest_series: "Contributor Path: Identity & Recognition"
quest_line: Contributor Chronicles
quest_arc: "Act II: Mastering the Craft"
fmContentType: quest
draft: false
comments: true
permalink: /quests/side-quest-stats-dashboard/
categories:
    - Quests
    - Community
    - Frontend
tags:
    - lvl-0010
    - contributor
    - stats
    - data-visualization
    - javascript
    - liquid
    - gamified-learning
    - project-based
prerequisites:
    knowledge_requirements:
        - Completed Forge Your Character quest
        - Basic HTML and CSS knowledge
        - Familiarity with Jekyll Liquid templates
    system_requirements:
        - Text editor or IDE
        - Local Jekyll development environment
quest_dependencies:
    required_quests:
        - /quests/forge-your-character/
    recommended_quests:
        - /quests/side-quest-badge-collector/
    unlocks_quests:
        - /quests/side-quest-contribution-calendar/
learning_paths:
    primary_paths:
        - Frontend Developer
        - Community Contributor
    character_classes:
        - 🧙 Wizard
        - 🗡️ Rogue
    skill_trees:
        - Frontend Development
        - Data Visualization
rewards:
    badges:
        - 📊 Data Sage — Enhanced stats visualization on character sheet
    progression_points: 100
validation_criteria:
    completion_requirements:
        - New stats visualization include created
        - Data renders from contributor YAML data
        - Visualization is responsive and accessible
        - Integrated into character_sheet.html
---

# 📊 Stats Dashboard: Enhancing Your Data Visualization

> *"Raw numbers are mere ink. Transform them into stories, and you wield true power."*
> — The Data Sage

## 🎯 Quest Objectives

- [ ] Understand the contributor data structure
- [ ] Create a new Liquid include for enhanced stats
- [ ] Add a language/category breakdown chart
- [ ] Build a contribution summary visualization
- [ ] Integrate the dashboard into the character sheet

## 📖 Background

Your character sheet already shows basic stat tiles (commits, PRs, etc.). This quest upgrades the stats panel with richer visualizations — bar charts, progress rings, and comparative displays — all using pure HTML/CSS and Liquid (no JavaScript libraries required).

## 🗺️ Quest Steps

### Step 1: Understand the Data

Your contributor YAML file (`_data/contributors/YOUR_USERNAME.yml`) contains:

```yaml
stats:
  top_languages:
    - name: Markdown
      percentage: 45
    - name: Ruby
      percentage: 25
    - name: JavaScript
      percentage: 15
  top_categories:
    - name: DevOps
      count: 12
    - name: Frontend
      count: 8
  lines_added: 5432
  lines_removed: 1234
```

All of this is accessible in Liquid as `site.data.contributors.YOUR_USERNAME.stats`.

### Step 2: Create the Enhanced Stats Include

Create `_includes/contributor/stats_dashboard.html`:

```html
{% raw %}
{% assign s = include.stats %}
{% if s %}
<div class="contributor-dashboard">

  <!-- Language Breakdown -->
  {% if s.top_languages.size > 0 %}
  <div class="dashboard-section">
    <h4>🔤 Languages</h4>
    <div class="language-bars">
      {% for lang in s.top_languages %}
      <div class="lang-row">
        <span class="lang-name">{{ lang.name }}</span>
        <div class="lang-bar-track">
          <div class="lang-bar-fill" style="width: {{ lang.percentage }}%">
            {{ lang.percentage }}%
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
  {% endif %}

  <!-- Lines of Code -->
  {% if s.lines_added > 0 or s.lines_removed > 0 %}
  <div class="dashboard-section">
    <h4>📝 Code Impact</h4>
    {% assign total_lines = s.lines_added | plus: s.lines_removed %}
    {% assign add_pct = s.lines_added | times: 100 | divided_by: total_lines %}
    <div class="code-impact-bar">
      <div class="impact-added" style="width: {{ add_pct }}%"
           title="{{ s.lines_added }} lines added">
        +{{ s.lines_added }}
      </div>
      <div class="impact-removed" style="width: {{ 100 | minus: add_pct }}%"
           title="{{ s.lines_removed }} lines removed">
        -{{ s.lines_removed }}
      </div>
    </div>
  </div>
  {% endif %}

</div>
{% endif %}
{% endraw %}
```

### Step 3: Add CSS Styles

Add to `assets/css/contributor-profile.css`:

```css
/* Dashboard */
.contributor-dashboard {
  display: grid;
  gap: 1.5rem;
  margin-top: 1.5rem;
}
.dashboard-section h4 {
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}
.lang-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.4rem;
}
.lang-name {
  min-width: 80px;
  font-size: 0.85rem;
}
.lang-bar-track {
  flex: 1;
  height: 20px;
  background: var(--contributor-bg, #f5f5f5);
  border-radius: 4px;
  overflow: hidden;
}
.lang-bar-fill {
  height: 100%;
  background: var(--contributor-accent, #6c3fc5);
  border-radius: 4px;
  font-size: 0.75rem;
  color: #fff;
  display: flex;
  align-items: center;
  padding-left: 6px;
  min-width: 30px;
}
.code-impact-bar {
  display: flex;
  height: 28px;
  border-radius: 4px;
  overflow: hidden;
  font-size: 0.8rem;
  color: #fff;
}
.impact-added {
  background: #2e7d32;
  display: flex;
  align-items: center;
  justify-content: center;
}
.impact-removed {
  background: #c5221f;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### Step 4: Integrate into Character Sheet

Edit `_includes/contributor/character_sheet.html` and add after the stats panel:

```liquid
{% raw %}
{% include contributor/stats_dashboard.html stats=contributor.stats %}
{% endraw %}
```

### Step 5: Verify

```bash
bundle exec jekyll serve
```

Check your profile page for the new visualizations.

- [ ] Language bars render with correct percentages
- [ ] Code impact bar shows +/- ratio
- [ ] Layout is responsive on mobile
- [ ] Colors match your class theme

## 💡 Bonus: Category Breakdown

Add a category section to your dashboard for extra polish:

```html
{% raw %}
{% if s.top_categories.size > 0 %}
<div class="dashboard-section">
  <h4>📂 Top Categories</h4>
  {% for cat in s.top_categories %}
  <span class="category-chip">{{ cat.name }} ({{ cat.count }})</span>
  {% endfor %}
</div>
{% endif %}
{% endraw %}
```

## 🏆 Reward: Data Sage Badge 📊

Once your enhanced stats dashboard renders on your profile, you've earned the **Data Sage** badge (+100 XP).

---

> *"You see beyond the numbers now. Welcome to the inner circle of data wielders."*
