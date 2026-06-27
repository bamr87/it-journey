#!/usr/bin/env python3
"""
brand_lint.py — deterministic brand/voice drift guard.

The cheap, fast half of "minimize drift": before any AI spends a token, a plain
scanner flags the objective stuff from _data/brand/glossary.yml —

  • spelling drift  — `preferred` variants (Github -> GitHub, jekyll -> Jekyll, ...)
  • hype            — `discouraged` empty-hype terms (comprehensive, powerful, ...)

in real prose only (front matter and fenced/inline code are skipped, so a code
sample that literally types `javascript` or a CLI flag isn't flagged). Vendored
content (front matter carrying source_repo/source_url) is read-only and ignored.

This is the same signal the cms engine mirrors into .cms/config.yml > brand; here
it is a standalone gate two CI lanes use:
  • content-review / content-factory — soft signal handed to the agent to fix.
  • content auto-merge — hard gate: an on-brand PR must be spelling-clean.

Usage:
    python3 scripts/ci/brand_lint.py FILE...           # scan specific files
    python3 scripts/ci/brand_lint.py --all             # scan pages/**/*.md
    python3 scripts/ci/brand_lint.py --all --json out.json
    python3 scripts/ci/brand_lint.py --all --warn-only # always exit 0 (report only)

Exit codes: 0 = clean (or --warn-only); 1 = drift found; 2 = bad invocation.
By default both spelling and hype findings fail; --spelling-only ignores hype
(used by the auto-merge gate, which must not block on stylistic hype).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

REPO = Path(__file__).resolve().parent.parent.parent
GLOSSARY = REPO / "_data" / "brand" / "glossary.yml"
CONTENT_GLOBS = ("pages/**/*.md", "pages/**/*.markdown")

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n", re.DOTALL)
FENCE_RE = re.compile(r"^([`~]{3,})")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
VENDORED_KEYS = ("source_repo:", "source_url:")


class C:
    Y = "\033[93m" if sys.stdout.isatty() else ""
    R = "\033[91m" if sys.stdout.isatty() else ""
    G = "\033[92m" if sys.stdout.isatty() else ""
    D = "\033[2m" if sys.stdout.isatty() else ""
    X = "\033[0m" if sys.stdout.isatty() else ""


@dataclass
class Finding:
    file: str
    line: int
    kind: str          # "spelling" | "hype"
    term: str          # the offending text as found
    suggestion: str    # canonical form, or "" for hype


def load_glossary() -> Dict:
    try:
        import yaml
        return yaml.safe_load(GLOSSARY.read_text(encoding="utf-8")) or {}
    except Exception as e:
        print(f"brand_lint: cannot read {GLOSSARY}: {e}", file=sys.stderr)
        return {}


def split_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "", text, 0
    fm = m.group(1)
    # number of lines the front matter occupies (so body line numbers stay true)
    offset = text[: m.end()].count("\n")
    return fm, text[m.end():], offset


def strip_code(body: str) -> List[str]:
    """Return body lines with fenced-code blocks blanked and inline code removed,
    so matches only land in prose. Line indices are preserved (blanked, not deleted)."""
    out: List[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    for raw in body.splitlines():
        m = FENCE_RE.match(raw.lstrip())
        if m:
            marker = m.group(1)
            ch, ln = marker[0], len(marker)
            if not in_fence:
                in_fence, fence_char, fence_len = True, ch, ln
            elif ch == fence_char and ln >= fence_len:
                in_fence = False
            out.append("")          # the fence line itself is not prose
            continue
        out.append("" if in_fence else INLINE_CODE_RE.sub(" ", raw))
    return out


def scan_file(path: Path, preferred: Dict[str, str], discouraged: List[str],
              spelling_only: bool) -> List[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []
    fm, body, offset = split_frontmatter(text)
    if any(k in fm for k in VENDORED_KEYS):
        return []                                   # vendored / read-only

    try:
        rel = path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        rel = path.as_posix()
    findings: List[Finding] = []
    lines = strip_code(body)

    # Spelling drift — whole-word, case-sensitive (the glossary keys ARE the
    # wrong casings, e.g. "Github", "javascript"); a couple of keys carry spaces.
    spell_terms = sorted(preferred.keys(), key=len, reverse=True)
    # Hype — whole-word, case-insensitive.
    hype_terms = [] if spelling_only else sorted(set(discouraged), key=len, reverse=True)

    for i, line in enumerate(lines):
        if not line.strip():
            continue
        for wrong in spell_terms:
            right = preferred[wrong]
            if wrong == right:
                continue
            pat = re.compile(rf"(?<![\w.]){re.escape(wrong)}(?![\w.])")
            if pat.search(line):
                # Don't flag when it already reads as the canonical form.
                findings.append(Finding(rel, offset + i + 1, "spelling", wrong, right))
        for term in hype_terms:
            if re.search(rf"(?i)(?<![\w-]){re.escape(term)}(?![\w-])", line):
                findings.append(Finding(rel, offset + i + 1, "hype", term, ""))
    return findings


def collect_all() -> List[Path]:
    seen, files = set(), []
    for g in CONTENT_GLOBS:
        for p in REPO.glob(g):
            if p.is_file() and p not in seen:
                seen.add(p)
                files.append(p)
    return sorted(files)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Deterministic brand/voice drift guard.")
    ap.add_argument("files", nargs="*", help="files to scan (relative to repo root)")
    ap.add_argument("--all", action="store_true", help="scan every pages/**/*.md")
    ap.add_argument("--json", metavar="FILE", help="write a JSON report")
    ap.add_argument("--warn-only", action="store_true", help="always exit 0")
    ap.add_argument("--spelling-only", action="store_true",
                    help="ignore hype terms; only flag spelling drift")
    args = ap.parse_args(argv)

    glossary = load_glossary()
    preferred = {str(k): str(v) for k, v in (glossary.get("preferred") or {}).items()}
    discouraged = [str(t) for t in (glossary.get("discouraged") or [])]
    if not preferred and not discouraged:
        print("brand_lint: empty glossary — nothing to check.", file=sys.stderr)
        return 0

    if args.all:
        targets = collect_all()
    elif args.files:
        targets = [(REPO / f if not Path(f).is_absolute() else Path(f)) for f in args.files]
        targets = [p for p in targets if p.suffix in (".md", ".markdown") and p.is_file()]
    else:
        print("brand_lint: pass files or --all.", file=sys.stderr)
        return 2

    findings: List[Finding] = []
    for p in targets:
        findings.extend(scan_file(p, preferred, discouraged, args.spelling_only))

    spelling = [f for f in findings if f.kind == "spelling"]
    hype = [f for f in findings if f.kind == "hype"]

    print(f"{C.D}brand_lint: scanned {len(targets)} file(s){C.X}")
    if spelling:
        print(f"\n{C.R}Spelling drift ({len(spelling)}):{C.X}")
        for f in spelling:
            print(f"  {f.file}:{f.line}  {f.term!r} -> {f.suggestion!r}")
    if hype:
        print(f"\n{C.Y}Possible hype ({len(hype)}) — replace with concrete value:{C.X}")
        for f in hype:
            print(f"  {f.file}:{f.line}  {f.term!r}")
    if not findings:
        print(f"{C.G}On-brand — no glossary drift. ✔{C.X}")

    if args.json:
        Path(args.json).write_text(
            json.dumps({"findings": [asdict(f) for f in findings],
                        "spelling": len(spelling), "hype": len(hype)}, indent=2),
            encoding="utf-8")

    if args.warn_only or not findings:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
