---
title: Jekyll and Travis
author: null
excerpt: Deploying Jekyll using Travis CI and Github
description: null
snippet: null
categories:
  - posts
  - guides
tags:
  - article
  - jekyll
  - travis ci
lastmod: '2022-01-13T17:30:34.958Z'
draft: false
slug: jekyll-and-travis
---

# Overview
 
Jekyll compiles your website into a `_site` available for FTP to your web server. This can be automated if your source code is already on GitHub.

Travis CI is a free Continuous Integration service for testing and deploying your open source GitHub projects.
A config file `.travis.yml` stored in the root directory of your project will instruct Travis CI when you push your code or merge a pull request on GitHub. Travis CI can then build your Jekyll site in a VM and deploys your code as per the settings in the config.

## Create a Travis CI config file

Create a new file in the root of your Jekyll project and name it `.travis.yml`.  The contents of this file will tell Travis CI how to build and deploy your site.

Since this is a ‘Dotfile’, it may be hidden in Finder or file explorer, but should appear in your text editor.
{: .alert .alert-primary }

This is the contents of my file:

```yaml
language: ruby
rvm:
  - 2.3.1

install:
  - bundle install
  - gem install jekyll
  - gem install jekyll-sitemap

branches:
  only:
    - master

env:
  global:
    - JEKYLL_ENV=production

notifications:
  email:
    recipients:
      - <youremail>@<domain>.<sub-domain>
    on_success: always
    on_failure: always

script:
  - chmod +x _scripts/build.sh
  - _scripts/build.sh

after_success:
  - chmod +x _scripts/deploy.sh
  - _scripts/deploy.sh

sudo: false
addons:
  apt:
    packages:
      - ncftp

```

NOTE: You need to udate `<youremail>@<domain>.<sub-domain>` with your email address.
{: .alert .alert-primary }

### Define the build environment and dependencies

```yaml
language: ruby
rvm: - 2.3.1
install:
 - bundle install
 - gem install jekyll
 - gem install jekyll-sitemap
 - gem install emoji_for_jekyll
branches:
  only:
    - master
env:
  global:
    - JEKYLL_ENV=production
```

This section tells Travis CI that the build requires Ruby and sets the version to 2.3.1. It also lists any Gem dependencies. ‘jekyll-sitemap’ and ‘emoji_for_jekyll’ are specific to my project.
The branches section allows you to control which branch in your repository you want to build. In my case I am just building the master branch but this section can be used to set up a staging environment too.
Setting JEKYLL_ENV to production means we can test for this environment variable while doing local testing to ignore things like Google Analytics.

## Building and Deploying the site

```yaml
script:
  - chmod +x _scripts/build.sh
  - _scripts/build.sh

after_success:
  - chmod +x _scripts/deploy.sh
  - _scripts/deploy.sh

sudo: false
addons:
  apt:
    packages:
      - ncftp
```

This section is telling Travis CI to find and execute the file located at _scripts/build.sh and on success execute the file at _scripts/deploy.sh.
The addons section tells Travis CI to also install an FTP client called ncftp. This will be used to deploy your site.

## Create a folder in the root called _scripts and inside create a build and deploy shell script.

**build.sh**

```bash
#!/bin/bash

bundle exec jekyll build --config _config.yml
```

The build script is essentially the same as the command you run in Terminal while building your site locally with the addition of defining the _config.yml file as the site’s configuration file.

**deploy.sh**

```bash
#!/bin/bash

if  [[ $TRAVIS_PULL_REQUEST = "false" ]]
then
    ncftp -u "$USERNAME" -p "$PASSWORD" "$HOST"<<EOF
    rm -rf site/wwwroot
    mkdir site/wwwroot
    quit
EOF

    cd _site || exit
    ncftpput -R -v -u "$USERNAME" -p "$PASSWORD" "$HOST" /site/wwwroot .
fi
```

The deploy script performs 3 main tasks:

* Logs into your FTP account using the $USERNAME, $PASSWORD and $HOST variables which you set in Travis CI settings.
* Deletes the site/wwwroot directory and recreates an empty one
* Copies the contents of the _site folder to /site/wwwroot

## Setting up Travis CI

For the deploy script to work you need to configure the environment variables for your GitHub repository in Travis CI.

1. Go your your Travis profile
2. Find your Jekyll repository, switch Travis CI on and click the gear icon
3. Set the Environment Variables for your FTP host.

## Environment Variables settings

Note: Build logs for open source projects are publicly visible so remember to keep the ‘Display value in build log’ option off.
{: .alert .alert-primary }

## Automate all the things

Now that everything is set up and configured, its simply a case of pushing your code to your GitHub master branch. Travis CI will watch your repository for changes and automatically trigger a build. If, and only when, the build is successful, Travis CI will deploy your site to your FTP host.

With a Pull Request workflow, Travis CI will run a build on the PR and only when it is successful will it allow the branch to be merged into master.
The notifications section in .travis.yml file can be used to manage who receives build status email notifications.

```yaml
notifications:
  email:
    recipients:
      - <youremail>@<domain>.<sub-domain>
    on_success: always
    on_failure: always
```

## Final thoughts

Deploying your Jekyll website using Travis CI is simple, fast and secure. The Pull Request workflow is perfect for collaborating on open source projects or simply scheduling your own content by merging branches when you’re ready.

All of the build process is handled by Travis CI which means you can commit changes to your repository from anywhere, have your code tested and validated and then merge to push your content live. Travis CI will also notify you when the build is successful or fails.

## References:

