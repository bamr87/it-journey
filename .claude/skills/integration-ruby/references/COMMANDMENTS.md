# Framework rules

Follow these when integrating PostHog into this framework.

- posthog-ruby is the Ruby SDK gem name (add `gem 'posthog-ruby'` to Gemfile) but require it with `require 'posthog'` (NOT `require 'posthog-ruby'`)
- Use PostHog::Client.new(api_key: key, host: host) for instance-based initialization in scripts and CLIs
- In CLIs and scripts: MUST call client.shutdown before exit or all events are lost
- Use begin/rescue/ensure with shutdown in the ensure block for proper cleanup
- capture and identify take a single hash argument: client.capture(distinct_id: 'user_123', event: 'my_event', properties: { key: 'value' })
- capture_exception takes POSITIONAL args (not keyword): client.capture_exception(exception, distinct_id, additional_properties) — do NOT use `distinct_id:` keyword syntax
