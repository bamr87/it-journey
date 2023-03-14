#!/bin/bash
echo "Install Homebrew?"
read -p "yes or no " parm1
if [ $parm1 = 'yes']
  then
  #statements
  echo "then"

  #bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
  exit
else
  exit
fi

# ruby option
# /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# to uninstall
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall.sh)"
