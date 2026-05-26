# frozen_string_literal: true

#
# File: preview_image_generator.rb
# Path: _plugins/preview_image_generator.rb
# Purpose: Jekyll plugin for AI-powered preview image generation
#
# This plugin provides Jekyll integration for the preview image generator,
# including Liquid tags, filters, and hooks for automatic image generation.
#
# Usage in templates:
#   {% preview_image_status %}              - Shows missing preview count
#   {{ page | preview_image_path }}         - Returns the preview image path
#   {{ page | has_preview_image }}          - Returns true/false
#
# Configuration in _config.yml:
#   preview_images:
#     enabled: true
#     provider: openai
#     auto_generate: false  # Set to true to generate during build (slow!)
#     style: "retro pixel art, 8-bit video game aesthetic"
#

module Jekyll
  module PreviewImageGenerator
    # Configuration defaults
    DEFAULTS = {
      'enabled' => true,
      'provider' => 'openai',
      'model' => 'dall-e-3',
      'size' => '1792x1024',
      'quality' => 'standard',
      'style' => 'retro pixel art, 8-bit video game aesthetic, vibrant colors, nostalgic, clean pixel graphics',
      'style_modifiers' => 'pixelated, retro gaming style, CRT screen glow effect, limited color palette',
      'output_dir' => 'assets/images/previews',
      'assets_prefix' => '/assets',
      'auto_prefix' => true,
      'auto_generate' => false,
      'collections' => ['posts', 'docs', 'quickstart']
    }.freeze

    # Get configuration with defaults
    def self.config(site)
      site_config = site.config['preview_images'] || {}
      DEFAULTS.merge(site_config)
    end

    # Check if a document has a preview image defined
    def self.has_preview?(doc)
      cached = cached_preview_entry(doc)
      return cached['has_preview'] unless cached.nil?

      preview = doc.data['preview']
      return false if preview.nil? || preview.to_s.strip.empty?
      
      # Reject non-path values (text descriptions used as preview)
      return false unless preview.match?(/\.(png|jpe?g|gif|svg|webp)$/i) || preview.start_with?('http')
      
      # Check if the preview file actually exists
      site = doc.site
      config = self.config(site)
      
      # External URL — assume it exists
      return true if preview.start_with?('http')
      
      # Normalize the preview path using assets_prefix
      normalized_preview = normalize_preview_path(preview, config)
      
      # Build candidate file paths to check
      candidates = []
      if normalized_preview.start_with?('/')
        candidates << File.join(site.source, normalized_preview.sub(/^\//, ''))
        candidates << File.join(site.source, 'assets', normalized_preview.sub(/^\//, ''))
      else
        candidates << File.join(site.source, 'assets', normalized_preview)
        candidates << File.join(site.source, normalized_preview)
        candidates << File.join(site.source, config['output_dir'], normalized_preview)
      end
      
      candidates.any? { |path| File.exist?(path) }
    end

    # Normalize a preview path by adding assets_prefix if needed
    def self.normalize_preview_path(preview, config)
      return preview if preview.nil? || preview.to_s.strip.empty?
      return preview if preview.start_with?('http')
      
      assets_prefix = config['assets_prefix'] || '/assets'
      auto_prefix = config['auto_prefix'] != false  # Default to true
      
      # If auto_prefix is enabled and path doesn't already contain assets_prefix
      if auto_prefix && !preview.include?(assets_prefix)
        "#{assets_prefix}#{preview}"
      else
        preview
      end
    end

    # Get the preview image path for a document
    def self.preview_path(doc)
      cached = cached_preview_entry(doc)
      return cached['path'] unless cached.nil?

      preview = doc.data['preview']
      return nil if preview.nil? || preview.to_s.strip.empty?
      
      # Reject non-path values
      return nil unless preview.match?(/\.(png|jpe?g|gif|svg|webp)$/i) || preview.start_with?('http')
      
      site = doc.site
      config = self.config(site)
      
      # If it's an external URL, return as-is
      return preview if preview.start_with?('http')
      
      # Normalize path with assets_prefix
      normalize_preview_path(preview, config)
    end

    # Get list of documents missing preview images
    def self.missing_previews(site)
      build_index(site)['missing']
    end

    def self.build_index(site)
      cached = site.data['preview_image_index']
      return cached if cached

      config = self.config(site)
      index = {}
      missing = []

      preview_documents(site, config).each do |doc, collection_name|
        key = preview_cache_key(doc)
        next if index.key?(key)

        preview = doc.data['preview']
        normalized_path = nil
        has_preview = false

        if preview && !preview.to_s.strip.empty? && (preview.match?(/\.(png|jpe?g|gif|svg|webp)$/i) || preview.start_with?('http'))
          normalized_path = preview.start_with?('http') ? preview : normalize_preview_path(preview, config)
          has_preview = preview.start_with?('http') || preview_file_exists?(site, normalized_path, config)
        end

        index[key] = {
          'has_preview' => has_preview,
          'path' => normalized_path,
          'collection' => collection_name
        }

        next if has_preview

        missing << {
          'path' => doc.relative_path,
          'title' => doc.data['title'] || File.basename(doc.relative_path),
          'collection' => collection_name
        }
      end

      site.data['preview_image_index'] = {
        'documents' => index,
        'missing' => missing
      }
    end

    def self.cached_preview_entry(doc)
      return nil unless doc.respond_to?(:site) && doc.site && doc.site.data['preview_image_index']

      doc.site.data['preview_image_index']['documents'][preview_cache_key(doc)]
    end

    def self.preview_documents(site, config)
      docs = []
      Array(config['collections']).each do |collection_name|
        collection = site.collections[collection_name]
        next unless collection

        collection.docs.each { |doc| docs << [doc, collection_name] }
      end

      site.posts.docs.each { |doc| docs << [doc, 'posts'] } if site.respond_to?(:posts) && site.posts
      docs
    end

    def self.preview_cache_key(doc)
      doc.respond_to?(:relative_path) ? doc.relative_path : doc.path
    end

    def self.preview_file_exists?(site, normalized_preview, config)
      candidates = []
      if normalized_preview.start_with?('/')
        candidates << File.join(site.source, normalized_preview.sub(/^\//, ''))
        candidates << File.join(site.source, 'assets', normalized_preview.sub(/^\//, ''))
      else
        candidates << File.join(site.source, 'assets', normalized_preview)
        candidates << File.join(site.source, normalized_preview)
        candidates << File.join(site.source, config['output_dir'], normalized_preview)
      end

      candidates.any? { |path| File.exist?(path) }
    end

    # Generate a preview image filename from document
    def self.generate_filename(doc)
      # Use the document's slug or generate from title
      slug = doc.data['slug'] || doc.basename_without_ext
      
      # Sanitize the slug for use as filename
      sanitized = slug.to_s.downcase
                       .gsub(/[^a-z0-9\-_]/, '-')
                       .gsub(/-+/, '-')
                       .gsub(/^-|-$/, '')
      
      "#{sanitized}-preview.png"
    end
  end

  # ==========================================================================
  # Liquid Filters
  # ==========================================================================
  
  module PreviewImageFilters
    # Check if a page/document has a preview image
    # Usage: {{ page | has_preview_image }}
    def has_preview_image(doc)
      return false unless doc.is_a?(Hash) || doc.respond_to?(:data)
      
      # Handle both Hash (from assign) and Document objects
      if doc.is_a?(Hash)
        preview = doc['preview']
        return false if preview.nil? || preview.to_s.strip.empty?
        # Only consider values that look like image paths or URLs
        preview.to_s.match?(/\.(png|jpe?g|gif|svg|webp)$/i) || preview.to_s.start_with?('http')
      else
        PreviewImageGenerator.has_preview?(doc)
      end
    end

    # Get the preview image path
    # Usage: {{ page | preview_image_path }}
    def preview_image_path(doc)
      return nil unless doc.is_a?(Hash) || doc.respond_to?(:data)
      
      if doc.is_a?(Hash)
        preview = doc['preview']
        return nil if preview.nil? || preview.to_s.strip.empty?
        return nil unless preview.to_s.match?(/\.(png|jpe?g|gif|svg|webp)$/i) || preview.to_s.start_with?('http')
        
        return preview if preview.start_with?('/') || preview.start_with?('http')
        
        # Get config from context if available
        site_config = @context.registers[:site].config['preview_images'] || {}
        output_dir = site_config['output_dir'] || 'assets/images/previews'
        "#{output_dir}/#{preview}"
      else
        PreviewImageGenerator.preview_path(doc)
      end
    end

    # Get suggested filename for a preview image
    # Usage: {{ page | preview_filename }}
    def preview_filename(doc)
      return nil unless doc.respond_to?(:data) || doc.respond_to?(:basename_without_ext)
      PreviewImageGenerator.generate_filename(doc)
    end
  end

  # ==========================================================================
  # Liquid Tags
  # ==========================================================================
  
  # Tag to display preview image status/count
  # Usage: {% preview_image_status %}
  class PreviewImageStatusTag < Liquid::Tag
    def render(context)
      site = context.registers[:site]
      missing = PreviewImageGenerator.missing_previews(site)
      
      if missing.empty?
        "<span class=\"badge bg-success\">All preview images present</span>"
      else
        "<span class=\"badge bg-warning text-dark\">#{missing.length} missing preview images</span>"
      end
    end
  end

  # Tag to list missing preview images
  # Usage: {% preview_images_missing %}
  class PreviewImagesMissingTag < Liquid::Tag
    def render(context)
      site = context.registers[:site]
      missing = PreviewImageGenerator.missing_previews(site)
      
      return "<p>All documents have preview images!</p>" if missing.empty?
      
      html = "<ul class=\"list-group\">\n"
      missing.each do |item|
        html += "  <li class=\"list-group-item d-flex justify-content-between align-items-center\">\n"
        html += "    <span>#{item['title']}</span>\n"
        html += "    <span class=\"badge bg-secondary\">#{item['collection']}</span>\n"
        html += "  </li>\n"
      end
      html += "</ul>"
      html
    end
  end

  # ==========================================================================
  # Generator Hook (optional auto-generation during build)
  # ==========================================================================
  
  class PreviewImageGeneratorHook < Generator
    safe true
    priority :low

    def generate(site)
      config = PreviewImageGenerator.config(site)
      
      return unless config['enabled']
      
      # Store missing previews in site data for access in templates
      preview_index = PreviewImageGenerator.build_index(site)
      site.data['preview_images_missing'] = preview_index['missing']
      site.data['preview_images_config'] = config
      
      # Log status
      missing_count = site.data['preview_images_missing'].length
      if missing_count > 0
        Jekyll.logger.info "Preview Images:", "#{missing_count} documents missing preview images"
        Jekyll.logger.info "Preview Images:", "Run 'scripts/generate-preview-images.sh' to generate them"
      end
      
      # Auto-generate is disabled by default (it's slow and requires API calls)
      # Users should run the shell script manually or via CI/CD
      if config['auto_generate']
        Jekyll.logger.warn "Preview Images:", "Auto-generation is enabled but not implemented in plugin"
        Jekyll.logger.warn "Preview Images:", "Use 'scripts/generate-preview-images.sh' instead"
      end
    end
  end

  # ==========================================================================
  # Register Liquid components
  # ==========================================================================
  
  Liquid::Template.register_filter(PreviewImageFilters)
  Liquid::Template.register_tag('preview_image_status', PreviewImageStatusTag)
  Liquid::Template.register_tag('preview_images_missing', PreviewImagesMissingTag)
end
