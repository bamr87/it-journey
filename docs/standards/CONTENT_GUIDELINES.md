# Content Guidelines

This document establishes writing style, formatting conventions, and content standards for the IT-Journey repository.

## Writing Style

### Voice and Tone

**Educational and Encouraging**
- Write in a friendly, approachable manner
- Encourage learning and experimentation
- Acknowledge that mistakes are part of learning
- Use "we" and "you" to create connection

**Example:**
```markdown
✅ Good: "Let's explore how Jekyll collections work. You'll find they make content organization much easier."
❌ Avoid: "Jekyll collections are a feature that developers should understand."
```

**Clear and Concise**
- Use simple language when possible
- Define technical terms on first use
- Break complex concepts into smaller chunks
- Prefer active voice over passive voice

**Example:**
```markdown
✅ Good: "Jekyll converts Markdown files into static HTML pages."
❌ Avoid: "Markdown files are converted into static HTML pages by Jekyll."
```

**Inclusive and Professional**
- Use gender-neutral language
- Avoid assumptions about prior knowledge
- Respect different learning styles and paces
- Welcome contributors of all skill levels

### Audience Considerations

**For Beginners:**
- Provide context and background
- Define acronyms and technical terms
- Include "why" along with "how"
- Offer multiple examples

**For Intermediate Learners:**
- Focus on practical applications
- Explain trade-offs and alternatives
- Reference additional resources
- Connect concepts to real-world scenarios

**For Advanced Users:**
- Provide technical depth
- Discuss edge cases and optimization
- Reference source code and documentation
- Encourage contribution and extension

## Markdown Conventions

### Headings

Use ATX-style headings with a space after the `#`:

```markdown
# H1: Page Title (one per document)
## H2: Major Sections
### H3: Subsections
#### H4: Sub-subsections
##### H5: Minor subdivisions
###### H6: Rarely used
```

**Guidelines:**
- One H1 per document (matches frontmatter title)
- Don't skip heading levels (H2 → H4)
- Use sentence case for headings
- Be descriptive and scannable

**Examples:**
```markdown
✅ Good: "## Setting Up Your Development Environment"
❌ Avoid: "## Setup" (too vague)
❌ Avoid: "## SETTING UP YOUR DEVELOPMENT ENVIRONMENT" (all caps)
```

### Paragraphs

- Use blank lines to separate paragraphs
- Keep paragraphs focused on one idea
- Aim for 2-5 sentences per paragraph
- Use line breaks within paragraphs only when necessary

```markdown
This is the first paragraph. It introduces a concept.

This is the second paragraph. It expands on the concept with details.

This is the third paragraph. It provides an example or conclusion.
```

### Lists

**Unordered Lists:**
Use `-` for consistency:
```markdown
- First item
- Second item
- Third item
  - Nested item
  - Another nested item
- Fourth item
```

**Ordered Lists:**
Use `1.` for all items (Markdown auto-numbers):
```markdown
1. First step
1. Second step
1. Third step
   1. Sub-step
   1. Another sub-step
1. Fourth step
```

**Task Lists:**
For checklists and to-do items:
```markdown
- [ ] Incomplete task
- [x] Completed task
- [ ] Another task
```

### Emphasis

**Bold** for emphasis and key terms:
```markdown
**Important:** Always test your changes locally before committing.
```

*Italic* for subtle emphasis or citations:
```markdown
The *Jekyll documentation* recommends using collections for this purpose.
```

**Avoid:**
- ALL CAPS for emphasis (use bold instead)
- Excessive use of bold or italic
- Mixing asterisks and underscores for same purpose

### Links

**Internal Links (within repository):**
```markdown
See the [Repository Structure](architecture/REPOSITORY_STRUCTURE.md) for details.

[Quest documentation](../pages/_quests/README.md)
```

**External Links:**
```markdown
Read the [Jekyll documentation](https://jekyllrb.com/docs/) for more information.
```

**Link Best Practices:**
- Use descriptive link text (not "click here")
- Prefer relative paths for internal links
- Check links periodically for validity
- Use reference-style links for repeated URLs

```markdown
<!-- Reference-style links -->
Check out [Jekyll docs][jekyll] and [GitHub Pages][gh-pages].

[jekyll]: https://jekyllrb.com/docs/
[gh-pages]: https://docs.github.com/en/pages
```

### Code Blocks

**Inline Code:**
Use backticks for commands, file names, and code snippets:
```markdown
Run `bundle exec jekyll serve` to start the development server.

Edit the `_config.yml` file to change site settings.

The `collections_dir` variable defines where collections are stored.
```

**Fenced Code Blocks:**
Always specify the language for syntax highlighting:

````markdown
```bash
cd it-journey
bundle install
bundle exec jekyll serve
```

```yaml
collections:
  posts:
    output: true
    permalink: /:collection/:year/:month/:day/:slug/
```

```python
def calculate_stats(links):
    total = len(links)
    broken = sum(1 for link in links if link.is_broken)
    return total, broken
```
````

**Supported Languages:**
bash, python, ruby, javascript, yaml, json, markdown, html, css, scss, liquid, diff

**Code Block Best Practices:**
- Always specify language for syntax highlighting
- Keep examples short and focused
- Add comments to explain complex code
- Include context and expected output when helpful

### Blockquotes

Use for callouts, notes, warnings, and quotes:

```markdown
> **Note:** This feature requires Jekyll 3.9 or higher.

> "The best way to learn is by doing." - Ancient Proverb

> **Warning:** This operation will delete all cached files.
```

**Callout Types:**
```markdown
> **Note:** Informational message
> **Tip:** Helpful suggestion
> **Warning:** Caution about potential issues
> **Important:** Critical information
```

### Tables

Use tables for structured data:

```markdown
| Command | Description | Example |
|---------|-------------|---------|
| `build` | Build the site | `jekyll build` |
| `serve` | Start dev server | `jekyll serve` |
| `clean` | Clean the site | `jekyll clean` |
```

**Table Guidelines:**
- Use header row with descriptive labels
- Align columns for readability in source
- Keep tables simple (max 5-6 columns)
- For complex data, consider alternative formats

### Horizontal Rules

Use three or more hyphens for section breaks:

```markdown
---
```

Use sparingly - prefer headings for structure.

### Images

**Basic Syntax:**
```markdown
![Alt text describing image](/assets/images/diagram.png)
```

**With Width Specification (Jekyll/Kramdown):**
```markdown
![Screenshot of dashboard](/assets/images/dashboard.png){:width="700px"}
```

**Image Best Practices:**
- Always include descriptive alt text
- Optimize images before committing (compress, resize)
- Use relative paths for local images
- Store images in `assets/images/` with descriptive names
- Preferred formats: PNG for screenshots, SVG for diagrams, JPG for photos
- Maximum width: 1200px for full-width images

## Content Structure

### Document Organization

**Standard Document Structure:**

```markdown
---
# Frontmatter
title: "Document Title"
date: 2025-10-13T00:00:00.000Z
---

# Document Title

Brief introduction paragraph explaining what this document covers.

## Overview

High-level summary of the content.

## Main Section 1

Detailed content for first major topic.

### Subsection 1.1

More specific information.

### Subsection 1.2

Additional details.

## Main Section 2

Second major topic.

## Conclusion

Wrap-up or next steps.

## Additional Resources

- Links to related documents
- External references

---

**Last Updated**: 2025-10-13  
**Version**: 1.0.0
```

### Tutorials and Guides

**Tutorial Structure:**

```markdown
# Tutorial Title

Brief description of what learner will accomplish.

## Prerequisites

- List required knowledge
- List required tools
- Estimated time to complete

## Step 1: Setup

Clear instructions for first step.

```bash
# Commands with expected output
```

Expected output or result.

## Step 2: Implementation

Next step instructions.

## Step 3: Testing

How to verify it works.

## Troubleshooting

Common issues and solutions.

## Next Steps

Where to go from here.
```

### Quest Content

**Quest-Specific Format:**

```markdown
# Quest Title

*Quest Level: 0101 | Difficulty: Intermediate | XP: 500*

## The Story

Engaging narrative that frames the technical challenge.

## Quest Objectives

- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

## Prerequisites

Knowledge and tools needed.

## The Journey

### Chapter 1: Beginning

First stage of the quest with instructions.

### Chapter 2: Challenge

Main technical implementation.

### Chapter 3: Mastery

Advanced features or optimization.

## Victory Conditions

How to know you've completed the quest successfully.

## Achievements Unlocked

- Achievement 1: Description
- Achievement 2: Description

## Continue Your Adventure

Links to related quests or next steps.
```

## Asset Management

### Image Guidelines

**Naming Conventions:**
```
descriptive-name-component.ext

Examples:
dashboard-overview.png
mermaid-diagram-workflow.svg
quest-level-progression-chart.png
```

**Organization:**
```
assets/
├── images/
│   ├── posts/           # Blog post images
│   ├── quests/          # Quest-specific images
│   ├── docs/            # Documentation images
│   └── screenshots/     # UI screenshots
├── svg/                 # SVG graphics and icons
└── gif/                 # Animated GIFs (use sparingly)
```

**Optimization:**
- Compress PNGs: Use tools like `pngquant` or `optipng`
- Compress JPGs: 85% quality is usually sufficient
- Prefer SVG for diagrams and icons (scalable, small file size)
- Limit animated GIFs (large file sizes affect performance)

### Code Examples

**Complete and Runnable:**
Provide complete, working examples when possible:

```python
# Complete example with context
def check_links(urls):
    """Check a list of URLs and return broken links.
    
    Args:
        urls: List of URLs to check
        
    Returns:
        List of broken URL dictionaries
    """
    broken = []
    for url in urls:
        if not is_valid(url):
            broken.append({'url': url, 'status': 'broken'})
    return broken
```

**Snippet with Context:**
If showing partial code, indicate what's omitted:

```python
# ... previous code ...

def process_results(results):
    # Process the link checking results
    total = len(results)
    broken = sum(1 for r in results if r['status'] == 'broken')
    return {'total': total, 'broken': broken}

# ... additional code ...
```

## Special Content Features

### Mermaid Diagrams

Enable in frontmatter and use in content:

```yaml
---
mermaid: true
---
```

```markdown
<div class="mermaid">
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
</div>
```

**Diagram Guidelines:**
- Keep diagrams simple and focused
- Use consistent naming and styling
- Add diagram title or caption
- Provide text alternative for accessibility

### Mathematical Notation

Enable in frontmatter and use LaTeX syntax:

```yaml
---
mathjax: true
---
```

```markdown
Inline math: $E = mc^2$

Display math:
$$
\begin{equation}
\frac{d}{dx}(x^2) = 2x
\end{equation}
$$
```

### Quest-Specific Elements

**Binary Level System:**
```markdown
**Quest Level:** 0101 (Binary: 5 in decimal)

Level progression:
- 0000 (0): Foundation
- 0001 (1): Beginner
- 0010 (2): Novice
- 0011 (3): Intermediate
- 0100 (4): Advanced
- 0101 (5): Expert
```

**Fantasy Theme Elements:**
```markdown
⚔️ **The Challenge:** Your task, brave developer...

🏆 **Reward:** Upon completion, you shall gain...

🗺️ **The Path Forward:** Your next adventure awaits...
```

## Link Formatting

### Internal Links

**To Other Collections:**
```markdown
See the [Link Guardian Quest](../../_quests/link-guardian.md) for details.
```

**Within Same Collection:**
```markdown
Check out the [previous post](./2025-10-12-setup-guide.md) in this series.
```

**To Documentation:**
```markdown
Review the [Repository Structure](../../docs/architecture/REPOSITORY_STRUCTURE.md).
```

### External Links

**With Context:**
```markdown
According to the [Jekyll documentation](https://jekyllrb.com/docs/collections/), collections are...
```

**Opening in New Tab (when appropriate):**
```markdown
Visit the [IT-Journey website](https://it-journey.dev){:target="_blank"} for more information.
```

## Accessibility

### Alt Text for Images

**Descriptive and Specific:**
```markdown
✅ Good: ![Dashboard showing 95% link success rate with 3 broken links highlighted in red](/path/to/image.png)

❌ Avoid: ![dashboard](/path/to/image.png)
❌ Avoid: ![image](/path/to/image.png)
```

### Semantic Structure

- Use proper heading hierarchy
- Use lists for lists (not paragraphs with bullets)
- Use tables for tabular data
- Provide text alternatives for diagrams

### Color and Contrast

- Don't rely solely on color to convey information
- Ensure sufficient contrast in images
- Use emoji thoughtfully (screen readers announce them)

## Version Control

### Commit Messages

When committing content:

```bash
# Good commit messages
git commit -m "Add Jekyll collections tutorial to docs"
git commit -m "Update link guardian quest with troubleshooting section"
git commit -m "Fix broken links in setup documentation"

# Avoid vague messages
git commit -m "Update files"
git commit -m "Changes"
git commit -m "Fix"
```

### Content Updates

When updating existing content:
1. Update the `lastmod` field in frontmatter
2. Document significant changes in commit message
3. Test links and code examples
4. Verify formatting renders correctly

## Quality Checklist

Before submitting content, verify:

- [ ] Frontmatter is complete and valid
- [ ] Spelling and grammar checked
- [ ] Links are working (internal and external)
- [ ] Code examples are tested and working
- [ ] Images are optimized and have alt text
- [ ] Markdown formatting is correct
- [ ] Headings use proper hierarchy
- [ ] Document follows style guidelines
- [ ] Local build succeeds (`bundle exec jekyll serve`)

## Common Patterns

### File Path References

When mentioning files, use inline code:

```markdown
The main configuration is in `_config.yml`.

Scripts are located in the `scripts/` directory.

Edit `pages/_posts/2025-10-13-my-post.md` to update the post.
```

### Command Examples

Show commands with context:

```markdown
To start the development server:

```bash
cd it-journey
bundle exec jekyll serve --config _config_dev.yml
```

This will start Jekyll on port 4002 (configured in `_config_dev.yml`).
```

### Expected Output

Show expected output after commands:

```markdown
Run the link checker:

```bash
python3 scripts/validation/link-checker.py --scope website
```

Expected output:
```
[INFO] Starting link health check...
[INFO] Scope: website
[INFO] Found 1,250 links to check
[SUCCESS] Link checking completed
[INFO] Results: 1,245 valid, 5 broken
```
```

## Additional Resources

- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/)
- [Kramdown Syntax](https://kramdown.gettalong.org/syntax.html)
- [Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

**Last Updated**: 2025-10-13  
**Version**: 1.0.0

