# Dig scripts

`candidates.py` reads the fleet registry and published digs. It lists eligible `bamr87` repositories and ranges already covered. It does not choose the next target. The daily agent does that.

`validate_dig.py` checks one installment against the collection contract: owner, post-2020 range, full SHAs, commit cap, `voice_profile: git-dig`, and the Scope, Facts, Inferences, Limits, and Retrospective headings.

```bash
python3 scripts/digs/candidates.py ../../_data/projects.yml
python3 scripts/digs/validate_dig.py pages/_digs/2020-07-30-first-steps.md
```

[`chronicle/`](chronicle/README.md) reads a repository's whole history once, files every commit in a ledger under `docs/git-archaeology/chronicle/`, and builds a time-lapse presentation of its growth, eras and lessons.

```bash
python3 scripts/digs/chronicle/chronicle.py run --repo ../zer0-mistakes
```
