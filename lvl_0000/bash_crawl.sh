#!/bin/bash

echo "Let's bash crawl"
read -p "launch Bar Crawl? yes or no" parm1
if [parm1 = "yes"]
  then
    echo 'you said $parm1 '
    echo 'bye'
  fi
exit

git clone https://gitlab.com/slackermedia/bashcrawl.git
