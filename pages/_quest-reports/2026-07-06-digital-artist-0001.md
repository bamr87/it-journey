---
title: Digital Artist · L0001 · 2026-07-06
description: Quest-perfection walkthrough of the Web Fundamentals slice digital-artist/0001 on 2026-07-06,
  engine verdict fail. An evidence-based, learner's-eye…
date: '2026-07-06T00:00:00.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- Digital Artist
tags:
- digital-artist
- level-0001
- walkthrough
- quest-perfection
- fail
- web-fundamentals
render_with_liquid: false
excerpt: 'Digital Artist · Level 0001 — Web Fundamentals: an evidence-based quest-perfection walkthrough
  from 2026-07-06.'
slice: digital-artist/0001
character: digital-artist
level: '0001'
theme: Web Fundamentals
tier: Apprentice
verdict: fail
quest_count: 5
walk_date: '2026-07-06'
run_url: https://github.com/bamr87/it-journey/actions/runs/28791022929
source_report: test/quest-validator/walkthroughs/2026-07-06-digital-artist-0001.md
---

> **Slice** `digital-artist/0001` · **Level** 0001 (Web Fundamentals) · **Apprentice tier** · **Engine verdict** ❌ fail · **Walked** 2026-07-06
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/28791022929) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-06-digital-artist-0001.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-06-digital-artist-0001.md)

---

## 🎯 Session Summary

I walked a **5-quest window** (window 3 of 6, offset 15) of the **Digital Artist →
Level 0001 · Web Fundamentals** slice — 3 main quests and 2 side quests, played in
dependency order in the disposable runner sandbox via the sealed execute-engine
evidence. **Headline verdict: FAIL.** The two core, fully-scored main quests both
fail on `commands_work` (Stats Portal **48%**, Terminal Mastery **44%**) because
their centerpiece commands crash or silently no-op when a learner runs them
verbatim; the third main quest (**Forge Your Character**), which is the *linchpin
prerequisite* for both side quests, produced **no verdict at all** (engine hit
max-turns), so the chain's most load-bearing quest is unverified. The two side
quests (Avatar Forge **79% warn**, Badge Collector **66% warn**) are structurally
sound but both silently assume a cloned, `bundle install`ed repo with a generated
contributor data file that no quest in the slice actually walks the learner through.

The dominant, repeating failure mode across this slice is **assumed-but-unprovided
state**: scripts with real bugs (Stats Portal), directories/files referenced before
they're created (Terminal Mastery), and repo/toolchain prerequisites stated only
implicitly (the whole Contributor Path). A maintainer acting on this report should
prioritize the three verified Ruby-script bugs in Stats Portal and the Chapter-3
state bug in Terminal Mastery — both are concrete, reproduced, and block a
first-time learner immediately.

## 🗺️ The Journey

Plan order (dependency-sorted; `walk-plan.json`):

1. ❌ **Forging the Stats Portal: Data Analytics Quest** — 48% — Solid template &
   structure, but the centerpiece Ruby generator has **3 verified bugs** that crash
   or empty it on the first run.
2. ❌ **Terminal Mastery: Conquering the Command-Line Realm** — 44% — Individually
   accurate commands, but a Chapter-2 state bug breaks half of Chapter 3, several
   examples reference never-created files, and Process Management (a stated
   objective) is untaught.
3. ❌/⚠️ **Forge Your Character: Crafting Your Contributor Identity** — *no score*
   (engine reached max-turns; verdict errored) — reasoned about statically below;
   this is the required prerequisite for both side quests.
4. ⚠️ **Avatar Forge: Crafting Your Digital Portrait** — 79% — Short, low-risk,
   all snippets technically correct; weakness is missing `bundle install` and no
   way to verify the "fallback still works" step.
5. ⚠️ **Badge Collector: Showcasing Your Achievements** — 66% — Internally
   consistent, but both runnable commands failed in-sandbox for lack of a stated
   repo/data-file prerequisite.

Aggregate: **0 pass · 2 warn · 3 fail · avg 59.2%** (4 scored, 1 errored).

## 🔬 Evidence

All statuses below are from commands the sealed execute engine actually ran in a
disposable sandbox (`walk-evidence.json`), unless labelled `reasoned`.

### 1. Stats Portal — `pages/_quests/0001/stating-the-stats.md` — ran 5/5 runnable (3✔ 2✗), 9 reasoned
Dimensions: commands_work **1** · content_accuracy **2** · completeness **3** ·
clarity **3** · structure **4** · safety **5**.

- ❌ `ruby scripts/generation/generate_statistics.rb` — **failed**: `NoMethodError:
  undefined method 'iso8601' for Time` — the script (line 271, `Time.now.iso8601`)
  requires only `'yaml'` and `'date'` (lines 256-257), never `'time'`.
- ❌ Script body — **failed** on two further bugs once the first is patched:
  `@site_root = File.expand_path('../..', __FILE__)` (line 264) resolves to
  `scripts/` not the repo root (the file is two dirs deep → needs `'../../..'`),
  causing `Errno::ENOENT` on `File.write`; and `YAML.safe_load($1)` (line 329)
  raises `Psych::DisallowedClass: Tried to load unspecified class: Date` for any
  post with an unquoted `date:` field — silently rescued per-post (lines 332-334),
  so the script reports **`Total posts: 0`**.
- ✅ `update_statistics.sh` — **passed** once the Ruby script was fixed.
- ✅ `pages/stats.md` Liquid/Bootstrap template — **passed** (built with Jekyll
  4.4.1 against generated data): categories/tags loops, tag-cloud sizing, `first`
  on a Hash, and the freshness-badge epoch math all rendered correctly.
- `reasoned`: `{​{ ... | number_with_delimiter }​}` (line 539) is **not** a real
  Jekyll/Liquid filter — verified against jekyll-4.4.1's filters.rb; Liquid
  silently no-ops it, so "Total Words" renders unformatted.

### 2. Terminal Mastery — `pages/_quests/0001/terminal-mastery.md` — ran 18/21 runnable (9✔ 9✗), 1 reasoned
Dimensions: commands_work **2** · content_accuracy **2** · completeness **2** ·
clarity **2** · structure **4** · safety **3**.

- ✅ Worked cleanly: `whoami`/`pwd`, `ls`/`ls -la`/`ls -lah`, `tree`, `ls -R`,
  `mkdir -p` with brace expansion, `touch`, `echo`/heredoc redirects, `wc`/`wc -l`,
  the `ls|grep|wc` pipelines, and the Novice/Apprentice/Expert challenge scaffolds.
- ❌ **State bug (root cause):** Chapter 2 Step 3 runs `mkdir -p projects/...`
  *before* `cd terminal-practice`, so `projects/` lands as a **sibling** of the
  workspace. Consequently Chapter 3 Step 2 `cp -r projects/ backup-projects/` —
  **failed** ("cannot stat 'projects/'").
- ❌ `mv quest-backup.md backups/`, `mv *.css styles/`, `cp -i important-file.txt
  backup/` — **failed**: `backups/`, `styles/`, `backup/`, and `important-file.txt`
  are never created earlier in the quest.
- ❌ Chapter 4 `grep "terminal" learning-notes.txt` — **failed (no match, exit 1)**
  even though the quest created `learning-notes.txt` — the file capitalizes
  "Terminal" and grep is case-sensitive. This is the *one* grep example run against
  a real quest-created file, and it silently fails to demonstrate its own claim.
- ❌ `tail -f logfile.txt`, `grep -r "function" projects/`, `grep -n "error"
  logfile.txt`, etc. — **failed**: referenced files/dirs never created.
- ❌ "Expected Output Example" fenced ` ```bash ` block whose first line is
  `$ ls -lah` — **failed** verbatim: `$: command not found` (exit 127).
- Completeness gap (reasoned + confirmed by engine): "Process Management" is a
  stated Primary Objective and completion-checklist item but is **never taught** —
  the only `ps` appearance is one incidental `ps aux | grep "node"` line.

### 3. Forge Your Character — `pages/_quests/0001/forge-your-character.md` — **NO VERDICT (engine errored)**
The engine reached its 40-turn max and exited non-zero (`errors: ["Reached maximum
number of turns (40)"]`) with a `permission_denials` entry on a
`curl … http://localhost:4444/` probe. **There is no per-dimension score, no
snippet coverage, and no command evidence for this quest** — its `overall: 0.0` is
an *engine error sentinel, not a content fail*. Everything I say about it below is
`reasoned` from the source only.

- `reasoned`: Steps are coherent and RPG-framed (clone → data file → class →
  profile page → `make contributor-stats` → `bundle exec jekyll serve` → PR). I
  confirmed (read-only, host repo) that every asset it references exists:
  `_data/contributors/_template.yml`, `pages/_about/contribute/contributors/_template`,
  `scripts/generation/generate_contributor_stats.{rb,sh}`, and a `contributor-stats`
  Makefile target — so the machinery is real.
- `reasoned` friction: Step 5 jumps straight to `bundle exec jekyll serve` with **no
  `bundle install`** shown; a fresh clone will error. Same missing-`bundle-install`
  gap the two side quests inherit.

### 4. Avatar Forge — `pages/_quests/0001/side-quest-avatar-forge.md` — ran 4/2 (4✔ 0✗)
Dimensions: commands_work **4** · content_accuracy **4** · completeness **3** ·
clarity **4** · structure **4** · safety **5**.

- ✅ Both YAML avatar snippets (GitHub `.png` URL and repo-relative path) — valid.
- ✅ `mkdir -p assets/images/contributors && cp /path/to/your/avatar.png …` —
  **passed** (mechanics correct; `/path/to/...` is an obvious placeholder).
- ✅ `bundle exec jekyll serve` — **passed** as a command form.
- Weaknesses (reasoned): no `bundle install` for a fresh clone; the checklist item
  "Fallback still works if image fails to load" has no concrete way to verify.

### 5. Badge Collector — `pages/_quests/0001/side-quest-badge-collector.md` — ran 3/2 runnable (0✔ 3✗), 2 reasoned
Dimensions: commands_work **2** · content_accuracy **3** · completeness **4** ·
clarity **4** · structure **5** · safety **5**.

- ❌ `make contributor-stats USERNAME=YOUR_USERNAME` — **failed** in-sandbox: no
  cloned/`bundle install`ed repo and no existing contributor data file.
- ❌ `cat _data/contributors/YOUR_USERNAME.yml` — **failed**: file doesn't exist
  (it is produced by the prerequisite quest, not this one).
- ❌ `bundle exec jekyll serve` — **failed**: same missing prerequisite.
- `reasoned`: the threshold pseudocode block and the `badges_pinned` YAML snippet
  are internally consistent with the achievement catalog and the pinning rules.

## 🐞 Issues Found

**High severity**

- **high** · Stats Portal · `scripts/generation/generate_statistics.rb` line ~256 ·
  *Observed:* first run crashes `NoMethodError: undefined method 'iso8601' for Time`.
  *Fix:* add `require 'time'`.
- **high** · Stats Portal · same script, line 264 · *Observed:* `File.expand_path('../..', __FILE__)`
  resolves to `scripts/`, causing `Errno::ENOENT` on `File.write` to a nonexistent
  `_data/`. *Fix:* use `'../../..'` (file is two dirs below repo root).
- **high** · Stats Portal · same script, line 329 · *Observed:* `YAML.safe_load($1)`
  raises `Psych::DisallowedClass: Date` on unquoted `date:` frontmatter (Ruby
  3.1+/Psych 4), silently dropping every post → `Total posts: 0`. *Fix:*
  `YAML.safe_load($1, permitted_classes: [Date, Time])` (or `unsafe_load` for
  trusted local content).
- **high** · Terminal Mastery · Chapter 2 Step 3 / Chapter 3 Step 2 · *Observed:*
  `projects/` created as a sibling of `terminal-practice` (mkdir before `cd`), so
  `cp -r projects/`, `mv *.css styles/`, `mv quest-backup.md backups/`,
  `cp -i important-file.txt backup/` all fail. *Fix:* `cd terminal-practice` first
  (or `mkdir -p` the target dirs), and create the referenced sample files/dirs.
- **high** · Terminal Mastery · Chapter 4 Step 2 · *Observed:* `grep "terminal"
  learning-notes.txt` returns no match because the file capitalizes "Terminal".
  *Fix:* use `grep -i "terminal"` or lowercase the sample text.
- **high** · Badge Collector · Steps 1 & 3 · *Observed:* `make contributor-stats`
  and `bundle exec jekyll serve` both fail with no cloned/`bundle install`ed repo +
  contributor data file. *Fix:* state the prerequisite explicitly (not only via the
  wiki-link footer) — cloned repo, `bundle install`, and a data file from Forge
  Your Character.

**Medium severity**

- **medium** · Stats Portal · `pages/stats.md` line 539 · `number_with_delimiter`
  is not a real Liquid/Jekyll filter (verified: silently no-ops). *Fix:* drop it or
  supply a real custom filter / manual formatting.
- **medium** · Stats Portal · Chapter 2 objective vs. content · objective claims
  "Generate statistics during Jekyll build process" but only manual invocation is
  shown. *Fix:* wire a real build hook/Rake/CI step, or soften wording.
- **medium** · Terminal Mastery · completeness · "Process Management" is a stated
  objective and checklist item but is never taught. *Fix:* add a chapter covering
  `ps`/`top`/`kill`/`jobs`, or remove the objective.
- **medium** · Terminal Mastery · illustrative ` ```bash ` blocks ("Expected Output
  Example", "Special directory symbols") error when pasted. *Fix:* fence as plain
  text or mark "sample output — do not run".
- **medium** · Terminal Mastery · hard-coded `Expected output: bamr87` /
  `/home/bamr87`. *Fix:* use `<your-username>` placeholders.
- **medium** · Avatar Forge · Step 4 · no `bundle install`; no way to test the
  "fallback still works" checklist item. *Fix:* add `bundle install` and a concrete
  fallback test (e.g., point avatar at a broken URL, confirm identicon).

**Low severity**

- **low** · Stats Portal · Knowledge Check asks about a `sort` filter in the
  categories loop, but no `sort` filter is used there (sorting is Ruby-side).
- **low** · Terminal Mastery · macOS-only `cd /Users/username/...` in a
  cross-platform chapter; `ps aux | grep node` self-match gotcha unmentioned.
- **low** · Avatar Forge · clarify `/path/to/your/avatar.png` is a placeholder;
  note commit/push is what makes the avatar live.
- **low** · Badge Collector · clarify `YOUR_USERNAME` placeholder; document what
  happens if a learner pins >3 or an unearned badge.

*This is not an empty result — there are real blocking issues, concentrated in the
two core main quests.*

## 🔗 Chain Continuity

**The window mixes two unrelated series.** Quest 1 (Stats Portal) is from the
*Jekyll Site Building / Development Mastery* line, while quests 3–5 form the
*Contributor Path: Identity & Recognition* arc; quest 2 (Terminal Mastery) is
standalone command-line. This is expected — the slice is a **date-rotated window
(3 of 6)** of a 26-quest level, not an authored chapter sequence — but it means a
learner walking *this window* does not experience one continuous storyline. For a
**Digital Artist**, Stats Portal (Ruby generator + Bootstrap/Liquid) is only
tangentially on-path; Terminal Mastery and the Contributor Path are the more
natural fit.

**The dependency ordering within the window is correct.** Terminal Mastery →
Forge Your Character → Avatar Forge / Badge Collector respects declared
`quest_dependencies`: Forge Your Character *recommends* Terminal Mastery (satisfied,
it comes first) and *unlocks* Avatar Forge + Badge Collector (both list Forge as a
`required_quest`, and both come after it). So the planner sequenced the linked
sub-chain sensibly.

**The load-bearing prerequisite is unverified and under-specified.** Forge Your
Character is the required predecessor for *both* side quests, yet the engine
produced **no verdict** for it (max-turns), so the one quest the chain most depends
on has zero machine evidence this run. Reading it as a learner, its machinery is
real (all referenced templates/scripts exist in the repo), but it is where the
chain's shared setup gap originates: **no quest in the slice ever runs
`bundle install`**, and neither side quest re-states the "cloned + installed repo +
generated data file" precondition except through a wiki-link footer. That gap is
exactly what the engine reproduced as the Badge Collector command failures — a real
beginner who starts at Badge Collector (or who skipped the implicit setup) gets
`make contributor-stats` / `jekyll serve` failures with no in-quest explanation.

**Where a real beginner gets stuck:**
- *Stats Portal:* dead on arrival at Chapter 2 — the generator crashes on run 1
  (`iso8601`), then writes to a bad path, then reports 0 posts. The "Expected
  Output: Total posts: 76" is unreachable following the steps verbatim.
- *Terminal Mastery:* fine through Chapter 2, then Chapter 3's copy/move demos start
  failing because the workspace state doesn't match what the text assumes.
- *Contributor Path:* the side quests are readable and correct in intent, but a
  learner who hasn't done a full clone + `bundle install` (never explicitly
  required) hits toolchain failures at the verify step.

## 🧠 Reasoning & Method

- **Mode:** `execute`. Evidence was **pre-computed and sealed** by the workflow's
  deterministic engine step; I consumed `walk-evidence.json` / `walk-evidence.md`
  **as-is** and did **not** re-run the engine (its child processes can't
  authenticate from the agent's Bash tool). I did not edit `walk-plan.json` or the
  evidence files, and I made no content edits.
- **What I ran vs. reasoned:** I ran nothing new against the quests. Every
  `passed`/`failed` in §Evidence comes verbatim from the sealed sandbox commands.
  The only commands I executed myself were **read-only existence checks** in the
  host repo (`ls`/`grep` for the contributor templates, scripts, and Makefile
  target) to strengthen the chain reasoning about Forge Your Character — those are
  labelled `reasoned`, not tested, and touched no content.
- **Coverage caps / honesty:**
  - **Quest 3 (Forge Your Character) has no score.** The engine hit its 40-turn
    limit and errored; I did not substitute a number. It is reasoned-only here, and
    its `overall: 0.0` should be read as an engine error, not a quality verdict.
    Re-running that single quest with a higher turn budget is the way to close this
    gap.
  - This is **window 3 of 6** (5 of 26 quests). The other 21 quests of Level 0001
    are out of scope for this run and are swept by other windows/days.
  - Long-running/interactive/system-mutating commands were `skipped` by the engine
    by design (Homebrew `curl|bash`, `wsl --install`, `apt/dnf upgrade`, `less`,
    `tail -f`, live dev-server + browser-open); coverage for the Stats template was
    obtained via a real `jekyll build` instead of an interactive serve.
- **Confidence:** High on the four scored quests — the high-severity issues are
  concrete, reproduced sandbox failures with exact error text, not inferences.
  Lower on Forge Your Character, which is reasoned-only due to the engine error.
  Overall session verdict **FAIL** is driven by the two failing core main quests
  plus the unverified linchpin prerequisite.
