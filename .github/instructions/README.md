# AI Agent Instructions Directory

This directory contains specialized instructions for AI agents (like VS Code Copilot, GitHub Copilot, and other AI assistants) to help them better assist contributors to the IT-Journey project.

## Purpose

These instruction files serve a different purpose than contributor documentation:

- **Human Documentation** (CONTRIBUTING.md, docs/) - Explains **what** to do and **how** to contribute
- **AI Instructions** (.github/instructions/) - Guides AI agents on **how to assist** humans contributing

## Structure

### Instruction File Format

Each `.instructions.md` file follows a consistent frontmatter format:

```yaml
---
applyTo: 'file-patterns'  # Required: glob patterns for file matching (use single quotes)
---

# Content Title

Brief description of the instruction file's purpose and scope.

## Content sections

---

**Version:** X.Y.Z | **Last Modified:** YYYY-MM-DD | **Author:** Team Name

**Related Files:**
- `other-file.md`: Relationship description
```

**Note:** Per GitHub Copilot documentation, only the `applyTo` field is required in frontmatter. Additional metadata (version, author, etc.) is placed in the document body footer.

### Available Instruction Files

| File | Purpose | Target Audience |
|------|---------|-----------------|
| `contributing.instructions.md` | Guide AI agents in assisting contributors | All contribution types |
| `README.instructions.md` | Standards for creating and maintaining README files | Documentation contributors |
| `quest.instructions.md` | Quest creation standards and patterns | Educational content creators |
| `posts.instructions.md` | Blog post creation and chronicle standards | Content authors |
| `features.instructions.md` | Feature development pipeline and CI/CD | Code contributors |
| `space.instructions.md` | Project organization and workspace structure | All contributors |
| `prompts.instructions.md` | Prompt engineering for AI development | AI-assisted development |
| `scripts.instructions.md` | Script development standards and best practices | Script developers and automation engineers |

## How AI Agents Use These Instructions

### Context Loading

When a user works on specific file types or tasks, AI agents should:

1. **Identify the task type** (contributing, creating quest, writing post, etc.)
2. **Load relevant instructions** from this directory
3. **Apply guidelines** while assisting the user
4. **Maintain quality standards** defined in the instructions

### Instruction Hierarchy

1. **Main Copilot Instructions** (`.github/copilot-instructions.md`) - Core principles
2. **Specific Instructions** (this directory) - Task-specific guidance
3. **Human Documentation** (docs/, CONTRIBUTING.md) - Context and requirements

### Integration Pattern

```markdown
// AI Agent workflow example:
// 1. User: "Help me create a new quest"
// 2. AI loads: quest.instructions.md
// 3. AI also references: README.instructions.md (for documentation)
// 4. AI assists while following IT-Journey principles (DFF, DRY, KIS, etc.)
```

## Key Principles

All instruction files emphasize:

- **🤖 Assist, Don't Replace** - Help humans, don't make decisions for them
- **📚 Educate While Helping** - Teach contributors project standards
- **✅ Maintain Quality** - Ensure contributions meet project requirements
- **🤝 Facilitate Collaboration** - Help contributors work with the community

## Differences from Contributor Docs

### Contributor Documentation

**Location:** `/CONTRIBUTING.md`, `/docs/`, `/pages/_about/contribute/`

**Audience:** Human contributors

**Purpose:**
- Explain how to contribute
- Provide setup instructions
- Document standards and guidelines
- Share best practices
- Link to resources

**Format:** Human-readable tutorials, guides, references

### AI Agent Instructions

**Location:** `/.github/instructions/`

**Audience:** AI agents (VS Code Copilot, etc.)

**Purpose:**
- Guide AI assistance behavior
- Define quality validation rules
- Provide generation templates
- Specify automation patterns
- Set guardrails for AI assistance

**Format:** Structured prompts, validation checklists, generation patterns

## Example Use Cases

### Use Case 1: Creating a Quest

**Human reads:** `docs/standards/CONTENT_GUIDELINES.md`, main `CONTRIBUTING.md`

**AI agent reads:** `quest.instructions.md`, `README.instructions.md`

**Result:** Human understands quest philosophy and structure; AI helps generate proper frontmatter, suggests educational content patterns, validates quest structure

### Use Case 2: Fixing Documentation

**Human reads:** Main `CONTRIBUTING.md`, `docs/CONTRIBUTING_DEVELOPER.md`

**AI agent reads:** `README.instructions.md`, `contributing.instructions.md`

**Result:** Human knows where to find issues; AI helps identify broken links, suggests improvements, validates markdown syntax

### Use Case 3: Building a Feature

**Human reads:** `docs/CONTRIBUTING_DEVELOPER.md`, `docs/setup/DEVELOPMENT_ENVIRONMENT.md`

**AI agent reads:** `features.instructions.md`, `space.instructions.md`

**Result:** Human understands development workflow; AI helps generate code following project patterns, creates tests, updates documentation

## Maintenance

### When to Update

Update instruction files when:
- [ ] Project standards change
- [ ] New contribution types are added
- [ ] AI assistance patterns improve
- [ ] Common issues are identified
- [ ] Community feedback suggests improvements

### Update Guidelines

1. **Keep descriptions under 160 characters** for frontmatter
2. **Use only supported frontmatter fields** (`description`, `applyTo`)
3. **Maintain consistency** with other instruction files
4. **Test with AI agents** to ensure effectiveness
5. **Document changes** in the instruction file itself

### Review Schedule

- **Weekly:** Check for broken references
- **Monthly:** Review effectiveness with contributors
- **Quarterly:** Update based on community feedback

## Contributing to Instructions

### Improving AI Instructions

If you notice AI agents could assist better:

1. **Identify the gap** - What could be clearer or more helpful?
2. **Check existing instructions** - Is it already covered?
3. **Propose improvement** - Open an issue or PR
4. **Test with AI** - Verify the improvement helps
5. **Document rationale** - Explain why the change helps

### Creating New Instructions

When adding new instruction files:

1. **Follow the template** - Use existing files as examples
2. **Keep frontmatter minimal** - Only `description` and `applyTo`
3. **Focus on AI guidance** - Not human documentation
4. **Include examples** - Show AI agents what to generate
5. **Add to this README** - Update the table above

## Related Resources

- **[Main Contributing Guide](../../CONTRIBUTING.md)** - Human contribution workflow
- **[Developer Guide](../../docs/CONTRIBUTING_DEVELOPER.md)** - Complete developer documentation
- **[Copilot Instructions](../copilot-instructions.md)** - Core AI agent principles
- **[Web Contributing Page](https://it-journey.dev/about/contributing/)** - Public contribution info

## Questions?

- **About human contributions:** See [CONTRIBUTING.md](../../CONTRIBUTING.md)
- **About AI assistance:** Open an issue with `ai-assistance` label
- **About instruction format:** Reference existing `.instructions.md` files

---

**Last Updated:** 2025-11-18  
**Maintained by:** IT-Journey Team  
**Purpose:** Enable AI agents to assist contributors more effectively while maintaining project quality and standards
