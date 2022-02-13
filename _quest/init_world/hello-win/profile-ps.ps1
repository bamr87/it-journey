# To create a new "Current user, Windows PowerShell ISE" profile, run this command:

if (!(Test-Path -Path $PROFILE ))
{ New-Item -Type File -Path $PROFILE -Force }

# To create a new "All users, Windows PowerShell ISE" profile, run this command:

if (!(Test-Path -Path $PROFILE.AllUsersCurrentHost))
{ New-Item -Type File -Path $PROFILE.AllUsersCurrentHost -Force }

# To create a new "Current user, All Hosts" profile, run this command:

if (!(Test-Path -Path $PROFILE.CurrentUserAllHosts))
{ New-Item -Type File -Path $PROFILE.CurrentUserAllHosts -Force }

# To create a new "All users, All Hosts" profile, type:

if (!(Test-Path -Path $PROFILE.AllUsersAllHosts))
{ New-Item -Type File -Path $PROFILE.AllUsersAllHosts -Force }

https://docs.microsoft.com/en-us/powershell/scripting/windows-powershell/ise/object-model/the-iseoptions-object?view=powershell-7.1
