---
mode: agent
description: "Review an AI conversation/PR and fold lessons back into instructions and prompts with citations"
date: 2026-05-18T17:21:39.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# 🔁 Retrospective: Close the AI Learning Loop

> **Mission**: Treat the AI agent's conversation as evidence. Extract every correction, course-change, and "we had to redo this" moment, then translate the most repeatable lessons into **small, citation-backed edits** to `.github/copilot-instructions.md`, the relevant `.github/instructions/*.md` files, and the responsible `.github/prompts/*.prompt.md` files — so the same mistake is harder to make next time.

This prompt is the deliberate counterpart to `/kaizen`: Kaizen improves *code and processes*; **Retrospective improves the instructions that guide future AI agents**. Used after every non-trivial session, it produces an ever-evolving, self-correcting prompt library.

## 🧭 Operating Philosophy

- **Evidence over opinion.** Every proposed instruction change must cite the exact turn, file, line, PR comment, or CI failure that motivated it.
- **Incremental over sweeping.** Prefer 3 small, surgical edits over one large rewrite. The instruction set should evolve, not be rewritten.
- **Generalizable over anecdotal.** Only promote a lesson into instructions if it would help on at least one *future, different* task. One-off fixes stay in the PR.
- **Citable over inferred.** Each new rule names the source PR/issue/file so future agents can audit where it came from.
- **Blameless.** The conversation is data. We are upgrading the *system*, not grading the agent.

## 📥 Intake

Before producing any output, confirm:

1. **Conversation source** — paste of the thread, a PR/issue number, or a path to a saved transcript. If only the current thread is available, summarize its full arc first (problem statement → actions taken → corrections → final state).
2. **Time-bounded** — limit analysis to the named conversation. Do not re-litigate older history unless the conversation explicitly references it.
3. **Scope** — instructions only, prompts only, or both (default both).
4. **Authority check** — confirm the agent has read:
   - `.github/copilot-instructions.md`
   - `.github/instructions/` (all `*.instructions.md` files relevant to the scope)
   - `.github/prompts/` (especially the prompt that was driving the failed session, if known)

If any of the above is missing, ask for it before proceeding.

## 🔬 Phase 1 — Mine the Conversation

Extract a structured ledger. Look specifically for these signals:

| Signal | Where it shows up | What it tells you |
|--------|-------------------|-------------------|
| User correction | "no, actually…", "we don't do it that way", "you forgot X" | A missing rule in the instructions |
| Self-correction | Agent reverts/rewrites its own output | The first attempt followed an unstated convention incorrectly |
| CI failure → fix loop | Validator/test failed, agent patched, repeat | The constraint isn't documented authoritatively |
| Re-asked question | Agent asks the same clarifier twice across sessions | Missing default in the prompt |
| Reviewer comment on PR | "this should be…" comments | A convention the prompt should have produced unprompted |
| Repeated reference to a file | Agent keeps re-discovering the same path/util | Worth adding to the relevant instruction's "Quick Reference" |
| Memory hit/miss | A `store_memory` fact that *should* have prevented the error | Memory exists but wasn't surfaced — promote to instructions |

Produce a numbered **Lesson Ledger** like this:

```markdown
### Lesson Ledger

| # | Observation (cite turn / file / line) | Generalizable? | Proposed home |
|---|---------------------------------------|----------------|---------------|
| 1 | Turn 4: agent set `description` to 92 chars; user pointed to validator's 120-char min (`scripts/validation/content-reviewer.py:138`) | Yes — affects all `pages/**` files | `copilot-instructions.md` Front Matter section |
| 2 | Turn 11: agent forgot `draft: false` on README at `pages/_quests/0000/README.md` | Yes — affects every quest README | `quest.instructions.md` checklist |
| 3 | Turn 17: agent re-asked "where is the Jekyll exclude list?" | Yes — chronic | Add anchor to `copilot-instructions.md` |
| 4 | Turn 22: one-off typo fix in a single post | **No** — leave in PR | — |
```

Aim for 3–8 ledger entries per retrospective. More than 8 usually means the analysis is too broad — split into multiple retrospectives.

## 🎯 Phase 2 — Triage Each Lesson

For every "Yes" row in the ledger, classify:

- **Tier A — Promote to `copilot-instructions.md`** if it applies across content types and tools (e.g., a CI-enforced rule, a security policy, a repo-wide convention).
- **Tier B — Promote to a specific `.github/instructions/<topic>.instructions.md`** if it applies to one collection or workflow (quests, posts, scripts, prompts, work directories, etc.).
- **Tier C — Patch the responsible `.github/prompts/<name>.prompt.md`** if the lesson is about *how the AI was asked* (missing constraint in the prompt, missing self-check step, missing default).
- **Tier D — `store_memory`** if it's user- or repo-specific context the next agent should remember but it doesn't yet warrant a documented rule.

Document the classification in a second table:

```markdown
### Triage

| Lesson # | Tier | Target file | Edit type |
|----------|------|-------------|-----------|
| 1 | A | `.github/copilot-instructions.md` | New row in Validated Frontmatter Constraints table |
| 2 | B | `.github/instructions/quest.instructions.md` | Add `draft: false` to README checklist |
| 3 | A | `.github/copilot-instructions.md` | Add quick-reference anchor |
```

## ✂️ Phase 3 — Generate the Minimal Edits

For each triaged lesson, produce a **surgical diff** the user can apply directly. Constraints:

- **Smallest possible change.** Prefer adding a single row/bullet over rewriting a section.
- **Cite the source.** Every new sentence or table row must reference the PR/issue/file/line that motivated it, in parentheses or a footnote — e.g. `(see PR #268)` or `(enforced by scripts/validation/content-reviewer.py:130)`.
- **No invented sources.** If you can't cite the conversation or a repo file, drop the lesson.
- **Preserve voice and structure.** Match the surrounding section's heading depth, list style, and tone.
- **Bump `lastmod`.** Every edited file needs its `lastmod` updated in the same diff.

Output each edit as a fenced block of the form:

````markdown
#### Edit 1 — `.github/copilot-instructions.md`
**Section:** Validated Frontmatter Constraints  
**Rationale:** Lesson #1; conversation turn 4; root cause of PR #267.

```diff
@@
 | `title` | **required** | 30–60 characters | `scripts/validation/content-reviewer.py:128-133` |
+| `title` (quest READMEs) | **required** | Same 30–60 char rule applies — README files under `pages/**` are processed by Jekyll (cause of PRs #264, #266, #268) | observed |
 | `description` | **required** | 120–160 characters (optimal 120–155) | ... |
```
````

## 🧪 Phase 4 — Validate the Proposed Edits

Before finalizing, run these sanity checks (and report them):

- [ ] **No duplication.** Does any proposed rule already exist verbatim or near-verbatim? If yes, *strengthen* the existing rule (add a citation or example) instead of adding a second copy.
- [ ] **No conflicts.** Does the new rule contradict anything in `copilot-instructions.md`, `AGENTS.md`, or another `.instructions.md`? If yes, reconcile explicitly.
- [ ] **Test against the conversation.** Replay the failed turns mentally with the new rule in place — would the rule have actually prevented the error?
- [ ] **Test against a different scenario.** Imagine one *unrelated* future task. Does the rule still make sense, or does it over-fit to this conversation?
- [ ] **Char budget.** Edits to `copilot-instructions.md` should add < 500 chars per retrospective unless a Tier-A rule truly demands more. The instruction set has gravity; bloat erodes it.
- [ ] **Citation completeness.** Every new sentence in the diff has a source.

## 📦 Phase 5 — Deliverable

Return a single retrospective report with these sections in this order:

```markdown
# Retrospective — <conversation identifier> — <YYYY-MM-DD>

## 1. Conversation Summary
2–4 sentences. Problem → actions → corrections → final state.

## 2. Lesson Ledger
(table from Phase 1)

## 3. Triage
(table from Phase 2)

## 4. Proposed Edits
(fenced diff blocks from Phase 3, one per Tier-A/B/C lesson)

## 5. Proposed Memories
(Tier-D items, formatted as `store_memory` tool calls with `fact`, `citations`, `scope`, `reason`)

## 6. Validation Report
(checklist from Phase 4, with pass/fail per item)

## 7. Discarded Observations
(One-off / non-generalizable items from the ledger, with one-line reason each — kept for transparency)

## 8. Suggested Next Retrospective Trigger
When should this be run again? (e.g., "after the next 5 PRs touching `pages/_quests/`", "if AI Content Review issues spike again")
```

## 🚦 Stop Conditions

Do **not** produce a retrospective when:

- The conversation contains zero corrections or course-changes (nothing to learn).
- All observations are Tier D — just call `store_memory` directly; don't ceremonially generate a retrospective.
- The conversation is < 5 turns and entirely successful.
- You cannot read the source files the diffs would touch (ask first; never propose blind edits).

## 🧱 Anti-Patterns (do not do these)

- ❌ Adding aspirational rules ("agents should be more careful") without a concrete check.
- ❌ Rewriting whole sections "for clarity" — that's a separate PR, not a retrospective.
- ❌ Promoting one user's stylistic preference into a repo-wide convention. Use `store_memory` with `scope: user` instead.
- ❌ Citing the conversation itself as the only authority. Cite the *code/CI/PR* that the conversation revealed.
- ❌ Touching files outside `.github/` (this prompt only edits instructions, prompts, and memories — not site content).
- ❌ Skipping the validation phase. An unchecked retrospective is just a wish list.

## 🔗 Related

- `.github/prompts/kaizen.prompt.md` — improves code/process; pair with Retrospective for full PDCA on AI sessions.
- `.github/instructions/prompts.instructions.md` — prompt engineering standards every proposed edit must respect.
- `.github/copilot-instructions.md` § Validated Frontmatter Constraints — example of a section that grew from prior retrospectives.

---

**Invocation:** `/retrospective` (optionally with `conversation_source: pr:<N>` or `path:<file>`).  
**Cadence:** Run after any AI session that produced ≥ 1 correction loop, after every multi-PR rework sweep, and on a standing weekly schedule for active repos.
