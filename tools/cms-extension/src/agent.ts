import * as path from "path";
import * as vscode from "vscode";
import { CmsDashboard } from "./dashboard";

// Load the (possibly ESM-only) SDK at runtime without TS downleveling import()
// to require(). Works whether the package ships CJS or ESM.
const dynamicImport = new Function("m", "return import(m)") as (m: string) => Promise<any>;

const READ_ONLY_TOOLS = new Set(["Read", "Grep", "Glob", "LS", "TodoWrite", "NotebookRead"]);

let idSeq = 0;
const nextId = () => `appr-${Date.now()}-${idSeq++}`;

export class CmsAgent {
  private current?: AbortController;

  constructor(
    private readonly repoRoot: string,
    private readonly dashboard: CmsDashboard
  ) {}

  get running(): boolean {
    return !!this.current;
  }

  stop(): void {
    this.current?.abort();
  }

  /** Run one agent pass with the given prompt (uses the cms-curator skill). */
  async run(prompt: string): Promise<void> {
    if (this.current) {
      vscode.window.showWarningMessage("CMS agent is already running.");
      return;
    }
    let sdk: any;
    try {
      sdk = await dynamicImport("@anthropic-ai/claude-agent-sdk");
    } catch (e) {
      this.dashboard.append(
        "error",
        "Could not load @anthropic-ai/claude-agent-sdk. Run `npm install` in tools/cms-extension. " +
          String(e)
      );
      return;
    }
    const query = sdk.query;
    if (typeof query !== "function") {
      this.dashboard.append("error", "Agent SDK has no query() export — version mismatch.");
      return;
    }

    const cfg = vscode.workspace.getConfiguration("itjCms");
    const model = cfg.get<string>("model", "claude-opus-4-8");
    const permissionMode = cfg.get<string>("permissionMode", "default");
    const maxTurns = cfg.get<number>("maxTurns", 40);

    const abort = new AbortController();
    this.current = abort;
    this.dashboard.clearTranscript();
    this.dashboard.setStatus("running", true);
    this.dashboard.append("system", `Starting agent · model ${model} · ${permissionMode}`);

    try {
      const response = query({
        prompt,
        options: {
          cwd: this.repoRoot,
          model,
          maxTurns,
          permissionMode,
          allowedTools: ["Read", "Grep", "Glob", "LS"],
          abortController: abort,
          systemPrompt: {
            type: "preset",
            preset: "claude_code",
            append:
              "You are running inside the IT-Journey CMS VS Code extension. " +
              "Use the cms-curator skill. Do NOT create a branch, commit, push, or open a PR — " +
              "the user reviews edits via the approval UI and handles git themselves.",
          },
          canUseTool: async (toolName: string, input: any) => {
            if (READ_ONLY_TOOLS.has(toolName)) {
              return { behavior: "allow", updatedInput: input };
            }
            const { summary, detail } = describeTool(toolName, input, this.repoRoot);
            const ok = await this.dashboard.requestApproval({
              id: nextId(),
              tool: toolName,
              summary,
              detail,
            });
            return ok
              ? { behavior: "allow", updatedInput: input }
              : { behavior: "deny", message: "Denied by the user in the CMS dashboard." };
          },
        },
      });

      for await (const message of response) {
        this.render(message);
      }
    } catch (e: any) {
      if (abort.signal.aborted) {
        this.dashboard.append("system", "Stopped.");
      } else {
        this.dashboard.append("error", "Agent error: " + (e?.message ?? String(e)));
      }
    } finally {
      this.current = undefined;
      this.dashboard.setStatus("idle", false);
    }
  }

  private render(message: any): void {
    const d = this.dashboard;
    try {
      switch (message?.type) {
        case "system":
          if (message.subtype === "init") {
            d.append("system", `session ${message.session_id ?? ""} ready`);
          }
          break;
        case "assistant": {
          const content = message.message?.content ?? [];
          for (const block of content) {
            if (block.type === "text" && block.text?.trim()) {
              d.append("assistant", block.text.trim());
            } else if (block.type === "tool_use") {
              d.append("tool", `→ ${block.name}(${briefInput(block.input)})`);
            }
          }
          break;
        }
        case "result": {
          const cost =
            typeof message.total_cost_usd === "number"
              ? ` · $${message.total_cost_usd.toFixed(4)}`
              : "";
          const turns = message.num_turns != null ? ` · ${message.num_turns} turns` : "";
          d.append(
            message.is_error ? "error" : "result",
            `done: ${message.subtype ?? "ok"}${turns}${cost}`
          );
          break;
        }
        // 'user' (tool results) and 'stream_event' are intentionally not rendered.
      }
    } catch {
      /* defensive: never let rendering break the stream */
    }
  }
}

function briefInput(input: any): string {
  if (!input || typeof input !== "object") return "";
  if (input.file_path) return path.basename(String(input.file_path));
  if (input.command) return String(input.command).slice(0, 60);
  if (input.pattern) return String(input.pattern).slice(0, 40);
  return Object.keys(input).slice(0, 3).join(", ");
}

/** Build an approval card summary + diff/detail for a mutating tool call. */
function describeTool(
  tool: string,
  input: any,
  repoRoot: string
): { summary: string; detail: string } {
  const rel = (p: any) =>
    p ? path.relative(repoRoot, path.isAbsolute(String(p)) ? String(p) : path.join(repoRoot, String(p))) : "";
  switch (tool) {
    case "Edit": {
      const file = rel(input?.file_path);
      const detail =
        input?.old_string != null && input?.new_string != null
          ? diffify(String(input.old_string), String(input.new_string))
          : JSON.stringify(input, null, 2).slice(0, 4000);
      return { summary: file, detail };
    }
    case "MultiEdit": {
      const file = rel(input?.file_path);
      const edits = Array.isArray(input?.edits) ? input.edits : [];
      const detail = edits
        .map((e: any, i: number) => `# edit ${i + 1}\n` + diffify(String(e.old_string ?? ""), String(e.new_string ?? "")))
        .join("\n");
      return { summary: `${file} (${edits.length} edits)`, detail };
    }
    case "Write": {
      const file = rel(input?.file_path);
      const content = String(input?.content ?? "");
      return {
        summary: `${file} (write ${content.length} chars)`,
        detail: content.slice(0, 4000) + (content.length > 4000 ? "\n… (truncated)" : ""),
      };
    }
    case "NotebookEdit": {
      return { summary: rel(input?.notebook_path), detail: JSON.stringify(input, null, 2).slice(0, 3000) };
    }
    case "Bash": {
      return { summary: "shell command", detail: String(input?.command ?? "").slice(0, 3000) };
    }
    default:
      return { summary: tool, detail: JSON.stringify(input, null, 2).slice(0, 3000) };
  }
}

/** Very small line-prefixed diff for the approval card. */
function diffify(oldStr: string, newStr: string): string {
  const out: string[] = [];
  for (const l of oldStr.split("\n")) out.push("- " + l);
  for (const l of newStr.split("\n")) out.push("+ " + l);
  return out.join("\n").slice(0, 4000);
}
