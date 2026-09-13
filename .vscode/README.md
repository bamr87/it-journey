# .vscode — the fleet run/debug convention

Every repo in the bamr87 workspace carries the same four files, so the task picker and the Run & Debug panel look the same wherever you are. Convention `fleet-vscode/v1 · 2026-09-09`.

| File | Holds | Rule |
|---|---|---|
| `tasks.json` | **Running** things: serve, build, verify, lint, test, plus this repo's extras | Every command delegates to the script, Make target, or npm script CI runs, so a button cannot drift from the gate. The `detail` line says whether it needs Docker or the host toolchain, and what it writes. |
| `launch.json` | **Debugging** things: a real debugger attached (browser, node, python, extension host) | Never a shell launcher. A config that needs a server names the `Serve` task as its `preLaunchTask`. |
| `settings.json` | Repo-scoped settings only: file associations, excludes, schemas, spell words | Personal editor preferences (font, autosave, minimap) live in the fleet workspace file (`zer0-CMS.code-workspace`), not here. |
| `extensions.json` | The fleet core set plus this repo's stack | No theme or keymap recommendations. |

## The task vocabulary

| Label | Meaning | How to run |
|---|---|---|
| `Serve` | Start the dev server; stays up until `Stop` | Terminal → Run Task |
| `Stop` | Tear the dev server down | Terminal → Run Task |
| `Build` | One production-parity build | ⇧⌘B (the default build task) |
| `Verify` | The gate CI enforces, run locally | Terminal → Run Test Task (the default test task) |
| `Lint` | The fast checks, no build | Terminal → Run Task |
| `Test` | Unit or tier tests where they differ from `Verify` | Terminal → Run Task |
| `Claude: session` | `claude` in this repo, with its agents and skills | Terminal → Run Task |
| `Area: thing` | Repo extras (`Release: …`, `Quest: …`, `Preview images: …`) | Terminal → Run Task |

A label is present only where it applies (a Python tool has no `Serve`). Launch configs are named `Debug: <what> (<where>)`; F5 runs the first one, the site in Edge on top of `Serve`. Change a config's `type` from `msedge` to `chrome` to use Chrome instead. In the multi-root workspace every entry is suffixed with its folder name, so the same label across repos stays unambiguous.

## Docker

The Jekyll repos build only in Docker on this host (the host Ruby is newer than the github-pages gem supports). Docker Desktop must be running, and `docker info` hangs rather than errors when it is down, so a task that sits silent means: start Docker first. Every task uses `docker compose` (v2), never `docker-compose`. Stopping a debug session does not stop `Serve`; run `Stop` when you are done.
