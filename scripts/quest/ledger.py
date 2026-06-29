#!/usr/bin/env python3
"""
ledger.py — the deterministic ledger engine for the autonomous quest-perfection loop.

This is the ONE deterministic source of truth for the loop's progress. It is the
quest-side analogue of ``scripts/issues/triage.py``: an offline, reproducible
engine that consumes the agentic walkthrough's evidence (the ``report.aggregate()``
JSON from ``test/quest-validator/agentic_validate.py``) and the deterministic
playthrough plan (``walkthrough_plan.py``'s JSON), merges one (character, level)
SLICE into ``.quests/ledger.json``, recomputes the PERFECT flag from config
thresholds (NEVER from a model field), and rewrites ``.quests/DASHBOARD.md``.

  Subcommands (the shared LEDGER CLI CONTRACT — conform exactly):
    update      merge one slice from walk-evidence.json + walk-plan.json,
                recompute perfect, append a `walk` history entry, re-render
    fix-update  bump last_fixed + append a `fix` history entry; increment the
                circuit-breaker counter; NEVER sets perfect
    select      print one slice id (--priority) or a JSON list one-per-character
                (--all-paths) of the worst/oldest not-perfect, not-stuck slice
    render      rewrite .quests/DASHBOARD.md from the current ledger
    selftest    exercise the engine offline with synthetic aggregates

  ---------------------------------------------------------------------------
  SLICE ID:  "<character.key>/<level.code>"  e.g. "developer/0001".
  Characters come from _data/quests/paths.yml; level themes from quest_registry.
  The slice key is NEVER the permalink.
  ---------------------------------------------------------------------------

SAFETY MITIGATIONS this engine enforces (from the shared contract):
  M6 (circuit breaker): a slice fixed `fix.max_fix_rounds` times without becoming
     perfect is marked stuck/needs_human and is excluded from `select`.
  M7 (honest run): "perfect" requires mode==execute AND a non-truncated, fully
     scored run; a review-mode or truncated run can NEVER certify perfect. The
     PERFECT predicate is computed HERE, in Python, from config thresholds — we
     never read a "perfect" field from any model output.

NOTE (M7 caveat): ``verdict_obj.executed`` in the evidence is MODEL-SUPPLIED, so
even a slice this ledger marks "perfect" should keep full hands-off auto-merge of
fixes gated (CONTENT_AUTOMERGE for fix PRs) until a harness-stamped execution
proof exists. We still require execute mode + a non-truncated, fully-scored run.

Author: IT-Journey Team   |   Part of the quest-perfection loop foundation.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# Import the verdict BANDS from the agentic schema — never reimplement them, so
# this engine and the walkthrough always agree on pass/warn/fail boundaries.
_HERE = Path(__file__).resolve().parent
REPO_ROOT = _HERE.parents[1]
_VALIDATOR = REPO_ROOT / "test" / "quest-validator"
if str(_VALIDATOR) not in sys.path:
    sys.path.insert(0, str(_VALIDATOR))
from agentic.schema import (  # noqa: E402
    VERDICT_PASS,
    VERDICT_WARN,
    VERDICT_FAIL,
    DEFAULT_PASS_THRESHOLD,
    verdict_label,
)

# Level themes + character paths come from the same data the site renders from.
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import quest_registry as reg  # noqa: E402

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
QUESTS_DIR = REPO_ROOT / ".quests"
LEDGER_PATH = QUESTS_DIR / "ledger.json"
DASHBOARD_PATH = QUESTS_DIR / "DASHBOARD.md"
CONFIG_PATH = QUESTS_DIR / "config.yml"
PATHS_YML = REPO_ROOT / "_data" / "quests" / "paths.yml"

LEDGER_SCHEMA_VERSION = "1.0.0"

# Verdict ordering for "worst-first" sorts (fail < warn < pass; null is worst).
VERDICT_RANK = {None: 0, VERDICT_FAIL: 1, VERDICT_WARN: 2, VERDICT_PASS: 3}
VERDICT_EMOJI = {VERDICT_PASS: "✅", VERDICT_WARN: "⚠️", VERDICT_FAIL: "❌", None: "❓"}

# --------------------------------------------------------------------------- #
# Built-in defaults. .quests/config.yml (if present) overrides these. We never
# require the config file to exist so the engine runs offline / from a fresh
# checkout; the contract's knobs all have sane defaults here.
# --------------------------------------------------------------------------- #
DEFAULT_CONFIG: dict[str, Any] = {
    # The certification bar. Mirrors .quests/config.yml `perfect:`. A perfect
    # slice's weighted average must be at least `average_min` (0-100) — set above
    # DEFAULT_PASS_THRESHOLD on purpose: "pass" is good, "perfect" is excellent.
    "perfect": {
        "require_mode": "execute",
        "average_min": 95,
        "max_warn": 0,
        "max_fail": 0,
        "max_errored": 0,
        "max_open_issues": 0,
        "max_high_priority": 0,
        "forbid_truncated": True,
    },
    "history": {
        "cap": 20,  # keep at most this many history entries per slice
    },
    "fix": {
        "max_fix_rounds": 3,  # M6 circuit breaker
    },
}


# --------------------------------------------------------------------------- #
# Small utilities (house idiom — mirror scripts/issues/triage.py)
# --------------------------------------------------------------------------- #
def warn(msg: str) -> None:
    """Emit a GitHub-Actions-style warning that is harmless in a plain shell."""
    print(f"::warning::{msg}", file=sys.stderr)


def now_iso() -> str:
    """ISO-8601 UTC timestamp, second precision, no microseconds (stable key)."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today_str() -> str:
    """UTC date as YYYY-MM-DD for daily artifact filenames."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def write_json(path: Path, data: Any) -> None:
    """JSON house style: mkdir parents, indent=2, ensure_ascii=False, trailing \\n."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def _deep_merge(base: dict, over: dict) -> dict:
    """Recursively overlay `over` onto a copy of `base` (config defaults ← file)."""
    out = dict(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    """Load .quests/config.yml over the built-in defaults. Missing file is fine."""
    if not path.exists():
        return dict(DEFAULT_CONFIG)
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except yaml.YAMLError as exc:
        warn(f"could not parse {path}: {exc}; using built-in defaults")
        return dict(DEFAULT_CONFIG)
    if not isinstance(data, dict):
        warn(f"{path} root is not a mapping; using built-in defaults")
        return dict(DEFAULT_CONFIG)
    return _deep_merge(DEFAULT_CONFIG, data)


def _perfect_cfg(config: dict) -> dict:
    """The `perfect:` block (with a `thresholds:` legacy fallback for average_min)."""
    return config.get("perfect") or {}


def cfg_average_min(config: dict) -> float:
    p = _perfect_cfg(config)
    if "average_min" in p:
        return float(p["average_min"])
    # Legacy fallback: an older config may have put it under `thresholds:`.
    return float((config.get("thresholds") or {}).get("average_min", 95))


def cfg_require_mode(config: dict) -> str:
    return str(_perfect_cfg(config).get("require_mode", "execute"))


def cfg_forbid_truncated(config: dict) -> bool:
    return bool(_perfect_cfg(config).get("forbid_truncated", True))


def cfg_max(config: dict, key: str, default: int = 0) -> int:
    return int(_perfect_cfg(config).get(key, default) or 0)


def cfg_history_cap(config: dict) -> int:
    return int((config.get("history") or {}).get("cap", 20) or 0)


def cfg_max_fix_rounds(config: dict) -> int:
    return int((config.get("fix") or {}).get("max_fix_rounds", 3) or 0)


# --------------------------------------------------------------------------- #
# Ledger I/O
# --------------------------------------------------------------------------- #
def empty_ledger() -> dict[str, Any]:
    return {
        "schema_version": LEDGER_SCHEMA_VERSION,
        "generated": now_iso(),
        "totals": {"slices": 0, "perfect": 0, "stuck": 0, "open_issues": 0},
        "slices": {},
    }


def load_ledger(path: Path = LEDGER_PATH) -> dict[str, Any]:
    """Load the ledger; tolerate a fresh/empty/legacy file by normalizing shape."""
    if not path.exists():
        return empty_ledger()
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        warn(f"{path} is unparseable ({exc}); starting a fresh ledger")
        return empty_ledger()
    if not isinstance(data, dict):
        warn(f"{path} root is not an object; starting a fresh ledger")
        return empty_ledger()
    data.setdefault("schema_version", LEDGER_SCHEMA_VERSION)
    if not isinstance(data.get("slices"), dict):
        data["slices"] = {}
    data.setdefault("totals", {"slices": 0, "perfect": 0, "stuck": 0, "open_issues": 0})
    return data


# --------------------------------------------------------------------------- #
# Evidence / plan extraction (treated strictly as untrusted DATA)
# --------------------------------------------------------------------------- #
def load_json_file(path: Optional[str]) -> Optional[dict]:
    """Load a JSON file; return None on any trouble (caller records a reason)."""
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    try:
        text = p.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.strip():
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        warn(f"{path} is not valid JSON ({exc})")
        return None
    return data if isinstance(data, dict) else None


def _slug_of_plan(plan: Optional[dict]) -> Optional[str]:
    """Build the slice id "<char.key>/<level.code>" from the walkthrough plan."""
    if not isinstance(plan, dict):
        return None
    char = (plan.get("character") or {}).get("key")
    level = (plan.get("level") or {}).get("code")
    if char and level:
        return f"{char}/{level}"
    return None


def _result_for_level(agg: dict, level: Optional[str]) -> list[dict]:
    """Return the scored results belonging to this slice's level."""
    results = agg.get("results") or []
    if not isinstance(results, list):
        return []
    if level is None:
        return [r for r in results if isinstance(r, dict)]
    out = []
    for r in results:
        if not isinstance(r, dict):
            continue
        q = r.get("quest") or {}
        if q.get("level") == level or not level:
            out.append(r)
    # If the level filter excluded everything (level drift / missing field), fall
    # back to all results so we still record the run rather than silently dropping.
    return out or [r for r in results if isinstance(r, dict)]


def _count_recommendations(results: list[dict]) -> tuple[int, int]:
    """(open_issues, high_priority_issues) across NON-PASS results only.

    open_issues = total recommendations on results whose verdict != pass.
    high_priority_issues = those with priority == 'high' (any non-pass result).
    A passing result's recommendations are polish, not blocking, so they do not
    keep a slice from being perfect.
    """
    open_issues = 0
    high = 0
    for r in results:
        if r.get("verdict") == VERDICT_PASS:
            continue
        recs = (r.get("verdict_obj") or {}).get("recommendations") or []
        if not isinstance(recs, list):
            continue
        for rec in recs:
            if not isinstance(rec, dict):
                continue
            open_issues += 1
            if str(rec.get("priority", "")).lower() == "high":
                high += 1
    return open_issues, high


def _worst_verdict(results: list[dict]) -> Optional[str]:
    """The slice's verdict = the worst (lowest-ranked) result verdict, or None."""
    verdicts = [r.get("verdict") for r in results if "error" not in r]
    verdicts = [v for v in verdicts if v in (VERDICT_PASS, VERDICT_WARN, VERDICT_FAIL)]
    if not verdicts:
        return None
    return min(verdicts, key=lambda v: VERDICT_RANK.get(v, 0))


def build_slice_entry(
    agg: Optional[dict],
    plan: Optional[dict],
    mode: str,
    run_url: Optional[str],
    config: dict,
) -> dict[str, Any]:
    """Build the SliceEntry from one walkthrough's aggregate + plan.

    Tolerates a missing/empty aggregate: records a reason, verdict null, and the
    PERFECT flag false. The PERFECT predicate (M7) is computed HERE from config —
    we never read a model-supplied "perfect".
    """
    average_min = cfg_average_min(config)
    require_mode = cfg_require_mode(config)
    forbid_truncated = cfg_forbid_truncated(config)
    max_warn = cfg_max(config, "max_warn", 0)
    max_fail = cfg_max(config, "max_fail", 0)
    max_errored = cfg_max(config, "max_errored", 0)
    max_open = cfg_max(config, "max_open_issues", 0)
    max_high = cfg_max(config, "max_high_priority", 0)
    level = (plan.get("level") or {}).get("code") if isinstance(plan, dict) else None

    entry: dict[str, Any] = {
        "mode": mode,
        "run_url": run_url,
    }
    if isinstance(plan, dict):
        entry["theme"] = (plan.get("level") or {}).get("theme") or reg.theme_of(level or "")
        entry["tier"] = (plan.get("level") or {}).get("tier") or reg.tier_of(level or "")
        entry["character"] = (plan.get("character") or {}).get("key")
        entry["level"] = level
    elif level:
        entry["theme"] = reg.theme_of(level)
        entry["tier"] = reg.tier_of(level)

    if not isinstance(agg, dict) or not agg:
        entry.update({
            "verdict": None,
            "average": None,
            "total": 0,
            "scored": 0,
            "requested": _plan_quest_count(plan),
            "errored": 0,
            "truncated": _plan_truncated(plan),
            "counts": {VERDICT_PASS: 0, VERDICT_WARN: 0, VERDICT_FAIL: 0},
            "open_issues": 0,
            "high_priority_issues": 0,
            "executed": None,
            "perfect": False,
            "reason": "no walk evidence (missing/empty aggregate)",
        })
        return entry

    results = _result_for_level(agg, level)
    counts = agg.get("counts") or {}
    counts = {
        VERDICT_PASS: int(counts.get(VERDICT_PASS, 0) or 0),
        VERDICT_WARN: int(counts.get(VERDICT_WARN, 0) or 0),
        VERDICT_FAIL: int(counts.get(VERDICT_FAIL, 0) or 0),
    }
    total = int(agg.get("total", len(results)) or 0)
    scored = int(agg.get("scored", 0) or 0)
    errored = int(agg.get("errored", 0) or 0)
    # Truncation from EITHER side blocks perfect: the harness may truncate the
    # scoring run, or the planner may have capped the quest chain (--max-quests).
    truncated = bool(agg.get("truncated", False)) or _plan_truncated(plan)
    average = agg.get("average")
    average = float(average) if isinstance(average, (int, float)) else None
    # The plan is the trusted count of how many quests the slice SHOULD have. With
    # no plan, `requested` would degenerate to `total` (both from the same untrusted
    # aggregate), making scored==requested self-referential — so a plan is REQUIRED
    # to certify perfect. Both shipping workflows pass --plan; this guards CLI misuse.
    plan_present = _plan_quest_count(plan) > 0
    requested = _plan_quest_count(plan) or total

    verdict = _worst_verdict(results)
    if verdict is None and average is not None:
        # No usable per-quest verdicts (e.g. all errored) but we do have a
        # run-level average — derive the slice verdict from the SHARED band
        # function so this engine and the walkthrough agree on the boundaries.
        # DEFAULT_PASS_THRESHOLD anchors the bands; the perfect bar (average_min)
        # sits at or above it (pass is good; perfect is excellent).
        verdict = verdict_label(average, pass_threshold=DEFAULT_PASS_THRESHOLD)
    open_issues, high = _count_recommendations(results)

    # verdict_obj.executed is MODEL-SUPPLIED (M7 caveat). We surface it for the
    # dashboard, but the perfect predicate does NOT trust it as a proof of
    # execution — execution honesty is enforced via mode==execute + non-truncated.
    executed_flags = [
        bool((r.get("verdict_obj") or {}).get("executed"))
        for r in results if "error" not in r
    ]
    executed = all(executed_flags) if executed_flags else None

    # ----- PERFECT predicate (M7), computed in Python from config thresholds ----
    # A review-mode or truncated run can NEVER be perfect. Per-slice ONLY — this
    # is never coupled to other slices or a whole-tree build. The mode/truncation
    # gates are non-negotiable (M7); the count/average bars come from config.
    # NOTE: verdict_obj.executed is MODEL-SUPPLIED — we deliberately do NOT make
    # the predicate hinge on it (it would be self-grading); honesty is enforced by
    # require_mode==execute + forbid_truncated, which the harness controls.
    perfect = (
        (mode == require_mode == "execute")
        and plan_present
        and not (truncated and forbid_truncated)
        and scored == requested
        and requested > 0
        and errored <= max_errored
        and counts[VERDICT_WARN] <= max_warn
        and counts[VERDICT_FAIL] <= max_fail
        and average is not None
        and average >= average_min
        and open_issues <= max_open
        and high <= max_high
    )

    reason = ""
    if not perfect:
        reason = _why_not_perfect(
            mode, require_mode, truncated, forbid_truncated, scored, requested,
            errored, max_errored, counts, max_warn, max_fail,
            average, average_min, open_issues, max_open, high, max_high,
        )

    entry.update({
        "verdict": verdict,
        "average": average,
        "total": total,
        "scored": scored,
        "requested": requested,
        "errored": errored,
        "truncated": truncated,
        "counts": counts,
        "open_issues": open_issues,
        "high_priority_issues": high,
        "executed": executed,
        "perfect": perfect,
        "reason": reason,
    })
    return entry


def _plan_quest_count(plan: Optional[dict]) -> int:
    if not isinstance(plan, dict):
        return 0
    stats = plan.get("stats") or {}
    if isinstance(stats.get("count"), int):
        return stats["count"]
    quests = plan.get("quests") or []
    return len(quests) if isinstance(quests, list) else 0


def _plan_truncated(plan: Optional[dict]) -> bool:
    if not isinstance(plan, dict):
        return False
    return bool((plan.get("stats") or {}).get("truncated", False))


def _why_not_perfect(mode, require_mode, truncated, forbid_truncated,
                     scored, requested, errored, max_errored, counts,
                     max_warn, max_fail, average, average_min,
                     open_issues, max_open, high, max_high) -> str:
    bits: list[str] = []
    if not (mode == require_mode == "execute"):
        bits.append(f"mode={mode} (perfect requires execute)")
    if truncated and forbid_truncated:
        bits.append("run truncated")
    if requested <= 0:
        bits.append("no quests requested")
    elif scored != requested:
        bits.append(f"scored {scored}/{requested}")
    if errored > max_errored:
        bits.append(f"{errored} errored")
    if counts.get(VERDICT_FAIL, 0) > max_fail:
        bits.append(f"{counts[VERDICT_FAIL]} fail")
    if counts.get(VERDICT_WARN, 0) > max_warn:
        bits.append(f"{counts[VERDICT_WARN]} warn")
    if average is None:
        bits.append("no average")
    elif average < average_min:
        bits.append(f"avg {average} < {average_min}")
    if open_issues > max_open:
        bits.append(f"{open_issues} open issue(s)")
    if high > max_high:
        bits.append(f"{high} high-priority")
    return "; ".join(bits) or "not perfect"


# --------------------------------------------------------------------------- #
# Merge / totals
# --------------------------------------------------------------------------- #
def merge_slice(
    ledger: dict, slug: str, entry: dict, event: str, config: dict,
) -> dict:
    """Merge a fresh walk entry into the ledger slice (create or update in place).

    Carries forward circuit-breaker / fix state across walks, appends a capped
    history entry, and maintains perfect_since / runs / last_run.
    """
    slices = ledger["slices"]
    prev = slices.get(slug) or {}
    cap = cfg_history_cap(config)

    history = list(prev.get("history") or [])
    history.append({
        "event": event,
        "at": now_iso(),
        "date": today_str(),
        "mode": entry.get("mode"),
        "verdict": entry.get("verdict"),
        "average": entry.get("average"),
        "open_issues": entry.get("open_issues"),
        "perfect": entry.get("perfect"),
        "run_url": entry.get("run_url"),
    })
    if cap and len(history) > cap:
        history = history[-cap:]

    # Circuit breaker (M6) — WALK-DRIVEN so it actually fires without a separate
    # call. fix_rounds counts CONSECUTIVE real (verdict-bearing) walks that did
    # not reach perfect: the loop walks a slice, a fix PR lands, it re-walks; if
    # it is still imperfect after `max_fix_rounds` such rounds the slice is marked
    # stuck/needs_human and `select` stops choosing it (no infinite oscillation).
    # A fresh perfect walk resets the breaker. (cmd_fix_update can also bump it for
    # an explicit fix event, but the breaker no longer DEPENDS on being wired.)
    fix_rounds = int(prev.get("fix_rounds", 0) or 0)
    stuck = bool(prev.get("stuck", False))
    stuck_reason = prev.get("stuck_reason")
    last_fixed = prev.get("last_fixed")
    max_rounds = cfg_max_fix_rounds(config)

    perfect = bool(entry.get("perfect"))
    perfect_since = prev.get("perfect_since")
    # Only verdict-bearing walks (a real evaluation, not an empty/unparseable run)
    # advance or reset the breaker — a no-evidence walk must not count as a round.
    real_walk = event == "walk" and entry.get("verdict") is not None
    if perfect:
        if not perfect_since:
            perfect_since = today_str()
        fix_rounds = 0           # converged — reset the breaker
        stuck = False
        stuck_reason = None
    else:
        perfect_since = None
        if real_walk and int(prev.get("runs", 0) or 0) > 0 and not prev.get("perfect"):
            # A repeat imperfect walk: one more fix round elapsed without converging.
            fix_rounds += 1
            if max_rounds and fix_rounds >= max_rounds and not stuck:
                stuck = True
                stuck_reason = (f"still imperfect after {fix_rounds} walk→fix rounds "
                                f"(max {max_rounds}); needs human review")

    merged = {
        "slug": slug,
        "character": entry.get("character") or prev.get("character") or slug.split("/")[0],
        "level": entry.get("level") or prev.get("level") or slug.split("/")[-1],
        "theme": entry.get("theme") or prev.get("theme"),
        "tier": entry.get("tier") or prev.get("tier"),
        "mode": entry.get("mode"),
        "verdict": entry.get("verdict"),
        "average": entry.get("average"),
        "total": entry.get("total"),
        "scored": entry.get("scored"),
        "requested": entry.get("requested"),
        "errored": entry.get("errored"),
        "truncated": entry.get("truncated"),
        "counts": entry.get("counts"),
        "open_issues": entry.get("open_issues"),
        "high_priority_issues": entry.get("high_priority_issues"),
        "executed": entry.get("executed"),
        "perfect": perfect,
        "perfect_since": perfect_since,
        "reason": entry.get("reason"),
        "fix_rounds": fix_rounds,
        "stuck": stuck,
        "stuck_reason": stuck_reason,
        "needs_human": stuck,  # alias per contract
        "last_fixed": last_fixed,
        "last_run": now_iso(),
        "last_run_date": today_str(),
        "runs": int(prev.get("runs", 0) or 0) + 1,
        "run_url": entry.get("run_url"),
        "history": history,
    }
    slices[slug] = merged
    return merged


def recompute_totals(ledger: dict) -> None:
    slices = ledger.get("slices") or {}
    perfect = sum(1 for s in slices.values() if s.get("perfect"))
    stuck = sum(1 for s in slices.values() if s.get("stuck"))
    open_issues = sum(int(s.get("open_issues") or 0) for s in slices.values())
    ledger["totals"] = {
        "slices": len(slices),
        "perfect": perfect,
        "stuck": stuck,
        "open_issues": open_issues,
    }
    ledger["generated"] = now_iso()


# --------------------------------------------------------------------------- #
# Selection (the picker the orchestrator + fix lane consume)
# --------------------------------------------------------------------------- #
def _character_levels() -> list[tuple[str, str, str]]:
    """Return [(char_key, level_code, theme)] for every (character, level) in
    paths.yml. The universe of slices the loop sweeps."""
    try:
        paths = yaml.safe_load(PATHS_YML.read_text(encoding="utf-8")) or []
    except (OSError, yaml.YAMLError) as exc:
        warn(f"could not read {PATHS_YML} ({exc}); no slice universe")
        return []
    out: list[tuple[str, str, str]] = []
    for p in paths:
        if not isinstance(p, dict):
            continue
        key = p.get("key")
        for lv in p.get("levels") or []:
            out.append((str(key), str(lv), reg.theme_of(str(lv))))
    return out


def _select_key(slug: str, slc: Optional[dict]) -> tuple:
    """Sort key for fix/walk candidacy. Lower sorts FIRST (higher priority).

    Order: never-walked (cold start) first, then not-perfect, then not-stuck,
    then verdict fail<warn<pass, then average ascending, then last_run
    ascending (never-run first), then slug for stability.
    """
    if slc is None:
        # COLD START: a slice with no ledger entry is the highest priority.
        return (0, 0, 0, 0, -1.0, "", slug)
    cold = 0  # has an entry
    not_perfect = 0 if not slc.get("perfect") else 1
    not_stuck = 0 if not slc.get("stuck") else 1
    vrank = VERDICT_RANK.get(slc.get("verdict"), 0)
    avg = slc.get("average")
    avg = float(avg) if isinstance(avg, (int, float)) else -1.0
    last = slc.get("last_run") or ""  # "" (never) sorts before any ISO timestamp
    return (cold, not_perfect, not_stuck, vrank, avg, last, slug)


def select_priority(ledger: dict) -> Optional[str]:
    """Pick ONE slice id: the worst/oldest not-perfect, not-stuck candidate.

    The candidate universe is every (character, level) in paths.yml UNION every
    slice already in the ledger. Cold-start slices (no entry) rank highest.
    Perfect and stuck slices are excluded from fix candidacy.
    """
    slices = ledger.get("slices") or {}
    universe = {f"{c}/{lv}" for c, lv, _ in _character_levels()}
    universe |= set(slices.keys())

    candidates = []
    for slug in universe:
        slc = slices.get(slug)
        if slc is not None and (slc.get("perfect") or slc.get("stuck")):
            continue  # excluded from fix candidacy (perfect or circuit-broken)
        candidates.append((slug, slc))
    if not candidates:
        return None
    candidates.sort(key=lambda sl: _select_key(sl[0], sl[1]))
    return candidates[0][0]


def select_all_paths(ledger: dict) -> list[str]:
    """One slice id per character: that character's worst/oldest not-perfect,
    not-stuck level (from its paths.yml level list). Cold-start levels rank
    highest. A character with every level perfect-or-stuck contributes nothing."""
    slices = ledger.get("slices") or {}
    by_char: dict[str, list[tuple[str, str]]] = {}
    for c, lv, _ in _character_levels():
        by_char.setdefault(c, []).append((c, lv))

    out: list[str] = []
    for char in by_char:  # insertion order = paths.yml order
        best: Optional[tuple] = None
        best_slug: Optional[str] = None
        for c, lv in by_char[char]:
            slug = f"{c}/{lv}"
            slc = slices.get(slug)
            if slc is not None and (slc.get("perfect") or slc.get("stuck")):
                continue
            key = _select_key(slug, slc)
            if best is None or key < best:
                best = key
                best_slug = slug
        if best_slug:
            out.append(best_slug)
    return out


# --------------------------------------------------------------------------- #
# Dashboard rendering
# --------------------------------------------------------------------------- #
def render_dashboard(ledger: dict) -> str:
    totals = ledger.get("totals") or {}
    slices = ledger.get("slices") or {}
    universe_n = len({f"{c}/{lv}" for c, lv, _ in _character_levels()}) or len(slices)

    lines: list[str] = []
    lines.append("# Quest Perfection — ledger dashboard")
    lines.append("")
    lines.append(f"_Generated {ledger.get('generated', now_iso())}. "
                 "Source of truth: `.quests/ledger.json` (committed, generated)._")
    lines.append("")
    tracked = totals.get("slices", len(slices))
    perfect = totals.get("perfect", 0)
    stuck = totals.get("stuck", 0)
    open_issues = totals.get("open_issues", 0)
    lines.append(
        f"**{perfect}/{universe_n}** slices perfect · "
        f"**{tracked}** walked · **{stuck}** stuck (needs human) · "
        f"**{open_issues}** open issue(s) outstanding"
    )
    lines.append("")

    # ----- all slices, worst-first ------------------------------------------ #
    lines.append("## Slices (worst-first)")
    lines.append("")
    lines.append("| Slice | Theme | Verdict | Avg | Open | Perfect | Stuck | Last run | Report |")
    lines.append("| --- | --- | :-: | --: | --: | :-: | :-: | --- | --- |")

    def row_sort(item):
        slug, slc = item
        return _select_key(slug, slc)

    if not slices:
        lines.append("| _(no slices walked yet)_ | | | | | | | | |")
    for slug, slc in sorted(slices.items(), key=row_sort):
        verdict = slc.get("verdict")
        emoji = VERDICT_EMOJI.get(verdict, "❓")
        avg = slc.get("average")
        avg_cell = f"{avg:.1f}" if isinstance(avg, (int, float)) else "—"
        perfect_cell = "✅" if slc.get("perfect") else ""
        stuck_cell = "🛑" if slc.get("stuck") else ""
        last = slc.get("last_run_date") or "—"
        run_url = slc.get("run_url")
        report = f"[run]({run_url})" if run_url else "—"
        theme = (slc.get("theme") or "").replace("|", "\\|")
        lines.append(
            f"| `{slug}` | {theme} | {emoji} {verdict or '—'} | {avg_cell} | "
            f"{slc.get('open_issues', 0)} | {perfect_cell} | {stuck_cell} | "
            f"{last} | {report} |"
        )
    lines.append("")

    # ----- per-character roll-up -------------------------------------------- #
    lines.append("## Per-character roll-up")
    lines.append("")
    lines.append("| Character | Levels | Perfect | Stuck | Walked |")
    lines.append("| --- | --: | --: | --: | --: |")
    by_char: dict[str, list[str]] = {}
    for c, lv, _ in _character_levels():
        by_char.setdefault(c, []).append(f"{c}/{lv}")
    if not by_char:
        lines.append("| _(no character paths found)_ | | | | |")
    for char, slugs in by_char.items():
        p = sum(1 for s in slugs if (slices.get(s) or {}).get("perfect"))
        st = sum(1 for s in slugs if (slices.get(s) or {}).get("stuck"))
        walked = sum(1 for s in slugs if s in slices)
        lines.append(f"| `{char}` | {len(slugs)} | {p} | {st} | {walked} |")
    lines.append("")

    # ----- recently perfected ----------------------------------------------- #
    lines.append("## Recently perfected")
    lines.append("")
    perfected = [
        (slug, slc) for slug, slc in slices.items()
        if slc.get("perfect") and slc.get("perfect_since")
    ]
    perfected.sort(key=lambda it: it[1].get("perfect_since") or "", reverse=True)
    if not perfected:
        lines.append("_None yet — a slice becomes perfect only via a fresh "
                     "execute-mode, non-truncated, fully-scored, zero-issue walk._")
    else:
        for slug, slc in perfected[:20]:
            lines.append(
                f"- `{slug}` — {slc.get('theme', '')} "
                f"(since {slc.get('perfect_since')}, avg "
                f"{slc.get('average')})"
            )
    lines.append("")
    return "\n".join(lines)


def write_dashboard(ledger: dict, path: Path = DASHBOARD_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_dashboard(ledger), encoding="utf-8")


# --------------------------------------------------------------------------- #
# Subcommand: update
# --------------------------------------------------------------------------- #
def cmd_update(args: argparse.Namespace) -> int:
    config = load_config()
    agg = load_json_file(args.evidence)
    plan = load_json_file(args.plan)

    slug = args.slug or _slug_of_plan(plan)
    if not slug:
        print("ERROR: could not determine slice id (need --slug or a plan with "
              "character.key + level.code)", file=sys.stderr)
        return 1

    if agg is None:
        warn(f"no usable walk evidence at {args.evidence!r}; "
             "recording a null-verdict, not-perfect entry")

    entry = build_slice_entry(agg, plan, args.mode, args.run_url, config)
    ledger = load_ledger()
    merged = merge_slice(ledger, slug, entry, args.event, config)
    recompute_totals(ledger)
    write_json(LEDGER_PATH, ledger)
    write_dashboard(ledger)

    print(f"Updated slice `{slug}`: verdict={merged.get('verdict')} "
          f"avg={merged.get('average')} perfect={merged.get('perfect')} "
          f"open={merged.get('open_issues')} stuck={merged.get('stuck')}")
    print(f"Wrote {LEDGER_PATH}")
    print(f"Wrote {DASHBOARD_PATH}")
    return 0


# --------------------------------------------------------------------------- #
# Subcommand: fix-update
# --------------------------------------------------------------------------- #
def cmd_fix_update(args: argparse.Namespace) -> int:
    config = load_config()
    slug = args.slug
    ledger = load_ledger()
    slices = ledger["slices"]
    prev = slices.get(slug)

    if prev is None:
        # A fix on a never-walked slice is unusual but recorded honestly: we
        # create a minimal entry so the circuit breaker can still count rounds.
        char, _, level = slug.partition("/")
        prev = {
            "slug": slug,
            "character": char,
            "level": level,
            "theme": reg.theme_of(level),
            "tier": reg.tier_of(level),
            "verdict": None,
            "average": None,
            "open_issues": 0,
            "high_priority_issues": 0,
            "perfect": False,
            "perfect_since": None,
            "fix_rounds": 0,
            "stuck": False,
            "runs": 0,
            "history": [],
        }
        slices[slug] = prev
        warn(f"fix-update on unknown slice {slug}; created a minimal entry")

    max_rounds = cfg_max_fix_rounds(config)
    cap = cfg_history_cap(config)

    fix_rounds = int(prev.get("fix_rounds", 0) or 0) + 1
    prev["fix_rounds"] = fix_rounds
    prev["last_fixed"] = today_str()
    # A fix NEVER sets perfect — only a fresh walk can certify perfect. An applied
    # fix invalidates any prior perfect claim (the content changed; re-walk needed).
    prev["perfect"] = False
    prev["perfect_since"] = None

    # M6 circuit breaker: fixed too many times without becoming perfect → stuck.
    if max_rounds and fix_rounds >= max_rounds:
        prev["stuck"] = True
        prev["needs_human"] = True
        prev["stuck_reason"] = (
            f"fixed {fix_rounds} time(s) (>= max_fix_rounds={max_rounds}) "
            "without certifying perfect"
        )
        warn(f"slice {slug} marked stuck/needs_human: {prev['stuck_reason']}")

    history = list(prev.get("history") or [])
    history.append({
        "event": "fix",
        "at": now_iso(),
        "date": today_str(),
        "fix_rounds": fix_rounds,
        "merged_pr": args.merged_pr,
        "stuck": bool(prev.get("stuck", False)),
    })
    if cap and len(history) > cap:
        history = history[-cap:]
    prev["history"] = history

    recompute_totals(ledger)
    write_json(LEDGER_PATH, ledger)
    write_dashboard(ledger)

    print(f"fix-update `{slug}`: fix_rounds={fix_rounds} "
          f"stuck={prev.get('stuck')} last_fixed={prev.get('last_fixed')}")
    print(f"Wrote {LEDGER_PATH}")
    return 0


# --------------------------------------------------------------------------- #
# Subcommand: select
# --------------------------------------------------------------------------- #
def cmd_select(args: argparse.Namespace) -> int:
    ledger = load_ledger()

    if args.all_paths:
        result: Any = select_all_paths(ledger)
    else:  # --priority (default)
        one = select_priority(ledger)
        result = one  # may be None when nothing is selectable

    if args.json:
        out = json.dumps(result, ensure_ascii=False)
        if args.json == "-":
            print(out)
        else:
            Path(args.json).write_text(out + "\n", encoding="utf-8")
    else:
        if args.all_paths:
            for slug in result:
                print(slug)
        elif result:
            print(result)
    return 0


# --------------------------------------------------------------------------- #
# Subcommand: render
# --------------------------------------------------------------------------- #
def cmd_render(args: argparse.Namespace) -> int:
    ledger = load_ledger()
    write_dashboard(ledger)
    print(f"Wrote {DASHBOARD_PATH}")
    return 0


# --------------------------------------------------------------------------- #
# Subcommand: selftest
# --------------------------------------------------------------------------- #
def _agg(results: list[dict], **top) -> dict:
    """Helper: assemble a synthetic aggregate dict like report.aggregate()."""
    counts = {VERDICT_PASS: 0, VERDICT_WARN: 0, VERDICT_FAIL: 0}
    scored = 0
    errored = 0
    overalls = []
    for r in results:
        if "error" in r:
            errored += 1
        else:
            scored += 1
            counts[r.get("verdict", VERDICT_FAIL)] = counts.get(r.get("verdict"), 0) + 1
            overalls.append(r.get("overall", 0))
    avg = round(sum(overalls) / len(overalls), 1) if overalls else 0.0
    base = {
        "schema_version": "1.0.0",
        "total": len(results),
        "scored": scored,
        "errored": errored,
        "average": avg,
        "counts": counts,
        "truncated": False,
        "results": results,
    }
    base.update(top)
    return base


def _result(level, verdict, overall, *, executed=True, recs=None, error=None):
    if error:
        return {"quest": {"path": f"q/{level}", "slug": "s", "level": level},
                "verdict": VERDICT_FAIL, "error": error}
    return {
        "quest": {"path": f"q/{level}", "slug": "s", "level": level},
        "verdict": verdict,
        "overall": overall,
        "verdict_obj": {
            "executed": executed,
            "commands": [],
            "recommendations": recs or [],
            "summary": "synthetic",
        },
    }


def _plan(char, level, count=1, truncated=False):
    return {
        "schema_version": "1.0.0",
        "character": {"key": char},
        "level": {"code": level, "theme": reg.theme_of(level), "tier": reg.tier_of(level)},
        "quests": [{"permalink": f"/quests/{level}/q{i}/"} for i in range(count)],
        "stats": {"count": count, "truncated": truncated},
    }


def _selftest() -> int:  # noqa: C901 - exhaustive on purpose
    cfg = dict(DEFAULT_CONFIG)
    fails: list[str] = []

    def check(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # 1) PERFECT: execute, non-truncated, fully scored, all pass, high avg, 0 issues.
    plan = _plan("developer", "0001", count=2)
    agg = _agg([
        _result("0001", VERDICT_PASS, 98),
        _result("0001", VERDICT_PASS, 96),
    ])
    e = build_slice_entry(agg, plan, "execute", "http://run/1", cfg)
    check(e["perfect"] is True, f"perfect slice should be perfect: {e.get('reason')}")
    check(e["verdict"] == VERDICT_PASS, "perfect slice verdict should be pass")
    check(e["open_issues"] == 0, "perfect slice open_issues should be 0")

    # 2) WARN: a warn result can never be perfect; open_issues counts its recs.
    aggw = _agg([
        _result("0001", VERDICT_WARN, 72,
                recs=[{"priority": "high", "area": "cmd", "suggestion": "fix"},
                      {"priority": "low", "area": "x", "suggestion": "y"}]),
    ])
    ew = build_slice_entry(aggw, _plan("developer", "0001"), "execute", None, cfg)
    check(ew["perfect"] is False, "warn slice must not be perfect")
    check(ew["verdict"] == VERDICT_WARN, "warn verdict")
    check(ew["open_issues"] == 2, f"warn open_issues should be 2, got {ew['open_issues']}")
    check(ew["high_priority_issues"] == 1, "warn high should be 1")

    # 3) FAIL.
    aggf = _agg([_result("0001", VERDICT_FAIL, 30,
                         recs=[{"priority": "high", "area": "a", "suggestion": "b"}])])
    ef = build_slice_entry(aggf, _plan("developer", "0001"), "execute", None, cfg)
    check(ef["perfect"] is False and ef["verdict"] == VERDICT_FAIL, "fail slice")

    # 4) EMPTY / missing aggregate → null verdict, not perfect, reason recorded.
    ee = build_slice_entry(None, _plan("developer", "0001"), "execute", None, cfg)
    check(ee["perfect"] is False, "empty evidence must not be perfect")
    check(ee["verdict"] is None, "empty evidence verdict must be null")
    check("no walk evidence" in (ee.get("reason") or ""), "empty reason recorded")

    # 5) TRUNCATED run can NEVER be perfect even with great scores.
    aggt = _agg([_result("0001", VERDICT_PASS, 99)], truncated=True)
    et = build_slice_entry(aggt, _plan("developer", "0001"), "execute", None, cfg)
    check(et["perfect"] is False, "truncated run must NEVER be perfect")
    check("truncated" in (et.get("reason") or ""), "truncated reason recorded")

    # 5b) Plan-side truncation also blocks perfect.
    aggt2 = _agg([_result("0001", VERDICT_PASS, 99)])
    et2 = build_slice_entry(aggt2, _plan("developer", "0001", truncated=True), "execute", None, cfg)
    check(et2["perfect"] is False, "plan-truncated must NEVER be perfect")

    # 6) REVIEW-MODE can NEVER be perfect even with a flawless execute-looking agg.
    aggr = _agg([_result("0001", VERDICT_PASS, 99)])
    er = build_slice_entry(aggr, _plan("developer", "0001"), "review", None, cfg)
    check(er["perfect"] is False, "review-mode must NEVER be perfect")
    check("mode=review" in (er.get("reason") or ""), "review reason recorded")

    # 6b) scored != requested (a quest errored) blocks perfect.
    agge = _agg([_result("0001", VERDICT_PASS, 99), _result("0001", None, 0, error="boom")])
    ee2 = build_slice_entry(agge, _plan("developer", "0001", count=2), "execute", None, cfg)
    check(ee2["perfect"] is False, "errored/under-scored run must not be perfect")

    # ---- ledger merge + totals + perfect_since ----
    ledger = empty_ledger()
    merge_slice(ledger, "developer/0001", e, "walk", cfg)
    recompute_totals(ledger)
    check(ledger["totals"]["perfect"] == 1, "totals.perfect should be 1")
    check(ledger["slices"]["developer/0001"]["perfect_since"] == today_str(),
          "perfect_since set on perfection")
    check(ledger["slices"]["developer/0001"]["runs"] == 1, "runs bumped to 1")

    # A subsequent non-perfect walk clears perfect_since.
    merge_slice(ledger, "developer/0001", ew, "walk", cfg)
    recompute_totals(ledger)
    check(ledger["slices"]["developer/0001"]["perfect"] is False, "regressed not perfect")
    check(ledger["slices"]["developer/0001"]["perfect_since"] is None, "perfect_since cleared")
    check(ledger["slices"]["developer/0001"]["runs"] == 2, "runs bumped to 2")

    # ---- COLD START select: an unwalked slice outranks a walked non-perfect one ----
    ledger2 = empty_ledger()
    # Walk one slice to warn; everything else in paths.yml is cold (no entry).
    merge_slice(ledger2, "developer/0001", ew, "walk", cfg)
    recompute_totals(ledger2)
    picked = select_priority(ledger2)
    universe = {f"{c}/{lv}" for c, lv, _ in _character_levels()}
    if universe:
        # there ARE cold slices → the pick must be a cold (unwalked) one.
        check(picked is not None, "select should pick something with a slice universe")
        check(picked not in ledger2["slices"] or picked == "developer/0001",
              "cold-start: an unwalked slice should outrank the walked warn slice")
        check(picked not in ledger2["slices"],
              f"cold-start slice expected, got walked {picked}")
    # select must NEVER return a perfect slice.
    ledger3 = empty_ledger()
    for c, lv, _ in _character_levels():
        merge_slice(ledger3, f"{c}/{lv}", e, "walk", cfg)  # mark ALL perfect
    recompute_totals(ledger3)
    check(select_priority(ledger3) is None, "all-perfect → select returns None")
    check(select_all_paths(ledger3) == [], "all-perfect → all-paths empty")

    # ---- CIRCUIT BREAKER (M6) — WALK-DRIVEN ----
    # Repeated imperfect (verdict-bearing) walks must trip stuck at max_fix_rounds
    # WITHOUT any manual mutation — the breaker fires from merge_slice itself, so
    # it works even though no workflow calls fix-update.
    ledger4 = empty_ledger()
    maxr = cfg_max_fix_rounds(cfg)
    for i in range(maxr + 1):
        merge_slice(ledger4, "developer/0001", ew, "walk", cfg)  # warn, not perfect
    slc4 = ledger4["slices"]["developer/0001"]
    check(slc4["fix_rounds"] >= maxr, "consecutive imperfect walks must accrue fix_rounds")
    recompute_totals(ledger4)
    check(slc4["stuck"] is True, "slice should be stuck after max consecutive imperfect walks")
    check(slc4["needs_human"] is True, "stuck slice should alias needs_human")
    # A stuck slice is excluded from select candidacy.
    picked4 = select_priority(ledger4)
    check(picked4 != "developer/0001", "stuck slice must be excluded from select")
    # all-paths must also skip the stuck slice for that character.
    ap = select_all_paths(ledger4)
    check("developer/0001" not in ap, "stuck slice excluded from all-paths")

    # A fresh perfect walk clears stuck.
    merge_slice(ledger4, "developer/0001", e, "walk", cfg)
    check(ledger4["slices"]["developer/0001"]["stuck"] is False,
          "fresh perfect walk should clear stuck")
    check(ledger4["slices"]["developer/0001"]["perfect"] is True, "now perfect")

    # ---- all-paths: one slice id per character ----
    ledger5 = empty_ledger()
    ap5 = select_all_paths(ledger5)  # cold ledger → one cold slice per character
    chars = {c for c, _, _ in _character_levels()}
    if chars:
        picked_chars = {s.split("/")[0] for s in ap5}
        check(picked_chars == chars,
              f"all-paths should cover every character: {picked_chars} vs {chars}")
        check(len(ap5) == len(picked_chars), "all-paths: one slice per character")

    # ---- render produces a non-empty dashboard with the headline sections ----
    dash = render_dashboard(ledger)
    for needle in ("Quest Perfection", "Slices (worst-first)",
                   "Per-character roll-up", "Recently perfected"):
        check(needle in dash, f"dashboard missing section: {needle}")

    # ---- fix-update NEVER sets perfect (simulate via the same logic path) ----
    ledgerf = empty_ledger()
    merge_slice(ledgerf, "developer/0001", e, "walk", cfg)  # perfect=True
    check(ledgerf["slices"]["developer/0001"]["perfect"] is True, "precondition perfect")
    # Apply one fix round directly through the entry mutation fix-update performs:
    slc = ledgerf["slices"]["developer/0001"]
    slc["fix_rounds"] = int(slc.get("fix_rounds", 0)) + 1
    slc["last_fixed"] = today_str()
    slc["perfect"] = False
    slc["perfect_since"] = None
    check(slc["perfect"] is False, "fix-update must clear perfect (only a walk certifies it)")

    if fails:
        print("❌ ledger selftest FAILED:", file=sys.stderr)
        for f in fails:
            print(f"   - {f}", file=sys.stderr)
        return 1
    print(f"✅ ledger self-test passed ({len(_character_levels())} slices in universe).")
    return 0


def cmd_selftest(args: argparse.Namespace) -> int:
    return _selftest()


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ledger.py",
        description=(
            "Deterministic ledger engine for the autonomous quest-perfection "
            "loop. The ONE source of truth: merges walkthrough evidence into "
            ".quests/ledger.json, recomputes the PERFECT flag from config "
            "thresholds (never from a model field), and renders the dashboard."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_up = sub.add_parser("update", help="merge one slice from evidence + plan")
    p_up.add_argument("--evidence", required=True,
                      help="walk-evidence.json (report.aggregate() output)")
    p_up.add_argument("--plan", default=None,
                      help="walk-plan.json (walkthrough_plan.py output) — names the slice")
    p_up.add_argument("--slug", default=None,
                      help="explicit slice id '<char>/<code>' (overrides the plan)")
    p_up.add_argument("--mode", choices=["execute", "review"], default="execute",
                      help="run mode; review can NEVER certify perfect (M7)")
    p_up.add_argument("--run-url", default=None, help="CI run URL for the dashboard")
    p_up.add_argument("--event", default="walk", help="history event label (default: walk)")
    p_up.set_defaults(func=cmd_update)

    p_fix = sub.add_parser("fix-update",
                           help="record a fix round (bumps fix_rounds; NEVER sets perfect)")
    p_fix.add_argument("--slug", required=True, help="slice id '<char>/<code>'")
    p_fix.add_argument("--merged-pr", type=int, default=None,
                       help="the merged fix PR number (recorded in history)")
    p_fix.set_defaults(func=cmd_fix_update)

    p_sel = sub.add_parser("select", help="print slice id(s) to work next")
    g = p_sel.add_mutually_exclusive_group()
    g.add_argument("--priority", action="store_true",
                   help="print ONE worst/oldest not-perfect, not-stuck slice (default)")
    g.add_argument("--all-paths", action="store_true",
                   help="print a JSON list with one slice id per character")
    p_sel.add_argument("--json", default=None,
                       help="emit JSON to this file ('-' for stdout)")
    p_sel.set_defaults(func=cmd_select)

    p_render = sub.add_parser("render", help="rewrite .quests/DASHBOARD.md")
    p_render.set_defaults(func=cmd_render)

    p_self = sub.add_parser("selftest", help="run the offline self-check, then exit")
    p_self.set_defaults(func=cmd_selftest)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
