---
title: "Fix a Local Jekyll Docker Build Broken by a Yanked FFI Gem"
description: "A local Jekyll build in Docker died on a yanked generic FFI platform. Here is the one Bundler command that fixed it, plus how to verify the rebuild."
date: 2026-06-22T12:00:00.000Z
lastmod: 2026-06-22T12:00:00.000Z
author: bamr87
categories: [DevOps, Infrastructure]
tags: [jekyll, docker, bundler, ci-cd, troubleshooting]
keywords: [jekyll docker build, yanked ffi gem, bundle lock remove-platform, gemfile.lock]
section_guide: devops
excerpt: "The local preview wouldn't boot because Gemfile.lock pinned a yanked FFI platform. One bundle command fixed it."
permalink: /posts/fix-local-jekyll-docker-yanked-ffi/
draft: false
---

## What broke

The local preview would not boot. `docker compose up jekyll` got partway through
`bundle install` and then stopped cold:

```text
Could not find ffi-1.16.3-x86_64-linux in locally installed gems
```

The build had worked the day before. Nothing in the site changed — the gem on the
other end did.

## Why it happened

`Gemfile.lock` pinned a *generic* `x86_64-linux` build of `ffi`. That specific
platform build was later yanked from RubyGems, so the exact pin no longer resolved
inside the Linux container. This is a Design-for-Failure moment: an upstream you do
not control can disappear, and the lockfile faithfully kept asking for the thing
that no longer exists.

## The fix

Drop the stale platform from the lockfile so Bundler resolves a build that still
exists:

```bash
bundle lock --remove-platform x86_64-linux
```

One important caveat: this is a **local-only** workaround. Do not commit the
modified `Gemfile.lock` — the committed lockfile is shared, and CI resolves its own
platform. Treat this as a local repair, not a project change.

See the [Bundler `lock` documentation](https://bundler.io/man/bundle-lock.1.html)
for what the flag does under the hood.

## Verify

Rebuild and confirm the server actually serves a page — a clean `bundle install` is
necessary but not proof the site renders:

```bash
docker compose up jekyll
# wait for: "Server running... http://0.0.0.0:4002"
curl -sSf http://localhost:4002/ >/dev/null && echo "build OK"
```

If `curl` returns `build OK`, the container is up and serving.

## Lessons

- A green `bundle install` is not the goal; a served page is. Verify the route.
- Keep the workaround out of version control — `git diff Gemfile.lock` before you
  stage anything.
- When an upstream yanks a build, the lockfile is doing its job; the fix is to let
  it re-resolve, not to fight it.

**Related:**
- [Foundational CI/CD Pipelines](/posts/foundational-ci-cd-pipelines-github-vscode-extensions/)
- [Docker Beginner's Tutorial](/posts/docker-beginners-tutorial/)
