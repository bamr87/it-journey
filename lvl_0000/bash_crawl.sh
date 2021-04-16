#!/bin/bash

echo "Let's bash crawl"
read -p "launch Bar Crawl? yes or no `echo $'\n>'`" parm1
read -rep $'launch Bar Crawl? yes or no  \n' parm2
if [[ $parm1 == "yes" ]]; then
    echo "you said $parm1"
    sleep 2
    echo 'installing bash crawl now...'
    echo $parm1
  elif [[ $parm1 == "no" ]]; then
    #statements
    echo "umm you said $parm1"
  else
    echo "wrong answer"
  fi
exit

git clone https://gitlab.com/slackermedia/bashcrawl.git
