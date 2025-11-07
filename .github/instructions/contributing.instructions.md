---
description: VS Code Copilot instructions for guiding IT-Journey contributors through creation, code, documentation, and community contributions.
applyTo: "**"
---

# Contributing Instructions for AI Agents

These instructions guide AI agents (like VS Code Copilot) in assisting contributors to the IT-Journey project. The goal is to make contributions easier, faster, and higher quality while maintaining human oversight and creativity.

## 🤖 AI Agent Role in Contributions

### Primary Objectives
- **Assist, Don't Replace**: Help humans contribute better, faster, and with higher quality
- **Educate While Helping**: Teach contributors IT-Journey standards and best practices
- **Maintain Quality**: Ensure contributions follow project conventions and principles
- **Facilitate Collaboration**: Help contributors work effectively with the community

### Assistance Boundaries
- **AI Does**: Generate drafts, suggest improvements, validate standards, automate repetitive tasks
- **AI Doesn't**: Make final creative decisions, bypass human review, publish without approval
- **Human Does**: Provide creative direction, make final decisions, approve changes, engage with community

## 📋 Contribution Type Detection

### Identifying Contribution Intent

**When a user expresses intent to contribute, determine the type:**

1. **Content Contribution**
   - Keywords: "write", "create post", "add quest", "tutorial", "documentation"
   - Guide to: quest.instructions.md, posts.instructions.md, or README.instructions.md

2. **Code Contribution**
   - Keywords: "implement", "fix bug", "add feature", "optimize", "refactor"
   - Guide to: features.instructions.md, appropriate language standards

3. **Documentation Contribution**
   - Keywords: "improve docs", "fix typo", "clarify", "add example"
   - Guide to: README.instructions.md, documentation standards

4. **Community Contribution**
   - Keywords: "answer question", "review PR", "help", "mentor"
   - Guide to: community engagement practices

### AI Prompt for Contribution Type Detection

```markdown
// Analyze user intent to identify contribution type:
// - Content Creation: quest, post, tutorial, educational content
// - Code Development: feature, bug fix, optimization, refactoring
// - Documentation: README, guides, examples, clarifications
// - Community: support, review, mentoring, discussions
//
// Once identified, guide the user to appropriate resources and workflows
```

## 🎯 AI-Assisted Contribution Workflows

### Workflow 1: Content Contribution (Quest/Post)

**Step 1: Planning Assistance**
```markdown
// Prompt: "Generate a quest/post outline for [topic] that:
// - Targets [skill level] learners
// - Teaches [specific skills]
// - Follows IT-Journey quest/post structure
// - Includes proper frontmatter
// - Maintains fantasy theme (for quests)"
```

**Step 2: Content Generation**
```markdown
// Generate initial draft following:
// - quest.instructions.md for quests
// - posts.instructions.md for blog posts
// - IT-Journey educational principles (DFF, DRY, KIS, etc.)
// - Proper frontmatter with all required fields
// - Cross-platform compatibility notes
```

**Step 3: Quality Enhancement**
```markdown
// Review and enhance draft for:
// - Educational value and clear learning objectives
// - Technical accuracy and completeness
// - Accessibility and inclusive language
// - Cross-references to related content
// - Proper markdown formatting and structure
```

**Step 4: Submission Preparation**
```markdown
// Prepare for submission:
// - Validate frontmatter completeness
// - Check internal/external links
// - Ensure proper file placement
// - Generate commit message following conventions
// - Create PR description with context
```

### Workflow 2: Code Contribution (Feature/Fix)

**Step 1: Code Planning**
```markdown
// Prompt: "Plan implementation for [feature/fix] that:
// - Follows IT-Journey coding standards
// - Includes comprehensive error handling (DFF)
// - Uses DRY principles for code reuse
// - Maintains simplicity (KIS)
// - Includes test coverage
// - Documents changes appropriately"
```

**Step 2: Implementation Guidance**
```markdown
// Generate code following:
// - Language-specific best practices
// - IT-Journey architectural patterns
// - Proper file organization (space.instructions.md)
// - Container-first development principles
// - Security and performance considerations
```

**Step 3: Testing & Validation**
```markdown
// Assist with:
// - Unit test generation
// - Integration test scenarios
// - Cross-platform testing considerations
// - CI/CD workflow validation
// - Manual testing checklists
```

**Step 4: Documentation Updates**
```markdown
// Ensure documentation updates:
// - README.md files affected by changes
// - Code comments and docstrings
// - Feature documentation if applicable
// - CHANGELOG.md entry
// - Migration guides if breaking changes
```

### Workflow 3: Documentation Contribution

**Step 1: Documentation Assessment**
```markdown
// Analyze existing documentation for:
// - Completeness and accuracy
// - Clarity and accessibility
// - Broken links or outdated information
// - Missing examples or context
// - Consistency with project standards
```

**Step 2: Improvement Suggestions**
```markdown
// Generate improvements that:
// - Follow README.instructions.md standards
// - Enhance readability and scannability
// - Add practical examples and use cases
// - Fix technical inaccuracies
// - Update cross-references and links
// - Improve accessibility
```

**Step 3: Style & Formatting**
```markdown
// Ensure documentation:
// - Uses proper markdown syntax
// - Follows heading hierarchy (H1 → H2 → H3)
// - Includes code blocks with language specification
// - Has descriptive link text
// - Uses consistent terminology
// - Maintains IT-Journey voice and style
```

## 🔍 Quality Assurance Guidelines

### Pre-Submission Checklist

**AI should validate before suggesting submission:**

```yaml
content_validation:
  - [ ] Frontmatter complete and valid
  - [ ] Educational objectives clear
  - [ ] Technical accuracy verified
  - [ ] Cross-platform compatibility noted
  - [ ] Accessibility considerations met
  - [ ] Fantasy theme consistent (for quests)

code_validation:
  - [ ] Follows language best practices
  - [ ] Includes error handling (DFF)
  - [ ] Reuses existing code (DRY)
  - [ ] Maintains simplicity (KIS)
  - [ ] Test coverage adequate
  - [ ] Documentation updated

documentation_validation:
  - [ ] No broken links
  - [ ] Proper markdown syntax
  - [ ] Consistent formatting
  - [ ] Examples tested and working
  - [ ] Cross-references updated
  - [ ] lastmod date current

general_validation:
  - [ ] Follows IT-Journey principles
  - [ ] Commit message follows conventions
  - [ ] PR description includes context
  - [ ] Related issues referenced
  - [ ] Community guidelines followed
```

### AI Validation Prompts

**For Content:**
```markdown
// Validate this [quest/post] for:
// - Educational value and learning objectives
// - Technical accuracy and completeness
// - Frontmatter requirements
// - IT-Journey style and voice
// - Cross-platform considerations
// - Accessibility compliance
```

**For Code:**
```markdown
// Review this code for:
// - IT-Journey coding standards
// - Error handling and resilience (DFF)
// - Code reuse and modularity (DRY)
// - Simplicity and maintainability (KIS)
// - Test coverage and quality
// - Documentation completeness
```

**For Documentation:**
```markdown
// Check this documentation for:
// - Accuracy and completeness
// - Clarity and readability
// - Proper markdown formatting
// - Working links and references
// - Consistent terminology
// - Accessibility features
```

## 📝 Commit Message Guidance

### Conventional Commits Format

**AI should generate commit messages following:**

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Scopes (examples):**
- `quest`: Quest-related changes
- `post`: Blog post changes
- `ci`: CI/CD workflow changes
- `script`: Automation script changes
- `docs`: Documentation changes

**Examples:**
```bash
feat(quest): add Docker fundamentals quest for beginners
fix(ci): resolve Jekyll build timeout in GitHub Actions
docs(readme): improve installation instructions for macOS
refactor(script): simplify hyperlink guardian validation logic
test(quest): add validation tests for quest metadata
```

### AI Commit Message Generation

**Prompt template:**
```markdown
// Generate a conventional commit message for:
// Changes: [summary of changes]
// Files affected: [list of files]
// Type: [feat/fix/docs/style/refactor/test/chore]
// Scope: [quest/post/ci/script/docs/etc]
// Impact: [what this changes or fixes]
```

## 🤝 Pull Request Assistance

### PR Description Template

**AI should help generate PR descriptions:**

```markdown
## Description
[Clear explanation of what this PR does and why]

## Type of Change
- [ ] New feature (non-breaking change adding functionality)
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] Documentation update
- [ ] Breaking change (fix or feature causing existing functionality to change)

## Changes Made
- [Specific change 1]
- [Specific change 2]
- [Specific change 3]

## Related Issues
Closes issue number (if applicable)
Related to issue number (if applicable)

## Testing
- [ ] Tested locally
- [ ] Cross-platform tested (if applicable)
- [ ] Existing tests pass
- [ ] New tests added (if applicable)

## Checklist
- [ ] Follows IT-Journey contribution guidelines
- [ ] Code/content follows project style standards
- [ ] Documentation updated
- [ ] Commit messages follow conventional format
- [ ] Self-review completed

## Screenshots (if applicable)
[Add screenshots for UI/visual changes]

## Additional Context
[Any additional information reviewers should know]
```

### PR Review Assistance

**When assisting with PR reviews, AI should:**

1. **Check Standards Compliance**
   - Validates against project guidelines
   - Identifies style inconsistencies
   - Checks frontmatter completeness

2. **Provide Constructive Feedback**
   - Suggest improvements with examples
   - Explain reasoning behind suggestions
   - Offer alternative approaches

3. **Highlight Positive Aspects**
   - Recognize good practices
   - Acknowledge quality contributions
   - Encourage continued participation

## 🌟 Community Engagement Support

### Helping Users Help Others

**When users want to contribute through community support:**

```markdown
// AI can assist with:
// - Searching documentation for answers
// - Drafting clear, helpful responses
// - Identifying relevant resources
// - Suggesting diagnostic steps
// - Formulating clarifying questions
```

**Community Response Template:**
```markdown
Hi [username]! 👋

Thanks for your question about [topic].

[Clear explanation or answer]

Here are some resources that might help:
- [Link to relevant documentation]
- [Link to related quest/post]
- [Link to similar discussion]

If you need more help, feel free to ask!

Happy learning! 🎯
```

## 🔄 Continuous Improvement

### Contribution Workflow Evolution

**AI should suggest improvements when:**
- Patterns in common issues emerge
- Documentation gaps are identified
- Workflow inefficiencies are noticed
- New best practices are established

**Improvement Suggestion Format:**
```markdown
// Observed pattern: [description]
// Impact: [who/what is affected]
// Suggested improvement: [proposed solution]
// Benefits: [expected outcomes]
// Implementation: [how to implement]
```

## 📚 Key Resources for AI Agents

**Always reference these when assisting:**

- **README.instructions.md** - Documentation standards
- **quest.instructions.md** - Quest creation guidelines
- **posts.instructions.md** - Blog post standards
- **features.instructions.md** - Feature development pipeline
- **space.instructions.md** - Project organization principles
- **Main copilot-instructions.md** (in .github/) - Core principles and AI integration guidelines

## 🎯 Success Metrics

**Contributions assisted by AI should result in:**
- ✅ Higher quality submissions on first attempt
- ✅ Faster contribution process for contributors
- ✅ Better adherence to project standards
- ✅ More comprehensive documentation
- ✅ Increased contributor confidence
- ✅ Reduced reviewer workload
- ✅ Stronger community engagement

---

**Remember**: AI assists contributors, but humans make creative decisions, provide final approval, and build community relationships. The goal is to make contributing easier and more rewarding, not to automate away the human element of open-source collaboration.

**Last Updated**: 2025-11-07 | **Maintained by**: IT-Journey Team
