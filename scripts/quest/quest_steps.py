#!/usr/bin/env python3
"""
quest_steps.py — turn a quest into a DETERMINISTIC, executable step plan.

The walkthrough/video lanes need to do more than "run the bash snippets": a
quest teaches by interleaving *commands to run* with *content to put in a file*
("In `index.html`, link your stylesheet…") and *things to open in a browser*
("`xdg-open index.html`"). Replaying a quest faithfully — and capturing the whole
stack it exercises — means knowing which is which.

This module is that classifier, and it is the ONE place the mapping lives. It
reuses ``quest_lib.extract_code_blocks`` (the single source of truth for what a
quest's code blocks are) and adds the execution semantics on top:

  kind = "shell"  run the block in the sandbox shell
       = "file"   write/append the block into the file the prose names
       = "open"   the learner would open a file/URL in a browser or editor —
                  the capture lane renders it and screenshots the result instead
                  of shelling out to a GUI that does not exist in a sandbox
       = "display" reference/output only (no language tag, or nothing to do)

Each step also carries the CHAPTER heading it lives under (so a recording can
label its chapters) and the PLATFORM section it belongs to (so a Linux sandbox
walks the Linux path and records the Windows path as not-applicable rather than
as a failure).

Inference rules (deliberately explicit, and unit-tested):
  * target file — the LAST `backticked.filename` mentioned in the prose within
    ``LOOKBACK`` characters before the fence; falls back to a per-language
    default (html→index.html, css→styles.css) only when the block is clearly
    file content and the prose named a file for an earlier step.
  * write vs append — first block for a target writes it; later blocks for the
    same target append (quests build a stylesheet up rule by rule).
  * insert — prose of the form "inside `<main>`" places the block before that
    element's closing tag instead of at end of file.
  * open — a shell block whose only real work is a GUI opener
    (open/xdg-open/start/Start-Process/code/subl/idle) becomes an "open" step
    targeting the file it names.

Usage:
  python3 scripts/quest/quest_steps.py pages/_quests/0001/css-styling-basics.md \
      [--platform linux|macos|windows|cloud] [--json steps.json] [--selftest]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import quest_lib  # noqa: E402

REPO_ROOT = SCRIPT_DIR.parent.parent

# How far back in the prose to look for the file a block belongs to.
LOOKBACK = 500

# Languages whose blocks are shell commands to run.
SHELL_LANGS = {"bash", "sh", "shell", "zsh", "console"}
# Languages that are file CONTENT when the prose names a target file.
FILE_LANGS = {
    "html": "index.html", "css": "styles.css", "javascript": "app.js",
    "js": "app.js", "json": "data.json", "yaml": "config.yml", "yml": "config.yml",
    "markdown": "guide.md", "md": "guide.md", "python": "main.py", "py": "main.py",
    "ruby": "main.rb", "scss": "styles.scss", "toml": "config.toml", "xml": "data.xml",
}
# Shell commands that mean "look at this in a GUI" — a sandbox has no GUI, so the
# capture lane renders the target in a headless browser instead.
GUI_OPENERS = ("xdg-open", "open ", "start ", "start-process", "code ", "subl ",
               "gnome-open", "firefox ", "chromium ", "google-chrome ")

PLATFORM_HEADINGS = {
    "macos": re.compile(r"^#{2,4}\s.*macos", re.IGNORECASE),
    "windows": re.compile(r"^#{2,4}\s.*windows", re.IGNORECASE),
    "linux": re.compile(r"^#{2,4}\s.*linux", re.IGNORECASE),
    "cloud": re.compile(r"^#{2,4}\s.*cloud", re.IGNORECASE),
}
# A heading that ends the platform-specific region (chapters etc.).
CHAPTER_RE = re.compile(r"^##\s+(.+?)\s*$")
ANY_H2_H3_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")

FILENAME_RE = re.compile(r"`([\w][\w./-]*\.(?:html|css|js|mjs|json|ya?ml|md|py|rb|sh|scss|toml|xml|txt))`")
INSIDE_TAG_RE = re.compile(r"inside\s+`?<(\w+)>`?", re.IGNORECASE)


def _strip_emoji_heading(text: str) -> str:
    """Human-friendly chapter label: drop leading emoji/decoration."""
    return re.sub(r"^[^\w(]+", "", text or "").strip()


def _context_map(body: str):
    """Per-line: the nearest preceding chapter heading and platform section."""
    lines = (body or "").split("\n")
    chapters, platforms = [], []
    chapter, platform = "", ""
    for line in lines:
        m2 = ANY_H2_H3_RE.match(line.strip())
        if m2:
            level, text = m2.group(1), m2.group(2)
            hit = next((p for p, rx in PLATFORM_HEADINGS.items() if rx.match(line.strip())), None)
            if hit:
                platform = hit
            elif level == "##":
                # A new top-level section closes any platform region.
                platform = ""
                chapter = _strip_emoji_heading(text)
        chapters.append(chapter)
        platforms.append(platform)
    return chapters, platforms


def _target_from_prose(body_lines, fence_line: int):
    """(filename, insert_anchor) inferred from the prose before the fence."""
    start = max(0, fence_line - 1 - 40)
    prose = "\n".join(body_lines[start:fence_line - 1])[-LOOKBACK:]
    names = FILENAME_RE.findall(prose)
    anchor = INSIDE_TAG_RE.search(prose)
    return (names[-1] if names else None), (anchor.group(1).lower() if anchor else None)


def _split_gui(code: str):
    """Split a shell block into (runnable lines, GUI-opener lines).

    Quests routinely end a setup block with `xdg-open index.html` — "now look at
    it". A sandbox has no GUI, so the opener is not a command to run and not a
    failure either: it is the point where the learner LOOKS at something. The
    runner executes the other lines and the capture lane renders the target.
    """
    lines = [l.strip() for l in code.split("\n")
             if l.strip() and not l.strip().startswith("#")]
    openers = [l for l in lines if l.lower().startswith(GUI_OPENERS)]
    rest = [l for l in lines if l not in openers]
    return rest, openers


def _gui_target(opener_lines):
    """The file/URL a GUI-opener line names (None when it names nothing useful)."""
    for line in reversed(opener_lines):
        m = re.search(r"(https?://\S+)", line)
        if m:
            return m.group(1)
        m = re.search(r"([\w][\w./-]*\.(?:html|css|md|js|json|txt))", line)
        if m:
            return m.group(1)
    return None


def build_steps(quest_path, platform: str = "linux") -> dict:
    """Return the ordered, executable step plan for one quest."""
    path = Path(quest_path)
    doc = quest_lib.read_quest(path)
    body = doc.body or ""
    body_lines = body.split("\n")
    chapters, platforms = _context_map(body)
    blocks = quest_lib.extract_code_blocks(body)

    steps = []
    written = set()
    for b in blocks:
        idx = b.line - 1
        chapter = chapters[idx] if idx < len(chapters) else ""
        block_platform = platforms[idx] if idx < len(platforms) else ""
        lang = (b.lang or "").lower()
        code = b.code or ""
        applicable = (not block_platform) or (block_platform == platform)

        kind, target, mode, anchor, opens = "display", None, None, None, None
        if lang in SHELL_LANGS:
            rest, openers = _split_gui(code)
            opens = _gui_target(openers)
            if openers and not rest:
                # Nothing to run — the whole block is "go look at this".
                kind, target = "open", opens
            else:
                kind = "shell"
        elif lang in FILE_LANGS:
            named, anchor = _target_from_prose(body_lines, b.line)
            target = named or (FILE_LANGS[lang] if any(
                s.get("kind") == "file" for s in steps) else None)
            if target:
                kind = "file"
                if anchor and target in written:
                    mode = "insert"
                else:
                    mode = "append" if target in written else "write"
                written.add(target)
        elif lang == "powershell":
            # Windows-only by construction; recorded as not-applicable elsewhere.
            kind = "shell"
            block_platform = block_platform or "windows"
            applicable = platform == "windows"

        steps.append({
            "index": len(steps),
            "kind": kind,
            "lang": lang,
            "code": code,
            "target": target,
            "mode": mode,
            "anchor": anchor,
            # For a shell step that ends by opening something in a GUI: what the
            # learner would then be looking at. The capture lane renders it.
            "opens": opens,
            "chapter": chapter,
            "platform": block_platform,
            "applicable": bool(applicable),
            "line": b.line,
        })

    fm = doc.fm or {}
    return {
        "schema_version": "1.0.0",
        "quest": {
            "path": _repo_rel(path),
            "title": fm.get("title") or path.stem,
            "level": str(fm.get("level") or ""),
            "permalink": fm.get("permalink") or "",
            "difficulty": fm.get("difficulty") or "",
            "quest_type": fm.get("quest_type") or "",
            "slug": quest_lib_slug(path),
        },
        "platform": platform,
        "steps": steps,
        "stats": {
            "total": len(steps),
            "runnable": sum(1 for s in steps if s["kind"] in ("shell", "file", "open")),
            "applicable": sum(1 for s in steps
                              if s["applicable"] and s["kind"] in ("shell", "file", "open")),
            "by_kind": {k: sum(1 for s in steps if s["kind"] == k)
                        for k in ("shell", "file", "open", "display")},
            "chapters": [c for i, c in enumerate(dict.fromkeys(
                s["chapter"] for s in steps if s["chapter"]))],
        },
    }


def _repo_rel(path: Path) -> str:
    """Repo-relative path when the quest lives in the repo; as-given otherwise."""
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def quest_lib_slug(path: Path) -> str:
    import quest_registry as reg  # noqa: PLC0415
    return reg.slug_from_filename(path.name)


# ─────────────────────────────────────────────────────────────────────────────

SELFTEST_MD = """---
title: Selftest Quest
level: '0001'
permalink: /quests/0001/selftest/
---

## Choose Your Adventure Platform

### Linux Territory Path

```bash
mkdir -p ~/demo && cd ~/demo
touch index.html styles.css
xdg-open index.html
```

### Windows Empire Path

```powershell
New-Item index.html
```

## Chapter 1: Structure

In `index.html`, add the page shell:

```html
<html><body><main></main></body></html>
```

Now in `styles.css`, style it:

```css
body { margin: 0; }
```

Then add more rules to `styles.css`:

```css
.card { color: red; }
```

Add this HTML inside `<main>`:

```html
<p>hi</p>
```
"""


def _selftest() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "selftest.md"
        p.write_text(SELFTEST_MD, encoding="utf-8")
        plan = build_steps(p, platform="linux")
    steps = plan["steps"]
    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    # The Linux setup block opens a GUI → classified as an "open" step.
    linux = steps[0]
    check("mixed setup+open block runs as shell", linux["kind"] == "shell")
    check("shell step declares what it opens", linux["opens"] == "index.html")
    check("linux platform tagged", linux["platform"] == "linux")
    check("linux applicable", linux["applicable"] is True)
    # PowerShell block is windows-only and not applicable on linux.
    ps = steps[1]
    check("powershell not applicable on linux", ps["applicable"] is False)
    check("powershell platform windows", ps["platform"] == "windows")
    # File targets come from the prose.
    html = steps[2]
    check("html targets index.html", html["kind"] == "file" and html["target"] == "index.html")
    check("html mode write", html["mode"] == "write")
    css1, css2 = steps[3], steps[4]
    check("css targets styles.css", css1["target"] == "styles.css" and css1["mode"] == "write")
    check("second css appends", css2["target"] == "styles.css" and css2["mode"] == "append")
    # "inside `<main>`" on an already-written file → insert with an anchor.
    ins = steps[5]
    check("insert mode", ins["mode"] == "insert" and ins["anchor"] == "main")
    check("chapter captured", steps[2]["chapter"].startswith("Chapter 1"))
    check("pure-open block is open-kind", _split_gui("xdg-open index.html") == ([], ["xdg-open index.html"]))
    check("gui target from url", _gui_target(["open https://codepen.io"]) == "https://codepen.io")
    check("stats runnable counted", plan["stats"]["runnable"] >= 5)

    ok = all(c for _, c in checks)
    for name, cond in checks:
        print(f"  {'✅' if cond else '❌'} {name}")
    print(f"\n{'✅ selftest passed' if ok else '❌ selftest FAILED'} "
          f"({sum(1 for _, c in checks if c)}/{len(checks)})")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("quest", nargs="?", help="quest markdown path")
    ap.add_argument("--platform", default="linux",
                    choices=["linux", "macos", "windows", "cloud"])
    ap.add_argument("--json", help="write the plan to this file (default: stdout summary)")
    ap.add_argument("--selftest", action="store_true", help="run the embedded self-test")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()
    if not args.quest:
        ap.error("a quest path is required (or --selftest)")

    plan = build_steps(args.quest, platform=args.platform)
    if args.json:
        Path(args.json).write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n",
                                   encoding="utf-8")
        print(f"📄 step plan → {args.json}")
    st = plan["stats"]
    print(f"⚔️  {plan['quest']['title']}  ({plan['quest']['level']}, {args.platform})")
    print(f"   {st['applicable']} applicable of {st['runnable']} runnable "
          f"({st['total']} blocks): {st['by_kind']}")
    for s in plan["steps"]:
        if s["kind"] == "display":
            continue
        flag = "" if s["applicable"] else "  [not applicable]"
        tgt = f" → {s['target']} ({s['mode']})" if s["target"] and s["mode"] else (
            f" → {s['target']}" if s["target"] else "")
        first = (s["code"].strip().split("\n") or [""])[0][:60]
        print(f"   {s['index']:>2}. [{s['kind']:<7}] {s['chapter'][:28]:<28}{tgt}{flag}")
        print(f"        {first}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
