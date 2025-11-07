---
title: Contributing
description: How to contribute to IT-Journey
slug: contributing
lastmod: 2025-11-02T00:00:00.000Z
---

# Contributing to IT-Journey

Thank you for your interest in contributing to IT-Journey! We welcome contributions from developers, content creators, and learners of all experience levels.

## Quick Start

1. **Read the Developer Guide**: See the comprehensive [Developer Contributing Guide](docs/CONTRIBUTING_DEVELOPER.md)
2. **Setup Your Environment**: Follow the [Development Environment Setup](docs/setup/DEVELOPMENT_ENVIRONMENT.md)
3. **Understand the Structure**: Review [Repository Structure](docs/architecture/REPOSITORY_STRUCTURE.md)
4. **Follow Standards**: Check [Content Guidelines](docs/standards/CONTENT_GUIDELINES.md) and [Frontmatter Standards](docs/standards/FRONTMATTER_STANDARDS.md)

## 🚀 First-Time Contributor Fast Track

**New here? Make your first contribution in under 5 minutes!**

Perfect first contributions that require no setup:
- Fix a typo in documentation
- Improve a README
- Add clarifying comments to code examples

```bash
# 1. Fork this repo on GitHub (click "Fork" button)

# 2. Clone and create branch (replace YOUR-USERNAME)
git clone https://github.com/YOUR-USERNAME/it-journey.git
cd it-journey
git checkout -b fix/my-first-contribution

# 3. Make your change (example: fix typo in this file)
# Edit CONTRIBUTING.md or any documentation file

# 4. Commit and push
git add .
git commit -m "docs: fix typo in CONTRIBUTING.md"
git push origin fix/my-first-contribution

# 5. Create Pull Request on GitHub
```

**That's it!** Once you've made your first contribution, explore the [full developer guide](docs/CONTRIBUTING_DEVELOPER.md) for more complex contributions.

## Documentation

All technical documentation for contributors has been organized as follows:

### For Human Contributors
- **[Developer Contributing Guide](docs/CONTRIBUTING_DEVELOPER.md)** - Complete contribution workflow
- **[Web Contributing Page](/about/contributing/)** - User-facing guide on it-journey.dev
- **[Repository Structure](docs/architecture/REPOSITORY_STRUCTURE.md)** - Directory organization
- **[Development Environment](docs/setup/DEVELOPMENT_ENVIRONMENT.md)** - Setup instructions
- **[Content Guidelines](docs/standards/CONTENT_GUIDELINES.md)** - Writing standards
- **[Frontmatter Standards](docs/standards/FRONTMATTER_STANDARDS.md)** - Metadata requirements

### For AI Agents (VS Code Copilot)
AI agents assisting with contributions should reference:
- **[Contributing Instructions](.github/instructions/contributing.instructions.md)** - AI agent guidance for contributions
- **[README Instructions](.github/instructions/README.instructions.md)** - Documentation standards
- **[Quest Instructions](.github/instructions/quest.instructions.md)** - Quest creation patterns
- **[Post Instructions](.github/instructions/posts.instructions.md)** - Blog post standards
- **[Feature Instructions](.github/instructions/features.instructions.md)** - Feature development
- **[Space Instructions](.github/instructions/space.instructions.md)** - Project organization

The `.github/instructions/` directory contains AI-optimized instructions that help VS Code Copilot and other AI agents assist contributors more effectively while maintaining project standards and quality.

### Additional Documentation
- **[Jekyll Implementation](docs/architecture/JEKYLL_IMPLEMENTATION.md)** - Jekyll details
- **[GitHub Actions](docs/workflows/GITHUB_ACTIONS.md)** - CI/CD workflows
- **[Scripts Guide](docs/scripts/SCRIPTS_GUIDE.md)** - Automation tools
- **[Testing Frameworks](docs/testing/TESTING_FRAMEWORKS.md)** - Quality assurance

## Types of Contributions

### Content Creation
- Write blog posts and tutorials
- Create gamified quests
- Add educational documentation
- Contribute Jupyter notebooks

### Code Contributions
- Improve automation scripts
- Enhance testing frameworks
- Optimize workflows
- Fix bugs and issues

### Documentation
- Improve developer documentation
- Add learning resources
- Update guides and tutorials
- Fix typos and errors

### Community Support
- Help answer questions
- Review pull requests
- Share your experiences
- Mentor new contributors

## Prerequisites

Before contributing, you should have:

- [ ] Git and GitHub account
- [ ] Development environment set up (see [setup guide](docs/setup/DEVELOPMENT_ENVIRONMENT.md))
- [ ] Familiarity with Jekyll (see [Jekyll docs](pages/_docs/jekyll/))
- [ ] Understanding of repository structure (see [architecture docs](docs/architecture/REPOSITORY_STRUCTURE.md))
- [ ] Knowledge of contribution standards (see [contributing guide](docs/CONTRIBUTING_DEVELOPER.md))

## Contribution Workflow

### Standard Workflow (All Contributions)

```bash
# 1. Fork and clone
git clone https://github.com/YOUR-USERNAME/it-journey.git
cd it-journey

# 2. Create branch (use descriptive name)
git checkout -b feature/your-feature-name

# 3. Make changes
# Edit files

# 4. Test locally (for code/Jekyll changes)
docker-compose up  # Or: bundle exec jekyll serve --config _config_dev.yml
# Visit http://localhost:4000 to verify changes

# 5. Commit with conventional format
git add .
git commit -m "feat(scope): description"
# Examples: 
#   "docs: improve contributing guide"
#   "feat(quest): add docker basics quest"
#   "fix(ci): resolve workflow timeout issue"

# 6. Push and create PR
git push origin feature/your-feature-name
# Go to GitHub and click "Create Pull Request"
```

**Commit Message Format**: `<type>(<scope>): <description>`
- **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- **Scope**: Component affected (quest, post, ci, script, etc.)
- **Description**: Brief summary in present tense

See the [Developer Contributing Guide](docs/CONTRIBUTING_DEVELOPER.md) for detailed workflow instructions.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and beginners
- Provide constructive feedback
- Focus on the work, not the person
- Respect different perspectives
- Be patient and empathetic

## Getting Help

### Questions
- Check [documentation](docs/README.md) first
- Search existing issues
- Create discussion in GitHub Discussions
- Ask in pull request comments

### Issues
- Bug reports: Use `bug` label
- Feature requests: Use `enhancement` label
- Questions: Use `question` label
- Documentation: Use `documentation` label

### Support Channels
- **Technical Issues**: [GitHub Issues](https://github.com/bamr87/it-journey/issues)
- **Discussions**: [GitHub Discussions](https://github.com/bamr87/it-journey/discussions)
- **Documentation**: See `docs/` directory in repository
- **Email**: For sensitive issues only

## Recognition

Contributors are recognized through:
- Repository contributors page
- Release notes acknowledgments
- About page (for significant contributions)
- Special recognition in related content

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

For complete contribution guidelines, please see the [Developer Contributing Guide](docs/CONTRIBUTING_DEVELOPER.md).

**Last Updated**: 2025-11-07 | **Next Review**: 2025-12-07
