// The stable contract between the IT-Journey CMS engine (scripts/cms/cms.py)
// and this extension. Types mirror the JSON the engine writes under .cms/.
// See docs/cms/EXTENSION_DESIGN.md §1.
import * as cp from "child_process";
import * as fs from "fs";
import * as path from "path";
import * as vscode from "vscode";

export type Lane = "mechanical" | "substantive";
export type Severity = "error" | "warning" | "info";
export type Freshness = "fresh" | "aging" | "stale" | "critical" | "unknown";

export interface CmsIssue {
  kind: string;
  severity: Severity;
  field: string;
  message: string;
  lane: Lane;
  suggestion: string | null;
}

export interface CmsFile {
  path: string;
  collection: string;
  fm_content_type: string;
  is_notebook: boolean;
  frontmatter_present: boolean;
  read_only: boolean;
  generated: boolean;
  structural: boolean;
  draft: boolean | null;
  title: string | null;
  description_len: number;
  title_len: number;
  word_count: number;
  heading_count: number;
  lastmod: string | null;
  date: string | null;
  age_days: number | null;
  freshness: Freshness;
  broken_links: number;
  health: number; // 0-100, -1 = not scored
  issues: CmsIssue[];
}

export interface CmsIndex {
  generated_at: string;
  files: CmsFile[];
}

export interface CollectionSummary {
  count: number;
  scored: number;
  mechanical: number;
  substantive: number;
  errors: number;
  avg_health: number | null;
}

export interface CmsSummary {
  generated_at: string;
  total_files: number;
  scored_files: number;
  actionable_files: number;
  avg_health: number | null;
  avg_health_actionable: number | null;
  total_mechanical_issues: number;
  total_substantive_issues: number;
  total_errors: number;
  read_only_files: number;
  by_collection: Record<string, CollectionSummary>;
  freshness_distribution: Record<string, number>;
  health_buckets: Record<string, number>;
}

const REL = {
  config: ".cms/config.yml",
  index: ".cms/index/content-index.json",
  summary: ".cms/index/summary.json",
  schema: ".cms/schema/content-schema.json",
};

/** Find the workspace folder that is an IT-Journey repo (contains .cms/config.yml). */
export function findRepoRoot(): string | undefined {
  const folders = vscode.workspace.workspaceFolders ?? [];
  for (const f of folders) {
    if (fs.existsSync(path.join(f.uri.fsPath, REL.config))) {
      return f.uri.fsPath;
    }
  }
  // Fallback: a single-folder workspace even if config not yet generated.
  return folders[0]?.uri.fsPath;
}

function readJson<T>(root: string, rel: string): T | undefined {
  const p = path.join(root, rel);
  try {
    return JSON.parse(fs.readFileSync(p, "utf8")) as T;
  } catch {
    return undefined;
  }
}

export function loadIndex(root: string): CmsIndex | undefined {
  return readJson<CmsIndex>(root, REL.index);
}
export function loadSummary(root: string): CmsSummary | undefined {
  return readJson<CmsSummary>(root, REL.summary);
}
export function loadSchema(root: string): any | undefined {
  return readJson<any>(root, REL.schema);
}

export function reportPath(root: string, dateUtc = utcDate()): string {
  return path.join(root, ".cms", "reports", `${dateUtc}.md`);
}
export function worklistPath(root: string, dateUtc = utcDate()): string {
  return path.join(root, ".cms", "worklists", `${dateUtc}.md`);
}

export function utcDate(): string {
  return new Date().toISOString().slice(0, 10);
}

/** Run the CMS engine (scripts/cms/cms.py <command>) and resolve with its output. */
export function runEngine(
  root: string,
  command: "index" | "analyze" | "plan" | "all" | "status"
): Promise<{ code: number; stdout: string; stderr: string }> {
  const python = vscode.workspace
    .getConfiguration("itjCms")
    .get<string>("pythonPath", "python3");
  return new Promise((resolve) => {
    cp.execFile(
      python,
      [path.join("scripts", "cms", "cms.py"), command],
      { cwd: root, maxBuffer: 32 * 1024 * 1024 },
      (err, stdout, stderr) => {
        resolve({
          code: err && typeof (err as any).code === "number" ? (err as any).code : err ? 1 : 0,
          stdout: stdout?.toString() ?? "",
          stderr: stderr?.toString() ?? "",
        });
      }
    );
  });
}

/** Run the deterministic mechanical normalizer in dry-run (preview) mode. */
export function runMechanicalPreview(
  root: string
): Promise<{ code: number; stdout: string; stderr: string }> {
  const python = vscode.workspace
    .getConfiguration("itjCms")
    .get<string>("pythonPath", "python3");
  return new Promise((resolve) => {
    cp.execFile(
      python,
      [path.join("scripts", "content", "normalize-frontmatter.py"), "pages/"],
      { cwd: root, maxBuffer: 32 * 1024 * 1024 },
      (err, stdout, stderr) => {
        // exit 2 = "changes pending" (not an error for a dry-run)
        resolve({
          code: err && typeof (err as any).code === "number" ? (err as any).code : err ? 1 : 0,
          stdout: stdout?.toString() ?? "",
          stderr: stderr?.toString() ?? "",
        });
      }
    );
  });
}

/** Files that are safe for the agent/UI to edit (not read-only/generated/structural). */
export function isEditable(f: CmsFile): boolean {
  return !f.read_only && !f.generated && !f.structural && !f.is_notebook;
}

export function healthIcon(health: number): string {
  if (health < 0) return "$(circle-outline)";
  if (health >= 90) return "$(pass-filled)";
  if (health >= 70) return "$(circle-filled)";
  if (health >= 50) return "$(warning)";
  return "$(error)";
}
