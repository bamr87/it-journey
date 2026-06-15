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

from . import schema

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
            "EXECUTION POLICY (execute mode):\n"
            "- You are in a disposable sandbox directory. You MAY run commands to verify the quest.\n"
            "- Run ONLY safe, self-contained commands: creating/editing files inside the sandbox, "
            "`git init`, language REPLs/one-liners, local builds, package help/version checks.\n"
            "- Do NOT: delete or modify anything outside the sandbox, run `sudo`, reformat disks, "
            "`rm -rf` outside cwd, send network requests that mutate remote state, or use real credentials.\n"
            "- For commands that are destructive, require secrets/paid services, take a very long time, "
            "or need hardware you lack: do NOT run them — mark them `reasoned` and judge correctness statically.\n"
            "- Record each command you tried in `commands` with an honest `passed`/`failed`/`skipped`/`reasoned` status.\n"
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


def build_user_prompt(quest, quest_file_name: str = "QUEST.md") -> str:
    meta = quest.to_meta()
    objectives = quest.objectives()
    obj_block = ""
    if objectives:
        obj_block = "\nStated objectives:\n" + "\n".join(f"  - {o}" for o in objectives)
    return (
        f"Review the quest in `./{quest_file_name}` (in your current directory).\n\n"
        f"Quest metadata:\n"
        f"  - Title: {meta['title']}\n"
        f"  - Level: {meta['level']}  ({meta['theme']})\n"
        f"  - Difficulty: {meta['difficulty'] or 'unspecified'}\n"
        f"  - Type: {meta['quest_type'] or 'unspecified'}\n"
        f"{obj_block}\n\n"
        f"Steps:\n"
        f"1. Read ./{quest_file_name} in full.\n"
        f"2. Walk through it as a learner would, in order.\n"
        f"3. Evaluate it against the dimensions, gathering concrete evidence.\n"
        f"4. Emit the single JSON verdict block per the schema. No prose after it."
    )
