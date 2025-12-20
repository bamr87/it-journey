
# IT-Journey Data Directory

This directory contains data files and scripts for the IT-Journey Jekyll site, including dynamic content statistics generation.

## 📊 Content Statistics System

The content statistics system automatically analyzes all posts and generates comprehensive metrics that can be displayed throughout the site.

### Files

- **`generate_statistics.rb`** - Ruby script that analyzes all posts and generates statistics
- **`generate_statistics.sh`** - Bash wrapper script for easy execution
- **`statistics_config.yml`** - Configuration file defining categories, mappings, and display preferences
- **`content_statistics.yml`** - Auto-generated statistics data file (updated when script runs)

### Usage

#### Generating Statistics

Run the statistics generator:
```bash
# From the project root
bash _data/generate_statistics.sh

# Or directly with Ruby
ruby _data/generate_statistics.rb
```

#### Displaying Statistics

Three display templates are available:

1. **Simple Display** (recommended for most uses):
   ```liquid
   {% include content_statistics/simple.html %}
   ```

2. **Summary Cards** (visual card layout):
   ```liquid
   {% include content_statistics/summary.html %}
   ```

3. **Detailed Analysis** (full statistical breakdown):
   ```liquid
   {% include content_statistics/detailed.html %}
   ```

### Configuration

Edit `statistics_config.yml` to customize:

- **Focus area mappings** - Keywords that map to content categories
- **Skill level detection** - Terms that indicate difficulty levels
- **Content type classification** - Rules for categorizing content
- **Display preferences** - Limits and highlighting options

Example configuration:
```yaml
focus_areas:
  "AI & Machine Learning":
    - ai
    - machine-learning
    - artificial-intelligence
  "Web Development":
    - web
    - javascript
    - jekyll
```

### Data Structure

The generated `content_statistics.yml` contains:

```yaml
generated_at: timestamp
total_posts: number
published: number
drafts: number
categories: 
  category_name: count
tags:
  tag_name: count
focus_areas:
  area_name: count
skill_levels:
  level_name: count
content_types:
  type_name: count
date_range:
  earliest: year
  latest: year
  span_years: number
# ... and more
```

### Automation

To automatically update statistics:

1. **With Git Hooks** - Add to `.git/hooks/pre-commit`:
   ```bash
   #!/bin/bash
   cd "$(git rev-parse --show-toplevel)"
   bash _data/generate_statistics.sh
   git add _data/content_statistics.yml
   ```

2. **With GitHub Actions** - Add to workflow:
   ```yaml
   - name: Generate Statistics
     run: |
       bash _data/generate_statistics.sh
       git add _data/content_statistics.yml
       git commit -m "Update content statistics" || exit 0
   ```

3. **With Jekyll Build** - Add to `_config.yml`:
   ```yaml
   plugins:
     - jekyll-hook
   
   # Custom hook to run before build
   hooks:
     before_build: bash _data/generate_statistics.sh
   ```

### Extending the System

#### Adding New Focus Areas

1. Edit `statistics_config.yml`
2. Add new area with keywords:
   ```yaml
   focus_areas:
     "New Technology Area":
       - keyword1
       - keyword2
   ```

#### Custom Analysis

The Ruby script can be extended with new analysis methods:

```ruby
def analyze_custom_metric(frontmatter)
  # Custom analysis logic
  if meets_criteria(frontmatter)
    @stats['custom_metric'] ||= 0
    @stats['custom_metric'] += 1
  end
end
```

#### New Display Templates

Create custom templates in `_includes/content_statistics/`:

```liquid
<!-- _includes/content_statistics/chart.html -->
{% assign stats = site.data.content_statistics %}
<!-- Custom visualization logic -->
```

### Troubleshooting

#### Common Issues

1. **Ruby not found**: Install Ruby 2.6+ 
2. **YAML parsing errors**: Check post frontmatter syntax
3. **File permissions**: Ensure scripts are executable
4. **Missing posts**: Verify `pages/_posts` directory exists

#### Debug Mode

Enable verbose output:
```bash
VERBOSE=1 ruby _data/generate_statistics.rb
```

### Performance

- **Generation time**: ~1-2 seconds for 100+ posts
- **File size**: ~10-20KB for comprehensive statistics
- **Cache**: Consider caching in CI/CD for large sites

## Navigation Data

The `navigation/` directory contains navigation menu configurations for different sections of the site. These are used by the theme's sidebar system.

### Navigation Files

| File | Purpose | Sidebar Config (`_config.yml`) | Collection/Section |
|------|---------|-------------------------------|-------------------|
| `main.yml` | Main site header navigation | Default for all pages | Site-wide header |
| `home.yml` | Home page sidebar navigation | N/A (used in header) | `/home/` page |
| `about.yml` | About section sidebar | `pages/_about` | `/about/` pages |
| `docs.yml` | Documentation sidebar | `pages/_docs` | `/docs/` pages |
| `posts.yml` | Posts/blog category navigation | N/A (uses `searchCats` mode) | `/posts/` pages |
| `quests.yml` | Quest system navigation by level | `pages/_quests` | `/quests/` pages |
| `quickstart.yml` | Quick-start guides navigation | `pages/_quickstart` | `/quickstart/` pages |
| `notebooks.yml` | Notes and notebooks navigation | `pages/_notes`, `pages/_notebooks` | `/notes/`, `/notebooks/` |
| `hobbies.yml` | Hobbies section navigation | `pages/_hobbies` | `/hobbies/` pages |

### Sidebar Navigation Modes

The theme supports multiple sidebar navigation modes configured in `_config.yml`:

| Mode | Description | Navigation Source |
|------|-------------|-------------------|
| `dynamic` | Auto-generated from folder structure | `sidebar-folders.html` |
| `searchCats` | Category-based navigation | `sidebar-categories.html` |
| `<filename>` | Manual navigation file | `_data/navigation/<filename>.yml` |

### Navigation Structure

Each navigation file uses a YAML array structure:
```yaml
- title: Section Name
  icon: icon-name    # Optional Bootstrap icon
  url: /section/     # Main section URL
  sublinks:          # Optional child links
    - title: Child Page
      url: /section/child/
```

### Updating Navigation

When adding new pages or collections:
1. Add the page with proper frontmatter and permalink
2. Update the relevant navigation file in `_data/navigation/`
3. If needed, update sidebar configuration in `_config.yml` defaults
4. Test navigation rendering locally with `bundle exec jekyll serve`

**Last Updated:** 2025-12-20

## Schema Data

The `schema/` directory contains structured data schemas used throughout the site for consistent data formatting.