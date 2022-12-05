---
title: Windows Setup
author: null
layout: default
description: null
categories:
  - machine-setup
slug: windows
lastmod: 2022-08-06T17:38:11.496Z
draft: false
---

These are the steps to setup this jekyll site repository on a Windows PC. All the code snippets are to be run in the Powershell terminal.

## Base setup

- Windows Developer Enabled
- Winget Package Manager
- Github CLI
- Ruby
- Jekyll

## Windows Developer Settings

![](/assets/images/windows-developer-settings.png)

![](/assets/images/windows-developer-settings-powershell.png)

### Install Winget

Winget is a package manager for Windows and is developed and maintained [here](https://github.com/microsoft/winget-cli).

Downloadable msi files can be found [here](https://github.com/microsoft/winget-cli/releases).

[Install docs](https://docs.microsoft.com/en-us/windows/package-manager/winget/)

You can directly download the msi file from the following link:

https://github.com/microsoft/winget-cli/releases/download/v1.1.12653/Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle

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

confirm that you have installed Winget by running the following command:

```powershell
# Confirm Winget installation
winget -v
```

### Install Github Command Line Interface

The Github CLI is a command line interface for the Github API. It is used to create and manage repositories. It is also used to create and manage issues and pull requests.

```powershell
# Install Github CLI
winget install git.git
winget install GitHub.cli
```

Reload the shell

Confirm that you have installed the Github Command Line Interface by running the following command:

```powershell
# Confirm Github CLI installation
gh -v
```

Login to gh cli using your github credentials

```powershell
# Login to gh cli
gh auth login
```

Find your User ID in the [github emails settings](https://github.com/settings/emails)
more info [here ](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address)

```powershell
$GIT_ID = Read-Host "What is your Github ID?"
$GIT_USER_NAME = Read-Host "What is your Github User Name?"
git config --global user.name "$GIT_ID+$GIT_USER_NAME@users.noreply.github.com"
git config --global user.email "$GIT_ID+$GIT_USER_NAME@users.noreply.github.com"
```

### Install Software Packages (optional)

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

#### Windows Terminal

##### Oh-My-Posh

[OMP](https://ohmyposh.dev/docs/installation/windows)

##### Nerd Fonts

[Nerd fonts git repo](https://github.com/ryanoasis/nerd-fonts#option-3-install-script)



#### Windows Sub Linus


Download Ubuntu

```powershell
Invoke-WebRequest -Uri https://aka.ms/wslubuntu2004 -OutFile Ubuntu.appx -UseBasicParsing
wsl --set-default-version 2
```
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

#### Docker

Windows Instructions [wsl](https://docs.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)

[Docker Instructions](https://docs.docker.com/desktop/install/windows-install/)



### Install VS Code

VS Code is a text editor that integrates well with Github. It is a free and open source software editor.

```powershell
#install VS Code via Winget
winget install Microsoft.VisualStudioCode
```

Log into VS code using your github account by clicking on the Account icon on the bottom left of the VS code window.

#### Install VS Code extensions (optional)

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

## Jekyll & ruby Setup

[Detailed instructions](https://jekyllrb.com/docs/installation/windows/)

[Github Pages Dependancies](https://pages.github.com/versions/)

### Install Ruby

Ruby is the programming language of choice for Jekyll, and also manages the dependencies for the Jekyll gem.

```powershell
# Install Ruby
winget install RubyInstallerTeam.RubyWithDevKit
```

If this doesn't work, download the MSI file and install manually.

[Ruby Downloads](https://rubyinstaller.org/downloads/)

exit the shell

### Install Jekyll

Once Ruby is installed, you can install Jekyll.
First exit the terminal and open a new terminal to initialize the new PATH variable.

```powershell
# Install Jekyll and Bundler
gem install bundler jekyll
```

Restart your terminal

### Verify that Jekyll is installed

```powershell
# Verify Jekyll is installed
jekyll --version
```

## Fork Github Repository

Now you can fork the repository from Github and start working on it.

```powershell
# Navigate to your home directory, create a github folder, and fork the github repo
cd ~
mkdir github
cd github
gh repo fork bamr87/it-journey
```

## Install Dependencies

Once the repo is installed, you can install the dependencies for the Jekyll gem.

```powershell
# Navigate to your github repo and install dependancies
cd ~/github/it-journey
bundle install
```

## Build Jekyll site

To build the Jekyll site, you need to run the following command:

```powershell
# Build Jekyll site
jekyll build
```

## Start Site locally

To start the site locally, you need to run the following command:

```powershell
# Start Jekyll site locally
jekyll serve
```
