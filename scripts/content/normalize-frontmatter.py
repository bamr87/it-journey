#!/usr/bin/env python3
"""
normalize-frontmatter.py — apply collection-aware frontmatter normalization
across the IT-Journey content tree.

Idempotent. Dry-run by default; pass --apply to write changes.

What it does (only when the existing value is broken or missing):

- Detects content type from path (posts, quests, docs, notes, about, quickstart,
  hobbies, notebooks, index-hub, post-readme).
- Coerces string `categories` / `tags` to YAML lists.
- Normalizes `date` and `lastmod` to ISO 8601 with milliseconds
  (`YYYY-MM-DDTHH:MM:SS.000Z`).
- Bumps `lastmod` to today when --touch-lastmod is set.
- For quests: flattens a list-shaped `keywords` into `{primary, secondary}`.
- For about/hobbies: coerces `draft: "published"` / `"draft"` to a boolean.
- For wargame docs missing `description`: derives a short description from
  the first prose paragraph (capped at 155 chars).
- Adds `draft: false` to publishable posts/docs missing it.

What it intentionally does NOT do:

- Rewrite prose, body content, or descriptions that exist.
- Touch frontmatter on category index files (`2000-01-01-index.md`) beyond the
  shared shape rules — see `.github/instructions/index-hub.instructions.md`.
- Touch frontmatter on level READMEs in `pages/_quests/<XXXX>/README.md`.

Usage:
    python3 scripts/content/normalize-frontmatter.py pages/                 # dry-run all
    python3 scripts/content/normalize-frontmatter.py pages/_posts --apply   # write
    python3 scripts/content/normalize-frontmatter.py pages/_quests --apply --touch-lastmod
    python3 scripts/content/normalize-frontmatter.py --report report.json pages/

Exit codes:
    0  no changes needed (or all changes applied cleanly)
    1  unparseable YAML / IO error
    2  changes pending in dry-run mode (use --apply to write)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(1)


FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")
SIMPLE_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
FILENAME_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")
DESC_MAX = 155

QUEST_REQUIRED = {
    "title", "description", "date", "level", "difficulty", "estimated_time",
    "primary_technology", "quest_type", "skill_focus", "learning_style",
    "quest_series", "author", "layout", "keywords", "permalink", "fmContentType",
}
POST_REQUIRED = {"title", "description", "date", "categories"}
DOC_REQUIRED = {"title", "description"}
NOTE_REQUIRED = {"title"}


@dataclass
class FileChange:
    path: str
    content_type: str
    changed_fields: list[str] = field(default_factory=list)
    skipped_reason: str | None = None
    error: str | None = None


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def detect_content_type(path: Path) -> str:
    parts = path.parts
    name = path.name
    if "_posts" in parts:
        if name == "2000-01-01-index.md":
            return "index-hub"
        if name == "README.md":
            return "post-readme"
        return "posts"
    if "_quests" in parts:
        if name == "README.md":
            return "quest-readme"
        if "templates" in parts:
            return "quest-template"
        if "docs" in parts:
            return "quest-docs"
        return "quests"
    if "_docs" in parts:
        if "wargames" in parts:
            return "docs-wargame"
        return "docs"
    if "_notes" in parts:
        return "notes"
    if "_about" in parts:
        return "about"
    if "_quickstart" in parts:
        return "quickstart"
    if "_hobbies" in parts:
        return "hobbies"
    if "_notebooks" in parts:
        return "notebooks"
    if "_drafts" in parts:
        return "drafts"
    return "other"


def parse_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """Return (frontmatter_dict, body, error_message)."""
    m = FM_RE.match(text)
    if not m:
        return None, text, "no frontmatter delimiters"
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return None, text, f"yaml parse error: {e}"
    if not isinstance(fm, dict):
        return None, text, "frontmatter not a mapping"
    return fm, m.group(2), None


def serialize_frontmatter(fm: dict, body: str) -> str:
    yaml_str = yaml.safe_dump(
        fm,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1000,
    )
    return f"---\n{yaml_str}---\n{body}"


def coerce_to_list(value: Any) -> list | None:
    """Return a list if the value can be coerced, else None."""
    if value is None:
        return None
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        if not value.strip():
            return None
        if "," in value:
            return [s.strip() for s in value.split(",") if s.strip()]
        return [value.strip()]
    return None


def normalize_iso_date(value: Any) -> str | None:
    """Return ISO 8601 string with millis if value is a recognizable date."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    if isinstance(value, str):
        if ISO_RE.match(value):
            return value
        m = SIMPLE_DATE_RE.match(value)
        if m:
            return f"{m.group(1)}-{m.group(2)}-{m.group(3)}T00:00:00.000Z"
        # Try common variants — defer to fromisoformat for liberal parsing.
        cleaned = value.replace("Z", "+00:00").strip()
        try:
            dt = datetime.fromisoformat(cleaned)
            return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        except ValueError:
            return None
    return None


def first_prose_paragraph(body: str) -> str | None:
    """First prose paragraph from a markdown body, capped at DESC_MAX chars."""
    in_code = False
    paragraph: list[str] = []
    for raw in body.splitlines():
        line = raw.rstrip()
        if line.startswith("```") or line.startswith("~~~"):
            in_code = not in_code
            if paragraph:
                break
            continue
        if in_code:
            continue
        stripped = line.lstrip()
        if not stripped:
            if paragraph:
                break
            continue
        if stripped.startswith(("#", ">", "|", "<", "{", "}", "[", "]", '"')):
            continue
        if re.match(r"^[-*+]\s", stripped):
            continue
        if re.match(r"^\d+\.\s", stripped):
            continue
        paragraph.append(stripped)
    if not paragraph:
        return None
    text = " ".join(paragraph)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_`]+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return None
    if len(text) > DESC_MAX:
        cut = text[: DESC_MAX - 1].rsplit(" ", 1)[0]
        text = cut.rstrip(".,;:") + "…"
    return text


def normalize_keywords_for_quest(value: Any) -> tuple[Any, bool]:
    """For quests, keywords must be `{primary: [...], secondary: [...]}`."""
    if isinstance(value, dict):
        if "primary" in value and isinstance(value["primary"], list):
            return value, False
    if isinstance(value, list) and value:
        half = max(1, len(value) // 2)
        return {"primary": value[:half], "secondary": value[half:]}, True
    return value, False


def normalize_draft(value: Any) -> tuple[Any, bool]:
    if isinstance(value, bool):
        return value, False
    if isinstance(value, str):
        lower = value.strip().lower()
        if lower in {"true", "published", "publish"}:
            return False, True  # published = not draft
        if lower in {"false", "draft", "unpublished"}:
            return True, True
    return value, False


def normalize_frontmatter(
    fm: dict,
    body: str,
    content_type: str,
    touch_lastmod: bool,
) -> tuple[dict, list[str]]:
    """Apply normalization rules; return (new_fm, list of changed field names)."""
    changes: list[str] = []
    fm = dict(fm)  # shallow copy

    # Coerce categories / tags to lists for all content types.
    for field_name in ("categories", "tags"):
        if field_name in fm:
            coerced = coerce_to_list(fm[field_name])
            if coerced is not None and coerced != fm[field_name]:
                fm[field_name] = coerced
                changes.append(field_name)

    # Normalize date / lastmod / publishDate / updatedDate to ISO 8601 with millis.
    for field_name in ("date", "lastmod", "publishDate", "updatedDate"):
        if field_name in fm and fm[field_name] is not None:
            new_val = normalize_iso_date(fm[field_name])
            if new_val and new_val != fm[field_name]:
                fm[field_name] = new_val
                changes.append(field_name)

    # Bump lastmod if requested.
    if touch_lastmod:
        new_ts = now_iso()
        if fm.get("lastmod") != new_ts:
            fm["lastmod"] = new_ts
            if "lastmod" not in changes:
                changes.append("lastmod")

    # Collection-specific rules.
    if content_type == "quests":
        if "keywords" in fm:
            new_kw, did_change = normalize_keywords_for_quest(fm["keywords"])
            if did_change:
                fm["keywords"] = new_kw
                changes.append("keywords")
        if "fmContentType" not in fm:
            fm["fmContentType"] = "quest"
            changes.append("fmContentType")

    if content_type == "about":
        if "draft" in fm:
            new_draft, did_change = normalize_draft(fm["draft"])
            if did_change:
                fm["draft"] = new_draft
                changes.append("draft")

    # Derive a description from the first prose paragraph for content types
    # where the field is missing or trivially short (<40 chars).
    derive_desc_types = {
        "docs-wargame", "docs", "notes", "about", "quickstart",
        "notebooks", "hobbies", "drafts",
    }
    if content_type in derive_desc_types:
        desc = fm.get("description") or ""
        if not isinstance(desc, str) or len(desc.strip()) < 40:
            derived = first_prose_paragraph(body)
            if derived and len(derived) >= 40:
                fm["description"] = derived
                changes.append("description")

    # Add draft: false for publishable posts/docs when the field is absent.
    if content_type in {"posts", "docs", "docs-wargame", "quickstart", "notes"}:
        if "draft" not in fm:
            fm["draft"] = False
            changes.append("draft")

    return fm, changes


def process_file(
    path: Path,
    repo_root: Path,
    apply: bool,
    touch_lastmod: bool,
) -> FileChange:
    try:
        rel = str(path.relative_to(repo_root))
    except ValueError:
        rel = str(path)
    content_type = detect_content_type(path)
    try:
        text = path.read_text(encoding="utf-8")
    except (IOError, UnicodeDecodeError) as e:
        return FileChange(rel, content_type, error=f"read failed: {e}")

    fm, body, err = parse_frontmatter(text)
    if err or fm is None:
        return FileChange(rel, content_type, skipped_reason=f"frontmatter: {err}")

    new_fm, changes = normalize_frontmatter(fm, body, content_type, touch_lastmod)
    if not changes:
        return FileChange(rel, content_type)

    if apply:
        new_text = serialize_frontmatter(new_fm, body)
        path.write_text(new_text, encoding="utf-8")
    return FileChange(rel, content_type, changed_fields=changes)


def iter_markdown_files(target: Path, repo_root: Path) -> list[Path]:
    if target.is_file():
        return [target]
    files: list[Path] = []
    for p in target.rglob("*.md"):
        # Skip _site, vendor, etc.
        if any(part in p.parts for part in ("_site", "node_modules", "vendor", ".venv")):
            continue
        files.append(p)
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collection-aware frontmatter normalizer for IT-Journey."
    )
    parser.add_argument("path", type=Path, help="File or directory to process.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes (default: dry-run preview).",
    )
    parser.add_argument(
        "--touch-lastmod",
        action="store_true",
        help="Bump lastmod to current UTC timestamp on every changed file.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Write a JSON report of all changes to this path.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-file output; print only summary.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    target = args.path.resolve()
    if not target.exists():
        print(f"ERROR: path does not exist: {target}", file=sys.stderr)
        return 1

    files = iter_markdown_files(target, repo_root)
    results: list[FileChange] = []
    error_count = 0
    change_count = 0
    skipped_count = 0

    for path in files:
        result = process_file(path, repo_root, args.apply, args.touch_lastmod)
        results.append(result)
        if result.error:
            error_count += 1
            if not args.quiet:
                print(f"  ERROR  {result.path}: {result.error}")
        elif result.skipped_reason:
            skipped_count += 1
            if not args.quiet:
                print(f"  SKIP   {result.path}: {result.skipped_reason}")
        elif result.changed_fields:
            change_count += 1
            if not args.quiet:
                tag = "APPLY" if args.apply else "WOULD"
                fields = ",".join(result.changed_fields)
                print(f"  {tag}  {result.path} ({result.content_type}) [{fields}]")

    total = len(files)
    print()
    print(f"Total markdown files:        {total}")
    print(f"Files with changes:          {change_count}")
    print(f"Files skipped (no fm/parse): {skipped_count}")
    print(f"Files with read errors:      {error_count}")

    if args.report:
        report = {
            "timestamp": now_iso(),
            "mode": "apply" if args.apply else "dry-run",
            "touch_lastmod": args.touch_lastmod,
            "target": str(target.relative_to(repo_root)),
            "summary": {
                "total_files": total,
                "changed_files": change_count,
                "skipped_files": skipped_count,
                "error_files": error_count,
            },
            "files": [asdict(r) for r in results if r.changed_fields or r.error or r.skipped_reason],
        }
        report_path = args.report.resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        try:
            display = report_path.relative_to(repo_root)
        except ValueError:
            display = report_path
        print(f"Report written to {display}")

    if error_count:
        return 1
    if change_count and not args.apply:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
