---
title: "Quest Walkthrough — Digital Artist · Level 0001 (Web Fundamentals)"
date: 2026-07-18T00:00:00.000Z
character: digital-artist
level: "0001"
theme: Web Fundamentals
tier: Apprentice
quest_count: 5
mode: execute
overall_verdict: fail
session:
  window: "3 of 6 (offset 15, size 5)"
  total_quests_in_level: 26
  evidence: walk-evidence.json
  engine_average: 61.4
  counts: { pass: 0, warn: 4, fail: 1 }
  cost_usd: 4.1662
---

## 🎯 Session Summary

I walked a **5-quest window** (window 3 of 6, offset 15) of the **Digital Artist → Level 0001 "Web Fundamentals" (🌱 Apprentice)** path, as sealed by `walk-plan.json`, and read every quest in plan order while consuming the pre-computed execute-mode evidence in `walk-evidence.json`. The engine ran the quests' safe commands for real in a disposable sandbox; I reasoned about the *linked journey* on top of that.

**Headline verdict: FAIL.** The engine returned 0 pass · 4 warn · 1 fail, average **61.4%**. The single hard fail is the opening main quest, **Forging the Stats Portal (45%)** — its two centerpiece artifacts (the Ruby stats generator and the `pages/stats.md` template) are **broken exactly as printed** and were reproduced as real failures in the sandbox, so a learner following it verbatim cannot complete it. The four warns share **one systemic defect**: every quest in the contributor arc assumes an already-cloned, `bundle install`-ed IT-Journey repo but never states it as a prerequisite or teaches the setup, so their verification commands (`bundle exec jekyll serve`, `make contributor-stats`) fail out of the box. Maintainer action: fix the three verified Ruby bugs + the `{% raw %}` artifacts in stating-the-stats, and add a shared "run this from your cloned, bundled repo" prerequisite block to the contributor quests.

## 🗺️ The Journey

Walked in `walk-plan.json` order:

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ❌ fail | Forging the Stats Portal: Data Analytics Quest | 45 | Solid pedagogy, but both centerpiece code artifacts are broken as printed (3 Ruby bugs + unstripped `{% raw %}` template). |
| 2 | ⚠️ warn | Terminal Mastery: Conquering the Command-Line Realm | 60 | Core nav/text commands run clean, but sequential cp/mv/rm/grep blocks break, and the claimed Process Management objective is never taught. |
| 3 | ⚠️ warn | Forge Your Character: Crafting Your Contributor Identity | 68 | File-copy/YAML/git steps check out; missing `bundle install`, an XP-vs-template inconsistency, and unverifiable real-repo scripts hold it back. |
| 4 | ⚠️ warn | Avatar Forge: Crafting Your Digital Portrait | 70 | Accurate facts, but assumes an unstated Jekyll/Bundler environment so the final verify command fails; placeholder path run verbatim errors. |
| 5 | ⚠️ warn | Badge Collector: Showcasing Your Achievements | 64 | Internally consistent catalog/thresholds, but both runnable commands fail against a clean sandbox lacking the never-stated repo prerequisite. |

## 🔬 Evidence

All outcomes below are from the sealed execute-mode run (`walk-evidence.json`, `weight_covered: 1.0` on every quest). Command labels (`passed`/`failed`/`skipped`/`reasoned`) are the engine's recorded status; I quote its findings, trimmed.

### 1. Forging the Stats Portal — 45% ❌ (ran 7/5 runnable snippets · 3✓ 4✗ · 2 skipped · 3 reasoned)

- **`failed` — ruby: `scripts/generation/generate_statistics.rb`** (the full generator, lines 252-408). Verified on Ruby 3.2.3:
  - `Time.now.iso8601` → `NoMethodError: undefined method 'iso8601' for Time` — the script only `require`s `yaml` and `date`, never `time` (the stdlib that defines `Time#iso8601`).
  - After patching that: `@site_root = File.expand_path('../..', __FILE__)` resolves one level too shallow (`<root>/scripts`, not `<root>`), so the output path `<root>/scripts/_data/…` doesn't exist → `Errno::ENOENT` on write. Needs `'../../..'`.
  - After patching that: `YAML.safe_load($1)` (Psych 5) raises `Psych::DisallowedClass: Tried to load unspecified class: Date` on normal unquoted Jekyll `date:` frontmatter, caught by the script's own rescue → posts silently dropped, `Total posts: 0`, no hard error surfaced. Needs `permitted_classes: [Date]`.
- **`failed` — bash: `update_statistics.sh` wrapper** — inherits all three failures because it just calls the broken script.
- **`failed` — markdown/liquid: `pages/stats.md` template** (lines 484-769). Rendered with the real Liquid gem (v5.13.0), the fenced block still contains its `{% raw %}…{% endraw %}` wrapper tags around every Liquid tag; copy-pasted as shown it renders literal `{% if site.data… %}` text instead of live data — a completely broken page. The quest never tells the learner to strip them.
- **`content_accuracy` finding:** `{{ … | number_with_delimiter }}` is a Rails helper, **not** a Jekyll/Liquid filter; Liquid silently ignores the unregistered filter, so the number renders unformatted (contradicting the implied behavior), and the "Create custom Liquid filters" mastery claim is never fulfilled.
- **`passed`:** the `_data/content_statistics.yml` example YAML and `_data/navigation.yml` example YAML both parse; `chmod +x … && ./update_statistics.sh` runs (the shell wrapper itself is valid). The `date`/`divided_by`/`times`/`minus`/`first` Liquid usages verify correct once fed correctly-shaped data.
- **`skipped`/`reasoned`:** `docker-compose up` / `bundle exec jekyll serve` / macOS `open` (no docker/gems, macOS-only) reasoned, not run; "Total posts: 76" Expected-Output block reasoned (it's the live-site number, not a general result).

### 2. Terminal Mastery — 60% ⚠️ (ran 15/21 · 11✓ 4✗ · 3 skipped · 3 reasoned)

- **`passed`:** Chapter 1 (`whoami`, `pwd`, `ls -la/-lah`, `tree`/`ls -R`), Chapter 2 Step 3 (`mkdir`/`mkdir -p`/`cd`), Chapter 3 Step 1 (`touch`/`echo >`/`cat` heredoc), Chapter 4 Steps 1 & 3 (`cat`/`less`/`head`/`tail`/`wc`; pipelines with `grep`/`wc`/`sort`), and both easy Mastery Challenges (Scavenger Hunt brace-expansion, Log Analysis heredoc) all ran cleanly.
- **`failed` — Chapter 2 Step 1:** `cd Documents` errors because `Documents` was never created earlier in the sequence.
- **`failed` — Chapter 3 Steps 2 & 3:** `cp *.js scripts/`, `cp -r projects/ …`, `mv … backups/`, `cp -i important-file.txt backup/`, `rm temp-file.txt`, `rm -rf old-project/` all reference targets/dirs the walkthrough never created — they read identically to the fully-sequential earlier blocks but break when followed in order.
- **`failed` — Chapter 4 Step 2:** `grep "terminal" learning-notes.txt` returns **no match** against the file the quest itself generated (the file's text is capitalized "Terminal"); needs `grep -i` or lowercased sample text.
- **Completeness finding:** the **Process Management** Primary Objective (and a requirement of the Master Challenge) is essentially untaught — no `ps`/`top`/`kill`/`jobs` chapter exists.
- **`skipped`:** the macOS/Windows/Linux setup paths (`curl | bash` Homebrew install, `wsl --install`, `sudo apt/dnf`) — correctly not executed in the sandbox. `reasoned`: expected-output transcripts and the Master Challenge (comments only).

### 3. Forge Your Character — 68% ⚠️ (ran 6/9 · 6✓ 0✗ · 5 skipped · 2 reasoned)

- **`passed`:** `cp _data/contributors/_template.yml …`, the YAML profile/stats/level template block, `cp -r …/_template …`, the README front-matter block, `cat …yml`, and the Step-6 git branch/add/commit sequence all verified against a faithful mock of the described repo structure. **Zero failed commands** — the cleanest quest in the slice.
- **`skipped`:** `git clone`, `make contributor-stats`, `bash/ruby generate_contributor_stats.*`, `bundle exec jekyll serve` — the real stats-generator scripts and Makefile target live in the it-journey repo the offline sandbox can't reach, so they couldn't be verified.
- **Content findings (reasoned):** Step 5 calls `bundle exec jekyll serve` with **no preceding `bundle install`** (a fresh clone has no gems); and the fresh template's `next_level_xp: 100` contradicts the documented formula `floor(log₂(xp/100))`, which puts the level-1 threshold at xp=200.

### 4. Avatar Forge — 70% ⚠️ (ran 4/2 · 2✓ 2✗ · highest score in slice)

- **`passed`:** both `profile: avatar:` YAML snippets (GitHub `.png` URL trick and repo-relative path) are valid.
- **`failed` — Step 3:** `mkdir -p assets/images/contributors && cp /path/to/your/avatar.png …` errors — `/path/to/your/avatar.png` is an unmarked placeholder run verbatim ("No such file").
- **`failed` — Step 4:** `bundle exec jekyll serve` fails outright (`bundle: command not found` in a clean sandbox) — the quest never states the "run from your cloned, `bundle install`-ed repo" prerequisite.

### 5. Badge Collector — 64% ⚠️ (ran 4/2 · 1✓ 3✗)

- **`passed`:** the `badges_pinned:` YAML block is valid and the badge catalog/threshold pseudo-code are internally consistent (verified matching).
- **`failed`:** `make contributor-stats USERNAME=…`, `cat _data/contributors/YOUR_USERNAME.yml` (the file doesn't exist without the forge step), and `bundle exec jekyll serve` all fail in a clean sandbox — same unstated repo/toolchain prerequisite as Avatar Forge.

## 🐞 Issues Found

Every item below is backed by a command actually run (`tested`) or an exact quoted line (`reasoned`). Grouped by quest, highest severity first.

1. **HIGH · Stating the Stats · `scripts/generation/generate_statistics.rb` (lines 252-408) · tested** — Script crashes/silently fails three ways as printed: missing `require 'time'` (NoMethodError on `Time.now.iso8601`), `File.expand_path('../..', __FILE__)` off-by-one path, and `YAML.safe_load` without `permitted_classes: [Date]` dropping every post. **Fix:** add `require 'time'`, use `'../../..'`, pass `permitted_classes: [Date]`. All three reproduced on Ruby 3.2.3 / Psych 5.
2. **HIGH · Stating the Stats · `pages/stats.md` code block (Ch.3 Step 1, lines 484-769) · tested** — The copy-pasteable template still carries `{% raw %}…{% endraw %}` wrappers around every Liquid tag; pasted verbatim it renders literal Liquid source. **Fix:** strip the raw wrappers from the fence, or explicitly instruct the learner to remove them before saving.
3. **MEDIUM · Stating the Stats · `number_with_delimiter` filter (line ~539) · tested** — Not a real Jekyll/Liquid filter; silently ignored, number renders unformatted; also leaves the "Create custom Liquid filters" mastery indicator unfulfilled. **Fix:** remove the filter or add a real custom-filter `_plugins/` step.
4. **HIGH · Terminal Mastery · Chapter 3 Steps 2 & 3 (cp/mv/rm blocks) · tested** — Reference `scripts/`, `backups/`, `styles/`, `backup/`, `important-file.txt`, `old-project/`, `*.js`, `*.css` never created earlier; break when followed in sequence. **Fix:** create the targets earlier, or clearly label the blocks as standalone syntax examples.
5. **HIGH · Terminal Mastery · Process Management objective · reasoned** — A Primary Objective + Master-Challenge requirement that no chapter teaches. **Fix:** add a chapter covering `ps`/`top`/`kill`/`jobs`/`df`/`free` before the Master Challenge.
6. **MEDIUM · Terminal Mastery · Chapter 4 Step 2 grep (line ~462) · tested** — `grep "terminal" learning-notes.txt` returns no match against the file the quest created (text is capitalized). **Fix:** use `grep -i` or lowercase the sample.
7. **HIGH · Forge Your Character · Step 5 (line ~283) · reasoned** — `bundle exec jekyll serve` with no preceding `bundle install`; a fresh clone has no gems. **Fix:** add a `bundle install` step + a link to an environment-setup guide.
8. **MEDIUM · Forge Your Character · XP formula vs. template (lines 187 & 355) · reasoned** — Template default `next_level_xp: 100` contradicts `floor(log₂(xp/100))` (level-1 threshold = 200). **Fix:** set the template default to 200 or correct the formula.
9. **HIGH · Avatar Forge · Step 4 verify (line ~128) · tested** — `bundle exec jekyll serve` fails with no stated prerequisite. **Fix:** state "run from the root of your cloned IT-Journey repo with `bundle install` done."
10. **MEDIUM · Avatar Forge · Step 3 cp (line ~120) · tested** — `/path/to/your/avatar.png` is an unmarked placeholder that errors when run verbatim. **Fix:** mark it `<path-to-your-local-avatar.png>` per the `YOUR_USERNAME` convention.
11. **HIGH · Badge Collector · Steps 1 & 3 (lines ~127, ~155) · tested** — `make contributor-stats` and `bundle exec jekyll serve` both fail without the never-stated cloned/bundled-repo context. **Fix:** add a one-line "run from the root of your IT-Journey checkout with `bundle install` done" prerequisite.
12. **LOW · Badge Collector · Step 3 verify · reasoned** — No profile-page URL is given (e.g. `http://localhost:4000/contributors/YOUR_USERNAME/`) nor a Ctrl+C stop note. **Fix:** state the URL and stop instruction.

## 🔗 Chain Continuity

Reading the five as one learner's path surfaced two structural observations the isolated per-quest scores don't capture:

- **The slice is a windowed cross-section, not a native chain.** `walk-plan.json` is window 3 of 6 (offset 15) over the 26-quest level, so it splices the standalone **Data Analytics arc** (Stating the Stats) next to the **Contributor Chronicles arc** (Forge Your Character → Avatar Forge → Badge Collector) plus the general **Terminal Mastery**. Quests 3→4→5 *are* a real declared chain (`forge-your-character` `unlocks` avatar-forge & badge-collector, both of which declare it `required`), and that sub-chain is coherent: Forge Your Character creates `_data/contributors/YOUR_USERNAME.yml`, and the two side quests edit exactly that file. Quests 1 and 2 are unrelated neighbors, not prerequisites — fine for a sweep, but a maintainer should read this as "5 quests audited," not "one 5-step journey."
- **A shared, unstated prerequisite is the dominant chain defect.** Forge Your Character (3) is the only contributor quest that walks the learner through fork/clone and file creation — yet it never runs `bundle install`, and its two dependents (4, 5) both jump straight to `bundle exec jekyll serve` / `make contributor-stats` assuming a fully provisioned repo. In the sandbox those commands failed for exactly that reason. So even a learner who completes quest 3 correctly is **not** left ready for 4 and 5 as written: the environment-setup rung is missing from the whole ladder. The single highest-leverage fix for this slice is a shared "Prerequisites: cloned + `bundle install`-ed repo" block referenced by all three contributor quests (and echoed in Stating the Stats, which also assumes a live Jekyll site it never sets up).
- **Ordering nit:** Forge Your Character lists Terminal Mastery as a *recommended* prior quest, which the window respects (2 before 3). Good — a learner hitting the git/`cp`/`cd` steps in quest 3 benefits from quest 2 first. But note quest 2 itself doesn't cleanly deliver the file-manipulation confidence it promises, because its own cp/mv blocks break mid-sequence (issue 4).

## 🧠 Reasoning & Method

- **Mode:** `execute` (real). I did **not** run the engine — I consumed the sealed, workflow-minted `walk-evidence.json` / `walk-evidence.md` as-is per the skill's step 2, and read all five quest sources in plan order for the linked-journey pass. `weight_covered` is 1.0 on every quest, so the engine exercised the full runnable weight of each.
- **What is `tested` vs `reasoned`:** every `passed`/`failed` above is a command the engine actually ran in its disposable sandbox (I quote its recorded status and findings). Items I label `reasoned` are ones the engine skipped/reasoned (network installs, docker/bundler-dependent serves, real-repo-only scripts) or that I judged statically from the quest text — I did not re-run or invent any of them.
- **Coverage caps / limits:** This is a **5-of-26 window** — I make no claim about the other 21 quests in Level 0001; the ledger accumulates those across runs. Genuinely un-run in-sandbox and therefore lower-confidence: anything requiring `bundle`/`docker`/`jekyll serve` or the real it-journey stats scripts (Forge Your Character's actual stat generation, all three quests' page renders) and the platform setup commands in Terminal Mastery. Confidence is **high** on the reproduced code bugs in Stating the Stats (concrete stack traces) and the broken sequential commands in Terminal Mastery; **medium** on the "missing prerequisite" warns, which are inferred from clean-sandbox failures plus the quest text rather than from a full end-to-end provisioned run.
- **Session cost:** $4.1662, 5/5 quests scored, 0 errored (per evidence meta).
- **Deliverable discipline:** one report, zero quest-content edits. Fixable bugs are in Issues Found for a content pass to action; I did not branch, commit, or open a PR — the workflow handles git.
