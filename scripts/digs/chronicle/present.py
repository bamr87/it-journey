"""Assemble the presentation from the ledger: one HTML deck, its data, its frames.

Everything here is derived. The deck reads ``data.json`` (and ``data.js``, the
same data as a script, so the page also opens from disk) plus the front-end
frames copied beside it. Re-building never touches Git or a model; it only
reads what ``ingest``, ``annotate``, ``eras`` and ``frames`` filed.
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path

from core import TOOL_VERSION, Ledger, month_of, now_iso
from facts import area_of
from replay import _week, mainline_order, timeline

HERE = Path(__file__).resolve().parent
ACTORS = ("human", "ai-assisted", "ai", "bot")
MILESTONES = (
    ("Jekyll site config", lambda p: p == "_config.yml"),
    ("Ruby Gemfile", lambda p: p == "Gemfile"),
    ("Ruby gem spec", lambda p: p.endswith(".gemspec") and "/" not in p),
    ("Node package.json", lambda p: p == "package.json"),
    ("Python project", lambda p: p in ("requirements.txt", "pyproject.toml", "setup.py")),
    ("Makefile", lambda p: p == "Makefile"),
    ("Docker", lambda p: p in ("Dockerfile", "docker-compose.yml", "compose.yml", "docker-compose.yaml")),
    ("Dev container", lambda p: p.startswith(".devcontainer/")),
    ("GitHub Actions", lambda p: p.startswith(".github/workflows/")),
    ("Dependabot", lambda p: p == ".github/dependabot.yml"),
    ("Theme layouts", lambda p: p.startswith("_layouts/")),
    ("Includes", lambda p: p.startswith("_includes/")),
    ("Sass styles", lambda p: p.startswith("_sass/")),
    ("Jekyll plugins", lambda p: p.startswith("_plugins/")),
    ("Site data", lambda p: p.startswith("_data/")),
    ("Collections under pages/", lambda p: p.startswith("pages/_")),
    ("Scripts folder", lambda p: p.startswith("scripts/")),
    ("Tests", lambda p: p.split("/", 1)[0] in ("test", "tests", "spec") and "/" in p),
    ("Docs folder", lambda p: p.startswith("docs/")),
    ("Changelog", lambda p: p == "CHANGELOG.md"),
    ("Release automation", lambda p: p in ("release-please-config.json", ".release-please-manifest.json")),
    ("Copilot instructions", lambda p: p == ".github/copilot-instructions.md"),
    ("Agent instructions (AGENTS/CLAUDE.md)", lambda p: p in ("AGENTS.md", "CLAUDE.md")),
    ("Claude Code layer (.claude/)", lambda p: p.startswith(".claude/")),
    ("Constitution & amendments", lambda p: p in ("docs/constitution.md",)),
)


def _weeks_between(first: str, last: str) -> list[str]:
    a = dt.date.fromisoformat(first)
    b = dt.date.fromisoformat(last)
    out = []
    while a <= b:
        out.append(a.isoformat())
        a += dt.timedelta(days=7)
    return out


def assemble(ledger: Ledger, frames_root: Path) -> dict:
    commits = ledger.commits()
    ann = ledger.annotations()
    man = ledger.manifest()
    head = man["head"]
    eras_doc = ledger.read_doc("eras.json") or {"eras": [], "learnings": [], "transitions": []}
    frames_doc = ledger.read_doc("frames.json") or {"pages": []}
    rows = sorted(commits.values(), key=lambda r: (r["ct"], r["sha"]))
    chain = mainline_order(commits, head)

    # cadence: every commit, by ISO week (Monday), gaps filled
    weeks: dict[str, dict] = {}
    for r in rows:
        w = weeks.setdefault(_week(r["ct"]), {"c": 0, "a": 0, "d": 0, "act": [0, 0, 0, 0]})
        w["c"] += 1
        w["a"] += r["totals"]["add"]
        w["d"] += r["totals"]["del"]
        w["act"][ACTORS.index(r["facts"]["actor"])] += 1
    span = _weeks_between(min(weeks), max(weeks))
    cadence = [{"w": w, **weeks.get(w, {"c": 0, "a": 0, "d": 0, "act": [0, 0, 0, 0]})} for w in span]

    tl = timeline(commits, head, depth=2, max_nodes=140)
    # one color slot per top-level area, fixed for the whole film (by peak size)
    peak: dict[str, float] = defaultdict(float)
    for fr in tl["frames"]:
        per: dict[str, float] = defaultdict(float)
        for i, n, ln, sz in fr["n"]:
            per[area_of(tl["nodes"][i]) if tl["nodes"][i] != "/" else "/"] += ln + sz / 40
        for k, v in per.items():
            peak[k] = max(peak[k], v)
    ranked = sorted(peak, key=lambda k: -peak[k])
    areas = [{"name": a, "slot": i + 1 if i < 7 else 0} for i, a in enumerate(ranked)]

    # tooling milestones, first appearance on the mainline
    milestones, seen = [], set()
    for r in chain:
        for f in r["files"]:
            if f["s"] not in "ARC":
                continue
            for label, test in MILESTONES:
                if label not in seen and test(f["p"]):
                    seen.add(label)
                    milestones.append({"label": label, "path": f["p"], "date": r["ct"][:10], "sha": r["sha"][:12]})

    # eras with deterministic stats
    eras = []
    for e in eras_doc.get("eras", []):
        inside = [r for r in rows if e["start"] <= month_of(r["ct"]) <= e["end"]]
        area_c = Counter()
        for r in inside:
            for a, v in r["facts"]["areas"].items():
                area_c[a] += v[0]
        eras.append({**e, "stats": {
            "commits": len(inside),
            "add": sum(r["totals"]["add"] for r in inside),
            "del": sum(r["totals"]["del"] for r in inside),
            "actors": [sum(1 for r in inside if r["facts"]["actor"] == a) for a in ACTORS],
            "areas": [a for a, _ in area_c.most_common(4)],
        }})

    def short(sha):
        return sha[:12]

    commit_rows = []
    for r in rows:
        a = ann.get(r["sha"], {})
        commit_rows.append([short(r["sha"]), r["ct"][:16], ACTORS.index(r["facts"]["actor"]), a.get("kind", ""),
                            a.get("significance", 1), a.get("summary") or r["subject"][:140],
                            1 if r["mainline"] else 0, r["totals"]["add"], r["totals"]["del"], r["totals"]["files"]])

    pages = []
    for p in frames_doc.get("pages", []):
        frs = []
        for fr in p["frames"]:
            a = ann.get(fr["sha"], {})
            frs.append({**fr, "sha": short(fr["sha"]), "summary": a.get("summary") or commits.get(fr["sha"], {})
                        .get("subject", ""), "image": "frames/" + fr["image"]})
        pages.append({**p, "frames": frs})

    last = tl["frames"][-1] if tl["frames"] else {"files": 0, "lines": 0, "bytes": 0}
    authors = {r["author_id"] for r in rows if r["facts"]["actor"] in ("human", "ai-assisted")}
    models = Counter(a.get("model", "?") for a in ann.values())
    url = f"https://github.com/{ledger.slug}" if not ledger.slug.startswith("local/") else ""
    return {
        "schema": "chronicle-presentation/v1",
        "repo": {"slug": ledger.slug, "url": url, "ref": man.get("ref"), "head": short(head),
                 "first": rows[0]["ct"][:10], "last": rows[-1]["ct"][:10]},
        "stats": {
            "commits": len(rows), "mainline": len(chain), "authors": len(authors),
            "activeWeeks": sum(1 for c in cadence if c["c"]), "weeks": len(cadence),
            "filesNow": last["files"], "linesNow": last["lines"], "bytesNow": last["bytes"],
            "peakLines": max((f["lines"] for f in tl["frames"]), default=0),
            "peakFiles": max((f["files"] for f in tl["frames"]), default=0),
            "actors": [sum(1 for r in rows if r["facts"]["actor"] == a) for a in ACTORS],
            "added": sum(r["totals"]["add"] for r in rows), "deleted": sum(r["totals"]["del"] for r in rows),
        },
        "story": {k: eras_doc.get(k) for k in ("headline", "summary", "learnings", "transitions")},
        "eras": eras,
        "cadence": cadence,
        "timeline": tl,
        "areas": areas,
        "milestones": milestones,
        "commits": commit_rows,
        "pages": pages,
        "library": library_block(ledger, commits, head, tl),
        "provenance": {
            "tool": f"chronicle {TOOL_VERSION}", "ledger": f"docs/git-archaeology/chronicle/{ledger.slug}/",
            "annotations": dict(models), "erasSource": eras_doc.get("source"),
            "commitPrompt": man.get("ai", {}).get("commitPromptVersion"),
            "eraPrompt": eras_doc.get("pv"), "costUsdEstimate": man.get("ai", {}).get("costUsdEstimate", 0),
            "renderer": frames_doc.get("renderer"), "generated": now_iso(),
        },
    }


QTYPES = ("main", "side", "epic", "bonus", "other")


def library_block(ledger: Ledger, commits: dict, head: str, tl: dict) -> dict | None:
    """Every article's lifeline, topic and quest level, on the file-system film's weekly frames."""
    from content import articles
    versions = ledger.versions()
    if not versions:
        return None
    arts = articles(commits, versions, head)
    if not arts:
        return None
    tax = ledger.read_doc("content/taxonomy.json") or {"topics": [{"key": "other", "name": "Other"}], "source": None}
    readings = ledger.article_topics()
    frame_of = {fr["week"]: i for i, fr in enumerate(tl["frames"])}
    last = len(tl["frames"]) - 1

    def frame(ct):
        return frame_of.get(_week(ct), last)

    # collections keep one color for the whole film, ranked by peak live count
    live_by_frame: dict[str, list[int]] = defaultdict(lambda: [0] * (last + 2))
    for a in arts:
        b, d = frame(a["born"]), frame(a["died"]) if a["died"] else last + 1
        live_by_frame[a["col"]][b] += 1
        live_by_frame[a["col"]][d] -= 1
    peaks = {}
    for col, deltas in live_by_frame.items():
        run, peak = 0, 0
        for x in deltas:
            run += x
            peak = max(peak, run)
        peaks[col] = peak
    cols = sorted(peaks, key=lambda c: (-peaks[c], c))
    col_index = {c: i for i, c in enumerate(cols)}
    topic_keys = [t["key"] for t in tax["topics"]]
    topic_index = {k: i for i, k in enumerate(topic_keys)}

    def qtype(a):
        q = str(a.get("qt") or "").lower()
        for t in QTYPES[:-1]:
            if q.startswith(t):
                return QTYPES.index(t)
        return len(QTYPES) - 1

    rows = []
    for a in arts:
        topic = readings.get(a["aid"], {}).get("topic", "other")
        rows.append([
            a.get("t") or a["path"].rsplit("/", 1)[-1], col_index[a["col"]], topic_index.get(topic, len(topic_keys) - 1),
            frame(a["born"]), frame(a["died"]) if a["died"] else -1, a.get("lvl", ""),
            qtype(a) if a.get("lvl") else -1, a["revs"], a["path"], a["born"][:10],
            a["died"][:10] if a["died"] else "", a.get("w", 0), 1 if a.get("draft") else 0, a["moves"],
        ])
    models = Counter(r.get("model", "?") for r in readings.values())
    return {
        "collections": [{"key": c, "label": c.rstrip("/") + (" (folder)" if c.endswith("/") else ""),
                         "slot": i + 1 if i < 7 else 0, "peak": peaks[c]} for i, c in enumerate(cols)],
        "topics": [{"key": t["key"], "name": t["name"], "description": t.get("description", "")}
                   for t in tax["topics"]],
        "qtypes": list(QTYPES),
        "levels": [f"{i:04b}" for i in range(16)] if any(a.get("lvl") for a in arts) else [],
        "paths": (ledger.read_doc("content/paths.json") or {}).get("paths", []),
        "tiers": (ledger.read_doc("content/paths.json") or {}).get("tiers", []),
        "articles": rows,
        "source": {"taxonomy": tax.get("source"), "topics": dict(models), "versions": len(versions)},
    }


def build(ledger: Ledger, cache: Path, out: Path) -> Path:
    data = assemble(ledger, cache / "frames")
    out.mkdir(parents=True, exist_ok=True)
    dest_frames = out / "frames"
    keep = set()
    for p in data["pages"]:
        for fr in p["frames"]:
            src = cache / fr["image"]
            dst = out / fr["image"]
            keep.add(dst)
            if src.exists() and (not dst.exists() or dst.stat().st_size != src.stat().st_size):
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
    if dest_frames.exists():
        for f in dest_frames.rglob("*.webp"):
            if f not in keep:
                f.unlink()
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    (out / "data.json").write_text(raw, encoding="utf-8")
    (out / "data.js").write_text("window.CHRONICLE_DATA=" + raw + ";\n", encoding="utf-8")
    name = ledger.slug.split("/")[-1]
    html = (HERE / "templates" / "deck.html").read_text(encoding="utf-8")
    html = html.replace("{{TITLE}}", f"{name} Chronicle")
    # page.html is the bare page for hosts that add their own document shell
    # (such as a claude.ai Artifact); it fetches data.json. index.html is the
    # same page as a full document that opens straight from disk, so it loads
    # data.js instead (browsers refuse fetch() on file:// URLs).
    (out / "page.html").write_text(html.replace("<!--DATA-SCRIPT-->\n", ""), encoding="utf-8")
    html = html.replace("<!--DATA-SCRIPT-->", '<script src="data.js"></script>')
    full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
            'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n'
            + html + "\n</body>\n</html>\n")
    (out / "index.html").write_text(full, encoding="utf-8")
    return out / "index.html"


def export_video(presentation: Path, log=print) -> list[Path]:
    """MP4 time-lapses beside the deck: the file-system film, the page flipbook and the library film."""
    import subprocess
    import tempfile
    out = presentation.parent / "video"
    out.mkdir(exist_ok=True)
    made = []
    with tempfile.TemporaryDirectory() as tmp:
        res = subprocess.run(["node", str(HERE / "video.mjs"), str(presentation), tmp], capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"frame capture failed: {res.stderr[-600:]}")
        counts = json.loads(res.stdout.strip().splitlines()[-1])
        for name, sub, rate in (("filesystem", "fs", 12), ("frontend", "fe", 1.25), ("library", "lib", 12)):
            n = counts.get(sub, 0)
            if not n:
                continue
            target = out / f"{name}.mp4"
            cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(rate), "-i", f"{tmp}/{sub}/%05d.png",
                   "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2,fps=24", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                   "-crf", "24", "-movflags", "+faststart", str(target)]
            subprocess.run(cmd, check=True)
            made.append(target)
            log(f"[video] {target} ({n} frames)")
    return made
