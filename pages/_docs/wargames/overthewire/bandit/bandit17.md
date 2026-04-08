---
title: Bandit17
description: 'Level Goal

  ----------

  The credentials for the next level can be retrieved by submitting the

  password of the current level to a port on localhost in the range

  31000 to 32000. First find out which of these ports have a server

  listening on them. Then fi...'
permalink: /docs/wargames/bandit/bandit17/
date: '2026-04-07T01:41:08.000Z'
lastmod: '2026-04-07T01:41:08.000Z'
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/bandit/bandit17.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Level Goal
----------
The credentials for the next level can be retrieved by submitting the
password of the current level to **a port on localhost in the range
31000 to 32000**. First find out which of these ports have a server
listening on them. Then find out which of those speak SSL/TLS and which
don't. There is only 1 server that will give the next credentials, the
others will simply send back to you whatever you send to it.

 **Helpful note: Getting "DONE", "RENEGOTIATING" or "KEYUPDATE"? Read the
"CONNECTED COMMANDS" section in the manpage.**

Commands you may need to solve this level
-----------------------------------------
ssh, telnet, nc, ncat, socat, openssl, s\_client, nmap, netstat, ss

Helpful Reading Material
------------------------
- [Port scanner on Wikipedia][]

[Port scanner on Wikipedia]: https://en.wikipedia.org/wiki/Port_scanner
