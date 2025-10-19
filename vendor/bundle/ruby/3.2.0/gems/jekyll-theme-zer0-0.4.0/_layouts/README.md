# Layout Files Documentation

This directory contains the Jekyll layout templates for the Zer0-Pages theme.  
Each layout has been organized with comprehensive comments explaining the template logic,  
structure, and usage patterns.

## Layout Hierarchy

```text
root.html (base template)
├── default.html (sidebar layout)
│   ├── journals.html (blog posts)
│   ├── collection.html (collection pages)
│   └── javascript.html (JavaScript demos)
├── home.html (homepage)
├── blog.html (blog homepage)
├── landing.html (landing pages)
├── stats.html (statistics dashboard)
└── index.html (search pages)
```

## Layout Files Overview

### 🏗️ Core Layouts

#### `root.html`

- **Purpose**: Base HTML structure for all pages
- **Features**: Bootstrap 5 dark theme, SEO optimization, scroll spy
- **Dependencies**: head.html, header.html, footer.html, js-cdn.html
- **Usage**: Inherited by all other layouts

#### `default.html`

- **Purpose**: Standard content layout with sidebars
- **Features**: Three-column responsive layout, navigation, table of contents
- **Dependencies**: sidebar-left.html, intro.html, sidebar-right.html
- **Usage**: Documentation pages, standard content

### 📝 Content Layouts

#### `journals.html`

- **Purpose**: Blog post and article display
- **Features**: Article structure, post navigation, comment system
- **Dependencies**: giscus.html for comments
- **Usage**: Individual blog posts and articles

#### `collection.html`

- **Purpose**: Collection listing with card grid
- **Features**: Responsive cards, sorting, preview images
- **Dependencies**: Bootstrap card components
- **Usage**: Portfolio, projects, grouped content

#### `blog.html`

- **Purpose**: Magazine-style blog homepage
- **Features**: Featured posts, sidebar, responsive design
- **Dependencies**: sidebar-categories.html, navigation data
- **Usage**: Blog index and homepage

### 🎯 Specialized Layouts

#### `home.html`

- **Purpose**: Clean homepage template
- **Features**: Minimal structure, RSS feed link
- **Dependencies**: None
- **Usage**: Site homepage, landing content

#### `landing.html`

- **Purpose**: Marketing pages with visual effects
- **Features**: Particles.js background, offcanvas navigation
- **Dependencies**: particles.js, sidebar-left.html
- **Usage**: Product pages, campaigns, portfolios

#### `index.html`

- **Purpose**: Search and indexing pages
- **Features**: Full-width container, search optimization
- **Dependencies**: Search engine integration
- **Usage**: Search results, site indexes

#### `stats.html`

- **Purpose**: Statistics and analytics dashboard
- **Features**: Full-width responsive layout, modular statistics components
- **Dependencies**: Bootstrap 5, Bootstrap Icons, Jekyll data files
- **Usage**: Site analytics, content metrics, performance dashboards

#### `javascript.html`

- **Purpose**: JavaScript demonstration pages
- **Features**: Interactive elements, code examples
- **Dependencies**: Custom JavaScript functions
- **Usage**: Tutorials, interactive demos

## Comment Organization Standards

Each layout file now includes:

### 1. Header Documentation Block

```html
<!--
  ===================================================================
  LAYOUT NAME - Brief description
  ===================================================================
  
  File: filename.html
  Path: _layouts/filename.html
  Inherits: parent-layout.html
  Purpose: Detailed purpose explanation
  
  Template Logic:
  - Key functionality points
  - Responsive behavior
  - Content organization
  
  Dependencies:
  - Include files used
  - External libraries
  - Required data/configuration
  ===================================================================
-->
```

### 2. Section Comments

```html
<!-- ================================ -->
<!-- SECTION NAME                     -->
<!-- ================================ -->
<!-- Description of what this section does -->
```

### 3. Subsection Comments

```html
<!-- ========================== -->
<!-- SUBSECTION NAME            -->
<!-- ========================== -->
<!-- Specific functionality notes -->
```

### 4. Inline Comments

```html
<!-- Explain complex logic or conditional statements -->
{% if condition %}
    <!-- Why this condition exists and what it affects -->
{% endif %}
```

## Template Logic Patterns

### Conditional Content Display

- Use descriptive comments for complex conditionals
- Explain the business logic behind template decisions
- Document fallback behaviors

### Loop Processing

- Explain data source and filtering logic
- Document sorting and limiting operations
- Note performance considerations

### Include Integration

- Document which includes are used and why
- Explain parameter passing to includes
- Note dependencies between includes

### Bootstrap Integration

- Document responsive behavior
- Explain grid system usage
- Note accessibility considerations

## Best Practices

1. **Documentation First**: Every layout should be self-documenting
2. **Consistent Structure**: Follow the established comment hierarchy
3. **Explain Intent**: Don't just describe what code does, explain why
4. **Update Comments**: Keep documentation current with code changes
5. **Template Logic**: Explain complex Liquid template operations
6. **Dependencies**: Document all external dependencies and includes
7. **Responsive Design**: Note mobile/desktop behavior differences
8. **Performance**: Comment on loading order and optimization

## Maintenance Guidelines

- Update comments when modifying layouts
- Test responsive behavior across devices
- Validate HTML5 semantic structure
- Check accessibility compliance
- Monitor Bootstrap version compatibility
- Update documentation for new features

---

*These layouts follow the Zer0-Mistakes theme standards for maintainable,  
documented, and responsive Jekyll templates.*
