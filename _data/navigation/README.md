# Navigation Data Schema Documentation

This directory contains YAML navigation data files used by the sidebar and navbar components. All files follow a standardized schema compatible with the **zer0-mistakes theme v0.17+**.

## Schema Definition

Each navigation item can have the following properties:

```yaml
- title: string        # Required - Display text
  url: string          # Optional - Link URL (relative to site root)
  icon: string         # Optional - Bootstrap Icons class (e.g., "bi-folder", "bi-house")
  description: string  # Optional - Tooltip or description text
  expanded: boolean    # Optional - Default expanded state (default: false)
  children: array      # Optional - Nested navigation items (max 2 levels deep)
```

### Property Details

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `title` | string | Yes | Display text for the navigation item |
| `url` | string | No | Link URL (relative to site root) |
| `icon` | string | No | Bootstrap Icons class with `bi-` prefix |
| `description` | string | No | Tooltip or additional description |
| `expanded` | boolean | No | Whether children are expanded by default |
| `children` | array | No | Nested navigation items (max 2 levels) |

## Navigation Modes

The sidebar supports three navigation modes set via `page.sidebar.nav`:

1. **auto** - Auto-generates from collection documents
2. **tree** - Uses YAML data from this directory (specify file name)
3. **categories** - Groups by Jekyll categories

## Available Files

| File | Purpose | Description |
|------|---------|-------------|
| `main.yml` | Primary site navigation | Navbar dropdowns and main menu |
| `docs.yml` | Documentation section | Sidebar for /docs/ pages |
| `about.yml` | About section | Sidebar for /about/ pages |
| `quickstart.yml` | Quick start guide | Sidebar for /quickstart/ pages |
| `home.yml` | Homepage quick links | Icon-based quick navigation |
| `posts.yml` | Blog categories | Category navigation for posts |
| `quests.yml` | Quest navigation | Educational quest hierarchy |
| `notebooks.yml` | Notes & notebooks | Sidebar for /notes/ pages |
| `hobbies.yml` | Hobbies section | Sidebar for /hobbies/ pages |

## Example Usage

### In Page Front Matter

```yaml
---
title: My Documentation Page
sidebar:
  nav: docs  # Uses _data/navigation/docs.yml
---
```

### Navigation File Example

```yaml
# _data/navigation/docs.yml
- title: Getting Started
  url: /docs/getting-started/
  icon: bi-rocket-takeoff
  expanded: true
  children:
    - title: Installation
      url: /docs/installation/
      icon: bi-download
    - title: Configuration
      url: /docs/configuration/
      icon: bi-gear
- title: API Reference
  url: /docs/api/
  icon: bi-code-slash
  children:
    - title: Authentication
      url: /docs/api/auth/
    - title: Endpoints
      url: /docs/api/endpoints/
```

## Bootstrap Icons Reference

Common icons used in navigation:

| Icon | Class | Use Case |
|------|-------|----------|
| 🏠 | `bi-house` | Home pages |
| 📖 | `bi-book` | Documentation |
| 🚀 | `bi-rocket-takeoff` | Quick start, getting started |
| 📰 | `bi-journal-text` | Blog, posts |
| 📚 | `bi-journal-bookmark` | Library, docs |
| 💻 | `bi-terminal` | Terminal, CLI |
| ⚙️ | `bi-gear` | Settings, config |
| ℹ️ | `bi-info-circle` | About, info |
| 🗺️ | `bi-map` | Navigation, maps |
| 📊 | `bi-bar-chart-line` | Statistics, analytics |
| 🤖 | `bi-robot` | AI, automation |
| 📦 | `bi-box-seam` | Containers, packages |

Full icon reference: [Bootstrap Icons](https://icons.getbootstrap.com/)

## Migration Notes (v0.17+)

The zer0-mistakes theme v0.17+ introduced these changes:

- ✅ Renamed `sublinks` to `children` for consistency with tree terminology
- ✅ Added `expanded` property for default collapsed/expanded state
- ✅ Added `description` property for tooltips
- ✅ Icons must use full Bootstrap Icons class with `bi-` prefix
- ✅ Navigation modes changed: `dynamic` → `auto`, `searchCats` → `categories`

## Schema Validation

Navigation YAML files are validated at build time. Invalid schemas will produce build warnings. Ensure all required properties are present and icon classes use the `bi-` prefix.

---

**Last Updated**: 2026-01-24  
**Theme Compatibility**: zer0-mistakes v0.17+
