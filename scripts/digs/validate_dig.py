#!/usr/bin/env python3
"""Validate one dig page against the collection contract."""
import re
import sys
from datetime import date
from pathlib import Path

REQUIRED = (
    "title", "description", "date", "lastmod", "author", "excerpt", "permalink",
    "repository", "range_start", "range_end", "start_sha", "end_sha", "commit_count",
)
SHA = re.compile(r"^[0-9a-f]{40}$")
REPO = re.compile(r"^bamr87/[A-Za-z0-9._-]+$")


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        raise ValueError("missing front matter")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def validate(path: Path, allowed: set[str] | None = None) -> list[str]:
    text = path.read_text(encoding="utf-8")
    fields = frontmatter(text)
    errors = [f"missing {key}" for key in REQUIRED if not fields.get(key)]
    description = fields.get("description", "")
    if description and not 80 <= len(description) <= 160:
        errors.append(f"description length {len(description)} outside 80-160")
    if fields.get("permalink") and not re.fullmatch(r"/digs/[a-z0-9-]+/", fields["permalink"]):
        errors.append("permalink must be /digs/<slug>/")
    if fields.get("repository") and not REPO.fullmatch(fields["repository"]):
        errors.append("repository must be bamr87/<name>")
    if allowed is not None and fields.get("repository") not in allowed:
        errors.append("repository is not in the candidate brief")
    try:
        start = date.fromisoformat(fields.get("range_start", ""))
        end = date.fromisoformat(fields.get("range_end", ""))
        if start < date(2020, 1, 1) or end < start:
            errors.append("range must start on or after 2020-01-01 and end on or after the start")
    except ValueError:
        errors.append("range dates must be YYYY-MM-DD")
    for key in ("start_sha", "end_sha"):
        if fields.get(key) and not SHA.fullmatch(fields[key]):
            errors.append(f"{key} must be a full lowercase SHA")
    try:
        count = int(fields.get("commit_count", "0"))
        if not 1 <= count <= 40:
            errors.append("commit_count must be 1-40")
    except ValueError:
        errors.append("commit_count must be an integer")
    if fields.get("voice_profile") != "git-dig":
        errors.append("voice_profile must be git-dig")
    for heading in ("## Scope", "## Facts", "## Inferences", "## Limits", "## Retrospective"):
        if heading not in text:
            errors.append(f"body needs {heading}")
    return errors


def main() -> int:
    errors = validate(Path(sys.argv[1]))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
