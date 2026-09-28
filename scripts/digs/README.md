# Dig scripts

`candidates.py` reads the fleet registry and published digs. It lists eligible `bamr87` repositories and ranges already covered. It does not choose the next target. The daily agent does that.

`validate_dig.py` checks one installment against the collection contract: owner, post-2020 range, full SHAs, commit cap, `voice_profile: git-dig`, and the Scope, Facts, Inferences, Limits, and Retrospective headings.

```bash
python3 scripts/digs/candidates.py ../../_data/projects.yml
python3 scripts/digs/validate_dig.py pages/_digs/2020-07-30-first-steps.md
```
