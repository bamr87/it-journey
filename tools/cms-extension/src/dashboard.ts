import * as vscode from "vscode";
import { CmsSummary } from "./contract";

export interface ApprovalRequest {
  id: string;
  tool: string;
  summary: string;
  detail: string; // markdown/diff text
}

type TranscriptRole = "assistant" | "tool" | "system" | "result" | "user" | "error";

/**
 * The CMS dashboard webview: summary cards, action buttons, a streaming agent
 * transcript, and inline diff/approve cards for each proposed edit.
 */
export class CmsDashboard {
  private panel?: vscode.WebviewPanel;
  private pending = new Map<string, (ok: boolean) => void>();
  private lastSummary: CmsSummary | undefined;

  /** Wired by the extension. */
  onCurateWorklist?: () => void;
  onRunMechanical?: () => void;
  onApplyMechanical?: () => void;
  onRefresh?: () => void;
  onStop?: () => void;

  constructor(
    private readonly ctx: vscode.ExtensionContext,
    private readonly repoRoot: string
  ) {}

  show(): void {
    if (this.panel) {
      this.panel.reveal(vscode.ViewColumn.Beside);
      return;
    }
    this.panel = vscode.window.createWebviewPanel(
      "itjCms.dashboard",
      "IT-Journey CMS",
      vscode.ViewColumn.Beside,
      { enableScripts: true, retainContextWhenHidden: true }
    );
    this.panel.iconPath = vscode.Uri.joinPath(this.ctx.extensionUri, "media", "cms.svg");
    this.panel.webview.html = this.html(this.panel.webview);
    this.panel.onDidDispose(() => {
      // resolve any dangling approvals as denied
      for (const r of this.pending.values()) r(false);
      this.pending.clear();
      this.panel = undefined;
    });
    this.panel.webview.onDidReceiveMessage((m) => {
      switch (m?.type) {
        case "ready":
          // Webview finished loading — send the cached summary so a freshly
          // opened dashboard renders without waiting for a refresh.
          if (this.lastSummary) this.post({ type: "summary", summary: this.lastSummary });
          break;
        case "approve":
        case "deny": {
          const res = this.pending.get(m.id);
          if (res) {
            this.pending.delete(m.id);
            res(m.type === "approve");
          }
          break;
        }
        case "curateWorklist":
          this.onCurateWorklist?.();
          break;
        case "runMechanical":
          this.onRunMechanical?.();
          break;
        case "applyMechanical":
          this.onApplyMechanical?.();
          break;
        case "refresh":
          this.onRefresh?.();
          break;
        case "stop":
          this.onStop?.();
          break;
      }
    });
  }

  private post(msg: any): void {
    this.panel?.webview.postMessage(msg);
  }

  postSummary(summary: CmsSummary | undefined): void {
    // Cache it, but do NOT force the panel open — that would pop the dashboard
    // on every activation/refresh. openDashboard() shows it explicitly.
    this.lastSummary = summary;
    if (this.panel) this.post({ type: "summary", summary });
  }

  append(role: TranscriptRole, text: string): void {
    this.show();
    this.post({ type: "transcript", role, text });
  }

  setStatus(text: string, running: boolean): void {
    this.show();
    this.post({ type: "status", text, running });
  }

  clearTranscript(): void {
    this.show();
    this.post({ type: "clear" });
  }

  /** Show a diff/approve card; resolves true (approve) / false (deny). */
  requestApproval(req: ApprovalRequest): Promise<boolean> {
    this.show();
    return new Promise((resolve) => {
      this.pending.set(req.id, resolve);
      this.post({ type: "approval", ...req });
    });
  }

  private html(webview: vscode.Webview): string {
    const nonce = String(Math.random()).slice(2) + String(Date.now());
    const csp = `default-src 'none'; style-src ${webview.cspSource} 'unsafe-inline'; script-src 'nonce-${nonce}';`;
    return /* html */ `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta http-equiv="Content-Security-Policy" content="${csp}" />
<style>
  body { font-family: var(--vscode-font-family); color: var(--vscode-foreground); padding: 12px; }
  h2 { font-size: 13px; text-transform: uppercase; opacity: .7; margin: 16px 0 6px; }
  .cards { display: flex; flex-wrap: wrap; gap: 8px; }
  .card { background: var(--vscode-editorWidget-background); border: 1px solid var(--vscode-widget-border); border-radius: 6px; padding: 8px 12px; min-width: 96px; }
  .card .n { font-size: 20px; font-weight: 600; }
  .card .l { font-size: 11px; opacity: .7; }
  .bar { display:flex; gap:8px; align-items:center; margin: 8px 0 4px; flex-wrap: wrap; }
  button { background: var(--vscode-button-background); color: var(--vscode-button-foreground); border: none; padding: 5px 12px; border-radius: 4px; cursor: pointer; }
  button.secondary { background: var(--vscode-button-secondaryBackground); color: var(--vscode-button-secondaryForeground); }
  button:hover { opacity: .9; }
  #status { font-size: 12px; opacity: .8; margin-left: auto; }
  .dot { display:inline-block; width:8px; height:8px; border-radius:50%; background: var(--vscode-testing-iconPassed, #3fb950); margin-right:5px; }
  .dot.run { background: var(--vscode-progressBar-background, #3794ff); animation: pulse 1s infinite; }
  @keyframes pulse { 50% { opacity: .3; } }
  table { border-collapse: collapse; width: 100%; font-size: 12px; }
  td, th { text-align: left; padding: 2px 8px 2px 0; }
  #transcript { margin-top: 8px; }
  .msg { border-left: 3px solid var(--vscode-widget-border); padding: 4px 10px; margin: 6px 0; white-space: pre-wrap; font-size: 12.5px; }
  .msg.assistant { border-color: var(--vscode-charts-blue, #3794ff); }
  .msg.tool { border-color: var(--vscode-charts-yellow, #d7ba7d); opacity:.9; font-family: var(--vscode-editor-font-family); }
  .msg.result { border-color: var(--vscode-testing-iconPassed, #3fb950); }
  .msg.error { border-color: var(--vscode-errorForeground, #f14c4c); color: var(--vscode-errorForeground); }
  .msg.system { opacity:.6; }
  .approval { border: 1px solid var(--vscode-inputValidation-warningBorder, #cca700); border-radius: 6px; padding: 8px 10px; margin: 8px 0; background: var(--vscode-editorWidget-background); }
  .approval pre { max-height: 240px; overflow:auto; background: var(--vscode-textCodeBlock-background); padding: 6px; border-radius:4px; font-size: 12px; }
  .approval .actions { margin-top: 6px; display:flex; gap:8px; }
  .add { color: var(--vscode-gitDecoration-addedResourceForeground, #3fb950); }
  .del { color: var(--vscode-gitDecoration-deletedResourceForeground, #f14c4c); }
  .muted { opacity:.6; }
</style>
</head>
<body>
  <div class="bar">
    <button id="btnCurate">✨ Curate worklist</button>
    <button class="secondary" id="btnMech">🪄 Mechanical preview</button>
    <button class="secondary" id="btnApply">✅ Apply mechanical</button>
    <button class="secondary" id="btnRefresh">↻ Refresh</button>
    <button class="secondary" id="btnStop">⏹ Stop</button>
    <span id="status"><span class="dot" id="dot"></span><span id="statusText">idle</span></span>
  </div>

  <div id="summary"><p class="muted">Run “Refresh” to build the index…</p></div>

  <h2>Agent</h2>
  <div id="transcript"></div>

<script nonce="${nonce}">
  const vscode = acquireVsCodeApi();
  const $ = (id) => document.getElementById(id);
  $('btnCurate').onclick = () => vscode.postMessage({type:'curateWorklist'});
  $('btnMech').onclick = () => vscode.postMessage({type:'runMechanical'});
  $('btnApply').onclick = () => vscode.postMessage({type:'applyMechanical'});
  $('btnRefresh').onclick = () => vscode.postMessage({type:'refresh'});
  $('btnStop').onclick = () => vscode.postMessage({type:'stop'});

  function esc(s){ return String(s).replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); }

  function renderSummary(s){
    const el = $('summary');
    if(!s){ el.innerHTML = '<p class="muted">No index yet — click Refresh.</p>'; return; }
    const b = s.health_buckets || {};
    let rows = '';
    const coll = s.by_collection || {};
    for(const k of Object.keys(coll).sort((a,b)=>coll[b].count-coll[a].count)){
      const c = coll[k];
      rows += '<tr><td>'+esc(k)+'</td><td>'+c.count+'</td><td>'+(c.avg_health??'—')+'</td><td>'+c.mechanical+'</td><td>'+c.substantive+'</td></tr>';
    }
    el.innerHTML =
      '<div class="cards">'
      + card(s.actionable_files, 'actionable files')
      + card((s.avg_health_actionable ?? '—')+'', 'avg health')
      + card(s.total_mechanical_issues, 'mechanical')
      + card(s.total_substantive_issues, 'substantive')
      + card(s.read_only_files, 'read-only')
      + '</div>'
      + '<h2>By collection</h2>'
      + '<table><tr><th>collection</th><th>files</th><th>health</th><th>mech</th><th>subs</th></tr>'+rows+'</table>';
  }
  function card(n,l){ return '<div class="card"><div class="n">'+esc(n)+'</div><div class="l">'+esc(l)+'</div></div>'; }

  function addMsg(role, text){
    const t = $('transcript');
    const d = document.createElement('div');
    d.className = 'msg ' + role;
    d.textContent = text;
    t.appendChild(d);
    d.scrollIntoView({block:'end'});
  }

  function addApproval(req){
    const t = $('transcript');
    const wrap = document.createElement('div');
    wrap.className = 'approval';
    const detail = esc(req.detail)
      .split('\\n').map(line => {
        if(line.startsWith('+')) return '<span class="add">'+line+'</span>';
        if(line.startsWith('-')) return '<span class="del">'+line+'</span>';
        return line;
      }).join('\\n');
    wrap.innerHTML = '<b>Approve '+esc(req.tool)+'?</b> '+esc(req.summary)
      + '<pre>'+detail+'</pre>'
      + '<div class="actions"><button data-a="approve">Approve</button>'
      + '<button class="secondary" data-a="deny">Deny</button></div>';
    wrap.querySelector('[data-a=approve]').onclick = () => { vscode.postMessage({type:'approve', id:req.id}); wrap.querySelector('.actions').innerHTML='<span class="muted">approved</span>'; };
    wrap.querySelector('[data-a=deny]').onclick = () => { vscode.postMessage({type:'deny', id:req.id}); wrap.querySelector('.actions').innerHTML='<span class="muted">denied</span>'; };
    t.appendChild(wrap);
    wrap.scrollIntoView({block:'end'});
  }

  window.addEventListener('message', (e) => {
    const m = e.data;
    if(m.type==='summary') renderSummary(m.summary);
    else if(m.type==='transcript') addMsg(m.role, m.text);
    else if(m.type==='approval') addApproval(m);
    else if(m.type==='clear') $('transcript').innerHTML='';
    else if(m.type==='status'){ $('statusText').textContent=m.text; $('dot').className='dot'+(m.running?' run':''); }
  });

  // Tell the extension we're ready so it can send the cached summary.
  vscode.postMessage({type:'ready'});
</script>
</body>
</html>`;
  }
}
