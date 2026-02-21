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