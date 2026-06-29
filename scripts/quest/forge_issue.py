#!/usr/bin/env python3
"""
forge_issue.py — the deterministic collector for the quest-forge pipeline.

Turns a "quest-forge proposal" GitHub issue (the kind lifehacker.dev's quest-forge
hook files into it-journey — see issue #365) into a structured JSON *manifest*:
the chapters, the build ledger (PR numbers + squash-merge SHAs), and the badges.

WHY THIS EXISTS — the honesty anchor.
The `quest-forge` agent authors gamified quest prose, but it must NEVER invent a
PR number or a commit hash. So it does not read the freeform issue and guess; it
runs this parser and quotes ONLY what the parser extracted. Every `#42` and every
`5853ef43b` in a generated quest is traceable to a row this collector found in the
issue body. This mirrors the producer side in lifehacker.dev
(`scripts/retro/collect_merged.rb`): a deterministic collector on both ends, with
the model only ever doing the creative wrapping in between.

Usage:
    # From a live issue (needs `gh` auth):
    python3 scripts/quest/forge_issue.py --issue 365 --json manifest.json

    # From a body on disk / stdin (CI passes the body through a file):
    gh issue view 365 --json body -q .body | python3 scripts/quest/forge_issue.py
    python3 scripts/quest/forge_issue.py --body-file issue.md

    # Self-check (no network, no gh): parses an embedded fixture and asserts.
    python3 scripts/quest/forge_issue.py --selftest

The output is advisory structure, not a schema gate: unparseable sections degrade
to empty lists rather than failing, because the issue format can drift. The agent
treats a thin manifest as "parse what you can, quote nothing you can't".
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from typing import Dict, List, Optional

# --- Chapter heading -------------------------------------------------------
# Matches lines like:
#   ### I. 🌱 The Summoning — `0001` · 🟢 Easy · 50 XP · 💻 Software Developer
# Tolerant of the em-dash, middot separators, and an optional emoji in the title.
CHAPTER_RE = re.compile(
    r"^#{2,4}\s+"
    r"(?P<numeral>[IVXLCDM]+)\.\s+"
    r"(?P<title>.+?)\s+[—-]\s+"
    r"`(?P<level>\d{3,4})`\s*"
    r"(?:[·*\-|]\s*(?P<difficulty>[^·*\n]+?)\s*)?"
    r"(?:[·*\-|]\s*(?P<xp>\d+)\s*XP\s*)?"
    r"(?:[·*\-|]\s*(?P<klass>[^·*\n]+?)\s*)?$",
    re.UNICODE,
)

# --- Build-ledger table row ------------------------------------------------
# Matches rows like:
#   | #1 | `892cd3bba` | 2026-06-23 | +3016/-13 | `claude/sweet-cannon` | Title… |
LEDGER_RE = re.compile(
    r"^\|\s*#?(?P<pr>\d+)\s*"
    r"\|\s*`?(?P<sha>[0-9a-f]{7,40})`?\s*"
    r"\|\s*(?P<date>[0-9-]+)?\s*"
    r"\|\s*(?P<delta>[+\-/0-9]+)?\s*"
    r"\|\s*`?(?P<branch>[^|`]+?)`?\s*"
    r"\|\s*(?P<title>.+?)\s*\|\s*$",
    re.UNICODE,
)

# --- Badge bullet ----------------------------------------------------------
#   - 🥇 **First Pull Request** — `#1`
BADGE_RE = re.compile(
    r"^\s*[-*]\s+(?P<emoji>[^\sA-Za-z*]+)?\s*\*\*(?P<name>[^*]+)\*\*\s*(?:[—-]\s*(?P<note>.+))?$",
    re.UNICODE,
)

# Inline PR / commit references anywhere in the body, for cross-checking.
PR_REF_RE = re.compile(r"#(\d+)\b")
SHA_REF_RE = re.compile(r"`([0-9a-f]{7,40})`")

ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(s: str) -> int:
    total, prev = 0, 0
    for ch in reversed(s.upper()):
        val = ROMAN.get(ch, 0)
        total += -val if val < prev else val
        prev = max(prev, val)
    return total


def _title(body: str) -> Optional[str]:
    for line in body.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def _badges_section(body: str) -> List[Dict[str, str]]:
    """Badges only from the 'Badges …' section, to avoid scooping every bold bullet."""
    out: List[Dict[str, str]] = []
    in_section = False
    for line in body.splitlines():
        # Anchor on a heading whose text *starts* with "Badges" (after an optional
        # leading emoji/symbol) — NOT just any heading mentioning "badges", so a
        # side-quest heading like "… (side_quests · badges)" never opens it.
        if re.match(r"^#{1,4}\s+[^\w]*badges?\b", line, re.IGNORECASE):
            in_section = True
            continue
        if in_section and re.match(r"^#{1,4}\s+", line):  # next heading ends it
            break
        if in_section:
            m = BADGE_RE.match(line)
            if m:
                out.append({
                    "emoji": (m.group("emoji") or "").strip(),
                    "name": m.group("name").strip(),
                    "note": (m.group("note") or "").strip(),
                })
    return out


def parse(body: str) -> Dict:
    chapters: List[Dict] = []
    ledger: List[Dict] = []

    for line in body.splitlines():
        cm = CHAPTER_RE.match(line)
        if cm:
            numeral = cm.group("numeral")
            chapters.append({
                "numeral": numeral,
                "order": roman_to_int(numeral),
                "title": cm.group("title").strip(),
                "level": cm.group("level").strip().zfill(4),
                "difficulty": (cm.group("difficulty") or "").strip(),
                "xp": int(cm.group("xp")) if cm.group("xp") else None,
                "class": (cm.group("klass") or "").strip(),
            })
            continue
        lm = LEDGER_RE.match(line)
        if lm and lm.group("sha"):
            ledger.append({
                "pr": int(lm.group("pr")),
                "sha": lm.group("sha"),
                "date": (lm.group("date") or "").strip(),
                "delta": (lm.group("delta") or "").strip(),
                "branch": lm.group("branch").strip(),
                "title": lm.group("title").strip(),
            })

    chapters.sort(key=lambda c: c["order"])
    seen, dedup_ledger = set(), []
    for row in ledger:
        if row["pr"] in seen:
            continue
        seen.add(row["pr"])
        dedup_ledger.append(row)

    return {
        "title": _title(body),
        "chapters": chapters,
        "ledger": dedup_ledger,
        "badges": _badges_section(body),
        "stats": {
            "chapter_count": len(chapters),
            "ledger_count": len(dedup_ledger),
            "badge_count": len(_badges_section(body)),
            "total_xp": sum(c["xp"] for c in chapters if c.get("xp")),
            "pr_numbers": sorted({int(n) for n in PR_REF_RE.findall(body)}),
        },
    }


def _read_body(args) -> str:
    if args.issue:
        repo = ["--repo", args.repo] if args.repo else []
        out = subprocess.run(
            ["gh", "issue", "view", str(args.issue), *repo, "--json", "body", "-q", ".body"],
            capture_output=True, text=True, check=True,
        )
        return out.stdout
    if args.body_file:
        with open(args.body_file, encoding="utf-8") as fh:
            return fh.read()
    return sys.stdin.read()


_FIXTURE = """# ⚔️ Epic Quest: The Self-Operating Website

### I. 🌱 The Summoning — `0001` · 🟢 Easy · 50 XP · 💻 Software Developer
Raise the site and give it a voice.

### II. ⚔️ The Proving Grounds — `0100` · 🟡 Medium · 75 XP · 🏗️ System Engineer
Build the first CI.

## 🧾 The canonical build ledger

| PR | Merge commit | Date | Δ | Branch | Title |
|---|---|---|---|---|---|
| #1 | `892cd3bba` | 2026-06-23 | +3016/-13 | `claude/sweet-cannon` | Evolve the site |
| #3 | `b97e50c1a` | 2026-06-23 | +865/-27 | `feat/ci-cd` | CI/CD quality gate |

## 🏅 Badges this campaign awards
- 🥇 **First Pull Request** — `#1`
- 🐛 **Bug Slayer** — survive `#13`
"""


def _selftest() -> int:
    m = parse(_FIXTURE)
    assert m["title"] == "⚔️ Epic Quest: The Self-Operating Website", m["title"]
    assert m["stats"]["chapter_count"] == 2, m["stats"]
    assert m["chapters"][0]["level"] == "0001"
    assert m["chapters"][0]["xp"] == 50
    assert m["chapters"][1]["difficulty"].startswith("🟡")
    assert m["stats"]["ledger_count"] == 2, m["stats"]
    assert m["ledger"][0]["sha"] == "892cd3bba"
    assert m["ledger"][0]["pr"] == 1
    assert m["stats"]["badge_count"] == 2, m["badges"]
    assert m["badges"][0]["name"] == "First Pull Request"
    assert m["stats"]["total_xp"] == 125
    print("forge_issue.py selftest: OK")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Collect a quest-forge issue into a structured manifest.")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--issue", type=int, help="issue number (read via gh)")
    src.add_argument("--body-file", help="path to the issue body markdown (else stdin)")
    ap.add_argument("--repo", help="owner/name for gh (default: current repo)")
    ap.add_argument("--json", dest="json_out", help="write manifest JSON here (default stdout)")
    ap.add_argument("--selftest", action="store_true", help="parse an embedded fixture and assert")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    manifest = parse(_read_body(args))
    text = json.dumps(manifest, indent=2, ensure_ascii=False)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"wrote {args.json_out}: {manifest['stats']}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
