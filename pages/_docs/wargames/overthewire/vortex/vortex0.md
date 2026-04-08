---
title: Vortex0
description: 'Level Goal

  ----------

  Your goal is to connect to port 5842 on vortex.labs.overthewire.org

  and read in 4 unsigned integers in host byte order. Add these

  integers together and send back the results to get a username and

  password for vortex1. This infor...'
permalink: /docs/wargames/vortex/vortex0/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/vortex/vortex0.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Level Goal
----------
Your goal is to connect to port 5842 on vortex.labs.overthewire.org
and read in 4 unsigned integers in host byte order. Add these
integers together and send back the results to get a username and
password for vortex1. This information can be used to log in using
SSH.

**Note:** vortex is on an 32bit x86 machine (meaning, a little endian
architecture)

Helpful Reading Material
------------------------
- [C Programming Introduction][]
- [Network Programming Tutorial][]

  [C Programming Introduction]: http://beej.us/guide/bgc/
  [Network Programming Tutorial]: http://beej.us/guide/bgnet/
