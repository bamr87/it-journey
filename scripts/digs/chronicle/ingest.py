"""Read every commit once and file its facts in the ledger.

One ``git log`` pass over the commits the ledger has not seen yet, with
``--raw`` (blob ids, statuses, renames) and ``--numstat`` (line deltas), merges
diffed against their first parent. A second batch call reads the size of each
new blob. Nothing is inferred: a record is what Git stores, plus the
deterministic readings in ``facts.py``.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from core import Ledger, git, now_iso
from facts import actor, conventional, summarize_files

FIELDS = ("H", "P", "an", "ae", "aI", "cn", "cI", "s", "b")
FORMAT = "%x1e" + "%x1f".join("%" + f for f in FIELDS)
NUMSTAT = re.compile(rb"^(\d+|-)\t(\d+|-)\t(.*)$", re.S)
BODY_CAP = 1500
BATCH = 400


def _num(v: bytes) -> int | None:
    return None if v == b"-" else int(v)


def parse_log(raw: bytes) -> list[dict]:
    """Parse ``git log -z --raw --numstat`` output produced with ``FORMAT``."""
    commits = []
    for chunk in raw.split(b"\x1e"):
        if not chunk.strip(b"\0\n"):
            continue
        head, _, rest = chunk.partition(b"\0")
        parts = head.decode("utf-8", errors="replace").split("\x1f")
        if len(parts) < len(FIELDS):
            parts += [""] * (len(FIELDS) - len(parts))
        meta = dict(zip(FIELDS, parts))
        toks = [t.lstrip(b"\n") for t in rest.split(b"\0")]
        raws, nums, i = [], [], 0
        while i < len(toks):
            t = toks[i]
            i += 1
            if not t:
                continue
            if t.startswith(b":"):
                f = t[1:].split(b" ")
                status = f[4].decode()
                if status[0] in "RC":
                    old, new = toks[i].decode("utf-8", "replace"), toks[i + 1].decode("utf-8", "replace")
                    i += 2
                else:
                    old, new = None, toks[i].decode("utf-8", "replace")
                    i += 1
                raws.append({"s": status, "p": new, "o": old, "m": f[1].decode(), "blob": f[3].decode()})
                continue
            m = NUMSTAT.match(t)
            if m:
                a, d, path = _num(m.group(1)), _num(m.group(2)), m.group(3)
                if not path:  # rename: old and new follow as separate tokens
                    path = toks[i + 1]
                    i += 2
                nums.append((a, d, path.decode("utf-8", "replace")))
        files = []
        for k, r in enumerate(raws):
            a, d = (nums[k][0], nums[k][1]) if k < len(nums) and nums[k][2] == r["p"] else _lookup(nums, r["p"])
            files.append({**r, "a": a, "d": d})
        commits.append({"meta": meta, "files": files})
    return commits


def _lookup(nums, path):
    for a, d, p in nums:
        if p == path:
            return a, d
    return None, None


def blob_sizes(repo: Path, blobs: set[str]) -> dict[str, int]:
    if not blobs:
        return {}
    out = git(repo, "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)",
              input_bytes=("\n".join(sorted(blobs)) + "\n").encode())
    sizes = {}
    for line in out.decode().splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[1] == "blob":
            sizes[parts[0]] = int(parts[2])
    return sizes


def build_record(c: dict, sizes: dict[str, int], mainline: set[str]) -> dict:
    m = c["meta"]
    files = []
    for f in c["files"]:
        rec = {"s": f["s"][0], "p": f["p"]}
        if f["o"]:
            rec["o"] = f["o"]
        if f["s"][0] in "RC":
            rec["sim"] = int(f["s"][1:] or 0)
        rec["a"], rec["d"] = f["a"], f["d"]
        if f["m"] == "160000":
            rec["sub"] = True
        elif f["s"][0] != "D":
            rec["b"] = sizes.get(f["blob"])
        files.append(rec)
    body = (m["b"] or "").strip()
    rec = {
        "sha": m["H"],
        "parents": m["P"].split() if m["P"] else [],
        "author": m["an"],
        "author_id": hashlib.sha1(m["ae"].strip().lower().encode()).hexdigest()[:10],
        "committer": m["cn"],
        "at": m["aI"],
        "ct": m["cI"],
        "subject": m["s"],
        "body": body[:BODY_CAP] + ("…" if len(body) > BODY_CAP else ""),
        "mainline": m["H"] in mainline,
        "files": files,
        "totals": {
            "files": len(files),
            "add": sum(f["a"] or 0 for f in files),
            "del": sum(f["d"] or 0 for f in files),
        },
        "facts": {"actor": actor(m["an"], m["cn"], body), **summarize_files(files)},
    }
    conv = conventional(m["s"])
    if conv:
        rec["facts"]["conventional"] = conv
    return rec


def ingest(repo: Path, ledger: Ledger, ref: str, log=print) -> dict:
    """File every commit reachable from ``ref`` that the ledger lacks."""
    head = git(repo, "rev-parse", ref + "^{commit}").decode().strip()
    reachable = git(repo, "rev-list", ref).decode().split()
    mainline = set(git(repo, "rev-list", "--first-parent", ref).decode().split())
    known = set(ledger.commits())
    todo = [s for s in reversed(reachable) if s not in known]
    log(f"[ingest] {ledger.slug}: {len(reachable)} reachable, {len(known)} already filed, {len(todo)} to read")
    added = 0
    for start in range(0, len(todo), BATCH):
        batch = todo[start:start + BATCH]
        raw = git(repo, "log", "--no-walk=unsorted", "--stdin", "-z", "--raw", "--numstat", "-M", "--root",
                  "--diff-merges=first-parent", "--no-abbrev", f"--format={FORMAT}",
                  input_bytes=("\n".join(batch) + "\n").encode())
        parsed = parse_log(raw)
        blobs = {f["blob"] for c in parsed for f in c["files"]
                 if f["s"][0] != "D" and f["m"] != "160000" and not f["blob"].startswith("0000000")}
        sizes = blob_sizes(repo, blobs)
        added += ledger.add_commits([build_record(c, sizes, mainline) for c in parsed])
        log(f"[ingest]   {min(start + BATCH, len(todo))}/{len(todo)}")
    tags = {}
    for line in git(repo, "for-each-ref", "refs/tags",
                    "--format=%(refname:short)\t%(*objectname)\t%(objectname)").decode().splitlines():
        name, peeled, obj = (line.split("\t") + ["", ""])[:3]
        tags[name] = peeled or obj
    man = ledger.manifest()
    if added or man.get("head") != head or man.get("tags") != tags:
        man.update({"ref": ref, "head": head, "commits": len(known) + added,
                    "mainline": len(mainline), "tags": tags})
        man.setdefault("runs", []).append({"at": now_iso(), "step": "ingest", "head": head, "added": added})
        ledger.save_manifest(man)
    return {"added": added, "head": head, "reachable": len(reachable)}
