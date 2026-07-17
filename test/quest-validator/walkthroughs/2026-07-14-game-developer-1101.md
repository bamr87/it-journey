---
title: "Walkthrough — Game Developer · Level 1101 (Machine Learning & AI)"
date: 2026-07-14T00:00:00.000Z
character: game-developer
level: "1101"
theme: Machine Learning & AI
tier: Master
quest_count: 5
mode: execute
overall_verdict: warn
session:
  window: "1 of 2 (5 of 10 level quests)"
  planned_order:
    - deep-learning-frameworks
    - computer-vision
    - natural-language-processing
    - mlops
    - ai-ethics
  engine_average: 84.2
  engine_counts: { pass: 3, warn: 1, fail: 1 }
  scored: 4
  errored: 1
  evidence_cost_usd: 2.7908
  evidence_source: walk-evidence.json (sealed by workflow; consumed as-is)
---

## 🎯 Session Summary

I walked a **5-quest window (window 1 of 2)** of the **Game Developer** path at **Level 1101 · Machine Learning & AI (Master)**, in the planner's order: Deep Learning Frameworks → Computer Vision → Natural Language Processing → MLOps → AI Ethics. Evidence came from the sealed execute-mode engine run (`walk-evidence.json` / `walk-evidence.md`) — I consumed it as-is and did **not** re-run the engine or edit any quest.

**Headline verdict: WARN.** Four quests scored and three passed cleanly (avg **84.2%**); the hands-on Python content across the slice is genuinely strong — nearly every runnable snippet was actually executed in the sandbox and its output matched the quest's own inline claims. Two things keep this from a clean pass: (1) a **high-priority broken snippet** in NLP — `pipeline("ner", grouped_entities=True)` crashes with a `TypeError` on the exact transformers version the quest's own unpinned install pulls (5.13.1); and (2) **MLOps could not be evaluated** — the engine hit its 40-turn cap mid-execution (launching and curling a FastAPI server), so its "fail" is a harness timeout, **not** a proven content defect. A maintainer should treat the NER fix as the one urgent item, re-run MLOps under a higher turn budget, and note that this slice is generic ML content with **zero game-developer framing**.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ✅ pass | Deep Learning Frameworks: PyTorch vs TensorFlow | 88 | Core PyTorch (tensors/autograd/training loop) runs exactly as claimed; TF/Keras half is an untrained stub and `DataLoader` objective is never taught. |
| 2 | ✅ pass | Computer Vision Mastery: CNNs and Transfer Learning | 89 | Every CNN/transfer-learning snippet ran (FashionMNIST → 87%, ResNet-18 fine-tune); friction: default install pulls ~4.8 GB CUDA, two secondary objectives untaught. |
| 3 | ⚠️ warn | Natural Language Processing: Transformers & LLMs | 71 | Tokenization/embeddings/challenges all pass; Chapter 3 NER line crashes on the version the quest installs — a concrete, high-priority fix. |
| 4 | ❌ n/a | MLOps Engineering: CI/CD Pipelines for ML in Production | — | **Not evaluated** — engine reached max turns (40) while running the serve-and-curl challenge; no verdict was produced. Reasoned-only below. |
| 5 | ✅ pass | AI Ethics: Bias Detection, Fairness & Governance | 89 | All runnable snippets pass; Fairlearn (the headline tool) is installed but never used, and the "conflicting fairness" objective/badge is claimed but untaught. |

## 🔬 Evidence

All per-quest numbers, commands, and outputs below are quoted from the sealed `walk-evidence.json` (execute mode). Snippet coverage is reported as `ran (passed/failed) · reasoned/skipped` out of the runnable snippets the engine found.

### 1. Deep Learning Frameworks — ✅ 88 · ran 5/8 runnable (5 passed, 0 failed) · 3 reasoned
- `commands_work 5 · content_accuracy 4 · completeness 3 · clarity 5 · structure 4 · safety 5` (weight covered 1.0)
- **Passed (run for real):** Linux venv+install path; Chapter 1 tensor create/reshape/broadcast/matmul/device; Chapter 2 autograd on `y = 3w² + 2w` → `w.grad = 26.0` (matches the quest's `# 26.0`); Chapter 3 full PyTorch training loop (nn.Sequential, MSELoss, Adam, 200 epochs) → loss falls to the ~0.01 floor exactly as the quest claims.
- **Reasoned (not executed):** macOS/Windows setup blocks; Colab CUDA check; the TensorFlow/Keras `Sequential` — it is only compiled (`model.fit(...)` is commented out).
- **Observed defect:** the Keras stub `Dense(16, activation="relu", input_shape=(1,))` "triggers a real deprecation warning under the installed TF 2.21/Keras 3 — the current recommended pattern is an explicit `keras.Input(shape=(1,))`."
- **Completeness gap:** the secondary objective *"Datasets & Loaders — batch data efficiently with `DataLoader`"* never appears in the body; *"Framework Fluency … compare"* is half-delivered because the TF model is never trained/compared.

### 2. Computer Vision — ✅ 89 · ran 6/7 runnable (6 passed, 0 failed) · 4 reasoned
- `commands_work 5 · content_accuracy 4 · completeness 4 · clarity 4 · structure 5 · safety 5`
- **Passed (run for real):** venv + `pip install torch torchvision …`; `import torch, torchvision` check; Chapter 1 `F.conv2d` edge detector on a 5×5 image; Chapter 2 full SmallCNN train/eval on FashionMNIST (2 epochs) → **~87% test accuracy**; Chapter 3 ResNet-18 transfer setup (freeze backbone, replace `fc`, 2 trainable tensors).
- **Reasoned:** Linux/macOS/Windows/Colab alternate setup blocks.
- **Observed friction:** "`pip install torch torchvision` as given pulls the full CUDA/GPU build on Linux … verified in the sandbox this downloaded ~4.8 GB including nvidia-cublas, nvidia-cudnn, triton, nccl … even though the quest states a GPU is [optional]."
- **Completeness gap:** two secondary objectives — *Data Augmentation* and *Confusion Analysis* — are named as masteries and reappear as explicit Mastery-Challenge requirements, but no body code teaches them.
- Note the engine confirmed CV uses the **current** weights API (`models.ResNet18_Weights.DEFAULT`), not the deprecated `pretrained=True` — good.

### 3. Natural Language Processing — ⚠️ 71 · ran 8/7 runnable (7 passed, **1 failed**) · 2 reasoned, 1 skipped
- `commands_work 3 · content_accuracy 3 · completeness 4 · clarity 4 · structure 4 · safety 5`
- **Passed (run for real):** venv + `pip install transformers torch scikit-learn numpy` (installed **transformers 5.13.1, torch 2.13.0**); Chapter 1 tokenization → `['[CLS]', 'transformers', 'revolution', '##ized', 'natural', 'language', 'processing', '.', '[SEP]']`; Chapter 2 embeddings → similar pair **0.892**, unrelated **0.606** (matches the `# high`/`# low` comments); all three Mastery Challenges (tokenize-and-count, semantic search, two-model comparison) validated.
- **FAILED (witnessed):** the Chapter 3 pipeline block — the sentiment half worked (`[{'label': 'POSITIVE', 'score': 0.9987…}]`), but the next line crashed:
  > `TypeError: TokenClassificationPipeline._sanitize_parameters() got an unexpected keyword argument 'grouped_entities'` — on transformers 5.13.1, the version the quest's own `pip install transformers` installs.
  The engine **confirmed the fix** by re-running with `aggregation_strategy="simple"`, which produced the expected grouped-entity (ORG/LOC) output.
- **Skipped:** the Linux `sudo apt` setup line.

### 4. MLOps Engineering — ❌ not evaluated (engine reached max turns) · no verdict, no scores
- `walk-evidence.json` carries **no `verdict_obj`** for this quest — only an error. Verbatim tail:
  > `claude exited 1: … "command":"curl -s http://127.0.0.1:8000/health; … curl -s -X POST http://127.0.0.1:8000/predict …"} … "terminal_reason":"max_turns" … "errors":["Reached maximum number of turns (40)"]`
- **Interpretation (honest):** the engine was actively standing up the Chapter 2 FastAPI service and calling `/health` + `/predict` (the Intermediate "Serve and Call" challenge) when it exhausted its 40-turn budget. This is a **harness limit, not evidence of a content defect** — I have **no** command result for MLOps and score it `reasoned`-only below. It should be re-run with a higher `--max-turns`.

### 5. AI Ethics — ✅ 89 · ran 5/6 runnable (5 passed, 0 failed) · 1 reasoned, 1 skipped
- `commands_work 5 · content_accuracy 4 · completeness 3 · clarity 5 · structure 5 · safety 5`
- **Passed (run for real):** macOS/Linux/Cloud install paths (`fairlearn scikit-learn pandas numpy`); Chapter 1 fairness-audit script (per-group accuracy + gap); Chapter 2 permutation feature-attribution on `load_breast_cancer` + RandomForest.
- **Reasoned:** Chapter 3 model-card text block. **Skipped:** Windows PowerShell path.
- **Observed defects:** Fairlearn is billed as the headline tool but "no runnable snippet ever imports or uses Fairlearn beyond the [install] verification"; the *"Conflicting Fairness"* secondary objective and *"Just Arbiter"* badge are asserted but never taught; and the Chapter 1 definition *"equalized odds (is the model equally accurate for each group?)"* is imprecise — "equalized odds formally requires equal true-positive and false-positive rates across groups, not equal overall accuracy."

## 🐞 Issues Found

Grouped by severity. Every item cites witnessed sandbox output or a quoted quest line; MLOps items are flagged `reasoned` because no command result exists for that quest.

**HIGH**
- **NLP · Chapter 3 code block · `pipeline("ner", grouped_entities=True)`** — *Observed:* crashes with `TypeError: … unexpected keyword argument 'grouped_entities'` on transformers 5.13.1, which the quest's own unpinned `pip install transformers` installs; a learner following the quest today gets a crash instead of the printed entity output. *Fix:* replace `grouped_entities=True` with `aggregation_strategy="simple"` (engine verified this produces the expected ORG/LOC output).

**MEDIUM**
- **NLP · all environment-setup blocks** — *Observed:* the code was written against the older `grouped_entities` API but the install pins no version. *Fix:* pin a compatible floor (e.g. `transformers>=4,<5` or an explicit version) or add a note that pipeline kwargs change across major versions.
- **Deep Learning Frameworks · Chapter 3 / Objectives** — *Observed:* the "Framework Fluency … compare" primary objective is half-delivered (Keras model compiled but `model.fit(...)` commented out, never trained/compared) and the "Datasets & Loaders / `DataLoader`" secondary objective has zero body content. *Fix:* either train+compare the Keras model or soften the objective wording; add a short `DataLoader` example or drop the objective.
- **Computer Vision · setup blocks** — *Observed:* `pip install torch torchvision` downloaded ~4.8 GB of CUDA packages in the sandbox despite the quest saying a GPU isn't needed. *Fix:* offer the CPU wheel index (`--index-url https://download.pytorch.org/whl/cpu`) or warn about the download size.
- **Computer Vision · Secondary Objectives / Mastery Challenges** — *Observed:* "Data Augmentation" and "Confusion Analysis" are promised masteries and required in challenges but never taught in the body. *Fix:* add minimal `transforms`/confusion-matrix snippets, or mark those challenges as stretch goals.
- **AI Ethics · headline tooling** — *Observed:* Fairlearn is installed and named as the core tool but `MetricFrame` is only described in prose; no example uses it. *Fix:* add one short `MetricFrame` snippet so the tool the quest installs is actually exercised.
- **MLOps · Chapter 2 "Serve and Call" challenge** — *(reasoned)* The engine timed out precisely on launching + curling the FastAPI server, which signals this is a long, multi-step, stateful challenge (start `uvicorn`, wait, POST a 30-feature vector, hit `/health`). *Fix (for authoring):* nothing proven broken, but consider a copy-paste one-liner or a note that the server must run in a second terminal; **for the walkthrough harness**, re-run MLOps with a higher `--max-turns`.

**LOW**
- **NLP · Chapter 2 embeddings** — *Observed:* loading `AutoModel.from_pretrained("distilbert-base-uncased")` prints harmless `UNEXPECTED` key-mismatch messages (dropped MLM head). *Fix:* one-line note so beginners don't mistake it for an error.
- **NLP · "Fine-Tuning vs Prompting" secondary objective** — *Observed:* only 1–2 narrative sentences, no runnable example. *Fix:* add a short decision checklist or code contrast.
- **Deep Learning Frameworks · Keras stub** — *Observed:* `Dense(…, input_shape=(1,))` raises a Keras 3 deprecation warning. *Fix:* use an explicit `keras.Input(shape=(1,))` layer.
- **Deep Learning Frameworks · Windows path** — *Observed:* never mentions the common `Activate.ps1` execution-policy error. *Fix:* one-line note about `Set-ExecutionPolicy`.
- **AI Ethics · Chapter 1 definition** — *Observed:* "equalized odds … equally accurate for each group" is imprecise. *Fix:* define it as equal TPR **and** FPR across groups.

## 🔗 Chain Continuity

**As a linked learning path, this window holds together well for the two quests that build directly on each other, and is coherent for the rest given the windowing.**

- **Prerequisite satisfaction inside the window is good for the "middle" of the chain.**
Deep Learning Frameworks (quest 1) `unlocks` Computer Vision, NLP, and MLOps, and both **Computer Vision** and **NLP** list *deep-learning-frameworks* as their **required** prerequisite — which the learner completes first in this exact plan order. So a learner walking 1→2→3 arrives at CV and NLP with precisely the tensors + four-beat training-loop foundation those quests assume. Continuity here is clean.
- **MLOps and AI Ethics reach back to `ml-fundamentals`, which is *outside* this window.**
Both `require: /quests/1101/ml-fundamentals/` (and DLF `requires: neural-networks`, also outside the window). This is **expected** for a windowed sweep (window 1 of 2, quests 5–10 of 10) — the ledger accumulates the lower quests separately — but a learner who literally started at this window would be missing the scikit-learn "train + evaluate a model" grounding that MLOps/AI-Ethics assume. Worth noting, not a defect of these files.
- **Ordering is sensible.** The `unlocks` graph (DLF → {CV, NLP, MLOps}; CV/NLP → {MLOps,
AI-Ethics}; MLOps → AI-Ethics; AI-Ethics ends the line) is consistent with the plan's linear order, and AI Ethics correctly presents itself as the capstone/conscience of the level. No forward-reference or circular-dependency problems surfaced.
- **Character-relevance gap (medium, spans the whole slice).** This is the **Game Developer**
path, yet all five quests are generic Data-Science/ML content (`categories: [Quests, Data-Science, …]`) with **no game-development framing** — no mention of game AI, NPC behavior, procedural content, RL agents, or in-engine inference. More concretely, every quest's **"Character Class Recommendations"** block lists only *Software Developer*, *System Engineer*, and *Data Scientist* — the **Game Developer class is never named**, so a learner arriving on this path gets no next-step guidance for their own class. A real game-dev beginner would reasonably wonder why "Level 1101" for their track is a straight ML curriculum. Recommend either adding a Game-Developer recommendation line or a short game-facing "why this matters for games" hook per quest.
- **Continuity friction a real beginner would hit:** (1) the NLP NER crash breaks the very
"run a pretrained transformer on your own text" objective mid-chapter; (2) the ~4.8 GB CV install would stall a bandwidth-limited learner right at quest 2; (3) MLOps front-loads a serve-and-curl exercise heavy enough that even the automated engine ran out of turns.

## 🧠 Reasoning & Method

- **Mode:** `execute` (sandboxed), consumed from the **pre-sealed** `walk-evidence.json` /
`walk-evidence.md`. Per the skill's step 2, I did **not** run the engine myself (its child `claude` processes can't authenticate from the agent's Bash tool) and did **not** modify `walk-plan.json` or the evidence files. Engine cost for this slice: **$2.7908**.
- **What I ran vs. reasoned:** I ran no quest commands myself — all `passed`/`failed`
outcomes above are the engine's actual sandbox executions, quoted from the evidence. I **read all five quest sources in plan order** and reasoned about the linked journey (prerequisites, ordering, character relevance, beginner friction) in §6. Anything I could only judge statically is labeled `reasoned` (notably **all** of MLOps and the alternate-OS setup blocks the engine chose not to run).
- **Coverage / limits (honest):**
  - **4 of 5 quests scored; MLOps was NOT evaluated** — the engine hit `max_turns: 40` while
    standing up the FastAPI service, so there is no MLOps verdict, no per-dimension scores,
    and no snippet tally. I did **not** invent one; its row is `—` and its issues are
    `reasoned`.
  - This is **window 1 of 2** (5 of the level's 10 quests). I walked exactly the planned
    window and did not expand to the other window or other characters.
  - Snippet coverage was partial by design: the engine ran one representative OS setup path
    per quest and reasoned about the others, and skipped `sudo apt` lines in a couple quests.
    Totals: DLF 5/8 ran, CV 6/7, NLP 8 (1 failed), Ethics 5/6.
- **Confidence:** **High** on the four scored quests — findings are backed by real,
reproducible sandbox output (and the NLP fix was independently verified by the engine). **Low** on MLOps — no execution evidence exists; its "fail" reflects a harness timeout, and the maintainer should re-run it before drawing any content conclusion.
- **Deliverable:** this single report. No quest content was edited; no branch/commit/PR was
  made. The workflow handles git. **STOP.**

---

### Appendix — machine evidence (verbatim excerpt from `walk-evidence.md`)

> **4** quests evaluated · ✅ 3 pass · ⚠️ 1 warn · ❌ 1 fail · avg **84.2%** · ~$2.7908
>
> - ✅ 88 — Deep Learning Frameworks — 5/8 snippets
> - ✅ 89 — Computer Vision Mastery — 6/7 snippets
> - ⚠️ 71 — Natural Language Processing — 8/7 (1✗)
> - ❌ — — MLOps Engineering — `claude exited 1 … "terminal_reason":"max_turns" … Reached maximum number of turns (40)`
> - ✅ 89 — AI Ethics — 5/6 snippets
