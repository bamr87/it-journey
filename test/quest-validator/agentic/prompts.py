"""
Prompt construction for the agentic quest validator.

Two modes:
  * ``review``  — read-only. The agent reasons about the quest like an expert
                  reviewer + first-time learner, executing nothing. Safe anywhere.
  * ``execute`` — the agent may RUN the quest's safe, self-contained commands in
                  an isolated sandbox to verify they actually work. Intended for
                  disposable environments (CI runners / containers).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from . import schema

# Reuse the shared deterministic snippet extractor (single source of truth for
# "what is a runnable snippet"). loader already puts scripts/quest on the path,
# but insert defensively so prompts can be imported standalone.
_QUEST_DIR = Path(__file__).resolve().parents[3] / "scripts" / "quest"
if str(_QUEST_DIR) not in sys.path:
    sys.path.insert(0, str(_QUEST_DIR))
try:
    import quest_lib  # noqa: E402
except Exception:  # pragma: no cover - prompts still work without snippet inventory
    quest_lib = None

_DIM_BLOCK = "\n".join(
    f"  - {key} ({schema.DIM_LABELS[key]}, weight {int(schema.WEIGHTS[key] * 100)}%): {schema.DIM_GUIDANCE[key]}"
    for key in schema.DIM_KEYS
)

_OUTPUT_CONTRACT = (
    "When finished, output your verdict as a SINGLE fenced ```json code block and "
    "nothing after it. It MUST conform exactly to this JSON Schema:\n\n"
    "```json\n{schema}\n```\n\n"
    "Score each dimension 0-5 (0 = broken/absent, 3 = adequate, 5 = excellent). "
    "Do not compute an overall score yourself — the harness derives it from your "
    "dimension scores using the fixed weights above. Base every score on concrete "
    "evidence; cite specifics from the quest in `findings`."
)


def build_system_prompt(mode: str) -> str:
    schema_json = json.dumps(schema.build_json_schema(), indent=2)
    if mode == "execute":
        exec_rules = (
            "EXECUTION POLICY (execute mode — you actually RUN the quest's code):\n"
            "- You are in a disposable, isolated sandbox directory. Your PRIMARY job is to "
            "WORK THROUGH THE QUEST AS A LEARNER WOULD and ACTUALLY RUN its code snippets, in order, "
            "to verify they work — not just read them.\n"
            "- Go snippet by snippet. For EACH runnable code block (shell, python, node, ruby, sql, etc.): "
            "actually execute it in the sandbox, observe the real output, and record the outcome. Carry state "
            "forward between snippets (files you create, dirs you cd into) the way a learner following the quest would.\n"
            "- Run ONLY safe, self-contained commands: creating/editing files inside the sandbox, `git init`, "
            "language REPLs/one-liners, local builds, package help/version checks, installs into the sandbox.\n"
            "- Do NOT: delete or modify anything outside the sandbox, run `sudo`, reformat disks, `rm -rf` outside "
            "cwd, send network requests that mutate remote state, or use real credentials.\n"
            "- A snippet is legitimately NOT runnable here if it: is destructive, needs secrets/paid services or "
            "specific hardware/OS you lack, needs a tool that isn't installed and can't be safely installed, or "
            "takes very long. For those, mark `skipped` (tool/OS/secret missing) or `reasoned` (judged statically) "
            "with the reason — do NOT force it.\n"
            "- Record EVERY snippet you encountered in `commands`, in quest order, each with an honest "
            "`passed` (ran, worked) / `failed` (ran, broke) / `skipped` (couldn't safely run) / `reasoned` "
            "(judged without running) status and a `detail` (the real error/output, or why skipped).\n"
            "- A snippet that errors when a learner runs it as written is a `failed` command and should pull down "
            "the `commands_work` dimension — this is the single most valuable signal you produce.\n"
            "- Set `executed: true` in your verdict.\n"
        )
    else:
        exec_rules = (
            "EXECUTION POLICY (review mode):\n"
            "- Do NOT run any commands. Evaluate purely by close reading + your expertise.\n"
            "- For every command/snippet, decide whether it WOULD work as described and mark it `reasoned`.\n"
            "- Set `executed: false` in your verdict.\n"
        )
    return (
        "You are a meticulous senior technical-curriculum QA reviewer for IT-Journey, "
        "a gamified learn-to-code platform. You evaluate a single 'quest' (a tutorial) "
        "the way a careful expert AND a first-time learner would: does it actually work, "
        "is it accurate, is it complete, can it be followed?\n\n"
        f"{exec_rules}\n"
        "Evaluate these weighted dimensions:\n"
        f"{_DIM_BLOCK}\n\n"
        "Be specific and fair. Reward correct, runnable, well-sequenced content; penalize "
        "broken commands, wrong technical claims, missing steps, ambiguous instructions, and "
        "unwarned destructive operations. The fantasy/gamified framing is intentional — judge "
        "the technical substance underneath it, not the theme.\n\n"
        + _OUTPUT_CONTRACT.format(schema=schema_json)
    )


def _snippet_block(quest, mode: str) -> str:
    """A deterministic inventory of the quest's code snippets, so the agent has a
    concrete checklist of what to run (execute) or reason about (review)."""
    if quest_lib is None:
        return ""
    try:
        summary = quest_lib.snippet_summary(quest.body)
    except Exception:
        return ""
    if not summary["total"]:
        return "\nThis quest contains no fenced code blocks — assess its instructions and concepts.\n"
    by_lang = ", ".join(f"{k}×{v}" for k, v in summary["by_lang"].items())
    verb = "RUN each runnable one in the sandbox" if mode == "execute" else "judge whether each WOULD run"
    return (
        f"\nCode snippets (deterministic count): {summary['total']} fenced block(s), "
        f"{summary['runnable']} runnable [{by_lang}].\n"
        f"Treat these as a checklist — {verb}, and record every one in `commands` in quest order.\n"
    )


def build_user_prompt(quest, quest_file_name: str = "QUEST.md", mode: str = "review") -> str:
    meta = quest.to_meta()
    objectives = quest.objectives()
    obj_block = ""
    if objectives:
        obj_block = "\nStated objectives:\n" + "\n".join(f"  - {o}" for o in objectives)
    snippet_block = _snippet_block(quest, mode)
    if mode == "execute":
        steps = (
            f"1. Read ./{quest_file_name} in full.\n"
            f"2. Work through it as a learner would, in order, ACTUALLY RUNNING each runnable code "
            f"snippet in the sandbox and observing the real result (carry state forward between steps).\n"
            f"3. Evaluate it against the dimensions from the evidence you gathered by running it.\n"
            f"4. Record every snippet in `commands` (passed/failed/skipped/reasoned + detail), then emit "
            f"the single JSON verdict block per the schema. No prose after it."
        )
    else:
        steps = (
            f"1. Read ./{quest_file_name} in full.\n"
            f"2. Walk through it as a learner would, in order.\n"
            f"3. Evaluate it against the dimensions, gathering concrete evidence.\n"
            f"4. Emit the single JSON verdict block per the schema. No prose after it."
        )
    return (
        f"Review the quest in `./{quest_file_name}` (in your current directory).\n\n"
        f"Quest metadata:\n"
        f"  - Title: {meta['title']}\n"
        f"  - Level: {meta['level']}  ({meta['theme']})\n"
        f"  - Difficulty: {meta['difficulty'] or 'unspecified'}\n"
        f"  - Type: {meta['quest_type'] or 'unspecified'}\n"
        f"{obj_block}\n"
        f"{snippet_block}\n"
        f"Steps:\n"
        f"{steps}"
    )
