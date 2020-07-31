# zer0

Box Breathing

## deploy_0S
  ### win https://docs.microsoft.com/en-us/windows/

  net_boot

  https://docs.microsoft.com/en-us/windows/deployment/configure-a-pxe-server-to-load-windows-pe


  prereq
  deploy_comp: win_comp app_win_adk
    `C:\Users\amrab\OneDrive\dev\deploy_0s`
      adksetup - master file
      adkwinpesetup - PE - preinstallation addon
  A DHCP server: A DHCP server or DHCP proxy configured to respond to PXE client requests is required.
  A PXE server: A server running the TFTP service that can host Windows PE boot files that the client will download.
  A file server: A server hosting a network file share.

      - Package managers
        - PowerShell
          - Winget
            - https://github.com/microsoft/winget-cli
          - NuGet
            - https://docs.microsoft.com/en-us/nuget/what-is-nuget
          - CHocolaty
            - https://chocolatey.org/docs/installation
            - @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command " [System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
        - MSI
        - EXE

### mac
  #### Homebrew
  Install
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
  uninstall
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall.sh)"



  #### atom
    apm install
      platformio-ide-terminal
      language-markdown
      language-latex
      latextools
      markdown-writer
      markdown-preview-enhanced
      atom-html-preview
      atom-beautify
      linter
      linter-ui-default
      pandoc-convert
      minimap
      minimap-highlight-selected
      highlight-selected
      pigments
      sync-settings
        gist id = 8ed47b23068717ccfd1f7745b4dede8b



## Install Toolbelts - TB

**SPM** "Software Package Managers"

//#homebrew_00

### SDK's
Python

###
**ADE**
  _Atom_ - <https://atom.io/>

    ::: [Homebrew]
        *#brew-ade*
    :::



tesseract


  _Git_

  _Latex_

  _Pandoc_
  https://pandoc.org/index.html

_Terminal_

        https://medium.com/@sahanarajasekar/5-ways-to-upgrade-your-terminal-2fb8ab447949

      iTerm

      Zsh

      OMZsh



#### ADE

    - Miktex
    - Atom

Networking
wireshark

## Full Stack Attack - FSA
