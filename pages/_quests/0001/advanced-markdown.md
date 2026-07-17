---
title: 'Advanced Markdown: Tables, Footnotes & Kramdown'
author: IT-Journey Team
description: 'Go beyond basic Markdown with tables, footnotes, fenced code, callouts, Kramdown attributes, and YAML frontmatter that builds Jekyll pages.'
excerpt: Level up your Markdown with tables, footnotes, fenced code, callouts, and Kramdown power features.
preview: images/previews/advanced-markdown-tables-footnotes-quest-title-ext.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0001'
difficulty: 🟢 Easy
estimated_time: 45-60 minutes
primary_technology: markdown
quest_type: main_quest
quest_series: Documentation Mastery
quest_line: The Web Fundamentals Codex
quest_arc: Forging Your First Website
quest_dependencies:
  required_quests: []
  recommended_quests: []
  unlocks_quests:
  - /quests/0001/seo-optimization/
  - /quests/0001/jekyll-plugins/
skill_focus: fullstack
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Basic Markdown (headings, bold, links, lists)
  - Comfort creating and editing text files
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - A text editor or IDE with Markdown preview
  skill_level_indicators:
  - Some exposure to basic Markdown is helpful
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A Markdown document using tables, footnotes, and fenced code
  skill_demonstrations:
  - Can author a Markdown table and a footnote
  - Can add frontmatter to a Markdown file
  knowledge_checks:
  - Understands what Kramdown adds over plain Markdown
  - Can explain how frontmatter drives a Jekyll page
permalink: /quests/0001/advanced-markdown/
categories:
- Quests
- Documentation
- Markdown
- Beginner
tags:
- '0001'
- markdown
- kramdown
- documentation
- tables
- main_quest
- hands-on
- beginner
keywords:
  primary:
  - '0001'
  - markdown
  - kramdown
  - documentation
  secondary:
  - tables
  - main_quest
  - hands-on
  - beginner
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0001 (1) Quest: Main Quest - Advanced Markdown'
rewards:
  badges:
  - 🏆 Scribe of the Codex - Authored rich, structured documents
  - 🌱 Sprout of the Written Word - Internalized Kramdown and frontmatter
  skills_unlocked:
  - 🛠️ Structured Documentation Authoring
  - 🧠 Frontmatter-Driven Content
  progression_points: 50
  unlocks_features:
  - Access to the publishing quests of Level 0001 Web Fundamentals
layout: quest
redirect_from:
- /quests/0010/advanced-markdown/
---
*Greetings, brave adventurer! Welcome to **Advanced Markdown** - the quest where your plain text grows tables, footnotes, callouts, and metadata. You already know that `# Heading` and `**bold**` work their small magics. Now you will learn the extended syntax that turns Markdown into a serious documentation and publishing tool - the very language every page on IT-Journey is written in.*

*Whether you write READMEs, blog posts, or quest pages like this one, this adventure will teach you the richer dialect - Kramdown and GitHub-flavored extensions - plus the frontmatter that lets a static site generator build whole pages from your words.*

## 📖 The Legend Behind This Quest

*Markdown was created in 2004 to let people write formatted documents in plain text that still reads naturally before it is ever converted to HTML. It was deliberately tiny. But "tiny" left gaps: no tables, no footnotes, no fenced code. So dialects arose. **GitHub-Flavored Markdown** added tables and task lists; **Kramdown** - the engine Jekyll uses - added footnotes, attribute lists, and definition lists. On top of the prose sits **frontmatter**, a block of metadata that tells the site generator the title, layout, and date. Master these and a single text file becomes a fully-built web page.*

*This quest teaches the extended syntax and the frontmatter that drive content-first sites like this one.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Tables** - Build readable, aligned data tables
- [ ] **Footnotes & Task Lists** - Add references and interactive checklists
- [ ] **Fenced Code & Callouts** - Highlight code by language and call out warnings
- [ ] **Frontmatter** - Drive a page's metadata with a YAML block

### Secondary Objectives (Bonus Achievements)
- [ ] **Kramdown Attributes** - Attach classes and ids to elements
- [ ] **Definition Lists** - Render term-and-definition pairs
- [ ] **Liquid Awareness** - Recognize when Markdown meets a templating language

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Author a clean, aligned table from memory
- [ ] Add a footnote and explain where it renders
- [ ] Write a frontmatter block and name what each field controls

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Basic Markdown (headings, bold/italic, links, lists)
- [ ] Comfort creating and editing plain text files
- [ ] Helpful: a basic idea of what HTML and YAML are

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] A text editor with Markdown preview (VS Code recommended)
- [ ] Optional: a Jekyll site to see frontmatter in action

### 🧠 Skill Level Indicators
This **🟢 Easy** quest expects:
- [ ] Beginner-friendly - some exposure to basic Markdown helps
- [ ] Willingness to preview your document as you write
- [ ] Ready for 45-60 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*Markdown is just text, so any editor works. The difference is how you preview the rendered result.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Create a Markdown file to experiment in
mkdir -p ~/md-quest && cd ~/md-quest
touch guide.md
code guide.md   # open in VS Code (or use any editor)
```

**macOS-Specific Notes:**
- In VS Code press `Cmd + K V` to open a side-by-side live preview.
- The built-in Quick Look (`Space` in Finder) renders Markdown too.

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Create a Markdown file to experiment in
mkdir $HOME\md-quest; cd $HOME\md-quest
New-Item guide.md
code guide.md
```

**Windows-Specific Notes:**
- In VS Code press `Ctrl + K V` for a live side-by-side preview.
- GitHub renders any `.md` file you push - a quick way to check syntax.

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Create a Markdown file to experiment in
mkdir -p ~/md-quest && cd ~/md-quest
touch guide.md
code guide.md   # or nano/vim if you prefer
```

**Linux-Specific Notes:**
- Press `Ctrl + K V` in VS Code for live preview.
- `pandoc guide.md -o guide.html` renders Markdown to HTML from the terminal.

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# No setup needed: write Markdown directly on GitHub.
# Create a new file ending in .md in any repo and use the Preview tab,
# or open https://dillinger.io for a live online Markdown editor.
```

**Cloud-Specific Notes:**
- GitHub's editor shows a Preview tab that uses GitHub-Flavored Markdown.
- Note: GitHub and Kramdown differ slightly - test on the engine you publish with.

</details>

## 🧙‍♂️ Chapter 1: Tables, Footnotes & Task Lists - Structured Prose

*Plain Markdown cannot make a table. The extended dialects can, and they add references and checklists too.*

### ⚔️ Skills You'll Forge in This Chapter
- Building aligned tables
- Adding footnotes
- Writing interactive task lists

### 🏗️ Tables and Alignment

A table is rows of pipes. The second row sets alignment with colons:

```markdown
| Feature      | Plain Markdown | Kramdown |
| :----------- | :------------: | -------: |
| Headings     | Yes            | Yes      |
| Tables       | No             | Yes      |
| Footnotes    | No             | Yes      |
```

`:---` left-aligns, `:--:` centers, and `---:` right-aligns that column. **Footnotes** keep your prose clean by moving references to the bottom:

```markdown
Static sites are fast because pages are pre-built.[^speed]

[^speed]: The server sends a finished file instead of building it per request.
```

The `[^speed]` marker renders as a small superscript link that jumps to the note. **Task lists** render as real checkboxes:

```markdown
- [x] Learn tables
- [ ] Learn footnotes
- [ ] Learn frontmatter
```

### 🔍 Knowledge Check: Tables & Footnotes
- [ ] How do you center a single column in a Markdown table?
- [ ] Where does the text of a footnote appear when rendered?
- [ ] What is the difference between `- [ ]` and `- [x]`?

### ⚡ Quick Wins and Checkpoints
- [ ] **Built a table**: A three-column table renders with aligned columns
- [ ] **Added a footnote**: A superscript marker links to a note at the bottom

## 🧙‍♂️ Chapter 2: Fenced Code, Callouts & Kramdown Power - Beyond Prose

*Code needs to be shown verbatim and highlighted; readers need their attention drawn to warnings; and Kramdown lets you attach HTML attributes to any element.*

### ⚔️ Skills You'll Forge in This Chapter
- Fenced code blocks with language hints
- Blockquote-based callouts
- Kramdown attribute lists and definition lists

### 🏗️ Fenced Code and Callouts

A **fenced code block** is three backticks plus a language id. The language enables syntax highlighting:

````markdown
```python
def greet(name):
    return f"Hello, {name}"
```
````

To show backticks themselves (as above), wrap the block in four backticks. **Callouts** are styled blockquotes - many renderers and themes give them color:

```markdown
> **Note:** Kramdown is the default Markdown engine in Jekyll.

> ⚠️ **Warning:** GitHub does not support every Kramdown feature.
```

**Kramdown attribute lists** let you attach a class or id to an element using `{: ... }`:

```markdown
This paragraph gets a CSS class and an id.
{: .lead #intro }

### A heading with an id
{: #custom-anchor }
```

That renders the paragraph as `<p class="lead" id="intro">`, so your CSS or theme can target it. **Definition lists** pair a term with its meaning:

```markdown
Static Site Generator
: A tool that renders source files into a finished website.

Frontmatter
: A YAML metadata block at the top of a content file.
```

### 🔍 Knowledge Check: Code & Kramdown
- [ ] Why add a language id to a fenced code block?
- [ ] What does the Kramdown line `{: .lead #intro }` produce in HTML?
- [ ] How many backticks do you need to display a three-backtick block as text?

### ⚡ Quick Wins and Checkpoints
- [ ] **Highlighted code**: A fenced block shows colored syntax in preview
- [ ] **Added an attribute**: An element carries a class you set with `{: ... }`

## 🧙‍♂️ Chapter 3: Frontmatter-Driven Content - Words That Become Pages

*The leap from "a document" to "a web page" is **frontmatter**: a YAML block fenced by `---` lines at the very top. A static site generator reads it to decide the page's title, layout, and more.*

### ⚔️ Skills You'll Forge in This Chapter
- Writing a frontmatter block
- Understanding how frontmatter drives rendering
- Recognizing Liquid templating inside Markdown

### 🏗️ A Frontmatter Block

Here is a complete content file. Everything between the two `---` lines is metadata; everything after is the body:

```markdown
---
title: My First Real Page
layout: default
date: 2026-06-14
tags: [markdown, jekyll]
---

# {% raw %}{{ page.title }}{% endraw %}

This body is plain Markdown, but the heading above is filled in
from the `title` field in the frontmatter.
```

Jekyll reads `title`, `layout`, and `date`, wraps your body in the named layout, and outputs HTML. The double-brace `{% raw %}{{ page.title }}{% endraw %}` is **Liquid**, Jekyll's templating language - it pulls a value out of the frontmatter and drops it into the page.

Because Liquid tags would otherwise be processed at build time, documentation that wants to *show* Liquid wraps it so it renders literally. In a Jekyll source file you would write:


```liquid
{% raw %}{% for post in site.posts %}{% endraw %}
  - [{% raw %}{{ post.title }}{% endraw %}]({% raw %}{{ post.url }}{% endraw %})
{% raw %}{% endfor %}{% endraw %}
```


The `raw` / `endraw` fence tells Jekyll "print these tags as text, do not execute them" - essential when you are teaching Liquid in a Jekyll-built page like this quest.

### 🔍 Knowledge Check: Frontmatter & Liquid
- [ ] What characters fence a frontmatter block, and where must it appear?
- [ ] What does `{% raw %}{{ page.title }}{% endraw %}` pull from, and who fills it in?
- [ ] Why wrap Liquid examples in a `raw` block inside a Jekyll page?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: A Rich README
**Objective**: Write a `README.md` that uses three extended features.

**Requirements**:
- [ ] At least one table with column alignment
- [ ] At least one footnote
- [ ] At least one fenced code block with a language id

**Validation**: All three render correctly in your editor's preview or on GitHub.

### 🟡 Intermediate Challenge: A Documented Component
**Objective**: Document a small concept using callouts and a definition list.

**Requirements**:
- [ ] A definition list of at least three terms
- [ ] A `Note` and a `Warning` callout
- [ ] One element given a class via a Kramdown attribute list

**Validation**: The definitions render as term/description pairs and the attribute appears in the HTML.

### 🔴 Advanced Challenge: A Frontmatter Page
**Objective**: Create a content file whose page is driven by frontmatter.

**Requirements**:
- [ ] A complete frontmatter block with `title`, `layout`, and `date`
- [ ] Use `{% raw %}{{ page.title }}{% endraw %}` in the body
- [ ] Include a `raw`-wrapped Liquid example for documentation

**Validation**: When built with Jekyll, the title appears from frontmatter and the wrapped Liquid renders as literal text.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Scribe of the Codex** - You authored rich, structured documents
- 🌱 **Sprout of the Written Word** - Kramdown and frontmatter are second nature

**🛠️ Skills Unlocked**:
- **Structured Documentation Authoring** - Tables, footnotes, callouts, and code
- **Frontmatter-Driven Content** - Turn text files into built pages

**🔓 Unlocked Quests**:
- SEO Optimization - Make the content you write discoverable
- Jekyll Plugins - Extend how your Markdown becomes a site

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [SEO Optimization](/quests/0001/seo-optimization/) - Help search engines find your writing

**Explore Side Adventures**:
- ⚔️ [Jekyll Plugins](/quests/0001/jekyll-plugins/) - Add build-time power to your content
- ⚔️ [CSS Styling Basics](/quests/0001/css-styling-basics/) - Style the pages your Markdown becomes

### Character Class Recommendations

**💻 Software Developer**: Continue to [Jekyll Plugins](/quests/0001/jekyll-plugins/)  
**🏗️ System Engineer**: Explore [SEO Optimization](/quests/0001/seo-optimization/)  
**🎨 Frontend Specialist**: Advance to [CSS Styling Basics](/quests/0001/css-styling-basics/)  

## 📚 Resources

### Official Documentation
- [Kramdown Syntax Reference](https://kramdown.gettalong.org/syntax.html) - The engine Jekyll uses
- [GitHub-Flavored Markdown Spec](https://github.github.com/gfm/) - Tables and task lists
- [Jekyll: Front Matter](https://jekyllrb.com/docs/front-matter/) - How metadata drives pages

### Community Resources
- [Markdown Guide](https://www.markdownguide.org/) - Basic and extended syntax explained
- [CommonMark](https://commonmark.org/) - The standardized Markdown core
- [Liquid Documentation](https://shopify.github.io/liquid/) - The templating language Jekyll speaks

### Learning Materials
- [Markdown Tutorial (interactive)](https://www.markdowntutorial.com/) - Practice in your browser
- [Dillinger Online Editor](https://dillinger.io/) - Live preview while you learn

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Wrote a document using tables, footnotes, and fenced code
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0001 - Web Fundamentals]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Unlocks:** [[SEO Optimization]] · [[Jekyll Plugins]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
