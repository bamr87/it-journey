---
title: Bandit21
description: 'Level Goal

  ----------

  There is a setuid binary in the homedirectory that does the

  following: it makes a connection to localhost on the port you

  specify as a commandline argument. It then reads a line of text from

  the connection and compares it to the...'
permalink: /docs/wargames/bandit/bandit21/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/bandit/bandit21.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Level Goal
----------
There is a setuid binary in the homedirectory that does the
following: it makes a connection to localhost on the port you
specify as a commandline argument. It then reads a line of text from
the connection and compares it to the password in the previous level
(bandit20). If the password is correct, it will transmit the
password for the next level (bandit21).

 **NOTE:** Try connecting to your own network daemon to see if it
works as you think

Commands you may need to solve this level
-----------------------------------------
ssh, nc, cat, bash, screen, tmux, Unix 'job control' (bg, fg, jobs, &, CTRL-Z, ...)

