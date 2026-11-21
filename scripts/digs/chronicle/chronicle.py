#!/usr/bin/env python3
"""chronicle — a time-lapse presentation of a Git repository's real history.

Reads every commit of any repository once, files the facts in a ledger
(docs/git-archaeology/chronicle/<owner>/<repo>/), asks a model only for what
needs judgement (what a commit meant, where the eras turn, what was learned),
and builds a presentation: a file-system time-lapse, a page-by-page front-end
time-lapse, the stack's evolution, the eras and their lessons.

    python3 scripts/digs/chronicle/chronicle.py run --repo ../zer0-mistakes
    python3 scripts/digs/chronicle/chronicle.py status --repo ../zer0-mistakes
    python3 scripts/digs/chronicle/chronicle.py show <sha> --repo ../zer0-mistakes

A re-run reads only commits the ledger has not filed and asks the model only
for annotations it has not stored. See README.md beside this file.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from core import DEFAULT_CACHE_ROOT, DEFAULT_LEDGER_ROOT, Ledger, default_ref, repo_slug  # noqa: E402


def _context(args) -> tuple[Path, Ledger, str]:
    repo = Path(args.repo).resolve()
    slug = args.slug or repo_slug(repo)
    ledger = Ledger(Path(args.ledger_root).resolve(), slug)
    ref = args.ref or default_ref(repo)
    return repo, ledger, ref


def cmd_ingest(args) -> int:
    from ingest import ingest
    repo, ledger, ref = _context(args)
    res = ingest(repo, ledger, ref)
    print(json.dumps(res))
    return 0


def cmd_annotate(args) -> int:
    from ai import annotate_commits, provider_from_args
    repo, ledger, ref = _context(args)
    res = annotate_commits(ledger, provider_from_args(args, "commits"), batch=args.batch, limit=args.limit)
    print(json.dumps(res))
    return 0


def cmd_eras(args) -> int:
    from ai import provider_from_args, read_eras
    repo, ledger, ref = _context(args)
    res = read_eras(ledger, provider_from_args(args, "eras"), force=args.force)
    print(json.dumps({"eras": len(res["eras"]), "source": res.get("source")}))
    return 0


def cmd_frames(args) -> int:
    from frames import render_frames
    repo, ledger, ref = _context(args)
    cache = Path(args.cache_root).resolve() / ledger.slug.replace("/", "__")
    res = render_frames(repo, ledger, cache, pages=args.pages, per_page=args.per_page, shoot=not args.no_shoot)
    print(json.dumps(res))
    return 0


def cmd_build(args) -> int:
    from present import build
    repo, ledger, ref = _context(args)
    cache = Path(args.cache_root).resolve() / ledger.slug.replace("/", "__")
    out = Path(args.out).resolve() if args.out else cache / "presentation"
    path = build(ledger, cache, out)
    print(path)
    return 0


def cmd_video(args) -> int:
    from present import export_video
    repo, ledger, ref = _context(args)
    cache = Path(args.cache_root).resolve() / ledger.slug.replace("/", "__")
    out = Path(args.out).resolve() if args.out else cache / "presentation"
    for path in export_video(out / "index.html"):
        print(path)
    return 0


def cmd_run(args) -> int:
    steps = [cmd_ingest, cmd_annotate, cmd_eras, cmd_frames, cmd_build]
    if args.video:
        steps.append(cmd_video)
    for step in steps:
        rc = step(args)
        if rc:
            return rc
    return 0


def cmd_status(args) -> int:
    repo, ledger, ref = _context(args)
    commits = ledger.commits()
    ann = ledger.annotations()
    eras = ledger.read_doc("eras.json") or {}
    man = ledger.manifest()
    print(json.dumps({
        "repository": ledger.slug, "ledger": str(ledger.dir), "head": man.get("head"),
        "commits_filed": len(commits), "annotated": len(ann),
        "annotated_by": _count(a.get("model", "?") for a in ann.values()),
        "eras": len(eras.get("eras", [])), "eras_source": eras.get("source"),
    }, indent=1))
    return 0


def cmd_show(args) -> int:
    repo, ledger, ref = _context(args)
    commits = ledger.commits()
    hits = [s for s in commits if s.startswith(args.sha)]
    if len(hits) != 1:
        print(f"{len(hits)} commits match {args.sha!r}", file=sys.stderr)
        return 1
    row = dict(commits[hits[0]])
    row["annotation"] = ledger.annotations().get(hits[0])
    print(json.dumps(row, indent=1, ensure_ascii=False))
    return 0


def _count(items) -> dict:
    out: dict = {}
    for i in items:
        out[i] = out.get(i, 0) + 1
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--repo", default=".", help="path to the repository checkout (default: .)")
        p.add_argument("--ref", help="ref to read (default: origin/main, origin/master, main, master, HEAD)")
        p.add_argument("--slug", help="owner/name (default: parsed from the origin URL)")
        p.add_argument("--ledger-root", default=str(DEFAULT_LEDGER_ROOT), help="where ledgers live")
        p.add_argument("--cache-root", default=str(DEFAULT_CACHE_ROOT), help="frames and builds (gitignored)")

    def ai_opts(p):
        p.add_argument("--ai", choices=("claude", "off"), default="claude",
                       help="model route; 'off' uses the deterministic fallback")
        p.add_argument("--model", help="override the model for this step")
        p.add_argument("--budget", type=float, default=None, help="max USD per model call")
        p.add_argument("--batch", type=int, default=40, help="commits per annotation call")
        p.add_argument("--limit", type=int, default=0, help="annotate at most N commits this run (0 = all)")
        p.add_argument("--force", action="store_true", help="re-read eras even if inputs are unchanged")

    def frame_opts(p):
        p.add_argument("--pages", type=int, default=4, help="pages in the front-end time-lapse")
        p.add_argument("--per-page", type=int, default=18, help="frames per page")
        p.add_argument("--no-shoot", action="store_true", help="render HTML but skip screenshots")

    for name, fn, extra in (
        ("ingest", cmd_ingest, ()), ("annotate", cmd_annotate, (ai_opts,)), ("eras", cmd_eras, (ai_opts,)),
        ("frames", cmd_frames, (frame_opts,)), ("build", cmd_build, ()), ("video", cmd_video, ()),
        ("run", cmd_run, (ai_opts, frame_opts)), ("status", cmd_status, ()),
    ):
        p = sub.add_parser(name)
        common(p)
        for e in extra:
            e(p)
        if name in ("build", "run", "video"):
            p.add_argument("--out", help="presentation directory (default: <cache>/presentation)")
        if name == "run":
            p.add_argument("--video", action="store_true", help="also export MP4 time-lapses (needs ffmpeg)")
        p.set_defaults(fn=fn)
    p = sub.add_parser("show")
    common(p)
    p.add_argument("sha")
    p.set_defaults(fn=cmd_show)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
