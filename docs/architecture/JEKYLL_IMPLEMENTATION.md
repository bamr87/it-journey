# Jekyll Implementation Details

This document details how Jekyll is configured and used in the IT-Journey repository, including collections, plugins, themes, and build processes.

## Jekyll Version & Configuration

### Version Information
- **Jekyll Version**: 3.9.5 (via github-pages gem ~> 231)
- **Ruby Version**: 3.2.3
- **GitHub Pages Compatible**: Yes
- **Theme**: `bamr87/zer0-mistakes` (remote theme)

### Configuration Files

#### `_config.yml` (Production)
Main configuration file for production builds and GitHub Pages deployment.

**Key Settings:**
```yaml
remote_theme: "bamr87/zer0-mistakes"
markdown: kramdown
permalink: pretty
collections_dir: pages
```

#### `_config_dev.yml` (Development)
Development-specific overrides for local testing.

**Usage:**
```bash
bundle exec jekyll serve --config _config_dev.yml
```

## Collections System

Jekyll collections organize content into logical groups with specific purposes and URL structures.

### Collection Definitions

All collections are stored in the `pages/` directory (defined by `collections_dir: pages`).

#### `_posts` Collection
Traditional Jekyll blog posts.

```yaml
posts:
  output: true
  permalink: /:collection/:year/:month/:day/:slug/
```

**URL Pattern:** `/posts/2025/10/13/my-post-title/`

**Purpose:** Blog articles, tutorials, journal entries, technical write-ups

**Frontmatter Requirements:** title, date, layout, tags (recommended)

#### `_docs` Collection
Learning resources and reference documentation.

```yaml
docs:
  output: true
  permalink: /:collection/:categories/:name/
```

**URL Pattern:** `/docs/jekyll/jekyll-config/` (if categories: jekyll)

**Purpose:** External tool documentation, reference guides, educational resources

**Note:** Distinct from developer docs in `/docs/` directory

#### `_quests` Collection
Gamified learning experiences with progressive difficulty.

```yaml
quests:
  output: true
  permalink: /:collection/:categories/:name/
```

**URL Pattern:** `/quests/automation/link-health-guardian/`

**Purpose:** Hands-on projects, skill-building exercises, themed learning adventures

**Special Features:**
- Binary level system (0000-1111)
- Fantasy RPG themes
- Achievement tracking
- Multi-platform support

#### `_notebooks` Collection
Jupyter notebooks and interactive code content.

```yaml
notebooks:
  output: true
  permalink: /:collection/:path/:name/
```

**URL Pattern:** `/notebooks/data-science/analysis-example/`

**Purpose:** Runnable code examples, data analysis, interactive tutorials

**Format Support:** .ipynb, .md (converted notebooks)

#### `_notes` Collection
Personal development notes and work-in-progress content.

```yaml
notes:
  output: true
  permalink: /:collection/:path/:name/
```

**URL Pattern:** `/notes/development/feature-idea/`

**Purpose:** Draft content, research notes, experimental ideas

**Visibility:** May be excluded from main navigation

#### `_about` Collection
Information about the IT-Journey project.

```yaml
about:
  output: true
  permalink: /:collection/:categories/:name/
```

**URL Pattern:** `/about/features/mermaid-diagrams/`

**Purpose:** Project information, site documentation, team pages

#### `_quickstart` Collection
Quick reference guides for rapid learning.

```yaml
quickstart:
  output: true
  permalink: /:collection/:name/
```

**URL Pattern:** `/quickstart/jekyll-setup/`

**Purpose:** Fast onboarding, cheat sheets, common task references

#### `_hobbies` Collection
Personal hobby-related content.

```yaml
hobbies:
  output: true
  permalink: /:collection/:categories/:name/
```

**URL Pattern:** `/hobbies/woodworking/project-name/`

**Purpose:** Non-technical personal projects

### Collection Defaults

Default frontmatter values for each collection are set in `_config.yml`:

```yaml
defaults:
  # All files
  - scope:
      path: ""
    values:
      layout: root
      author_profile: false
      read_time: true
      comments: false
      share: true
      related: true

  # Posts-specific
  - scope:
      path: pages/_posts
    values:
      layout: journals
      sidebar:
        nav: dynamic

  # Docs-specific
  - scope:
      path: pages/_docs
    values:
      layout: default
      sidebar:
        nav: docs

  # Quests-specific
  - scope:
      path: pages/_quests
    values:
      layout: default
      sidebar:
        nav: dynamic
```

## Plugins

### Enabled Plugins

Plugins are defined in `_config.yml` and `Gemfile`:

```yaml
plugins:
  - github-pages
  - jekyll-remote-theme
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag
  - jekyll-paginate
  - jekyll-relative-links
```

#### `github-pages`
Meta-gem that includes all GitHub Pages-compatible Jekyll plugins.
- Version: ~> 231
- Includes: jekyll, jekyll-sass-converter, kramdown, liquid, rouge, and more

#### `jekyll-remote-theme`
Enables using themes hosted on GitHub without installing them locally.
- Theme: `bamr87/zer0-mistakes`
- Allows local overrides of theme files

#### `jekyll-feed`
Generates an Atom feed for posts at `/feed.xml`.
- Automatic post discovery
- Configurable via frontmatter

#### `jekyll-sitemap`
Creates sitemap.xml for search engines.
- Automatic page discovery
- Respects frontmatter `sitemap: false` to exclude pages

#### `jekyll-seo-tag`
Adds meta tags for SEO and social media sharing.
- Open Graph tags
- Twitter Card tags
- Canonical URLs
- JSON-LD structured data

#### `jekyll-paginate`
Provides pagination for posts.
```yaml
paginate: 10
paginate_path: "/pages/:num/"
```

#### `jekyll-relative-links`
Converts relative links to proper Jekyll links.
- Automatically finds linked files
- Generates correct URLs

## Markdown Processing

### Kramdown Configuration

```yaml
markdown: kramdown

kramdown:
  input: GFM  # GitHub Flavored Markdown
  header_offset: 0
  toc_levels: 1..6
```

**Features:**
- GitHub Flavored Markdown syntax
- Automatic table of contents generation
- Code syntax highlighting with Rouge
- Footnote support
- Table support with alignment
- Task list support (- [ ] and - [x])

### Syntax Highlighting

Handled by Rouge (included in github-pages gem):
- Automatic language detection
- Support for 200+ languages
- Customizable themes
- Line numbers (via theme)

**Usage in Markdown:**
````markdown
```python
def hello_world():
    print("Hello, IT-Journey!")
```
````

## Theme Integration

### Remote Theme: zer0-mistakes

**Repository:** https://github.com/bamr87/zer0-mistakes

**Theme Structure:**
- Base layouts in theme `_layouts/`
- Base includes in theme `_includes/`
- Base styles in theme `_sass/`
- Assets in theme `assets/`

### Local Overrides

Local files take precedence over theme files:

**Override Priority:**
1. Local `_layouts/javascript.html` → Used
2. Theme `_layouts/default.html` → Used (if no local version)
3. Local `assets/css/custom.css` → Appended to theme CSS
4. Local `_includes/` → Override or extend theme includes

### Theme Configuration

```yaml
theme_skin: "dark"  # Options: air, aqua, contrast, dark, dirt, neon, mint, plum, sunrise

theme_color:
  main: #007bff
  secondary: #6c757d
  # ... additional color definitions
```

## Layouts

### Available Layouts

#### From Theme (zer0-mistakes)
- `root` - Base HTML structure
- `default` - Standard page layout
- `journals` - Blog post layout with metadata
- `collection` - Collection index pages

#### Local Custom Layouts
- `javascript.html` - JavaScript-heavy interactive pages

### Layout Hierarchy

```
root.html (theme)
└── default.html (theme)
    ├── journals.html (theme)
    ├── collection.html (theme)
    └── javascript.html (local)
```

### Layout Usage

Specified in frontmatter:
```yaml
---
layout: journals
---
```

Or via collection defaults in `_config.yml`.

## Includes

### Theme Includes
Provided by zer0-mistakes theme (partial list):
- Navigation components
- Header/footer
- Sidebar
- SEO tags
- Analytics integration

### Local Custom Includes
Located in `_includes/`:
- `content_statistics/` - Content metrics displays
  - `minimal.html`
  - `simple_fixed.html`
  - `static_test.html`
  - `test.html`
  - `ultra_simple.html`
- `content_stats_direct.html` - Direct statistics

### Using Includes

In layouts or content:
```liquid
{% include content_stats_direct.html %}
```

## Data Files

Located in `_data/`, accessible via `site.data`:

### Navigation Data
`_data/navigation/main.yml`:
```yaml
- title: "About"
  url: /about/
- title: "Quests"
  url: /quests/
- title: "Docs"
  url: /docs/
```

**Access in templates:**
```liquid
{% for item in site.data.navigation.main %}
  <a href="{{ item.url }}">{{ item.title }}</a>
{% endfor %}
```

### Other Data Files
- `ui-text.yml` - Interface text and translations
- `prerequisites.yml` - Learning prerequisites
- `statistics_config.yml` - Content statistics configuration

## Assets & SCSS

### SCSS Compilation

Jekyll compiles SCSS to CSS automatically:

**Source:** `assets/css/main.scss`
```scss
---
# Front matter required for Jekyll processing
---

@import "custom";
@import "theme-variables";
// ... additional imports
```

**Output:** `_site/assets/css/main.css`

### Asset Pipeline

1. SCSS files in `_sass/` are imported
2. Theme SCSS is imported automatically
3. Local overrides applied
4. Compiled to single CSS file
5. Served from `_site/assets/`

### Custom Styles

Located in `assets/css/custom.css` for direct CSS or `_sass/custom.scss` for SCSS.

## Build Process

### Local Development Build

```bash
# Standard build
bundle exec jekyll build

# Development server with auto-reload
bundle exec jekyll serve --config _config_dev.yml --livereload

# Production build
JEKYLL_ENV=production bundle exec jekyll build
```

### GitHub Pages Build

Automatic on push to `main` branch:
1. GitHub Actions triggered
2. Jekyll build with `github-pages` gem
3. Output deployed to GitHub Pages
4. Available at configured URL

### Docker Build

```bash
# Start development server
docker-compose up

# Build only
docker-compose run jekyll bundle exec jekyll build
```

## Environment Variables

### `JEKYLL_ENV`

Controls build environment:
- `development` (default) - Development mode
- `production` - Production optimizations

**Usage:**
```liquid
{% if jekyll.environment == "production" %}
  <!-- Production-only code -->
{% endif %}
```

### Custom Environment Variables

Defined in `_config.yml` and accessible via `site.*`:
```yaml
url: 'https://it-journey.dev'
baseurl: ""
port: 4002
```

## Special Features

### Mermaid Diagrams

Enabled via frontmatter:
```yaml
---
mermaid: true
---
```

Then use in content:
```markdown
<div class="mermaid">
graph TD;
    A-->B;
    A-->C;
</div>
```

### MathJax Support

Enabled via frontmatter:
```yaml
---
mathjax: true
---
```

Then use LaTeX syntax:
```markdown
$a^2 + b^2 = c^2$

$$\begin{equation}
E = mc^2
\end{equation}$$
```

### Comments (Giscus)

GitHub Discussions-based comments:
```yaml
gisgus:
  enabled: true
  data-repo-id: "MDEwOlJlcG9zaXRvcnkyODM4MjI1NzM"
  data-category-id: "DIC_kwDOEOrJ7c4CAn8D"
```

## Performance Optimizations

### Incremental Builds

```bash
bundle exec jekyll serve --incremental
```

Only rebuilds changed files (experimental).

### Exclude from Build

In `_config.yml`:
```yaml
exclude:
  - .sass-cache/
  - .jekyll-cache/
  - node_modules/
  - vendor/
  - Gemfile.lock
```

### Caching

Jekyll caches:
- Markdown conversions (`.jekyll-cache/`)
- Sass compilations (`.sass-cache/`)

Delete cache directories to force full rebuild.

## Troubleshooting

### Common Build Issues

**Issue:** Bundle install fails
```bash
# Solution: Update bundler
gem update bundler
bundle install
```

**Issue:** Port already in use
```bash
# Solution: Use different port
bundle exec jekyll serve --port 4003
```

**Issue:** Theme not loading
```bash
# Solution: Clear cache and rebuild
rm -rf .jekyll-cache _site
bundle exec jekyll serve
```

### Debug Mode

```bash
# Verbose output
bundle exec jekyll serve --verbose

# Show configuration
bundle exec jekyll serve --config _config_dev.yml --verbose
```

## Best Practices

### Configuration
- Keep sensitive data out of `_config.yml`
- Use environment variables for secrets
- Test with `_config_dev.yml` before deploying

### Collections
- Use appropriate collection for content type
- Set proper permalinks in collection config
- Define collection defaults to reduce repetition

### Performance
- Optimize images before committing
- Use incremental builds during development
- Exclude unnecessary files from build

### Theme Customization
- Override only what you need
- Keep customizations in local files
- Document custom includes and layouts

## Additional Resources

- [Jekyll Official Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Kramdown Syntax](https://kramdown.gettalong.org/syntax.html)
- [Liquid Template Language](https://shopify.github.io/liquid/)
- [zer0-mistakes Theme](https://github.com/bamr87/zer0-mistakes)

---

**Last Updated**: 2025-10-13  
**Version**: 1.0.0

