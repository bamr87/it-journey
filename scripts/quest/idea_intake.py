#!/usr/bin/env python3
"""
idea_intake.py — the deterministic collector for the quest-idea intake lane.

Turns a "quest idea" GitHub issue (filed by the Quest Idea Forge portal at
/quests/ideas/ through the .github/ISSUE_TEMPLATE/quest-idea.yml issue form)
into a structured JSON *manifest*: the parsed fields, a readiness score against
a fixed rubric, conservative spam signals, and near-duplicate matches against
the published quest registry.

WHY THIS EXISTS — the gatekeeping floor.
The `idea-refiner` agent reviews portal submissions, but its verdict must never
be more generous than the deterministic signal: the manifest's verdict is a
ceiling the model may lower (e.g. declining a well-formed ad) and never raise.
Spam heuristics here are deliberately conservative — they exist to catch the
obvious (link dumps, keyboard mash, empty forms), not to judge ideas; judging
substance is the model's half of the lane.

The same rubric runs client-side in assets/js/quest-idea-portal.js so the
portal's live readiness meter and this collector agree. If you tune a point
value or threshold here, mirror it there.

Usage:
    # From a live issue (needs `gh` auth):
    python3 scripts/quest/idea_intake.py --issue 412 --json manifest.json

    # From a body on disk / stdin (CI passes the body through a file):
    gh issue view 412 --json body -q .body | python3 scripts/quest/idea_intake.py
    python3 scripts/quest/idea_intake.py --body-file issue.md

    # Self-check (no network, no gh): parses embedded fixtures and asserts.
    python3 scripts/quest/idea_intake.py --selftest

Unparseable sections degrade to empty values rather than failing — a missing
field simply earns no points and shows up in the checks list.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
NETWORK_JSON_DEFAULT = "assets/data/quest-network.json"

# Verdict thresholds — mirrored in assets/js/quest-idea-portal.js.
READY_THRESHOLD = 70

# The issue-form fields, matched by their rendered `### <label>` headings.
# GitHub renders an issue form as `### Label\n\n<value>` blocks and prints
# `_No response_` for skipped optional fields. Keys here are normalized heading
# prefixes (lowercased, punctuation stripped) → canonical field names, checked
# in order, first prefix match wins.
HEADING_MAP = [
    ("whats the quest idea", "summary"),
    ("why does it matter", "why"),
    ("learning objectives", "objectives"),
    ("character path", "path"),
    ("level", "level"),
    ("difficulty", "difficulty"),
    ("tools technologies", "technologies"),
    ("similar existing quests", "existing"),
]

FIELD_NAMES = [name for _, name in HEADING_MAP]

# Controlled vocabularies (subset of scripts/quest/quest_registry.py — kept
# inline so this collector stays import-free and runnable anywhere).
SKILL_FOCUS = [
    "frontend", "backend", "fullstack", "devops", "security",
    "data-engineering", "cloud", "infrastructure", "ai-ml",
]
DIFFICULTY_KEYS = ["easy", "medium", "hard", "epic"]

NO_RESPONSE = "_no response_"
URL_RE = re.compile(r"https?://\S+")
HEADING_RE = re.compile(r"^###\s+(?P<label>.+?)\s*$")
CODE_SPAN_RE = re.compile(r"`[^`\n]+`")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def _norm_heading(label: str) -> str:
    """Lowercase, drop everything but letters/digits/spaces, collapse spaces."""
    deapostrophed = label.lower().replace("'", "").replace("’", "")
    cleaned = re.sub(r"[^a-z0-9 ]+", " ", deapostrophed)
    return re.sub(r"\s+", " ", cleaned).strip()


def _field_for(label: str) -> Optional[str]:
    normed = _norm_heading(label)
    for prefix, name in HEADING_MAP:
        if normed.startswith(prefix):
            return name
    return None


def parse_fields(body: str) -> Dict[str, str]:
    """Split an issue-form body into its canonical fields, all treated as DATA.

    Only the form's own headings switch fields: a '###' line the user wrote
    inside a field (or inside a fenced code block) stays part of that field's
    value instead of silently truncating everything after it.
    """
    fields: Dict[str, str] = {name: "" for name in FIELD_NAMES}
    current: Optional[str] = None
    buf: List[str] = []
    in_fence = False

    def flush() -> None:
        if current is None:
            return
        value = "\n".join(buf).strip()
        if value.lower() == NO_RESPONSE:
            value = ""
        # First occurrence wins; a duplicated heading never overwrites.
        if not fields[current]:
            fields[current] = value

    for line in body.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            if current is not None:
                buf.append(line)
            continue
        m = None if in_fence else HEADING_RE.match(line)
        if m:
            name = _field_for(m.group("label"))
            if name is not None:
                flush()
                current = name
                buf = []
            elif current is not None:
                buf.append(line)   # user-written '###' inside a field value
        elif current is not None:
            buf.append(line)
    flush()
    return fields


def _title(body: str, fields: Dict[str, str], issue_title: str = "") -> str:
    cleaned = re.sub(r"^\s*quest idea:\s*", "", issue_title, flags=re.IGNORECASE).strip()
    if cleaned:
        return cleaned
    in_fence = False
    for line in body.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return (fields.get("summary") or "").splitlines()[0][:80] if fields.get("summary") else ""


def _objective_lines(raw: str) -> List[str]:
    """Non-empty objective lines with list markers stripped."""
    out = []
    for line in raw.splitlines():
        stripped = re.sub(r"^\s*(?:[-*+]|\d+[.)])?\s*(?:\[[ xX]\])?\s*", "", line).strip()
        if stripped:
            out.append(stripped)
    return out


def _tech_tokens(raw: str) -> List[str]:
    return [t.strip().lower() for t in re.split(r"[,;\n]+", raw) if t.strip()]


def _valid_level(raw: str) -> str:
    m = re.search(r"\b([01]{4})\b", raw or "")
    return m.group(1) if m else ""


def _valid_path(raw: str) -> str:
    lowered = (raw or "").strip().lower()
    return lowered if lowered in SKILL_FOCUS else ""


def _valid_difficulty(raw: str) -> str:
    lowered = (raw or "").lower()
    for key in DIFFICULTY_KEYS:
        if key in lowered:
            return key
    return ""


# --- Readiness rubric --------------------------------------------------------
# Point values mirrored in assets/js/quest-idea-portal.js — keep in sync.

def score(fields: Dict[str, str], known_techs: Optional[set] = None) -> Dict:
    summary = fields.get("summary", "")
    why = fields.get("why", "")
    objectives = _objective_lines(fields.get("objectives", ""))
    techs = _tech_tokens(fields.get("technologies", ""))
    prose = "\n".join([summary, fields.get("objectives", ""), why])

    # Tokenizer mirrored in assets/js/quest-idea-portal.js rubric(): plain
    # [a-z0-9]{3,} tokens for single-word techs, substring scan for vocab
    # entries carrying separators (github-actions, ai-ml, ...).
    specific = bool(CODE_SPAN_RE.search(prose))
    if not specific and known_techs:
        prose_lower = prose.lower()
        words = set(re.findall(r"[a-z0-9]{3,}", prose_lower))
        specific = bool(words & known_techs) or any(
            t in prose_lower for t in known_techs if re.search(r"[^a-z0-9]", t))

    checks = [
        {"id": "summary", "label": "Idea described (≥ 80 chars)",
         "points": 20, "earned": 20 if len(summary) >= 80 else 0},
        {"id": "summary_depth", "label": "Idea described in depth (≥ 200 chars)",
         "points": 5, "earned": 5 if len(summary) >= 200 else 0},
        {"id": "why", "label": "Outcome / why it matters (≥ 40 chars)",
         "points": 15, "earned": 15 if len(why) >= 40 else 0},
        {"id": "objectives", "label": "At least 2 learning objectives",
         "points": 15, "earned": 15 if len(objectives) >= 2 else 0},
        {"id": "objectives_depth", "label": "3+ learning objectives",
         "points": 5, "earned": 5 if len(objectives) >= 3 else 0},
        {"id": "path", "label": "Character path chosen",
         "points": 10, "earned": 10 if _valid_path(fields.get("path", "")) else 0},
        {"id": "level", "label": "Binary level chosen",
         "points": 5, "earned": 5 if _valid_level(fields.get("level", "")) else 0},
        {"id": "difficulty", "label": "Difficulty chosen",
         "points": 5, "earned": 5 if _valid_difficulty(fields.get("difficulty", "")) else 0},
        {"id": "technologies", "label": "Tools / technologies named",
         "points": 10, "earned": 10 if techs else 0},
        {"id": "specificity", "label": "Concrete tools or code mentioned in the prose",
         "points": 10, "earned": 10 if specific else 0},
    ]
    total = sum(c["earned"] for c in checks)
    return {"score": total, "max_score": sum(c["points"] for c in checks), "checks": checks}


# --- Spam signals (conservative on purpose) ----------------------------------

def spam_flags(body: str, fields: Dict[str, str]) -> Dict[str, bool]:
    content = "\n".join(fields.get(k, "") for k in ("summary", "why", "objectives"))
    urls = URL_RE.findall(body)
    url_chars = sum(len(u) for u in urls)
    alpha = [ch for ch in content.lower() if ch.isalpha()]

    flags = {
        "too_short": len(content.strip()) < 80,
        "link_spam": len(urls) >= 5 or (len(urls) >= 2 and url_chars > 0.4 * max(len(body), 1)),
        "low_diversity": len(alpha) >= 60 and len(set(alpha)) <= 6,
        "shouting": (
            len(content) >= 60
            and sum(1 for ch in content if ch.isupper()) > 0.7 * max(sum(1 for ch in content if ch.isalpha()), 1)
        ),
    }
    return flags


# --- Duplicate radar ----------------------------------------------------------

def load_network(path: Path) -> List[Dict]:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh).get("nodes", [])
    except (OSError, ValueError):
        return []


def find_duplicates(title: str, summary: str, nodes: List[Dict], limit: int = 3) -> List[Dict]:
    """Fuzzy-match the idea against published quest titles."""
    probe = f"{title} {summary[:160]}".lower()
    if not probe.strip():
        return []
    scored = []
    for node in nodes:
        node_title = str(node.get("title") or "")
        ratio = difflib.SequenceMatcher(None, title.lower(), node_title.lower()).ratio()
        tokens_a = set(re.findall(r"[a-z0-9]{3,}", probe))
        tokens_b = set(re.findall(r"[a-z0-9]{3,}", node_title.lower()))
        overlap = len(tokens_a & tokens_b) / len(tokens_b) if tokens_b else 0.0
        best = max(ratio, overlap)
        if best >= 0.55:
            scored.append({
                "title": node_title,
                "permalink": node.get("id", ""),
                "level": node.get("level", ""),
                "similarity": round(best, 2),
            })
    scored.sort(key=lambda d: -d["similarity"])
    return scored[:limit]


# --- Manifest -----------------------------------------------------------------

def collect(body: str, network_path: Path, issue_title: str = "") -> Dict:
    fields = parse_fields(body)
    nodes = load_network(network_path)
    known_techs = set()
    for node in nodes:
        tech = node.get("technology")
        for item in (tech if isinstance(tech, list) else [tech]):
            if item:
                known_techs.add(str(item).lower())

    title = _title(body, fields, issue_title)
    rubric = score(fields, known_techs)
    flags = spam_flags(body, fields)
    spam = any(flags.values())

    if spam:
        verdict = "spam_suspect"
    elif rubric["score"] >= READY_THRESHOLD:
        verdict = "ready"
    else:
        verdict = "needs_detail"

    return {
        "title": title,
        "fields": fields,
        "normalized": {
            "path": _valid_path(fields.get("path", "")),
            "level": _valid_level(fields.get("level", "")),
            "difficulty": _valid_difficulty(fields.get("difficulty", "")),
            "objectives": _objective_lines(fields.get("objectives", "")),
            "technologies": _tech_tokens(fields.get("technologies", "")),
        },
        "readiness": {**rubric, "threshold": READY_THRESHOLD},
        "flags": flags,
        "duplicates": find_duplicates(title, fields.get("summary", ""), nodes),
        "verdict": verdict,
        "stats": {
            "field_count": sum(1 for v in fields.values() if v),
            "network_nodes": len(nodes),
        },
    }


def _read_body(args) -> tuple:
    """Return (issue_title, body). gh's stderr flows through to the caller's log."""
    if args.issue:
        repo = ["--repo", args.repo] if args.repo else []
        out = subprocess.run(
            ["gh", "issue", "view", str(args.issue), *repo, "--json", "title,body"],
            stdout=subprocess.PIPE, text=True, check=True,
        )
        data = json.loads(out.stdout)
        return str(data.get("title") or ""), str(data.get("body") or "")
    if args.body_file:
        with open(args.body_file, encoding="utf-8") as fh:
            return "", fh.read()
    return "", sys.stdin.read()


_FIXTURE_READY = """### What's the quest idea?

Build a self-healing uptime monitor for a personal site: a GitHub Actions cron
pings the site, and on failure it opens an issue, rolls back the last deploy
with `git revert`, and posts the incident timeline. Learners wire the whole
loop themselves and watch it catch a real (staged) outage.

### Why does it matter?

It turns "CI/CD" from a buzzword into an operational reflex — learners feel an
outage end-to-end and ship the automation that ends it.

### Learning objectives

- Schedule a GitHub Actions cron workflow and read its logs
- Trigger a rollback with `git revert` from a workflow
- Open and label an incident issue automatically

### Character path (skill focus)

devops

### Level (binary progression)

0101

### Difficulty

🟡 Medium

### Tools & technologies

github-actions, bash, git

### Similar existing quests you checked

_No response_
"""

_FIXTURE_THIN = """### What's the quest idea?

make a quest about docker

### Why does it matter?

_No response_

### Learning objectives

_No response_

### Character path (skill focus)

Not sure

### Level (binary progression)

Not sure yet

### Difficulty

Not sure

### Tools & technologies

_No response_

### Similar existing quests you checked

_No response_
"""


def _selftest() -> int:
    ready = collect(_FIXTURE_READY, REPO_ROOT / "does-not-exist.json")
    assert ready["verdict"] == "ready", (ready["verdict"], ready["readiness"]["score"])
    assert ready["readiness"]["score"] >= READY_THRESHOLD
    assert ready["normalized"]["path"] == "devops"
    assert ready["normalized"]["level"] == "0101"
    assert ready["normalized"]["difficulty"] == "medium"
    assert len(ready["normalized"]["objectives"]) == 3
    assert not any(ready["flags"].values()), ready["flags"]

    thin = collect(_FIXTURE_THIN, REPO_ROOT / "does-not-exist.json")
    assert thin["verdict"] == "spam_suspect", thin["verdict"]  # too_short catches it
    assert thin["flags"]["too_short"]
    assert thin["readiness"]["score"] < READY_THRESHOLD

    print("idea_intake.py selftest: OK")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Collect a quest-idea issue into a structured manifest.")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--issue", type=int, help="issue number (read via gh)")
    src.add_argument("--body-file", help="path to the issue body markdown (else stdin)")
    ap.add_argument("--repo", help="owner/name for gh (default: current repo)")
    ap.add_argument("--network", default=str(REPO_ROOT / NETWORK_JSON_DEFAULT),
                    help="quest-network.json for duplicate detection")
    ap.add_argument("--json", dest="json_out", help="write manifest JSON here (default stdout)")
    ap.add_argument("--selftest", action="store_true", help="parse embedded fixtures and assert")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    issue_title, body = _read_body(args)
    manifest = collect(body, Path(args.network), issue_title=issue_title)
    text = json.dumps(manifest, indent=2, ensure_ascii=False)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"wrote {args.json_out}: verdict={manifest['verdict']} "
              f"score={manifest['readiness']['score']}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
