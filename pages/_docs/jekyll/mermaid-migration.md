---
title: Mermaid Auto-Detection Migration Guide
subcategory: jekyll
date: 2025-01-27
tags:
  - Mermaid
  - Migration
  - Auto-Detection
  - Theme-Update
lastmod: 2025-01-27T18:30:00.000Z
---

# Mermaid Auto-Detection Migration Guide

## What Changed? 🎯

The zer0-mistakes theme now automatically detects Mermaid diagrams. You no longer need `mermaid: true` in front matter!

### Before (Manual Configuration)
```yaml
---
title: My Post
mermaid: true  # Required for diagrams to render
---
```

### After (Auto-Detection)
```yaml
---
title: My Post
# No flag needed! Auto-detection handles this
---
```

## Action Required

**None!** Your existing posts still work (backwards compatible).

The theme automatically:
- ✅ Detects ```mermaid code blocks in your content
- ✅ Loads Mermaid.js library on-demand
- ✅ Renders diagrams with optimized settings
- ✅ Maintains all existing functionality

## Optional Cleanup

You can remove `mermaid: true` from front matter to clean up your posts:

````diff
---
title: My Post
- mermaid: true
---
````

### Benefits of Cleanup

- 🎯 **Better DX** - impossible to forget configuration
- ⚡ **Performance** - library loads only when needed
- 🔧 **Less maintenance** - fewer front matter fields
- 📝 **Cleaner content** - standard markdown syntax

## Migration Steps

### Step 1: Update Theme

Ensure you're using zer0-mistakes v0.5.0+:

```yaml
# _config.yml
remote_theme: "bamr87/zer0-mistakes"
```

### Step 2: Test Your Diagrams

1. Start local Jekyll server:
   ```bash
   bundle exec jekyll serve --port 4002
   ```

2. Visit pages with Mermaid diagrams
3. Check browser console for "Mermaid diagrams detected" message
4. Verify all diagrams render correctly

### Step 3: Remove Front Matter Flags (Optional)

Search for files with `mermaid: true`:

```bash
grep -r "mermaid: true" pages/
```

Remove the flag from each file:

````diff
---
title: My Post
- mermaid: true
---
````

### Step 4: Update Documentation

Update any internal documentation that mentions the old approach:

- Remove references to `mermaid: true` requirement
- Update examples to show auto-detection
- Add notes about performance benefits

## Technical Details

### How Auto-Detection Works

1. **Content Scanning**: Theme scans page content for ```mermaid blocks
2. **Dynamic Loading**: Mermaid.js loads from CDN only when needed
3. **Automatic Rendering**: Diagrams render with optimized theme settings
4. **Performance**: Zero impact on pages without diagrams

### Detection Methods

The theme detects Mermaid content through:
- ```mermaid code blocks in markdown
- `<div class="mermaid">` HTML elements
- `mermaid: true` front matter (backwards compatibility)

### Performance Impact

**Before:**
- Mermaid.js loaded site-wide if any post had `mermaid: true`
- ~200KB library loaded on every page

**After:**
- Mermaid.js loads only on pages with diagrams
- Zero impact on pages without diagrams
- Improved site performance

## Troubleshooting

### Diagrams Not Rendering?

1. **Check theme version**: Ensure zer0-mistakes v0.5.0+
2. **Browser console**: Look for "Mermaid diagrams detected" message
3. **Syntax validation**: Test at [mermaid.live](https://mermaid.live/)
4. **Network tab**: Verify Mermaid.js loads from CDN

### Common Issues

**Issue**: Old posts with `mermaid: true` don't work
- **Solution**: Update theme to v0.5.0+
- **Solution**: Check browser console for errors

**Issue**: New posts without `mermaid: true` don't work
- **Solution**: Ensure theme is updated
- **Solution**: Check for syntax errors in diagrams

**Issue**: Performance seems slower
- **Solution**: This shouldn't happen - auto-detection is faster
- **Solution**: Check for multiple Mermaid.js loads in network tab

## Rollback Plan

If you need to rollback to manual configuration:

1. **Revert theme**: Use zer0-mistakes v0.4.0
2. **Add flags**: Add `mermaid: true` to all posts with diagrams
3. **Test**: Verify diagrams render correctly

## Benefits Summary

### Developer Experience
- ✅ Zero configuration required
- ✅ Impossible to forget setup
- ✅ Standard markdown syntax
- ✅ Better error messages

### Performance
- ✅ On-demand loading only
- ✅ Faster page loads
- ✅ Reduced bandwidth usage
- ✅ Better caching

### Maintenance
- ✅ Fewer front matter fields
- ✅ Cleaner content files
- ✅ Less configuration drift
- ✅ Easier onboarding

## Support

If you encounter issues during migration:

1. **Check documentation**: [Mermaid Guide](jekyll-diagram-with-mermaid.md)
2. **Test syntax**: [Mermaid Live Editor](https://mermaid.live/)
3. **Browser console**: Look for error messages
4. **Theme version**: Ensure v0.5.0+ is installed

## Next Steps

1. **Update theme** to zer0-mistakes v0.5.0+
2. **Test diagrams** on local development server
3. **Remove flags** from front matter (optional)
4. **Update documentation** to reflect new approach
5. **Enjoy** the improved developer experience!

---

*This migration guide is part of the zer0-mistakes theme v0.5.0 release. For more information, visit the [theme documentation](https://bamr87.github.io/zer0-mistakes/).*
