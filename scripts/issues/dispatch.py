#!/usr/bin/env python3
"""
dispatch.py — Issue Autopilot OODA controller / budget gate.

Decides what the autopilot should actually act on THIS run, clamped to human
review speed. It reads the plan produced by triage.py (.issues/plan.json) and the
backpressure caps (.issues/budget.yml), OBSERVES how many auto:issue PRs are
already open, ORIENTS the plan's batches into triage-only vs PR-opening, and
DECIDES how many resolution PRs may be proposed without burying the reviewer.

  Loop (OODA):
    OBSERVE  count open PRs labeled `auto:issue` (via gh).
    ORIENT   split plan batches into triage (close/decompose/needs-human; no PR)
             and resolve (resolve-content/resolve-code; opens a PR).
    DECIDE   if open auto:issue PRs >= caps.max_open_prs -> backlog_heavy: open
             nothing. Else fill remaining slots, capped by
             max_resolve_batches_per_run; the rest are deferred (with reasons).
    ACT      (elsewhere) — this script only emits the dispatch plan.

  ---------------------------------------------------------------------------
  READ / PLAN ONLY. This script NEVER mutates GitHub. It does not open, close,
  comment on, or merge anything. It only reads (gh pr list) and writes
  .issues/dispatch.json plus an optional GitHub Actions matrix line. The
  workflow/agents ACT on this output.
  ---------------------------------------------------------------------------

  FAIL-SAFE: if plan.json is missing OR older than caps.plan_max_age_minutes,
  the resolve list is empty, a ::warning:: is printed, and we exit 0.

Author: IT-Journey Team   |   Part of the Issue Autopilot foundation.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
ISSUES_DIR = REPO_ROOT / ".issues"
DEFAULT_PLAN = ISSUES_DIR / "plan.json"
BUDGET_PATH = ISSUES_DIR / "budget.yml"
CONFIG_PATH = ISSUES_DIR / "config.yml"

# Actions that open a PR (resolve lane) vs triage-only (no new PR).
RESOLVE_ACTIONS = {"resolve-content", "resolve-code"}

# The PR label the autopilot owns (fallback if config is unreadable).
DEFAULT_AUTO_ISSUE_LABEL = "auto:issue"


# --------------------------------------------------------------------------- #
# Small utilities
# --------------------------------------------------------------------------- #
def warn(msg: str) -> None:
    """Emit a GitHub-Actions-style warning that is harmless in a plain shell."""
    print(f"::warning::{msg}", file=sys.stderr)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML mapping with a clear error on parse failure."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except FileNotFoundError:
        raise
    except yaml.YAMLError as exc:
        print(f"ERROR: could not parse {path}: {exc}", file=sys.stderr)
        raise
    if not isinstance(data, dict):
        raise ValueError(f"{path} root must be a mapping, got {type(data).__name__}")
    return data


def load_plan(path: Path) -> Optional[dict[str, Any]]:
    """Load plan.json. Returns None (with a warning) if missing/unparseable."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        warn(f"plan not found at {path}; nothing to dispatch")
        return None
    except json.JSONDecodeError as exc:
        warn(f"plan at {path} is not valid JSON ({exc}); nothing to dispatch")
        return None
    if not isinstance(data, dict):
        warn(f"plan at {path} is not a JSON object; nothing to dispatch")
        return None
    return data


def auto_issue_label(config: Optional[dict[str, Any]]) -> str:
    """Resolve the auto:issue PR label from config, with a safe default."""
    if not config:
        return DEFAULT_AUTO_ISSUE_LABEL
    labels = config.get("labels") or {}
    return str(labels.get("pr") or DEFAULT_AUTO_ISSUE_LABEL)


# --------------------------------------------------------------------------- #
# OBSERVE
# --------------------------------------------------------------------------- #
def count_open_auto_prs(repo: str, label: str) -> Optional[int]:
    """
    Count currently-open PRs carrying the auto:issue label. Returns None if gh is
    unavailable/errors (caller treats None as "unknown" and stays conservative).
    """
    cmd = [
        "gh", "pr", "list",
        "--repo", repo,
        "--state", "open",
        "--label", label,
        "--json", "number",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
    except (OSError, FileNotFoundError) as exc:
        warn(f"gh unavailable counting open PRs ({exc}); treating as unknown")
        return None
    if proc.returncode != 0:
        warn(
            f"gh pr list exited {proc.returncode}: "
            f"{proc.stderr.strip() or '(no stderr)'}; treating as unknown"
        )
        return None
    try:
        prs = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError as exc:
        warn(f"could not parse gh pr list JSON ({exc}); treating as unknown")
        return None
    if not isinstance(prs, list):
        return None
    return len(prs)


# --------------------------------------------------------------------------- #
# ORIENT
# --------------------------------------------------------------------------- #
def orient_batches(
    plan: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Split plan batches into (triage_batches, resolve_batches).

    triage  = close-* / decompose / needs-human (no new PR).
    resolve = resolve-content / resolve-code (opens a PR).
    Already-deferred resolve batches stay in resolve so the dispatcher can
    re-evaluate them, but they are eligible for re-deferral below.
    """
    triage: list[dict[str, Any]] = []
    resolve: list[dict[str, Any]] = []
    for batch in plan.get("batches") or []:
        if not isinstance(batch, dict):
            continue
        if batch.get("action") in RESOLVE_ACTIONS:
            resolve.append(batch)
        else:
            triage.append(batch)
    return triage, resolve


# --------------------------------------------------------------------------- #
# DECIDE
# --------------------------------------------------------------------------- #
def plan_is_stale(plan: dict[str, Any], max_age_minutes: int) -> bool:
    """True if plan.generated is older than max_age_minutes (or unparseable)."""
    if not max_age_minutes:
        return False
    generated = plan.get("generated")
    if not generated:
        warn("plan has no `generated` timestamp; treating as stale")
        return True
    raw = str(generated)
    if raw.endswith("Z"):  # normalize a 'Z' suffix (fromisoformat pre-3.11 can't)
        raw = raw[:-1] + "+00:00"
    try:
        ts = datetime.fromisoformat(raw)
    except ValueError:
        warn(f"plan `generated` ({generated!r}) is unparseable; treating as stale")
        return True
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    age_minutes = (datetime.now(timezone.utc) - ts).total_seconds() / 60.0
    return age_minutes > max_age_minutes


def decide(
    plan: dict[str, Any],
    budget: dict[str, Any],
    open_prs: Optional[int],
) -> dict[str, Any]:
    """
    Core OODA decision. Returns the dispatch dict (without `generated`/matrix).
    Never raises on policy; degrades to an empty resolve list when in doubt.
    """
    caps = budget.get("caps") or {}
    max_open_prs = int(caps.get("max_open_prs", 5) or 0)
    max_resolve = int(caps.get("max_resolve_batches_per_run", 3) or 0)

    triage_batches, resolve_batches = orient_batches(plan)
    triage_ids = [b.get("id") for b in triage_batches]

    deferred: list[dict[str, Any]] = []

    # If we couldn't observe the PR queue, stay conservative: open nothing.
    if open_prs is None:
        warn("open auto:issue PR count unknown; opening no resolution PRs this run")
        for b in resolve_batches:
            deferred.append({
                "id": b.get("id"),
                "reason": "open-PR count unknown (gh unavailable); conservative no-op",
            })
        return {
            "open_auto_issue_prs": None,
            "triage": triage_ids,
            "resolve": [],
            "deferred": deferred,
        }

    # Backlog-heavy backpressure: at/over cap → open nothing new.
    if max_open_prs and open_prs >= max_open_prs:
        warn(
            f"backlog_heavy: {open_prs} open auto:issue PR(s) >= "
            f"max_open_prs={max_open_prs}; opening no new resolution PRs"
        )
        for b in resolve_batches:
            deferred.append({
                "id": b.get("id"),
                "reason": (
                    f"backlog_heavy: {open_prs} open auto:issue PRs "
                    f">= max_open_prs={max_open_prs}"
                ),
            })
        return {
            "open_auto_issue_prs": open_prs,
            "triage": triage_ids,
            "resolve": [],
            "deferred": deferred,
        }

    # Normal: fill remaining slots, capped by max_resolve_batches_per_run.
    # max_open_prs == 0 means "no PR-backpressure limit" (consistent with
    # max_resolve == 0 meaning "no per-run cap") rather than "open nothing".
    available_slots = (max(0, max_open_prs - open_prs) if max_open_prs
                       else len(resolve_batches))
    take = min(available_slots, max_resolve, len(resolve_batches)) if max_resolve \
        else min(available_slots, len(resolve_batches))

    resolve_selected = resolve_batches[:take]
    for idx, b in enumerate(resolve_batches[take:], start=take):
        if idx >= available_slots:
            reason = (
                f"no free slot: available_slots="
                f"{available_slots} (max_open_prs={max_open_prs} - "
                f"open={open_prs})"
            )
        else:
            reason = (
                f"exceeds max_resolve_batches_per_run={max_resolve} this run"
            )
        deferred.append({"id": b.get("id"), "reason": reason})

    if deferred:
        warn(
            f"deferred {len(deferred)} resolve batch(es) this run "
            f"(open={open_prs}, slots={available_slots}, cap={max_resolve})"
        )

    return {
        "open_auto_issue_prs": open_prs,
        "triage": triage_ids,
        "resolve": resolve_selected,
        "deferred": deferred,
    }


# --------------------------------------------------------------------------- #
# EMIT
# --------------------------------------------------------------------------- #
def build_matrix(resolve_batches: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Build a GitHub Actions matrix include-list for the selected resolve batches.
    issue_numbers is a comma-joined string so each matrix entry is a clean scalar.
    Always returns a valid object; empty selection -> {"include": []}.
    """
    include: list[dict[str, Any]] = []
    for b in resolve_batches:
        numbers = b.get("issue_numbers") or []
        include.append({
            "batch_id": b.get("id"),
            "action": b.get("action"),
            "area": b.get("area"),
            "issue_numbers": ",".join(str(n) for n in numbers),
        })
    return {"include": include}


def append_github_output(path: Path, matrix: dict[str, Any]) -> None:
    """Append `matrix=<json>` to the $GITHUB_OUTPUT-style file."""
    line = "matrix=" + json.dumps(matrix, ensure_ascii=False, separators=(",", ":"))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def write_dispatch(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


# --------------------------------------------------------------------------- #
# Main flow
# --------------------------------------------------------------------------- #
def run(args: argparse.Namespace) -> int:
    # Config (only used to resolve the auto:issue label + repo fallback).
    config: Optional[dict[str, Any]] = None
    try:
        config = load_yaml(CONFIG_PATH)
    except (FileNotFoundError, ValueError, yaml.YAMLError):
        warn(f"config unreadable at {CONFIG_PATH}; using defaults")

    # Budget caps.
    try:
        budget = load_yaml(BUDGET_PATH)
    except FileNotFoundError:
        print(f"ERROR: budget not found at {BUDGET_PATH}", file=sys.stderr)
        return 1
    except (ValueError, yaml.YAMLError):
        return 1

    caps = budget.get("caps") or {}
    max_age = int(caps.get("plan_max_age_minutes", 0) or 0)

    repo = args.repo or (config.get("repo") if config else None) or ""
    label = auto_issue_label(config)

    plan_path = Path(args.plan) if args.plan else DEFAULT_PLAN
    plan = load_plan(plan_path)

    # Always emit a valid (possibly empty) matrix so the workflow never errors.
    empty_matrix = {"include": []}

    # FAIL-SAFE: missing plan -> empty resolve, exit 0.
    if plan is None:
        dispatch = {
            "generated": now_iso(),
            "open_auto_issue_prs": None,
            "triage": [],
            "resolve": [],
            "deferred": [{"id": None, "reason": "plan.json missing/unreadable"}],
        }
        _emit(args, dispatch, empty_matrix)
        return 0

    # FAIL-SAFE: stale plan -> empty resolve, exit 0.
    if plan_is_stale(plan, max_age):
        warn(
            f"plan is older than caps.plan_max_age_minutes={max_age}; "
            f"opening no resolution PRs this run"
        )
        triage_batches, resolve_batches = orient_batches(plan)
        dispatch = {
            "generated": now_iso(),
            "open_auto_issue_prs": None,
            "triage": [b.get("id") for b in triage_batches],
            "resolve": [],
            "deferred": [
                {"id": b.get("id"), "reason": "plan stale (exceeds plan_max_age_minutes)"}
                for b in resolve_batches
            ],
        }
        _emit(args, dispatch, empty_matrix)
        return 0

    if not repo:
        warn("no repo (args/config); cannot observe PR queue — staying conservative")
        open_prs = None
    else:
        open_prs = count_open_auto_prs(repo, label)

    decision = decide(plan, budget, open_prs)
    dispatch = {"generated": now_iso(), **decision}
    matrix = build_matrix(decision["resolve"])
    _emit(args, dispatch, matrix)
    return 0


def _emit(args: argparse.Namespace, dispatch: dict[str, Any],
          matrix: dict[str, Any]) -> None:
    """Print + (unless dry-run) write dispatch.json and the matrix line."""
    n_resolve = len(dispatch.get("resolve") or [])
    n_triage = len(dispatch.get("triage") or [])
    n_deferred = len(dispatch.get("deferred") or [])
    open_prs = dispatch.get("open_auto_issue_prs")

    print("Issue Autopilot — dispatch")
    print(f"  open auto:issue PRs: {open_prs}")
    print(f"  triage batches:      {n_triage}")
    print(f"  resolve (open PRs):  {n_resolve}")
    print(f"  deferred:            {n_deferred}")
    for b in dispatch.get("resolve") or []:
        print(f"    -> {b.get('id')} ({b.get('action')}) issues={b.get('issue_numbers')}")
    for d in dispatch.get("deferred") or []:
        print(f"    ~ deferred {d.get('id')}: {d.get('reason')}")

    if args.dry_run:
        print("\n--- dispatch.json (dry-run, not written) ---")
        print(json.dumps(dispatch, indent=2, ensure_ascii=False))
        print("\n--- matrix (dry-run) ---")
        print("matrix=" + json.dumps(matrix, ensure_ascii=False, separators=(",", ":")))
        return

    out_path = ISSUES_DIR / "dispatch.json"
    write_dispatch(out_path, dispatch)
    print(f"Wrote {out_path}")

    if args.github_output:
        append_github_output(Path(args.github_output), matrix)
        print(f"Appended matrix to {args.github_output}")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dispatch.py",
        description=(
            "Issue Autopilot OODA controller / budget gate. READ + PLAN ONLY — "
            "never mutates GitHub. Decides which resolve batches may open a PR "
            "this run without burying the reviewer, and emits dispatch.json."
        ),
    )
    parser.add_argument(
        "--repo", default=None, help="owner/name (default: config.repo)"
    )
    parser.add_argument(
        "--plan", default=None,
        help="path to plan.json (default: .issues/plan.json)",
    )
    parser.add_argument(
        "--github-output", default=None,
        help="path of a $GITHUB_OUTPUT-style file to append `matrix=<json>` to",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="compute and print the decision but write nothing",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
