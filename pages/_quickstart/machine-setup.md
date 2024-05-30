---
title: Machine Setup
author: bamr87
description: A guide to setting up your machine for Jekyll development.
excerpt: A guide to setting up your machine for Jekyll development.
layout: default
keywords:
  - machine setup
  - jekyll
  - ruby
  - github
  - visual studio code
  - homebrew
  - winget
  - apt
lastmod: 2024-05-30T22:34:02.510Z
draft: true
slug: machine-setup
---

Before you can begin developing, your machine (computer) needs to be configured and loaded with the necessary software and dependencies.
Each OS (Windows, Mac, Linux) will have its own method to download and install software based on the technology stack you're working with.
In this guide, we will focus on how to build a Minimal Viable Product (MVP) to prep your machine to create a Static Website Generator using Jekyll.

## Core Setup Overview

For this guide, we will be using the following tools:

- [Software Package Manager](#software-package-manager)
  - Retrieves your applications/libraries/code through a trusted repository
    - winget (Windows)
    - Homebrew (Mac)
    - APT (Linux)
- [Source Code Repository](#source-code-repository)
  - The place where your code is stored and managed
    - [Github](https://github.com)
    - [Github CLI](https://cli.github.com/)
      - The command line tool to interact with Github repos
- Integrated Development Environment (IDE)
  - [Visual Studio Code](https://code.visualstudio.com/)
  - The best integrated development environment for beginners to advanced programmers
- Programming Languages
  - [Ruby](https://www.ruby-lang.org/en/)
    - The programming language and framework used by Jekyll and Github pages
  - [Python](https://www.python.org/)
    - A programming language used for various tasks
  - [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
    - The programming language used for web development
  - [liquid](https://shopify.github.io/liquid/)
    - The templating language used by Jekyll

### Software Package Manager

A [package manager](https://en.wikipedia.org/wiki/Package_manager) is a software that allows you to install, upgrade, remove other software packages on your computer in a consistent manner. With a package manager, you can easily maintain and track your collection of software packages required for use, but also install any other packages that are dependant in order to function.

The job of a package manager is to present an interface which assists the user in managing the collection of packages installed on his or her system.

**MacOS**

The most popular package manager for MacOS is Homebrew. Homebrew is a package manager for macOS. It simplifies the installation of software on the Mac operating system. It is a free and open-source software package management system that simplifies the installation of software on Apple's macOS operating system.

[Install docs](https://docs.brew.sh/Installation)

- [Homebrew](https://docs.brew.sh/Installation) is a package manager for macOS.

For more information, visit the [Homebrew website](https://brew.sh/).

```zsh
# Install Homebrew
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

confirm that you have installed Homebrew by running the following command:

```bash
# Confirm Homebrew installation
brew -v
```

**Windows**

the most popular package manager for Windows is Winget. Winget is a package manager for Windows. It is a command-line tool that allows you to install, update, and manage software packages on your Windows machine. Winget is a package manager for Windows that allows you to install, update, and manage software packages from the command line.

for more information, visit the [Winget website](https://docs.microsoft.com/en-us/windows/package-manager/winget/).

- [Winget](https://docs.microsoft.com/en-us/windows/package-manager/winget/) - is a package manager for Windows.

**Linux**

Depending on the distribution of Linux you are using, you will have a different package manager. Some of the most popular package managers for Linux are:

- [APT](https://en.wikipedia.org/wiki/APT_(software)) -Debian/Ubuntu
- [YUM](https://en.wikipedia.org/wiki/Yum_(software)) - Fedora
- [RPM](https://en.wikipedia.org/wiki/RPM_Package_Manager) - Redhat/CentOS

### Source Code Repository

A source code repository is a file archive and web hosting facility where a large amount of source code, for software or for web pages, is kept, either publicly or privately. They are often used by open-source projects and other multi-developer projects to maintain and manage the source code.

- [Git](https://git-scm.com/) is a distributed version control system for tracking changes in source code during software development. It is designed for coordinating work among programmers, but it can be used to track changes in any set of files.
- [Github](https://github.com) is a web-based platform that uses Git for version control. It is a repository hosting service that provides a web-based graphical interface and access control for repositories. It is commonly used for code. It offers all of the distributed version control and source code management (SCM) functionality of Git as well as adding its own features.
- [Github CLI](https://cli.github.com/) is a command line interface for the Github API. It is used to create and manage repositories. It is also used to create and manage issues and pull requests.

### git installation

to install git on your machine, you can use the following commands:

**MacOS**

```shell
# Install git via Homebrew
brew install git
```

**Windows**

```shell
# Install git via Winget
winget install git.git
```

**Linux**

```shell
# Install git via APT
sudo apt install git
```

[Detailed instructions](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)

### git configuration

Find your User ID in the [github emails settings](https://github.com/settings/emails)
more info [here ](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address)

```powershell
$GIT_ID = Read-Host "What is your Github ID?"
$GIT_USER_NAME = Read-Host "What is your Github User Name?"
git config --global user.name "$GIT_USER_NAME@users.noreply.github.com"
git config --global user.email "$GIT_ID+$GIT_USER_NAME@users.noreply.github.com"
```

```bash
echo 'What is your Github ID?'
read GIT_ID
echo 'What is your Github User Name?'
read GIT_USER_NAME
git config --global user.name "$
git config --global user.email "$
```

### Github Command Line Interface

to install the Github CLI on your machine, you can use the following commands:

**MacOS**

```shell
# Install Github CLI via Homebrew
brew install gh
```

**Windows**

```shell
# Install Github CLI via Winget
winget install GitHub.cli
```

**Linux**

```shell
# Install Github CLI via APT
sudo apt install gh
```

[apt install](https://github.com/cli/cli/blob/trunk/docs/install_linux.md#debian-ubuntu-linux-raspberry-pi-os-apt)

The Github CLI is a command line interface for the Github API. It is used to create and manage repositories. It is also used to create and manage issues and pull requests.

```bash
# Install Github CLI the hard way
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

Most people are familiar with downloading and installing software from a website the manual way. However, there are a few things that can be done with the package manager that can make it easier and automatic. For instance, you can install a package with a single command (i.e. `brew cask install visual-studio-code`), or you can install multiple packages at once.

This repository has 2 submodules that contain files for installing different collections of software. You can find the files in the `\homebrew` or `\winget` directory.

To add submodules to your repository, run the following command:

```shell
git submodule add https://github.com/bamr87/homebrew.git submodules/homebrew
git submodule add https://github.com/bamr87/winget-packages submodules/winget
```

If the directories are empty, run the following command to fetch the submodules:

```shell
git submodule update --init
```

to pull the latest changes from the submodule, run the following command:

```shell
git submodule update --remote
```

***Mac***

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

```

***Linux***

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

***windows***

For a list of packages you can download/install using winget, see [here](https://winget.run/)

For a list of package bundles, see [here](https://winstall.app/)

Detailed instructions for installing software packages can be found in the [Winget](/quickstart/winget/) section.

```powershell
# Navigate to your home directory and clone the winget packages
cd ~
gh repo clone bamr87/winget-packages .winget
```

```powershell
# Navigate into winget file repo and install packages
cd ~/.winget
winget import --import-file winget-app-core.json
winget import --import-file winget-app-dev.json
```

Here's a recommended list of VS Code extensions to install:

```
aaron-bond.better-comments
DavidAnson.vscode-markdownlint
eliostruyf.vscode-front-matter
esbenp.prettier-vscode
Gruntfuggly.todo-tree
James-Yu.latex-workshop
leodevbro.blockman
mdickin.markdown-shortcuts
ms-azuretools.vscode-docker
ms-dotnettools.csharp
ms-kubernetes-tools.vscode-kubernetes-tools
ms-python.python
ms-python.vscode-pylance
ms-toolsai.jupyter
ms-toolsai.jupyter-keymap
ms-toolsai.jupyter-renderers
ms-vscode-remote.remote-containers
ms-vscode-remote.remote-wsl
ms-vscode.powershell
ms-vsliveshare.vsliveshare
ms-vsliveshare.vsliveshare-audio
ms-vsliveshare.vsliveshare-pack
redhat.vscode-xml
redhat.vscode-yaml
sissel.shopify-liquid
streetsidesoftware.code-spell-checker
syler.sass-indented
TakumiI.markdowntable
tchayen.markdown-links
telesoho.vscode-markdown-paste-image
yzhang.markdown-all-in-one
```

[source](https://code.visualstudio.com/docs/editor/extension-marketplace#_command-line-extension-management)

[Iterating over file to install extensions](https://stackoverflow.com/questions/58513266/how-to-install-multiple-extensions-in-vscode-using-command-line/62403267#62403267)

```powershell
cd ~/github/it-journey/_quickstart
Get-Content extensions.txt | ForEach-Object {code --install-extension $_}
```

### Install VS Code

VS Code is a text editor that integrates well with Github. It is a free and open source software editor.

***Mac***

```shell
#install VS Code via Homebrew
brew cask install visual-studio-code
```
[Detailed instructions - Mac](https://jekyllrb.com/docs/installation/macos/)

***windows***

```shell
#install VS Code via Winget
winget install Microsoft.VisualStudioCode
```

[Detailed instructions - Windows](https://jekyllrb.com/docs/installation/windows/)

***Linux***

[Detailed instructions - Linux](https://code.visualstudio.com/docs/setup/linux#_debian-and-ubuntu-based-distributions)

```shell
#install VS Code via APT
sudo apt install code
```

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

### Install Ruby

Ruby is the programming language of choice for Jekyll, and also manages the dependencies for the Jekyll gem.

***Mac***

```shell
# Install Ruby
brew install ruby@2.7
```

***windows***

```powershell
# Install Ruby (version 2.7 for github pages)
winget install RubyInstallerTeam.RubyWithDevKit.2.7 -v 2.7.4-1
```

If this doesn't work, download the MSI file and install manually.

[Ruby Downloads](https://rubyinstaller.org/downloads/)


***Linux***

```shell
# Install Ruby via APT
sudo apt-get install ruby-full build-essential zlib1g-dev
```

```bash
# Add Ruby to your PATH if you're using Zsh
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Add Ruby to PATH (Mac and Linux)

Ah, the `$PATH` variable in Linux and MacOS – it's like the wise old map of a seasoned explorer! This variable is crucial because it tells your system where to look for the executable files (those little adventurers that actually run your commands) when you type a command in the terminal.

Imagine you're in a vast library (your computer) looking for a specific book (a program, like `python` or `git`). Now, if this library had no organization, you'd be wandering around forever! That's where `$PATH` comes in – it's like a magical index telling you exactly in which aisles (directories) to look for your book (executable file).

When you type a command, the system checks each directory listed in your `$PATH` variable, in the order they're listed. If it finds the executable file in one of these directories, voilà! The command runs. If not, it's like hitting a dead end in a maze, and you get an error saying the command wasn't found.

You can see your current `$PATH` by typing `echo $PATH` in the terminal. It shows a list of paths, separated by colons. You can add new paths to it, ensuring that your system knows about more places to look for your programs.

Just remember, with great power comes great responsibility. Modify the `$PATH` wisely, or you might lead your system into a labyrinth of confusion!

After install, you need to add the executables to your PATH. Otherwise, you will not be able to run Ruby or Jekyll.

First check which terminal shell you are using:

```bash
echo $SHELL
```

Add new PATH to ruby 2.7 by inserting into your profile

```shell
# This tells your system where to look for the executable files and where the gems are located

export PATH="/usr/local/opt/ruby/bin:/usr/local/opt/ruby@2.7/bin:/usr/local/lib/ruby/gems/2.7.0/bin:$PATH"
export PATH=/usr/local/opt/ruby@2.7/bin:$PATH
export PATH=`gem environment gemdir`/bin:$PATH
```

```bash
# Add Ruby to your PATH if you're using Zsh
echo 'export PATH="/usr/local/opt/ruby/bin:/usr/local/lib/ruby/gems/2.7.4/bin:$PATH"' >> ~/.zshrc
echo 'export PATH=`gem environment gemdir`/bin:$PATH' >> ~/.zshrc
```


```bash
# Add Ruby to your PATH If you're using Bash
echo 'export PATH="/usr/local/opt/ruby/bin:/usr/local/lib/ruby/gems/2.7.4/bin:$PATH"' >> ~/.bash_profile
```

After install, you need to add the executables to your PATH. Otherwise, you will not be able to run Ruby or Jekyll.

First check which terminal shell you are using:

```shell
echo $SHELL
```

```zsh
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

```shell
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

```shell
# Verify Jekyll is installed
jekyll --version
```

## Fork Github Repository

Now you can fork the repository from Github and start working on it.

```shell
# Navigate to your home directory, create a github folder, and fork the github repo
cd ~
mkdir github
cd github
gh repo fork bamr87/it-journey
```

If you want to clone the repository to your local machine, you can run the following command:

```shell
# Clone the repository to your local machine
gh repo clone bamr87/it-journey
```

## Install Dependencies

Once the repo is installed, you can install the dependencies for the Jekyll gem.

```shell
# Navigate to your github repo and install dependencies
cd ~/github/it-journey
bundle install
```

## Build Jekyll site

To build the Jekyll site, you need to run the following command:

```shell
# Build Jekyll site
jekyll build
```

## Start Site locally

To start the site locally, you need to run the following command:

```shell
# Start Jekyll site locally
jekyll serve
```

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

### Set SDKROOT (only macOS Catalina or later)

```bash
export SDKROOT=$(xcrun --show-sdk-path)
```

## Windows Developer Settings (Windows 10 only)

Update your OS settings to allow shell scripts to execute and to install winget (if applicable). Without this setting, you may run into issues later on.

![dev settings](/assets/gif/windows-developer-settings.gif)

NOTE: This change opens up a lot of security vualnerabilities so proceed with caution.

### Install Winget (Windows 10 only)

Winget is a package manager for Windows and is developed and maintained [here](https://github.com/microsoft/winget-cli).

Downloadable msi files can be found [here](https://github.com/microsoft/winget-cli/releases).

[Install docs](https://docs.microsoft.com/en-us/windows/package-manager/winget/)

You can directly download the msi file from the following link:

[Winget install](https://github.com/microsoft/winget-cli/releases/download/v1.1.12653/Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle)

Or you can run the following commands in Powershell to download the msi file:

```powershell
# Navigate to the directory where the msi file will be installed
cd ~
$download_folder = ".winget"
mkdir $download_folder
cd $download_folder
```

```powershell
# Download installation package

$version = "v1.1.12653"
$url = "https://github.com/microsoft/winget-cli/releases/download/$version/Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle"
$FileName = Split-Path $url -Leaf
$FullPath = "$pwd\$FileName"

$webclient = New-Object System.Net.WebClient
$webclient.DownloadFile($url, $FullPath)

echo "Saved $FileName"
```

Open installation file

```powershell
ii $FullPath
```

Silent Install Option

```powershell
msiexec /i $FullPath /qn /norestart
```

### Iterm2

```shell
brew install iterm2

$ sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

```

### Windows Terminal

#### Oh-My-Posh

[OMP](https://ohmyposh.dev/docs/installation/windows)

#### Nerd Fonts

[Nerd fonts git repo](https://github.com/ryanoasis/nerd-fonts#option-3-install-script)

### Windows Sub Linux

[install docs](https://learn.microsoft.com/en-us/windows/wsl/install)

Download Ubuntu

```powershell
Invoke-WebRequest -Uri https://aka.ms/wslubuntu2004 -OutFile Ubuntu.appx -UseBasicParsing
wsl --set-default-version 2
```

dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

### Docker

Windows Instructions [wsl](https://docs.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)

[Docker Instructions](https://docs.docker.com/desktop/install/windows-install/)
