echo 'hi this is your profile speaking'
$continue = Read-Host 'continue?:' 										#https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/read-host?view=powershell-7.1
#TODO: convert into a function

#Here's my build

$computerInfo = Get-ComputerInfo
Write-Host 																#Convert into list, formatting?
"
	Computer Name: 			$($computerInfo.CsDNSHostName) or $($env:computername) or $($computerInfo.CsCaption)
	Arch:				$($computerInfo.OsArchitecture)
	OS:				$($computerInfo.OsName)
	version:			$($computerInfo.OsVersion)
	PowerShell version:		$($PSVersionTable.PSVersion)"

if ($continue -eq 'no') { 												#TODO: build into a loop and Function
	echo "Ok boss"

	exit
}
elseif ($continue -eq 'yes') {
	echo 'loading profile...'
}
else {
	echo 'invalid input'
	exit
}

# Remote SSH connections https://code.visualstudio.com/blogs/2019/07/25/remote-ssh

echo 'Code on?'

$continue = Read-Host 'on?:' 											#https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/read-host?view=powershell-7.1
$PS_Repo = ""

if ($continue -eq 'on') { 												#TODO: build into a loop and Function
	echo "rock $continue"
	#Stop-Service -Name "I don't know"									#Stop service by name - https://winaero.com/stop-service-windows-10/
	#taskkill /IM "anuacui.exe" /F										#End task by name - https://winaero.com/kill-process-windows-10/
	open ""
}
elseif ($continue -eq 'off') {
	echo "ok, goof $continue then"
}
else {
	echo 'invalid input'
	exit
}

Push-Location $PSScriptRoot

Get-ChildItem ps*.ps1 | ForEach-Object {. $_.FullName}

function prompt {
    $uiTitle = $PWD | Convert-Path | Split-Path -Leaf
    $Host.UI.RawUI.WindowTitle = $uiTitle
    Write-Host "`n$env:USERNAME" -ForegroundColor Green -NoNewline
    if (Test-Administrator) {
        Write-Host " as " -NoNewline
        Write-Host "Administrator" -ForegroundColor Red -NoNewline
        $Host.UI.RawUI.WindowTitle = $uiTitle + " (Administrator)"
    }
    Write-Host " at " -NoNewline
    Write-Host $env:COMPUTERNAME -ForegroundColor Magenta -NoNewline
    Write-Host " in " -NoNewline
    Write-Host $ExecutionContext.SessionState.Path.CurrentLocation -ForegroundColor Cyan
    return "PS $('>' * ($NestedPromptLevel + 1)) "
}

Pop-Location

$PROFILE_EXISTS = Test-Path $Profile									# Check profile exists
$PROFILE_EXISTS =[System.Convert]::ToString($PROFILE_EXISTS)			# Convert bool to string

echo "The path PROFILE_EXISTS is $PROFILE_EXISTS "

Start-Sleep -s 1

echo "now setting your UI settings" #PS UI settings
sleep 1
$Shell = $Host.UI.RawUI
$size = $Shell.WindowSize
$size.width=90
$size.height=40
$Shell.WindowSize = $size

$size = $Shell.BufferSize
$size.width=90
$size.height=5000
$Shell.BufferSize = $size


# Fetch list of apps


echo "checking apps" # Create list of installed apps
#TODO: add list maker function

#Gig Hub CLI path
$gh_path = (Get-Command -CommandType application gh).Path
echo $gh_path

$app_installed = (Get-Command -CommandType Application).Name
# foreach ()

#TODO: build dependancy function https://docs.microsoft.com/en-us/powershell/scripting/learn/ps101/09-functions?view=powershell-7.1
function Check-Ver {
	$PSVersionTable.PSVersion
}
# Display version
Check-Ver
#Add Winget

#add go - prereq gh cli

# winget install -e --id Golang.Go-Unstable 		# https://golang.org/doc/install
# winget install -e --id ChristianSchenk.MiKTeX  	# Latex Editor
# winget install github.cli 						# Add Github CLI
# winget install git.git							# Add Git

# gh repo clone bamr87/it-journey

#Add VS Code

$wg_vs = 'Microsoft.VisualStudioCode'
winget list -q $wg_vs

# winget install -e --id $wg_vs
# winget install -e --id Git.Git
# winget install -e --id StrawberryPerl.StrawberryPerl

# VS Code Extensions
# code --install-extension ms-vscode.powershell
# code --install-extension ms-python.python
# code --install-extension James-Yu.latex-workshop #LaTeX Workshop

# code --install-extension GitHub.vscode-pull-request-github # https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github
# Install-Module -Name posh-git

# https://code.visualstudio.com/docs/editor/command-line

#TODO: add atom


#check Sync-Settings installed

$atom_app = 'Sync-Settings'

$atom_ver = apm ls | Select-String -Pattern $atom_app
$app_installed = $atom_ver | %{$_ -match $atom_app}
if ($app_installed -contains $True) {
	Write-Host "$atom_app installed"
	echo $atom_ver
} else {
	Write-Host "installing $atom_app"
	apm install $atom_app
}


#Set gist token and id


$file = Get-Content $HOME\.atom\config.cson
$containsWord = $file | %{$_ -match "gistId"}
if ($containsWord -contains $true) {
    Write-Host "There is!"
} else {
    Write-Host "Adding ID and Token..."
	# add insert logic
}


#TODO: add application checking

#TODO: add winget install

#adding dependanct Microsoft.VCLibs.x64.14.00.Desktop.appx if needed
# Add-AppxPackage https://aka.ms/Microsoft.VCLibs.x64.14.00.Desktop.appx

set-Alias -Name np -Value "C:\Program Files\Notepad++\notepad++.exe"

#psdoc and cheats

$pscheats = 'https://www.comparitech.com/net-admin/powershell-cheat-sheet/'
$psdoc = 'https://docs.microsoft.com/en-us/powershell/scripting/overview?view=powershell-7.1'
start $psdoc

echo 'Opening up your profile'
start-sleep -seconds 5
code $profile

# https://code.visualstudio.com/blogs/2019/09/03/wsl2
