---
title: Semtex0
description: 'Get a shell

  -----------

  semtex.labs.overthewire.org'
permalink: /docs/wargames/semtex/semtex0/
date: '2026-04-07T01:41:09.000Z'
lastmod: '2026-04-07T01:41:09.000Z'
categories:
- wargames
tags:
- security
- wargames
- linux
- ctf
- cybersecurity
toc_sticky: true
source_repo: https://github.com/OverTheWireOrg/OverTheWire-website
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/semtex/semtex0.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Get a shell
-----------
semtex.labs.overthewire.org

| x86/elf:    | Connect to port 24000 |
| amd64/elf:  | Connect to port 24001 |
| ppc/mach-O: | Connect to port 24002 |


Receive data until the port is closed.

Every second byte you receive is trash, ignore it.
The other bytes are an executable that shows you the password.

Then login to [semtex1@semtex.labs.overthewire.org][] on port 2229

**Thanks to mrx for the amd64 and ppc binaries!**

Reading Material
----------------
- [Beej's guide to network programming][]

[semtex1@semtex.labs.overthewire.org]: ssh://semtex1@semtex.labs.overthewire.org:2229
[Beej's guide to network programming]: http://beej.us/guide/bgnet/
