# Testing Frameworks

This document provides an overview of the testing infrastructure in the IT-Journey repository.

## Overview

The IT-Journey repository includes comprehensive testing frameworks to ensure content quality, link health, and structural integrity. All testing code is located in the `test/` directory.

## Test Directory Structure

```
test/
├── hyperlink-guardian/       # Link validation and health monitoring
│   ├── docs/                # Guardian documentation
│   ├── config.yml           # Configuration file
│   ├── validator.py         # Core validation logic
│   └── README.md
├── quest-validator/          # Quest content structure validation
│   ├── docs/                # Validator documentation
│   ├── validator.py         # Quest validation logic
│   ├── schemas/             # JSON schemas for validation
│   └── README.md
├── test-results/             # Test output artifacts
└── README.md                 # Testing overview
```

## Hyperlink Guardian

### Purpose

The Hyperlink Guardian is a comprehensive link validation system that proactively monitors link health across the IT-Journey website.

### Location

- **Main Script:** `scripts/link-checker.py` (unified implementation)
- **Documentation:** `test/hyperlink-guardian/docs/`
- **Workflow:** `.github/workflows/link-checker.yml`

### Features

**Core Capabilities:**
- Comprehensive link checking using Lychee link checker
- Multiple scope options (website, internal, external, docs, posts, quests)
- Configurable timeout and retry settings
- Categorized failure analysis
- AI-powered root cause identification (optional)
- Automated GitHub issue creation

**Analysis Levels:**
- **Basic:** Link checking only
- **Standard:** Link checking + failure categorization
- **Comprehensive:** Full analysis + AI insights
- **AI-Only:** Analyze existing results without re-checking

### Usage

**Command Line:**
```bash
# Basic website check
python3 scripts/link-checker.py --scope website

# Comprehensive analysis with AI
python3 scripts/link-checker.py \
  --scope website \
  --analysis-level comprehensive \
  --timeout 30 \
  --output-dir link-check-results

# Create GitHub issue with results
python3 scripts/link-checker.py \
  --scope website \
  --create-issue \
  --repository bamr87/it-journey
```

**GitHub Actions:**
```yaml
# Manual dispatch via Actions UI
Actions > Link Health Guardian > Run workflow
# Configure options in UI
```

### Configuration

**Scope Options:**
- `website` - Full website check (default)
- `internal` - Internal links only
- `external` - External links only
- `docs` - Documentation directory only
- `posts` - Blog posts only
- `quests` - Quest content only
- `all` - Everything including experimental

**Timeout Settings:**
- `10` seconds - Fast, may miss slow sites
- `20` seconds - Balanced
- `30` seconds - Recommended default
- `45` seconds - Patient
- `60` seconds - Very patient

### Output Files

```
link-check-results/
├── lychee_results.json       # Raw link checker output
├── link_analysis.json        # Categorized failures
├── ai_analysis.md            # AI insights (if enabled)
├── github_issue.md           # Issue content
├── statistics.env            # Key metrics
└── issue_url.txt             # Created issue URL
```

### AI Analysis

When enabled (`--ai-analysis` or default), the Guardian uses OpenAI GPT-4 to:
- Identify root causes of link failures
- Detect patterns across multiple failures
- Provide Jekyll-specific insights
- Suggest prioritized fixes
- Recommend prevention strategies

**Requirements:**
- `OPENAI_API_KEY` environment variable
- `requests` Python library

**Cost:** ~$0.01-0.10 per analysis depending on results size

### Integration

**CI/CD Pipeline:**
```yaml
# Scheduled runs
- Monday 6 AM UTC (weekly comprehensive)
- Friday 6 PM UTC (end-of-week validation)

# Outputs
- GitHub issues for broken links
- Workflow artifacts (30-day retention)
- Workflow summaries with health status
```

### Documentation

Comprehensive documentation available:
- **Setup Guide:** `test/hyperlink-guardian/docs/setup.md`
- **Usage Guide:** `test/hyperlink-guardian/docs/usage.md`
- **Quest:** `pages/_quests/link-to-the-future-automated-hyperlink-checking-and-error-reporting.md`

### Troubleshooting

**Common Issues:**

**Issue:** High false positive rate
```bash
# Solution: Increase timeout
python3 scripts/link-checker.py --scope website --timeout 45
```

**Issue:** AI analysis not working
```bash
# Solution: Check API key
echo $OPENAI_API_KEY
# Set if missing
export OPENAI_API_KEY="your-key-here"
```

**Issue:** Rate limiting errors
```bash
# Solution: Add delays between requests (automatic in script)
# Or check .lycheeignore file for patterns
```

## Quest Validator

### Purpose

The Quest Validator ensures quest content follows structural requirements and maintains quality standards.

### Location

- **Main Script:** `test/quest-validator/validator.py`
- **Schemas:** `test/quest-validator/schemas/`
- **Documentation:** `test/quest-validator/docs/`

### Features

**Validation Checks:**
- Frontmatter completeness and format
- Quest-specific fields (level, difficulty, xp)
- Content structure (objectives, chapters)
- Code block syntax and testing
- Asset references and links
- Achievement definitions

**Quest Requirements:**
```yaml
# Required frontmatter fields
title: "Quest Title"
date: YYYY-MM-DDTHH:MM:SS.sssZ
level: "0101"                    # Binary format
difficulty: "intermediate"        # beginner|intermediate|advanced|expert
quest_type: "automation"          # Quest category
xp: 500                          # Experience points
achievements: [...]              # List of achievements
prerequisites: [...]             # List of requirements
estimated_time: "2-3 hours"      # Completion time
platforms: [...]                 # Supported OS
```

### Usage

**Command Line:**
```bash
# Validate single quest
python3 test/quest-validator/validator.py \
  pages/_quests/my-quest.md

# Validate all quests
python3 test/quest-validator/validator.py \
  pages/_quests/

# Verbose output
python3 test/quest-validator/validator.py \
  pages/_quests/ \
  --verbose
```

### Output

**Validation Report:**
```
Quest Validation Report
=======================

File: pages/_quests/link-guardian-quest.md
Status: ✅ PASSED

Checks:
  ✅ Frontmatter valid
  ✅ Required fields present
  ✅ Quest-specific fields valid
  ✅ Content structure valid
  ✅ Code blocks syntax valid
  ⚠️  Missing platform: Windows
  ✅ Achievements defined

Summary: 6 passed, 1 warning, 0 errors
```

### Configuration

**Schema Files:**
```
test/quest-validator/schemas/
├── quest-frontmatter.json    # Frontmatter schema
├── quest-structure.json      # Content structure
└── quest-achievements.json   # Achievement definitions
```

### CI/CD Integration

Currently manual. Planned GitHub Actions integration:
```yaml
# Future workflow
name: Quest Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 test/quest-validator/validator.py pages/_quests/
```

## Running Tests Locally

### Prerequisites

```bash
# Python 3.11+
python3 --version

# Install dependencies
pip install requests pyyaml jsonschema

# Lychee link checker (for hyperlink guardian)
# macOS
brew install lychee

# Linux
curl -sSL https://github.com/lycheeverse/lychee/releases/latest/download/lychee-x86_64-unknown-linux-gnu.tar.gz | tar -xz
sudo mv lychee /usr/local/bin/
```

### Test Commands

**Link Health Check:**
```bash
# Quick internal link check
python3 scripts/link-checker.py --scope internal --timeout 10

# Comprehensive check with AI
python3 scripts/link-checker.py \
  --scope website \
  --analysis-level comprehensive
```

**Quest Validation:**
```bash
# Validate all quests
python3 test/quest-validator/validator.py pages/_quests/

# Validate specific quest
python3 test/quest-validator/validator.py \
  pages/_quests/link-guardian-quest.md
```

**Jekyll Build Test:**
```bash
# Test build
bundle exec jekyll build --verbose

# Check for issues
bundle exec jekyll doctor
```

## Test Artifacts

### Storage Location

Test results are stored in:
- `test-results/` (local, gitignored)
- GitHub Actions artifacts (30-day retention)

### Artifact Types

**Link Checker Artifacts:**
- `lychee_results.json` - Full results
- `link_analysis.json` - Categorized analysis
- `ai_analysis.md` - AI insights
- `github_issue.md` - Issue content

**Quest Validator Artifacts:**
- `validation_report.txt` - Text report
- `validation_report.json` - JSON format
- `errors.log` - Error details

## Continuous Integration

### Automated Testing

**On Every Push:**
- Jekyll build validation
- Frontmatter validation

**On Pull Requests:**
- Content quality review (AI)
- Frontmatter validation
- Build validation

**Scheduled:**
- Link health check (Mon/Fri)
- Quest validation (planned)
- Security scanning (weekly)
- Dependency checking (weekly)

### Test Results

**View in GitHub:**
```
Repository > Actions > Select workflow > View results
```

**Download Artifacts:**
```
Workflow run > Artifacts section > Download zip
```

## Best Practices

### Test-Driven Content

1. **Write tests first** (for new features)
2. **Test locally before pushing**
3. **Review test results in PRs**
4. **Fix failures promptly**
5. **Keep tests up to date**

### Performance Considerations

**Link Checking:**
- Use appropriate timeout for scope
- Check internal links more frequently than external
- Use caching when possible
- Consider rate limiting for external sites

**Quest Validation:**
- Validate changed quests only in PRs
- Full validation on schedule
- Cache validation results

### Test Maintenance

**Weekly:**
- Review failed test runs
- Update ignore patterns for link checker
- Check for flaky tests

**Monthly:**
- Update test dependencies
- Review test coverage
- Optimize slow tests

**Quarterly:**
- Audit test effectiveness
- Update schemas and validators
- Review and remove obsolete tests

## Future Enhancements

### Planned Testing Features

**Content Testing:**
- Spell checking and grammar validation
- Style guide compliance checking
- Readability scoring
- SEO optimization checks

**Integration Testing:**
- End-to-end page rendering tests
- Navigation and search testing
- Cross-browser compatibility
- Mobile responsiveness testing

**Performance Testing:**
- Page load time monitoring
- Asset size optimization
- Build time tracking

## Additional Resources

### Documentation
- [Link Checker Setup](../../test/hyperlink-guardian/docs/setup.md)
- [Link Checker Usage](../../test/hyperlink-guardian/docs/usage.md)
- [Quest Validator README](../../test/quest-validator/README.md)

### External Tools
- [Lychee Link Checker](https://github.com/lycheeverse/lychee)
- [JSON Schema](https://json-schema.org/)
- [GitHub Actions Testing](https://docs.github.com/en/actions/automating-builds-and-tests)

### Related Documentation
- [GitHub Actions](../workflows/GITHUB_ACTIONS.md)
- [Scripts Guide](../scripts/SCRIPTS_GUIDE.md)
- [Contributing Guide](../CONTRIBUTING_DEVELOPER.md)

---

**Last Updated**: 2025-10-13  
**Version**: 1.0.0

