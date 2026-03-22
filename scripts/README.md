# Scripts Directory

This directory contains automation scripts and tools for the IT-Journey project.

## 📁 Directory Structure

```
scripts/
├── core/                    # Core environment and system scripts
│   ├── environment-setup.sh
│   └── version-manager.sh
├── deployment/              # Deployment automation
│   ├── azure-jekyll-deploy.sh
│   └── update-settings.sh
├── development/             # Development workflow scripts
│   ├── build/              # Build automation
│   ├── content/            # Content management
│   └── testing/            # Testing utilities
├── generation/             # Content generation scripts
│   ├── generate_statistics.rb          # Content statistics generator (Ruby)
│   ├── generate_statistics.sh          # Statistics generator wrapper (Bash)
│   ├── generate_contributor_stats.rb   # Contributor stats generator (Ruby)
│   ├── generate_contributor_stats.sh   # Contributor stats wrapper (Bash)
│   ├── update_statistics.sh            # CI/CD statistics updater (Bash)
│   ├── generate-preview-images.sh
│   ├── generate-zer0-script.sh
│   └── zer0-to-hero-*.sh
├── lib/                     # Shared libraries
│   └── preview_generator.py
├── prd-machine/             # PRD automation tool
├── quest/                   # Quest tooling (generation, validation, linking)
├── testing/                 # Test scripts
│   └── test-generated-script.sh
├── utils/                   # Utility scripts
│   └── extract-script.sh
├── validation/             # Validation and monitoring tools
│   ├── link-checker.py
│   ├── frontmatter-validator.*
│   ├── content-freshness-check.rb
│   ├── ctr-report-generator.rb
│   ├── seo-tracker.py
│   └── requirements.txt
└── README.md
```

## 🔗 Link Health Guardian

The Link Health Guardian is a unified, comprehensive link checking system for the IT-Journey website. It provides automated link validation, cross-run caching, delta-based AI analysis, and GitHub integration with minimal workflow complexity.

### 🚀 Features

- **Unified Script Architecture**: Single Python script contains all functionality
- **Declarative Configuration**: `.lychee.toml` for all lychee settings (no hardcoded CLI args)
- **Cross-Run Caching**: `.lycheecache` persists via `actions/cache` — unchanged URLs skip re-checking
- **Delta-Based AI Analysis**: Only new broken links are sent to AI, saving tokens
- **Multi-Provider AI**: Supports OpenAI, Anthropic, or no AI (`--ai-provider`)
- **Dual Engine**: `--engine lychee` (default) or `--engine curl` (fallback, ported from guardian.sh)
- **Incremental PR Checks**: `--changed-only` checks only files modified in a PR
- **Opt-In `_site/` Scanning**: `--include-site` flag to scan build output
- **Automatic Issue Creation**: Creates detailed GitHub issues with results
- **Multiple Scope Options**: Check website, internal links, docs, posts, quests, or all content

### 📁 File Structure

```
scripts/
├── validation/              # Validation and monitoring tools
│   ├── link-checker.py      # Link health monitoring
│   ├── frontmatter-validator.py  # Frontmatter validation (Python)
│   ├── frontmatter-validator.rb  # Frontmatter validation (Ruby)
│   ├── content-freshness-check.rb # Content freshness tracking
│   ├── ctr-report-generator.rb    # SEO/CTR reports
│   ├── seo-tracker.py       # SEO tracking automation
│   └── requirements.txt     # Python dependencies
├── quest/                   # Quest tooling (generation, validation, linking)
├── deployment/               # Deployment automation
│   └── azure-jekyll-deploy.sh # Azure deployment
└── ...

.github/workflows/
└── link-checker.yml         # Minimal workflow that calls the Python script
```

### 🔧 Usage

#### Manual Execution

```bash
# Basic website check (uses lychee + .lychee.toml)
python3 scripts/validation/link-checker.py --scope website

# Comprehensive analysis with AI (OpenAI)
python3 scripts/validation/link-checker.py --scope website --ai-provider openai

# Comprehensive analysis with AI (Anthropic)
python3 scripts/validation/link-checker.py --scope website --ai-provider anthropic

# Create GitHub issue with results
python3 scripts/validation/link-checker.py --scope website --create-issue

# Check only files changed vs main branch
python3 scripts/validation/link-checker.py --changed-only

# Use curl fallback engine
python3 scripts/validation/link-checker.py --engine curl --scope docs

# Include _site/ directory
python3 scripts/validation/link-checker.py --scope website --include-site

# Dry-run AI (see prompt without calling API)
python3 scripts/validation/link-checker.py --scope website --dry-run-ai
```

#### GitHub Actions Workflow

The workflow runs in two modes:

1. **Pull Request**: Fast incremental check (changed files only, no AI) — 10 min timeout
2. **Scheduled**: Full scan every Monday at 6 AM UTC — 30 min timeout
3. **Manual dispatch**: Configurable scope, analysis level, AI provider, and issue creation

#### Configuration Options

| Parameter | Description | Options |
|-----------|-------------|---------|
| `scope` | Content to check | `website`, `internal`, `external`, `docs`, `posts`, `quests`, `all` |
| `analysis-level` | Analysis depth | `basic`, `standard`, `comprehensive`, `ai-only` |
| `engine` | Link checking engine | `lychee` (default), `curl` (fallback) |
| `ai-provider` | AI provider | `openai`, `anthropic`, `none` |
| `ai-model` | Override AI model | e.g. `gpt-4o`, `claude-sonnet-4-20250514` |
| `changed-only` | Only check changed files | Flag (no value) |
| `include-site` | Also scan `_site/` | Flag (no value) |
| `create-issue` | Create GitHub issue | Flag (no value) |
| `dry-run-ai` | Show AI prompt without calling | Flag (no value) |

#### Exclusions (Noise Reduction)

The link checker intentionally excludes non-site directories to avoid false positives, including:

- `.crush/`, `.github/`, `.devcontainer/`
- `.venv/`, `node_modules/`, `vendor/`
- `_site/`, `link-check-results/`, `logs/`, `work/`

### 🧠 AI Analysis

When enabled (`--ai-provider openai` or `--ai-provider anthropic`), the AI analysis:

- **Delta-Only**: Only sends *new* broken links (compared to baseline) to save tokens
- **Compact Prompts**: Top 10 new broken links, max 500 tokens response
- **Multi-Provider**: OpenAI (default `gpt-4o-mini`) or Anthropic (default `claude-sonnet-4-20250514`)
- **Fallback Template**: When no AI key is available, generates a template report
- **Prioritized Recommendations**: Actionable steps for fixing issues

### 📊 Output Files

The script generates comprehensive output in the specified directory:

- `lychee_results.json` - Raw link checker results
- `summary.md` - Human-readable markdown summary
- `link_analysis.json` - Categorized failure analysis
- `broken_links_baseline.json` - Baseline for delta computation (cached across CI runs)
- `ai_analysis.md` - AI-generated insights (if enabled)
- `github_issue.md` - GitHub issue content
- `statistics.env` - Key metrics for workflow integration (includes timing data)
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

- `OPENAI_API_KEY` - For OpenAI AI analysis (optional)
- `ANTHROPIC_API_KEY` - For Anthropic AI analysis (optional)
- `GITHUB_TOKEN` - For GitHub issue creation

#### Testing

```bash
# Test with dry-run AI (no actual API calls)
python3 scripts/validation/link-checker.py --scope website --dry-run-ai

# Test curl engine on a small scope
python3 scripts/validation/link-checker.py --engine curl --scope docs

# Test changed-only mode
python3 scripts/validation/link-checker.py --changed-only --dry-run-ai
```

#### Unit Tests

There's a small test harness that validates the parser logic for different Lychee output formats:

```bash
python3 scripts/validation/test_link_checker.py
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

---

## 🧭 Quest Automation

Quest tooling has been organized into a dedicated subdirectory to keep the root of `scripts/` focused on cross-cutting utilities.

### Location

- `scripts/quest/` - Quest generation, validation, and network maintenance
  - See `scripts/quest/README.md` for full usage

### Common Commands

```bash
# Validate quest network
python3 scripts/quest/validate-quest-network.py

# Remove placeholder dependencies (YAML-aware)
python3 scripts/quest/remove-placeholder-deps.py --dry-run

# Update level READMEs and quest overview
python3 scripts/quest/update-quest-links.py --dry-run

# Generate a quest network report
./scripts/quest/generate-network-report.sh
```

### Backward Compatibility

Legacy paths under `scripts/` still exist as thin wrappers and will print a deprecation warning before dispatching to `scripts/quest/`.

---

## 📊 SEO & Content Automation

A suite of Ruby scripts for SEO optimization, content validation, and freshness tracking. All scripts are designed to run in the Docker/Jekyll environment.

### Scripts Overview

| Script | Purpose | Key Features |
|--------|---------|--------------|
| `frontmatter-validator.rb` | Validate frontmatter SEO fields | Multi-type validation, SEO scoring (0-100), JSON reports |
| `ctr-report-generator.rb` | Generate SEO/CTR reports | Baseline metrics, weekly templates, opportunities analysis |
| `content-freshness-check.rb` | Track content age/staleness | Freshness categories, health scoring, priority ranking |

### 🔧 Usage

All scripts run inside Docker for consistent environment:

```bash
# Frontmatter Validation
docker-compose exec jekyll ruby scripts/validation/frontmatter-validator.rb pages/
docker-compose exec jekyll ruby scripts/validation/frontmatter-validator.rb pages/_quests/ --errors-only
docker-compose exec jekyll ruby scripts/validation/frontmatter-validator.rb pages/ -o report.json

# CTR Report Generation
docker-compose exec jekyll ruby scripts/validation/ctr-report-generator.rb --baseline
docker-compose exec jekyll ruby scripts/validation/ctr-report-generator.rb --weekly -o weekly.md
docker-compose exec jekyll ruby scripts/validation/ctr-report-generator.rb --opportunities
docker-compose exec jekyll ruby scripts/validation/ctr-report-generator.rb --json -o metrics.json

# Content Freshness Checking
docker-compose exec jekyll ruby scripts/validation/content-freshness-check.rb pages/
docker-compose exec jekyll ruby scripts/validation/content-freshness-check.rb pages/ --stale-only
docker-compose exec jekyll ruby scripts/validation/content-freshness-check.rb pages/ --json -o freshness.json
docker-compose exec jekyll ruby scripts/validation/content-freshness-check.rb pages/ --markdown -o report.md
```

### 📈 SEO Scoring (frontmatter-validator.rb)

The validator scores content on a 100-point scale:
- **Description** (40 pts): 120-160 chars optimal
- **Title** (20 pts): Presence and quality
- **Keywords** (20 pts): Relevant keywords array
- **Tags** (10 pts): Categorization tags
- **Lastmod** (5 pts): Update tracking
- **Author** (5 pts): Attribution

### 📅 Freshness Thresholds (content-freshness-check.rb)

Content is categorized by age:
- 🟢 **Fresh**: 0-30 days (good)
- 🟡 **Aging**: 31-60 days (monitor)
- 🟠 **Stale**: 61-90 days (review needed)
- 🔴 **Critical**: >90 days (update urgently)
- ❓ **Unknown**: No lastmod date

Different content types have adjusted thresholds (posts can be older than quests).

### 📊 Output Locations

Reports are saved to the TODO directory:
- `TODO/seo/data/frontmatter-report.json` - Validation data
- `TODO/seo/data/seo-metrics.json` - SEO baseline metrics
- `TODO/seo/data/freshness-report.json` - Freshness tracking
- `TODO/seo/reports/*.md` - Human-readable reports

---

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
Located in `scripts/generation/`:
- `zer0-to-hero-complete.sh` - Complete learning journey script
- `zer0-to-hero-generated.sh` - Auto-generated version
- `generate-preview-images.sh` - Preview image generation
- `generate-zer0-script.sh` - Script generation utility

### Testing Scripts
Located in `scripts/testing/`:
- `test-generated-script.sh` - Test harness for generated scripts

### Utility Scripts
Located in `scripts/utils/`:
- `extract-script.sh` - Script extraction utility

## 🔧 Usage Guidelines

### Local Development
1. Clone the repository
2. Install Python dependencies: `pip install -r scripts/validation/requirements.txt`
3. Run link checker locally: `python3 scripts/validation/link-checker.py --scope website --verbose`

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
└── deployment/
    ├── azure-jekyll-deploy.sh          # Main deployment script
    ├── azure-jekyll-deploy-README.md   # Comprehensive documentation
    └── azure-jekyll-deploy-TESTING.md  # Testing checklist and procedures

.github/workflows/
└── azure-jekyll-deploy.yml             # Example GitHub Actions workflow
```

### 🔧 Usage

#### Quick Start

```bash
# Make executable and run interactive setup
chmod +x scripts/deployment/azure-jekyll-deploy.sh
./scripts/deployment/azure-jekyll-deploy.sh setup

# Deploy with minimal configuration
./scripts/deployment/azure-jekyll-deploy.sh deploy --app-name my-jekyll-site --github-repo https://github.com/user/repo
```

#### Advanced Usage

```bash
# Full deployment with custom domain
./scripts/deployment/azure-jekyll-deploy.sh deploy \
  --app-name production-site \
  --github-repo https://github.com/org/production-site \
  --custom-domain www.mysite.com \
  --verbose \
  --yes

# Dry-run to preview changes
./scripts/deployment/azure-jekyll-deploy.sh --dry-run deploy --app-name test-site

# Step-by-step deployment
./scripts/deployment/azure-jekyll-deploy.sh configure --jekyll-dir ./my-site
./scripts/deployment/azure-jekyll-deploy.sh azure-create --app-name my-site
./scripts/deployment/azure-jekyll-deploy.sh github-workflow --github-repo https://github.com/user/my-site
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
- [Azure Jekyll Deploy README](deployment/azure-jekyll-deploy-README.md) - Complete usage guide
- [Azure Jekyll Deploy Testing](deployment/azure-jekyll-deploy-TESTING.md) - Testing procedures

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
- Test locally before committing changes: `python3 scripts/validation/link-checker.py --scope website --dry-run`
- Verify AI analysis produces meaningful insights
- Ensure workflow compatibility across different operating systems
- Document any new configuration options or environment variables
- Follow the unified script architecture pattern for consistency
