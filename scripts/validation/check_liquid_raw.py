#!/usr/bin/env python3
"""
check_liquid_raw.py — deterministic Liquid raw-guard gate for content markdown.

WHY THIS EXISTS. Jekyll runs Liquid BEFORE Markdown, so code fences and backticks
do NOT protect `{{ … }}` / `{% … %}` / GitHub Actions `${{ … }}`. Pages must wrap
such snippets in a `{% raw %}` … `{% endraw %}` block. The raw block does not
nest and cannot contain a literal `{% endraw %}` — Liquid always pairs an opening
`{% raw %}` with the NEXT `{% endraw %}` it sees, so any leftover `{% endraw %}`
is an orphan and every Jekyll build (dev, CI, and production GitHub Pages alike)
dies at parse time with "Unknown tag 'endraw'", taking the deploy down.

This gate models Liquid's actual sequential raw-block pairing and fails BEFORE
the slow Jekyll build, with a precise file:line. It flags:

  1. ORPHAN `{% endraw %}` — an endraw with no raw block open. The classic cause
     is trying to display raw/endraw tags literally inline, e.g.
     `{% raw %}{% endraw %}{% endraw %}`: Liquid closes the block at the FIRST
     endraw and the second is an orphan. FATAL in every build.
  2. NESTED `{% raw %}` — a raw tag inside an already-open raw block. Liquid
     treats it as literal text, so the inner guard's endraw closes the OUTER
     block early and a later endraw becomes an orphan. Flagged at the cause line.
  3. UNCLOSED `{% raw %}` at end of file. FATAL.
  4. UNGUARDED GitHub Actions `${{ … }}` outside any raw region — not valid
     Jekyll Liquid, so it is always a code example that must be raw-guarded (it
     renders to `$` at best, or throws on `||`/`==` at worst). Bare `{{`/`{%`
     are LEGITIMATE Liquid templating (e.g. pages/stats.md) and are not flagged.

Escaped early once already: the display-only guard note that shipped in PR #445
(`{% raw %}{% endraw %}{% endraw %}` inline) passed the old line-based checker —
it only modeled full-line raw blocks and scrubbed balanced inline spans — and
broke the production Pages build. Tags are now paired sequentially across the
whole file, exactly like Liquid's parser.

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
TAG_RE = re.compile(rf"(?P<raw>{RAW_T})|(?P<endraw>{ENDRAW_T})")


def check_text(text: str):
    """Yield (line_no, problem) for one file's text.

    Walks raw/endraw tags in document order, mirroring Liquid's parser: an
    opening raw pairs with the NEXT endraw, unconditionally. Everything between
    a pair is a guarded region; `${{` is only legal inside one.
    """
    def line_of(pos: int) -> int:
        return text.count("\n", 0, pos) + 1

    raw_spans = []          # (start, end) offsets of guarded regions
    open_at = None          # offset of the currently open {% raw %}, or None
    for m in TAG_RE.finditer(text):
        if m.lastgroup == "raw":
            if open_at is None:
                open_at = m.start()
            else:
                # Literal to Liquid, but a trap for authors: the next endraw
                # closes the OUTER block, orphaning the one after it.
                yield (line_of(m.start()),
                       "{% raw %} inside an open raw block → nesting "
                       "(raw does not nest; the next {% endraw %} closes the outer block)")
        else:  # endraw
            if open_at is None:
                yield (line_of(m.start()),
                       "orphan {% endraw %} with no open {% raw %} block "
                       "(fatal: Liquid 'Unknown tag endraw')")
            else:
                raw_spans.append((open_at, m.end()))
                open_at = None
    if open_at is not None:
        yield (line_of(open_at), "unclosed {% raw %} block at end of file")
        raw_spans.append((open_at, len(text)))  # treat rest as guarded: avoid double-reporting

    for m in re.finditer(r"\$\{\{", text):
        if not any(s <= m.start() < e for s, e in raw_spans):
            line = text.split("\n")[line_of(m.start()) - 1]
            yield (line_of(m.start()),
                   f"unguarded GitHub Actions ${{{{ outside {{% raw %}}: {line.strip()[:60]}")


def iter_files(paths):
    for p in paths:
        pp = Path(p)
        if pp.is_dir():
            yield from sorted(pp.rglob("*.md"))
            yield from sorted(pp.rglob("*.markdown"))
        elif pp.suffix in (".md", ".markdown") and pp.is_file():
            yield pp


_GOOD = (
    "intro\n{% raw %}\n```yaml\nx: ${{ y }}\n```\n{% endraw %}\n"
    "inline `a{% raw %}${{ z }}{% endraw %}b` ok\n"
    "mid-line open {% raw %}\n${{ spans_lines }}\n{% endraw %} mid-line close\n"
)
_BAD_NESTED = "{% raw %}\n```yaml\nif: {% raw %}${{ always() }}{% endraw %}\n```\n{% endraw %}\n"
# The exact inline pattern that took down the Pages build (PR #445):
_BAD_ORPHAN = ("> The `{% raw %}{% raw %}{% endraw %}` / `{% raw %}{% endraw %}{% endraw %}` "
               "lines below are display-only guards.\n")
_BAD_BARE_ORPHAN = "close it with `{% endraw %}` when done\n"
_BAD_UNCLOSED = "{% raw %}\n${{ never_closed }}\n"
_BAD_UNGUARDED = "run: echo ${{ github.sha }}\n"


def _selftest() -> int:
    assert list(check_text(_GOOD)) == [], list(check_text(_GOOD))
    nested = list(check_text(_BAD_NESTED))
    assert any("nesting" in p for _, p in nested), nested
    assert any("orphan" in p for _, p in nested), nested  # the outer endraw is orphaned
    orphan = list(check_text(_BAD_ORPHAN))
    assert any("orphan" in p for _, p in orphan), orphan
    bare = list(check_text(_BAD_BARE_ORPHAN))
    assert any("orphan" in p for _, p in bare), bare
    unclosed = list(check_text(_BAD_UNCLOSED))
    assert [p for _, p in unclosed] == ["unclosed {% raw %} block at end of file"], unclosed
    unguarded = list(check_text(_BAD_UNGUARDED))
    assert any("unguarded" in p for _, p in unguarded), unguarded
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
              f"fatal to EVERY Jekyll build (dev, CI, and production Pages).", file=sys.stderr)
        return 1
    if not args.quiet:
        print(f"✅ Liquid raw-guards clean across {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
