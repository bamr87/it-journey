#!/usr/bin/env python3
"""
check_liquid_raw.py — deterministic Liquid raw-guard gate for content markdown.

WHY THIS EXISTS. Jekyll runs Liquid BEFORE Markdown, so code fences and backticks
do NOT protect `{{ … }}` / `{% … %}` / GitHub Actions `${{ … }}`. Pages must wrap
such snippets in a `{% raw %}` … `{% endraw %}` block. Two mistakes ship a page
that builds locally (the dev/CI config sets `liquid.error_mode: warn`, which
DOWNGRADES Liquid parse errors to warnings) yet FAILS the production GitHub Pages
build (strict), taking the live site down:

  1. NESTED raw — a `{% raw %}` block wrapped around code that already contains an
     inline `{% raw %}…{% endraw %}` guard. raw does not nest, so the inner
     `{% endraw %}` closes the block early and the outer one is an orphan
     ("Unknown tag 'endraw'"). FATAL.
  2. UNGUARDED expression — a `{{`/`${{`/`{%` left outside any raw block.

This gate models Liquid's raw-block parsing and fails the build BEFORE Jekyll, with
a precise file:line, so the bug is caught in CI instead of in production.

Usage:
    python3 scripts/validation/check_liquid_raw.py [paths-or-dirs ...]   # default: pages
    python3 scripts/validation/check_liquid_raw.py --selftest
Exit: 0 clean · 1 problems found · 2 bad invocation.
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

# Tags, tolerant of Liquid whitespace-trim hyphens: {%- raw -%}, {% raw %}, etc.
RAW_T = r"\{%-?\s*raw\s*-?%\}"
ENDRAW_T = r"\{%-?\s*endraw\s*-?%\}"
OPEN_RE = re.compile(rf"^\s*{RAW_T}\s*$")
CLOSE_RE = re.compile(rf"^\s*{ENDRAW_T}\s*$")
ANY_RAW_RE = re.compile(rf"{RAW_T}|{ENDRAW_T}")
INLINE_SPAN = re.compile(rf"{RAW_T}.*?{ENDRAW_T}")          # a balanced inline guard is fine


def _is_open(s: str) -> bool:  return bool(OPEN_RE.match(s))
def _is_close(s: str) -> bool: return bool(CLOSE_RE.match(s))


def check_text(text: str):
    """Yield (line_no, problem) for one file's text."""
    depth = 0
    for i, raw_line in enumerate(text.split("\n"), 1):
        s = raw_line
        if _is_open(s):
            if depth:
                yield (i, "nested {% raw %} (raw blocks do not nest)")
            depth = 1
            continue
        if _is_close(s):
            if depth == 0:
                yield (i, "{% endraw %} with no open {% raw %} block")
            depth = 0
            continue
        if depth:
            # Inside a raw block everything is literal — but an inline raw/endraw
            # here is exactly the nesting trap that breaks the production build.
            if ANY_RAW_RE.search(s):
                yield (i, f"inline raw tag inside a {{% raw %}} block → nesting: {s.strip()[:60]}")
            continue
        # Outside a raw block, only flag GitHub Actions `${{ … }}` — it is NOT valid
        # Jekyll Liquid, so it is always a code example that must be raw-guarded (it
        # renders to `$` at best, or throws on `||`/`==` at worst). Bare `{{`/`{%`
        # are LEGITIMATE Liquid templating (e.g. pages/stats.md) and must not be flagged.
        scrubbed = INLINE_SPAN.sub("", s)            # genuine inline guards are safe
        if "${{" in scrubbed:
            yield (i, f"unguarded GitHub Actions ${{{{ outside {{% raw %}}: {s.strip()[:60]}")
    if depth:
        yield (0, "unclosed {% raw %} block at end of file")


def iter_files(paths):
    for p in paths:
        pp = Path(p)
        if pp.is_dir():
            yield from sorted(pp.rglob("*.md"))
            yield from sorted(pp.rglob("*.markdown"))
        elif pp.suffix in (".md", ".markdown") and pp.is_file():
            yield pp


_GOOD = "intro\n{% raw %}\n```yaml\nx: ${{ y }}\n```\n{% endraw %}\ninline `a{% raw %}${{ z }}{% endraw %}b` ok\n"
_BAD = "{% raw %}\n```yaml\nif: {% raw %}${{ always() }}{% endraw %}\n```\n{% endraw %}\n"


def _selftest() -> int:
    assert list(check_text(_GOOD)) == [], list(check_text(_GOOD))
    bad = list(check_text(_BAD))
    assert any("nesting" in p for _, p in bad), bad
    print("check_liquid_raw selftest: OK")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Deterministic Liquid raw-guard gate.")
    ap.add_argument("paths", nargs="*", default=["pages"], help="files or dirs (default: pages)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("-q", "--quiet", action="store_true", help="only print on failure")
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest()

    files = list(iter_files(args.paths or ["pages"]))
    total = 0
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        for ln, prob in check_text(text):
            print(f"{f}:{ln}: {prob}")
            total += 1
    if total:
        print(f"\n❌ {total} Liquid raw-guard problem(s) in {len(files)} file(s) — "
              f"these build locally (error_mode: warn) but FAIL production Pages.", file=sys.stderr)
        return 1
    if not args.quiet:
        print(f"✅ Liquid raw-guards clean across {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
