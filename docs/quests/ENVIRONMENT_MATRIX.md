# Quest Environment Matrix — the refactoring plan

**Goal:** a quest should read as if it were written for the machine you are sitting at. The environment a quest assumes — OS, shell, editor, package manager, the folder its commands create — becomes **declared data** instead of prose, so it can be *rendered* for the reader, *configured* by them, and *matrixed over* by the testing framework.

## The problem this fixes

A typical quest documents four platform paths:

```markdown
### 🍎 macOS Kingdom Path      ### 🪟 Windows Empire Path
### 🐧 Linux Territory Path    ### ☁️ Cloud Realms Path
```

Three of those four are never useful to any given reader, and nothing about them is machine-readable. Concretely, before this refactor:

- **Readers** scrolled past instructions for operating systems they do not run, then mentally substituted their own folder name for the one the quest picked.
- **The testing framework** had to *guess* which snippets applied to the sandbox it was running in — heading-regex inference, re-derived per tool.
- **Nothing could tell** whether a quest claimed a Windows path it did not actually provide.

## The contract

Quests declare an `environment:` block in frontmatter (registered in `quest_registry.py` as an optional structured field):

```yaml
environment:
  os: [macos, windows, linux, cloud]   # the paths this quest actually provides
  shell: [zsh, bash, powershell]       # shells its commands are written for
  variables:
    project_dir: css-quest             # the folder its commands create
  requires:                            # optional, human-facing
    - git >= 2.30
```

The **axes** — their labels, icons, options and per-OS defaults — live once in `quest_registry.py` (`ENVIRONMENT_AXES`) and are published to the site as `_data/quests/environments.yml` by `make quest-data`:

| axis | options | default follows |
|---|---|---|
| `os` | macos · windows · linux · cloud | detected from the browser |
| `shell` | zsh · bash · powershell · fish | the OS (macOS→zsh, Windows→PowerShell, Linux/Cloud→bash) |
| `editor` | vscode · vim · nano · jetbrains | vscode |
| `pkg` | brew · apt · winget · choco · none | the OS (macOS→brew, Linux→apt, Windows→winget, Cloud→none) |

Variables are declared per quest and defined once in `ENVIRONMENT_VARIABLES` (currently `project_dir`).

## What it does for each audience

**Readers** get a visible control at the top of the quest (`_includes/quest/quest-env.html` + `assets/js/quest-env.js`). It detects their OS on first visit, shows only the platform path that matches, rewrites every snippet to the folder name they type, and remembers the choice across quests in `localStorage`. With JavaScript off, every path stays visible exactly as before.

**The testing framework** resolves an environment the *same* way the browser does — declaration → registry default → explicit override — in `quest_steps.py`:

```bash
python3 scripts/quest/quest_steps.py pages/_quests/0001/css-styling-basics.md \
    --env os=windows,shell=powershell        # walks the Windows path
python3 scripts/quest/quest_steps.py pages/_quests/0001/css-styling-basics.md \
    --env os=macos,project_dir=my-css-lab    # zsh + brew, folder substituted
```

Each resolution yields a different step plan from the same quest: the applicable steps change, and the declared variables are substituted into the commands — so the sandbox runs exactly what a reader on that machine would read. `stack_capture.mjs` then walks that plan and photographs it (see `VIDEO_FRAMEWORK.md`).

**Validation** gains a question it could not previously ask: does a quest's declared `os` list match the sections it actually contains? (`env_migrate.py` derives the answer; a future `quest_audit` check can gate on it.)

## The migration

`scripts/quest/env_migrate.py` derives the block from what each quest already contains — no prose is rewritten:

- **OS paths** from the platform headings it documents.
- **Shells** from its own fenced-block languages (plus zsh when it has a macOS path).
- **`project_dir`** from the folder its commands create (`mkdir -p ~/css-quest`, `mkdir $HOME\css-quest`).

```bash
python3 scripts/quest/env_migrate.py pages/_quests            # dry run
python3 scripts/quest/env_migrate.py pages/_quests --apply    # write
```

It is idempotent and conservative: a path is claimed only when the quest really documents it, and a hand-tuned `environment:` block is never overwritten without `--force`.

**Applied:** 122 quests gained the block. 83 quests correctly have none — they are conceptual (no platform instructions to vary).

### The rendering bug the migration exposed

Fenced code inside `<details>` was **not being parsed at all**. Kramdown does not process markdown inside a raw HTML block unless the element carries `markdown="1"`, so every collapsed platform snippet rendered as literal backticks rather than a highlighted, copyable code block — on every quest using the convention. The same migration pass repairs it (`fix_details`), which also makes those snippets real `<code>` elements the environment control can rewrite.

## Rollout status

| Phase | State |
|---|---|
| Axis vocabulary in the registry + generated site data | ✅ done |
| `environment:` frontmatter contract + migration tool | ✅ done (122 quests) |
| `<details markdown="1">` repair | ✅ done (same pass) |
| Reader-facing control (detect / filter / substitute / remember) | ✅ done |
| Environment-aware step planning + variable substitution | ✅ done |
| Environment-aware sandbox capture + video | ✅ done via `stack_capture.mjs` |
| CI matrix walking every declared OS path per quest | ⏭️ next — the planner already accepts `--env`; the workflow needs a matrix axis |
| `quest_audit` check: declared paths ⇄ documented sections | ⏭️ next |
| Authoring: new quests declare `environment:` from the template | ⏭️ next (template + `quest.instructions.md`) |

## Design notes

- **One source of truth.** The axes exist once, in the registry. The frontmatter contract, the generated data file, the rendered control and the step planner all read it; none of them re-declare the vocabulary.
- **Detection is data, not magic.** The keyword table that maps a heading to an OS is mirrored deliberately in `env_migrate.py` and `quest-env.js` so page and tooling classify a section identically.
- **Substitution is idempotent.** Both the browser and the planner rewrite from the *original* text every time, so toggling values can never compound.
- **Nothing is hidden from the reader by default.** With no selection (or no JS), every path shows — the control narrows, it never conceals content the reader did not ask to hide.
