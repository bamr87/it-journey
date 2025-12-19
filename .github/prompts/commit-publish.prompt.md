---
agent: agent
mode: agent
description: "Review changes, run tests, update documentation, and publish IT-Journey Jekyll site via PR to gh-pages branch"
---

# Commit & Publish Workflow for IT-Journey Jekyll Site

Review open changes, run appropriate tests, create/update documentation, update the changelog, and publish the Jekyll site by creating a pull request to the gh-pages branch for GitHub Pages deployment.

## Task Overview

Execute the complete release pipeline for the IT-Journey Jekyll site. This workflow handles Docker-first development, Jekyll site validation, and deployment via pull request to the gh-pages branch for GitHub Pages hosting.

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

3. **IT-Journey-Specific Change Categories**:
   - **Quests** (`pages/_quests/`): Educational quest content changes
   - **Posts** (`pages/_posts/`): Blog post changes
   - **Pages** (`pages/_*/`): Static page changes
   - **Assets** (`assets/`): Static file changes
   - **Data** (`_data/`): Configuration data changes
   - **Config** (`_config*.yml`): Jekyll configuration changes
   - **Scripts** (`scripts/`): Automation script changes

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
   - Update quest-specific READMEs in `pages/_quests/README.md`
   - Ensure all new content is documented

2. **Update Content Documentation**:
   - Add front matter documentation to new quests/posts
   - Document learning objectives and prerequisites
   - Update usage examples in the `/docs/` directory

3. **Update Site Documentation**:
   - If content structure changes, update `docs/content/` documentation
   - If configuration changes, update `docs/configuration/`
   - If new features, add to `docs/features/`

## Step 4: Update CHANGELOG.md

1. **Determine Release Type** based on changes:
   - **MAJOR**: Breaking changes, major content restructuring, config incompatibilities
   - **MINOR**: New quests, posts, features (backward-compatible)
   - **PATCH**: Bug fixes, documentation, minor improvements

2. **Add Changelog Entry** following Keep a Changelog format:
   ```markdown
   ## [Unreleased] - YYYY-MM-DD
   
   ### Added
   - **New Quest: `quest-name.md`** - Description of the quest
   - **New Post: `post-title.md`** - Description of the post
   - New features or content
   
   ### Changed
   - **Enhanced: `filename.md`** - Description of improvements
   - Changes to existing functionality
   
   ### Fixed
   - **Critical: issue description** - Resolution details
   - Bug fixes with context
   
   ### Removed
   - Removed content or features
   ```

3. **Reference Issues/PRs** if applicable

## Step 5: Build Site for Deployment

1. **Build the Jekyll Site**:
   ```bash
   # Build with Docker
   docker-compose exec jekyll bundle exec jekyll build --destination /tmp/_site
   
   # Or locally if Docker not running
   bundle exec jekyll build --destination /tmp/_site
   ```

2. **Verify Build Output**:
   - Check that `_site/` directory is generated correctly
   - Validate key pages (index.html, quests, posts)
   - Ensure no build errors or warnings

## Step 6: Prepare for Publication

1. **Stage All Changes**:
   ```bash
   git add -A
   ```

2. **Create Semantic Commit Message**:
   Format: `<type>(<scope>): <description>`
   
   Types:
   - `feat`: New feature (quest, post, functionality)
   - `fix`: Bug fix
   - `docs`: Documentation changes
   - `style`: Code style changes (formatting, CSS)
   - `refactor`: Code refactoring
   - `test`: Test additions/changes
   - `chore`: Maintenance tasks (deps, configs)
   - `content`: Content additions/updates

   Scopes (IT-Journey specific):
   - `quests`: Quest content changes
   - `posts`: Blog post changes
   - `pages`: Static page changes
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

4. **Push to Main Branch**:
   ```bash
   git push origin main
   ```

5. **Create Pull Request to gh-pages Branch**:
   - Switch to gh-pages branch or create it if needed
   - Copy built site from `/tmp/_site` to repository root
   - Commit and push the built site to gh-pages branch
   - Create a pull request from main to gh-pages (or directly push if allowed)
   
   ```bash
   # Switch to gh-pages branch
   git checkout gh-pages
   
   # Copy built site
   cp -r /tmp/_site/* .
   
   # Commit built site
   git add -A
   git commit -m "Deploy site for <version/date>
   
   Built from commit: <main-commit-hash>
   Changes: <summary>"
   
   # Push to gh-pages
   git push origin gh-pages
   
   # Create PR (if using PR workflow)
   # Use GitHub CLI or web interface to create PR from main to gh-pages
   gh pr create --base gh-pages --head main --title "Deploy Site Updates" --body "Site deployment from main branch"
   ```

## Success Criteria

- [ ] All tests pass with no failures (`./test/test_runner.sh`)
- [ ] Jekyll builds successfully (`docker-compose exec jekyll jekyll build`)
- [ ] All changed content has proper documentation
- [ ] CHANGELOG.md updated with new entry
- [ ] Site builds correctly to `_site/` directory
- [ ] Git commit follows semantic commit format
- [ ] Changes pushed to main branch
- [ ] Pull request created to gh-pages branch
- [ ] Site deployed to GitHub Pages (optional, via PR merge)

## Output Format

After completing all steps, provide a summary:

```markdown
## Release Summary

**Date**: YYYY-MM-DD

### Changes Included
- [ ] New quest: `quest-name.md`
- [ ] New post: `post-title.md`
- [ ] Content update: description
- [ ] etc.

### Test Results
- Test Suite: PASSED/FAILED
- Jekyll Build: SUCCESS/FAILED
- Site Validation: OK/WARNINGS

### Files Modified
- pages/_quests/new-quest.md
- pages/_posts/new-post.md
- _data/navigation.yml
- assets/images/new-image.png

### Documentation Updated
- [ ] README.md
- [ ] CHANGELOG.md
- [ ] docs/features/new-feature.md
- [ ] Content front matter

### Commit Information
- Hash: <commit-hash>
- Message: <commit-message>
- Branch: main

### Publication Status
- Pull Request: https://github.com/bamr87/it-journey/pull/<pr-number>
- gh-pages Branch: Updated with built site
- GitHub Pages: https://bamr87.github.io/it-journey/ (after PR merge)
```

## Rollback Procedure

If issues are discovered after publication:

1. **Close/Revert the Pull Request**:
   ```bash
   # Close the PR without merging
   gh pr close <pr-number>
   
   # Or revert the merge if already merged
   git revert <merge-commit-hash>
   git push origin gh-pages
   ```

2. **Revert the Main Branch Commit** (if needed):
   ```bash
   git revert <commit-hash>
   git push origin main
   ```

3. **Clean up gh-pages Branch** (if deployed):
   ```bash
   git checkout gh-pages
   git reset --hard <previous-commit>
   git push origin gh-pages --force
   ```

4. **Create a Fix Release**:
   - Fix the issues on main branch
   - Follow the workflow again to create a new PR

---

## Quick Reference Commands

```bash
# Docker development
docker-compose up                    # Start dev server
docker-compose exec jekyll bash      # Shell access

# Testing
./test/test_runner.sh               # Full test suite
./test/test_runner.sh --verbose     # Verbose output

# Site building
docker-compose exec jekyll bundle exec jekyll build  # Build site
bundle exec jekyll build --destination /tmp/_site    # Build to temp dir

# Git workflow
git add -A                         # Stage all changes
git commit -m "feat(content): add new quest"  # Semantic commit
git push origin main               # Push to main

# Deployment to gh-pages
git checkout gh-pages              # Switch to gh-pages branch
cp -r /tmp/_site/* .               # Copy built site
git add -A                         # Stage built files
git commit -m "Deploy site updates" # Commit deployment
git push origin gh-pages           # Push to gh-pages

# Pull request creation
gh pr create --base gh-pages --head main --title "Deploy Site Updates" --body "Site deployment from main branch"
```

---

**Note**: Always run tests and validate Jekyll builds before publishing. Use Docker for consistent environment. The deployment process involves building the site, committing the built files to the gh-pages branch, and creating a pull request for review before merging to deploy to GitHub Pages.