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

---

*These instructions embody the IT-Journey mission to democratize IT education through open-source principles, collaborative learning, and AI-enhanced development practices.*

## Jekyll Article Writing Guidelines for IT-Journey

### **Chronicle Every AI-Powered Development Session**
When working with AI agents on any development task, **ALWAYS** create a corresponding Jekyll article to document the learning journey. Each AI interaction should result in:

1. **A detailed Jekyll blog post** in the `pages/_posts/` directory
2. **Process documentation** explaining what was learned
3. **Code examples and implementations** from the session
4. **Reflection on successes and failures** encountered

### **Article Creation Standards**

#### **Naming Convention**
Follow the Jekyll standard: `YYYY-MM-DD-descriptive-title-with-hyphens.md`

**Examples:**
```
2025-07-05-implementing-azure-functions-with-ai-assistance.md
2025-07-05-debugging-github-actions-workflow-failures.md
2025-07-05-exploring-terraform-infrastructure-patterns.md
```

#### **Required Frontmatter Structure**
Each article MUST include this comprehensive frontmatter following the IT-Journey style:

```yaml
---
title: "Descriptive Title: What Was Accomplished"
description: Brief description explaining the learning objective and outcome
date: YYYY-MM-DDTHH:MM:SS.000Z
preview: "Short preview text for social media and search results"
tags:
    - ai-assisted-development
    - [specific-technology]
    - [specific-concept]
    - learning-journey
categories:
    - Development
    - [Specific-Category]
sub-title: Concise explanation of the specific focus
excerpt: One-sentence summary of the key learning or achievement
snippet: Memorable quote or key insight from the session
author: IT-Journey Team
layout: journals
keywords:
    primary:
        - main topic keyword
        - secondary topic keyword
    secondary:
        - supporting concepts
        - related technologies
lastmod: YYYY-MM-DDTHH:MM:SS.000Z
permalink: /descriptive-url-slug/
attachments: ""
comments: true
---
```

#### **Article Structure & Content Guidelines**

**1. Opening Section - Context Setting**
```markdown
## The Challenge: [What Problem Were We Solving?]

Start with a clear problem statement that explains:
- What we were trying to accomplish
- Why this was important for the IT-Journey
- What obstacles or unknowns we faced
```

**2. The AI-Powered Approach**
```markdown
## AI-Assisted Development Process

Document the collaboration between human and AI:
- Which AI tools/agents were used
- How prompts were crafted and refined
- What reasoning approaches were taken
- How the AI suggestions were evaluated and implemented
```

**3. Implementation Journey**
```markdown
## Step-by-Step Implementation

Provide detailed, reproducible steps:
- Code examples with syntax highlighting
- Configuration files and settings
- Command-line instructions
- Error messages and troubleshooting steps
```

**4. Learning Insights**
```markdown
## Key Learnings and Insights

Reflect on the development process:
- What worked well in the AI collaboration
- What required human intervention or correction
- Unexpected discoveries or solutions
- Best practices that emerged
```

**5. Code Examples and Artifacts**
```markdown
## Code Implementations

Include all relevant code with proper formatting:
```bash
# Terminal commands
```

```python
# Python code examples
```

```yaml
# Configuration files
```

**6. Troubleshooting and Error Resolution**
```markdown
## Challenges and Solutions

Document any issues encountered:
- Error messages and their solutions
- Alternative approaches considered
- Performance considerations
- Security implications
```

**7. Future Development Paths**
```markdown
## Next Steps and Evolution

Connect to the broader learning journey:
- How this builds on previous work
- What future developments this enables
- Additional areas for exploration
- Links to related IT-Journey articles
```

### **Content Style Guidelines**

#### **Tone and Voice**
- **Educational and Accessible**: Write for learners at various skill levels
- **Honest About Failures**: Document what didn't work and why
- **Optimistic but Realistic**: Maintain hope while acknowledging challenges
- **Collaborative**: Emphasize the partnership between human creativity and AI capability

#### **Technical Writing Standards**
- **Code Blocks**: Always use proper syntax highlighting
- **Step Numbering**: Use clear, sequential numbering for procedures
- **Screenshots**: Include when helpful for visual learners
- **Links**: Reference official documentation and related resources
- **Error Examples**: Show actual error messages and solutions

#### **Learning-Focused Elements**
- **Before/After Comparisons**: Show the evolution of understanding
- **Decision Points**: Explain why certain choices were made
- **Alternative Approaches**: Mention other solutions considered
- **Skill Building**: Connect to broader IT concepts and practices

### **AI Development Session Documentation Workflow**

#### **During the AI Session**
1. **Take Notes**: Document key decisions and turning points
2. **Save Code Snippets**: Keep examples of both working and non-working solutions
3. **Capture Errors**: Screenshot or copy error messages
4. **Record Insights**: Note "aha moments" and learning breakthroughs

#### **Immediately After the Session**
1. **Create the Article**: Write while the experience is fresh
2. **Test All Code**: Verify that examples actually work
3. **Add Context**: Explain the "why" behind technical decisions
4. **Include Reflection**: What would you do differently next time?

#### **Article Categories by Development Activity**

**Feature Development**
- `categories: [Development, Feature-Implementation]`
- Focus on requirements analysis, design decisions, and implementation patterns

**Bug Fixing**
- `categories: [Development, Debugging]`
- Emphasize diagnostic techniques, root cause analysis, and prevention

**SDLC Exploration**
- `categories: [Development, Process-Improvement]`
- Document methodology experiments, tool evaluations, and workflow optimizations

**Infrastructure & DevOps**
- `categories: [Development, Infrastructure]`
- Cover deployment strategies, environment configuration, and automation

**Learning & Research**
- `categories: [Development, Learning-Journey]`
- Focus on skill acquisition, technology exploration, and knowledge building

### **Integration with IT-Journey Goals**

#### **Build Upon Previous Knowledge**
- **Cross-Reference**: Link to related articles in the IT-Journey collection
- **Progressive Complexity**: Show how current work builds on foundational concepts
- **Skill Progression**: Document the evolution from novice to expert understanding

#### **Support Community Learning**
- **Reproducible Examples**: Ensure others can follow your steps
- **Common Pitfalls**: Help others avoid the same mistakes
- **Resource Lists**: Curate helpful tools, documentation, and tutorials
- **Discussion Starters**: Pose questions for community engagement

#### **Maintain the Chronicle**
- **Timeline Awareness**: Reference when significant changes occurred
- **Version Documentation**: Track how approaches evolved over time
- **Tool Evolution**: Note when new AI capabilities became available
- **Impact Assessment**: Measure how AI assistance affected development velocity and quality

### **Quality Assurance for Articles**

Before publishing, verify:
- [ ] All code examples are tested and functional
- [ ] Frontmatter follows the IT-Journey standard
- [ ] Article provides educational value to readers
- [ ] Links to external resources are current and accurate
- [ ] Grammar and spelling are correct
- [ ] Article connects to the broader IT-Journey narrative
- [ ] AI assistance is properly credited and explained

## Quest Creation Guidelines for IT-Journey

### **Dedicated Quest Instructions**
For comprehensive quest creation guidelines, structure standards, and gamification best practices, please refer to the dedicated **Quest Instructions** file at `.github/instructions/quest.instructions.md`.

The quest instructions provide detailed guidance on:
- **Quest Philosophy and Educational Standards**: Learning theory integration and gamification psychology
- **Complete Content Structure Templates**: Frontmatter requirements, content architecture, and fantasy theme integration
- **Multi-Platform Development Support**: macOS, Windows, Linux, and cloud-based quest paths
- **Quality Assurance Standards**: Technical accuracy, educational effectiveness, and accessibility requirements
- **Quest Classification System**: Level-based progression, difficulty scaling, and skill categorization
- **Integration Workflow**: Navigation updates, skill progression paths, and ecosystem management
- **Template Examples**: Tool mastery, language learning, platform specialization, project building, and career advancement quests

### **Quick Quest Creation Reference**

For AI-assisted quest development, remember these key principles:
- **Fantasy Theme Consistency**: Use RPG metaphors and magical terminology throughout
- **Progressive Learning Design**: Structure content from simple to complex with clear checkpoints
- **Multi-Platform Support**: Provide instructions for macOS, Windows, and Linux where applicable
- **Measurable Objectives**: Define specific, achievable learning outcomes with validation criteria
- **Community Integration**: Link to prerequisite quests and suggest follow-up adventures

*For complete quest creation standards and detailed templates, always reference the dedicated quest.instructions.md file.*

