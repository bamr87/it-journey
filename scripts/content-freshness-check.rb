#!/usr/bin/env ruby
# frozen_string_literal: true

# content-freshness-check.rb
#
# IT-Journey Content Freshness Checker
# Scans all content files and identifies stale content based on lastmod dates.
# Helps maintain content quality by flagging pages that need review/updates.
#
# Features:
# - Scan all markdown files for lastmod dates
# - Categorize by freshness (fresh, aging, stale, critical)
# - Generate actionable reports
# - Export JSON for automation
# - Support for content-type specific thresholds
#
# Author: IT-Journey Team
# Created: 2025-12-20
# Version: 1.0.0
#
# Usage:
#   ruby content-freshness-check.rb pages/           # Scan directory
#   ruby content-freshness-check.rb --stale-only     # Show only stale content
#   ruby content-freshness-check.rb --json -o report.json  # Export JSON

require 'yaml'
require 'json'
require 'optparse'
require 'date'
require 'pathname'
require 'time'

# ANSI color codes
module Colors
  RED = "\e[0;31m"
  GREEN = "\e[0;32m"
  YELLOW = "\e[1;33m"
  BLUE = "\e[0;34m"
  MAGENTA = "\e[0;35m"
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

# Content freshness status
class FreshnessStatus
  FRESH = 'fresh'       # Updated within threshold
  AGING = 'aging'       # Approaching staleness
  STALE = 'stale'       # Needs review
  CRITICAL = 'critical' # Urgently needs update
  UNKNOWN = 'unknown'   # No lastmod date
end

# Single file freshness result
class FileResult
  attr_accessor :file_path, :title, :content_type, :lastmod, :created,
                :days_since_update, :status, :priority

  def initialize(file_path:)
    @file_path = file_path
    @title = nil
    @content_type = 'other'
    @lastmod = nil
    @created = nil
    @days_since_update = nil
    @status = FreshnessStatus::UNKNOWN
    @priority = 0
  end

  def to_h
    {
      file_path: @file_path,
      title: @title,
      content_type: @content_type,
      lastmod: @lastmod&.to_s,
      created: @created&.to_s,
      days_since_update: @days_since_update,
      status: @status,
      priority: @priority
    }
  end
end

# Aggregated report
class FreshnessReport
  attr_accessor :timestamp, :total_files, :files_with_lastmod, :files_without_lastmod,
                :by_status, :by_type, :results, :average_age

  def initialize
    @timestamp = Time.now.iso8601
    @total_files = 0
    @files_with_lastmod = 0
    @files_without_lastmod = 0
    @by_status = Hash.new(0)
    @by_type = Hash.new(0)
    @results = []
    @average_age = 0
  end
end

# Main checker class
class ContentFreshnessChecker
  # Freshness thresholds in days (customizable by content type)
  THRESHOLDS = {
    default: {
      fresh: 30,      # 0-30 days = fresh
      aging: 60,      # 31-60 days = aging
      stale: 90,      # 61-90 days = stale
      critical: 90    # >90 days = critical
    },
    posts: {
      fresh: 60,      # Blog posts can be slightly older
      aging: 120,
      stale: 180,
      critical: 180
    },
    quests: {
      fresh: 45,      # Quests should be kept fresh
      aging: 90,
      stale: 120,
      critical: 120
    },
    docs: {
      fresh: 60,      # Docs updated less frequently
      aging: 120,
      stale: 180,
      critical: 180
    }
  }.freeze

  # Directories to skip
  SKIP_DIRS = %w[_site node_modules .git __pycache__ templates ARCHIVE work test TODO].freeze

  # Files to skip
  SKIP_FILES = %w[README.md CHANGELOG.md LICENSE CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md].freeze

  def initialize(verbose: false)
    @verbose = verbose
    @today = Date.today
  end

  def log(msg)
    print_info(msg) if @verbose
  end

  def detect_content_type(file_path)
    path_str = file_path.to_s.downcase

    if path_str.include?('_posts') || path_str.include?('/posts/')
      'posts'
    elsif path_str.include?('_quests') || path_str.include?('/quests/')
      'quests'
    elsif path_str.include?('_docs') || path_str.include?('/docs/')
      'docs'
    elsif path_str.include?('_notes') || path_str.include?('/notes/')
      'notes'
    else
      'other'
    end
  end

  def should_skip?(file_path)
    return true if SKIP_FILES.include?(File.basename(file_path))

    path_parts = Pathname.new(file_path).each_filename.to_a
    SKIP_DIRS.any? { |skip_dir| path_parts.include?(skip_dir) }
  end

  def extract_frontmatter(file_path)
    content = File.read(file_path, encoding: 'UTF-8')

    match = content.match(/\A---\s*\n(.*?)\n---\s*\n?/m)
    return nil unless match

    YAML.safe_load(match[1], permitted_classes: [Date, Time])
  rescue StandardError => e
    log("Error parsing #{file_path}: #{e.message}")
    nil
  end

  def parse_date(value)
    return nil if value.nil?

    case value
    when Date
      value
    when Time
      value.to_date
    when String
      # Try parsing various date formats
      begin
        Date.parse(value)
      rescue ArgumentError
        nil
      end
    else
      nil
    end
  end

  def calculate_status(days_old, content_type)
    thresholds = THRESHOLDS[content_type.to_sym] || THRESHOLDS[:default]

    if days_old.nil?
      FreshnessStatus::UNKNOWN
    elsif days_old <= thresholds[:fresh]
      FreshnessStatus::FRESH
    elsif days_old <= thresholds[:aging]
      FreshnessStatus::AGING
    elsif days_old <= thresholds[:stale]
      FreshnessStatus::STALE
    else
      FreshnessStatus::CRITICAL
    end
  end

  def calculate_priority(status, days_old, impressions = 0)
    # Priority: Higher = more urgent
    base_priority = case status
                    when FreshnessStatus::CRITICAL then 100
                    when FreshnessStatus::STALE then 70
                    when FreshnessStatus::AGING then 40
                    when FreshnessStatus::UNKNOWN then 30
                    else 0
                    end

    # Add age factor
    age_factor = [days_old.to_i / 10, 20].min

    # Add impressions factor (if available)
    impressions_factor = [impressions / 100, 10].min

    base_priority + age_factor + impressions_factor
  end

  def check_file(file_path)
    result = FileResult.new(file_path: file_path.to_s)
    result.content_type = detect_content_type(file_path)

    fm = extract_frontmatter(file_path)
    return result unless fm

    result.title = fm['title']
    result.lastmod = parse_date(fm['lastmod'])
    result.created = parse_date(fm['date'] || fm['created'])

    if result.lastmod
      result.days_since_update = (@today - result.lastmod).to_i
    elsif result.created
      result.days_since_update = (@today - result.created).to_i
    end

    result.status = calculate_status(result.days_since_update, result.content_type)
    result.priority = calculate_priority(result.status, result.days_since_update)

    result
  end

  def scan_directory(directory)
    results = []

    Dir.glob(File.join(directory, '**', '*.md')).each do |md_file|
      next if should_skip?(md_file)

      log("Checking: #{md_file}")
      result = check_file(md_file)
      results << result
    end

    results
  rescue StandardError => e
    print_error("Error scanning directory: #{e.message}")
    []
  end

  def generate_report(results)
    report = FreshnessReport.new
    report.total_files = results.size
    report.results = results

    total_age = 0
    aged_files = 0

    results.each do |r|
      # Count by status
      report.by_status[r.status] += 1

      # Count by type
      report.by_type[r.content_type] += 1

      # Track lastmod presence
      if r.lastmod
        report.files_with_lastmod += 1
        total_age += r.days_since_update if r.days_since_update
        aged_files += 1 if r.days_since_update
      else
        report.files_without_lastmod += 1
      end
    end

    report.average_age = aged_files.positive? ? (total_age.to_f / aged_files).round(1) : 0

    report
  end

  def print_summary(report)
    puts "\n#{Colors::BOLD}#{'=' * 60}#{Colors::NC}"
    puts "#{Colors::BOLD}📅 Content Freshness Report#{Colors::NC}"
    puts "#{Colors::BOLD}#{'=' * 60}#{Colors::NC}\n"

    puts "📆 Report Date: #{Date.today}"
    puts "📁 Files Scanned: #{report.total_files}"
    puts "📊 Average Content Age: #{report.average_age} days"
    puts

    # Freshness summary
    puts "#{Colors::BOLD}📈 Freshness Status:#{Colors::NC}"
    
    fresh = report.by_status[FreshnessStatus::FRESH]
    aging = report.by_status[FreshnessStatus::AGING]
    stale = report.by_status[FreshnessStatus::STALE]
    critical = report.by_status[FreshnessStatus::CRITICAL]
    unknown = report.by_status[FreshnessStatus::UNKNOWN]

    puts "   #{Colors::GREEN}✅ Fresh (0-30 days):#{Colors::NC} #{fresh}"
    puts "   #{Colors::YELLOW}⏳ Aging (31-60 days):#{Colors::NC} #{aging}"
    puts "   #{Colors::YELLOW}⚠️  Stale (61-90 days):#{Colors::NC} #{stale}"
    puts "   #{Colors::RED}🚨 Critical (>90 days):#{Colors::NC} #{critical}"
    puts "   #{Colors::BLUE}❓ Unknown (no lastmod):#{Colors::NC} #{unknown}"
    puts

    # Health score calculation
    if report.files_with_lastmod.positive?
      healthy_files = fresh + aging
      health_score = (healthy_files.to_f / report.files_with_lastmod * 100).round(1)
      
      health_color = if health_score >= 80
                       Colors::GREEN
                     elsif health_score >= 60
                       Colors::YELLOW
                     else
                       Colors::RED
                     end
      
      puts "#{Colors::BOLD}🏥 Content Health Score: #{health_color}#{health_score}%#{Colors::NC}"
      puts
    end

    # Files by type
    puts "#{Colors::BOLD}📂 Files by Type:#{Colors::NC}"
    report.by_type.sort.each do |content_type, count|
      puts "   #{content_type}: #{count}"
    end
    puts

    # Lastmod coverage
    coverage = report.total_files.positive? ? (report.files_with_lastmod.to_f / report.total_files * 100).round(1) : 0
    puts "#{Colors::BOLD}📋 Lastmod Coverage:#{Colors::NC} #{coverage}% (#{report.files_with_lastmod}/#{report.total_files})"
    puts

    # Critical/Stale items needing attention
    needs_attention = report.results.select { |r| [FreshnessStatus::STALE, FreshnessStatus::CRITICAL].include?(r.status) }
    if needs_attention.any?
      puts "#{Colors::BOLD}🔴 Content Requiring Attention:#{Colors::NC}"
      needs_attention.sort_by { |r| -r.priority }.first(15).each do |r|
        status_icon = r.status == FreshnessStatus::CRITICAL ? '🚨' : '⚠️'
        status_color = r.status == FreshnessStatus::CRITICAL ? Colors::RED : Colors::YELLOW
        title = r.title || File.basename(r.file_path)
        title = title.length > 40 ? "#{title[0..37]}..." : title
        puts "   #{status_color}#{status_icon}#{Colors::NC} #{title} (#{r.days_since_update} days)"
      end
    else
      puts "#{Colors::GREEN}✅ No content requires immediate attention!#{Colors::NC}"
    end

    # Files without lastmod
    no_lastmod = report.results.select { |r| r.status == FreshnessStatus::UNKNOWN }
    if no_lastmod.any? && no_lastmod.size <= 10
      puts
      puts "#{Colors::BOLD}📝 Files Missing lastmod:#{Colors::NC}"
      no_lastmod.first(10).each do |r|
        title = r.title || File.basename(r.file_path)
        title = title.length > 50 ? "#{title[0..47]}..." : title
        puts "   #{Colors::BLUE}❓#{Colors::NC} #{title}"
      end
    elsif no_lastmod.any?
      puts
      puts "#{Colors::YELLOW}📝 #{no_lastmod.size} files are missing lastmod dates#{Colors::NC}"
    end

    puts "\n#{Colors::BOLD}#{'=' * 60}#{Colors::NC}\n"
  end

  def generate_markdown_report(report)
    lines = [
      "# 📅 Content Freshness Report",
      "",
      "**Generated**: #{Time.now.strftime('%Y-%m-%d %H:%M')}",
      "**Files Scanned**: #{report.total_files}",
      "**Average Age**: #{report.average_age} days",
      "",
      "## 📈 Freshness Summary",
      "",
      "| Status | Count | Description |",
      "|--------|-------|-------------|",
      "| ✅ Fresh | #{report.by_status[FreshnessStatus::FRESH]} | Updated within 30 days |",
      "| ⏳ Aging | #{report.by_status[FreshnessStatus::AGING]} | 31-60 days old |",
      "| ⚠️ Stale | #{report.by_status[FreshnessStatus::STALE]} | 61-90 days old |",
      "| 🚨 Critical | #{report.by_status[FreshnessStatus::CRITICAL]} | Over 90 days old |",
      "| ❓ Unknown | #{report.by_status[FreshnessStatus::UNKNOWN]} | No lastmod date |",
      ""
    ]

    # Health score
    if report.files_with_lastmod.positive?
      healthy = report.by_status[FreshnessStatus::FRESH] + report.by_status[FreshnessStatus::AGING]
      score = (healthy.to_f / report.files_with_lastmod * 100).round(1)
      emoji = score >= 80 ? '🟢' : (score >= 60 ? '🟡' : '🔴')
      lines << "## 🏥 Content Health Score: #{emoji} #{score}%"
      lines << ""
    end

    # Content needing attention
    needs_attention = report.results.select { |r| [FreshnessStatus::STALE, FreshnessStatus::CRITICAL].include?(r.status) }
    if needs_attention.any?
      lines << "## 🔴 Content Requiring Attention"
      lines << ""
      lines << "| Priority | Title | Type | Days Old | Status |"
      lines << "|----------|-------|------|----------|--------|"
      
      needs_attention.sort_by { |r| -r.priority }.first(20).each do |r|
        title = r.title || File.basename(r.file_path)
        title = title.length > 35 ? "#{title[0..32]}..." : title
        status_emoji = r.status == FreshnessStatus::CRITICAL ? '🚨' : '⚠️'
        lines << "| #{r.priority} | #{title} | #{r.content_type} | #{r.days_since_update} | #{status_emoji} #{r.status} |"
      end
      lines << ""
    end

    # Recommendations
    lines << "## 📋 Recommendations"
    lines << ""
    
    if report.by_status[FreshnessStatus::CRITICAL].positive?
      lines << "1. **Urgent**: #{report.by_status[FreshnessStatus::CRITICAL]} files need immediate review (>90 days old)"
    end
    
    if report.by_status[FreshnessStatus::STALE].positive?
      lines << "2. **Soon**: #{report.by_status[FreshnessStatus::STALE]} files should be reviewed within 2 weeks"
    end
    
    if report.files_without_lastmod.positive?
      lines << "3. **Metadata**: Add `lastmod` dates to #{report.files_without_lastmod} files"
    end

    lines << ""
    lines << "---"
    lines << "*Run `ruby scripts/content-freshness-check.rb --help` for options*"

    lines.join("\n")
  end

  def save_json_report(report, output_path)
    report_dict = {
      timestamp: report.timestamp,
      summary: {
        total_files: report.total_files,
        files_with_lastmod: report.files_with_lastmod,
        files_without_lastmod: report.files_without_lastmod,
        average_age_days: report.average_age,
        by_status: report.by_status,
        by_type: report.by_type
      },
      files: report.results.map(&:to_h)
    }

    File.write(output_path, JSON.pretty_generate(report_dict))
    print_success("JSON report saved to: #{output_path}")
  end

  def save_markdown_report(report, output_path)
    content = generate_markdown_report(report)
    File.write(output_path, content)
    print_success("Markdown report saved to: #{output_path}")
  end
end

# Main execution
if __FILE__ == $PROGRAM_NAME
  options = {
    verbose: false,
    output: nil,
    format: 'terminal',
    filter_status: nil
  }

  OptionParser.new do |opts|
    opts.banner = 'Usage: content-freshness-check.rb [options] PATH'

    opts.on('-v', '--verbose', 'Enable verbose output') do
      options[:verbose] = true
    end

    opts.on('-o', '--output FILE', 'Save report to file') do |file|
      options[:output] = file
    end

    opts.on('--json', 'Output as JSON') do
      options[:format] = 'json'
    end

    opts.on('--markdown', 'Output as Markdown') do
      options[:format] = 'markdown'
    end

    opts.on('--stale-only', 'Show only stale and critical content') do
      options[:filter_status] = [FreshnessStatus::STALE, FreshnessStatus::CRITICAL]
    end

    opts.on('--aging', 'Show aging, stale, and critical content') do
      options[:filter_status] = [FreshnessStatus::AGING, FreshnessStatus::STALE, FreshnessStatus::CRITICAL]
    end

    opts.on('--no-lastmod', 'Show only files without lastmod') do
      options[:filter_status] = [FreshnessStatus::UNKNOWN]
    end

    opts.on('-h', '--help', 'Show help') do
      puts opts
      puts "\nExamples:"
      puts '  content-freshness-check.rb pages/              # Check all content'
      puts '  content-freshness-check.rb pages/ --stale-only # Show only stale'
      puts '  content-freshness-check.rb pages/ --json -o report.json'
      puts '  content-freshness-check.rb pages/ --markdown -o report.md'
      exit
    end
  end.parse!

  target_path = ARGV[0] || 'pages/'

  unless File.exist?(target_path)
    print_error("Path does not exist: #{target_path}")
    exit 1
  end

  # Initialize checker
  checker = ContentFreshnessChecker.new(verbose: options[:verbose])

  # Run scan
  print_info("Scanning content freshness: #{target_path}")

  results = if File.file?(target_path)
              [checker.check_file(target_path)]
            else
              checker.scan_directory(target_path)
            end

  # Apply status filter if specified
  if options[:filter_status]
    results = results.select { |r| options[:filter_status].include?(r.status) }
  end

  # Generate report
  report = checker.generate_report(results)

  # Output based on format
  case options[:format]
  when 'json'
    if options[:output]
      checker.save_json_report(report, options[:output])
    else
      puts JSON.pretty_generate({
        timestamp: report.timestamp,
        summary: {
          total_files: report.total_files,
          by_status: report.by_status,
          average_age_days: report.average_age
        },
        files: report.results.map(&:to_h)
      })
    end
  when 'markdown'
    if options[:output]
      checker.save_markdown_report(report, options[:output])
    else
      puts checker.generate_markdown_report(report)
    end
  else
    checker.print_summary(report)
    checker.save_markdown_report(report, options[:output]) if options[:output]
  end

  # Exit with code based on critical content
  critical_count = report.by_status[FreshnessStatus::CRITICAL]
  exit(critical_count.positive? ? 1 : 0)
end
