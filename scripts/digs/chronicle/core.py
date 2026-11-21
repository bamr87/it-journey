"""Paths, ledger storage and the manifest for the repository chronicle.

The ledger is the durable record of what the chronicle has already read. Every
commit is processed once: its deterministic facts land in a month shard under
``commits/``, its AI reading in the matching shard under ``annotations/``, and a
re-run skips anything already filed. Shards are JSON Lines sorted by commit
time, so a closed month never changes and a re-run only rewrites the shards
that gained a line.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Iterable, Iterator

TOOL_VERSION = "1.0.0"
SCHEMA = "chronicle/v1"
ROOT = Path(__file__).resolve().parents[3]  # the it-journey checkout
DEFAULT_LEDGER_ROOT = ROOT / "docs" / "git-archaeology" / "chronicle"
DEFAULT_CACHE_ROOT = ROOT / ".cache" / "chronicle"


def git(repo: Path, *args: str, input_bytes: bytes | None = None) -> bytes:
    """Run git in ``repo`` and return stdout bytes; raise with stderr on failure."""
    cmd = ["git", "-C", str(repo), "-c", "core.quotePath=false", *args]
    res = subprocess.run(cmd, input=input_bytes, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:3])} failed: {res.stderr.decode(errors='replace').strip()}")
    return res.stdout


def repo_slug(repo: Path) -> str:
    """``owner/name`` from the origin URL, falling back to the directory name."""
    try:
        url = git(repo, "remote", "get-url", "origin").decode().strip()
    except RuntimeError:
        url = ""
    m = re.search(r"[/:]([^/:]+)/([^/]+?)(?:\.git)?/?$", url)
    if m:
        return f"{m.group(1)}/{m.group(2)}"
    return f"local/{repo.resolve().name}"


def default_ref(repo: Path) -> str:
    for ref in ("origin/main", "origin/master", "main", "master"):
        try:
            git(repo, "rev-parse", "--verify", "--quiet", ref + "^{commit}")
            return ref
        except RuntimeError:
            continue
    return "HEAD"


def month_of(iso: str) -> str:
    """UTC ``YYYY-MM`` of an ISO-8601 timestamp."""
    t = dt.datetime.fromisoformat(iso)
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m")


def stable_hash(obj) -> str:
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


class Ledger:
    """One repository's chronicle: commit facts, AI annotations, derived records."""

    def __init__(self, root: Path, slug: str):
        self.slug = slug
        owner, name = slug.split("/", 1)
        self.dir = root / owner / name
        self.commits_dir = self.dir / "commits"
        self.ann_dir = self.dir / "annotations"
        self.manifest_path = self.dir / "manifest.json"

    # ------------------------------------------------------------------ io
    @staticmethod
    def _read_jsonl(path: Path) -> Iterator[dict]:
        if not path.exists():
            return
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    yield json.loads(line)

    @staticmethod
    def _write_jsonl(path: Path, rows: Iterable[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
        os.replace(tmp, path)

    def _shards(self, base: Path) -> list[Path]:
        return sorted(base.glob("*.jsonl")) if base.is_dir() else []

    @staticmethod
    def _sha_key(row: dict) -> str:
        return row["sha"]

    def _load(self, base: Path, key=None) -> dict[str, dict]:
        key = key or self._sha_key
        out: dict[str, dict] = {}
        for shard in self._shards(base):
            for row in self._read_jsonl(shard):
                out[key(row)] = row
        return out

    def _merge(self, base: Path, rows: list[dict], key_time: str, key=None) -> int:
        """File ``rows`` into month shards; an existing key is never overwritten."""
        key = key or self._sha_key
        by_month: dict[str, list[dict]] = {}
        for row in rows:
            by_month.setdefault(month_of(row[key_time]), []).append(row)
        added = 0
        for month, new in by_month.items():
            path = base / f"{month}.jsonl"
            existing = {key(r): r for r in self._read_jsonl(path)}
            fresh = [r for r in new if key(r) not in existing]
            if not fresh:
                continue
            added += len(fresh)
            merged = list(existing.values()) + fresh
            merged.sort(key=lambda r: (r.get(key_time, ""), key(r)))
            self._write_jsonl(path, merged)
        return added

    # ---------------------------------------------------------- commits
    def commits(self) -> dict[str, dict]:
        return self._load(self.commits_dir)

    def add_commits(self, rows: list[dict]) -> int:
        return self._merge(self.commits_dir, rows, "ct")

    # ------------------------------------------------------ annotations
    def annotations(self) -> dict[str, dict]:
        return self._load(self.ann_dir)

    def add_annotations(self, rows: list[dict]) -> int:
        return self._merge(self.ann_dir, rows, "ct")

    # ----------------------------------------------------------- content
    # One record per (commit, path) for every article version on the mainline,
    # and one topic reading per article id.
    @staticmethod
    def version_key(row: dict) -> str:
        return row["sha"] + ":" + row["p"]

    @staticmethod
    def article_key(row: dict) -> str:
        return row["aid"]

    def versions(self) -> dict[str, dict]:
        return self._load(self.dir / "content" / "versions", self.version_key)

    def add_versions(self, rows: list[dict]) -> int:
        return self._merge(self.dir / "content" / "versions", rows, "ct", self.version_key)

    def article_topics(self) -> dict[str, dict]:
        return self._load(self.dir / "content" / "topics", self.article_key)

    def add_article_topics(self, rows: list[dict]) -> int:
        return self._merge(self.dir / "content" / "topics", rows, "born", self.article_key)

    # --------------------------------------------------------- documents
    def read_doc(self, name: str) -> dict | None:
        path = self.dir / name
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None

    def write_doc(self, name: str, doc: dict) -> None:
        path = self.dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    def manifest(self) -> dict:
        return self.read_doc("manifest.json") or {"schema": SCHEMA, "repository": self.slug, "runs": []}

    def save_manifest(self, doc: dict) -> None:
        doc["schema"] = SCHEMA
        doc["repository"] = self.slug
        doc["toolVersion"] = TOOL_VERSION
        doc["runs"] = doc.get("runs", [])[-25:]
        self.write_doc("manifest.json", doc)
