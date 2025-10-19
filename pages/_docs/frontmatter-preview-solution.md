# FrontMatter Preview Configuration

This directory contains the implementation for simplified FrontMatter CMS preview functionality in the IT-Journey repository.

## Overview

The goal was to create a systematic way to link the FrontMatter CMS preview button with Jekyll-generated content, providing a consistent and reliable preview experience during development.

## Solution Implemented

Instead of trying to handle Jekyll's complex permalink logic within FrontMatter's templating system, we implemented a **simplified preview directory structure** that:

1. **Standardizes all preview URLs** to `/preview/<collection>/<filename>/`
2. **Automatically generates preview directories** during Jekyll build
3. **Works consistently** regardless of custom permalinks or Jekyll collection settings

## Components

### 1. FrontMatter Configuration (`frontmatter.json`)

Updated the `frontMatter.content.pageFolders` configuration to use a simple, consistent preview path structure:

```json
{
  "title": "posts",
  "previewPath": "/preview/posts/{{pathToken.fileName}}/",
  "path": "[[workspace]]/pages/_posts",
  "contentTypes": ["default"]
}
```

**Key Template Variables:**
- `{{pathToken.fileName}}` - The filename without extension (e.g., "2025-10-19-test-post")
- Collection name is hardcoded in the path for consistency

### 2. Jekyll Preview Generator Plugin (`_plugins/preview_generator.rb`)

A custom Jekyll plugin that runs during the build process to create the preview directory structure:

**Features:**
- Runs only in development environment (`JEKYLL_ENV=development`)
- Processes all Jekyll collections (posts, quests, docs, notes, etc.)
- Creates `/preview/<collection>/<filename>/index.html` for each document
- Copies the fully rendered HTML content to each preview directory
- Provides detailed logging for debugging

**Example Generated Structure:**
```
_site/
  preview/
    posts/
      2025-10-19-test-post/
        index.html
    quests/
      2023-11-23-begin-your-it-journey/
        index.html
    docs/
      example-documentation/
        index.html
```

## Usage

### For Content Creators

1. **Open any markdown file** in VS Code within the configured collections
2. **Click the FrontMatter "Open Preview" button**
3. **Preview opens** at `http://localhost:4002/preview/<collection>/<filename>/`

### For Developers

The preview URLs follow a predictable pattern:
- Posts: `/preview/posts/<filename>/`
- Quests: `/preview/quests/<filename>/`
- Docs: `/preview/docs/<filename>/`
- Notes: `/preview/notes/<filename>/`
- About: `/preview/about/<filename>/`
- Quickstart: `/preview/quickstart/<filename>/`

## Benefits

### ✅ Advantages of This Approach

1. **Simplicity**: No complex templating logic in FrontMatter configuration
2. **Reliability**: Works regardless of Jekyll permalink settings
3. **Consistency**: All preview URLs follow the same pattern
4. **Performance**: Direct file access, no Jekyll routing logic needed
5. **Debugging**: Easy to troubleshoot with predictable URLs
6. **Development Focus**: Optimized for development workflow, not production

### 🔄 Trade-offs

1. **Development Only**: Preview structure only exists during development builds
2. **Disk Space**: Creates duplicate HTML files for preview purposes
3. **Build Time**: Slight increase in Jekyll build time due to file copying
4. **URL Differences**: Preview URLs differ from production URLs

## Configuration Details

### Environment Requirements

- **Jekyll Environment**: Must be set to `development`
- **Docker Setup**: Works with the existing Docker-based Jekyll environment
- **Port**: Jekyll server running on `localhost:4002`

### FrontMatter Template Variables Available

- `{{pathToken.fileName}}` - Filename without extension
- `{{pathToken.relPath}}` - Relative file path
- `{{slug}}` - URL-friendly slug
- `{{date|format}}` - Date formatting (for posts)

## Troubleshooting

### Preview Directory Not Created

1. Check Jekyll environment: `docker-compose exec jekyll env | grep JEKYLL_ENV`
2. Verify plugin logs in Docker output: `docker-compose logs jekyll`
3. Ensure development config is loaded: `_config.yml,_config_dev.yml`

### Preview Button Not Working

1. Verify FrontMatter configuration in `frontmatter.json`
2. Check file is in configured collection path
3. Ensure Jekyll server is running on port 4002
4. Test URL manually: `http://localhost:4002/preview/<collection>/<filename>/`

### Plugin Not Running

1. Check plugin file exists: `_plugins/preview_generator.rb`
2. Verify Jekyll can load plugins (development mode)
3. Look for plugin output in logs: `Preview Generator: Hook triggered!`

## Testing

A test file is included: `pages/_posts/2025-10-19-test-frontmatter-preview.md`

**Test Steps:**
1. Open the test file in VS Code
2. Click FrontMatter preview button
3. Should open: `http://localhost:4002/preview/posts/2025-10-19-test-frontmatter-preview/`
4. Verify content renders correctly

## Future Enhancements

Potential improvements for this system:

1. **Conditional Logic**: Add support for custom permalinks when defined
2. **Production Mode**: Adapt for production environments if needed
3. **Performance**: Optimize file copying for large collections
4. **Caching**: Implement intelligent rebuilding for changed files only
5. **Integration**: Enhanced integration with other development tools

## Related Files

- `/frontmatter.json` - FrontMatter CMS configuration
- `/_plugins/preview_generator.rb` - Jekyll plugin for preview generation
- `/_config_dev.yml` - Development configuration
- `/docker-compose.yml` - Development environment setup

---

*This implementation provides a robust, maintainable solution for FrontMatter preview functionality that prioritizes developer experience and reliability over complexity.*