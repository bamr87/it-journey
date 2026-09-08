#!/usr/bin/env ruby
# =============================================================================
# usage.rb — capture ONE normalized usage record per AI invocation
# -----------------------------------------------------------------------------
# The metering half of the universal AI runner. Every model call in the repo
# already flows through scripts/ai/run.sh (Claude Code) or scripts/ai/api_call.rb
# (API fallback) — this library turns each call's raw usage payload into one
# JSONL record so tokens and cost are never invisible. Records accumulate in
# AI_USAGE_DIR (default: $RUNNER_TEMP/ai-usage — OUTSIDE the checkout, so
# agents never see a dirty tree), and scripts/ai/usage_report.rb publishes them
# (step summary + artifact + PR comment) at the end of the job.
#
# Cost semantics: Claude Code reports its own total_cost_usd — recorded verbatim
# (cost_source: "reported"). That figure is what the tokens would bill at API
# list prices; under subscription OAuth the marginal dollar cost is $0, so every
# surface labels it "API-equivalent". Paths that report tokens but no dollars
# (the raw API fallback) get cost_source: "estimated" from _data/ai_pricing.yml.
#
#   ruby scripts/ai/usage.rb ingest-claude <result.json> [--agent X] [--rc N] [--emit-result]
#   ruby scripts/ai/usage.rb ingest-execution-log <log.json> [--agent X]
#
# ingest-claude exits non-zero when the file is not a Claude result JSON, so
# run.sh can treat "unparseable output" like a failed run (fallback engages).
# Stdlib only — no gems — so it runs on a bare runner before `bundle install`.
# =============================================================================
require 'json'
require 'yaml'
require 'time'
require 'digest'
require 'fileutils'

module AIUsage
  ROOT = File.expand_path('../..', __dir__)

  module_function

  def dir
    ENV['AI_USAGE_DIR'].to_s.empty? ? File.join(ENV['RUNNER_TEMP'] || ENV['TMPDIR'] || '/tmp', 'ai-usage') : ENV['AI_USAGE_DIR']
  end

  def records_path
    File.join(dir, 'records.jsonl')
  end

  # --- pricing (estimates only — reported costs are always preferred) --------
  def pricing
    @pricing ||= begin
      raw = YAML.respond_to?(:unsafe_load) ? YAML.unsafe_load(File.read(File.join(ROOT, '_data', 'ai_pricing.yml'))) : YAML.load(File.read(File.join(ROOT, '_data', 'ai_pricing.yml')))
      raw.is_a?(Hash) ? raw : {}
    rescue StandardError
      {}
    end
  end

  def price_for(model)
    models = pricing['models'] || {}
    key = models.keys.reject { |k| k == 'default' }
                .select { |k| model.to_s.start_with?(k) }
                .max_by(&:length)
    models[key] || models['default'] || { 'input' => 5.0, 'output' => 25.0 }
  end

  # tokens: {'input'=>, 'output'=>, 'cache_read'=>, 'cache_5m'=>, 'cache_1h'=>}
  # Reproduces the CLI's own arithmetic (validated to the cent, 2026-07-14).
  def estimate_cost(model, tokens)
    p = price_for(model)
    m = pricing['multipliers'] || {}
    inp = p['input'].to_f / 1_000_000
    out = p['output'].to_f / 1_000_000
    tokens['input'].to_i * inp +
      tokens['output'].to_i * out +
      tokens['cache_read'].to_i * inp * (m['cache_read'] || 0.1).to_f +
      tokens['cache_5m'].to_i * inp * (m['cache_write_5m'] || 1.25).to_f +
      tokens['cache_1h'].to_i * inp * (m['cache_write_1h'] || 2.0).to_f
  end

  # --- shared context ---------------------------------------------------------
  def auth_mode
    return 'oauth' unless ENV['CLAUDE_CODE_OAUTH_TOKEN'].to_s.empty?
    return 'api_key' unless ENV['ANTHROPIC_API_KEY'].to_s.empty?
    'none'
  end

  # One safe, bounded line out of a model-supplied error string: credentials
  # masked, whitespace collapsed, length capped. These records ship as build
  # artifacts and land in the public ledger, so nothing verbatim goes in.
  MAX_ERROR_CHARS = 500
  def scrub(text)
    text.to_s
        .gsub(/sk-ant-[A-Za-z0-9_-]{8,}/, 'sk-ant-***')
        .gsub(/\s+/, ' ')
        .strip[0, MAX_ERROR_CHARS]
        .to_s
  end

  def ci_context
    {
      'repo'        => ENV['GITHUB_REPOSITORY'].to_s,
      'workflow'    => ENV['GITHUB_WORKFLOW'].to_s,
      'job'         => ENV['GITHUB_JOB'].to_s,
      'run_id'      => ENV['GITHUB_RUN_ID'].to_s,
      'run_attempt' => ENV['GITHUB_RUN_ATTEMPT'].to_s,
      'event'       => ENV['GITHUB_EVENT_NAME'].to_s,
      'ref'         => ENV['GITHUB_REF_NAME'].to_s,
      'sha'         => ENV['GITHUB_SHA'].to_s
    }
  end

  def base_record(source:, agent:, ts: nil)
    {
      'id'          => nil,                       # set by the ingester (stable per payload)
      'ts'          => (ts || Time.now.utc).iso8601,
      'source'      => source,                    # claude-code | api-fallback | claude-code-action
      'status'      => 'success',
      'agent'       => agent.to_s,
      'model'       => '',
      'auth'        => auth_mode,
      'tokens'      => { 'input' => 0, 'output' => 0, 'cache_read' => 0, 'cache_creation' => 0 },
      'model_usage' => {},
      'cost_usd'    => 0.0,
      'cost_source' => 'reported',
      'duration_ms' => nil,
      'num_turns'   => nil,
      'session_id'  => nil,
      'pr'          => nil,                       # attributed later by usage_report.rb
      'pr_source'   => nil                        # 'event' (ran on the PR) | 'created' (run opened it)
    }.merge(ci_context)
  end

  def stable_id(payload_anchor)
    Digest::SHA256.hexdigest("#{ENV['GITHUB_RUN_ID']}|#{ENV['GITHUB_JOB']}|#{payload_anchor}")[0, 16]
  end

  # --- ingesters ---------------------------------------------------------------
  # A `claude -p --output-format json` result object (the probed 2026 schema:
  # total_cost_usd, usage{...}, modelUsage{<id>=>{...costUSD}}, num_turns, uuid).
  def from_claude_result(res, agent: '', exit_code: 0, source: 'claude-code')
    rec = base_record(source: source, agent: agent)
    rec['id']          = stable_id(res['uuid'] || res['session_id'] || Digest::SHA256.hexdigest(res.to_s))
    rec['status']      = (res['is_error'] || exit_code.to_i != 0) ? 'error' : 'success'
    rec['duration_ms'] = res['duration_ms']
    rec['num_turns']   = res['num_turns']
    rec['session_id']  = res['session_id']
    # WHY it failed, not just that it did. A rejected call reports zero tokens
    # and an empty model, so without this the record is indistinguishable from
    # any other dead run and the caller's evidence is already gone.
    if rec['status'] == 'error'
      rec['error'] = {
        'subtype'   => res['subtype'].to_s,
        'exit_code' => exit_code.to_i,
        'message'   => scrub(res['result'] || res['error'])
      }
    end

    usage = res['usage'] || {}
    rec['tokens'] = {
      'input'          => usage['input_tokens'].to_i,
      'output'         => usage['output_tokens'].to_i,
      'cache_read'     => usage['cache_read_input_tokens'].to_i,
      'cache_creation' => usage['cache_creation_input_tokens'].to_i
    }

    mu = res['modelUsage'] || {}
    mu.each do |model, u|
      rec['model_usage'][model] = {
        'input'          => u['inputTokens'].to_i,
        'output'         => u['outputTokens'].to_i,
        'cache_read'     => u['cacheReadInputTokens'].to_i,
        'cache_creation' => u['cacheCreationInputTokens'].to_i,
        'cost_usd'       => u['costUSD'].to_f
      }
    end
    # Primary model = the one that did the most output work (subagents may add others).
    rec['model'] = mu.max_by { |_, u| u['outputTokens'].to_i }&.first || ''

    if res['total_cost_usd']
      rec['cost_usd']    = res['total_cost_usd'].to_f
      rec['cost_source'] = 'reported'
    else
      cache = usage['cache_creation'] || {}
      rec['cost_usd'] = estimate_cost(rec['model'], rec['tokens'].merge(
        'cache_5m' => cache['ephemeral_5m_input_tokens'].to_i,
        'cache_1h' => cache['ephemeral_1h_input_tokens'].to_i
      ))
      rec['cost_source'] = 'estimated'
    end
    rec
  end

  # A raw Messages API response (api_call.rb fallback). No cost field — estimate.
  def from_api_response(data, agent: '')
    rec = base_record(source: 'api-fallback', agent: agent)
    rec['id']     = stable_id(data['id'] || Digest::SHA256.hexdigest(data.to_s))
    rec['model']  = data['model'].to_s
    rec['status'] = data['stop_reason'] == 'refusal' ? 'error' : 'success'
    usage = data['usage'] || {}
    cache = usage['cache_creation'] || {}
    rec['tokens'] = {
      'input'          => usage['input_tokens'].to_i,
      'output'         => usage['output_tokens'].to_i,
      'cache_read'     => usage['cache_read_input_tokens'].to_i,
      'cache_creation' => usage['cache_creation_input_tokens'].to_i
    }
    rec['cost_usd'] = estimate_cost(rec['model'], rec['tokens'].merge(
      'cache_5m' => cache['ephemeral_5m_input_tokens'] ? cache['ephemeral_5m_input_tokens'].to_i : usage['cache_creation_input_tokens'].to_i,
      'cache_1h' => cache['ephemeral_1h_input_tokens'].to_i
    ))
    rec['cost_source'] = 'estimated'
    rec['model_usage'][rec['model']] = rec['tokens'].merge('cost_usd' => rec['cost_usd'])
    rec
  end

  # A claude-code-action execution log: a JSON array (or NDJSON) of stream
  # events. Prefer the final `result` event (same shape as ingest-claude);
  # fall back to summing per-message assistant usage when the log has none.
  def from_execution_log(text, agent: '')
    events =
      begin
        parsed = JSON.parse(text)
        parsed.is_a?(Array) ? parsed : [parsed]
      rescue JSON::ParserError
        text.split("\n").map { |l| JSON.parse(l) rescue nil }.compact
      end
    result = events.reverse.find { |e| e.is_a?(Hash) && e['type'] == 'result' }
    return from_claude_result(result, agent: agent, source: 'claude-code-action') if result

    rec = base_record(source: 'claude-code-action', agent: agent)
    rec['id'] = stable_id(Digest::SHA256.hexdigest(text))
    turns = 0
    events.each do |e|
      next unless e.is_a?(Hash) && e['type'] == 'assistant'
      msg   = e['message'] || {}
      usage = msg['usage'] || {}
      next if usage.empty?
      turns += 1
      model = msg['model'].to_s
      mu = rec['model_usage'][model] ||= { 'input' => 0, 'output' => 0, 'cache_read' => 0, 'cache_creation' => 0, 'cost_usd' => 0.0 }
      mu['input']          += usage['input_tokens'].to_i
      mu['output']         += usage['output_tokens'].to_i
      mu['cache_read']     += usage['cache_read_input_tokens'].to_i
      mu['cache_creation'] += usage['cache_creation_input_tokens'].to_i
      %w[input output cache_read cache_creation].each { |k| rec['tokens'][k] += mu_key(usage, k) }
    end
    rec['num_turns'] = turns
    rec['model'] = rec['model_usage'].max_by { |_, u| u['output'].to_i }&.first || ''
    rec['model_usage'].each do |model, u|
      u['cost_usd'] = estimate_cost(model, u.merge('cache_5m' => u['cache_creation'], 'cache_1h' => 0))
      rec['cost_usd'] += u['cost_usd']
    end
    rec['cost_source'] = 'estimated'
    rec
  end

  def mu_key(usage, key)
    { 'input' => usage['input_tokens'], 'output' => usage['output_tokens'],
      'cache_read' => usage['cache_read_input_tokens'],
      'cache_creation' => usage['cache_creation_input_tokens'] }[key].to_i
  end

  # --- sink ---------------------------------------------------------------------
  def append(rec, to: nil)
    path = to || records_path
    FileUtils.mkdir_p(File.dirname(path))
    File.open(path, 'a') { |io| io.puts(JSON.generate(rec)) }
    rec
  end
end

# --- CLI -------------------------------------------------------------------------
if __FILE__ == $PROGRAM_NAME
  cmd = ARGV.shift
  agent = ''
  rc = 0
  emit = false
  file = nil
  args = ARGV.dup
  until args.empty?
    case (a = args.shift)
    when '--agent'       then agent = args.shift.to_s
    when '--rc'          then rc = args.shift.to_i
    when '--emit-result' then emit = true
    else file ||= a
    end
  end

  case cmd
  when 'ingest-claude'
    abort '[usage] no input file' unless file && File.exist?(file)
    res = begin
      JSON.parse(File.read(file, encoding: 'UTF-8'))
    rescue JSON::ParserError, Errno::ENOENT
      warn '[usage] not a Claude result JSON — nothing recorded.'
      exit 65
    end
    unless res.is_a?(Hash) && (res.key?('usage') || res.key?('total_cost_usd'))
      warn '[usage] JSON has no usage payload — nothing recorded.'
      exit 65
    end
    rec = AIUsage.append(AIUsage.from_claude_result(res, agent: agent, exit_code: rc))
    warn "[usage] recorded #{rec['id']}: #{rec['model']} $#{format('%.4f', rec['cost_usd'])} (#{rec['tokens']['output']} out tok, #{rec['status']})"
    warn "[usage] failure: #{[rec['error']['subtype'], rec['error']['message']].reject { |v| v.to_s.empty? }.join(' — ')}" if rec['error']
    # Emit the result text only on success — on error the caller falls back to
    # the API path, and emitting here would double the output it produces.
    print res['result'].to_s if emit && rec['status'] == 'success'
    exit(rec['status'] == 'success' ? 0 : 1)
  when 'ingest-execution-log'
    abort '[usage] no input file' unless file && File.exist?(file)
    rec = AIUsage.append(AIUsage.from_execution_log(File.read(file, encoding: 'UTF-8'), agent: agent))
    warn "[usage] recorded #{rec['id']}: #{rec['model']} $#{format('%.4f', rec['cost_usd'])} (#{rec['source']})"
  else
    abort "usage: usage.rb ingest-claude <result.json> [--agent X] [--rc N] [--emit-result]\n" \
          "       usage.rb ingest-execution-log <log.json> [--agent X]"
  end
end
