# Use an official Ruby runtime as a parent image
FROM ruby:2.7.4

# Set environment variables
ENV GITHUB_GEM_VERSION 231
ENV JSON_GEM_VERSION 1.8.6

# Set the working directory in the container to /app
WORKDIR /app
# WORKDIR /usr/src/app

# Add the current directory contents into the container at /app 
ADD . /app

# Install any needed packages specified in Gemfile
RUN gem update --system 3.3.22
RUN bundle update
RUN bundle install

# Clean up 
RUN bundle clean --force

# Make port 4002 available to the world outside this container
EXPOSE 4002
# EXPOSE 4000 80

# Run Jekyll when the container launches
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]
# CMD jekyll serve -d /_site --watch --force_polling -H 0.0.0.0 -P 4000
