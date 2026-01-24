# AI-Powered Content Review and Frontmatter Management

This documentation describes the AI-powered workflows for automated content review and frontmatter management in the IT-Journey repository.

## Overview

The repository now includes two automated workflows that help maintain content quality and consistency:

1. **AI Content Review Workflow** - Analyzes content quality using AI and provides improvement suggestions
2. **Frontmatter Validation Workflow** - Validates and automatically fixes frontmatter issues
3. **Link Health Guardian Workflow** - Checks links and produces a summarized health report

## AI Content Review Workflow

### File: `.github/workflows/ai-content-review.yml`

This workflow automatically reviews markdown files in the `pages/` directory using OpenAI's GPT-4 API whenever:
- A pull request is opened or updated with markdown file changes
- Changes are pushed to the main branch

### Features

- **Automatic Trigger**: Runs on PR creation/updates and pushes to main
- **AI Analysis**: Uses GPT-4 to analyze content quality, SEO, and technical accuracy
- **PR Comments**: Posts review results as comments on pull requests
- **Issue Creation**: Creates improvement suggestion issues for main branch pushes
- **Artifact Storage**: Saves review results for 30 days

### Setup Requirements

1. **OpenAI API Key**: Add `OPENAI_API_KEY` to repository secrets
   - Go to Repository Settings > Secrets and Variables > Actions
   - Add new repository secret: `OPENAI_API_KEY`
   - Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

2. **GitHub Token**: Uses built-in `GITHUB_TOKEN` (automatically available)

### Review Criteria

The AI reviews content based on:

- **Frontmatter Completeness**: Checks required fields (title, description, date, author, categories, tags)
- **Content Quality**: Assesses writing quality, structure, and technical accuracy
- **SEO Optimization**: Suggests improvements for discoverability
- **Accessibility**: Checks heading structure and alt text
- **Technical Accuracy**: Reviews code examples and technical content

### Output

The workflow generates:
- Overall quality score (1-10)
- List of positive aspects
- Priority action items
- Frontmatter issues
- Content suggestions
- SEO improvements

## Frontmatter Validation Workflow

### File: `.github/workflows/frontmatter-validation.yml`

This workflow validates frontmatter fields and can automatically fix common issues.

### Triggers

- **Pull Request**: Validates changed markdown files
- **Manual Trigger**: Can be run manually with option to apply fixes
  - Go to Actions > Frontmatter Validation > Run workflow
  - Choose whether to apply automatic fixes

### Features

- **Validation**: Checks for missing required fields and formatting issues
- **Auto-Fix**: Can automatically add missing fields like dates, authors, categories
- **Reports**: Generates detailed validation reports
- **Safe Operations**: Preview mode shows what would be changed before applying

### Required Fields

The workflow enforces these required frontmatter fields:
- `title` - Post/page title
- `description` - Meta description for SEO
- `date` - Publication date (ISO 8601 format)
- `author` - Content author
- `categories` - Content categories (list)
- `tags` - Content tags (list)

### Recommended Fields

Additional fields that improve content management:
- `excerpt` - Short summary
- `lastmod` - Last modification date
- `draft` - Draft status (true/false)

### Auto-Fix Capabilities

When enabled, the workflow can automatically:
- Extract dates from filenames (e.g., `2024-01-01-title.md`)
- Generate descriptions from content
- Infer categories from directory structure
- Add default author information
- Set appropriate draft status
- Add modification timestamps

## Usage Examples

### Running Manual Frontmatter Validation

1. Go to Actions tab in GitHub
2. Select "Frontmatter Validation and Auto-Fix"
3. Click "Run workflow"
4. Choose "true" for `apply_fixes` to apply automatic fixes
5. Review the results in the workflow run

### Setting Up AI Review

1. Obtain OpenAI API key
2. Add to repository secrets as `OPENAI_API_KEY`
3. Create a pull request with markdown changes
4. Review the AI-generated feedback in PR comments

### Interpreting Results

#### Quality Scores
- **8-10**: Excellent content, minimal improvements needed
- **6-7**: Good content, some enhancements suggested
- **4-5**: Fair content, several improvements recommended
- **1-3**: Poor content, significant improvements required

#### Common Issues and Fixes

| Issue | Auto-Fix | Manual Action Required |
|-------|----------|----------------------|
| Missing date | ✅ Extracts from filename or uses file timestamp | - |
| Missing author | ✅ Sets to default author | Update if incorrect |
| Missing categories | ✅ Infers from directory structure | Review and refine |
| Missing description | ✅ Generates from content | Review and improve |
| Missing tags | ✅ Basic inference from content | Add relevant tags |
| Content too short | ❌ | Expand with more details |
| Missing headers | ❌ | Add section headers |
| Broken links | ❌ | Fix or remove broken links |

## Link Health Guardian Workflow

### File: `.github/workflows/link-checker.yml`

This workflow runs the Link Health Guardian to validate links across the site and generate a workflow summary, even when link checks fail.

### Triggers

- **Schedule**: Mondays at 6 AM UTC, Fridays at 6 PM UTC
- **Manual Trigger**: Configurable scope, analysis level, timeouts, and AI analysis

### Output

- Link statistics exported via `statistics.env`
- Markdown summary in the Actions run summary
- Artifact archive under `link-check-results/`

## Best Practices

### For Content Creators

1. **Use Descriptive Titles**: 30-60 characters for optimal SEO
2. **Write Meta Descriptions**: 120-160 characters summarizing content
3. **Structure Content**: Use headers (H1, H2, H3) to organize information
4. **Add Alt Text**: Provide descriptive alt text for all images
5. **Include Examples**: Add code examples and practical demonstrations
6. **Link Appropriately**: Include relevant internal and external links

### For Repository Maintainers

1. **Monitor Workflow Runs**: Check for failures and address API issues
2. **Review AI Suggestions**: Not all suggestions may be applicable
3. **Update Required Fields**: Modify validation rules as needed
4. **Manage API Costs**: Monitor OpenAI API usage
5. **Train Contributors**: Help team members understand quality standards

## Troubleshooting

### Common Issues

#### AI Review Not Working
- Check if `OPENAI_API_KEY` secret is set correctly
- Verify API key has sufficient credits
- Check workflow logs for error messages

#### Frontmatter Validation Fails
- Ensure YAML syntax is correct in frontmatter
- Check for special characters that need escaping
- Verify file encoding is UTF-8

#### Build Failures After Auto-Fix
- Review changes made by auto-fix
- Check Jekyll build logs for specific errors
- Verify frontmatter follows Jekyll conventions

### Getting Help

1. Check workflow run logs in GitHub Actions
2. Review generated reports and artifacts
3. Create an issue with workflow logs if problems persist
4. Refer to Jekyll and GitHub Actions documentation

## Configuration

### Customizing Validation Rules

Edit `frontmatter-validation.yml` to modify:
- Required fields list
- Default values
- Validation criteria
- File selection patterns

### Customizing AI Review

Edit `ai-content-review.yml` to modify:
- AI model used (currently GPT-4)
- Review criteria prompts
- Output format
- Trigger conditions

## Future Enhancements

Planned improvements include:
- Integration with additional AI providers
- More sophisticated content analysis
- Automated content improvement suggestions
- Integration with content management tools
- Performance optimization for large repositories

## Related Documentation

For comprehensive workflow documentation, see:
- **[GitHub Actions Guide](../../docs/workflows/GITHUB_ACTIONS.md)** - Complete workflow documentation
- **[Link Checker Resolution](../../docs/workflows/LINK_CHECKER_FIX_RESOLUTION.md)** - Link health fixes
- **[Link Checker Validation](../../docs/workflows/LINK_CHECKER_VALIDATION.md)** - Validation results
- **[Testing Frameworks](../../docs/testing/TESTING_FRAMEWORKS.md)** - Test infrastructure
- **[Contributing Guide](../../docs/CONTRIBUTING_DEVELOPER.md)** - Contribution workflow

## Contributing

To contribute improvements to these workflows:
1. Test changes in a fork first
2. Document any new configuration options
3. Update relevant documentation in `docs/workflows/`
4. Submit pull requests with clear descriptions
5. Follow the [Developer Contributing Guide](../../docs/CONTRIBUTING_DEVELOPER.md)

---

*This documentation is maintained as part of the IT-Journey project. For complete workflow documentation, see the [GitHub Actions Guide](../../docs/workflows/GITHUB_ACTIONS.md).*