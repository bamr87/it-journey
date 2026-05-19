---
title: Bandit24
description: 'Level Goal

  ----------

  A program is running automatically at regular intervals from

  cron, the time-based job scheduler. Look in /etc/cron.d/ for

  the configuration and see what command is being executed.'
permalink: /docs/wargames/bandit/bandit24/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/bandit/bandit24.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Level Goal
----------
A program is running automatically at regular intervals from
**cron**, the time-based job scheduler. Look in **/etc/cron.d/** for
the configuration and see what command is being executed.

 **NOTE:** This level requires you to create your own first
shell-script. This is a very big step and you should be proud of
yourself when you beat this level!

 **NOTE 2:** Keep in mind that your shell script is removed once
executed, so you may want to keep a copy around...

Commands you may need to solve this level
-----------------------------------------
chmod, cron, crontab, crontab(5) (use "man 5 crontab" to access this)

