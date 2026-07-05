#!/usr/bin/env python3
"""
walkthrough_plan.py — the deterministic planner for the quest-walkthrough routine.

Picks ONE *linked set of quests for a specific level and character* and emits it
as an ordered, dependency-sorted **playthrough plan** (JSON + human text). This is
the deterministic collector the `quest-walkthrough` skill consumes: the agent
plays exactly the quests this planner selected, in exactly this order, and never
chooses the curriculum itself.

WHY THIS EXISTS — the controlled-environment anchor.
The daily routine must walk a *coherent slice* of the curriculum end-to-end, not a
random scatter of quests. A character class (`developer`, `security-specialist`, …)
and a binary level (`0000`..`1111`) together name one such slice. This planner
resolves that slice from the SAME data the site renders from (the generated quest
network — `assets/data/quest-network.json`, falling back to `_data/quests/network.yml`
— plus the curated `_data/quests/paths.yml`), orders it by the quest dependency graph
(prerequisites first), and rotates the (character, level) pair by date so a daily run
sweeps the whole curriculum over time. Selection is data-driven and reproducible;
only the walkthrough + report are agentic.

Usage:
    # Explicit slice:
    python3 scripts/quest/walkthrough_plan.py --character developer --level 0001

    # Date-rotated slice (the daily routine's default — deterministic per day):
    python3 scripts/quest/walkthrough_plan.py --date 2026-06-29 --json plan.json

    # Ledger-driven SELECTION (the quest-perfection loop): one highest-priority
    # not-yet-perfect slice, falling back to date-rotation if the ledger is cold:
    python3 scripts/quest/walkthrough_plan.py --priority --json plan.json

    # One slice per character (fans the loop across every path), writing each
    # plan into --out-dir and printing the chosen slugs as a JSON list:
    python3 scripts/quest/walkthrough_plan.py --all-paths --out-dir .work

    # List the characters / levels available, then exit:
    python3 scripts/quest/walkthrough_plan.py --list

    # Self-check (no network, no args): asserts the planner on the live data.
    python3 scripts/quest/walkthrough_plan.py --selftest

SELECTION vs PLANNING — this file owns only the deterministic curriculum slicing
(`build_plan` / `rotate_slice`, UNCHANGED). The `--priority` / `--all-paths` modes
add *ledger-aware selection* on top: they ask `scripts/quest/ledger.py` (the ONE
source of truth) which slice is worst/oldest-not-perfect, then plan exactly that
slice. The ledger is consulted as an oracle; this planner never writes it. If
`ledger.py` or `.quests/ledger.json` is missing or cold, selection degrades
gracefully to the existing date-rotation, so the planner always emits a plan.

The plan is advisory structure, not a schema gate: a level with no quests degrades
to an empty `quests` list with a reason rather than failing, because the network
data is regenerated and can drift.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date as _date
from pathlib import Path
from typing import Dict, List, Optional

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    print("Error: PyYAML is required but not installed (pip install pyyaml).",
          file=sys.stderr)
    raise

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import quest_registry as reg  # noqa: E402

REPO_ROOT = _HERE.parents[1]
# The full network JSON carries the authoritative on-disk `file` per node (a
# quest's permalink slug often differs from its filename — e.g.
# /quests/0001/avatar-forge/ lives in side-quest-avatar-forge.md), so it is the
# preferred source. The trimmed _data YAML is the fallback (no `file` field).
NETWORK_JSON = REPO_ROOT / "assets" / "data" / "quest-network.json"
NETWORK_YML = REPO_ROOT / "_data" / "quests" / "network.yml"
PATHS_YML = REPO_ROOT / "_data" / "quests" / "paths.yml"

# Quest types we actually walk: the playable curriculum. Epic/bonus hubs live in
# codex/ and are landing pages, not step-by-step playthroughs, so we skip them.
WALKABLE_TYPES = ("main_quest", "side_quest")


# --- data loading ----------------------------------------------------------

def load_network(path: Optional[Path] = None) -> dict:
    """Load the quest network. Prefers the full JSON (it carries the authoritative
    on-disk `file` per node); falls back to the trimmed _data YAML."""
    if path is not None:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    elif NETWORK_JSON.exists():
        data = json.loads(NETWORK_JSON.read_text(encoding="utf-8")) or {}
    elif NETWORK_YML.exists():
        data = yaml.safe_load(NETWORK_YML.read_text(encoding="utf-8")) or {}
    else:
        raise FileNotFoundError(
            f"No quest network found ({NETWORK_JSON} / {NETWORK_YML}) — "
            f"run `make quest-data` to generate it."
        )
    data.setdefault("nodes", [])
    data.setdefault("edges", [])
    return data


def load_paths(path: Path = PATHS_YML) -> List[dict]:
    if not path.exists():
        raise FileNotFoundError(f"{path} not found.")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or []


# --- ledger-aware selection (oracle only; this planner never writes it) -----

# Default ledger path mirrors the LEDGER CLI CONTRACT (.quests/ledger.json).
DEFAULT_LEDGER = REPO_ROOT / ".quests" / "ledger.json"


def _import_ledger():
    """Import scripts/quest/ledger.py (it lives beside this file). Returns the
    module, or None if it cannot be imported — callers then degrade to rotation.

    The ledger is the ONE deterministic source of truth for which slice is
    worst/oldest-not-perfect; we consult its `select_*` helpers as an oracle and
    never mutate it here. Missing/broken ledger.py is non-fatal by design."""
    if str(_HERE) not in sys.path:
        sys.path.insert(0, str(_HERE))
    try:
        import ledger as _ledger  # noqa: E402  (scripts/quest/ledger.py)
        return _ledger
    except Exception:  # pragma: no cover - degrade to rotation if unavailable
        return None


def _load_ledger_or_none(ledger_mod, ledger_path: Path) -> Optional[dict]:
    """Load the ledger dict via the module's loader (tolerates a cold/empty file).
    Returns None if the module is absent or loading raised — caller falls back."""
    if ledger_mod is None:
        return None
    try:
        return ledger_mod.load_ledger(ledger_path)
    except Exception:  # pragma: no cover - any trouble → rotation fallback
        return None


def resolve_slug(paths: List[dict], slug: str) -> tuple:
    """Resolve a ledger slice id "<char>/<code>" to a (character, level) pair.

    The slug is the deterministic slice key (NEVER a permalink). The character
    key must exist in paths.yml; the level must be a valid 4-bit code."""
    if not slug or "/" not in slug:
        raise ValueError(f"malformed slice id '{slug}' (expected '<char>/<code>')")
    char_key, _, level = slug.partition("/")
    character = resolve_character(paths, char_key)
    if not reg.is_valid_level(level):
        raise ValueError(f"slice id '{slug}' has invalid level '{level}'")
    return character, level


def select_priority_slug(paths: List[dict], on: _date,
                         ledger_path: Path = DEFAULT_LEDGER) -> str:
    """Pick ONE slice id (worst/oldest not-perfect) via the ledger oracle.

    Degrades to date-rotation when ledger.py / ledger.json is missing or cold:
    a cold ledger has no informative ordering, so the deterministic daily
    rotation is the honest fallback."""
    ledger_mod = _import_ledger()
    ledger = _load_ledger_or_none(ledger_mod, ledger_path)
    if ledger_mod is not None and ledger is not None:
        try:
            slug = ledger_mod.select_priority(ledger)
        except Exception:  # pragma: no cover - degrade to rotation
            slug = None
        if slug:
            return slug
    char, level = rotate_slice(paths, on)
    return f"{char.get('key')}/{level}"


def select_all_paths_slugs(paths: List[dict], on: _date,
                           ledger_path: Path = DEFAULT_LEDGER) -> List[str]:
    """One slice id per character via the ledger oracle.

    Per-character degrade: if the ledger yields no slice for a character (cold or
    absent), fall back to rotate_slice([char], on) for THAT character, so every
    path still contributes a slice. Order follows paths.yml."""
    ledger_mod = _import_ledger()
    ledger = _load_ledger_or_none(ledger_mod, ledger_path)
    ledger_slugs: Dict[str, str] = {}
    if ledger_mod is not None and ledger is not None:
        try:
            for s in ledger_mod.select_all_paths(ledger) or []:
                char_key = str(s).split("/", 1)[0]
                ledger_slugs.setdefault(char_key, s)
        except Exception:  # pragma: no cover - degrade per-character below
            ledger_slugs = {}

    out: List[str] = []
    for c in paths:
        key = c.get("key")
        slug = ledger_slugs.get(key)
        if not slug:
            _, level = rotate_slice([c], on)
            slug = f"{key}/{level}"
        out.append(slug)
    return out


# --- selection -------------------------------------------------------------

def resolve_character(paths: List[dict], key: str) -> dict:
    for p in paths:
        if p.get("key") == key:
            return p
    keys = ", ".join(p.get("key", "?") for p in paths)
    raise ValueError(f"unknown character '{key}'. Available: {keys}")


def rotate_slice(paths: List[dict], on: _date) -> tuple:
    """Deterministically pick a (character, level) pair for a given date.

    Sweeps every character's level list over time: the day-ordinal selects the
    character (mod N), and the day-ordinal // N selects which level *within that
    character's path* — so consecutive days advance through one class's levels
    before rotating to the next class. Same date in → same slice out.
    """
    if not paths:
        raise ValueError("no character paths defined in paths.yml")
    ordinal = on.toordinal()
    char = paths[ordinal % len(paths)]
    levels = list(char.get("levels") or [])
    if not levels:
        # Degenerate path with no levels: fall back to the canonical order.
        levels = list(reg.LEVEL_ORDER)
    level = levels[(ordinal // len(paths)) % len(levels)]
    return char, level


def _order_links(quests: List[dict], edges: List[dict]) -> List[dict]:
    """Order a set of quests into a linked chain: prerequisites first.

    Edge semantics (from scripts/quest/build-quest-network.py):
      * required / recommended  source→target  ⇒  target is a prereq of source.
      * unlocks                 source→target  ⇒  source comes before target.
    We build a "comes-before" DAG over only the quests in this slice, Kahn
    topo-sort it, and break ties by difficulty then permalink so the order is
    stable and reproducible. Quests with no in-slice links keep curriculum order.
    """
    ids = [q["id"] for q in quests]
    idset = set(ids)
    by_id = {q["id"]: q for q in quests}

    # succ[x] = quests that must come AFTER x (x is their in-slice prereq).
    succ: Dict[str, set] = {qid: set() for qid in ids}
    for e in edges:
        src, tgt, kind = e.get("source"), e.get("target"), e.get("kind")
        if src not in idset or tgt not in idset:
            continue  # only links *within* this slice shape the order
        if kind in ("required", "recommended"):
            succ[tgt].add(src)            # src requires/recommends tgt → tgt first
        elif kind == "unlocks":
            succ[src].add(tgt)            # src unlocks tgt → src first

    # Difficulty rank for stable tie-breaking (easy quests first within a tier).
    diff_rank = {d: i for i, d in enumerate(reg.DIFFICULTIES)}

    def sort_key(qid: str) -> tuple:
        q = by_id[qid]
        return (diff_rank.get(q.get("difficulty", ""), len(reg.DIFFICULTIES)), qid)

    # The graph has genuine cycles (mutually-recommending quests), so a plain
    # topo-sort can't exist. We condense strongly-connected components (each
    # cycle collapses to one node), topo-sort the resulting DAG — which DOES
    # exist — and expand each component by sort_key. This respects every acyclic
    # "before" constraint and only ever reorders *within* a true cycle.
    components = _strongly_connected(ids, succ)
    comp_of = {qid: i for i, comp in enumerate(components) for qid in comp}

    # Condensation edges + indegree between components.
    cedges: Dict[int, set] = {i: set() for i in range(len(components))}
    cindeg: Dict[int, int] = {i: 0 for i in range(len(components))}
    for x in ids:
        for y in succ[x]:
            ci, cj = comp_of[x], comp_of[y]
            if ci != cj and cj not in cedges[ci]:
                cedges[ci].add(cj)
                cindeg[cj] += 1

    # Component sort key: by the best (smallest) member key, so ready components
    # are emitted deterministically and easiest-first.
    comp_key = {i: min(sort_key(q) for q in comp) for i, comp in enumerate(components)}

    ordered: List[dict] = []
    ready = sorted((i for i in range(len(components)) if cindeg[i] == 0),
                   key=lambda i: comp_key[i])
    while ready:
        ci = ready.pop(0)
        for qid in sorted(components[ci], key=sort_key):
            ordered.append(by_id[qid])
        for cj in sorted(cedges[ci], key=lambda j: comp_key[j]):
            cindeg[cj] -= 1
            if cindeg[cj] == 0:
                ready.append(cj)
                ready.sort(key=lambda i: comp_key[i])
    return ordered


def _strongly_connected(ids: List[str], succ: Dict[str, set]) -> List[List[str]]:
    """Tarjan's SCC — returns components in reverse-topological order, which we
    re-topo-sort by condensation. Iterative to avoid recursion limits on deep
    dependency chains."""
    index: Dict[str, int] = {}
    low: Dict[str, int] = {}
    on_stack: set = set()
    stack: List[str] = []
    comps: List[List[str]] = []
    counter = 0

    for root in ids:
        if root in index:
            continue
        work = [(root, iter(sorted(succ[root])))]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on_stack.add(root)
        while work:
            node, it = work[-1]
            advanced = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack.add(w)
                    work.append((w, iter(sorted(succ[w]))))
                    advanced = True
                    break
                elif w in on_stack:
                    low[node] = min(low[node], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[node])
            if low[node] == index[node]:
                comp = []
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    comp.append(w)
                    if w == node:
                        break
                comps.append(comp)
    return comps


def build_plan(character: dict, level: str, network: dict,
               max_quests: int = 0, window: int = 0,
               window_on: Optional[_date] = None) -> dict:
    """Resolve the linked playthrough plan for one (character, level) slice.

    Two independent ways to bound a big slice (a level can hold 20-30 quests):
      * `max_quests` — a hard first-N cap (the standalone/manual arm). Flags
        `stats.truncated`: the run only ever sees the first N quests.
      * `window` — a date-ROTATED window of N quests (the perfection loop). Each
        run walks a different contiguous slice, so over ceil(total/N) days the
        whole level is covered. The ledger accumulates that per-quest coverage
        across runs and only certifies `perfect` once the sweep is complete, so a
        single window is NOT treated as the whole slice. `stats.total_quests`
        always carries the full size for that cross-run accounting.
    `window` wins if both are set.
    """
    if not reg.is_valid_level(level):
        raise ValueError(f"invalid level '{level}' (expected a 4-bit code like 0001).")

    nodes = [n for n in network.get("nodes", [])
             if n.get("level") == level and n.get("type") in WALKABLE_TYPES]
    ordered = _order_links(nodes, network.get("edges", []))
    total_quests = len(ordered)

    truncated = False
    window_info: Optional[dict] = None
    if window and window > 0:
        # Date-rotated window: systematic daily sweep (index += 1 per day, wraps).
        # An empty/small slice (total <= window) is one window covering everything.
        num_windows = max(1, math.ceil(total_quests / window)) if total_quests else 1
        on = window_on or _date.today()
        index = on.toordinal() % num_windows
        start = index * window
        ordered = ordered[start:start + window]
        window_info = {
            "index": index,
            "of": num_windows,
            "size": window,
            "offset": start,
        }
    elif max_quests and max_quests > 0 and len(ordered) > max_quests:
        ordered = ordered[:max_quests]
        truncated = True

    quests = [{
        "permalink": q["id"],
        "title": q.get("title", ""),
        "level": q.get("level", level),
        "type": q.get("type", ""),
        "difficulty": q.get("difficulty", ""),
        # The agent reads the full quest source from this path. Prefer the node's
        # authoritative `file` (slug ≠ filename for many quests); derive from the
        # permalink only when the network has no `file` field (YAML fallback).
        "path": q.get("file") or _permalink_to_path(q["id"]),
    } for q in ordered]

    reason = ""
    if not quests:
        reason = (f"No walkable quests at level {level} for the {character.get('key')} "
                  f"path — the level may be sparse or all-codex. Pick another level.")

    return {
        "schema_version": "1.0.0",
        "character": {
            "key": character.get("key"),
            "name": character.get("name"),
            "icon": character.get("icon"),
            "tagline": character.get("tagline"),
            "levels": list(character.get("levels") or []),
        },
        "level": {
            "code": level,
            "theme": reg.theme_of(level),
            "tier": reg.tier_of(level),
            "tier_emoji": reg.tier_emoji_of(level),
            "permalink": reg.canonical_level_permalink(level),
        },
        "quests": quests,
        "stats": {
            "count": len(quests),
            # The FULL slice size — the denominator the ledger's cross-run coverage
            # + perfect predicate use. `count` is just this run's (possibly windowed)
            # subset; `total_quests` is the whole level.
            "total_quests": total_quests,
            "truncated": truncated,
            # Present only for a rotated (loop) plan: which window of the sweep this
            # run walks. Absent/None for a full or first-N-capped plan.
            "windowed": window_info is not None,
            "window": window_info,
            "by_type": _count(quests, "type"),
            "by_difficulty": _count(quests, "difficulty"),
        },
        "reason": reason,
    }


def _permalink_to_path(permalink: str) -> Optional[str]:
    """Best-effort map a quest permalink to its on-disk markdown file.

    Permalinks are /quests/<level>/<slug>/ or /quests/<level>/side-quests/<slug>/.
    The file is pages/_quests/<level>/<slug>.md regardless of the side-quests URL
    segment (side quests live in the level dir, not a side-quests subdir on disk).
    """
    parts = [p for p in permalink.strip("/").split("/") if p]
    # parts == ["quests", "<level>", (maybe "side-quests"), "<slug>"]
    if len(parts) < 3 or parts[0] != "quests":
        return None
    level = parts[1]
    slug = parts[-1]
    candidate = REPO_ROOT / "pages" / "_quests" / level / f"{slug}.md"
    rel = candidate.relative_to(REPO_ROOT)
    return str(rel) if candidate.exists() else str(rel)  # report path even if absent


def _count(items: List[dict], key: str) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for it in items:
        out[it.get(key, "")] = out.get(it.get(key, ""), 0) + 1
    return out


# --- rendering -------------------------------------------------------------

def render_text(plan: dict) -> str:
    c, lv = plan["character"], plan["level"]
    lines = [
        f"⚔️  Quest Walkthrough Plan",
        f"   Character : {c['icon']} {c['name']} ({c['key']})",
        f"   Level     : {lv['tier_emoji']} {lv['code']} — {lv['theme']} ({lv['tier']} tier)",
        f"   Quests    : {plan['stats']['count']} linked, in playthrough order",
        "",
    ]
    if plan["reason"]:
        lines.append(f"   ⚠️  {plan['reason']}")
        return "\n".join(lines)
    for i, q in enumerate(plan["quests"], 1):
        diff = q["difficulty"] or "—"
        lines.append(f"   {i:>2}. [{q['type']}] {q['title']}")
        lines.append(f"       {diff}  ·  {q['permalink']}  ·  {q['path']}")
    stats = plan["stats"]
    if stats["truncated"]:
        lines.append("\n   (list truncated by --max-quests)")
    w = stats.get("window")
    if w:
        lines.append(
            f"\n   (rotated window {w['index'] + 1}/{w['of']} — quests "
            f"{w['offset'] + 1}‑{w['offset'] + stats['count']} of "
            f"{stats['total_quests']}; the ledger accumulates full-slice coverage "
            f"across runs)")
    return "\n".join(lines)


# --- self-test -------------------------------------------------------------

def _selftest() -> int:
    """Exercise the planner against the live data with no network/args."""
    paths = load_paths()
    network = load_network()
    assert paths, "paths.yml produced no character paths"
    assert network.get("nodes"), "network.yml has no nodes — run `make quest-data`"

    # Rotation is deterministic and stays within the chosen character's levels.
    d = _date(2026, 6, 29)
    char, level = rotate_slice(paths, d)
    char2, level2 = rotate_slice(paths, d)
    assert (char["key"], level) == (char2["key"], level2), "rotation not deterministic"
    assert level in char["levels"], "rotated level escaped the character's path"

    # A concrete slice builds, is ordered, and respects in-slice prerequisites.
    plan = build_plan(resolve_character(paths, "developer"), "0001", network)
    assert plan["level"]["code"] == "0001"
    order = [q["permalink"] for q in plan["quests"]]
    assert len(order) == len(set(order)), "duplicate quests in plan"

    # Verify the order respects every "must come before" constraint that is NOT
    # part of a dependency cycle. (The live network has genuine cycles — e.g. a
    # pair that recommends each other — and in a cycle one constraint MUST be
    # violated; only acyclic constraints are hard.) Build the before-graph, take
    # its transitive closure, and treat a constraint a→b as hard unless b also
    # reaches a (i.e. they're mutually constrained = cyclic).
    idx = {pid: i for i, pid in enumerate(order)}
    eset = set(idx)
    before_pairs = set()  # (x, y): x must come before y
    for e in network.get("edges", []):
        if e["source"] not in eset or e["target"] not in eset:
            continue
        if e["kind"] in ("required", "recommended"):
            before_pairs.add((e["target"], e["source"]))   # prereq before dependent
        elif e["kind"] == "unlocks":
            before_pairs.add((e["source"], e["target"]))    # unlocker before unlocked

    reach: Dict[str, set] = {pid: set() for pid in order}
    for x, y in before_pairs:
        reach[x].add(y)
    changed = True
    while changed:  # transitive closure (tiny graph)
        changed = False
        for x in order:
            new = set().union(*(reach[m] for m in reach[x])) if reach[x] else set()
            if not new <= reach[x]:
                reach[x] |= new
                changed = True
    for x, y in before_pairs:
        if x in reach[y]:
            continue  # cyclic (y also reaches x) — violation is unavoidable
        assert idx[x] <= idx[y], f"acyclic prereq {x} ordered after dependent {y}"

    # Every planned quest resolves to a real file on disk (the path comes from
    # the node's authoritative `file`, since slug ≠ filename for many quests).
    missing = [q["path"] for c in paths for lv in c["levels"]
               for q in build_plan(c, lv, network)["quests"]
               if not (REPO_ROOT / q["path"]).exists()]
    assert not missing, f"{len(missing)} planned quest path(s) do not exist, e.g. {missing[:3]}"

    # max_quests truncates and flags it.
    capped = build_plan(resolve_character(paths, "developer"), "0001", network, max_quests=1)
    assert capped["stats"]["count"] <= 1
    if len(order) > 1:
        assert capped["stats"]["truncated"], "truncation not flagged"

    # --- rotated window: bounds the run to N, carries the FULL size, and sweeps
    # every quest over ceil(total/N) days without gap or overlap.
    dev = resolve_character(paths, "developer")
    full = build_plan(dev, "0001", network)["stats"]["total_quests"]
    if full > 2:
        N = 2
        num_windows = math.ceil(full / N)
        seen: list = []
        for day in range(num_windows):
            wp = build_plan(dev, "0001", network, window=N,
                            window_on=_date.fromordinal(d.toordinal() + day))
            ws = wp["stats"]
            assert ws["count"] <= N, "window exceeded its size"
            assert ws["total_quests"] == full, "window lost the full slice size"
            assert ws["windowed"] and ws["window"], "window not flagged"
            assert ws["window"]["of"] == num_windows, "window count drift"
            seen += [q["permalink"] for q in wp["quests"]]
        # num_windows consecutive days must cover every quest exactly once (the last
        # window may be short, so it's a set-equality, not a multiset check).
        allq = [q["permalink"] for q in build_plan(dev, "0001", network)["quests"]]
        assert set(seen) == set(allq), \
            f"rotation did not sweep the full slice ({len(set(seen))}/{len(allq)})"
        # window wins over max_quests when both are set.
        both = build_plan(dev, "0001", network, max_quests=1, window=N)["stats"]
        assert both["windowed"] and both["count"] <= N, "window must win over max_quests"

    # --- ledger-aware SELECTION (offline): exercise --priority / --all-paths.
    # We point at a guaranteed-absent ledger path. Whatever ledger.py does with a
    # cold/missing file (cold-start selection if it's importable, or None if it
    # is not), the SELECTION layer must always yield valid, resolvable, buildable
    # slices — one per character for --all-paths, in paths.yml order.
    no_ledger = Path("/nonexistent/walkthrough_plan_selftest/ledger.json")
    assert not no_ledger.exists(), "self-test sentinel ledger path unexpectedly exists"

    # --priority: produces ONE valid slug that resolves and plans without raising.
    pslug = select_priority_slug(paths, d, no_ledger)
    assert pslug and "/" in pslug, f"--priority produced a malformed slug: {pslug!r}"
    pchar, plevel = resolve_slug(paths, pslug)
    _ = build_plan(pchar, plevel, network)  # must not raise

    # --all-paths: one slug per character, in paths.yml order, each buildable.
    aslugs = select_all_paths_slugs(paths, d, no_ledger)
    assert len(aslugs) == len(paths), \
        f"--all-paths must emit one slice per character ({len(aslugs)} vs {len(paths)})"
    for c, slug in zip(paths, aslugs):
        ac, al = resolve_slug(paths, slug)
        assert ac["key"] == c["key"], "--all-paths slice order escaped paths.yml order"
        _ = build_plan(ac, al, network)  # must not raise

    # Force the GENUINE degradation path: with the ledger module unavailable, both
    # modes MUST fall back to deterministic rotation (priority → whole-paths
    # rotation; all-paths → per-character rotation), proving graceful degradation.
    _real_import = _import_ledger
    try:
        globals()["_import_ledger"] = lambda: None  # simulate missing ledger.py
        fslug = select_priority_slug(paths, d, no_ledger)
        rchar, rlevel = rotate_slice(paths, d)
        assert fslug == f"{rchar.get('key')}/{rlevel}", \
            "--priority must fall back to date-rotation when ledger.py is unavailable"
        fall = select_all_paths_slugs(paths, d, no_ledger)
        for c, slug in zip(paths, fall):
            _, fl = rotate_slice([c], d)
            assert slug == f"{c.get('key')}/{fl}", \
                "--all-paths must fall back to per-character rotation when ledger.py is unavailable"
    finally:
        globals()["_import_ledger"] = _real_import

    print("✅ walkthrough_plan self-test passed "
          f"(developer/0001 → {len(order)} quests, rotation deterministic; "
          f"--priority → {pslug}, --all-paths → {len(aslugs)} slices; "
          f"degradation-to-rotation verified offline).")
    return 0


# --- CLI -------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="Deterministic planner for the quest-walkthrough routine.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--character", help="Character path key (e.g. developer). Default: date-rotated.")
    p.add_argument("--level", help="Binary level code (e.g. 0001). Default: date-rotated.")
    p.add_argument("--date", help="ISO date (YYYY-MM-DD) used to rotate the slice. Default: today.")
    p.add_argument("--max-quests", type=int, default=0,
                   help="Hard first-N cap on the chain (0 = no cap). Bounds a long "
                        "walkthrough; the run only ever sees the first N quests.")
    p.add_argument("--window", type=int, default=0,
                   help="Walk a date-ROTATED window of N quests instead of a first-N "
                        "cap (the perfection loop). Over ceil(total/N) days the whole "
                        "level is swept; the ledger accumulates coverage across runs. "
                        "Rotated by --date. Takes precedence over --max-quests.")
    p.add_argument("--priority", action="store_true",
                   help="Ledger SELECTION: plan the worst/oldest not-perfect slice "
                        "(falls back to date-rotation if the ledger is absent/cold).")
    p.add_argument("--all-paths", action="store_true",
                   help="Ledger SELECTION: one slice per character. Writes "
                        "plans/walk-plan-<char>-<code>.json into --out-dir and prints "
                        "a JSON list of '<char>/<code>' slugs to stdout.")
    p.add_argument("--ledger", default=str(DEFAULT_LEDGER),
                   help="Path to the ledger consulted by --priority/--all-paths "
                        "(default .quests/ledger.json).")
    p.add_argument("--out-dir",
                   help="Output directory for --all-paths plans (plans/ subdir is created).")
    p.add_argument("--json", help="Write the plan as JSON to this file ('-' for stdout).")
    p.add_argument("--list", action="store_true",
                   help="List characters and their levels, then exit.")
    p.add_argument("--selftest", action="store_true",
                   help="Run the offline self-check against the live data, then exit.")
    args = p.parse_args()

    if args.selftest:
        return _selftest()

    paths = load_paths()

    if args.list:
        for c in paths:
            print(f"{c['icon']} {c['key']:<20} {c['name']}")
            for lv in c.get("levels", []):
                print(f"     {lv}  {reg.theme_of(lv)} ({reg.tier_of(lv)})")
        return 0

    network = load_network()
    on = _date.fromisoformat(args.date) if args.date else _date.today()
    ledger_path = Path(args.ledger)

    # --all-paths: fan SELECTION across every character. One slice per path
    # (ledger oracle, per-character rotation fallback), each planned and written
    # as plans/walk-plan-<char>-<code>.json under --out-dir; stdout gets the
    # JSON list of chosen "<char>/<code>" slugs (skipping empty slices). Explicit
    # --character/--level still win over this (handled below), so guard for them.
    if args.all_paths and not (args.character or args.level):
        # --out-dir IS the plans directory (the orchestrator passes --out-dir plans
        # and then looks in plans/walk-plan-<char>-<code>.json — no extra subdir).
        plans_dir = Path(args.out_dir) if args.out_dir else Path.cwd()
        plans_dir.mkdir(parents=True, exist_ok=True)
        chosen: List[str] = []
        for slug in select_all_paths_slugs(paths, on, ledger_path):
            character, level = resolve_slug(paths, slug)
            plan = build_plan(character, level, network,
                              max_quests=args.max_quests,
                              window=args.window, window_on=on)
            print(render_text(plan), file=sys.stderr)
            if not plan["quests"]:
                continue  # empty slice (sparse/all-codex level): nothing to walk
            dest = plans_dir / f"walk-plan-{character.get('key')}-{level}.json"
            dest.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
            print(f"\n📄 Plan → {dest}", file=sys.stderr)
            chosen.append(f"{character.get('key')}/{level}")
        print(json.dumps(chosen, ensure_ascii=False))
        return 0

    # Resolve the (character, level) slice: explicit args win; then --priority
    # SELECTION (ledger oracle, rotation fallback); otherwise rotate (default).
    if args.character and args.level:
        character = resolve_character(paths, args.character)
        level = args.level
    elif args.character:
        character = resolve_character(paths, args.character)
        _, level = rotate_slice([character], on)
    elif args.level:
        character, _ = rotate_slice(paths, on)
        level = args.level
    elif args.priority:
        character, level = resolve_slug(paths, select_priority_slug(paths, on, ledger_path))
    else:
        character, level = rotate_slice(paths, on)

    plan = build_plan(character, level, network, max_quests=args.max_quests,
                      window=args.window, window_on=on)

    print(render_text(plan), file=sys.stderr)
    if args.json:
        out = json.dumps(plan, indent=2, ensure_ascii=False)
        if args.json == "-":
            print(out)
        else:
            Path(args.json).write_text(out + "\n", encoding="utf-8")
            print(f"\n📄 Plan → {args.json}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
