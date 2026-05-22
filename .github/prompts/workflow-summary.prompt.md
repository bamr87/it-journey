---
mode: agent
description: "Generate a comprehensive workflow execution summary with outputs and next steps"
date: 2025-11-22T16:10:21.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# Workflow Execution Summary

Generate a comprehensive summary of the workflow execution.

**Workflow**: {{ inputs.workflow_name }}
**Execution ID**: {{ inputs.execution_id }}

## Summary Requirements

1. **What Was Created**
   - Article title and location
   - Quest title and location
   - Supporting files

2. **Quality Metrics**
   - Validation scores
   - Improvements made
   - Final quality assessment

3. **Next Steps**
   - Manual review tasks
   - Testing recommendations
   - Publication checklist

4. **Files Created**
   - Complete list with paths
   - File sizes and line counts

## Output Format

Return a well-formatted summary suitable for README or documentation.
