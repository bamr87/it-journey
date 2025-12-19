# IT-Journey Developer Documentation

Welcome to the IT-Journey developer documentation. This directory contains comprehensive technical information for contributors, maintainers, and AI agents working on the IT-Journey repository.

## 📚 Documentation Structure

### Architecture
- **[Repository Structure](architecture/REPOSITORY_STRUCTURE.md)** - Complete directory tree and organization
- **[Jekyll Implementation](architecture/JEKYLL_IMPLEMENTATION.md)** - Jekyll configuration, collections, and build process
- **[About Reorganization](architecture/ABOUT_REORGANIZATION_SUMMARY.md)** - _about directory restructuring between repositories

### Standards
- **[Frontmatter Standards](standards/FRONTMATTER_STANDARDS.md)** - Content metadata requirements and templates
- **[Content Guidelines](standards/CONTENT_GUIDELINES.md)** - Writing style, formatting, and conventions
- **[Quest Template Enhancement](standards/QUEST_TEMPLATE_ENHANCEMENT_SUMMARY.md)** - Quest template system improvements

### Setup & Development
- **[Development Environment](setup/DEVELOPMENT_ENVIRONMENT.md)** - Local setup and configuration
- **[Installation Updates](setup/INSTALLATION_UPDATE.md)** - Theme installation and deployment

### Workflows & Automation
- **[GitHub Actions](workflows/GITHUB_ACTIONS.md)** - CI/CD workflows and automation
- **[Dependency Updates](workflows/DEPENDENCY_UPDATE_SUMMARY.md)** - Dependency management and build checking
- **[Link Checker Resolution](workflows/LINK_CHECKER_FIX_RESOLUTION.md)** - Link health monitoring fixes
- **[Link Checker Validation](workflows/LINK_CHECKER_VALIDATION.md)** - Validation test results
- **[Link Consolidation](workflows/LINK_CONSOLIDATION_SUMMARY.md)** - Link checker workflow consolidation

### Scripts & Tools
- **[Scripts Guide](scripts/SCRIPTS_GUIDE.md)** - Automation scripts overview and usage
- **[PRD Machine](scripts/PRD_MACHINE.md)** - Autonomous PRD generation and maintenance
- **[Cleanup Summary](scripts/CLEANUP_SUMMARY.md)** - Script consolidation results
- **[Consolidation Plan](scripts/CONSOLIDATION_PLAN.md)** - Script organization strategy

### Testing
- **[Testing Frameworks](testing/TESTING_FRAMEWORKS.md)** - Test infrastructure and validation tools

### Contributing
- **[Developer Contribution Guide](CONTRIBUTING_DEVELOPER.md)** - Technical contribution workflow

## 🎯 Quick Start for Contributors

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/bamr87/it-journey.git
cd it-journey

# Install dependencies
bundle install

# Run local development server
bundle exec jekyll serve --config _config_dev.yml
```

### 2. Understanding the Structure
- `pages/` - All content collections (_posts, _docs, _quests, _notebooks, etc.)
- `_config.yml` - Main Jekyll configuration
- `scripts/` - Automation and development tools
- `test/` - Testing frameworks and validators
- `.github/workflows/` - CI/CD automation

### 3. Making Contributions
1. Read [CONTRIBUTING_DEVELOPER.md](CONTRIBUTING_DEVELOPER.md)
2. Review [Content Guidelines](standards/CONTENT_GUIDELINES.md)
3. Follow [Frontmatter Standards](standards/FRONTMATTER_STANDARDS.md)
4. Test locally before submitting PR

## 🔑 Key Concepts

### Collections System
IT-Journey uses Jekyll collections for content organization:
- `_posts` - Blog posts and journal entries
- `_docs` - Learning resources and reference documentation
- `_quests` - Gamified learning experiences
- `_notebooks` - Jupyter notebooks and interactive content
- `_notes` - Personal development notes
- `_about` - About pages and site information
- `_quickstart` - Quick reference guides

### Content Types
Each content type has specific frontmatter requirements and conventions. See [Frontmatter Standards](standards/FRONTMATTER_STANDARDS.md) for details.

### Automation
The repository includes extensive automation:
- **Link Health Guardian** - Automated link validation with AI analysis
- **Content Organization** - Automated post organization and cleanup
- **Build Validation** - Jekyll build verification
- **Dependency Checking** - Security and version monitoring

## 🛠️ Development Tools

### Local Development
```bash
# Development server with live reload
bundle exec jekyll serve --config _config_dev.yml --livereload

# Docker development
docker-compose up

# Build only (no server)
bundle exec jekyll build
```

### Testing
```bash
# Run link checker locally
python3 scripts/link-checker.py --scope website

# Validate frontmatter
# (Automated via GitHub Actions)

# Test quest validator
cd test/quest-validator && python validator.py
```

### Scripts
```bash
# Core scripts
scripts/core/environment-setup.sh
scripts/core/version-manager.sh

# Development scripts
scripts/development/build/build-site.sh
scripts/development/content/jupyter-to-markdown.sh
```

## 🤖 AI Agent Guidelines

### Context for AI Assistants
When working with this repository, AI agents should:
1. **Read architecture docs first** - Understand structure before making changes
2. **Follow standards strictly** - Adhere to frontmatter and content guidelines
3. **Check existing patterns** - Review similar content before creating new
4. **Test locally** - Verify builds succeed before committing
5. **Reference documentation** - Use these docs for authoritative information

### Key Files for AI Context
- `_config.yml` - Site configuration and collection definitions
- `docs/architecture/REPOSITORY_STRUCTURE.md` - Complete directory layout
- `docs/standards/FRONTMATTER_STANDARDS.md` - Content metadata requirements
- `docs/architecture/JEKYLL_IMPLEMENTATION.md` - Build system details

### Common AI Tasks
- **Creating new content** → Follow [Frontmatter Standards](standards/FRONTMATTER_STANDARDS.md)
- **Modifying scripts** → Review [Scripts Guide](scripts/SCRIPTS_GUIDE.md)
- **Updating workflows** → Check [GitHub Actions](workflows/GITHUB_ACTIONS.md)
- **Fixing broken links** → See [Link Checker Resolution](workflows/LINK_CHECKER_FIX_RESOLUTION.md)

## 📖 Additional Resources

### External Documentation
- [Jekyll Official Docs](https://jekyllrb.com/docs/)
- [Liquid Template Language](https://shopify.github.io/liquid/)
- [GitHub Pages](https://docs.github.com/en/pages)
- [zer0-mistakes Theme](https://github.com/bamr87/zer0-mistakes)

### Learning Resources
The `pages/_docs/` directory contains educational content for learners:
- Jekyll usage tutorials (specific to this repo)
- Tool and technology references
- External documentation links

These are separate from developer documentation and focus on the learning journey.

## 🆘 Getting Help

### Documentation Issues
- If documentation is unclear or incorrect, open an issue
- Suggest improvements via pull requests
- Ask questions in GitHub Discussions

### Development Issues
- Check [Common Setup Issues](setup/DEVELOPMENT_ENVIRONMENT.md#troubleshooting)
- Review [Workflow Troubleshooting](workflows/GITHUB_ACTIONS.md#troubleshooting)
- Search existing issues before creating new ones

### Contact
- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - Questions and community support
- **Pull Requests** - Code and documentation contributions

---

## 📝 Documentation Maintenance

This documentation is maintained alongside the codebase. When making changes:
- Update relevant documentation in the same PR as code changes
- Keep examples current and tested
- Follow the established documentation structure
- Add new sections as needed for new features

**Last Updated**: 2025-11-26  
**Documentation Version**: 1.1.0

