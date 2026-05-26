# frozen_string_literal: true

require 'digest'

#
# File: obsidian_links.rb
# Path: _plugins/obsidian_links.rb
# Purpose: Convert Obsidian-flavoured Markdown to GitHub-Pages-compatible HTML
#          at build time (server-side path).
#
# ⚠️  IMPORTANT — Plugin loading on GitHub Pages
#
#   The default repository build uses the `github-pages` gem, which forces
#   `safe: true` and overrides `plugins_dir` to a random hash. That means
#   THIS PLUGIN DOES NOT RUN on the default GH Pages remote_theme build.
#
#   For those deployments, the equivalent transformations happen in the
#   browser via assets/js/obsidian-wiki-links.js using
#   assets/data/wiki-index.json. That is the primary, supported path.
#
#   This Ruby plugin is kept as an opt-in for forks that:
#     - Build their site with vanilla Jekyll (no `github-pages` gem), or
#     - Use a custom GitHub Actions workflow (Strategy 1 in the integration
#       plan) that bypasses the GH Pages plugin whitelist.
#
#   In those setups, server-side rewrites give better SEO and avoid the
#   client-side flash before the JS resolver runs.
#
# Toggle: set `obsidian: enabled: false` in _config.yml to disable everything.
#
# Handled syntax (no-op when not present, so plain Markdown is unaffected):
#   - Wiki-links:        [[Page Title]]            → <a class="wiki-link">…</a>
#                        [[Page Title|Alias]]      with custom display text
#                        [[Page Title#Heading]]    anchor preserved
#                        [[Page Title^block-id]]   degrades gracefully (anchor stripped)
#   - Embeds:            ![[image.png]]            → <img …>
#                        ![[image.png|400]]        width hint
#                        ![[Note Title]]           → transcluded note content
#   - Callouts:          > [!note] Title           → Bootstrap alert component
#                        Supported types: note, tip, info, success, warning, danger,
#                        question, quote, abstract, example, bug, todo, important,
#                        caution, failure
#   - Inline tags:       #tag (outside code blocks/links) → linked tag badge
#
# A site-wide title → permalink index is also exposed as `site.obsidian.index`
# for use by Liquid (e.g. assets/data/wiki-index.json) and by the client-side
# fallback resolver in assets/js/obsidian-wiki-links.js (used by the
# remote_theme GitHub Pages build, where this plugin does not run).
#
# Runs as a :pre_render hook on every document and page; transforms only the
# raw markdown body before kramdown converts it.
#
# Toggle: set `obsidian: enabled: false` in _config.yml to disable everything.
#
module Jekyll
  module Obsidian
    DEFAULT_CONFIG = {
      'enabled' => true,
      'attachments_path' => '/assets/images/notes',
      'tag_base_url' => '/tags/',
      'callout_class_prefix' => 'obsidian-callout',
      'wiki_link_class' => 'wiki-link',
      'broken_link_class' => 'wiki-link wiki-link-broken',
      # Slugs (normalised: lowercase, stripped) that are too generic to be
      # useful as wiki-link targets and whose collisions should be silenced.
      # Add entries in _config.yml under `obsidian.skip_slugs`.
      'skip_slugs' => []
    }.freeze

    # Bootstrap alert mapping per Obsidian callout type.
    # https://help.obsidian.md/Editing+and+formatting/Callouts
    CALLOUT_TYPES = {
      'note'      => { alert: 'primary',   icon: 'bi-pencil-square'         },
      'abstract'  => { alert: 'secondary', icon: 'bi-card-text'             },
      'summary'   => { alert: 'secondary', icon: 'bi-card-text'             },
      'tldr'      => { alert: 'secondary', icon: 'bi-card-text'             },
      'info'      => { alert: 'info',      icon: 'bi-info-circle'           },
      'todo'      => { alert: 'info',      icon: 'bi-check2-square'         },
      'tip'       => { alert: 'success',   icon: 'bi-lightbulb'             },
      'hint'      => { alert: 'success',   icon: 'bi-lightbulb'             },
      'important' => { alert: 'warning',   icon: 'bi-exclamation-circle'    },
      'success'   => { alert: 'success',   icon: 'bi-check-circle'          },
      'check'     => { alert: 'success',   icon: 'bi-check-circle'          },
      'done'      => { alert: 'success',   icon: 'bi-check-circle'          },
      'question'  => { alert: 'info',      icon: 'bi-question-circle'       },
      'help'      => { alert: 'info',      icon: 'bi-question-circle'       },
      'faq'       => { alert: 'info',      icon: 'bi-question-circle'       },
      'warning'   => { alert: 'warning',   icon: 'bi-exclamation-triangle'  },
      'caution'   => { alert: 'warning',   icon: 'bi-exclamation-triangle'  },
      'attention' => { alert: 'warning',   icon: 'bi-exclamation-triangle'  },
      'failure'   => { alert: 'danger',    icon: 'bi-x-octagon'             },
      'fail'      => { alert: 'danger',    icon: 'bi-x-octagon'             },
      'missing'   => { alert: 'danger',    icon: 'bi-x-octagon'             },
      'danger'    => { alert: 'danger',    icon: 'bi-shield-exclamation'    },
      'error'     => { alert: 'danger',    icon: 'bi-shield-exclamation'    },
      'bug'       => { alert: 'danger',    icon: 'bi-bug'                   },
      'example'   => { alert: 'secondary', icon: 'bi-code-slash'            },
      'quote'     => { alert: 'secondary', icon: 'bi-chat-quote'            },
      'cite'      => { alert: 'secondary', icon: 'bi-chat-quote'            }
    }.freeze

    # Image extensions that trigger the embed → <img> path.
    IMAGE_EXTENSIONS = %w[.png .jpg .jpeg .gif .svg .webp .avif .bmp].freeze

    # ---------------------------------------------------------------------
    # Index — built once per build, keyed by lowercase title and basename.
    # ---------------------------------------------------------------------
    class Index
      attr_reader :entries

      def initialize(site, config = {})
        @entries = {}
        @skip_slugs = Array(config['skip_slugs'])
                        .map { |s| s.to_s.downcase.strip.gsub(/\s+/, ' ') }
                        .to_set
        build(site)
      end

      def build(site)
        # All renderable docs across collections + standalone HTML pages.
        # Filtering to output_ext == '.html' ensures raw binary docs (e.g.
        # .ipynb notebook files) are not indexed as wiki-link targets.
        items = []
        items.concat(site.documents.select { |d| d.respond_to?(:output_ext) && d.output_ext == '.html' }) if site.respond_to?(:documents)
        items.concat(site.pages.select { |p| p.output_ext == '.html' })

        items.each do |doc|
          title = doc.data['title'].to_s.strip
          basename = File.basename(doc.relative_path, File.extname(doc.relative_path))
          url = doc.url

          register(title, url, doc) unless title.empty?
          register(basename, url, doc) unless basename.empty?

          # Aliases: Obsidian frontmatter `aliases:` — also wired to redirect_from.
          Array(doc.data['aliases']).each do |alias_name|
            register(alias_name.to_s.strip, url, doc)
          end
        end
      end

      def register(key, url, doc)
        slug = normalize(key)
        return if slug.empty?
        return if @skip_slugs.include?(slug)

        # First registration wins; subsequent collisions produce a deterministic
        # warning so authors can disambiguate (e.g. via `aliases:`).
        if @entries.key?(slug) && @entries[slug][:url] != url
          Jekyll.logger.warn(
            'Obsidian:',
            "wiki-link target collision for #{key.inspect} — keeping #{@entries[slug][:url]}, ignoring #{url}"
          )
          return
        end

        @entries[slug] = {
          url: url,
          title: doc.data['title'].to_s.strip,
          collection: (doc.respond_to?(:collection) && doc.collection ? doc.collection.label : nil)
        }
      end

      def lookup(key)
        @entries[normalize(key)]
      end

      def to_h
        @entries.each_with_object({}) do |(slug, info), out|
          out[slug] = { 'url' => info[:url], 'title' => info[:title], 'collection' => info[:collection] }
        end
      end

      private

      def normalize(value)
        value.to_s.downcase.strip.gsub(/\s+/, ' ')
      end
    end

    # ---------------------------------------------------------------------
    # Converter — pure-string transformations on the raw markdown body.
    # ---------------------------------------------------------------------
    class Converter
      # Match fenced code blocks (``` or ~~~), indented code lines, and inline
      # code spans so we can skip them when rewriting wiki-link / tag syntax.
      FENCED_CODE_RE = /(^[ \t]{0,3}(```|~~~)[^\n]*\n.*?^[ \t]{0,3}\2[^\n]*$)/m
      INLINE_CODE_RE = /(`+)[^`\n]*?\1/

      # ![[target]]  or  ![[target|width-or-alias]]
      EMBED_RE = /!\[\[([^\]\n|]+?)(?:\|([^\]\n]+))?\]\]/

      # [[target]]  or  [[target|alias]]   (target may include #heading or ^block)
      LINK_RE  = /\[\[([^\]\n|]+?)(?:\|([^\]\n]+))?\]\]/

      # Inline #tag — letters, digits, slashes, dashes, underscores. Skips
      # leading-position fragments (markdown headings) and anything inside
      # links (handled separately via masking).
      INLINE_TAG_RE = /(?<![\w\/#&])#([A-Za-z][\w\/-]{0,63})/

      # Callout block: > [!type] optional title  followed by zero+ continuation
      # lines starting with `>`. Multiline match is scoped per blockquote group.
      CALLOUT_RE = /^(?<indent>[ \t]{0,3})>\s*\[!(?<type>[A-Za-z]+)\](?<fold>[+-]?)\s*(?<title>[^\n]*)\n(?<body>(?:^[ \t]{0,3}>(?:[^\n]*)\n?)*)/

      def initialize(site, index, config)
        @site = site
        @index = index
        @config = config
      end

      def convert(markdown, current_url: nil)
        return markdown if markdown.nil? || markdown.empty?

        # Mask code spans / fences so syntax inside them is left untouched.
        masked, restorer = mask_code_blocks(markdown)

        masked = transform_callouts(masked)
        masked = transform_embeds(masked)
        masked = transform_wiki_links(masked, current_url: current_url)
        masked = transform_inline_tags(masked)

        restorer.call(masked)
      end

      private

      def mask_code_blocks(text)
        placeholders = []
        masked = text.gsub(FENCED_CODE_RE) do
          placeholders << Regexp.last_match(0)
          "\u0000FENCE#{placeholders.length - 1}\u0000"
        end
        masked = masked.gsub(INLINE_CODE_RE) do
          placeholders << Regexp.last_match(0)
          "\u0000CODE#{placeholders.length - 1}\u0000"
        end

        restorer = ->(t) {
          t.gsub(/\u0000(?:FENCE|CODE)(\d+)\u0000/) { placeholders[Regexp.last_match(1).to_i] }
        }

        [masked, restorer]
      end

      # > [!type] Title  →  Bootstrap alert. Body is dedented (leading "> ").
      def transform_callouts(text)
        text.gsub(CALLOUT_RE) do
          m = Regexp.last_match
          type = m[:type].downcase
          spec = CALLOUT_TYPES[type] || CALLOUT_TYPES['note']
          fold = m[:fold]
          title = m[:title].to_s.strip
          title = type.capitalize if title.empty?
          body = m[:body].to_s.gsub(/^[ \t]{0,3}>[ \t]?/, '').rstrip

          # Allow inner Markdown by emitting a span with `markdown="1"` so
          # kramdown still parses the body content.
          collapsed_attr = fold == '-' ? ' data-collapsed="true"' : ''
          alert_class = "alert alert-#{spec[:alert]} #{@config['callout_class_prefix']} #{@config['callout_class_prefix']}-#{type}"

          <<~HTML

            <div class="#{alert_class}" role="alert"#{collapsed_attr} markdown="0">
              <div class="#{@config['callout_class_prefix']}-title"><i class="bi #{spec[:icon]} me-2" aria-hidden="true"></i>#{escape_html(title)}</div>
              <div class="#{@config['callout_class_prefix']}-body" markdown="1">

            #{body}

            </div>
            </div>

          HTML
        end
      end

      def transform_embeds(text)
        text.gsub(EMBED_RE) do
          target = Regexp.last_match(1).to_s.strip
          modifier = Regexp.last_match(2).to_s.strip
          ext = File.extname(target).downcase

          if IMAGE_EXTENSIONS.include?(ext)
            render_image_embed(target, modifier)
          else
            render_note_embed(target, modifier)
          end
        end
      end

      def render_image_embed(target, modifier)
        width_attr = ''
        alt = target
        if !modifier.empty?
          if modifier =~ /\A\d+\z/
            width_attr = %( width="#{modifier}")
          else
            alt = modifier
          end
        end

        # Resolve absolute paths (/foo/bar.png) verbatim, otherwise prefix the
        # configured attachments path.
        src = if target.start_with?('/')
                target
              else
                "#{@config['attachments_path'].chomp('/')}/#{target}"
              end

        %(<img src="#{src}" alt="#{escape_html(alt)}" loading="lazy" class="obsidian-embed obsidian-embed-image"#{width_attr} />)
      end

      def render_note_embed(target, _modifier)
        clean_target, anchor = split_anchor(target)
        info = @index.lookup(clean_target)
        if info.nil?
          %(<div class="obsidian-embed obsidian-embed-broken alert alert-warning" role="alert">Embed not found: <code>#{escape_html(target)}</code></div>)
        else
          # Use a Liquid include so the embedded note can be rendered with the
          # transclude template (avoids re-running this converter on its body).
          url = info[:url].to_s
          url += "##{anchor}" unless anchor.nil? || anchor.empty?
          %({% include content/transclude.html target="#{escape_attr(clean_target)}" url="#{escape_attr(url)}" %})
        end
      end

      def transform_wiki_links(text, current_url: nil)
        text.gsub(LINK_RE) do
          target = Regexp.last_match(1).to_s.strip
          alias_text = Regexp.last_match(2).to_s.strip
          clean_target, anchor = split_anchor(target)
          display = alias_text.empty? ? (anchor.nil? ? clean_target : "#{clean_target} › #{anchor}") : alias_text

          info = @index.lookup(clean_target)
          if info.nil?
            %(<a href="#" class="#{@config['broken_link_class']}" data-wiki-target="#{escape_attr(clean_target)}" title="Unresolved wiki-link: #{escape_attr(clean_target)}">#{escape_html(display)}</a>)
          else
            url = info[:url].to_s
            url += "##{anchorize(anchor)}" unless anchor.nil? || anchor.empty?
            current_attr = current_url && info[:url] == current_url ? ' aria-current="page"' : ''
            %(<a href="#{url}" class="#{@config['wiki_link_class']}" data-wiki-target="#{escape_attr(clean_target)}"#{current_attr}>#{escape_html(display)}</a>)
          end
        end
      end

      def transform_inline_tags(text)
        text.gsub(INLINE_TAG_RE) do
          tag = Regexp.last_match(1)
          base = @config['tag_base_url'].to_s
          base = "#{base}/" unless base.end_with?('/')
          %(<a href="#{base}##{slugify(tag)}" class="obsidian-tag">##{escape_html(tag)}</a>)
        end
      end

      # Split "[[Page#Heading]]" or "[[Page^block-id]]" into [page, anchor].
      # Block refs (^id) are degraded to a heading-style anchor.
      def split_anchor(target)
        if target =~ /\A(.+?)\^([\w-]+)\z/
          [Regexp.last_match(1).strip, Regexp.last_match(2).strip]
        elsif target =~ /\A(.+?)#(.+)\z/
          [Regexp.last_match(1).strip, Regexp.last_match(2).strip]
        else
          [target, nil]
        end
      end

      def anchorize(anchor)
        return '' if anchor.nil?

        anchor.downcase.strip.gsub(/[^\w\s-]/, '').gsub(/\s+/, '-')
      end

      def slugify(value)
        value.downcase.gsub(/[^\w\/-]+/, '-').gsub(/-+/, '-').gsub(%r{/}, '-')
      end

      def escape_html(value)
        value.to_s
             .gsub('&', '&amp;')
             .gsub('<', '&lt;')
             .gsub('>', '&gt;')
             .gsub('"', '&quot;')
      end

      def escape_attr(value)
        escape_html(value).gsub("'", '&#39;')
      end
    end

    # ---------------------------------------------------------------------
    # Hook registration — runs once per build, then once per document.
    # ---------------------------------------------------------------------
    class << self
      attr_accessor :index, :config

      def site_config(site)
        DEFAULT_CONFIG.merge(site.config['obsidian'] || {})
      end

      def install_hooks
        Jekyll::Hooks.register :site, :pre_render do |site|
          self.config = site_config(site)
          if config['enabled']
            self.index = build_or_reuse_index(site)
            site.config['obsidian'] = config.merge('index' => index.to_h)
            Jekyll.logger.info('Obsidian:', "indexed #{index.entries.size} wiki-link targets")
          else
            Jekyll.logger.info('Obsidian:', 'integration disabled via _config.yml (obsidian.enabled = false)')
          end
        end

        Jekyll::Hooks.register :documents, :pre_render do |doc|
          rewrite_document(doc) if obsidian_enabled?(doc)
        end

        Jekyll::Hooks.register :pages, :pre_render do |page|
          rewrite_document(page) if obsidian_enabled?(page) && markdown?(page)
        end
      end

      def obsidian_enabled?(doc)
        config && config['enabled'] && doc.respond_to?(:content) && doc.content.is_a?(String)
      end

      def markdown?(doc)
        ext = File.extname(doc.relative_path).downcase
        %w[.md .markdown].include?(ext)
      end

      def rewrite_document(doc)
        return unless index
        return unless needs_rewrite?(doc.content)

        converter = Converter.new(nil, index, config)
        doc.content = converter.convert(doc.content, current_url: doc.url)
      end

      def needs_rewrite?(content)
        content.include?('[[') || content.include?('> [!') || content.match?(Converter::INLINE_TAG_RE)
      end

      private

      # Reuse the cached index when the document set is unchanged (URLs, titles,
      # and aliases all match). Common during incremental rebuilds where only
      # page body content is modified.
      def build_or_reuse_index(site)
        # Cheap early-exit: if Jekyll hands us the same Site object as the
        # previous :pre_render call, the document set cannot have changed and
        # we can skip the O(n) fingerprint walk entirely. Matters on 500+ doc
        # sites where compute_url_fingerprint shows up in --profile output.
        if @cached_site_id == site.object_id && @cached_index
          return @cached_index
        end

        current_fingerprint = compute_url_fingerprint(site)
        if @cached_fingerprint && @cached_fingerprint == current_fingerprint && @cached_index
          Jekyll.logger.debug('Obsidian:', 'reusing cached wiki-link index (URLs, titles, and aliases unchanged)')
          @cached_site_id = site.object_id
          return @cached_index
        end

        new_index = Index.new(site, self.config)
        @cached_fingerprint = current_fingerprint
        @cached_site_id = site.object_id
        @cached_index = new_index
        new_index
      end

      # Fingerprint covering URLs, titles, and aliases so the cache is
      # invalidated whenever any of those change (not only page additions/removals).
      def compute_url_fingerprint(site)
        items = []
        items.concat(site.documents) if site.respond_to?(:documents)
        items.concat(site.pages.select { |p| p.output_ext == '.html' })
        sig = items.map { |d|
          aliases = Array(d.data['aliases']).sort.join(',')
          "#{d.url}|#{d.data['title']}|#{aliases}"
        }.sort.join("\n")
        Digest::MD5.hexdigest(sig)
      end
    end
  end
end

Jekyll::Obsidian.install_hooks
