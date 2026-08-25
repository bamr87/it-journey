#!/usr/bin/env python3
"""
video_manifest.py — the DETERMINISTIC half of the quest walkthrough-video lane.

Two subcommands, both model-free (mirroring the ledger/normalizer discipline —
the agentic engine witnesses a run once; everything downstream is replayable):

  build   Read the recorder's <videos>/manifest.json (walkthrough_video.mjs)
          and compose the YouTube upload plan: per-video title, description
          (with chapters + provenance), tags, category, privacy. Pure function
          of (manifest, run-url, date) → videos/upload-plan.json.

  apply   Read the uploader's videos/uploads.json (youtube_upload.py) and
          write each published video back into the repo:
            * the quest's frontmatter gains/updates a `walkthrough_video:`
              block (provider/id/url/recorded/run_url) + a `lastmod` bump —
              a minimal, idempotent TEXT edit that leaves every other
              frontmatter byte alone (same philosophy as the normalizer);
            * the committed catalog `.quests/videos.yml` gains/updates the
              quest's entry (the queryable source of truth for coverage).
          Dry-run by default; --apply writes (repo convention).

YouTube constraints honored here so the uploader can stay dumb:
  * title ≤ 100 chars, no '<' or '>';
  * description ≤ 5000 chars, no '<' or '>';
  * chapter lines: first at 00:00, ≥ 3 entries, ≥ 10s apart (else omitted);
  * tags total ≤ 460 chars (API limit is 500 — headroom is deliberate).

Usage:
  python3 scripts/quest/video_manifest.py build \
      --manifest videos/manifest.json --out videos/upload-plan.json \
      --run-url https://github.com/bamr87/it-journey/actions/runs/<id> \
      [--privacy unlisted] [--date YYYY-MM-DD]

  python3 scripts/quest/video_manifest.py apply \
      --uploads videos/uploads.json [--catalog .quests/videos.yml] \
      [--date YYYY-MM-DD] [--apply]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent

SITE = "https://it-journey.dev"
REPO_URL = "https://github.com/bamr87/it-journey"
YT_CATEGORY_EDUCATION = "27"
TITLE_MAX = 100
DESC_MAX = 5000
TAGS_MAX_TOTAL = 460
CHAPTER_MIN_GAP_S = 10
CHAPTER_MIN_COUNT = 3

_FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_VIDEO_BLOCK_RE = re.compile(r"^walkthrough_video:[^\n]*\n(?:[ \t]+[^\n]*\n)*", re.MULTILINE)
_LASTMOD_RE = re.compile(r"^(lastmod:[ \t]*)(['\"]?)([^'\"\n]*)(\2)[ \t]*$", re.MULTILINE)
_YT_ID_RE = re.compile(r"^[A-Za-z0-9_-]{6,20}$")


def _die(msg: str, code: int = 2):
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(code)


def _today(date_arg: str | None) -> str:
    if date_arg:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_arg):
            _die(f"--date must be YYYY-MM-DD, got {date_arg!r}")
        return date_arg
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _yt_text(s: str) -> str:
    """YouTube forbids angle brackets in titles/descriptions."""
    return str(s or "").replace("<", "‹").replace(">", "›").strip()


def _mmss(seconds: float) -> str:
    s = max(0, int(round(seconds)))
    if s >= 3600:
        return f"{s // 3600}:{(s % 3600) // 60:02d}:{s % 60:02d}"
    return f"{s // 60:02d}:{s % 60:02d}"


# ─────────────────────────────────────────────────────────────────────────────
# build — recorder manifest → upload plan
# ─────────────────────────────────────────────────────────────────────────────

def compose_title(quest_title: str, level: str) -> str:
    base = _yt_text(quest_title)
    suffix = f" — IT-Journey Quest Walkthrough (Level {level})"
    if len(base) + len(suffix) > TITLE_MAX:
        short = f" — IT-Journey Walkthrough"
        if len(base) + len(short) > TITLE_MAX:
            base = base[: TITLE_MAX - len(short) - 1].rstrip() + "…"
        return base + short
    return base + suffix


def compose_chapters(chapters: list[dict]) -> list[str]:
    """Collapse to YouTube-valid chapter lines, or [] when too few/too close."""
    lines, last_kept = [], None
    for ch in chapters or []:
        start = float(ch.get("start") or 0)
        label = _yt_text(ch.get("label") or "").strip() or "Step"
        if last_kept is None:
            start = 0.0  # YouTube requires the first chapter at 00:00
        elif start - last_kept < CHAPTER_MIN_GAP_S:
            continue
        last_kept = start
        lines.append(f"{_mmss(start)} {label}")
    return lines if len(lines) >= CHAPTER_MIN_COUNT else []


def compose_description(video: dict, plan_meta: dict, run_url: str, date: str) -> str:
    q = video.get("quest") or {}
    ev = video.get("evidence") or {}
    character = (plan_meta.get("character") or {}).get("name") or "adventurer"
    level = q.get("level") or (plan_meta.get("level") or {}).get("code") or ""
    theme = (plan_meta.get("level") or {}).get("theme") or ""
    base_url = plan_meta.get("base_url") or SITE
    quest_url = f"{base_url}{q.get('permalink') or ''}"
    score = ev.get("overall")
    verdict_line = (f"{ev.get('verdict')} · score {round(score)}%"
                    if isinstance(score, (int, float)) else "see the CI run")

    parts = [
        f"A verified, automated walkthrough of “{_yt_text(q.get('title'))}” — "
        f"Level {level} ({_yt_text(theme)}) on the {_yt_text(character)} path of IT-Journey, "
        f"the gamified open-source IT learning platform.",
        "",
        "Left: the quest as published. Right: the recorded terminal session — every command "
        "was executed for real in a clean, disposable CI sandbox by IT-Journey's autonomous "
        "quest-perfection loop. The video is rendered from that sealed evidence: no cuts, no staging.",
        "",
        f"📖 Take this quest: {quest_url}",
        f"🗺️ All quests: {SITE}/quests/",
        f"📊 Session verdict: {_yt_text(verdict_line)} (recorded {date})",
    ]
    if run_url:
        parts.append(f"🔎 Provenance — the CI run that executed and recorded this session: {run_url}")
    chapter_lines = compose_chapters(video.get("chapters") or [])
    if chapter_lines:
        parts += ["", "Chapters:"] + chapter_lines
    parts += [
        "",
        f"IT-Journey is open source (MIT) — {REPO_URL}",
        "New quests are validated continuously; when a walkthrough finds a broken step, "
        "the loop repairs the quest and re-records.",
        "",
        "#ITJourney #QuestWalkthrough #LearnToCode",
    ]
    desc = "\n".join(parts)
    return desc[:DESC_MAX]


def compose_tags(video: dict, plan_meta: dict) -> list[str]:
    q = video.get("quest") or {}
    level = q.get("level") or ""
    theme = (plan_meta.get("level") or {}).get("theme") or ""
    character = (plan_meta.get("character") or {}).get("key") or ""
    difficulty = re.sub(r"[^A-Za-z ]", "", q.get("difficulty") or "").strip().lower()
    raw = ["it-journey", "quest walkthrough", "learn it", "tutorial",
           f"level {level}", theme.lower(), character, difficulty,
           "hands-on", "terminal", "open source education"]
    tags, total, seen = [], 0, set()
    for t in raw:
        t = _yt_text(t).strip()
        if not t or t in seen:
            continue
        if total + len(t) > TAGS_MAX_TOTAL:
            break
        seen.add(t)
        tags.append(t)
        total += len(t)
    return tags


def cmd_build(args) -> int:
    mpath = Path(args.manifest)
    try:
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        _die(f"cannot read recorder manifest {mpath}: {e}")
    date = _today(args.date)
    slice_slug = ""
    if manifest.get("character") and manifest.get("level"):
        slice_slug = f"{manifest['character'].get('key')}/{manifest['level'].get('code')}"
    items = []
    for video in manifest.get("videos") or []:
        q = video.get("quest") or {}
        ev = video.get("evidence") or {}
        items.append({
            "slug": video.get("slug"),
            "name": video.get("name"),
            "file": video.get("file"),
            "permalink": q.get("permalink"),
            "quest_path": q.get("path"),
            "snippet": {
                "title": compose_title(q.get("title") or video.get("slug") or "Quest", q.get("level") or ""),
                "description": compose_description(video, manifest, args.run_url or "", date),
                "tags": compose_tags(video, manifest),
                "categoryId": YT_CATEGORY_EDUCATION,
            },
            "status": {
                "privacyStatus": args.privacy,
                "selfDeclaredMadeForKids": False,
            },
            "recorded": date,
            "run_url": args.run_url or "",
            "slice": slice_slug,
            "duration_s": video.get("duration_s"),
            "verdict": ev.get("verdict"),
            "score": ev.get("overall"),
            # The captured review signal (walkthrough_video.mjs analyzeResults):
            # per-status counts + how many steps did not cleanly pass. Rides
            # through uploads.json into the catalog so coverage dashboards and
            # the publish PR can surface what the recording witnessed.
            "results": video.get("results"),
            "issues_count": video.get("issues_count"),
        })
    plan = {
        "schema_version": "1.0.0",
        "generated": date,
        "privacy": args.privacy,
        "run_url": args.run_url or "",
        "slice": slice_slug,
        "items": items,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"📋 upload plan: {len(items)} video(s) → {out}")
    if not items:
        print("⚠️  the recorder manifest holds no videos — nothing to upload.", file=sys.stderr)
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# apply — published uploads → quest frontmatter + committed catalog
# ─────────────────────────────────────────────────────────────────────────────

def video_block(video_id: str, recorded: str, run_url: str) -> str:
    lines = [
        "walkthrough_video:",
        "  provider: youtube",
        f"  id: {video_id}",
        f"  url: https://www.youtube.com/watch?v={video_id}",
        f"  recorded: '{recorded}'",
    ]
    if run_url:
        lines.append(f"  run_url: {run_url}")
    return "\n".join(lines) + "\n"


def apply_to_quest(text: str, video_id: str, recorded: str, run_url: str) -> str:
    """Insert/replace the walkthrough_video block; bump lastmod. Idempotent."""
    m = _FM_RE.match(text)
    if not m:
        raise ValueError("no frontmatter block found")
    fm = m.group(1) + "\n"
    block = video_block(video_id, recorded, run_url)
    if _VIDEO_BLOCK_RE.search(fm):
        new_fm = _VIDEO_BLOCK_RE.sub(block, fm, count=1)
    else:
        new_fm = fm + block
    lm = _LASTMOD_RE.search(new_fm)
    if lm:
        quote = lm.group(2) or "'"
        new_fm = _LASTMOD_RE.sub(rf"\g<1>{quote}{recorded}T00:00:00.000Z{quote}", new_fm, count=1)
    new_fm = new_fm.rstrip("\n") + "\n"
    return f"---\n{new_fm}---\n" + text[m.end():]


def _quest_file(entry: dict) -> Path | None:
    p = entry.get("quest_path")
    if p and (REPO_ROOT / p).exists():
        return REPO_ROOT / p
    # Fallback: map the permalink to pages/_quests/<level>/<slug>.md
    permalink = entry.get("permalink") or ""
    parts = [x for x in permalink.strip("/").split("/") if x and x != "side-quests"]
    if len(parts) >= 3 and parts[0] == "quests":
        cand = REPO_ROOT / "pages" / "_quests" / parts[1] / f"{parts[-1]}.md"
        if cand.exists():
            return cand
    return None


def load_catalog(path: Path) -> dict:
    try:
        import yaml  # noqa: PLC0415
    except ImportError:
        _die("pyyaml is required for apply (pip install pyyaml)")
    if path.exists():
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            data = {}
    else:
        data = {}
    data.setdefault("schema_version", "1.0.0")
    data.setdefault("videos", {})
    return data


CATALOG_HEADER = """\
# =============================================================================
# .quests/videos.yml — the committed quest walkthrough-video catalog
# -----------------------------------------------------------------------------
# One entry per quest permalink → the published YouTube walkthrough video for
# that quest. WRITTEN by `scripts/quest/video_manifest.py apply` (the deterministic
# arm of the quest-video lane, driven by .github/workflows/quest-video.yml);
# read by dashboards and coverage checks. The same reference is embedded in the
# quest's own frontmatter (`walkthrough_video:`), which is what the site renders
# — this file is the queryable index across quests. Do not hand-edit ids.
# =============================================================================
"""


def save_catalog(path: Path, data: dict):
    import yaml  # noqa: PLC0415
    data["videos"] = dict(sorted((data.get("videos") or {}).items()))
    body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)
    path.write_text(CATALOG_HEADER + body, encoding="utf-8")


def cmd_apply(args) -> int:
    upath = Path(args.uploads)
    try:
        uploads_doc = json.loads(upath.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        _die(f"cannot read uploads file {upath}: {e}")
    uploads = uploads_doc.get("uploads") or []
    if not uploads:
        print("⚠️  no uploads to apply — nothing to do.")
        return 0
    date = _today(args.date)
    catalog_path = Path(args.catalog)
    catalog = load_catalog(catalog_path)
    changed, errors = [], []
    for entry in uploads:
        vid = str(entry.get("video_id") or "")
        permalink = entry.get("permalink") or ""
        if not _YT_ID_RE.match(vid):
            errors.append(f"{permalink}: implausible video id {vid!r}")
            continue
        qfile = _quest_file(entry)
        if qfile is None:
            errors.append(f"{permalink}: quest file not found "
                          f"(quest_path={entry.get('quest_path')!r})")
            continue
        recorded = entry.get("recorded") or date
        run_url = entry.get("run_url") or ""
        text = qfile.read_text(encoding="utf-8")
        try:
            new_text = apply_to_quest(text, vid, recorded, run_url)
        except ValueError as e:
            errors.append(f"{qfile}: {e}")
            continue
        if new_text != text:
            if args.apply:
                qfile.write_text(new_text, encoding="utf-8")
            changed.append(str(qfile.relative_to(REPO_ROOT)))
        catalog["videos"][permalink] = {
            "id": vid,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "title": entry.get("title") or "",
            "recorded": recorded,
            "run_url": run_url,
            "slice": entry.get("slice") or "",
            "duration_s": entry.get("duration_s"),
            "verdict": entry.get("verdict"),
            "score": entry.get("score"),
            # Witnessed review signal: steps in the recording that did not
            # cleanly pass (failed or skipped). A non-zero count is a standing
            # invitation to re-run the fix lane against this video's evidence.
            "issues": entry.get("issues_count"),
        }
    if args.apply:
        catalog_path.parent.mkdir(parents=True, exist_ok=True)
        save_catalog(catalog_path, catalog)
    verb = "updated" if args.apply else "would update (dry run — pass --apply)"
    print(f"🎬 {verb}: {len(changed)} quest file(s) + {catalog_path}")
    for c in changed:
        print(f"   • {c}")
    for e in errors:
        print(f"⚠️  {e}", file=sys.stderr)
    return 1 if errors else 0


# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="recorder manifest → YouTube upload plan")
    b.add_argument("--manifest", default="videos/manifest.json")
    b.add_argument("--out", default="videos/upload-plan.json")
    b.add_argument("--run-url", default="")
    b.add_argument("--privacy", default="unlisted",
                   choices=["public", "unlisted", "private"])
    b.add_argument("--date", help="YYYY-MM-DD (default: today UTC) — pin for determinism")
    b.set_defaults(func=cmd_build)

    a = sub.add_parser("apply", help="published uploads → frontmatter + catalog")
    a.add_argument("--uploads", default="videos/uploads.json")
    a.add_argument("--catalog", default=str(REPO_ROOT / ".quests" / "videos.yml"))
    a.add_argument("--date", help="YYYY-MM-DD (default: today UTC)")
    a.add_argument("--apply", action="store_true",
                   help="write changes (default: dry run — repo convention)")
    a.set_defaults(func=cmd_apply)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
