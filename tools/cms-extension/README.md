# IT-Journey CMS — VS Code extension

AI-augmented content management for IT-Journey, embedded in VS Code. It reads the
`.cms/` contract this repo emits and adds:

- **Content view** (Activity Bar) — collections → files → issues, ranked by health.
- **Dashboard** — health summary by collection, worklist, and a live agent panel.
- **Curate with Claude** — runs the `cms-curator` skill via the Claude Agent SDK,
  with an **approve/deny diff card for every edit** before it touches disk.
- **Mechanical preview** — dry-run of the deterministic frontmatter normalizer.

This is the Phase 1–3 MVP of the design in
[`docs/cms/EXTENSION_DESIGN.md`](../../docs/cms/EXTENSION_DESIGN.md). It currently
lives in-repo (`tools/cms-extension/`) for fast iteration; it will graduate to its
own repo, still reading the same `.cms/` contract.

## Test it (F5)

Prereqs: Node ≥ 18, VS Code, and the CMS engine prereqs (`python3` + `pyyaml`).
For the **Curate** (agent) commands you also need a Claude credential the SDK can
use — log in with `claude` (Claude Code) or set `ANTHROPIC_API_KEY`.

```bash
cd tools/cms-extension
npm install
```

Then in VS Code:

1. **Open the `tools/cms-extension` folder** (File ▸ Open Folder).
2. Press **F5** ("Run Extension"). A second VS Code window (the *Extension
   Development Host*) opens with the `it-journey` repo loaded and the extension
   active.
3. Click the **IT-Journey CMS** icon in the Activity Bar.
4. **CMS: Refresh Index** (view title ↻) builds `.cms/` and populates the tree +
   dashboard. (No Claude needed for this — it's pure Python.)
5. **CMS: Open Dashboard** for the health summary and agent panel.
6. Right-click a file in the Content view → **Curate This File with Claude**, or
   click **✨ Curate worklist** in the dashboard. Approve/deny each edit as it
   streams in.

To try it as a real install instead of F5:

```bash
npm install -g @vscode/vsce
vsce package           # produces it-journey-cms-0.1.0.vsix
code --install-extension it-journey-cms-0.1.0.vsix
```

## Settings

| Setting | Default | Purpose |
|---|---|---|
| `itjCms.pythonPath` | `python3` | Interpreter for the CMS engine |
| `itjCms.model` | `claude-opus-4-8` | Model for the agent commands |
| `itjCms.permissionMode` | `default` | `default` = approve each edit; `acceptEdits` = auto; `plan` = read-only |
| `itjCms.maxTurns` | `40` | Safety cap per curate run |

## Architecture (maps to the design doc)

| File | Role |
|---|---|
| `src/contract.ts` | Types + loaders for `.cms/*` + engine runner (`cms.py`) |
| `src/contentTree.ts` | `TreeDataProvider` — the Content view |
| `src/dashboard.ts` | Webview: summary, worklist, transcript, diff/approve cards |
| `src/agent.ts` | Agent SDK `query()` runner; `canUseTool` → approve/deny |
| `src/extension.ts` | `activate()` — wires views, commands, status bar |

The extension never bypasses the engine's safety boundaries: the agent uses the
`cms-curator` skill (which refuses to touch vendored/generated content), and every
mutating tool call is gated by the approval UI.
