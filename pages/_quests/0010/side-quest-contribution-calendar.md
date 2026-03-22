---
title: "Contribution Calendar: Mapping Your Journey Through Time"
author: Quest Master IT-Journey Team
keywords:
    - contribution calendar
    - heatmap
    - CSS grid
    - data visualization
description: Build a GitHub-style contribution heatmap for your character profile using the 52-week calendar data
excerpt: The Timekeeper reveals your patterns — a heatmap of dedication etched in light.
snippet: Time is the truest measure of an adventurer's resolve
date: 2026-03-20T00:00:00.000Z
lastmod: 2026-03-21T15:12:32.256Z
level: "0010"
difficulty: 🟡 Medium
estimated_time: 45-60 minutes
primary_technology: css
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
permalink: /quests/side-quest-contribution-calendar/
categories:
    - Quests
    - Community
    - Frontend
tags:
    - lvl-0010
    - contributor
    - calendar
    - heatmap
    - css-grid
    - liquid
    - gamified-learning
    - project-based
prerequisites:
    knowledge_requirements:
        - Completed Forge Your Character quest
        - CSS Grid basics
        - Jekyll Liquid template syntax
    system_requirements:
        - Text editor or IDE
        - Local Jekyll development environment
quest_dependencies:
    required_quests:
        - /quests/forge-your-character/
    recommended_quests:
        - /quests/side-quest-stats-dashboard/
    unlocks_quests: []
learning_paths:
    primary_paths:
        - Frontend Developer
        - Community Contributor
    character_classes:
        - 🧙 Wizard
        - 🏹 Ranger
    skill_trees:
        - Frontend Development
        - CSS Layout
rewards:
    badges:
        - 📆 Timekeeper — Contribution calendar displayed on character sheet
    progression_points: 100
validation_criteria:
    completion_requirements:
        - Calendar heatmap include created
        - 52 weeks of data render as colored cells
        - Color intensity reflects commit count
        - Calendar is responsive
---

# 📆 Contribution Calendar: Mapping Your Journey Through Time

> *"The calendar does not lie. Each square is a day — each shade, a measure of your will."*
> — The Timekeeper

## 🎯 Quest Objectives

- [ ] Understand the contribution calendar data structure
- [ ] Create a CSS Grid-based heatmap component
- [ ] Map commit counts to color intensities
- [ ] Integrate the calendar into your character sheet
- [ ] Verify responsiveness

## 📖 Background

Your stats generator already records a 52-week contribution history in `contribution_calendar`:

```yaml
contribution_calendar:
  - week: "2026-01-05"
    commits: 3
  - week: "2026-01-12"
    commits: 0
  - week: "2026-01-19"
    commits: 7
  # ... up to 52 weeks
```

This quest turns that data into a visual heatmap — similar to GitHub's contribution graph.

## 🗺️ Quest Steps

### Step 1: Create the Calendar Include

Create `_includes/contributor/contribution_calendar.html`:

```html
{% raw %}
{% assign calendar = include.calendar %}
{% if calendar and calendar.size > 0 %}
<div class="contributor-calendar">
  <h4>📆 Contribution History</h4>
  <div class="calendar-grid">
    {% for week in calendar %}
      {% if week.commits == 0 %}
        {% assign intensity = "zero" %}
      {% elsif week.commits < 3 %}
        {% assign intensity = "low" %}
      {% elsif week.commits < 7 %}
        {% assign intensity = "medium" %}
      {% elsif week.commits < 15 %}
        {% assign intensity = "high" %}
      {% else %}
        {% assign intensity = "max" %}
      {% endif %}
      <div class="calendar-cell calendar-{{ intensity }}"
           title="{{ week.week }}: {{ week.commits }} commits">
      </div>
    {% endfor %}
  </div>
  <div class="calendar-legend">
    <span>Less</span>
    <div class="calendar-cell calendar-zero"></div>
    <div class="calendar-cell calendar-low"></div>
    <div class="calendar-cell calendar-medium"></div>
    <div class="calendar-cell calendar-high"></div>
    <div class="calendar-cell calendar-max"></div>
    <span>More</span>
  </div>
</div>
{% endif %}
{% endraw %}
```

### Step 2: Add CSS Styles

Add to `assets/css/contributor-profile.css`:

```css
/* Contribution Calendar */
.contributor-calendar {
  margin-top: 1.5rem;
}
.contributor-calendar h4 {
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(52, 1fr);
  gap: 2px;
}
.calendar-cell {
  aspect-ratio: 1;
  border-radius: 2px;
  min-width: 8px;
}
.calendar-zero   { background: var(--cal-zero, #ebedf0); }
.calendar-low    { background: var(--cal-low, #9be9a8); }
.calendar-medium { background: var(--cal-med, #40c463); }
.calendar-high   { background: var(--cal-high, #30a14e); }
.calendar-max    { background: var(--cal-max, #216e39); }

/* Class-themed calendar colors */
.contributor-card--wizard ~ .contributor-calendar .calendar-low    { background: #c4b5fd; }
.contributor-card--wizard ~ .contributor-calendar .calendar-medium { background: #8b5cf6; }
.contributor-card--wizard ~ .contributor-calendar .calendar-high   { background: #6d28d9; }
.contributor-card--wizard ~ .contributor-calendar .calendar-max    { background: #4c1d95; }

.calendar-legend {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: var(--contributor-muted, #666);
  justify-content: flex-end;
}
.calendar-legend .calendar-cell {
  width: 12px;
  height: 12px;
  min-width: 12px;
}

/* Responsive: stack or scroll on small screens */
@media (max-width: 600px) {
  .calendar-grid {
    grid-template-columns: repeat(26, 1fr);
  }
}
```

### Step 3: Integrate into Character Sheet

Edit `_includes/contributor/character_sheet.html` and add after the stats panel or achievement wall:

```liquid
{% raw %}
{% include contributor/contribution_calendar.html calendar=contributor.stats.contribution_calendar %}
{% endraw %}
```

### Step 4: Verify

```bash
bundle exec jekyll serve
```

Check your profile page for the heatmap.

- [ ] 52 cells render in a row
- [ ] Color intensity varies by commit count
- [ ] Tooltip shows week date and count on hover
- [ ] Legend displays correctly
- [ ] Responsive on mobile (stacks to 26 columns)

## 💡 Bonus: Streak Indicator

Add a streak highlight by finding the longest consecutive non-zero run and adding a CSS border or glow to those cells.

## 🏆 Reward: Timekeeper Badge 📆

Once your contribution calendar renders on your profile, you've earned the **Timekeeper** badge (+100 XP).

---

> *"The passage of time reveals all. Your dedication is now written in light."*
