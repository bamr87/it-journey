# -*- encoding: utf-8 -*-
# stub: jekyll-theme-zer0 0.4.0 ruby lib

Gem::Specification.new do |s|
  s.name = "jekyll-theme-zer0".freeze
  s.version = "0.4.0"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.metadata = { "allowed_push_host" => "https://rubygems.org", "changelog_uri" => "https://github.com/bamr87/zer0-mistakes/blob/main/CHANGELOG.md", "documentation_uri" => "https://github.com/bamr87/zer0-mistakes#readme", "homepage_uri" => "https://github.com/bamr87/zer0-mistakes", "plugin_type" => "theme", "source_code_uri" => "https://github.com/bamr87/zer0-mistakes" } if s.respond_to? :metadata=
  s.require_paths = ["lib".freeze]
  s.authors = ["Amr Abdel".freeze]
  s.date = "2025-10-10"
  s.description = "Bootstrap Jekyll theme for headless Github Pages CMS with Docker-first development approach".freeze
  s.email = ["amr@it-journey.dev".freeze]
  s.homepage = "https://github.com/bamr87/zer0-mistakes".freeze
  s.licenses = ["MIT".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 2.7.0".freeze)
  s.rubygems_version = "3.4.20".freeze
  s.summary = "Jekyll theme based on bootstrap and compatible with github pages".freeze

  s.installed_by_version = "3.4.20" if s.respond_to? :installed_by_version

  s.specification_version = 4

  s.add_runtime_dependency(%q<jekyll>.freeze, [">= 0"])
  s.add_development_dependency(%q<bundler>.freeze, ["~> 2.3"])
  s.add_development_dependency(%q<rake>.freeze, ["~> 13.0"])
  s.add_development_dependency(%q<rspec>.freeze, ["~> 3.0"])
end
