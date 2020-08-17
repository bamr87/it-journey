_Terminal Upgrade_

1. Get iTerm
fratures:
  - split pane
  - easier search (it highlights all the words),
  - better mouse text selection support,
  - more customizable.

Download it here: https://www.iterm2.com/version3.html

2. Shortcuts:

   - Ctrl + A Go to the beginning of the line you are currently typing on
   - Ctrl + E Go to the end of the line you are currently typing on
   - Ctrl + R Lets you search through previously used commands
   -      Ctrl + W Delete the word before the cursor
(iTerm only) Move through tabs right: Cmd + → and left: Cmd + ←
(iTerm only) Move through panes next: Cmd + ] and previous: Cmd + [

Setup iTerm’s system-wide hotkey to open window from anywhere:
In iTerm preferences, click on the “Keys” tab. In the bottom left, under “Hotkey”, check “Show/hide iTerm with a system-wide hotkey” and assign the hotkey you’d like to use.
Enable word jump: In iTerm preferences, click on the “Keys” tab, add new Key Mapping.
Keybord shortcut: option + → | Action: Send Escape Sequence | Esc+: f
Keybord shortcut: option + ← | Action: Send Escape Sequence | Esc+: b
3. Upgrade your shell
When you launch the terminal it will always run with a program inside it to communicate with the computer, this is called the shell. On OS X, the default shell is Bash. If your terminal is using Bash you should see -bash or /bin/bash when you type “echo $SHELL” in the terminal.
Zsh is another type of shell for your terminal. Zsh has a ton of cool features -that may seem small but they can really increase your efficiency in the terminal.
Hit tab repeatedly to cycle through autocomplete options
Image for post
Hit tab to use path expansion
Image for post
Hit tab to finish a command using substring command history search
Image for post
Maintain a shared command history between tabs
Image for post
Keep your volume on for this command! ;)
Create custom layouts (keep reading for more on this)
Let’s install it! First, you will need to download Homebrew, which makes downloading new packages on OS X much easier.
Install homebrew:
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
Install zsh:
brew install zsh zsh-completions
To get all the great tools zsh has to offer we will be using oh-my-zsh, a nicely packaged zsh framework.
Install oh-my-zsh:
curl -L https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh | sh
Open a new tab and give it a try. If you like it, make zsh your default shell:
chsh -s /bin/zsh
Now try “echo $SHELL” again — you should see -zsh or /bin/zsh.
4. Make your terminal look more “you”
With zsh installed, you may have noticed that your terminal looks a little different. Oh-my-zsh has a ton of themes to choose from here. You can use themes to show information that’s important to you in the terminal like time, git branch, file path, etc.
Image for post
Some of the themes to choose from
Once you find a theme that you like, set ZSH_THEME to the name of the theme in your ~/.zshrc.
ZSH_THEME="avit"
Customizing your theme further is pretty easy. You can find all the theme files under~/.oh-my-zsh/themes/ — duplicate a theme that you like, rename it, and make any changes.
To add emojis to your command prompt, open up your custom theme file in a text editor and use “alt+command+T” to open up the special character library. Add emojis in the PROMPT line of your custom theme file. Protip: add a space after each emoji so they don’t overlap.
Image for post
5. Use aliases
Aliases are shortcuts or abbreviations for commands you type in the terminal. They can save you time if you repeatedly use certain long commands.
To set up aliases, create a file ~/.aliases:
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
Oh-my-zsh installs many git aliases. Open up a new tab/window and give your aliases a try.
