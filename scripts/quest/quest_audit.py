#!/usr/bin/env python3
"""
quest_audit.py — the unified IT-Journey quest validation system.

ONE command, ONE consolidated report, ONE exit code. It runs every layer of
quest validation and decides, deterministically, whether the quest tree is
sound:

  1. content    — tier-1 structural/quality scoring (quest_validator.py) over
                  all quests (or just changed files), gated at --fail-threshold.
  2. network    — dependency-graph integrity (validate-quest-network.py):
                  missing deps, cycles, duplicate permalinks, dangling edges,
                  retired fields, shipped quest-network.json soundness.
  3. freshness  — regenerates every registry-derived data artifact to a scratch
                  copy and diffs it against what's committed, proving the
                  generated _data/ has not drifted (the "never hand-edit"
                  invariant). Non-mutating: originals are always restored.
  4. tier2      — OPTIONAL Claude Code review (agentic_validate.py). Advisory by
                  default (never gates) so routine runs cost nothing; opt in with
                  --tier2 review|execute, gate with --tier2-gate.

Designed to be the single entry point for local dev (`make quest-audit`), the
Docker image (`make docker-validate`), and CI. Pure-Python deterministic layers
need only pyyaml; tier2 needs the `claude` CLI (or --tier2 mock).

Examples:
  quest_audit.py                          # full deterministic audit
  quest_audit.py --changed a.md b.md      # only these quests (PR fast-path)
  quest_audit.py --json report.json       # machine-readable consolidated report
  quest_audit.py --tier2 review --tier2-sample 5   # + advisory Claude review
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

_HERE = Path(__file__).resolve().parent
REPO_ROOT = _HERE.parents[1]
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import quest_registry as reg  # noqa: E402
import quest_lib  # noqa: E402

QUESTS_DIR = REPO_ROOT / "pages" / "_quests"
NETWORK_JSON = REPO_ROOT / "assets" / "data" / "quest-network.json"

# Registry-derived data artifacts that must stay in sync with the registry +
# quest files. (generator script, [output files]) — the freshness check
# regenerates each and diffs against what's on disk.
GENERATORS = [
    ("generate-quest-levels-data.py", [
        "_data/quests/levels.yml", "_data/quests/tiers.yml", "_data/quests/order.yml",
    ]),
    ("generate-quest-navigation.py", [
        "_data/navigation/quests.yml",
    ]),
    ("build-quest-network.py", [
        "assets/data/quest-network.json", "_data/quests/network.yml",
    ]),
]

# ── console helpers ──────────────────────────────────────────────────────────
_TTY = sys.stdout.isatty()
def _c(code): return code if _TTY else ""
RED, GREEN, YELLOW, BLUE, BOLD, NC = (
    _c("\033[0;31m"), _c("\033[0;32m"), _c("\033[1;33m"),
    _c("\033[0;34m"), _c("\033[1m"), _c("\033[0m"),
)
PASS, WARN, FAIL = f"{GREEN}✅{NC}", f"{YELLOW}⚠️{NC}", f"{RED}❌{NC}"


@dataclass
class Section:
    """Result of one audit layer."""
    name: str
    status: str = "pass"          # pass | warn | fail | skip
    gating: bool = True           # does a fail here fail the audit?
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    summary: str = ""
    detail: Dict = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.status in ("pass", "warn", "skip")


# ── lazy imports of sibling tools ────────────────────────────────────────────

def _import_quest_validator():
    qv_dir = REPO_ROOT / "test" / "quest-validator"
    if str(qv_dir) not in sys.path:
        sys.path.insert(0, str(qv_dir))
    import quest_validator  # noqa
    return quest_validator


def _import_network_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_quest_network", str(_HERE / "validate-quest-network.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── layer 1: content (tier 1) ────────────────────────────────────────────────

def run_content(changed: Optional[List[Path]], fail_threshold: int,
                exclude_drafts: bool, strict: bool) -> Section:
    qv = _import_quest_validator()
    config = REPO_ROOT / "_config.yml"
    validator = qv.QuestValidator(
        verbose=False, exclude_drafts=exclude_drafts,
        fail_threshold=fail_threshold,
        config_path=str(config) if config.exists() else None,
    )
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink):
        if changed:
            for f in changed:
                if quest_lib.is_meta_file(f):
                    continue
                validator.results.append(validator.validate_quest_file(f))
        else:
            validator.validate_directory(QUESTS_DIR)
    report = validator.generate_report()

    sec = Section("content")
    sec.detail = {
        "total": report["total"], "passed": report["passed"],
        "failed": report["failed"], "average_score": round(report["average_score"], 1),
        "placeholders": report["placeholders"],
    }
    for r in report["results"]:
        if not r.passed:
            for e in r.errors:
                sec.errors.append(f"{Path(r.quest_file).name}: {e}")
        for w in r.warnings:
            sec.warnings.append(f"{Path(r.quest_file).name}: {w}")
    if report["failed"] > 0:
        sec.status = "fail"
    elif strict and report["total_warnings"] > 0:
        sec.status = "fail"
    elif report["total_warnings"] > 0:
        sec.status = "warn"
    sec.summary = (f"{report['passed']}/{report['total']} quests pass "
                   f"(avg {report['average_score']:.1f}%), "
                   f"{report['failed']} failed, {report['placeholders']} placeholder(s)")
    return sec


# ── layer 2: network ─────────────────────────────────────────────────────────

def run_network(strict: bool) -> Section:
    mod = _import_network_validator()
    network_json = str(NETWORK_JSON) if NETWORK_JSON.exists() else None
    res = mod.run_network_validation(
        str(QUESTS_DIR), network_json=network_json, strict=strict, quiet=True)
    sec = Section("network")
    sec.errors = list(res["errors"])
    sec.warnings = list(res["warnings"])
    sec.detail = res["stats"]
    if res["errors"]:
        sec.status = "fail"
    elif strict and res["warnings"]:
        sec.status = "fail"
    elif res["warnings"]:
        sec.status = "warn"
    s = res["stats"]
    sec.summary = (f"{s['total_quests']} nodes, {s['broken_dependencies']} broken dep(s), "
                   f"{s['duplicate_permalinks']} dup permalink(s), {s['orphaned_quests']} orphan(s)")
    return sec


# ── layer 3: data freshness ──────────────────────────────────────────────────

def run_freshness(gate: bool) -> Section:
    """Regenerate every registry-derived artifact and diff against disk.

    Non-mutating: each target file is backed up in memory, regenerated, compared,
    then restored — so a dev's working tree is never left modified, even if a
    generator raises midway (restore happens in `finally`).
    """
    sec = Section("freshness", gating=gate)
    targets = [REPO_ROOT / p for _, outs in GENERATORS for p in outs]
    backups: Dict[Path, Optional[bytes]] = {
        p: (p.read_bytes() if p.exists() else None) for p in targets
    }
    stale: List[str] = []
    try:
        for script, outs in GENERATORS:
            proc = subprocess.run(
                [sys.executable, str(_HERE / script)],
                cwd=str(REPO_ROOT), capture_output=True, text=True)
            if proc.returncode != 0:
                sec.errors.append(f"generator {script} failed: "
                                  f"{(proc.stderr or proc.stdout).strip()[-300:]}")
        for p in targets:
            new = p.read_bytes() if p.exists() else None
            if new != backups[p]:
                stale.append(str(p.relative_to(REPO_ROOT)))
    finally:
        for p, original in backups.items():
            if original is None:
                if p.exists():
                    p.unlink()
            else:
                p.write_bytes(original)

    sec.detail = {"stale_files": stale}
    if sec.errors:
        sec.status = "fail"
    elif stale:
        sec.status = "fail" if gate else "warn"
        for f in stale:
            (sec.errors if gate else sec.warnings).append(
                f"stale generated data: {f} — run `make quest-data` and commit")
    sec.summary = ("all generated data in sync" if not stale
                   else f"{len(stale)} stale generated file(s): {', '.join(stale)}")
    return sec


# ── layer 4: tier 2 (Claude, optional + advisory) ────────────────────────────

def run_tier2(mode: str, changed: Optional[List[Path]], sample: int,
              gate: bool, fail_threshold: int, mock: bool,
              max_cost_usd: float, max_turns: int, isolate: str) -> Section:
    sec = Section("tier2", gating=gate)
    av_dir = REPO_ROOT / "test" / "quest-validator"
    cmd = [sys.executable, str(av_dir / "agentic_validate.py"),
           "--mode", mode, "--report", "/tmp/quest-tier2.json"]
    if mock:
        cmd.append("--mock")
    # Filter meta files FIRST, then decide the target. A changed set that is all
    # meta files must NOT silently fall through to a full-tree, uncapped review
    # against the real CLI — skip instead.
    files = [str(f) for f in (changed or []) if not quest_lib.is_meta_file(f)]
    if changed and not files:
        sec.status = "skip"
        sec.summary = "tier2 skipped: no non-meta quests in the changed set"
        return sec
    if files:
        cmd += files
    else:
        cmd += ["-d", str(QUESTS_DIR), "--sample", str(sample)]
    if max_cost_usd:
        cmd += ["--max-cost-usd", str(max_cost_usd)]
    if max_turns:
        cmd += ["--max-turns", str(max_turns)]
    if isolate and isolate != "none":
        cmd += ["--isolate", isolate]
    if gate and fail_threshold:
        cmd += ["--fail-threshold", str(fail_threshold)]
    try:
        proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    except Exception as e:  # pragma: no cover
        sec.status = "skip"
        sec.summary = f"tier2 skipped: {e}"
        return sec
    rc = proc.returncode
    data = {}
    try:
        data = json.loads(Path("/tmp/quest-tier2.json").read_text())
    except Exception:
        pass
    counts = (data.get("counts") or {}) if isinstance(data, dict) else {}
    # Aggregate snippet-execution coverage across quests (execute mode).
    snip_ran = snip_runnable = snip_failed = 0
    for r in (data.get("results") or []) if isinstance(data, dict) else []:
        s = r.get("snippets") or {}
        if s.get("available_runnable"):
            snip_ran += s.get("ran", 0)
            snip_runnable += s.get("available_runnable", 0)
            snip_failed += s.get("failed", 0)
    sec.detail = {
        "schema_version": data.get("schema_version"),
        "scored": data.get("scored"),
        "average": data.get("average"),
        "counts": counts,
        "cost_usd": data.get("cost_usd"),
        "snippets_ran": snip_ran,
        "snippets_runnable": snip_runnable,
        "snippets_failed": snip_failed,
    } if isinstance(data, dict) else {}
    snip_bit = (f" · ran {snip_ran}/{snip_runnable} snippets"
                + (f" ({snip_failed} failed)" if snip_failed else "")) if snip_runnable else ""
    tier2_line = (
        f"{data.get('scored', 0)} quest(s), avg {data.get('average', 0)}% — "
        f"{counts.get('pass', 0)} pass / {counts.get('warn', 0)} warn / "
        f"{counts.get('fail', 0)} fail"
        + snip_bit
        + (f" · ~${data.get('cost_usd')}" if data.get('cost_usd') else "")
    ) if isinstance(data, dict) and data else None
    if rc == 2:
        # Auth / no CLI / no quests — advisory, never fail the whole audit.
        sec.status = "skip"
        sec.summary = ("tier2 unavailable (no claude CLI / auth / quests) — "
                       "advisory only; use --tier2 mock to test the pipeline")
        return sec
    if gate and rc == 1:
        sec.status = "fail"
        sec.errors.append(f"tier2 quality gate failed (threshold {fail_threshold}%)")
    elif rc == 1:
        sec.status = "warn"
        sec.warnings.append("tier2 flagged quests below threshold (advisory)")
    if gate:
        sec.summary = (f"tier2 {mode} gate {'passed' if rc == 0 else 'failed'}"
                       + (f" — {tier2_line}" if tier2_line else ""))
    else:
        sec.summary = tier2_line or f"tier2 {mode} complete (advisory)"
    return sec


# ── report ───────────────────────────────────────────────────────────────────

def render(sections: List[Section], quiet: bool) -> int:
    gating_fail = any(s.gating and s.status == "fail" for s in sections)
    if not quiet:
        print()
        print(f"{BOLD}{'═'*72}{NC}")
        print(f"{BOLD}  IT-JOURNEY QUEST AUDIT{NC}")
        print(f"{BOLD}{'═'*72}{NC}")
        for s in sections:
            icon = {"pass": PASS, "warn": WARN, "fail": FAIL, "skip": "•"}[s.status]
            gate = "" if s.gating else f" {BLUE}(advisory){NC}"
            print(f"\n{icon} {BOLD}{s.name}{NC}{gate} — {s.summary}")
            for e in s.errors[:25]:
                print(f"    {RED}✗ {e}{NC}")
            if len(s.errors) > 25:
                print(f"    {RED}… and {len(s.errors)-25} more error(s){NC}")
            for w in s.warnings[:8]:
                print(f"    {YELLOW}~ {w}{NC}")
            if len(s.warnings) > 8:
                print(f"    {YELLOW}… and {len(s.warnings)-8} more warning(s){NC}")
        print(f"\n{BOLD}{'─'*72}{NC}")
        verdict = f"{FAIL} AUDIT FAILED" if gating_fail else f"{PASS} AUDIT PASSED"
        print(f"{BOLD}  {verdict}{NC}")
        print(f"{BOLD}{'═'*72}{NC}\n")
    return 1 if gating_fail else 0


def to_json(sections: List[Section]) -> dict:
    gating_fail = any(s.gating and s.status == "fail" for s in sections)
    return {
        "passed": not gating_fail,
        "sections": [
            {"name": s.name, "status": s.status, "gating": s.gating,
             "summary": s.summary, "errors": s.errors, "warnings": s.warnings,
             "detail": s.detail}
            for s in sections
        ],
    }


def main() -> int:
    p = argparse.ArgumentParser(
        description="Unified IT-Journey quest validation (content + network + freshness + optional Claude).",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    p.add_argument("--changed", nargs="*", metavar="FILE",
                   help="Limit content + tier2 to these quest files (PR fast-path).")
    p.add_argument("--fail-threshold", type=int, default=70,
                   help="Tier-1 per-quest minimum score %% (default 70; 0 disables).")
    p.add_argument("--exclude-drafts", action="store_true", help="Skip draft quests in tier 1.")
    p.add_argument("--strict", action="store_true",
                   help="Treat content/network warnings as failures.")
    p.add_argument("--no-content", action="store_true", help="Skip tier-1 content scoring.")
    p.add_argument("--no-network", action="store_true", help="Skip network validation.")
    p.add_argument("--no-freshness", action="store_true", help="Skip data-freshness check.")
    p.add_argument("--freshness-warn", action="store_true",
                   help="Report stale generated data as a warning, not a failure.")
    p.add_argument("--tier2", choices=["off", "review", "execute"], default="off",
                   help="Run Claude Code review (default off). review = read-only; execute = sandboxed.")
    p.add_argument("--tier2-sample", type=int, default=3, help="Quests to sample for tier2 (default 3).")
    p.add_argument("--tier2-gate", action="store_true",
                   help="Make tier2 gating (fail the audit on low scores). Default: advisory.")
    p.add_argument("--tier2-mock", action="store_true", help="Run tier2 with synthetic verdicts (no CLI/cost).")
    p.add_argument("--max-cost-usd", type=float, default=0.0, help="Tier2 cost ceiling (USD, 0 = none).")
    p.add_argument("--max-turns", type=int, default=0, help="Tier2 per-quest turn ceiling (0 = none).")
    p.add_argument("--isolate", choices=["none", "docker"], default="none",
                   help="Tier2 execute isolation (docker = run claude in a disposable container).")
    p.add_argument("--json", metavar="FILE", help="Write the consolidated report as JSON.")
    p.add_argument("--quiet", action="store_true", help="Suppress the console report.")
    args = p.parse_args()

    changed = [Path(f) for f in args.changed] if args.changed else None
    sections: List[Section] = []

    if not args.no_content:
        sections.append(run_content(changed, args.fail_threshold,
                                    args.exclude_drafts, args.strict))
    if not args.no_network:
        sections.append(run_network(args.strict))
    if not args.no_freshness:
        # Freshness is whole-tree; skip it in changed-only mode to keep PRs fast
        # (the scheduled/Docker audit owns the staleness gate).
        if changed:
            sec = Section("freshness", gating=False, status="skip",
                          summary="skipped in --changed mode (owned by the full audit)")
            sections.append(sec)
        else:
            sections.append(run_freshness(gate=not args.freshness_warn))

    if args.tier2 != "off":
        sections.append(run_tier2(
            args.tier2, changed, args.tier2_sample, args.tier2_gate,
            args.fail_threshold, args.tier2_mock, args.max_cost_usd,
            args.max_turns, args.isolate))

    rc = render(sections, args.quiet)

    if args.json:
        Path(args.json).write_text(json.dumps(to_json(sections), indent=2, default=str),
                                   encoding="utf-8")
        if not args.quiet:
            print(f"📄 Consolidated report → {args.json}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
