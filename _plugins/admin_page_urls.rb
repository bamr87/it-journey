# frozen_string_literal: true

# Populates site.data['admin_page_urls'] once per build with a pipe-delimited
# string of /about/ page URLs (e.g. "|/about/config/|/about/settings/theme/|").
# Templates use a `contains` check against this string instead of re-running
# `site.html_pages | where_exp | map | join` on every page render.
Jekyll::Hooks.register :site, :pre_render do |site|
  admin_urls = site.pages
                   .select { |p| p.output_ext == '.html' && p.url.include?('/about/') }
                   .map(&:url)
                   .sort
                   .join('|')
  admin_urls = "|#{admin_urls}|" unless admin_urls.empty?
  site.data ||= {}
  site.data['admin_page_urls'] = admin_urls
end
