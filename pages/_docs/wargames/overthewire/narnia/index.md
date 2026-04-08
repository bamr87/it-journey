---
title: Narnia
description: 'Narnia is a wargame that has been rescued from the demise of

  intruded.net, previously hosted on narnia.intruded.net. Big thanks

  to adc, morla and reth for their help in resurrecting this game!'
permalink: /docs/wargames/narnia/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/narnia/index.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Narnia
======

### We all have to start somewhere.

Narnia is a wargame that has been rescued from the demise of
**intruded.net**, previously hosted on narnia.intruded.net. **Big thanks
to adc, morla and reth** for their help in resurrecting this game!

What follows below is the original description of narnia, copied from
intruded.net:

    Summary:
    Difficulty:     2/10
    Levels:         10
    Platform:   Linux/x86

    Author:
    nite

    Special Thanks:
    lx_jakal for pointing out a bug that made a level easier =)

    Description:
    This wargame is for the ones that want to learn basic exploitation. You can see the most
    common bugs in this game and we've tried to make them easy to exploit. You'll get the
    source code of each level to make it easier for you to spot the vuln and abuse it. The
    difficulty of the game is somewhere between Leviathan and Behemoth, but some of the
    levels could be quite tricky.

Narnia's levels are called **narnia0, narnia1, ... etc.** and can be
accessed on **narnia.labs.overthewire.org** through SSH on port 2226.

To login to the first level use:

    Username: narnia0
    Password: narnia0

Data for the levels can be found in **/narnia/**.

Tools you may find useful to solve this wargame
-----------------------------------------------

objdump, ghidra, pwntools, gcc, gdb
