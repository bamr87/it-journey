# Quest Walkthrough Video Framework

**The VIDEO lane of the quest-perfection loop:** turn a verified quest run into a side-by-side video — the rendered quest page on the left, the recorded sandbox terminal session on the right — publish it to YouTube, and reference it from the quest's own page. One artifact serves two goals: **video evidence** that the quest actually works as written, and **educational content** a learner can watch before (or instead of) reading.

```
                    ┌────────────────────── quest-video.yml (dispatch) ──────────────────────┐
                    │                                                                        │
 walkthrough_plan.py ──► walk-plan.json ──► agentic execute engine ──► walk-evidence.json    │
 (deterministic planner)                    (agentic_validate.py,      (sealed transcript:   │
        ▲                                    workflow-minted — the      commands + status +  │
        │ or: source_run_id reuses the      SAME engine + contract      detail per quest)    │
        │ sealed artifact of a              as quest-perfection.yml)          │              │
        │ quest-perfection run                                                ▼              │
        │                                              walkthrough_video.mjs (Playwright)    │
        │                                              ┌──────────────┬───────────────────┐  │
        │                                              │ quest page   │ terminal replay   │  │
        │                                              │ (live site,  │ (typed commands + │  │
        │                                              │ auto-scroll) │ ✓/✗/∅/~ outcomes) │  │
        │                                              └──────────────┴───────────────────┘  │
        │                                                   videos/<level>-<slug>.mp4        │
        │                                                   videos/manifest.json (chapters)  │
        │                                                              │                     │
        │                              video_manifest.py build ──► upload-plan.json          │
        │                              (title/description/chapters/tags — deterministic)     │
        └────────────────────────────────────────────────────────────────────────────────────┘
                                                                       │  publish: true + YOUTUBE_* secrets
                                                                       ▼
                                        youtube_upload.py ──► YouTube (unlisted) ──► uploads.json
                                                                       │
                                        video_manifest.py apply ──► quest frontmatter walkthrough_video:
                                                                    + .quests/videos.yml (catalog)
                                                                       │
                                        ONE `quest-video`-labeled PR ──► human review ──► merge
                                                                       │
                                        _includes/quest/quest-video.html embeds it on the quest page
```

## Why this design

The framework deliberately reuses the quest-perfection loop's architecture instead of inventing a recording rig:

- **The evidence already exists.** The perfection loop's execute engine (`test/quest-validator/agentic_validate.py --mode execute`) already plays each quest's commands for real in a disposable runner sandbox and records a per-quest transcript (`verdict_obj.commands[]`: command, status, detail). A video of "a run of the quest" is a *rendering problem*, not a new measurement problem.
- **Workflow-minted, sealed evidence.** Exactly like `quest-perfection.yml`, the engine runs as a deterministic workflow step (its job env carries the Claude auth — Claude Code scrubs auth env vars from Bash-tool subprocesses, so the engine can never run inside an agent). Unlike the walk lane, **no agent step runs in this workflow at all**, so there is nothing to seal against: every byte between the engine and YouTube is produced by deterministic, reviewable scripts.
- **Replay, don't screen-grab.** The recorder (`scripts/quest/walkthrough_video.mjs`) renders a *studio page* — left pane: a capture of the real quest page off the live site, auto-scrolling in sync; right pane: the transcript typed out with its ✓ passed / ✗ failed / ∅ skipped / ~ reasoned outcomes — and records it with Playwright's built-in video recording. That makes the video deterministic given (plan, evidence), honest (it renders only witnessed commands and outcomes, never a model's synthesis), and cheap (a re-render costs $0 of model spend, especially with `source_run_id` evidence reuse).
- **Human holds the publish button.** Uploads default to **unlisted**, and the frontmatter/catalog change ships as a `quest-video`-labeled PR that matches **no** auto-merge policy in `content-auto-merge.yml`. Reviewing the PR *is* reviewing the video; the human merges the reference and flips the video public on YouTube when satisfied.

## Components

| Piece | Role |
|---|---|
| `.github/workflows/quest-video.yml` | The lane: gate → plan → evidence (fresh engine pass, or `source_run_id` reuse of a quest-perfection/quest-walkthrough artifact) → record → optional publish leg. Dispatch-only, OFF by default. |
| `scripts/quest/walkthrough_video.mjs` | Deterministic side-by-side renderer: studio HTML + timed replay + Playwright `recordVideo` → `videos/<level>-<slug>.webm` (+ `.mp4` when ffmpeg is present) + `manifest.json` with per-step chapter times. |
| `scripts/quest/video_manifest.py` | `build`: recorder manifest → YouTube upload plan (title ≤100 chars, description with chapters + provenance links, bounded tags, category Education, privacy). `apply`: uploads → the quest's `walkthrough_video:` frontmatter block (+ `lastmod` bump) and the committed catalog. Unit-tested (`scripts/quest/test_video_manifest.py`). |
| `scripts/quest/youtube_upload.py` | Stdlib-only YouTube Data API v3 resumable uploader (OAuth refresh-token flow, chunked with resume/retry, optional playlist). Idempotent against the catalog — a quest with a published video is skipped unless `--force`. |
| `.quests/videos.yml` | The committed catalog: quest permalink → published video (id/url/recorded/run_url/slice/verdict/score). The queryable index; the per-quest frontmatter block is what the site renders. |
| `_includes/quest/quest-video.html` + `_layouts/quest.html` + `assets/css/quest-system.css` | The embed: a lazy, privacy-enhanced (`youtube-nocookie.com`) responsive player above the quest body, rendered only when the page's frontmatter carries `walkthrough_video`. |
| `quest_registry.py` | Schema registration: `walkthrough_video` is an optional structured field (`WALKTHROUGH_VIDEO_KEYS = provider/id/url/recorded/run_url`). |

## The frontmatter contract

Written only by `video_manifest.py apply` (idempotent text edit — every other frontmatter byte is left alone); rendered by the quest layout; indexed by the catalog:

```yaml
walkthrough_video:
  provider: youtube
  id: dQw4w9WgXcQ
  url: https://www.youtube.com/watch?v=dQw4w9WgXcQ
  recorded: '2026-08-19'
  run_url: https://github.com/bamr87/it-journey/actions/runs/<run id>
```

`run_url` is the provenance link — the CI run whose sealed evidence the video replays. The normalizer never strips the block (it only drops `RETIRED_FIELDS`), and `_data/quests/*` generation does not consume it, so `make quest-data` is not required after an apply.

## Which quest gets recorded

“A side-by-side run of the **main quest**”: by default the recorder picks the **first `main_quest` in plan order that has recorded evidence** — the plan is dependency-ordered, so that is the slice's main quest. Options widen or pin the set:

- `--quest <permalink|path|slug>` — pin one quest explicitly (the workflow's `quest` input).
- `--all-main` — every evidenced main quest in the slice (the `all_main` input).
- `--all` — every evidenced quest (side quests too); CLI-only, for local batches.

Quests without recorded evidence are skipped (listed in the manifest's `failures`), because a video without evidence would be staging, not proof. `--allow-no-evidence` exists for local demos only.

## Gates and setup (OFF by default)

Two staged gates, mirroring the fleet's kill-switch discipline:

1. **Record** — requires the `QUEST_VIDEO_ENABLED` repo variable AND Claude auth (`CLAUDE_CODE_OAUTH_TOKEN` / `ANTHROPIC_API_KEY`) — or a `source_run_id`, which needs no model at all. Output: the video as a 14-day run artifact. Nothing published, nothing committed.
2. **Publish** — additionally requires the `publish: true` dispatch input AND the YouTube secrets. Uploads land **unlisted**; the reference PR awaits human review.

```bash
# 1) engine auth (skip if the perfection loop is already set up)
gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo bamr87/it-journey

# 2) YouTube credentials (see below)
gh secret set YOUTUBE_CLIENT_ID      --repo bamr87/it-journey
gh secret set YOUTUBE_CLIENT_SECRET  --repo bamr87/it-journey
gh secret set YOUTUBE_REFRESH_TOKEN  --repo bamr87/it-journey
gh secret set YOUTUBE_PLAYLIST_ID    --repo bamr87/it-journey   # optional

# 3) the kill switch
gh variable set QUEST_VIDEO_ENABLED --body true --repo bamr87/it-journey
```

### Getting the YouTube credentials (one-time, ~10 minutes)

1. In [Google Cloud Console](https://console.cloud.google.com/), create (or reuse) a project → **Enable the YouTube Data API v3**.
2. **OAuth consent screen**: External, add yourself as a test user (Testing status is fine — refresh tokens for test users of a "Desktop" client don't expire on the 7-day schedule web clients do, but note Google can still revoke; re-mint if uploads start failing with `invalid_grant`).
3. **Credentials → Create credentials → OAuth client ID → Desktop app.** Note the client id + secret.
4. Mint a refresh token with the upload scope (add `https://www.googleapis.com/auth/youtube` instead if you want playlist filing too):

   ```bash
   # any machine with a browser; uses the OAuth out-of-band-free loopback flow
   python3 -c "
   import urllib.parse
   p = dict(client_id='YOUR_CLIENT_ID', redirect_uri='http://localhost:8080',
            response_type='code', access_type='offline', prompt='consent',
            scope='https://www.googleapis.com/auth/youtube.upload')
   print('open: https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode(p))"
   # open the URL, approve, copy the ?code=... from the redirected localhost URL, then:
   curl -s https://oauth2.googleapis.com/token \
     -d client_id=YOUR_CLIENT_ID -d client_secret=YOUR_CLIENT_SECRET \
     -d code=THE_CODE -d grant_type=authorization_code \
     -d redirect_uri=http://localhost:8080
   # → the JSON's "refresh_token" is what goes into YOUTUBE_REFRESH_TOKEN
   ```

5. Verify from anywhere: `YOUTUBE_CLIENT_ID=… YOUTUBE_CLIENT_SECRET=… YOUTUBE_REFRESH_TOKEN=… python3 scripts/quest/youtube_upload.py --verify-only`.

**Quota note:** a video upload costs ~1600 units of the default 10,000/day YouTube API quota — ~6 uploads/day headroom, far above this lane's cadence.

## Running it

**CI (the normal path):** Actions → *🎬 Quest Walkthrough Video* → Run workflow. Typical dispatches:

- Fresh recording of a slice's main quest: set `character` + `level` (blank = date-rotated), leave `publish` off → review the `quest-video-<slug>` artifact.
- Free re-render from yesterday's perfection run: set `source_run_id` to that run's id (+ the same `character`/`level`) — no model spend.
- Publish: same dispatch with `publish: true` → unlisted upload + the reference PR.

**Locally** (render only; uses whatever `walk-plan.json`/`walk-evidence.json` a walkthrough left in the working dir):

```bash
make quest-video-plan        # preview which quest would be recorded (no browser, no cost)
make quest-video             # render videos/ from walk-plan.json + walk-evidence.json
make quest-video-selftest    # unit tests for the deterministic manifest/apply arm
```

The renderer needs `npm install --no-save playwright && npx playwright install chromium ffmpeg`; an `ffmpeg` on PATH additionally produces the `.mp4` (YouTube accepts the raw `.webm` either way).

## Guardrails

- **Evidence-only replay** — the video renders the sealed transcript's commands and outcomes verbatim; no step invents, reorders, or re-runs anything. A quest without evidence gets no video.
- **No agent in the lane** — everything after the engine is deterministic script; there is no model output anywhere in the render → upload → apply path.
- **Human-reviewed publish** — unlisted by default; the `quest-video` label matches no auto-merge policy, so the reference PR always waits for a human.
- **Idempotent + catalog-guarded** — re-runs skip already-published quests (`.quests/videos.yml`); `--force` is an explicit choice. `video_manifest.py apply` is an idempotent text edit and never touches anything but the `walkthrough_video:` block and `lastmod`.
- **Kill switch** — unset `QUEST_VIDEO_ENABLED` and the lane is a no-op; the publish leg dies separately with the `YOUTUBE_*` secrets removed.
- **Vendored quests** — carry `source_repo`/`source_url` and are synced from upstream; do not target them with the publish leg (the apply edit would be overwritten by the next sync and the upstream owner should own their media).

## Roadmap (deliberately not built yet)

- **Scheduled cadence** — once trusted, a weekly cron that records the ledger's newly-`perfect` slices (the natural "this quest is done, film it" trigger) and a re-record trigger when a quest's `lastmod` moves past its video's `recorded`.
- **Narration** — a TTS voice-over track composed from the quest's chapter text (needs a voice + licensing decision; the silent side-by-side is already self-explanatory).
- **Coverage on the dashboard** — a `.quests/DASHBOARD.md` column counting quests with a fresh `walkthrough_video` per slice, fed from the catalog.
- **Level-hub reels** — stitching a level's per-quest videos into one “Level 0001 in 10 minutes” cut with ffmpeg concat.
