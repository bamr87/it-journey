#!/bin/bash

echo "Let's bash crawl"
read -p "Do you want to play Bash Crawl? yes or no `echo $'\n>'`" parm1
read -rep $'Do you know how to nano? yes or no  \n' parm2

if [[ $parm1 == "no" ]]; then
    echo "umm you said $parm1"
    exit 0
elif [[ $parm1 == "yes" && $parm2 == "yes" ]]; then
    sleep 2
    echo 'installing bash crawl now...'
    
    if [ ! -d "bashcrawl" ]; then
        git clone https://github.com/bamr87/bashcrawl.git
    else
        echo "bashcrawl already installed."
    fi
    
    cd bashcrawl || exit 1
    chmod +x entrance.sh
    ./entrance.sh
else
    echo "wrong answer"
    exit 1
fi
