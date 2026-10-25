# it-journey tools

> Operator scripts for this repository — the prose and docs generators, the docs index and the git hooks; nothing here ships to users.

| Where | What |
| --- | --- |
| [`hooks/`](hooks/) | `pre-commit` (one-paragraph-per-line on staged markdown, installed by `make hooks-install`) and `unwrap-md-hook.sh` (the same rule as a Claude Code PostToolUse hook) |
| [`unwrap-prose.py`](unwrap-prose.py) | unwrap-prose.py — join soft-wrapped prose lines so each paragraph is one line (vendored from the bamr87 hub; do not edit here) |
| [`docs_index.py`](docs_index.py) | docs_index.py — generate the `docs/README.md` index from each document's summary line (vendored byte-identical from the bamr87 hub; do not edit here) |
| [`gen_reference.py`](gen_reference.py) | gen_reference.py — generate `docs/reference/` (workflow and make-target references) from the workflow files and the Makefile |

`make docs` runs both generators; `make docs-check` fails when either output is stale.
