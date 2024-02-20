---
title: Windows Sub-linux Setup
author: null
excerpt: null
description: null
snippet: null
categories:
  - posts
tags:
  - article
meta: null
draft: true
lastmod: 2022-05-21T23:56:40.448Z
---

If wsl is installed 

```powershell
wsl --install
wsl --update

```powershell
Invoke-WebRequest -Uri https://aka.ms/wslubuntu2004 -OutFile Ubuntu.appx -UseBasicParsing
wsl --set-default-version 2
```
