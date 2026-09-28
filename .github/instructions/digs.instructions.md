---
applyTo: "pages/_digs/**/*.md"
description: "Author a published Git dig: one bamr87 repository, one commit range since 2020, facts kept apart from inference."
date: 2026-09-26T21:21:40.000Z
lastmod: 2026-09-26T21:21:40.000Z
---

# Digs — `pages/_digs/**`

A dig is a published historical reading of Git activity. It is not a quest, a note, or a governance verdict.

## Required front matter

| Field | Constraint |
|---|---|
| `title` | Plain string, at most 60 characters |
| `description` | 80–160 characters, one sentence |
| `date` | ISO-8601 with milliseconds; the publication date, not the historical range |
| `lastmod` | ISO-8601 with milliseconds |
| `author` | `bamr87` |
| `categories` | YAML list containing `digs` |
| `tags` | YAML list |
| `excerpt` | One sentence |
| `permalink` | `/digs/<slug>/` |
| `repository` | `bamr87/<name>` from the candidate brief |
| `range_start` | `YYYY-MM-DD`, on or after 2020-01-01 |
| `range_end` | `YYYY-MM-DD`, on or after `range_start` |
| `start_sha` | Full 40-hex commit at the start of the examined chain |
| `end_sha` | Full 40-hex commit at the end of the examined chain |
| `commit_count` | Positive integer, at most 40 |
| `draft` | `false` only when the page is ready to publish on merge |
| `voice_profile` | `git-dig` |

The index page omits the repository fields. An installment must include them.

## Voice

Installments use `voice_profile: git-dig`. The profile lives in `_data/brand/voice.yml`. The section guide is `_data/brand/sections/dig.md`. Read those. Do not invent a second voice in the page.

The lead may be dry, satirical, sarcastic, inquisitive, and philosophical. Satire frames the record. It does not change a date, path, subject, or diff. No emoji. No fantasy ranks.

## Body

An installment opens with an unlabeled lead, then these headings, in order:

1. `## Scope` — repository, dates, commit count, and what this sample did not collect.
2. `## Facts` — only what the commits record. Cite commit URLs.
3. `## Inferences` — readings that the objects suggest but do not prove. Say what they rest on.
4. `## Limits` — what this sample cannot say, including any question left open.
5. `## Retrospective` — the last section. Written from now, not from the commits. What the author wishes they had known, or the cheaper next move that would have saved learning time. Each item must point at a cited commit or a pattern already established in Facts. It is advice, not a recovered motive, and it must say so.

A commit subject is not a diff. A script file is not a recorded run. Do not copy local paths, gist identifiers, credentials, or remote-install recipes into the page. Do not invent measurements, test results, or motives. A count is allowed only when the examined commits support it, and it stays inside Facts. The retrospective may name a better approach. It may not pretend the historical author wrote that wish down.

One paragraph per line. Do not enable Liquid on an installment. The collection default already sets `render_with_liquid: false`.

## Evidence

A bounded evidence index may live under `docs/git-archaeology/<id>/`. That directory is not a site path. The page cites the commits, not a `/docs/` URL.

## Daily lane

The hub workflow `git-digs.yml` asks an agent to choose the repository and the range. `scripts/digs/candidates.py` only lists what is eligible and what is already covered. `scripts/digs/validate_dig.py` rejects a page outside those rules. The workflow opens a draft pull request. It does not merge.
