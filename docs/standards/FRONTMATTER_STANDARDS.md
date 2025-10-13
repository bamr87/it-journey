# Frontmatter Standards

This document defines the required and optional frontmatter fields for each content type in the IT-Journey repository.

## Overview

Frontmatter is YAML metadata at the beginning of each Markdown file, enclosed by triple dashes (`---`). It provides structured information that Jekyll uses to process and display content.

## Universal Fields

These fields are applicable to all content types:

### Required Universal Fields

```yaml
title: "Your Content Title"
```

### Recommended Universal Fields

```yaml
description: "Brief description of the content"
author: "Author Name"
date: 2025-10-13T00:00:00.000Z
lastmod: 2025-10-13T00:00:00.000Z
```

### Optional Universal Fields

```yaml
draft: false                    # Set to true to mark as draft
slug: "custom-url-slug"        # Override default URL slug
permalink: "/custom/path/"      # Override default permalink
excerpt: "Short summary"        # Manual excerpt (auto-generated if not set)
```

## Content Type Templates

### Blog Posts (`_posts`)

**File Naming:** `YYYY-MM-DD-title-slug.md`

**Required Fields:**
```yaml
---
title: "Post Title"
date: 2025-10-13T00:00:00.000Z
layout: journals
---
```

**Complete Template:**
```yaml
---
title: "Understanding Jekyll Collections"
description: "A deep dive into Jekyll's collection system"
author: "Amr Abdel-Motaleb"
layout: journals
date: 2025-10-13T12:00:00.000Z
lastmod: 2025-10-13T15:30:00.000Z
categories:
  - development
  - jekyll
tags:
  - jekyll
  - collections
  - static-sites
slug: jekyll-collections-deep-dive
excerpt: "Explore how Jekyll collections organize content effectively"
image: /assets/images/posts/jekyll-collections.png
mermaid: false
mathjax: false
toc: true
toc_sticky: true
draft: false
---
```

**Field Descriptions:**
- `layout` - Always "journals" for posts
- `categories` - List of categories (affects URL structure)
- `tags` - List of tags for filtering and search
- `image` - Hero image or thumbnail
- `mermaid` - Set to `true` to enable Mermaid diagrams
- `mathjax` - Set to `true` to enable mathematical notation
- `toc` - Set to `true` to generate table of contents
- `toc_sticky` - Set to `true` for sticky TOC sidebar

### Quests (`_quests`)

**File Naming:** `descriptive-quest-title.md`

**Required Fields:**
```yaml
---
title: "Quest Title"
date: 2025-10-13T00:00:00.000Z
layout: default
---
```

**Complete Template:**
```yaml
---
title: "The Link Guardian's Quest: Automated Hyperlink Validation"
description: "Master the art of automated link checking with AI-powered analysis"
author: "Amr Abdel-Motaleb"
layout: default
date: 2025-10-13T00:00:00.000Z
lastmod: 2025-10-13T00:00:00.000Z
categories:
  - automation
  - devops
tags:
  - python
  - github-actions
  - ai
  - testing
level: "0101"                   # Binary level (0000-1111)
difficulty: "intermediate"       # beginner, intermediate, advanced, expert
quest_type: "automation"         # automation, development, devops, data-science
xp: 500                         # Experience points
achievements:
  - "Link Guardian"
  - "CI/CD Master"
prerequisites:
  - "Basic Python knowledge"
  - "GitHub Actions familiarity"
estimated_time: "2-3 hours"
platforms:
  - macOS
  - Windows
  - Linux
slug: link-guardian-quest
excerpt: "Learn to implement automated link validation with AI analysis"
image: /assets/images/quests/link-guardian.png
toc: true
toc_sticky: true
mermaid: true
draft: false
---
```

**Quest-Specific Fields:**
- `level` - Binary system (0000, 0001, 0010, etc.) indicating progression
- `difficulty` - Difficulty rating: beginner, intermediate, advanced, expert
- `quest_type` - Category of quest
- `xp` - Experience points awarded upon completion
- `achievements` - List of achievements earned
- `prerequisites` - Required knowledge or previous quests
- `estimated_time` - Expected completion time
- `platforms` - Supported operating systems

### Documentation (`_docs`)

**File Naming:** `tool-topic-description.md`

**Required Fields:**
```yaml
---
title: "Jekyll - Liquid Templating"
date: 2025-10-13T00:00:00.000Z
---
```

**Complete Template:**
```yaml
---
title: "Jekyll - Liquid Templating"
description: "Guide to using Liquid templating language in Jekyll"
author: "Amr Abdel-Motaleb"
layout: default
date: 2025-10-13T00:00:00.000Z
lastmod: 2025-10-13T00:00:00.000Z
subcategory: jekyll             # Grouping within docs
tags:
  - jekyll
  - liquid
  - templating
key: tutorial                   # Legacy field, optional
index: 8111                     # Legacy ordering, optional
sources:
  - https://shopify.github.io/liquid/
  - https://jekyllrb.com/docs/liquid/
slug: jekyll-liquid-templating
excerpt: "Master Liquid templating for Jekyll sites"
toc: true
toc_sticky: true
draft: false
---
```

**Docs-Specific Fields:**
- `subcategory` - Used to group related docs (e.g., all Jekyll docs)
- `sources` - List of external reference URLs
- `key` - Legacy field from old system (optional)
- `index` - Legacy numbering system (optional)

### Notebooks (`_notebooks`)

**File Naming:** `descriptive-notebook-name.md` or `notebook.ipynb`

**For Markdown (.md):**
```yaml
---
title: "Data Analysis with Pandas"
description: "Exploratory data analysis using Pandas library"
author: "Amr Abdel-Motaleb"
layout: default
date: 2025-10-13T00:00:00.000Z
lastmod: 2025-10-13T00:00:00.000Z
categories:
  - data-science
tags:
  - python
  - pandas
  - data-analysis
notebook_type: "tutorial"       # tutorial, analysis, visualization, ml
language: "python"              # python, r, julia, javascript
kernel: "python3"
packages:
  - pandas
  - numpy
  - matplotlib
slug: pandas-data-analysis
excerpt: "Learn data analysis fundamentals with Pandas"
draft: false
---
```

**For Jupyter (.ipynb):**
Frontmatter is stored in the notebook metadata. When converting to markdown, extract and format appropriately.

**Notebook-Specific Fields:**
- `notebook_type` - Type of notebook content
- `language` - Programming language used
- `kernel` - Jupyter kernel name
- `packages` - Required Python/R packages

### Notes (`_notes`)

**File Naming:** `descriptive-note-name.md`

**Minimal Template:**
```yaml
---
title: "Feature Idea: AI-Powered Content Suggestions"
date: 2025-10-13T00:00:00.000Z
status: "draft"                 # draft, in-progress, complete, archived
---
```

**Complete Template:**
```yaml
---
title: "Feature Idea: AI-Powered Content Suggestions"
description: "Exploring AI-driven content recommendations"
author: "Amr Abdel-Motaleb"
date: 2025-10-13T00:00:00.000Z
lastmod: 2025-10-13T00:00:00.000Z
status: "in-progress"           # draft, in-progress, complete, archived
categories:
  - development
  - ai
tags:
  - ai
  - features
  - ideas
visibility: "private"           # private, team, public
related_quest: "ai-integration-quest"
slug: ai-content-suggestions
---
```

**Notes-Specific Fields:**
- `status` - Current state: draft, in-progress, complete, archived
- `visibility` - Who can see this: private, team, public
- `related_quest` - Link to related quest (if applicable)

### About Pages (`_about`)

**File Naming:** `descriptive-page-name.md`

**Required Fields:**
```yaml
---
title: "About IT-Journey"
layout: default
---
```

**Complete Template:**
```yaml
---
title: "About IT-Journey"
description: "Learn about the IT-Journey learning platform"
layout: default
date: 2025-10-13T00:00:00.000Z
lastmod: 2025-10-13T00:00:00.000Z
permalink: /about/
categories:
  - about
sidebar:
  nav: about
toc: true
slug: about-it-journey
excerpt: "Discover the IT-Journey mission and vision"
---
```

### Quickstart Guides (`_quickstart`)

**File Naming:** `tool-quickstart.md`

**Required Fields:**
```yaml
---
title: "Jekyll Quickstart"
layout: default
---
```

**Complete Template:**
```yaml
---
title: "Jekyll Quickstart"
description: "Quick reference for Jekyll commands and configuration"
layout: default
date: 2025-10-13T00:00:00.000Z
lastmod: 2025-10-13T00:00:00.000Z
categories:
  - quickstart
tags:
  - jekyll
  - reference
tool: "Jekyll"                  # Tool/technology name
version: "3.9.5"                # Tool version
sidebar:
  nav: quickstart
toc: true
slug: jekyll-quickstart
excerpt: "Essential Jekyll commands and tips"
---
```

**Quickstart-Specific Fields:**
- `tool` - Name of tool/technology
- `version` - Version number for reference

## Date Formatting

### ISO 8601 Format (Preferred)

```yaml
date: 2025-10-13T12:30:00.000Z
lastmod: 2025-10-13T15:45:30.000Z
```

### Alternative Formats (Also Supported)

```yaml
date: 2025-10-13
date: 2025-10-13 12:30:00 -0600
```

## Category and Tag Conventions

### Categories
- Use lowercase with hyphens
- Limit to 2-3 categories per post
- Categories affect URL structure
- Be consistent across similar content

**Examples:**
```yaml
categories:
  - development
  - jekyll
  - automation
```

### Tags
- Use lowercase with hyphens
- More specific than categories
- Can have many tags per post
- Used for search and filtering

**Examples:**
```yaml
tags:
  - python
  - github-actions
  - ci-cd
  - automation
  - testing
```

## Boolean Values

Always use lowercase `true` and `false`:

```yaml
draft: false
toc: true
toc_sticky: true
mermaid: false
mathjax: false
```

## Lists and Arrays

Use YAML list syntax:

```yaml
# Method 1: Dash notation
tags:
  - python
  - jekyll
  - automation

# Method 2: Inline array (less readable, not recommended)
tags: [python, jekyll, automation]
```

## Multi-line Strings

Use YAML multi-line syntax:

```yaml
# Literal block (preserves newlines)
description: |
  This is a longer description
  that spans multiple lines
  and preserves formatting.

# Folded block (joins lines)
excerpt: >
  This is a longer excerpt
  that will be joined into
  a single paragraph.
```

## Special Characters

Escape or quote strings with special characters:

```yaml
# Quotes required for colons
title: "Jekyll: A Static Site Generator"

# Quotes required for quotes
excerpt: 'He said, "Hello World"'

# Escape quotes within same quote type
excerpt: "He said, \"Hello World\""
```

## Validation

### Required Field Checklist

Before committing content, verify:

- [ ] Title is present and descriptive
- [ ] Date is in valid ISO 8601 format
- [ ] Layout is specified (or uses collection default)
- [ ] Categories/tags are lowercase with hyphens
- [ ] No extra spaces or tabs (YAML is whitespace-sensitive)
- [ ] Boolean values are lowercase
- [ ] Special characters are properly escaped/quoted

### Automated Validation

The repository includes automated frontmatter validation via GitHub Actions:

- Runs on all commits to `main` branch
- Checks required fields for each content type
- Validates date formats
- Ensures proper YAML syntax
- Reports errors in workflow logs

See `.github/workflows/frontmatter-validation.yml` for details.

## Common Mistakes

### ❌ Incorrect

```yaml
# Missing quotes with colon
title: Jekyll: Static Site Generator

# Uppercase boolean
draft: True

# Mixed case tags
tags:
  - Python
  - GitHub-Actions

# Inconsistent date format
date: 10/13/2025

# Extra spaces in list
tags:
  -  python
  -   jekyll
```

### ✅ Correct

```yaml
# Proper quoting
title: "Jekyll: Static Site Generator"

# Lowercase boolean
draft: true

# Lowercase tags
tags:
  - python
  - github-actions

# ISO 8601 date
date: 2025-10-13T00:00:00.000Z

# Consistent spacing
tags:
  - python
  - jekyll
```

## Frontmatter Tools

### VS Code Extensions
- **Front Matter CMS** - Visual frontmatter editor
- **YAML** - YAML syntax highlighting and validation

### Validation Scripts
```bash
# Check frontmatter in a file
bundle exec jekyll doctor

# Build site (will show frontmatter errors)
bundle exec jekyll build --verbose
```

## Migration Notes

### Legacy Fields

Some content may have legacy fields from previous systems:

- `key: tutorial` - Old categorization system (optional, can keep)
- `index: 8111` - Old numbering system (optional, can keep)
- `subcategory` - Still used in docs collection

These fields don't break anything but can be cleaned up gradually.

### Updating Old Content

When updating old content:
1. Add missing required fields
2. Standardize date formats to ISO 8601
3. Convert categories/tags to lowercase-hyphen format
4. Add description and excerpt if missing
5. Update lastmod date

## Best Practices

1. **Be Consistent** - Use the same field names and formats across similar content
2. **Be Descriptive** - Write clear titles and descriptions
3. **Be Complete** - Include all recommended fields, not just required ones
4. **Be Precise** - Use accurate dates, especially for lastmod
5. **Be Organized** - Use categories and tags thoughtfully
6. **Be Valid** - Test with `jekyll build` before committing
7. **Be Current** - Update lastmod when making significant changes

## Additional Resources

- [Jekyll Front Matter Documentation](https://jekyllrb.com/docs/front-matter/)
- [YAML Specification](https://yaml.org/spec/1.2.2/)
- [ISO 8601 Date Format](https://en.wikipedia.org/wiki/ISO_8601)

---

**Last Updated**: 2025-10-13  
**Version**: 1.0.0

