# frozen_string_literal: true

# Regenerates content statistics on every Jekyll build.
#
# Runs after site init, writes _data/content_statistics.yml, and reloads
# site.data so templates see fresh counts and generated_at (build time).
#
# Disable in _config.yml:
#   content_statistics:
#     auto_generate: false
#
# Manual refresh: ruby _data/generate_statistics.rb  (or rake stats:generate)

require 'yaml'

module Jekyll
  module ContentStatisticsBuild
    module_function

    def generator_script(site)
      candidates = [
        File.join(site.source, '_data', 'generate_statistics.rb')
      ]

      theme_root = site.theme&.root
      candidates << File.join(theme_root, '_data', 'generate_statistics.rb') if theme_root

      candidates.find { |path| File.exist?(path) }
    end
  end
end

Jekyll::Hooks.register :site, :after_init do |site|
  auto_generate = site.config.dig('content_statistics', 'auto_generate')
  auto_generate = true if auto_generate.nil?
  next unless auto_generate

  generator_script = Jekyll::ContentStatisticsBuild.generator_script(site)
  unless generator_script
    Jekyll.logger.debug 'ContentStatistics:', 'Generator script not found; skipping'
    next
  end

  begin
    load generator_script unless defined?(SiteStatisticsGenerator)

    generator = SiteStatisticsGenerator.new(site.source)
    generator.generate!

    stats_file = File.join(site.source, '_data', 'content_statistics.yml')
    if File.exist?(stats_file)
      site.data ||= {}
      site.data['content_statistics'] = YAML.safe_load_file(
        stats_file,
        permitted_classes: [Date, Time],
        aliases: true
      )
      overview = site.data['content_statistics']['overview'] || {}
      Jekyll.logger.info(
        'ContentStatistics:',
        "Updated at #{site.data['content_statistics']['generated_at']} " \
        "(#{overview['total_posts']} posts, #{overview['total_categories']} categories, " \
        "#{overview['total_tags']} tags)"
      )
    end
  rescue StandardError => e
    Jekyll.logger.warn 'ContentStatistics:', "Generation failed: #{e.message}"
  end
end
