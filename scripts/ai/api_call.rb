#!/usr/bin/env ruby
# =============================================================================
# api_call.rb — the Claude API fallback (single-shot Messages call)
# -----------------------------------------------------------------------------
# Used by scripts/ai/run.sh when the Claude Code CLI is unavailable or fails.
# Calls POST /v1/messages over Ruby's stdlib (net/http + json) — NO gem — so it
# runs on a bare runner just like the rest of scripts/. Reads ANTHROPIC_API_KEY
# and _data/ai.yml. Prints the model's text to stdout.
#
# Auth note: this path is ANTHROPIC_API_KEY-only by design. A Claude Code OAuth
# token (CLAUDE_CODE_OAUTH_TOKEN) authenticates the `claude` CLI, NOT the raw
# Messages API, so it cannot be used here. run.sh selects the credential and only
# reaches this fallback when an API key is present; with only an OAuth token the
# primary Claude Code path runs and this fallback is intentionally unavailable.
#
# This is a degraded path: a single message in, the final text out — not the
# full agent. It covers the text-generation/analysis steps (a review comment, a
# draft, a classification); steps that need multi-file edits should run under
# Claude Code (the primary), which run.sh tries first.
#
#   ruby scripts/ai/api_call.rb --prompt "..." [--system "..."]
#   echo "..." | ruby scripts/ai/api_call.rb
# =============================================================================
require 'net/http'
require 'uri'
require 'json'
require 'yaml'

# kit: ai-runner — stdlib only and self-contained (no repo-local library), so the
# same file runs in every repo that carries scripts/ai/run.sh.
ROOT = File.expand_path('../..', __dir__)
cfg = begin
  raw = File.read(File.join(ROOT, '_data', 'ai.yml'), encoding: 'UTF-8')
  (YAML.respond_to?(:unsafe_load) ? YAML.unsafe_load(raw) : YAML.load(raw)) || {}
rescue StandardError
  {}
end
MODEL   = ENV['AI_MODEL'] || cfg['fallback_model'] || cfg['model'] || 'claude-opus-4-8'
MAXTOK  = (ENV['AI_MAX_TOKENS'] || cfg['max_tokens'] || 8000).to_i
VERSION = cfg['api_version'] || '2023-06-01'
BASE    = cfg['api_base'] || 'https://api.anthropic.com'

key = ENV['ANTHROPIC_API_KEY'].to_s
abort '[api_call] ANTHROPIC_API_KEY not set — cannot use the Claude API fallback' if key.empty?

# --- parse args: --prompt/-p, --system, else stdin -------------------------
args = ARGV.dup
system_prompt = nil
if (i = args.index('--system'))
  system_prompt = args[i + 1]
  args.delete_at(i + 1); args.delete_at(i)
end
prompt =
  if (i = (args.index('--prompt') || args.index('-p'))) then args[i + 1]
  elsif !args.empty? then args.join(' ')
  else $stdin.read
  end
abort '[api_call] empty prompt' if prompt.to_s.strip.empty?

body = { 'model' => MODEL, 'max_tokens' => MAXTOK,
         'messages' => [{ 'role' => 'user', 'content' => prompt }] }
body['system'] = system_prompt if system_prompt

# Dry run: print the request shape without calling the API (for tests).
if ENV['AI_DRY_RUN'] == '1'
  puts JSON.pretty_generate('endpoint' => "#{BASE}/v1/messages", 'model' => MODEL,
                            'max_tokens' => MAXTOK, 'anthropic_version' => VERSION,
                            'has_system' => !system_prompt.nil?)
  exit 0
end

uri  = URI.join(BASE, '/v1/messages')
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = (uri.scheme == 'https')
http.read_timeout = 120
http.open_timeout = 20

attempt = 0
loop do
  attempt += 1
  req = Net::HTTP::Post.new(uri)
  req['x-api-key'] = key
  req['anthropic-version'] = VERSION
  req['content-type'] = 'application/json'
  req.body = JSON.generate(body)

  res = (http.request(req) rescue nil)
  code = res ? res.code.to_i : 0

  if code == 200
    data = JSON.parse(res.body)
    # Meter the call (tokens were billed either way — refusals included). The
    # record is an ESTIMATE from _data/ai_pricing.yml: the raw API reports
    # usage but not dollars. Best-effort — a metering bug must never break
    # the actual AI step.
    begin
      require_relative 'usage'
      AIUsage.append(AIUsage.from_api_response(data, agent: ENV['AI_ROLE'].to_s))
    rescue StandardError => e
      warn "[api_call] usage record failed (non-fatal): #{e.class}: #{e.message}"
    end
    if data['stop_reason'] == 'refusal'
      warn '[api_call] request refused by safety classifiers'
      exit 2
    end
    text = (data['content'] || []).select { |b| b['type'] == 'text' }.map { |b| b['text'] }.join
    warn "[api_call] Claude API fallback ok (model=#{data['model']}, stop=#{data['stop_reason']})"
    puts text
    exit 0
  elsif code == 401 || code == 403
    # Auth failure is not transient — don't retry, and say so plainly so a
    # misconfigured/expired/insufficient ANTHROPIC_API_KEY is diagnosable instead
    # of hiding behind the generic HTTP error below.
    warn "[api_call] authentication failed (HTTP #{code}) — the ANTHROPIC_API_KEY is missing, invalid, expired, or lacks access. #{res && res.body.to_s[0, 200]}"
    exit 1
  elsif (code.zero? || [429, 500, 502, 503, 529].include?(code)) && attempt < 4
    warn "[api_call] transient (HTTP #{code}), retry #{attempt}/3"
    sleep([2**attempt, 30].min)
    next
  else
    warn "[api_call] HTTP #{code}: #{res && res.body.to_s[0, 300]}"
    exit 1
  end
end
