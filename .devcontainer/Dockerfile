FROM mcr.microsoft.com/devcontainers/ruby:3.2

# Set environment variables to match project requirements
ENV GITHUB_GEM_VERSION=231
ENV JSON_GEM_VERSION=1.8.6
ENV JEKYLL_ENV=development

# Install additional system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        # For building native gems
        build-essential \
        # For image processing
        imagemagick \
        # For better file watching in Jekyll
        inotify-tools \
        # For better terminal experience
        zsh \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 (already handled by devcontainer features)
# Install GitHub CLI (already handled by devcontainer features)

# Set up bundle cache directory
RUN mkdir -p /usr/local/bundle && chown vscode:vscode /usr/local/bundle

# Switch to vscode user
USER vscode

# Install latest bundler and Jekyll
RUN gem install bundler jekyll

# Set working directory
WORKDIR /workspace

# Copy Gemfile for dependency installation (will be overridden by mount)
COPY Gemfile* ./

# Install dependencies
RUN bundle install

# Expose Jekyll ports
EXPOSE 4000 4002 35729
