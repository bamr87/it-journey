# Preview Generator Plugin
# This plugin creates a simplified preview directory structure for development
# It mirrors the actual file path structure under /preview/

Jekyll::Hooks.register :site, :post_write do |site|
  puts "Preview Generator: Hook triggered! [Updated]"
  puts "Preview Generator: Jekyll environment = #{Jekyll.env}"
  
  # Only run in development environment
  unless Jekyll.env == 'development'
    puts "Preview Generator: Skipping (not development environment)"
    next
  end
  
  puts "Preview Generator: Starting preview directory generation..."
  
  preview_dir = File.join(site.dest, 'preview')
  puts "Preview Generator: Creating preview directory at #{preview_dir}"
  
  # Create preview directory if it doesn't exist
  FileUtils.mkdir_p(preview_dir) unless Dir.exist?(preview_dir)
  
  total_generated = 0
  
  # SIMPLIFIED APPROACH: Scan ALL markdown files in the pages directory
  pages_source = File.join(site.source, 'pages')
  puts "Preview Generator: Scanning #{pages_source} for all markdown files..."
  
  if Dir.exist?(pages_source)
    Dir.glob("#{pages_source}/**/*.md").each do |file_path|
      puts "Debug: Found markdown file: #{file_path}"
      
      # Get the relative path from the workspace root (this matches FrontMatter pathToken.relPath exactly)
      # pathToken.relPath is relative to the workspace root, so include "pages/" prefix
      relative_path = file_path.sub("#{site.source}/", "")
      puts "Debug: Relative path (FrontMatter format): #{relative_path}"
      
      # Remove the .md extension for the directory structure
      preview_path_base = relative_path.gsub(/\.md$/, '')
      puts "Debug: Preview path base: #{preview_path_base}"
      
      # Create the full preview directory path
      full_preview_dir = File.join(preview_dir, preview_path_base)
      FileUtils.mkdir_p(full_preview_dir)
      puts "Debug: Created directory: #{full_preview_dir}"
      
      # Create index.html in the directory
      index_file = File.join(full_preview_dir, 'index.html')
      
      # Try to find the corresponding Jekyll document for this file
      jekyll_doc = nil
      
      # Check all collections for this file
      site.collections.each do |collection_name, collection|
        collection.docs.each do |doc|
          if doc.path == file_path
            jekyll_doc = doc
            break
          end
        end
        break if jekyll_doc
      end
      
      # Check posts
      unless jekyll_doc
        site.posts.docs.each do |post|
          if post.path == file_path
            jekyll_doc = post
            break
          end
        end
      end
      
      # Check pages
      unless jekyll_doc
        site.pages.each do |page|
          if page.path == file_path
            jekyll_doc = page
            break
          end
        end
      end
      
      # Create the preview content
      if jekyll_doc && jekyll_doc.output
        # Use Jekyll's processed output
        File.write(index_file, jekyll_doc.output)
        puts "Generated preview (Jekyll processed): /preview/#{preview_path_base}/"
      else
        # Create a basic preview with file information
        file_name = File.basename(file_path, '.md')
        preview_content = <<~HTML
          <!DOCTYPE html>
          <html>
          <head>
            <meta charset="utf-8">
            <title>Preview: #{file_name}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
              body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 20px; 
                line-height: 1.6;
              }
              .notice { 
                background: #f0f8ff; 
                padding: 15px; 
                border-left: 4px solid #0066cc; 
                margin: 20px 0; 
                border-radius: 4px;
              }
              .file-info {
                background: #f8f9fa;
                padding: 10px;
                border-radius: 4px;
                font-family: monospace;
                margin: 10px 0;
              }
            </style>
          </head>
          <body>
            <div class="notice">
              <h3>🔧 Preview Notice</h3>
              <p>This file exists but wasn't processed by Jekyll collections.</p>
              <p><strong>Possible solutions:</strong></p>
              <ul>
                <li>Add proper frontmatter with layout specification</li>
                <li>Move to appropriate Jekyll collection directory</li>
                <li>Ensure the file isn't marked as draft</li>
              </ul>
            </div>
            <h1>📄 #{file_name}</h1>
            <div class="file-info">
              <strong>File path:</strong> #{relative_path}<br>
              <strong>Full path:</strong> #{file_path}<br>
              <strong>Preview URL:</strong> /preview/#{preview_path_base}/
            </div>
            <p>This preview was auto-generated to demonstrate the FrontMatter CMS preview functionality.</p>
          </body>
        </html>
        HTML
        
        File.write(index_file, preview_content)
        puts "Generated preview (basic): /preview/#{preview_path_base}/"
      end
      
      total_generated += 1
    end
  end
  
  puts "Preview Generator: Generated #{total_generated} preview files"
  puts "Preview directory generation complete!"
end