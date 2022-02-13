# _Terminal Upgrade_

 # Shortcuts:

 # Nav
   echo " opt + Arrow - Go to end of the word"
   echo " cmd + Arrow - Go to end of the line"
   echo " fn + delete the word before the cursor"
   echo " cmd + \` - switch between windows"
   echo " cmd + tab - Switch between apps"
   echo " crtl + L - Select whole line"
   echo " command + >> to add to file"

Echo "Upgrade your shell"

echo $SHELL "is your terminal."

## Dependancies
#Homebrew:

brew install zsh zsh-completions

#To get all the great tools zsh has to offer we will be using oh-my-zsh, a nicely packaged zsh framework.

Echo "Install oh-my-zsh"

sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

#Make zsh your default shell:
chsh -s /bin/zsh

echo $SHELL "again — you should see zsh or /bin/zsh"

# 4. Make your terminal look more “you”

Set ZSH_THEME to the name of the theme in your ~/.zshrc.
ZSH_THEME="avit"

theme files under~/.oh-my-zsh/themes/

5. Use aliases
Aliases are shortcuts or abbreviations for commands you type in the terminal.

To set up aliases,
create a file ~/.aliases:

# vim [https://vim.rtorr.com/]
# vi ~/.aliases
touch ~/.aliases

#Add command shortcuts in ~/.aliases:

Echo "I sed add this line"
echo "alias alitest=\"echo it worked\"" >> .aliases
echo "alias ls='ls -GlaF'" >> .aliases
echo "alias home='cd ~'" >> .aliases
# If you already use bash aliases, you can easily transfer those over to zsh by coping them over to ~/.aliases.

# In ~/.zshrc add aliases to your source

echo "source \$HOME/.aliases" >> ~/.zshrc
