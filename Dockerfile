# Use an official Ruby runtime as a parent image
FROM ruby:2.7.4
# escape=\

# FROM starefossen/ruby-node:2-6-alpine

# Set environment variables
ENV GITHUB_GEM_VERSION 231
ENV JSON_GEM_VERSION 1.8.6

# Install Node.js
# RUN apt-get update -qq && apt-get install -y nodejs

# Install specific versions of Jekyll and Bundler that are compatible with Ruby 2.7
# RUN gem install jekyll -v 3.9.0 && gem install bundler -v 1.17.3

RUN gem install nokogiri -v 1.15.5
RUN gem install faraday-net_http -v 3.0.2
RUN gem install faraday -v 2.8.1
RUN gem install github-pages

# RUN apk --update add --virtual build_deps \
#     build-base ruby-dev libc-dev linux-headers \
#   && gem install --verbose --no-document \
#     json:${JSON_GEM_VERSION} \
#     github-pages:${GITHUB_GEM_VERSION} \
#     jekyll-github-metadata \
#     minitest \
#   && apk del build_deps 
#   && apk add git \
#   && mkdir -p /usr/src/app \
#   && rm -rf /usr/lib/ruby/gems/*/cache/*.gem

# Set the working directory in the container to /app
WORKDIR /app
# WORKDIR /usr/src/app

# Add the current directory contents into the container at /app 
ADD . /app

# Install any needed packages specified in Gemfile
RUN bundle install

# Make port 4002 available to the world outside this container
EXPOSE 4002
# EXPOSE 4000 80


# Run Jekyll when the container launches
CMD ["jekyll", "serve", "--host", "0.0.0.0"]
# CMD jekyll serve -d /_site --watch --force_polling -H 0.0.0.0 -P 4000
