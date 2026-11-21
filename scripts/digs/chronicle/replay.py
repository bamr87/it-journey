"""Rebuild the repository's file tree at any mainline commit from the ledger.

The mainline is the first-parent chain of the ledger's head. Each mainline
record is a diff against its first parent, so replaying them in order
reproduces the exact tree (paths, line counts, blob sizes) without asking Git
again. ``timeline`` samples that replay into frames for the presentation.
"""
from __future__ import annotations

import datetime as dt
from collections import defaultdict

from facts import LAYERS, area_of, classify_path


def mainline_order(commits: dict[str, dict], head: str) -> list[dict]:
    chain, sha = [], head
    seen = set()
    while sha and sha in commits and sha not in seen:
        seen.add(sha)
        row = commits[sha]
        chain.append(row)
        sha = row["parents"][0] if row["parents"] else None
    chain.reverse()
    return chain


def apply(state: dict[str, list], row: dict) -> None:
    """Apply one first-parent diff to ``state`` (path -> [lines, bytes, binary])."""
    for f in row["files"]:
        s, p = f["s"], f["p"]
        a, d = f.get("a"), f.get("d")
        binary = a is None and not f.get("sub")
        if s == "D":
            state.pop(p, None)
            continue
        if s in "RC" and f.get("o"):
            base = state.pop(f["o"], None) if s == "R" else state.get(f["o"])
            lines = (base[0] if base else 0)
        elif s == "A":
            lines = 0
        else:
            prev = state.get(p)
            lines = prev[0] if prev else 0
        if not binary:
            lines = max(0, lines + (a or 0) - (d or 0))
        else:
            lines = 0
        size = f.get("b")
        if size is None:
            prev = state.get(p)
            size = prev[1] if prev else 0
        state[p] = [lines, size, binary]


def tree_at(commits: dict[str, dict], head: str) -> dict[str, list]:
    state: dict[str, list] = {}
    for row in mainline_order(commits, head):
        apply(state, row)
    return state


def _week(iso: str) -> str:
    t = dt.datetime.fromisoformat(iso).astimezone(dt.timezone.utc).date()
    monday = t - dt.timedelta(days=t.weekday())
    return monday.isoformat()


def node_of(path: str, depth: int) -> str:
    parts = path.split("/")
    if len(parts) == 1:
        return "/"
    return "/".join(parts[:min(depth, len(parts) - 1)])


def timeline(commits: dict[str, dict], head: str, depth: int = 2, max_nodes: int = 160) -> dict:
    """Weekly frames of the mainline tree: directory nodes, languages, layers, totals.

    Each frame is the tree at the last mainline commit of a week that had one.
    Nodes are directories down to ``depth`` (root files collapse into ``/``);
    the node dictionary keeps the ``max_nodes`` largest by peak size, the rest
    of each top-level area folds into ``<area>/…``.
    """
    chain = mainline_order(commits, head)
    state: dict[str, list] = {}
    frames = []
    for i, row in enumerate(chain):
        apply(state, row)
        last_of_week = i == len(chain) - 1 or _week(chain[i + 1]["ct"]) != _week(row["ct"])
        if not last_of_week:
            continue
        nodes: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])
        langs: dict[str, int] = defaultdict(int)
        layers: dict[str, int] = defaultdict(int)
        layers_b: dict[str, int] = defaultdict(int)
        lines = size = 0
        for path, (ln, sz, binary) in state.items():
            n = nodes[node_of(path, depth)]
            n[0] += 1
            n[1] += ln
            n[2] += sz
            lang, layer = classify_path(path)
            langs[lang] += ln
            layers[layer] += ln
            layers_b[layer] += sz
            lines += ln
            size += sz
        frames.append({"week": _week(row["ct"]), "sha": row["sha"], "ct": row["ct"],
                       "files": len(state), "lines": lines, "bytes": size,
                       "nodes": dict(nodes), "langs": dict(langs), "layers": dict(layers),
                       "layers_b": dict(layers_b)})
    # node dictionary: keep the largest nodes by peak (lines + bytes/40 so assets count)
    peak: dict[str, float] = defaultdict(float)
    for fr in frames:
        for k, (n, ln, sz) in fr["nodes"].items():
            peak[k] = max(peak[k], ln + sz / 40)
    keep = set(sorted(peak, key=peak.get, reverse=True)[:max_nodes])
    names = sorted(keep | {area_of(k) + "/…" for k in peak if k not in keep})
    index = {n: i for i, n in enumerate(names)}
    lang_names = sorted({lang for fr in frames for lang in fr["langs"]})
    out_frames = []
    for fr in frames:
        packed: dict[int, list[int]] = {}
        for k, (n, ln, sz) in fr["nodes"].items():
            key = k if k in keep else area_of(k) + "/…"
            cell = packed.setdefault(index[key], [0, 0, 0])
            cell[0] += n
            cell[1] += ln
            cell[2] += sz
        out_frames.append({
            "week": fr["week"], "sha": fr["sha"], "files": fr["files"], "lines": fr["lines"], "bytes": fr["bytes"],
            "n": [[i, *v] for i, v in sorted(packed.items())],
            "langs": [fr["langs"].get(lang, 0) for lang in lang_names],
            "layers": [fr["layers"].get(layer, 0) for layer in LAYERS],
            "layersB": [fr["layers_b"].get(layer, 0) for layer in LAYERS],
        })
    return {"nodes": names, "langs": lang_names, "layers": list(LAYERS), "frames": out_frames}
