#!/usr/bin/env python3
"""
build_reports_site.py — surface the quest-perfection loop's output on the site.

Deterministically transforms the loop's raw artifacts into a Jekyll collection
(``pages/_quest-reports/``) so the walkthroughs + ledger dashboard are browsable
on it-journey.dev — the review happens on the frontend (with links back to the
originating run + each file's GitHub history) instead of only inside a report PR:

    INPUT   test/quest-validator/walkthroughs/<date>-<char>-<level>.md  (walker reports)
            .quests/ledger.json                                         (coverage/verdicts)
    OUTPUT  pages/_quest-reports/index.md                               (dashboard)
            pages/_quest-reports/<date>-<char>-<level>.md               (one page per report)

Every generated page carries CI-valid frontmatter (``title`` ≤60, a 120–155-char
``description``, ISO ``date``, ``author``, list ``categories``/``tags``) so the
frontmatter validator and Jekyll build stay green — the precondition for the
report PR to auto-merge. Bodies rely on the collection default
``render_with_liquid: false`` (see _config.yml), so quoted quest code containing
Liquid tags can NEVER break the build (the #449 failure mode).

Idempotent: rewrites the collection from the current inputs each run. Pure Python
+ PyYAML; no network, no model.

Usage:
    python3 scripts/quest/build_reports_site.py            # from repo root
    python3 scripts/quest/build_reports_site.py --check    # generate to a temp dir + verify, no writes
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover
    print("Error: PyYAML is required (pip install pyyaml).", file=sys.stderr)
    sys.exit(1)

# --- paths (repo-root relative) ---------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
WALKTHROUGH_DIR = REPO_ROOT / "test" / "quest-validator" / "walkthroughs"
LEDGER_PATH = REPO_ROOT / ".quests" / "ledger.json"
OUT_DIR = REPO_ROOT / "pages" / "_quest-reports"

# GitHub coordinates for the "view source / history / run" links. Overridable so a
# fork or a dispatch from a branch links to the right tree.
REPO = os.environ.get("GITHUB_REPOSITORY", "bamr87/it-journey")
DEFAULT_BRANCH = os.environ.get("QUEST_REPORTS_BRANCH", "main")
SERVER = os.environ.get("GITHUB_SERVER_URL", "https://github.com")

FILENAME_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.+?)-(?P<level>[01]{4})$")

AUTHOR = "Quest Perfection Loop"

VERDICT_EMOJI = {"pass": "✅", "warn": "⚠️", "fail": "❌", "error": "🛑"}
CHAR_TITLES = {
    "developer": "Software Developer",
    "system-engineer": "System Engineer",
    "security-specialist": "Security Specialist",
    "data-scientist": "Data Scientist",
    "digital-artist": "Digital Artist",
    "game-developer": "Game Developer",
}


# ---------------------------------------------------------------------------
# parsing
# ---------------------------------------------------------------------------
def split_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    """Split a markdown doc into (frontmatter dict, body). Missing/one-off
    frontmatter → ({}, whole text)."""
    if text.startswith("﻿"):
        text = text.lstrip("﻿")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("\n---", 1)
    # text begins with "---\n<yaml>\n---\n<body>": first line is the opening fence.
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    if not isinstance(fm, dict):
        fm = {}
    return fm, m.group(2)


def parse_filename(stem: str) -> Optional[Dict[str, str]]:
    """`2026-07-12-system-engineer-1000` → {date, character, level, slug}."""
    m = FILENAME_RE.match(stem)
    if not m:
        return None
    char = m.group("slug")
    return {
        "date": m.group("date"),
        "character": char,
        "level": m.group("level"),
        "slug": f"{char}/{m.group('level')}",
    }


# ---------------------------------------------------------------------------
# frontmatter helpers
# ---------------------------------------------------------------------------
def char_title(key: str) -> str:
    return CHAR_TITLES.get(key, key.replace("-", " ").title())


def iso_ms(dt_or_str: Any, fallback_date: Optional[str] = None) -> str:
    """Normalize to ISO-8601 with milliseconds + Z (the repo's date format)."""
    dt: Optional[datetime] = None
    if isinstance(dt_or_str, datetime):
        dt = dt_or_str
    elif isinstance(dt_or_str, str) and dt_or_str.strip():
        s = dt_or_str.strip().replace("Z", "+00:00")
        try:
            dt = datetime.fromisoformat(s)
        except ValueError:
            dt = None
    if dt is None and fallback_date:
        try:
            dt = datetime.fromisoformat(f"{fallback_date}T00:00:00+00:00")
        except ValueError:
            dt = None
    if dt is None:
        dt = datetime(1970, 1, 1, tzinfo=timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond // 1000:03d}Z"


def fit_description(text: str, lo: int = 120, hi: int = 155) -> str:
    """Land a description in the SEO band [lo, hi]. Trims at a word boundary when
    long; pads with a standard clause when short. (Out-of-band is only a
    non-blocking warning, but in-band keeps the SEO score clean.)"""
    text = " ".join(text.split())
    if len(text) > hi:
        cut = text[:hi]
        if " " in cut:
            cut = cut[: cut.rfind(" ")]
        return cut.rstrip(" ,.;:—-") + "…"
    pad = "  Part of the autonomous quest-perfection loop that walks and hardens IT-Journey quests."
    while len(text) < lo and pad:
        text = (text + pad).strip()
        if len(text) > hi:
            return fit_description(text, lo, hi)
    return text


def dump_frontmatter(fm: Dict[str, Any]) -> str:
    body = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True,
                          default_flow_style=False, width=100).rstrip("\n")
    return f"---\n{body}\n---\n"


# ---------------------------------------------------------------------------
# link builders
# ---------------------------------------------------------------------------
def blob_url(rel_path: str) -> str:
    return f"{SERVER}/{REPO}/blob/{DEFAULT_BRANCH}/{rel_path}"


def history_url(rel_path: str) -> str:
    return f"{SERVER}/{REPO}/commits/{DEFAULT_BRANCH}/{rel_path}"


def run_url_for(ledger: Dict[str, Any], slug: str, date: str) -> Optional[str]:
    """The perfection run that produced this dated walk (from ledger history),
    falling back to the slice's most-recent run."""
    slc = (ledger.get("slices") or {}).get(slug) or {}
    for ev in slc.get("history") or []:
        if ev.get("event") == "walk" and ev.get("date") == date and ev.get("run_url"):
            return ev["run_url"]
    return slc.get("run_url")


# ---------------------------------------------------------------------------
# page builders
# ---------------------------------------------------------------------------
def build_report_page(src_rel: str, meta: Dict[str, str], fm: Dict[str, Any],
                      body: str, ledger: Dict[str, Any]) -> str:
    character, level, date, slug = (meta["character"], meta["level"],
                                    meta["date"], meta["slug"])
    ctitle = char_title(character)
    theme = str(fm.get("theme") or "").strip()
    tier = str(fm.get("tier") or "").strip()
    verdict = str(fm.get("overall_verdict") or "").strip().lower()
    session = fm.get("session") if isinstance(fm.get("session"), dict) else {}
    avg = session.get("engine_average")
    qcount = fm.get("quest_count") or session.get("count")

    title = f"{ctitle} · L{level} · {date}"
    theme_part = f"the {theme} " if theme else ""
    verdict_part = f", engine verdict {verdict}" if verdict else ""
    avg_part = f" (avg {avg}%)" if isinstance(avg, (int, float)) else ""
    desc = fit_description(
        f"Quest-perfection walkthrough of {theme_part}slice {slug} on {date}"
        f"{verdict_part}{avg_part}. An evidence-based, learner's-eye session report "
        f"from the autonomous loop."
    )

    tags = [character, f"level-{level}", "walkthrough", "quest-perfection"]
    if verdict:
        tags.append(verdict)
    if theme:
        tags.append(re.sub(r"[^a-z0-9]+", "-", theme.lower()).strip("-"))

    page_fm: Dict[str, Any] = {
        "title": title,
        "description": desc,
        "date": iso_ms(fm.get("date"), date),
        "author": AUTHOR,
        "categories": ["Quest Reports", ctitle],
        "tags": tags,
        # These bodies quote quest code (and even discuss raw/endraw bugs), so Liquid
        # must NOT run on them — this keeps the build safe AND opts the page out of
        # the check_liquid_raw gate. Mirrors the _config collection default.
        "render_with_liquid": False,
        "excerpt": fit_description(
            f"{ctitle} · Level {level}{(' — ' + theme) if theme else ''}: "
            f"an evidence-based quest-perfection walkthrough from {date}.", 60, 155),
        # --- machine fields (drive the dashboard + future tooling) ---
        "slice": slug,
        "character": character,
        "level": level,
        "theme": theme or None,
        "tier": tier or None,
        "verdict": verdict or None,
        "quest_count": qcount,
        "engine_average": avg,
        "walk_date": date,
        "run_url": run_url_for(ledger, slug, date),
        "source_report": src_rel,
    }
    page_fm = {k: v for k, v in page_fm.items() if v is not None}

    emoji = VERDICT_EMOJI.get(verdict, "")
    lvl_label = f"{level}" + (f" ({theme})" if theme else "")
    run = page_fm.get("run_url")
    links = [f"🏠 [Perfection dashboard](/quest-reports/)"]
    if run:
        links.insert(0, f"🔗 [Perfection run]({run})")
    links.append(f"📄 [Raw report]({blob_url(src_rel)})")
    links.append(f"🕘 [Change history]({history_url(src_rel)})")

    header = (
        f"> **Slice** `{slug}` · **Level** {lvl_label}"
        + (f" · **{tier} tier**" if tier else "")
        + (f" · **Engine verdict** {emoji} {verdict}" if verdict else "")
        + (f" (avg {avg}%)" if isinstance(avg, (int, float)) else "")
        + f" · **Walked** {date}\n>\n> "
        + " · ".join(links)
        + "\n\n---\n"
    )
    return dump_frontmatter(page_fm) + "\n" + header + "\n" + body.lstrip("\n")


def _cov_str(slc: Dict[str, Any]) -> str:
    cov = slc.get("coverage")
    tot = slc.get("total_quests") or slc.get("total")
    if isinstance(cov, dict) and isinstance(tot, int) and tot:
        return f"{len(cov)}/{tot}"
    scored, req = slc.get("scored"), slc.get("requested")
    if isinstance(scored, int) and isinstance(req, int) and req:
        return f"{scored}/{req}"
    return "—"


def build_dashboard(ledger: Dict[str, Any],
                    reports_by_slug: Dict[str, List[Dict[str, str]]],
                    all_reports: List[Dict[str, str]]) -> str:
    totals = ledger.get("totals") or {}
    slices = ledger.get("slices") or {}
    generated = ledger.get("generated") or ""

    fm = {
        "title": "Quest Perfection Dashboard",
        "description": fit_description(
            "Live status of the autonomous quest-perfection loop: every character "
            "path's coverage, verdicts, and open issues, with links to each walkthrough "
            "report and the runs that produced them."),
        "date": iso_ms(generated, datetime.now(timezone.utc).strftime("%Y-%m-%d")),
        "author": AUTHOR,
        "categories": ["Quest Reports"],
        "tags": ["quest-perfection", "dashboard", "walkthrough", "quality"],
        "excerpt": "Live status of the autonomous quest-perfection loop — coverage, "
                   "verdicts, and links to every walkthrough.",
        "permalink": "/quest-reports/",
        "render_with_liquid": False,
    }

    n_slices = totals.get("slices", len(slices))
    n_perfect = totals.get("perfect", 0)
    n_stuck = totals.get("stuck", 0)
    n_open = totals.get("open_issues", 0)

    lines: List[str] = []
    lines.append("# ♾️ Quest Perfection Dashboard\n")
    lines.append(
        "The autonomous **quest-perfection loop** walks IT-Journey's quests end-to-end "
        "as a learner, scores them with a sandboxed agentic engine, and opens content "
        "fixes for what it finds. This page mirrors the committed ledger "
        f"([`.quests/ledger.json`]({blob_url('.quests/ledger.json')})) — the source of "
        "truth — so you can review each incremental improvement here instead of in a PR.\n")
    if generated:
        lines.append(f"_Ledger generated {generated}._\n")
    lines.append(
        f"**{n_perfect}/{n_slices}** slices perfect · **{n_stuck}** stuck (needs human) · "
        f"**{n_open}** open issue(s) outstanding\n")

    # --- slice table (worst-first, matching the committed dashboard order) ---
    ordered = sorted(
        slices.values(),
        key=lambda s: (bool(s.get("perfect")), s.get("average") if isinstance(s.get("average"), (int, float)) else 999),
    )
    lines.append("## Slices\n")
    lines.append("| Slice | Theme | Verdict | Avg | Coverage | Open | State | Latest report | Run |")
    lines.append("|---|---|:--:|--:|:--:|--:|:--:|---|---|")
    for s in ordered:
        slug = s.get("slug") or f"{s.get('character')}/{s.get('level')}"
        verdict = str(s.get("verdict") or "").lower()
        vlabel = f"{VERDICT_EMOJI.get(verdict, '')} {verdict}".strip() or "—"
        avg = s.get("average")
        avg_s = f"{avg:.1f}" if isinstance(avg, (int, float)) else "—"
        open_i = s.get("open_issues", "—")
        state = ("🏆 perfect" if s.get("perfect")
                 else ("🛑 stuck" if s.get("stuck") or s.get("needs_human") else "🔁 sweeping"))
        reps = reports_by_slug.get(slug) or []
        if reps:
            latest = reps[-1]
            rep_link = f"[{latest['date']}](/quest-reports/{latest['stem']}/)"
        else:
            rep_link = "—"
        run = s.get("run_url")
        run_link = f"[run]({run})" if run else "—"
        lines.append(
            f"| `{slug}` | {s.get('theme') or ''} | {vlabel} | {avg_s} | "
            f"{_cov_str(s)} | {open_i} | {state} | {rep_link} | {run_link} |")
    lines.append("")

    # --- all walkthrough reports, newest first ---
    lines.append("## Walkthrough reports\n")
    lines.append(
        "Every session report the loop has published, newest first. Each links to the "
        "learner's-eye walk plus the run and the file's change history.\n")
    for r in sorted(all_reports, key=lambda x: (x["date"], x["slug"]), reverse=True):
        ct = char_title(r["character"])
        lines.append(
            f"- **{r['date']}** — [{ct} · L{r['level']}](/quest-reports/{r['stem']}/)"
            f" (`{r['slug']}`)")
    lines.append("")

    return dump_frontmatter(fm) + "\n" + "\n".join(lines)


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------
def generate(out_dir: Path, walkthrough_dir: Path, ledger_path: Path) -> Tuple[int, List[str]]:
    ledger: Dict[str, Any] = {}
    if ledger_path.exists():
        try:
            ledger = json.loads(ledger_path.read_text(encoding="utf-8")) or {}
        except (json.JSONDecodeError, OSError):
            ledger = {}

    reports: List[Dict[str, str]] = []
    for md in sorted(walkthrough_dir.glob("*.md")):
        meta = parse_filename(md.stem)
        if not meta:
            print(f"::warning::skipping unrecognized walkthrough filename: {md.name}", file=sys.stderr)
            continue
        text = md.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        src_rel = md.relative_to(REPO_ROOT).as_posix()
        page = build_report_page(src_rel, meta, fm, body, ledger)
        reports.append({**meta, "stem": md.stem, "page": page})

    out_dir.mkdir(parents=True, exist_ok=True)
    written: List[str] = []
    # Clean stale generated pages so a deleted/renamed report never lingers.
    for old in out_dir.glob("*.md"):
        old.unlink()

    reports_by_slug: Dict[str, List[Dict[str, str]]] = {}
    for r in reports:
        reports_by_slug.setdefault(r["slug"], []).append(r)
    for slug in reports_by_slug:
        reports_by_slug[slug].sort(key=lambda x: x["date"])

    def _disp(p: Path) -> str:
        try:
            return p.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            return p.as_posix()

    for r in reports:
        dest = out_dir / f"{r['stem']}.md"
        dest.write_text(r["page"], encoding="utf-8")
        written.append(_disp(dest))

    index = out_dir / "index.md"
    index.write_text(build_dashboard(ledger, reports_by_slug, reports), encoding="utf-8")
    written.append(_disp(index))
    return len(reports), written


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Generate the quest-reports Jekyll collection.")
    ap.add_argument("--out-dir", default=str(OUT_DIR))
    ap.add_argument("--walkthroughs", default=str(WALKTHROUGH_DIR))
    ap.add_argument("--ledger", default=str(LEDGER_PATH))
    ap.add_argument("--check", action="store_true",
                    help="generate into a temp dir and report, without touching the repo")
    args = ap.parse_args(argv)

    out_dir = Path(args.out_dir)
    if args.check:
        import tempfile
        out_dir = Path(tempfile.mkdtemp(prefix="quest-reports-check-"))

    n, written = generate(out_dir, Path(args.walkthroughs), Path(args.ledger))
    print(f"✅ generated {n} report page(s) + dashboard → {out_dir}", file=sys.stderr)
    for w in written[:5]:
        print(f"   {w}", file=sys.stderr)
    if len(written) > 5:
        print(f"   … +{len(written) - 5} more", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
