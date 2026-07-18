# PostHog Analytics for IT-Journey Scripts

IT-Journey's Ruby SEO/content scripts optionally emit structured PostHog events on each run, so script activity and content health can be tracked over time. The integration uses the instance-based `PostHog::Client` API (from the `posthog-ruby` gem) and always calls `shutdown` in an `ensure` block so buffered events are flushed before the process exits.

## Opt-in by design

Every script reads its configuration from the environment at runtime — **no tokens are hardcoded**:

| Variable | Purpose | Default |
|----------|---------|---------|
| `POSTHOG_PROJECT_TOKEN` | PostHog project API key (starts with `phc_`). | _unset_ |
| `POSTHOG_HOST` | Ingestion host for your region. | `https://us.i.posthog.com` |

When `POSTHOG_PROJECT_TOKEN` is **unset**, the scripts skip analytics entirely — no client is created, no network call is made, and behavior/exit codes are identical to before. This means CI without the secret runs unchanged; set the token (locally in `.env`, in CI as a secret) only where you want capture.

See [`.env.example`](../../.env.example) for the variable stubs.

## Events

| Event | Fires when | File |
|-------|------------|------|
| `content_scan_completed` | A content freshness scan finishes — file counts, freshness breakdown, average age, computed health score. | [`scripts/validation/content-freshness-check.rb`](../../scripts/validation/content-freshness-check.rb) |
| `ctr_report_generated` | A CTR/SEO report is generated — report type (`baseline`/`weekly`/`opportunities`/`json`) and whether it was saved. | [`scripts/validation/ctr-report-generator.rb`](../../scripts/validation/ctr-report-generator.rb) |
| `gsc_csv_parsed` | A Google Search Console CSV export is parsed — page/query counts, total impressions, total clicks, average CTR. | [`scripts/validation/ctr-report-generator.rb`](../../scripts/validation/ctr-report-generator.rb) |
| `frontmatter_validation_completed` | Frontmatter validation finishes — total/valid/invalid counts, error/warning totals, average SEO score, filter options. | [`scripts/validation/frontmatter-validator.rb`](../../scripts/validation/frontmatter-validator.rb) |
| `statistics_generated` | Content statistics generation completes — post counts, category/tag/author counts, focus-area and content-type counts. | [`scripts/generation/generate_statistics.rb`](../../scripts/generation/generate_statistics.rb) |

All events are captured with the `distinct_id` `it-journey-ci`.

> **Note:** `statistics_generated` currently reports zeros because the blog
> (`pages/_posts`) was removed in the quests-only overhaul; the instrumentation
> is correct and will report real numbers if that script is revised to read the
> quest collections.

## Dashboards (PostHog project 517639)

- [Analytics basics — Dashboard](https://us.posthog.com/project/517639/dashboard/1867288)
- [Script runs over time](https://us.posthog.com/project/517639/insights/Kmt50zd0)
- [Content health score trend](https://us.posthog.com/project/517639/insights/XZzhZ2Rd)
- [Frontmatter validation quality](https://us.posthog.com/project/517639/insights/szOu5Gqt)
- [CTR reports by type](https://us.posthog.com/project/517639/insights/dtzaeI6b)
- [Content critical file rate](https://us.posthog.com/project/517639/insights/cpRzO8T8)

## Verification

The integration was verified end-to-end by pointing `POSTHOG_HOST` at a local mock ingestion server and running each script:

- All five events fire with correct, well-typed properties.
- With `POSTHOG_PROJECT_TOKEN` unset, no events are sent, no network call is
  attempted, and exit codes are unchanged.
- The event capture is placed **before** each script's `exit`, so events are not
lost when a script exits non-zero (e.g. content-freshness exiting `1` on critical content).

For further PostHog work in this repo, see the agent skill under [`.claude/skills/integration-ruby/`](../../.claude/skills/integration-ruby/).
