# Repository chronicle

> Reads every commit of any Git repository once, files the facts in a ledger, asks a model only for what needs judgement, and builds a time-lapse presentation of how the repository grew.

The chronicle is the whole-history companion to the [digs](../README.md). A dig reads one bounded range closely. The chronicle reads every commit and presents the whole arc: a file-system time-lapse, a page-by-page front-end time-lapse, the stack's evolution, the eras, their transitions and the lessons the record supports. It works on any repository with a Git history. It was first applied to `bamr87/it-journey` and `bamr87/zer0-mistakes`.

## Run it

```bash
python3 scripts/digs/chronicle/chronicle.py run --repo ../zer0-mistakes            # everything, incrementally
python3 scripts/digs/chronicle/chronicle.py run --repo . --video                   # plus MP4 time-lapses
python3 scripts/digs/chronicle/chronicle.py status --repo ../zer0-mistakes         # what the ledger holds
python3 scripts/digs/chronicle/chronicle.py show 7b01447 --repo .                  # one commit's record and reading
python3 scripts/digs/chronicle/test_chronicle.py                                   # tests (no network, no model)
make chronicle CHRONICLE_REPO=../zer0-mistakes                                     # the same run, from make
```

The repository must be a full clone (`git fetch --unshallow` on a shallow one), because the chronicle reads history Git has not fetched as missing. The presentation lands in `.cache/chronicle/<owner>__<repo>/presentation/`: open `index.html` from disk, or publish the folder (`page.html` is the same page without a document shell, for hosts that add their own).

## Pipeline

| Step | Reads | Writes | Judgement |
| --- | --- | --- | --- |
| `ingest` | `git log --raw --numstat`, blob sizes | `commits/YYYY-MM.jsonl` in the ledger | none |
| `annotate` | the ledger's commit records | `annotations/YYYY-MM.jsonl` | a model: kind, area, one-line summary, significance, themes |
| `eras` | a month-by-month digest of the ledger | `eras.json` | a model: eras, transitions, hindsight lessons with cited commits |
| `frames` | page sources at sampled commits | `frames.json`, screenshots in `.cache/` | none |
| `build` | the ledger and the frames | the presentation in `.cache/` | none |
| `video` | the built presentation | `video/filesystem.mp4`, `video/frontend.mp4` | none |

`run` performs the first five in order; `--video` adds the sixth. Every step can run on its own.

## Read once, filed for retrieval

The ledger lives at `docs/git-archaeology/chronicle/<owner>/<repo>/` and is committed, so a later run on any machine starts where the last one stopped. Its format is documented in [the ledger README](../../../docs/git-archaeology/chronicle/README.md).

- A commit is read once. `ingest` asks Git only for commits the ledger has not filed; a closed month's shard never changes.
- A commit is annotated once. `annotate` asks the model only for commits with no reading. A deterministic `heuristic` reading, written when no model is available, is upgraded the next time one is; a model's reading is never replaced.
- The era reading is keyed by a hash of its input digest. It is read again only when the history it summarises has changed, or with `eras --force`.
- Frames are cached by commit and path in `.cache/chronicle/`, which is gitignored and rebuilt from the ledger and Git on a fresh clone.

A re-run with nothing new reads no commit, makes no model call, renders no frame and leaves the ledger byte-identical.

## AI

Model calls go through `claude -p` (Claude Code, the fleet's local route; authenticated by the session or `CLAUDE_CODE_OAUTH_TOKEN`), with no tools, a replaced system prompt, an empty working directory and a `--max-budget-usd` cap per call. Defaults: `claude-haiku-5-5` for commit annotations (40 commits per call, 4 calls at a time), `claude-opus-5-5` for the era reading. Override with `--model`, `--budget`, or `CHRONICLE_COMMITS_MODEL` / `CHRONICLE_ERAS_MODEL`. `--ai off` uses the deterministic fallback for both.

Answers are validated before they are filed. An unknown kind, a missing commit or unparseable output falls back to the heuristic reading for those commits. An era that cites a commit the digest did not contain loses the citation, and eras are made contiguous over the observed months. The presentation marks every model-written passage as an AI reading and keeps computed numbers apart from it. Commit text is passed as data, with an instruction never to follow it.

The first full runs cost about $0.41 API-equivalent (estimate) to annotate 2,622 commits and $0.48 for the two era readings. The manifest keeps a running estimate.

## The front-end time-lapse is a simulation

Pages are chosen from the ledger: the home page (`permalink: /`, else a root `index.*`, else the README), followed back through every file that served `/`; the README; and the most-revised content pages. Each page is followed through its renames, and its mainline versions are sampled (18 per page by default).

Each frame is rendered from that commit's own source: the Markdown or HTML, its front matter, the site title and navigation from that commit's `_config.yml` and `_data/navigation/`, its stylesheets and images. Liquid tags are reduced to labelled placeholders. The page is drawn in a neutral shell, so a frame shows what the source said, not what the historical build looked like: no theme gem or remote theme is resolved. Playwright takes each screenshot with every network request blocked.

## Files

| File | Holds |
| --- | --- |
| `chronicle.py` | The command line |
| `core.py` | Git helper, paths, the ledger and its manifest |
| `facts.py` | Deterministic readings: language and layer by path, actor, conventional type |
| `ingest.py` | The once-per-commit Git reader |
| `replay.py` | Rebuilds the tree at any mainline commit from the ledger; the weekly frames of the file-system film |
| `ai.py` | The model route, commit annotations, the era reading, the heuristic fallback |
| `frames.py`, `shot.mjs` | Page choice, the source renderer, the Playwright screenshots |
| `present.py`, `templates/deck.html` | The presentation: data assembly and the page (vanilla JS, no build step) |
| `video.mjs` | Steps the presentation's players for the MP4 export |
| `test_chronicle.py` | Tests against a synthetic repository |

Requirements: Python 3.10+ with PyYAML and Pillow, Git, Node with Playwright (screenshots and video), ffmpeg (video only), the `claude` CLI (model readings only). Python-Markdown renders Markdown frames when installed; a small built-in renderer is used otherwise.
