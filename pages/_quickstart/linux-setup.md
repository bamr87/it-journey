---
title: Linux Setup
author: null
layout: default
description: null
categories:
    - quickstart
    - machine-setup
slug: linux
lastmod: '2022-01-28T03:31:19.415Z'
draft: false
---

These are the steps to setup this jekyll site repository on a Mac. All the code snippets are to be run in the terminal.

## Base setup

- [Github CLI](https://cli.github.com/)
- [Ruby](https://www.ruby-lang.org/)
- [Jekyll](https://jekyllrb.com/)

### Install Github Command Line Interface

The Github CLI is a command line interface for the Github API. It is used to create and manage repositories. It is also used to create and manage issues and pull requests.

[apt install](https://github.com/cli/cli/blob/trunk/docs/install_linux.md#debian-ubuntu-linux-raspberry-pi-os-apt)

```bash
# Install Github CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/etc/apt/trusted.gpg.d/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/trusted.gpg.d/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
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

### Install Software Packages (optional)

Detailed instructions for installing software packages can be found in the [](/quickstart/linux/) section.

```bash
# Navigate to your home directory and clone the brewfile
cd ~
gh repo clone bamr87/apt ~/.apt
```


```bash
# Navigate into brew file repo and install packages
cd ~/.apt
apt bundle
apt bundle --file bundles/core/
```

### Install VS Code

VS Code is a text editor that integrates well with Github. It is a free and open source software editor.

[Install](https://code.visualstudio.com/docs/setup/linux#_debian-and-ubuntu-based-distributions)

```bash
#install VS Code via Homebrew
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg

```

Then update the package cache and install the package using:

```bash
sudo apt install apt-transport-https
sudo apt update
sudo apt install code # or code-insiders
```

Log into VS code using your github account by clicking on the Account icon on the bottom left of the VS code window.

## Jekyll & ruby Setup

[Detailed instructions](https://jekyllrb.com/docs/installation/ubuntu/)

### Install Ruby

Ruby is the programming language of choice for Jekyll, and also manages the dependencies for the Jekyll gem.

```bash
# Install Ruby
sudo apt-get install ruby-full build-essential zlib1g-dev
```

#### Add Ruby to PATH

After install, you need to add the executables to your PATH. Otherwise, you will not be able to run Ruby or Jekyll.

First check which terminal shell you are using:

```bash
echo $SHELL
```

```bash
# Add Ruby to your PATH if you're using Zsh
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Install Jekyll

Once Ruby is installed, you can install Jekyll. 
First exit the terminal and open a new terminal to initialize the new PATH variable.

```bash
# Install Jekyll and Bundler
gem install jekyll bundler
```

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
