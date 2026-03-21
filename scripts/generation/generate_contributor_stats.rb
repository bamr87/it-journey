#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
require 'date'
require 'open3'

# Generates contributor statistics from git history and content files.
# Merges auto-generated stats into _data/contributors/{username}.yml
# while preserving user-editable profile fields.

class ContributorStatsGenerator
  PROJECT_ROOT = File.join(__dir__, '..', '..')
  CONTRIBUTORS_DIR = File.join(PROJECT_ROOT, '_data', 'contributors')
  QUESTS_DIR = File.join(PROJECT_ROOT, 'pages', '_quests')
  POSTS_DIR = File.join(PROJECT_ROOT, 'pages', '_posts')

  XP_PER_COMMIT = 10
  XP_PER_PR_MERGED = 50
  XP_PER_QUEST_AUTHORED = 200
  XP_PER_POST_AUTHORED = 100

  TIERS = {
    0 => 'Apprentice',
    1 => 'Apprentice',
    2 => 'Apprentice',
    3 => 'Apprentice',
    4 => 'Adventurer',
    5 => 'Adventurer',
    6 => 'Adventurer',
    7 => 'Adventurer',
    8 => 'Warrior',
    9 => 'Warrior',
    10 => 'Warrior',
    11 => 'Warrior',
    12 => 'Master',
    13 => 'Master',
    14 => 'Master',
    15 => 'Master'
  }.freeze

  ACHIEVEMENT_RULES = [
    { id: 'first_blood', name: 'First Blood', icon: '⚔️',
      description: 'Made your first commit', field: :total_commits, threshold: 1 },
    { id: 'ten_commits', name: 'Dedicated', icon: '🔟',
      description: 'Reached 10 commits', field: :total_commits, threshold: 10 },
    { id: 'centurion', name: 'Centurion', icon: '💯',
      description: 'Reached 100 commits', field: :total_commits, threshold: 100 },
    { id: 'guild_founder', name: 'Guild Founder', icon: '🏛️',
      description: 'Reached 500 commits — founder level', field: :total_commits, threshold: 500 },
    { id: 'quest_forger', name: 'Quest Forger', icon: '🏰',
      description: 'Authored your first quest', field: :total_quests_authored, threshold: 1 },
    { id: 'chronicler', name: 'Chronicler', icon: '📜',
      description: 'Published your first post', field: :total_posts_authored, threshold: 1 },
    { id: 'five_posts', name: 'Prolific Writer', icon: '✍️',
      description: 'Published 5 posts', field: :total_posts_authored, threshold: 5 },
    { id: 'marathon_runner', name: 'Marathon Runner', icon: '🏃',
      description: '7-day commit streak', field: :streak_days, threshold: 7 },
    { id: 'streak_master', name: 'Streak Master', icon: '🔥',
      description: '30-day commit streak', field: :streak_days, threshold: 30 },
    { id: 'polyglot', name: 'Polyglot', icon: '🌐',
      description: 'Commits touching 5+ languages', field: :language_count, threshold: 5 }
  ].freeze

  def initialize(username)
    @username = username
    @data_file = File.join(CONTRIBUTORS_DIR, "#{username}.yml")
  end

  def generate
    puts "🧙 Generating stats for contributor: #{@username}"

    unless File.exist?(@data_file)
      puts "❌ Contributor file not found: #{@data_file}"
      return false
    end

    existing = YAML.safe_load(File.read(@data_file), permitted_classes: [Date, Time]) || {}
    profile = existing['profile'] || {}

    github_username = profile.dig('links', 'github') || @username
    stats = compute_stats(github_username)
    achievements = compute_achievements(stats, existing['achievements'] || [])
    level = compute_level(stats)

    merged = {
      'profile' => profile,
      'stats' => stats,
      'achievements' => achievements,
      'level' => level
    }

    File.write(@data_file, yaml_header + YAML.dump(merged))
    puts "✅ Stats updated for #{@username}"
    display_summary(stats, level, achievements)
    true
  end

  private

  def yaml_header
    <<~HEADER
      # Contributor Profile: #{@username}
      # ============================
      # Fields under `profile` are user-editable. Customize freely!
      # Fields under `stats`, `achievements`, and `level` are auto-generated
      # by the contributor stats generator and overwritten on each CI run.
      #
      # Generated at: #{Time.now.strftime('%Y-%m-%dT%H:%M:%S%z')}

    HEADER
  end

  def compute_stats(github_username)
    commits_data = git_commit_stats(github_username)
    pr_count = git_merged_pr_count(github_username)
    quests = count_authored_content(QUESTS_DIR, github_username)
    posts = count_authored_content(POSTS_DIR, github_username)
    languages = git_top_languages(github_username)
    categories = content_top_categories(github_username)
    calendar = git_contribution_calendar(github_username)

    {
      'total_commits' => commits_data[:count],
      'total_prs_merged' => pr_count,
      'total_quests_authored' => quests,
      'total_posts_authored' => posts,
      'lines_added' => commits_data[:added],
      'lines_removed' => commits_data[:removed],
      'first_contribution_date' => commits_data[:first_date],
      'latest_contribution_date' => commits_data[:latest_date],
      'active_days' => commits_data[:active_days],
      'streak_days' => commits_data[:streak],
      'top_languages' => languages,
      'top_categories' => categories,
      'contribution_calendar' => calendar
    }
  end

  def git_commit_stats(username)
    # Get commit count and dates
    log_cmd = "git -C #{shell_escape(PROJECT_ROOT)} log --author=#{shell_escape(username)} --format=%aI --no-merges"
    dates_output, _status = Open3.capture2(log_cmd)
    dates = dates_output.strip.split("\n").reject(&:empty?).map { |d| Date.parse(d) rescue nil }.compact

    # Get lines added/removed
    stat_cmd = "git -C #{shell_escape(PROJECT_ROOT)} log --author=#{shell_escape(username)} --pretty=tformat: --numstat --no-merges"
    stat_output, _status = Open3.capture2(stat_cmd)
    added = 0
    removed = 0
    stat_output.strip.split("\n").each do |line|
      parts = line.split("\t")
      next if parts.length < 2
      added += parts[0].to_i if parts[0] != '-'
      removed += parts[1].to_i if parts[1] != '-'
    end

    unique_days = dates.map(&:to_s).uniq.sort
    streak = calculate_streak(unique_days)

    {
      count: dates.length,
      added: added,
      removed: removed,
      first_date: unique_days.first,
      latest_date: unique_days.last,
      active_days: unique_days.length,
      streak: streak
    }
  end

  def calculate_streak(sorted_date_strings)
    return 0 if sorted_date_strings.empty?

    today = Date.today
    dates = sorted_date_strings.map { |d| Date.parse(d) }.sort.reverse

    streak = 0
    expected = today

    dates.each do |d|
      if d == expected
        streak += 1
        expected -= 1
      elsif d == expected - 1
        # Allow one gap day for "yesterday" start
        streak += 1 if streak.zero?
        expected = d - 1
      elsif d < expected
        break
      end
    end

    streak
  end

  def git_merged_pr_count(username)
    # Count merge commits authored by user (approximation without GitHub API)
    cmd = "git -C #{shell_escape(PROJECT_ROOT)} log --author=#{shell_escape(username)} --merges --oneline"
    output, _status = Open3.capture2(cmd)
    output.strip.split("\n").reject(&:empty?).length
  end

  def count_authored_content(directory, username)
    return 0 unless Dir.exist?(directory)

    count = 0
    Dir.glob(File.join(directory, '**', '*.md')).each do |file|
      content = File.read(file)
      frontmatter = extract_frontmatter(content)
      next unless frontmatter

      author = (frontmatter['author'] || '').to_s.downcase
      if author.include?(username.downcase) || author.include?(@username.downcase)
        count += 1
      end
    end
    count
  end

  def git_top_languages(username)
    cmd = "git -C #{shell_escape(PROJECT_ROOT)} log --author=#{shell_escape(username)} --pretty=tformat: --name-only --no-merges"
    output, _status = Open3.capture2(cmd)

    ext_counts = Hash.new(0)
    output.strip.split("\n").each do |file|
      ext = File.extname(file).downcase.delete('.')
      next if ext.empty? || %w[lock json yml yaml].include?(ext)
      ext_counts[ext] += 1
    end

    ext_counts.sort_by { |_, v| -v }.first(5).map { |ext, count| { 'name' => ext, 'count' => count } }
  end

  def content_top_categories(username)
    categories = Hash.new(0)

    [POSTS_DIR, QUESTS_DIR].each do |dir|
      next unless Dir.exist?(dir)
      Dir.glob(File.join(dir, '**', '*.md')).each do |file|
        content = File.read(file)
        fm = extract_frontmatter(content)
        next unless fm
        author = (fm['author'] || '').to_s.downcase
        next unless author.include?(username.downcase) || author.include?(@username.downcase)

        (fm['categories'] || []).each do |cat|
          categories[cat.to_s.strip] += 1 if cat.is_a?(String)
        end
      end
    end

    categories.sort_by { |_, v| -v }.first(5).map { |cat, count| { 'name' => cat, 'count' => count } }
  end

  def git_contribution_calendar(username)
    # Last 52 weeks of weekly commit counts
    weeks = []
    52.times do |i|
      week_end = Date.today - (i * 7)
      week_start = week_end - 6
      cmd = "git -C #{shell_escape(PROJECT_ROOT)} log --author=#{shell_escape(username)} " \
            "--after=#{shell_escape(week_start.to_s)} --before=#{shell_escape((week_end + 1).to_s)} " \
            "--oneline --no-merges"
      output, _status = Open3.capture2(cmd)
      count = output.strip.split("\n").reject(&:empty?).length
      weeks.unshift(count)
    end
    weeks
  end

  def compute_achievements(stats, existing_achievements)
    existing_ids = existing_achievements.map { |a| a['id'] }
    today = Date.today.to_s
    new_achievements = existing_achievements.dup

    stat_values = {
      total_commits: stats['total_commits'],
      total_prs_merged: stats['total_prs_merged'],
      total_quests_authored: stats['total_quests_authored'],
      total_posts_authored: stats['total_posts_authored'],
      streak_days: stats['streak_days'],
      language_count: (stats['top_languages'] || []).length
    }

    ACHIEVEMENT_RULES.each do |rule|
      next if existing_ids.include?(rule[:id])
      value = stat_values[rule[:field]] || 0
      if value >= rule[:threshold]
        new_achievements << {
          'id' => rule[:id],
          'name' => rule[:name],
          'icon' => rule[:icon],
          'description' => rule[:description],
          'earned_date' => today
        }
      end
    end

    new_achievements
  end

  def compute_level(stats)
    xp = (stats['total_commits'] * XP_PER_COMMIT) +
         (stats['total_prs_merged'] * XP_PER_PR_MERGED) +
         (stats['total_quests_authored'] * XP_PER_QUEST_AUTHORED) +
         (stats['total_posts_authored'] * XP_PER_POST_AUTHORED)

    level_num = xp > 0 ? [Math.log2([xp.to_f / 100, 1].max).floor, 15].min : 0
    binary_level = level_num.to_s(2).rjust(4, '0')
    tier = TIERS[level_num]

    next_level_xp = 100 * (2**(level_num + 1))
    current_level_xp = level_num > 0 ? 100 * (2**level_num) : 0
    xp_range = next_level_xp - current_level_xp
    xp_into_level = xp - current_level_xp
    progress = xp_range > 0 ? [[((xp_into_level.to_f / xp_range) * 100).round, 0].max, 100].min : 0

    {
      'xp' => xp,
      'current_level' => binary_level,
      'tier' => tier,
      'xp_to_next_level' => [next_level_xp - xp, 0].max,
      'progress_percent' => progress
    }
  end

  def extract_frontmatter(content)
    return nil unless content.start_with?('---')
    parts = content.split('---', 3)
    return nil if parts.length < 3
    YAML.safe_load(parts[1], permitted_classes: [Date, Time], aliases: true)
  rescue Psych::SyntaxError, Psych::BadAlias
    nil
  end

  def shell_escape(str)
    Shellwords.escape(str.to_s)
  end

  def display_summary(stats, level, achievements)
    puts "  📊 Commits: #{stats['total_commits']}"
    puts "  📝 Posts: #{stats['total_posts_authored']} | Quests: #{stats['total_quests_authored']}"
    puts "  📈 Lines: +#{stats['lines_added']} / -#{stats['lines_removed']}"
    puts "  🔥 Streak: #{stats['streak_days']} days | Active: #{stats['active_days']} days"
    puts "  ⭐ XP: #{level['xp']} | Level: #{level['current_level']} (#{level['tier']})"
    puts "  🏆 Achievements: #{achievements.length}"
  end
end

# --- Main ---
require 'shellwords'

if ARGV.empty?
  puts "Usage: ruby generate_contributor_stats.rb <username> | --all"
  exit 1
end

contributors_dir = File.join(__dir__, 'contributors')

if ARGV[0] == '--all'
  files = Dir.glob(File.join(contributors_dir, '*.yml')).reject { |f| File.basename(f).start_with?('_') }
  if files.empty?
    puts "❌ No contributor files found in #{contributors_dir}"
    exit 1
  end
  files.each do |f|
    username = File.basename(f, '.yml')
    ContributorStatsGenerator.new(username).generate
  end
else
  username = ARGV[0]
  generator = ContributorStatsGenerator.new(username)
  exit 1 unless generator.generate
end
