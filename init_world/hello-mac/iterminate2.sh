# _Terminal Upgrade_

2. Shortcuts:

   - Ctrl + A Go to the beginning of the line you are currently typing on
   - Ctrl + E Go to the end of the line you are currently typing on
   - Ctrl + R Lets you search through previously used commands
   -      Ctrl + W Delete the word before the cursor
(iTerm only) Move through tabs right: Cmd + → and left: Cmd + ←
(iTerm only) Move through panes next: Cmd + ] and previous: Cmd + [

3. Upgrade your shell

“echo $SHELL” in the terminal.

## Dependancies
Homebrew:

brew install zsh zsh-completions
To get all the great tools zsh has to offer we will be using oh-my-zsh, a nicely packaged zsh framework.

Install oh-my-zsh:

$ sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

Make zsh your default shell:
chsh -s /bin/zsh

“echo $SHELL” again — you should see -zsh or /bin/zsh.

4. Make your terminal look more “you”

Set ZSH_THEME to the name of the theme in your ~/.zshrc.
ZSH_THEME="avit"

theme files under~/.oh-my-zsh/themes/

5. Use aliases
Aliases are shortcuts or abbreviations for commands you type in the terminal.

To set up aliases,
create a file ~/.aliases:
vi ~/.aliases

Add command shortcuts in ~/.aliases:
alias alias_name="command_to_run"

If you already use bash aliases, you can easily transfer those over to zsh by coping them over to ~/.aliases.

In ~/.zshrc add:
source $HOME/.aliases

Bash and zsh can also share the same aliases. In ~/.bashrc add:
if [ -f ~/.aliases ]; then
   . ~/.aliases
fi
