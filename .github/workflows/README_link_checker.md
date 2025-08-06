# 🔗 Automated Link Checker Workflow Documentation

This workflow provides automated link checking for the IT-Journey Jekyll site with AI-powered analysis and issue reporting.

## 🚀 Features

- **Comprehensive Link Testing**: Checks all markdown files across Jekyll collections
- **Intelligent Categorization**: Groups link failures by type (timeouts, certificate errors, etc.)
- **AI-Powered Analysis**: Uses OpenAI GPT to analyze patterns and provide recommendations
- **Automated Issue Creation**: Creates GitHub issues with detailed reports and actionable suggestions
- **Flexible Scope**: Can check all links or focus on specific content types (pages, posts, quests)
- **Environment-Aware**: Handles Jekyll-specific patterns and GitHub Pages requirements

## 🛠️ Setup Requirements

### Required Secrets

1. **OPENAI_API_KEY** (Optional but recommended):
   ```bash
   # Add this secret to your repository settings
   # Go to Settings > Secrets and variables > Actions
   # Add new repository secret: OPENAI_API_KEY
   ```

### GitHub Permissions

The workflow requires these permissions (automatically configured):
- `contents: read` - To access repository files
- `issues: write` - To create issue reports
- `pull-requests: write` - For PR comments (future feature)

## 📋 Usage

### Manual Trigger

1. Go to **Actions** tab in your repository
2. Select **"Automated Link Checker with AI Analysis"**
3. Click **"Run workflow"**
4. Configure options:
   - **Scope**: Choose what to check (`all`, `pages-only`, `posts-only`, `quests-only`)
   - **Create Issue**: Whether to automatically create a GitHub issue with results

### Automatic Triggers

- **Scheduled**: Runs every Monday at 9 AM UTC
- **Content Changes**: Runs when markdown files are modified (with debouncing to avoid spam)

## 🎯 Scope Options

### `all` (Default)
Checks all markdown files in:
- `pages/**/*.md`
- `*.md` (root level files)
- `index.md`

### `pages-only`
Focused check on:
- `pages/_pages/**/*.md`
- `pages/index.html`
- `pages/home.md`
- `pages/search.md`

### `posts-only`
Checks only blog posts:
- `pages/_posts/**/*.md`

### `quests-only`
Checks only quest files:
- `pages/_quests/**/*.md`

## 🔧 Configuration

### Link Ignore Patterns (`.lycheeignore`)

The workflow uses `.lycheeignore` to skip problematic URLs:

```bash
# Local development URLs
http://localhost:*
https://localhost:*

# Social media (often rate-limited)
https://twitter\.com/.*
https://instagram\.com/.*

# Email addresses
mailto:.*

# File downloads
.*\.pdf$
.*\.zip$
```

### Adding Custom Ignore Patterns

Edit `.lycheeignore` to add URLs that should be skipped:

```bash
# Add your custom patterns
https://problematic-site\.com/.*
.*maintenance.*
```

## 📊 Analysis Features

### Link Categorization

The workflow categorizes link failures:

- **Broken External**: External links that return 404 or similar errors
- **Broken Internal**: Jekyll internal links that don't resolve
- **Certificate Errors**: SSL/TLS certificate issues
- **Network Errors**: Connectivity problems
- **Timeouts**: Slow-responding sites
- **Rate Limited**: Sites blocking automated requests

### AI Analysis

When OpenAI API key is configured, the workflow provides:

- **Root Cause Analysis**: Identifies patterns in link failures
- **Jekyll-Specific Insights**: Recognizes common Jekyll/GitHub Pages issues
- **Prioritized Recommendations**: Actionable steps to fix issues
- **Prevention Strategies**: Suggestions to avoid future problems

## 📄 Output Formats

### GitHub Issue Report

Automatically created issues include:

```markdown
# 🔗 Automated Link Check Report

## 📊 Summary
- Total links checked: 150
- Broken links found: 8
- Success rate: 94.7%
- Scope: all

## 🔍 Detailed Results
[Detailed breakdown of link failures]

## 🤖 AI Analysis
[AI-powered insights and recommendations]

## 🛠️ Next Steps
[Actionable recommendations]
```

### Workflow Artifacts

Downloadable artifacts include:

- `results.json` - Raw lychee output
- `summary.md` - Human-readable summary
- `analysis.json` - Categorized analysis
- `ai_analysis.md` - AI insights (if available)

## 🔍 Troubleshooting

### Common Issues

#### High False Positives
- **Solution**: Add problematic domains to `.lycheeignore`
- **Example**: Rate-limited social media sites

#### Internal Links Failing
- **Cause**: Jekyll baseurl configuration
- **Solution**: Check `_config.yml` baseurl and permalink settings

#### Certificate Errors in CI
- **Cause**: Restrictive CI environment
- **Solution**: These may work in production but fail in CI

#### Network Timeouts
- **Cause**: Slow external sites
- **Solution**: Increase timeout in workflow or add to ignore list

### Workflow Debugging

1. **Check Workflow Logs**: Look at the Actions tab for detailed output
2. **Download Artifacts**: Get detailed JSON results for analysis
3. **Test Locally**: Run lychee manually on specific files
4. **Adjust Timeouts**: Modify workflow parameters for slow sites

## 🎨 Customization

### Modifying Check Parameters

Edit `.github/workflows/link-checker.yml`:

```yaml
# Adjust lychee parameters
--timeout 30              # Increase timeout for slow sites
--max-retries 3           # Number of retry attempts
--max-redirects 5         # Maximum redirects to follow
--user-agent "Custom/1.0" # Custom user agent string
```

### AI Analysis Customization

Modify the AI prompt in the workflow to:
- Focus on specific types of analysis
- Add domain-specific context
- Customize recommendation format

### Issue Template Customization

The issue creation section can be modified to:
- Change issue labels
- Modify assignee settings
- Customize issue body format
- Add project board automation

## 🔄 Integration with Other Workflows

### Pre-deployment Checks

Add link checking to your deployment workflow:

```yaml
- name: Check Links Before Deploy
  uses: ./.github/workflows/link-checker.yml
  with:
    scope: all
    create_issue: false
```

### PR Validation

Use for pull request validation:

```yaml
on:
  pull_request:
    paths:
      - 'pages/**/*.md'
```

## 📈 Performance Considerations

### Optimizing for Large Sites

- Use **scope filtering** to check only relevant content
- Adjust **timeout values** based on your external link performance
- Consider **scheduled runs** instead of every commit
- Use **artifact caching** for repeated checks

### Rate Limiting Management

- Add rate-limited domains to `.lycheeignore`
- Increase delays between requests if needed
- Use custom user agents if required by target sites

## 🛡️ Security Considerations

- **API Keys**: Store OpenAI API key as repository secret
- **Permissions**: Workflow uses minimal required permissions
- **External Requests**: All external requests go through lychee with proper user agent
- **Data Privacy**: No link content is sent to AI, only metadata and patterns

## 🤝 Contributing

To improve this workflow:

1. Test changes on a subset of content first
2. Update documentation for new features
3. Add appropriate error handling
4. Consider backward compatibility
5. Update the ignore patterns as needed

## 📚 Resources

- [Lychee Documentation](https://github.com/lycheeverse/lychee)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

---

*This workflow is part of the IT-Journey automated quality assurance system, helping maintain a reliable and professional learning platform.*