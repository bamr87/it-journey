---
name: run-it-journey
description: Build, run, and drive the IT-Journey Jekyll site. Use when asked to start IT-Journey, serve the site locally, preview a content change, take a screenshot of a page, smoke-test routes, or validate frontmatter/quests.
---

IT-Journey is a large GitHub-Pages **Jekyll site** (quests, docs, notes, posts).
You run it with **Docker Compose** (port 4002) and drive it with
`.claude/skills/run-it-journey/smoke.sh` — a smoke harness that checks routes
and screenshots pages with headless Google Chrome.

All paths below are relative to the **repo root**.

> Authored and verified on **macOS (Apple Silicon)**. The stock macOS system
> Ruby (2.6.10) **cannot** run this site — `github-pages` (v232) needs Ruby
> ≥ 3.1 — and there's no `rbenv`/`brew` Ruby here, so the native
> `bundle exec jekyll serve` path is a dead end. **Docker is the path.** The
> `jekyll/jekyll:latest` image ships Ruby 3.1.1, which is why it works.

## Prerequisites

- **Docker Desktop**, running. Verify: `docker info >/dev/null && echo ok`.
- **Google Chrome** (for screenshots), at the default macOS location
  `/Applications/Google Chrome.app`. Verify:
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version`.
  (`smoke.sh` skips screenshots with a warning if Chrome is absent; override
  with `CHROME=/path/to/chrome`.)

No `apt-get`/`bundle install` on the host — everything Ruby happens inside the
container.

## Setup

The compose `jekyll` service declares `env_file: .env`, so that file must exist
(its API keys are optional and unused for serving):

```bash
cp .env.example .env
```

## Run (agent path)

**1. Start the server** (first run is slow — see Gotchas):

```bash
docker compose up -d jekyll
```

The first start runs `bundle install` inside the container and then a full site
build. **Wait for `Server running`** before driving it:

```bash
# blocks until the server is actually serving (build takes ~8-10 min)
until docker compose logs jekyll 2>&1 | grep -q 'Server running'; do sleep 10; done
docker compose logs jekyll 2>&1 | grep -E 'done in|Server (address|running)'
```

**2. Drive it** — route checks + screenshots:

```bash
bash .claude/skills/run-it-journey/smoke.sh
```

Expected tail: seven `HTTP 200 OK` routes and `==> PASS`. Screenshots land in
**`/tmp/it-journey-shots/`** (`home.png`, `quests.png`). **Open them** — a curl
200 with a blank body still "passes"; the PNG is the proof the site rendered.

`smoke.sh` knobs (all optional env / args):

| invocation | what it does |
|---|---|
| `bash .../smoke.sh` | check `/ /home/ /quests/ /docs/ /notes/ /about/ /sitemap/`, shoot `/` + `/quests/` |
| `bash .../smoke.sh /quests/ /docs/` | check just those routes |
| `SHOTS="/ /docs/ /notes/" bash .../smoke.sh` | screenshot a custom set |
| `BASE_URL=http://localhost:4002 OUT_DIR=/tmp/x bash .../smoke.sh` | override URL / output dir |

**Stop** when done:

```bash
docker compose down          # stops + removes the container; keeps the
                             # bundle_cache + jekyll-cache volumes for next time
```

## Run (human path)

`make serve` (→ `bundle exec jekyll serve --config _config.yml,_config_dev.yml
--livereload --port 4002`) is the documented native workflow, but it needs a
local Ruby ≥ 3.1 with gems bundled. On stock macOS system Ruby it fails with
`command not found: jekyll`. Use the Docker path above unless you've set up a
modern Ruby yourself.

## Test

Lightweight syntax/sanity checks (host Ruby is fine — no gems needed):

```bash
make test          # ruby -c + bash -n on the statistics scripts → "All tests passed!"
```

Content / frontmatter validation (PRs here are mostly markdown). Host Python
lacks `pyyaml`, so run it in a throwaway container — `python:3.12-slim` is the
small base used here:

```bash
docker run --rm -v "$PWD":/app -w /app python:3.12-slim \
  sh -c "pip install -q pyyaml requests && python3 scripts/validation/frontmatter-validator.py pages/_about"
# → "✅ No files with errors!" and an SEO-score summary.
# Swap pages/_about for pages/ to validate everything, or pages/_quests for quests.
```

The repo also ships a `quest-validator` compose service for the same purpose
(`docker compose run --rm quest-validator`), but it builds the heavier
`Dockerfile` image (full `bundle install` + pip) on first use.

## Gotchas

- **First serve takes ~8-10 minutes, and `:4002` refuses connections the whole
  time.** `docker-compose.yml` pins `platform: linux/amd64`, so on Apple Silicon
  the container runs under emulation; the site build alone was `done in 494
  seconds` here. Until it finishes, `curl localhost:4002` returns *"Connection
  reset by peer."* Don't kill it — watch for `Server running` in the logs.
- **`.env` must exist or `docker compose up jekyll` errors.** The service has
  `env_file: .env`; the repo only ships `.env.example`. `cp .env.example .env`.
- **Don't fight the host Ruby.** System Ruby 2.6.10 can't resolve `github-pages`
  232 (needs ≥ 3.1) and there's no version manager installed. `bundle exec
  jekyll …` on the host gives `command not found: jekyll`. The whole point of
  Docker here is the 3.1.1 image.
- **A curl 200 is not proof of a render.** Always open the screenshot PNG.
- **macOS sometimes hands scripts a stripped PATH** — bare `curl`/`grep` come
  back `command not found`. `smoke.sh` pins PATH defensively; in one-off shells
  use absolute paths like `/usr/bin/curl`.
- **Harmless build warning, every time:** `Liquid syntax error … Unexpected
  character $ in "{{slugify ${title}}"` in
  `pages/_posts/data-analytics/2024-04-25-placeholders.md`. It's a placeholder
  file, not a build failure.

## Troubleshooting

- **`curl: (56) Recv failure: Connection reset by peer` on :4002** — the server
  is still building. Wait for `Server running` (`docker compose logs -f jekyll`).
- **`Error: PyYAML is required but not installed`** when running a validator on
  the host — host Python has no deps. Use the `python:3.12-slim` docker command
  in the Test section.
- **`bundler: command not found: jekyll`** on the host — system Ruby has no gems
  installed and is too old anyway. Use Docker.
- **`docker compose up` hangs at `Generating...`** — it's not hung; that's the
  ~8 min build. Confirm forward progress with `docker compose logs jekyll`.
