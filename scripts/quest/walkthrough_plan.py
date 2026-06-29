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

    # List the characters / levels available, then exit:
    python3 scripts/quest/walkthrough_plan.py --list

    # Self-check (no network, no args): asserts the planner on the live data.
    python3 scripts/quest/walkthrough_plan.py --selftest

The plan is advisory structure, not a schema gate: a level with no quests degrades
to an empty `quests` list with a reason rather than failing, because the network
data is regenerated and can drift.
"""
from __future__ import annotations

import argparse
import json
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
               max_quests: int = 0) -> dict:
    """Resolve the linked playthrough plan for one (character, level) slice."""
    if not reg.is_valid_level(level):
        raise ValueError(f"invalid level '{level}' (expected a 4-bit code like 0001).")

    nodes = [n for n in network.get("nodes", [])
             if n.get("level") == level and n.get("type") in WALKABLE_TYPES]
    ordered = _order_links(nodes, network.get("edges", []))

    truncated = False
    if max_quests and max_quests > 0 and len(ordered) > max_quests:
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
            "truncated": truncated,
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
    if plan["stats"]["truncated"]:
        lines.append("\n   (list truncated by --max-quests)")
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

    print("✅ walkthrough_plan self-test passed "
          f"(developer/0001 → {len(order)} quests, rotation deterministic).")
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
                   help="Cap the chain to N quests (0 = no cap). Bounds a long walkthrough.")
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

    # Resolve the (character, level) slice: explicit args win; otherwise rotate.
    on = _date.fromisoformat(args.date) if args.date else _date.today()
    if args.character and args.level:
        character = resolve_character(paths, args.character)
        level = args.level
    elif args.character:
        character = resolve_character(paths, args.character)
        _, level = rotate_slice([character], on)
    elif args.level:
        character, _ = rotate_slice(paths, on)
        level = args.level
    else:
        character, level = rotate_slice(paths, on)

    plan = build_plan(character, level, network, max_quests=args.max_quests)

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
