---
title: zer0
sub-title: 2 her0
description: zer0
excerpt: zer0 to her0
version: 0.0.4
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
layout: default
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

Version Test take 5

# {{ page.title }} Version {{ page.version }}

This is the seed of the project with all the commands, scripts, and instructions that build this application from the ground up.
In theory, this should be the only file you need to build the project from scratch.
However, in practice, you may need to install additional dependencies or configure the environment to match the target system. 
For example, you may need to install Ruby, Node.js, or other tools to run the application locally or deploy it to a server.
Therefore, part of this document is to provide a list of prerequisites and setup instructions to help you get started with the project.

For my development machine, I use the following specs:

- Model Name: MacBook Pro
- Model Identifier: Mac15,6
- Model Number: MRX33LL/A
- Chip: Apple M3 Pro
- System Firmware Version: 10151.101.3
- System Version: macOS 14.4.1 (23E224)
- Kernel Version: Darwin 23.4.0

```shell
# Get specific hardware and software information for Macs

system_profiler SPHardwareDataType | awk '/Model Name:|Model Identifier:|Model Number:|Chip:|System Firmware Version:/ {print $0}'
system_profiler SPSoftwareDataType | awk '/System Version:|Kernel Version:/ {print $0}'

```
{: .d-none }

## Prerequisites

Before we begin, make sure you have the following:

- [VS code](https://code.visualstudio.com/) installed on your machine.
- [docker](https://docs.docker.com/get-docker/) installed on your machine.
- [homebrew](https://brew.sh/) installed on your machine.
- [git](https://git-scm.com/) installed on your machine.
- [gh cli](https://cli.github.com/) installed on your machine.
- A GitHub account and a repository where you want to publish the markdown files.
- Basic knowledge of JavaScript and TypeScript.
- Basic knowledge of the VS Code extension API.
- A personal access token from GitHub to authenticate with the GitHub API.
- A text editor or IDE to write and test the extension code.
- A terminal or command line interface to run commands.
- An internet connection to install dependencies and access documentation.
- A desire to automate the process of saving Copilot conversations as markdown files as the building blocks of your documentation.
- A willingness to learn and experiment with VS Code extension development.
- A cup of coffee or your favorite beverage to keep you energized.
- A positive attitude and a sense of curiosity.
- A sense of adventure and a willingness to explore new tools and technologies.
- A growth mindset and a willingness to embrace challenges and learn from mistakes.
- A sense of humor and the ability to laugh at unexpected errors and bugs.
- A supportive community or network of friends and colleagues to ask for help and share your progress.
- A clear goal and motivation to build a useful and practical extension.
- A spirit of creativity and a desire to express yourself through code and technology.
- A sense of responsibility and a commitment to ethical and inclusive software development practices.
- A sense of empathy and a desire to create tools that benefit others and make the world a better place.
- A sense of gratitude and appreciation for the opportunities and resources that enable you to learn and grow.
- A sense of wonder and a curiosity about the possibilities of AI and machine learning in software development.
- A sense of purpose and a vision for how your extension can help developers be more productive and creative.
- A sense of determination and a willingness to persevere through challenges and setbacks.
- A sense of humility and a willingness to learn from others and share your knowledge with the community.
- A sense of optimism and a belief in the potential of technology to improve people's lives and create positive change.
- A sense of fun and a spirit of playfulness to make the learning process enjoyable and engaging.
- A sense of balance and a commitment to taking breaks and caring for your well-being while working on the extension.
- A sense of completion and a desire to celebrate your achievements and share your extension with the world.
- A sense of anticipation and excitement to see how your extension can make a difference in the developer community.
- A sense of satisfaction and fulfillment from creating something that brings joy and value to others.
- A sense of connection and belonging in the global community of developers and creators.
- A sense of possibility and a belief in your ability to create something meaningful and impactful.
- A sense of wonder and awe at the power of technology to transform ideas into reality.
- A sense of responsibility and a commitment to using your skills and talents for good.
- A sense of curiosity and a desire to explore new ideas and possibilities.
- A sense of adventure and a willingness to take risks and try new things.
- A sense of playfulness and a spirit of fun and creativity.
- A sense of purpose and a commitment to making a positive impact on the world.
- A sense of connection and a desire to build relationships and community.
- A sense of gratitude and appreciation for the opportunities and resources that enable you to learn and grow.
- A sense of wonder and awe at the beauty and complexity of the world.

## Confirm Prerequisites

Make sure you have the following installed on your machine:

```shell
brew install git
brew install gh
brew install docker
brew install --cask visual-studio-code
```

## Set your environment variables

```shell
export GITHOME=~/github
export GHUSER=bamr87
export GIT_REPO=$GHUSER.github.io
export ZREPO=$GITHOME/$GIT_REPO

echo $GITHOME # /Users/bamr87/github
echo $GHUSER # bamr87
echo $GIT_REPO # bamr87.github.io
echo $ZREPO # /Users/bamr87/github/bamr87.github.io
```

```shell
git config --global user.email "$GHUSER@users.noreply.github.com"
git config --global user.name "$GHUSER"
```

## Initialize your new github repository

[gh cli docs](https://cli.github.com/manual/)

```shell
cd ~
mkdir $GITHOME
cd $GITHOME
mkdir $GIT_REPO
cd $ZREPO
```

```shell
# If repo already exists
cd $ZREPO
gh repo clone $GHUSER/$GIT_REPO
```

```shell
# If new repo
cd $ZREPO
git init
echo "# Building new report from $ZREPO" >> README.md
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/$GHUSER/$GHUSER.github.io.git
git push -u origin main
```

## Checkpoint - Github Repo Initialized

```shell
# non-github.io version
gh repo create $GIT_REPO --public --source=. --remote=upstream
git remote add origin https://$GHUSER@github.com/$GHUSER/$GIT_REPO.git
```

## Initialize Jekyll - If New Repo

Install [jekyll](https://jekyllrb.com/docs/installation/)

```shell
cd $ZREPO
jekyll new ./ --force
bundle install
```

```shell
# If running MacOS
bundle add webrick
bundle install
```

```shell
jekyll serve
```

## Initialize Jekyll - If Existing Repo

```shell
cd $ZREPO
bundle update
bundle install
jekyll serve
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

![](../assets/images/about-profile.png)  

## Download your home

```shell
d=$(date +%Y-%m-%d)
echo "$d"
```

```shell
cd $ZREPO/_posts
wget -O $d-home.md https://raw.githubusercontent.com/bamr87/it-journey/master/home.md 
```

![](../assets/images/header_pages.png)  

