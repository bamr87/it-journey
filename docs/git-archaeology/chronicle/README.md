# Chronicle ledgers

> Every commit of a repository, read once and filed by the repository chronicle, with the model's reading of each kept apart from the facts.

Each directory here is one repository's ledger, written by [`scripts/digs/chronicle/`](../../../scripts/digs/chronicle/README.md). The ledger is the durable record of what the chronicle has read, so a re-run reads only what is new. Git objects remain the evidence; a ledger is a derived index of them. `docs/` is excluded from the Jekyll build, so none of this is published as a site path.

## Ledgers

| Repository | Ledger |
| --- | --- |
| `bamr87/it-journey` | [`bamr87/it-journey/`](bamr87/it-journey/manifest.json) |
| `bamr87/zer0-mistakes` | [`bamr87/zer0-mistakes/`](bamr87/zer0-mistakes/manifest.json) |

## Layout

| Path | Written by | Holds |
| --- | --- | --- |
| `manifest.json` | every step | Schema, repository, ref and head read, commit counts, tags, the AI prompt versions, the running cost estimate, the last 25 runs |
| `commits/YYYY-MM.jsonl` | `ingest` | One line per commit, sorted by commit time, in the UTC month it was committed |
| `annotations/YYYY-MM.jsonl` | `annotate` | One line per commit: the model's (or the heuristic's) reading |
| `eras.json` | `eras` | The era reading, its input hash, model, prompt version and cost |
| `frames.json` | `frames` | The pages chosen for the front-end time-lapse and the commit behind each frame |

## Commit record

Facts only, as Git stores them:

| Field | Meaning |
| --- | --- |
| `sha`, `parents` | Full commit id and parent ids |
| `author`, `author_id` | Author name; the first 10 hex of the SHA-1 of the lowercased author email (the email itself is not stored) |
| `committer`, `at`, `ct` | Committer name; author and committer timestamps (ISO 8601) |
| `subject`, `body` | The message; the body is capped at 1,500 characters |
| `mainline` | Whether the commit is on the first-parent chain of the ref read |
| `files` | One entry per changed path: `s` status (`A M D R C T`), `p` path, `o` old path on a rename or copy, `sim` similarity, `a`/`d` lines added and deleted (`null` for binary), `b` blob size in bytes after the change, `sub` for a submodule |
| `totals` | Files changed, lines added, lines deleted |
| `facts` | `actor` (`human`, `ai-assisted`, `ai`, `bot`, from the author and the trailers the commit carries), `conventional` type and scope, and per-language, per-area and per-layer counts `[files, added, deleted]` |

A merge commit is diffed against its first parent, so replaying the mainline records in order rebuilds the exact tree at any mainline commit.

## Annotation record

`sha`, `ct`, `pv` (prompt version), `model` (or `heuristic`), `kind`, `area`, `summary`, `significance` (0 trivial to 3 turning point), `themes`, `at`. These are interpretation. A summary describes what the commit's paths and message show; it is not a recovered motive.

## Query it

```bash
python3 scripts/digs/chronicle/chronicle.py show 7b01447 --repo .        # one commit, with its reading
python3 scripts/digs/chronicle/chronicle.py status --repo ../zer0-mistakes
cat docs/git-archaeology/chronicle/bamr87/it-journey/annotations/*.jsonl | python3 -c "import json,sys; [print(r['ct'][:10], r['sha'][:7], r['summary']) for r in map(json.loads, sys.stdin) if r['significance'] == 3]"
```
