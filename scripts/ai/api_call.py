#!/usr/bin/env python3
"""
api_call.py — single-shot Claude API fallback for the universal AI runner.

scripts/ai/run.sh calls this ONLY when the Claude Code CLI is unavailable or
fails AND an ANTHROPIC_API_KEY is present. It produces one text completion (no
tools, no file edits) — a graceful degradation of the full agent, not a
replacement for it. Model + budget come from _data/ai.yml; the actual HTTP is
delegated to the repo's existing scripts/lib/ai_client.py so provider wiring
lives in one place.

Usage:
    python3 scripts/ai/api_call.py --prompt "..." [--system "..."] [--model ...]

Exits 0 and prints the completion to stdout on success; exits 1 with the error
on stderr otherwise. Requires ANTHROPIC_API_KEY in the environment.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "scripts" / "lib"))


def _ai_config() -> dict:
    try:
        import yaml
        return yaml.safe_load((REPO / "_data" / "ai.yml").read_text()) or {}
    except Exception:
        return {}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Single-shot Claude API fallback.")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--system", default="")
    ap.add_argument("--model", default="")
    args = ap.parse_args(argv)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("[api_call] no ANTHROPIC_API_KEY — cannot run the API fallback.", file=sys.stderr)
        return 1

    cfg = _ai_config()
    model = args.model or os.environ.get("ITJ_AI_MODEL") or cfg.get("fallback_model") or cfg.get("model") or "claude-opus-4-8"
    max_tokens = int(cfg.get("max_tokens") or 8000)

    try:
        from ai_client import AIClient  # scripts/lib/ai_client.py
    except Exception as e:  # pragma: no cover - import guard
        print(f"[api_call] could not import ai_client: {e}", file=sys.stderr)
        return 1

    client = AIClient(provider="anthropic", model=model)
    result = client.chat(
        prompt=args.prompt,
        system=args.system or None,
        max_tokens=max_tokens,
        temperature=0.2,
    )
    if getattr(result, "success", False):
        sys.stdout.write(result.content or "")
        return 0
    print(f"[api_call] API error: {getattr(result, 'error', 'unknown')}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
