# Developer Contribution Guide

This guide provides comprehensive instructions for developers and AI agents contributing to the IT-Journey repository.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [AI Agent Guidelines](#ai-agent-guidelines)

## Getting Started

### Prerequisites

Before contributing, ensure you have:

1. **Development Environment Set Up**
   - Follow [Development Environment Setup](setup/DEVELOPMENT_ENVIRONMENT.md)
   - Verify local build works: `bundle exec jekyll serve --config _config_dev.yml`

2. **Familiarity with Project Structure**
   - Read [Repository Structure](architecture/REPOSITORY_STRUCTURE.md)
   - Review [Jekyll Implementation](architecture/JEKYLL_IMPLEMENTATION.md)

3. **Understanding of Standards**
   - Review [Frontmatter Standards](standards/FRONTMATTER_STANDARDS.md)
   - Read [Content Guidelines](standards/CONTENT_GUIDELINES.md)

### Fork and Clone

```bash
# Fork the repository on GitHub (click Fork button)

# Clone your fork
git clone https://github.com/YOUR-USERNAME/it-journey.git
cd it-journey

# Add upstream remote
git remote add upstream https://github.com/bamr87/it-journey.git

# Verify remotes
git remote -v
```

## Development Workflow

### 1. Sync with Upstream

Before starting work, sync with the main repository:

```bash
# Fetch latest changes
git fetch upstream

# Checkout main branch
git checkout main

# Merge upstream changes
git merge upstream/main

# Push to your fork
git push origin main
```

### 2. Create Feature Branch

Use descriptive branch names:

```bash
# Branch naming convention
# Type:
#   - feature/ (new functionality)
#   - fix/ (bug fix)
#   - docs/ (documentation)
#   - refactor/ (code refactoring)
#   - test/ (testing improvements)

# Examples
git checkout -b feature/add-quest-validator
git checkout -b fix/broken-link-in-docs
git checkout -b docs/update-setup-guide
git checkout -b refactor/consolidate-scripts
```

### 3. Make Changes

**Code Changes:**
```bash
# Edit files
# Follow coding standards (see below)

# Test locally
bundle exec jekyll serve --config _config_dev.yml

# Verify in browser
open http://localhost:4002
```

**Content Changes:**
```bash
# Create or edit markdown files in pages/

# Validate frontmatter
python3 scripts/validate-frontmatter.py pages/_posts/your-post.md

# Test build
bundle exec jekyll build --config _config_dev.yml
```

**Script Changes:**
```bash
# Make executable
chmod +x scripts/category/new-script.sh

# Test with dry run
./scripts/category/new-script.sh --dry-run

# Check syntax
shellcheck scripts/category/new-script.sh
```

### 4. Commit Changes

Follow conventional commit message format:

```bash
# Commit message format
<type>(<scope>): <subject>

<body>

<footer>

# Types: feat, fix, docs, style, refactor, test, chore
# Scope: area of change (quest, docs, scripts, workflow, etc.)

# Examples
git commit -m "feat(quest): add automated link checking quest"
git commit -m "fix(docs): correct broken links in setup guide"
git commit -m "docs(architecture): update repository structure"
git commit -m "refactor(scripts): consolidate build scripts"
git commit -m "test(links): improve link checker coverage"
```

**Good Commit Messages:**
```
✅ feat(quest): add link guardian quest with AI analysis
✅ fix(workflow): resolve link checker timeout issues
✅ docs(setup): add Docker setup instructions
✅ refactor(scripts): unify version management scripts
```

**Avoid:**
```
❌ Update files
❌ Fix bug
❌ Changes
❌ WIP
```

### 5. Push Changes

```bash
# Push to your fork
git push origin feature/your-feature-name

# If branch already pushed, force push if needed (after rebase)
git push origin feature/your-feature-name --force-with-lease
```

## Code Standards

### Frontmatter Standards

All content must include proper frontmatter:

```yaml
---
title: "Descriptive Title"
description: "Brief description for SEO"
author: "Your Name"
date: 2025-10-13T00:00:00.000Z
lastmod: 2025-10-13T00:00:00.000Z
categories:
  - category-one
  - category-two
tags:
  - tag-one
  - tag-two
draft: false
---
```

**See:** [Frontmatter Standards](standards/FRONTMATTER_STANDARDS.md)

### Markdown Standards

Follow markdown best practices:

```markdown
# Use ATX-style headings with space after #

Use blank lines to separate paragraphs.

- Use `-` for unordered lists
- Keep list items consistent
- Indent nested items properly

1. Use `1.` for all ordered list items
1. Markdown will auto-number
1. Makes reordering easier

Use **bold** for emphasis and *italic* for subtle emphasis.

\`Inline code\` for commands, file names, and code snippets.

\`\`\`language
# Code blocks with language specified
command --option value
\`\`\`
```

**See:** [Content Guidelines](standards/CONTENT_GUIDELINES.md)

### Script Standards

Scripts must follow these conventions:

```bash
#!/usr/bin/env bash
#
# @file scripts/category/script-name.sh
# @description Brief description
# @author IT-Journey Team
# @created 2025-10-13
# @version 1.0.0

# Exit on error
set -e
set -u
set -o pipefail

# Error handling
error_exit() {
    echo "Error: $1" >&2
    exit 1
}

# Main function
main() {
    # Script logic here
    echo "Script running..."
}

# Run main
main "$@"
```

**See:** [Scripts Guide](scripts/SCRIPTS_GUIDE.md)

### Python Standards

Python scripts follow PEP 8:

```python
"""
Module description.

@file scripts/category/script-name.py
@author IT-Journey Team
@created 2025-10-13
@version 1.0.0
"""

import sys
from typing import List, Dict

def function_name(param: str) -> bool:
    """
    Function description.
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
    """
    # Implementation
    return True

if __name__ == "__main__":
    # Main execution
    pass
```

## Testing Requirements

### Local Testing Checklist

Before submitting PR, verify:

- [ ] Jekyll builds successfully
- [ ] No broken links (run link checker)
- [ ] Frontmatter is valid
- [ ] Images load correctly
- [ ] Code examples work
- [ ] Scripts are executable and functional
- [ ] No linting errors

### Run Tests Locally

```bash
# 1. Test Jekyll build
bundle exec jekyll build --config _config_dev.yml

# 2. Check for issues
bundle exec jekyll doctor

# 3. Validate frontmatter
# (Run on changed files only)
python3 scripts/validate-frontmatter.py pages/_posts/your-post.md

# 4. Check links
python3 scripts/validation/link-checker.py --scope internal

# 5. Test scripts
# If you modified scripts
./scripts/your-script.sh --dry-run

# 6. Check shell scripts
shellcheck scripts/**/*.sh
```

### Automated Testing

CI/CD runs automatically on PR:
- Build validation
- Frontmatter validation
- Link checking (internal only for PRs)
- CodeQL security scanning

## Pull Request Process

### 1. Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature

# Go to GitHub and click "Create Pull Request"
```

### 2. PR Title and Description

**Title Format:**
```
<type>(<scope>): <description>

Examples:
feat(quest): add link guardian automation quest
fix(docs): correct setup instructions for macOS
docs(contributing): update PR guidelines
```

**Description Template:**
```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Checklist
- [ ] Local build succeeds
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Follows code standards
- [ ] Commits follow convention

## Related Issues
Closes #123
Related to #456

## Screenshots (if applicable)
[Add screenshots here]

## Additional Notes
Any additional context or notes.
```

### 3. Code Review Process

**For Contributors:**
- Respond to review comments promptly
- Make requested changes in new commits
- Update PR description if scope changes
- Resolve conflicts with main branch

**For Reviewers:**
- Review within 48 hours when possible
- Be constructive and specific
- Suggest improvements, not just problems
- Approve when standards are met

### 4. Merging

**Requirements for Merge:**
- [ ] At least one approval from maintainer
- [ ] All CI checks passing
- [ ] No merge conflicts
- [ ] Up to date with main branch
- [ ] Documentation updated (if needed)

**Merge Process:**
1. Maintainer reviews and approves
2. Squash and merge (default) or merge commit
3. Delete feature branch
4. Close related issues

## Branch Protection Rules

The `main` branch is protected with these rules:

- Require pull request reviews (1 approval minimum)
- Require status checks to pass
  - Build validation
  - Frontmatter validation
  - CodeQL analysis
- Require branches to be up to date before merging
- Require signed commits (recommended)
- Include administrators

## AI Agent Guidelines

### Context for AI Assistants

When working on this repository, AI agents should:

1. **Read Documentation First**
   - Start with [Repository Structure](architecture/REPOSITORY_STRUCTURE.md)
   - Review relevant standards before making changes

2. **Follow Established Patterns**
   - Look at existing similar content/code
   - Match style and structure
   - Use same tools and workflows

3. **Validate Changes**
   - Test builds locally
   - Check frontmatter
   - Verify links work
   - Run applicable tests

4. **Provide Context**
   - Explain reasoning in commit messages
   - Document decisions in PRs
   - Link to relevant documentation

### AI-Specific Workflows

**For Content Creation:**
```
1. Review existing content in same collection
2. Follow frontmatter template exactly
3. Match writing style and tone
4. Include all required fields
5. Test markdown rendering
```

**For Code Changes:**
```
1. Review similar existing code
2. Follow established patterns
3. Add comprehensive error handling
4. Include usage examples
5. Update documentation
```

**For Documentation Updates:**
```
1. Review entire document for consistency
2. Update cross-references
3. Maintain formatting standards
4. Test all links
5. Update "Last Updated" date
```

## Communication

### Getting Help

**Questions:**
- Create discussion in GitHub Discussions
- Ask in pull request comments
- Create issue with `question` label

**Bug Reports:**
- Create issue with `bug` label
- Include reproduction steps
- Provide system information
- Include error messages/logs

**Feature Requests:**
- Create issue with `enhancement` label
- Describe use case and benefits
- Suggest implementation approach

### Response Times

We strive for:
- **Issues:** Response within 48 hours
- **Pull Requests:** Review within 48 hours
- **Discussions:** Response within 72 hours

## Best Practices

### Do's

✅ Write clear, descriptive commit messages  
✅ Test thoroughly before submitting PR  
✅ Update documentation with code changes  
✅ Respond promptly to review feedback  
✅ Keep PRs focused and reasonably sized  
✅ Follow established conventions  
✅ Ask for clarification when unsure

### Don'ts

❌ Commit directly to main branch  
❌ Submit PRs without testing  
❌ Ignore CI failures  
❌ Make unrelated changes in same PR  
❌ Skip documentation updates  
❌ Use force push on shared branches  
❌ Include sensitive data or secrets

## Recognition

Contributors are recognized in:
- Repository contributors page
- Release notes
- About page (for significant contributions)
- Special acknowledgment in related content

## License

By contributing, you agree that your contributions will be licensed under the MIT License, the same license as the project.

## Additional Resources

### Documentation
- [Repository Structure](architecture/REPOSITORY_STRUCTURE.md)
- [Jekyll Implementation](architecture/JEKYLL_IMPLEMENTATION.md)
- [Frontmatter Standards](standards/FRONTMATTER_STANDARDS.md)
- [Content Guidelines](standards/CONTENT_GUIDELINES.md)
- [Development Environment](setup/DEVELOPMENT_ENVIRONMENT.md)

### External Resources
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

## Questions or Problems?

- **Documentation Issues:** Open issue or PR with corrections
- **Process Questions:** Create discussion in GitHub Discussions
- **Technical Problems:** Create issue with `help wanted` label
- **Security Issues:** Email security@it-journey.dev (do not create public issue)

---

Thank you for contributing to IT-Journey! Your efforts help build a better learning platform for everyone.

**Last Updated**: 2025-10-13  
**Version**: 1.0.0

