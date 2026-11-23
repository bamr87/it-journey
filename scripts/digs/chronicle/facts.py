"""Deterministic readings of a commit: language, layer, actor, conventional type.

Nothing here guesses. A path's language comes from its name, an actor from the
author and the trailers the commit actually carries, a conventional type from
the subject's prefix. Anything that needs judgement is left to ``ai.py``.
"""
from __future__ import annotations

import re
from pathlib import PurePosixPath

# extension -> (language, layer). Layers group languages for the stack view:
# content, markup, style, code, config, data, assets, docs-tooling, other.
EXT = {
    ".md": ("Markdown", "content"), ".markdown": ("Markdown", "content"), ".mdx": ("MDX", "content"),
    ".txt": ("Text", "content"), ".rst": ("reStructuredText", "content"), ".adoc": ("AsciiDoc", "content"),
    ".ipynb": ("Notebook", "content"),
    ".html": ("HTML", "markup"), ".htm": ("HTML", "markup"), ".liquid": ("Liquid", "markup"),
    ".xml": ("XML", "markup"), ".svg": ("SVG", "assets"),
    ".css": ("CSS", "style"), ".scss": ("SCSS", "style"), ".sass": ("Sass", "style"), ".less": ("Less", "style"),
    ".js": ("JavaScript", "code"), ".mjs": ("JavaScript", "code"), ".cjs": ("JavaScript", "code"),
    ".jsx": ("JavaScript", "code"), ".ts": ("TypeScript", "code"), ".tsx": ("TypeScript", "code"),
    ".py": ("Python", "code"), ".rb": ("Ruby", "code"), ".rake": ("Ruby", "code"), ".gemspec": ("Ruby", "code"),
    ".sh": ("Shell", "code"), ".bash": ("Shell", "code"), ".zsh": ("Shell", "code"), ".ps1": ("PowerShell", "code"),
    ".go": ("Go", "code"), ".rs": ("Rust", "code"), ".java": ("Java", "code"), ".kt": ("Kotlin", "code"),
    ".c": ("C", "code"), ".h": ("C", "code"), ".cpp": ("C++", "code"), ".cs": ("C#", "code"),
    ".php": ("PHP", "code"), ".swift": ("Swift", "code"), ".lua": ("Lua", "code"), ".gd": ("GDScript", "code"),
    ".sql": ("SQL", "code"), ".r": ("R", "code"), ".pl": ("Perl", "code"), ".bat": ("Batch", "code"),
    ".yml": ("YAML", "config"), ".yaml": ("YAML", "config"), ".toml": ("TOML", "config"),
    ".ini": ("INI", "config"), ".cfg": ("INI", "config"), ".env": ("Env", "config"),
    ".json": ("JSON", "data"), ".jsonl": ("JSON", "data"), ".csv": ("CSV", "data"), ".tsv": ("CSV", "data"),
    ".lock": ("Lockfile", "config"),
    ".png": ("Image", "assets"), ".jpg": ("Image", "assets"), ".jpeg": ("Image", "assets"),
    ".gif": ("Image", "assets"), ".webp": ("Image", "assets"), ".ico": ("Image", "assets"),
    ".avif": ("Image", "assets"), ".bmp": ("Image", "assets"),
    ".mp4": ("Video", "assets"), ".webm": ("Video", "assets"), ".mov": ("Video", "assets"),
    ".mp3": ("Audio", "assets"), ".wav": ("Audio", "assets"),
    ".woff": ("Font", "assets"), ".woff2": ("Font", "assets"), ".ttf": ("Font", "assets"), ".otf": ("Font", "assets"),
    ".pdf": ("PDF", "assets"), ".zip": ("Archive", "assets"),
}
NAMES = {
    "dockerfile": ("Dockerfile", "config"), "makefile": ("Makefile", "code"), "gemfile": ("Ruby", "config"),
    "rakefile": ("Ruby", "code"), "procfile": ("Config", "config"), "license": ("Text", "content"),
    ".gitignore": ("Git", "config"), ".gitattributes": ("Git", "config"), ".gitmodules": ("Git", "config"),
    "cname": ("Config", "config"), ".editorconfig": ("Config", "config"), ".nojekyll": ("Config", "config"),
}
LAYERS = ("content", "markup", "style", "code", "config", "data", "assets", "other")

BOT_NAMES = re.compile(r"(\[bot\]$|^dependabot|^github-actions|^renovate|-bot$|^bot$|^actions-user$)", re.I)
AI_TRAILER = re.compile(
    r"(co-authored-by:\s*(claude|copilot|chatgpt|gpt|codex|cursor|grok|gemini)[^\n]*|"
    r"generated with \[?claude code|claude\.ai/code|🤖 generated with|copilot-swe-agent)", re.I)
AI_AUTHORS = re.compile(r"^(claude|copilot|copilot-swe-agent|codex|devin|grok)\b", re.I)
CONVENTIONAL = re.compile(r"^(?P<type>[a-zA-Z]+)(?:\((?P<scope>[^)]{1,40})\))?(?P<bang>!)?:\s")


def classify_path(path: str) -> tuple[str, str]:
    """(language, layer) for a path, by extension or well-known file name."""
    p = PurePosixPath(path)
    name = p.name.lower()
    if name in NAMES:
        return NAMES[name]
    if name.startswith("dockerfile"):
        return NAMES["dockerfile"]
    ext = p.suffix.lower()
    if ext in EXT:
        return EXT[ext]
    if path.startswith(".github/workflows/"):
        return ("YAML", "config")
    return ("Other", "other")


def area_of(path: str) -> str:
    """The top-level directory, or ``/`` for a root file."""
    return path.split("/", 1)[0] if "/" in path else "/"


def conventional(subject: str) -> dict | None:
    m = CONVENTIONAL.match(subject or "")
    if not m:
        return None
    out = {"type": m.group("type").lower()}
    if m.group("scope"):
        out["scope"] = m.group("scope")
    if m.group("bang") or "BREAKING CHANGE" in subject:
        out["breaking"] = True
    return out


def actor(author: str, committer: str, body: str) -> str:
    """``bot`` for automation accounts, ``ai`` for agent-authored commits,
    ``ai-assisted`` for human commits carrying an AI co-author trailer, else ``human``."""
    if BOT_NAMES.search(author or ""):
        return "bot"
    if AI_AUTHORS.search(author or ""):
        return "ai"
    if AI_TRAILER.search(body or ""):
        return "ai-assisted"
    return "human"


def summarize_files(files: list[dict]) -> dict:
    """Per-language and per-area line deltas for one commit."""
    langs: dict[str, list[int]] = {}
    areas: dict[str, list[int]] = {}
    layers: dict[str, list[int]] = {}
    for f in files:
        lang, layer = classify_path(f["p"])
        a, d = f.get("a") or 0, f.get("d") or 0
        for bucket, key in ((langs, lang), (areas, area_of(f["p"])), (layers, layer)):
            row = bucket.setdefault(key, [0, 0, 0])
            row[0] += 1
            row[1] += a
            row[2] += d
    return {"langs": langs, "areas": areas, "layers": layers}
