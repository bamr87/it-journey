---
title: Bandit14
description: 'Level Goal

  ----------

  The password for the next level is stored in

  /etc/bandit\pass/bandit14 and can only be read by user

  bandit14. For this level, you don''t get the next password, but you

  get a private SSH key that can be used to log into the next l...'
permalink: /docs/wargames/bandit/bandit14/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/bandit/bandit14.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Level Goal
----------
The password for the next level is stored in
**/etc/bandit\_pass/bandit14 and can only be read by user
bandit14**. For this level, you don't get the next password, but you
get a private SSH key that can be used to log into the next level.
Look at the commands that logged you into previous bandit levels,
and find out how to use the key for this level.

Commands you may need to solve this level
-----------------------------------------
ssh, scp, umask, chmod, cat, nc, install

Helpful Reading Material
------------------------
- [SSH/OpenSSH/Keys][]

[SSH/OpenSSH/Keys]: https://help.ubuntu.com/community/SSH/OpenSSH/Keys
