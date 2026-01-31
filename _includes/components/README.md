# Jekyll Include Components

This directory contains reusable Jekyll include components for the IT-Journey site.

## Components

### powered-by.html

Displays a "Powered by" section showing the technologies used to build the site.

**Features:**
- Bootstrap 5 card grid layout (responsive: 1 column mobile, 3 columns desktop)
- Graceful handling of empty version numbers
- Dynamic icons from Bootstrap Icons
- External links with "Learn More" buttons

**Usage:**
```liquid
{% include components/powered-by.html %}
```

**Data Source:**
The component reads from `site.powered_by` array in `_config.yml`:

```yaml
powered_by:
  - name: "Ruby"
    version: "3.2.3"
    url: "https://www.ruby-lang.org/"
    icon: "bi-gem"
  - name: "Jekyll"
    version: "3.9.5"
    url: "https://jekyllrb.com/"
    icon: "bi-joystick"
```

**Fields:**
- `name` (required): Technology name displayed in card title
- `version` (optional): Version number shown as badge (hidden if empty)
- `url` (required): Link to technology website
- `icon` (required): Bootstrap icon class (e.g., `bi-gem`)

## Adding New Components

When adding new components to this directory:

1. Create a descriptive `.html` file with appropriate comments
2. Document the component in this README
3. Follow Bootstrap 5 conventions for styling
4. Ensure accessibility with proper ARIA labels where needed
5. Test responsiveness across breakpoints

---

**Last Updated:** 2026-01-30
