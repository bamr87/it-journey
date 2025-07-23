#!/bin/bash

# Create a new Gemfile
touch Gemfile

# Write the non-commented lines to the Gemfile
echo 'source "https://rubygems.org"' >> Gemfile
echo "gem 'github-pages' , '231'" >> Gemfile
echo "gem 'jekyll' , '3.9.5'" >> Gemfile
echo "group :jekyll_plugins do" >> Gemfile
echo "  gem 'jekyll-feed', \"~> 0.17\"" >> Gemfile
echo "  gem 'jekyll-sitemap' , \"~> 1.4.0\"" >> Gemfile
echo "  gem 'jekyll-seo-tag', \"~> 2.8.0\"" >> Gemfile
echo "  gem 'jekyll-paginate', '~> 1.1'" >> Gemfile
echo "end" >> Gemfile