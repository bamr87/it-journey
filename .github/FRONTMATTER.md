<!--
description: Canonical frontmatter schema for AI agent instructions and prompts across bashconsultants, zer0-mistakes, and it-journey repositories. date: 2026-05-18T12:00:00.000Z lastmod: 2026-05-18T12:00:00.000Z -->

# Frontmatter Schema for AI Agent Files

This is the **canonical schema** for `.github/instructions/*.instructions.md` and `.github/prompts/*.prompt.md` files. It is shared across all three repositories (bashconsultants, zer0-mistakes, it-journey) so a single mental model applies everywhere.

## Why a schema?

VS Code Copilot, Cursor, Aider, Continue, Claude Code, and other AGENTS.md-aware tools read these files. Inconsistent frontmatter causes:

- Tooltips and pickers to show nothing useful.
- `applyTo` to silently match nothing.
- `lastmod` staleness audits to fail.
- Cross-repo prompt sharing to break.

## `.prompt.md` — canonical fields

```yaml
---
mode: agent                     # required — always "agent" for agent-mode prompts
description: "<= 160 chars"     # required — double-quoted, single line, shown in UI
tools: [tool1, tool2]           # optional — restricts which tools the prompt may invoke
date: 2025-MM-DDTHH:MM:SS.000Z  # required — original creation date (preserve when editing)
lastmod: 2026-05-18T12:00:00.000Z # required — bump on every meaningful edit
---
```

**Dropped legacy fields** (do not reintroduce): `agent`, `name`, `version`, `category`, `trigger`, `inputs`, `outputs`, `related_prompts`, `related_instructions`, `purpose`, `title`.

If you need to document inputs/outputs/related files, put them as Markdown sections in the body, not in YAML.

## `.instructions.md` — canonical fields

```yaml
---
applyTo: "glob1,glob2"            # required — comma-separated globs (no spaces) OR single-quoted single glob
description: "<= 160 chars"       # required — double-quoted, single line
date: 2025-MM-DDTHH:MM:SS.000Z    # required — original creation date
lastmod: 2026-05-18T12:00:00.000Z # required — bump on every meaningful edit
---
```

## Conventions

1. **Quoting**: always double-quote `description` and `applyTo`. Dates are unquoted ISO-8601.
2. **`lastmod`**: bump to today's date in ISO-8601 with milliseconds (`YYYY-MM-DDTHH:MM:SS.000Z`).
3. **`description` length**: hard limit 160 characters. Aim for 120–155. One sentence. No trailing period.
4. **`applyTo`**: prefer narrow globs. `**/*` should be reserved for genuinely repo-wide instructions (`contributing`, `work`).
5. **Filename = behavior**: `prompts/foo.prompt.md` becomes the `/foo` slash command. `instructions/bar.instructions.md` is auto-loaded when files match `applyTo`.
6. **One concern per file**. If a file covers two distinct domains, split it.

## Validating

Quick check that every file has the four required keys:

```bash
for f in .github/prompts/*.prompt.md; do
  for k in mode description date lastmod; do
    grep -q "^$k:" "$f" || echo "MISSING $k in $f"
  done
done

for f in .github/instructions/*.instructions.md; do
  for k in applyTo description date lastmod; do
    grep -q "^$k:" "$f" || echo "MISSING $k in $f"
  done
done
```

## Cross-repo links

The same `FRONTMATTER.md` lives in each repo's `.github/`. Keep the three copies in sync. When in doubt, the version in `zer0-mistakes` is the source of truth and changes there should be mirrored to `it-journey` and `bashconsultants`.
