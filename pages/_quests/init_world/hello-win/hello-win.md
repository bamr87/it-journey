---
Title: Init World - Win
Author: bamr87
Layout: post
permalink: /init-world/hello-win/
Keywords: init, world
Description: This is the init world.
Dependancies: null
lastmod: 2023-12-03T08:47:22.762Z
---
## Powershell

cheatsheet: <https://www.zerrouki.com/the-ps-cheatsheets/>

<https://docs.microsoft.com/en-us/windows/wsl/install-win10>
<https://docs.microsoft.com/en-us/windows/wsl/interop>

## run in Powershell as admin

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart -verb RunAs
```

## enable VM's

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

## Set wsl version

[wsl](https://docs.microsoft.com/nl-nl/windows/wsl/wsl2-kernel)

```powershell
wsl --set-default-version 2
```

## Install distro

<https://docs.microsoft.com/en-us/windows/wsl/install-manual>

Invoke-WebRequest -Uri <https://aka.ms/wsl-debian-gnulinux> -OutFile Debian.appx -UseBasicParsing
cd ~/Downloads
Add-AppxPackage .\Debian.appx

## Setup new user and password

<https://docs.microsoft.com/en-us/windows/wsl/user-support>

## Update Shell Override in Platformio

## Download/Install Apps

<https://docs.microsoft.com/en-us/windows/package-manager/>

winget <https://github.com/microsoft/winget-cli/releases>

# Core Universal OS Apps (Win/Linux/Mac)

[ShareX](https://getsharex.com/)
[GIMP](https://www.gimp.org/)
VS Code
Atom
Firefox
Chrome
Github
Google cloud
Google Drive
InkScape

# Google Cloud SDK

```powershell
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")

& $env:Temp\GoogleCloudSDKInstaller.exe
```
