---
title: "Badge Collector: Showcasing Your Achievements"
author: Quest Master IT-Journey Team
keywords:
    - badges
    - achievements
    - gamification
    - contributor profile
description: Learn how badges are earned and pin your proudest achievements to your character profile
excerpt: The Trophy Hall awaits — curate your collection of hard-won badges.
snippet: Every achievement tells a story. Pin the ones that matter most.
date: 2026-03-20T00:00:00.000Z
lastmod: 2026-03-21T15:12:32.239Z
level: "0001"
difficulty: 🟡 Medium
estimated_time: 30-45 minutes
primary_technology: yaml
quest_type: side_quest
skill_focus:
    - devops
    - frontend
learning_style: hands-on
quest_series: "Contributor Path: Identity & Recognition"
quest_line: Contributor Chronicles
quest_arc: "Act I: Arrival at the Guild"
fmContentType: quest
draft: false
comments: true
permalink: /quests/side-quest-badge-collector/
categories:
    - Quests
    - Community
    - Customization
tags:
    - lvl-0001
    - contributor
    - badges
    - achievements
    - yaml
    - gamified-learning
    - hands-on
prerequisites:
    knowledge_requirements:
        - Completed Forge Your Character quest
        - At least one earned achievement badge
        - Basic YAML editing skills
    system_requirements:
        - Text editor or IDE
quest_dependencies:
    required_quests:
        - /quests/forge-your-character/
    recommended_quests:
        - /quests/side-quest-avatar-forge/
    unlocks_quests: []
learning_paths:
    primary_paths:
        - Community Contributor
    character_classes:
        - ⚔️ Warrior
        - 🛡️ Paladin
    skill_trees:
        - Community & Collaboration
rewards:
    badges:
        - 🏅 Badge Collector — Curated a pinned badge showcase
    progression_points: 75
validation_criteria:
    completion_requirements:
        - badges_pinned array has 1-3 valid badge IDs
        - Pinned badges display in the Featured section
        - Understand how achievement thresholds work
---

# 🏅 Badge Collector: Showcasing Your Achievements

> *"Deeds in the dark matter not. Display your triumphs for all to see."*
> — The Trophy Keeper

## 🎯 Quest Objectives

- [ ] Understand the achievement system and how badges are earned
- [ ] Identify which badges you've already earned
- [ ] Pin your top badges to the Featured section
- [ ] Verify the pinned badges display correctly

## 📖 The Achievement System

Badges are **auto-earned** by the stats generator when you hit contribution milestones. You don't claim them manually — they appear when you've done the work.

### Achievement Catalog

| Badge ID | Icon | Name | How to Earn |
|----------|------|------|-------------|
| `first_blood` | 🩸 | First Blood | Make your first commit |
| `centurion` | 💯 | Centurion | Reach 100 commits |
| `thousand_cuts` | ⚔️ | Thousand Cuts | Reach 1,000 commits |
| `team_player` | 🤝 | Team Player | Get your first PR merged |
| `pr_machine` | 🔄 | PR Machine | Get 50 PRs merged |
| `quest_forger` | 📜 | Quest Forger | Author your first quest |
| `quest_master` | 🏰 | Quest Master | Author 10 quests |
| `scribe` | ✍️ | Scribe | Write your first post |
| `prolific_author` | 📚 | Prolific Author | Write 20 posts |
| `marathon_runner` | 🏃 | Marathon Runner | Achieve a 7-day contribution streak |
| `polyglot` | 🌐 | Polyglot | Contribute in 5+ languages |
| `guild_founder` | 🏛️ | Guild Founder | Reserved for project founders |

### How Badges Work

The stats generator (`scripts/generation/generate_contributor_stats.rb`) checks thresholds after counting your contributions:

```
commits >= 1          → first_blood
commits >= 100        → centurion
commits >= 1000       → thousand_cuts
prs_merged >= 1       → team_player
prs_merged >= 50      → pr_machine
quests_authored >= 1   → quest_forger
quests_authored >= 10  → quest_master
posts_authored >= 1    → scribe
posts_authored >= 20   → prolific_author
current_streak >= 7    → marathon_runner
top_languages.size >= 5 → polyglot
```

Badges include an `earned_on` date that's preserved across regeneration — your achievements are permanent.

## 🗺️ Quest Steps

### Step 1: Check Your Current Badges

Run the stats generator (or check your data file after it's been auto-updated):

```bash
make contributor-stats USERNAME=YOUR_USERNAME
cat _data/contributors/YOUR_USERNAME.yml
```

Look at the `achievements` section to see what badges you've earned.

### Step 2: Pin Your Favorites

Edit `_data/contributors/YOUR_USERNAME.yml` and add up to 3 badge IDs to the pinned array:

```yaml
profile:
  badges_pinned:
    - first_blood
    - quest_forger
    - marathon_runner
```

> **Rules**: 
> - Maximum 3 pinned badges  
> - Must be badges you've actually earned  
> - Order matters — first badge is displayed most prominently

### Step 3: Verify the Display

Build and check your profile:

```bash
bundle exec jekyll serve
```

On your profile page, you should see:

1. **Featured Badges** section with your pinned badges at the top
2. **All Achievements** section below with every earned badge

- [ ] Pinned badges appear in Featured section
- [ ] All earned badges display correctly with earned dates

### Step 4: Earn More Badges

Want to fill your trophy wall? Here are quickest paths:

| Badge | Fastest Path |
|-------|-------------|
| First Blood 🩸 | Any commit (you probably have this!) |
| Scribe ✍️ | Write a blog post in `pages/_posts/` |
| Quest Forger 📜 | Create a quest in `pages/_quests/` |
| Marathon Runner 🏃 | Commit something 7 days in a row |

## 🏆 Reward: Badge Collector 🏅

Once you've pinned at least one badge to your Featured section, you've earned the **Badge Collector** badge (+75 XP).

---

> *"A well-curated trophy wall speaks louder than a thousand commits."*
