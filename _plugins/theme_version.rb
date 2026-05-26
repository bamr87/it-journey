# frozen_string_literal: true

#
# File: theme_version.rb
# Path: _plugins/theme_version.rb
# Purpose: Automatically extract theme version from gem specification
#
# This plugin runs during Jekyll build and extracts version information
# from the active theme's gemspec, making it available as site.theme_specs
#
# Usage in templates: {{ site.theme_specs | where: "name", "theme-name" | map: "version" | first }}
#

module Jekyll
  class ThemeVersionGenerator < Generator
    safe true
    priority :high

    def generate(site)
      theme_specs = []

      # Try to get version from remote_theme or local theme
      if site.config['remote_theme']
        # For remote themes, we'll rely on the theme-info.html to show "Latest"
        # since we can't easily get the version without cloning the repo
        remote_theme = site.config['remote_theme']
        theme_specs << {
          'name' => remote_theme.split('/').last,
          'type' => 'remote',
          'repository' => remote_theme,
          'version' => 'latest'
        }
      elsif site.config['theme']
        # For local gem themes, try to extract version from Gem specification
        theme_name = site.config['theme']
        
        begin
          # Attempt to load the gem specification
          require 'rubygems'
          spec = Gem::Specification.find_by_name(theme_name)
          
          if spec
            theme_specs << {
              'name' => spec.name,
              'version' => spec.version.to_s,
              'type' => 'gem',
              'homepage' => spec.homepage,
              'summary' => spec.summary,
              'authors' => spec.authors
            }
          end
        rescue Gem::LoadError
          # Theme gem not found, just record basic info
          theme_specs << {
            'name' => theme_name,
            'version' => 'unknown',
            'type' => 'gem'
          }
        end
      end

      # Also scan for jekyll-theme-* gems that might be installed
      begin
        Gem::Specification.each do |spec|
          if spec.name =~ /^jekyll-theme-/
            theme_specs << {
              'name' => spec.name,
              'version' => spec.version.to_s,
              'type' => 'gem',
              'homepage' => spec.homepage,
              'summary' => spec.summary
            }
          end
        end
      rescue => e
        Jekyll.logger.warn "ThemeVersion:", "Could not scan gems: #{e.message}"
      end

      # Make theme specs available to templates
      site.config['theme_specs'] = theme_specs

      # Log the theme information
      theme_specs.each do |spec|
        Jekyll.logger.info "ThemeVersion:", "#{spec['name']} v#{spec['version']} (#{spec['type']})"
      end
    end
  end
end
