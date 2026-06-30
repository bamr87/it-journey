---
title: Contributing to IT-Journey
author: IT-Journey Team
excerpt: Join our community of learners, creators, and adventurers building the future of IT education
description: How to contribute to IT-Journey, the gamified open-source platform for IT education — content, code, AI-agent workflows, and developer setup.
snippet: Transform IT education through open-source collaboration
categories:
- about
tags:
- contributing
- community
- open-source
- collaboration
meta:
  keywords: contributing, open source, IT education, community, collaboration
draft: false
lastmod: '2026-06-30T00:00:00.000Z'
permalink: /about/contributing/
date: '2024-05-11T16:54:12.000Z'
redirect_from:
- /docs/contributing/contributing-developer/contributing-developer/
---
# Contributing to IT-Journey

Welcome, adventurer! 🎯 IT-Journey thrives on community collaboration. Whether you're fixing a typo, creating epic quests, or building powerful tools, your contribution matters.

## 🚀 Quick Start for New Contributors

**Never contributed to open source before?** Perfect! Start here:

1. **Read the Full Guide**: Check our comprehensive [Contributing Guide](https://github.com/bamr87/it-journey/blob/main/CONTRIBUTING.md) on GitHub
2. **Pick Your Adventure**: Choose from content creation, code contributions, documentation, or community support
3. **Setup Your Environment**: Follow our [Development Setup Guide](https://github.com/bamr87/it-journey/blob/main/docs/setup/DEVELOPMENT_ENVIRONMENT.md)
4. **Make Your First Contribution**: Start with something small like fixing a typo or improving documentation

## 🎭 Types of Contributions

### 📝 Content Creation
- **Write Quests**: Create gamified learning experiences
- **Develop Tutorials**: Build step-by-step guides and quickstart paths
- **Improve Docs & Notes**: Expand the reference docs and curated cheatsheets
- **Refine Quest Paths**: Improve prerequisites, level maps, and walkthroughs

### 💻 Code Contributions  
- **Build Features**: Implement new capabilities
- **Fix Bugs**: Squash those pesky issues
- **Improve Scripts**: Enhance automation
- **Optimize Workflows**: Streamline processes

### 📚 Documentation
- **Improve Guides**: Make docs clearer
- **Add Examples**: Show, don't just tell
- **Update READMEs**: Keep information current
- **Translate Content**: Make IT-Journey multilingual

### 🤝 Community Support
- **Answer Questions**: Help fellow adventurers
- **Review PRs**: Provide constructive feedback
- **Mentor Others**: Share your expertise
- **Spread the Word**: Tell others about IT-Journey

## ⚔️ The Developer's Contribution Path

Ready to commit code? This is the battle-tested workflow every developer (and AI agent) follows to land a change in the repo.

### 🍴 Fork, Clone, and Sync

```bash
# Clone your fork, then point at the upstream repo
git clone https://github.com/YOUR-USERNAME/it-journey.git
cd it-journey
git remote add upstream https://github.com/bamr87/it-journey.git

# Sync before every new branch
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 🌿 Branch with Intent

Never commit to `main`. Branch with a type prefix that announces your quest:

```bash
git checkout -b feature/add-quest-validator   # new functionality
git checkout -b fix/broken-link-in-docs       # bug fix
git checkout -b docs/update-setup-guide        # documentation
git checkout -b refactor/consolidate-scripts   # code refactoring
```

### 📜 Commit Like a Chronicler

We follow [Conventional Commits](https://www.conventionalcommits.org/) — `<type>(<scope>): <subject>`. Types are `feat, fix, docs, style, refactor, test, chore`.

```bash
✅ feat(quest): add link guardian quest with AI analysis
✅ fix(docs): correct broken links in setup guide
✅ refactor(scripts): unify version management scripts

❌ Update files
❌ Fix bug
❌ WIP
```

### 🔍 Verify Before You Push

Run the local checks so CI doesn't surprise you:

```bash
make build-ci          # CI-parity Jekyll build
make content-audit     # frontmatter + link validation
make quest-audit       # only if you touched quests
```

CI re-runs build validation, frontmatter validation, internal link checking, and CodeQL on every pull request — green checks are required before merge.

### 🎯 Open a Focused Pull Request

Use a Conventional-Commits-style title (`feat(quest): add link guardian automation`) and a description that covers **what changed**, **why**, the **type of change**, a **testing checklist**, and any **related issues** (`Closes #123`). Keep each PR focused — one concern per PR makes review fast. A maintainer reviews (target: within 48 hours), then squash-and-merges once checks are green.

## 🤖 Contributing with AI Agents

IT-Journey embraces **AIPD** (AI-Powered Development) — AI is a force multiplier, not a replacement for human judgment. There are two supported paths.

### 🛰️ Delegate an Issue to GitHub Copilot

The [GitHub Copilot coding agent](https://docs.github.com/en/copilot/using-github-copilot/using-claude-sonnet-in-github-copilot) works directly inside the repo's CI environment:

1. Open an issue, then in the **Assignees** panel assign **Copilot**.
2. Copilot opens a PR on a new branch and posts progress as comments.
3. Review the diff as you would any contributor's — agents can miss project conventions.
4. Confirm CI is green, then **squash and merge**.

A `copilot-setup-steps.yml` workflow pre-installs Ruby, Bundler, and dependencies automatically, so the agent's environment matches local development.

### 🧙 Drive an AI Assistant Locally

Use Claude, Copilot, Cursor, Continue.dev, or similar in your editor to draft changes, then verify and open the PR yourself. A few prompt strategies that work well here:

| Task | Prompt strategy |
|------|----------------|
| **New doc page** | "Create a Jekyll Markdown file in `pages/_docs/<topic>/` with all required frontmatter fields." |
| **Fix frontmatter** | "Audit this file's YAML frontmatter against the Frontmatter Standards and add missing fields." |
| **Improve content** | "Review this for clarity, accuracy, and completeness; suggest additions for a contributor." |
| **Update a guide** | "Update this to reflect [change], keep the existing voice, and bump `lastmod` to today." |

**Agent do's and don'ts:**

✅ Always bump `lastmod` when editing a file  
✅ Run `make build-ci` to confirm the site compiles  
✅ Write clear PR descriptions explaining what and why  
✅ Follow Conventional Commits  

❌ Never commit secrets, API keys, or credentials  
❌ Don't touch CI workflow files unless asked  
❌ Don't reorder or drop frontmatter fields without understanding the impact  
❌ Don't hard-code absolute local paths or bypass branch protection  

## 🌟 Our Contributors

We're proud to recognize everyone who has contributed to IT-Journey:

### Core Contributors

- [Amr (bamr87)](/contributors/bamr87/) - Founder & Maintainer

### How to Add Your Profile

Every contributor gets a **Character Profile** — an RPG-style character sheet with auto-calculated stats, badges, and a class identity powered by your git history.

**Quick Setup:**

1. Copy the template folder:
   ```bash
   cp -r pages/_about/contribute/contributors/_template \
         pages/_about/contribute/contributors/YOUR_USERNAME
   ```
2. Copy the data template:
   ```bash
   cp _data/contributors/_template.yml _data/contributors/YOUR_USERNAME.yml
   ```
3. Edit both files — replace `YOUR_GITHUB_USERNAME` and `YOUR_DISPLAY_NAME` with your info
4. Choose your **class**: Wizard, Warrior, Ranger, Rogue, Healer, Bard, or Paladin
5. Commit + push — the GitHub Action will auto-generate your stats on the next push to `main`

See the [Forge Your Character quest](/quests/0001/forge-your-character/) for a full walkthrough.

**Alternative — Git Subtree Method:**

```bash
cd ~/github/it-journey

# Add your GitHub profile repository as a remote
git remote add {{ page.username | default: 'YOUR_USERNAME' }} https://github.com/{{ page.username | default: 'YOUR_USERNAME' }}/{{ page.username | default: 'YOUR_USERNAME' }}.git

# Add your profile as a subtree
git subtree add --prefix=pages/_about/contributors/{{ page.username | default: 'YOUR_USERNAME' }} {{ page.username | default: 'YOUR_USERNAME' }} main
```

## 📖 Essential Resources

### For All Contributors
- **[Main Contributing Guide](https://github.com/bamr87/it-journey/blob/main/CONTRIBUTING.md)** - Complete contribution workflow
- **[Code of Conduct](https://github.com/bamr87/it-journey/blob/main/CODE_OF_CONDUCT.md)** - Community standards
- **[Open Source Guide](https://opensource.guide/)** - Learn about open source

### Technical Documentation
- **[Repository Structure](https://github.com/bamr87/it-journey/blob/main/docs/architecture/REPOSITORY_STRUCTURE.md)** - How things are organized
- **[Content Guidelines](https://github.com/bamr87/it-journey/blob/main/docs/standards/CONTENT_GUIDELINES.md)** - Writing standards
- **[Frontmatter Standards](https://github.com/bamr87/it-journey/blob/main/docs/standards/FRONTMATTER_STANDARDS.md)** - Metadata requirements

### For Content Creators
- **[Quest Creation Guide](https://github.com/bamr87/it-journey/blob/main/.github/instructions/quest.instructions.md)** - Build epic quests
- **[Notes Writing Guide](https://github.com/bamr87/it-journey/blob/main/.github/instructions/notes.instructions.md)** - Author cheatsheets and reference notes
- **[Quickstart Guide](https://github.com/bamr87/it-journey/blob/main/.github/instructions/quickstart.instructions.md)** - Write fast-track onboarding guides
- **[README Guidelines](https://github.com/bamr87/it-journey/blob/main/.github/instructions/README.instructions.md)** - Documentation standards

## 🎯 IT-Journey Principles

All contributions should follow our core principles:

- **DFF** (Design for Failure): Build resilient, error-tolerant content
- **DRY** (Don't Repeat Yourself): Reuse and reference, don't duplicate
- **KIS** (Keep It Simple): Clarity over complexity
- **REnO** (Release Early and Often): Iterate and improve continuously
- **MVP** (Minimum Viable Product): Start small, expand gradually
- **COLAB** (Collaboration): Welcome community input and feedback
- **AIPD** (AI-Powered Development): Leverage AI to enhance, not replace, human creativity

## 💡 Contribution Ideas

Not sure where to start? Try these:

### Easy First Contributions (5-15 minutes)
- Fix a typo in documentation
- Improve a README
- Add clarifying comments to code
- Update a broken link

### Intermediate Contributions (1-2 hours)
- Create a beginner-level quest
- Add a cheatsheet or reference note for a tool you use
- Improve existing documentation
- Add test coverage

### Advanced Contributions (2+ hours)
- Build a new feature
- Create a quest series
- Implement automation scripts
- Refactor major components

## 🤔 Getting Help

**Questions?** We're here to help!

- **Technical Issues**: [GitHub Issues](https://github.com/bamr87/it-journey/issues)
- **Discussions**: [GitHub Discussions](https://github.com/bamr87/it-journey/discussions)
- **General Questions**: Check our [documentation](https://github.com/bamr87/it-journey/tree/main/docs) first

## 🏆 Recognition

Your contributions are valued and recognized through:

- **Character Profile** with auto-calculated stats from your git history
- **Achievement badges** unlocked by contribution milestones
- **XP and leveling** — earn XP for commits, PRs, and completed quests
- Contributor profile page on our website
- Mentions in release notes
- Recognition in the About page
- Community spotlight features

## 📜 License

By contributing to IT-Journey, you agree that your contributions will be licensed under the [MIT License](https://github.com/bamr87/it-journey/blob/main/LICENSE).

---

**Ready to start your contribution adventure?** Head over to our [GitHub repository](https://github.com/bamr87/it-journey) and make your first contribution today!

**Last Updated**: 2025-11-07 | **Maintained by**: IT-Journey Team