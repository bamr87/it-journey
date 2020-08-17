
https://docs.microsoft.com/en-us/windows/wsl/install-win10

## run in Powershell as admin

dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart -verb RunAs

## enable VM's
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

## Set wsl version
wsl --set-default-version 2
