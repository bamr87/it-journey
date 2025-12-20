---
title: "SEO Frontmatter Template"
description: "Standard frontmatter template for SEO-optimized content"
created: 2025-12-19T00:00:00.000Z
lastmod: 2025-12-19T00:00:00.000Z
status: "ACTIVE"
category: "templates"
tags:
  - template
  - seo
  - frontmatter
---

# 📝 SEO Frontmatter Template

Use this template when creating or updating content for optimal search engine visibility.

---

## 🎯 Blog Post Template

```yaml
---
title: "[Action Verb] + [Topic] + [Benefit/Context]"
# Example: "Create Bootable macOS Installer: Complete Guide for Recovery"
# Keep under 60 characters for full SERP display

description: "[What] + [How] + [Benefit]. [Secondary detail]."
# Example: "Step-by-step tutorial to create bootable macOS installers using Terminal. Includes commands for Sonoma, Ventura, Monterey & older versions."
# Target: 150-160 characters for full SERP display

date: YYYY-MM-DDTHH:MM:SS.000Z
lastmod: YYYY-MM-DDTHH:MM:SS.000Z

author: IT-Journey Team
layout: default

excerpt: "[Expanded description for social sharing and previews - can be longer than description]"

categories:
  - posts
  - [primary-category]      # e.g., tutorials, guides, reference
  - [secondary-category]    # e.g., macos, linux, devops

tags:
  - [primary-topic]         # e.g., macos, docker, python
  - [secondary-topic]       # related technologies
  - [tool-name]             # specific tools mentioned
  - [platform]              # macos, linux, windows
  - [skill-level]           # beginner, intermediate, advanced

keywords:
  - [exact search phrase 1]    # e.g., "create bootable macos usb"
  - [exact search phrase 2]    # e.g., "macos installer terminal"
  - [exact search phrase 3]    # e.g., "createinstallmedia command"
  - [related search phrase]    # e.g., "macos recovery"

meta: "[One-line summary for meta tags]"
snippet: "[Short teaser - 1 sentence max]"

draft: false                 # Set to true only during active editing
difficulty: beginner | intermediate | advanced
estimated_time: "[X minutes/hours]"
section: "[Department/Category]"
---
```

---

## 🗺️ Quest Template

```yaml
---
title: "[Quest Name]: [Descriptive Subtitle]"
# Example: "Nerd Font Enchantment: Terminal Icon Mastery"

description: "[Action-oriented description with platform mentions]. [Time estimate]. [Key benefit]."
# Example: "Complete step-by-step guide to install Nerd Fonts on macOS, Linux & Windows. Transform your terminal with icons, symbols, and visual themes. 20-minute setup tutorial."

date: YYYY-MM-DDTHH:MM:SS.000Z
lastmod: YYYY-MM-DDTHH:MM:SS.000Z
preview: images/previews/[slug].png

tags:
  - [level-tag]              # e.g., lvl-0010, binary-level-indicator
  - [primary-skill]          # e.g., terminal-mastery
  - [tool-name]              # e.g., nerd-fonts, docker
  - [platforms...]           # macos, linux, windows
  - [category]               # e.g., development-tools

categories:
  - Quests
  - [Quest-Type]             # Side-Quests, Main-Quests
  - [Skill-Area]             # Terminal-Mastery, DevOps, Frontend

sub-title: "[Quest classification and brief descriptor]"
excerpt: "[Extended description for previews - mention platforms and key outcomes]"
snippet: "[One compelling sentence summary]"

author: IT-Journey Team
layout: journals

keywords:
  primary:
    - [main search term 1]
    - [main search term 2]
    - [platform-specific term]  # e.g., "nerd fonts macos"
  secondary:
    - [related term 1]
    - [tool integration]        # e.g., "oh-my-zsh fonts"
    - [use case term]           # e.g., "terminal customization"

permalink: /quests/[descriptive-slug]/
difficulty: 🟢 Easy | 🟡 Medium | 🔴 Hard
estimated_time: "[X-Y minutes]"

prerequisites:
  - [Skill or knowledge needed]
  - [Tools required]

rewards:
  - 🏆 [Achievement Name] - [Description]
  - ⚡ [Skill Badge] - [What it represents]

level: "[XXXX]"              # Binary level number
quest_type: main_quest | side_quest
---
```

---

## 📚 Documentation Template

```yaml
---
key: tutorial | reference | guide
title: "[Tool/Topic]: [What This Covers]"
# Example: "Jekyll Mermaid Diagrams: Auto-Detection Guide for Flowcharts"

description: "[Complete guide/tutorial] to [action] with [tool]. [Key features]. [Benefit]."
# Example: "Complete guide to adding Mermaid diagrams to Jekyll sites with zero configuration. Create flowcharts, sequence diagrams, Gantt charts, and more."

subcategory: [jekyll | python | devops | etc.]
date: YYYY-MM-DDTHH:MM:SS.000Z
lastmod: YYYY-MM-DDTHH:MM:SS.000Z

excerpt: "[Extended description mentioning key features and outcomes]"

tags:
  - [primary-tool]
  - [secondary-tool]
  - [feature-1]
  - [feature-2]
  - [category]

categories:
  - tutorials | reference | guides
  - [technology]
  - [use-case]

keywords:
  - [tool + action phrase]      # e.g., "jekyll mermaid"
  - [how-to phrase]             # e.g., "add diagrams to jekyll"
  - [feature phrase]            # e.g., "mermaid auto-detection"

difficulty: beginner | intermediate | advanced
estimated_time: "[X minutes]"
---
```

---

## ✅ SEO Frontmatter Checklist

Before publishing, verify:

### Title (60 chars max)
- [ ] Starts with action verb or key topic
- [ ] Includes primary keyword
- [ ] Compelling and click-worthy
- [ ] Under 60 characters

### Description (160 chars max)
- [ ] Describes what user will learn/get
- [ ] Includes primary keyword naturally
- [ ] Mentions platforms if applicable
- [ ] Has clear benefit statement
- [ ] 150-160 characters

### Keywords & Tags
- [ ] Primary keyword in title AND description
- [ ] Platform-specific tags (macos, linux, windows)
- [ ] Tool-specific tags
- [ ] Skill level indicated
- [ ] 5-10 relevant tags total

### Technical Fields
- [ ] `draft: false` (unless actively editing)
- [ ] `lastmod` updated to current date
- [ ] `difficulty` set appropriately
- [ ] `estimated_time` is realistic
- [ ] `permalink` is descriptive (for quests/docs)

### Content Signals
- [ ] `excerpt` is unique and descriptive
- [ ] `snippet` is compelling one-liner
- [ ] `categories` are accurate
- [ ] `meta` summary is concise

---

## 🎯 Keyword Research Tips

### Finding Good Keywords
1. **Google Search Console** - See what queries bring traffic
2. **Google Autocomplete** - Type topic and see suggestions
3. **"People Also Ask"** - Related questions to answer
4. **Competitor Analysis** - What terms do similar sites rank for

### Keyword Placement Priority
1. **Title** - Most important
2. **Description** - Second most important  
3. **H1/H2 Headers** - In content
4. **First paragraph** - Early in body
5. **Keywords field** - For internal tracking

### Platform-Specific Keywords
Always include platform when relevant:
- ❌ "install nerd fonts"
- ✅ "install nerd fonts macos"
- ✅ "nerd fonts linux terminal"
- ✅ "nerd fonts windows powershell"

---

## 📊 Examples of Good vs Bad

### Titles
| ❌ Bad | ✅ Good |
|--------|---------|
| "Bootable mac os" | "Create Bootable macOS Installer: Complete Guide" |
| "Mermaid Diagrams" | "Jekyll Mermaid Diagrams: Auto-Detection Guide" |
| "Widgets" | "Install Rainmeter Desktop Widgets on Windows" |

### Descriptions
| ❌ Bad | ✅ Good |
|--------|---------|
| `null` | "Step-by-step tutorial to create bootable macOS installers..." |
| "Install fonts" | "Complete guide to install Nerd Fonts on macOS, Linux & Windows..." |
| Generic copy | Action-oriented with platforms and benefits |

---

**Template Version**: 1.0.0  
**Created**: 2025-12-19  
**Usage**: Copy relevant section when creating new content
