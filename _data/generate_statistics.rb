#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
require 'date'

# Script to generate dynamic content statistics for IT-Journey posts
# This script analyzes all posts in the _posts directory and generates
# comprehensive statistics that can be rendered using Liquid templates

class ContentStatisticsGenerator
  POSTS_DIR = File.join(__dir__, '..', 'pages', '_posts')
  OUTPUT_FILE = File.join(__dir__, '..', '_data', 'content_statistics.yml')
  CONFIG_FILE = File.join(__dir__, 'statistics_config.yml')
  INDEX_FILE = '2000-01-01-index.md'

  def initialize
    @config = load_config
    @stats = {
      'generated_at' => Time.now.strftime('%Y-%m-%dT%H:%M:%S.%L%z'),
      'total_posts' => 0,
      'categories' => {},
      'tags' => {},
      'authors' => {},
      'years' => {},
      'date_range' => {},
      'skill_levels' => {},
      'focus_areas' => {},
      'content_types' => {},
      'drafts' => 0,
      'published' => 0
    }
  end

  def generate
    puts "📊 Generating content statistics for IT-Journey..."
    
    analyze_posts
    calculate_derived_stats
    save_statistics
    
    puts "✅ Statistics generated successfully!"
    puts "📁 Output saved to: #{OUTPUT_FILE}"
    display_summary
  end

  private

  def load_config
    if File.exist?(CONFIG_FILE)
      YAML.load_file(CONFIG_FILE)
    else
      puts "⚠️  Configuration file not found: #{CONFIG_FILE}"
      puts "📝 Using default configuration..."
      default_config
    end
  end

  def default_config
    {
      'focus_areas' => {
        'AI & Machine Learning' => ['ai', 'ml', 'machine-learning'],
        'Web Development' => ['web', 'javascript', 'jekyll'],
        'DevOps & Infrastructure' => ['devops', 'docker', 'ci/cd'],
        'System Administration' => ['linux', 'windows', 'system'],
        'Programming & Scripting' => ['programming', 'python', 'bash'],
        'Data & Analytics' => ['data', 'database', 'analytics']
      },
      'skill_levels' => {
        'beginner' => ['beginner', 'intro', 'basics'],
        'intermediate' => ['intermediate', 'practical'],
        'advanced' => ['advanced', 'expert', 'architecture'],
        'expert' => ['expert', 'research', 'innovation']
      },
      'content_types' => {
        'Tutorial' => ['tutorial', 'guide', 'how-to'],
        'Article' => ['article', 'analysis', 'insights'],
        'Journal Entry' => ['journal', 'learning-journey'],
        'Documentation' => ['documentation', 'reference']
      }
    }
  end

  def analyze_posts
    post_files = Dir.glob(File.join(POSTS_DIR, '*.md')).reject { |f| File.basename(f) == INDEX_FILE }
    
    @stats['total_posts'] = post_files.length
    
    post_files.each do |file|
      analyze_post_file(file)
    end
  end

  def analyze_post_file(file)
    content = File.read(file)
    frontmatter = extract_frontmatter(content)
    
    return unless frontmatter
    
    # Count drafts vs published
    if frontmatter['draft'] == true
      @stats['drafts'] += 1
    else
      @stats['published'] += 1
    end
    
    # Analyze categories
    analyze_categories(frontmatter['categories'] || [])
    
    # Analyze tags
    analyze_tags(frontmatter['tags'] || [])
    
    # Analyze authors
    analyze_authors(frontmatter['author'])
    
    # Analyze dates
    analyze_dates(frontmatter['date'])
    
    # Analyze skill levels (from tags or categories)
    analyze_skill_levels(frontmatter)
    
    # Analyze focus areas (from categories and tags)
    analyze_focus_areas(frontmatter)
    
    # Analyze content types (from layout, categories, or inferred)
    analyze_content_types(frontmatter)
  end

  def extract_frontmatter(content)
    return nil unless content.start_with?('---')
    
    parts = content.split('---', 3)
    return nil if parts.length < 3
    
    begin
      YAML.safe_load(parts[1], [Date, Time])
    rescue Psych::SyntaxError => e
      puts "⚠️  YAML parsing error: #{e.message}"
      nil
    end
  end

  def analyze_categories(categories)
    return unless categories.is_a?(Array)
    
    categories.each do |category|
      next unless category.is_a?(String)
      
      clean_category = category.strip.downcase
      @stats['categories'][clean_category] ||= 0
      @stats['categories'][clean_category] += 1
    end
  end

  def analyze_tags(tags)
    return unless tags.is_a?(Array)
    
    tags.each do |tag|
      next unless tag.is_a?(String)
      
      clean_tag = tag.strip.downcase
      @stats['tags'][clean_tag] ||= 0
      @stats['tags'][clean_tag] += 1
    end
  end

  def analyze_authors(author)
    return unless author.is_a?(String)
    
    clean_author = author.strip
    @stats['authors'][clean_author] ||= 0
    @stats['authors'][clean_author] += 1
  end

  def analyze_dates(date_field)
    return unless date_field
    
    begin
      date = if date_field.is_a?(String)
               Date.parse(date_field)
             elsif date_field.is_a?(Date)
               date_field
             else
               return
             end
      
      year = date.year.to_s
      @stats['years'][year] ||= 0
      @stats['years'][year] += 1
    rescue Date::Error => e
      puts "⚠️  Date parsing error: #{e.message}"
    end
  end

  def analyze_skill_levels(frontmatter)
    return unless @config['skill_levels']
    
    all_text = [
      frontmatter['title'],
      frontmatter['description'],
      frontmatter['categories'],
      frontmatter['tags']
    ].flatten.compact.join(' ').downcase
    
    @config['skill_levels'].each do |level, indicators|
      if indicators.any? { |indicator| all_text.include?(indicator) }
        @stats['skill_levels'][level] ||= 0
        @stats['skill_levels'][level] += 1
      end
    end
  end

  def analyze_focus_areas(frontmatter)
    return unless @config['focus_areas']
    
    all_text = [
      frontmatter['title'],
      frontmatter['description'],
      frontmatter['categories'],
      frontmatter['tags']
    ].flatten.compact.join(' ').downcase
    
    @config['focus_areas'].each do |area, keywords|
      if keywords.any? { |keyword| all_text.include?(keyword) }
        @stats['focus_areas'][area] ||= 0
        @stats['focus_areas'][area] += 1
      end
    end
  end

  def analyze_content_types(frontmatter)
    return unless @config['content_types']
    
    # Check layout first
    layout = frontmatter['layout']
    if layout
      case layout.downcase
      when 'journals', 'journal'
        increment_content_type('Journal Entry')
      when 'tutorial', 'guide'
        increment_content_type('Tutorial')
      when 'article'
        increment_content_type('Article')
      when 'documentation', 'docs'
        increment_content_type('Documentation')
      end
    end
    
    # Check title and description
    all_text = [
      frontmatter['title'],
      frontmatter['description']
    ].compact.join(' ').downcase
    
    @config['content_types'].each do |type, keywords|
      if keywords.any? { |keyword| all_text.include?(keyword) }
        increment_content_type(type)
      end
    end
    
    # Default fallback
    increment_content_type('Article') if @stats['content_types'].empty?
  end

  def increment_content_type(type)
    @stats['content_types'][type] ||= 0
    @stats['content_types'][type] += 1
  end

  def calculate_derived_stats
    # Calculate date range
    years = @stats['years'].keys.map(&:to_i).sort
    if years.any?
      @stats['date_range'] = {
        'earliest' => years.first,
        'latest' => years.last,
        'span_years' => years.last - years.first + 1
      }
    end
    
    # Sort categories and tags by count (descending)
    @stats['categories'] = @stats['categories'].sort_by { |_, count| -count }.to_h
    @stats['tags'] = @stats['tags'].sort_by { |_, count| -count }.to_h
    @stats['authors'] = @stats['authors'].sort_by { |_, count| -count }.to_h
    @stats['focus_areas'] = @stats['focus_areas'].sort_by { |_, count| -count }.to_h
    @stats['content_types'] = @stats['content_types'].sort_by { |_, count| -count }.to_h
    @stats['skill_levels'] = @stats['skill_levels'].sort_by { |_, count| -count }.to_h
    
    # Calculate percentages
    total = @stats['total_posts']
    @stats['category_count'] = @stats['categories'].length
    @stats['tag_count'] = @stats['tags'].length
    @stats['author_count'] = @stats['authors'].length
    
    # Top categories and tags
    @stats['top_categories'] = @stats['categories'].first(5).to_h
    @stats['top_tags'] = @stats['tags'].first(10).to_h
  end

  def save_statistics
    File.open(OUTPUT_FILE, 'w') do |file|
      file.write("# Auto-generated content statistics for IT-Journey\n")
      file.write("# Generated at: #{@stats['generated_at']}\n")
      file.write(@stats.to_yaml)
    end
  end

  def display_summary
    puts "\n📊 Content Statistics Summary:"
    puts "━" * 50
    puts "📝 Total Posts: #{@stats['total_posts']}"
    puts "📚 Published: #{@stats['published']}"
    puts "📝 Drafts: #{@stats['drafts']}"
    puts "🏷️  Categories: #{@stats['category_count']}"
    puts "🔖 Tags: #{@stats['tag_count']}"
    puts "👥 Authors: #{@stats['author_count']}"
    puts "📅 Date Range: #{@stats['date_range']['earliest']}-#{@stats['date_range']['latest']}"
    puts "━" * 50
    
    puts "\n🏆 Top Categories:"
    @stats['top_categories'].each { |cat, count| puts "   #{cat}: #{count}" }
    
    puts "\n🎯 Focus Areas:"
    @stats['focus_areas'].each { |area, count| puts "   #{area}: #{count}" }
  end
end

# Run the generator if this script is executed directly
if __FILE__ == $0
  generator = ContentStatisticsGenerator.new
  generator.generate
end
