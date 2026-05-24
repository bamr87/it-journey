---
title: 'Dual Boot Windows and Linux: Setup Guide'
author: bamr87
excerpt: A step-by-step guide to setting up a dual boot system with Windows and Linux, including partitioning and bootloader configuration.
description: Learn how to configure a dual boot environment with Windows and Linux, including installing VS Code on Linux and managing the bootloader for seamless switching.
snippet: null
categories:
- System Administration
tags:
- dual-boot
- windows
- linux
- bootloader
- setup
keywords:
- dual boot windows linux
- install linux alongside windows
- linux windows bootloader
- ubuntu windows dual boot
- dual boot setup guide
meta: null
draft: true
lastmod: '2022-03-07T00:48:22.000Z'
section: System Administration
date: '2021-09-21T13:25:50.000Z'
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
