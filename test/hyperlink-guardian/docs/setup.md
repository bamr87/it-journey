# Guardian 2.0 Setup Guide

This guide will help you set up and configure the Guardian 2.0 Hyperlink Testing Framework for your Jekyll-based GitHub Pages site.

## 🚀 Quick Start

### Prerequisites

- **Git repository** with Jekyll-based GitHub Pages site
- **GitHub Actions** enabled on your repository
- **Python 3.7+** for local development and AI analysis
- **Bash 4.0+** for the testing scripts
- **curl, jq, bc** system utilities

### 1. Installation

#### Option A: Automated Setup (Recommended)

```bash
# Clone or navigate to your repository
cd /path/to/your/jekyll-site

# Run the automated setup
./test/hyperlink-guardian/scripts/validate.sh setup
```

#### Option B: Manual Setup

```bash
# Ensure required directories exist
mkdir -p test-results/{artifacts,reports}

# Make scripts executable
chmod +x test/hyperlink-guardian/scripts/*.sh
chmod +x test/hyperlink-guardian/scripts/*.py

# Install Python dependencies
pip3 install openai requests pyyaml --break-system-packages

# Install optional Node.js dependencies
npm install -g markdown-link-check
```

### 2. Configuration

#### Basic Configuration

The Guardian 2.0 system works out of the box with sensible defaults, but you can customize it using configuration files:

**Main Configuration**: `test/hyperlink-guardian/config/guardian-config.yml`

```yaml
# Site configuration
site:
  url: "https://your-username.github.io/your-repo"
  name: "Your Site Name"

# Testing parameters
testing:
  max_parallel: 10
  timeout: 30
  retry_count: 2

# AI analysis configuration
ai_analysis:
  model: "gpt-4"
  max_tokens: 3000
  temperature: 0.3
```

**URL Exclusions**: `test/hyperlink-guardian/config/exclusions.txt`

```txt
# Add regex patterns for URLs to exclude
localhost
127\.0\.0\.1
example\.com
```

#### GitHub Secrets Configuration

For AI-powered analysis, configure the OpenAI API key:

1. Go to your repository's **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `OPENAI_API_KEY`
4. Value: Your OpenAI API key
5. Click **Add secret**

### 3. Validation

Verify your Guardian 2.0 installation:

```bash
# Validate the complete setup
./test/hyperlink-guardian/scripts/validate.sh validate

# Check dependencies only
./test/hyperlink-guardian/scripts/validate.sh dependencies

# Quick functionality test
./test/hyperlink-guardian/scripts/validate.sh test
```

## 🔧 Advanced Configuration

### Environment Variables

Guardian 2.0 supports environment variable overrides:

```bash
export SITE_URL="https://your-site.com"
export MAX_PARALLEL=20
export TIMEOUT=45
export VERBOSE=true
export OPENAI_API_KEY="your-api-key"
```

### Custom Configuration Files

Create custom configuration files for different environments:

```bash
# Development configuration
cp test/hyperlink-guardian/config/guardian-config.yml dev-config.yml

# Use custom configuration
./test/hyperlink-guardian/scripts/guardian.sh --config dev-config.yml
```

### GitHub Actions Workflow Customization

The workflow is located at `.github/workflows/hyperlink-guardian.yml`. Key customization points:

```yaml
# Change schedule (currently daily at 3 AM UTC)
on:
  schedule:
    - cron: '0 3 * * *'  # Modify this line

# Modify environment variables
env:
  MAX_PARALLEL: 15      # Increase parallel processing
  TIMEOUT: 45           # Increase timeout for slow sites
```

## 🧪 Local Testing

### Basic Local Testing

```bash
# Run a basic scan
./test/hyperlink-guardian/scripts/guardian.sh

# Run with verbose output
./test/hyperlink-guardian/scripts/guardian.sh --verbose

# Test only internal links
./test/hyperlink-guardian/scripts/guardian.sh --internal-only

# Exclude specific domains
./test/hyperlink-guardian/scripts/guardian.sh --exclude "github\.com|localhost"
```

### AI Analysis Testing

```bash
# Set up OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run AI analysis on existing results
python3 test/hyperlink-guardian/scripts/ai-analyzer.py \
  --input ./test-results \
  --output ./ai-analysis.json \
  --verbose
```

### Development Testing

```bash
# Quick validation without full scan
./test/hyperlink-guardian/scripts/validate.sh test --quick

# Dry run to see what would be executed
./test/hyperlink-guardian/scripts/guardian.sh --dry-run

# Test with limited URLs for development
MAX_PARALLEL=2 TIMEOUT=10 \
./test/hyperlink-guardian/scripts/guardian.sh --parallel 2 --timeout 10
```

## 🔀 Migration from Guardian 1.0

If you're upgrading from the previous hyperlink guardian system:

### 1. Backup Existing Configuration

```bash
# Backup old scripts (if they exist)
mkdir -p backup/old-guardian
cp scripts/hyperlink-guardian.sh backup/old-guardian/ 2>/dev/null || true
cp scripts/ai-link-analyzer.py backup/old-guardian/ 2>/dev/null || true
```

### 2. Update GitHub Actions Workflow

The new workflow automatically uses the Guardian 2.0 framework. No manual updates needed if you're using the refactored workflow.

### 3. Migrate Custom Configuration

```bash
# If you had custom exclusion patterns in the old system
# Add them to test/hyperlink-guardian/config/exclusions.txt

# If you had custom timeouts or parallel settings
# Add them to test/hyperlink-guardian/config/guardian-config.yml
```

### 4. Validate Migration

```bash
# Ensure everything works correctly
./test/hyperlink-guardian/scripts/validate.sh validate --verbose
```

## 🚨 Troubleshooting

### Common Issues

#### "Permission Denied" Errors

```bash
# Make all scripts executable
find test/hyperlink-guardian/scripts/ -name "*.sh" -exec chmod +x {} \;
find test/hyperlink-guardian/scripts/ -name "*.py" -exec chmod +x {} \;
```

#### "Command Not Found" Errors

```bash
# Check required dependencies
./test/hyperlink-guardian/scripts/validate.sh dependencies

# Install missing dependencies
./test/hyperlink-guardian/scripts/validate.sh setup
```

#### Python Package Installation Issues

```bash
# Use --break-system-packages for externally managed Python environments
pip3 install openai requests pyyaml --break-system-packages

# Or use virtual environment
python3 -m venv guardian-env
source guardian-env/bin/activate
pip install openai requests pyyaml
```

#### No Links Found

```bash
# Check if you're in the correct directory
pwd  # Should be your Jekyll site root

# Verify file patterns
find . -name "*.md" | head -5

# Run with verbose output
./test/hyperlink-guardian/scripts/guardian.sh --verbose
```

#### AI Analysis Fails

```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test API connectivity
python3 -c "import openai; print('OpenAI library works')"

# Run with fallback analysis
# Guardian 2.0 automatically provides enhanced fallback when AI is unavailable
```

### Debug Mode

Enable comprehensive debugging:

```bash
# Enable debug output
export DEBUG=true
export VERBOSE=true

# Run with maximum debugging
./test/hyperlink-guardian/scripts/guardian.sh --verbose 2>&1 | tee debug.log
```

### Log Files

Guardian 2.0 generates comprehensive logs:

```
test-results/
├── artifacts/
│   ├── guardian.log          # Main execution log
│   ├── ai-analyzer.log       # AI analysis log
│   └── raw-links.txt         # All discovered links
└── summary.json              # High-level results
```

## 📚 Configuration Reference

### Guardian Configuration File Structure

```yaml
# Complete configuration example
site:
  url: "https://example.github.io/repo"
  name: "Example Site"
  description: "Educational platform"

testing:
  max_parallel: 10
  timeout: 30
  retry_count: 2
  retry_delay: 5
  internal_only: false
  user_agent: "Guardian-2.0"
  
  # Performance thresholds
  slow_response_threshold: 5.0
  critical_response_threshold: 10.0

exclusions:
  patterns:
    - "localhost"
    - "127\\.0\\.0\\.1"
    - "example\\.com"
  url_patterns:
    - "^#.*"
    - "^mailto:"
    - "^tel:"

ai_analysis:
  model: "gpt-4"
  max_tokens: 3000
  temperature: 0.3
  enable_fallback: true
  fallback_model: "gpt-3.5-turbo"

output:
  base_directory: "test-results"
  artifacts:
    retention_days: 30
    include_raw_data: true

github:
  create_issues: true
  issue_labels:
    - "automated-report"
    - "guardian-2.0"
  close_old_issues: true
  old_issue_threshold_days: 7

monitoring:
  track_response_times: true
  track_success_rates: true
  track_error_patterns: true
  enable_trend_analysis: true

educational:
  prioritize_learning_resources: true
  analyze_quest_links: true
  assess_learner_impact: true

development:
  verbose_logging: false
  debug_mode: false
  test_mode: false
```

### Command Line Options

```bash
# Guardian script options
./test/hyperlink-guardian/scripts/guardian.sh [OPTIONS]

Options:
  -h, --help              Show help message
  -v, --verbose           Enable verbose output
  -u, --url URL           Set target site URL
  -o, --output DIR        Set output directory
  -p, --parallel NUM      Set max parallel tests
  -t, --timeout SEC       Set request timeout
  -r, --retry NUM         Set retry count
  -c, --config FILE       Load configuration file
  --internal-only         Test only internal links
  --exclude PATTERN       Exclude URLs matching regex

# AI analyzer options
python3 test/hyperlink-guardian/scripts/ai-analyzer.py [OPTIONS]

Options:
  -h, --help              Show help message
  -i, --input DIR         Input directory with scan results
  -o, --output FILE       Output file for analysis
  -m, --model MODEL       OpenAI model to use
  -c, --config FILE       Configuration file
  -v, --verbose           Enable verbose logging

# Validation script options
./test/hyperlink-guardian/scripts/validate.sh [COMMAND] [OPTIONS]

Commands:
  setup                   Set up development environment
  validate                Full validation
  test                    Quick functionality test
  dependencies            Check dependencies
  config                  Validate configuration

Options:
  -h, --help              Show help message
  -v, --verbose           Enable verbose output
  -d, --dry-run           Show what would be done
  -q, --quick             Quick tests only
```

## 🎯 Next Steps

After successful setup:

1. **Test the System**: Run a manual workflow trigger to verify everything works
2. **Customize Configuration**: Adjust settings for your specific site needs
3. **Set Up Monitoring**: Monitor the daily reports and adjust as needed
4. **Explore Advanced Features**: Investigate AI analysis capabilities and performance monitoring
5. **Contribute**: Consider contributing improvements back to the IT-Journey project

## 🔗 Related Documentation

- [Guardian 2.0 Usage Guide](usage.md)
- [Guardian 2.0 Troubleshooting](troubleshooting.md)
- [Main Test Directory README](../README.md)
- [Hyperlink Guardian Quest](../../../pages/_quests/link-to-the-future-automated-hyperlink-checking-and-error-reporting.md)

---

*Guardian 2.0 is part of the IT-Journey Testing Framework, designed to ensure reliable access to educational resources while providing real-world examples of modern DevOps practices.* 