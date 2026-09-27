#!/usr/bin/env python3
"""List bamr87 repositories and dig coverage. Does not choose a target."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO_RX = re.compile(r"repo_url:\s+https://github\.com/(bamr87/[A-Za-z0-9._-]+)")
FIELD_RX = re.compile(r"^(repository|range_start|range_end):\s+(\S+)\s*$", re.M)


def registry_repos(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return sorted(set(REPO_RX.findall(text)))


def covered(digs: Path) -> list[dict[str, str]]:
    rows = []
    if not digs.is_dir():
        return rows
    for page in sorted(digs.glob("*.md")):
        if page.name == "index.md":
            continue
        fields = dict(FIELD_RX.findall(page.read_text(encoding="utf-8")))
        if "repository" in fields:
            rows.append({"page": str(page.relative_to(digs.parent.parent)), **fields})
    return rows


def main() -> int:
    registry = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / ".." / ".." / "_data" / "projects.yml"
    payload = {
        "since": "2020-01-01",
        "max_commits": 40,
        "repositories": registry_repos(registry),
        "covered": covered(ROOT / "pages" / "_digs"),
        "selection": "agent",
    }
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
