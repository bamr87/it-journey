#!/usr/bin/env python3
"""
check_mermaid_flags.py

IT-Journey Mermaid Rendering Guard
==================================

The zer0-mistakes theme only loads the Mermaid library when a page declares
`mermaid: true` in its front matter:

    {% if page.mermaid %}{% include components/mermaid.html %}{% endif %}

Any content file that contains a Mermaid diagram (a ```mermaid fenced block or
an HTML element with class="mermaid") but omits that flag will silently fail to
render — the diagram shows up as a raw code block instead of a chart.

This script scans every content file, decides whether it actually contains a
Mermaid diagram (using a proper GFM fenced-code scanner so that *illustrative*
mermaid examples nested inside a larger fence don't count), and reports — or
fixes — any file whose flag is out of sync with its content.

Modes
-----
    --check   (default) report files that need `mermaid: true`; exit 1 if any.
    --fix     insert `mermaid: true` into the front matter of those files.
    --prune   additionally report files that declare the flag but have no
              diagram (informational; never auto-removed).

Usage
-----
    python3 scripts/validation/check_mermaid_flags.py            # check
    python3 scripts/validation/check_mermaid_flags.py --fix      # apply
    python3 scripts/validation/check_mermaid_flags.py --json out.json

Author: IT-Journey Team
Created: 2026-06-20
Version: 1.0.0
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Directories to scan, relative to the repo root.
CONTENT_GLOBS = ("pages/**/*.md", "pages/**/*.markdown", "pages/**/*.html")

# Vendored / read-only content is never edited; surfaced separately.
# Detected by frontmatter key (no vendored path tree remains after the
# wargames extraction to github.com/bamr87/wargames).
VENDORED_PATH_MARKERS = ()
VENDORED_FRONTMATTER_KEYS = ("source_repo",)

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n", re.DOTALL)
FENCE_RE = re.compile(r"^([`~]{3,})(.*)$")
MERMAID_DIV_RE = re.compile(r"""class\s*=\s*["'][^"']*\bmermaid\b""")
# A flag counts as "true" even with surrounding whitespace or a trailing
# comment, so `mermaid: true  # render charts` is recognized (and never
# duplicated). Case-insensitive; accepts true/yes.
FLAG_TRUE_RE = re.compile(r"(?im)^mermaid:\s*(true|yes)\s*(#.*)?$")
# Any top-level `mermaid:` key, regardless of value.
FLAG_ANY_RE = re.compile(r"(?im)^mermaid:\s*(.+?)\s*$")


class C:
    """ANSI colors (no-op when not a TTY)."""

    G = "\033[92m" if sys.stdout.isatty() else ""
    Y = "\033[93m" if sys.stdout.isatty() else ""
    R = "\033[91m" if sys.stdout.isatty() else ""
    B = "\033[94m" if sys.stdout.isatty() else ""
    D = "\033[2m" if sys.stdout.isatty() else ""
    X = "\033[0m" if sys.stdout.isatty() else ""


# --------------------------------------------------------------------------- #
# Detection
# --------------------------------------------------------------------------- #


def split_frontmatter(text: str):
    """Return (frontmatter_text_or_None, body_text)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def body_has_mermaid(body: str) -> bool:
    """
    True when the body contains a *renderable* Mermaid diagram.

    Implements GFM fenced-code semantics: the first fence of a run opens a
    block; a closing fence must use the same character, be at least as long,
    and carry no info string. A ```mermaid fence nested inside a larger fence
    is literal text and does NOT count (those are tutorials showing syntax).
    Raw HTML <... class="mermaid"> elements always count.
    """
    in_fence = False
    fence_char = ""
    fence_len = 0

    for raw in body.splitlines():
        stripped = raw.lstrip()
        m = FENCE_RE.match(stripped)
        if m:
            marker, rest = m.group(1), m.group(2).strip()
            char, length = marker[0], len(marker)
            if not in_fence:
                in_fence = True
                fence_char, fence_len = char, length
                info = rest.split()[0].lower() if rest else ""
                if info == "mermaid":
                    return True
            else:
                # A bare same-char fence of >= length closes the block.
                if char == fence_char and length >= fence_len and rest == "":
                    in_fence = False
            continue
        # Only inspect raw-HTML mermaid divs when not inside a code fence.
        if not in_fence and MERMAID_DIV_RE.search(raw):
            return True
    return False


@dataclass
class FileResult:
    path: str
    has_diagram: bool
    has_flag: bool
    flag_value: Optional[str]  # raw value if `mermaid:` key present
    has_frontmatter: bool
    vendored: bool

    @property
    def needs_flag(self) -> bool:
        # Only files with NO `mermaid:` key at all get a flag inserted. A file
        # that has a non-true value (e.g. `mermaid: false`) is a *conflict*,
        # routed to its own lane so --fix never emits a duplicate key.
        return (
            self.has_diagram
            and self.has_frontmatter
            and not self.has_flag
            and self.flag_value is None
            and not self.vendored
        )

    @property
    def conflict(self) -> bool:
        # Diagram present but flag explicitly set to a non-true value.
        return (
            self.has_diagram
            and self.flag_value is not None
            and not self.has_flag
        )

    @property
    def stale_flag(self) -> bool:
        return self.has_flag and not self.has_diagram and not self.vendored


def analyze(path: Path) -> FileResult:
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    has_fm = fm is not None
    has_diagram = body_has_mermaid(body)

    flag_value = None
    has_flag = False
    vendored = any(marker in path.as_posix() for marker in VENDORED_PATH_MARKERS)
    if has_fm:
        has_flag = bool(FLAG_TRUE_RE.search(fm))
        any_m = FLAG_ANY_RE.search(fm)
        if any_m:
            flag_value = any_m.group(1).strip()
        if any(re.search(rf"(?m)^{re.escape(k)}:", fm) for k in VENDORED_FRONTMATTER_KEYS):
            vendored = True

    return FileResult(
        path=path.as_posix(),
        has_diagram=has_diagram,
        has_flag=has_flag,
        flag_value=flag_value,
        has_frontmatter=has_fm,
        vendored=vendored,
    )


# --------------------------------------------------------------------------- #
# Fix
# --------------------------------------------------------------------------- #


def insert_flag(path: Path) -> bool:
    """Insert `mermaid: true` as a top-level key just before the closing ---.

    Preserves the file's existing line-ending convention (newline="" disables
    universal-newline translation) and refuses to act if ANY `mermaid:` key is
    already present, so it can never emit a duplicate mapping key.
    """
    text = path.read_text(encoding="utf-8", newline="")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return False
    fm_block = m.group(0)  # includes opening/closing fences
    if FLAG_ANY_RE.search(fm_block):
        return False  # already declares mermaid (any value) — never duplicate

    # Closing fence is the final '---' line of the matched block.
    closing = re.search(r"\n---[ \t]*\r?\n$", fm_block) or re.search(r"\n---\s*\n$", fm_block)
    if not closing:
        return False
    nl = "\r\n" if "\r\n" in fm_block else "\n"
    insert_at = m.start() + closing.start() + 1  # right after the newline
    new_text = text[:insert_at] + "mermaid: true" + nl + text[insert_at:]
    path.write_text(new_text, encoding="utf-8", newline="")
    return True


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def collect_files(root: Path) -> List[Path]:
    seen: set = set()
    files: List[Path] = []
    for pattern in CONTENT_GLOBS:
        for p in root.glob(pattern):
            if p.is_file() and p not in seen:
                seen.add(p)
                files.append(p)
    return sorted(files)


def main() -> int:
    ap = argparse.ArgumentParser(description="Mermaid front-matter flag guard.")
    ap.add_argument("--fix", action="store_true", help="insert missing flags")
    ap.add_argument("--prune", action="store_true", help="also report stale flags")
    ap.add_argument("--json", metavar="FILE", help="write a JSON report")
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    results = [analyze(p) for p in collect_files(root)]

    needs = [r for r in results if r.needs_flag]
    conflicts = [r for r in results if r.conflict]
    stale = [r for r in results if r.stale_flag]
    no_fm = [r for r in results if r.has_diagram and not r.has_frontmatter]
    vendored = [r for r in results if r.has_diagram and r.vendored and not r.has_flag]
    diagrams = [r for r in results if r.has_diagram]

    def rel(p: str) -> str:
        return str(Path(p).resolve().relative_to(root))

    print(f"{C.B}Mermaid flag guard{C.X}  ·  scanned {len(results)} files, "
          f"{len(diagrams)} contain diagrams")

    fixed = 0
    if needs:
        verb = "Fixing" if args.fix else "Missing flag"
        print(f"\n{C.Y}{verb} ({len(needs)}):{C.X}")
        for r in needs:
            if args.fix:
                ok = insert_flag(Path(r.path))
                fixed += int(ok)
                mark = f"{C.G}fixed{C.X}" if ok else f"{C.R}skip{C.X}"
                print(f"  {mark}  {rel(r.path)}")
            else:
                print(f"  {C.R}·{C.X} {rel(r.path)}")

    if conflicts:
        print(f"\n{C.R}Conflicts — diagram present but mermaid flag is not true "
              f"({len(conflicts)}):{C.X}")
        for r in conflicts:
            print(f"  · {rel(r.path)}  (mermaid: {r.flag_value})")

    if no_fm:
        print(f"\n{C.R}Diagram but NO front matter ({len(no_fm)}):{C.X}")
        for r in no_fm:
            print(f"  · {rel(r.path)}")

    if vendored:
        print(f"\n{C.D}Vendored (read-only) files with diagrams, left untouched "
              f"({len(vendored)}):{C.X}")
        for r in vendored:
            print(f"  · {rel(r.path)}")

    if args.prune and stale:
        print(f"\n{C.D}Stale flag — mermaid: true but no diagram ({len(stale)}):{C.X}")
        for r in stale:
            print(f"  · {rel(r.path)}")

    if args.json:
        payload = {
            "scanned": len(results),
            "with_diagrams": len(diagrams),
            "needs_flag": [rel(r.path) for r in needs],
            "conflicts": [{"file": rel(r.path), "value": r.flag_value} for r in conflicts],
            "no_frontmatter": [rel(r.path) for r in no_fm],
            "vendored_with_diagrams": [rel(r.path) for r in vendored],
            "stale_flags": [rel(r.path) for r in stale],
            "fixed": fixed,
        }
        Path(args.json).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"\n{C.D}JSON report → {args.json}{C.X}")

    if args.fix:
        print(f"\n{C.G}Applied {fixed} fix(es).{C.X}")
        return 0

    problems = len(needs) + len(conflicts) + len(no_fm)
    if problems:
        print(f"\n{C.R}{problems} file(s) need attention. Run with --fix to "
              f"insert missing flags.{C.X}")
        return 1
    print(f"\n{C.G}All diagrams have the mermaid flag. ✔{C.X}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
