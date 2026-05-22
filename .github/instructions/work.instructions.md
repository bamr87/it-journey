---
applyTo: "**/*"
description: "Use a work/ directory pattern for fast, isolated, cacheable, and disposable workspaces"
date: 2025-11-16T08:17:59.000Z
lastmod: 2026-05-18T12:00:00.000Z
---

# `work/` Directory Pattern

A `work/` directory at the repo root holds everything that is generated, cached, or temporary — kept out of source control, organized for fast rebuilds, and safe to wipe at any time.

## 1. Standard Layout

```
work/
├── cache/        # PERSISTENT — downloaded deps, restored across runs
├── output/       # GENERATED — builds, reports, artifacts to upload/keep
├── temp/         # EPHEMERAL — wiped on every run
├── runtime/      # JOB-LOCAL — running services (DBs, mocks) for current run
├── data/         # INPUT — large source data not appropriate for git
└── logs/         # TRACKING — execution and debug logs
```

Use only the subdirectories you need; minimum useful set is `cache/`, `output/`, `temp/`.

## 2. Non-Negotiable Rules

1. **Always gitignore `work/`** — add `work/` to `.gitignore` at the repo root.
2. **Cache only `work/cache/`** in CI — never cache `output/`, `temp/`, or `runtime/`.
3. **Wipe `temp/` and `runtime/`** at the start and end of every run.
4. **Use env vars, not hardcoded paths.** Standard names:
   - `WORK_DIR` (default `./work`)
   - `WORK_CACHE_DIR`, `WORK_OUTPUT_DIR`, `WORK_TEMP_DIR`, `WORK_LOG_DIR`
5. **Never commit `work/` artifacts** — even if accidentally staged.

## 3. CI Cache Key Pattern

Cache keys should include OS, tool, and the hash of the lockfile that drives the cache:

```yaml
key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json', '**/requirements.txt') }}
restore-keys:
  - ${{ runner.os }}-deps-
```

Partition caches per tool (`work/cache/npm`, `work/cache/pip`, `work/cache/bundler`, …) so a single tool's invalidation doesn't blow the whole cache.

## 4. Minimal GitHub Actions Example

```yaml
env:
  WORK_DIR: ${{ github.workspace }}/work

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Init work tree
        run: mkdir -p work/{cache/{npm,pip},output,temp,logs}

      - name: Restore deps cache
        uses: actions/cache@v4
        with:
          path: work/cache/**
          key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
          restore-keys: ${{ runner.os }}-deps-

      - name: Install
        run: npm install --cache work/cache/npm --prefer-offline

      - name: Build
        run: npm run build -- --output-path=work/output/dist

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build
          path: work/output/

      - name: Cleanup ephemeral
        if: always()
        run: rm -rf work/{temp,runtime}
```

## 5. Local Setup Helper

```bash
#!/usr/bin/env bash
set -euo pipefail
WORK_DIR="${WORK_DIR:-./work}"
mkdir -p "$WORK_DIR"/{cache,output,temp,runtime,logs}
export WORK_DIR
export WORK_CACHE_DIR="$WORK_DIR/cache"
export WORK_OUTPUT_DIR="$WORK_DIR/output"
export WORK_TEMP_DIR="$WORK_DIR/temp"
export WORK_LOG_DIR="$WORK_DIR/logs"
trap 'rm -rf "$WORK_DIR/temp" "$WORK_DIR/runtime"' EXIT
```

## 6. Docker Pattern

Use BuildKit cache mounts for `work/cache/`; copy final artifacts out of `work/output/`:

```dockerfile
# syntax=docker/dockerfile:1.6
FROM node:18-alpine AS build
WORKDIR /app
RUN mkdir -p work/{cache/npm,output}
COPY package*.json ./
RUN --mount=type=cache,target=/app/work/cache/npm \
    npm install --cache /app/work/cache/npm --prefer-offline
COPY . .
RUN npm run build -- --output-path=/app/work/output/dist

FROM node:18-alpine
WORKDIR /app
COPY --from=build /app/work/output/dist ./dist
CMD ["node", "dist/server.js"]
```

## 7. Cross-Platform Notes

- **Paths:** prefer relative paths and forward slashes; use `$WORK_DIR` everywhere.
- **macOS/Linux RAM disk** (optional perf boost): mount `work/` as `tmpfs` or APFS RAM disk for I/O-heavy builds.
- **Windows:** native paths work; avoid symlinks under `work/` unless Developer Mode is on.

## 8. Health Check Quickies

```bash
# Total work/ size
du -sh work/

# Per-subdir size
du -sh work/*

# Largest files
find work/ -type f -size +50M -exec ls -lh {} \; | sort -k5 -hr | head

# Cache freshness (oldest file)
find work/cache -type f -printf '%T@ %p\n' | sort -n | head -1
```

## 9. Cleanup Policy

| Subdir | Policy |
|---|---|
| `cache/` | Keep across runs; expire by lockfile-hash change |
| `output/` | Upload as artifact, then delete |
| `temp/` | Delete at start and end of every run |
| `runtime/` | Stop services + delete after run |
| `data/` | Manual lifecycle — never auto-delete |
| `logs/` | Rotate; keep last N runs |

---

**Related:** [`features.instructions.md`](features.instructions.md) for the larger CI/CD pipeline, [`scripts.instructions.md`](scripts.instructions.md) for shell-script conventions.
