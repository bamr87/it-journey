---
title: Machine Setup
author: null
layout: default
description: null
categories:
    - quickstart
slug: machine-setup
lastmod: '2022-01-12T20:23:25.494Z'
draft: false
---

# Machine Setup Overview

Before you can begin developing, your machine (computer) needs to be configured and loaded with the necessary software. Regardless of the OS you are using (Windows, Mac, Linux), there are specific components required. Detailed instructions based on your OS are provided, and can be accessed from the left side bar. 

## Base setup

- [Software Package Manager](#software-package-manager)
- [Github CLI](https://cli.github.com/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Ruby](https://www.ruby-lang.org/en/)
- [Jekyll](https://jekyllrb.com/)

### Software Package Manager

A [package manager](https://en.wikipedia.org/wiki/Package_manager) is a software that allows you to install, upgrade, remove other software packages on your computer in a consistent manner. With a package manager, you can easily maintain and track your collection of software packages required for use, but also install any other packages that are dependant in order to function.

Often, a package is just a particular program. On the other hand, it is common for programs to consist of several interrelated packages. For instance, the gimp image editor consists not only of the gimp package, but also of the gimp-data package; in addition, several optional add-on packages (containing esoteric data, documentation, and so on) are also available. It is also possible for several small, related programs to be contained in a single package: for instance, the fileutils package contains several common Unix commands, such as ls, cp, etc.

If a package A conflicts with another package B, then the two packages cannot be installed at the same time. For instance, fb-music-hi conflicts with fb-music-low because they provide alternate sets of music for the game Frozen Bubble.

The job of a package manager is to present an interface which assists the user in managing the collection of packages installed on his or her system.

**MacOS**

- [Homebrew](https://docs.brew.sh/Installation) is a package manager for macOS.

**Windows**

- [Winget](https://docs.microsoft.com/en-us/windows/package-manager/winget/) - is a package manager for Windows.
- [Chocolaty](https://chocolatey.org/)
- [Nuget](https://www.nuget.org/) - .NET Package manager

**Linux**

- [APT](https://en.wikipedia.org/wiki/APT_(software)) -Debian/Ubuntu
- [YUM](https://en.wikipedia.org/wiki/Yum_(software)) - Fedora
- [RPM](https://en.wikipedia.org/wiki/RPM_Package_Manager) - Redhat/CentOS

Click on the links below to navigate to the detailed instructions:

- [Install Homebrew](/quickstart/machine-setup/mac/#install-homebrew)
- [Install Winget](/quickstart/machine-setup/windows/#install-winget)

### Github Command Line Interface

The Github CLI is a command line interface for the Github API. It is used to create and manage repositories. It is also used to create and manage issues and pull requests.

[Link to install Github CLI](/quickstart/github/#install-github-cli)

### Install Software Packages (optional)

Detailed instructions for installing software packages can be found in the [Brewfile](/quickstart/homebrew/) section.

```bash
# Navigate to your home directory and clone the brewfile
cd ~
gh repo clone bamr87/brewfile ~/.brew

# Navigate into brew file repo and install packages
cd ~/.brew
brew bundle
brew bundle --file bundles/core/
```

### Install VS Code

VS Code is a text editor that integrates well with Github. It is a free and open source software editor.

```bash
#install VS Code via Homebrew
brew cask install visual-studio-code
```

Log into VS code using your github account by clicking on the Account icon on the bottom left of the VS code window.

#### Install VS Code extensions (optional)



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
echo 'export PATH="$HOME/.gem/ruby/3.3.0/bin:$PATH"' >> ~/.zshrc
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
# Navigate to your github repo and install dependancies
cd ~/github/it-journey
bundle install
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
