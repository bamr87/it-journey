#!/usr/bin/env python3
"""mcp_server.py — serve the IT-Journey quest system over the Model Context Protocol.

An agent asked to *execute* a quest campaign needs the campaign's method, not a
web page. This is a stdio MCP server that hands an agent exactly that: the
campaign map, each chapter's objectives and procedure, the runnable snippets,
the canonical glossary, and full-text search across the corpus.

Transport is newline-delimited JSON-RPC 2.0 on stdin/stdout, per the MCP stdio
transport. Stdlib only — no SDK, no install step — so it runs anywhere the repo
is checked out and cannot drift from `quest_lib` (which it reuses, so the server
and the validators always agree about what a quest is).

  Wire it into Claude Code:
    claude --mcp-config scripts/quest/mcp.json --strict-mcp-config -p "..."

  Drive it by hand (one JSON-RPC message per line):
    echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python3 scripts/quest/mcp_server.py

  Check it:
    python3 scripts/quest/mcp_server.py --self-test
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

import quest_lib as ql  # noqa: E402
import quest_registry as reg  # noqa: E402

SERVER_NAME = "it-journey-quests"
SERVER_VERSION = "1.0.0"
DEFAULT_PROTOCOL = "2025-06-18"

# A tool result larger than this is truncated with an explicit marker, so a
# single fat quest can never blow an agent's context without telling it.
MAX_CHARS = 60_000


# ─────────────────────────────────────────────────────────────────────────────
# Corpus access (thin layer over quest_lib so this can never disagree with CI)
# ─────────────────────────────────────────────────────────────────────────────

_CACHE: Dict[str, Any] = {}


def _all_quests() -> List[ql.QuestDoc]:
    if "quests" not in _CACHE:
        _CACHE["quests"] = [d for d in ql.load_quests(quests_only=True) if not d.fm_error]
    return _CACHE["quests"]


def _codex_docs() -> List[ql.QuestDoc]:
    """Codex pages (glossary, world map, epic hubs) — not all carry fmContentType: quest."""
    if "codex" not in _CACHE:
        out = []
        codex_dir = ql.QUESTS_DIR / "codex"
        if codex_dir.is_dir():
            for p in sorted(codex_dir.glob("*.md")):
                doc = ql.read_quest(p)
                if not doc.fm_error:
                    out.append(doc)
        _CACHE["codex"] = out
    return _CACHE["codex"]


def _find(ident: str) -> Optional[ql.QuestDoc]:
    """Resolve a quest by slug, permalink, title, or repo-relative path."""
    needle = (ident or "").strip().lower().rstrip("/")
    if not needle:
        return None
    for doc in _all_quests() + _codex_docs():
        candidates = {
            doc.slug.lower(),
            doc.permalink.lower().rstrip("/"),
            doc.title.lower(),
            doc.rel_path.lower(),
            doc.path.stem.lower(),
        }
        if needle in candidates:
            return doc
        # permalink given without the leading slash, or slug with the level prefix
        if doc.permalink and needle == doc.permalink.lower().strip("/"):
            return doc
    return None


def _chapters_of(hub: ql.QuestDoc) -> List[ql.QuestDoc]:
    """A campaign's chapters, in the hub's own declared unlock order."""
    deps = hub.fm.get("quest_dependencies") or {}
    order = deps.get("unlocks_quests") or []
    by_permalink = {d.permalink.rstrip("/"): d for d in _all_quests() if d.permalink}
    out: List[ql.QuestDoc] = []
    for link in order:
        link = str(link).split("#")[0].strip().rstrip("/")
        doc = by_permalink.get(link)
        if doc is not None:
            out.append(doc)
    if out:
        return out
    # Fall back to quest_series when a hub predates the dependency convention.
    series = hub.fm.get("quest_series")
    if series:
        return sorted(
            (d for d in _all_quests() if d.fm.get("quest_series") == series and d.path != hub.path),
            key=lambda d: d.slug,
        )
    return []


def _objectives(body: str) -> List[str]:
    """The `- [ ]` checkboxes under the Quest Objectives heading."""
    out: List[str] = []
    in_section = False
    for line in body.splitlines():
        if re.match(r"^##\s", line):
            in_section = bool(re.search(r"Quest Objectives", line, re.I))
            continue
        if in_section:
            m = re.match(r"^\s*-\s*\[[ xX]\]\s*(.+)$", line)
            if m:
                out.append(re.sub(r"\*\*(.+?)\*\*", r"\1", m.group(1)).strip())
    return out


def _headings(body: str) -> List[str]:
    return [re.sub(r"^#+\s*", "", l).strip() for l in body.splitlines() if re.match(r"^##\s", l)]


def _section(body: str, name: str) -> Optional[str]:
    """Return one `## `-delimited section by (case-insensitive, emoji-tolerant) name."""
    needle = re.sub(r"[^a-z0-9 ]+", "", name.lower()).strip()
    lines = body.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s", line):
            title = re.sub(r"[^a-z0-9 ]+", "", re.sub(r"^#+\s*", "", line).lower()).strip()
            if start is not None:
                return "\n".join(lines[start:i]).strip()
            if needle and needle in title:
                start = i
    if start is not None:
        return "\n".join(lines[start:]).strip()
    return None


def _clip(text: str) -> str:
    if len(text) <= MAX_CHARS:
        return text
    return text[:MAX_CHARS] + f"\n\n…[truncated at {MAX_CHARS} chars — request a specific section]"


# ─────────────────────────────────────────────────────────────────────────────
# Tools
# ─────────────────────────────────────────────────────────────────────────────

def tool_list_campaigns(_: Dict) -> str:
    rows = []
    for doc in _codex_docs() + _all_quests():
        if doc.quest_type != "epic_quest":
            continue
        chapters = _chapters_of(doc)
        rows.append({
            "slug": doc.slug,
            "title": doc.title,
            "permalink": doc.permalink,
            "difficulty": doc.fm.get("difficulty", ""),
            "estimated_time": doc.fm.get("estimated_time", ""),
            "chapters": len(chapters),
            "description": doc.fm.get("description", ""),
        })
    rows.sort(key=lambda r: r["slug"])
    return json.dumps({"campaigns": rows}, indent=2)


def tool_get_campaign(args: Dict) -> str:
    hub = _find(args.get("campaign", ""))
    if hub is None:
        return json.dumps({"error": f"no campaign matches {args.get('campaign')!r}",
                           "hint": "call list_campaigns for valid slugs"})
    chapters = []
    for i, doc in enumerate(_chapters_of(hub), start=1):
        chapters.append({
            "n": i,
            "slug": doc.slug,
            "title": doc.title,
            "level": doc.level,
            "difficulty": doc.fm.get("difficulty", ""),
            "permalink": doc.permalink,
            "objectives": _objectives(doc.body),
            "sections": _headings(doc.body),
        })
    return _clip(json.dumps({
        "slug": hub.slug,
        "title": hub.title,
        "permalink": hub.permalink,
        "description": hub.fm.get("description", ""),
        "objectives": _objectives(hub.body),
        "chapters": chapters,
    }, indent=2))


def tool_get_quest(args: Dict) -> str:
    doc = _find(args.get("quest", ""))
    if doc is None:
        return json.dumps({"error": f"no quest matches {args.get('quest')!r}",
                           "hint": "call search_quests or list_campaigns"})
    section = args.get("section")
    if section:
        found = _section(doc.body, section)
        if found is None:
            return json.dumps({"error": f"no section matching {section!r}",
                               "available_sections": _headings(doc.body)})
        return _clip(found)
    return _clip(f"# {doc.title}\n\n{doc.body.strip()}")


def tool_get_method(args: Dict) -> str:
    """The campaign distilled to what an agent must DO: per chapter, the
    objectives and the runnable snippets, with prose stripped out."""
    hub = _find(args.get("campaign", ""))
    if hub is None:
        return json.dumps({"error": f"no campaign matches {args.get('campaign')!r}"})
    steps = []
    for i, doc in enumerate(_chapters_of(hub), start=1):
        snippets = [
            {"lang": b.lang, "code": b.code.strip()}
            for b in ql.runnable_snippets(doc.body)
        ]
        steps.append({
            "chapter": i,
            "title": doc.title,
            "level": doc.level,
            "objectives": _objectives(doc.body),
            "sections": _headings(doc.body),
            "runnable_snippets": snippets,
        })
    return _clip(json.dumps({
        "campaign": hub.title,
        "method": "Execute the chapters in order. Every claim about the relic is a "
                  "hypothesis until the relic itself testifies: run it, diff it, "
                  "reconcile it. Never record a conclusion you did not verify.",
        "chapters": steps,
    }, indent=2))


def tool_search_quests(args: Dict) -> str:
    q = (args.get("query") or "").strip().lower()
    if not q:
        return json.dumps({"error": "query is required"})
    limit = int(args.get("limit") or 10)
    hits = []
    for doc in _all_quests() + _codex_docs():
        hay = (doc.title + "\n" + doc.body).lower()
        n = hay.count(q)
        if n:
            idx = hay.find(q)
            hits.append({
                "slug": doc.slug,
                "title": doc.title,
                "permalink": doc.permalink,
                "level": doc.level,
                "hits": n,
                "context": doc.body[max(0, idx - 120): idx + 200].replace("\n", " ").strip(),
            })
    hits.sort(key=lambda h: -h["hits"])
    return json.dumps({"query": q, "matches": len(hits), "results": hits[:limit]}, indent=2)


def tool_get_glossary(args: Dict) -> str:
    doc = _find("glossary")
    if doc is None:
        return json.dumps({"error": "glossary not found in the corpus"})
    term = (args.get("term") or "").strip().lower()
    if not term:
        return _clip(doc.body)
    rows = [l for l in doc.body.splitlines() if l.startswith("|") and term in l.lower()]
    if not rows:
        return json.dumps({"error": f"no glossary entry matching {term!r}"})
    return "\n".join(["| Fantasy | In the mortal world | Field notes |", "|---|---|---|"] + rows)


TOOLS = [
    {
        "name": "list_campaigns",
        "description": "List the epic-quest campaigns in the IT-Journey corpus, with chapter counts. Start here.",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": tool_list_campaigns,
    },
    {
        "name": "get_campaign",
        "description": "Get one campaign: its objectives plus every chapter in order, with each chapter's objectives and section headings.",
        "inputSchema": {
            "type": "object",
            "properties": {"campaign": {"type": "string", "description": "campaign slug, title, or permalink"}},
            "required": ["campaign"],
        },
        "handler": tool_get_campaign,
    },
    {
        "name": "get_quest",
        "description": "Get the full text of one quest chapter, or a single named section of it (e.g. 'Quest Objectives', 'Mastery Challenge').",
        "inputSchema": {
            "type": "object",
            "properties": {
                "quest": {"type": "string", "description": "quest slug, title, or permalink"},
                "section": {"type": "string", "description": "optional section heading to return alone"},
            },
            "required": ["quest"],
        },
        "handler": tool_get_quest,
    },
    {
        "name": "get_method",
        "description": "The campaign distilled into an executable method: per chapter, the objectives and every runnable code snippet, prose stripped. Use this to DO a campaign rather than read it.",
        "inputSchema": {
            "type": "object",
            "properties": {"campaign": {"type": "string", "description": "campaign slug, title, or permalink"}},
            "required": ["campaign"],
        },
        "handler": tool_get_method,
    },
    {
        "name": "search_quests",
        "description": "Full-text search across every quest and codex page. Returns ranked hits with surrounding context.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "description": "max results (default 10)"},
            },
            "required": ["query"],
        },
        "handler": tool_search_quests,
    },
    {
        "name": "get_glossary",
        "description": "The canonical fantasy-to-technical lexicon. Pass a term to get matching entries only; omit it for the whole codex.",
        "inputSchema": {
            "type": "object",
            "properties": {"term": {"type": "string", "description": "optional term filter"}},
        },
        "handler": tool_get_glossary,
    },
]

BY_NAME = {t["name"]: t for t in TOOLS}


# ─────────────────────────────────────────────────────────────────────────────
# JSON-RPC 2.0 over stdio
# ─────────────────────────────────────────────────────────────────────────────

def _result(msg_id: Any, payload: Dict) -> Dict:
    return {"jsonrpc": "2.0", "id": msg_id, "result": payload}


def _error(msg_id: Any, code: int, message: str) -> Dict:
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}


def _audit(name: str, args: Dict) -> None:
    """Append one line per served call when QUEST_MCP_LOG names a file.

    Off unless the variable is set. A harness that wants to *prove* an agent
    consulted the quest — rather than assume it — reads this log; without it,
    a server that silently serves nothing is indistinguishable from one the
    agent never called.
    """
    path = os.environ.get("QUEST_MCP_LOG")
    if not path:
        return
    try:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "ts": datetime.now(timezone.utc).isoformat(),
                "tool": name,
                "args": {k: str(v)[:120] for k, v in sorted(args.items())},
            }) + "\n")
    except OSError:
        pass  # auditing must never break the server


def handle(msg: Dict) -> Optional[Dict]:
    """Handle one JSON-RPC message. Returns None for notifications."""
    method = msg.get("method")
    msg_id = msg.get("id")
    params = msg.get("params") or {}

    if method == "initialize":
        requested = params.get("protocolVersion") or DEFAULT_PROTOCOL
        return _result(msg_id, {
            "protocolVersion": requested,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
        })

    if method in ("notifications/initialized", "initialized", "notifications/cancelled"):
        return None

    if method == "ping":
        return _result(msg_id, {})

    if method == "tools/list":
        return _result(msg_id, {
            "tools": [{k: t[k] for k in ("name", "description", "inputSchema")} for t in TOOLS]
        })

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        tool = BY_NAME.get(name)
        if tool is None:
            return _result(msg_id, {
                "content": [{"type": "text", "text": f"unknown tool {name!r}; available: {sorted(BY_NAME)}"}],
                "isError": True,
            })
        # Say what is missing. A client that guesses a parameter name otherwise gets
        # a confusing semantic error ("no campaign matches None") instead of being
        # told which argument it failed to supply.
        required = tool["inputSchema"].get("required") or []
        absent = [r for r in required if args.get(r) in (None, "")]
        if absent:
            return _result(msg_id, {
                "content": [{"type": "text", "text": json.dumps({
                    "error": f"missing required argument(s): {', '.join(absent)}",
                    "expected": sorted(tool["inputSchema"].get("properties", {})),
                })}],
                "isError": True,
            })
        try:
            text = tool["handler"](args)
        except Exception as exc:  # a broken tool must not kill the server
            return _result(msg_id, {
                "content": [{"type": "text", "text": f"{type(exc).__name__}: {exc}"}],
                "isError": True,
            })
        _audit(name, args)
        return _result(msg_id, {"content": [{"type": "text", "text": text}]})

    if msg_id is None:
        return None
    return _error(msg_id, -32601, f"method not found: {method}")


def serve() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            sys.stdout.write(json.dumps(_error(None, -32700, "parse error")) + "\n")
            sys.stdout.flush()
            continue
        reply = handle(msg)
        if reply is not None:
            sys.stdout.write(json.dumps(reply) + "\n")
            sys.stdout.flush()
    return 0


def _selftest() -> int:
    failures = []

    def check(label, cond, detail=""):
        if cond:
            print(f"  ok   {label}")
        else:
            print(f"  FAIL {label} {detail}")
            failures.append(label)

    print("mcp_server self-test")
    init = handle({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": "2025-06-18"}})
    check("initialize returns serverInfo", init["result"]["serverInfo"]["name"] == SERVER_NAME)
    check("initialize echoes the protocol version", init["result"]["protocolVersion"] == "2025-06-18")
    check("initialized notification gets no reply",
          handle({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None)

    tools = handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})["result"]["tools"]
    check("tools/list returns every tool", len(tools) == len(TOOLS), f"got {len(tools)}")
    check("every tool has a schema", all("inputSchema" in t for t in tools))

    camps = json.loads(_call("list_campaigns", {}))
    check("list_campaigns finds campaigns", len(camps["campaigns"]) > 0, f"got {camps}")
    slugs = [c["slug"] for c in camps["campaigns"]]
    check("every campaign resolves chapters",
          all(c["chapters"] > 0 for c in camps["campaigns"]),
          f"{[(c['slug'], c['chapters']) for c in camps['campaigns']]}")

    one = json.loads(_call("get_campaign", {"campaign": slugs[0]}))
    check("get_campaign returns ordered chapters", one["chapters"][0]["n"] == 1)
    check("chapters carry objectives", any(c["objectives"] for c in one["chapters"]))

    method = json.loads(_call("get_method", {"campaign": slugs[0]}))
    check("get_method returns runnable snippets",
          any(c["runnable_snippets"] for c in method["chapters"]))

    first_chapter = one["chapters"][0]["slug"]
    body = _call("get_quest", {"quest": first_chapter})
    check("get_quest returns a body", len(body) > 500, f"got {len(body)} chars")
    sect = _call("get_quest", {"quest": first_chapter, "section": "Quest Objectives"})
    check("get_quest returns one section", "Quest Objectives" in sect and len(sect) < len(body))

    search = json.loads(_call("search_quests", {"query": "reconcile", "limit": 3}))
    check("search finds hits", search["matches"] > 0, str(search)[:200])

    gloss = _call("get_glossary", {"term": "relic"})
    check("glossary filters by term", "Relic" in gloss or "relic" in gloss, gloss[:120])

    bad = handle({"jsonrpc": "2.0", "id": 9, "method": "tools/call",
                  "params": {"name": "nope", "arguments": {}}})
    check("unknown tool is an isError result, not a crash", bad["result"].get("isError") is True)
    missing = json.loads(_call("get_quest", {"quest": "definitely-not-a-quest"}))
    check("unknown quest returns a helpful error", "error" in missing)
    unknown = handle({"jsonrpc": "2.0", "id": 10, "method": "no/such/method"})
    check("unknown method returns JSON-RPC -32601", unknown["error"]["code"] == -32601)

    # A client that guesses a parameter name must be told what it got wrong, not
    # handed a semantic error about the resulting None.
    guessed = handle({"jsonrpc": "2.0", "id": 11, "method": "tools/call",
                      "params": {"name": "get_campaign", "arguments": {"slug": "x"}}})
    guessed_text = guessed["result"]["content"][0]["text"]
    check("a missing required argument names itself",
          guessed["result"].get("isError") is True
          and "missing required argument" in guessed_text
          and "campaign" in guessed_text)

    # The audit log is how a harness proves an agent consulted the quest rather
    # than assuming it, so it has to actually write when asked to.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "audit.jsonl"
        before = os.environ.get("QUEST_MCP_LOG")
        os.environ["QUEST_MCP_LOG"] = str(log)
        try:
            _call("list_campaigns", {})
            lines = log.read_text().splitlines() if log.exists() else []
        finally:
            if before is None:
                os.environ.pop("QUEST_MCP_LOG", None)
            else:
                os.environ["QUEST_MCP_LOG"] = before
    check("QUEST_MCP_LOG records one line per served call",
          len(lines) == 1 and json.loads(lines[0])["tool"] == "list_campaigns")
    check("auditing is off when QUEST_MCP_LOG is unset",
          os.environ.get("QUEST_MCP_LOG") is None)

    print(f"\n{len(failures)} failure(s)")
    return 1 if failures else 0


def _call(name: str, args: Dict) -> str:
    reply = handle({"jsonrpc": "2.0", "id": 99, "method": "tools/call",
                    "params": {"name": name, "arguments": args}})
    return reply["result"]["content"][0]["text"]


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(_selftest())
    if "--list-tools" in sys.argv:
        print(json.dumps([{k: t[k] for k in ("name", "description")} for t in TOOLS], indent=2))
        sys.exit(0)
    sys.exit(serve())
