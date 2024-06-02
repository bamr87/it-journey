#!/bin/bash
# Get specific hardware and software information for Macs

system_profiler SPHardwareDataType | awk '/Model Name:|Model Identifier:|Model Number:|Chip:|System Firmware Version:/ {print $0}'
system_profiler SPSoftwareDataType | awk '/System Version:|Kernel Version:/ {print $0}'

# install and update prerequisites
brew install git
brew install gh
brew install docker
brew install --cask visual-studio-code
# Or use the following to set the environment variables

export GITHOME=~/github
export GHUSER=bamr87
export GIT_REPO=zer0-mistakes
export ZREPO=$GITHOME/$GIT_REPO

# Confirm the environment variables by echoing them

echo $GITHOME # /Users/bamr87/github
echo $GHUSER # bamr87
echo $GIT_REPO # zer0-mistakes
echo $ZREPO # /Users/bamr87/github/zer0-mistakes
# Set your Git email and name to tag your commits

git config --global user.email "$GHUSER@users.noreply.github.com"
git config --global user.name "$GHUSER"
# If you didnt already set it in the previous step
# FIXME: quotes in comments dont work

echo "What is your Github ID?"
read GIT_ID

# Set your email using ID

git config --global user.email "$GIT_ID+$GHUSER@users.noreply.github.com"
# confirm your email

git config -l

# Initialize your github repository

gh repo create $GHUSER/$GIT_REPO --public
# Create your github home directory and repo

mkdir -p $ZREPO
# If new repo, initialize it

cd $ZREPO
git init
echo "# Building new report from $ZREPO" >> README.md
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/${GHUSER}/${GIT_REPO}.git
git push -u origin main

# Open your new github repository in the browser

open https://github.com/${GHUSER}/${GIT_REPO}

cd $ZREPO
jekyll new ./ --force
bundle install
# If running MacOS
bundle add webrick
bundle install
jekyll serve
cd $ZREPO
bundle update
bundle install
jekyll serve
code _config.yml
cd $ZREPO
wget https://raw.githubusercontent.com/bamr87/it-journey/master/favicon.ico
bundle lock --add-platform x86-mingw32 x64-mingw32 x86-mswin32 java
# find theme path
bundle info --path minima
JEKYLL_THEME=$(bundle info --path minima)
echo $JEKYLL_THEME
cd $JEKYLL_THEME

cp -aR $JEKYLL_THEME/* $ZREPO
bundle remove jekyll-theme-minima
#_config.yml
# Build settings
# theme: minima
plugins:
  - jekyll-feed
bundle remove minima --install
jekyll serve
{%- raw -%}
cd $ZREPO
mkdir _layout
cd _layout
echo "{{ content }}" >> default.html 
{% endraw %}
#tree #alias #zshrc #profile
alias tree="find . -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'"
echo alias tree="find . -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'" >> ~/.zshrc

tree
cd -
d=$(date +%Y-%m-%d)
echo "$d"
cd $ZREPO/_posts
wget -O $d-home.md https://raw.githubusercontent.com/bamr87/it-journey/master/home.md 
