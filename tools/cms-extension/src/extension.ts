import * as path from "path";
import * as vscode from "vscode";
import { CmsAgent } from "./agent";
import {
  CmsSummary,
  condenseNormalizerOutput,
  findRepoRoot,
  loadIndex,
  loadSummary,
  reportPath,
  runEngine,
  runMechanicalApply,
  runMechanicalPreview,
  worklistPath,
} from "./contract";
import { CmsTreeProvider } from "./contentTree";
import { CmsDashboard } from "./dashboard";

export function activate(ctx: vscode.ExtensionContext): void {
  const repoRoot = findRepoRoot();
  if (!repoRoot) {
    vscode.window.showWarningMessage(
      "IT-Journey CMS: no workspace folder with .cms/ found."
    );
    return;
  }

  const out = vscode.window.createOutputChannel("IT-Journey CMS");
  const tree = new CmsTreeProvider(repoRoot);
  const dashboard = new CmsDashboard(ctx, repoRoot);
  const agent = new CmsAgent(repoRoot, dashboard);

  const treeView = vscode.window.createTreeView("itjCms.content", {
    treeDataProvider: tree,
    showCollapseAll: true,
  });

  const status = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Left,
    50
  );
  status.command = "itjCms.openDashboard";
  status.tooltip = "IT-Journey CMS — open dashboard";
  ctx.subscriptions.push(out, treeView, status);

  // ---- shared refresh ---------------------------------------------------- //
  const reload = (): CmsSummary | undefined => {
    const index = loadIndex(repoRoot);
    const summary = loadSummary(repoRoot);
    tree.setIndex(index);
    dashboard.postSummary(summary);
    if (summary) {
      status.text = `$(database) CMS ${summary.avg_health_actionable ?? "—"}`;
      status.show();
    }
    return summary;
  };

  const refresh = async (): Promise<void> => {
    await vscode.window.withProgress(
      { location: vscode.ProgressLocation.Notification, title: "CMS: rebuilding index…" },
      async () => {
        const r = await runEngine(repoRoot, "all");
        out.appendLine(r.stdout || r.stderr);
        if (r.code !== 0) {
          vscode.window.showErrorMessage("CMS engine failed — see the IT-Journey CMS output.");
          out.show();
        }
        reload();
      }
    );
  };

  // ---- commands ---------------------------------------------------------- //
  const reg = (id: string, fn: (...a: any[]) => any) =>
    ctx.subscriptions.push(vscode.commands.registerCommand(id, fn));

  reg("itjCms.refresh", refresh);

  reg("itjCms.openDashboard", () => {
    dashboard.show();
    dashboard.postSummary(loadSummary(repoRoot));
  });

  reg("itjCms.curateFile", (node?: any) => {
    let rel: string | undefined = node?.file?.path;
    if (!rel && vscode.window.activeTextEditor) {
      rel = path.relative(repoRoot, vscode.window.activeTextEditor.document.uri.fsPath);
    }
    if (!rel) {
      vscode.window.showWarningMessage("CMS: open a content file or pick one in the Content view.");
      return;
    }
    dashboard.show();
    agent.run(
      `Use the cms-curator skill to improve ONLY this one file: \`${rel}\`. ` +
        `Apply the minimal change that resolves its issues per the schema in .cms/config.yml and ` +
        `.github/copilot-instructions.md. Do not touch other files. Do not branch/commit/push/PR.`
    );
  });

  reg("itjCms.curateWorklist", () => {
    dashboard.show();
    agent.run(
      `Use the cms-curator skill to run ONE substantive (Lane B) pass over today's ` +
        `.cms worklist: take the top items (respect the batch cap in .cms/config.yml), apply the ` +
        `minimal fixes, and validate. Do not branch/commit/push/PR — the user reviews each edit.`
    );
  });

  reg("itjCms.runMechanical", async () => {
    dashboard.show();
    dashboard.clearTranscript();
    dashboard.setStatus("running mechanical preview", true);
    dashboard.append("system", "Mechanical lane PREVIEW (dry-run via normalize-frontmatter.py)…");
    const r = await runMechanicalPreview(repoRoot);
    const { shown, skipped } = condenseNormalizerOutput(r.stdout || r.stderr);
    dashboard.append(r.code === 0 || r.code === 2 ? "result" : "error", shown);
    if (skipped) {
      dashboard.append("system", `(${skipped} vendored/read-only files skipped — protected)`);
    }
    dashboard.append(
      "system",
      'This was a dry-run. Click "✅ Apply mechanical" to write these changes.'
    );
    dashboard.setStatus("idle", false);
  });

  reg("itjCms.applyMechanical", async () => {
    const ok = await vscode.window.showWarningMessage(
      "Apply deterministic frontmatter normalization to pages/ ? This writes files (vendored content is skipped). Review the diff in Source Control afterward.",
      { modal: true },
      "Apply"
    );
    if (ok !== "Apply") return;
    dashboard.show();
    dashboard.setStatus("applying mechanical fixes", true);
    dashboard.append("system", "Applying mechanical normalization…");
    const r = await runMechanicalApply(repoRoot);
    const { shown, skipped } = condenseNormalizerOutput(r.stdout || r.stderr);
    dashboard.append(r.code === 0 || r.code === 2 ? "result" : "error", shown);
    if (skipped) dashboard.append("system", `(${skipped} vendored/read-only files skipped)`);
    dashboard.setStatus("idle", false);
    await refresh(); // re-index so the tree/summary reflect the applied fixes
    vscode.window.showInformationMessage("CMS: mechanical fixes applied — review the diff in Source Control.");
  });

  reg("itjCms.openReport", async () => {
    await openIfExists(reportPath(repoRoot));
  });
  reg("itjCms.openWorklist", async () => {
    await openIfExists(worklistPath(repoRoot));
  });

  // ---- dashboard buttons ------------------------------------------------- //
  dashboard.onRefresh = refresh;
  dashboard.onStop = () => agent.stop();
  dashboard.onRunMechanical = () => vscode.commands.executeCommand("itjCms.runMechanical");
  dashboard.onApplyMechanical = () => vscode.commands.executeCommand("itjCms.applyMechanical");
  dashboard.onCurateWorklist = () => vscode.commands.executeCommand("itjCms.curateWorklist");

  // ---- initial load ------------------------------------------------------ //
  const summary = reload();
  if (!summary) {
    vscode.window
      .showInformationMessage("IT-Journey CMS: no index yet. Build it now?", "Refresh")
      .then((c) => {
        if (c === "Refresh") void refresh();
      });
  }
}

export function deactivate(): void {
  /* noop */
}

async function openIfExists(p: string): Promise<void> {
  const uri = vscode.Uri.file(p);
  try {
    await vscode.workspace.fs.stat(uri);
    await vscode.window.showTextDocument(uri);
  } catch {
    vscode.window.showWarningMessage(
      `CMS: ${path.basename(p)} not found — run CMS: Refresh Index first.`
    );
  }
}
