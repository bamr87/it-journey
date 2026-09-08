#!/usr/bin/env ruby
# =============================================================================
# usage_report.rb — publish a job's AI usage records (summary, artifact, PR comment)
# -----------------------------------------------------------------------------
# The reporting half of AI metering. usage.rb captured one JSONL record per AI
# call into AI_USAGE_DIR/records.jsonl; this script, run at the end of the
# job (the claude-run composite calls it automatically), does four things:
#
#   1. ATTRIBUTE  — resolve which PR the spend belongs to: an explicit --pr,
#                   the pull_request event payload, or the pr-result.txt file
#                   the factory/fleet agents write after opening a PR (that
#                   run's records become the PR's CREATION cost).
#   2. CONSUME    — move records.jsonl to a reported-*.jsonl file (so a second
#                   AI step in the same job never double-reports) and print
#                   `file=` / `name=` to $GITHUB_OUTPUT for the artifact upload.
#   3. SUMMARIZE  — append a per-call table to $GITHUB_STEP_SUMMARY.
#   4. COMMENT    — upsert ONE sticky "AI usage & cost" comment on the PR,
#                   found by its <!-- lh-ai-usage --> marker (never
#                   `--edit-last`, which grabs whatever the bot said last).
#                   The comment embeds its own base64 data blob, so each run
#                   merges records by id — cumulative, idempotent, and safe to
#                   re-run. Concurrent jobs can still race the read-merge-write
#                   (last writer wins for the VIEW); the artifacts + nightly
#                   ledger remain the source of truth.
#
# Every dollar figure is API-equivalent: what the tokens would bill at list
# prices. Subscription (OAuth) runs cost $0 marginal — the label says so.
# Best-effort by design: metering must never fail the job. Stdlib + `gh` only.
#
#   ruby scripts/ai/usage_report.rb [--pr N] [--pr-result pr-result.txt]
# =============================================================================
require 'json'
require 'time'
require 'digest'
require 'securerandom'
require_relative 'usage'

MARKER    = '<!-- lh-ai-usage -->'.freeze
DATA_HEAD = '<!-- lh-ai-usage-data:'.freeze
MAX_BLOB_RECORDS = 150   # older records fold into a rollup so the comment stays < 64KB
MAX_TABLE_ROWS   = 30

pr_arg = nil
pr_result_file = 'pr-result.txt'
args = ARGV.dup
until args.empty?
  case (a = args.shift)
  when '--pr'        then pr_arg = args.shift.to_i
  when '--pr-result' then pr_result_file = args.shift.to_s
  end
end

# --- 1. load this job's records ------------------------------------------------
src = AIUsage.records_path
records = File.exist?(src) ? File.read(src, encoding: 'UTF-8').split("\n").map { |l| JSON.parse(l) rescue nil }.compact : []
if records.empty?
  warn '[usage_report] no AI usage records this job — nothing to report.'
  File.open(ENV['GITHUB_OUTPUT'], 'a') { |io| io.puts('file='); io.puts('name=') } if ENV['GITHUB_OUTPUT']
  exit 0
end

# --- 2. attribute to a PR --------------------------------------------------------
pr = nil
pr_source = nil
if pr_arg && pr_arg > 0
  pr = pr_arg
  pr_source = 'event'
elsif ENV['GITHUB_EVENT_PATH'] && File.exist?(ENV['GITHUB_EVENT_PATH'])
  ev = JSON.parse(File.read(ENV['GITHUB_EVENT_PATH'])) rescue {}
  n = ev.dig('pull_request', 'number')
  if n
    pr = n.to_i
    pr_source = 'event'
  end
end
if pr.nil? && File.exist?(pr_result_file)
  # The factory/fleet convention: the agent writes the PR/issue URL(s) it opened
  # to pr-result.txt. The first pull URL is the PR this run CREATED — its spend
  # is that PR's creation cost.
  if (m = File.read(pr_result_file, encoding: 'UTF-8')[%r{/pull/(\d+)}, 1])
    pr = m.to_i
    pr_source = 'created'
  end
end
records.each { |r| r['pr'] ||= pr; r['pr_source'] ||= pr_source if pr }

# --- 3. consume: move to a reported file, hand the path to the uploader ----------
reported = File.join(AIUsage.dir, "reported-#{Time.now.utc.strftime('%H%M%S')}-#{SecureRandom.hex(3)}.jsonl")
File.open(reported, 'w') { |io| records.each { |r| io.puts(JSON.generate(r)) } }
File.delete(src)
if ENV['GITHUB_OUTPUT']
  artifact = "ai-usage-#{ENV['GITHUB_RUN_ID'] || 'local'}-#{(ENV['GITHUB_JOB'] || 'job').gsub(/[^A-Za-z0-9_-]/, '_')}-#{SecureRandom.hex(3)}"
  File.open(ENV['GITHUB_OUTPUT'], 'a') { |io| io.puts("file=#{reported}"); io.puts("name=#{artifact}") }
end

fmt_usd = ->(v) { format('$%.4f', v.to_f) }
fmt_tok = ->(v) { v.to_i >= 10_000 ? "#{(v.to_i / 1000.0).round}k" : v.to_i.to_s }

# --- 4. step summary --------------------------------------------------------------
if ENV['GITHUB_STEP_SUMMARY']
  total = records.sum { |r| r['cost_usd'].to_f }
  lines = []
  lines << '## 🤖 AI usage (this job)'
  lines << ''
  lines << '| role | model | turns | in | out | cache r/w | cost (API-equiv) | via |'
  lines << '|---|---|---|---|---|---|---|---|'
  records.each do |r|
    t = r['tokens'] || {}
    lines << "| #{r['agent'].to_s.empty? ? '—' : r['agent']} | #{r['model']} | #{r['num_turns'] || '—'} " \
             "| #{fmt_tok.call(t['input'])} | #{fmt_tok.call(t['output'])} " \
             "| #{fmt_tok.call(t['cache_read'])}/#{fmt_tok.call(t['cache_creation'])} " \
             "| #{fmt_usd.call(r['cost_usd'])}#{r['cost_source'] == 'estimated' ? '*' : ''} | #{r['auth']} |"
  end
  lines << ''
  # A failed call bills nothing, so it is invisible in the table above — spell
  # out what the model refused, right where the operator is already looking.
  records.select { |r| r['error'] }.each do |r|
    e = r['error']
    lines << "> ❌ **#{r['agent'].to_s.empty? ? 'AI call' : r['agent']} failed** " \
             "(`#{e['subtype'].to_s.empty? ? "exit #{e['exit_code']}" : e['subtype']}`): #{e['message']}"
    lines << ''
  end
  lines << "**Job total: #{fmt_usd.call(total)}** (API-equivalent#{records.any? { |r| r['cost_source'] == 'estimated' } ? '; * = estimated from _data/ai_pricing.yml' : ''})."
  lines << ''
  File.open(ENV['GITHUB_STEP_SUMMARY'], 'a') { |io| io.puts(lines.join("\n")) }
end

# --- 5. sticky PR comment (best-effort) --------------------------------------------
repo = ENV['GITHUB_REPOSITORY'].to_s
exit 0 if pr.nil? || repo.empty?
unless system('gh --version > /dev/null 2>&1') && !(ENV['GH_TOKEN'].to_s + ENV['GITHUB_TOKEN'].to_s).empty?
  warn '[usage_report] no gh/token — skipping the PR comment (records still in the artifact).'
  exit 0
end

def gh_json(args)
  out = IO.popen(['gh'] + args, err: %i[child out], &:read)
  return nil unless $?.success?
  JSON.parse(out)
rescue StandardError
  nil
end

# Find the existing sticky comment by MARKER (any author, any position).
existing = nil
page = 1
loop do
  batch = gh_json(['api', "repos/#{repo}/issues/#{pr}/comments?per_page=100&page=#{page}"])
  break unless batch.is_a?(Array)
  existing = batch.find { |c| c['body'].to_s.start_with?(MARKER) }
  break if existing || batch.size < 100 || page >= 10
  page += 1
end

# Merge this job's records into the comment's embedded blob (dedup by id).
blob = { 'records' => [], 'folded' => nil }
if existing && (m = existing['body'].to_s[/#{Regexp.escape(DATA_HEAD)}([A-Za-z0-9+\/=]+) -->/, 1])
  blob = JSON.parse(m.unpack1('m')) rescue { 'records' => [], 'folded' => nil }
end
compact = ->(r) do
  t = r['tokens'] || {}
  { 'i' => r['id'], 't' => r['ts'], 'w' => r['workflow'], 'j' => r['job'], 'r' => r['run_id'],
    'a' => r['agent'], 'm' => r['model'], 'ti' => t['input'].to_i, 'to' => t['output'].to_i,
    'tr' => t['cache_read'].to_i, 'tc' => t['cache_creation'].to_i,
    'c' => r['cost_usd'].to_f.round(6), 's' => r['cost_source'], 'au' => r['auth'],
    'st' => r['status'], 'ps' => r['pr_source'] }
end
known = blob['records'].map { |r| r['i'] }
records.each { |r| blob['records'] << compact.call(r) unless known.include?(r['id']) }
blob['records'].sort_by! { |r| r['t'].to_s }
while blob['records'].size > MAX_BLOB_RECORDS
  old = blob['records'].shift
  f = blob['folded'] ||= { 'n' => 0, 'c' => 0.0, 'ti' => 0, 'to' => 0 }
  f['n'] += 1
  f['c'] = (f['c'] + old['c'].to_f).round(6)
  f['ti'] += old['ti'].to_i
  f['to'] += old['to'].to_i
end

all      = blob['records']
folded   = blob['folded']
total    = all.sum { |r| r['c'].to_f } + (folded ? folded['c'].to_f : 0.0)
creation = all.select { |r| r['ps'] == 'created' }.sum { |r| r['c'].to_f }
downstream = total - creation
estimated = all.any? { |r| r['s'] == 'estimated' }
oauth_only = all.all? { |r| r['au'] == 'oauth' }

body = []
body << MARKER
body << '## 🤖 AI usage & cost for this PR'
body << ''
body << "**Total: #{fmt_usd.call(total)} API-equivalent** across #{all.size + (folded ? folded['n'] : 0)} AI call(s) — " \
        "creation #{fmt_usd.call(creation)}, reviews/fixes/checks #{fmt_usd.call(downstream)}."
body << ''
body << '| when (UTC) | workflow · job | role | model | out tok | cost |'
body << '|---|---|---|---|---|---|'
body << "| _earlier_ | _#{folded['n']} older call(s), folded_ | | | #{fmt_tok.call(folded['to'])} | #{fmt_usd.call(folded['c'])} |" if folded
all.last(MAX_TABLE_ROWS).each do |r|
  run_link = r['r'].to_s.empty? ? (r['w'].to_s.empty? ? 'local' : r['w']) : "[#{r['w']} · #{r['j']}](https://github.com/#{repo}/actions/runs/#{r['r']})"
  body << "| #{r['t'].to_s[5, 11]} | #{run_link} | #{r['a'].to_s.empty? ? '—' : r['a']}#{r['ps'] == 'created' ? ' 🌱' : ''} " \
          "| #{r['m']} | #{fmt_tok.call(r['to'])} | #{fmt_usd.call(r['c'])}#{r['s'] == 'estimated' ? '*' : ''} |"
end
body << "| | _…#{all.size - MAX_TABLE_ROWS} more in the ledger_ | | | | |" if all.size > MAX_TABLE_ROWS
body << ''
notes = ['🌱 = the run that opened this PR (creation cost).']
notes << '\\* = estimated from `_data/ai_pricing.yml` (that path reports tokens, not dollars).' if estimated
notes << (oauth_only ? 'All calls ran on Claude Code subscription auth (OAuth) — $0 marginal spend; the figure is what these tokens would bill at API list prices.' \
                     : 'Some calls used a metered API key — those dollars are real.')
notes << 'Updated automatically after every AI job; full history at [/docs/ai-usage/](https://lifehacker.dev/docs/ai-usage/).'
body << notes.map { |n| "_#{n}_" }.join(' ')
body << ''
body << "#{DATA_HEAD}#{[JSON.generate(blob)].pack('m0')} -->"

payload = JSON.generate('body' => body.join("\n"))
tmp = File.join(AIUsage.dir, 'comment-payload.json')
File.write(tmp, payload)
ok =
  if existing
    system('gh', 'api', '-X', 'PATCH', "repos/#{repo}/issues/comments/#{existing['id']}", '--input', tmp, out: File::NULL, err: %i[child out])
  else
    system('gh', 'api', "repos/#{repo}/issues/#{pr}/comments", '--input', tmp, out: File::NULL, err: %i[child out])
  end
warn(ok ? "[usage_report] PR ##{pr} cost comment #{existing ? 'updated' : 'created'} (total #{fmt_usd.call(total)})." \
        : "[usage_report] PR ##{pr} comment update failed (non-fatal; records are in the artifact).")
exit 0
