---
title: Contributor Profile Includes
description: Jekyll Liquid includes for the gamified contributor character sheet system
lastmod: 2026-03-20
---

# Contributor Profile Includes

Jekyll includes that compose the RPG-style character sheet displayed on contributor profile pages.

## Architecture

```
character_sheet.html          ← Master include (use this one)
  ├── profile_card.html       ← Avatar, name, class, level, XP bar, links
  ├── stats_panel.html        ← Contribution stats grid + languages/categories
  └── achievement_wall.html   ← Pinned badges + all earned achievements
```

## Usage

In a contributor profile page:

```liquid
{% raw %}
{% include contributor/character_sheet.html username="bamr87" %}
{% endraw %}
```

The `username` parameter loads data from `_data/contributors/{username}.yml`.

## Files

| File | Purpose |
|------|---------|
| `character_sheet.html` | Master orchestrator — loads data and composes sub-includes |
| `profile_card.html` | Hero card with avatar, class icon, tier badge, XP progress bar, bio, social links |
| `stats_panel.html` | Grid of stat tiles (commits, PRs, quests, posts, active days, streak) + top languages/categories |
| `achievement_wall.html` | Featured (pinned) badges section + earned achievements grid |

## Data Dependencies

All includes read from `site.data.contributors[username]`:

- `profile` — user-editable identity (class, avatar, bio, links, pinned badges)
- `stats` — auto-generated contribution numbers
- `achievements` — auto-generated badge list
- `level` — auto-generated XP/tier/progress

## Styling

Requires `assets/css/contributor-profile.css` linked in the page:

```html
<link rel="stylesheet" href="{{ '/assets/css/contributor-profile.css' | relative_url }}">
```

## Class Theming

The profile card applies a CSS class based on the contributor's chosen class:

| Class | CSS Class | Accent Color |
|-------|-----------|-------------|
| Wizard | `contributor-card--wizard` | `#6c3fc5` |
| Warrior | `contributor-card--warrior` | `#c5221f` |
| Ranger | `contributor-card--ranger` | `#2e7d32` |
| Rogue | `contributor-card--rogue` | `#e65100` |
| Healer | `contributor-card--healer` | `#00838f` |
| Bard | `contributor-card--bard` | `#ad1457` |
| Paladin | `contributor-card--paladin` | `#1565c0` |

Contributors can also set a custom `banner_color` in their data file.
