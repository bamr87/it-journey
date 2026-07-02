---
name: quest-forge
description: Forge a "quest-forge proposal" GitHub issue into a complete, validated epic-quest campaign in pages/_quests/codex/ and open one gated PR. Use when asked to "forge a quest from an issue", turn an epic-quest proposal into content, or driven by quest-forge.yml in CI. Composes the deterministic collector (forge_issue.py) + quest.instructions + brand-voice.
---

You are running **one forge pass**: a single epic-quest proposal issue becomes one
pull request carrying a complete, audit-passing quest campaign. This skill is the
single source of loop behavior for both `/forge-quest` locally and the
`quest-forge.yml` CI workflow, so a maintainer and the runner forge identically.

It ends in **exactly one pull request** (or a clean no-op with a reason), never an
open-ended authoring spree.

---

## 0. Inputs

- **`ISSUE`** — the proposal issue number (e.g. `365`).
- Auth + model come from the runner (`scripts/ai/run.sh` + `_data/ai.yml`).

## 1. Collect (deterministic, before any prose)

```bash
python3 scripts/quest/forge_issue.py --issue "$ISSUE" --json /tmp/forge.json
gh issue view "$ISSUE" --json title,body,comments
```

`/tmp/forge.json` holds `chapters` (numeral, level, difficulty, xp, class, title),
`ledger` (PR # + squash-merge SHA per merged branch), and `badges`. **This manifest
is your only license to quote a PR number or commit hash.** Read issue comments too
— a proposal is often *updated* (a 10th chapter, a new badge) rather than re-filed.

## 2. Load the law and the voice

- **Structure:** `.github/instructions/quest.instructions.md` — required
  frontmatter (§1), permalink rules (§3, epic/bonus → `/quests/codex/<slug>/`),
  required body sections (§4), validation (§9). This governs; do not deviate.
- **Voice:** run the **`brand-voice`** skill for the `quests` section and read
  `_data/brand/sections/quest.md` — the `quest-fantasy` profile (gamified,
  encouraging, emoji-rich; technical accuracy intact under the fantasy wrapper).
- **Vocabulary:** `pages/_quests/codex/glossary.md` (`/quests/codex/glossary/`)
  — the canonical fantasy↔technical lexicon. Take names from it; never mint a
  synonym for a term it already names; a new coinage is added there first (same
  PR), then used in the quest.

## 3. Plan the campaign (placement + manifest)

Decide the file set **before** writing. The hub is the campaign's `epic_quest`
landing page; each chapter is a first-class `main_quest` placed at its **binary
level** so it also surfaces on that level's hub (the campaign should run *through*
the levels, not sit in one bucket):

| File | type | path | permalink |
|---|---|---|---|
| hub | `epic_quest` | `pages/_quests/codex/<campaign>.md` | `/quests/codex/<campaign>/` |
| chapter N | `main_quest` | `pages/_quests/<level>/<campaign>-NN-<slug>.md` | `/quests/<level>/<campaign>-NN-<slug>/` |

`epic_quest` MUST use the `/quests/codex/` URL namespace (validator rule — it is the
home of epic landing pages, not a lesser bucket). Each `main_quest` chapter lives in
the directory of its proposal binary `level:`, which must match that `level` field.
Map difficulty to the enum exactly (`🟢 Easy`/`🟡 Medium`/`🔴 Hard`/`⚔️ Epic`); map
`class` to a `skill_focus` enum value (`fullstack`/`devops`/`security`/
`data-engineering`/…) — there is no "digital-artist" focus, fold it into `fullstack`.
When a chapter's level theme differs from its topic (the proposal levels are a
difficulty signal), add one line noting the campaign uses the level for progression.

## 4. Wire the dependency graph (warning-free)

- **Hub** → `unlocks_quests`: every chapter codex permalink. `recommended_quests`:
  the prequel epic if one exists.
- **Chapters** → chain with `recommended_quests` (previous chapter) +
  `unlocks_quests` (next chapter). Keep `required_quests` empty or same-/lower-level
  only: the network validator warns when a `required` prerequisite sits at a *higher*
  level than the quest, and the campaign's narrative order is not level-ascending.
- Every referenced permalink must exist by end of the PR (you are creating them) or
  carry a `# planned quest` suffix (side-quests still living in lifehacker.dev).

## 5. Author each file (the real work)

Per quest, in order (quest.instructions §4):

1. Italic fantasy hook + real-world stakes.
2. `## 🎯 Quest Objectives` — `- [ ]` checkboxes (**required**; validator errors without it).
3. `## 🗺️ Quest Prerequisites` and `## 🌍 Choose Your Adventure Platform` where the topic is OS-dependent; every fenced block has a language tag.
4. **Chapters** with annotated code, knowledge checks, and a **"🔁 Reproduce it"**
   block linking the manifest's PRs/commits (`bamr87/lifehacker.dev#42`,
   `bamr87/lifehacker.dev@5853ef43b`) as the canonical reference build.
5. A Mermaid **network** diagram (prereq → this → unlocks).
6. `## 🎁 Rewards & Progression` aligned with frontmatter `rewards`
   (`progression_points` = chapter XP; `badges` from the manifest).
7. `## 🔮 Next Adventures` using canonical permalinks; `## 📚 Resource Codex`.
8. `## 🕸️ Knowledge Graph` footer with `[[wiki links]]` to the hub and neighbors.

**Liquid safety (load-bearing).** Jekyll runs Liquid *before* Markdown, so a code
fence does **not** protect `${{ … }}` / `{{ … }}` / `{% … %}`. Any code block or
inline span that shows GitHub Actions expressions or Liquid syntax MUST be wrapped
in `{% raw %}…{% endraw %}` (the convention 40+ existing quests already follow). An
unguarded `${{ A || B }}` is a Liquid syntax error that fails the required build —
and the validator only checks that `{% raw %}` pairs balance, not that every
expression is guarded, so the build is the real catch.

The **hub** additionally carries the quest-metadata table, the chapter index table
(links to every chapter), the badge roster, the boss-fight gate, and the full build
ledger table — quoted verbatim from the manifest.

## 6. Verify (do not skip)

```bash
make quest-data    # regenerate levels/tiers/order/network/navigation from the registry
make quest-audit   # content ≥70%, network integrity, freshness (must pass)
```

Fix every error before opening. `make quest-audit` SCORES every `main_quest`
chapter (each must clear 70%) and network-/freshness-validates the whole campaign.
The `epic_quest` hub lives in `codex/`, which tier-1 scoring skips — author it to the
full quest structure anyway. If the audit reports stale data, you forgot
`make quest-data`; run it and re-audit.

## 7. Open exactly one PR

```bash
# Dedup first — never a second PR for the same issue:
gh pr list --state open --label auto:quest --search "$ISSUE" --json number,title

git switch -c "quest/forge-issue-$ISSUE"
git add pages/_quests/codex _data/quests assets/data/quest-network.json
git commit -m "content(quests): forge epic quest from #$ISSUE"
gh pr create --label auto:content --label auto:quest --label automated \
  --title "content(quests): forge epic quest from #$ISSUE" \
  --body "$(printf 'Forged from #%s by the quest-forge skill.\n\n%s\n\nNever-merge: flows through quest-validation + content gates.' "$ISSUE" "$(python3 scripts/quest/forge_issue.py --issue "$ISSUE" --json /dev/stdout | python3 -c 'import json,sys;print(json.load(sys.stdin)["stats"])')")"
echo "<pr-url>" > pr-result.txt
gh issue comment "$ISSUE" --body "⚔️ Forged → <pr-url>. Review and merge to publish."
```

Then **STOP**. One issue, one PR, content-only diff (the smuggle guard in
`content-auto-merge.yml` will reject it otherwise). Never merge; never touch
`.github/**`, `.claude/**`, `scripts/**`, `_config*.yml`, `_data/brand/**`, `.cms/**`,
or deps — flag those in the PR body instead.
