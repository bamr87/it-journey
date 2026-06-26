"""
Verdict schema + deterministic scoring for the agentic quest validator.

The agent returns a structured *verdict* (one JSON object). To keep results
reproducible and tamper-resistant, the **overall score is computed in Python**
from the per-dimension scores the agent assigns — we never trust the model's own
arithmetic. The model supplies 0-5 scores + evidence per dimension; we apply the
fixed weights below.
"""

from __future__ import annotations

# (key, label, weight, guidance). Weights sum to 1.0.
DIMENSIONS = [
    ("commands_work",    "Commands & code work",    0.30,
     "Runnable commands, snippets, and config in the quest execute and behave as described."),
    ("content_accuracy", "Technical accuracy",      0.25,
     "Claims, versions, flags, APIs, and explanations are correct and current."),
    ("completeness",     "Completeness",            0.15,
     "The quest delivers on its stated objectives / learning outcomes; no critical gaps."),
    ("clarity",          "Clarity & followability", 0.15,
     "Steps are unambiguous, correctly ordered, and a learner could actually follow them."),
    ("structure",        "Structure & pedagogy",    0.05,
     "Logical flow; prerequisites, validation criteria, and rewards are coherent."),
    ("safety",           "Safety",                  0.10,
     "No destructive or dangerous commands without a clear, prominent warning."),
]

DIM_KEYS = [d[0] for d in DIMENSIONS]
DIM_LABELS = {d[0]: d[1] for d in DIMENSIONS}
WEIGHTS = {d[0]: d[2] for d in DIMENSIONS}
DIM_GUIDANCE = {d[0]: d[3] for d in DIMENSIONS}
MAX_DIM = 5  # each dimension scored 0..5

# Verdict schema version. Bump when DIMENSIONS / weights / the JSON shape change
# so persisted reports and the envelope contract test can detect a mismatch.
SCHEMA_VERSION = "1.0.0"

VERDICT_PASS, VERDICT_WARN, VERDICT_FAIL = "pass", "warn", "fail"
VERDICT_EMOJI = {VERDICT_PASS: "✅", VERDICT_WARN: "⚠️", VERDICT_FAIL: "❌"}

# Default verdict bands (overall %). Configurable from the CLI.
DEFAULT_PASS_THRESHOLD = 80
DEFAULT_WARN_THRESHOLD = 60


def build_json_schema() -> dict:
    """JSON Schema passed to ``claude --json-schema`` AND mirrored in the prompt."""
    dim_props = {}
    for key, label, _weight, guidance in DIMENSIONS:
        dim_props[key] = {
            "type": "object",
            "additionalProperties": False,
            "required": ["score", "findings"],
            "properties": {
                "score": {
                    "type": "integer", "minimum": 0, "maximum": MAX_DIM,
                    "description": f"{label} — {guidance} 0 = broken/absent, 3 = adequate, 5 = excellent.",
                },
                "findings": {
                    "type": "array", "items": {"type": "string"},
                    "description": "Concrete, specific observations that justify the score (quote the quest).",
                },
            },
        }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["executed", "dimensions", "commands", "recommendations", "summary"],
        "properties": {
            "executed": {
                "type": "boolean",
                "description": "True if you actually RAN commands in the sandbox; false if you only reasoned statically.",
            },
            "dimensions": {
                "type": "object",
                "additionalProperties": False,
                "required": DIM_KEYS,
                "properties": dim_props,
            },
            "commands": {
                "type": "array",
                "description": "Every concrete command / code snippet you evaluated, in quest order.",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["command", "status"],
                    "properties": {
                        "command": {"type": "string", "description": "The command or a short label for the snippet."},
                        "status": {
                            "type": "string",
                            "enum": ["passed", "failed", "skipped", "reasoned"],
                            "description": "passed/failed = actually run; skipped = unsafe/irrelevant; reasoned = judged statically.",
                        },
                        "detail": {"type": "string", "description": "What happened, or why it failed / was skipped."},
                    },
                },
            },
            "recommendations": {
                "type": "array",
                "description": "Prioritized, actionable fixes. Empty array if the quest is excellent.",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["priority", "area", "suggestion"],
                    "properties": {
                        "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                        "area": {"type": "string", "description": "Which part of the quest (section / command / claim)."},
                        "suggestion": {"type": "string", "description": "A concrete change the author should make."},
                    },
                },
            },
            "summary": {"type": "string", "description": "1-3 sentence overall assessment for the author."},
        },
    }


def _clamp_int(val, lo, hi):
    try:
        v = int(round(float(val)))
    except (TypeError, ValueError):
        return None
    return max(lo, min(hi, v))


def score_verdict(verdict: dict) -> dict:
    """Compute the weighted overall score (0-100) from per-dimension scores.

    Missing/invalid dimension scores are treated as absent and dropped from the
    weighted average (so a partial verdict still yields a meaningful number),
    with the dimension reported as ``None``.
    """
    dims = verdict.get("dimensions") or {}
    per: dict = {}
    acc = 0.0
    total_w = 0.0
    for key in DIM_KEYS:
        raw = dims.get(key) or {}
        s = _clamp_int(raw.get("score"), 0, MAX_DIM)
        per[key] = s
        if s is not None:
            acc += WEIGHTS[key] * (s / MAX_DIM)
            total_w += WEIGHTS[key]
    overall = round((acc / total_w) * 100, 1) if total_w else 0.0
    return {"overall": overall, "per_dimension": per, "weight_covered": round(total_w, 3)}


def verdict_label(overall: float,
                  pass_threshold: int = DEFAULT_PASS_THRESHOLD,
                  warn_threshold: int = DEFAULT_WARN_THRESHOLD) -> str:
    if overall >= pass_threshold:
        return VERDICT_PASS
    if overall >= warn_threshold:
        return VERDICT_WARN
    return VERDICT_FAIL
