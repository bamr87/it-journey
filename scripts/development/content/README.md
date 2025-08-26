# Post Organizer Utility

A comprehensive utility to organize Jekyll markdown posts based on frontmatter metadata. This tool automatically sorts posts into subdirectories based on their `section` field and renames them using their slug values.

## 🎯 Features

- **Automatic Organization**: Moves posts to subdirectories based on `section` frontmatter
- **Smart Slug Extraction**: Extracts slugs from `permalink`, `slug`, `title`, or filename
- **Validation**: Only processes files with valid sections from your posts.yml config
- **Comprehensive Logging**: Tracks all operations, skipped files, and errors
- **Dry Run Mode**: Preview changes before applying them
- **Flexible Configuration**: Supports custom posts directories and config files
- **Error Handling**: Gracefully handles missing fields and invalid data

## 📁 File Structure

```
scripts/development/content/
├── organize-posts.py       # Main Python script
├── organize-posts.sh       # Bash wrapper script
├── requirements.txt        # Python dependencies
└── README.md              # This documentation
```

## 🚀 Quick Start

### Using the Bash Wrapper (Recommended)

```bash
# Navigate to the IT-Journey root directory
cd /path/to/it-journey

# Run with dry-run to preview changes
./scripts/development/content/organize-posts.sh --dry-run

# Run the actual organization
./scripts/development/content/organize-posts.sh
```

### Using Python Directly

```bash
# Install dependencies
pip install -r scripts/development/content/requirements.txt

# Run the script
python3 scripts/development/content/organize-posts.py --dry-run
```

## 📋 Requirements

- **Python 3.6+**
- **PyYAML library** (`pip install pyyaml`)
- Jekyll site with posts in `pages/_posts/` directory
- Posts configuration file at `_data/navigation/posts.yml`

## 🛠️ Usage Options

### Bash Script Options

```bash
./organize-posts.sh [OPTIONS]

OPTIONS:
    -d, --posts-dir PATH     Path to posts directory
    -c, --config-file PATH   Path to posts.yml config file
    -n, --dry-run           Preview changes without moving files
    -i, --install-deps      Install Python dependencies only
    -h, --help              Show help message
```

### Python Script Options

```bash
python3 organize-posts.py [OPTIONS]

OPTIONS:
    --posts-dir PATH        Path to posts directory (default: pages/_posts)
    --config-file PATH      Path to posts.yml configuration file
    --dry-run              Show what would be done without moving files
```

## 📊 How It Works

### 1. Frontmatter Analysis

The script analyzes each markdown file's YAML frontmatter:

```yaml
---
title: "My Blog Post"
section: technology
permalink: /posts/my-blog-post/
---
```

### 2. Section Validation

Validates the `section` field against your `posts.yml` configuration:

```yaml
- title: Technology
  icon: tech
  url: /posts/tech/
- title: Business
  icon: cash
  url: /posts/business/
```

### 3. Slug Extraction

Extracts slug in this priority order:
1. From `permalink` field (last segment)
2. From explicit `slug` field
3. Generated from `title` field
4. Generated from filename (without date prefix)

### 4. File Organization

Moves files to structure like:
```
pages/_posts/
├── technology/
│   ├── my-tech-post.md
│   └── another-tech-post.md
├── business/
│   ├── business-strategy.md
│   └── market-analysis.md
└── world/
    └── global-trends.md
```

## ⚠️ File Processing Rules

### Files are PROCESSED when they have:
- ✅ Valid YAML frontmatter
- ✅ A `section` field with a value matching posts.yml
- ✅ Determinable slug from permalink, slug, title, or filename

### Files are SKIPPED when they:
- ❌ Don't have valid YAML frontmatter
- ❌ Don't have a `section` field
- ❌ Have an invalid section (not in posts.yml)
- ❌ Can't determine a slug

### Error Handling:
- 🔴 Files with processing errors are logged
- 🔄 Target files that already exist are not overwritten
- 📝 All operations are logged to `post-organization.log`

## 📝 Example Output

```
2024-08-24 10:30:15 - INFO - Starting post organization in: /path/to/pages/_posts
2024-08-24 10:30:15 - INFO - Found 45 markdown files to process
2024-08-24 10:30:15 - INFO - Processing: 2021-10-27-build-die-repeat.md
2024-08-24 10:30:15 - INFO - Created/verified directory: /path/to/pages/_posts/technology
2024-08-24 10:30:15 - INFO - Moved: 2021-10-27-build-die-repeat.md -> /path/to/pages/_posts/technology/build-destroy-repeat-mastery.md

============================================================
POST ORGANIZATION SUMMARY
============================================================
Successfully processed: 38 files
  ✓ 2021-10-27-build-die-repeat.md -> technology/build-destroy-repeat-mastery.md
  ✓ 2023-03-17-penrose-triangle.md -> technology/penrose-triangle-impossible-geometry.md

Skipped: 7 files
  ⚠ 2024-05-09-bootstrap-your-theme-and-character.md: No valid section found in frontmatter
    Section value: 'None'

Valid sections: ['business', 'home', 'tech', 'technology', 'world']
============================================================
```

## 🔧 Configuration

### Posts Configuration File

The script reads valid sections from your `_data/navigation/posts.yml`:

```yaml
- title: Home
  icon: home
  url: /posts/
- title: Technology
  icon: tech
  url: /posts/tech/
- title: Business
  icon: cash
  url: /posts/business/
- title: World
  icon: world
  url: /posts/world/
```

### Custom Configuration

You can specify a custom config file:

```bash
./organize-posts.sh --config-file /path/to/custom-posts.yml
```

## 🚨 Safety Features

### Dry Run Mode
Always test with `--dry-run` first:

```bash
./organize-posts.sh --dry-run
```

### Backup Recommendation
Consider backing up your posts before running:

```bash
cp -r pages/_posts pages/_posts.backup
```

### Logging
All operations are logged to `post-organization.log` for audit trails.

## 🐛 Troubleshooting

### Common Issues

**PyYAML Not Found**
```bash
# Install the required dependency
pip install pyyaml
```

**Permission Denied**
```bash
# Make the script executable
chmod +x scripts/development/content/organize-posts.sh
```

**Invalid Section Values**
- Check your posts.yml file structure
- Verify section names match exactly
- Use `--dry-run` to see which sections are detected

**Files Not Moving**
- Verify frontmatter syntax is valid YAML
- Check that section field exists and has a valid value
- Ensure slug can be determined from the post

### Debug Steps

1. Run with `--dry-run` to see what would happen
2. Check the log file `post-organization.log`
3. Verify your posts.yml configuration
4. Test with a single file first

## 🔄 Integration with IT-Journey Workflow

This utility is designed to work with the IT-Journey workflow:

1. **Content Creation**: Authors create posts in `pages/_posts/`
2. **Organization**: This script organizes them by section
3. **Publication**: Jekyll builds the organized structure
4. **Maintenance**: Regular organization keeps content structured

## 📚 Related Documentation

- [IT-Journey Content Guidelines](../../../pages/_quests/README.md)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [YAML Frontmatter Spec](https://jekyllrb.com/docs/front-matter/)

## 🤝 Contributing

To improve this utility:

1. Test with various frontmatter configurations
2. Add support for additional slug sources
3. Enhance error handling and validation
4. Add more configuration options

## 📄 License

This utility is part of the IT-Journey project and follows the same license terms.
