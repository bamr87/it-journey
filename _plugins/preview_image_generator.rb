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
      preview = doc.data['preview']
      return false if preview.nil? || preview.to_s.strip.empty?
      
      # Check if the preview file actually exists
      site = doc.site
      config = self.config(site)
      
      # Build the full path
      preview_path = if preview.start_with?('/')
                       File.join(site.source, preview)
                     elsif preview.start_with?('http')
                       return true  # External URL, assume it exists
                     else
                       File.join(site.source, config['output_dir'], preview)
                     end
      
      File.exist?(preview_path)
    end

    # Get the preview image path for a document
    def self.preview_path(doc)
      preview = doc.data['preview']
      return nil if preview.nil? || preview.to_s.strip.empty?
      
      site = doc.site
      config = self.config(site)
      
      # If it's already a full path or URL, return as-is
      return preview if preview.start_with?('/') || preview.start_with?('http')
      
      # Build relative path from output_dir
      "#{config['output_dir']}/#{preview}"
    end

    # Get list of documents missing preview images
    def self.missing_previews(site)
      config = self.config(site)
      missing = []
      
      config['collections'].each do |collection_name|
        collection = site.collections[collection_name]
        next unless collection
        
        collection.docs.each do |doc|
          unless has_preview?(doc)
            missing << {
              'path' => doc.relative_path,
              'title' => doc.data['title'] || File.basename(doc.relative_path),
              'collection' => collection_name
            }
          end
        end
      end
      
      # Also check posts (which are special in Jekyll)
      site.posts.docs.each do |doc|
        unless has_preview?(doc)
          missing << {
            'path' => doc.relative_path,
            'title' => doc.data['title'] || File.basename(doc.relative_path),
            'collection' => 'posts'
          }
        end
      end
      
      missing.uniq { |m| m['path'] }
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
        !preview.nil? && !preview.to_s.strip.empty?
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
        
        # Get config from context if available
        site_config = @context.registers[:site].config['preview_images'] || {}
        output_dir = site_config['output_dir'] || 'assets/images/previews'
        
        return preview if preview.start_with?('/') || preview.start_with?('http')
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
      site.data['preview_images_missing'] = PreviewImageGenerator.missing_previews(site)
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
