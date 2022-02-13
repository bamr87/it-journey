#!/bin/bash
echo "Hello Brew! Lets intall some crap"
read -p 'Install or Uninstall? ' parm1
if [ $parm1 = 'Install']
  then
    echo '$parm1 now...'
    exit
  else
    exit
brew $parm1 --cask atom \
 google-chrome \
 google-drive-file-stream \
 firefox \
 onedrive \
 alfred \
 iterm2 \
 google-cloud-sdk \
 inkscape \
 sonic-pi \
 postman \
 awscli \
 visual-studio-code
brew $parm1 wget \
 bash-completion \
 zsh \
 node \
 rdesktop \
 irssi \
 gh \
 tree \
 nmap \
 powershell \

fi
