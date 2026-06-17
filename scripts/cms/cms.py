#!/usr/bin/env python3
"""
cms.py — IT-Journey AI-augmented CMS engine.

A thin orchestration + indexing layer over the content tree. It does NOT
duplicate fixes or validation logic that already lives in the repo; it
aggregates a full-coverage *view* of all content and turns it into:

  - .cms/index/content-index.json   one record per content file
  - .cms/index/summary.json         repo-wide rollup
  - .cms/schema/content-schema.json  consolidated canonical field schema
  - .cms/reports/<date>.md          human-readable daily analysis
  - .cms/worklists/<date>.md        prioritized batch for the cms-curator loop

Subcommands:
  index     scan pages/, build the index + summary + schema
  analyze   write the daily Markdown analysis report (implies index)
  plan      write the prioritized worklist (mechanical vs substantive)
  status    print a terminal dashboard
  all       index + analyze + plan

Design notes:
  * Mechanical fixes are applied elsewhere by scripts/content/normalize-frontmatter.py
    (`make content-normalize-apply`). This engine only *detects and classifies*.
  * Output lives under .cms/ (a dot-dir) so Jekyll ignores it and the future
    VS Code extension reads it at a stable path.

Author: IT-Journey Team   |   Part of the AI-augmented CMS foundation.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
CONFIG_PATH = REPO_ROOT / ".cms" / "config.yml"
FRONTMATTER_JSON = REPO_ROOT / "frontmatter.json"

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)
ISO_MS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")
HEADING_RE = re.compile(r"^#{1,6}\s+\S", re.MULTILINE)
CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)


# --------------------------------------------------------------------------- #
# Issue catalog — single source of truth for severity + remediation lane.
# lane: "mechanical" = deterministic, safe to auto-merge after green CI.
#       "substantive" = needs authoring/judgment, goes to a reviewed PR.
# --------------------------------------------------------------------------- #
@dataclass
class Issue:
    kind: str
    severity: str           # error | warning | info
    field: str
    message: str
    lane: str               # mechanical | substantive
    suggestion: Optional[str] = None


# Missing required fields are always SUBSTANTIVE: the mechanical lane only runs
# format normalization (scripts/content/normalize-frontmatter.py), which does not
# reliably *populate* missing values across every collection. Adding a value is a
# judgment call (what author? what categories?) and belongs in the reviewed lane.
# These fields, when missing, are merely warnings (lower urgency) rather than
# errors, because they have site-level defaults and rarely block rendering.
LOW_URGENCY_REQUIRED = {"author", "date", "draft", "lastmod"}


@dataclass
class FileRecord:
    path: str
    collection: str
    fm_content_type: str
    is_notebook: bool = False
    frontmatter_present: bool = True
    read_only: bool = False
    generated: bool = False
    structural: bool = False
    draft: Optional[bool] = None
    title: Optional[str] = None
    description_len: int = 0
    title_len: int = 0
    word_count: int = 0
    heading_count: int = 0
    lastmod: Optional[str] = None
    date: Optional[str] = None
    age_days: Optional[int] = None
    freshness: str = "unknown"
    broken_links: int = 0
    health: int = 0
    issues: list = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i["severity"] == "error")

    @property
    def mechanical_count(self) -> int:
        return sum(1 for i in self.issues if i["lane"] == "mechanical")

    @property
    def substantive_count(self) -> int:
        return sum(1 for i in self.issues if i["lane"] == "substantive")


# --------------------------------------------------------------------------- #
# Config + schema loading
# --------------------------------------------------------------------------- #
def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_frontmatter_schema() -> dict:
    """Read frontmatter.json content-type field definitions (best effort)."""
    if not FRONTMATTER_JSON.exists():
        return {}
    try:
        fm = json.loads(FRONTMATTER_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    out = {}
    for ct in fm.get("frontMatter.taxonomy.contentTypes", []):
        out[ct["name"]] = ct.get("fields", [])
    return out


# --------------------------------------------------------------------------- #
# Frontmatter / body parsing
# --------------------------------------------------------------------------- #
def parse_file(p: Path) -> tuple[Optional[dict], str, Optional[str]]:
    try:
        content = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return None, "", f"read error: {e}"
    m = FM_RE.match(content)
    if not m:
        return None, content, "no frontmatter"
    try:
        fm = yaml.safe_load(m.group(1))
    except (yaml.YAMLError, ValueError) as e:
        # ValueError: PyYAML's timestamp constructor raises a bare ValueError on
        # out-of-range dates (e.g. 2024-13-45); it is NOT a yaml.YAMLError.
        return None, content, f"yaml error: {e}"
    if fm is None:
        return None, m.group(2), "empty frontmatter"
    if not isinstance(fm, dict):
        return None, m.group(2), "frontmatter not a mapping"
    return fm, m.group(2), None


def count_words(body: str) -> int:
    body = CODE_FENCE_RE.sub(" ", body)
    body = re.sub(r"\{%.*?%\}", " ", body, flags=re.DOTALL)   # liquid tags
    body = re.sub(r"[#>*_`\[\]()|-]", " ", body)
    return len([w for w in body.split() if any(c.isalpha() for c in w)])


def to_dt(val: Any) -> Optional[datetime]:
    if val is None:
        return None
    if isinstance(val, datetime):
        return val if val.tzinfo else val.replace(tzinfo=timezone.utc)
    if hasattr(val, "year") and not isinstance(val, str):   # date object
        return datetime(val.year, val.month, val.day, tzinfo=timezone.utc)
    s = str(val).strip().strip('"').strip("'")
    # Prefer fromisoformat (handles arbitrary fractional precision + offsets).
    iso = s[:-1] + "+00:00" if s.endswith("Z") else s
    try:
        dt = datetime.fromisoformat(iso)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        pass
    # Fallback: a leading YYYY-MM-DD. Guard against calendar-invalid values.
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        try:
            return datetime(int(m[1]), int(m[2]), int(m[3]), tzinfo=timezone.utc)
        except ValueError:
            return None
    return None


def is_iso_ms(val: Any) -> bool:
    return isinstance(val, str) and bool(ISO_MS_RE.match(val))


# --------------------------------------------------------------------------- #
# Classification helpers
# --------------------------------------------------------------------------- #
def collection_for(rel: str, cfg: dict) -> tuple[str, dict]:
    """Map a repo-relative path to its collection + collection config."""
    best, best_cfg, best_len = "pages", cfg["collections"]["pages"], -1
    for name, c in cfg["collections"].items():
        cpath = c["path"]
        if name == "pages":
            continue
        if rel.startswith(cpath + "/"):
            if len(cpath) > best_len:
                best, best_cfg, best_len = name, c, len(cpath)
    return best, best_cfg


def _glob_to_re(g: str) -> str:
    """Translate a glob (supporting recursive **) to a full-path regex."""
    out, i = [], 0
    while i < len(g):
        c = g[i]
        if c == "*":
            if g[i:i + 2] == "**":
                i += 2
                if g[i:i + 1] == "/":      # '**/' = zero or more whole segments
                    out.append("(?:[^/]+/)*")
                    i += 1
                else:                      # trailing/bare '**' = anything
                    out.append(".*")
                continue
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        elif c in ".()+|^$@%{}[]\\":
            out.append("\\" + c)
        else:
            out.append(c)
        i += 1
    return "^" + "".join(out) + "$"


_GLOB_CACHE: dict[str, re.Pattern] = {}


def glob_match(rel: str, globs: list[str]) -> bool:
    for g in globs:
        pat = _GLOB_CACHE.get(g)
        if pat is None:
            pat = _GLOB_CACHE[g] = re.compile(_glob_to_re(g))
        if pat.match(rel):
            return True
    return False


# --------------------------------------------------------------------------- #
# Per-file analysis
# --------------------------------------------------------------------------- #
def analyze_file(p: Path, cfg: dict, now: datetime,
                 link_map: dict, fresh: dict) -> FileRecord:
    rel = str(p.relative_to(REPO_ROOT))
    coll, ccfg = collection_for(rel, cfg)
    rec = FileRecord(path=rel, collection=coll,
                     fm_content_type=ccfg.get("fm_content_type", "default"))

    ro = cfg["read_only"]
    rec.read_only = glob_match(rel, ro.get("globs", []))
    rec.structural = glob_match(rel, ro.get("structural_globs", []))
    rec.generated = glob_match(rel, cfg["generated"].get("globs", []))

    if p.suffix == ".ipynb":
        rec.is_notebook = True
        rec.frontmatter_present = False
        rec.health = -1                     # not scored
        return rec

    whitelisted = rec.read_only or rec.structural or rec.generated
    fm, body, err = parse_file(p)
    if fm is None:
        rec.frontmatter_present = False
        if whitelisted:
            rec.health = 100        # templates/vendored/generated may lack frontmatter
            return rec
        rec.issues.append(asdict(Issue(
            "no_frontmatter", "error", "frontmatter",
            err or "missing frontmatter", "substantive",
            "Add a YAML frontmatter block")))
        rec.health = 0
        return rec

    # vendored detection via frontmatter markers
    for marker in ro.get("frontmatter_markers", []):
        if marker in fm:
            rec.read_only = True

    t = fm.get("title")
    if isinstance(t, str) and t.strip():
        rec.title = t
        rec.title_len = len(t)
    desc = fm.get("description")
    if isinstance(desc, str) and desc.strip():
        rec.description_len = len(desc)
    rec.draft = _coerce_draft(fm.get("draft"))
    rec.word_count = count_words(body)
    rec.heading_count = len(HEADING_RE.findall(body))

    # freshness
    lm = fm.get("lastmod") or fm.get("date")
    rec.lastmod = str(fm.get("lastmod")) if fm.get("lastmod") else None
    rec.date = str(fm.get("date")) if fm.get("date") else None
    dt = to_dt(lm)
    if dt:
        rec.age_days = max((now - dt).days, 0)
        rec.freshness = _freshness_bucket(rec.age_days, cfg)
    # enrich freshness from external report if our parse failed
    if rec.age_days is None and rel in fresh:
        rec.age_days = fresh[rel].get("days_since_update")
        rec.freshness = fresh[rel].get("status", "unknown")

    rec.broken_links = link_map.get(rel, 0)

    # effective required fields: quest-only extras apply solely to playable quests
    required = list(cfg["required_base"])
    extra = list(ccfg.get("required_extra", []))
    if rec.fm_content_type == "quest" and not _is_playable_quest(fm):
        extra = []
    required += extra

    # skip deep field checks on read-only / structural / generated content
    if not (rec.read_only or rec.structural or rec.generated):
        _check_fields(rec, fm, required, cfg)
        _check_seo(rec, fm, cfg)
        _check_structure(rec, cfg)
    if rec.broken_links:
        rec.issues.append(asdict(Issue(
            "broken_links", "warning", "body",
            f"{rec.broken_links} broken link(s) from last scan", "substantive",
            "Fix or remove dead links")))

    rec.health = _score(rec, required, cfg)
    return rec


def _is_playable_quest(fm: dict) -> bool:
    """A file under pages/_quests is a playable quest (needs quest fields) only
    if it carries quest typing. Hubs/index pages use fmContentType instead."""
    return (fm.get("fmContentType") == "quest" or "quest_type" in fm
            or "level" in fm)


def _coerce_draft(v: Any) -> Optional[bool]:
    if isinstance(v, bool):
        return v
    if v is None:
        return None
    s = str(v).strip().lower()
    if s in ("false", "published", "no"):
        return False
    if s in ("true", "draft", "in progress", "yes"):
        return True
    return None


def _freshness_bucket(age: int, cfg: dict) -> str:
    f = cfg["freshness"]
    if age <= f["fresh_max_days"]:
        return "fresh"
    if age <= f["aging_max_days"]:
        return "aging"
    if age <= f["stale_max_days"]:
        return "stale"
    return "critical"


def _empty(v: Any) -> bool:
    return v is None or (isinstance(v, str) and not v.strip()) or v == []


def _check_fields(rec: FileRecord, fm: dict, required: list, cfg: dict) -> None:
    for fld in required:
        if fld not in fm or _empty(fm.get(fld)):
            sev = "warning" if fld in LOW_URGENCY_REQUIRED else "error"
            rec.issues.append(asdict(Issue(
                f"missing_required:{fld}", sev, fld,
                f"missing/empty required field '{fld}'", "substantive",
                f"Set '{fld}'")))
    # shape checks (mechanical)
    for fld in ("categories", "tags"):
        if fld in fm and isinstance(fm[fld], str):
            rec.issues.append(asdict(Issue(
                f"{fld}_not_list", "warning", fld,
                f"'{fld}' is a string, should be a YAML list", "mechanical",
                "Run make content-normalize-apply")))
    for fld in ("date", "lastmod"):
        v = fm.get(fld)
        # Only a STRING can be a non-ISO value the normalizer rewrites. A bare
        # YAML date object (e.g. 2026-01-14) is already a valid date — not broken.
        if isinstance(v, str) and not is_iso_ms(v):
            rec.issues.append(asdict(Issue(
                f"{fld}_not_iso", "info", fld,
                f"'{fld}' not ISO-8601 with ms", "mechanical",
                "Run make content-normalize-apply")))
    if "draft" in fm and fm["draft"] is not None and not isinstance(fm["draft"], bool):
        # Coercing a non-boolean draft means interpreting intent (publication
        # state vs literal boolean); the normalizer only handles known state
        # strings and inverts "true"/"false". Treat as substantive — a human/
        # agent sets the intended value.
        rec.issues.append(asdict(Issue(
            "draft_not_boolean", "warning", "draft",
            f"draft is '{fm['draft']}', should be a boolean", "substantive",
            "Set draft to true/false for the intended publication state")))
    if "permalink" in fm and fm["permalink"] is None:
        rec.issues.append(asdict(Issue(
            "null_permalink", "warning", "permalink",
            "permalink is null", "mechanical",
            "Remove the null permalink key to use the collection default")))
    # quest keyword shape
    if rec.fm_content_type == "quest" and isinstance(fm.get("keywords"), list):
        rec.issues.append(asdict(Issue(
            "quest_keywords_list_shape", "info", "keywords",
            "quest keywords should be {primary, secondary}", "mechanical",
            "Run make content-normalize-apply")))
    # filename with spaces
    if " " in Path(rec.path).name:
        rec.issues.append(asdict(Issue(
            "filename_has_spaces", "warning", "filename",
            "filename contains spaces (breaks tooling)", "substantive",
            "Rename to kebab-case and update inbound links")))


def _check_seo(rec: FileRecord, fm: dict, cfg: dict) -> None:
    c = cfg["constraints"]
    if rec.title_len and rec.title_len > c["title"]["hard_max"]:
        rec.issues.append(asdict(Issue(
            "title_too_long", "warning", "title",
            f"title {rec.title_len} chars (> {c['title']['hard_max']})",
            "substantive", "Shorten the title")))
    if rec.description_len:
        if rec.description_len < c["description"]["hard_min"]:
            rec.issues.append(asdict(Issue(
                "description_too_short", "warning", "description",
                f"description {rec.description_len} chars (< {c['description']['hard_min']})",
                "substantive", "Expand the description")))
        elif rec.description_len > c["description"]["hard_max"]:
            rec.issues.append(asdict(Issue(
                "description_too_long", "warning", "description",
                f"description {rec.description_len} chars (> {c['description']['hard_max']})",
                "substantive", "Trim the description")))
    kw = fm.get("keywords")
    if kw is not None:
        kw_count = _keyword_count(kw)
        if kw_count < c["keywords"]["min"]:
            rec.issues.append(asdict(Issue(
                "keywords_too_few", "info", "keywords",
                f"{kw_count} keywords (< {c['keywords']['min']})", "substantive",
                "Add a few relevant keywords")))


def _keyword_count(kw: Any) -> int:
    if isinstance(kw, list):
        return len([x for x in kw if x])
    if isinstance(kw, dict):
        n = 0
        for v in kw.values():
            if isinstance(v, list):
                n += len([x for x in v if x])
            elif isinstance(v, str) and v.strip():
                n += len([t for t in re.split(r"[,;]", v) if t.strip()])
        return n
    if isinstance(kw, str):
        return len([t for t in re.split(r"[,;]", kw) if t.strip()])
    return 0


def _check_structure(rec: FileRecord, cfg: dict) -> None:
    wc = cfg["constraints"]["word_count"]
    if rec.word_count < wc["min"] and rec.draft is not True:
        rec.issues.append(asdict(Issue(
            "thin_content", "warning", "body",
            f"only {rec.word_count} words (< {wc['min']})", "substantive",
            "Expand the content")))
    if rec.heading_count < cfg["constraints"]["headings"]["min"]:
        rec.issues.append(asdict(Issue(
            "no_headings", "info", "body",
            "no headings found", "substantive", "Add section headings")))


def _score(rec: FileRecord, required: list, cfg: dict) -> int:
    if rec.read_only or rec.structural or rec.generated:
        return 100
    w = cfg["health_weights"]
    c = cfg["constraints"]
    missing = sum(1 for i in rec.issues if i["kind"].startswith("missing_required:"))
    req_score = max(0.0, 1 - missing / max(len(required), 1))

    seo = 1.0
    if rec.title_len == 0 or rec.title_len > c["title"]["hard_max"]:
        seo -= 0.4
    if not (c["description"]["hard_min"] <= rec.description_len <= c["description"]["hard_max"]):
        seo -= 0.4
    seo = max(0.0, seo)

    fresh_map = {"fresh": 1.0, "aging": 0.66, "stale": 0.33,
                 "critical": 0.0, "unknown": 0.5}
    fresh_score = fresh_map.get(rec.freshness, 0.5)
    link_score = 0.0 if rec.broken_links else 1.0
    struct = 1.0
    if rec.heading_count < 1:
        struct -= 0.5
    if rec.word_count < c["word_count"]["min"]:
        struct -= 0.5
    struct = max(0.0, struct)

    total = (req_score * w["required_fields"] + seo * w["seo"]
             + fresh_score * w["freshness"] + link_score * w["links"]
             + struct * w["structure"])
    return round(total / sum(w.values()) * 100)


# --------------------------------------------------------------------------- #
# External enrichment
# --------------------------------------------------------------------------- #
def load_link_map(cfg: dict) -> dict:
    p = REPO_ROOT / cfg["enrich_from"]["link_report"]
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    out: dict[str, int] = {}
    # link-checker.py (v2) serializes categories as {name: [ {url, error, file}, ... ]}.
    # Older/alternate shapes use {name: {links: [...]}}. Handle both.
    for cat in data.get("categories", {}).values():
        items = cat if isinstance(cat, list) else (
            cat.get("links", []) if isinstance(cat, dict) else [])
        for item in items or []:
            if not isinstance(item, dict):
                continue
            src = item.get("file") or item.get("source") or item.get("source_file")
            if src:
                key = src.lstrip("./")
                out[key] = out.get(key, 0) + 1
    return out


def load_freshness(cfg: dict) -> dict:
    p = REPO_ROOT / cfg["enrich_from"]["freshness_report"]
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {f["file_path"]: f for f in data.get("files", []) if "file_path" in f}


# --------------------------------------------------------------------------- #
# Index build
# --------------------------------------------------------------------------- #
def build_index(cfg: dict, now: datetime) -> list[FileRecord]:
    root = REPO_ROOT / cfg["content_root"]
    exts = set(cfg["file_extensions"])
    link_map = load_link_map(cfg)
    fresh = load_freshness(cfg)
    records = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix not in exts:
            continue
        if "/.jekyll-cache/" in str(p) or "/_site/" in str(p):
            continue
        try:
            records.append(analyze_file(p, cfg, now, link_map, fresh))
        except Exception as e:   # one bad file must never abort the whole scan
            rel = str(p.relative_to(REPO_ROOT))
            coll, ccfg = collection_for(rel, cfg)
            rec = FileRecord(path=rel, collection=coll,
                             fm_content_type=ccfg.get("fm_content_type", "default"),
                             health=0, frontmatter_present=False)
            rec.issues.append(asdict(Issue(
                "engine_error", "error", "file",
                f"engine could not index this file: {e}", "substantive",
                "Inspect the file for malformed content")))
            records.append(rec)
    return records


def _actionable(r: FileRecord) -> bool:
    return (r.health >= 0 and not r.read_only and not r.structural
            and not r.generated and not r.is_notebook)


def summarize(records: list[FileRecord], now: datetime) -> dict:
    scored = [r for r in records if r.health >= 0]
    actionable = [r for r in records if _actionable(r)]
    by_coll: dict[str, dict] = {}
    for r in records:
        d = by_coll.setdefault(r.collection, {"count": 0, "health_sum": 0,
                                              "scored": 0, "mechanical": 0,
                                              "substantive": 0, "errors": 0})
        d["count"] += 1
        if r.health >= 0:
            d["health_sum"] += r.health
            d["scored"] += 1
        d["mechanical"] += r.mechanical_count
        d["substantive"] += r.substantive_count
        d["errors"] += r.error_count
    for d in by_coll.values():
        d["avg_health"] = round(d["health_sum"] / d["scored"], 1) if d["scored"] else None
        del d["health_sum"]
    fresh_dist: dict[str, int] = {}
    for r in scored:
        fresh_dist[r.freshness] = fresh_dist.get(r.freshness, 0) + 1
    return {
        "generated_at": now.isoformat(),
        "total_files": len(records),
        "scored_files": len(scored),
        "actionable_files": len(actionable),
        "avg_health": round(sum(r.health for r in scored) / len(scored), 1) if scored else None,
        "avg_health_actionable": round(sum(r.health for r in actionable) / len(actionable), 1) if actionable else None,
        "total_mechanical_issues": sum(r.mechanical_count for r in records),
        "total_substantive_issues": sum(r.substantive_count for r in records),
        "total_errors": sum(r.error_count for r in records),
        "read_only_files": sum(1 for r in records if r.read_only),
        "by_collection": by_coll,
        "freshness_distribution": fresh_dist,
        "health_buckets": {
            "excellent_90_100": sum(1 for r in scored if r.health >= 90),
            "good_70_89": sum(1 for r in scored if 70 <= r.health < 90),
            "fair_50_69": sum(1 for r in scored if 50 <= r.health < 70),
            "poor_0_49": sum(1 for r in scored if r.health < 50),
        },
    }


# --------------------------------------------------------------------------- #
# Schema emit
# --------------------------------------------------------------------------- #
def build_schema(cfg: dict) -> dict:
    fm_fields = load_frontmatter_schema()
    collections = {}
    for name, c in cfg["collections"].items():
        ct = c.get("fm_content_type", "default")
        collections[name] = {
            "path": c["path"],
            "fm_content_type": ct,
            "required": list(cfg["required_base"]) + list(c.get("required_extra", [])),
            "recommended": c.get("recommended", []),
            "fields": fm_fields.get(ct, []),
            "registry_governed": c.get("registry_governed", False),
        }
    return {
        "version": cfg["version"],
        "generated_from": ["frontmatter.json", ".cms/config.yml",
                           ".github/content-review-config.yml"],
        "constraints": cfg["constraints"],
        "read_only": cfg["read_only"],
        "generated": cfg["generated"],
        "collections": collections,
    }


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #
def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str) + "\n", encoding="utf-8")


def cmd_index(cfg: dict, now: datetime, verbose: bool) -> tuple[list, dict]:
    records = build_index(cfg, now)
    summary = summarize(records, now)
    write_json(REPO_ROOT / cfg["output"]["index"],
               {"generated_at": now.isoformat(),
                "files": [asdict(r) for r in records]})
    write_json(REPO_ROOT / cfg["output"]["summary"], summary)
    write_json(REPO_ROOT / cfg["output"]["schema"], build_schema(cfg))
    if verbose:
        print(f"Indexed {summary['total_files']} files "
              f"({summary['scored_files']} scored, avg health {summary['avg_health']}).")
    return records, summary


def _date_str(now: datetime) -> str:
    return now.strftime("%Y-%m-%d")


def cmd_analyze(cfg: dict, records: list, summary: dict, now: datetime) -> Path:
    lines = [f"# IT-Journey content analysis — {_date_str(now)}", ""]
    lines.append(f"_Generated by `scripts/cms/cms.py` at {now.isoformat()}_")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(f"- **Total content files**: {summary['total_files']} "
                 f"({summary['scored_files']} scored, "
                 f"{summary['actionable_files']} actionable)")
    lines.append(f"- **Average health (all)**: {summary['avg_health']}/100")
    lines.append(f"- **Average health (actionable)**: "
                 f"{summary['avg_health_actionable']}/100")
    lines.append(f"- **Read-only/vendored**: {summary['read_only_files']}")
    lines.append(f"- **Mechanical issues** (auto-fixable): "
                 f"{summary['total_mechanical_issues']}")
    lines.append(f"- **Substantive issues** (need authoring): "
                 f"{summary['total_substantive_issues']}")
    lines.append(f"- **Errors**: {summary['total_errors']}")
    lines.append("")

    hb = summary["health_buckets"]
    lines += ["## Health distribution", "",
              f"| Bucket | Files |", "|---|---|",
              f"| 🟢 Excellent (90–100) | {hb['excellent_90_100']} |",
              f"| 🟡 Good (70–89) | {hb['good_70_89']} |",
              f"| 🟠 Fair (50–69) | {hb['fair_50_69']} |",
              f"| 🔴 Poor (0–49) | {hb['poor_0_49']} |", ""]

    lines += ["## By collection", "",
              "| Collection | Files | Avg health | Mechanical | Substantive | Errors |",
              "|---|---|---|---|---|---|"]
    for name, d in sorted(summary["by_collection"].items(),
                          key=lambda kv: -(kv[1]["count"])):
        lines.append(f"| {name} | {d['count']} | {d['avg_health']} | "
                     f"{d['mechanical']} | {d['substantive']} | {d['errors']} |")
    lines.append("")

    lines += ["## Freshness", "",
              "| Status | Files |", "|---|---|"]
    for status in ("fresh", "aging", "stale", "critical", "unknown"):
        lines.append(f"| {status} | {summary['freshness_distribution'].get(status, 0)} |")
    lines.append("")

    # top issue kinds
    kinds: dict[str, int] = {}
    for r in records:
        for i in r.issues:
            kinds[i["kind"].split(":")[0]] = kinds.get(i["kind"].split(":")[0], 0) + 1
    lines += ["## Top issue types", "", "| Issue | Count |", "|---|---|"]
    for k, n in sorted(kinds.items(), key=lambda kv: -kv[1])[:15]:
        lines.append(f"| `{k}` | {n} |")
    lines.append("")

    # lowest-health files
    worst = sorted([r for r in records if _actionable(r)],
                   key=lambda r: r.health)[:20]
    lines += ["## Lowest-health files (actionable only)", "",
              "| Health | File | Errors | Issues |", "|---|---|---|---|"]
    for r in worst:
        lines.append(f"| {r.health} | `{r.path}` | {r.error_count} | "
                     f"{len(r.issues)} |")
    lines.append("")

    path = REPO_ROOT / cfg["output"]["reports_dir"] / f"{_date_str(now)}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def cmd_plan(cfg: dict, records: list, now: datetime) -> Path:
    loop = cfg["loop"]
    prio = loop["collection_priority"]

    # candidates = files with issues, not read-only/structural/generated/notebook
    cands = [r for r in records
             if r.issues and not (r.read_only or r.structural
                                  or r.generated or r.is_notebook)]

    def rank(r: FileRecord) -> float:
        weight = prio.get(r.collection, 1.0)
        # urgency: errors heavily, then low health, then issue count
        return (r.error_count * 10 + (100 - max(r.health, 0)) / 10
                + len(r.issues)) * weight

    cands.sort(key=rank, reverse=True)

    mech = [r for r in cands if r.mechanical_count]
    subs = [r for r in cands if r.substantive_count]
    mech_batch = mech[: loop["mechanical_batch_size"]]
    subs_batch = subs[: loop["batch_size"]]

    d = _date_str(now)
    lines = [f"# CMS worklist — {d}", "",
             f"_Generated by `scripts/cms/cms.py plan`. Input for the "
             f"`cms-curator` loop. See `.cms/reports/{d}.md` for the full analysis._",
             "",
             "## Lane A — Mechanical (deterministic, auto-merge after green CI)", "",
             "These are fixed in one pass by `make content-normalize-apply` plus a "
             "small set of safe key edits. They do **not** need content review.", ""]

    mech_kinds: dict[str, int] = {}
    for r in mech:
        for i in r.issues:
            if i["lane"] == "mechanical":
                mech_kinds[i["kind"].split(":")[0]] = mech_kinds.get(i["kind"].split(":")[0], 0) + 1
    if mech_kinds:
        lines += ["| Fix kind | Files affected |", "|---|---|"]
        for k, n in sorted(mech_kinds.items(), key=lambda kv: -kv[1]):
            lines.append(f"| `{k}` | {n} |")
        lines.append("")
        lines.append(f"**Action**: `make content-normalize-apply` (touches up to "
                     f"{len(mech)} files), then re-run `make content-validate`. "
                     f"If quest frontmatter changed, run `make quest-data`.")
    else:
        lines.append("_No mechanical issues outstanding._")
    lines.append("")

    lines += [f"## Lane B — Substantive (reviewed PR, batch of {len(subs_batch)})",
              "",
              "Each item needs authoring/judgment. Work top-down; keep the daily "
              "PR reviewable. Group commits by collection.", "",
              "| # | Health | Collection | File | Top issues |",
              "|---|---|---|---|---|"]
    for n, r in enumerate(subs_batch, 1):
        top = "; ".join(sorted({i["kind"].split(":")[0] for i in r.issues
                                if i["lane"] == "substantive"}))[:80]
        lines.append(f"| {n} | {r.health} | {r.collection} | `{r.path}` | {top} |")
    lines.append("")
    lines += ["## Detail (substantive batch)", ""]
    for n, r in enumerate(subs_batch, 1):
        lines.append(f"### {n}. `{r.path}`  (health {r.health})")
        for i in r.issues:
            if i["lane"] == "substantive":
                sug = f" — _{i['suggestion']}_" if i.get("suggestion") else ""
                lines.append(f"- **{i['severity']}** `{i['field']}`: {i['message']}{sug}")
        lines.append("")

    path = REPO_ROOT / cfg["output"]["worklists_dir"] / f"{d}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def cmd_status(summary: dict) -> None:
    print("IT-Journey CMS — status")
    print("=" * 40)
    print(f"  files indexed : {summary['total_files']} "
          f"({summary['actionable_files']} actionable)")
    print(f"  avg health    : {summary['avg_health']}/100 "
          f"(actionable {summary['avg_health_actionable']}/100)")
    print(f"  mechanical    : {summary['total_mechanical_issues']} issues")
    print(f"  substantive   : {summary['total_substantive_issues']} issues")
    print(f"  errors        : {summary['total_errors']}")
    print(f"  read-only     : {summary['read_only_files']}")
    print("  by collection :")
    for name, d in sorted(summary["by_collection"].items(),
                          key=lambda kv: -(kv[1]["count"])):
        print(f"    {name:<11} {d['count']:>4} files  "
              f"health {str(d['avg_health']):>5}  "
              f"mech {d['mechanical']:>3}  subs {d['substantive']:>3}")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="IT-Journey AI-augmented CMS engine")
    ap.add_argument("command",
                    choices=["index", "analyze", "plan", "status", "all"],
                    help="action to run")
    ap.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    now = datetime.now(timezone.utc)
    verbose = not args.quiet

    records, summary = cmd_index(cfg, now, verbose and args.command in ("index", "all"))

    if args.command in ("analyze", "all"):
        p = cmd_analyze(cfg, records, summary, now)
        if verbose:
            print(f"Analysis report: {p.relative_to(REPO_ROOT)}")
    if args.command in ("plan", "all"):
        p = cmd_plan(cfg, records, now)
        if verbose:
            print(f"Worklist: {p.relative_to(REPO_ROOT)}")
    if args.command == "status":
        cmd_status(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
