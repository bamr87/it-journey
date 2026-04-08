---
title: Leviathan
description: 'Leviathan is a wargame that has been rescued from the demise of

  intruded.net, previously hosted on leviathan.intruded.net. Big

  thanks to adc, morla and reth for their help in resurrecting this

  game!'
permalink: /docs/wargames/leviathan/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/leviathan/index.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Leviathan
=========

### Dare you face the lord of the oceans?

Leviathan is a wargame that has been rescued from the demise of
**intruded.net**, previously hosted on leviathan.intruded.net. **Big
thanks to adc, morla and reth** for their help in resurrecting this
game!

What follows below is the original description of leviathan, copied from
intruded.net:

    Summary:
    Difficulty:     1/10
    Levels:         8
    Platform:   Linux/x86

    Author:
    Anders Tonfeldt

    Special Thanks:
    We would like to thank AstroMonk for coming up with a replacement idea for the last level,
    deadfood for finding a leveljump and Coi for finding a non-planned vulnerability.

    Description:
    This wargame doesn't require any knowledge about programming - just a bit of common
    sense and some knowledge about basic *nix commands. We had no idea that it'd be this
    hard to make an interesting wargame that wouldn't require programming abilities from 
    the players. Hopefully we made an interesting challenge for the new ones.

Leviathan's levels are called **leviathan0, leviathan1, ... etc.** and
can be accessed on **leviathan.labs.overthewire.org** through SSH on port 2223.

To login to the first level use:

    Username: leviathan0
    Password: leviathan0

Data for the levels can be found in **the homedirectories**. You can look
at **/etc/leviathan_pass** for the various level passwords.

Tools you may find useful to solve this wargame
-----------------------------------------------

strings, hexdump, objdump, ghidra
