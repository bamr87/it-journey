#!/bin/bash
# Get specific hardware and software information for Macs

system_profiler SPHardwareDataType | awk '/Model Name:|Model Identifier:|Model Number:|Chip:|System Firmware Version:/ {print $0}'
system_profiler SPSoftwareDataType | awk '/System Version:|Kernel Version:/ {print $0}'

# install and update prerequisites

brew install git
brew install gh
brew install --cask docker
brew install --cask visual-studio-code
# Or enter them in the terminal

echo "Please enter your GitHub username:"
read GHUSER
export GHUSER

echo "Please enter your Git repository name:"
read GIT_REPO
export GIT_REPO
export GITHOME=~/github
export ZREPO=$GITHOME/$GIT_REPO
# Confirm the environment variables by echoing them and logging them to a file

echo "$(date) - Log started" > env-variables.log
echo -e "GITHOME: $GITHOME\nGHUSER: $GHUSER\nGIT_REPO: $GIT_REPO\nZREPO: $ZREPO" >> env-variables.log
# Set your Git email and name to tag your commits
# If the GIT_ID is set, use it to tag your commits. "https://github.com/settings/emails"

git config --global user.name "$GHUSER"
git config --global user.email "$GHUSER@users.noreply.github.com"
if [ -n "$GIT_ID" ]; then
  git config --global user.email "$GIT_ID+$GHUSER@users.noreply.github.com"
fi
# confirm your email

git config -l | tee -a env-variables.log
# Create your github home directory and repo

mkdir -p $ZREPO
# Initialize your github repository

gh repo create $GIT_REPO --gitignore Jekyll -l mit --public
# If new repo, initialize it

cd $ZREPO
git init
git remote add origin https://github.com/${GHUSER}/${GIT_REPO}.git
git pull origin main

# Create a README.md file based on the zer0.md file from this repo
curl https://raw.githubusercontent.com/bamr87/it-journey/master/zer0.md > README.md
git add README.md
git commit -m "Init $GIT_REPO"
git branch -M main
git push -u origin main
# Open your new github repository in the browser

open https://github.com/${GHUSER}/${GIT_REPO}

# Create a new Gemfile
cd $ZREPO
touch Gemfile

# Write the non-commented lines to the Gemfile
echo 'source "https://rubygems.org"' >> Gemfile
echo "gem 'github-pages' , '231'" >> Gemfile
echo "gem 'jekyll' , '3.9.5'" >> Gemfile
echo "gem 'jekyll-theme-zer0'" >> Gemfile
echo "group :jekyll_plugins do" >> Gemfile
echo "  gem 'jekyll-feed', \"~> 0.17\"" >> Gemfile
echo "  gem 'jekyll-sitemap' , \"~> 1.4.0\"" >> Gemfile
echo "  gem 'jekyll-seo-tag', \"~> 2.8.0\"" >> Gemfile
echo "  gem 'jekyll-paginate', \"~> 1.1\"" >> Gemfile
echo "end" >> Gemfile
# Download the _config.yml file from the jekyll-theme-zer0 repo

curl https://raw.githubusercontent.com/bamr87/zer0-mistakes/main/_config.yml > _config.yml
# Create a new Dockerfile
cd $ZREPO
touch Dockerfile

# Write the content to the Dockerfile
echo "# Use an official Ruby runtime as a parent image" >> Dockerfile
echo "FROM ruby:2.7.4" >> Dockerfile
echo "# escape=\\" >> Dockerfile
echo "ENV GITHUB_GEM_VERSION 231" >> Dockerfile
echo "ENV JSON_GEM_VERSION 1.8.6" >> Dockerfile
echo "ENV GIT_REPO ${GIT_REPO}" >> Dockerfile
echo "WORKDIR /app" >> Dockerfile
echo "ADD . /app" >> Dockerfile
echo "RUN gem update --system 3.3.22" >> Dockerfile
echo "RUN bundle update" >> Dockerfile
echo "RUN bundle install" >> Dockerfile
echo "RUN bundle clean --force" >> Dockerfile
echo "EXPOSE 4000" >> Dockerfile
echo 'CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]' >> Dockerfile
# build the docker image based on the Dockerfile
docker build -t ${GIT_REPO} .
# Run the container in detached mode
docker run -d -p 4000:4000 -v ${ZREPO}:/app --name zer0_container ${GIT_REPO}

# Start the container and run the CMD line from the Dockerfile
docker start zer0_container

open http://localhost:4000/
