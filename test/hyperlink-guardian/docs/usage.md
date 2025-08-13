# Guardian 2.0 Usage Guide

This guide covers how to effectively use the Guardian 2.0 Hyperlink Testing Framework for maintaining link health in your Jekyll-based educational platform.

## 🎯 Overview

Guardian 2.0 provides three main interaction methods:
1. **Automated GitHub Actions** - Daily scheduled scans with AI analysis
2. **Local Command Line** - Manual testing and development
3. **Configuration Management** - Customizing behavior and thresholds

## 🤖 GitHub Actions Workflow

### Automatic Execution

The Guardian 2.0 workflow runs automatically every day at 3:00 AM UTC. It:

1. **Scans** all markdown and HTML files for links
2. **Tests** each unique URL with retry logic
3. **Categorizes** failures using enhanced error detection
4. **Analyzes** results with AI-powered insights (if configured)
5. **Creates** detailed GitHub issues with recommendations
6. **Cleans up** old reports automatically

### Manual Execution

You can trigger the workflow manually:

1. Go to **Actions** tab in your GitHub repository
2. Select **🔗 Hyperlink Guardian - Daily Link Health Check**
3. Click **Run workflow**
4. Configure optional parameters:
   - **Force full site scan**: Override change detection
   - **Maximum parallel tests**: Adjust for performance

### Workflow Parameters

```yaml
# Manual trigger options
force_scan: false           # Force full scan even if no changes
max_parallel: 10           # Maximum parallel link tests
```

### Understanding Results

The workflow creates detailed GitHub issues with:

#### Executive Summary
- Overall health grade (A+ to F)
- Critical issues requiring immediate attention
- Educational impact assessment

#### Enhanced Categorization
- **SSL Certificate Issues**: Certificate problems
- **DNS Resolution Failures**: Domain name resolution problems
- **Connection Timeouts**: Network connectivity issues
- **External Documentation**: Broken documentation links
- **GitHub Repositories**: Repository or GitHub-specific issues
- **Internal Links**: Site-internal navigation problems

#### Priority Actions
- **High Priority**: Immediate fixes needed for critical educational content
- **Medium Priority**: Important but not blocking issues
- **Low Priority**: Nice-to-have improvements

## 💻 Local Command Line Usage

### Basic Scanning

```bash
# Basic scan with default settings
./test/hyperlink-guardian/scripts/guardian.sh

# Scan with verbose output
./test/hyperlink-guardian/scripts/guardian.sh --verbose

# Custom site URL
./test/hyperlink-guardian/scripts/guardian.sh --url https://example.com

# Custom output directory
./test/hyperlink-guardian/scripts/guardian.sh --output ./my-results
```

### Advanced Scanning Options

```bash
# Test only internal links
./test/hyperlink-guardian/scripts/guardian.sh --internal-only

# Exclude specific domains
./test/hyperlink-guardian/scripts/guardian.sh --exclude "github\.com|localhost"

# Adjust performance settings
./test/hyperlink-guardian/scripts/guardian.sh --parallel 20 --timeout 45

# Use custom configuration
./test/hyperlink-guardian/scripts/guardian.sh --config my-config.yml

# Combine multiple options
./test/hyperlink-guardian/scripts/guardian.sh \
  --verbose \
  --parallel 15 \
  --timeout 30 \
  --exclude "example\.com" \
  --output ./test-results
```

### Environment Variable Overrides

```bash
# Set environment variables for session
export SITE_URL="https://my-site.com"
export MAX_PARALLEL=20
export TIMEOUT=45
export VERBOSE=true

# Run with environment settings
./test/hyperlink-guardian/scripts/guardian.sh

# Or set for single command
VERBOSE=true MAX_PARALLEL=5 \
./test/hyperlink-guardian/scripts/guardian.sh --parallel 5
```

## 🧠 AI Analysis

### Local AI Analysis

```bash
# Run AI analysis on existing results
export OPENAI_API_KEY="your-api-key"
python3 test/hyperlink-guardian/scripts/ai-analyzer.py \
  --input ./test-results \
  --output ./ai-analysis.json

# Use different AI model
python3 test/hyperlink-guardian/scripts/ai-analyzer.py \
  --model gpt-3.5-turbo \
  --input ./test-results \
  --verbose

# Custom configuration
python3 test/hyperlink-guardian/scripts/ai-analyzer.py \
  --config ./custom-ai-config.yml \
  --input ./test-results
```

### AI Analysis Output Structure

The AI analysis provides structured insights:

```json
{
  "executive_summary": "High-level assessment of link health",
  "health_assessment": {
    "overall_grade": "B+",
    "critical_issues": ["List of urgent problems"],
    "educational_impact_level": "medium"
  },
  "category_analysis": {
    "external_documentation": {
      "impact": "high",
      "root_cause": "Documentation sites moved",
      "recommended_actions": ["Update to new URLs"]
    }
  },
  "priority_actions": [
    {
      "action": "Fix broken quest navigation",
      "priority": "high",
      "educational_benefit": "Prevents learner frustration"
    }
  ]
}
```

## 🔧 Configuration Management

### Configuration Hierarchy

Guardian 2.0 uses a layered configuration system:

1. **Built-in defaults** - Sensible starting values
2. **Configuration files** - YAML/JSON overrides
3. **Environment variables** - Runtime adjustments
4. **Command line arguments** - Per-execution customization

### Site Configuration

```yaml
# test/hyperlink-guardian/config/guardian-config.yml
site:
  url: "https://your-site.github.io/repo"
  name: "Your Educational Platform"
  description: "Learning resources and tutorials"
```

### Testing Parameters

```yaml
testing:
  max_parallel: 15              # Parallel link tests
  timeout: 45                   # Request timeout (seconds)
  retry_count: 3                # Number of retries
  retry_delay: 5                # Delay between retries
  internal_only: false          # Test internal links only
  
  # Performance thresholds
  slow_response_threshold: 5.0  # Mark as slow (seconds)
  critical_response_threshold: 10.0  # Mark as critical
```

### URL Exclusions

```yaml
exclusions:
  patterns:
    - "localhost"
    - "127\\.0\\.0\\.1"
    - "example\\.com"
    - "\\{\\{.*\\}\\}"  # Jekyll variables
  
  url_patterns:
    - "^#.*"            # Anchor links
    - "^mailto:"        # Email links
    - "^tel:"           # Phone links
```

### AI Configuration

```yaml
ai_analysis:
  model: "gpt-4"
  max_tokens: 3000
  temperature: 0.3
  
  # Fallback settings
  enable_fallback: true
  fallback_model: "gpt-3.5-turbo"
```

### Educational Platform Settings

```yaml
educational:
  prioritize_learning_resources: true
  analyze_quest_links: true
  analyze_tutorial_links: true
  assess_learner_impact: true
  assess_content_accessibility: true
```

## 📊 Understanding Results

### Output Files Structure

```
test-results/
├── summary.json              # High-level statistics and metadata
├── detailed-results.csv      # Complete test results with timestamps
├── broken-links.json        # Categorized broken link analysis
├── ai-analysis.json         # AI-generated insights (if available)
├── artifacts/               # Supporting files and logs
│   ├── guardian.log         # Execution log
│   ├── ai-analyzer.log      # AI analysis log
│   ├── raw-links.txt        # All discovered links
│   └── processed-links.txt  # Normalized and categorized links
└── reports/                 # Generated reports (future)
```

### Summary Statistics

```json
{
  "summary_statistics": {
    "total_links": 150,
    "working_links": 142,
    "broken_links": 8,
    "redirects": 3,
    "success_rate": 94.67,
    "average_response_time": 1.23
  }
}
```

### Enhanced Error Categorization

Guardian 2.0 provides detailed error classification:

- **`ssl_error`**: SSL certificate issues
- **`dns_error`**: Domain name resolution failures
- **`timeout`**: Connection or response timeouts
- **`connection_refused`**: Server actively refusing connections
- **`not_found`**: HTTP 404 errors
- **`server_error`**: HTTP 5xx errors
- **`client_error`**: HTTP 4xx errors (other than 404)

### Link Type Classification

- **`internal_absolute`**: Site-internal absolute paths (`/path/to/page`)
- **`internal_relative`**: Site-internal relative paths (`./page.html`)
- **`internal_full`**: Full URLs pointing to same site
- **`external`**: Links to other domains
- **`external_relative`**: Relative links that resolve externally

## 🚀 Performance Optimization

### Parallel Processing

```bash
# Conservative (slow connections)
./test/hyperlink-guardian/scripts/guardian.sh --parallel 5

# Balanced (default)
./test/hyperlink-guardian/scripts/guardian.sh --parallel 10

# Aggressive (fast connections)
./test/hyperlink-guardian/scripts/guardian.sh --parallel 20

# Maximum (use with caution)
./test/hyperlink-guardian/scripts/guardian.sh --parallel 50
```

### Timeout Configuration

```bash
# Quick test (may miss slow sites)
./test/hyperlink-guardian/scripts/guardian.sh --timeout 10

# Balanced (default)
./test/hyperlink-guardian/scripts/guardian.sh --timeout 30

# Patient (for slow educational sites)
./test/hyperlink-guardian/scripts/guardian.sh --timeout 60
```

### Exclusion Strategies

```bash
# Exclude known slow domains
./test/hyperlink-guardian/scripts/guardian.sh \
  --exclude "slow-academic-site\.edu|overloaded-cdn\.com"

# Test only critical links
./test/hyperlink-guardian/scripts/guardian.sh \
  --internal-only
```

## 🎓 Educational Platform Best Practices

### Quest and Tutorial Links

Guardian 2.0 automatically categorizes educational content:

```yaml
# Configuration for educational analysis
educational:
  prioritize_learning_resources: true
  analyze_quest_links: true        # Links in learning quests
  analyze_tutorial_links: true     # Tutorial navigation
  analyze_reference_links: true    # External references
```

### Learner Impact Assessment

The AI analysis considers educational impact:

- **High Impact**: Broken links in core learning paths
- **Medium Impact**: Supplementary resource failures
- **Low Impact**: Non-essential external references

### Content Accessibility

Guardian 2.0 evaluates how broken links affect:

- **Learning Journey Continuity**: Sequential tutorial progress
- **Resource Availability**: Access to external tools and documentation
- **Navigation Flow**: Site structure and wayfinding

## 🔍 Monitoring and Alerting

### GitHub Issue Labels

Guardian 2.0 uses consistent labeling:

- `guardian-2.0`: All reports from the new system
- `automated-report`: Machine-generated issues
- `links`: Link-related problems
- `bug`: Broken functionality (when links are broken)
- `maintenance`: Routine monitoring (when all links work)

### Issue Lifecycle

1. **Creation**: New issues for each scan with problems
2. **Classification**: Automatic labeling and prioritization
3. **Cleanup**: Old issues closed after 7 days
4. **History**: Searchable record of link health over time

### Performance Monitoring

Track key metrics over time:

```yaml
monitoring:
  track_response_times: true
  track_success_rates: true
  track_error_patterns: true
  enable_trend_analysis: true
  trend_window_days: 30
```

## 🛠️ Development and Testing

### Development Mode

```bash
# Quick validation without full scan
./test/hyperlink-guardian/scripts/validate.sh test --quick

# Test with limited parallel processes
MAX_PARALLEL=2 TIMEOUT=10 \
./test/hyperlink-guardian/scripts/guardian.sh --parallel 2

# Dry run to see what would be executed
DEBUG=true VERBOSE=true \
./test/hyperlink-guardian/scripts/guardian.sh --verbose
```

### Local Testing Workflow

```bash
# 1. Validate setup
./test/hyperlink-guardian/scripts/validate.sh validate

# 2. Run basic test
./test/hyperlink-guardian/scripts/guardian.sh --verbose

# 3. Check results
cat test-results/summary.json | jq '.'

# 4. Test AI analysis (if API key available)
export OPENAI_API_KEY="your-key"
python3 test/hyperlink-guardian/scripts/ai-analyzer.py \
  --input ./test-results \
  --verbose
```

### Debugging

```bash
# Enable comprehensive debugging
export DEBUG=true
export VERBOSE=true

# Run with full logging
./test/hyperlink-guardian/scripts/guardian.sh --verbose 2>&1 | tee debug.log

# Check specific components
./test/hyperlink-guardian/scripts/validate.sh dependencies
./test/hyperlink-guardian/scripts/validate.sh config
```

## 🚨 Error Handling and Recovery

### Common Failure Scenarios

#### Network Issues
```bash
# Increase timeouts for unstable connections
./test/hyperlink-guardian/scripts/guardian.sh --timeout 60 --retry 3
```

#### Rate Limiting
```bash
# Reduce parallel requests
./test/hyperlink-guardian/scripts/guardian.sh --parallel 5
```

#### Large Sites
```bash
# Use configuration file for complex settings
./test/hyperlink-guardian/scripts/guardian.sh --config large-site-config.yml
```

### Recovery Strategies

1. **Graceful Degradation**: AI analysis falls back when API unavailable
2. **Retry Logic**: Automatic retries for transient failures
3. **Progress Preservation**: Results saved incrementally
4. **Error Categorization**: Detailed classification for targeted fixes

## 📈 Advanced Usage Patterns

### Multi-Environment Testing

```bash
# Test different environments
./test/hyperlink-guardian/scripts/guardian.sh --url https://staging.example.com
./test/hyperlink-guardian/scripts/guardian.sh --url https://prod.example.com

# Compare results
diff -u staging-results/summary.json prod-results/summary.json
```

### Custom Analysis Scripts

```python
# Load Guardian 2.0 results for custom analysis
import json

with open('test-results/summary.json') as f:
    summary = json.load(f)

# Analyze patterns
broken_by_domain = {}
for link in summary['broken_link_details']:
    domain = urlparse(link['url']).netloc
    broken_by_domain[domain] = broken_by_domain.get(domain, 0) + 1

print("Most problematic domains:")
for domain, count in sorted(broken_by_domain.items(), key=lambda x: x[1], reverse=True):
    print(f"  {domain}: {count} broken links")
```

### Integration with External Tools

```bash
# Export results for external analysis
jq '.broken_link_details[] | .url' test-results/summary.json > broken-urls.txt

# Generate reports for stakeholders
python3 -c "
import json
with open('test-results/summary.json') as f:
    data = json.load(f)
print(f'Link Health Report: {data[\"summary_statistics\"][\"success_rate\"]}% success rate')
"
```

## 🔗 Related Workflows

### Pre-Commit Hooks

```bash
# Add Guardian 2.0 validation to git hooks
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
echo "Running Guardian 2.0 quick validation..."
./test/hyperlink-guardian/scripts/validate.sh test --quick
EOF
chmod +x .git/hooks/pre-push
```

### CI/CD Integration

```yaml
# Add to other GitHub Actions workflows
- name: Validate Links
  run: ./test/hyperlink-guardian/scripts/guardian.sh --internal-only
```

---

*Guardian 2.0 empowers educational platforms with comprehensive link health monitoring, intelligent analysis, and proactive maintenance - ensuring learners always have reliable access to educational resources.* 