# Repository chronicle

> Reads every commit of any Git repository once, files the facts in a ledger, asks a model only for what needs judgement, and builds a time-lapse presentation of how the repository grew.

The chronicle is the whole-history companion to the [digs](../README.md). A dig reads one bounded range closely. The chronicle reads every commit and presents the whole arc: a file-system time-lapse, a page-by-page front-end time-lapse, a library time-lapse of every article by topic and learning path, the stack's evolution, the eras, their transitions and the lessons the record supports. It works on any repository with a Git history. It was first applied to `bamr87/it-journey` and `bamr87/zer0-mistakes`.

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
| `content` | every mainline version of every article (`git cat-file --batch`) | `content/versions/`, `content/taxonomy.json`, `content/topics/`, `content/paths.json` | a model: one topic taxonomy per repository, one topic per article |
| `frames` | page sources at sampled commits | `frames.json`, screenshots in `.cache/` | none |
| `build` | the ledger and the frames | the presentation in `.cache/` | none |
| `video` | the built presentation | `video/filesystem.mp4`, `video/frontend.mp4`, `video/library.mp4` | none |

`run` performs the first six in order; `--video` adds the last. Every step can run on its own.

## Read once, filed for retrieval

The ledger lives at `docs/git-archaeology/chronicle/<owner>/<repo>/` and is committed, so a later run on any machine starts where the last one stopped. Its format is documented in [the ledger README](../../../docs/git-archaeology/chronicle/README.md).

- A commit is read once. `ingest` asks Git only for commits the ledger has not filed; a closed month's shard never changes.
- A commit is annotated once. `annotate` asks the model only for commits with no reading. A deterministic `heuristic` reading, written when no model is available, is upgraded the next time one is; a model's reading is never replaced.
- The era reading is keyed by a hash of its input digest. It is read again only when the history it summarises has changed, or with `eras --force`.
- An article version is read once, keyed by commit and path. The topic taxonomy is designed once and kept until `content --force`; each article is filed under a topic once per taxonomy, and a heuristic filing is upgraded when a model is available.
- Frames are cached by commit and path in `.cache/chronicle/`, which is gitignored and rebuilt from the ledger and Git on a fresh clone.

A re-run with nothing new reads no commit, makes no model call, renders no frame and leaves the ledger byte-identical.

## AI

Model calls go through `claude -p` (Claude Code, the fleet's local route; authenticated by the session or `CLAUDE_CODE_OAUTH_TOKEN`), with no tools, a replaced system prompt, an empty working directory and a `--max-budget-usd` cap per call. Defaults: `claude-haiku-5-5` for commit annotations (40 commits per call, 4 calls at a time) and article topics (60 articles per call), `claude-opus-5-5` for the era reading and the topic taxonomy. Override with `--model`, `--budget`, or `CHRONICLE_COMMITS_MODEL`, `CHRONICLE_ERAS_MODEL`, `CHRONICLE_TAXONOMY_MODEL`, `CHRONICLE_TOPICS_MODEL`. `--ai off` uses the deterministic fallbacks: the conventional type for a commit, years for eras, the collection for a topic.

Answers are validated before they are filed. An unknown kind, a missing commit or unparseable output falls back to the heuristic reading for those commits. An era that cites a commit the digest did not contain loses the citation, and eras are made contiguous over the observed months. The presentation marks every model-written passage as an AI reading and keeps computed numbers apart from it. Commit text is passed as data, with an instruction never to follow it.

The first full runs cost about $0.41 API-equivalent (estimate) to annotate 2,622 commits, $0.48 for the two era readings, and under $0.30 to design IT-Journey's taxonomy and file its 1,120 articles. The manifest keeps a running estimate.

## The library time-lapse

An article is a content page: a Markdown or HTML file in a Jekyll collection (`_quests`, `pages/_notes`…), a plain content folder (`docs/`), or the root (`index.md`). Theme, tooling and agent files are not articles. The `content` step reads every mainline version of every article once and keeps its front matter: title, tags, categories, quest `level` and `quest_type`, description, word count. Replaying those versions gives each article a lifeline (born, revised, moved, retired). An article keeps its identity across a rename Git detected, and across a delete and an add in one commit when the title or file name matches. On IT-Journey the replay reproduces the 487 article files at HEAD exactly.

The deck's Library section plays those lifelines week by week: every live article as a dot, grouped by topic and colored by collection, with that week's new and retired articles beside it. Below it, the quest level grid (`0000` to `1111` by quest type) and the learning paths from `_data/quests/paths.yml` fill in as quests appear; the paths are drawn as they are declared at HEAD. Then live articles by collection, and one small chart per topic with its oldest article. The level grid appears for any repository whose articles carry a binary `level`; the paths appear when the repository has a paths file.

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
| `content.py` | Articles: the once-per-version front-matter reader, lifelines, the topic taxonomy and filing, learning paths |
| `frames.py`, `shot.mjs` | Page choice, the source renderer, the Playwright screenshots |
| `present.py`, `templates/deck.html` | The presentation: data assembly and the page (vanilla JS, no build step) |
| `video.mjs` | Steps the presentation's players for the MP4 export |
| `test_chronicle.py` | Tests against a synthetic repository |

Requirements: Python 3.10+ with PyYAML and Pillow, Git, Node with Playwright (screenshots and video), ffmpeg (video only), the `claude` CLI (model readings only). Python-Markdown renders Markdown frames when installed; a small built-in renderer is used otherwise.
