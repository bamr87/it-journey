# IT-Journey Copilot Instructions

These instructions are based on the core principles and approaches outlined in our About page, designed to guide AI-powered development practices for the IT-Journey platform.

## Core Development Principles

### Design for Failure (DFF)
- Always implement error handling and graceful degradation in generated code
- Include try-catch blocks with meaningful error messages
- Suggest redundancy and fallback mechanisms
- Add monitoring and logging capabilities where appropriate
- Consider edge cases and potential failure points

### Don't Repeat Yourself (DRY)
- Extract common functionality into reusable functions, components, or modules
- Suggest refactoring when duplicate code patterns are detected
- Create utility functions for repeated operations
- Use configuration files for repeated constants or settings
- Recommend template patterns for similar structures

### Keep It Simple (KIS)
- Prefer clear, readable code over clever optimizations
- Use descriptive variable and function names
- Break complex functions into smaller, focused units
- Avoid unnecessary abstractions or over-engineering
- Choose well-established patterns over custom solutions

### Release Early and Often (REnO)
- Suggest incremental development approaches
- Recommend feature flags for gradual rollouts
- Focus on minimal viable implementations first
- Include versioning strategies in code suggestions
- Encourage continuous integration practices

### Minimum Viable Product (MVP)
- Prioritize core functionality over advanced features
- Suggest starting with basic implementations that can be enhanced later
- Focus on solving the primary user problem first
- Recommend iterative improvement approaches
- Avoid feature creep in initial implementations

### Collaboration (COLAB)
- Write self-documenting code with clear comments
- Follow consistent coding standards and conventions
- Include comprehensive README and documentation suggestions
- Use semantic commit messages and PR descriptions
- Consider team workflows in code organization

### AI-Powered Development (AIPD)
- Leverage AI tools effectively for code generation and review
- Suggest AI-assisted testing and documentation approaches
- Recommend AI integration patterns for enhanced productivity
- Balance AI assistance with human oversight and review
- Use AI for learning and skill development, not replacement

## Technology-Specific Guidelines

### @azure Rule - Use Azure Best Practices
When generating code for Azure, running terminal commands for Azure, or performing operations related to Azure, invoke your `azure_development-get_best_practices` tool if available.

### Open Source Development
- Follow open source licensing and contribution guidelines
- Include appropriate attribution and credits
- Use community-standard project structures
- Encourage community contributions and feedback
- Maintain compatibility with popular tools and frameworks

### Documentation Standards
- Generate comprehensive README files for all projects
- Include installation, usage, and contribution guidelines
- Add inline code documentation for complex logic
- Create user guides and API documentation when relevant
- Maintain changelogs and version documentation

### Testing Approaches
- Include unit tests for core functionality
- Suggest integration tests for system interactions
- Recommend end-to-end tests for critical user workflows
- Use AI-powered testing tools when appropriate
- Implement test automation in CI/CD pipelines

## Code Quality Standards

### Security Best Practices
- Validate all user inputs and external data
- Use secure authentication and authorization patterns
- Avoid hardcoding sensitive information
- Implement proper error handling without information leakage
- Follow security frameworks and standards

### Performance Considerations
- Optimize for readability first, performance second
- Suggest performance improvements only when necessary
- Use appropriate data structures and algorithms
- Consider caching strategies for expensive operations
- Monitor and measure performance impacts

### Accessibility & Inclusivity
- Follow web accessibility guidelines (WCAG) for web projects
- Use inclusive language in code comments and documentation
- Consider internationalization and localization needs
- Design for diverse user abilities and technologies
- Test with assistive technologies when relevant

## Learning & Education Focus

### Beginner-Friendly Approach
- Explain complex concepts in simple terms
- Provide step-by-step guidance for implementations
- Include learning resources and references
- Suggest progressive skill-building exercises
- Encourage experimentation and exploration

### Real-World Applications
- Focus on practical, usable solutions
- Include examples relevant to everyday development
- Connect theoretical concepts to practical implementations
- Suggest projects that build portfolio value
- Emphasize industry-standard practices

### Community Learning
- Encourage peer collaboration and code review
- Suggest community resources and forums
- Promote knowledge sharing and mentoring
- Include contribution opportunities in suggestions
- Foster inclusive and welcoming environments

## AI Integration Guidelines

### AI-Assisted Development
- Use AI for code generation, but always review and understand output
- Leverage AI for documentation generation and maintenance
- Implement AI-powered testing and quality assurance
- Use AI for learning acceleration and skill development
- Balance automation with human creativity and oversight

### Best Practices for AI Tools
- Provide clear context and requirements to AI assistants
- Review AI-generated code for security and performance
- Use AI feedback loops for continuous improvement
- Maintain human oversight for critical decisions
- Document AI tool usage and configurations

## Pages Directory Structure and Content Guidelines

The `pages/` directory is the heart of the IT-Journey content ecosystem, organized into specialized subsections that serve different educational and organizational purposes. Each subsection follows specific style, structure, and content requirements to maintain consistency and educational effectiveness.

### _about/ - Platform Information and Philosophy

**Purpose**: Contains foundational information about the IT-Journey platform, its principles, and organizational structure.

**Structure Requirements**:
- Use clear, informative frontmatter with `title`, `excerpt`, `permalink`, and `description`
- Include comprehensive category and tag systems
- Maintain consistent permalink structure (`/about/[topic]/`)
- Use `draft: published` status for live content

**Content Guidelines**:
- **Tone**: Professional, welcoming, and educational
- **Audience**: New visitors and community members
- **Length**: Comprehensive but accessible (500-2000 words)
- **Format**: Well-structured with clear headings and sections
- **Required Elements**:
  - Mission statement and platform overview
  - Core development principles (DRY, KIS, DFF, REnO, MVP, COLAB, AIPD)
  - Community guidelines and contribution information
  - Platform features and capabilities

**Subdirectories**:
- `contribute/` - Contribution guidelines and processes
- `features/` - Platform feature documentation
- `profile/` - User profile and personalization settings
- `settings/` - Configuration and customization options

### _posts/ - Learning Journey Chronicles

**Purpose**: Chronological blog posts documenting AI-assisted development sessions, learning experiences, and technical discoveries.

**Naming Convention**: `YYYY-MM-DD-descriptive-title-with-hyphens.md`

**Frontmatter Requirements**:
```yaml
---
title: "Descriptive Title: Clear Learning Objective"
description: "Brief description explaining the learning objective and outcome"
date: YYYY-MM-DDTHH:MM:SS.000Z
preview: "Short preview text or image path"
tags:
    - ai-assisted-development
    - [specific-technology]
    - learning-journey
categories:
    - Development
    - Learning-Journey
sub-title: "Concise explanation of the specific focus"
excerpt: "One-sentence summary of the key learning or achievement"
snippet: "Memorable quote or key insight from the session"
author: "IT-Journey Team"
layout: journals
keywords:
    primary:
        - main topic keyword
    secondary:
        - supporting concepts
lastmod: YYYY-MM-DDTHH:MM:SS.000Z
---
```

**Content Structure**:
1. **Challenge Introduction**: What problem were we solving?
2. **AI-Assisted Approach**: Tools used, collaboration process
3. **Step-by-Step Implementation**: Detailed, reproducible steps
4. **Learning Insights**: Key discoveries and best practices
5. **Code Examples**: Fully functional, well-commented code
6. **Troubleshooting**: Challenges encountered and solutions
7. **Future Development**: Next steps and evolution paths

**Content Guidelines**:
- **Educational Focus**: Emphasize learning process over just results
- **AI Collaboration**: Document human-AI partnership clearly
- **Reproducibility**: Ensure others can follow the steps
- **Code Quality**: All examples must be tested and functional
- **Reflection**: Include honest assessment of successes and failures

### _notes/ - Technical Documentation and Quick References

**Purpose**: Organized technical documentation, tutorials, quick references, and development notes.

**Organization Structure**:
- **Date-based files**: `YYYY-MM-DD-topic-name.md` for time-sensitive content
- **Topical subdirectories**:
  - `cheetsheets/` - Quick reference guides and command summaries
  - `code-snippets/` - Reusable code examples and utilities
  - `dev/` - Development environment setup and configuration
  - `Journal Entries/` - Personal learning reflections and progress tracking
  - `misc/` - Miscellaneous technical notes and discoveries
  - `zero/` - Foundational concepts and beginner-friendly guides

**Frontmatter Standards**:
```yaml
---
title: "Clear, Descriptive Title"
description: "Brief description for search and social media"
date: YYYY-MM-DDTHH:MM:SS.000Z
preview: "/path/to/preview/image.png"
tags:
    - specific-technology
    - topic-category
    - difficulty-level
categories:
    - guides
    - [specific-category]
excerpt: "Brief summary of the content's value"
author: "[Author Name]"
lastmod: YYYY-MM-DDTHH:MM:SS.000Z
draft: "draft|published"
---
```

**Content Requirements**:
- **Practical Focus**: Immediately actionable information
- **Clear Examples**: Step-by-step instructions with expected outputs
- **Cross-Platform Support**: Include macOS, Windows, and Linux instructions where applicable
- **Version Information**: Specify tool versions and compatibility
- **Update Schedule**: Regular review and maintenance for accuracy

### _quests/ - Gamified Learning Experiences

**Purpose**: Interactive, gamified learning modules that transform technical education into engaging adventures.

**Structure**: Follow the comprehensive quest creation standards outlined in `quest.instructions.md`

**Key Requirements**:
- **Binary Level System**: Use binary-coded progression (Level 0000-1111+)
- **Fantasy Theme Integration**: RPG metaphors and magical terminology
- **Multi-Platform Paths**: Support for macOS, Windows, Linux, and cloud platforms
- **Progressive Difficulty**: Clear skill building from novice to expert
- **Measurable Objectives**: Specific, achievable learning outcomes
- **Validation Criteria**: Methods to verify skill acquisition

**Content Elements**:
- Epic fantasy-themed introductions
- Clear quest objectives and learning outcomes
- Multi-platform implementation paths
- Progressive learning chapters
- Hands-on implementation challenges
- Rewards and achievement systems
- Comprehensive resource libraries

### _notebooks/ - Jupyter Notebook Integration

**Purpose**: Interactive computational documents combining code, documentation, and results.

**File Types**:
- `.ipynb` - Original Jupyter notebook files
- `.md` - Markdown conversions of notebooks for web display
- Supporting documentation files

**Content Standards**:
- **Educational Focus**: Clear explanations accompanying code cells
- **Reproducibility**: Include all dependencies and setup instructions
- **Output Preservation**: Maintain cell outputs for reference
- **Documentation**: Comprehensive markdown cells explaining concepts
- **Code Quality**: Well-commented, production-ready code examples

**Integration Requirements**:
- Automatic conversion to markdown for Jekyll integration
- Consistent frontmatter for web display
- Version control best practices for notebook files
- Clear learning objectives and outcomes

### _docs/ - Technical Documentation Hub

**Purpose**: Comprehensive technical documentation, API references, and system guides.

**Organization**:
- `index.md` - Documentation navigation and overview
- Topic-specific subdirectories (e.g., `jekyll/`)
- Hierarchical structure matching system architecture

**Documentation Standards**:
- **Comprehensive Coverage**: Complete feature and API documentation
- **Searchable Content**: Well-structured with clear headings
- **Cross-References**: Links between related topics
- **Examples**: Practical code examples and use cases
- **Maintenance**: Regular updates reflecting system changes

### _hobbies/ - Personal Interest Content

**Purpose**: Content related to personal interests and hobbies that may intersect with technology.

**Content Guidelines**:
- **Casual Tone**: More relaxed and personal writing style
- **Technology Integration**: Show how IT skills apply to personal interests
- **Community Building**: Encourage sharing of diverse interests
- **Learning Opportunities**: Connect hobbies to skill development

### _quickstart/ - Rapid Onboarding Guides

**Purpose**: Fast-track guides for immediate platform engagement and quick wins.

**Content Requirements**:
- **Brevity**: Essential information only, no unnecessary details
- **Sequential Steps**: Clear, numbered procedures
- **Quick Validation**: Immediate feedback and success confirmation
- **Progressive Disclosure**: Links to deeper learning resources
- **Platform Agnostic**: Work across different environments when possible

### Root-Level Pages

**home.md**: Platform landing page with welcoming introduction and navigation
**search.md**: Search functionality and content discovery tools
**index.html**: Technical index page for Jekyll processing

## Content Quality Assurance Standards

### Universal Requirements for All Pages Sections

1. **Accessibility**: Follow WCAG guidelines with proper heading hierarchy
2. **SEO Optimization**: Complete frontmatter with meta descriptions
3. **Mobile Responsiveness**: Content readable on all device sizes
4. **Cross-Platform Compatibility**: Instructions work across operating systems
5. **Version Control**: Semantic versioning for significant updates
6. **Community Guidelines**: Inclusive language and welcoming tone
7. **Educational Value**: Every piece of content teaches something valuable
8. **Practical Application**: Real-world relevance and actionable information

### Content Review Checklist

Before publishing any content in the pages directory:
- [ ] Frontmatter follows section-specific standards
- [ ] Content aligns with educational mission and principles
- [ ] Code examples are tested and functional
- [ ] Language is inclusive and accessible
- [ ] Cross-references and links are validated
- [ ] SEO elements are properly configured
- [ ] Content provides clear learning value
- [ ] Formatting follows Jekyll and Markdown standards

---

*These instructions embody the IT-Journey mission to democratize IT education through open-source principles, collaborative learning, and AI-enhanced development practices.*

