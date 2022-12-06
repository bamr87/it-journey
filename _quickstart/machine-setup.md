---
title: Master Setup
author: null
layout: default
description: null
categories:
  - machine-setup
slug: /home/
lastmod: '2022-05-21T20:45:39.643Z'
draft: false
---

# Master Setup Overview

Before you can begin developing, your machine (computer) needs to be configured and loaded with the necessary software. Regardless of the OS you are using (Windows, Mac, Linux), there are specific components required. Detailed instructions based on your OS are provided, and can be accessed from the left side bar. 

## Core setup

- [Software Package Manager](#software-package-manager)
- [Github CLI](https://cli.github.com/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Ruby](https://www.ruby-lang.org/en/)
- [Jekyll](https://jekyllrb.com/)


Core Apps

- Source Code Control (Git, GitHub CLI)
- Integrated Development Environment (VS Code)
- Archiver/compressor (7zip)
- Screen Capture (ShareX)
- File Transfer Utility (Filezilla)

### Software Package Manager

A [package manager](https://en.wikipedia.org/wiki/Package_manager) is a software that allows you to install, upgrade, remove other software packages on your computer in a consistent manner. With a package manager, you can easily maintain and track your collection of software packages required for use, but also install any other packages that are dependant in order to function.

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

Most people are familiar with downloading and installing software from a website the manual way. However, there are a few things that can be done with the package manager that can make it easier and automatic. For instance, you can install a package with a single command (i.e. `brew cask install visual-studio-code`), or you can install multiple packages at once.

This repository has 2 submodules that contain files for installing different collections of software. You can find the files in the `\homebrew` or `\winget` directory.

If the directories are empty, run the following command to fetch the submodules:

```shell
git submodule update --init
```

Detailed instructions for installing software packages can be found in the [Brewfile](/quickstart/machine-setup/mac/#install-software-packages-optional) section for Mac, or the [Winget](/quickstart/machine-setup/windows/#install-software-packages-optional) section for Windows.

[Homebrew packages](/quickstart/homebrew/)

Packages are grouped into the following categories:



Development Tools

- Programming Languages 
  - Python
  - Perl
  - .NET
  - Node.js
  - Ruby
  - MikTex
- Databases
  - MySQL
  - PostgreSQL
  - MongoDB
  - Redis
- 

Graphic Design Software

Music Software

Web 


### Install VS Code

VS Code is a text editor that integrates well with Github. It is a free and open source software editor.

```bash
#install VS Code via Homebrew
brew cask install visual-studio-code
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
