---
title: dual boot win linux
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
lastmod: '2022-03-07T00:48:22.406Z'
---


## VS Code install

```shell
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg
```

```shell
sudo apt install apt-transport-https
sudo apt update
sudo apt install code # or code-insiders

```
