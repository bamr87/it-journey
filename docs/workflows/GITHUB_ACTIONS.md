# GitHub Actions Workflows

This document provides comprehensive documentation for all GitHub Actions workflows in the IT-Journey repository.

## Overview

The IT-Journey repository uses GitHub Actions for continuous integration, automated testing, content validation, and deployment. All workflows are located in `.github/workflows/`.

## Workflow Summary

| Workflow | Trigger | Purpose | Status |
|----------|---------|---------|--------|
| Link Checker | Schedule, Manual | Validate links with AI analysis | Active |
| Build Validation | Push, PR | Verify Jekyll builds successfully | Active |
| Frontmatter Validation | PR, Manual | Validate content frontmatter | Active |
| AI Content Review | PR, Push | AI-powered content quality review | Active |
| Organize Posts | Schedule, Manual | Automated content organization | Active |
| CodeQL Analysis | Schedule, Push | Security code scanning | Active |
| Dependency Checker | Schedule | Check for outdated dependencies | Active |
| Update Settings | Manual | Update repository settings | Manual |
| Auto PR | Manual | Automated pull request creation | Manual |
| Feature Request | Manual | Create feature request issues | Manual |

## Active Workflows

### Link Health Guardian

**File:** `.github/workflows/link-checker.yml`

**Purpose:** Automated link validation with AI-powered analysis to maintain content quality.

**Triggers:**
- Scheduled: Monday 6 AM UTC, Friday 6 PM UTC
- Manual: workflow_dispatch with configuration options

**Configuration Options:**
```yaml
scope:          # website, internal, external, docs, posts, quests, all
analysis_level: # basic, standard, comprehensive, ai-only  
create_issue:   # true/false - Create GitHub issue with results
ai_analysis:    # true/false - Enable AI-powered analysis
timeout:        # 10, 20, 30, 45, 60 seconds
```

**Required Secrets:**
- `OPENAI_API_KEY` (optional, for AI analysis)
- `GITHUB_TOKEN` (automatic)

**Outputs:**
- `link-check-results/` - Detailed JSON results
- `link_analysis.json` - Categorized failures
- `ai_analysis.md` - AI insights (if enabled)
- `github_issue.md` - Issue content
- GitHub issue (if enabled)

**Example Manual Trigger:**
```bash
# Via GitHub CLI
gh workflow run link-checker.yml \
  -f scope=website \
  -f analysis_level=comprehensive \
  -f create_issue=true \
  -f ai_analysis=true \
  -f timeout=30
```

**Workflow Steps:**
1. Checkout repository
2. Setup Python 3.11
3. Install dependencies (requests library)
4. Run unified link-checker.py script
5. Extract results for summary
6. Archive results as artifacts
7. Display workflow summary

**See Also:** 
- [Link Checker Resolution](LINK_CHECKER_FIX_RESOLUTION.md)
- [Link Checker Validation](LINK_CHECKER_VALIDATION.md)

### Build Validation

**File:** `.github/workflows/build-validation.yml`

**Purpose:** Ensure Jekyll builds successfully before merging changes.

**Triggers:**
- Push to main branch
- Pull requests to main branch

**Process:**
1. Checkout repository
2. Setup Ruby 3.2.3
3. Install Jekyll and dependencies
4. Build site with Jekyll
5. Check for build errors
6. Report build status

**Failure Scenarios:**
- Invalid YAML in `_config.yml`
- Broken Liquid syntax
- Missing includes or layouts
- Invalid frontmatter
- Plugin errors

**Troubleshooting:**
```bash
# Test locally before pushing
bundle exec jekyll build --verbose

# Check for configuration errors
bundle exec jekyll doctor
```

### Frontmatter Validation

**File:** `.github/workflows/frontmatter-validation.yml`

**Purpose:** Validate and auto-fix frontmatter in markdown files.

**Triggers:**
- Pull requests (validation only)
- Manual dispatch (with optional auto-fix)

**Configuration Options:**
```yaml
apply_fixes: # true/false - Apply automatic fixes
```

**Validated Fields:**
- **Required:** title, description, date, author, categories, tags
- **Recommended:** excerpt, lastmod, draft

**Auto-Fix Capabilities:**
- Extract date from filename
- Generate description from content
- Infer categories from directory structure
- Add default author
- Set modification timestamps

**Usage:**
```bash
# Via GitHub Actions UI
Actions > Frontmatter Validation > Run workflow
# Select apply_fixes: true to apply fixes automatically
```

**See Also:** [Frontmatter Standards](../standards/FRONTMATTER_STANDARDS.md)

### AI Content Review

**File:** `.github/workflows/ai-content-review.yml`

**Purpose:** AI-powered content quality analysis using GPT-4.

**Triggers:**
- Pull requests with markdown changes
- Push to main branch

**Required Secrets:**
- `OPENAI_API_KEY` - OpenAI API key

**Review Criteria:**
- Frontmatter completeness
- Content quality and structure
- SEO optimization
- Technical accuracy
- Accessibility
- Writing style

**Output:**
- Quality score (1-10)
- Positive aspects
- Priority action items
- Frontmatter issues
- Content suggestions
- SEO improvements

**Quality Scores:**
- 8-10: Excellent content
- 6-7: Good content
- 4-5: Fair content
- 1-3: Poor content

**Cost Considerations:**
This workflow uses the OpenAI API and incurs costs. Monitor usage in the OpenAI dashboard.

### Organize Posts Weekly

**File:** `.github/workflows/organize-posts-weekly.yml`

**Purpose:** Automated weekly organization of blog posts by categories.

**Triggers:**
- Scheduled: Weekly (configurable)
- Manual dispatch

**Process:**
1. Run organization script
2. Move posts to appropriate directories
3. Update navigation if needed
4. Commit changes (if any)

**Script:** `scripts/development/content/organize-posts.py`

### CodeQL Analysis

**File:** `.github/workflows/codeql-analysis.yml`

**Purpose:** Automated security scanning for vulnerabilities.

**Triggers:**
- Push to main branch
- Pull requests to main branch
- Scheduled: Weekly

**Languages Analyzed:**
- Python
- JavaScript
- Ruby (if applicable)

**Outputs:**
- Security alerts in Security tab
- CodeQL analysis results
- Recommended remediations

**Viewing Results:**
```
Repository > Security > Code scanning alerts
```

### Dependency Checker

**File:** `.github/workflows/dependency-checker.yml`

**Purpose:** Monitor for outdated or vulnerable dependencies.

**Triggers:**
- Scheduled: Weekly

**Checks:**
- Ruby gems (Gemfile.lock)
- Node packages (package.json, if present)
- GitHub Actions versions

**Actions Taken:**
- Create issue for outdated dependencies
- Highlight security vulnerabilities
- Suggest version updates

## Manual Workflows

### Update Settings

**File:** `.github/workflows/update-settings.yml`

**Purpose:** Update repository settings and configurations.

**Trigger:** Manual dispatch only

**Uses:** `scripts/deployment/update-settings.sh`

### Auto PR

**File:** `.github/workflows/auto-pr.yml`

**Purpose:** Create automated pull requests for batch changes.

**Trigger:** Manual dispatch only

**Use Cases:**
- Bulk content updates
- Automated refactoring
- Configuration changes

### Feature Request

**File:** `.github/workflows/new-feature-request.yml`

**Purpose:** Streamlined feature request creation.

**Trigger:** Manual dispatch with inputs

**Inputs:**
- Feature title
- Feature description
- Priority level
- Category

## Workflow Best Practices

### Secret Management

**Required Secrets:**
```
GITHUB_TOKEN        # Automatic, no setup needed
OPENAI_API_KEY     # For AI-powered features
```

**Adding Secrets:**
```
Repository > Settings > Secrets and Variables > Actions > New repository secret
```

**Security:**
- Never commit secrets to repository
- Rotate secrets periodically
- Use least privilege access
- Audit secret usage

### Workflow Debugging

**View Workflow Runs:**
```
Repository > Actions > Select workflow > View run
```

**Download Artifacts:**
```
Workflow run > Artifacts section > Download
```

**Re-run Failed Workflows:**
```
Failed workflow run > Re-run jobs
```

**Enable Debug Logging:**
Add repository secrets:
```
ACTIONS_STEP_DEBUG = true
ACTIONS_RUNNER_DEBUG = true
```

### Performance Optimization

**Caching:**
Workflows use caching for:
- Ruby gems
- Python packages
- Node modules

**Timeout Settings:**
Most workflows have 45-minute timeout:
```yaml
timeout-minutes: 45
```

**Concurrency Control:**
Some workflows limit concurrent runs:
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Workflow Status and Monitoring

### Status Badges

Add to README.md:
```markdown
![Build Status](https://github.com/bamr87/it-journey/actions/workflows/build-validation.yml/badge.svg)
![Link Health](https://github.com/bamr87/it-journey/actions/workflows/link-checker.yml/badge.svg)
```

### Notifications

Configure in:
```
Repository > Settings > Notifications
```

Options:
- Email notifications
- Slack/Discord webhooks
- GitHub mobile app

### Workflow Run History

View past runs:
```
Actions > All workflows > Filter by status/branch/actor
```

Retention:
- Workflow run logs: 90 days
- Artifacts: 30 days (configurable)

## Troubleshooting

### Common Issues

**Issue:** Workflow doesn't trigger
**Solution:**
- Check trigger conditions in workflow file
- Verify branch names match
- Ensure workflow file is in `main` branch

**Issue:** Secrets not accessible
**Solution:**
- Verify secret name matches exactly
- Check secret is set at repository level (not environment)
- Ensure workflow has correct permissions

**Issue:** Build fails on specific step
**Solution:**
- Check step logs for error messages
- Test commands locally
- Verify dependencies are installed

**Issue:** Workflow times out
**Solution:**
- Increase `timeout-minutes` value
- Optimize long-running steps
- Consider splitting into multiple jobs

### Getting Help

1. **Workflow Logs:** Check detailed logs in Actions tab
2. **GitHub Docs:** [GitHub Actions Documentation](https://docs.github.com/en/actions)
3. **Community:** [GitHub Community Forum](https://github.community/)
4. **Issues:** Create repository issue with workflow logs

## Workflow Development

### Creating New Workflows

**Template Structure:**
```yaml
name: Workflow Name

on:
  push:
    branches: [ main ]
  workflow_dispatch:

env:
  KEY: value

jobs:
  job-name:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Environment
        # Setup steps
      
      - name: Run Task
        run: |
          # Commands
      
      - name: Upload Results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: results
          path: output/
```

### Testing Workflows

**Local Testing:**
```bash
# Install act (GitHub Actions local runner)
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow locally
act -W .github/workflows/workflow-name.yml
```

**Branch Testing:**
1. Create feature branch
2. Modify workflow file
3. Push to trigger workflow
4. Review results before merging

### Workflow Permissions

Set appropriate permissions:
```yaml
permissions:
  contents: read      # Read repository content
  issues: write       # Create/update issues
  pull-requests: write # Comment on PRs
```

## Maintenance

### Regular Tasks

**Weekly:**
- Review failed workflow runs
- Check for outdated actions
- Monitor artifact storage usage

**Monthly:**
- Update action versions
- Review and optimize slow workflows
- Clean up old artifacts

**Quarterly:**
- Audit secrets and permissions
- Review workflow effectiveness
- Update documentation

### Updating Actions

Keep actions up to date:
```yaml
# Check for updates
- uses: actions/checkout@v4  # Current
- uses: actions/setup-python@v5  # Current
- uses: actions/upload-artifact@v4  # Current
```

Use Dependabot to automate:
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)
- [Community Workflows](https://github.com/actions/starter-workflows)

---

**Last Updated**: 2025-10-13  
**Version**: 1.0.0

