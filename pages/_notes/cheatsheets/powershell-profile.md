---
title: PowerShell Profile and Environment Setup
description: "Set persistent environment variables, sync your PowerShell profile from a GitHub gist, and reload the shell — the commands worth keeping close."
excerpt: Persistent environment variables, a profile synced from a GitHub gist, and the reload commands that go with them.
author: bamr87
date: '2021-11-07T17:20:34.000Z'
lastmod: '2026-08-22T00:00:00.000Z'
permalink: /notes/cheatsheets/powershell-profile/
categories:
  - notes
  - cheatsheets
tags:
  - powershell
  - windows
  - profile
  - environment-variables
  - shell
keywords:
  primary:
    - powershell profile
    - powershell environment variables
  secondary:
    - windows shell setup
    - powershell gist sync
draft: false
toc: true
---

Your PowerShell profile is the script that runs every time a session starts. Keeping it in a gist means a new machine is one download away from feeling like your own.

## Open PowerShell as administrator

```powershell
powershell -Command "Start-Process PowerShell -Verb RunAs"
```

## Persistent environment variables

`$env:NAME = 'value'` only lives as long as the session. To make a variable survive a restart, write it to the user's environment block.

```powershell
function Set-EnvVar {
  param($EnvName, $EnvValue)
  [System.Environment]::SetEnvironmentVariable($EnvName, $EnvValue, [System.EnvironmentVariableTarget]::User)
  $env:$EnvName = $EnvValue   # also set it for the session you are in
  Write-Host "Set $EnvName"
}

Set-EnvVar 'PSGIST' '<your-gist-id>'
```

Read it back with `$env:PSGIST`. The `User` target writes to the current account; use `Machine` for all users, which needs an elevated session.

| Target | Scope | Needs admin |
|---|---|---|
| `Process` | This session only | No |
| `User` | Current account, persists | No |
| `Machine` | Every account, persists | Yes |

## Where the profile lives

```powershell
$PROFILE                  # full path to the current host's profile
$PROFILE | Select-Object *  # every profile path PowerShell knows about
Split-Path $PROFILE | Set-Location
```

If the file does not exist yet, create it along with any missing folders.

```powershell
if (-not (Test-Path $PROFILE)) {
  New-Item -ItemType File -Path $PROFILE -Force
}
```

## Pull the profile from a gist

Keep the canonical profile in a gist, store its id in an environment variable, and fetch it on a new machine.

```powershell
function Get-GitProfile {
  $gitUser = 'bamr87'
  $masterProfile = 'Microsoft.PowerShell_profile.ps1'
  $url = "https://gist.githubusercontent.com/$gitUser/$env:PSGIST/raw/$masterProfile"
  Invoke-WebRequest -Uri $url -OutFile $PROFILE
  Write-Host "Profile written to $PROFILE"
}
```

`Invoke-WebRequest` replaces the older `New-Object System.Net.WebClient` pattern and reports failures as terminating errors you can catch.

## Reload after editing

```powershell
. $PROFILE          # re-run the profile in the current session
```

A full restart is sometimes cleaner, especially after changing environment variables.

```powershell
function Restart-Powershell {
  Start-Process powershell
  exit
}
```

## Execution policy

A downloaded profile will not run under the default policy on Windows. Allow local scripts while still requiring signatures on remote ones.

```powershell
Get-ExecutionPolicy -List
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## See also

- [PowerShell cheatsheet](/notes/cheatsheets/powershell/) — the broader command reference
- [Terminal shortcuts](/notes/cheatsheets/terminal-shortcuts/) — keyboard movement that works in most shells
