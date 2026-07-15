---
title: 'Quest Walkthrough — Data Scientist · Level 1101 (Machine Learning & AI)'
date: '2026-07-15T13:04:24.000Z'
character: data-scientist
level: '1101'
theme: Machine Learning & AI
tier: Master
quest_count: 5
mode: execute
overall_verdict: warn
session:
  window: '1 of 2 (5 of 10 quests in the level)'
  average_score: 85.0
  engine_counts: '4 pass · 1 warn · 0 fail'
  engine_cost_usd: 3.278
  evidence: walk-evidence.json / walk-evidence.md (sealed by the workflow; consumed as-is)
---

## 🎯 Session Summary

Walked the first date-rotated **window (5 of 10)** of the Data Scientist Master
level `1101` end-to-end in the runner sandbox, in the planner's dependency-sorted
order. The machine-checked execute engine scored **4 pass, 1 warn, avg 85.0%** and
I read every quest source as a learner would to judge the *linked journey*.

Headline: **warn**. The three core ML quests (`python-data-science` →
`ml-fundamentals` → `neural-networks`) form a genuinely coherent, dependency-linked
learning arc, and the first two run flawlessly on a fresh 2026 scientific-Python
stack. The single blocking problem sits at the *end* of that arc: the capstone
`neural-networks` Chapter 1 forward-pass snippet **crashes as written** on the exact
`pip install numpy` the whole slice installs (NumPy 2.5.1) — a `float()`-on-1-element-array
`TypeError`. Because every earlier quest in the chain happily installs that same NumPy,
this is a *chain-level* currency bug: the learner carries a working numpy through two
quests and then hits a hard crash in the finale. Two other slice members
(`self-operating-website-07`, `ouroboros-loop-06`) are self-contained mid-campaign
chapters from **different** campaigns that merely share the `1101` level bin; they are
technically strong but sit off the Data Scientist's ML learning path.

## 🗺️ The Journey

Plan order (dependency-sorted by the planner). `verdict · title · score · takeaway`:

1. ✅ **Python for Data Science: NumPy, Pandas & Matplotlib** — **83** · Every setup
   command + all four chapter snippets + all three mastery challenges ran and matched
   the text exactly; deductions are a now-stale `SettingWithCopyWarning` indicator
   (pandas 3.0 CoW) and an untaught "Merging Data" objective.
2. ✅ **The Named Familiars: Agents, Skills, and a Self-Review Loop** — **94** · YAML,
   frontmatter, and the real `claude --agent … --print` CLI invocation all verified
   against the installed Claude Code CLI; only gap is the `agent-auditor` body being
   promised but never shown in full. *(Off the ML path — see Chain Continuity.)*
3. ✅ **Machine Learning Fundamentals with Scikit-Learn** — **92** · All 8 snippets +
   3 reconstructed challenges ran on scikit-learn 1.9.0 with matching output; the one
   real weakness is a regularization demo whose numbers contradict its own narrative.
4. ✅ **The Fixer's Oath: Repairs Kept by Gates, Not Grades** — **88** · The keep/revert
   gate was verified end-to-end (checker-fail, linter-fail, clean-keep all reproduced);
   the circuit-breaker fragment `NameError`s standalone by design. *(Mid-campaign
   chapter VI/VII of a different campaign — see Chain Continuity.)*
5. ⚠️ **Neural Networks Deep Dive: Build One From Scratch** — **68** · The from-scratch
   XOR backprop and the PyTorch loop run flawlessly, but Chapter 1's forward pass
   crashes on current NumPy and the Advanced Challenge invites a double-softmax bug.

## 🔬 Evidence

All statuses below are from commands the execute engine **actually ran** in the
disposable sandbox (`walk-evidence.json`), except items explicitly labeled `reasoned`
(judged statically) or `skipped` (no OS/network available). Environment for every
quest: fresh Python 3.12.13 venv, numpy 2.5.1, pandas 3.0.3, matplotlib 3.11.0,
scikit-learn 1.9.0, torch 2.13.0+cu130.

### 1. Python for Data Science — ran 11/11 commands passed, 2 skipped
- ✅ venv + `pip install numpy pandas matplotlib seaborn scikit-learn jupyter` — clean, no conflicts.
- ✅ Ch1 NumPy — output matched exactly: `[ 2 4 6 8 10]`, `3.0 1.4142135623730951`, `[3 4 5]`.
- ✅ Ch2 pandas/sklearn — `df.shape=(150,6)`, groupby species means correct, **zero warnings**.
- ✅ Ch3 EDA/cleaning — `isna().sum()` 2/1/1 → 0/0/0 after median/mode impute. **No `SettingWithCopyWarning`** (pandas 3.0 CoW default — see Issues).
- ✅ Ch4 matplotlib — `iris_eda.png` (60,561 bytes) written headless (auto Agg backend).
- ✅ All 3 mastery challenges (`load_wine` summary, inject-NaN+impute+groupby, LogisticRegression) ran; Advanced reported `Accuracy: 1.0` **with an unflagged `ConvergenceWarning`** (lbfgs, 1000 iters).
- ⏭️ Windows PowerShell block (no Windows env) and `sudo apt` (sudo blocked) — skipped; venv/pip path identical to macOS block which passed.

### 2. The Named Familiars — ran 8/8 commands passed, 1 reasoned
- ✅ 5 YAML/frontmatter blocks (`content-reviewer`, `agent-auditor`, `claude-run/action.yml`, `content-review.yml`, `agent-audit.yml`) all parsed with PyYAML.
- ✅ **Live CLI check**: `claude --agent content-reviewer --permission-mode acceptEdits --print "…"` verified against the installed CLI (v2.1.197) — all three flags real; reached the auth check (`Not logged in`) rather than a syntax error. `claude setup-token` confirmed to exist.
- ✅ Python rubric sketch (`checks = […]`) ran and printed the list.
- 🧠 `reasoned`: Quest-Network Mermaid diagram — no `mmdc` in sandbox; syntax standard.

### 3. Machine Learning Fundamentals — ran 10/10 commands passed, 1 skipped
- ✅ venv + install; `import sklearn` → `scikit-learn 1.9.0`.
- ✅ Ch2 Iris split/scale/fit/eval — `Test accuracy: 0.933`, confusion matrix `[[10,0,0],[0,9,1],[0,1,9]]`, full classification report. No warnings under `-W error::DeprecationWarning`.
- ✅ Ch3 `cross_val_score` RF cv=5 → `CV accuracy: 0.950 ± 0.017`.
- ✅ Ch3 regularization — `Strong-reg 0.867` vs `Weak-reg 1.0` — ran fine but **contradicts the surrounding "strong reg resists overfitting" prose** (see Issues).
- ✅ Ch4 KMeans → `Cluster sizes: [62 50 38]`, `Inertia 78.9`.
- ✅ All 3 mastery challenges reconstructed from stated requirements and ran; Intermediate reproduced the quest's own Validation claim (unlimited-tree gap 0.088 > depth-3 gap 0.037).
- ⏭️ Windows PowerShell block skipped (no Windows env).

### 4. The Fixer's Oath — ran 5 commands: 4 passed, 1 failed, 1 reasoned
- ✅ Ch2 gate YAML — parsed, and its embedded shell ran end-to-end against a real git repo + toy `scripts/check.sh` + real `npx markdownlint-cli2`: **checker-fail revert, linter-fail revert (genuine MD041 caught), and clean-keep all reproduced exactly.**
- ❌ **Ch3 circuit-breaker fragment — `NameError: name 'covered' is not defined`** when run verbatim; it assumes `covered`/`shelf`/`data` from the Chapter V ledger script the quest references (see Issues).
- ✅ Same breaker logic with mock context supplied — behaved exactly as documented (mid-sweep no-increment; 3 imperfect rounds → `needs_human=True`; perfect round resets).
- ✅ Both Mermaid diagrams rendered via `@mermaid-js/mermaid-cli` v11.16.0 (valid SVGs).
- 🧠 `reasoned`: `.claude/agents/potion-fixer.md` role file (config prose, internally consistent). *Note:* cited PR #445 / run 28791022929 could not be verified — **outbound network denied** in sandbox (unconfirmed, not contradicted).

### 5. Neural Networks Deep Dive — ran 7 commands: 6 passed, 1 failed, 2 skipped
- ✅ venv + `pip install numpy torch matplotlib` → torch 2.13.0+cu130; `cuda False` on CPU runner.
- ❌ **Ch1 forward pass — `TypeError: only 0-dimensional arrays can be converted to Python scalars`** at `float(y_hat)`. `y_hat` is shape `(1,)`; NumPy 2.5.1 (this quest's own uncapped install) forbids implicit `float()` of a 1-element array. "Hidden activations" printed (`[0. 0.092 0.367]`) then it crashed before "Prediction".
- ✅ Ch2 from-scratch XOR backprop — loss 0.3267 → 0.0007 over 5000 epochs; predictions `[0.02, 0.98, 0.98, 0.03]` ≈ XOR `[0,1,1,0]`.
- ✅ Ch3 PyTorch loop — loss 0.6981 → ~0.0000; rounded predictions `[0.0, 1.0, 1.0, 0.0]`.
- ⏭️ macOS and Windows setup blocks skipped (no such env); syntax reasoned correct.

## 🐞 Issues Found

Grouped by severity; each cites what was observed. Nothing here is a content edit — a
content-curator / human acts on these. **This slice has one high-severity blocker.**

**HIGH**
- **`neural-networks` · Ch1 forward pass (`float(y_hat)`, ~line 238)** — *tested, failed.*
  Crashes verbatim with `TypeError: only 0-dimensional arrays can be converted to
  Python scalars` on NumPy 2.5.1, the version the quest's own `pip install numpy`
  installs. Every learner following setup literally hits this. **Fix:** `float(y_hat.item())`
  or `float(y_hat[0])`.

**MEDIUM**
- **`neural-networks` · Advanced Challenge (~line 385)** — *reasoned.* "Build a 64→64→10
  network with ReLU and softmax (`CrossEntropyLoss`)" invites a double-softmax bug:
  `nn.CrossEntropyLoss` already applies log-softmax to raw logits. **Fix:** state the
  net should output raw logits and warn against a separate `nn.Softmax` layer.
- **`ml-fundamentals` · Ch3 regularization demo (~lines 332–339)** — *tested.* On clean
  Iris, `C=100` (weak) scored `1.0` vs `C=0.1` (strong) `0.867` — the **opposite** of the
  "strong regularization resists overfitting" narrative, because there's no overfitting
  to fight on this toy set. **Fix:** use a noisier/harder setup (noise features, higher-degree
  expansion) so the printed numbers support the lesson.
- **`python-data-science` · Mastery Indicator "Troubleshoot a `SettingWithCopyWarning`" (line 117)** — *tested.*
  pandas 3.0 (pulled by the uncapped `pip install pandas`) enables Copy-on-Write by
  default; the classic chained-assignment pattern raised **0 warnings** in the sandbox.
  A learner literally cannot reproduce the warning today. **Fix:** pin `pandas<3.0` for
  that exercise, demonstrate a still-warning construct, or replace with a CoW-relevant concept.
- **`python-data-science` · Secondary Objective "Merging Data" (line 109)** — *reasoned.*
  Listed as an objective but `pd.merge`/`df.join` is never taught or exercised anywhere
  in the body or challenges. **Fix:** add a short merge/join example or challenge step.
- **`ouroboros-loop-06` · Ch3 circuit-breaker fragment (~lines 287–297)** — *tested, failed.*
  `NameError` when run standalone; it depends on `covered`/`shelf`/`data` from the
  Chapter V ledger script. **Fix:** show the surrounding Chapter V variable definitions
  or explicitly label it "insert into your existing Chapter V function", not a runnable script.
- **`ouroboros-loop-06` · Mastery Challenge "no-op" leg** — *reasoned.* The kept/reverted
  legs get full runnable YAML; the honest-no-op leg gets only a prose rule + diagram box.
  **Fix:** add a short worked no-op example (write `fix-notes.md`, exit green).
- **`self-operating-website-07` · Ch2 `agent-auditor.md`** — *reasoned.* Frontmatter is
  shown with "(frontmatter shown)" and the body is *promised* ("its body spells out the
  persona and the same rubric") but never given in full, unlike `content-reviewer.md`.
  **Fix:** show the full assembled auditor file so learners have a copy-pasteable artifact.

**LOW**
- **`python-data-science`** — Windows `Activate.ps1` execution-policy gotcha not mentioned (*skipped/reasoned*); Advanced Challenge `LogisticRegression` emits an **unflagged `ConvergenceWarning`** (*tested*); `plt.savefig` "or `plt.show()` in a notebook" doesn't explain the non-notebook terminal case (*reasoned*).
- **`ml-fundamentals`** — elbow method described but never coded despite matplotlib being required (*reasoned*); no knowledge-check answer key (*reasoned*); `$HOME\ml-quest` resolves to a literal backslash under cross-platform `pwsh` (*reasoned*).
- **`neural-networks`** — matplotlib installed but never used, so the "read a falling loss curve" indicator rests on printed numbers only (*reasoned*); cross-entropy-vs-MSE is asked in a Knowledge Check but never answered in the body (*reasoned*).
- **`self-operating-website-07`** — no explicit local dry-run command (e.g. `claude --agent … --print`) despite the prereqs promising you can "test agents before pushing" (*reasoned*); `#`-comment "hard rules" inside the illustrative frontmatter could be mistaken for enforced config (*reasoned*).
- **`ouroboros-loop-06`** — cited PR #445 / run `28791022929` unverifiable (network denied); consider an inline summary so the claim is self-verifying (*reasoned*).

## 🔗 Chain Continuity

**The ML arc (quests 1 → 3 → 5) is a real, well-linked path — with one cross-quest crack.**
`python-data-science` (`unlocks_quests: ml-fundamentals`) → `ml-fundamentals`
(`recommended: python-data-science`, `unlocks: neural-networks`) → `neural-networks`
(`required: ml-fundamentals`). The prerequisites each quest assumes *are* delivered by
its predecessor: quest 1 forges NumPy/pandas and even a first `LogisticRegression` in
its Advanced Challenge, exactly the footing `ml-fundamentals` expects; `ml-fundamentals`
teaches train/test discipline and sklearn datasets that `neural-networks`' `load_digits`
Advanced Challenge builds on. A learner finishing quest N is genuinely ready for N+1.

**The crack is a shared-environment currency bug.** All three ML quests instruct an
uncapped `pip install numpy`, which today yields NumPy 2.5.1. Quests 1 and 3 run
cleanly on it; the capstone quest 5 **crashes on it in Chapter 1**. So the failure is
worse *in the chain* than in isolation: the learner installs numpy in quest 1, uses it
successfully for two quests, reasonably reuses/reinstalls the same version for the
finale, and hits a hard `TypeError` on the very first hands-on snippet of the Epic
capstone. Fixing the one line (`float(y_hat.item())`) restores end-to-end continuity.

**Two slice members are off the Data Scientist's path.** The planner sorts by level
membership, and level `1101` ("Machine Learning & AI") also bins two chapters from
*different* campaigns:
- `self-operating-website-07` — `quest_line: The Self-Operating Website`,
  `skill_focus: devops`; prereq is **Chapter VI (level 1100)** and a Claude Code OAuth
  token + owned GitHub repo. Self-contained and high-quality, but its prerequisites are
  **not** satisfied by anything in this slice, and its subject (agent/skill separation,
  CI wiring) is orthogonal to a data-scientist's ML learning arc.
- `ouroboros-loop-06` — chapter **VI of a VII-part** "Ouroboros Loop" campaign that
  explicitly depends on artifacts (`evidence.txt`, `ledger.json`, `scripts/check.sh`,
  `potions/`) built in Chapters I–V, none present here. The evidence confirms this: the
  breaker fragment `NameError`s precisely because its Chapter-V context is absent. It
  cannot be completed in isolation and is a mid-campaign automation chapter, not
  data-science content.

So for the **data-scientist character specifically**, the coherent, completable learning
journey in this window is the 3-quest ML spine; the other two are strong-but-misfiled
neighbors sharing the level code. Worth a maintainer noting whether the character-path
selection should filter by `skill_focus`/`quest_line` as well as level. This is a
window (5 of 10); the second window may or may not continue the ML spine.

## 🧠 Reasoning & Method

- **Mode: execute (real).** I did **not** run the engine — per the skill, `walk-evidence.json`
  / `walk-evidence.md` were pre-computed and sealed by the workflow (the engine's child
  `claude` processes can't authenticate from an agent's Bash tool). I consumed them as-is
  and edited nothing. Every `passed`/`failed` above traces to a command the engine ran in
  the disposable sandbox; every `reasoned`/`skipped` is labeled as such.
- **What I added (step 3):** I `Read` all five quest sources in plan order and reasoned
  about the *linked journey* — prerequisite satisfaction, the shared-numpy currency crack
  across quests 1→5, and the character-coherence of the two interleaved automation chapters.
  These chain findings are mine; the per-quest scores are the engine's.
- **Coverage / limits, stated honestly:**
  - This is **window 1 of 2** — 5 of the level's 10 quests. I did not walk the second window and make no claim about it.
  - **Skipped, not tested:** all Windows PowerShell and macOS setup blocks (Linux sandbox only), and `sudo apt` steps (sudo blocked). These are `skipped`, and the non-privileged venv/pip paths that *were* run are identical.
  - **Network denied:** `ouroboros-loop-06`'s external PR/run citations are unverified (not contradicted). The two CI-bound quests (`self-operating-website-07`, `ouroboros-loop-06`) can't be exercised fully end-to-end without a real repo + OAuth secret + Actions run — inherent to CI-bound content, not a defect; syntax/CLI were verified where possible.
  - Two mastery-challenge sets (`python-data-science`, `ml-fundamentals`) were *reconstructed from stated requirements* by the engine (the quests specify requirements, not literal code) and ran — a slightly weaker signal than copy-paste-verbatim, noted for honesty.
- **Confidence: high** on the code-execution findings (they reproduced in the sandbox with
  exact output), **medium** on the static/`reasoned` content and pedagogy findings.
  Overall verdict **warn**: the slice is strong (avg 85, 4/5 pass) but the ML capstone
  carries a verbatim crash-on-install that a real learner *will* hit, so the linked
  journey does not currently hold together end-to-end until that one line is fixed.
