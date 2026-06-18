# CMS extension — now **zer0-CMS** (separate repo)

The VS Code CMS extension for IT-Journey is **[zer0-CMS](https://github.com/bamr87/zer0-CMS)**
— a fork of [Front Matter CMS](https://github.com/estruyf/vscode-front-matter)
(MIT) extended with the IT-Journey AI layer.

It is **not** built in this repo. It only **consumes the contract this repo
emits**: the `.cms/` directory produced by `scripts/cms/cms.py` (content index,
schema, daily report, and the mechanical/substantive worklist). See
[`.cms/README.md`](../../.cms/README.md) for that contract.

## What zer0-CMS adds on top of Front Matter

- Content-health insight sourced from `.cms/`.
- Embedded Claude Code agents (the `cms-curator` skill) with an approve/deny
  diff gate. The AI modules live in `src/zer0/` of the zer0-CMS repo.

## History

An earlier standalone prototype lived here at `tools/cms-extension/`. Its working
AI modules (the Claude agent runner + the `.cms` contract loader) were salvaged
into zer0-CMS (`src/zer0/`), and the prototype was removed. See the zer0-CMS
repo's `FORK.md` and `src/zer0/README.md` for the design and integration plan.
