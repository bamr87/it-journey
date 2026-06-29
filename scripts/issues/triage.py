#!/usr/bin/env python3
"""
triage.py — Issue Autopilot classifier / planner (deterministic engine).

Reads every OPEN GitHub issue for the configured repo, classifies each one into a
`disposition` (per .issues/config.yml, first-match-wins), groups the resolvable /
closable ones into PR-sized `batches`, and emits a stable machine contract
(.issues/plan.json) plus human-readable worklist + report Markdown.

  Subcommands:
    plan     fetch open issues, classify, group, write all artifacts
    status   print a concise dashboard (reads plan.json if present, else recomputes)

  Artifacts written by `plan` (unless --dry-run):
    .issues/index.json                 raw snapshot of open issues (transient)
    .issues/plan.json                  the machine contract (transient)
    .issues/worklists/<YYYY-MM-DD>.md  readable worklist for the autopilot loop
    .issues/reports/<YYYY-MM-DD>.md    short health report

  ---------------------------------------------------------------------------
  READ / PLAN ONLY. This script NEVER mutates GitHub. It does not close,
  comment, label, or open PRs. It only reads issues (via the `gh` CLI, the
  repo's house pattern) and writes plan files to .issues/. Closing /
  commenting / PR-opening is performed elsewhere by the autopilot agents and
  workflows, which ACT on this plan but never re-decide policy.

  HARD GUARDRAIL (enforced in code below, not a config knob): a HUMAN-authored
  issue can NEVER receive a *close* disposition. Any such match is downgraded to
  `needs-human`. Only bot/automation-authored noise is ever auto-close eligible.

  Untrusted-input quarantine: issue title/body text is treated strictly as DATA.
  It is regex-matched and copied into reports, but NEVER eval'd / exec'd / shelled.
  ---------------------------------------------------------------------------

Author: IT-Journey Team   |   Part of the Issue Autopilot foundation.
"""
from __future__ import annotations

import argparse
import json
import re
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
CONFIG_PATH = ISSUES_DIR / "config.yml"

# Bot detection heuristics layered on top of gh's author.is_bot flag.
BOT_LOGIN_SUFFIX = "[bot]"
BOT_LOGIN_EXACT = "app/github-actions"

# How many open issues to ask gh for.
GH_FETCH_LIMIT = 200

GH_JSON_FIELDS = (
    "number,title,body,labels,author,createdAt,updatedAt,comments,milestone"
)


# --------------------------------------------------------------------------- #
# Small utilities
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


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    """Load .issues/config.yml, conforming to its exact schema."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except FileNotFoundError:
        print(f"ERROR: config not found at {path}", file=sys.stderr)
        raise
    except yaml.YAMLError as exc:
        print(f"ERROR: could not parse {path}: {exc}", file=sys.stderr)
        raise
    if not isinstance(data, dict):
        raise ValueError(f"config root must be a mapping, got {type(data).__name__}")
    return data


# --------------------------------------------------------------------------- #
# Fetch
# --------------------------------------------------------------------------- #
def fetch_issues_via_gh(repo: str) -> list[dict[str, Any]]:
    """Fetch open issues with the `gh` CLI. Raises on any gh failure."""
    cmd = [
        "gh",
        "issue",
        "list",
        "--repo",
        repo,
        "--state",
        "open",
        "--limit",
        str(GH_FETCH_LIMIT),
        "--json",
        GH_JSON_FIELDS,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"gh exited {proc.returncode}: {proc.stderr.strip() or '(no stderr)'}"
        )
    try:
        issues = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"could not parse gh JSON output: {exc}") from exc
    if not isinstance(issues, list):
        raise RuntimeError("gh returned non-list JSON for issue list")
    return issues


def load_issues_from_file(path: Path) -> list[dict[str, Any]]:
    """Load a previously-saved index.json (gh fallback). Returns [] on trouble."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        warn(f"--from-file {path} not found; proceeding with zero issues")
        return []
    except json.JSONDecodeError as exc:
        warn(f"--from-file {path} is not valid JSON ({exc}); proceeding with zero issues")
        return []
    if not isinstance(data, list):
        warn(f"--from-file {path} did not contain a JSON list; proceeding with zero issues")
        return []
    return data


def acquire_issues(
    repo: str, from_file: Optional[str]
) -> tuple[list[dict[str, Any]], str]:
    """
    Resolve the issue list and report the source.

    Order of preference:
      1. --from-file (explicit offline mode).
      2. gh CLI.
      3. on gh failure, fall back to .issues/index.json if present.

    Returns (issues, source) where source describes provenance. Degrades to an
    empty list (never raises) so callers can still emit a partial plan + exit 0.
    """
    if from_file:
        return load_issues_from_file(Path(from_file)), f"file:{from_file}"

    try:
        return fetch_issues_via_gh(repo), "gh"
    except (RuntimeError, FileNotFoundError, OSError) as exc:
        warn(f"gh unavailable or errored ({exc}); attempting .issues/index.json fallback")
        idx = ISSUES_DIR / "index.json"
        if idx.exists():
            return load_issues_from_file(idx), f"fallback:{idx}"
        warn("no cached index.json fallback found; proceeding with zero issues")
        return [], "empty"


# --------------------------------------------------------------------------- #
# Normalization helpers (issue field extraction — all treated as DATA)
# --------------------------------------------------------------------------- #
def label_names(issue: dict[str, Any]) -> list[str]:
    """Return label name strings; tolerate either dict-labels or bare strings."""
    out: list[str] = []
    for lbl in issue.get("labels") or []:
        if isinstance(lbl, dict):
            name = lbl.get("name")
            if isinstance(name, str):
                out.append(name)
        elif isinstance(lbl, str):
            out.append(lbl)
    return out


def author_login(issue: dict[str, Any]) -> str:
    author = issue.get("author") or {}
    if isinstance(author, dict):
        return str(author.get("login") or "")
    return ""


def is_bot_author(issue: dict[str, Any]) -> bool:
    """
    Bot-ness per the rules: gh's author.is_bot OR a login containing "[bot]"
    OR login == "app/github-actions".
    """
    author = issue.get("author") or {}
    if isinstance(author, dict) and author.get("is_bot") is True:
        return True
    login = author_login(issue)
    if BOT_LOGIN_SUFFIX in login:
        return True
    if login == BOT_LOGIN_EXACT:
        return True
    return False


def infer_area(issue: dict[str, Any], collections: list[str]) -> Optional[str]:
    """
    Infer the collection/area for a content issue from its labels first
    (`collection:quests` or `collection/quests`), then from a title mention.
    Returns a collection name or None.
    """
    labels = label_names(issue)
    for lbl in labels:
        low = lbl.lower()
        for sep in (":", "/"):
            prefix = f"collection{sep}"
            if low.startswith(prefix):
                candidate = low[len(prefix):].strip()
                # Tolerate `_quests` / `quests` / `quest`.
                candidate = candidate.lstrip("_")
                for coll in collections:
                    if candidate == coll or candidate == coll.rstrip("s"):
                        return coll
    title = str(issue.get("title") or "")
    title_low = title.lower()
    for coll in collections:
        # Word-ish match on the collection name in the title.
        if re.search(rf"\b{re.escape(coll)}\b", title_low):
            return coll
    return None


# --------------------------------------------------------------------------- #
# Classification
# --------------------------------------------------------------------------- #
def match_disposition(
    issue: dict[str, Any], match: dict[str, Any]
) -> bool:
    """
    Evaluate a single disposition `match` object as an AND over present keys.
    Omitted keys are unconstrained. Title/body are regex-matched as DATA only.
    """
    if not isinstance(match, dict):
        return False

    labels = label_names(issue)
    label_set = {lbl.lower() for lbl in labels}

    if "author_is_bot" in match:
        if bool(is_bot_author(issue)) != bool(match["author_is_bot"]):
            return False

    if "any_label" in match:
        wanted = {str(x).lower() for x in (match["any_label"] or [])}
        if not (label_set & wanted):
            return False

    if "all_label" in match:
        wanted = {str(x).lower() for x in (match["all_label"] or [])}
        if not wanted.issubset(label_set):
            return False

    if "title_regex" in match and match["title_regex"]:
        title = str(issue.get("title") or "")
        try:
            if not re.search(str(match["title_regex"]), title, re.IGNORECASE):
                return False
        except re.error as exc:
            warn(f"invalid title_regex {match['title_regex']!r}: {exc}")
            return False

    if "body_regex" in match and match["body_regex"]:
        body = issue.get("body")
        body = "" if body is None else str(body)
        try:
            if not re.search(str(match["body_regex"]), body, re.IGNORECASE):
                return False
        except re.error as exc:
            warn(f"invalid body_regex {match['body_regex']!r}: {exc}")
            return False

    return True


def classify_issue(
    issue: dict[str, Any], config: dict[str, Any]
) -> dict[str, Any]:
    """
    Classify one issue. Returns the per-issue plan record. Applies the hard
    human-authored close guardrail unconditionally.
    """
    dispositions = config.get("dispositions") or []
    default = config.get("default_disposition") or {
        "id": "needs-human",
        "action": "route-human",
    }
    collections = (config.get("areas") or {}).get("collections") or []

    is_bot = is_bot_author(issue)
    labels = label_names(issue)
    login = author_login(issue)

    chosen: dict[str, Any] = {}
    for disp in dispositions:
        if not isinstance(disp, dict):
            continue
        if match_disposition(issue, disp.get("match") or {}):
            chosen = disp
            break
    if not chosen:
        chosen = default

    disposition_id = str(chosen.get("id") or "needs-human")
    action = str(chosen.get("action") or "route-human")
    route_to = chosen.get("route_to")
    note = chosen.get("note")
    downgrade_reason: Optional[str] = None

    # HARD GUARDRAIL: a close disposition on a HUMAN-authored issue is downgraded
    # to needs-human, unconditionally and in code (never a config knob).
    is_close = action.startswith("recommend-close") or disposition_id.startswith("close-")
    if is_close and not is_bot:
        downgrade_reason = "human-authored; close requires a human"
        disposition_id = str(default.get("id") or "needs-human")
        action = str(default.get("action") or "route-human")
        route_to = default.get("route_to")
        note = default.get("note")
        is_close = action.startswith("recommend-close") or disposition_id.startswith("close-")

    # Auto-close eligibility: only a close action AND a bot author qualifies.
    eligible_autoclose = bool(is_close and is_bot)

    area = infer_area(issue, collections)

    record: dict[str, Any] = {
        "number": issue.get("number"),
        "title": str(issue.get("title") or ""),
        "author_login": login,
        "is_bot": is_bot,
        "labels": labels,
        "disposition_id": disposition_id,
        "action": action,
        "route_to": route_to,
        "note": note,
        "area": area,
        "eligible_autoclose": eligible_autoclose,
        "created_at": issue.get("createdAt"),
        "updated_at": issue.get("updatedAt"),
    }
    if downgrade_reason:
        record["downgrade_reason"] = downgrade_reason
    return record


# --------------------------------------------------------------------------- #
# Batching
# --------------------------------------------------------------------------- #
def _branch_for(action: str, disposition_id: str, area: Optional[str],
                numbers: list[int]) -> str:
    """Compute a suggested branch name from the action + area + first issue."""
    first = numbers[0] if numbers else 0
    if action.startswith("recommend-close") or disposition_id.startswith("close-"):
        return f"chore/issue-autopilot-{disposition_id}"
    if action == "resolve-content":
        area_part = area or "general"
        return f"content/issue-{area_part}-{first}"
    if action == "resolve-code":
        return f"fix/issue-{first}"
    if action == "decompose":
        return f"chore/issue-autopilot-decompose-{first}"
    return f"chore/issue-autopilot-{disposition_id}"


def _suggested_labels(config: dict[str, Any], action: str,
                      disposition_id: str) -> list[str]:
    """Pick the autopilot label set appropriate for the batch action."""
    labels_cfg = config.get("labels") or {}
    out: list[str] = []
    triaged = labels_cfg.get("triaged")
    if triaged:
        out.append(str(triaged))
    if action.startswith("recommend-close") or disposition_id.startswith("close-"):
        stale = labels_cfg.get("stale")
        if stale:
            out.append(str(stale))
    elif action in ("resolve-content", "resolve-code"):
        pr = labels_cfg.get("pr")
        if pr:
            out.append(str(pr))
    elif action == "decompose":
        epic = labels_cfg.get("epic")
        if epic:
            out.append(str(epic))
    elif action == "route-human":
        nh = labels_cfg.get("needs_human")
        if nh:
            out.append(str(nh))
    return out


def build_batches(
    records: list[dict[str, Any]], config: dict[str, Any]
) -> list[dict[str, Any]]:
    """
    Group classified issues into PR-sized batches per the grouping rules:
      - close-* dispositions   -> one batch per disposition.
      - resolve-content        -> one batch per area (collection).
      - resolve-code           -> one batch per issue.
      - decompose (epic)       -> one batch per issue.
      - needs-human            -> one batch (informational; no PR).

    Honors limits.max_resolve_batches_per_run: extra resolve batches are KEPT
    but marked deferred=true with a reason (never silently dropped).
    """
    limits = config.get("limits") or {}
    max_resolve = int(limits.get("max_resolve_batches_per_run", 3) or 0)

    batches: list[dict[str, Any]] = []

    # --- close-* : one batch per disposition -------------------------------- #
    close_groups: dict[str, list[dict[str, Any]]] = {}
    # --- resolve-content : one batch per area ------------------------------- #
    content_groups: dict[Optional[str], list[dict[str, Any]]] = {}
    # --- resolve-code : per issue ------------------------------------------- #
    code_records: list[dict[str, Any]] = []
    # --- decompose : per issue ---------------------------------------------- #
    decompose_records: list[dict[str, Any]] = []
    # --- needs-human : one informational batch ------------------------------ #
    human_records: list[dict[str, Any]] = []

    for rec in records:
        action = rec["action"]
        disp = rec["disposition_id"]
        if action.startswith("recommend-close") or disp.startswith("close-"):
            close_groups.setdefault(disp, []).append(rec)
        elif action == "resolve-content":
            content_groups.setdefault(rec.get("area"), []).append(rec)
        elif action == "resolve-code":
            code_records.append(rec)
        elif action == "decompose":
            decompose_records.append(rec)
        else:  # route-human / needs-human / anything else
            human_records.append(rec)

    # close batches (one per disposition) — triage, no PR.
    for disp, recs in sorted(close_groups.items()):
        numbers = [r["number"] for r in recs]
        action = recs[0]["action"]
        note = recs[0].get("note")
        batches.append({
            "id": disp,
            "disposition_id": disp,
            "action": action,
            "area": None,
            "issue_numbers": numbers,
            "title": f"Recommend close: {disp} ({len(numbers)} issue(s))",
            "suggested_branch": _branch_for(action, disp, None, numbers),
            "suggested_labels": _suggested_labels(config, action, disp),
            "note": note,
            "deferred": False,
        })

    # decompose batches (one per epic issue) — triage, no PR.
    for rec in decompose_records:
        disp = rec["disposition_id"]
        n = rec["number"]
        batches.append({
            "id": f"{disp}-{n}",
            "disposition_id": disp,
            "action": rec["action"],
            "area": rec.get("area"),
            "issue_numbers": [n],
            "title": f"Decompose epic #{n}: {rec['title'][:60]}",
            "suggested_branch": _branch_for(rec["action"], disp, rec.get("area"), [n]),
            "suggested_labels": _suggested_labels(config, rec["action"], disp),
            "note": rec.get("note"),
            "deferred": False,
        })

    # --- resolve batches: collect first, then apply the per-run cap --------- #
    resolve_batches: list[dict[str, Any]] = []

    for area, recs in sorted(
        content_groups.items(), key=lambda kv: (kv[0] is None, kv[0] or "")
    ):
        numbers = [r["number"] for r in recs]
        area_id = area or "general"
        resolve_batches.append({
            "id": f"content-{area_id}",
            "disposition_id": recs[0]["disposition_id"],
            "action": "resolve-content",
            "area": area,
            "issue_numbers": numbers,
            "title": f"Resolve content ({area_id}): {len(numbers)} issue(s)",
            "suggested_branch": _branch_for("resolve-content", recs[0]["disposition_id"], area, numbers),
            "suggested_labels": _suggested_labels(config, "resolve-content", recs[0]["disposition_id"]),
            "note": recs[0].get("note"),
            "deferred": False,
        })

    for rec in code_records:
        n = rec["number"]
        disp = rec["disposition_id"]
        resolve_batches.append({
            "id": f"code-{n}",
            "disposition_id": disp,
            "action": "resolve-code",
            "area": rec.get("area"),
            "issue_numbers": [n],
            "title": f"Resolve code #{n}: {rec['title'][:60]}",
            "suggested_branch": _branch_for("resolve-code", disp, rec.get("area"), [n]),
            "suggested_labels": _suggested_labels(config, "resolve-code", disp),
            "note": rec.get("note"),
            "deferred": False,
        })

    # Apply the cap: keep extras but flag them deferred (never drop silently).
    for idx, batch in enumerate(resolve_batches):
        if max_resolve and idx >= max_resolve:
            batch["deferred"] = True
            batch["deferred_reason"] = (
                f"exceeds limits.max_resolve_batches_per_run={max_resolve} "
                f"(resolve batch #{idx + 1} of {len(resolve_batches)})"
            )
            warn(
                f"deferred resolve batch {batch['id']} "
                f"({batch['deferred_reason']})"
            )
    batches.extend(resolve_batches)

    # needs-human informational batch (no PR).
    if human_records:
        numbers = [r["number"] for r in human_records]
        default = config.get("default_disposition") or {}
        disp = str(default.get("id") or "needs-human")
        batches.append({
            "id": "needs-human",
            "disposition_id": disp,
            "action": str(default.get("action") or "route-human"),
            "area": None,
            "issue_numbers": numbers,
            "title": f"Needs human ({len(numbers)} issue(s))",
            "suggested_branch": None,
            "suggested_labels": _suggested_labels(config, "route-human", disp),
            "note": "Informational. No PR — these require human judgment.",
            "deferred": False,
        })

    return batches


# --------------------------------------------------------------------------- #
# Counts + plan assembly
# --------------------------------------------------------------------------- #
def compute_counts(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_disposition: dict[str, int] = {}
    bot = human = eligible = 0
    for rec in records:
        by_disposition[rec["disposition_id"]] = (
            by_disposition.get(rec["disposition_id"], 0) + 1
        )
        if rec["is_bot"]:
            bot += 1
        else:
            human += 1
        if rec["eligible_autoclose"]:
            eligible += 1
    return {
        "by_disposition": dict(sorted(by_disposition.items())),
        "total": len(records),
        "bot": bot,
        "human": human,
        "eligible_autoclose": eligible,
    }


def build_plan(
    issues: list[dict[str, Any]], config: dict[str, Any], repo: str
) -> dict[str, Any]:
    """Classify, batch, and assemble the full plan dict (the machine contract)."""
    limits = config.get("limits") or {}
    max_issues = int(limits.get("max_issues_per_run", 0) or 0)

    # Boundedness: classify everything, but only plan up to max_issues_per_run.
    considered = issues
    deferred_count = 0
    if max_issues and len(issues) > max_issues:
        considered = issues[:max_issues]
        deferred_count = len(issues) - max_issues
        warn(
            f"{deferred_count} issue(s) beyond limits.max_issues_per_run="
            f"{max_issues} were not classified this run"
        )

    records = [classify_issue(i, config) for i in considered]
    batches = build_batches(records, config)
    counts = compute_counts(records)

    return {
        "generated": now_iso(),
        "repo": repo,
        "counts": counts,
        "batches": batches,
        "issues": records,
        "deferred_unclassified_count": deferred_count,
        "total_open_seen": len(issues),
    }


# --------------------------------------------------------------------------- #
# Artifact writers
# --------------------------------------------------------------------------- #
def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def _md_code(text: str) -> str:
    """
    Render arbitrary text as a backtick-safe inline-code span so it reads as
    opaque DATA in the worklist, never as Markdown structure or instructions.
    The fence is chosen longer than the longest backtick run inside the text, and
    padded with spaces so a leading/trailing backtick can't merge with the fence.
    """
    text = re.sub(r"\s+", " ", text or "").strip()
    if not text:
        return "``"
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    fence = "`" * (longest + 1)
    return f"{fence} {text} {fence}"


def _md_issue_line(rec: dict[str, Any]) -> str:
    """
    One worklist line for an issue. The title is attacker-controlled, so it is
    emitted as an inline-code span (DATA) — never as plain Markdown the reading
    agent could mistake for instructions.
    """
    extra = ""
    if rec.get("downgrade_reason"):
        extra = f"  _(downgraded: {rec['downgrade_reason']})_"
    return f"  - `#{rec['number']}` — {_md_code(rec.get('title') or '')}{extra}"


def render_worklist_md(plan: dict[str, Any]) -> str:
    counts = plan["counts"]
    lines: list[str] = []
    lines.append("# Issue Autopilot — worklist")
    lines.append("")
    lines.append(f"_Generated {plan['generated']} for `{plan['repo']}`._")
    lines.append("")
    lines.append(
        f"Open issues seen: **{plan.get('total_open_seen', counts['total'])}** "
        f"· classified: **{counts['total']}** "
        f"· bot: **{counts['bot']}** · human: **{counts['human']}** "
        f"· auto-close eligible: **{counts['eligible_autoclose']}**"
    )
    lines.append("")

    # Dispositions summary table.
    lines.append("## Dispositions")
    lines.append("")
    lines.append("| disposition | count | action |")
    lines.append("| --- | ---: | --- |")
    action_by_disp: dict[str, str] = {}
    for rec in plan["issues"]:
        action_by_disp.setdefault(rec["disposition_id"], rec["action"])
    for disp, count in counts["by_disposition"].items():
        lines.append(f"| `{disp}` | {count} | {action_by_disp.get(disp, '?')} |")
    lines.append("")

    # Batches.
    lines.append("## Batches")
    lines.append("")
    active_batches = [b for b in plan["batches"] if b["id"] != "needs-human"]
    if not active_batches:
        lines.append("_No actionable batches this run._")
        lines.append("")
    issues_by_number = {r["number"]: r for r in plan["issues"]}
    for batch in active_batches:
        flag = " (DEFERRED)" if batch.get("deferred") else ""
        lines.append(f"### `{batch['id']}`{flag} — {batch['title']}")
        lines.append("")
        lines.append(f"- **Action:** `{batch['action']}`")
        if batch.get("area"):
            lines.append(f"- **Area:** `{batch['area']}`")
        if batch.get("suggested_branch"):
            lines.append(f"- **Suggested branch:** `{batch['suggested_branch']}`")
        if batch.get("suggested_labels"):
            labs = ", ".join(f"`{x}`" for x in batch["suggested_labels"])
            lines.append(f"- **Suggested labels:** {labs}")
        if batch.get("deferred") and batch.get("deferred_reason"):
            lines.append(f"- **Deferred:** {batch['deferred_reason']}")
        if batch.get("note"):
            note = re.sub(r"\s+", " ", str(batch["note"])).strip()
            lines.append(f"- **Note:** {note}")
        lines.append("- **Issues:**")
        for n in batch["issue_numbers"]:
            rec = issues_by_number.get(n)
            if rec:
                lines.append(_md_issue_line(rec))
            else:
                lines.append(f"  - `#{n}`")
        lines.append("")

    # Needs human.
    lines.append("## Needs human")
    lines.append("")
    human_batch = next((b for b in plan["batches"] if b["id"] == "needs-human"), None)
    if human_batch and human_batch["issue_numbers"]:
        for n in human_batch["issue_numbers"]:
            rec = issues_by_number.get(n)
            if rec:
                lines.append(_md_issue_line(rec))
        lines.append("")
    else:
        lines.append("_None this run._")
        lines.append("")

    # Boundedness note — never imply full coverage.
    lines.append("## Skipped / deferred")
    lines.append("")
    deferred_batches = [b for b in plan["batches"] if b.get("deferred")]
    unclassified = plan.get("deferred_unclassified_count", 0)
    if not deferred_batches and not unclassified:
        lines.append(
            "_Nothing deferred this run. This worklist reflects only the open "
            "issues seen at generation time — it is not a guarantee of full "
            "backlog coverage._"
        )
    else:
        if unclassified:
            lines.append(
                f"- **{unclassified}** open issue(s) beyond "
                f"`limits.max_issues_per_run` were not classified this run."
            )
        for b in deferred_batches:
            lines.append(
                f"- Resolve batch `{b['id']}` deferred: "
                f"{b.get('deferred_reason', 'cap reached')}"
            )
        lines.append("")
        lines.append(
            "_This worklist reflects only the open issues seen at generation "
            "time and is bounded by the configured per-run limits — it is not a "
            "guarantee of full backlog coverage._"
        )
    lines.append("")
    return "\n".join(lines)


def render_report_md(plan: dict[str, Any], issues_raw: list[dict[str, Any]]) -> str:
    counts = plan["counts"]
    lines: list[str] = []
    lines.append("# Issue Autopilot — health report")
    lines.append("")
    lines.append(f"_Generated {plan['generated']} for `{plan['repo']}`._")
    lines.append("")
    lines.append(f"- Open issues seen: **{plan.get('total_open_seen', counts['total'])}**")
    lines.append(f"- Classified this run: **{counts['total']}**")
    lines.append(f"- Bot-authored: **{counts['bot']}** · Human-authored: **{counts['human']}**")
    lines.append(f"- Auto-close eligible (bot + close): **{counts['eligible_autoclose']}**")
    # Count needs-human directly from records (the disposition id may differ).
    need_human = sum(1 for r in plan["issues"] if r["action"] == "route-human")
    lines.append(f"- Need human attention: **{need_human}**")

    # Oldest open issue (by createdAt) from the raw snapshot.
    oldest = _oldest_issue(issues_raw)
    if oldest:
        n = oldest.get("number")
        created = oldest.get("createdAt") or "?"
        lines.append(
            f"- Oldest open issue: `#{n}` ({created}) — "
            f"{_md_code(str(oldest.get('title') or ''))}"
        )
    lines.append("")

    lines.append("## Disposition breakdown")
    lines.append("")
    lines.append("| disposition | count |")
    lines.append("| --- | ---: |")
    for disp, count in counts["by_disposition"].items():
        lines.append(f"| `{disp}` | {count} |")
    lines.append("")
    return "\n".join(lines)


def _oldest_issue(issues_raw: list[dict[str, Any]]) -> Optional[dict[str, Any]]:
    dated = [i for i in issues_raw if i.get("createdAt")]
    if not dated:
        return None
    return min(dated, key=lambda i: str(i.get("createdAt")))


# --------------------------------------------------------------------------- #
# Subcommand: plan
# --------------------------------------------------------------------------- #
def cmd_plan(args: argparse.Namespace) -> int:
    try:
        config = load_config()
    except (FileNotFoundError, ValueError, yaml.YAMLError):
        return 1

    repo = args.repo or str(config.get("repo") or "")
    if not repo:
        print("ERROR: no repo specified and config has no `repo` key", file=sys.stderr)
        return 1

    issues, source = acquire_issues(repo, args.from_file)
    print(f"Fetched {len(issues)} open issue(s) [source={source}]", file=sys.stderr)

    plan = build_plan(issues, config, repo)

    output_cfg = config.get("output") or {}
    # Default to the repo root (script-relative), NOT cwd, so artifacts always land
    # in <repo>/.issues/ and dispatch.py (which reads script-relative) agrees,
    # regardless of where the command was invoked from.
    base = Path(args.output_dir) if args.output_dir else REPO_ROOT
    index_path = base / str(output_cfg.get("index", ".issues/index.json"))
    plan_path = base / str(output_cfg.get("plan", ".issues/plan.json"))
    worklist_dir = base / str(output_cfg.get("worklist_dir", ".issues/worklists"))
    report_dir = base / str(output_cfg.get("report_dir", ".issues/reports"))

    worklist_md = render_worklist_md(plan)
    report_md = render_report_md(plan, issues)

    if args.dry_run:
        print("--- plan.json (dry-run, not written) ---")
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        print("\n--- worklist (dry-run, not written) ---")
        print(worklist_md)
        return 0

    # Persist raw snapshot only when freshly fetched (don't clobber a --from-file
    # source with itself, but always write when source is gh/fallback).
    if source.startswith("gh") or source.startswith("fallback") or source == "empty":
        write_json(index_path, issues)
    write_json(plan_path, plan)

    worklist_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    day = today_str()
    (worklist_dir / f"{day}.md").write_text(worklist_md, encoding="utf-8")
    (report_dir / f"{day}.md").write_text(report_md, encoding="utf-8")

    print(f"Wrote {plan_path}")
    print(f"Wrote {worklist_dir / (day + '.md')}")
    print(f"Wrote {report_dir / (day + '.md')}")
    return 0


# --------------------------------------------------------------------------- #
# Subcommand: status
# --------------------------------------------------------------------------- #
def cmd_status(args: argparse.Namespace) -> int:
    try:
        config = load_config()
    except (FileNotFoundError, ValueError, yaml.YAMLError):
        return 1

    output_cfg = config.get("output") or {}
    base = Path(args.output_dir) if args.output_dir else REPO_ROOT
    plan_path = base / str(output_cfg.get("plan", ".issues/plan.json"))

    plan: Optional[dict[str, Any]] = None
    if plan_path.exists():
        try:
            with plan_path.open("r", encoding="utf-8") as fh:
                plan = json.load(fh)
        except json.JSONDecodeError as exc:
            warn(f"existing plan.json is unparseable ({exc}); recomputing")
            plan = None

    if plan is None:
        repo = args.repo or str(config.get("repo") or "")
        issues, source = acquire_issues(repo, args.from_file)
        print(f"(recomputed from {source})", file=sys.stderr)
        plan = build_plan(issues, config, repo)

    counts = plan["counts"]
    print("Issue Autopilot — status")
    print(f"  repo:      {plan.get('repo')}")
    print(f"  generated: {plan.get('generated')}")
    print(f"  total:     {counts['total']} (bot={counts['bot']} human={counts['human']})")
    print(f"  auto-close eligible: {counts['eligible_autoclose']}")
    need_human = sum(1 for r in plan["issues"] if r["action"] == "route-human")
    print(f"  need human:          {need_human}")
    print("  by disposition:")
    for disp, count in counts["by_disposition"].items():
        print(f"    {disp:<16} {count}")
    active = [b for b in plan["batches"] if b["id"] != "needs-human"]
    deferred = [b for b in active if b.get("deferred")]
    print(f"  batches: {len(active)} actionable ({len(deferred)} deferred)")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="triage.py",
        description=(
            "Issue Autopilot classifier/planner. READ + PLAN ONLY — never "
            "mutates GitHub. Classifies open issues and emits plan artifacts."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_plan = sub.add_parser(
        "plan", help="fetch open issues, classify, group, write artifacts"
    )
    p_plan.add_argument("--repo", default=None, help="owner/name (default: config.repo)")
    p_plan.add_argument(
        "--from-file", default=None,
        help="read a saved index.json instead of calling gh (offline fallback)",
    )
    p_plan.add_argument(
        "--dry-run", action="store_true",
        help="compute and print the plan but write nothing",
    )
    p_plan.add_argument(
        "--output-dir", default=None,
        help="base dir for artifacts (default: current working directory)",
    )
    p_plan.set_defaults(func=cmd_plan)

    p_status = sub.add_parser(
        "status", help="print a dashboard (reads latest plan.json, else recomputes)"
    )
    p_status.add_argument("--repo", default=None, help="owner/name (default: config.repo)")
    p_status.add_argument(
        "--from-file", default=None,
        help="read a saved index.json instead of calling gh (offline fallback)",
    )
    p_status.add_argument(
        "--output-dir", default=None,
        help="base dir to look for plan.json (default: current working directory)",
    )
    p_status.set_defaults(func=cmd_status)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
