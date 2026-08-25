#!/usr/bin/env python3
"""
loop_health.py — the quest-perfection loop's self-maintained health issue.

The loop runs unattended. When it CANNOT make progress — the shared Claude
credential is rejected, or every slice is rate-limited — a red workflow run is
the wrong alarm: scheduled runs attach their check-runs to main's HEAD, and
sync-gh-pages deploys only a fully-green HEAD, so a daily red quietly **stops
the site publishing** (that is exactly what eight consecutive dead-token runs
did). Runs therefore stay green on these EXPECTED failure modes, and THIS
script is the loud part: it keeps exactly ONE open GitHub issue describing what
is wrong and what a human must do, then closes it the moment the loop scores
again.

Contract:
  report  --kind auth|rate-limit|engine --lane walk|fix --run-url URL [--detail …]
          Upsert the single health issue (label: quest-loop-health). Creates it
          if absent; otherwise adds a comment, but at most one per
          --min-repeat-hours per kind so a daily schedule can't spam.
  resolve --run-url URL [--note …]
          Close the open health issue (if any) with a "recovered" comment.
          Called by the report job whenever a run scores >=1 quest.

Dedupe is by LABEL, never by title, so a human may rename the issue freely.
Everything is best-effort over the `gh` CLI (GH_TOKEN in env): health reporting
must never be the thing that fails the pipeline, so any gh error is a warning
and exit 0. Exit is non-zero only for bad invocations.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

LABEL = "quest-loop-health"
# Route the issue in the issue-autopilot: needs-human is its own escalation
# label, keeping this out of every recommend-close disposition.
EXTRA_LABELS = ["automated", "needs-human"]
MARKER = "<!-- quest-loop-health"          # comment marker prefix: `<!-- quest-loop-health:KIND -->`
TITLE = "♾️ Quest perfection loop needs attention (auto-diagnosed)"

KINDS = {
    "auth": {
        "headline": "Claude credentials are broken — the loop is halted until a human rotates the token",
        "body": (
            "Every engine call is **rejected before a single quest can be scored** "
            "(invalid / expired / revoked token, or a billing hold on the account). "
            "Retrying on the schedule cannot fix this — the same secret fails "
            "identically every day.\n\n"
            "**How to fix**\n\n"
            "1. On a machine with a logged-in Claude Code: `claude setup-token`\n"
            "2. `gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo {repo}` (paste the token)\n"
            "3. Optionally re-run the workflow, or just wait for the next schedule.\n"
        ),
    },
    "rate-limit": {
        "headline": "Claude rate limit exhausted for the whole run — no quest scored",
        "body": (
            "The shared token hit a **sustained rate limit** and zero quests scored "
            "this run. The window refills on its own, so the loop simply retries on "
            "its next schedule — occasionally this is normal.\n\n"
            "**If this repeats daily**: something else is draining the shared window "
            "before the loop's cron fires. Consider moving this workflow's schedule, "
            "spacing the other Claude workflows, or reviewing plan limits.\n"
        ),
    },
    "engine": {
        "headline": "The execute engine produced no scored quests, and not because of auth or rate limits",
        "body": (
            "Slices ran but no quest scored, and the evidence carries **no auth or "
            "rate-limit signal** — this smells like an engine or workflow bug, not "
            "credentials. Read the run logs (link below) and the uploaded "
            "`walk-evidence.json` artifacts.\n"
        ),
    },
}

FOOTER = (
    "\n---\n"
    "_This issue is opened, updated, and closed automatically by the quest-perfection "
    "loop (`scripts/quest/loop_health.py`). It closes itself on the loop's next "
    "productive run — resolve the cause rather than the issue._\n"
)


def _gh(*args: str) -> subprocess.CompletedProcess:
    # Explicit -R: these jobs check out with persist-credentials:false, so repo
    # detection from the git remote is not guaranteed — never rely on it.
    return subprocess.run(["gh", args[0], args[1], "-R", _repo(), *args[2:]],
                          capture_output=True, text=True)


def _warn(msg: str) -> None:
    print(f"::warning::loop-health: {msg}", file=sys.stderr)


def _repo() -> str:
    return os.environ.get("GITHUB_REPOSITORY", "bamr87/it-journey")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _find_open_issue() -> int | None:
    p = _gh("issue", "list", "--label", LABEL, "--state", "open",
            "--json", "number", "--limit", "5")
    if p.returncode != 0:
        _warn(f"gh issue list failed: {p.stderr.strip()[:200]}")
        return None
    try:
        rows = json.loads(p.stdout or "[]")
    except json.JSONDecodeError:
        return None
    return rows[0]["number"] if rows else None


def _ensure_labels() -> None:
    # --force makes create idempotent (updates instead of erroring on existing).
    for name, color, desc in (
        (LABEL, "b60205", "Auto-managed: the quest-perfection loop cannot make progress"),
        ("automated", "ededed", "Created by an automated workflow"),
        ("needs-human", "d93f0b", "Needs a human decision or action"),
    ):
        p = _gh("label", "create", name, "--color", color, "--description", desc, "--force")
        if p.returncode != 0:
            _warn(f"gh label create {name} failed: {p.stderr.strip()[:200]}")


def _recent_same_kind_comment(number: int, kind: str, min_repeat_hours: float) -> bool:
    """True if the newest health comment already reports `kind` within the window
    (so a daily schedule updates the issue at most once per window per kind)."""
    p = _gh("issue", "view", str(number), "--json", "comments,body,createdAt")
    if p.returncode != 0:
        return False
    try:
        data = json.loads(p.stdout or "{}")
    except json.JSONDecodeError:
        return False
    newest_ts, newest_kind = None, None
    body = data.get("body") or ""
    if f"{MARKER}:{kind}" in body:
        newest_ts, newest_kind = data.get("createdAt"), kind
    for c in data.get("comments") or []:
        cbody = c.get("body") or ""
        if MARKER in cbody:
            newest_ts = c.get("createdAt")
            newest_kind = cbody.split(f"{MARKER}:", 1)[-1].split(" ", 1)[0].rstrip("->").strip(": -\n")
    if not newest_ts or newest_kind != kind:
        return False
    try:
        ts = datetime.fromisoformat(str(newest_ts).replace("Z", "+00:00"))
    except ValueError:
        return False
    return (_now() - ts).total_seconds() < min_repeat_hours * 3600


def _detail_block(detail: str) -> str:
    detail = (detail or "").strip()
    if not detail:
        return ""
    return "\n\nLast engine output:\n\n```\n" + detail[:600] + "\n```\n"


def cmd_report(args: argparse.Namespace) -> int:
    kind = KINDS[args.kind]
    stamp = _now().strftime("%Y-%m-%d %H:%M UTC")
    body_intro = (
        f"{MARKER}:{args.kind} -->\n"
        f"## {kind['headline']}\n\n"
        f"Diagnosed by the **{args.lane} lane** on {stamp} — "
        f"[run]({args.run_url}).\n\n"
        + kind["body"].format(repo=_repo())
        + _detail_block(args.detail)
    )
    if args.dry_run:
        print(f"[dry-run] would upsert issue (label {LABEL}) with:\n{body_intro}")
        return 0
    _ensure_labels()
    number = _find_open_issue()
    if number is None:
        label_flags: list[str] = []
        for lbl in (LABEL, *EXTRA_LABELS):
            label_flags += ["--label", lbl]
        p = _gh("issue", "create", "--title", TITLE,
                "--body", body_intro + FOOTER, *label_flags)
        if p.returncode != 0:
            _warn(f"could not create the health issue: {p.stderr.strip()[:300]}")
            return 0
        print(f"opened health issue: {p.stdout.strip()}")
        return 0
    if _recent_same_kind_comment(number, args.kind, args.min_repeat_hours):
        print(f"health issue #{number} already reports '{args.kind}' within "
              f"{args.min_repeat_hours}h — not commenting again.")
        return 0
    comment = (
        f"{MARKER}:{args.kind} -->\n"
        f"**{stamp} — {args.lane} lane** diagnosed **{args.kind}** again "
        f"([run]({args.run_url}))."
        + _detail_block(args.detail)
    )
    p = _gh("issue", "comment", str(number), "--body", comment)
    if p.returncode != 0:
        _warn(f"could not comment on health issue #{number}: {p.stderr.strip()[:300]}")
    else:
        print(f"updated health issue #{number} ({args.kind}).")
    return 0


def cmd_resolve(args: argparse.Namespace) -> int:
    if args.dry_run:
        print("[dry-run] would close the open health issue, if any.")
        return 0
    number = _find_open_issue()
    if number is None:
        print("no open health issue — nothing to resolve.")
        return 0
    stamp = _now().strftime("%Y-%m-%d %H:%M UTC")
    note = f" {args.note.strip()}" if args.note else ""
    p = _gh("issue", "close", str(number), "--comment",
            f"{MARKER}:recovered -->\n✅ **{stamp}** — the loop scored quests again "
            f"([run]({args.run_url})).{note} Closing.")
    if p.returncode != 0:
        _warn(f"could not close health issue #{number}: {p.stderr.strip()[:300]}")
    else:
        print(f"closed health issue #{number} (recovered).")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    rep = sub.add_parser("report", help="Upsert the single open health issue.")
    rep.add_argument("--kind", required=True, choices=sorted(KINDS))
    rep.add_argument("--lane", default="walk", choices=["walk", "fix"])
    rep.add_argument("--run-url", required=True)
    rep.add_argument("--detail", default="", help="Last engine/probe output (truncated to 600 chars).")
    rep.add_argument("--min-repeat-hours", type=float, default=12.0)
    rep.add_argument("--dry-run", action="store_true")
    rep.set_defaults(fn=cmd_report)

    res = sub.add_parser("resolve", help="Close the open health issue after a productive run.")
    res.add_argument("--run-url", required=True)
    res.add_argument("--note", default="")
    res.add_argument("--dry-run", action="store_true")
    res.set_defaults(fn=cmd_resolve)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
