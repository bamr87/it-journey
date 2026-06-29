#!/usr/bin/env python3
"""
classify_changes.py — the auto-merge smuggle guard.

Reads a list of changed file paths (one per line on stdin, e.g. from
`gh pr diff <n> --name-only`) and prints the distinct CATEGORIES present, one
per line, from:

  content   — pages/**, _data/{quests,navigation,...}, assets/** (the site)
  infra     — .github/**, scripts/**, Dockerfile, docker-compose, Gemfile*, Makefile
  config    — _config*.yml, _data/ai.yml, _data/brand/**, .cms/**, *.json config
  data      — other _data/**

The content auto-merge workflow refuses to merge any PR whose categories include
anything other than `content` — so an `auto:content` PR can never quietly carry a
workflow, dependency, brand-rule, or AI-config change to main without a human.
Unknown paths classify as `infra` (fail safe — when unsure, require a human).

The content category is deliberately broad (it includes theme files like
`_layouts/**`, `_includes/**`, `_sass/**`). A caller that needs a TIGHTER scope
than "any content" — e.g. the issue autopilot, whose resolver may only edit
`pages/**`, `assets/**`, `_data/quests/**` — adds `--allow-globs` to require that
every changed path also matches one of the given globs. `--content-only` and
`--allow-globs` compose: both must pass.

Usage:
    gh pr diff 123 --name-only | python3 scripts/ci/classify_changes.py
    python3 scripts/ci/classify_changes.py a.md b.yml      # paths as args
    ... | python3 scripts/ci/classify_changes.py --content-only   # exit 0 iff content-only
    ... | python3 scripts/ci/classify_changes.py --content-only \
              --allow-globs 'pages/**' 'assets/**' '_data/quests/**'  # tighter scope
"""
from __future__ import annotations

import argparse
import sys
from fnmatch import fnmatch

# Order matters: first matching rule wins. Most specific first.
RULES = [
    ("config", [
        "_config.yml", "_config*.yml",
        "_data/ai.yml", "_data/brand/*", "_data/brand/**",
        ".cms/*", ".cms/**",
        "frontmatter.json", ".frontmatter/*", ".frontmatter/**",
    ]),
    ("infra", [
        ".github/*", ".github/**",
        ".claude/*", ".claude/**",
        "scripts/*", "scripts/**",
        "Dockerfile", "docker-compose*.yml", "docker-compose*.yaml",
        "Gemfile", "Gemfile.lock", "Makefile",
        "*.gemspec", "package.json", "package-lock.json",
        "_plugins/*", "_plugins/**",
    ]),
    ("content", [
        "pages/*", "pages/**",
        "assets/*", "assets/**",
        "_layouts/*", "_layouts/**", "_includes/*", "_includes/**", "_sass/*", "_sass/**",
        "_data/quests/*", "_data/quests/**",
        "_data/navigation/*", "_data/navigation/**",
        "index.html", "index.md", "*.md",
    ]),
]
FALLBACK = "infra"   # unknown -> require a human (fail safe)


def classify_one(path: str) -> str:
    p = path.strip()
    if not p:
        return ""
    for category, patterns in RULES:
        for pat in patterns:
            if fnmatch(p, pat):
                return category
    return "data" if p.startswith("_data/") else FALLBACK


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Classify changed paths for the auto-merge guard.")
    ap.add_argument("paths", nargs="*", help="paths (else read stdin, one per line)")
    ap.add_argument("--content-only", action="store_true",
                    help="exit 0 iff every path is content; exit 1 otherwise")
    ap.add_argument("--allow-globs", nargs="*", default=None, metavar="GLOB",
                    help="require every changed path to match one of these globs "
                         "(tighter than --content-only); composes with it")
    args = ap.parse_args(argv)

    raw = [line for line in (args.paths if args.paths else sys.stdin.read().splitlines())
           if line.strip()]
    cats = []
    for line in raw:
        c = classify_one(line)
        if c and c not in cats:
            cats.append(c)

    # When either gate is requested, ALL requested gates must pass (exit 0/1).
    if args.content_only or args.allow_globs is not None:
        ok = True
        if args.content_only:
            content_ok = bool(cats) and cats == ["content"]
            if not content_ok:
                others = [c for c in cats if c != "content"] or ["<empty diff>"]
                print(f"not content-only: also touches {', '.join(others)}", file=sys.stderr)
            ok = ok and content_ok
        if args.allow_globs is not None:
            offenders = [p.strip() for p in raw
                         if not any(fnmatch(p.strip(), g) for g in args.allow_globs)]
            # An empty diff is never "allowed" — there is nothing legitimate to merge.
            if not raw:
                print("no changed paths — refusing (nothing to merge)", file=sys.stderr)
                ok = False
            elif offenders:
                print(f"outside allowed scope ({', '.join(args.allow_globs)}): "
                      f"{', '.join(offenders)}", file=sys.stderr)
                ok = False
        return 0 if ok else 1

    for c in cats:
        print(c)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
