---
title: 'Walkthrough — Security Specialist · Level 1011 (Security & Compliance)'
date: '2026-07-17T00:00:00.000Z'
character: security-specialist
level: '1011'
theme: Security & Compliance
tier: Warrior
quest_count: 2
mode: execute
overall_verdict: warn
session:
  window: '2 of 3 (offset 10, size 5)'
  total_quests_in_level: 12
  quests_walked: 2
  engine_scored: 1
  engine_errored: 1
  average_score: 97.0
  cost_usd: 0.3815
  notes: >-
    Sealed workflow-minted evidence consumed as-is (walk-plan.json +
    walk-evidence.json/md). Quest 1 (Penetration Testing) produced NO execute
    evidence — the agentic engine timed out after 600s, so that quest is
    reasoned-only. Quest 2 (Compliance Standards) executed fully (4/4 runnable
    snippets passed).
---

## 🎯 Session Summary

I walked the **window 2 of 3** slice of the **Security Specialist → Level 1011 (Security & Compliance, 🔥 Warrior)** path: two `main_quest` pages — **Penetration Testing** (🔴 Hard) and **Compliance Standards** (🟡 Medium) — in the order the planner sorted them. The full level holds 12 quests; this rotating window covered the last two.

**Headline verdict: ⚠️ warn.** Not because a quest is broken, but because the slice is only **half-covered by real evidence**. The **Compliance Standards** quest is excellent — it scored **97%**, and all **4/4 runnable snippets actually executed and passed** in the sandbox with content verified accurate against current framework revisions (SOC 2 TSC, ISO 27001:2022, GDPR, PCI-DSS v4.0). But the **Penetration Testing** quest yielded **zero execute evidence**: the engine **timed out after 600s** and returned a `fail` with `overall: 0`. That is an *engine/tooling* failure, not a demonstrated content defect — so I treat every pentest observation below as `reasoned` (read statically from source), never `tested`. A maintainer should read this as "one quest proven solid, one quest un-walked" and re-run the pentest quest with a longer budget before trusting any verdict on it.

## 🗺️ The Journey

1. ❌ **Penetration Testing: Tools and Ethical Hacking Methodologies** — score **—**
(engine timed out after 600s; no snippets run) · *Content reads well and is ethics-first, but it is heavy on external tooling (docker, brew/winget casks, nmap, Burp/ZAP) — almost certainly why the execute engine exhausted its 600s budget. Un-walked; reasoned-only.*
2. ✅ **Compliance Standards: SOC 2, ISO 27001, GDPR, and PCI-DSS** — score **97**
(4/4 runnable snippets passed, 4 reasoned) · *A clean, accurate, well-structured documentation/process quest; only thin spots are two lightly-covered secondary objectives.*

## 🔬 Evidence

### Quest 1 — Penetration Testing (❌ no evidence gathered)

- **Engine result:** `error: "claude timed out after 600s"`, `verdict: fail`,
`overall: 0.0`, `verdict_obj: null`. No commands were recorded, no snippets ran, no per-dimension scores exist.
- **Coverage:** ran **0** snippets — this quest was **not executed**. Everything I say
about it is `reasoned` from the source file (`pages/_quests/1011/penetration-testing.md`), not witnessed in the sandbox.
- **Why it likely timed out (reasoned):** every platform path front-loads slow,
network-heavy installs and container pulls — `brew install --cask zap/burp-suite` (macOS), `winget install …` (Windows), `sudo apt install -y nmap zaproxy` + `docker run … bkimminich/juice-shop` (Linux). An execute engine attempting these will spend its whole budget on downloads. This is consistent with a 600s timeout and is itself a real learner-friction signal (see Issues).

### Quest 2 — Compliance Standards (✅ executed, 97%)

- **Coverage:** `ran 4/4` runnable snippets — **4 passed, 0 failed, 0 skipped**;
  4 additional non-runnable text blocks judged `reasoned`. Executed in 101.6s / 9 turns.
- **Per-dimension:** commands_work **5**, content_accuracy **5**, completeness **4**,
  clarity **5**, structure **5**, safety **5**.

Commands actually run (from `walk-evidence.json`):

| Command (platform path) | Status | Observed outcome |
|---|---|---|
| macOS: `mkdir ~/compliance` → `printf … > controls-matrix.csv` → `open -a Numbers … \|\| cat` | ✅ passed | `open` absent on Linux, stderr suppressed; `\|\| cat` fallback printed header `Control,SOC2,ISO27001,GDPR,PCI-DSS,Evidence` |
| Windows PowerShell: `New-Item` → `Set-Content` → `Get-Content` | ✅ passed | Executed via `pwsh -NoProfile`; produced the expected CSV header, no errors |
| Linux: `mkdir` → `echo … > csv` → `git init -q && git add` | ✅ passed | `git status` afterward confirmed `controls-matrix.csv` staged as a new file |
| Cloud Realms: `echo "Inherit provider controls; you remain responsible…"` | ✅ passed | Printed the expected shared-responsibility string verbatim |

Reasoned (non-runnable) content the engine verified as accurate: the SOC 2 vs ISO 27001 comparison table, the PCI-DSS 1–12 requirement groupings (matches v4.0), the MFA controls-mapping matrix (SOC 2 CC6.1 / ISO 27001 A.8.5 / GDPR Art. 32 / PCI-DSS Req. 8.4-8.5), and the audit-evidence / Type II period discussion.

> From `walk-evidence.md`: *"all four platform snippets ran successfully in the
> sandbox exactly as described. Minor gaps exist only in the depth of coverage for
> two secondary objectives (Gap Assessment, Shared Responsibility)…"*

## 🐞 Issues Found

**Penetration Testing** (all `reasoned` — the quest was not executed, so these are static-read observations, not sandbox-witnessed failures):

- **medium · Penetration Testing · platform setup blocks (lines 147-188) · engine
timeout / heavy prerequisites.** The engine **timed out after 600s** and captured no evidence. Reading the source, every path requires large external installs plus a Docker container pull (`docker run … bkimminich/juice-shop`). *Suggested fix:* offer a lighter "no-install / hosted lab" default (the Cloud Realms path already points at PortSwigger Academy + TryHackMe — promote it as the primary walkthrough target) so both a real beginner and the execute engine can complete the quest without a multi-hundred-MB toolchain. This is the single highest-value change for making this quest walkable.
- **low · Penetration Testing · Linux path (lines 183-187) · privilege assumption.**
`sudo apt install …` and `sudo docker run …` assume passwordless sudo and a Docker daemon. A learner on a locked-down machine (or the sandbox) gets stuck with no fallback. *Suggested fix:* note the rootless/Docker-Desktop alternative and that `sudo` may be unavailable.
- **low · Penetration Testing · Chapter 3 (line 308) · `zap.sh` on PATH.** The
headless command `zap.sh -cmd …` assumes `zap.sh` is on `PATH`, but the macOS cask and Windows winget installs don't guarantee that binary name/location. *Suggested fix:* mention the platform-specific launcher path or that ZAP must be started from its install dir.
- **low · Penetration Testing · Knowledge Graph (line 436) · stale wiki-link title.**
The `**Unlocks:**` link reads `[[Compliance Standards: SOC 2, GDPR, and HIPAA Requirements]]`, but the actual unlocked quest is titled **"SOC 2, ISO 27001, GDPR, and PCI-DSS"** — it covers PCI-DSS, not HIPAA. *Suggested fix:* update the wiki-link to the current title so the graph resolves and no beginner expects a HIPAA chapter that doesn't exist.

**Compliance Standards** (low, from the engine's own recommendations):

- **low · Compliance Standards · Secondary Objectives (lines 105, 107) · thin
coverage.** "Gap Assessment" appears only as an unguided mastery challenge and "Shared Responsibility" is only the one-line Cloud Realms echo — both are named objectives. *Suggested fix:* add a short worked example (a mini gap-assessment row; 2-3 sentences on provider-vs-customer ownership).
- **low · Compliance Standards · Continuous Compliance (line 313) · one-paragraph
depth.** Vanta/Drata/custom-scripts get a single paragraph. *Suggested fix:* add a concrete example of what an automated evidence query might check.

No **high-severity, sandbox-witnessed** content failures were found. The only high- impact problem in this slice is the **inability to gather evidence for the pentest quest at all**, which is a tooling/budget issue to resolve on re-run.

## 🔗 Chain Continuity

Reading the two quests as one journey a Security Specialist would actually take:

- **Prerequisites are met by earlier windows, not this one.** Both quests declare
`required_quests: /quests/1011/security-fundamentals/`. That quest sits in an earlier window of this level (this is window 2 of 3, offset 10), so a learner reaching here is *assumed* to have the CIA-triad / controls grounding both quests lean on. Within this window nothing is orphaned — neither quest assumes setup the other was supposed to provide.
- **Ordering is correct and the narrative hands off cleanly.** Penetration Testing
declares `unlocks_quests: /quests/1011/compliance-standards/`, and Compliance Standards lists pentest as a `recommended_quest`. The pentest quest's closing "Unlocked Quests" explicitly frames the transition — *"Compliance Standards — Penetration tests are often a required audit control"* — and Compliance Standards pays it off in Chapter 2 (PCI-DSS requirements 10-11: *"logging, scans, penetration tests"*). A learner finishing the pentest report arrives at compliance understanding *why* that report is audit evidence. That is genuinely good linked design.
- **The forward continuity I could verify holds; the backward half I could not
execute.** Because the pentest quest never ran, I cannot confirm from evidence that a learner actually *completes* it and emerges "ready" for compliance — only that the two pages are wired together correctly and the prose transition is coherent. The likely real-world snag is upstream of the narrative: a beginner may stall on the pentest tooling install (same friction that timed out the engine) and never reach the hand-off. Making the hosted-lab path the default would protect the whole chain.
- **One cosmetic graph break:** the pentest quest's Obsidian `Unlocks` wiki-link names
a "HIPAA" version of the compliance quest that doesn't exist (see Issues) — a learner exploring the graph would hit a dead/renamed node.

## 🧠 Reasoning & Method

- **Mode:** `execute`. I consumed **sealed, workflow-minted evidence**
(`walk-plan.json` + `walk-evidence.json` + `walk-evidence.md`) exactly as provided. I did **not** run, regenerate, or edit the engine or its evidence (the engine's child `claude` processes cannot authenticate from my Bash tool), and I did not edit any quest content. My only write is this report.
- **What was tested vs. reasoned:** Only **Compliance Standards** carries real
sandbox evidence (4/4 runnable snippets executed and passed; 4 text blocks reasoned). **Penetration Testing carries no evidence** — the engine timed out at 600s — so every statement I make about it is `reasoned` from the source file, and I have labeled it as such throughout. I did not fabricate a score, command, or output for it.
- **Coverage honesty:** This was a **2-quest window (2 of 3)** of a 12-quest level;
I did **not** walk the other 10 quests, and I did not walk the level's prerequisite chain — those belong to other windows and are accumulated by the perfection ledger over time. Within my window, **50% of quests produced usable evidence**; the pentest quest is effectively un-walked and should not be counted as validated.
- **Confidence:** **High** on the Compliance Standards verdict (direct, reproducible
execute evidence, accurate content). **Low** on Penetration Testing — I can only attest that it reads coherently and is ethics-first; I cannot attest that its commands work, because none were run. The `warn` overall verdict reflects that split.
- **Recommended next action:** re-run the Penetration Testing quest through the execute
engine with a larger time/turn budget, or after promoting the hosted-lab (Cloud Realms) path to primary so the sandbox isn't forced through heavyweight installs.
