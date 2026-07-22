---
name: content-curator
description: Run one agentic, on-brand content-improvement pass for a single IT-Journey collection and open one gated PR. The Lane B (substantive) executor that wires the cms-curator loop to the brand-voice system. Use when asked to "improve a collection", "run the content factory", or driven by content-factory.yml in CI.
---

You are running **one substantive content-improvement pass** for a single collection. This skill is deliberately thin: it **composes two skills you already have** — [`cms-curator`](../cms-curator/SKILL.md) for the loop mechanics and [`brand-voice`](../brand-voice/SKILL.md) for how the writing must read — and adds the per-collection, open-one-PR discipline the `content-curator` agent and `.github/workflows/content-factory.yml` rely on.

It ends in **exactly one pull request** (or a clean no-op with a reason), never an open-ended rewrite.

---

## 0. Inputs

- **`COLLECTION`** — one of `quests · docs · notes · quickstart · about` (the loose
  `pages/` root counts as `root`). You improve only this collection this run.
- Auth + model come from the runner (`scripts/ai/run.sh` + `_data/ai.yml`); you
  don't manage them.

## 1. Orient (delegate to cms-curator §1)

```bash
make cms-all            # refresh .cms/index + today's worklist
make cms-status         # health dashboard
```

Open `.cms/worklists/<YYYY-MM-DD>.md` and read **Lane B (substantive)** rows whose path is in your `COLLECTION`. That is your candidate set. Also read the policy files cms-curator §0 lists (`.cms/config.yml`, the per-collection `.github/instructions/*.instructions.md`, `_data/brand/`).

## 2. Load the voice (delegate to brand-voice)

Run the **`brand-voice`** skill for `COLLECTION` so the section's profile, values, and `_data/brand/glossary.yml` are loaded before you write. The arc is **zer0 → her0**; teach, don't hype.

## 3. Pick exactly one target

- Dedup first: `gh pr list --state open --label auto:content --json title,headRefName`.
  If your best candidate already has an open PR, take the next.
- Prefer the **lowest health / most drift** Lane B item for the collection. If Lane
B is dry, pick the weakest existing page in the collection (lowest cms health) and improve that — **never silently no-op**.

## 4. Improve it (the real work)

Apply cms-curator §"Lane B" judgment plus the brand-voice bar:

- Tighten prose; fix structure; add a concrete "you'll know it worked when…".
- Normalize frontmatter to CI constraints (title 30–60, description 120–160,
ISO-8601 dates, YAML-list tags/categories). Reuse `make content-normalize-apply` for mechanical bits — don't hand-fix what a fixer handles.
- Kill drift: `python3 scripts/ci/brand_lint.py <file>` must come back clean
  (fix `preferred` spellings and replace `discouraged` hype with specifics).
- Honesty rule: every command/output/link is real and verified.

## 5. Verify (delegate to cms-curator §validate)

```bash
make prose-oneline-apply               # unwrap soft-wrapped prose (the 'oneline' gate)
make content-audit                     # frontmatter + network
# quests only:
make quest-data && make quest-audit
```

**One paragraph per line.** Write body prose as a single unwrapped line per paragraph — never soft-wrap at ~80 cols. The `markdown-oneline` CI gate fails any PR with wrapped prose, so run `make prose-oneline-apply` after you edit (it only joins prose; code/tables/Liquid/front-matter are left untouched) and stage the result.

Do not open a PR that fails. Fix or shrink scope until green.

## 6. Open exactly one PR

```bash
git switch -c content/curator-<COLLECTION>-<short-slug>
# commit with a Conventional-Commits message: content(<COLLECTION>): <what>
gh pr create --label auto:content --label collection/<COLLECTION> \
  --title "content(<COLLECTION>): <concise what>" \
  --body "<what changed + why, the brand_lint result, and any infra fix you could NOT make (out of scope)>"
echo "<pr-url>" > pr-result.txt
```

Then **STOP**. One collection, one PR, minimal diff. Never merge; the gate and the auto-merge workflow decide. Never touch `.github/**`, `.claude/**`, `scripts/**`, `_config*.yml`, `_data/brand/**`, `.cms/**`, or dependencies — flag those in the PR body instead.
