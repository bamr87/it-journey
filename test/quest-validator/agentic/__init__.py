"""
Agentic quest validation (tier 2).

The structural validator (``quest_validator.py``, tier 1) checks that a quest is
*shaped* correctly — frontmatter, sections, taxonomy, Liquid safety. This package
adds a second tier: it drives **Claude Code** (authenticated via OAuth) to actually
read a quest, attempt its commands end-to-end in an isolated sandbox, judge the
content/accuracy/clarity, and return a weighted score plus prioritized
recommendations.

Public surface:
    schema   — verdict JSON Schema + deterministic scoring
    prompts  — system/user prompt construction
    loader   — quest discovery + frontmatter parsing (reuses quest_registry)
    runner   — Claude Code invocation, sandboxing, output parsing (+ mock/dry-run)
    report   — aggregation + console/markdown/json rendering
"""

__all__ = ["schema", "prompts", "loader", "runner", "report"]
