import * as path from "path";
import * as vscode from "vscode";
import { CmsFile, CmsIndex, healthIcon, isEditable } from "./contract";

type Node =
  | { kind: "collection"; name: string; files: CmsFile[] }
  | { kind: "file"; file: CmsFile }
  | { kind: "issue"; file: CmsFile; index: number };

export class CmsTreeProvider implements vscode.TreeDataProvider<Node> {
  private _onDidChange = new vscode.EventEmitter<Node | undefined | void>();
  readonly onDidChangeTreeData = this._onDidChange.event;

  private index?: CmsIndex;
  constructor(private repoRoot: string) {}

  setIndex(index: CmsIndex | undefined): void {
    this.index = index;
    this._onDidChange.fire();
  }

  getTreeItem(node: Node): vscode.TreeItem {
    if (node.kind === "collection") {
      const scored = node.files.filter((f) => f.health >= 0);
      const avg = scored.length
        ? Math.round(scored.reduce((s, f) => s + f.health, 0) / scored.length)
        : 0;
      const withIssues = node.files.filter((f) => f.issues.length).length;
      const item = new vscode.TreeItem(
        `${node.name}`,
        vscode.TreeItemCollapsibleState.Collapsed
      );
      item.description = `${node.files.length} files · avg ${avg} · ${withIssues} need work`;
      item.iconPath = new vscode.ThemeIcon("folder");
      item.contextValue = "cmsCollection";
      return item;
    }

    if (node.kind === "file") {
      const f = node.file;
      const label = path.basename(f.path);
      const collapsible = f.issues.length
        ? vscode.TreeItemCollapsibleState.Collapsed
        : vscode.TreeItemCollapsibleState.None;
      const item = new vscode.TreeItem(label, collapsible);
      const h = f.health < 0 ? "—" : String(f.health);
      const flags = [
        f.read_only ? "read-only" : "",
        f.generated ? "generated" : "",
        f.draft ? "draft" : "",
      ].filter(Boolean);
      item.description = `${h}/100 · ${f.freshness}${flags.length ? " · " + flags.join(",") : ""}`;
      item.iconPath = new vscode.ThemeIcon(
        healthIcon(f.health).replace(/^\$\(|\)$/g, "")
      );
      item.tooltip = new vscode.MarkdownString(
        [
          `**${f.path}**`,
          "",
          `- health: ${h}/100`,
          `- freshness: ${f.freshness}` + (f.age_days != null ? ` (${f.age_days}d)` : ""),
          `- words: ${f.word_count}, headings: ${f.heading_count}`,
          `- issues: ${f.issues.length} (${f.issues.filter((i) => i.lane === "mechanical").length} mechanical / ${f.issues.filter((i) => i.lane === "substantive").length} substantive)`,
          f.read_only ? "- **read-only / vendored**" : "",
        ]
          .filter(Boolean)
          .join("\n")
      );
      item.contextValue = isEditable(f) ? "cmsFile" : "cmsFileReadonly";
      item.resourceUri = vscode.Uri.file(path.join(this.repoRoot, f.path));
      item.command = {
        command: "vscode.open",
        title: "Open",
        arguments: [item.resourceUri],
      };
      return item;
    }

    // issue
    const issue = node.file.issues[node.index];
    const icon =
      issue.severity === "error"
        ? "error"
        : issue.severity === "warning"
        ? "warning"
        : "info";
    const item = new vscode.TreeItem(
      issue.message,
      vscode.TreeItemCollapsibleState.None
    );
    item.iconPath = new vscode.ThemeIcon(icon);
    item.description = `${issue.lane} · ${issue.field}`;
    item.tooltip = issue.suggestion ?? issue.message;
    item.contextValue = "cmsIssue";
    return item;
  }

  getChildren(node?: Node): Node[] {
    if (!this.index) return [];
    if (!node) {
      const byColl = new Map<string, CmsFile[]>();
      for (const f of this.index.files) {
        if (!byColl.has(f.collection)) byColl.set(f.collection, []);
        byColl.get(f.collection)!.push(f);
      }
      return [...byColl.entries()]
        .sort((a, b) => b[1].length - a[1].length)
        .map(([name, files]) => ({ kind: "collection", name, files }) as Node);
    }
    if (node.kind === "collection") {
      // worst health first, but only files that have issues or are low-health
      return node.files
        .filter((f) => f.issues.length || (f.health >= 0 && f.health < 90))
        .sort((a, b) => (a.health < 0 ? 999 : a.health) - (b.health < 0 ? 999 : b.health))
        .map((file) => ({ kind: "file", file }) as Node);
    }
    if (node.kind === "file") {
      return node.file.issues.map(
        (_, i) => ({ kind: "issue", file: node.file, index: i }) as Node
      );
    }
    return [];
  }

  /** Resolve a tree node's file (for the curate-file command). */
  fileFromNode(node: Node | undefined): CmsFile | undefined {
    if (node?.kind === "file") return node.file;
    return undefined;
  }
}
