#!/usr/bin/env python3
"""
env_migrate.py — give every quest a machine-readable ``environment:`` block,
derived from the platform instructions it ALREADY contains.

The quest corpus encodes its environment assumptions as prose: four sections
("🍎 macOS Kingdom Path", "🪟 Windows Empire Path", …), a `mkdir -p ~/css-quest`
buried in a setup snippet, a PowerShell block that only Windows readers need.
That is invisible to tooling and unhelpful to a reader who has to scroll past
three paths that are not theirs.

This migrates that knowledge into frontmatter, without rewriting a single line of
quest prose:

    environment:
      os: [macos, windows, linux, cloud]   # the paths this quest provides
      shell: [zsh, bash, powershell]       # shells its commands are written for
      variables:
        project_dir: css-quest             # the folder its commands create

Downstream that block powers three things at once:
  * the reader-facing environment control (_includes/quest/quest-env.html), which
    shows only the path matching the reader's machine and rewrites the snippets
    with their chosen folder;
  * quest_steps.py / stack_capture.mjs, which walk the quest per environment —
    the same declaration decides which steps a Linux CI sandbox should run and
    which it should record as not-applicable;
  * validation, which can now ask "does this quest claim a Windows path it does
    not actually provide?".

Detection is conservative: a path is only claimed when the quest really has a
section for it, and an existing ``environment:`` block is never overwritten
unless --force is passed (so hand-tuned values win over inference).

Usage:
  python3 scripts/quest/env_migrate.py [PATH] [--apply] [--force] [--report]
  (default PATH = pages/_quests; without --apply it is a dry run)
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

from ruamel.yaml import YAML

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import quest_lib  # noqa: E402
import quest_registry as reg  # noqa: E402

REPO_ROOT = SCRIPT_DIR.parent.parent

yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096

HEADING_RE = re.compile(r"^(#{2,4})\s+(.*)$")
# `mkdir -p ~/css-quest`, `mkdir $HOME\css-quest`, `cd ~/css-quest`
PROJECT_DIR_RE = re.compile(
    r"(?:mkdir(?:\s+-p)?|cd)\s+(?:~|\$HOME|\$env:USERPROFILE)[/\\]([\w][\w.-]*)")

OS_KEYWORDS = {
    "macos": ("macos", "mac os", "kingdom"),
    "windows": ("windows", "empire", "powershell"),
    "linux": ("linux", "territory", "ubuntu", "debian"),
    "cloud": ("cloud", "realms", "container", "codespace", "docker"),
}


def detect_os_paths(body: str) -> list:
    """Which OS paths this quest actually documents, in registry order."""
    found = set()
    for line in (body or "").split("\n"):
        m = HEADING_RE.match(line.strip())
        if not m:
            continue
        text = m.group(2).lower()
        for os_value, words in OS_KEYWORDS.items():
            if any(w in text for w in words):
                found.add(os_value)
    return [o for o in reg.env_options("os") if o in found]


def detect_shells(body: str, os_paths: list) -> list:
    """Shells the quest's own snippets are written for."""
    langs = {(b.lang or "").lower() for b in quest_lib.extract_code_blocks(body or "")}
    shells = []
    if langs & {"bash", "sh", "shell", "console", "zsh"}:
        # A macOS path implies zsh (its default shell) alongside bash.
        if "macos" in os_paths:
            shells.append("zsh")
        shells.append("bash")
    if "powershell" in langs or "windows" in os_paths:
        shells.append("powershell")
    seen, out = set(), []
    for s in shells:
        if s in reg.env_options("shell") and s not in seen:
            seen.add(s)
            out.append(s)
    return out


def detect_project_dir(body: str):
    """The folder the quest's commands create, if they create one."""
    hits = PROJECT_DIR_RE.findall(body or "")
    if not hits:
        return None
    # The most frequently referenced folder is the quest's project dir.
    ranked = sorted(set(hits), key=lambda h: (-hits.count(h), hits.index(h)))
    return ranked[0]


def build_environment(body: str) -> dict:
    os_paths = detect_os_paths(body)
    if not os_paths:
        return {}
    env = {"os": os_paths}
    shells = detect_shells(body, os_paths)
    if shells:
        env["shell"] = shells
    project = detect_project_dir(body)
    if project:
        env["variables"] = {"project_dir": project}
    return env


# `<details>` wrappers around the platform paths. Kramdown does NOT parse
# markdown inside a raw HTML block unless the element carries markdown="1" — so
# every fenced snippet inside these renders as literal backticks instead of a
# highlighted, copyable code block. That breaks the reader's experience AND the
# environment control (which can only rewrite real <code> elements), so the
# migration repairs it.
DETAILS_RE = re.compile(r"<details(?![^>]*\bmarkdown=)([^>]*)>")


def fix_details(text: str):
    """Add markdown="1" to <details> wrappers that contain a fenced code block.

    Returns (new_text, count). Idempotent: a wrapper that already declares the
    attribute is left alone.
    """
    out, count, pos = [], 0, 0
    for m in DETAILS_RE.finditer(text):
        # Only wrappers whose body actually holds a fence need the attribute.
        end = text.find("</details>", m.end())
        body = text[m.end():end if end > 0 else len(text)]
        out.append(text[pos:m.start()])
        if "```" in body or "~~~" in body:
            out.append(f"<details markdown=\"1\"{m.group(1)}>")
            count += 1
        else:
            out.append(m.group(0))
        pos = m.end()
    out.append(text[pos:])
    return "".join(out), count


def _split_frontmatter(text: str):
    if not text.startswith("---"):
        return None, None, None
    end = text.find("\n---", 3)
    if end == -1:
        return None, None, None
    fm_text = text[text.find("\n", 0) + 1:end].rstrip("\n")
    return text[:text.find("\n") + 1], fm_text, text[end + len("\n---"):]


def migrate_file(path: Path, force: bool = False, details: bool = True):
    """Return (new_text_or_False, detail). Writes nothing — caller decides."""
    text = quest_lib.read_text(path)
    head, fm_text, after = _split_frontmatter(text)
    if fm_text is None:
        return False, "no frontmatter"
    fm = yaml.load(io.StringIO(fm_text))
    if fm is None:
        return False, "empty frontmatter"
    if not reg.is_quest(fm):
        return False, "not a quest page"
    if fm.get("source_repo") or fm.get("source_url"):
        return False, "vendored (read-only)"
    doc = quest_lib.read_quest(path)
    body_after, fixed = (fix_details(after) if details else (after, 0))
    declared = "environment" in fm and not force

    env = {} if declared else build_environment(doc.body)
    if declared and not fixed:
        return False, "already declared"
    if not declared and not env and not fixed:
        return False, "no platform sections detected"

    if env:
        fm["environment"] = env
    buf = io.StringIO()
    yaml.dump(fm, buf)
    new_text = head + buf.getvalue().rstrip("\n") + "\n---" + body_after
    bits = []
    if env:
        bits.append("os=" + ",".join(env["os"]))
        if env.get("shell"):
            bits.append("shell=" + ",".join(env["shell"]))
        if env.get("variables"):
            bits.append("project_dir=" + env["variables"]["project_dir"])
    if fixed:
        bits.append(f"{fixed} <details> made markdown-aware")
    return new_text, " ".join(bits)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default="pages/_quests")
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing environment: block (hand-tuned values normally win)")
    ap.add_argument("--report", action="store_true", help="list every file's outcome")
    ap.add_argument("--no-details-fix", action="store_true",
                    help="skip adding markdown=\"1\" to <details> wrappers holding code fences")
    args = ap.parse_args()

    root = Path(args.path)
    files = [root] if root.is_file() else sorted(quest_lib.iter_quest_files(root))
    changed, skipped = [], {}
    for f in files:
        result, detail = migrate_file(f, force=args.force, details=not args.no_details_fix)
        rel = str(f.relative_to(REPO_ROOT)) if f.is_absolute() else str(f)
        if result:
            changed.append((rel, detail))
            if args.apply:
                f.write_text(result, encoding="utf-8")
        else:
            skipped[detail] = skipped.get(detail, 0) + 1
            if args.report:
                print(f"  ·  {rel}: {detail}")

    for rel, detail in changed:
        print(f"  {'✍️ ' if args.apply else '➕'} {rel}  ({detail})")
    verb = "wrote" if args.apply else "would write"
    print(f"\n{verb} environment: for {len(changed)} quest(s).")
    for reason, n in sorted(skipped.items(), key=lambda kv: -kv[1]):
        print(f"   skipped {n:>4}  — {reason}")
    if not args.apply and changed:
        print("\nRe-run with --apply to write.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
