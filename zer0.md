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
---

This is the seed of the project with all the commands, scripts, and instructions that build this application from the ground up.
In theory, this should be the only file you need to build the project from scratch.
However, in practice, you may need to install additional dependencies or configure the environment to match the target system. 
For example, you may need to install Ruby, Node.js, or other tools to run the application locally or deploy it to a server.
Therefore, part of this document is to provide a list of prerequisites and setup instructions to help you get started with the project.

## {{ page.title }} Version {{ page.version }}

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
# install and update prerequisites

brew install git
brew install gh
brew install --cask docker
brew install --cask visual-studio-code
```

## Environment

### Set your own environment variables

{% if site.level == 'her0' %}
  {% include zer0-env-var.html %}
{% endif %}

### Set the default environment variables

```shell
# Or use the following to set the environment variables

export GITHOME=~/github
export GHUSER=bamr87
export GIT_REPO=zer0-mistakes
export ZREPO=$GITHOME/$GIT_REPO
```

### Add the environment variables to your shell profile (optional)

```shell
#open Code to edit your shell profile and copy the environment variables

code ~/.zprofile
```

```shell
# Confirm the environment variables by echoing them

echo $GITHOME # /Users/bamr87/github
echo $GHUSER # bamr87
echo $GIT_REPO # zer0-mistakes
echo $ZREPO # /Users/bamr87/github/zer0-mistakes
```

### Set your Git email and name

```shell
# Set your Git email and name to tag your commits

git config --global user.email "$GHUSER@users.noreply.github.com"
git config --global user.name "$GHUSER"
```

### Set your GitHub email using ID (optional)

See [here](https://github.com/settings/emails) for details.

```shell
# If you didnt already set it in the previous step
# FIXME: quotes in comments dont work

echo "What is your Github ID?"
read GIT_ID
```

```shell
# Set your email using ID

git config --global user.email "$GIT_ID+$GHUSER@users.noreply.github.com"
```

```shell
# confirm your email

git config -l
```

## Initialize your new github repository

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
git init -b main
git remote add origin https://github.com/${GHUSER}/${GIT_REPO}.git
git pull origin main
curl https://raw.githubusercontent.com/bamr87/it-journey/master/zer0.md > README.md
git add README.md
git commit -m "Init zer0-mistakes"
git branch -M main
git push -u origin main
```

### Checkpoint - Github Repo Initialized

Go to your new github repository.

```shell
# Open your new github repository in the browser

open https://github.com/${GHUSER}/${GIT_REPO}

```

<a id="repo-link"></a>

![Checkpoint 1](/assets/images/zer0-checkpoint-1.png)

## Clone Github Repo - Optional

```shell
# Remove and Clone the new github repository if needed. Mostly a checkpoint test.
rm -rf $ZREPO
gh repo clone $GHUSER/$GIT_REPO $ZREPO

```

## Deploy Jekyll

### Create Gemfile

```shell
# Create a new Gemfile
cd $ZREPO
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
```

## Create Docker Image and container

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
echo 'CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]' >> Dockerfile
```

```shell
# build the docker image based on the Dockerfile
docker build -t ${GIT_REPO} .
```

```shell
# Run the container in detached mode
docker run -d -p 4000:4000 -v ${ZREPO}:/app --name zer0_container ${GIT_REPO}

# Start the container and run the CMD line from the Dockerfile
docker start zer0_container

# Attach to the running container
docker exec -it zer0_container /bin/bash
```

## Checkpoint - Jekyll Initialized

```shell
open http://localhost:4000/zer0/
```

![](/assets/images/zer0-checkpoint-2.png)

## Configure Jekyll

```shell
# Download the default it-journey configuration file
curl https://raw.githubusercontent.com/bamr87/it-journey/master/_config.yml > $ZREPO/_config.yml
```

```yaml
{% include_relative _config.yml %}
```

```shell
code _config.yml
```

```yaml
title: zer0-mistakes
email: bamr87@zer0-mistakes.com
description: >- # this means to ignore newlines until "baseurl:"
  Write an awesome description for your new site here. You can edit this
  line in _config.yml. It will appear in your document head meta (for
  Google search results) and in your feed.xml site description.
baseurl: null # the subpath of your site, e.g. /blog
url: null # the base hostname & protocol for your site, e.g. http://example.com
twitter_username: bamr87
github_username:  bamr87
```

<!-- TODO: add favicon instructions for branding -->

```shell
cd $ZREPO
wget https://raw.githubusercontent.com/bamr87/it-journey/master/favicon.ico
```

## Install Jekyll

Install [jekyll](https://jekyllrb.com/docs/installation/)

```shell
docker run jekyll new ./ --force
bundle install
```

## Checkpoint - Jekyll Initialized
![](../assets/images/jekyll-serve-1.png)  

```shell
code _config.yml
```

```yaml
title: zer0-mistakes
email: bamr87@zer0-mistakes.com
description: >- # this means to ignore newlines until "baseurl:"
  Write an awesome description for your new site here. You can edit this
  line in _config.yml. It will appear in your document head meta (for
  Google search results) and in your feed.xml site description.
baseurl: null # the subpath of your site, e.g. /blog
url: null # the base hostname & protocol for your site, e.g. http://example.com
twitter_username: bamr87
github_username:  bamr87
```

<!-- TODO: add favicon instructions for branding -->

```shell
cd $ZREPO
wget https://raw.githubusercontent.com/bamr87/it-journey/master/favicon.ico
```

## Checkpoint 1

```shell

bundle lock --add-platform x86-mingw32 x64-mingw32 x86-mswin32 java
```

### Override default
https://jekyllrb.com/docs/themes/#overriding-theme-defaults

```shell
# find theme path

bundle info --path minima
JEKYLL_THEME=$(bundle info --path minima)
echo $JEKYLL_THEME
cd $JEKYLL_THEME
```

### Copy theme repo

```shell
cp -aR $JEKYLL_THEME/* $ZREPO
```

### Remove Theme plugin

```shell
bundle remove jekyll-theme-minima
```

### Comment out the theme from config and Gemfile

```shell
#_config.yml
# Build settings
# theme: minima
plugins:
  - jekyll-feed
```

```shell
bundle remove minima --install
```

Restart jekyll
```shell
jekyll serve
```

## Building the theme

### Build default page

```shell
{%- raw -%}
cd $ZREPO
mkdir _layout
cd _layout
echo "{{ content }}" >> default.html 
{% endraw %}
``` 


```shell
#tree #alias #zshrc #profile
alias tree="find . -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'"
echo alias tree="find . -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'" >> ~/.zshrc

tree
cd -
```



## Plant the seed

```shell
# Set the date format
d=$(date +%Y-%m-%d)
echo "$d"
```

```shell
# Download the seed page
cd $ZREPO
wget -O $d-zer0.md https://raw.githubusercontent.com/bamr87/it-journey/master/zer0.md 
```

![](../assets/images/header_pages.png)  

## Convert zer0.md to zer0.sh using Python

```python
def convert_md_to_files(md_file_path):
    language_files = {}
    language_mode = None
    language_extensions = {'python': '.py', 'shell': '.sh'}
    shebang_lines = {'python': '#!/usr/bin/env python3\n', 'shell': '#!/bin/bash\n'}

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
                            language_file = open(md_file_path.replace('.md', language_extensions[language]), 'w')
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
