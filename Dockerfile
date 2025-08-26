# Use an official Ruby runtime as a parent image
FROM ruby:3.2.3

# Set environment variables
ENV GITHUB_GEM_VERSION=231
ENV JSON_GEM_VERSION=1.8.6

# Set the working directory in the container to /app
WORKDIR /app

# Copy dependency files first for better caching
COPY Gemfile Gemfile.lock* ./

# Install dependencies
RUN bundle install

# Add the rest of the application
COPY . .

# Clean up 
RUN bundle clean --force

# Make port 4002 available to the world outside this container
EXPOSE 4002

# Run Jekyll when the container launches
CMD ["bundle", "exec", "jekyll", "serve", "--config", "_config.yml,_config_dev.yml", "--host", "0.0.0.0"]

# source .env
# docker build -t ${GIT_REPO} .
# docker run -d -p 4002:4002 -v ${ZREPO}:/app --name ${GIT_REPO}-container ${GIT_REPO}
# docker start ${GIT_REPO}-container
# docker exec -it ${GIT_REPO}-container /bin/bash
