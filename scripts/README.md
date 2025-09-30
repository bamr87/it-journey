# Scripts Directory

This directory contains automation scripts and tools for the IT-Journey project.

## 🔗 Link Health Guardian

The Link Health Guardian is a unified, comprehensive link checking system for the IT-Journey website. It provides automated link validation, intelligent analysis, and GitHub integration with minimal workflow complexity.

### 🚀 Features

- **Unified Script Architecture**: Single Python script contains all functionality
- **Minimal Workflow Logic**: GitHub Actions workflow simply calls the Python script
- **Comprehensive Link Checking**: Uses Lychee link checker for robust validation
- **AI-Powered Analysis**: OpenAI integration for intelligent failure analysis
- **Automatic Issue Creation**: Creates detailed GitHub issues with results
- **Multiple Scope Options**: Check website, internal links, docs, posts, quests, or all content
- **Flexible Analysis Levels**: Basic, standard, comprehensive, or AI-only analysis

### � File Structure

```
scripts/
└── link-checker.py          # Single unified script with all functionality

.github/workflows/
└── link-checker.yml         # Minimal workflow that calls the Python script
```

### 🔧 Usage

#### Manual Execution

```bash
# Basic website check
python3 scripts/link-checker.py --scope website

# Comprehensive analysis with AI
python3 scripts/link-checker.py --scope website --analysis-level comprehensive

# Create GitHub issue with results
python3 scripts/link-checker.py --scope website --create-issue --repository bamr87/it-journey

# Check specific content types
python3 scripts/link-checker.py --scope posts
python3 scripts/link-checker.py --scope quests  
python3 scripts/link-checker.py --scope docs
```

#### GitHub Actions Workflow

The workflow can be triggered:

1. **Manually** via GitHub Actions UI with configurable options
2. **Scheduled** runs:
   - Monday at 6 AM UTC (weekly comprehensive check)
   - Friday at 6 PM UTC (end-of-week validation)

#### Configuration Options

| Parameter | Description | Options |
|-----------|-------------|---------|
| `scope` | Content to check | `website`, `internal`, `external`, `docs`, `posts`, `quests`, `all` |
| `analysis-level` | Analysis depth | `basic`, `standard`, `comprehensive`, `ai-only` |
| `timeout` | Request timeout | `10`, `20`, `30`, `45`, `60` seconds |
| `create-issue` | Create GitHub issue | `true`, `false` |
| `ai-analysis` | Enable AI analysis | `true`, `false` |

### 🧠 AI Analysis

When enabled, the AI analysis provides:

- **Root Cause Identification**: Analyzes patterns in link failures
- **Jekyll-Specific Insights**: Identifies GitHub Pages and Jekyll-related issues
- **Prioritized Recommendations**: Actionable steps for fixing issues
- **Prevention Strategies**: Suggestions for avoiding future problems

### 📊 Output Files

The script generates comprehensive output in the specified directory:

- `lychee_results.json` - Raw link checker results
- `link_analysis.json` - Categorized failure analysis
- `ai_analysis.md` - AI-generated insights (if enabled)
- `github_issue.md` - GitHub issue content
- `statistics.env` - Key metrics for workflow integration
- `issue_url.txt` - Created issue URL (if applicable)

### 🔄 Workflow Integration

The unified approach provides:

1. **Single Point of Execution**: All logic in one Python script
2. **Minimal Workflow Complexity**: GitHub Actions simply calls the script
3. **Consistent Results**: Same behavior whether run locally or in CI
4. **Easy Maintenance**: Updates only require modifying the Python script
5. **Comprehensive Outputs**: All results available for workflow decisions

### 🛠️ Development

#### Requirements

- Python 3.11+
- `requests` library
- Lychee link checker (auto-installed)
- GitHub CLI (for issue creation)

#### Environment Variables

- `OPENAI_API_KEY` - For AI analysis (optional)
- `GITHUB_TOKEN` - For GitHub issue creation

#### Testing

```bash
# Test with dry run (no actual changes)
python3 scripts/link-checker.py --scope website --dry-run

# Test specific analysis level
python3 scripts/link-checker.py --scope internal --analysis-level basic

# Test without AI (faster execution)
python3 scripts/link-checker.py --scope docs --no-ai
```

### 📈 Architecture Benefits

#### Before: Complex Modular Approach
- 5 separate script files
- Complex workflow with embedded logic
- Multiple coordination points
- Difficult maintenance and debugging

#### After: Unified Single-Script Approach
- 1 comprehensive Python script
- Minimal workflow (just calls the script)
- Single point of truth
- Easy to maintain, test, and extend

## 🏗️ Development Scripts

### Core Scripts
- `environment-setup.sh` - Development environment configuration
- `version-manager.sh` - Version management utilities

### Deployment Scripts
- `update-settings.sh` - Configuration updates

### Content Scripts
- `append_feature.py` - Feature addition automation
- `jupyter-to-markdown.sh` - Notebook conversion

### Generated Scripts
- `zer0-to-hero-complete.sh` - Complete learning journey script
- `zer0-to-hero-generated.sh` - Auto-generated version
- Various test and extraction scripts

## 🔧 Usage Guidelines

### Local Development
1. Clone the repository
2. Install Python dependencies: `pip install requests`
3. Run link checker locally: `python3 scripts/link-checker.py --scope website --verbose`

### CI/CD Integration
1. Set `OPENAI_API_KEY` secret in GitHub repository settings (optional for AI analysis)
2. Workflow runs automatically on schedule (Monday 6 AM UTC, Friday 6 PM UTC)
3. Review issues created by the guardian when broken links are detected
4. Fix broken links as recommended by the AI analysis

### Customization
- Modify scope and analysis level in the workflow inputs
- Adjust timeout and retry settings for different network conditions
- Configure AI analysis prompts for specific insights
- Customize issue templates and labeling

## 📚 Educational Value

The Link Health Guardian system exemplifies several key DevOps and automation concepts:

- **Proactive Monitoring**: Early detection prevents user impact through automated link validation
- **AI Integration**: Intelligent analysis beyond simple status codes using OpenAI
- **Workflow Automation**: Complete CI/CD pipeline integration with GitHub Actions
- **Error Handling**: Graceful degradation and fallback strategies for API failures
- **Observability**: Comprehensive logging and reporting with artifact storage
- **Scalability**: Configurable timeouts and retry logic for different site sizes
- **Single Responsibility**: Unified script architecture for easy maintenance

This system serves as both a practical tool and an educational example of modern DevOps practices in action.

### 🔗 Related Documentation

- [Lychee Link Checker Documentation](https://github.com/lycheeverse/lychee)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [GitHub CLI Documentation](https://cli.github.com/manual/)

## 🤝 Contributing

When adding new scripts:
1. Follow the existing naming conventions
2. Include comprehensive help documentation
3. Add error handling and logging
4. Update this README with usage examples
5. Consider educational value and learning opportunities

For the Link Health Guardian system specifically:
- Test locally before committing changes: `python3 scripts/link-checker.py --scope website --dry-run`
- Verify AI analysis produces meaningful insights
- Ensure workflow compatibility across different operating systems
- Document any new configuration options or environment variables
- Follow the unified script architecture pattern for consistency
