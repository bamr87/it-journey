#!/usr/bin/env ruby
# frozen_string_literal: true

# ctr-report-generator.rb
#
# IT-Journey CTR (Click-Through Rate) Report Generator
# Generates SEO performance reports from Google Search Console data exports
# or baseline metrics, outputting markdown reports for tracking.
#
# Features:
# - Parse Google Search Console CSV exports
# - Compare current vs baseline metrics
# - Identify improvement opportunities
# - Generate markdown weekly reports
# - Track new content performance
#
# Author: IT-Journey Team
# Created: 2025-12-20
# Version: 1.0.0
#
# Usage:
#   ruby ctr-report-generator.rb --baseline        # Generate baseline report
#   ruby ctr-report-generator.rb --weekly          # Generate weekly template
#   ruby ctr-report-generator.rb --parse FILE.csv  # Parse GSC export
#   ruby ctr-report-generator.rb --opportunities   # Show improvement opportunities

require 'csv'
require 'json'
require 'optparse'
require 'date'
require 'pathname'
require 'fileutils'

# ANSI color codes
module Colors
  RED = "\e[0;31m"
  GREEN = "\e[0;32m"
  YELLOW = "\e[1;33m"
  BLUE = "\e[0;34m"
  CYAN = "\e[0;36m"
  NC = "\e[0m"
  BOLD = "\e[1m"
end

def print_info(msg)
  puts "#{Colors::BLUE}[INFO]#{Colors::NC} #{msg}"
end

def print_success(msg)
  puts "#{Colors::GREEN}[SUCCESS]#{Colors::NC} #{msg}"
end

def print_warning(msg)
  puts "#{Colors::YELLOW}[WARNING]#{Colors::NC} #{msg}"
end

def print_error(msg)
  puts "#{Colors::RED}[ERROR]#{Colors::NC} #{msg}"
end

# CTR Report Generator
class CTRReportGenerator
  # Configuration
  SCRIPT_DIR = Pathname.new(__FILE__).dirname
  PROJECT_ROOT = SCRIPT_DIR.parent
  SEO_DIR = PROJECT_ROOT / 'TODO' / 'seo'
  DATA_DIR = SEO_DIR / 'data'
  REPORTS_DIR = SEO_DIR / 'reports'

  # Baseline metrics from Google Search Console analysis (Oct-Nov 2025)
  BASELINE_METRICS = {
    overall: {
      avg_ctr: 0.7,
      avg_position: 32,
      total_impressions: 10_000,
      total_clicks: 70
    },
    pages: {
      '/quests/level-010-nerd-font-enchantment/' => {
        title: 'Nerd Font Quest',
        impressions: 755,
        clicks: 5,
        ctr: 0.7,
        position: 35,
        optimized: '2025-12-19',
        target_ctr: 1.5
      },
      '/posts/2024/03/27/bootable-mac-os/' => {
        title: 'Bootable macOS Guide',
        impressions: 557,
        clicks: 3,
        ctr: 0.5,
        position: 40,
        optimized: '2025-12-19',
        target_ctr: 1.2
      },
      '/posts/django-pi-guide/' => {
        title: 'Django Pi Guide',
        impressions: 461,
        clicks: 10,
        ctr: 2.2,
        position: 20,
        optimized: nil,
        status: 'performing_well'
      },
      '/quests/bashcrawl/' => {
        title: 'Bashcrawl Quest',
        impressions: 352,
        clicks: 5,
        ctr: 1.4,
        position: 25,
        optimized: nil,
        status: 'performing_well'
      },
      '/docs/jekyll-mermaid/' => {
        title: 'Jekyll Mermaid Guide',
        impressions: 43,
        clicks: 0,
        ctr: 0.0,
        position: 45,
        optimized: '2025-12-19',
        target_ctr: 0.8
      },
      '/posts/sec-edgar-guide/' => {
        title: 'SEC EDGAR Guide',
        impressions: 41,
        clicks: 0,
        ctr: 0.0,
        position: 50,
        optimized: '2025-12-19',
        target_ctr: 0.8
      }
    },
    targets: {
      ctr: 1.5,
      position: 20,
      impressions_growth: 20
    },
    new_content: {
      '/docs/terminal-shortcuts-cheat-sheet/' => {
        title: 'Terminal Shortcuts Cheat Sheet',
        published: '2025-12-20',
        target_keywords: ['terminal shortcuts', 'bash shortcuts', 'command line shortcuts']
      },
      '/posts/essential-vscode-extensions-developers/' => {
        title: 'VS Code Extensions Guide',
        published: '2025-12-20',
        target_keywords: ['vscode extensions', 'best vscode extensions']
      },
      '/posts/docker-beginners-tutorial/' => {
        title: 'Docker Tutorial for Beginners',
        published: '2025-12-20',
        target_keywords: ['docker tutorial', 'docker for beginners', 'learn docker']
      }
    }
  }.freeze

  def initialize(verbose: false)
    @verbose = verbose
  end

  def ensure_dirs
    FileUtils.mkdir_p(DATA_DIR)
    FileUtils.mkdir_p(REPORTS_DIR)
  end

  def format_percent(value)
    "#{value.round(2)}%"
  end

  def format_change(current, baseline)
    return 'NEW' if baseline.zero?

    change = ((current - baseline) / baseline.to_f) * 100
    if change > 0
      "#{Colors::GREEN}↑ #{change.round(1)}%#{Colors::NC}"
    elsif change < 0
      "#{Colors::RED}↓ #{change.abs.round(1)}%#{Colors::NC}"
    else
      '→ 0%'
    end
  end

  def format_change_md(current, baseline)
    return 'NEW' if baseline.zero?

    change = ((current - baseline) / baseline.to_f) * 100
    if change > 0
      "↑ #{change.round(1)}%"
    elsif change < 0
      "↓ #{change.abs.round(1)}%"
    else
      '→ 0%'
    end
  end

  # Parse Google Search Console CSV export
  def parse_gsc_csv(file_path)
    unless File.exist?(file_path)
      print_error("File not found: #{file_path}")
      return nil
    end

    print_info("Parsing GSC export: #{file_path}")

    data = {
      pages: {},
      queries: {},
      overall: { impressions: 0, clicks: 0, ctr: 0, position: 0 }
    }

    begin
      # GSC exports can have different formats, try to detect
      csv_content = File.read(file_path, encoding: 'UTF-8')

      # Determine delimiter (comma or tab)
      delimiter = csv_content.include?("\t") ? "\t" : ','

      CSV.parse(csv_content, headers: true, col_sep: delimiter) do |row|
        # GSC Page report format
        if row['Top pages'] || row['Page']
          page = row['Top pages'] || row['Page']
          data[:pages][page] = {
            impressions: (row['Impressions'] || row['印象数'] || 0).to_i,
            clicks: (row['Clicks'] || row['クリック数'] || 0).to_i,
            ctr: (row['CTR'] || row['クリック率'] || '0').to_s.gsub('%', '').to_f,
            position: (row['Position'] || row['掲載順位'] || 0).to_f.round(1)
          }
        end

        # GSC Query report format
        if row['Top queries'] || row['Query']
          query = row['Top queries'] || row['Query']
          data[:queries][query] = {
            impressions: (row['Impressions'] || 0).to_i,
            clicks: (row['Clicks'] || 0).to_i,
            ctr: (row['CTR'] || '0').to_s.gsub('%', '').to_f,
            position: (row['Position'] || 0).to_f.round(1)
          }
        end
      end

      # Calculate overall metrics
      if data[:pages].any?
        total_impressions = data[:pages].values.sum { |p| p[:impressions] }
        total_clicks = data[:pages].values.sum { |p| p[:clicks] }
        data[:overall][:impressions] = total_impressions
        data[:overall][:clicks] = total_clicks
        data[:overall][:ctr] = total_impressions.positive? ? (total_clicks.to_f / total_impressions * 100).round(2) : 0
        data[:overall][:position] = data[:pages].values.sum { |p| p[:position] } / data[:pages].size
      end

      print_success("Parsed #{data[:pages].size} pages, #{data[:queries].size} queries")
      data
    rescue StandardError => e
      print_error("Error parsing CSV: #{e.message}")
      nil
    end
  end

  # Generate baseline report
  def generate_baseline_report
    lines = [
      '=' * 60,
      'SEO BASELINE REPORT - IT-Journey',
      "Generated: #{Time.now.strftime('%Y-%m-%d %H:%M')}",
      '=' * 60,
      '',
      '## Overall Metrics (Baseline)',
      ''
    ]

    overall = BASELINE_METRICS[:overall]
    targets = BASELINE_METRICS[:targets]

    lines << '| Metric | Baseline | Target | Gap |'
    lines << '|--------|----------|--------|-----|'
    lines << "| Average CTR | #{overall[:avg_ctr]}% | #{targets[:ctr]}% | #{(targets[:ctr] - overall[:avg_ctr]).round(1)}% |"
    lines << "| Average Position | #{overall[:avg_position]} | #{targets[:position]} | #{overall[:avg_position] - targets[:position]} positions |"
    lines << "| Monthly Impressions | #{overall[:total_impressions].to_s.reverse.gsub(/(\d{3})(?=\d)/, '\\1,').reverse} | +#{targets[:impressions_growth]}% | — |"
    lines << ''

    # Page-level baseline
    lines << '## Page-Level Baseline'
    lines << ''
    lines << '| Page | Impressions | CTR | Position | Status |'
    lines << '|------|-------------|-----|----------|--------|'

    BASELINE_METRICS[:pages].each do |page, metrics|
      status = metrics[:optimized] ? "✅ Optimized #{metrics[:optimized]}" : (metrics[:status] == 'performing_well' ? '⭐ Performing Well' : '⬜ Pending')
      short_page = page.length > 35 ? "#{page[0..32]}..." : page
      lines << "| #{short_page} | #{metrics[:impressions]} | #{metrics[:ctr]}% | #{metrics[:position]} | #{status} |"
    end
    lines << ''

    # New content tracking
    lines << '## New Content (Phase 3)'
    lines << ''
    lines << '| Content | Published | Target Keywords |'
    lines << '|---------|-----------|-----------------|'

    BASELINE_METRICS[:new_content].each do |_url, info|
      lines << "| #{info[:title]} | #{info[:published]} | #{info[:target_keywords][0..1].join(', ')} |"
    end

    lines.join("\n")
  end

  # Generate weekly review template
  def generate_weekly_template
    today = Date.today
    week_start = today - today.wday + 1 # Monday
    week_end = week_start + 6

    <<~TEMPLATE
      # Weekly SEO Review: #{week_start.strftime('%b %d')} - #{week_end.strftime('%b %d, %Y')}

      ## Data Collection Checklist

      - [ ] Export Google Search Console data (Performance > Export)
      - [ ] Save to `TODO/seo/data/gsc-#{today.strftime('%Y-%m-%d')}.csv`
      - [ ] Run comparison: `ruby scripts/ctr-report-generator.rb --parse TODO/seo/data/gsc-#{today.strftime('%Y-%m-%d')}.csv`

      ## Key Metrics This Week

      | Metric | Last Week | This Week | Change |
      |--------|-----------|-----------|--------|
      | Total Impressions | ___ | ___ | ___ |
      | Total Clicks | ___ | ___ | ___ |
      | Average CTR | ___% | ___% | ___ |
      | Average Position | ___ | ___ | ___ |

      ## Top Pages Performance

      | Page | Impressions | Clicks | CTR | Position | Δ CTR |
      |------|-------------|--------|-----|----------|-------|
      | Nerd Font Quest | ___ | ___ | ___% | ___ | ___ |
      | Bootable macOS Guide | ___ | ___ | ___% | ___ | ___ |
      | Django Pi Guide | ___ | ___ | ___% | ___ | ___ |
      | Bashcrawl Quest | ___ | ___ | ___% | ___ | ___ |

      ## New Content Tracking

      | Content | Impressions | Clicks | CTR | Position |
      |---------|-------------|--------|-----|----------|
      | Terminal Shortcuts | ___ | ___ | ___% | ___ |
      | VS Code Extensions | ___ | ___ | ___% | ___ |
      | Docker Tutorial | ___ | ___ | ___% | ___ |

      ## Insights & Actions

      ### Wins 🎉
      - 

      ### Issues 🔴
      - 

      ### Next Week Actions 📋
      - [ ] 
      - [ ] 

      ---
      *Report generated: #{Time.now.strftime('%Y-%m-%d %H:%M')}*
    TEMPLATE
  end

  # Generate opportunities report
  def generate_opportunities_report
    lines = [
      '=' * 60,
      'SEO IMPROVEMENT OPPORTUNITIES - IT-Journey',
      "Generated: #{Time.now.strftime('%Y-%m-%d %H:%M')}",
      '=' * 60,
      '',
      '## High-Opportunity Pages',
      '',
      'Pages with high impressions but low CTR (opportunity to improve):',
      '',
      '| Page | Impressions | Current CTR | Target CTR | Potential Clicks |'
    ]
    lines << '|------|-------------|-------------|------------|------------------|'

    opportunities = []
    BASELINE_METRICS[:pages].each do |page, metrics|
      target_ctr = metrics[:target_ctr] || BASELINE_METRICS[:targets][:ctr]
      potential_clicks = ((target_ctr - metrics[:ctr]) / 100.0 * metrics[:impressions]).round

      next unless potential_clicks.positive?

      opportunities << {
        page: page,
        impressions: metrics[:impressions],
        ctr: metrics[:ctr],
        target_ctr: target_ctr,
        potential: potential_clicks,
        title: metrics[:title]
      }
    end

    opportunities.sort_by { |o| -o[:potential] }.each do |opp|
      short_page = opp[:title] || (opp[:page].length > 30 ? "#{opp[:page][0..27]}..." : opp[:page])
      lines << "| #{short_page} | #{opp[:impressions]} | #{opp[:ctr]}% | #{opp[:target_ctr]}% | +#{opp[:potential]} |"
    end

    lines << ''
    lines << '## Quick Wins'
    lines << ''
    lines << 'Recommended actions to improve CTR:'
    lines << ''

    quick_wins = [
      '1. **Title Optimization**: Make titles more compelling with action verbs',
      '2. **Meta Descriptions**: Ensure all pages have 120-155 character descriptions',
      '3. **Rich Snippets**: Add structured data for how-to content',
      '4. **Internal Links**: Cross-link related quests and posts',
      '5. **Content Freshness**: Update lastmod dates when content changes'
    ]

    lines.concat(quick_wins)

    lines << ''
    lines << '## Zero-CTR Pages'
    lines << ''
    lines << 'Pages with impressions but zero clicks (need immediate attention):'
    lines << ''

    zero_ctr = BASELINE_METRICS[:pages].select { |_, m| m[:ctr].zero? && m[:impressions].positive? }
    if zero_ctr.any?
      lines << '| Page | Impressions | Optimization Status |'
      lines << '|------|-------------|---------------------|'
      zero_ctr.each do |page, metrics|
        status = metrics[:optimized] ? "✅ Optimized #{metrics[:optimized]}" : '⬜ Pending'
        lines << "| #{metrics[:title] || page} | #{metrics[:impressions]} | #{status} |"
      end
    else
      lines << '✅ No zero-CTR pages with significant impressions!'
    end

    lines.join("\n")
  end

  # Compare two datasets
  def generate_comparison_report(baseline_data, current_data)
    lines = [
      '=' * 60,
      'SEO COMPARISON REPORT - IT-Journey',
      "Generated: #{Time.now.strftime('%Y-%m-%d %H:%M')}",
      '=' * 60,
      '',
      '## Overall Metrics Comparison',
      ''
    ]

    lines << '| Metric | Baseline | Current | Change |'
    lines << '|--------|----------|---------|--------|'
    lines << "| Impressions | #{baseline_data[:overall][:impressions]} | #{current_data[:overall][:impressions]} | #{format_change_md(current_data[:overall][:impressions], baseline_data[:overall][:impressions])} |"
    lines << "| Clicks | #{baseline_data[:overall][:clicks]} | #{current_data[:overall][:clicks]} | #{format_change_md(current_data[:overall][:clicks], baseline_data[:overall][:clicks])} |"
    lines << "| CTR | #{baseline_data[:overall][:ctr]}% | #{current_data[:overall][:ctr]}% | #{format_change_md(current_data[:overall][:ctr], baseline_data[:overall][:ctr])} |"
    lines << ''

    lines.join("\n")
  end

  # Generate JSON metrics export
  def generate_metrics_json
    {
      generated: Time.now.iso8601,
      baseline: BASELINE_METRICS,
      summary: {
        total_tracked_pages: BASELINE_METRICS[:pages].size,
        new_content_count: BASELINE_METRICS[:new_content].size,
        avg_ctr_baseline: BASELINE_METRICS[:overall][:avg_ctr],
        target_ctr: BASELINE_METRICS[:targets][:ctr],
        pages_optimized: BASELINE_METRICS[:pages].count { |_, m| m[:optimized] },
        pages_performing_well: BASELINE_METRICS[:pages].count { |_, m| m[:status] == 'performing_well' }
      }
    }
  end

  # Save report to file
  def save_report(content, filename)
    ensure_dirs
    file_path = REPORTS_DIR / filename
    File.write(file_path, content)
    print_success("Report saved to: #{file_path}")
    file_path
  end
end

# Main execution
if __FILE__ == $PROGRAM_NAME
  options = {
    verbose: false,
    output: nil
  }

  command = nil
  input_file = nil

  OptionParser.new do |opts|
    opts.banner = 'Usage: ctr-report-generator.rb [command] [options]'

    opts.on('--baseline', 'Generate baseline metrics report') do
      command = :baseline
    end

    opts.on('--weekly', 'Generate weekly review template') do
      command = :weekly
    end

    opts.on('--opportunities', 'Show improvement opportunities') do
      command = :opportunities
    end

    opts.on('--parse FILE', 'Parse Google Search Console CSV export') do |file|
      command = :parse
      input_file = file
    end

    opts.on('--json', 'Export metrics as JSON') do
      command = :json
    end

    opts.on('-o', '--output FILE', 'Save report to file') do |file|
      options[:output] = file
    end

    opts.on('-v', '--verbose', 'Enable verbose output') do
      options[:verbose] = true
    end

    opts.on('-h', '--help', 'Show help') do
      puts opts
      puts "\nExamples:"
      puts '  ctr-report-generator.rb --baseline              # Show baseline metrics'
      puts '  ctr-report-generator.rb --weekly -o report.md   # Generate weekly template'
      puts '  ctr-report-generator.rb --opportunities         # Show improvement opportunities'
      puts '  ctr-report-generator.rb --parse data.csv        # Parse GSC export'
      puts '  ctr-report-generator.rb --json -o metrics.json  # Export as JSON'
      exit
    end
  end.parse!

  # Default to baseline if no command specified
  command ||= :baseline

  generator = CTRReportGenerator.new(verbose: options[:verbose])

  case command
  when :baseline
    report = generator.generate_baseline_report
    puts report
    generator.save_report(report, "baseline-report-#{Date.today}.md") if options[:output]

  when :weekly
    report = generator.generate_weekly_template
    puts report
    if options[:output]
      generator.save_report(report, options[:output])
    else
      generator.save_report(report, "weekly-review-#{Date.today}.md")
    end

  when :opportunities
    report = generator.generate_opportunities_report
    puts report
    generator.save_report(report, "opportunities-#{Date.today}.md") if options[:output]

  when :parse
    if input_file
      data = generator.parse_gsc_csv(input_file)
      if data
        puts "\n## Parsed Data Summary"
        puts "Pages: #{data[:pages].size}"
        puts "Queries: #{data[:queries].size}"
        puts "Total Impressions: #{data[:overall][:impressions]}"
        puts "Total Clicks: #{data[:overall][:clicks]}"
        puts "Average CTR: #{data[:overall][:ctr]}%"
      end
    else
      print_error('Please provide a CSV file with --parse FILE')
      exit 1
    end

  when :json
    metrics = generator.generate_metrics_json
    output = JSON.pretty_generate(metrics)
    puts output
    if options[:output]
      File.write(options[:output], output)
      print_success("JSON exported to: #{options[:output]}")
    end
  end
end
