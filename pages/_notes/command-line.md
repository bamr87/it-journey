---
title: Shell and the CLI
description: Command Line Interface Notes
permalink: /notes/shell
lastmod: '2022-01-05T00:55:02.209Z'
---

# Command Line

## bash

```bash
echo "hello world"
cd ~
```

## powershell

[operators](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators?view=powershell-7.1)

[sub-expression](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators?view=powershell-7.1#subexpression-operator--)

```powershell
write-host "hello world"
```

```powershell
"Today is $(Get-Date)"
```

> Today is 12/02/2019 13:15:20

## github cli

To create a clone of your fork, use the --clone flag.

```cmd
$gh_repo = "bamr87/it-journey"
gh repo fork $gh_repo --clone=true
```

wmic 
/output:C:\Temp\list.txt product get name, version
exit

```powershell

Set-ExecutionPolicy Unrestricted -Scope CurrentUser -Force

Install-Script -Name Get-RemoteProgram

cd ~\OneDrive\dev\os\win

Export-StartLayout -UseDesktopApplicationID -Path layout.xml

```
