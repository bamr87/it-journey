#!/usr/bin/env ruby
# frozen_string_literal: true

# frontmatter-validator.rb
#
# IT-Journey Frontmatter Validation Tool
# Validates YAML frontmatter across all content files for quality, SEO optimization,
# and consistency with project standards.
#
# Features:
# - Multi-content type support (posts, quests, docs, notes)
# - SEO field validation (description length, keywords)
# - Required field checking by content type
# - JSON report generation for automation
# - Severity-based issue categorization
#
# Author: IT-Journey Team
# Created: 2025-12-20
# Version: 1.0.0

require 'yaml'
require 'json'
require 'optparse'
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

# Represents a single validation issue
class ValidationIssue
  attr_accessor :severity, :field, :message, :suggestion

  def initialize(severity:, field:, message:, suggestion: nil)
    @severity = severity
    @field = field
    @message = message
    @suggestion = suggestion
  end

  def to_h
    {
      severity: @severity,
      field: @field,
      message: @message,
      suggestion: @suggestion
    }
  end
end

# Stores validation results for a single file
class FileValidationResult
  attr_accessor :file_path, :content_type, :is_valid, :issues, :seo_score, :max_seo_score, :frontmatter_present

  def initialize(file_path:, content_type:)
    @file_path = file_path
    @content_type = content_type
    @is_valid = true
    @issues = []
    @seo_score = 0
    @max_seo_score = 100
    @frontmatter_present = true
  end

  def error_count
    @issues.count { |i| i.severity == 'error' }
  end

  def warning_count
    @issues.count { |i| i.severity == 'warning' }
  end

  def info_count
    @issues.count { |i| i.severity == 'info' }
  end
end

# Aggregated validation report
class ValidationReport
  attr_accessor :timestamp, :total_files, :valid_files, :invalid_files,
                :total_errors, :total_warnings, :files_by_type, :results, :average_seo_score

  def initialize
    @timestamp = Time.now.iso8601
    @total_files = 0
    @valid_files = 0
    @invalid_files = 0
    @total_errors = 0
    @total_warnings = 0
    @files_by_type = {}
    @results = []
    @average_seo_score = 0.0
  end
end

# Main validator class
class FrontmatterValidator
  # Field requirements by content type
  REQUIRED_FIELDS = {
    'posts' => %w[title description date categories],
    'quests' => %w[title description level difficulty estimated_time permalink categories],
    'docs' => %w[title description],
    'notes' => %w[title],
    'other' => %w[title]
  }.freeze

  # SEO-recommended fields
  SEO_FIELDS = {
    'posts' => %w[keywords tags excerpt author lastmod meta],
    'quests' => %w[keywords tags excerpt author lastmod preview],
    'docs' => %w[keywords tags lastmod],
    'notes' => %w[tags],
    'other' => %w[tags]
  }.freeze

  # SEO constraints
  SEO_CONSTRAINTS = {
    description_min: 50,
    description_max: 160,
    description_optimal_min: 120,
    description_optimal_max: 155,
    title_max: 60,
    keywords_min: 3,
    keywords_max: 10
  }.freeze

  # Directories to skip
  SKIP_DIRS = %w[_site node_modules .git __pycache__ templates ARCHIVE work test TODO].freeze

  # Files to skip
  SKIP_FILES = %w[README.md CHANGELOG.md LICENSE CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md].freeze

  def initialize(verbose: false)
    @verbose = verbose
    @results = []
  end

  def log(level, msg)
    return unless @verbose

    case level
    when 'info' then print_info(msg)
    when 'warning' then print_warning(msg)
    when 'error' then print_error(msg)
    end
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
    # Skip specific filenames
    return true if SKIP_FILES.include?(File.basename(file_path))

    # Skip files in certain directories
    path_parts = Pathname.new(file_path).each_filename.to_a
    SKIP_DIRS.any? { |skip_dir| path_parts.include?(skip_dir) }
  end

  def extract_frontmatter(file_path)
    content = File.read(file_path, encoding: 'UTF-8')

    # Match frontmatter between --- delimiters
    match = content.match(/\A---\s*\n(.*?)\n---\s*\n?(.*)/m)

    unless match
      return [nil, content, 'No frontmatter found (missing --- delimiters)']
    end

    begin
      frontmatter = YAML.safe_load(match[1], permitted_classes: [Date, Time])
      body = match[2]
      return [nil, body, 'Empty frontmatter'] if frontmatter.nil?

      [frontmatter, body, nil]
    rescue Psych::SyntaxError => e
      [nil, content, "YAML parsing error: #{e.message}"]
    end
  rescue IOError, Errno::ENOENT => e
    [nil, '', "Could not read file: #{e.message}"]
  end

  def validate_required_fields(fm, content_type, result)
    required = REQUIRED_FIELDS[content_type] || REQUIRED_FIELDS['other']

    required.each do |field_name|
      if !fm.key?(field_name)
        result.issues << ValidationIssue.new(
          severity: 'error',
          field: field_name,
          message: "Missing required field: #{field_name}",
          suggestion: "Add '#{field_name}:' to frontmatter"
        )
        result.is_valid = false
      elsif fm[field_name].nil? || (fm[field_name].is_a?(String) && fm[field_name].strip.empty?)
        result.issues << ValidationIssue.new(
          severity: 'error',
          field: field_name,
          message: "Required field is empty: #{field_name}",
          suggestion: "Provide a value for '#{field_name}'"
        )
        result.is_valid = false
      end
    end
  end

  def validate_seo_fields(fm, content_type, result)
    constraints = SEO_CONSTRAINTS
    score = 0

    # Description validation (40 points)
    description = fm['description'].to_s
    if !description.empty?
      desc_len = description.length

      if desc_len < constraints[:description_min]
        result.issues << ValidationIssue.new(
          severity: 'warning',
          field: 'description',
          message: "Description too short (#{desc_len} chars). Minimum: #{constraints[:description_min]}",
          suggestion: 'Expand description with more detail about content and benefits'
        )
        score += 10
      elsif desc_len > constraints[:description_max]
        result.issues << ValidationIssue.new(
          severity: 'warning',
          field: 'description',
          message: "Description too long (#{desc_len} chars). May be truncated in search results. Max: #{constraints[:description_max]}",
          suggestion: 'Shorten description to under 160 characters'
        )
        score += 25
      elsif desc_len >= constraints[:description_optimal_min] && desc_len <= constraints[:description_optimal_max]
        score += 40
        result.issues << ValidationIssue.new(
          severity: 'info',
          field: 'description',
          message: "Description length optimal (#{desc_len} chars)"
        )
      else
        score += 30
      end
    else
      result.issues << ValidationIssue.new(
        severity: 'error',
        field: 'description',
        message: 'Missing description - critical for SEO',
        suggestion: 'Add a compelling 120-155 character description'
      )
    end

    # Title validation (20 points)
    title = fm['title'].to_s
    if !title.empty?
      title_len = title.length
      if title_len > constraints[:title_max]
        result.issues << ValidationIssue.new(
          severity: 'warning',
          field: 'title',
          message: "Title may be truncated in search (#{title_len} chars). Max: #{constraints[:title_max]}",
          suggestion: 'Consider shortening title'
        )
        score += 10
      else
        score += 20
      end
    end

    # Keywords validation (20 points)
    keywords = fm['keywords']
    if keywords
      if keywords.is_a?(Array)
        kw_count = keywords.length
        if kw_count < constraints[:keywords_min]
          result.issues << ValidationIssue.new(
            severity: 'warning',
            field: 'keywords',
            message: "Too few keywords (#{kw_count}). Recommended: #{constraints[:keywords_min]}-#{constraints[:keywords_max]}",
            suggestion: 'Add more relevant keywords'
          )
          score += 10
        elsif kw_count > constraints[:keywords_max]
          result.issues << ValidationIssue.new(
            severity: 'info',
            field: 'keywords',
            message: "Many keywords (#{kw_count}). Consider focusing on top #{constraints[:keywords_max]}"
          )
          score += 15
        else
          score += 20
        end
      else
        result.issues << ValidationIssue.new(
          severity: 'warning',
          field: 'keywords',
          message: 'Keywords should be a list/array',
          suggestion: "Format as: keywords:\n  - keyword1\n  - keyword2"
        )
      end
    else
      result.issues << ValidationIssue.new(
        severity: 'warning',
        field: 'keywords',
        message: 'Missing keywords field',
        suggestion: 'Add keywords for better discoverability'
      )
    end

    # Tags validation (10 points)
    seo_fields = SEO_FIELDS[content_type] || SEO_FIELDS['other']
    if seo_fields.include?('tags')
      tags = fm['tags']
      if tags.is_a?(Array) && tags.length >= 2
        score += 10
      elsif tags
        score += 5
        result.issues << ValidationIssue.new(
          severity: 'info',
          field: 'tags',
          message: 'Consider adding more tags'
        )
      else
        result.issues << ValidationIssue.new(
          severity: 'info',
          field: 'tags',
          message: 'No tags defined',
          suggestion: 'Add relevant tags for categorization'
        )
      end
    end

    # Lastmod validation (5 points)
    if fm['lastmod']
      score += 5
    else
      result.issues << ValidationIssue.new(
        severity: 'info',
        field: 'lastmod',
        message: 'No lastmod date',
        suggestion: 'Add lastmod to indicate content freshness'
      )
    end

    # Author validation (5 points)
    score += 5 if fm['author']

    result.seo_score = score
    result.max_seo_score = 100
  end

  def validate_quest_specific(fm, result)
    # Level format validation (4-digit)
    level = fm['level'].to_s
    unless level.empty?
      unless level.match?(/^\d{4}$/)
        result.issues << ValidationIssue.new(
          severity: 'warning',
          field: 'level',
          message: "Level format unusual: #{level}. Expected: 4-digit (e.g., '0010')",
          suggestion: 'Use 4-digit format for consistency'
        )
      end
    end

    # Difficulty validation
    valid_difficulties = ['🟢 Easy', '🟡 Medium', '🔴 Hard', '⚔️ Epic',
                          'beginner', 'intermediate', 'advanced', 'expert']
    difficulty = fm['difficulty'].to_s
    unless difficulty.empty?
      unless valid_difficulties.any? { |d| d.casecmp(difficulty).zero? }
        result.issues << ValidationIssue.new(
          severity: 'info',
          field: 'difficulty',
          message: "Non-standard difficulty: #{difficulty}",
          suggestion: "Consider using: #{valid_difficulties[0..3].join(', ')}"
        )
      end
    end

    # Permalink validation
    permalink = fm['permalink'].to_s
    unless permalink.empty?
      unless permalink.start_with?('/quests/')
        result.issues << ValidationIssue.new(
          severity: 'warning',
          field: 'permalink',
          message: "Quest permalink should start with '/quests/': #{permalink}",
          suggestion: 'Update permalink to follow quest URL structure'
        )
      end
    end
  end

  def validate_file(file_path)
    content_type = detect_content_type(file_path)
    result = FileValidationResult.new(file_path: file_path.to_s, content_type: content_type)

    # Extract frontmatter
    fm, _body, error = extract_frontmatter(file_path)

    if error
      result.frontmatter_present = false
      result.is_valid = false
      result.issues << ValidationIssue.new(
        severity: 'error',
        field: 'frontmatter',
        message: error,
        suggestion: 'Ensure file starts with --- followed by YAML and closing ---'
      )
      return result
    end

    # Validate required fields
    validate_required_fields(fm, content_type, result)

    # Validate SEO fields
    validate_seo_fields(fm, content_type, result)

    # Content-type specific validation
    validate_quest_specific(fm, result) if content_type == 'quests'

    result
  end

  def scan_directory(directory)
    results = []

    Dir.glob(File.join(directory, '**', '*.md')).each do |md_file|
      next if should_skip?(md_file)

      log('info', "Validating: #{md_file}")
      result = validate_file(md_file)
      results << result
    end

    results
  rescue StandardError => e
    print_error("Error scanning directory: #{e.message}")
    []
  end

  def generate_report(results)
    report = ValidationReport.new
    report.total_files = results.length
    report.results = results

    files_by_type = Hash.new(0)
    total_seo_score = 0
    seo_scored_files = 0

    results.each do |r|
      # Count by validity
      if r.is_valid
        report.valid_files += 1
      else
        report.invalid_files += 1
      end

      # Count by type
      files_by_type[r.content_type] += 1

      # Aggregate errors/warnings
      report.total_errors += r.error_count
      report.total_warnings += r.warning_count

      # Calculate average SEO score
      if r.frontmatter_present
        total_seo_score += r.seo_score
        seo_scored_files += 1
      end
    end

    report.files_by_type = files_by_type
    report.average_seo_score = seo_scored_files.positive? ? (total_seo_score.to_f / seo_scored_files).round(1) : 0.0

    report
  end

  def print_summary(report)
    puts "\n#{Colors::BOLD}#{'=' * 60}#{Colors::NC}"
    puts "#{Colors::BOLD}📊 Frontmatter Validation Report#{Colors::NC}"
    puts "#{Colors::BOLD}#{'=' * 60}#{Colors::NC}\n"

    puts "📅 Timestamp: #{report.timestamp}"
    puts "📁 Files Scanned: #{report.total_files}"
    puts

    # Validity summary
    valid_pct = report.total_files.positive? ? (report.valid_files.to_f / report.total_files * 100) : 0
    puts "#{Colors::GREEN}✅ Valid Files: #{report.valid_files}#{Colors::NC}"
    puts "#{Colors::RED}❌ Invalid Files: #{report.invalid_files}#{Colors::NC}"
    puts "📈 Validity Rate: #{valid_pct.round(1)}%"
    puts

    # Issue summary
    puts "#{Colors::RED}🚨 Total Errors: #{report.total_errors}#{Colors::NC}"
    puts "#{Colors::YELLOW}⚠️  Total Warnings: #{report.total_warnings}#{Colors::NC}"
    puts

    # SEO score
    puts "🔍 Average SEO Score: #{report.average_seo_score}/100"
    puts

    # Files by type
    puts "#{Colors::BOLD}📂 Files by Type:#{Colors::NC}"
    report.files_by_type.sort.each do |content_type, count|
      puts "   #{content_type}: #{count}"
    end
    puts

    # Show problem files
    problem_files = report.results.select { |r| r.error_count.positive? }
    if problem_files.any?
      puts "#{Colors::BOLD}🔴 Files Requiring Attention:#{Colors::NC}"
      problem_files.sort_by { |r| -r.error_count }.first(10).each do |r|
        rel_path = File.basename(r.file_path)
        puts "   #{Colors::RED}❌#{Colors::NC} #{rel_path}: #{r.error_count} errors, #{r.warning_count} warnings"
      end
    else
      puts "#{Colors::GREEN}✅ No files with errors!#{Colors::NC}"
    end

    puts "\n#{Colors::BOLD}#{'=' * 60}#{Colors::NC}\n"
  end

  def save_json_report(report, output_path)
    report_dict = {
      timestamp: report.timestamp,
      summary: {
        total_files: report.total_files,
        valid_files: report.valid_files,
        invalid_files: report.invalid_files,
        total_errors: report.total_errors,
        total_warnings: report.total_warnings,
        average_seo_score: report.average_seo_score,
        files_by_type: report.files_by_type
      },
      files: report.results.map do |r|
        {
          file_path: r.file_path,
          content_type: r.content_type,
          is_valid: r.is_valid,
          frontmatter_present: r.frontmatter_present,
          seo_score: r.seo_score,
          error_count: r.error_count,
          warning_count: r.warning_count,
          issues: r.issues.map(&:to_h)
        }
      end
    }

    File.write(output_path, JSON.pretty_generate(report_dict))
    print_success("JSON report saved to: #{output_path}")
  end
end

# Main execution
if __FILE__ == $PROGRAM_NAME
  options = {
    verbose: false,
    output: nil,
    errors_only: false,
    type: 'all'
  }

  OptionParser.new do |opts|
    opts.banner = 'Usage: frontmatter-validator.rb [options] PATH'

    opts.on('-v', '--verbose', 'Enable verbose output') do
      options[:verbose] = true
    end

    opts.on('-o', '--output FILE', 'Output JSON report to file') do |file|
      options[:output] = file
    end

    opts.on('--errors-only', 'Only show files with errors') do
      options[:errors_only] = true
    end

    opts.on('--type TYPE', %w[posts quests docs notes all], 'Filter by content type') do |type|
      options[:type] = type
    end

    opts.on('-h', '--help', 'Show help') do
      puts opts
      puts "\nExamples:"
      puts '  frontmatter-validator.rb pages/                    # Validate all files in pages/'
      puts '  frontmatter-validator.rb pages/_posts/ -v          # Verbose validation of posts'
      puts '  frontmatter-validator.rb pages/_quests/ -o report.json   # Save JSON report'
      puts '  frontmatter-validator.rb . --errors-only           # Show only files with errors'
      exit
    end
  end.parse!

  if ARGV.empty?
    print_error('Please provide a path to validate')
    exit 1
  end

  target_path = ARGV[0]

  unless File.exist?(target_path)
    print_error("Path does not exist: #{target_path}")
    exit 1
  end

  # Initialize validator
  validator = FrontmatterValidator.new(verbose: options[:verbose])

  # Run validation
  print_info("Starting frontmatter validation: #{target_path}")

  results = if File.file?(target_path)
              [validator.validate_file(target_path)]
            else
              validator.scan_directory(target_path)
            end

  # Filter by content type if specified
  results = results.select { |r| r.content_type == options[:type] } if options[:type] != 'all'

  # Filter errors-only if specified
  results = results.select { |r| r.error_count.positive? } if options[:errors_only]

  # Generate report
  report = validator.generate_report(results)

  # Print summary
  validator.print_summary(report)

  # Save JSON report if requested
  validator.save_json_report(report, options[:output]) if options[:output]

  # Exit with error code if issues found
  exit(report.invalid_files.positive? ? 1 : 0)
end
