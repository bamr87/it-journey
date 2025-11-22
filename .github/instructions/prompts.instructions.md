---
applyTo: '**/prompts/**/*.md'
---

# Prompt Engineering Instructions with Kaizen Integration

These instructions guide VS Code Copilot and AI agents in applying Kaizen (continuous improvement) principles to prompt engineering for optimal AI communication and development workflows.

## 🎯 Core Philosophy

**Prompt Engineering** is the systematic process of designing, refining, and optimizing instructions for AI language models to produce desired outputs.

**Kaizen Integration** means treating every prompt as an opportunity for continuous improvement through the PDCA cycle:
- **Plan**: Define success criteria before writing prompts
- **Do**: Implement prompt with structured components
- **Check**: Measure output quality against criteria
- **Act**: Refine based on observations and iterate

## 🔄 PDCA Cycle for Prompt Development

### Phase 1: PLAN - Define Success Before Prompting

Before writing any prompt, establish:

**1. Clear Objective**
```markdown
What specific outcome do I need from this prompt?

Example:
❌ Bad: "I need code help"
✅ Good: "Generate a Python function that validates email addresses 
using regex, handles edge cases (empty, special chars), and returns 
boolean with error message"
```

**2. Success Criteria**
```markdown
How will I know the output is successful?

Criteria types:
- Functional: Does it work correctly?
- Format: Is it structured as requested?
- Quality: Is it clear, efficient, maintainable?
- Completeness: Does it address all requirements?

Example:
For code generation:
✅ Compiles/runs without errors
✅ Handles specified edge cases
✅ Includes docstring with examples
✅ Follows project style guide
✅ < 20 lines (complexity constraint)
```

**3. Baseline Measurement**
```markdown
What's the current state or previous attempt?

Document:
- Previous prompt (if iterating)
- Previous output quality (rating 1-10)
- Specific issues encountered
- What worked well (keep)
- What needs improvement (change)
```

### Phase 2: DO - Implement Structured Prompt

Apply proven prompt engineering patterns:

#### **Pattern 1: Role-Context-Task-Format (RCTF)**

```markdown
[ROLE]
You are a [specific expert role with relevant experience].

[CONTEXT]
The user is [situation and background information].
Current state: [what exists now]
Goal: [what we're trying to achieve]

[TASK]
Your task is to [specific, actionable request].

[CONSTRAINTS]
- Constraint 1 (e.g., "Must use Python 3.8+")
- Constraint 2 (e.g., "Maximum 50 lines")
- Constraint 3 (e.g., "Include error handling")

[OUTPUT FORMAT]
Structure your response as:
1. [Section 1 description]
2. [Section 2 description]
3. [Section 3 description]

[EXAMPLES] (if using few-shot)
Example Input: [sample]
Example Output: [sample]
```

**Example Application**:
```markdown
[ROLE]
You are a senior Python developer specializing in data validation 
and security best practices.

[CONTEXT]
The user is building a web API that processes user registration data.
Current state: Basic validation exists but misses edge cases.
Goal: Robust email validation that prevents injection attacks.

[TASK]
Write a Python function that validates email addresses with:
- Regex pattern matching RFC 5322 standard
- Sanitization of special characters
- Length limits (max 254 chars)
- Prevention of SQL injection patterns

[CONSTRAINTS]
- Python 3.8+ with no external libraries
- Return tuple: (is_valid: bool, error_message: str or None)
- Include comprehensive docstring
- Maximum 30 lines

[OUTPUT FORMAT]
1. Function implementation with type hints
2. Docstring with 3 usage examples
3. Brief explanation of security considerations
```

#### **Pattern 2: Chain-of-Thought (CoT) with Verification**

```markdown
Problem: [State the problem clearly]

Approach this step-by-step:
1. [Break down the problem]
2. [Identify key considerations]
3. [Propose solution]
4. [Verify solution addresses requirements]

For each step, explain your reasoning.

After generating the solution, verify:
- Does it meet requirement X?
- Does it handle edge case Y?
- Are there any potential issues?
```

#### **Pattern 3: Few-Shot with Quality Examples**

```markdown
I'll show you the pattern I want:

Example 1 (Simple case):
Input: [simple input]
Output: [high-quality output showing pattern]

Example 2 (Edge case):
Input: [edge case input]
Output: [how to handle edge case]

Example 3 (Complex case):
Input: [complex input]
Output: [complex output demonstrating full pattern]

Now apply this pattern to:
Input: [your actual input]
```

**Example Selection Criteria**:
- **Diversity**: Cover different scenarios (simple, edge, complex)
- **Balance**: Equal representation if classification task
- **Clarity**: Pattern should be obvious
- **Relevance**: Similar to actual use case
- **Quality**: Demonstrate best practices, not minimal solutions

### Phase 3: CHECK - Measure Output Quality

Evaluate the AI's output against your success criteria:

#### **Quality Assessment Framework**

```markdown
Category 1: Functional Correctness
- [ ] Produces expected result for normal inputs (Y/N)
- [ ] Handles edge cases appropriately (Y/N)
- [ ] Free of bugs or logical errors (Y/N)
- [ ] Score: [0-10]

Category 2: Format Compliance
- [ ] Follows requested structure (Y/N)
- [ ] Includes all required sections (Y/N)
- [ ] Uses specified syntax/language (Y/N)
- [ ] Score: [0-10]

Category 3: Quality & Best Practices
- [ ] Clear, readable, well-documented (Y/N)
- [ ] Efficient and maintainable (Y/N)
- [ ] Follows project conventions (Y/N)
- [ ] Score: [0-10]

Category 4: Completeness
- [ ] Addresses all requirements (Y/N)
- [ ] Provides sufficient context/explanation (Y/N)
- [ ] Includes examples if requested (Y/N)
- [ ] Score: [0-10]

Overall Score: [Average] / 10
```

#### **Failure Mode Analysis**

When output quality is insufficient, diagnose:

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| Vague output | Prompt too general | Add specificity, constraints |
| Wrong format | Unclear formatting instruction | Use explicit template |
| Missing edge cases | Insufficient examples | Add few-shot examples for edges |
| Hallucination | Lacking verification | Add "cite sources" or "if unsure, say so" |
| Inconsistent quality | Prompt ambiguity | Remove ambiguity, add structure |
| Too complex | Trying to do too much | Break into smaller prompts |

### Phase 4: ACT - Refine and Standardize

Based on measurement, take action:

#### **Iteration Protocol**

```markdown
Current Prompt Version: [X]
Overall Score: [Y/10]

Issues Identified:
1. [Specific issue 1] - Impact: [High/Medium/Low]
2. [Specific issue 2] - Impact: [High/Medium/Low]

Improvement Hypothesis:
- Change: [What will I modify?]
- Reason: [Why will this help?]
- Expected improvement: [What score increase?]

New Prompt Version: [X+1]
[Modified prompt here]

Test Results:
- New score: [Z/10]
- Improvement: [+/- points]
- Decision: [Keep change / Revert / Modify further]
```

**Example Iteration Log**:
```markdown
## Iteration 1 (Baseline)
Prompt: "Write a function to validate emails"
Score: 3/10
Issues:
- Too vague, got minimal implementation
- No error handling
- No edge cases covered

## Iteration 2 (Add Structure)
Change: Added RCTF pattern with role, context, constraints
New Prompt: [ROLE: senior dev] [TASK: validate email with regex...]
Score: 7/10
Improvement: +4 points
Issues remaining:
- Still missing some edge cases
- Security considerations not mentioned

## Iteration 3 (Add Examples)
Change: Added 3 few-shot examples showing edge case handling
Score: 9/10
Improvement: +2 points
Issues remaining:
- Minor: Could add more inline comments

Decision: Keep this version, document as reusable template
```

#### **Template Creation**

When a prompt consistently achieves high scores, templatize it:

```markdown
## Template: [Name]

**Use Case**: [When to use this template]

**Success Rate**: [X/10 based on Y tests]

**Structure**:
[ROLE]
You are a [PLACEHOLDER: role description]

[CONTEXT]
[PLACEHOLDER: background information]

[TASK]
[PLACEHOLDER: specific action to perform]

[CONSTRAINTS]
- [PLACEHOLDER: constraint 1]
- [PLACEHOLDER: constraint 2]

[OUTPUT FORMAT]
[PLACEHOLDER: desired output structure]

**Example Instantiation**:
[Filled-in version for reference]

**Known Issues**:
- [Any limitations or failure modes observed]
```

## 🛠️ Prompt Engineering Techniques Reference

### Zero-Shot Prompting
**When to Use**: Simple, standard tasks with clear requirements.
**Pattern**:
```
Task: [Clear, specific instruction]
Context: [Any necessary background]
Requirements: [What the output must include]
```

**Kaizen Checkpoint**:
- Measure: Does output quality meet threshold without examples?
- If no: Switch to few-shot
- If yes: Document and reuse pattern

### Few-Shot Prompting
**When to Use**: Custom formats, domain-specific patterns, quality inconsistency.
**Pattern**:
```
[Instruction introducing the pattern]

Example 1: [Input] → [Desired output]
Example 2: [Input] → [Desired output]
Example 3: [Input] → [Desired output]

Now apply to: [Your input]
```

**Kaizen Checkpoint**:
- Measure: Test with 3-5 examples
- Track: Which example count gives best quality/token ratio?
- Optimize: Remove redundant examples, add clarifying ones

### Chain-of-Thought (CoT)
**When to Use**: Multi-step reasoning, complex logic, debugging.
**Pattern**:
```
Problem: [State clearly]

Let's solve step-by-step:
1. [First logical step]
2. [Second step]
3. [Final step]

Solution: [Answer]
```

**Kaizen Checkpoint**:
- Measure: Are intermediate steps correct?
- Verify: Does reasoning lead to right conclusion?
- Improve: Add verification step: "Check if this solution addresses [X]"

### ReAct (Reason + Act)
**When to Use**: Tasks requiring external tools, research, multi-step actions.
**Pattern**:
```
You can use these tools: [tool1, tool2, tool3]

For each step:
Thought: [What to do next and why]
Action: [tool_name(parameters)]
Observation: [Tool result]

Repeat until task is complete.
```

**Kaizen Checkpoint**:
- Measure: Track tool usage efficiency
- Optimize: Are actions redundant? Can steps combine?

### Self-Consistency
**When to Use**: High-stakes decisions, ambiguous problems.
**Pattern**:
```
Generate 3 different solutions using different reasoning approaches:

Approach 1: [Method 1]
Solution 1: [Answer]

Approach 2: [Method 2]
Solution 2: [Answer]

Approach 3: [Method 3]
Solution 3: [Answer]

Compare and select the most robust solution with justification.
```

**Kaizen Checkpoint**:
- Measure: Do multiple paths converge on same answer?
- If yes: High confidence
- If no: Examine disagreements, refine problem statement

## 📊 Measurement & Metrics

### Prompt Quality Metrics

**1. Output Quality Score (0-10 scale)**
- Correctness: Does it work?
- Completeness: Addresses all requirements?
- Clarity: Easy to understand?
- Efficiency: Optimal solution?

**2. Consistency Score**
```
Run same prompt 5 times
Count how many produce acceptable output
Consistency = (acceptable_outputs / total_runs) * 100%

Target: >80% for production prompts
```

**3. Iteration Count**
```
Track: How many PDCA cycles to achieve target quality?

Benchmark:
- Simple tasks: 1-2 iterations
- Medium complexity: 3-5 iterations
- Complex tasks: 5-10 iterations

If > 10 iterations: Break task into smaller prompts
```

**4. Token Efficiency**
```
Calculate: output_quality / token_count

Optimize:
- Remove unnecessary verbosity
- Use few-shot only when zero-shot fails
- Compress context without losing clarity
```

### Tracking Template

```markdown
## Prompt Performance Log

Date: [YYYY-MM-DD]
Prompt ID: [unique identifier]
Task: [brief description]

| Iteration | Changes Made | Quality Score | Consistency % | Token Count | Notes |
|-----------|-------------|---------------|---------------|-------------|-------|
| 1 (Baseline) | Initial prompt | 4/10 | 60% | 150 | Too vague |
| 2 | Added RCTF structure | 7/10 | 80% | 200 | Better clarity |
| 3 | Added 3 examples | 9/10 | 90% | 350 | Good, consider token cost |

Final Decision: Use iteration 2 for most cases, iteration 3 for critical tasks

Template Created: [Yes/No]
Template Location: [path if yes]
```

## 🚫 Seven Wastes in Prompt Engineering

Apply Kaizen's waste elimination to prompts:

### 1. **Overproduction** - Prompts that generate more than needed
**Example**: Asking for "comprehensive analysis" when summary suffices
**Fix**: Be specific about scope: "Provide 3 key insights, 2 sentences each"

### 2. **Waiting** - Prompts requiring multiple rounds due to ambiguity
**Example**: Vague prompt → clarification needed → re-prompt
**Fix**: Front-load context and requirements in initial prompt

### 3. **Transportation** - Excessive copy-paste between prompts
**Example**: Manually reformatting each output
**Fix**: Specify output format in prompt: "Format as JSON with keys: [list]"

### 4. **Over-Processing** - Unnecessarily complex prompts
**Example**: 500-word prompt for simple task
**Fix**: Simplify: Use zero-shot for standard tasks, few-shot only when needed

### 5. **Inventory** - Unused prompt variations stockpiled
**Example**: 20 similar prompts, unclear which works best
**Fix**: Document best performing prompt, archive others

### 6. **Motion** - Inefficient prompt refinement process
**Example**: Random changes without measurement
**Fix**: Use PDCA cycle, change one thing at a time

### 7. **Defects** - Low-quality outputs requiring rework
**Example**: Generic response doesn't meet requirements
**Fix**: Add verification step: "Before responding, verify you've addressed [X, Y, Z]"

## 🎯 VS Code Copilot Integration

### Copilot Chat Prompt Best Practices

**Pattern for Code Generation**:
```
@workspace I need help with [specific task]

Context:
- File: [which file]
- Purpose: [what this code does]
- Constraints: [language version, style requirements]

Please:
1. [Specific request with clear acceptance criteria]
2. Include type hints/JSDoc
3. Add error handling for [specific edge cases]
4. Follow [project style guide]

Format output as ready-to-use code with brief explanation.
```

**Pattern for Debugging**:
```
@workspace This code in [file:line] is [specific problem]

Expected behavior: [what should happen]
Actual behavior: [what's happening]
Error message: [if any]

Please:
1. Analyze step-by-step
2. Identify root cause
3. Provide fix with explanation
4. Suggest prevention for future
```

**Pattern for Refactoring**:
```
@workspace Refactor this code to [specific improvement goal]

Current code: [selection or file reference]

Requirements:
- Maintain existing functionality
- Improve [specific aspect: performance/readability/maintainability]
- Follow [design pattern or principle]
- Add tests if missing

Explain trade-offs of your approach.
```

### Copilot Inline Suggestions

**Trigger Better Suggestions**:
```python
# BAD: Vague comment
# function to validate

# GOOD: Specific, structured comment
def validate_email(email: str) -> tuple[bool, str | None]:
    """
    Validate email address against RFC 5322 standard.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        error_message is None if valid
        
    Handles:
        - Invalid format
        - Missing @ symbol
        - Invalid domain
        - Length > 254 chars
    """
    # Implementation (Copilot will suggest better based on detailed docstring)
```

### Quality Gates for AI-Generated Code

Before accepting Copilot suggestions:
- [ ] **Verify correctness**: Does it work as intended?
- [ ] **Check security**: Any injection vulnerabilities?
- [ ] **Review efficiency**: Is there a better approach?
- [ ] **Assess maintainability**: Will others understand it?
- [ ] **Validate style**: Matches project conventions?

## 📚 Reusable Prompt Templates Library

### Template: Code Review
```markdown
You are an experienced [LANGUAGE] developer conducting code review.

Review this code for:
1. Correctness: Logic errors, bugs, edge cases
2. Security: Injection risks, auth issues, data leaks
3. Performance: Algorithmic complexity, bottlenecks
4. Maintainability: Readability, documentation, design

Code:
[CODE HERE]

For each issue, provide:
- Line number
- Severity (Critical/High/Medium/Low)
- Description
- Specific fix (code example)
```

### Template: Documentation Generation
```markdown
Generate clear, comprehensive documentation for:

[CODE/API/MODULE HERE]

Include:
1. Overview: What it does and why it exists
2. Usage: Code examples for common scenarios
3. Parameters/Arguments: Type, purpose, constraints
4. Return values: Type, possible values, errors
5. Examples: 3 practical use cases
6. Edge cases: Known limitations or gotchas

Format as [Markdown/JSDoc/docstring]
Target audience: [developers/end-users/etc]
```

### Template: Test Case Generation
```markdown
Generate test cases for this [function/class/module]:

[CODE HERE]

Cover:
1. Happy path (normal inputs → expected outputs)
2. Edge cases (boundary values, empty inputs)
3. Error cases (invalid inputs, exceptions)
4. Integration scenarios (interaction with dependencies)

For each test:
- Descriptive name (test_feature_when_condition_then_outcome)
- Setup (given)
- Action (when)
- Assertion (then)

Framework: [pytest/jest/unittest/etc]
```

### Template: Debugging Assistant
```markdown
Help debug this issue:

**Problem**: [Specific error or unexpected behavior]

**Context**:
- Language/Framework: [details]
- Environment: [OS, versions]
- Error message: [full error]

**Code**:
[RELEVANT CODE SNIPPET]

**Expected**: [What should happen]
**Actual**: [What is happening]

Please:
1. Analyze step-by-step
2. Identify root cause
3. Provide fix with explanation
4. Suggest how to prevent similar issues
```

## 🔄 Continuous Improvement Protocol

### Daily Practice
- [ ] Write 3-5 prompts with clear success criteria
- [ ] Measure output quality (use 0-10 scale)
- [ ] Apply PDCA to 1 underperforming prompt
- [ ] Document 1 learning or pattern observed

### Weekly Review
- [ ] Review all prompts from the week
- [ ] Identify top 3 performing patterns
- [ ] Create/update templates for reuse
- [ ] Track improvement metrics (avg quality score trend)

### Monthly Optimization
- [ ] Audit prompt template library
- [ ] Remove unused/low-performing templates
- [ ] Consolidate similar patterns
- [ ] Share top patterns with team
- [ ] Analyze token usage trends, optimize costs

### Blameless Post-Mortem for Prompt Failures

When a critical prompt produces poor results:

```markdown
## Prompt Failure Analysis

Date: [YYYY-MM-DD]
Prompt: [The prompt that failed]
Context: [What was it trying to achieve]

**Timeline**:
- [Time] Prompt sent
- [Time] Output received
- [Time] Issue identified

**What Happened**:
[Factual description of failure]

**Impact**:
- Severity: [Critical/High/Medium/Low]
- Scope: [Who/what was affected]
- Duration: [How long to fix]

**Root Cause Analysis** (5 Whys):
1. Why did the prompt fail? [Answer]
2. Why [answer from 1]? [Answer]
3. Why [answer from 2]? [Answer]
4. Why [answer from 3]? [Answer]
5. Why [answer from 4]? [Root cause]

**Contributing Factors**:
- [Factor 1]
- [Factor 2]

**What Went Well**:
- [Positive aspect 1]
- [Positive aspect 2]

**Action Items**:
- [ ] Immediate fix: [What]
- [ ] Process improvement: [What]
- [ ] Documentation update: [Where]
- [ ] Template update: [Which]

**Prevention**:
How to avoid this in future:
- [Prevention strategy 1]
- [Prevention strategy 2]
```

---

## 🎓 Prompt Engineering Kaizen Checklist

Use this checklist for every significant prompt:

### Before Writing (PLAN)
- [ ] Defined clear, measurable success criteria
- [ ] Identified appropriate prompt technique (zero-shot, few-shot, CoT, etc.)
- [ ] Documented baseline (if iterating on existing prompt)
- [ ] Estimated token budget
- [ ] Identified potential failure modes

### While Writing (DO)
- [ ] Used structured format (RCTF or similar)
- [ ] Included specific constraints and requirements
- [ ] Added examples if using few-shot (3-5, diverse, balanced)
- [ ] Specified output format explicitly
- [ ] Included verification/error handling instructions

### After Response (CHECK)
- [ ] Tested output against success criteria
- [ ] Scored quality (0-10 scale)
- [ ] Ran consistency check (same prompt multiple times)
- [ ] Identified specific issues or improvements
- [ ] Documented what worked well

### Refining (ACT)
- [ ] Made targeted improvement based on measurement
- [ ] Re-tested and compared to previous version
- [ ] Decided: keep, revert, or iterate further
- [ ] Updated template library if high-performing
- [ ] Shared learnings with team

### Long-term
- [ ] Tracked metrics over time (quality trend, consistency, token efficiency)
- [ ] Eliminated wasteful patterns
- [ ] Created reusable templates
- [ ] Conducted periodic reviews and optimizations

---

*Remember: Prompt engineering is both an art and a science. The art comes from creativity and intuition. The science comes from Kaizen—systematic measurement, continuous improvement, and data-driven decisions. Master both to become a true Prompt Crystal Forger.*

---

## 📖 Additional Resources

- **IT-Journey Kaizen Quest**: Complete guide to applying Kaizen in software development
- **Kaizen Agent Protocol**: Full PDCA framework for AI-assisted development
- **Quest Instructions**: Standards for educational content creation
- **VS Code Copilot Documentation**: Official integration guidelines

---

**Version:** 1.0.0 | **Last Modified:** 2025-01-27 | **Author:** IT-Journey Team

**Usage:** Kaizen-based prompt engineering instructions for VS Code Copilot and AI agent development. Combines prompt engineering techniques with Kaizen methodology for systematic prompt optimization and continuous improvement.
