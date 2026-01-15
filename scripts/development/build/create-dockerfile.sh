#!/bin/bash
#
# @file scripts/development/build/create-dockerfile.sh
# @description Create a new Dockerfile for Jekyll projects
# @author IT-Journey Team
# @created 2025-01-01
# @version 1.0.0
#
# Usage: ./scripts/development/build/create-dockerfile.sh [OUTPUT_FILE]
#
# Creates a new Dockerfile with standard Jekyll configuration.

set -euo pipefail

OUTPUT_FILE="${1:-Dockerfile}"

# Check if file already exists
if [[ -f "$OUTPUT_FILE" ]]; then
    echo "Error: $OUTPUT_FILE already exists. Remove it first or specify a different output file." >&2
    exit 1
fi

# Create a new Dockerfile
cat > "$OUTPUT_FILE" << 'EOF'
# Use an official Ruby runtime as a parent image
FROM ruby:3.2.3

# Set environment variables
ENV GITHUB_GEM_VERSION=231
ENV JSON_GEM_VERSION=1.8.6

# Set the working directory in the container to /app
WORKDIR /app

# Copy dependency files first for better caching
COPY Gemfile Gemfile.lock* ./

# Install Ruby dependencies
RUN bundle install

# Add the rest of the application
COPY . .

# Make port 4002 available to the world outside this container
EXPOSE 4002

# Run Jekyll when the container launches
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]
EOF

echo "Created Dockerfile: $OUTPUT_FILE"