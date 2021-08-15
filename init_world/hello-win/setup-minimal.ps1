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
choco install -y googlechrome

# Media
choco install -y spotify vlc

# Utils
choco install -y 7zip 
choco install -y imgburn
choco install -y adobereader
choco install -y lightshot

# Runtimes
choco install -y silverlight
choco install -y adobeair