# _includes Directory Organization

This directory has been reorganized for better maintainability and clarity. Files are now grouped by functionality into subdirectories.

## Directory Structure

### `core/`

Essential layout components that form the foundation of the site:

- `head.html` - HTML document head with meta tags, scripts, and styles
- `header.html` - Main site header with navigation
- `footer.html` - Site footer (if exists)
- `branding.html` - Site branding and title display

### `navigation/`

All navigation-related components:

- `navbar.html` - Main navigation menu
- `sidebar-left.html` - Left sidebar with dynamic navigation
- `sidebar-right.html` - Right sidebar content
- `sidebar-folders.html` - Dynamic folder structure generation
- `sidebar-categories.html` - Category-based navigation
- `nav_list.html` - Manual navigation list rendering
- `breadcrumbs.html` - Navigation breadcrumbs

### `analytics/`

Analytics and tracking integrations:

- `google-analytics.html` - Google Analytics tracking
- `google-tag-manager-head.html` - GTM head section
- `google-tag-manager-body.html` - GTM body section

### `components/`

Reusable UI components and widgets:

- `searchbar.html` - Search functionality
- `powered-by.html` - "Powered by" credits display
- `quick-index.html` - Quick page index
- `dev-shortcuts.html` - Developer shortcuts
- `info-section.html` - Settings/info modal
- `halfmoon.html` - Dark mode toggle
- `zer0-env-var.html` - Environment variable configuration
- `svg.html` - SVG icon definitions
- `js-cdn.html` - CDN JavaScript libraries

### `content/`

Content-specific features and enhancements:

- `seo.html` - SEO meta tags and structured data
- `toc.html` - Table of contents generation
- `giscus.html` - GitHub Discussions comment system
- `intro.html` - Page introduction section
- `sitemap.html` - Sitemap generation

### `landing/`

Landing page specific components:

- `landing-install-cards.html` - Installation method cards
- `landing-quick-links.html` - Quick links bar

### `docs/`

Documentation and reference materials:

- `bootstrap-docs.html` - Bootstrap documentation (moved from style.html)

## Usage

When including files in layouts or other templates, use the full path:

```liquid
{% include core/head.html %}
{% include navigation/sidebar-left.html %}
{% include components/searchbar.html %}
{% include analytics/google-analytics.html %}
```

## Benefits of This Organization

1. **Logical Grouping**: Related functionality is grouped together
2. **Easier Maintenance**: Finding and editing specific components is simpler
3. **Reduced Conflicts**: Clear separation reduces naming conflicts
4. **Better Documentation**: Each directory has a clear purpose
5. **Scalability**: Easy to add new components to appropriate directories

## Migration Notes

- All include paths in layouts have been updated to reflect the new structure
- The duplicate `toc` file has been removed
- Large Bootstrap documentation moved to `docs/` directory
- No functionality has been changed, only organization
