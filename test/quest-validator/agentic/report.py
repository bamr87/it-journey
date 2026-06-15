"""
Aggregation + rendering for agentic validation results (console / markdown / json).
"""

from __future__ import annotations

import json
from typing import List

from . import schema


def aggregate(results: List[dict]) -> dict:
    scored = [r for r in results if "error" not in r]
    errored = [r for r in results if "error" in r]
    counts = {schema.VERDICT_PASS: 0, schema.VERDICT_WARN: 0, schema.VERDICT_FAIL: 0}
    for r in results:
        counts[r.get("verdict", schema.VERDICT_FAIL)] = counts.get(r.get("verdict", schema.VERDICT_FAIL), 0) + 1
    avg = round(sum(r["overall"] for r in scored) / len(scored), 1) if scored else 0.0
    cost = sum((r.get("meta", {}).get("cost_usd") or 0.0) for r in results)
    return {
        "total": len(results), "scored": len(scored), "errored": len(errored),
        "average": avg, "counts": counts, "cost_usd": round(cost, 4),
        "results": results,
    }


# ---- console -----------------------------------------------------------

def render_console(agg: dict, verbose: bool = False) -> str:
    lines = []
    for r in agg["results"]:
        meta = r["quest"]
        emoji = schema.VERDICT_EMOJI.get(r.get("verdict"), "❓")
        head = f"{emoji} {r.get('overall', 0):5.1f}  {meta['title']}  ({meta['level']} · {meta['path']})"
        lines.append(head)
        if "error" in r:
            lines.append(f"      ⚠️  {r['error']}")
            continue
        v = r.get("verdict_obj") or {}
        per = r.get("per_dimension", {})
        dim_bits = "  ".join(
            f"{schema.DIM_LABELS[k].split(' ')[0].lower()}={per.get(k) if per.get(k) is not None else '-'}/5"
            for k in schema.DIM_KEYS
        )
        lines.append(f"      {dim_bits}   executed={v.get('executed')}")
        if v.get("summary"):
            lines.append(f"      {v['summary']}")
        recs = v.get("recommendations") or []
        if recs:
            shown = recs if verbose else recs[:3]
            for rec in shown:
                lines.append(f"        → [{rec.get('priority','?')}] {rec.get('area','')}: {rec.get('suggestion','')}")
            if not verbose and len(recs) > 3:
                lines.append(f"        … +{len(recs) - 3} more (use -v)")
        lines.append("")
    c = agg["counts"]
    lines.append("=" * 64)
    lines.append("AGENTIC VALIDATION SUMMARY")
    lines.append("=" * 64)
    lines.append(f"Quests evaluated: {agg['total']}   (scored {agg['scored']}, errored {agg['errored']})")
    lines.append(f"  {schema.VERDICT_EMOJI['pass']} pass {c.get('pass',0)}   "
                 f"{schema.VERDICT_EMOJI['warn']} warn {c.get('warn',0)}   "
                 f"{schema.VERDICT_EMOJI['fail']} fail {c.get('fail',0)}")
    lines.append(f"Average score: {agg['average']}%")
    if agg["cost_usd"]:
        lines.append(f"Estimated cost: ${agg['cost_usd']}")
    lines.append("=" * 64)
    return "\n".join(lines)


# ---- markdown (CI artifact / PR comment / job summary) -----------------

def render_markdown(agg: dict, title: str = "Agentic Quest Review") -> str:
    c = agg["counts"]
    out = [f"## 🤖 {title}", ""]
    out.append(f"**{agg['scored']}** quests evaluated · "
               f"{schema.VERDICT_EMOJI['pass']} {c.get('pass',0)} pass · "
               f"{schema.VERDICT_EMOJI['warn']} {c.get('warn',0)} warn · "
               f"{schema.VERDICT_EMOJI['fail']} {c.get('fail',0)} fail · "
               f"avg **{agg['average']}%**"
               + (f" · ~${agg['cost_usd']}" if agg["cost_usd"] else ""))
    out.append("")
    out.append("| | Score | Quest | Level | Executed | Summary |")
    out.append("|---|--:|---|---|:-:|---|")
    for r in agg["results"]:
        m = r["quest"]
        emoji = schema.VERDICT_EMOJI.get(r.get("verdict"), "❓")
        if "error" in r:
            out.append(f"| {emoji} | — | {m['title']} | {m['level']} | — | ⚠️ {r['error']} |")
            continue
        v = r.get("verdict_obj") or {}
        summ = (v.get("summary") or "").replace("|", "\\|").replace("\n", " ")
        out.append(f"| {emoji} | {r.get('overall',0):.0f} | {m['title']} | {m['level']} | "
                   f"{'yes' if v.get('executed') else 'no'} | {summ} |")
    out.append("")
    # Detailed recommendations for non-passing quests.
    flagged = [r for r in agg["results"]
               if "error" not in r and r.get("verdict") != schema.VERDICT_PASS
               and (r.get("verdict_obj") or {}).get("recommendations")]
    if flagged:
        out.append("<details><summary>Recommendations for flagged quests</summary>")
        out.append("")
        for r in flagged:
            m = r["quest"]
            out.append(f"**{m['title']}** (`{m['path']}`) — {r.get('overall',0):.0f}%")
            for rec in (r["verdict_obj"]["recommendations"]):
                out.append(f"- **{rec.get('priority','?')}** · {rec.get('area','')}: {rec.get('suggestion','')}")
            out.append("")
        out.append("</details>")
    return "\n".join(out)


def render_json(agg: dict) -> str:
    return json.dumps(agg, indent=2, ensure_ascii=False)
