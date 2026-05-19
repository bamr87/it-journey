---
applyTo: "scripts/**/*"
description: "Standards for scripts/: structure, naming, logging, README-First, and cross-platform safety"
date: 2025-11-19T22:51:22.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# `scripts/` Standards

Rules for every automation script in this repo. The full bash skeleton lives in [`../prompts/bash-it.prompt.md`](../prompts/bash-it.prompt.md); this file covers repo-level conventions only.

## 1. Directory Layout

```
scripts/
├── core/             # Environment, setup, bootstrap (rarely changes)
├── deployment/       # CI/CD, releases, publishing
├── development/      # Local dev helpers (content, link checks, generators)
├── monitoring/       # Health checks, metrics, reports
├── validation/       # Frontmatter, links, quest validators
├── lib/              # Shared shell modules sourced by other scripts
└── README.md         # Index of all scripts (see §6)
```

Pick the most specific subdirectory. Don't create a new top-level category without updating `scripts/README.md`.

## 2. Naming

| Convention | Example |
|---|---|
| Lower-case, hyphen-separated | `link-checker.py`, `generate-statistics.sh` |
| Verb-first for action scripts | `update-settings.sh`, `validate-quest.py` |
| Noun for libraries | `lib/common.sh`, `lib/git.sh` |
| Extension matches interpreter | `.sh`, `.bash`, `.py`, `.rb` |

## 3. Header Template

Every script starts with a header identifying purpose, usage, author, and date:

```bash
#!/usr/bin/env bash
# =====================================================================
# <name> — <one-line purpose>
# Usage:  ./<name> [options]
# Author: <author>          Created: YYYY-MM-DD
# =====================================================================
set -euo pipefail
IFS=$'\n\t'
```

Python equivalent:

```python
#!/usr/bin/env python3
"""<name> — <one-line purpose>

Usage: ./<name> [options]
"""
from __future__ import annotations
```

## 4. Mandatory Features

Every executable script must support:

- `--help` / `-h` — usage and examples
- `--version` / `-V` — semantic version
- `--dry-run` / `-n` — preview without side effects
- `--verbose` / `-v` — DEBUG-level logging
- Non-zero exit code on any failure
- A `trap` cleanup handler (bash) or `try/finally` (python)

## 5. Logging

- Log to `${LOG_DIR:-scripts/logs}/<script>-YYYYMMDD.log` **and** stderr.
- Levels: `DEBUG`, `INFO`, `WARN`, `ERROR`.
- Include a timestamp on every line.
- Never log secrets — redact tokens, passwords, API keys before writing.

Minimal bash logger:

```bash
log()   { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*" | tee -a "$LOG_FILE"; }
info()  { log "INFO  $*"; }
warn()  { log "WARN  $*" >&2; }
error() { log "ERROR $*" >&2; }
debug() { [[ "${VERBOSE:-false}" == true ]] && log "DEBUG $*"; }
```

## 6. README-First

Every script directory has a `README.md` listing every script with: filename, purpose, primary arguments, example invocation. See [`README.instructions.md`](README.instructions.md) §4 for the script-directory template.

When you add or modify a script, update that directory's README in the same commit.

## 7. Security Rules

- **Never hardcode secrets.** Read from env vars or a gitignored `.env`.
- **Validate all input.** Treat CLI args, env vars, and file contents as untrusted.
- **Quote all expansions:** `"$var"`, `"${arr[@]}"`. Never bare `$var`.
- **Never `eval`** user-controlled strings. Never `curl ... | bash` inside a script.
- **File operations:** check existence, confirm before overwrite, use `mktemp` for temp files, set restrictive `umask` (`077`) when writing secrets.
- **Subprocess in Python:** use `subprocess.run([...], check=True)` with a list, never `shell=True` with interpolation.

## 8. Cross-Platform Safety

- Target bash ≥ 3.2 (macOS default) or explicitly require ≥ 4 with `# requires bash >= 4` and a version check.
- Use `command -v` not `which`.
- Prefer `printf` over `echo -e`.
- Use `python3` not `python`.
- Avoid GNU-only flags (`sed -i ''` on macOS vs `sed -i` on Linux); use a small wrapper or `gsed`.

## 9. Python Scripts

- Python 3.10+ with type hints.
- Use `argparse` for CLI; one `main()` function; `if __name__ == "__main__": sys.exit(main())`.
- Use `pathlib.Path`, not `os.path` string concatenation.
- Use `logging` module; configure once in `main()`.
- Use `subprocess.run` with `check=True`, `capture_output=True`, `text=True`.
- Use `try/except` with specific exception types; never bare `except:`.

## 10. Testing Checklist

Before committing a new or modified script:

- [ ] `bash -n script.sh` (syntax)
- [ ] `shellcheck script.sh` (zero errors)
- [ ] `./script.sh --help` renders
- [ ] `./script.sh --dry-run --verbose` produces sane preview
- [ ] Idempotent: running twice produces the same result
- [ ] Tested on at least macOS or Linux (matches deployment target)
- [ ] Directory README updated
- [ ] Logs land in `scripts/logs/`, not the repo root

## 11. Commit Conventions

Use the standard repo conventions (see `.github/copilot-instructions.md`):

```
feat(scripts): add <thing>
fix(scripts): correct <bug> in <script>
docs(scripts): update README for <script>
refactor(scripts): extract <fn> into lib/common.sh
```

## 12. Generating New Scripts

Use the `/bash-it` prompt for non-trivial scripts — it enforces this entire contract automatically. See [`../prompts/bash-it.prompt.md`](../prompts/bash-it.prompt.md).

---

**Related:** [`work.instructions.md`](work.instructions.md) for `work/` layout · [`README.instructions.md`](README.instructions.md) for directory READMEs · [`features.instructions.md`](features.instructions.md) for CI integration.
