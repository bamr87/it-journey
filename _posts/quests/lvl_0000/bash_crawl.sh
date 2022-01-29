#!/bin/bash

echo "Let's bash crawl"
read -p "Do you want to play Bash Crawl? yes or no `echo $'\n>'`" parm1
read -rep $'Do you know how to nano? yes or no  \n' parm2
if [[ $parm1 == "no" ]]; then
    #statements
    echo "umm you said $parm1"
    exit
  elif [[ $parm1 == "yes" && $parm2 == "yes" ]]; then
    sleep 2
    #statements
    nano bash_crawl.sh
    echo 'installing bash crawl now...'
  else
    echo "wrong answer"
  fi
exit

git clone https://gitlab.com/slackermedia/bashcrawl.git
