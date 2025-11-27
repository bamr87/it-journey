---
agent: agent
mode: agent
description: "Review changes, run tests, update documentation, bump version, and publish Jekyll theme gem"
---

# Commit & Publish Workflow for Zer0-Mistakes Jekyll Theme

Review open changes, run appropriate tests, create/update documentation, update the changelog, bump the version according to semantic versioning, and publish the Ruby gem.

## Task Overview

Execute the complete release pipeline for the zer0-mistakes Jekyll theme. This workflow handles Docker-first development, Jekyll theme validation, and Ruby gem publishing to RubyGems.org.

## Step 1: Review Open Changes

1. **Analyze Git Changes**:
   - Run `git status` to identify all modified, added, and deleted files
   - Run `git diff --cached` for staged changes and `git diff` for unstaged changes
   - Categorize changes by type:
     - **Features**: New layouts, includes, components, or functionality
     - **Bug Fixes**: Issues resolved in templates, styles, or scripts
     - **Breaking Changes**: Changes that break backward compatibility (layout renames, config changes)
     - **Documentation**: README, CHANGELOG, or `/docs/` updates
     - **Refactoring**: Code improvements without functionality changes
     - **Dependencies**: Gemfile or gemspec updates
     - **Tests**: Test additions or modifications in `/test/`
     - **UI/UX**: Layout, include, CSS, or JavaScript changes

2. **Summarize Changes**:
   - Create a concise summary of all changes
   - Use `./scripts/analyze-commits.sh HEAD~5..HEAD` to determine impact level
   - Note any breaking changes that require migration

3. **Jekyll-Specific Change Categories**:
   - **Layouts** (`_layouts/`): Template structure changes
   - **Includes** (`_includes/`): Component changes
   - **Sass** (`_sass/`): Style changes
   - **Assets** (`assets/`): Static file changes
   - **Data** (`_data/`): Configuration data changes
   - **Config** (`_config*.yml`): Jekyll configuration changes

## Step 2: Run Appropriate Tests

1. **Identify Test Requirements**:
   - Based on changed files, determine which tests to run
   - For layout/include changes → run Jekyll build tests
   - For config changes → run full validation suite
   - For all changes → run comprehensive test suite

2. **Execute Tests**:
   ```bash
   # Run comprehensive test suite
   ./test/test_runner.sh
   
   # Run core tests only
   ./test/test_core.sh
   
   # Run tests with verbose output
   ./test/test_runner.sh --verbose
   
   # Build validation with Docker
   docker-compose exec jekyll jekyll build --verbose
   
   # Run Jekyll doctor for config validation
   docker-compose exec jekyll jekyll doctor
   ```

3. **Verify Test Results**:
   - Ensure all tests pass before proceeding
   - If tests fail, stop and report the failures
   - Document any test warnings or deprecation notices

## Step 3: Create/Update Documentation

1. **Update Affected README Files**:
   - Update `README.md` for user-facing changes
   - Update `scripts/README.md` for automation changes
   - Update component-specific READMEs in `_layouts/README.md`, `_includes/README.md`
   - Ensure all new features are documented

2. **Update Component Documentation**:
   - Add front matter documentation headers to new layouts/includes
   - Document parameters and dependencies for new components
   - Update usage examples in the `/docs/` directory

3. **Update Theme Documentation**:
   - If layout changes, update `docs/jekyll/` documentation
   - If configuration changes, update `docs/configuration/`
   - If new features, add to `docs/features/`

## Step 4: Update CHANGELOG.md

1. **Determine Version Type** based on changes:
   - **MAJOR** (X.0.0): Breaking changes, layout renames, config incompatibilities
   - **MINOR** (0.X.0): New layouts, components, features (backward-compatible)
   - **PATCH** (0.0.X): Bug fixes, documentation, minor improvements

2. **Add Changelog Entry** following Keep a Changelog format:
   ```markdown
   ## [X.Y.Z] - YYYY-MM-DD
   
   ### Added
   - **New Layout: `layout-name.html`** - Description of the layout
   - **New Component: `component.html`** - Description of the component
   - New features or capabilities
   
   ### Changed
   - **Enhanced: `filename.html`** - Description of improvements
   - Changes to existing functionality
   
   ### Deprecated
   - Features marked for removal
   
   ### Removed
   - Removed features or components
   
   ### Fixed
   - **Critical: issue description** - Resolution details
   - Bug fixes with context
   
   ### Security
   - Security updates
   ```

3. **Reference Issues/PRs** if applicable

## Step 5: Bump Version

1. **Update Version File** (`lib/jekyll-theme-zer0/version.rb`):
   ```ruby
   # frozen_string_literal: true
   
   module JekyllThemeZer0
     VERSION = "X.Y.Z"
   end
   ```

2. **Verify Version Consistency**:
   - Ensure `lib/jekyll-theme-zer0/version.rb` has correct version
   - Check `jekyll-theme-zer0.gemspec` reads from version.rb correctly
   - Verify CHANGELOG.md has entry for new version

3. **Alternative: Use Release Script**:
   ```bash
   # Preview version bump
   ./scripts/release patch --dry-run
   
   # Or let the script handle version updates
   ./scripts/release patch --skip-publish --no-github-release
   ```

## Step 6: Prepare for Publication

1. **Stage All Changes**:
   ```bash
   git add -A
   ```

2. **Create Semantic Commit Message**:
   Format: `<type>(<scope>): <description>`
   
   Types:
   - `feat`: New feature (layout, component, functionality)
   - `fix`: Bug fix
   - `docs`: Documentation changes
   - `style`: Code style changes (formatting, CSS)
   - `refactor`: Code refactoring
   - `test`: Test additions/changes
   - `chore`: Maintenance tasks (deps, configs)
   - `breaking`: Breaking changes

   Scopes (Jekyll-specific):
   - `layouts`: Layout template changes
   - `includes`: Component changes
   - `sass`: Style changes
   - `assets`: Static file changes
   - `config`: Configuration changes
   - `scripts`: Automation script changes

3. **Commit Changes**:
   ```bash
   git commit -m "<type>(<scope>): <description>

   <detailed description of changes>

   - Change 1
   - Change 2
   - Change 3

   Closes #<issue-number> (if applicable)"
   ```

4. **Use Full Release Workflow** (Recommended):
   ```bash
   # Full release with gem publishing and GitHub release
   ./scripts/release patch
   
   # Or minor/major releases
   ./scripts/release minor
   ./scripts/release major
   ```

5. **Manual Release Alternative**:
   ```bash
   # Build gem
   ./scripts/build
   
   # Create tag
   git tag -a v<X.Y.Z> -m "Release v<X.Y.Z>: <summary>"
   
   # Push changes
   git push origin main
   git push origin --tags
   
   # Publish to RubyGems
   gem push jekyll-theme-zer0-<X.Y.Z>.gem
   ```

## Success Criteria

- [ ] All tests pass with no failures (`./test/test_runner.sh`)
- [ ] Jekyll builds successfully (`docker-compose exec jekyll jekyll build`)
- [ ] All changed code has proper documentation
- [ ] CHANGELOG.md updated with new version entry
- [ ] `lib/jekyll-theme-zer0/version.rb` updated to new version
- [ ] Gemspec validates correctly (`bundle exec gem build`)
- [ ] Git commit follows semantic commit format
- [ ] Git tag created: `v<version>`
- [ ] Gem published to RubyGems (optional)
- [ ] GitHub release created (optional)

## Output Format

After completing all steps, provide a summary:

```markdown
## Release Summary

**Version**: X.Y.Z (from X.Y.Z)
**Type**: MAJOR | MINOR | PATCH
**Date**: YYYY-MM-DD

### Changes Included
- [ ] New layout: `layout-name.html`
- [ ] Component update: `component.html`
- [ ] Bug fix: description
- [ ] etc.

### Test Results
- Test Suite: PASSED/FAILED
- Jekyll Build: SUCCESS/FAILED
- Jekyll Doctor: OK/WARNINGS

### Files Modified
- _layouts/new-layout.html
- _includes/components/new-component.html
- _sass/custom.scss
- assets/js/script.js

### Documentation Updated
- [ ] README.md
- [ ] CHANGELOG.md
- [ ] docs/features/new-feature.md
- [ ] Component inline documentation

### Commit Information
- Hash: <commit-hash>
- Message: <commit-message>
- Tag: v<version>

### Publication Status
- RubyGems: https://rubygems.org/gems/jekyll-theme-zer0/versions/<version>
- GitHub Release: https://github.com/bamr87/zer0-mistakes/releases/tag/v<version>
```

## Rollback Procedure

If issues are discovered after publication:

1. **Revert the commit**:
   ```bash
   git revert <commit-hash>
   ```

2. **Delete the tag**:
   ```bash
   git tag -d v<version>
   git push origin :refs/tags/v<version>
   ```

3. **Yank the gem from RubyGems** (if published):
   ```bash
   gem yank jekyll-theme-zer0 -v <version>
   ```

4. **Create a patch release** with the fix:
   ```bash
   ./scripts/release patch
   ```

---

## Quick Reference Commands

```bash
# Docker development
docker-compose up                    # Start dev server
docker-compose exec jekyll bash      # Shell access

# Testing
./test/test_runner.sh               # Full test suite
./test/test_runner.sh --verbose     # Verbose output

# Version analysis
./scripts/analyze-commits.sh HEAD~5..HEAD

# Release workflow
./scripts/release patch --dry-run    # Preview release
./scripts/release patch              # Patch release
./scripts/release minor              # Minor release
./scripts/release major              # Major release

# Build only (no publish)
./scripts/build
./scripts/release patch --skip-publish --no-github-release
```

---

**Note**: Always run tests and validate Jekyll builds before publishing. Use Docker for consistent environment. The `./scripts/release` command handles the complete workflow including changelog generation, version bumping, testing, building, tagging, and publishing.