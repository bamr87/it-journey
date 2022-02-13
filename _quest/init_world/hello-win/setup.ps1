# Install Chocolatey
Try
{
  choco --version
  $chocolateyInstalled=$True
}
catch
{
  $chocolateyInstalled=$False
}

if($chocolateyInstalled)
{
  Write-Host "Update Chocolatey"
  choco upgrade chocolatey
}
else
{
  Write-Host "Install Chocolatey"
  Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}

# Windows Settings
Write-Host "Power and Sleep adjusted to never"
Powercfg /Change -monitor-timeout-ac 0
Powercfg /Change -standby-timeout-ac 0

# Browsers
choco install -y googlechrome firefox
choco install -y adblockplus-firefox

# Comms
choco install -y discord slack

# Media
choco install -y spotify vlc

# Apps
choco install -y qbittorrent
choco install -y vscode
choco install -y figma

# Utils
choco install -y 7zip 
choco install -y teamviewer
choco install -y teracopy
choco install -y imgburn
choco install -y adobereader
choco install -y lightshot
choco install -y handbrake
choco install -y treesizefree
choco install -y therenamer
choco install -y sharpkeys
choco install -y powertoys

# Network
choco install -y wireshark
choco install -y angryip
choco install -y putty

# Runtimes
choco install -y silverlight
choco install -y adobeair

# Dev
choco install -y hyper
choco install -y git.install
choco install -y nodejs.install
choco install -y yarn
choco install -y epicgameslauncher
choco install -y unity

# System
choco install -y geforce-experience 

# VS Code Plugins
refreshenv
# TODO Fetch from Mac-setup repo instead
echo "Installing vscode themes and plugins"
code --install-extension monokai.theme-monokai-pro-vscode
code --install-extension alexanderte.dainty-vscode
code --install-extension dracula-theme.theme-dracula
code --install-extension pkief.material-icon-theme
## Extensions
code --install-extension alefragnani.project-manager
code --install-extension aliariff.auto-add-brackets
code --install-extension apollographql.vscode-apollo
code --install-extension burkeholland.react-food-truck
code --install-extension burkeholland.simple-react-snippets
code --install-extension capaj.vscode-exports-autocomplete
code --install-extension christian-kohler.npm-intellisense
code --install-extension christian-kohler.path-intellisense
code --install-extension CoenraadS.bracket-pair-colorizer
code --install-extension dbaeumer.vscode-eslint
code --install-extension dsznajder.es7-react-js-snippets
code --install-extension eamodio.gitlens
code --install-extension eg2.vscode-npm-script
code --install-extension eriklynd.json-tools
code --install-extension esbenp.prettier-vscode
code --install-extension formulahendry.auto-close-tag
code --install-extension formulahendry.auto-rename-tag
code --install-extension jpoissonnier.vscode-styled-components
code --install-extension kumar-harsh.graphql-for-vscode
code --install-extension mgmcdermott.vscode-language-babel
code --install-extension Prisma.vscode-graphql
code --install-extension streetsidesoftware.code-spell-checker
code --install-extension wix.vscode-import-cost
code --install-extension shyykoserhiy.vscode-spotify
