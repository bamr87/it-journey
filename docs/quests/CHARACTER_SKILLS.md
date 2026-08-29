# Character Skills — per-path voices and exercises for the quest-perfection loop

The quest-perfection loop always works one **(character, level) slice**: the walk lane (`quest-walkthrough` skill → `quest-walker` agent) plays it as a learner, and the fix lane (`quest-fix` skill → `quest-fixer` agent) repairs what the walk witnessed. Until now "as a learner of this character class" was a single sentence of instruction; the **character skills** make it a real, versioned contract — one skill per character path, holding the persona, the voice, the per-level exercise checkpoints, and the friction lens for that path.

## The files

One skill per `_data/quests/paths.yml` entry, named by the path key:

```
.claude/skills/quest-character-<key>/SKILL.md     # developer, system-engineer,
                                                  # security-specialist, data-scientist,
                                                  # digital-artist, game-developer
```

Each skill has the same shape, so the fleet reads them uniformly:

| section | consumer | content |
|---|---|---|
| Who you are playing | walk lane | the persona: background, starting knowledge, what costs this learner confidence |
| Path roadmap | both | **generated** — the path's levels/themes/tiers/XP from paths.yml + the registry |
| Voice | walk lane | the character's fantasy dialect for *report narration*, plus the two-layer voice rule |
| Walk lens | walk lane | character-specific friction checks beyond the generic rubric |
| Per-level exercises | both | per level on the path: competence checkpoints to verify + what fixes must preserve |
| Fix lens | fix lane | which repairs serve this learner; guardrails against flavor injection |
| Hard rules | both | data sources, precedence, and the never-expands-scope clause |

## How the loop consumes them

Agents in the loop have no `Skill` tool — they **`Read`** the file. The resolution is deterministic: `walk-plan.json` carries `character.key`, and the sheet lives at `.claude/skills/quest-character-<character.key>/SKILL.md`.

- **Walk lane** — `quest-walkthrough` step 3 now starts by putting on the character
sheet: role-play the persona while chain-reading, verify the level's exercise checkpoints, judge continuity against them, and narrate the session report in the character's dialect. A missing sheet is noted in the report's method section, never a failure.
- **Fix lane** — `quest-fix` step 3 reads the sheet before the first edit: the fix
lens ranks repairs by what serves this path's learner, and the per-level "preserve" lists guard against score-gaming deletions. The sheet informs edit *choice* only — the M-rules (smallest edit, deterministic keep/revert, content-only surface) are unchanged and always win.

## The two-layer voice rule

Levels are **shared** across paths (level `0100` is walked by developer, digital-artist, and game-developer alike), so quest *content* keeps the one neutral `quest-fantasy` brand voice (`_data/brand/voice.yml`, `_data/brand/sections/quest.md`). The character dialect (forge-and-craft, wards-and-watch, atelier-and-canvas, …) colors only the **walkthrough report's narration** and the judgment of fit. Every sheet states this rule, because the failure mode it prevents is real: a fix lane that rewrites shared quests into one class's flavor degrades them for the other five paths.

## Consistency machinery (why the sheets can't drift)

The facts in a sheet come from the same sources the planner resolves slices from, and a generator keeps them mechanically identical:

- `scripts/quest/character_skills.py` regenerates each sheet's **roadmap block**
(between `<!-- BEGIN GENERATED: character-roadmap -->` markers) from `_data/quests/paths.yml` + `scripts/quest/quest_registry.py`. Everything outside the markers is hand-authored and never touched.
- `--check` verifies: every path has a sheet, no orphan sheets for removed paths,
roadmap blocks are byte-fresh, the authored exercises cover exactly the path's levels (one `### … Level <code>` heading each), and the frontmatter `name:` matches the directory.
- `make quest-skills` (regenerate) / `make quest-skills-check` (verify);
`quest_audit.py` runs the same check as its **non-gating `skills` layer** — advisory because the audit's PR triggers don't watch paths.yml, so a gating check could red an unrelated content PR. Drift heals with one make target.
- Deliberately **not** part of `make quest-data`: the fix lane runs quest-data and
  must never write `.claude/**` (fix PRs stay content-only, M4).

## Changing the paths

Adding, removing, or re-leveling a character in `paths.yml`:

1. Edit `_data/quests/paths.yml` (it is curated, not generated).
2. Run `make quest-skills` — stale roadmaps regenerate; a new path is reported as a
   missing sheet.
3. For a new path, author the sheet by copying an existing one's section skeleton,
then write the persona/voice/lenses and one exercises heading per level; `make quest-skills` fills the roadmap and `make quest-skills-check` proves coverage.
4. A removed path's sheet is reported as an orphan — delete the directory.

## What this deliberately is not

- **Not one skill per quest.** ~230 per-quest files would drift with every content
PR; the concrete quest list already reaches every run through `walk-plan.json`, and quest-grain expectations live in the per-level exercise checkpoints.
- **Not a workflow change.** The loop's workflows already say "use the
quest-walkthrough / quest-fix skill"; the sheets ride in through those skills' step 3, so nothing under `.github/workflows/` moved.
- **Not new authority.** A sheet never expands an agent's writable surface, never
overrides `quest.instructions.md`, the brand guides, or an M-rule, and never outranks `walk-plan.json` on what the slice contains.
