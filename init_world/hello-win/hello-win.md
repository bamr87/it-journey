
#dependancies

#Powershell

cheatsheet: https://www.zerrouki.com/the-ps-cheatsheets/

https://docs.microsoft.com/en-us/windows/wsl/install-win10
https://docs.microsoft.com/en-us/windows/wsl/interop
## run in Powershell as admin

dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart -verb RunAs

## enable VM's
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

## Set wsl version
https://docs.microsoft.com/nl-nl/windows/wsl/wsl2-kernel
wsl --set-default-version 2

## Install distro
https://docs.microsoft.com/en-us/windows/wsl/install-manual

Invoke-WebRequest -Uri https://aka.ms/wsl-debian-gnulinux -OutFile Debian.appx -UseBasicParsing
cd ~/Downloads
Add-AppxPackage .\Debian.appx

## Setup new user and password
https://docs.microsoft.com/en-us/windows/wsl/user-support

## Update Shell Override in Platformio

## Download/Install Apps

https://docs.microsoft.com/en-us/windows/package-manager/

winget https://github.com/microsoft/winget-cli/releases

# Univeral OS Apps
Share X
GIMP
atom
firefox
Github
gcloud
gdrive
inkscape
