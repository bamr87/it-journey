---
title: Learning Resources Library
author: Amr Abdel Eissa
permalink: /docs/
description: Reference documentation and learning resources for tools and technologies used in IT-Journey
excerpt: Reference documentation and learning resources covering terminal, Bash, Jekyll, Liquid, and development tools used in IT-Journey.
categories:
  - docs
  - home
tags:
  - docs
  - reference
  - learning-resources
  - jekyll
  - terminal
toc_sticky: true
date: 2021-12-03T09:05:06.000Z
lastmod: 2026-04-07T02:46:45.139Z
draft: false
keywords:
  primary:
    - learning resources
    - documentation
  secondary:
    - terminal reference
    - jekyll docs
    - bash guide
---

# Learning Resources Library

Reference documentation and educational resources for the tools and technologies powering IT-Journey. Browse by topic below, or use the sidebar to navigate directly to a specific technology.

## About This Library

**Purpose:** Educational content and reference documentation for external tools, frameworks, and technologies used in IT-Journey.

**Audience:** Learners, students, and anyone exploring the technologies used in building and maintaining the IT-Journey platform.

## Developer Documentation

> **Note for Contributors:** If you're looking for technical documentation about the IT-Journey repository structure, contribution workflows, or development setup, see the **Developer Documentation** in the repository root (`/docs/` directory on GitHub).

### Quick Links for Developers
- [Repository Structure](../../docs/architecture/REPOSITORY_STRUCTURE.md)
- [Jekyll Implementation](../../docs/architecture/JEKYLL_IMPLEMENTATION.md)
- [Development Environment Setup](../../docs/setup/DEVELOPMENT_ENVIRONMENT.md)
- [Contributing Guide](../../docs/CONTRIBUTING_DEVELOPER.md)
- [Frontmatter Standards](../../docs/standards/FRONTMATTER_STANDARDS.md)

## Available Documentation

### Terminal

Command-line reference and productivity guides for working effectively in the terminal.

**Topics:**
- [Terminal Shortcuts Cheat Sheet](/docs/terminal-shortcuts-cheat-sheet/) - Keyboard shortcuts for macOS, Linux, and Windows
- [Complete BASH Reference](/docs/bash-complete-reference/) - Exhaustive GNU Bash reference: built-ins, scripting, text processing, and advanced techniques

### Jekyll

The IT-Journey platform is built with Jekyll, a static site generator. The Jekyll documentation covers how IT-Journey specifically implements and uses Jekyll features.

**Topics:**
- [Jekyll Overview](jekyll/) - Jekyll as used in IT-Journey
- [Configuration Options](jekyll/jekyll-config.md) - Jekyll configuration reference
- [Frontmatter CMS](jekyll/jekyll-frontmatter-cms.md) - Using frontmatter as a CMS
- [Frontmatter Preview Configuration](jekyll/jekyll-frontmatter-preview-configuration.md) - Configure VS Code preview with permalinks
- [Liquid Templating](jekyll/jekyll-liquid.md) - Liquid template language
- [Mermaid Diagrams](jekyll/jekyll-diagram-with-mermaid.md) - Creating diagrams
- [Math Symbols](jekyll/jekyll-math-symbols-with-mathjax.md) - Mathematical notation

### Wargames (External)

Security challenges aggregated from the [OverTheWire](https://overthewire.org/wargames/) community project. Learn and practice security concepts through gamified challenges.

**Topics:**
- [Wargames Overview](/docs/wargames/) - Introduction, game list, and how to get started

> This section is populated by the [docs aggregation pipeline](/it-journey/scripts/docs-aggregator/). Run `bash scripts/docs-aggregator/aggregate_docs.sh` to update.

### Future Documentation Areas

This library will expand to include reference documentation for:

**Planned Topics:**
- **Ruby** - Ruby programming language fundamentals
- **Liquid** - Advanced Liquid templating techniques
- **Bootstrap** - Bootstrap framework usage
- **GitHub Pages** - GitHub Pages deployment and configuration
- **Markdown** - Advanced Markdown techniques
- **Git** - Version control workflows

## Documentation Philosophy

### What Belongs Here

This `/docs/` learning library contains:
- External tool and technology references
- Educational tutorials and guides
- Framework and library documentation
- Technology overviews and comparisons
- Learning paths and resources

### What Belongs in Developer Docs

The repository `/docs/` directory contains:
- IT-Journey repository structure and architecture
- Development environment setup
- Contribution workflows and standards
- Testing frameworks and automation
- Scripts and tools documentation
- GitHub Actions and CI/CD workflows

## How to Use This Library

### For Learners

1. **Explore by Topic** - Browse available technology documentation
2. **Follow Learning Paths** - Use resources to build understanding
3. **Practice with IT-Journey** - Apply concepts in the IT-Journey codebase
4. **Contribute Back** - Share your learning by improving documentation

### For Contributors

1. **Reference While Developing** - Use as quick reference for tools
2. **Learn New Technologies** - Understand technologies before contributing
3. **Add New Resources** - Contribute documentation for new tools
4. **Keep It Updated** - Help maintain accuracy and relevance

## Contributing to This Library

### Adding New Documentation

To add documentation for a new tool or technology:

1. **Create Directory** - Add subdirectory under `pages/_docs/`
   ```bash
   mkdir pages/_docs/new-tool/
   ```

2. **Create Index** - Add `index.md` with overview
   ```bash
   touch pages/_docs/new-tool/index.md
   ```

3. **Add Content** - Create topic-specific markdown files
   ```bash
   touch pages/_docs/new-tool/getting-started.md
   ```

4. **Follow Standards** - Use [Frontmatter Standards](../../docs/standards/FRONTMATTER_STANDARDS.md)

5. **Update Navigation** - Add to `_data/navigation/docs.yml`

### Content Guidelines

- **Focus on IT-Journey Context** - Show how the tool is used in IT-Journey
- **Include Examples** - Provide practical, working examples
- **Link to Official Docs** - Reference authoritative sources
- **Keep It Current** - Update when technologies change
- **Be Educational** - Write for learners, not just reference

See [Content Guidelines](../../docs/standards/CONTENT_GUIDELINES.md) for detailed writing standards.

## Documentation Sources

### Git Submodules & Aggregation

The documentation library supports two approaches for integrating external content:

**Docs Aggregation Pipeline** (Active):
```bash
# Aggregate external documentation into _docs
bash scripts/docs-aggregator/aggregate_docs.sh
```

The aggregation pipeline clones external repos, extracts documentation, transforms it to Jekyll-compatible format with it-journey frontmatter, and places it under `pages/_docs/`. See [docs-aggregator README](../../scripts/docs-aggregator/README.md) for details and how to add new sources.

**Git Submodules** (Future alternative):

```bash
# Example: Adding Jekyll official docs
git submodule add https://github.com/jekyll/jekyll.git jekyll-docs

# Configure sparse checkout for specific directories
cd jekyll-docs/docs/_docs
git sparse-checkout init --cone
git sparse-checkout set docs/_docs
```

This approach allows:
- Always up-to-date official documentation
- Clean separation of sources
- Easy updates via Git

### Manual Documentation

For tools without suitable official docs, we create our own:
- Custom tutorials and guides
- IT-Journey-specific implementations
- Integration examples and patterns

## Technology Stack

IT-Journey is built with:

### Core Technologies
- **Jekyll 3.9.5** - Static site generator
- **Ruby 3.2.3** - Programming language
- **Liquid** - Template language
- **Kramdown** - Markdown processor
- **Bootstrap 5.2.0** - CSS framework

### Development Tools
- **Git** - Version control
- **Docker** - Containerization
- **GitHub Actions** - CI/CD automation
- **Python 3.11** - Scripting and automation

### Services
- **GitHub Pages** - Hosting
- **OpenAI GPT-4** - AI-powered analysis
- **Giscus** - Comments via GitHub Discussions

For detailed information, see [Jekyll Implementation](../../docs/architecture/JEKYLL_IMPLEMENTATION.md).

## Getting Help

### Questions About This Library
- Create issue with `documentation` label
- Suggest improvements via pull requests
- Start discussion in GitHub Discussions

### Questions About Contributing
- See [Contributing Guide](../../docs/CONTRIBUTING_DEVELOPER.md)
- Check [Development Environment Setup](../../docs/setup/DEVELOPMENT_ENVIRONMENT.md)
- Review [Repository Structure](../../docs/architecture/REPOSITORY_STRUCTURE.md)

## Additional Resources

### Other IT-Journey Collections

| Collection | What It Is |
|------------|------------|
| [📘 Quick Start Guide](/quickstart/) | Step-by-step setup — machine config, Jekyll, GitHub, VS Code, deployment, CI/CD |
| [🏰 Quest Map](/quests/home/) | 144 gamified quests across 16 binary levels — from terminal basics to system architecture |
| [📝 Notes](/notes/) | Working notes, code snippets, and quick references from development |
| [📰 Blog Posts](/posts/) | Tutorials, AI development chronicles, and technical write-ups across 10 categories |

### External Resources
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Liquid Documentation](https://shopify.github.io/liquid/)
- [Markdown Guide](https://www.markdownguide.org/)

---

**Last Updated:** 2025-10-13  
**Version:** 2.0.0

*The Learning Resources Library is part of the IT-Journey project. For technical developer documentation, see the [`/docs/` directory](../../docs/).*
