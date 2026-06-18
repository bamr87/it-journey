# IT-Journey CMS — VS Code extension design & contract

> Status: design (the extension is built in a **separate repo**; this document is
> the spec + the stable contract this repo emits).

The goal is a local VS Code extension that works as a **CMS with embedded Claude
Code agents** — like the Front Matter CMS extension, but with content health,
the daily-loop worklist, and one-click agentic editing/curation built in. It is
the capstone (layer 4) on top of the foundation already in this repo:

```
layer 1  Content model + index   →  scripts/cms/cms.py  →  .cms/
layer 2  Analysis & reporting     →  .cms/reports/, .cms/index/summary.json
layer 3  Daily agent loop         →  .claude/skills/cms-curator + CI workflow
layer 4  VS Code extension        →  THIS DOC (separate repo)  ← reuses 1–3
```

The extension does **not** re-implement scanning, schema, or loop logic. It reads
what this repo produces and drives the same skill. That keeps one source of truth
across CLI, CI, and editor.

---

## 1. The contract this repo emits (stable API)

The extension depends only on these stable paths in the workspace root:

| Path | What | Shape |
|---|---|---|
| `.cms/config.yml` | policy: collections, lanes, safety globs, weights | YAML (see `.cms/config.yml`) |
| `.cms/schema/content-schema.json` | consolidated per-collection field schema | JSON (below) |
| `.cms/index/content-index.json` | one record per content file | JSON (below) |
| `.cms/index/summary.json` | repo-wide rollup | JSON |
| `.cms/worklists/<date>.md` | today's prioritized work | Markdown |
| `.cms/reports/<date>.md` | today's analysis | Markdown |
| `frontmatter.json` | existing Front Matter content types/taxonomy | JSON |

Regenerate everything with `python3 scripts/cms/cms.py index` (the extension shells
out to this on open and on a watcher; it is fast, pure-Python + pyyaml).

### `content-index.json` record (TypeScript)

```ts
interface CmsIndex { generated_at: string; files: CmsFile[] }

interface CmsFile {
  path: string;                 // repo-relative, e.g. "pages/_posts/devops/x.md"
  collection: string;           // posts | quests | docs | notes | ...
  fm_content_type: string;      // "default" | "quest"
  is_notebook: boolean;
  frontmatter_present: boolean;
  read_only: boolean;           // vendored — never edit
  generated: boolean;           // regenerated artifact — never hand-edit
  structural: boolean;          // README/template — skip deep checks
  draft: boolean | null;
  title: string | null;
  title_len: number;
  description_len: number;
  word_count: number;
  heading_count: number;
  lastmod: string | null;
  date: string | null;
  age_days: number | null;
  freshness: "fresh" | "aging" | "stale" | "critical" | "unknown";
  broken_links: number;
  health: number;               // 0–100, -1 = not scored (notebooks)
  issues: CmsIssue[];
}

interface CmsIssue {
  kind: string;                 // e.g. "missing_required:description", "title_too_long"
  severity: "error" | "warning" | "info";
  field: string;
  message: string;
  lane: "mechanical" | "substantive";
  suggestion: string | null;
}
```

`content-schema.json` carries `collections[].{path, fm_content_type, required,
recommended, fields}` (fields verbatim from `frontmatter.json`), plus
`constraints`, `read_only`, `generated`. The extension uses it to render schema-
aware editors and to validate before save — identical rules to CLI and CI.

---

## 2. Architecture

VS Code extensions run their logic in a **Node extension host**, so the
[Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/typescript)
(`@anthropic-ai/claude-agent-sdk`, `query()`) runs in-process. No separate
server.

```
┌──────────────────────── VS Code window ───────────────────────────┐
│  Activity-bar view "IT-Journey CMS"                                 │
│  ┌──────────────┐   ┌──────────────────────────────────────────┐  │
│  │ TreeView      │   │ Webview: Dashboard / Agent panel          │  │
│  │ Content browser│  │  • Contents grid (health, freshness)      │  │
│  │  by collection │  │  • Taxonomy & Media views                 │  │
│  │  ▸ posts (~90) │  │  • Worklist (Lane A / Lane B)             │  │
│  │  ▸ quests(~200)│  │  • Agent transcript + diff/approve UI     │  │
│  └──────────────┘   └──────────────────────────────────────────┘  │
│            │                         │                              │
│            ▼   extension host (Node) ▼                              │
│   read .cms/*  ──►  state  ◄──  Agent SDK query() ──► canUseTool ──►│ webview approve/deny
│        │                                   │                        │
│        ▼ shell out                         ▼ runs the SAME skill    │
│   python3 scripts/cms/cms.py        .claude/skills/cms-curator      │
└────────────────────────────────────────────────────────────────────┘
```

### Embedding Claude Code

- Drive `query({ prompt, options })` from the extension host. Options:
  `permissionMode: 'default'`, an explicit `allowedTools` allowlist,
  `maxTurns`/`maxBudgetUsd` caps, `cwd` = workspace, `model: 'claude-opus-4-8'`,
  `systemPrompt: { type: 'preset', preset: 'claude_code', append: <cms context> }`.
- Route **every** tool call through the `canUseTool` callback → render a
  diff/approve card in the webview; nothing writes to disk without the user's
  click (this is the editor-side analog of the loop's PR review).
- Reuse the **`cms-curator` skill** verbatim so editor behavior == CI behavior.
- Use **structured output** (`outputFormat: { type: 'json_schema' }`) for
  proposals (`{ file, action, rationale, frontmatter_changes }`) so the panel can
  show a clean review list and validate against `content-schema.json` first.
- Stream `SDKMessage`s to the webview via `postMessage`; wire a Stop button to
  `query.interrupt()` / an `AbortController`.
- Pin a recent `@anthropic-ai/claude-agent-sdk` (one new enough to expose
  `outputFormat: { type: 'json_schema' }` and the canonical `query()` API; verify
  against the current npm release before locking a version). Do **not** use the
  deprecated unstable V2 session API (`unstable_v2_*`); use `query()` with
  `options.resume` for multi-turn.

> Auth: reuse the user's existing Claude Code login (OAuth) or `ANTHROPIC_API_KEY`,
> mirroring `CLAUDE_CODE_OAUTH_TOKEN` used in CI.

---

## 3. Feature map (parity with Front Matter + AI augmentation)

| Front Matter feature | CMS extension equivalent | AI augmentation |
|---|---|---|
| Contents dashboard | TreeView + Contents grid from `content-index.json` | sort/filter by **health**, **freshness**, **lane** |
| Taxonomy dashboard | Taxonomy view from `frontmatter.json` + taxonomyDb | "suggest tags/categories" from existing taxonomy (no dupes) |
| Media dashboard | Media view over `assets/` | "backfill alt/caption" agent action |
| Content types / fields | schema-aware editor from `content-schema.json` | "fill required fields to spec" |
| Snippets / templates | reuse `.frontmatter/templates/*` | "generate from template + topic" |
| SEO checks | health scorecard per file (title/desc/keywords) | "fix SEO" one-click |
| — (new) | **Worklist panel** (Lane A/B from `.cms/worklists`) | "run mechanical lane", "curate top N" |
| — (new) | **Agent panel** with diff/approve | run `cms-curator` on selection/batch |

### Commands (package.json `contributes.commands`, sketch)

- `itjCms.refreshIndex` — run `cms.py index`, reload views.
- `itjCms.openDashboard` — open the webview.
- `itjCms.curateFile` — run the agent on the active file (diff/approve).
- `itjCms.runMechanicalLane` — `make content-normalize-apply` + preview diff.
- `itjCms.curateWorklist` — run the substantive batch with approvals.
- `itjCms.fixIssue` — quick-fix from a TreeView issue node.
- `itjCms.previewSite` — reuse `make serve` / the `run-it-journey` flow.

### Views (`contributes.views` under a custom `itjCms` container)

- `itjCms.content` — TreeDataProvider: collection → file → issues (cheap, native).
- `itjCms.dashboard` — Webview (`retainContextWhenHidden: true`) for grid +
  agent transcript.

---

## 4. Coexistence with Front Matter CMS

The extension **complements**, not replaces, `eliostruyf.vscode-front-matter`:

- It reads `frontmatter.json` as the field-schema source (single source of truth).
- It does not touch Front Matter's git posture (`git.enabled: false`) — commits/
  PRs go through git/`gh` + the existing CI gates, same as the loop.
- Users keep Front Matter for manual authoring; the new extension adds the health
  view, the worklist, and the agent. (Long-term, a fork that grafts Claude Code
  into Front Matter's panels via its extensibility SDK —
  `registerPanelView`/`registerCustomField` — is an option, but the standalone
  reader above ships faster and carries no upstream maintenance burden.)

---

## 5. Build phases (separate repo)

1. **MVP — read-only viewer.** Activity-bar container, TreeView + Contents grid
   from `content-index.json`, status bar health, `refreshIndex` (shell out to
   `cms.py`). No AI yet. Proves the contract.
2. **Worklist + mechanical.** Worklist panel; `runMechanicalLane` (shell to
   `make content-normalize-apply`) with a diff preview. Still no model calls.
3. **Agent panel.** Embed `query()`, `canUseTool` approve/deny, run `cms-curator`
   on a file/selection, structured proposals validated against the schema.
4. **Dashboards.** Taxonomy + Media views; SEO scorecard; "generate from
   template" actions.
5. **Polish.** Multi-turn resume, budget/turn telemetry, settings, packaging to
   the marketplace.

### Suggested repo scaffold

```
it-journey-cms-extension/
  package.json            # engines.vscode, contributes.{commands,views,viewsContainers}
  src/
    extension.ts          # activate(): register views/commands
    contract/index.ts     # CmsFile/CmsIssue types + loader for .cms/*
    tree/contentTree.ts   # TreeDataProvider
    webview/dashboard.ts  # webview host + postMessage bridge
    agent/runner.ts       # Agent SDK query() driver + canUseTool
    media/ taxonomy/ seo/  # dashboards
  webview-ui/             # the dashboard front-end (vanilla or a framework)
  README.md
```

The only coupling to IT-Journey is the **contract in §1** — point the extension at
any workspace that emits `.cms/` and it works, so the same extension can later
manage `zer0-mistakes` and `bashconsultants` (which already share the frontmatter
schema).
