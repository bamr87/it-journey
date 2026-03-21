---
applyTo: 'TODO/**/*'
date: 2025-12-20T10:05:28.000Z

---

# TODO Directory Instructions for AI Agents

AI agent instructions for managing, maintaining, and optimizing the TODO directory in the IT-Journey project. These instructions guide AI assistants in helping users create, organize, track, and complete tasks effectively while maintaining quality standards and project alignment.

## 🤖 AI Agent Role in TODO Management

### Primary Objectives
- **Assist in Task Organization**: Help users structure TODOs with clear objectives, priorities, and success criteria
- **Maintain Consistency**: Ensure all TODO items follow project standards and frontmatter conventions
- **Track Progress**: Help monitor task completion, identify blockers, and suggest next actions
- **Prioritize Effectively**: Use data-driven insights to recommend task ordering
- **Connect to Roadmap**: Align TODOs with project goals in `roadmap.md` and `PRD.md`

### AI Assistant Boundaries
- **AI Does**: Generate task templates, suggest priorities, validate TODO structure, automate status updates
- **AI Doesn't**: Make strategic decisions, determine business priorities, approve resource allocation
- **Human Does**: Define project goals, approve priorities, allocate resources, make final decisions
- **Human Validates**: Ensures alignment with business objectives, validates effort estimates

## 📋 TODO Directory Structure

### Standard Directory Layout

```
TODO/
├── README.md                    # Hub for all TODOs (this file)
├── todo.instructions.md         # AI agent instructions (this file)
├── STATUS.md                    # Real-time status dashboard
├── ARCHIVE/                     # Completed TODO projects
│   └── [completed-project]/     # Archived project files
├── seo/                         # SEO optimization TODOs
│   ├── README.md                # SEO project overview
│   ├── OPTIMIZATION_PLAN.md     # Detailed plan
│   ├── QUICK_ACTIONS.md         # Immediate tasks
│   └── TRACKING.md              # Performance tracking
├── content/                     # Content creation TODOs
│   └── [topic-specific-files]
├── technical/                   # Technical debt and improvements
│   └── [feature-specific-files]
└── templates/                   # Reusable templates
    ├── PROJECT_TEMPLATE.md      # New project template
    ├── TASK_TEMPLATE.md         # Individual task template
    └── TRACKING_TEMPLATE.md     # Progress tracking template
```

### File Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Project README | `README.md` | `seo/README.md` |
| Action Plan | `[ACTION]_PLAN.md` | `OPTIMIZATION_PLAN.md` |
| Quick Tasks | `QUICK_ACTIONS.md` | `seo/QUICK_ACTIONS.md` |
| Tracking | `TRACKING.md` | `seo/TRACKING.md` |
| Templates | `[TYPE]_TEMPLATE.md` | `PROJECT_TEMPLATE.md` |

## 🎯 TODO Item Standards

### Required Frontmatter for TODO Files

```yaml
---
title: "[Clear, action-oriented title]"
description: "[What this TODO accomplishes and why it matters]"
created: YYYY-MM-DDTHH:MM:SS.000Z
lastmod: YYYY-MM-DDTHH:MM:SS.000Z
status: "PLANNING | IN_PROGRESS | BLOCKED | REVIEW | COMPLETE | ARCHIVED"
priority: "CRITICAL | HIGH | MEDIUM | LOW"
category: "[seo | content | technical | documentation | automation]"
owner: "[team or individual]"
estimated_effort: "[time estimate]"
due_date: YYYY-MM-DD  # Optional
dependencies: []       # List of blocking items
tags:
  - todo
  - [category]
  - [priority-level]
---
```

### Task Item Format

Individual tasks within TODO files should follow this structure:

```markdown
### Task Title
- [ ] **Actionable item** with clear deliverable
  - **File**: `path/to/file.md` (if applicable)
  - **Current State**: What exists now
  - **Target State**: What should exist after
  - **Effort**: [time estimate]
  - **Priority**: [CRITICAL | HIGH | MEDIUM | LOW]
  - **Dependencies**: [list any blockers]
```

### Priority Definitions

| Priority | Criteria | Response Time |
|----------|----------|---------------|
| 🔴 CRITICAL | Blocking production, affects users | Immediate (same day) |
| 🟠 HIGH | Important for goals, time-sensitive | Within 1 week |
| 🟡 MEDIUM | Improves quality, planned work | Within 2-4 weeks |
| 🟢 LOW | Nice-to-have, future improvement | When convenient |

### Status Definitions

| Status | Description | Next Action |
|--------|-------------|-------------|
| 📋 PLANNING | Defining scope and requirements | Create action plan |
| 🔄 IN_PROGRESS | Active work happening | Continue execution |
| ⏸️ BLOCKED | Waiting on dependency | Resolve blocker |
| 👀 REVIEW | Ready for validation | Review and approve |
| ✅ COMPLETE | Finished and verified | Archive |
| 📦 ARCHIVED | Historical reference | None |

## 🤖 AI Workflows for TODO Management

### Workflow 1: Creating New TODO Projects

**Step 1: Intent Detection**
```markdown
// Prompt: "Analyze user request to determine TODO type:
// - Is this a new project or addition to existing?
// - What category does it belong to (seo/content/technical)?
// - What's the scope and estimated effort?
// - What are the dependencies and blockers?"
```

**Step 2: Structure Generation**
```markdown
// Generate TODO structure that:
// - Follows project frontmatter standards
// - Breaks work into actionable tasks
// - Sets realistic priorities and estimates
// - Connects to roadmap goals
// - Includes success metrics
```

**Step 3: File Creation**
```markdown
// Create appropriate files:
// - Main README.md for project overview
// - Detailed plan files for complex work
// - Quick actions for immediate tasks
// - Tracking templates for progress monitoring
```

### Workflow 2: Processing and Prioritizing TODOs

**Step 1: Analysis**
```markdown
// Analyze existing TODOs for:
// - Completeness of task definitions
// - Accuracy of priority assignments
// - Alignment with project goals
// - Realistic effort estimates
// - Missing dependencies or blockers
```

**Step 2: Prioritization Recommendations**
```markdown
// Suggest task ordering based on:
// - Impact vs effort matrix (do high-impact/low-effort first)
// - Dependency chains (unblock other work)
// - Time sensitivity (deadlines, events)
// - Resource availability
// - Strategic alignment with roadmap
```

**Step 3: Status Updates**
```markdown
// Help maintain status by:
// - Prompting for progress updates
// - Identifying stale items (no updates > 7 days)
// - Suggesting status transitions
// - Flagging potential blockers
```

### Workflow 3: Tracking and Reporting

**Step 1: Progress Collection**
```markdown
// Gather progress data:
// - Count tasks by status (not-started, in-progress, complete)
// - Calculate completion percentages
// - Identify velocity trends
// - Highlight blockers and risks
```

**Step 2: Report Generation**
```markdown
// Generate reports including:
// - Executive summary (what's done, what's next)
// - Detailed status by project
// - Blockers and risk assessment
// - Recommendations for next actions
```

## 📊 AI-Generated Templates

### New Project Template

```markdown
---
title: "[Project Name]"
description: "[What this project accomplishes]"
created: YYYY-MM-DDTHH:MM:SS.000Z
lastmod: YYYY-MM-DDTHH:MM:SS.000Z
status: "PLANNING"
priority: "[CRITICAL | HIGH | MEDIUM | LOW]"
category: "[category]"
owner: "IT-Journey Team"
estimated_effort: "[total estimate]"
expected_impact: "[measurable outcome]"
tags:
  - todo
  - [category]
---

# 📁 [Project Name]

> **Project Goal**: [Clear statement of what success looks like]

## 📋 Project Overview

### Objectives
- 🎯 [Primary objective]
- 🎯 [Secondary objective]
- 🎯 [Tertiary objective]

### Success Metrics
| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| [Metric 1] | [baseline] | [goal] | [date] |
| [Metric 2] | [baseline] | [goal] | [date] |

### Scope
**In Scope:**
- [Included work item]
- [Included work item]

**Out of Scope:**
- [Excluded work item]
- [Excluded work item]

---

## 🚀 Phase 1: [Phase Name] (Week X)
*Target: [What this phase accomplishes]*

### High Priority Tasks
- [ ] **Task 1** - [Description]
  - File: `path/to/file`
  - Effort: [estimate]
- [ ] **Task 2** - [Description]
  - Effort: [estimate]

### Medium Priority Tasks
- [ ] **Task 3** - [Description]
- [ ] **Task 4** - [Description]

---

## 🚀 Phase 2: [Phase Name] (Week X)
*Target: [What this phase accomplishes]*

[Continue with phases...]

---

## 📊 Progress Tracking

### Weekly Status
| Week | Planned | Completed | Blockers |
|------|---------|-----------|----------|
| 1    |         |           |          |
| 2    |         |           |          |

### Current Blockers
- [ ] [Blocker description] - Owner: [name]

---

## ⚠️ Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [L/M/H] | [L/M/H] | [Action] |

---

**Status**: 📋 PLANNING
**Next Action**: [Specific next step]
**Owner**: IT-Journey Team
**Review Schedule**: [frequency]
**Last Updated**: YYYY-MM-DD
```

### Quick Actions Template

```markdown
---
title: "[Category] Quick Actions"
description: "Immediate high-impact tasks for this week"
created: YYYY-MM-DDTHH:MM:SS.000Z
lastmod: YYYY-MM-DDTHH:MM:SS.000Z
status: "IN_PROGRESS"
priority: "HIGH"
category: "[category]"
---

# ⚡ Quick Actions

> **Time Investment**: [total estimate] | **Expected Impact**: [outcome]

## 🔴 Critical (Do Today)

### 1. [Task Name]
**File**: `path/to/file`
- [ ] [Specific action 1]
- [ ] [Specific action 2]
- [ ] [Specific action 3]
**Time**: [estimate] | **Impact**: [outcome]

---

## 🟠 High Priority (This Week)

### 2. [Task Name]
- [ ] [Action item]
- [ ] [Action item]
**Time**: [estimate]

### 3. [Task Name]
- [ ] [Action item]
**Time**: [estimate]

---

## 🟡 Medium Priority (Next Week)

### 4. [Task Name]
- [ ] [Action item]

---

## ✅ Completion Checklist

- [ ] All critical tasks completed
- [ ] High priority tasks completed
- [ ] Status updated in main tracking
- [ ] Next week's priorities identified

---

**Next Action**: [Start with task X]
**Last Updated**: YYYY-MM-DD
```

## 🔍 AI Validation Checks

### Pre-Creation Validation

Before creating TODO items, AI should verify:

```yaml
todo_validation:
  structure:
    - [ ] Frontmatter follows required format
    - [ ] Status is valid enum value
    - [ ] Priority is assigned appropriately
    - [ ] Category matches directory structure
    - [ ] Dependencies are listed if applicable
  
  content:
    - [ ] Title is action-oriented and clear
    - [ ] Description explains the "why"
    - [ ] Tasks are specific and measurable
    - [ ] Effort estimates are realistic
    - [ ] Success criteria are defined
  
  alignment:
    - [ ] Connects to roadmap goals
    - [ ] Doesn't duplicate existing TODOs
    - [ ] Priority matches project importance
    - [ ] Owner is assigned
```

### Status Update Validation

When updating TODO status, verify:

```yaml
status_transitions:
  PLANNING_to_IN_PROGRESS:
    - [ ] Action plan is defined
    - [ ] Resources are available
    - [ ] Dependencies are resolved
  
  IN_PROGRESS_to_REVIEW:
    - [ ] All tasks are marked complete
    - [ ] Deliverables are created
    - [ ] Tests/validation is done
  
  REVIEW_to_COMPLETE:
    - [ ] Human review is approved
    - [ ] Documentation is updated
    - [ ] Success metrics are measured
  
  COMPLETE_to_ARCHIVED:
    - [ ] Lessons learned documented
    - [ ] Files moved to ARCHIVE folder
    - [ ] References updated
```

## 🔗 Integration with IT-Journey Ecosystem

### Connecting TODOs to Project Documentation

```markdown
// When creating TODOs, reference:
// - roadmap.md for strategic alignment
// - PRD.md for product requirements
// - CONTRIBUTING.md for contribution guidelines
// - docs/ for technical standards
```

### Cross-Referencing Pattern

```markdown
<!-- In TODO files, use this pattern for cross-references -->

## Related Resources
- **Roadmap**: See [Phase X in roadmap](/roadmap/#phase-x) for strategic context
- **PRD**: Implements [Requirement Y](/PRD.md#section) 
- **Documentation**: Technical details in [docs/topic/](/docs/topic/)
- **Quest**: Learning content at [quest-name](/quests/category/quest-name/)
```

### Status Dashboard Integration

The `STATUS.md` file should aggregate all active TODOs:

```markdown
# 📊 TODO Status Dashboard

> **Last Updated**: YYYY-MM-DD | **Active Projects**: X | **Completion Rate**: Y%

## 🔴 Critical Items
| Project | Task | Owner | Due | Status |
|---------|------|-------|-----|--------|
| [Project] | [Task] | [Name] | [Date] | 🔄 |

## 📈 Project Status Summary
| Project | Progress | Priority | Next Milestone |
|---------|----------|----------|----------------|
| [SEO Optimization] | 25% | HIGH | Week 1 complete |
| [Content Gap] | 0% | MEDIUM | Planning |

## 🚧 Blockers
- [Blocker 1] - Assigned to [owner] - ETA: [date]

## ✅ Recently Completed
- [Project/Task] - Completed YYYY-MM-DD
```

## 📝 Best Practices for AI Agents

### DO ✅
- Break large tasks into smaller, actionable items
- Use specific file paths when tasks involve code/content changes
- Include effort estimates based on similar past work
- Set realistic priorities based on impact and urgency
- Update `lastmod` dates when modifying files
- Archive completed projects rather than deleting
- Connect TODOs to broader project goals

### DON'T ❌
- Create vague tasks like "improve SEO" without specifics
- Set everything as HIGH priority
- Leave tasks without effort estimates
- Forget to update status when work progresses
- Create duplicate TODOs for the same work
- Mix different project types in the same file
- Skip frontmatter in TODO files

### When to Escalate to Humans

AI should prompt for human input when:
- Priority decisions affect multiple stakeholders
- Resource allocation is needed
- Strategic direction is unclear
- Technical decisions require domain expertise
- Risks or blockers need management approval

## 🔄 Maintenance Schedule

### Daily (AI-Automated)
- Check for stale items (no update > 7 days)
- Identify blocked items
- Update completion percentages

### Weekly (AI-Assisted, Human Review)
- Review progress against milestones
- Reprioritize based on new information
- Update STATUS.md dashboard
- Archive completed items

### Monthly (Human-Led)
- Strategic alignment review
- Resource reallocation decisions
- Process improvement identification
- Archive old projects

---

**Version:** 1.0.0 | **Last Modified:** 2025-12-19 | **Author:** IT-Journey Team

**Related Files:**
- `README.md`: TODO directory hub
- `STATUS.md`: Real-time status dashboard
- `roadmap.md`: Project roadmap alignment
- `PRD.md`: Product requirements reference
- `.github/instructions/contributing.instructions.md`: General contribution guidelines

**Usage:** AI agents should reference these instructions when helping users create, organize, track, and complete TODO items. Focus on actionable, measurable tasks with clear priorities and realistic effort estimates.
