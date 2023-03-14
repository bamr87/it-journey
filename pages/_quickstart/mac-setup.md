---
title: Mac Setup
author: null
layout: default
description: null
categories:
    - machine-setup
slug: mac
lastmod: '2022-02-14T03:08:28.573Z'
draft: false
---

These are the steps to setup this jekyll site repository on a Mac. All the code snippets are to be run in the terminal.

## Base setup

- Apple [Xcode](https://developer.apple.com/xcode/) Command Line Tools
- [Homebrew](https://brew.sh/) Package Manager
- [Github CLI](https://cli.github.com/)
- [Ruby](https://www.ruby-lang.org/)
- [Jekyll](https://jekyllrb.com/)

### Install Xcode Command Line Tools

Homebrew requires Xcode Command Line Tools to be installed if Xcode is not already installed.

Open the Terminal (Command + Space) and run the following command:

```zsh
xcode-select --install
```

Confirm that you have installed Xcode Command Line Tools by running the following command:

```zsh
xcode-select -p
```

### Install Homebrew

Homebrew is a package manager for macOS. It is a fork of the original Homebrew package manager for Linux, and is developed and maintained by [Homebrew](https://brew.sh/).

[Install docs](https://docs.brew.sh/Installation)

```zsh
# Install Homebrew
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

confirm that you have installed Homebrew by running the following command:

```bash
# Confirm Homebrew installation
brew -v
```

### Install Github Command Line Interface

The Github CLI is a command line interface for the Github API. It is used to create and manage repositories. It is also used to create and manage issues and pull requests.

```bash
# Install Github CLI
brew install gh
```

Confirm that you have installed the Github Command Line Interface by running the following command:

```bash
# Confirm Github CLI installation
gh --version
```

Login to gh cli using your github credentials

```bash
# Login to gh cli
gh auth login
```

Find your User ID in the [github emails settings](https://github.com/settings/emails)
more info [here ](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address)

```bash
echo 'What is your Github ID?' 
read GIT_ID
echo 'What is your Github User Name?'
read GIT_USER_NAME
git config --global user.name "$GIT_ID+$GIT_USER_NAME@users.noreply.github.com"
git config --global user.email "$GIT_ID+$GIT_USER_NAME@users.noreply.github.com"
```

### Install Software Packages (optional)

Detailed instructions for installing software packages can be found in the [Brewfile](/quickstart/homebrew/) section.

```bash
# Navigate to your home directory and clone the brewfile
cd ~
gh repo clone bamr87/brewfile ~/.brew
```


```bash
# Navigate into brew file repo and install packages
cd ~/.brew
brew bundle
brew bundle --file bundles/core/
```

Or install individually using a loop

```shell
# Include init_world/hello-mac/hb-packages.sh
mkdir _quest/init_world/hello-mac/
ln ../_quest/init_world/hello-mac/hb-packages.sh _quest/init_world/hello-mac/hb-packages.sh

{% include_relative /_quest/init_world/hello-mac/hb-packages.sh %}
```

### Install VS Code

VS Code is a text editor that integrates well with Github. It is a free and open source software editor.

```bash
#install VS Code via Homebrew
brew install cask visual-studio-code
```

Log into VS code using your github account by clicking on the Account icon on the bottom left of the VS code window.

## Jekyll & ruby Setup

[Detailed instructions](https://jekyllrb.com/docs/installation/macos/)

### Set SDKROOT (only macOS Catalina or later)

```bash
export SDKROOT=$(xcrun --show-sdk-path)
```

### Install Ruby

Ruby is the programming language of choice for Jekyll, and also manages the dependencies for the Jekyll gem.

```bash
# Install Ruby
brew install ruby
```

#### Add Ruby to PATH

After install, you need to add the executables to your PATH. Otherwise, you will not be able to run Ruby or Jekyll.

First check which terminal shell you are using:

```bash
echo $SHELL
```

```bash
# Add Ruby to your PATH if you're using Zsh
echo 'export PATH="/usr/local/opt/ruby/bin:/usr/local/lib/ruby/gems/3.0.0/bin:$PATH"' >> ~/.zshrc
```


```bash
# Add Ruby to your PATH If you're using Bash
echo 'export PATH="/usr/local/opt/ruby/bin:/usr/local/lib/ruby/gems/3.0.0/bin:$PATH"' >> ~/.bash_profile
```

### Install Jekyll

Once Ruby is installed, you can install Jekyll. 
First exit the terminal and open a new terminal to initialize the new PATH variable.

```bash
# Install Jekyll and Bundler
gem install --user-install bundler jekyll
```

### Append the Jekyll Gem your path file

First get the ruby version using:

```bash
# Get Ruby version
ruby -v
```


Replace X.X.0 with the version of ruby you just installed

```bash
# Add path to zshrc profile
echo 'export PATH="$HOME/.gem/ruby/3.0.0/bin:$PATH"' >> ~/.zshrc
```


```bash
# Add to your .bash_profile
echo 'export PATH="$HOME/.gem/ruby/3.0.0/bin:$PATH"' >> ~/.bash_profile
```

Restart your terminal

### Verify that Jekyll is installed

```bash
# Verify Jekyll is installed
jekyll --version
```

## Fork Github Repository

Now you can fork the repository from Github and start working on it.

```bash
# Navigate to your home directory, create a github folder, and fork the github repo
cd ~
mkdir github
cd github
gh repo fork bamr87/it-journey
```

## Install Dependencies

Once the repo is installed, you can install the dependencies for the Jekyll gem.

```bash
# Navigate to your github repo and install dependencies
cd ~/github/it-journey
bundle install
bundle update
```

## Build Jekyll site

To build the Jekyll site, you need to run the following command:

```bash
# Build Jekyll site
jekyll build
```

## Start Site locally

To start the site locally, you need to run the following command:

```bash
# Start Jekyll site locally
jekyll serve
```

## Iterm2

```shell
brew install iterm2

$ sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

```
