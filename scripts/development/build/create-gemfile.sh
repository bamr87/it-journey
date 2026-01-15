#!/bin/bash
#
# @file scripts/development/build/create-gemfile.sh
# @description Create a new Gemfile for Jekyll projects
# @author IT-Journey Team
# @created 2025-01-01
# @version 1.0.0
#
# Usage: ./scripts/development/build/create-gemfile.sh [OUTPUT_FILE]
#
# Creates a new Gemfile with standard Jekyll dependencies.

set -euo pipefail

OUTPUT_FILE="${1:-Gemfile}"

# Check if file already exists
if [[ -f "$OUTPUT_FILE" ]]; then
    echo "Error: $OUTPUT_FILE already exists. Remove it first or specify a different output file." >&2
    exit 1
fi

# Create a new Gemfile
cat > "$OUTPUT_FILE" << 'EOF'
source "https://rubygems.org"

gem 'github-pages', '231'
gem 'jekyll', '3.9.5'

group :jekyll_plugins do
  gem 'jekyll-feed', '~> 0.17'
  gem 'jekyll-sitemap', '~> 1.4.0'
  gem 'jekyll-seo-tag', '~> 2.8.0'
  gem 'jekyll-paginate', '~> 1.1'
end
EOF

echo "Created Gemfile: $OUTPUT_FILE"