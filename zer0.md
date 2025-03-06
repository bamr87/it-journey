---
title: zer0
sub-title: 2 her0
description: Seed page with scripts, commands, instructions to build the most epic statically generated website in the universe.
version: 0.0.9
tags:
  - jekyll
  - bootstrap5
  - javascript
  - docker
categories:
  - bootstrap
  - quickstart
created: 2024-02-10T23:51:11.480Z
lastmod: 2024-05-27T04:50:51.594Z
draft: draft
layout: journals
sidebar:
  nav: dynamic
permalink: /zer0/
slug: zer0
keywords:
  - jekyll
  - bootstrap5
  - javascript
  - docker
  - zer0
date: 2024-05-27T04:49:32.883Z
snippet: What is a snippet?
comments: true
---

testing pr workflow again again, Damn it. I think i figured it out.

[![pages-build-deployment](https://github.com/bamr87/it-journey/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/bamr87/it-journey/actions/workflows/pages/pages-build-deployment)

[![Gem Version](https://badge.fury.io/rb/jekyll-theme-zer0.svg)](https://badge.fury.io/rb/jekyll-theme-zer0)

This is the seed of the project with all the commands, scripts, and instructions that build this application from the ground up.
In theory, this should be the only file you need to build the project from scratch.
However, in practice, you may need to install additional dependencies or configure the environment to match the target system. 
For example, you may need to install Ruby, Node.js, or other tools to run the application locally or deploy it to a server.
Therefore, part of this document is to provide a list of prerequisites and setup instructions to help you get started with the project.

## System Specs

For my development machine, I use the following specs:

- Model Name: MacBook Pro
- Model Identifier: Mac15,6
- Model Number: MRX33LL/A
- Chip: Apple M3 Pro
- System Firmware Version: 10151.101.3
- System Version: macOS 14.4.1 (23E224)
- Kernel Version: Darwin 23.4.0

Inspect the page to see the hidden code to populate your system specs for a MacBook pro. Press (cmd + shift + c) in the browser.

```shell
# Get specific hardware and software information for Macs

system_profiler SPHardwareDataType | awk '/Model Name:|Model Identifier:|Model Number:|Chip:|System Firmware Version:/ {print $0}'
system_profiler SPSoftwareDataType | awk '/System Version:|Kernel Version:/ {print $0}'

```
{: .d-none }

## Prerequisites

Before we begin, make sure you have the following software installed on your machine:

- [VS code](https://code.visualstudio.com/) installed on your machine (if you're smart)
- [docker](https://docs.docker.com/get-docker/) installed on your machine (if you're a pro)
- [homebrew](https://brew.sh/) installed on your machine (if you're a cli junkie)
- [git](https://git-scm.com/) installed on your machine (if you want to track the truth)
- [gh cli](https://cli.github.com/) installed on your machine (if you want to publish the truth)

For step-by-step instructions on how to install these tools, visit the "Quickstart" section of the site here: [Quickstart](/quickstart)

To use these tools effectively, you need:

- A GitHub account and a repository where you want to maintain and publish your site.
- A personal access token from GitHub to authenticate with the GitHub API.
- A cup of coffee or your favorite beverage to keep you energized.
- A positive attitude and a sense of curiosity.
- A sense of adventure and a willingness to explore new tools and technologies.
- A growth mindset and a willingness to embrace challenges and learn from mistakes.
- A sense of humor and the ability to laugh at unexpected errors and bugs.
- A supportive community or network of friends and colleagues to ask for help and share your progress.
- A clear goal and motivation to build this project and share your knowledge with the world.
- A spirit of creativity and a desire to express yourself through code and technology.

More importantly, you need to:

- Embrace responsibility and ethical, inclusive software development.
- Cultivate empathy and create tools that benefit others.
- Appreciate opportunities and resources for learning and growth.
- Foster curiosity about AI and machine learning.
- Pursue a purpose that enhances productivity and creativity.
- Persevere through challenges with determination.
- Learn from others and share knowledge with humility.
- Believe in technology's potential to improve lives and create positive change.
- Make the learning process fun and engaging.
- Balance work with breaks for well-being.
- Celebrate achievements and share your work with the world.
- Anticipate making a difference in the developer community.
- Find satisfaction and fulfillment in creating value for others.
- Connect with the global community of developers and creators.
- Believe in your ability to create something meaningful and impactful.
- Stand in awe of technology's power to transform ideas into reality.

## Confirm Prerequisites

Make sure you have the following installed on your machine:

```shell
# Check if git is installed
if ! git --version > /dev/null 2>&1; then
  echo "git is not installed. Installing..."
  brew install git
else
  echo "git is already installed."
fi

# Check if gh is installed
if ! gh --version > /dev/null 2>&1; then
  echo "gh is not installed. Installing..."
  brew install gh
else
  echo "gh is already installed."
fi

# Check if gh is authenticated
if ! gh auth status > /dev/null 2>&1; then
  echo "gh is not authenticated. Please authenticate..."
  gh auth login
else
  echo "gh is already authenticated."
fi

# Check if Docker is installed
if ! docker --version > /dev/null 2>&1; then
  echo "Docker is not installed. Installing..."
  brew install --cask docker
else
  echo "Docker is already installed."
fi

# Check if Visual Studio Code is installed
if ! code --version > /dev/null 2>&1; then
  echo "Visual Studio Code is not installed. Installing..."
  brew install --cask visual-studio-code
else
  echo "Visual Studio Code is already installed."
fi
```

The script checks if certain tools (git, gh, docker, and Visual Studio Code) are installed and if gh is authenticated on a macOS system using Homebrew. 

For each tool, it runs a version check command and redirects the output to null. If the tool is not installed, it installs it using Homebrew. If the tool is already installed, it prints a message indicating that. For gh, it also checks if it is authenticated and prompts the user to authenticate if it is not.


## Environment

This section of the document is about setting up environment variables for a project. It provides two methods to set these variables:

Manual Entry:

Prompts the user to enter their GitHub username and repository name in the terminal.
These values are then stored as environment variables.
Automatic Setup:

Sets default values for the environment variables, including the GitHub home directory, the GitHub username (retrieved using the GitHub CLI), the repository name, and the full path to the repository.
Finally, it confirms the environment variables by printing them to the terminal and logging them to a file named env-variables.log.

### Enter Variables

{% if site.level == 'her0' %}
  {% include zer0-env-var.html %}
{% endif %}

### Or use default

```shell
# Or enter them in the terminal

echo "Please enter your GitHub username:"
read GHUSER
export GHUSER

echo "Please enter your Git repository name:"
read GIT_REPO
export GIT_REPO
```

```shell
export GITHOME=~/github
export GHUSER=$(gh api user --jq '.login')
export GIT_REPO=zer0-mistakes
export ZREPO=$GITHOME/$GIT_REPO
```

```shell
# Confirm the environment variables by echoing them and logging them to a file

echo "$(date) - Log started" > env-variables.log
echo -e "GITHOME: $GITHOME\nGHUSER: $GHUSER\nGIT_REPO: $GIT_REPO\nZREPO: $ZREPO" >> env-variables.log
```

### Set Git email and username

```shell
# Set your Git email and name to tag your commits
# If the GIT_ID is set, use it to tag your commits. "https://github.com/settings/emails"

git config --global user.name "$GHUSER"
git config --global user.email "$GHUSER@users.noreply.github.com"
if [ -n "$GIT_ID" ]; then
  git config --global user.email "$GIT_ID+$GHUSER@users.noreply.github.com"
fi
```

```shell
# confirm your email

git config -l | tee -a env-variables.log
```

## Initialize github

[gh cli docs](https://cli.github.com/manual/)

```shell
# Create your github home directory and repo

mkdir -p $ZREPO
```

```shell
# Initialize your github repository

gh repo create $GIT_REPO --gitignore Jekyll -l mit --public
```

```shell
# If new repo, initialize it

cd $ZREPO
git init
git remote add origin https://github.com/${GHUSER}/${GIT_REPO}.git
git pull origin main

```

```shell
# Create a README.md file based on the zer0.md file from this repo
curl https://raw.githubusercontent.com/bamr87/it-journey/master/zer0.md > README.md
git add README.md
git commit -m "Init $GIT_REPO"
git branch -M main
git push -u origin main
```

### Checkpoint - Github Repo

Go to your new github repository.

```shell
# Open your new github repository in the browser

open https://github.com/${GHUSER}/${GIT_REPO}

```

<a id="repo-link"></a>

![Checkpoint 1](/assets/images/zer0-checkpoint-1.png)

## Initialize Jekyll

### Create Gemfile

```shell
# Create a new Gemfile
cd $ZREPO
touch Gemfile

# Write the non-commented lines to the Gemfile
echo 'source "https://rubygems.org"' >> Gemfile
echo "gem 'github-pages'" >> Gemfile
echo "gem 'jekyll-theme-zer0'" >> Gemfile
echo "group :jekyll_plugins do" >> Gemfile
echo "  gem 'jekyll-remote-theme', \"~> 0.4.3\"" >> Gemfile
echo "  gem 'jekyll-feed', \"~> 0.17\"" >> Gemfile
echo "  gem 'jekyll-sitemap' , \"~> 1.4.0\"" >> Gemfile
echo "  gem 'jekyll-seo-tag', \"~> 2.8.0\"" >> Gemfile
echo "  gem 'jekyll-paginate', \"~> 1.1\"" >> Gemfile
echo "end" >> Gemfile
```

### Download Config file

```shell
# Download the _config.yml file from the jekyll-theme-zer0 repo

curl https://raw.githubusercontent.com/bamr87/zer0-mistakes/main/_config.yml > _config.yml
```

### Create Dockerfile

```shell
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
echo 'CMD ["bundle", "exec", "jekyll", "serve", "--verbose", "--host", "0.0.0.0"]' >> Dockerfile
```

```shell
# build the docker image based on the Dockerfile
docker build -t ${GIT_REPO} .
```

```shell
# Run the container in detached mode
docker run -d -p 4000:4000 -v ${ZREPO}:/app --name ${GIT_REPO}-container ${GIT_REPO}

# Start the container and run the CMD line from the Dockerfile
docker start ${GIT_REPO}-container

```

## Checkpoint - Jekyll

```shell
open http://localhost:4000/${GIT_REPO}
```

## Python Script

```python
import os

def convert_md_to_files(md_file_path):
    language_files = {}
    language_mode = None
    language_extensions = {'python': '.py', 'shell': '.sh'}
    shebang_lines = {'python': '#!/usr/bin/env python3\n', 'shell': '#!/bin/bash\n'}

    output_folder = "script"
    os.makedirs(output_folder, exist_ok=True)

    with open(md_file_path, 'r') as md_file:
        for line in md_file:
            if line.startswith('```'):
                if language_mode:
                    # End of a language block, switch back to markdown mode
                    language_mode = None
                else:
                    # Start of a language block, open a new file for this language if not already open
                    language = line.strip('`\n')
                    if language in language_extensions:
                        language_mode = language
                        if language not in language_files:
                            output_file_path = os.path.join(output_folder, os.path.basename(md_file_path).replace('.md', language_extensions[language]))
                            language_file = open(output_file_path, 'w')
                            if language in shebang_lines:
                                language_file.write(shebang_lines[language])
                            language_files[language] = language_file
                continue

            if language_mode:
                language_files[language_mode].write(line)

    # Close all open language files
    for language_file in language_files.values():
        language_file.close()

convert_md_to_files('zer0.md')
```

## Config file

```yaml
{% include_relative _config.yml %}
```

## Scripts

```liquid
{% include_relative script/zer0.sh %}
```
