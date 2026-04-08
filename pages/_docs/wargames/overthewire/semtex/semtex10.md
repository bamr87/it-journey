---
title: Semtex10
description: 'Hacking szene

  -------------

  Thanks to zaphod and Mush for finding a bugs in this level'
permalink: /docs/wargames/semtex/semtex10/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/semtex/semtex10.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Hacking szene
-------------
**Thanks to zaphod and Mush for finding a bugs in this level**

Do you know these hacking movies where they push some buttons, then
the evil hacker script window turns up and a percentage bar is
showing how far the password cracking has gone?


    0%....10%....20%....30%....40%....50%....60%....70%....80%....90%....100%
    password cracked!

Ever wanted to do it yourself? Here is your chance.\

This level implements a weakness in the authentication scheme used
by M$ win95 and win98 for the netbios shares.

There is a TCP daemon on brebera port 24019. It authenticates your
password. Once you send the correct password, it echoes it back.
Well, let the source speak for itself. As far as brute force may
take you, a little brain is never bad :P Perhaps you have heard of
pqwak?


