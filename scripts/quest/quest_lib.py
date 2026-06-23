#!/usr/bin/env python3
"""
quest_lib.py — Shared parsing + discovery for the IT-Journey quest tooling.

This is the *one* place that knows how to turn a markdown file on disk into a
parsed quest. Before this module existed, the same frontmatter regex + YAML
load was reimplemented five times (quest_validator, validate-quest-network,
build-quest-network, generate-quest-navigation, agentic/loader) with subtly
different error handling, and the network validator re-hardcoded the taxonomy
instead of importing the registry. Every validator now shares these helpers so
they can never disagree about *what a quest is* or *how to read one*.

Design rules:
  * Taxonomy/schema constants live in ``quest_registry`` (the data SSOT). This
    module owns *behaviour* (parse, discover), never *vocabulary*.
  * Parsing is tolerant: a BOM, CRLF line endings, or trailing whitespace after
    the closing ``---`` must not turn a real quest into "Failed to parse
    frontmatter". A YAML error is reported as a structured signal, not a crash.
  * Discovery is deterministic (sorted) so callers that feed generated, diffable
    data files stay stable.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    print("Error: PyYAML is required but not installed (pip install pyyaml).",
          file=sys.stderr)
    raise

# The registry is the single source of truth for taxonomy + collection rules.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import quest_registry as reg  # noqa: E402

REPO_ROOT = _HERE.parents[1]
QUESTS_DIR = REPO_ROOT / "pages" / "_quests"

# Frontmatter delimiter. Tolerant of an optional UTF-8 BOM, CRLF endings, and
# trailing whitespace on the fence lines. Body is captured as the remainder.
_FM_RE = re.compile(
    r"^﻿?---[ \t]*\r?\n(?P<fm>.*?)\r?\n---[ \t]*\r?\n?(?P<body>.*)\Z",
    re.DOTALL,
)


class FrontmatterError(ValueError):
    """Raised (or attached to a result) when YAML frontmatter cannot be parsed."""


def parse_frontmatter(text: str) -> Tuple[Optional[Dict], str]:
    """Split ``text`` into (frontmatter_dict, body).

    Returns ``(None, original_text)`` when there is no frontmatter block at all.
    Raises :class:`FrontmatterError` when a block exists but the YAML inside it
    is invalid — callers decide whether that is fatal or a reported finding.
    Normalises CRLF to LF in the returned body so downstream regexes that match
    on ``\n`` behave identically across platforms.
    """
    if text is None:
        return None, ""
    m = _FM_RE.match(text)
    if not m:
        return None, text
    raw_fm = m.group("fm")
    body = m.group("body").replace("\r\n", "\n")
    try:
        fm = yaml.safe_load(raw_fm)
    except yaml.YAMLError as e:
        raise FrontmatterError(str(e)) from e
    if fm is None:
        fm = {}
    if not isinstance(fm, dict):
        raise FrontmatterError(
            f"frontmatter is a {type(fm).__name__}, expected a mapping"
        )
    return fm, body


def read_text(path: Path) -> str:
    """Read a markdown file as UTF-8, replacing undecodable bytes rather than
    failing the whole run on one mojibake file."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


@dataclass
class QuestDoc:
    """A parsed quest-tree markdown file.

    ``fm`` is the frontmatter mapping (``{}`` when absent), ``body`` the content
    after the closing fence. Derived attributes use the registry so they match
    every other tool. ``fm_error`` is set when frontmatter YAML was invalid.
    """

    path: Path
    fm: Dict = field(default_factory=dict)
    body: str = ""
    fm_error: Optional[str] = None

    @property
    def rel_path(self) -> str:
        try:
            return str(self.path.relative_to(REPO_ROOT))
        except ValueError:
            return str(self.path)

    @property
    def title(self) -> str:
        return str(self.fm.get("title") or self.path.stem)

    @property
    def level(self) -> str:
        return str(self.fm.get("level") or "")

    @property
    def quest_type(self) -> str:
        return str(self.fm.get("quest_type") or "")

    @property
    def permalink(self) -> str:
        return str(self.fm.get("permalink") or "")

    @property
    def slug(self) -> str:
        return reg.slug_from_filename(self.path.name)

    @property
    def theme(self) -> str:
        return reg.theme_of(self.level) if self.level else ""

    def is_quest(self) -> bool:
        return reg.is_quest(self.fm)

    def is_draft(self) -> bool:
        return reg.is_draft(self.fm)

    def is_scored(self) -> bool:
        return reg.is_scored(self.fm)

    def has_placeholder_marker(self) -> bool:
        return reg.has_placeholder_marker(self.body)

    # Directory level (the 4-bit dir a file lives under, if any) — used to
    # cross-check the frontmatter ``level`` and to bucket reports.
    @property
    def dir_level(self) -> Optional[str]:
        for part in self.path.parts:
            if reg.LEVEL_RE.match(part):
                return part
        return None


def read_quest(path) -> QuestDoc:
    """Parse one file into a :class:`QuestDoc` (never raises on bad YAML — the
    error is captured in ``fm_error`` so a single broken file can't abort a
    whole-corpus audit)."""
    p = Path(path)
    if not p.is_absolute():
        p = (REPO_ROOT / p).resolve()
    text = read_text(p)
    try:
        fm, body = parse_frontmatter(text)
    except FrontmatterError as e:
        return QuestDoc(path=p, fm={}, body=text, fm_error=str(e))
    return QuestDoc(path=p, fm=fm or {}, body=body)


def is_meta_file(path: Path) -> bool:
    """True when a file is collection scaffolding, not a quest page.

    Mirrors the registry skip rules plus the ALL_CAPS report convention
    (NETWORK_REPORT.md, QUEST_BUILD_PLAN.md, …). One predicate, used by every
    tool and the CI changed-file filter, so they can never disagree.
    """
    stem = path.stem
    if stem in reg.SKIP_STEMS:
        return True
    if stem.upper() in ("README", "INDEX", "HOME"):
        return True
    if stem.isupper() and "_" in stem:
        return True
    return False


def is_quest_index_readme(path: Path) -> bool:
    """True when a README/index is the *hub page* of a multi-file quest, e.g.
    ``0000/bashcrawl/README.md`` which Jekyll serves at ``/quests/0000/bashcrawl/``.

    Such a page is a real, linkable node (other quests legitimately list it as a
    prerequisite), unlike a level-index README (``0000/README.md``) or a section
    README (``tools/README.md``). The rule: name is README/index, the immediate
    parent is NOT a 4-bit level dir, and the grandparent IS one.
    """
    if path.stem.upper() not in ("README", "INDEX"):
        return False
    parent = path.parent
    grandparent = parent.parent
    return (not reg.LEVEL_RE.match(parent.name)) and bool(reg.LEVEL_RE.match(grandparent.name))


def iter_quest_files(
    root=None,
    *,
    skip_subdirs: Optional[set] = None,
    include_meta: bool = False,
    include_index_readmes: bool = False,
) -> Iterator[Path]:
    """Yield quest-tree ``.md`` files in deterministic (sorted) order.

    ``skip_subdirs`` defaults to the registry's ``SKIP_SUBDIRS`` (templates,
    docs, inventory). Pass an explicit set to widen/narrow the exclusion (e.g.
    the network graph historically also walks ``tools/`` and ``codex/`` because
    those carry permalinks). When ``include_meta`` is False (default), README /
    HOME / ALL_CAPS report files are skipped — except that
    ``include_index_readmes`` re-admits multi-file quest *hub* READMEs
    (``0000/bashcrawl/README.md``), which are real linkable nodes.
    """
    base = Path(root) if root else QUESTS_DIR
    if not base.is_absolute():
        base = (REPO_ROOT / base).resolve()
    skip = reg.SKIP_SUBDIRS if skip_subdirs is None else skip_subdirs
    for md in sorted(base.rglob("*.md")):
        rel_parts = md.relative_to(base).parts[:-1]
        if any(part in skip for part in rel_parts):
            continue
        if not include_meta and is_meta_file(md):
            if include_index_readmes and is_quest_index_readme(md):
                yield md
            continue
        yield md


def load_quests(
    root=None,
    *,
    scored_only: bool = False,
    quests_only: bool = True,
    include_drafts: bool = True,
    skip_subdirs: Optional[set] = None,
) -> List[QuestDoc]:
    """Discover and parse quest documents under ``root``.

    * ``quests_only`` (default True): keep only pages with ``fmContentType: quest``.
    * ``scored_only``: keep only published (non-draft) quests.
    * ``include_drafts`` is ignored when ``scored_only`` is True.
    """
    out: List[QuestDoc] = []
    for path in iter_quest_files(root, skip_subdirs=skip_subdirs):
        doc = read_quest(path)
        if doc.fm_error:
            # Surface parse failures as documents with no frontmatter so the
            # caller can report them rather than silently dropping the file.
            out.append(doc)
            continue
        if quests_only and not doc.is_quest():
            continue
        if scored_only and not doc.is_scored():
            continue
        if not include_drafts and doc.is_draft():
            continue
        out.append(doc)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Code-snippet extraction (for "actually run the snippets" validation)
# ─────────────────────────────────────────────────────────────────────────────
# Languages whose fenced blocks are commands/programs an agent can RUN.
RUNNABLE_LANGS = {
    "bash", "sh", "shell", "zsh", "console", "shell-session", "sh-session",
    "python", "py", "python3", "javascript", "js", "node", "nodejs",
    "typescript", "ts", "ruby", "rb", "go", "golang", "rust", "rs",
    "sql", "powershell", "ps1", "fish",
}
# Languages that are config / markup / output — SHOWN, never executed.
NONRUNNABLE_LANGS = {
    "yaml", "yml", "json", "json5", "toml", "ini", "markdown", "md", "mdx",
    "text", "txt", "plaintext", "mermaid", "html", "xml", "liquid", "handlebars",
    "css", "scss", "less", "diff", "patch", "csv", "tsv", "dockerfile", "docker",
    "makefile", "make", "gitignore", "env", "dotenv", "properties", "log",
    "http", "graphql", "regex", "ascii", "",
}


@dataclass
class CodeBlock:
    """A fenced code block lifted from a quest body."""
    lang: str
    code: str
    runnable: bool
    line: int  # 1-based line of the opening fence in the body


def is_runnable_lang(lang: str) -> bool:
    """Whether a fenced-block language tag denotes something runnable.

    Known runnable → True; known display/config → False; unknown/empty → False
    (conservative: don't claim a fragment is runnable when we can't tell)."""
    return (lang or "").lower() in RUNNABLE_LANGS


def extract_code_blocks(body: str) -> List[CodeBlock]:
    """Return the TOP-LEVEL fenced code blocks in ``body``, in order.

    A block opens on a ```/~~~ fence (optionally with a language tag) and closes
    on a fence of at least the same length with no trailing text — so a longer
    fence used to *display* nested backticks is treated as content, not a close.
    This mirrors the fence handling in quest_validator's code-block check.
    """
    blocks: List[CodeBlock] = []
    in_block = False
    fence = ""
    ticks = 0
    lang = ""
    start = 0
    buf: List[str] = []
    for idx, line in enumerate((body or "").split("\n"), start=1):
        stripped = line.strip()
        m = re.match(r"^([`~]{3,})(.*)$", stripped)
        if not in_block:
            if m:
                fence = m.group(1)[0]
                ticks = len(m.group(1))
                info = m.group(2).strip()
                lang = info.split()[0].lower() if info else ""
                start, buf, in_block = idx, [], True
        else:
            # Close only on the SAME fence char, length ≥ opener, and no info text.
            if m and m.group(1)[0] == fence and len(m.group(1)) >= ticks and not m.group(2).strip():
                blocks.append(CodeBlock(lang=lang, code="\n".join(buf),
                                        runnable=is_runnable_lang(lang), line=start))
                in_block = False
            else:
                buf.append(line)
    if in_block:  # unclosed fence — keep what we captured
        blocks.append(CodeBlock(lang=lang, code="\n".join(buf),
                                runnable=is_runnable_lang(lang), line=start))
    return blocks


def runnable_snippets(body: str) -> List[CodeBlock]:
    """The subset of code blocks an agent should attempt to run."""
    return [b for b in extract_code_blocks(body) if b.runnable]


def snippet_summary(body: str) -> Dict:
    """A compact, deterministic inventory of a quest's code blocks.

    Returns {total, runnable, by_lang: {lang: count}} — used to tell the execute
    agent what to run and to report execution coverage.
    """
    blocks = extract_code_blocks(body)
    by_lang: Dict[str, int] = {}
    for b in blocks:
        by_lang[b.lang or "(none)"] = by_lang.get(b.lang or "(none)", 0) + 1
    return {
        "total": len(blocks),
        "runnable": sum(1 for b in blocks if b.runnable),
        "by_lang": dict(sorted(by_lang.items())),
    }


if __name__ == "__main__":
    # Smoke test: parse the whole corpus and report shape.
    docs = load_quests(quests_only=False)
    quests = [d for d in docs if d.is_quest()]
    broken = [d for d in docs if d.fm_error]
    print(f"quest-tree files scanned : {len(docs)}")
    print(f"  fmContentType == quest : {len(quests)}")
    print(f"  scored (published)     : {sum(1 for d in quests if d.is_scored())}")
    print(f"  drafts                 : {sum(1 for d in quests if d.is_draft())}")
    print(f"  frontmatter errors     : {len(broken)}")
    for d in broken:
        print(f"    ! {d.rel_path}: {d.fm_error}")
