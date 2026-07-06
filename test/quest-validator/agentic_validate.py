#!/usr/bin/env python3
"""
Agentic Quest Validator (tier 2) — IT-Journey.

Drives **Claude Code** (authenticated via OAuth) to read quests, attempt their
commands end-to-end in an isolated sandbox, and return a weighted score (0-100)
plus prioritized recommendations. This complements the structural validator
(``quest_validator.py``, tier 1), which only checks shape/schema/Liquid safety.

Auth: the ``claude`` CLI handles it. Locally it uses your logged-in session;
in CI export ``CLAUDE_CODE_OAUTH_TOKEN`` (generate with ``claude setup-token``).

Examples:
  # Offline pipeline test (no CLI, no cost):
  agentic_validate.py -d pages/_quests --sample 3 --mock --summary

  # Inspect exactly what would be sent (no invocation):
  agentic_validate.py pages/_quests/0101/secrets-management.md --dry-run

  # Real read-only review of one quest:
  agentic_validate.py pages/_quests/0101/secrets-management.md

  # Sandboxed end-to-end run of a representative sample, write reports, gate at 70%:
  agentic_validate.py -d pages/_quests --sample 5 --mode execute \
      --md review.md --report review.json --fail-threshold 70
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from agentic import loader, report, runner, schema  # noqa: E402


def _collect_quests(args):
    if args.quest_files:
        out = []
        for f in args.quest_files:
            q = loader.load_quest(f)
            if q is None:
                print(f"⚠️  Skipping (not a parseable quest): {f}", file=sys.stderr)
                continue
            out.append(q)
        if not out:
            print("❌ None of the given files are parseable quests.", file=sys.stderr)
            sys.exit(2)
        return out
    quests = loader.discover(args.directory, include_drafts=args.include_drafts)
    if args.sample and args.sample > 0:
        quests = loader.sample(quests, args.sample)
    return quests


def main():
    p = argparse.ArgumentParser(
        description="Agentic (Claude Code / OAuth) end-to-end quest validator.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("quest_files", nargs="*", help="One or more quest .md files to validate.")
    p.add_argument("-d", "--directory", help="Directory of quests (default: pages/_quests).")
    p.add_argument("--sample", type=int, default=0,
                   help="Evaluate a representative sample of N quests (spread across levels).")
    p.add_argument("--include-drafts", action="store_true", help="Include draft quests.")
    p.add_argument("--mode", choices=["review", "execute"], default="review",
                   help="review = read-only expert assessment (safe anywhere); "
                        "execute = run safe commands in a sandbox (use in CI/containers).")
    p.add_argument("--model", help="Model override passed to claude (e.g. an alias).")
    p.add_argument("--timeout", type=int, default=600, help="Per-quest timeout in seconds (default 600).")
    p.add_argument("--max-turns", type=int, default=0,
                   help="Per-quest agent turn ceiling (0 = CLI default). Bounds runaway loops.")
    p.add_argument("--max-cost-usd", type=float, default=0.0,
                   help="Abort the batch once cumulative reported cost exceeds this (0 = no ceiling).")
    p.add_argument("--isolate", choices=["none", "docker"], default="none",
                   help="execute-mode isolation. 'docker' is provided by running this whole "
                        "validator inside a container (see `make docker-audit-tier2`); accepted "
                        "here so callers can pass it through without erroring.")
    p.add_argument("--claude-bin", default="claude", help="Path to the claude CLI.")
    p.add_argument("--mock", action="store_true",
                   help="Synthetic deterministic verdicts (no CLI, no cost) — for pipeline testing.")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the command + prompts that WOULD be sent, then exit.")
    p.add_argument("--list", action="store_true", help="List the quests that would be evaluated, then exit.")
    p.add_argument("--report", "--json", dest="report", help="Write the full results as JSON to this file.")
    p.add_argument("--md", help="Write a markdown report to this file (CI artifact / PR comment).")
    p.add_argument("--summary", action="store_true", help="Print the markdown summary to stdout too.")
    p.add_argument("--fail-threshold", type=int, default=0,
                   help="Exit non-zero if any quest's score is below this %% (0 = never fail).")
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()

    quests = _collect_quests(args)
    if not quests:
        print("No quests matched.", file=sys.stderr)
        sys.exit(2)

    if args.list:
        for q in quests:
            print(f"{q.level}  {q.rel_path}  —  {q.title}")
        print(f"\n{len(quests)} quest(s).")
        sys.exit(0)

    r = runner.AgenticRunner(
        mode=args.mode, model=args.model, timeout=args.timeout,
        claude_bin=args.claude_bin, mock=args.mock, dry_run=args.dry_run,
        verbose=args.verbose, max_turns=args.max_turns,
    )

    if not (args.mock or args.dry_run) and not r.available():
        print(f"❌ `{args.claude_bin}` not found on PATH.\n"
              f"   Install Claude Code and run `claude setup-token`, or use --mock for a pipeline test.",
              file=sys.stderr)
        sys.exit(2)

    if args.mode == "execute" and not (args.mock or args.dry_run) and not os.environ.get("CI"):
        print("⚠️  execute mode runs the quests' commands for real. The sandbox is a temp dir, "
              "NOT a hard filesystem boundary — prefer a disposable container/CI runner. "
              "Use --mode review for a safe read-only assessment.", file=sys.stderr)

    if args.dry_run:
        for q in quests:
            out = r.run(q)
            print(f"\n=== {q.rel_path} ===")
            print("command:", " ".join(out["command"]))
            print(f"\n--- system prompt ({len(out['system_prompt'])} chars) ---\n{out['system_prompt']}")
            print(f"\n--- user prompt ---\n{out['user_prompt']}")
        sys.exit(0)

    results = []
    spent = 0.0
    truncated = False
    auth_truncated = False
    for i, q in enumerate(quests, 1):
        if args.max_cost_usd and spent >= args.max_cost_usd:
            print(f"\n💰 Cost ceiling reached (${spent:.4f} ≥ ${args.max_cost_usd}); "
                  f"stopping after {i - 1}/{len(quests)} quest(s).", file=sys.stderr)
            truncated = True
            break
        if not args.mock:
            print(f"[{i}/{len(quests)}] {args.mode}: {q.rel_path} …", file=sys.stderr, flush=True)
        try:
            res = r.run(q)
            results.append(res)
            spent += (res.get("meta", {}) or {}).get("cost_usd") or 0.0
        except runner.AuthError as e:
            # Auth won't recover between quests (throttle / expired token), so stop
            # the batch — but DON'T discard the quests that already scored. We
            # aggregate + write the partial evidence below (marked truncated), so a
            # rate-limited run still contributes its completed quests as coverage
            # rather than reddening the job and losing everything. A run that got
            # ZERO quests still hard-fails (exit 2) at the end.
            print(f"\n⚠️  {e}", file=sys.stderr)
            print(f"⚠️  Auth failed after {len(results)}/{len(quests)} quest(s) — "
                  f"stopping the batch and writing PARTIAL evidence.", file=sys.stderr)
            truncated = True
            auth_truncated = True
            break
        except runner.RunnerError as e:
            results.append({"quest": q.to_meta(), "mode": args.mode, "meta": {},
                            "error": str(e), "overall": 0.0, "verdict": schema.VERDICT_FAIL,
                            "verdict_obj": None})

    agg = report.aggregate(results)
    if truncated:
        # Record partial coverage so a truncated batch is never mistaken for full,
        # clean coverage (by a human, the ledger, or the gate below).
        agg["truncated"] = True
        agg["evaluated"] = len(results)
        agg["requested"] = len(quests)
        if auth_truncated:
            agg["auth_truncated"] = True
    print("\n" + report.render_console(agg, verbose=args.verbose))
    if truncated:
        cause = "auth failure" if auth_truncated else "cost ceiling"
        print(f"\n⚠️  BATCH TRUNCATED by {cause} — evaluated {len(results)}/{len(quests)} quest(s). "
              f"The score gate covers only the evaluated subset.", file=sys.stderr)

    if args.report:
        Path(args.report).write_text(report.render_json(agg), encoding="utf-8")
        print(f"\n📄 JSON report → {args.report}")
    if args.md:
        Path(args.md).write_text(report.render_markdown(agg), encoding="utf-8")
        print(f"📝 Markdown report → {args.md}")
    if args.summary:
        print("\n" + report.render_markdown(agg))

    # Exit code: gate on threshold if requested; always non-zero if everything errored.
    if args.fail_threshold > 0:
        below = [r for r in results if r.get("overall", 0) < args.fail_threshold]
        if below:
            print(f"\n❌ {len(below)} quest(s) below {args.fail_threshold}%.", file=sys.stderr)
            sys.exit(1)
        # A truncated batch cannot certify the quests it never evaluated, so a
        # gated run must NOT report success on partial coverage.
        if truncated:
            print(f"\n❌ Cannot certify a cost-truncated batch against a "
                  f"{args.fail_threshold}% gate ({len(results)}/{len(quests)} evaluated).",
                  file=sys.stderr)
            sys.exit(1)
    # Nothing scored is a hard failure regardless of cause — an auth throttle that
    # let ZERO quests through is exit 2 (matching the pre-partial behavior), any
    # other empty run is exit 1. A PARTIAL run that scored ≥1 quest exits 0: it
    # wrote usable (truncated) evidence the ledger records as coverage, and the
    # caller shouldn't red the whole slice job for an expected rate-limit.
    if agg["scored"] == 0:
        sys.exit(2 if auth_truncated else 1)
    sys.exit(0)


if __name__ == "__main__":
    main()
