Commit and publish the open changes following IT-Journey repository standards.

## Workflow

1. **README-First**: Read relevant README.md files in affected directories to understand context before proceeding.

2. **Review Changes**: Inspect all staged/unstaged changes (`git status`, `git diff`) to understand scope and impact.

3. **Validate Quality**:
   - Run `bundle exec jekyll build` to verify the site builds without errors.
   - Check for broken links in changed Markdown files.
   - Validate front matter completeness for any new/modified content files (posts, quests, docs).
   - Run any relevant tests (e.g., quest validator for quest files).

4. **README-Last**: Update README.md files in affected directories:
   - Add/update entries for new or changed files.
   - Update `lastmod` dates in front matter.
   - Fix any broken cross-references.
   - Verify all links work.

5. **Stage and Commit** using Conventional Commits format:
   - Determine the correct type: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `style:`, `perf:`, `test:`
   - Include scope when applicable: e.g., `feat(quest):`, `fix(ci):`, `docs(readme):`
   - Use imperative mood, keep subject under 50 chars, no trailing period.
   - Add body explaining WHAT and WHY (not HOW) when changes are non-trivial.
   - Reference related issues: `Closes #123` or `Related to #456`
   - Example: `feat(quest): add Docker fundamentals quest for beginners`

6. **Push Changes**: Push the current branch to origin.

## Rules

- Never commit directly to `main` — use feature branches and PRs.
- Group related changes into logical, atomic commits.
- Ensure all content files have valid YAML front matter.
- Do not commit build artifacts, `_site/`, or `work/` directories.
- Update CHANGELOG.md for significant changes if applicable.

## Detailed Testing and Deployment

### Test Execution
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

### Site Building and Deployment
```bash
# Build with Docker
docker-compose exec jekyll bundle exec jekyll build --destination /tmp/_site

# Or locally if Docker not running
bundle exec jekyll build --destination /tmp/_site

# Deploy to gh-pages branch
git checkout gh-pages
cp -r /tmp/_site/* .
git add -A
git commit -m "Deploy site for <version/date>

Built from commit: <main-commit-hash>
Changes: <summary>"
git push origin gh-pages
```

### Pull Request Creation
```bash
# Create PR from main to gh-pages
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