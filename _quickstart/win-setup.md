---
title: Windows Setup
author: null
layout: default
description: null
categories:
    - quickstart
    - machine-setup
slug: windows
lastmod: '2022-01-05T00:38:08.407Z'
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

### Install Software Packages (optional)

Detailed instructions for installing software packages can be found in the [Winget](/quickstart/winget/) section.

```powershell
# Navigate to your home directory and clone the winget packages
cd ~
gh repo clone bamr87/winget-packages .winget
```

```powershell
# Navigate into brew file repo and install packages
cd ~/.winget
winget import --import-file winget-app-core.json
winget import --import-file winget-app-dev.json
```

### Install VS Code

VS Code is a text editor that integrates well with Github. It is a free and open source software editor.

```powershell
#install VS Code via Winget
winget install Microsoft.VisualStudioCode
```

Log into VS code using your github account by clicking on the Account icon on the bottom left of the VS code window.

## Jekyll & ruby Setup

[Detailed instructions](https://jekyllrb.com/docs/installation/windows/)

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
