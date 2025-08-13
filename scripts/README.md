# Scripts Directory

This directory contains automation scripts and tools for the IT-Journey project.

## 🔗 Hyperlink Guardian System (Moved to Test Directory)

**Important Notice**: The Hyperlink Guardian system has been **refactored and moved** to the dedicated test directory structure for better organization.

### 📍 New Location

**Guardian 2.0 is now located at**: `test/hyperlink-guardian/`

### 🎯 What Changed

- **Enhanced Architecture**: Better organized with dedicated test framework
- **Improved Configuration**: YAML-based configuration with layered overrides
- **Advanced Categorization**: Enhanced error detection and link classification
- **Better Documentation**: Comprehensive setup, usage, and troubleshooting guides
- **Validation Tools**: Built-in validation and setup assistance

### 🔗 Guardian 2.0 Resources

- **Main Documentation**: [test/README.md](../test/README.md)
- **Setup Guide**: [test/hyperlink-guardian/docs/setup.md](../test/hyperlink-guardian/docs/setup.md)
- **Usage Guide**: [test/hyperlink-guardian/docs/usage.md](../test/hyperlink-guardian/docs/usage.md)
- **Quest Documentation**: [Link to the Future Quest](../pages/_quests/link-to-the-future-automated-hyperlink-checking-and-error-reporting.md)

### 🚀 Quick Start with Guardian 2.0

```bash
# Validate and setup
./test/hyperlink-guardian/scripts/validate.sh setup

# Run basic scan
./test/hyperlink-guardian/scripts/guardian.sh

# Run with enhanced features
./test/hyperlink-guardian/scripts/guardian.sh --verbose --config test/hyperlink-guardian/config/guardian-config.yml
```

**Note**: The GitHub Actions workflow has been automatically updated to use Guardian 2.0.

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
2. Install dependencies: `npm install -g markdown-link-check`
3. Run guardian locally: `./scripts/hyperlink-guardian.sh --verbose`

### CI/CD Integration
1. Set `OPENAI_API_KEY` secret in GitHub repository settings
2. Workflow runs automatically on schedule
3. Review issues created by the guardian
4. Fix broken links as recommended

### Customization
- Modify exclusion patterns in the workflow
- Adjust parallel processing limits for performance
- Configure retry counts for flaky external services
- Customize AI analysis prompts for specific needs

## 📚 Educational Value

The Hyperlink Guardian system exemplifies several key DevOps and automation concepts:

- **Proactive Monitoring:** Early detection prevents user impact
- **AI Integration:** Intelligent analysis beyond simple status codes
- **Workflow Automation:** Complete CI/CD pipeline integration
- **Error Handling:** Graceful degradation and fallback strategies
- **Observability:** Comprehensive logging and reporting
- **Scalability:** Parallel processing and configurable limits

This system serves as both a practical tool and an educational example of modern DevOps practices in action.

## 🤝 Contributing

When adding new scripts:
1. Follow the existing naming conventions
2. Include comprehensive help documentation
3. Add error handling and logging
4. Update this README with usage examples
5. Consider educational value and learning opportunities

For the Hyperlink Guardian system specifically:
- Test locally before committing changes
- Verify AI analysis produces meaningful insights
- Ensure workflow compatibility across platforms
- Document any new configuration options
