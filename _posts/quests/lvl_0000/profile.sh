#!/bin/bash

echo "running the $0 script"
read -p 'see bin?' see_bin
if [[ $see_bin = "yes" ]]; then
  #statements
  myComandVar=$( ls /bin )
else
  echo "you said $see_bin"
fi

echo "This is my Bin: $myComandVar"
if [[ -d /usr/local/Caskroom/google-cloud-sdk ]]; then
  read -p 'Enter something here: ' parm1
  myVar=$parm1
  echo "$myVar is parameter 1"
  echo "$1 is parameter 2"
else
  echo "Google Cloud SDK is not installed!"
  #statements
fi
exit
