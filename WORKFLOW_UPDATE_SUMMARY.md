# Organize Posts Weekly Workflow Update

## Summary of Changes

This update modifies the `organize-posts-weekly.yml` workflow to create a pull request with the proposed organization results instead of directly committing to the main branch.

## What Changed

### Before
- The workflow ran the organize-posts script
- Changes were committed directly to the main branch with `git push origin main`
- No review process for the automated changes

### After
- The workflow runs the organize-posts script
- Changes are committed to a new branch: `automated/organize-posts-{run_id}`
- A pull request is automatically created with:
  - Descriptive title including the workflow run ID
  - Comprehensive PR body with summary of changes
  - Links to the workflow run
  - Labels: `automated`, `content-organization`, `posts`
  - Auto-assigned to: `bamr87`
- The PR can be reviewed before merging
- The branch is automatically deleted after PR is merged/closed

## Key Updates

### 1. Replaced Direct Push with PR Creation
**Removed:**
```yaml
- name: 'Commit and Push Changes'
  run: |
    git add pages/_posts/
    git commit -m "$commit_msg"
    git push origin main
```

**Added:**
```yaml
- name: 'Create Branch and Commit Changes'
  run: |
    BRANCH_NAME="automated/organize-posts-${{ github.run_id }}"
    git checkout -b "$BRANCH_NAME"
    git add pages/_posts/
    git commit -m "🤖 Weekly post organization and archiving"
    git push origin "$BRANCH_NAME"

- name: 'Create Pull Request with GitHub CLI'
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    gh pr create \
      --title "🤖 Weekly Post Organization - ${{ github.run_id }}" \
      --body-file pr_body.md \
      --base main \
      --label "automated" \
      --label "content-organization" \
      --label "posts" \
      --assignee "bamr87"
    ...
```

### 2. Enhanced Workflow Summary
The workflow summary now reports:
- Whether a PR was created
- PR number and URL (when applicable)
- Clearer status messages for different execution modes

### 3. Removed Duplicate PR Creation Step
The old "Create Pull Request (if manual trigger with dry-run)" step has been removed as the main PR creation step now handles all scenarios.

## Benefits

1. **Review Process**: All automated changes now go through a PR review process
2. **Traceability**: Each PR links back to the workflow run that created it
3. **Safety**: Changes can be reviewed and rejected if needed
4. **Transparency**: Clear documentation in the PR body about what was changed
5. **Rollback**: Easy to close the PR if changes are unwanted

## Testing

The workflow can be tested by:
1. Manual trigger: Go to Actions → Weekly Post Organization → Run workflow
2. Scheduled trigger: Runs automatically every Sunday at 2 AM UTC
3. Dry-run mode: Use the dry_run input to preview changes without creating a PR

## No Script Changes Required

The Python script (`organize-posts.py`) and bash wrapper (`organize-posts.sh`) remain unchanged. They correctly organize posts based on frontmatter metadata and work as expected with the new PR-based workflow.
