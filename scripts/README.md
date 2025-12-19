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
6. **Placeholder Handling**: The link-checker ignores documented placeholder patterns (like `$GHUSER`, `$GIT_REPO`) via `.lycheeignore` so example links don't falsely trigger failures during CI runs.

### 🛠️ Development

#### Requirements

- Python 3.11+
- `requests` library
- Lychee link checker (auto-installed)
   - The script attempts to install Lychee automatically:
      - macOS: will try Homebrew (`brew install lychee`) when available
      - Debian/Ubuntu: will try `apt-get` when available
      - Fallback: download official tarball from GitHub releases and extract
      - Tip: In CI or restricted environments, use `--skip-install` and pre-install `lychee` via your package manager
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

#### Unit Tests

There's a small test harness that validates the parser logic for different Lychee output formats:

```bash
python3 scripts/test_link_checker.py
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

### IT-Journey Documentation
- [Scripts Instructions](../.github/instructions/scripts.instructions.md) - Standards and best practices for scripts
- [Scripts Guide](../docs/scripts/SCRIPTS_GUIDE.md) - Comprehensive scripts documentation
- [Script Cleanup Summary](../docs/scripts/CLEANUP_SUMMARY.md) - Consolidation results
- [Script Consolidation Plan](../docs/scripts/CONSOLIDATION_PLAN.md) - Organization strategy
- [Development Environment](../docs/setup/DEVELOPMENT_ENVIRONMENT.md) - Setup guide
- [Contributing Guide](../docs/CONTRIBUTING_DEVELOPER.md) - Contribution workflow

### External Documentation
- [Lychee Link Checker Documentation](https://github.com/lycheeverse/lychee)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [GitHub CLI Documentation](https://cli.github.com/manual/)

## ☁️ Azure Jekyll Deploy

The Azure Jekyll Deploy script is a comprehensive automation tool that transforms the Azure Ascension quest into a production-ready deployment solution. It provides complete automation for deploying Jekyll sites to Azure Static Web Apps with GitHub Actions CI/CD integration.

### 🚀 Features

- **Complete Azure Integration**: Automated Azure Static Web Apps setup and configuration
- **GitHub Actions CI/CD**: Full pipeline creation with deployment workflows
- **Custom Domain Support**: Automated DNS configuration and SSL certificate setup
- **Multi-Platform Compatibility**: Works on macOS, Linux, and WSL2 environments
- **Interactive & Non-Interactive Modes**: Flexible deployment options for different use cases
- **Dry-Run Capability**: Safe testing mode to preview all changes before execution
- **Comprehensive Error Handling**: Detailed logging with specific exit codes and recovery procedures
- **Security-First Design**: No hardcoded credentials, proper input validation, and secure token handling

### 📁 File Structure

```
scripts/
├── azure-jekyll-deploy.sh              # Main deployment script
├── azure-jekyll-deploy-README.md       # Comprehensive documentation
└── azure-jekyll-deploy-TESTING.md      # Testing checklist and procedures

.github/workflows/
└── azure-jekyll-deploy.yml             # Example GitHub Actions workflow
```

### 🔧 Usage

#### Quick Start

```bash
# Make executable and run interactive setup
chmod +x scripts/azure-jekyll-deploy.sh
./scripts/azure-jekyll-deploy.sh setup

# Deploy with minimal configuration
./scripts/azure-jekyll-deploy.sh deploy --app-name my-jekyll-site --github-repo https://github.com/user/repo
```

#### Advanced Usage

```bash
# Full deployment with custom domain
./scripts/azure-jekyll-deploy.sh deploy \
  --app-name production-site \
  --github-repo https://github.com/org/production-site \
  --custom-domain www.mysite.com \
  --verbose \
  --yes

# Dry-run to preview changes
./scripts/azure-jekyll-deploy.sh --dry-run deploy --app-name test-site

# Step-by-step deployment
./scripts/azure-jekyll-deploy.sh configure --jekyll-dir ./my-site
./scripts/azure-jekyll-deploy.sh azure-create --app-name my-site
./scripts/azure-jekyll-deploy.sh github-workflow --github-repo https://github.com/user/my-site
```

#### Available Commands

| Command | Description |
|---------|-------------|
| `setup` | Interactive initial setup and dependency checks |
| `deploy` | Complete end-to-end deployment |
| `configure` | Configure Jekyll site for deployment |
| `azure-create` | Create and configure Azure Static Web App |
| `github-workflow` | Setup GitHub Actions deployment pipeline |
| `domain-setup` | Configure custom domain and SSL |
| `cleanup` | Remove Azure resources |

### 🛠️ Dependencies

- **Azure CLI**: For Azure resource management
- **GitHub CLI** (optional): For automated secret setup
- **Jekyll**: Static site generator
- **Git**: Version control operations
- **curl, jq**: HTTP requests and JSON processing

### 📊 Educational Value

This script demonstrates advanced automation concepts:

- **Infrastructure as Code**: Azure resource creation via CLI commands
- **CI/CD Pipeline Design**: GitHub Actions workflow automation
- **Multi-Cloud Deployment**: Azure Static Web Apps best practices
- **Security Automation**: Secure credential handling and validation
- **Error Recovery**: Comprehensive error handling and rollback procedures
- **Cross-Platform Scripting**: Bash scripting for multiple operating systems

### 🔗 Related Documentation

- [Azure Ascension Quest](../../pages/_quests/level-0082-azure-ascension-jekyll-deployment/index.md) - Original educational content
- [Azure Jekyll Deploy README](azure-jekyll-deploy-README.md) - Complete usage guide
- [Azure Jekyll Deploy Testing](azure-jekyll-deploy-TESTING.md) - Testing procedures

## 🤖 PRD Machine

The PRD Machine is an autonomous agent that writes, maintains, and evolves perfect PRDs (Product Requirements Documents) faster and more accurately than any human PM.

### 🚀 Features

- **Single Command Sync**: `prd-machine sync` instantly produces or updates a perfect PRD.md
- **Zero Manual Writing**: Automatic ingestion of git commits, markdown files, and feature definitions
- **Conflict Detection**: Real-time detection of conflicting requirements with proposed resolutions
- **Auto-Generated Sections**: MVP, UX, API, NFR, EDGE, OOS, ROAD, RISK, DONE sections
- **Health Monitoring**: Track PRD freshness and alert when stale (> 6 hours)

### 📁 File Structure

```
scripts/
└── prd-machine/
    ├── prd-machine           # Bash wrapper script
    ├── prd-machine.py        # Main Python implementation
    └── README.md             # Detailed documentation

.github/workflows/
└── prd-sync.yml              # Automated PRD synchronization

PRD.md                        # Generated PRD document
```

### 🔧 Usage

```bash
# Generate or update PRD.md
./scripts/prd-machine/prd-machine sync

# Check PRD health status
./scripts/prd-machine/prd-machine status

# Show detected conflicts
./scripts/prd-machine/prd-machine conflicts

# Generate with specific history window
./scripts/prd-machine/prd-machine sync --days 7
```

### 📊 Signal Sources

| Source | Type | Description |
|--------|------|-------------|
| Git Commits | Active | Subject, body, author, date |
| Markdown Files | Active | Quests, posts, docs with frontmatter |
| Features YAML | Active | Feature definitions and status |

### 🔄 CI/CD Integration

The PRD Machine runs automatically via GitHub Actions:
- **Scheduled**: Every 6 hours to maintain freshness
- **On Push**: When relevant content changes (quests, posts, features)
- **Manual**: Via workflow dispatch for on-demand sync

### 🔗 Related Documentation

- [PRD Machine README](prd-machine/README.md) - Complete usage guide
- [PRD.md](../PRD.md) - Generated product requirements document

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
